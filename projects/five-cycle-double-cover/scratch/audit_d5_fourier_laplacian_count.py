#!/usr/bin/env python3
"""Independent audit of a Fourier/Laplacian formula for D5 flows.

A D5 flow assigns a weight-two vector in the even-weight subspace of
F_2^5 to every edge and has xor zero at every vertex.  This script:

* checks the 16-entry Fourier table directly;
* compares a closed binary-Laplacian Gauss sum with direct enumeration;
* compares the resulting subset expansion with direct D5-flow counts on
  small simple and multigraph examples; and
* tests the tempting mod-3 nonvanishing criterion on the complete
  bridgeless cubic simple census produced by nauty-geng.

Only the Python standard library is used.  Loops and parallel edges are
represented by repeated pairs (u, v), with u == v for a loop.
"""

from __future__ import annotations

import argparse
import itertools
import shutil
import subprocess
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Iterator, Sequence


D5 = tuple((1 << i) | (1 << j) for i in range(5) for j in range(i + 1, 5))


@dataclass(frozen=True)
class Graph:
    order: int
    edges: tuple[tuple[int, int], ...]
    name: str = ""
    graph6: str | None = None


def q(value: int) -> int:
    """The complement-invariant quadratic form on F_2^5/<11111>.

    Values 0,...,15 are representatives whose fifth coordinate is zero.
    """

    weight = value.bit_count()
    return (weight * (weight - 1) // 2) & 1


def character(y: int, a: int) -> int:
    return -1 if (y & a).bit_count() & 1 else 1


def fourier_table() -> tuple[int, ...]:
    return tuple(sum(character(y, a) for a in D5) for y in range(16))


def expected_fourier_table() -> tuple[int, ...]:
    return tuple(2 * (-1 if q(y) else 1) + (8 if y == 0 else 0) for y in range(16))


def gf2_rank(rows: Sequence[int], columns: int) -> int:
    work = list(rows)
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(work)) if (work[row] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for row in range(rank + 1, len(work)):
            if (work[row] >> column) & 1:
                work[row] ^= work[rank]
        rank += 1
    return rank


def binary_laplacian(order: int, edges: Sequence[tuple[int, int]]) -> tuple[int, ...]:
    """Return rows of the multigraph Laplacian over F_2.

    A loop contributes zero.  Two parallel edges cancel, as required.
    """

    rows = [0] * order
    for u, v in edges:
        if u == v:
            continue
        bit_pair = (1 << u) | (1 << v)
        rows[u] ^= bit_pair
        rows[v] ^= bit_pair
    return tuple(rows)


def direct_gauss_sum(graph: Graph) -> int:
    total = 0
    for assignment in itertools.product(range(16), repeat=graph.order):
        exponent = 0
        for u, v in graph.edges:
            exponent ^= q(assignment[u] ^ assignment[v])
        total += -1 if exponent else 1
    return total


def closed_gauss_sum(graph: Graph) -> int:
    rank = gf2_rank(binary_laplacian(graph.order, graph.edges), graph.order)
    return (-1 if rank & 1 else 1) * (1 << (4 * graph.order - 2 * rank))


class DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, value: int) -> int:
        root = value
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[value] != value:
            value, self.parent[value] = self.parent[value], root
        return root

    def union(self, first: int, second: int) -> None:
        first = self.find(first)
        second = self.find(second)
        if first != second:
            self.parent[second] = first


def quotient_laplacian_data(graph: Graph, chosen_mask: int) -> tuple[int, int]:
    """Return (number of quotient vertices, binary Laplacian rank).

    Edges selected by ``chosen_mask`` impose equality and are contracted.
    Selected loops merely contribute their expansion coefficient.
    Unselected loops disappear from the quadratic exponent.
    """

    dsu = DisjointSet(graph.order)
    for index, (u, v) in enumerate(graph.edges):
        if (chosen_mask >> index) & 1 and u != v:
            dsu.union(u, v)

    roots = {}
    blocks = []
    for vertex in range(graph.order):
        root = dsu.find(vertex)
        if root not in roots:
            roots[root] = len(roots)
        blocks.append(roots[root])

    quotient_order = len(roots)
    rows = [0] * quotient_order
    for index, (u, v) in enumerate(graph.edges):
        if (chosen_mask >> index) & 1:
            continue
        a, b = blocks[u], blocks[v]
        if a == b:
            continue
        bit_pair = (1 << a) | (1 << b)
        rows[a] ^= bit_pair
        rows[b] ^= bit_pair
    return quotient_order, gf2_rank(rows, quotient_order)


