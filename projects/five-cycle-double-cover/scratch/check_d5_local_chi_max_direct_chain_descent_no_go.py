#!/usr/bin/env python3
"""Literal checker for the smallest local direct chain-descent no-go.

The checker is deliberately self-contained: it uses only Python's standard
library and the displayed graph, labels, roots, and two switches.  It checks
the D5 flow equations, every factor component, surface Euler characteristic,
local chi maximality, all neutral first moves, and the explicit two-neutral-move
rescue.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations


EDGES = (
    (0, 3),
    (0, 4),
    (0, 5),
    (1, 4),
    (1, 5),
    (1, 6),
    (2, 5),
    (2, 6),
    (2, 7),
    (3, 6),
    (3, 7),
    (4, 7),
)
STATE = tuple(
    int(label, 16)
    for label in "03 05 06 06 05 03 03 05 06 06 05 03".split()
)
ROOTS = (1, 7)
PAIRS = tuple(combinations(range(5), 2))


def validate_flow(state: tuple[int, ...]) -> None:
    assert len(state) == len(EDGES)
    assert all(label.bit_count() == 2 for label in state)
    incidence = [[] for _ in range(8)]
    for edge, (left, right) in enumerate(EDGES):
        incidence[left].append(edge)
        incidence[right].append(edge)
    assert all(len(row) == 3 for row in incidence)
    for row in incidence:
        assert state[row[0]] ^ state[row[1]] ^ state[row[2]] == 0


def edge_components(mask: int) -> tuple[int, ...]:
    unused = {edge for edge in range(len(EDGES)) if (mask >> edge) & 1}
    answers = []
    while unused:
        seed = min(unused)
        stack = [seed]
        unused.remove(seed)
        component = 0
        while stack:
            edge = stack.pop()
            component |= 1 << edge
            endpoints = set(EDGES[edge])
            adjacent = [
                other
                for other in sorted(unused)
                if endpoints & set(EDGES[other])
            ]
            for other in adjacent:
                unused.remove(other)
                stack.append(other)
        answers.append(component)
    return tuple(answers)


def coordinate_components(state: tuple[int, ...], coordinate: int) -> int:
    mask = sum(
        1 << edge
        for edge, label in enumerate(state)
        if (label >> coordinate) & 1
    )
    return len(edge_components(mask))


def surface_chi(state: tuple[int, ...]) -> int:
    # Here n=8 and m=12, so V_coloured-m+n = V_coloured-4.
    return (
        sum(coordinate_components(state, coordinate) for coordinate in range(5))
        - 4
    )


def factor_components(
    state: tuple[int, ...], pair: tuple[int, int]
) -> tuple[int, ...]:
    first, second = pair
    mask = sum(
        1 << edge
        for edge, label in enumerate(state)
        if ((label >> first) & 1) ^ ((label >> second) & 1)
    )
    components = edge_components(mask)
    # Every nonempty factor component must be a circuit.
    for component in components:
        degree = [0] * 8
        for edge, (left, right) in enumerate(EDGES):
            if (component >> edge) & 1:
                degree[left] += 1
                degree[right] += 1
        assert all(value in (0, 2) for value in degree)
    return components


def switch(
    state: tuple[int, ...],
    pair: tuple[int, int],
    component: int,
) -> tuple[int, ...]:
    transposition = (1 << pair[0]) | (1 << pair[1])
    answer = tuple(
        label ^ transposition
        if (component >> edge) & 1
        else label
        for edge, label in enumerate(state)
    )
    validate_flow(answer)
    return answer


def moves(state: tuple[int, ...]):
    old_chi = surface_chi(state)
    for pair in PAIRS:
        for component in factor_components(state, pair):
            other = switch(state, pair, component)
            yield pair, component, surface_chi(other) - old_chi, other


def factor_chain_distance(
    state: tuple[int, ...], source: int, target: int
) -> int:
    factors = [
        component
        for pair in PAIRS
        for component in factor_components(state, pair)
    ]
    start = [index for index, item in enumerate(factors) if (item >> source) & 1]
    goal = {
        index for index, item in enumerate(factors) if (item >> target) & 1
    }
    queue = deque((index, 1) for index in start)
    seen = set(start)
    while queue:
        index, distance = queue.popleft()
        if index in goal:
            return distance
        for other in range(len(factors)):
            if other not in seen and factors[index] & factors[other]:
                seen.add(other)
                queue.append((other, distance + 1))
    raise AssertionError("factor-component hypergraph is disconnected")


def edge_mask(edges: set[int]) -> int:
    return sum(1 << edge for edge in edges)


def main() -> int:
    validate_flow(STATE)
    assert surface_chi(STATE) == 1
    assert factor_chain_distance(STATE, *ROOTS) == 2

    first_moves = list(moves(STATE))
    assert first_moves
    assert all(delta <= 0 for _, _, delta, _ in first_moves)
    neutral = [item for item in first_moves if item[2] == 0]
    assert len(neutral) == 11
    assert all(
        factor_chain_distance(other, *ROOTS) == 2
        for _, _, _, other in neutral
    )

    first_pair = (0, 3)
    first_component = edge_mask({0, 1, 10, 11})
    first_state = switch(STATE, first_pair, first_component)
    assert first_component in factor_components(STATE, first_pair)
    assert surface_chi(first_state) == surface_chi(STATE)
    assert factor_chain_distance(first_state, *ROOTS) == 2
    assert first_state == tuple(
        int(label, 16)
        for label in "0a 0c 06 06 05 03 03 05 06 06 0c 0a".split()
    )

    second_pair = (2, 4)
    second_component = edge_mask({1, 2, 3, 4})
    final_state = switch(first_state, second_pair, second_component)
    assert second_component in factor_components(first_state, second_pair)
    assert surface_chi(final_state) == surface_chi(first_state)
    assert factor_chain_distance(final_state, *ROOTS) == 1
    assert final_state == tuple(
        int(label, 16)
        for label in "0a 18 12 12 11 03 03 05 06 06 0c 0a".split()
    )

    print("PASS")
    print("graph6: GCrb`o")
    print("initial chi and factor-chain distance: 1, 2")
    print("neutral first moves: 11; direct descents among them: 0")
    print("explicit neutral distance sequence: 2, 2, 1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
