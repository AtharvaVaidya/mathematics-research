#!/usr/bin/env python3
"""Dependency-free exhaustive replay of the Petersen obstruction."""

from __future__ import annotations

from collections import Counter, deque


EDGES = (
    (0, 3),
    (0, 6),
    (0, 9),
    (1, 4),
    (1, 6),
    (1, 8),
    (2, 5),
    (2, 6),
    (2, 7),
    (3, 7),
    (3, 8),
    (4, 7),
    (4, 9),
    (5, 8),
    (5, 9),
)
MATCHING = frozenset((1, 3, 6))
EXPECTED_MINIMUM_CYCLES = {
    frozenset((1, 2, 3, 5, 6, 7, 12, 13)),
    frozenset((1, 2, 3, 4, 6, 8, 11, 14)),
}


def is_even(edge_set: frozenset[int]) -> bool:
    degree = [0] * 10
    for edge in edge_set:
        left, right = EDGES[edge]
        degree[left] ^= 1
        degree[right] ^= 1
    return not any(degree)


def components(edge_set: frozenset[int]) -> tuple[frozenset[int], ...]:
    adjacency = [[] for _ in range(10)]
    for edge in edge_set:
        left, right = EDGES[edge]
        adjacency[left].append(right)
        adjacency[right].append(left)
    unseen = set(range(10))
    result = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        queue = deque((root,))
        component = {root}
        while queue:
            vertex = queue.popleft()
            for other in adjacency[vertex]:
                if other in unseen:
                    unseen.remove(other)
                    component.add(other)
                    queue.append(other)
        result.append(frozenset(component))
    return tuple(result)


def terminal_parity(component: frozenset[int]) -> int:
    count = 0
    for edge in MATCHING:
        left, right = EDGES[edge]
        count += left in component
        count += right in component
    return count & 1


def main() -> None:
    assert len(EDGES) == 15
    assert len(set(EDGES)) == 15
    assert all(left < right for left, right in EDGES)
    assert all(
        sum(vertex in edge for edge in EDGES) == 3 for vertex in range(10)
    )
    matching_vertices = [vertex for edge in MATCHING for vertex in EDGES[edge]]
    assert len(set(matching_vertices)) == 2 * len(MATCHING)

    cycles = []
    for mask in range(1 << len(EDGES)):
        edge_set = frozenset(
            edge for edge in range(len(EDGES)) if (mask >> edge) & 1
        )
        if is_even(edge_set):
            cycles.append(edge_set)
    assert len(cycles) == 64

    containing = [cycle for cycle in cycles if MATCHING <= cycle]
    assert len(containing) == 8
    assert Counter(map(len, containing)) == Counter({8: 2, 9: 4, 10: 2})
    minimum = min(map(len, containing))
    minimum_cycles = {cycle for cycle in containing if len(cycle) == minimum}
    assert minimum == 8
    assert minimum_cycles == EXPECTED_MINIMUM_CYCLES

    all_edges = frozenset(range(len(EDGES)))
    expected_rows = {
        frozenset((1, 2, 3, 5, 6, 7, 12, 13)): (
            (frozenset((0, 2, 3, 4, 7, 8)), frozenset((1, 6)), frozenset((5, 9))),
            (1, 0, 1),
        ),
        frozenset((1, 2, 3, 4, 6, 8, 11, 14)): (
            (frozenset((0, 1, 3, 5, 7, 8)), frozenset((2, 6)), frozenset((4, 9))),
            (1, 0, 1),
        ),
    }
    for cycle in sorted(minimum_cycles, key=lambda item: sorted(item)):
        complement_components = components(all_edges - cycle)
        parities = tuple(map(terminal_parity, complement_components))
        assert (complement_components, parities) == expected_rows[cycle]
        assert any(parities)

    print(
        "PASS: 64 binary cycles; 8 contain M; minimum profile "
        "{8:2,9:4,10:2}; both minimum complements have parity (1,0,1)."
    )


if __name__ == "__main__":
    main()