def fourier_flow_count(graph: Graph) -> int:
    """Evaluate the exact Fourier expansion, as an integer."""

    total = 0
    for chosen_mask in range(1 << len(graph.edges)):
        quotient_order, rank = quotient_laplacian_data(graph, chosen_mask)
        sign = -1 if rank & 1 else 1
        total += (
            (4 ** chosen_mask.bit_count())
            * sign
            * (1 << (4 * quotient_order - 2 * rank))
        )
    numerator = (1 << len(graph.edges)) * total
    denominator = 1 << (4 * graph.order)
    assert numerator % denominator == 0
    return numerator // denominator


def signed_rank_sum(graph: Graph) -> int:
    return sum(
        -1 if quotient_laplacian_data(graph, mask)[1] & 1 else 1
        for mask in range(1 << len(graph.edges))
    )


def two_adic_valuation(value: int) -> int:
    if value == 0:
        raise ValueError("the 2-adic valuation of zero is infinite")
    return (abs(value) & -abs(value)).bit_length() - 1


def cubic_coefficient_profile(graph: Graph) -> dict[int, int]:
    """Group cubic-graph summands by d(F) = eta(F) + bicycle(H_F).

    The input is required to be connected and cubic.  The quotient H_F
    is then connected, so bicycle(H_F) = k(F) - 1 - rank(L_H_F).
    """

    if not is_connected(graph):
        raise ValueError("the cubic profile requires a connected graph")
    degrees = [0] * graph.order
    for u, v in graph.edges:
        if u == v:
            degrees[u] += 2
        else:
            degrees[u] += 1
            degrees[v] += 1
    if any(degree != 3 for degree in degrees):
        raise ValueError("the cubic profile requires degree three at every vertex")

    coefficients: Counter[int] = Counter()
    for mask in range(1 << len(graph.edges)):
        quotient_order, rank = quotient_laplacian_data(graph, mask)
        eta = mask.bit_count() - graph.order + quotient_order
        bicycle = quotient_order - 1 - rank
        assert eta >= 0
        assert bicycle >= 0
        coefficients[eta + bicycle] += -1 if rank & 1 else 1
    return dict(sorted(coefficients.items()))


def count_from_cubic_profile(graph: Graph, coefficients: dict[int, int]) -> int:
    """Use N_D = 2^(2-n/2) sum_d A_d 4^d."""

    polynomial_at_four = sum(
        coefficient * (4**degree) for degree, coefficient in coefficients.items()
    )
    denominator_exponent = graph.order // 2 - 2
    if denominator_exponent >= 0:
        denominator = 1 << denominator_exponent
        assert polynomial_at_four % denominator == 0
        return polynomial_at_four // denominator
    return polynomial_at_four << (-denominator_exponent)


def valuation_predictions(
    graph: Graph, coefficients: dict[int, int]
) -> tuple[int | None, int, int]:
    """Return (A_0 prediction, tropical profile prediction, exact v2).

    The first prediction retains only A_0.  The tropical prediction takes
    the least valuation among all nonzero grouped terms but ignores
    cancellation among groups tied at that least valuation.
    """

    base_exponent = 2 - graph.order // 2
    leading = coefficients.get(0, 0)
    leading_prediction = (
        None
        if leading == 0
        else base_exponent + two_adic_valuation(leading)
    )
    tropical_prediction = min(
        base_exponent + 2 * degree + two_adic_valuation(coefficient)
        for degree, coefficient in coefficients.items()
        if coefficient
    )
    exact = two_adic_valuation(count_from_cubic_profile(graph, coefficients))
    return leading_prediction, tropical_prediction, exact


