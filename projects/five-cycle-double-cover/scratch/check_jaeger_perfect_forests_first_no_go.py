#!/usr/bin/env python3
"""Exact no-go for choosing Scott-perfect forests before tree extension.

Three capacity-respecting perfect forests in a 10-vertex cubic graph
already satisfy the Jaeger component-parity target, but cannot be
simultaneously extended to a partition of 2G-delta(r) into three trees.

Only the Python standard library is used.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations


# A labelled presentation of the 10-vertex Möbius ladder.
EDGES = (
    (0, 5), (0, 6), (0, 7),
    (1, 5), (1, 7), (1, 8),
    (2, 5), (2, 8), (2, 9),
    (3, 6), (3, 7), (3, 9),
    (4, 6), (4, 8), (4, 9),
)
VERTEX_COUNT = 10
ROOT = 0
ROOT_STAR = frozenset((0, 1, 2))

KERNELS = (
    frozenset((0, 4, 7, 11, 12)),
    frozenset((1, 5, 6, 10, 14)),
    frozenset((2, 5, 6, 11, 12)),
)

# A separate positive choice on the same graph and root.  This binds the
# scope: the no-go is to universal forest-first extension, not to the
# existential star-fibre parity lemma.
SUCCESS_KERNELS = (
    frozenset((0, 5, 8, 10, 12)),
    frozenset((1, 4, 6, 11, 13)),
    frozenset((2, 4, 6, 7, 8, 10, 12)),
)
SUCCESS_TREES = (
    frozenset((0, 3, 5, 7, 8, 10, 11, 12, 13)),
    frozenset((1, 3, 4, 5, 6, 9, 11, 13, 14)),
    frozenset((2, 4, 6, 7, 8, 9, 10, 12, 14)),
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


def component_partition(
    edge_set: frozenset[int],
) -> tuple[frozenset[int], ...]:
    unseen = set(range(VERTEX_COUNT))
    answer = []
    while unseen:
        start = min(unseen)
        component = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for edge in INCIDENCE[vertex]:
                if edge not in edge_set:
                    continue
                left, right = EDGES[edge]
                other = right if left == vertex else left
                if other not in component:
                    component.add(other)
                    stack.append(other)
        unseen -= component
        answer.append(frozenset(component))
    return tuple(answer)


def is_forest(edge_set: frozenset[int]) -> bool:
    return len(edge_set) == VERTEX_COUNT - len(
        component_partition(edge_set)
    )


def all_odd(edge_set: frozenset[int]) -> bool:
    return all(
        sum(edge in edge_set for edge in row) % 2 == 1
        for row in INCIDENCE
    )


def is_scott_perfect_forest(edge_set: frozenset[int]) -> bool:
    if not is_forest(edge_set) or not all_odd(edge_set):
        return False
    for component in component_partition(edge_set):
        for edge, (left, right) in enumerate(EDGES):
            if left in component and right in component and edge not in edge_set:
                return False
    return True


def is_spanning_tree(edge_set: frozenset[int]) -> bool:
    return (
        len(edge_set) == VERTEX_COUNT - 1
        and len(component_partition(edge_set)) == 1
    )


def odd_kernel(tree: frozenset[int]) -> frozenset[int]:
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
    result = frozenset(answer)
    assert all_odd(result)
    return result


def multiplicity(edge: int) -> int:
    return 1 if edge in ROOT_STAR else 2


def capacity_respecting(
    kernels: tuple[frozenset[int], ...],
) -> bool:
    return all(
        sum(edge in kernel for kernel in kernels) <= multiplicity(edge)
        for edge in range(len(EDGES))
    )


def component_parity_good(
    kernels: tuple[frozenset[int], ...],
) -> bool:
    common = kernels[0] & kernels[1]
    for component in component_partition(kernels[2]):
        boundary_size = sum(
            edge in common
            and ((left in component) ^ (right in component))
            for edge, (left, right) in enumerate(EDGES)
        )
        if boundary_size % 2:
            return False
    return True


def residual_copies(
    kernels: tuple[frozenset[int], ...],
) -> tuple[tuple[int, int], ...]:
    answer = []
    for edge in range(len(EDGES)):
        count = multiplicity(edge) - sum(
            edge in kernel for kernel in kernels
        )
        assert count >= 0
        answer.extend((edge, copy) for copy in range(count))
    return tuple(answer)


def contracted_graphic_rank(
    kernel: frozenset[int],
    copies: tuple[tuple[int, int], ...],
) -> int:
    """Rank of displayed copies in the graphic matroid contracted by K."""
    parent = list(range(VERTEX_COUNT))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in kernel:
        left, right = EDGES[edge]
        left_root, right_root = find(left), find(right)
        assert left_root != right_root
        parent[left_root] = right_root

    rank = 0
    for edge, _copy in copies:
        left, right = EDGES[edge]
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[left_root] = right_root
            rank += 1
    return rank


def canonical_partition(edge_set: frozenset[int]) -> tuple[int, ...]:
    components = component_partition(edge_set)
    return tuple(
        next(index for index, component in enumerate(components)
             if vertex in component)
        for vertex in range(VERTEX_COUNT)
    )


def merged_partition(
    partition: tuple[int, ...], left: int, right: int
) -> tuple[int, ...] | None:
    first, second = partition[left], partition[right]
    if first == second:
        return None
    raw = tuple(first if value == second else value for value in partition)
    relabel: dict[int, int] = {}
    return tuple(
        relabel.setdefault(value, len(relabel))
        for value in raw
    )


def extension_count(
    kernels: tuple[frozenset[int], ...],
) -> int:
    """Directly count acyclic assignments of all residual copies."""
    copies = residual_copies(kernels)
    initial = tuple(canonical_partition(kernel) for kernel in kernels)
    memo: dict[
        tuple[int, tuple[tuple[int, ...], ...]], int
    ] = {}

    def search(
        position: int, partitions: tuple[tuple[int, ...], ...]
    ) -> int:
        if position == len(copies):
            return int(all(len(set(partition)) == 1
                           for partition in partitions))
        key = (position, partitions)
        if key in memo:
            return memo[key]
        edge, _copy = copies[position]
        left, right = EDGES[edge]
        answer = 0
        for coordinate in range(3):
            updated = merged_partition(
                partitions[coordinate], left, right
            )
            if updated is None:
                continue
            next_partitions = list(partitions)
            next_partitions[coordinate] = updated
            answer += search(position + 1, tuple(next_partitions))
        memo[key] = answer
        return answer

    return search(0, initial)


def is_star_partition(
    trees: tuple[frozenset[int], ...],
) -> bool:
    return (
        all(is_spanning_tree(tree) for tree in trees)
        and all(
            sum(edge in tree for tree in trees) == multiplicity(edge)
            for edge in range(len(EDGES))
        )
    )


def main() -> None:
    assert len(EDGES) == 15
    assert all(left != right for left, right in EDGES)
    assert len({frozenset(edge) for edge in EDGES}) == len(EDGES)
    assert all(len(row) == 3 for row in INCIDENCE)
    assert connected()
    assert all(
        connected(frozenset(deleted))
        for size in (1, 2)
        for deleted in combinations(range(len(EDGES)), size)
    )

    assert all(is_scott_perfect_forest(kernel) for kernel in KERNELS)
    assert all(len(kernel) == 5 for kernel in KERNELS)
    assert all(
        all(len(component) == 2
            for component in component_partition(kernel))
        for kernel in KERNELS
    )
    assert KERNELS[0] & KERNELS[1] == frozenset()
    assert capacity_respecting(KERNELS)
    assert component_parity_good(KERNELS)
    assert tuple(kernel & ROOT_STAR for kernel in KERNELS) == (
        frozenset((0,)),
        frozenset((1,)),
        frozenset((2,)),
    )

    copies = residual_copies(KERNELS)
    assert copies == (
        (3, 0), (3, 1), (4, 0), (7, 0),
        (8, 0), (8, 1), (9, 0), (9, 1),
        (10, 0), (13, 0), (13, 1), (14, 0),
    )
    obstruction = tuple(
        copy for index, copy in enumerate(copies) if index not in (2, 8)
    )
    assert len(obstruction) == 10
    assert tuple(
        contracted_graphic_rank(kernel, obstruction)
        for kernel in KERNELS
    ) == (3, 3, 3)
    expected_joined_components = (
        (
            frozenset((0, 1, 5, 7)),
            frozenset((2, 3, 4, 6, 8, 9)),
        ),
        (
            frozenset((0, 3, 6, 7)),
            frozenset((1, 2, 4, 5, 8, 9)),
        ),
        (
            frozenset((0, 7)),
            frozenset((1, 2, 3, 4, 5, 6, 8, 9)),
        ),
    )
    obstruction_edges = frozenset(edge for edge, _copy in obstruction)
    assert tuple(
        component_partition(kernel | obstruction_edges)
        for kernel in KERNELS
    ) == expected_joined_components
    # Independent exhaustive replay of the same nonextension claim.
    assert extension_count(KERNELS) == 0

    # Scope check: another perfect-forest choice does extend and satisfies
    # component parity on the same graph and root.
    assert all(
        is_scott_perfect_forest(kernel) for kernel in SUCCESS_KERNELS
    )
    assert capacity_respecting(SUCCESS_KERNELS)
    assert component_parity_good(SUCCESS_KERNELS)
    assert is_star_partition(SUCCESS_TREES)
    assert tuple(odd_kernel(tree) for tree in SUCCESS_TREES) == (
        SUCCESS_KERNELS
    )

    print("PASS")
    print("graph=10-vertex Mobius ladder; n=10 m=15; 3-edge-connected")
    print("root=0 star_edges=0,1,2")
    print("chosen_K_sizes=5,5,5 (three Scott-perfect matchings)")
    print("K1_intersection_K2=empty; component_parity=good")
    print("residual_copies=12 obstruction_copies=10")
    print("contracted_ranks=3,3,3; rank_sum=9<10")
    print("simultaneous_extensions=0")
    print("scope=universal forests-first extension false; existential lemma survives")


if __name__ == "__main__":
    main()
