#!/usr/bin/env python3
"""Independent literal replay of the minimum-order radius-four no-go."""

from __future__ import annotations

import itertools
from collections import deque


GRAPH6 = "O??CAA_SD@DOB_F?AgAA_"
VERTICES = 16
EDGES = (
    (0, 6), (1, 7), (0, 8), (2, 8), (1, 9), (3, 9),
    (0, 10), (2, 10), (8, 10), (2, 11), (4, 11), (6, 11),
    (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
    (3, 14), (5, 14), (7, 14), (1, 15), (7, 15), (9, 15),
)
ROOTS = (1, 3)
INITIAL = tuple(
    int(name, 16)
    for name in (
        "03", "03", "05", "06", "05", "06",
        "06", "05", "03", "03", "06", "05",
        "03", "05", "06", "03", "05", "06",
        "05", "03", "06", "06", "05", "03",
    )
)
PATH = (
    ((0, 1), (2, 3, 6, 7)),
    ((0, 3), (0, 3, 6, 8, 9, 11)),
    ((1, 3), (2, 3, 6, 7)),
    ((0, 1), (0, 3, 6, 8, 9, 10, 13, 14, 16, 17)),
    ((0, 4), (0, 3, 6, 8, 9, 10, 12, 14)),
)
ROOT_LABEL_PATH = (
    ("01", "12"),
    ("01", "02"),
    ("01", "23"),
    ("01", "12"),
    ("01", "02"),
    ("01", "24"),
)
FINAL_RESCUE_COMPONENT = (
    0, 1, 3, 5, 6, 8, 9, 10, 13, 14, 15, 16, 19, 20, 21, 23,
)
PAIRS = tuple(itertools.combinations(range(5), 2))


INCIDENCE = [[] for _ in range(VERTICES)]
for edge, (left, right) in enumerate(EDGES):
    INCIDENCE[left].append(edge)
    INCIDENCE[right].append(edge)


def decode_short_graph6(row: str) -> tuple[tuple[int, int], ...]:
    assert row and row[0] != "~"
    vertices = ord(row[0]) - 63
    assert vertices == VERTICES
    bits = []
    for character in row[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    answer = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                answer.append((left, right))
            cursor += 1
    return tuple(answer)


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
    assert decode_short_graph6(GRAPH6) == EDGES
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


def exhaustive_shortest_distance() -> tuple[int, tuple[int, ...], int]:
    seen = {INITIAL}
    queue = deque([(INITIAL, 0)])
    while queue:
        state, distance = queue.popleft()
        if root_good(state):
            return distance, state, len(seen)
        for other, _, _ in root_component_moves(state):
            if other not in seen:
                seen.add(other)
                queue.append((other, distance + 1))
    raise AssertionError("root-component orbit has no rescue")


def replay_five_switch_path() -> None:
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
        states[-1], (1, 4)
    )


def main() -> None:
    validate_graph_and_flow()
    assert coordinate_profile(INITIAL) == (3, 2, 3, 0, 0)
    replay_five_switch_path()
    shortest, rescued_state, states_seen = exhaustive_shortest_distance()
    assert shortest == 5
    assert root_good(rescued_state)
    print(
        "PASS: exhaustive literal BFS finds no rescue within four "
        "root-component switches and shortest rescue distance five "
        f"({states_seen} states discovered before the first rescue)"
    )


if __name__ == "__main__":
    main()