def spanning_forest(graph: Graph) -> tuple[set[int], list[int], list[int | None]]:
    """Return tree-edge indices, a root-to-leaf order, and parents."""

    incident = [[] for _ in range(graph.order)]
    for edge_index, (u, v) in enumerate(graph.edges):
        if u == v:
            continue
        incident[u].append((v, edge_index))
        incident[v].append((u, edge_index))

    tree_edges: set[int] = set()
    order: list[int] = []
    parent: list[int | None] = [None] * graph.order
    seen = [False] * graph.order
    for root in range(graph.order):
        if seen[root]:
            continue
        seen[root] = True
        component_order = [root]
        for vertex in component_order:
            order.append(vertex)
            for other, edge_index in incident[vertex]:
                if seen[other]:
                    continue
                seen[other] = True
                parent[other] = edge_index
                tree_edges.add(edge_index)
                component_order.append(other)
    return tree_edges, order, parent


def direct_flow_count(graph: Graph) -> int:
    """Enumerate cotree labels and force tree labels from the leaves."""

    tree_edges, order, parent_edge = spanning_forest(graph)
    cotree_edges = [i for i in range(len(graph.edges)) if i not in tree_edges]
    count = 0

    for free_labels in itertools.product(D5, repeat=len(cotree_edges)):
        labels = [0] * len(graph.edges)
        for edge_index, label in zip(cotree_edges, free_labels):
            labels[edge_index] = label

        for vertex in reversed(order):
            edge_index = parent_edge[vertex]
            if edge_index is None:
                continue
            forced = 0
            for index, (u, v) in enumerate(graph.edges):
                if u == v:
                    continue
                if u == vertex or v == vertex:
                    forced ^= labels[index]
            labels[edge_index] = forced

        valid = True
        for vertex in range(graph.order):
            parity = 0
            for index, (u, v) in enumerate(graph.edges):
                if u == v:
                    continue
                if u == vertex or v == vertex:
                    parity ^= labels[index]
            if parity != 0:
                valid = False
                break
        if valid and all(label in D5 for label in labels):
            count += 1
    return count


