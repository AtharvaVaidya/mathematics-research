#!/usr/bin/env python3
"""Literal replay of the minimum H=0 root-radius-two no-go."""

from __future__ import annotations

import itertools
from collections import deque


VERTICES = 14
EDGES = (
    (0, 6), (0, 7), (1, 7), (0, 8), (1, 8), (7, 8), (1, 9),
    (2, 9), (6, 9), (3, 10), (4, 10), (6, 10), (2, 11), (3, 11),
    (5, 11), (2, 12), (4, 12), (5, 12), (3, 13), (4, 13), (5, 13),
)
INITIAL = tuple(
    int(name, 16)
    for name in (
        "03", "05", "06", "06", "05", "03", "03",
        "09", "0a", "11", "18", "09", "11", "18",
        "09", "18", "09", "11", "09", "11", "18",
    )
)
ROOTS = (1, 20)
PAIRS = tuple(itertools.combinations(range(5), 2))
LINE = ((0, 1), (0, 2), (1, 2))
K1 = (1, 2, 3, 4)
K2 = (0, 1, 4, 5, 6, 7, 9, 11, 12, 14, 16, 17, 18, 19)
INITIAL_PATH = (
    (ROOTS[0], (0, 1), (1, 2, 3, 4)),
    (ROOTS[0], (1, 3), (0, 1, 4, 5, 6, 7, 10, 11, 15, 16)),
    (ROOTS[1], (0, 3), (16, 17, 19, 20)),
)
ENDPOINT_PATH = (
    (ROOTS[0], (0, 3), (1, 2, 3, 4)),
    (ROOTS[0], (1, 3), (0, 1, 4, 5, 6, 7, 10, 11, 15, 16)),
    (ROOTS[1], (2, 3), (16, 17, 19, 20)),
)
FINAL_COMMON = (0, 1, 4, 5, 6, 7, 9, 11, 12, 14, 18, 20)


INCIDENCE = [[] for _ in range(VERTICES)]
for edge, (left, right) in enumerate(EDGES):
    INCIDENCE[left].append(edge)
    INCIDENCE[right].append(edge)


def factor_components(state, pair):
    mask = (1 << pair[0]) | (1 << pair[1])
    unseen = {
        edge
        for edge, label in enumerate(state)
        if (label & mask).bit_count() == 1
    }
    answer = []
    while unseen:
        first = unseen.pop()
        component = {first}
        stack = [first]
        while stack:
            edge = stack.pop()
            for vertex in EDGES[edge]:
                for other in INCIDENCE[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        component.add(other)
                        stack.append(other)
        answer.append(tuple(sorted(component)))
    return tuple(sorted(answer))


def switched(state, pair, component):
    mask = (1 << pair[0]) | (1 << pair[1])
    answer = list(state)
    for edge in component:
        answer[edge] ^= mask
        assert answer[edge].bit_count() == 2
    return tuple(answer)


def root_good(state):
    for pair in PAIRS:
        for component in factor_components(state, pair):
            if all(root in component for root in ROOTS):
                return pair, component
    return None


def root_moves(state):
    assert root_good(state) is None
    for root in ROOTS:
        root_label = state[root]
        for pair in PAIRS:
            pair_mask = (1 << pair[0]) | (1 << pair[1])
            if (root_label & pair_mask).bit_count() != 1:
                continue
            component = next(
                component
                for component in factor_components(state, pair)
                if root in component
            )
            assert sum(item in component for item in ROOTS) == 1
            yield switched(state, pair, component), (root, pair, component)


def distance_at_most_two(initial):
    assert root_good(initial) is None
    first_layer = {state for state, _ in root_moves(initial)}
    assert len(tuple(root_moves(initial))) == 12
    assert not any(root_good(state) for state in first_layer)
    second_layer = {
        last
        for state in first_layer
        for last, _ in root_moves(state)
    }
    assert not any(root_good(state) for state in second_layer)


def shortest_distance(initial):
    seen = {initial}
    queue = deque([(initial, 0)])
    while queue:
        state, distance = queue.popleft()
        if root_good(state):
            return distance
        for other, _ in root_moves(state):
            if other not in seen:
                seen.add(other)
                queue.append((other, distance + 1))
    raise AssertionError("no rescue in the root-transition orbit")


def replay_path(initial, path):
    state = initial
    for root, pair, component in path:
        assert component in factor_components(state, pair)
        assert root in component
        assert sum(item in component for item in ROOTS) == 1
        state = switched(state, pair, component)
    certificate = root_good(state)
    assert certificate == ((0, 2), FINAL_COMMON)


def validate_graph_and_flow():
    assert all(len(row) == 3 for row in INCIDENCE)
    assert all(label.bit_count() == 2 for label in INITIAL)
    assert all(
        INITIAL[row[0]] ^ INITIAL[row[1]] ^ INITIAL[row[2]] == 0
        for row in INCIDENCE
    )
    assert INITIAL[ROOTS[0]] == int("05", 16)  # coordinates 02
    assert INITIAL[ROOTS[1]] == int("18", 16)  # coordinates 34
    assert not (INITIAL[ROOTS[0]] & INITIAL[ROOTS[1]])
    assert (
        INITIAL[ROOTS[0]] | INITIAL[ROOTS[1]]
    ) != 0b11111
    assert (
        __import__("functools").reduce(int.__or__, INITIAL, 0)
        == 0b11111
    )

    # Independent bridgelessness check: delete each edge and run BFS.
    for removed in range(len(EDGES)):
        seen = {0}
        queue = deque([0])
        while queue:
            vertex = queue.popleft()
            for edge in INCIDENCE[vertex]:
                if edge == removed:
                    continue
                left, right = EDGES[edge]
                other = left ^ right ^ vertex
                if other not in seen:
                    seen.add(other)
                    queue.append(other)
        assert len(seen) == VERTICES


def main():
    validate_graph_and_flow()
    assert root_good(INITIAL) is None
    state = INITIAL
    circuits = []
    for pair, expected in zip(LINE, (K1, K2, K1)):
        component = next(
            component
            for component in factor_components(state, pair)
            if ROOTS[0] in component
        )
        assert component == expected
        assert ROOTS[1] not in component
        circuits.append(component)
        state = switched(state, pair, component)
        assert root_good(state) is None

    assert circuits[0] == circuits[2]
    assert tuple(sorted(set(circuits[0]) ^ set(circuits[1]))) == (
        0, 2, 3, 5, 6, 7, 9, 11, 12, 14, 16, 17, 18, 19
    )
    endpoint = state

    distance_at_most_two(INITIAL)
    distance_at_most_two(endpoint)
    assert shortest_distance(INITIAL) == 3
    assert shortest_distance(endpoint) == 3
    replay_path(INITIAL, INITIAL_PATH)
    replay_path(endpoint, ENDPOINT_PATH)

    print(
        "PASS: order-14 H=0 line loop; both endpoints have exact "
        "root-transition rescue distance three"
    )


if __name__ == "__main__":
    main()
