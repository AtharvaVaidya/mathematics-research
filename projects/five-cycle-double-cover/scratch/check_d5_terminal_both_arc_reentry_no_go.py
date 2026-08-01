#!/usr/bin/env python3
"""Standalone no-go to the terminal both-arc self-reentry dichotomy.

The conjectured move was: for a shortest distance-two chain C,D, where
C is a Y_P circuit through r and H,D are distinct Y_Q circuits through
r,s, if both orientations of C encounter a new H-intersection before
their first D-intersection, then switching Q on H immediately makes the
roots share a factor circuit.

The literal terminal-plateau state below satisfies every hypothesis.
The H switch is neutral, but the rooted distance remains two.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, permutations


VERTICES = 12
EDGES = (
    (0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8),
    (2, 6), (2, 9), (2, 10), (3, 7), (3, 9), (3, 11),
    (4, 8), (4, 10), (4, 11), (5, 9), (5, 10), (5, 11),
)
STATE = tuple(
    int(label, 16)
    for label in (
        "03", "05", "06", "05", "06", "03",
        "06", "03", "05", "03", "06", "05",
        "05", "06", "03", "05", "03", "06",
    )
)
ROOTS = (1, 15)
P = (0, 1)
Q = (0, 3)
C = 0x315E
H = 0x5A2B
D = 0x18180
P_PRIME = (1, 3)
EXPECTED_C_ORDER = (1, 4, 3, 6, 8, 13, 12, 2)
PAIRS = tuple(combinations(range(5), 2))

INCIDENCE = [[] for _ in range(VERTICES)]
for edge, (left, right) in enumerate(EDGES):
    INCIDENCE[left].append(edge)
    INCIDENCE[right].append(edge)


def edge_set(mask):
    return frozenset(
        edge for edge in range(len(EDGES)) if (mask >> edge) & 1
    )


def edge_components(selected):
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
        pair_mask = (1 << pair[0]) | (1 << pair[1])
        answer.extend(
            (pair, component)
            for component in edge_components(
                edge
                for edge, label in enumerate(state)
                if (label & pair_mask).bit_count() == 1
            )
        )
    return tuple(answer)


def switch(state, pair, component):
    pair_mask = (1 << pair[0]) | (1 << pair[1])
    answer = tuple(
        label ^ pair_mask if edge in component else label
        for edge, label in enumerate(state)
    )
    validate_flow(answer)
    return answer


def chi(state):
    coordinate_components = 0
    for coordinate in range(5):
        coordinate_components += len(edge_components(
            edge
            for edge, label in enumerate(state)
            if (label >> coordinate) & 1
        ))
    return coordinate_components - len(EDGES) + VERTICES


def factor_distance(state):
    family = factors(state)
    start = {
        index
        for index, (_, component) in enumerate(family)
        if ROOTS[0] in component
    }
    goal = {
        index
        for index, (_, component) in enumerate(family)
        if ROOTS[1] in component
    }
    queue = deque((index, 1) for index in start)
    seen = set(start)
    while queue:
        index, level = queue.popleft()
        if index in goal:
            return level
        for other, (_, component) in enumerate(family):
            if other not in seen and family[index][1] & component:
                seen.add(other)
                queue.append((other, level + 1))
    raise AssertionError("factor-component hypergraph disconnected")


def cycle_order(component, root):
    selected = edge_set(component)
    local = [[] for _ in range(VERTICES)]
    for edge in selected:
        left, right = EDGES[edge]
        local[left].append(edge)
        local[right].append(edge)
    assert all(len(row) in (0, 2) for row in local)
    vertex = EDGES[root][1]
    previous = root
    order = [root]
    while True:
        edge = (
            local[vertex][0]
            if local[vertex][0] != previous
            else local[vertex][1]
        )
        if edge == root:
            return tuple(order)
        order.append(edge)
        left, right = EDGES[edge]
        vertex = left ^ right ^ vertex
        previous = edge


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
        assert len(seen) == VERTICES


def terminal_plateau():
    level = chi(STATE)
    initial = canonical(STATE)
    states = {initial}
    queue = deque([initial])
    positive_exits = 0
    while queue:
        state = queue.popleft()
        for pair, component in factors(state):
            other = switch(state, pair, component)
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

    c_set, h_set, d_set = edge_set(C), edge_set(H), edge_set(D)
    assert c_set in tuple(
        component for pair, component in factors(STATE) if pair == P
    )
    q_components = tuple(
        component for pair, component in factors(STATE) if pair == Q
    )
    assert h_set in q_components and d_set in q_components
    assert h_set.isdisjoint(d_set)
    assert ROOTS[0] in c_set & h_set
    assert ROOTS[1] in d_set
    assert c_set & d_set == {8}
    assert factor_distance(STATE) == 2

    order = cycle_order(C, ROOTS[0])
    assert order == EXPECTED_C_ORDER
    assert [edge for edge in order if edge in h_set] == [1, 3, 12]
    assert [edge for edge in order if edge in d_set] == [8]
    # A0={1}.  Forward sees H edge 3 before D edge 8; reverse sees
    # H edge 12 before that same D edge.
    assert order.index(3) < order.index(8)
    assert order[::-1].index(12) < order[::-1].index(8)

    switched = switch(STATE, Q, h_set)
    assert chi(STATE) == chi(switched) == 0
    assert factor_distance(switched) == 2
    p_prime_components = tuple(
        component
        for pair, component in factors(switched)
        if pair == P_PRIME
    )
    assert p_prime_components == (edge_set(0x33CDE),)
    assert ROOTS[0] in p_prime_components[0]
    assert ROOTS[1] not in p_prime_components[0]

    assert Counter(
        chi(switch(STATE, pair, component)) - chi(STATE)
        for pair, component in factors(STATE)
    ) == {0: 12, -2: 6}

    plateau, positive_exits = terminal_plateau()
    assert len(plateau) == 7
    assert positive_exits == 0
    assert canonical(switched) in plateau

    print("PASS")
    print("graph6: K??FEbGL@WB_")
    print("terminal plateau: chi 0, 7 states mod S5, no positive exit")
    print("both C orientations encounter H before D")
    print("neutral H switch leaves rooted factor distance 2, not 1")


if __name__ == "__main__":
    main()
