#!/usr/bin/env python3
"""Independent replay of the order-24 APX score-one near-state.

Only the Python standard library is used.  The packing oracle enumerates
the complete binary cycle space and applies the even-marked circuit
criterion.  The script then enumerates every simple circuit switch.

Scope: this checks an auxiliary near-state.  It is neither a FiveCDC
counterexample nor an APX counterexample.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "fano-apx-score1-order24.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(record: str) -> tuple[int, list[tuple[int, int]]]:
    require(record and record[0] != "~", "only small graph6 is supported")
    order = ord(record[0]) - 63
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            require(cursor < len(bits), "truncated graph6")
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, edges


def incidence(
    order: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    answer = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        answer[left].append(edge)
        answer[right].append(edge)
    return answer


def vertex_components(
    order: int,
    edges: list[tuple[int, int]],
    kept_mask: int,
) -> list[set[int]]:
    adjacency = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        if (kept_mask >> edge) & 1:
            adjacency[left].append(right)
            adjacency[right].append(left)
    seen: set[int] = set()
    answer: list[set[int]] = []
    for start in range(order):
        if start in seen:
            continue
        piece = {start}
        seen.add(start)
        queue = [start]
        for vertex in queue:
            for other in adjacency[vertex]:
                if other not in seen:
                    seen.add(other)
                    piece.add(other)
                    queue.append(other)
        answer.append(piece)
    return answer


def piece_has_cycle(
    piece: set[int],
    edges: list[tuple[int, int]],
    kept_mask: int,
) -> bool:
    internal = sum(
        ((kept_mask >> edge) & 1)
        and left in piece
        and right in piece
        for edge, (left, right) in enumerate(edges)
    )
    return internal >= len(piece)


def fundamental_cycle_basis(
    order: int,
    edges: list[tuple[int, int]],
    inc: list[list[int]],
    kept_mask: int,
) -> list[int]:
    parent = [-1] * order
    parent_edge = [-1] * order
    depth = [0] * order
    tree_mask = 0
    for root in range(order):
        if parent[root] >= 0:
            continue
        parent[root] = root
        queue = [root]
        for vertex in queue:
            for edge in inc[vertex]:
                if not ((kept_mask >> edge) & 1):
                    continue
                left, right = edges[edge]
                other = left ^ right ^ vertex
                if parent[other] >= 0:
                    continue
                parent[other] = vertex
                parent_edge[other] = edge
                depth[other] = depth[vertex] + 1
                tree_mask |= 1 << edge
                queue.append(other)
    basis: list[int] = []
    for edge, (left0, right0) in enumerate(edges):
        if not ((kept_mask >> edge) & 1) or ((tree_mask >> edge) & 1):
            continue
        cycle = 1 << edge
        left, right = left0, right0
        while depth[left] > depth[right]:
            cycle ^= 1 << parent_edge[left]
            left = parent[left]
        while depth[right] > depth[left]:
            cycle ^= 1 << parent_edge[right]
            right = parent[right]
        while left != right:
            cycle ^= 1 << parent_edge[left]
            left = parent[left]
            cycle ^= 1 << parent_edge[right]
            right = parent[right]
        basis.append(cycle)
    return basis


class PackingOracle:
    def __init__(
        self,
        order: int,
        edges: list[tuple[int, int]],
        inc: list[list[int]],
    ) -> None:
        self.order = order
        self.edges = edges
        self.inc = inc
        self.all_edges = (1 << len(edges)) - 1
        self.cache: dict[int, bool] = {}

    def packs(self, matching: int) -> bool:
        known = self.cache.get(matching)
        if known is not None:
            return known
        terminal_mask = 0
        for edge, (left, right) in enumerate(self.edges):
            if (matching >> edge) & 1:
                terminal_mask ^= (1 << left) | (1 << right)
        kept = self.all_edges ^ matching
        basis = fundamental_cycle_basis(
            self.order, self.edges, self.inc, kept
        )
        cycle = 0
        previous_gray = 0
        for choice in range(1 << len(basis)):
            gray = choice ^ (choice >> 1)
            if choice:
                changed = gray ^ previous_gray
                bit = changed.bit_length() - 1
                cycle ^= basis[bit]
            previous_gray = gray
            if any(
                ((terminal_mask >> vertex) & 1)
                and sum((cycle >> edge) & 1 for edge in self.inc[vertex]) != 2
                for vertex in range(self.order)
            ):
                continue
            selected_components = vertex_components(
                self.order, self.edges, cycle
            )
            if all(
                sum((terminal_mask >> vertex) & 1 for vertex in piece) % 2
                == 0
                for piece in selected_components
                if any(
                    (cycle >> edge) & 1
                    for vertex in piece
                    for edge in self.inc[vertex]
                )
            ):
                self.cache[matching] = True
                return True
        self.cache[matching] = False
        return False


def value_classes(flow: tuple[int, ...]) -> list[int]:
    answer = [0] * 8
    for edge, value in enumerate(flow):
        answer[value] |= 1 << edge
    return answer


def successful_values(
    flow: tuple[int, ...], oracle: PackingOracle
) -> list[int]:
    classes = value_classes(flow)
    return [value for value in range(1, 8) if oracle.packs(classes[value])]


def dot(functional: int, value: int) -> int:
    return (functional & value).bit_count() & 1


def support_component_index(
    order: int,
    edges: list[tuple[int, int]],
    flow: tuple[int, ...],
    functional: int,
) -> list[int]:
    kept = sum(
        (dot(functional, value) << edge)
        for edge, value in enumerate(flow)
    )
    pieces = vertex_components(order, edges, kept)
    answer = [-1] * order
    for component, piece in enumerate(pieces):
        for vertex in piece:
            answer[vertex] = component
    require(all(item >= 0 for item in answer), "component index missing")
    return answer


def apx_witnesses(
    order: int,
    edges: list[tuple[int, int]],
    flow: tuple[int, ...],
    oracle: PackingOracle,
) -> list[tuple[int, int, int, int]]:
    classes = value_classes(flow)
    answer: list[tuple[int, int, int, int]] = []
    for value in range(1, 8):
        members = [
            edge for edge, item in enumerate(flow) if item == value
        ]
        for functional in range(1, 8):
            if dot(functional, value):
                continue
            component = support_component_index(
                order, edges, flow, functional
            )
            types: dict[tuple[int, int], list[int]] = {}
            for edge in members:
                left, right = edges[edge]
                edge_type = tuple(
                    sorted((component[left], component[right]))
                )
                types.setdefault(edge_type, []).append(edge)
            for same_type in types.values():
                for first, second in combinations(same_type, 2):
                    reduced = classes[value]
                    reduced ^= (1 << first) | (1 << second)
                    if oracle.packs(reduced):
                        answer.append(
                            (value, functional, first, second)
                        )
    return answer


def all_simple_circuits(
    order: int,
    edges: list[tuple[int, int]],
    inc: list[list[int]],
) -> list[int]:
    answer: list[int] = []
    used = [False] * order
    path: list[int] = []

    def visit(start: int, vertex: int, support: int) -> None:
        for edge in inc[vertex]:
            left, right = edges[edge]
            other = left ^ right ^ vertex
            if other == start:
                if len(path) >= 3 and path[1] < vertex:
                    answer.append(support | (1 << edge))
                continue
            if other < start or used[other]:
                continue
            used[other] = True
            path.append(other)
            visit(start, other, support | (1 << edge))
            path.pop()
            used[other] = False

    for start in range(order):
        used[start] = True
        path[:] = [start]
        visit(start, start, 0)
        used[start] = False
    require(len(answer) == len(set(answer)), "duplicate simple circuit")
    return answer


def has_tait_coloring(
    edges: list[tuple[int, int]], inc: list[list[int]]
) -> bool:
    colors = [-1] * len(edges)
    used = [0] * len(inc)

    def search(colored: int) -> bool:
        if colored == len(edges):
            return True
        best_edge = -1
        best_available = 0
        best_count = 4
        for edge, (left, right) in enumerate(edges):
            if colors[edge] >= 0:
                continue
            available = 0b111 & ~(used[left] | used[right])
            count = available.bit_count()
            if not count:
                return False
            if count < best_count:
                best_edge = edge
                best_available = available
                best_count = count
        require(best_edge >= 0, "edge-color search lost an edge")
        left, right = edges[best_edge]
        available = best_available
        while available:
            color_bit = available & -available
            available ^= color_bit
            colors[best_edge] = color_bit.bit_length() - 1
            used[left] |= color_bit
            used[right] |= color_bit
            if search(colored + 1):
                return True
            used[left] ^= color_bit
            used[right] ^= color_bit
            colors[best_edge] = -1
        return False

    return search(0)


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    order, edges = decode_graph6(data["graph6"])
    require(order == 24 and len(edges) == 36, "wrong graph size")
    require(
        [list(edge) for edge in edges] == data["edge_order"],
        "graph6 edge-order mismatch",
    )
    require(len(set(edges)) == len(edges), "parallel edge")
    require(all(left != right for left, right in edges), "loop")
    inc = incidence(order, edges)
    require(all(len(row) == 3 for row in inc), "not cubic")
    all_edges = (1 << len(edges)) - 1
    require(
        vertex_components(order, edges, all_edges)
        == [set(range(order))],
        "not connected",
    )
    for size in range(1, 4):
        for removed in combinations(range(len(edges)), size):
            kept = all_edges
            for edge in removed:
                kept ^= 1 << edge
            pieces = vertex_components(order, edges, kept)
            require(
                sum(piece_has_cycle(piece, edges, kept) for piece in pieces)
                < 2,
                "cyclic edge cut below four",
            )
    require(not has_tait_coloring(edges, inc), "graph is Tait-colourable")

    flow = tuple(data["flow_values_by_edge"])
    require(len(flow) == len(edges), "wrong flow length")
    require(all(1 <= item <= 7 for item in flow), "zero flow value")
    require(
        all(
            flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0
            for row in inc
        ),
        "flow conservation failed",
    )
    for value in range(1, 8):
        endpoints: set[int] = set()
        for edge, item in enumerate(flow):
            if item != value:
                continue
            left, right = edges[edge]
            require(
                left not in endpoints and right not in endpoints,
                "value class is not a matching",
            )
            endpoints.update((left, right))
    oracle = PackingOracle(order, edges, inc)
    initial_success = successful_values(flow, oracle)
    require(
        initial_success == data["expected_initial_successful_values"],
        "initial flow is not bad",
    )
    initial_witnesses = apx_witnesses(order, edges, flow, oracle)
    require(
        len(initial_witnesses) == data["expected_apx_score"],
        "initial APX score mismatch",
    )
    frozen = data["expected_unique_apx_witness"]
    expected_witness = (
        frozen["s"], frozen["mu"], *frozen["pair"]
    )
    require(
        initial_witnesses == [expected_witness],
        "unique APX witness mismatch",
    )
    for row in data["unique_witness_canonical_defects"]:
        functional = row["nu"]
        require(dot(functional, frozen["s"]) == 1,
                "defect functional does not see s")
        factor_mask = sum(
            ((1 - dot(functional, value)) << edge)
            for edge, value in enumerate(flow)
        )
        factor_pieces = vertex_components(order, edges, factor_mask)
        factor_index = [-1] * order
        for component, piece in enumerate(factor_pieces):
            for vertex in piece:
                factor_index[vertex] = component

        def quotient_boundary(edge_set: list[int]) -> int:
            boundary = 0
            for edge in edge_set:
                left, right = edges[edge]
                boundary ^= (
                    (1 << factor_index[left])
                    ^ (1 << factor_index[right])
                )
            return boundary

        sigma = quotient_boundary(frozen["pair"])
        rainbow_vectors = {
            quotient_boundary(
                [
                    edge
                    for edge, value in enumerate(flow)
                    if value == affine_value
                ]
            )
            for affine_value in range(1, 8)
            if dot(functional, affine_value)
        }
        require(len(rainbow_vectors) == 1,
                "affine boundary parities disagree")
        rainbow = rainbow_vectors.pop()
        defect = sigma ^ rainbow
        require(
            {
                "nu": functional,
                "sigma": sigma,
                "rainbow": rainbow,
                "defect": defect,
            }
            == row,
            "canonical defect vector mismatch",
        )
        require(defect and defect.bit_count() % 2 == 0,
                "defect is not nonzero even")

    circuits = all_simple_circuits(order, edges, inc)
    require(
        len(circuits) == data["expected_simple_circuit_count"],
        "simple circuit count mismatch",
    )
    require(
        min(circuit.bit_count() for circuit in circuits)
        == data["expected_girth"],
        "girth mismatch",
    )
    repair = data["displayed_apx_repair"]
    repair_circuit = sum(1 << edge for edge in repair["circuit_edges"])
    require(repair_circuit in circuits, "displayed repair is not a circuit")
    witness_line = {
        value
        for value in range(8)
        if not dot(frozen["mu"], value)
    }
    require(
        [
            edge
            for edge in repair["circuit_edges"]
            if flow[edge] in witness_line
        ]
        == frozen["pair"],
        "displayed circuit does not have the exact affine trace",
    )
    switch_value = repair["switch_value"]
    require(
        switch_value in witness_line - {0, frozen["s"]},
        "displayed switch value is not on the witness line",
    )
    displayed_switched = tuple(
        value ^ switch_value
        if (repair_circuit >> edge) & 1
        else value
        for edge, value in enumerate(flow)
    )
    require(
        successful_values(displayed_switched, oracle)
        == repair["expected_successful_values"],
        "displayed APX repair did not replay",
    )
    legal_switches = 0
    bad_legal_switches = 0
    minimum_bad_score: int | None = None
    bad_score_distribution: Counter[int] = Counter()
    for circuit in circuits:
        present = {
            flow[edge]
            for edge in range(len(edges))
            if (circuit >> edge) & 1
        }
        for switch_value in range(1, 8):
            if switch_value in present:
                continue
            legal_switches += 1
            switched = tuple(
                value ^ switch_value
                if (circuit >> edge) & 1
                else value
                for edge, value in enumerate(flow)
            )
            require(
                all(
                    switched[row[0]]
                    ^ switched[row[1]]
                    ^ switched[row[2]]
                    == 0
                    for row in inc
                ),
                "switch broke flow conservation",
            )
            if successful_values(switched, oracle):
                continue
            bad_legal_switches += 1
            score = len(apx_witnesses(order, edges, switched, oracle))
            bad_score_distribution[score] += 1
            minimum_bad_score = (
                score
                if minimum_bad_score is None
                else min(minimum_bad_score, score)
            )
    require(
        legal_switches == data["expected_legal_switch_count"],
        "legal-switch count mismatch",
    )
    require(
        bad_legal_switches == data["expected_bad_legal_switch_count"],
        "bad legal-switch count mismatch",
    )
    require(
        minimum_bad_score
        == data["expected_minimum_bad_neighbor_apx_score"],
        "bad-neighbour APX minimum mismatch",
    )
    require(
        {str(score): count for score, count
         in sorted(bad_score_distribution.items())}
        == data["expected_bad_neighbor_score_distribution"],
        "bad-neighbour APX score distribution mismatch",
    )
    print("independent order-24 APX score-one checker: PASS")
    print("initial APX witness:", initial_witnesses[0])
    print("simple circuits:", len(circuits))
    print("legal one-circuit switches:", legal_switches)
    print("bad legal one-circuit neighbours:", bad_legal_switches)
    print("minimum APX score among bad neighbours:", minimum_bad_score)
    print("bad-neighbour APX score distribution:",
          dict(sorted(bad_score_distribution.items())))
    print("scope: near-state only; APX and FiveCDC remain open")


if __name__ == "__main__":
    main()
