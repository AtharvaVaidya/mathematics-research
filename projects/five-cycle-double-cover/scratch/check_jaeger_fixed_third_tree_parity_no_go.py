#!/usr/bin/env python3
"""Exact cube no-go for a fixed-third-tree parity-extension lemma.

For the star fibre 2G-delta(0), the displayed spanning tree T3 has 16
ordered completions to a three-tree partition.  None makes K(T1) cap
K(T2) have even boundary on every component of K(T3).  A different T3
does work, so this is not a counterexample to the existential Jaeger
star-fibre lemma.

Only the Python standard library is used.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations


# This is K_{4,4} minus the matching 07,16,25,34, hence the cube.
EDGES = (
    (0, 4), (0, 5), (0, 6),
    (1, 4), (1, 5), (1, 7),
    (2, 4), (2, 6), (2, 7),
    (3, 5), (3, 6), (3, 7),
)
VERTEX_COUNT = 8
ROOT = 0
ROOT_STAR = frozenset((0, 1, 2))
FIXED_T3 = frozenset((0, 3, 4, 7, 8, 9, 11))

# Swapping T1 and T2 accounts for the other eight ordered extensions.
# The normalization is root edge 1 in T1 and root edge 2 in T2.
EXPECTED_NORMALIZED = (
    (
        (1, 3, 4, 5, 6, 7, 10),
        (2, 5, 6, 8, 9, 10, 11),
        (2, 5, 6, 9),
        (5, 6),
    ),
    (
        (1, 3, 4, 5, 6, 10, 11),
        (2, 5, 6, 7, 8, 9, 10),
        (2, 5, 6, 9),
        (5, 6),
    ),
    (
        (1, 3, 5, 6, 7, 9, 10),
        (2, 4, 5, 6, 8, 10, 11),
        (2, 4, 6, 11),
        (6,),
    ),
    (
        (1, 3, 5, 6, 9, 10, 11),
        (2, 4, 5, 6, 7, 8, 10),
        (2, 4, 6, 7, 8, 10),
        (6, 10),
    ),
    (
        (1, 4, 5, 6, 7, 8, 10),
        (2, 3, 5, 6, 9, 10, 11),
        (2, 5, 6, 9),
        (5, 6),
    ),
    (
        (1, 4, 5, 6, 8, 10, 11),
        (2, 3, 5, 6, 7, 9, 10),
        (2, 5, 6, 9),
        (5, 6),
    ),
    (
        (1, 5, 6, 7, 8, 9, 10),
        (2, 3, 4, 5, 6, 10, 11),
        (2, 4, 6, 11),
        (6,),
    ),
    (
        (1, 5, 6, 8, 9, 10, 11),
        (2, 3, 4, 5, 6, 7, 10),
        (2, 3, 4, 5, 7, 10),
        (5, 10),
    ),
)

SUCCESSFUL_TRIPLE = (
    frozenset((1, 3, 4, 7, 8, 9, 11)),
    frozenset((2, 5, 6, 8, 9, 10, 11)),
    frozenset((0, 3, 4, 5, 6, 7, 10)),
)


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


def is_spanning_tree(tree: frozenset[int]) -> bool:
    if len(tree) != VERTEX_COUNT - 1:
        return False
    parent = list(range(VERTEX_COUNT))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in tree:
        left, right = EDGES[edge]
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            return False
        parent[left_root] = right_root
    root = find(0)
    return all(find(vertex) == root for vertex in range(VERTEX_COUNT))


def spanning_trees() -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(chosen)
        for chosen in combinations(range(len(EDGES)), VERTEX_COUNT - 1)
        if is_spanning_tree(frozenset(chosen))
    )


def all_odd(edge_set: frozenset[int]) -> bool:
    return all(
        sum(edge in edge_set for edge in row) % 2 == 1
        for row in INCIDENCE
    )


def odd_kernel(tree: frozenset[int]) -> frozenset[int]:
    """The unique all-vertices-odd subgraph K(T) contained in a tree."""
    tree_adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(VERTEX_COUNT)
    ]
    for edge in tree:
        left, right = EDGES[edge]
        tree_adjacency[left].append((right, edge))
        tree_adjacency[right].append((left, edge))

    parent = [-1] * VERTEX_COUNT
    parent_edge = [-1] * VERTEX_COUNT
    parent[0] = 0
    order = [0]
    for vertex in order:
        for other, edge in tree_adjacency[vertex]:
            if parent[other] < 0:
                parent[other] = vertex
                parent_edge[other] = edge
                order.append(other)
    assert len(order) == VERTEX_COUNT

    subtree_size = [1] * VERTEX_COUNT
    answer = set()
    for vertex in reversed(order[1:]):
        if subtree_size[vertex] % 2 == 1:
            answer.add(parent_edge[vertex])
        subtree_size[parent[vertex]] += subtree_size[vertex]
    kernel = frozenset(answer)
    assert kernel <= tree
    assert all_odd(kernel)
    return kernel


def components(edge_set: frozenset[int]) -> tuple[frozenset[int], ...]:
    unseen = set(range(VERTEX_COUNT))
    answer = []
    while unseen:
        start = min(unseen)
        component = {start}
        queue = [start]
        while queue:
            vertex = queue.pop()
            for edge in INCIDENCE[vertex]:
                if edge not in edge_set:
                    continue
                left, right = EDGES[edge]
                other = right if left == vertex else left
                if other not in component:
                    component.add(other)
                    queue.append(other)
        unseen -= component
        answer.append(frozenset(component))
    return tuple(answer)


def boundary(
    edge_set: frozenset[int], vertices: frozenset[int]
) -> frozenset[int]:
    return frozenset(
        edge
        for edge in edge_set
        if ((EDGES[edge][0] in vertices) ^ (EDGES[edge][1] in vertices))
    )


def parity_good(
    first: frozenset[int],
    second: frozenset[int],
    third: frozenset[int],
) -> bool:
    common = odd_kernel(first) & odd_kernel(second)
    return all(
        len(boundary(common, component)) % 2 == 0
        for component in components(odd_kernel(third))
    )


def star_multiplicity(edge: int) -> int:
    return 1 if edge in ROOT_STAR else 2


def is_star_partition(
    triple: tuple[frozenset[int], frozenset[int], frozenset[int]]
) -> bool:
    return (
        all(is_spanning_tree(tree) for tree in triple)
        and all(
            sum(edge in tree for tree in triple) == star_multiplicity(edge)
            for edge in range(len(EDGES))
        )
    )


def extensions(
    third: frozenset[int],
    trees: tuple[frozenset[int], ...],
) -> tuple[tuple[frozenset[int], frozenset[int]], ...]:
    tree_set = set(trees)
    answer = []
    for first in trees:
        second = set()
        valid = True
        for edge in range(len(EDGES)):
            remaining = star_multiplicity(edge) - (edge in third)
            second_copy = remaining - (edge in first)
            if second_copy not in (0, 1):
                valid = False
                break
            if second_copy:
                second.add(edge)
        frozen_second = frozenset(second)
        if valid and frozen_second in tree_set:
            answer.append((first, frozen_second))
    return tuple(answer)


def main() -> None:
    assert len(EDGES) == 12
    assert all(left != right for left, right in EDGES)
    assert len({frozenset(edge) for edge in EDGES}) == len(EDGES)
    assert all(len(row) == 3 for row in INCIDENCE)
    assert connected()
    assert all(
        connected(frozenset(deleted))
        for size in (1, 2)
        for deleted in combinations(range(len(EDGES)), size)
    )

    trees = spanning_trees()
    assert len(trees) == 384
    # Independently confirm uniqueness of K(T) for every literal tree.
    for tree in trees:
        candidates = []
        tree_edges = tuple(sorted(tree))
        for mask in range(1 << len(tree_edges)):
            candidate = frozenset(
                tree_edges[index]
                for index in range(len(tree_edges))
                if (mask >> index) & 1
            )
            if all_odd(candidate):
                candidates.append(candidate)
        assert candidates == [odd_kernel(tree)]

    assert is_spanning_tree(FIXED_T3)
    assert FIXED_T3 & ROOT_STAR == {0}
    fixed_extensions = extensions(FIXED_T3, trees)
    assert len(fixed_extensions) == 16
    assert all(
        is_star_partition((first, second, FIXED_T3))
        for first, second in fixed_extensions
    )
    assert all(
        not parity_good(first, second, FIXED_T3)
        for first, second in fixed_extensions
    )

    fixed_k3 = odd_kernel(FIXED_T3)
    assert fixed_k3 == {0, 4, 7, 11}
    assert components(fixed_k3) == (
        frozenset((0, 4)),
        frozenset((1, 5)),
        frozenset((2, 6)),
        frozenset((3, 7)),
    )

    normalized = []
    for first, second in fixed_extensions:
        if 1 not in first:
            continue
        first_k = odd_kernel(first)
        second_k = odd_kernel(second)
        assert first_k == {1, 5, 6, 10}
        normalized.append(
            (
                tuple(sorted(first)),
                tuple(sorted(second)),
                tuple(sorted(second_k)),
                tuple(sorted(first_k & second_k)),
            )
        )
    assert tuple(sorted(normalized)) == tuple(sorted(EXPECTED_NORMALIZED))

    # The obstruction is exactly an odd-degree quotient: K3 has the
    # displayed four matching components, while every possible
    # K1-intersection-K2 is one of these four non-Eulerian edge sets.
    possible_common = {
        odd_kernel(first) & odd_kernel(second)
        for first, second in fixed_extensions
    }
    assert possible_common == {
        frozenset((5, 6)),
        frozenset((6,)),
        frozenset((6, 10)),
        frozenset((5, 10)),
    }
    assert all(
        any(
            len(boundary(common, component)) % 2 == 1
            for component in components(fixed_k3)
        )
        for common in possible_common
    )

    # Scope check: the original existential star-fibre statement still
    # succeeds on this graph and root when T3 is chosen jointly.
    assert is_star_partition(SUCCESSFUL_TRIPLE)
    assert parity_good(*SUCCESSFUL_TRIPLE)
    assert odd_kernel(SUCCESSFUL_TRIPLE[0]) & odd_kernel(
        SUCCESSFUL_TRIPLE[1]
    ) == frozenset()

    feasible_third = []
    bad_third = []
    for third in trees:
        completions = extensions(third, trees)
        if not completions:
            continue
        feasible_third.append(third)
        if not any(parity_good(first, second, third)
                   for first, second in completions):
            bad_third.append(third)
    assert len(feasible_third) == 132
    assert len(bad_third) == 12
    assert FIXED_T3 in bad_third

    print("PASS")
    print("graph=cube n=8 m=12 simple cubic 3-edge-connected")
    print("root=0 star_edges=0,1,2")
    print("fixed_T3=0,3,4,7,8,9,11")
    print("K3=0,4,7,11 (four matching components)")
    print("ordered_extensions=16 normalized_extensions=8")
    print("successful_fixed_T3_extensions=0")
    print("possible_K1_intersection_K2=5,6 | 6 | 6,10 | 5,10")
    print("feasible_T3=132 bad_T3=12")
    print("scope=fixed-third-tree extension lemma false; existential lemma survives")


if __name__ == "__main__":
    main()
