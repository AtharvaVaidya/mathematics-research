#!/usr/bin/env python3
"""Independent exhaustive verifier for the 12-vertex closure no-go.

The tested strengthening asks for a fixed-fibre packing (T0,T1,T2) and
some coordinate k such that

    K(Ti) intersection K(Tj) is contained in cl(K(Tk)),

where {i,j,k}={0,1,2} and closure is in the graphic matroid.  The exact
Jaeger target only asks that this intersection have even degree after
contracting every K(Tk)-component.

Only the Python standard library is used.  The checker does not import or
invoke the SAT producer.
"""

from __future__ import annotations

from collections import defaultdict, deque
from itertools import combinations


GRAPH6 = "K?`@E`gFCKEO"
VERTEX_COUNT = 12
EDGES = (
    (0, 4), (1, 5), (2, 6), (0, 7), (1, 7), (3, 7),
    (1, 8), (2, 8), (4, 8), (3, 9), (4, 9), (5, 9),
    (0, 10), (5, 10), (6, 10), (2, 11), (3, 11), (6, 11),
)
DEFECT_TRIPLES = ((0, 4, 11), (1, 3, 10))
EXPECTED_WITNESSES = (
    (50431, 212774, 259016),
    (103103, 159573, 260576),
)
ALL_EDGES = (1 << len(EDGES)) - 1


def parse_short_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    order = ord(record[0]) - 63
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    cursor = 0
    edges = []
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def incidence() -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(VERTEX_COUNT)]
    for edge, (left, right) in enumerate(EDGES):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


INCIDENCE = incidence()


def connected(deleted: frozenset[int] = frozenset()) -> bool:
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for edge in INCIDENCE[vertex]:
            if edge in deleted:
                continue
            left, right = EDGES[edge]
            other = right if left == vertex else left
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return len(seen) == VERTEX_COUNT


def is_tree(mask: int) -> bool:
    if mask.bit_count() != VERTEX_COUNT - 1:
        return False
    parent = list(range(VERTEX_COUNT))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge, (left, right) in enumerate(EDGES):
        if not ((mask >> edge) & 1):
            continue
        a, b = find(left), find(right)
        if a == b:
            return False
        parent[a] = b
    return True


def odd_kernel(tree: int) -> int:
    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(VERTEX_COUNT)
    ]
    for edge, (left, right) in enumerate(EDGES):
        if (tree >> edge) & 1:
            adjacency[left].append((right, edge))
            adjacency[right].append((left, edge))
    parent = [-2] * VERTEX_COUNT
    parent_edge = [-1] * VERTEX_COUNT
    parent[0] = -1
    order = [0]
    for vertex in order:
        for other, edge in adjacency[vertex]:
            if parent[other] == -2:
                parent[other] = vertex
                parent_edge[other] = edge
                order.append(other)
    assert len(order) == VERTEX_COUNT
    size = [1] * VERTEX_COUNT
    answer = 0
    for vertex in reversed(order[1:]):
        if size[vertex] & 1:
            answer |= 1 << parent_edge[vertex]
        size[parent[vertex]] += size[vertex]
    assert answer & ~tree == 0
    assert all(
        sum((answer >> edge) & 1 for edge in row) & 1
        for row in INCIDENCE
    )
    return answer


def component_map(forest: int) -> tuple[int, ...]:
    parent = list(range(VERTEX_COUNT))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge, (left, right) in enumerate(EDGES):
        if not ((forest >> edge) & 1):
            continue
        a, b = find(left), find(right)
        assert a != b
        parent[a] = b
    return tuple(find(vertex) for vertex in range(VERTEX_COUNT))


def closure_good(kernels: tuple[int, int, int], coordinate: int) -> bool:
    first, second = (index for index in range(3) if index != coordinate)
    common = kernels[first] & kernels[second]
    component = component_map(kernels[coordinate])
    return all(
        not ((common >> edge) & 1) or component[left] == component[right]
        for edge, (left, right) in enumerate(EDGES)
    )


def parity_good(kernels: tuple[int, int, int], coordinate: int) -> bool:
    first, second = (index for index in range(3) if index != coordinate)
    common = kernels[first] & kernels[second]
    component = component_map(kernels[coordinate])
    boundary: dict[int, int] = defaultdict(int)
    for edge, (left, right) in enumerate(EDGES):
        if not ((common >> edge) & 1):
            continue
        a, b = component[left], component[right]
        if a != b:
            boundary[a] ^= 1
            boundary[b] ^= 1
    return not any(boundary.values())


