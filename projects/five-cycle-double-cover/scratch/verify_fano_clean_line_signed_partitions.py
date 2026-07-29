#!/usr/bin/env python3
"""Solver-free audit of the signed-partition clean-line gluing law.

The first half enumerates the abstract boundary states for at most four
line-valued terminals and checks the literal bipartite gluing rule.  The
second half independently enumerates every covering three-dimensional
binary cycle subspace of the Petersen graph.  For every nonzero functional
and every edge cut of size at most four it computes the two shore states
from the graph and checks that signed-partition gluing agrees with the
global clean-line definition.  A final cross-test imports the separately
written unbounded-component construction and checks all of its diamond
interfaces through order 322.

No third-party Python package or SAT solver is used.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, product

import verify_unbounded_fano_line_components as unbounded


PETERSEN_EDGES = tuple(
    sorted(
        {(index, (index + 1) % 5) for index in range(5)}
        | {(5 + index, 5 + (index + 2) % 5) for index in range(5)}
        | {(index, 5 + index) for index in range(5)}
    )
)


def set_partitions(size: int) -> tuple[tuple[int, ...], ...]:
    """Canonical restricted-growth words for the partitions of [size]."""
    if size == 0:
        return ((),)
    rows: list[tuple[int, ...]] = []

    def extend(prefix: tuple[int, ...]) -> None:
        if len(prefix) == size:
            rows.append(prefix)
            return
        for block in range(max(prefix, default=-1) + 2):
            extend(prefix + (block,))

    extend((0,))
    return tuple(rows)


def signed_states(size: int, parity: int) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    rows = []
    for partition in set_partitions(size):
        blocks = max(partition, default=-1) + 1
        for bits in product((0, 1), repeat=blocks):
            if sum(bits) % 2 == parity:
                rows.append((partition, bits))
    return tuple(rows)


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def join(self, first: int, second: int) -> None:
        first = self.find(first)
        second = self.find(second)
        if first != second:
            self.parent[second] = first


def compatible(
    left: tuple[tuple[int, ...], tuple[int, ...]],
    right: tuple[tuple[int, ...], tuple[int, ...]],
) -> bool:
    """Literal component-graph gluing for two abstract shore states."""
    left_partition, left_bits = left
    right_partition, right_bits = right
    left_blocks = len(left_bits)
    right_blocks = len(right_bits)
    union = UnionFind(left_blocks + right_blocks)
    for terminal in range(len(left_partition)):
        union.join(
            left_partition[terminal],
            left_blocks + right_partition[terminal],
        )
    defects: Counter[int] = Counter()
    for block, bit in enumerate(left_bits):
        defects[union.find(block)] ^= bit
    for block, bit in enumerate(right_bits):
        defects[union.find(left_blocks + block)] ^= bit
    return not any(defects.values())


def incidence(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[tuple[int, int], ...], ...]:
    rows: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        rows[first].append((second, edge))
        rows[second].append((first, edge))
    return tuple(tuple(row) for row in rows)


def cycle_basis(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[int, ...]:
    adjacent = incidence(order, edges)
    parent = [-1] * order
    parent_edge = [-1] * order
    parent[0] = 0
    queue = deque([0])
    tree_edges: set[int] = set()
    while queue:
        vertex = queue.popleft()
        for neighbor, edge in adjacent[vertex]:
            if parent[neighbor] < 0:
                parent[neighbor] = vertex
                parent_edge[neighbor] = edge
                tree_edges.add(edge)
                queue.append(neighbor)
    assert -1 not in parent

    def path(first: int, second: int) -> int:
        first_prefix: dict[int, int] = {}
        mask = 0
        vertex = first
        while True:
            first_prefix[vertex] = mask
            if vertex == 0:
                break
            mask ^= 1 << parent_edge[vertex]
            vertex = parent[vertex]
        mask = 0
        vertex = second
        while vertex not in first_prefix:
            mask ^= 1 << parent_edge[vertex]
            vertex = parent[vertex]
        return mask ^ first_prefix[vertex]

    basis = []
    for edge, (first, second) in enumerate(edges):
        if edge not in tree_edges:
            basis.append((1 << edge) ^ path(first, second))
    assert len(basis) == len(edges) - order + 1
    return tuple(basis)


def binary_rank(vectors: tuple[int, ...]) -> int:
    pivots: dict[int, int] = {}
    for original in vectors:
        vector = original
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = vector
                break
            vector ^= pivots[pivot]
    return len(pivots)


def covering_three_spaces(
    cycles: tuple[int, ...], all_edges: int
) -> tuple[tuple[int, int, int], ...]:
    spaces: dict[tuple[int, ...], tuple[int, int, int]] = {}
    for basis in combinations(cycles[1:], 3):
        if binary_rank(basis) != 3 or (basis[0] | basis[1] | basis[2]) != all_edges:
            continue
        span = tuple(
            sorted(
                (
                    basis[0],
                    basis[1],
                    basis[2],
                    basis[0] ^ basis[1],
                    basis[0] ^ basis[2],
                    basis[1] ^ basis[2],
                    basis[0] ^ basis[1] ^ basis[2],
                )
            )
        )
        spaces.setdefault(span, basis)
    return tuple(spaces.values())


def flow_values(
    basis: tuple[int, int, int], edge_count: int
) -> tuple[int, ...]:
    values = []
    for edge in range(edge_count):
        value = sum(((basis[coordinate] >> edge) & 1) << coordinate for coordinate in range(3))
        assert value
        values.append(value)
    return tuple(values)


def components_on_edges(
    vertices: set[int],
    edges: tuple[tuple[int, int], ...],
    selected: set[int],
) -> tuple[dict[int, int], tuple[frozenset[int], ...]]:
    adjacent: dict[int, list[int]] = {vertex: [] for vertex in vertices}
    for edge in selected:
        first, second = edges[edge]
        assert first in vertices and second in vertices
        adjacent[first].append(second)
        adjacent[second].append(first)
    component_of: dict[int, int] = {}
    components: list[frozenset[int]] = []
    for root in sorted(vertices):
        if root in component_of:
            continue
        found = {root}
        queue = deque([root])
        component_of[root] = len(components)
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacent[vertex]:
                if neighbor not in found:
                    found.add(neighbor)
                    component_of[neighbor] = len(components)
                    queue.append(neighbor)
        components.append(frozenset(found))
    return component_of, tuple(components)


def component_defect(
    component: frozenset[int],
    edges: tuple[tuple[int, int], ...],
    values: tuple[int, ...],
    base: int,
) -> int:
    return sum(
        value == base and ((first in component) != (second in component))
        for (first, second), value in zip(edges, values, strict=True)
    ) % 2


def global_clean(
    order: int,
    edges: tuple[tuple[int, int], ...],
    values: tuple[int, ...],
    functional: int,
    base: int,
) -> bool:
    vertices = set(range(order))
    line_edges = {
        edge
        for edge, value in enumerate(values)
        if (functional & value).bit_count() % 2 == 0
    }
    _, components = components_on_edges(vertices, edges, line_edges)
    return all(
        component_defect(component, edges, values, base) == 0
        for component in components
    )


def shore_state(
    vertices: set[int],
    edges: tuple[tuple[int, int], ...],
    values: tuple[int, ...],
    functional: int,
    base: int,
    boundary: tuple[int, ...],
) -> tuple[bool, tuple[tuple[int, ...], tuple[int, ...]]]:
    internal_line_edges = {
        edge
        for edge, ((first, second), value) in enumerate(zip(edges, values, strict=True))
        if first in vertices
        and second in vertices
        and (functional & value).bit_count() % 2 == 0
    }
    component_of, components = components_on_edges(vertices, edges, internal_line_edges)
    line_terminals = [
        edge
        for edge in boundary
        if (functional & values[edge]).bit_count() % 2 == 0
    ]
    touched_components = []
    for edge in line_terminals:
        first, second = edges[edge]
        endpoint = first if first in vertices else second
        touched_components.append(component_of[endpoint])
    open_components = sorted(set(touched_components))
    open_index = {component: index for index, component in enumerate(open_components)}
    partition = tuple(open_index[component] for component in touched_components)
    bits = tuple(
        component_defect(components[component], edges, values, base)
        for component in open_components
    )
    closed_clean = all(
        component_defect(component, edges, values, base) == 0
        for index, component in enumerate(components)
        if index not in open_index
    )
    return closed_clean, (partition, bits)


def small_cuts(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[set[int], tuple[int, ...]], ...]:
    all_vertices = (1 << order) - 1
    rows = []
    for mask in range(1, all_vertices):
        complement = all_vertices ^ mask
        if mask > complement:
            continue
        boundary = tuple(
            edge
            for edge, (first, second) in enumerate(edges)
            if ((mask >> first) & 1) != ((mask >> second) & 1)
        )
        if 2 <= len(boundary) <= 4:
            rows.append(
                (
                    {vertex for vertex in range(order) if (mask >> vertex) & 1},
                    boundary,
                )
            )
    return tuple(rows)


def check_one_cut(
    order: int,
    edges: tuple[tuple[int, int], ...],
    values: tuple[int, ...],
    left_vertices: set[int],
) -> int:
    right_vertices = set(range(order)) - left_vertices
    boundary = tuple(
        edge
        for edge, (first, second) in enumerate(edges)
        if (first in left_vertices) != (second in left_vertices)
    )
    comparisons = 0
    for functional in range(1, 8):
        base = next(
            value
            for value in range(1, 8)
            if (functional & value).bit_count() % 2 == 1
        )
        actual = global_clean(order, edges, values, functional, base)
        left_closed, left = shore_state(
            left_vertices, edges, values, functional, base, boundary
        )
        right_closed, right = shore_state(
            right_vertices, edges, values, functional, base, boundary
        )
        predicted = left_closed and right_closed and compatible(left, right)
        assert predicted == actual
        comparisons += 1
    return comparisons


def check_cap_gluing_no_go() -> None:
    """Literal two-cut warning: clean caps need not give a clean gluing."""
    cap_edges = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    left_cap_flow = (2, 5, 7, 7, 5, 2)
    right_cap_flow = (2, 1, 3, 3, 1, 2)
    for values in (left_cap_flow, right_cap_flow):
        for row in incidence(4, cap_edges):
            total = 0
            for _, edge in row:
                total ^= values[edge]
            assert total == 0
        assert global_clean(4, cap_edges, values, 1, 1)

    graph_edges = (
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
        (4, 6),
        (4, 7),
        (5, 6),
        (5, 7),
        (6, 7),
        (0, 4),
        (1, 5),
    )
    graph_flow = (
        left_cap_flow[1],
        left_cap_flow[2],
        left_cap_flow[3],
        left_cap_flow[4],
        left_cap_flow[5],
        right_cap_flow[1],
        right_cap_flow[2],
        right_cap_flow[3],
        right_cap_flow[4],
        right_cap_flow[5],
        2,
        2,
    )
    rows = incidence(8, graph_edges)
    assert all(len(row) == 3 for row in rows)
    for row in rows:
        total = 0
        for _, edge in row:
            total ^= graph_flow[edge]
        assert total == 0
    # Every single-edge deletion remains connected.
    for omitted in range(len(graph_edges)):
        seen = {0}
        queue = deque([0])
        while queue:
            vertex = queue.popleft()
            for neighbor, edge in rows[vertex]:
                if edge != omitted and neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        assert len(seen) == 8

    boundary = (10, 11)
    left_closed, left = shore_state(
        set(range(4)), graph_edges, graph_flow, 1, 1, boundary
    )
    right_closed, right = shore_state(
        set(range(4, 8)), graph_edges, graph_flow, 1, 1, boundary
    )
    assert left_closed and right_closed
    assert left == ((0, 1), (0, 0))
    assert right == ((0, 1), (1, 1))
    assert not compatible(left, right)
    assert not global_clean(8, graph_edges, graph_flow, 1, 1)

    # The warning graph itself is FiveCDC-positive: this proper Tait
    # coloring gives the three duads 01,02,12 and two empty coordinates.
    tait_colors = (0, 1, 1, 0, 2, 0, 1, 1, 0, 2, 2, 2)
    duads = (0b00011, 0b00101, 0b00110)
    labels = tuple(duads[color] for color in tait_colors)
    for row in rows:
        assert len({tait_colors[edge] for _, edge in row}) == 3
        total = 0
        for _, edge in row:
            total ^= labels[edge]
        assert total == 0


def main() -> None:
    expected_state_counts = (1, 1, 3, 11, 47)
    composition_counts = []
    for size, expected in enumerate(expected_state_counts):
        parity_counts = []
        clean_counts = []
        for parity in (0, 1):
            states = signed_states(size, parity)
            parity_counts.append(len(states))
            clean_counts.append(
                sum(compatible(left, right) for left in states for right in states)
            )
        if size == 0:
            # The empty state exists only when its forced total defect is zero.
            assert parity_counts == [1, 0]
        else:
            assert parity_counts == [expected, expected]
            assert clean_counts[0] == clean_counts[1]
        composition_counts.append(clean_counts[0])

    order = 10
    edges = PETERSEN_EDGES
    assert len(edges) == 15
    assert all(len(row) == 3 for row in incidence(order, edges))
    basis = cycle_basis(order, edges)
    cycles = [0]
    for vector in basis:
        cycles += [cycle ^ vector for cycle in cycles]
    cycles_tuple = tuple(sorted(cycles))
    assert len(cycles_tuple) == 64
    spaces = covering_three_spaces(cycles_tuple, (1 << len(edges)) - 1)
    cuts = small_cuts(order, edges)
    cut_histogram = Counter(len(boundary) for _, boundary in cuts)

    tests = 0
    clean_tests = 0
    for flow_basis in spaces:
        values = flow_values(flow_basis, len(edges))
        for functional in range(1, 8):
            base = next(
                value
                for value in range(1, 8)
                if (functional & value).bit_count() % 2 == 1
            )
            actual = global_clean(order, edges, values, functional, base)
            clean_tests += actual
            for left_vertices, boundary in cuts:
                line_count = sum(
                    (functional & values[edge]).bit_count() % 2 == 0
                    for edge in boundary
                )
                assert line_count % 2 == len(boundary) % 2
            # check_one_cut repeats the seven functionals, so do the literal
            # comparison once per flow/cut outside this functional loop.
        for left_vertices, _ in cuts:
            tests += check_one_cut(order, edges, values, left_vertices)

    # Cross-check every two-edge diamond interface in the sharp unbounded
    # clean-line family through order 322.  This is a retained hard family:
    # the number of line components grows at every expansion.
    diamond_tests = 0
    hard_order, hard_edges, hard_flow, hard_labels = unbounded.base_instance()
    for depth in range(3):
        outside = {
            edge for edge, value in enumerate(hard_flow) if value not in unbounded.LINE
        }
        tree = unbounded.adapted_tree(hard_order, hard_edges, outside)
        cotree = sorted(set(range(len(hard_edges))) - tree)
        first_new_vertex = hard_order
        hard_order, hard_edges, hard_flow, hard_labels = unbounded.expand(
            hard_order, hard_edges, hard_flow, hard_labels, tree
        )
        for position in range(len(cotree)):
            gadget = set(
                range(
                    first_new_vertex + 4 * position,
                    first_new_vertex + 4 * position + 4,
                )
            )
            boundary_size = sum(
                (first in gadget) != (second in gadget)
                for first, second in hard_edges
            )
            assert boundary_size == 2
            diamond_tests += check_one_cut(
                hard_order, hard_edges, hard_flow, gadget
            )
    check_cap_gluing_no_go()

    print("signed-partition clean-line composition: PASS")
    print("abstract state counts m=0..4:", " ".join(map(str, expected_state_counts)))
    print("compatible ordered pairs for parity 0:", " ".join(map(str, composition_counts)))
    print("Petersen covering binary three-spaces:", len(spaces))
    print(
        "Petersen cuts of size 2..4:",
        " ".join(f"{size}:{cut_histogram[size]}" for size in range(2, 5)),
    )
    print("literal flow/functional/cut comparisons:", tests)
    print("clean flow/functionals (before cut multiplication):", clean_tests)
    print("unbounded-family diamond-interface comparisons:", diamond_tests)
    print("clean-cap two-cut gluing no-go: checked on an 8-vertex Tait graph")


if __name__ == "__main__":
    main()
