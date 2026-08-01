#!/usr/bin/env python3
"""Standalone terminal no-go to `distance-up implies immediate down`.

At the displayed state a neutral shared-coordinate self-reentry switch
raises factor-chain distance 2 -> 3, while every other neutral first move
keeps distance 2.  A neutral 2 -> 2 -> 1 route still exists.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, permutations


V = 12
EDGES = (
    (0, 4), (0, 6), (0, 8), (1, 5), (1, 7), (1, 11),
    (2, 7), (2, 9), (2, 10), (3, 8), (3, 9), (3, 10),
    (4, 6), (4, 8), (5, 10), (5, 11), (6, 9), (7, 11),
)
STATE = tuple(
    int(x, 16)
    for x in (
        "03", "05", "06", "03", "05", "06",
        "06", "05", "03", "03", "06", "05",
        "06", "05", "06", "05", "03", "03",
    )
)
ROOTS = (1, 3)
PAIRS = tuple(combinations(range(5), 2))
RAISING = ((0, 1), 0x3006)
K1 = ((0, 3), 0x12B83)
K2 = ((0, 2), 0x24168)
PLATEAU_PATH = (((0, 2), 0x11605), ((0, 1), 0x28018))

INCIDENCE = [[] for _ in range(V)]
for edge, (left, right) in enumerate(EDGES):
    INCIDENCE[left].append(edge)
    INCIDENCE[right].append(edge)


def bits(mask):
    return frozenset(edge for edge in range(len(EDGES)) if (mask >> edge) & 1)


def components(selected):
    unseen = set(selected)
    answer = []
    while unseen:
        edge = min(unseen)
        unseen.remove(edge)
        component = {edge}
        queue = [edge]
        while queue:
            current = queue.pop()
            for vertex in EDGES[current]:
                for other in INCIDENCE[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        component.add(other)
                        queue.append(other)
        answer.append(frozenset(component))
    return tuple(answer)


def factors(state):
    answer = []
    for pair in PAIRS:
        mask = (1 << pair[0]) | (1 << pair[1])
        selected = [
            edge
            for edge, label in enumerate(state)
            if (label & mask).bit_count() == 1
        ]
        answer.extend((pair, component) for component in components(selected))
    return tuple(answer)


def switch(state, pair, component):
    mask = (1 << pair[0]) | (1 << pair[1])
    answer = tuple(
        label ^ mask if edge in component else label
        for edge, label in enumerate(state)
    )
    validate_flow(answer)
    return answer


def chi(state):
    coordinate_count = 0
    for coordinate in range(5):
        coordinate_count += len(components(
            edge
            for edge, label in enumerate(state)
            if (label >> coordinate) & 1
        ))
    return coordinate_count - len(EDGES) + V


def distance(state):
    family = factors(state)
    starts = {
        index
        for index, (_, component) in enumerate(family)
        if ROOTS[0] in component
    }
    goals = {
        index
        for index, (_, component) in enumerate(family)
        if ROOTS[1] in component
    }
    queue = deque((index, 1) for index in starts)
    seen = set(starts)
    while queue:
        index, level = queue.popleft()
        if index in goals:
            return level
        for other, (_, component) in enumerate(family):
            if other not in seen and family[index][1] & component:
                seen.add(other)
                queue.append((other, level + 1))
    raise AssertionError("factor hypergraph disconnected")


TABLES = []
for permutation in permutations(range(5)):
    table = []
    for label in range(32):
        image = 0
        for coordinate in range(5):
            if (label >> coordinate) & 1:
                image |= 1 << permutation[coordinate]
        table.append(image)
    TABLES.append(tuple(table))


def canonical(state):
    return min(tuple(table[label] for label in state) for table in TABLES)


def validate_flow(state):
    assert len(state) == len(EDGES)
    assert all(label.bit_count() == 2 for label in state)
    assert all(len(row) == 3 for row in INCIDENCE)
    assert all(
        state[row[0]] ^ state[row[1]] ^ state[row[2]] == 0
        for row in INCIDENCE
    )


def validate_graph():
    assert len(set(EDGES)) == len(EDGES)
    assert all(left != right for left, right in EDGES)
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
        assert len(seen) == V


def plateau():
    level = chi(STATE)
    initial = canonical(STATE)
    seen = {initial}
    queue = deque([initial])
    positive = 0
    while queue:
        state = queue.popleft()
        for pair, component in factors(state):
            other = switch(state, pair, component)
            delta = chi(other) - level
            if delta > 0:
                positive += 1
            elif delta == 0:
                other = canonical(other)
                if other not in seen:
                    seen.add(other)
                    queue.append(other)
    return seen, positive


def main():
    validate_graph()
    validate_flow(STATE)
    assert canonical(STATE) == STATE
    assert chi(STATE) == 0
    assert distance(STATE) == 2

    initial_moves = [
        (pair, component, switch(STATE, pair, component))
        for pair, component in factors(STATE)
    ]
    assert len(initial_moves) == 18
    assert Counter(chi(other) - chi(STATE) for _, _, other in initial_moves) == {
        0: 18
    }
    assert Counter(distance(other) - 2 for _, _, other in initial_moves) == {
        0: 16,
        1: 2,
    }

    raising_pair, raising_mask = RAISING
    raising_component = bits(raising_mask)
    assert raising_component in tuple(
        component
        for pair, component in factors(STATE)
        if pair == raising_pair
    )
    raised = switch(STATE, raising_pair, raising_component)
    assert chi(raised) == 0 and distance(raised) == 3

    first_pair, first_mask = K1
    second_pair, second_mask = K2
    first_component = bits(first_mask)
    second_component = bits(second_mask)
    assert first_component in tuple(
        component for pair, component in factors(STATE) if pair == first_pair
    )
    assert second_component in tuple(
        component for pair, component in factors(STATE) if pair == second_pair
    )
    assert len(components(first_component & raising_component)) == 2
    assert not second_component & raising_component
    assert first_component & second_component == {8}

    current = STATE
    distance_sequence = [distance(current)]
    for pair, mask in PLATEAU_PATH:
        component = bits(mask)
        assert component in tuple(
            item for factor, item in factors(current) if factor == pair
        )
        current = canonical(switch(current, pair, component))
        assert chi(current) == 0
        distance_sequence.append(distance(current))
    assert distance_sequence == [2, 2, 1]

    states, positive = plateau()
    assert len(states) == 112
    assert positive == 0
    assert canonical(raised) in states

    print("PASS")
    print("graph6: K?`CRAWK`gGg")
    print("terminal plateau: chi 0, 112 states mod S5, no positive exit")
    print("neutral first-move distance changes: {0:16, +1:2}, no descent")
    print("explicit neutral safe route: 2 -> 2 -> 1")


if __name__ == "__main__":
    main()
