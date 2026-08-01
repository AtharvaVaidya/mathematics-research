#!/usr/bin/env python3
"""Check a terminal-plateau no-go to distance-primary endpoint lifting.

The displayed neutral root-component switch occurs inside a genuine
terminal equal-chi plateau, yet raises the exact factor-chain distance
from two to three.  A forced second splice rescues the roots but loses
four units of chi, so it is unavailable inside the terminal plateau.

This is a counterexample to that proposed proof move, not to FiveCDC.
The checker uses only Python's standard library and literal graph data.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, permutations


VERTICES = 12
EDGES = (
    (0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 9),
    (2, 6), (2, 8), (2, 10), (3, 7), (3, 9), (3, 11),
    (4, 8), (4, 10), (4, 11), (5, 9), (5, 10), (5, 11),
)
STATE = tuple(
    int(label, 16)
    for label in (
        "03", "05", "06", "05", "09", "0c",
        "06", "03", "05", "0c", "09", "05",
        "05", "03", "06", "05", "06", "03",
    )
)
ROOTS = (4, 13)
FIRST_PAIR = (0, 1)
FIRST_COMPONENT = frozenset(
    edge for edge in range(18) if (0x1DD5E >> edge) & 1
)
SECOND_PAIR = (0, 2)
SECOND_COMPONENT = frozenset(
    edge for edge in range(18) if (0x36000 >> edge) & 1
)
REENTRY_PAIR = (1, 3)
REENTRY_COMPONENT = frozenset(
    edge for edge in range(18) if (0x630 >> edge) & 1
)
FORCED_SPLICE = frozenset(
    edge for edge in range(18) if (0x5A06 >> edge) & 1
)
PAIRS = tuple(combinations(range(5), 2))

INCIDENCE = [[] for _ in range(VERTICES)]
for edge, (left, right) in enumerate(EDGES):
    INCIDENCE[left].append(edge)
    INCIDENCE[right].append(edge)


def edge_components(selected) -> tuple[frozenset[int], ...]:
    unseen = set(selected)
    answer = []
    while unseen:
        first = min(unseen)
        unseen.remove(first)
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
        answer.append(frozenset(component))
    return tuple(answer)


def factor_components(state, pair) -> tuple[frozenset[int], ...]:
    pair_mask = (1 << pair[0]) | (1 << pair[1])
    return edge_components(
        edge
        for edge, label in enumerate(state)
        if (label & pair_mask).bit_count() == 1
    )


def all_factors(state):
    return tuple(
        (pair, component)
        for pair in PAIRS
        for component in factor_components(state, pair)
    )


def switched(state, pair, component):
    pair_mask = (1 << pair[0]) | (1 << pair[1])
    answer = tuple(
        label ^ pair_mask if edge in component else label
        for edge, label in enumerate(state)
    )
    validate_flow(answer)
    return answer


def coordinate_components(state, coordinate):
    return edge_components(
        edge
        for edge, label in enumerate(state)
        if (label >> coordinate) & 1
    )


def chi(state):
    return (
        sum(
            len(coordinate_components(state, coordinate))
            for coordinate in range(5)
        )
        - len(EDGES)
        + VERTICES
    )


def factor_chain_distance(state, source, target):
    factors = all_factors(state)
    start = {
        index
        for index, (_, component) in enumerate(factors)
        if source in component
    }
    goal = {
        index
        for index, (_, component) in enumerate(factors)
        if target in component
    }
    queue = deque((index, 1) for index in start)
    seen = set(start)
    while queue:
        index, distance = queue.popleft()
        if index in goal:
            return distance
        component = factors[index][1]
        for other, (_, candidate) in enumerate(factors):
            if other not in seen and component & candidate:
                seen.add(other)
                queue.append((other, distance + 1))
    raise AssertionError("factor hypergraph disconnected")


PERMUTATION_TABLES = []
for permutation in permutations(range(5)):
    table = []
    for label in range(32):
        image = 0
        for coordinate in range(5):
            if (label >> coordinate) & 1:
                image |= 1 << permutation[coordinate]
        table.append(image)
    PERMUTATION_TABLES.append(tuple(table))


def canonical(state):
    return min(
        tuple(table[label] for label in state)
        for table in PERMUTATION_TABLES
    )


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
    assert all(len(row) == 3 for row in INCIDENCE)
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


def terminal_plateau():
    """Return the equal-chi component and positive-exit count mod S5."""
    level = chi(STATE)
    initial = canonical(STATE)
    states = {initial}
    queue = deque([initial])
    positive_exits = 0
    while queue:
        state = queue.popleft()
        assert chi(state) == level
        for pair, component in all_factors(state):
            other = switched(state, pair, component)
            delta = chi(other) - level
            if delta > 0:
                positive_exits += 1
            elif delta == 0:
                other = canonical(other)
                if other not in states:
                    states.add(other)
                    queue.append(other)
    return states, positive_exits


def main():
    validate_graph()
    validate_flow(STATE)
    assert canonical(STATE) == STATE
    assert FIRST_COMPONENT in factor_components(STATE, FIRST_PAIR)
    assert SECOND_COMPONENT in factor_components(STATE, SECOND_PAIR)
    assert REENTRY_COMPONENT in factor_components(STATE, REENTRY_PAIR)
    assert ROOTS[0] in FIRST_COMPONENT & REENTRY_COMPONENT
    assert ROOTS[1] in SECOND_COMPONENT
    assert FIRST_COMPONENT & SECOND_COMPONENT
    assert not REENTRY_COMPONENT & SECOND_COMPONENT
    assert len(edge_components(FIRST_COMPONENT & REENTRY_COMPONENT)) == 2

    first = switched(STATE, REENTRY_PAIR, REENTRY_COMPONENT)
    join = min(FIRST_COMPONENT & SECOND_COMPONENT)
    assert join == 14
    assert FORCED_SPLICE in factor_components(first, FIRST_PAIR)
    assert join in FORCED_SPLICE
    second = switched(first, FIRST_PAIR, FORCED_SPLICE)

    assert [chi(state) for state in (STATE, first, second)] == [2, 2, -2]
    assert [
        factor_chain_distance(state, *ROOTS)
        for state in (STATE, first, second)
    ] == [2, 3, 1]

    initial_deltas = Counter(
        chi(switched(STATE, pair, component)) - chi(STATE)
        for pair, component in all_factors(STATE)
    )
    assert initial_deltas == {0: 15, -2: 5}

    plateau, positive_exits = terminal_plateau()
    assert len(plateau) == 42
    assert positive_exits == 0
    assert canonical(first) in plateau

    print("PASS")
    print("graph6: K??FEagT@WB_")
    print("terminal equal-chi plateau: chi 2, 42 states mod S5, no positive exit")
    print("neutral shared-pair self-reentry switch: distance 2 -> 3")
    print("forced second splice: chi 2 -> -2, distance 3 -> 1")


if __name__ == "__main__":
    main()