def decode_graph6(record: str) -> Graph:
    data = [ord(character) - 63 for character in record.strip()]
    if not data or not (0 <= data[0] <= 62):
        raise ValueError("only short graph6 records are supported")
    order = data[0]
    bits = []
    for value in data[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for v in range(1, order):
        for u in range(v):
            if bits[cursor]:
                edges.append((u, v))
            cursor += 1
    return Graph(order, tuple(edges), graph6=record.strip())


def is_connected(graph: Graph) -> bool:
    if graph.order == 0:
        return True
    adjacency = [[] for _ in range(graph.order)]
    for u, v in graph.edges:
        if u != v:
            adjacency[u].append(v)
            adjacency[v].append(u)
    reached = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other in adjacency[vertex]:
            if other not in reached:
                reached.add(other)
                stack.append(other)
    return len(reached) == graph.order


def has_bridge(graph: Graph) -> bool:
    """Deletion test, valid for loops and repeated parallel edges."""

    for omitted, (u, v) in enumerate(graph.edges):
        if u == v:
            continue
        adjacency = [[] for _ in range(graph.order)]
        for index, (a, b) in enumerate(graph.edges):
            if index == omitted or a == b:
                continue
            adjacency[a].append(b)
            adjacency[b].append(a)
        reached = {u}
        stack = [u]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if other not in reached:
                    reached.add(other)
                    stack.append(other)
        if v not in reached:
            return True
    return False


def geng_cubic_graphs(order: int) -> Iterator[Graph]:
    executable = shutil.which("geng")
    if executable is None:
        raise RuntimeError("nauty-geng was not found on PATH")
    result = subprocess.run(
        [executable, "-cq", "-d3", "-D3", str(order)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    for row in result.stdout.splitlines():
        if row and not row.startswith(">"):
            yield decode_graph6(row)


def examples() -> tuple[Graph, ...]:
    return (
        decode_graph6("C~"),  # K4
        decode_graph6("EFz_"),  # K3,3
        decode_graph6("Gl_XIS"),  # cube
        decode_graph6("IheA@GUAo"),  # Petersen
        Graph(1, ((0, 0),), "one loop"),
        Graph(2, ((0, 1), (0, 1)), "two parallel edges"),
        Graph(2, ((0, 1), (0, 1), (0, 0)), "parallel pair plus loop"),
    )


def gauss_examples() -> tuple[Graph, ...]:
    return (
        Graph(1, (), "isolated vertex"),
        Graph(1, ((0, 0),), "loop"),
        Graph(2, ((0, 1),), "K2"),
        Graph(2, ((0, 1), (0, 1)), "parallel pair"),
        Graph(3, ((0, 1), (1, 2), (2, 0)), "triangle"),
        Graph(3, ((0, 1), (1, 2), (2, 0), (0, 1)), "triangle plus parallel edge"),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--census-max-order",
        type=int,
        default=10,
        help="largest even order in the complete bridgeless cubic simple census",
    )
    parser.add_argument(
        "--skip-direct-petersen",
        action="store_true",
        help="omit the one-million-cotree-assignment direct Petersen check",
    )
    arguments = parser.parse_args()

    assert fourier_table() == expected_fourier_table()
    assert Counter(fourier_table()) == Counter({10: 1, 2: 5, -2: 10})

    for graph in gauss_examples():
        direct = direct_gauss_sum(graph)
        closed = closed_gauss_sum(graph)
        assert direct == closed, (graph.name, direct, closed)

    comparison_rows = []
    for graph in examples():
        name = graph.name or graph.graph6
        if arguments.skip_direct_petersen and graph.graph6 == "IheA@GUAo":
            continue
        direct = direct_flow_count(graph)
        transformed = fourier_flow_count(graph)
        assert direct == transformed, (name, direct, transformed)
        comparison_rows.append((name, graph.order, len(graph.edges), direct))

    if arguments.census_max_order < 4 or arguments.census_max_order & 1:
        raise ValueError("--census-max-order must be an even integer at least 4")

    census_rows = []
    first_mod3_zero = None
    first_zero_leading_coefficient = None
    first_leading_valuation_failure = None
    first_tropical_valuation_failure = None
    for order in range(4, arguments.census_max_order + 1, 2):
        generated = 0
        bridgeless = 0
        residue_counts: Counter[int] = Counter()
        for graph in geng_cubic_graphs(order):
            generated += 1
            assert is_connected(graph)
            assert all(
                sum(1 for edge in graph.edges if vertex in edge) == 3
                for vertex in range(graph.order)
            )
            if has_bridge(graph):
                continue
            bridgeless += 1
            coefficients = cubic_coefficient_profile(graph)
            signed_sum = sum(coefficients.values())
            residue = signed_sum % 3
            residue_counts[residue] += 1
            if first_mod3_zero is None and residue == 0:
                first_mod3_zero = (
                    graph.graph6,
                    order,
                    len(graph.edges),
                    signed_sum,
                )
            if (
                first_zero_leading_coefficient is None
                and coefficients.get(0, 0) == 0
            ):
                first_zero_leading_coefficient = (
                    graph.graph6,
                    order,
                    coefficients,
                )
            leading_prediction, tropical_prediction, exact_valuation = (
                valuation_predictions(graph, coefficients)
            )
            if (
                first_leading_valuation_failure is None
                and leading_prediction != exact_valuation
            ):
                first_leading_valuation_failure = (
                    graph.graph6,
                    order,
                    coefficients,
                    leading_prediction,
                    exact_valuation,
                    count_from_cubic_profile(graph, coefficients),
                )
            if (
                first_tropical_valuation_failure is None
                and tropical_prediction != exact_valuation
            ):
                first_tropical_valuation_failure = (
                    graph.graph6,
                    order,
                    coefficients,
                    tropical_prediction,
                    exact_valuation,
                    count_from_cubic_profile(graph, coefficients),
                )
        census_rows.append((order, generated, bridgeless, dict(sorted(residue_counts.items()))))

    assert first_mod3_zero is not None
    assert first_mod3_zero[0] == "C~"

    print("PASS: Fourier table, Gauss formula, and exact flow counts agree.")
    print("exact flow-count comparisons:")
    for row in comparison_rows:
        print(" ", row)
    print("complete connected cubic simple census (bridgeless subset):")
    for row in census_rows:
        print(" ", row)
    print("first signed-rank sum divisible by 3:")
    print(" ", first_mod3_zero)
    print("first zero coefficient A_0 (None means no example in the census):")
    print(" ", first_zero_leading_coefficient)
    print("first failure of the A_0-only v2 prediction:")
    print(" ", first_leading_valuation_failure)
    print("first failure of the tropical grouped-term v2 prediction:")
    print(" ", first_tropical_valuation_failure)
    print(
        "CONCLUSION: the proposed mod-3 nonvanishing route fails already on K4; "
        "this is not a Five-Cycle Double Cover resolution."
    )


if __name__ == "__main__":
    main()
