#!/usr/bin/env python3
"""Check the triangle contraction/lifting obstruction for kernel closure.

The checker is independent of the SAT encodings.  It verifies:

1. contracting one triangle of the 16-vertex countermodel gives the stated
   14-vertex graph;
2. an explicit closure-good star packing of the contracted graph;
3. all six legal triangle lifts of that packing fail closure in every
   coordinate;
4. contracting all three disjoint triangles gives Petersen, and the three
   expanded vertices are an alternating class of the distance-two C6 from
   the bad root.
"""

from __future__ import annotations

from collections import deque
from itertools import permutations


FULL_EDGES = (
    (0, 6), (0, 9), (0, 10),
    (1, 7), (1, 10), (1, 11),
    (2, 8), (2, 12), (2, 15),
    (3, 9), (3, 13), (3, 14),
    (4, 10), (4, 13), (4, 15),
    (5, 11), (5, 12), (5, 13),
    (6, 9), (6, 12),
    (7, 11), (7, 14),
    (8, 14), (8, 15),
)
FULL_ROOT = 13
FULL_STAR = (10, 13, 17)
TRIANGLE = (0, 1, 18)  # triangle on original vertices 0,6,9

# Quotient parts: triangle first, then the remaining old vertices.
PARTS = (
    frozenset((0, 6, 9)),
    frozenset((1,)), frozenset((2,)), frozenset((3,)),
    frozenset((4,)), frozenset((5,)), frozenset((7,)),
    frozenset((8,)), frozenset((10,)), frozenset((11,)),
    frozenset((12,)), frozenset((13,)), frozenset((14,)),
    frozenset((15,)),
)
QUOTIENT_EDGES = (
    (0, 3), (1, 6), (2, 7), (0, 8), (1, 8), (4, 8),
    (1, 9), (5, 9), (6, 9), (0, 10), (2, 10), (5, 10),
    (3, 11), (4, 11), (5, 11), (3, 12), (6, 12),
    (7, 12), (2, 13), (4, 13), (7, 13),
)
QUOTIENT_TO_FULL = (
    9, 3, 6, 2, 4, 12, 5, 15, 20, 19, 7,
    16, 10, 13, 17, 11, 21, 22, 8, 14, 23,
)
QUOTIENT_ROOT = 11
QUOTIENT_STAR = (12, 13, 14)
QUOTIENT_TREES = (
    (1, 2, 3, 5, 6, 9, 10, 11, 12, 15, 16, 17, 20),
    (0, 2, 4, 6, 7, 8, 10, 11, 14, 15, 17, 18, 19),
    (0, 1, 3, 4, 5, 7, 8, 9, 13, 16, 18, 19, 20),
)

ALL_TRIANGLES = (
    frozenset((0, 6, 9)),
    frozenset((1, 7, 11)),
    frozenset((2, 8, 15)),
)


