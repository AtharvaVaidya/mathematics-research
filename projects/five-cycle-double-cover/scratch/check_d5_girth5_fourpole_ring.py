#!/usr/bin/env python3
"""Test the natural ring iteration of the girth-five order-16 four-pole."""

from __future__ import annotations

import itertools
from collections import deque


A, B, C = 0x03, 0x05, 0x06
PAIRS = tuple(itertools.combinations(range(5), 2))
EXPECTED_MAXIMUM = {2: 3, 3: 1, 4: 3, 5: 1, 6: 3}


def fourpole_ring(poles: int):
    """Substitute one 8-vertex four-pole at each vertex of a doubled cycle."""
    assert poles >= 2
    edges = []
    state = []
    local_edges = []

    def add(left, right, label):
        edges.append((left, right))
        state.append(label)
        return len(edges) - 1

    # Local vertices 0,...,3 are cubic cores; 4,...,7 are terminals.
    # Every external terminal edge has label A.
    pattern = (
        (0, 2, A), (1, 3, A),
        (4, 0, B), (4, 1, C),
        (5, 1, B), (5, 2, C),
        (6, 0, C), (6, 3, B),
        (7, 2, B), (7, 3, C),
    )
    for pole in range(poles):
        offset = 8 * pole
        row = []
        for left, right, label in pattern:
            row.append(add(offset + left, offset + right, label))
        local_edges.append(tuple(row))
    for pole in range(poles):
        following = (pole + 1) % poles
        add(8 * pole + 6, 8 * following + 4, A)
        add(8 * pole + 7, 8 * following + 5, A)
    return tuple(edges), tuple(state), tuple(local_edges)


def incidence_rows(vertices, edges, removed=frozenset()):
    rows = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        if edge in removed:
            continue
        rows[left].append((edge, right))
        rows[right].append((edge, left))
    return rows


def vertex_components(vertices, edges, removed=frozenset()):
    rows = incidence_rows(vertices, edges, removed)
    unseen = set(range(vertices))
    answer = []
    while unseen:
        first = unseen.pop()
        component = {first}
        queue = [first]
        while queue:
            vertex = queue.pop()
            for _, other in rows[vertex]:
                if other in unseen:
                    unseen.remove(other)
                    component.add(other)
                    queue.append(other)
        answer.append(component)
    return answer


def component_has_cycle(component, edges, removed):
    internal = sum(
        edge not in removed and left in component and right in component
        for edge, (left, right) in enumerate(edges)
    )
    return internal >= len(component)


def validate_graph_and_flow(edges, state, poles):
    vertices = 8 * poles
    assert len(edges) == 12 * poles
    assert len(set(tuple(sorted(edge)) for edge in edges)) == len(edges)
    rows = incidence_rows(vertices, edges)
    assert all(len(row) == 3 for row in rows)
    assert all(
        state[row[0][0]] ^ state[row[1][0]] ^ state[row[2][0]] == 0
        for row in rows
    )

    # Girth at least five: no triangle or quadrilateral.
    adjacency = [{other for _, other in row} for row in rows]
    assert not any(
        right in adjacency[left]
        for vertex in range(vertices)
        for left, right in itertools.combinations(adjacency[vertex], 2)
    )
    assert not any(
        len(adjacency[left] & adjacency[right]) >= 2
        for left, right in itertools.combinations(range(vertices), 2)
        if right not in adjacency[left]
    )

    # No cyclic edge cut of size at most three.
    for size in range(1, 4):
        for cut in itertools.combinations(range(len(edges)), size):
            components = vertex_components(vertices, edges, frozenset(cut))
            cyclic = sum(
                component_has_cycle(component, edges, frozenset(cut))
                for component in components
            )
            assert cyclic < 2


def factor_context(edges):
    vertices = 1 + max(max(edge) for edge in edges)
    rows = incidence_rows(vertices, edges)

    def components(selected):
        unseen = set(selected)
        answer = []
        while unseen:
            first = unseen.pop()
            component = {first}
            queue = [first]
            while queue:
                edge = queue.pop()
                for vertex in edges[edge]:
                    for other, _ in rows[vertex]:
                        if other in unseen:
                            unseen.remove(other)
                            component.add(other)
                            queue.append(other)
            answer.append(component)
        return answer

    def factor_components(state, pair):
        mask = (1 << pair[0]) | (1 << pair[1])
        return components(
            edge
            for edge, label in enumerate(state)
            if (label & mask).bit_count() == 1
        )

    return factor_components


def shortest_distance(edges, initial, roots, factor_components):
    def root_good(state):
        return any(
            all(root in component for root in roots)
            for pair in PAIRS
            for component in factor_components(state, pair)
        )

    if root_good(initial):
        return 0
    seen = {initial}
    queue = deque([(initial, 0)])
    while queue:
        state, distance = queue.popleft()
        for pair in PAIRS:
            mask = (1 << pair[0]) | (1 << pair[1])
            for component in factor_components(state, pair):
                if sum(root in component for root in roots) != 1:
                    continue
                other = list(state)
                for edge in component:
                    other[edge] ^= mask
                other = tuple(other)
                if other in seen:
                    continue
                if root_good(other):
                    return distance + 1
                seen.add(other)
                queue.append((other, distance + 1))
    raise AssertionError("root-component orbit has no rescue")


def main():
    for poles, expected in EXPECTED_MAXIMUM.items():
        edges, state, local = fourpole_ring(poles)
        validate_graph_and_flow(edges, state, poles)
        factors = factor_context(edges)
        opposite = poles // 2
        distances = []
        for left in local[0]:
            for right in local[opposite]:
                distances.append(
                    shortest_distance(edges, state, (left, right), factors)
                )
        maximum = max(distances)
        assert maximum == expected
        print(
            f"{poles} poles: vertices={8 * poles}, girth>=5, "
            f"cyclic edge connectivity>=4, cross-pole maximum={maximum}"
        )
    print("PASS: the natural four-pole ring has bounded observed radius")


if __name__ == "__main__":
    main()
