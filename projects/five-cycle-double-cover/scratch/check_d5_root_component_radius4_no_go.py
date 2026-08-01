#!/usr/bin/env python3
"""Independent literal replay of the minimum-order radius-three no-go."""

from __future__ import annotations

import itertools
from collections import deque


VERTICES = 14
EDGES = (
    (0, 5), (0, 7), (0, 9), (1, 6), (1, 8), (1, 13), (2, 7),
    (2, 9), (2, 10), (3, 8), (3, 11), (3, 12), (4, 10), (4, 11),
    (4, 12), (5, 10), (5, 11), (6, 12), (6, 13), (7, 9), (8, 13),
)
ROOTS = (3, 6)
INITIAL = tuple(
    int(name, 16)
    for name in (
        "03", "05", "06", "05", "06", "03", "06",
        "05", "03", "03", "06", "05", "05", "03",
        "06", "06", "05", "03", "06", "03", "05",
    )
)
PATH = (
    ((0, 1), (1, 2, 6, 7)),
    ((0, 1), (3, 4, 18, 20)),
    ((0, 3), (0, 2, 6, 8, 12, 13, 16, 19)),
    ((1, 4), (3, 5, 9, 10, 13, 14, 17, 20)),
)
ROOT_LABEL_PATH = (
    ("02", "12"),
    ("02", "02"),
    ("12", "02"),
    ("12", "23"),
    ("24", "23"),
)
FINAL_RESCUE_COMPONENT = (
    0, 2, 3, 5, 6, 8, 9, 10, 12, 14, 16, 17, 19, 20,
)
PAIRS = tuple(itertools.combinations(range(5), 2))


INCIDENCE = [[] for _ in range(VERTICES)]
for edge, (left, right) in enumerate(EDGES):
    INCIDENCE[left].append(edge)
    INCIDENCE[right].append(edge)


def components(selected: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    unseen = set(selected)
    answer = []
    while unseen:
        first = unseen.pop()
        component = {first}
        queue = [first]
        while queue:
            edge = queue.pop()
            for vertex in EDGES[edge]:
                for other in INCIDENCE[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        component.add(other)
                        queue.append(other)
        answer.append(tuple(sorted(component)))
    return tuple(sorted(answer))


def factor_components(
    state: tuple[int, ...],
    pair: tuple[int, int],
) -> tuple[tuple[int, ...], ...]:
    mask = (1 << pair[0]) | (1 << pair[1])
    return components(tuple(
        edge
        for edge, label in enumerate(state)
        if (label & mask).bit_count() == 1
    ))


def switched(
    state: tuple[int, ...],
    pair: tuple[int, int],
    component: tuple[int, ...],
) -> tuple[int, ...]:
    mask = (1 << pair[0]) | (1 << pair[1])
    result = list(state)
    for edge in component:
        result[edge] ^= mask
        assert result[edge].bit_count() == 2
    return tuple(result)


def root_good(state: tuple[int, ...]) -> bool:
    return any(
        ROOTS[0] in component and ROOTS[1] in component
        for pair in PAIRS
        for component in factor_components(state, pair)
    )


def root_component_moves(state: tuple[int, ...]):
    assert not root_good(state)
    for pair in PAIRS:
        for component in factor_components(state, pair):
            if sum(root in component for root in ROOTS) != 1:
                continue
            yield switched(state, pair, component), pair, component


def coordinate_profile(state: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        len(components(tuple(
            edge
            for edge, label in enumerate(state)
            if (label >> coordinate) & 1
        )))
        for coordinate in range(5)
    )


def label_name(label: int) -> str:
    return "".join(
        str(coordinate)
        for coordinate in range(5)
        if (label >> coordinate) & 1
    )


def validate_graph_and_flow() -> None:
    assert len(set(EDGES)) == len(EDGES)
    assert all(left != right for left, right in EDGES)
    assert all(len(row) == 3 for row in INCIDENCE)
    assert all(label.bit_count() == 2 for label in INITIAL)
    for row in INCIDENCE:
        assert INITIAL[row[0]] ^ INITIAL[row[1]] ^ INITIAL[row[2]] == 0
    for removed in range(len(EDGES)):
        seen = {0}
        queue = deque([0])
        while queue:
            vertex = queue.popleft()
            for edge in INCIDENCE[vertex]:
                if edge == removed:
                    continue
                other = EDGES[edge][0] ^ EDGES[edge][1] ^ vertex
                if other not in seen:
                    seen.add(other)
                    queue.append(other)
        assert len(seen) == VERTICES


def exhaustive_shortest_distance() -> tuple[int, tuple[int, ...]]:
    seen = {INITIAL}
    queue = deque([(INITIAL, 0)])
    while queue:
        state, distance = queue.popleft()
        if root_good(state):
            return distance, state
        for other, _, _ in root_component_moves(state):
            if other not in seen:
                seen.add(other)
                queue.append((other, distance + 1))
    raise AssertionError("root-component orbit has no rescue")


def replay_four_switch_path() -> None:
    states = [INITIAL]
    for pair, component in PATH:
        assert component in factor_components(states[-1], pair)
        assert sum(root in component for root in ROOTS) == 1
        states.append(switched(states[-1], pair, component))
    observed_labels = tuple(
        (
            label_name(state[ROOTS[0]]),
            label_name(state[ROOTS[1]]),
        )
        for state in states
    )
    assert observed_labels == ROOT_LABEL_PATH
    assert not any(root_good(state) for state in states[:-1])
    assert root_good(states[-1])
    assert FINAL_RESCUE_COMPONENT in factor_components(
        states[-1], (3, 4)
    )


def main() -> None:
    validate_graph_and_flow()
    assert coordinate_profile(INITIAL) == (2, 2, 3, 0, 0)
    replay_four_switch_path()
    shortest, rescued_state = exhaustive_shortest_distance()
    assert shortest == 4
    assert root_good(rescued_state)
    print(
        "PASS: exhaustive literal BFS finds no rescue within three "
        "root-component switches and shortest rescue distance four"
    )


if __name__ == "__main__":
    main()