def incidence(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


def is_tree(
    order: int, edges: tuple[tuple[int, int], ...], tree: set[int]
) -> bool:
    if len(tree) != order - 1:
        return False
    rows = incidence(order, edges)
    seen = {0}
    queue = deque(seen)
    while queue:
        vertex = queue.popleft()
        for edge in rows[vertex]:
            if edge not in tree:
                continue
            left, right = edges[edge]
            other = right if left == vertex else left
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return len(seen) == order


def odd_kernel(
    order: int, edges: tuple[tuple[int, int], ...], tree: set[int]
) -> set[int]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge in tree:
        left, right = edges[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    parent = [-2] * order
    parent_edge = [-1] * order
    parent[0] = -1
    traversal = [0]
    for vertex in traversal:
        for other, edge in adjacency[vertex]:
            if parent[other] == -2:
                parent[other] = vertex
                parent_edge[other] = edge
                traversal.append(other)
    assert len(traversal) == order
    size = [1] * order
    answer: set[int] = set()
    for vertex in reversed(traversal[1:]):
        if size[vertex] % 2:
            answer.add(parent_edge[vertex])
        size[parent[vertex]] += size[vertex]
    return answer


def closure_vector(
    order: int,
    edges: tuple[tuple[int, int], ...],
    kernels: tuple[set[int], set[int], set[int]],
) -> tuple[bool, bool, bool]:
    answer = []
    for coordinate in range(3):
        parent = list(range(order))

        def find(vertex: int) -> int:
            while parent[vertex] != vertex:
                parent[vertex] = parent[parent[vertex]]
                vertex = parent[vertex]
            return vertex

        for edge in kernels[coordinate]:
            left, right = edges[edge]
            a, b = find(left), find(right)
            assert a != b
            parent[a] = b
        first, second = (
            index for index in range(3) if index != coordinate
        )
        common = kernels[first] & kernels[second]
        answer.append(
            all(
                find(edges[edge][0]) == find(edges[edge][1])
                for edge in common
            )
        )
    return tuple(answer)  # type: ignore[return-value]


def quotient_edge_map() -> tuple[int, ...]:
    answer = []
    for qleft, qright in QUOTIENT_EDGES:
        candidates = [
            edge
            for edge, (left, right) in enumerate(FULL_EDGES)
            if (
                left in PARTS[qleft] and right in PARTS[qright]
            ) or (
                right in PARTS[qleft] and left in PARTS[qright]
            )
        ]
        assert len(candidates) == 1
        answer.append(candidates[0])
    return tuple(answer)


def contract_all_triangles() -> tuple[
    tuple[frozenset[int], ...], tuple[tuple[int, int], ...]
]:
    used = set().union(*ALL_TRIANGLES)
    parts = ALL_TRIANGLES + tuple(
        frozenset((vertex,))
        for vertex in range(16)
        if vertex not in used
    )
    quotient = set()
    for left, right in FULL_EDGES:
        a = next(i for i, part in enumerate(parts) if left in part)
        b = next(i for i, part in enumerate(parts) if right in part)
        if a != b:
            quotient.add((min(a, b), max(a, b)))
    return parts, tuple(sorted(quotient))


def main() -> None:
    assert quotient_edge_map() == QUOTIENT_TO_FULL
    quotient_trees = tuple(set(tree) for tree in QUOTIENT_TREES)
    assert all(
        is_tree(14, QUOTIENT_EDGES, tree) for tree in quotient_trees
    )
    for edge in range(len(QUOTIENT_EDGES)):
        expected = 1 if edge in QUOTIENT_STAR else 2
        assert sum(edge in tree for tree in quotient_trees) == expected
    quotient_kernels = tuple(
        odd_kernel(14, QUOTIENT_EDGES, tree) for tree in quotient_trees
    )
    assert closure_vector(
        14, QUOTIENT_EDGES, quotient_kernels
    ) == (False, False, True)
    assert tuple(
        sorted(kernel & {0, 3, 9}) for kernel in quotient_kernels
    ) == ([9], [0], [0, 3, 9])

    lift_vectors = []
    for omitted in permutations(TRIANGLE):
        full_trees = tuple(
            {
                QUOTIENT_TO_FULL[edge]
                for edge in quotient_trees[coordinate]
            }
            | (set(TRIANGLE) - {omitted[coordinate]})
            for coordinate in range(3)
        )
        assert all(
            is_tree(16, FULL_EDGES, tree) for tree in full_trees
        )
        for edge in range(len(FULL_EDGES)):
            expected = 1 if edge in FULL_STAR else 2
            assert sum(edge in tree for tree in full_trees) == expected
        full_kernels = tuple(
            odd_kernel(16, FULL_EDGES, tree) for tree in full_trees
        )
        lift_vectors.append(
            closure_vector(16, FULL_EDGES, full_kernels)
        )
    assert lift_vectors == [(False, False, False)] * 6

    parts, petersen_edges = contract_all_triangles()
    assert len(parts) == 10 and len(petersen_edges) == 15
    petersen_rows = incidence(10, petersen_edges)
    assert all(len(row) == 3 for row in petersen_rows)
    # Petersen characterization sufficient here: cubic, triangle-free,
    # and every two nonadjacent vertices have exactly one common neighbour.
    adjacency = [set() for _ in range(10)]
    for left, right in petersen_edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    assert not any(
        right in adjacency[left]
        for vertex in range(10)
        for left in adjacency[vertex]
        for right in adjacency[vertex]
        if left < right
    )
    assert all(
        len(adjacency[left] & adjacency[right]) == 1
        for left in range(10)
        for right in range(left + 1, 10)
        if right not in adjacency[left]
    )
    root_part = next(
        index for index, part in enumerate(parts) if FULL_ROOT in part
    )
    expanded_parts = set(range(3))
    distance_two = {
        vertex
        for vertex in range(10)
        if vertex != root_part
        and vertex not in adjacency[root_part]
    }
    assert len(distance_two) == 6
    assert expanded_parts <= distance_two
    assert all(
        other not in adjacency[vertex]
        for vertex in expanded_parts
        for other in expanded_parts
        if vertex != other
    )
    # A 2-regular graph on these six vertices, hence the distance-two C6.
    assert all(
        len(adjacency[vertex] & distance_two) == 2
        for vertex in distance_two
    )
    assert {
        vertex
        for vertex in distance_two
        if vertex not in expanded_parts
    } == distance_two - expanded_parts
    assert all(
        other not in adjacency[vertex]
        for vertex in distance_two - expanded_parts
        for other in distance_two - expanded_parts
        if vertex != other
    )

    print("PASS")
    print(
        "contracted 14v packing closure vector=(false,false,true); "
        "all six legal lifts=(false,false,false)"
    )
    print(
        "contracting all three triangles gives Petersen; expanded "
        "vertices are one alternating class of the bad root's distance-2 C6"
    )


if __name__ == "__main__":
    main()