def all_spanning_trees() -> tuple[int, ...]:
    answer = []
    for choice in combinations(range(len(EDGES)), VERTEX_COUNT - 1):
        mask = sum(1 << edge for edge in choice)
        if is_tree(mask):
            answer.append(mask)
    return tuple(answer)


def verify_defect(
    trees: tuple[int, ...],
    kernels: dict[int, int],
    defect_edges: tuple[int, int, int],
    expected_witness: tuple[int, int, int],
) -> tuple[int, int, int, dict[tuple[int, int], int]]:
    defect = sum(1 << edge for edge in defect_edges)
    double = ALL_EDGES ^ defect
    tree_set = set(trees)
    by_defect_part: dict[int, list[int]] = defaultdict(list)
    for tree in trees:
        by_defect_part[tree & defect].append(tree)

    packings = 0
    closure_packings = 0
    parity_packings = 0
    coordinate_histogram: dict[tuple[int, int], int] = defaultdict(int)
    saw_witness = False

    for first in trees:
        first_defect = first & defect
        for second_defect, candidates in by_defect_part.items():
            if first_defect & second_defect:
                continue
            for second in candidates:
                # A double edge cannot be omitted by both first trees.
                if double & ~(first | second):
                    continue
                third = (
                    ((first ^ second) & double)
                    | (defect & ~(first | second))
                )
                if third not in tree_set:
                    continue

                triple = (first, second, third)
                for edge in range(len(EDGES)):
                    expected = 1 if (defect >> edge) & 1 else 2
                    assert sum((tree >> edge) & 1 for tree in triple) == expected
                triple_kernels = tuple(kernels[tree] for tree in triple)
                closure_coordinates = sum(
                    closure_good(triple_kernels, coordinate)
                    for coordinate in range(3)
                )
                parity_coordinates = sum(
                    parity_good(triple_kernels, coordinate)
                    for coordinate in range(3)
                )
                packings += 1
                closure_packings += closure_coordinates > 0
                parity_packings += parity_coordinates > 0
                coordinate_histogram[
                    (closure_coordinates, parity_coordinates)
                ] += 1
                if triple == expected_witness:
                    saw_witness = True
                    assert closure_coordinates == 0
                    assert parity_coordinates == 1

    assert saw_witness
    return (
        packings,
        closure_packings,
        parity_packings,
        dict(coordinate_histogram),
    )


def main() -> None:
    assert parse_short_graph6(GRAPH6) == (VERTEX_COUNT, EDGES)
    assert len(EDGES) == 18
    assert len({frozenset(edge) for edge in EDGES}) == len(EDGES)
    assert all(left != right for left, right in EDGES)
    assert all(len(row) == 3 for row in INCIDENCE)
    assert connected()
    assert all(
        connected(frozenset(deleted))
        for size in (1, 2)
        for deleted in combinations(range(len(EDGES)), size)
    )

    # The two defect triples are the alternating matchings of this 6-cycle.
    alternating_cycle = (0, 10, 11, 1, 4, 3)
    assert frozenset(DEFECT_TRIPLES[0]) == frozenset(
        alternating_cycle[::2]
    )
    assert frozenset(DEFECT_TRIPLES[1]) == frozenset(
        alternating_cycle[1::2]
    )

    trees = all_spanning_trees()
    assert len(trees) == 8640
    kernels = {tree: odd_kernel(tree) for tree in trees}

    results = tuple(
        verify_defect(trees, kernels, defect, witness)
        for defect, witness in zip(DEFECT_TRIPLES, EXPECTED_WITNESSES)
    )
    expected = (
        355392,
        0,
        7704,
        {(0, 0): 347688, (0, 1): 7704},
    )
    assert results == (expected, expected)

    print("PASS")
    print(f"graph6={GRAPH6}; n=12 m=18; simple cubic 3-edge-connected")
    print("spanning_trees=8640")
    print("defect_triples=0,4,11 and 1,3,10")
    print("ordered_packings_per_fibre=355392")
    print("packings_good_for_kernel_closure=0")
    print("packings_good_for_exact_component_parity=7704")
    print("histogram=(closure_coordinates,parity_coordinates):"
          " (0,0)=347688 (0,1)=7704")
    print("scope=kernel-closure strengthening false; exact parity survives")


if __name__ == "__main__":
    main()
