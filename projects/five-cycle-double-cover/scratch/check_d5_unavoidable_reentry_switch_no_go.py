#!/usr/bin/env python3
"""Independent exact check of the unavoidable-reentry switch no-go.

The literal D5 flow below has a shortest two-component rooted chain C,D.
For the Q-component H through the first root, H re-enters C before the
unique C-D join in both cyclic directions.  Nevertheless switching Q on H
is neutral and leaves the exact rooted factor-chain distance equal to two.

The source belongs to a terminal equal-chi Kempe plateau.  The same literal
C,D,H works with a shared-coordinate factor P and with a disjoint factor P.
This refutes the proposed proof lemma, not FiveCDC.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, permutations


GRAPH6 = "K??FEbGL@WB_"
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
PAIRS = tuple(combinations(range(5), 2))

# Both P choices have exactly this component C in the source.
P_SHARED = (0, 1)
P_DISJOINT = (2, 4)
Q = (0, 3)
C = frozenset((1, 2, 3, 4, 6, 8, 12, 13))
D = frozenset((7, 8, 15, 16))
H = frozenset((0, 1, 3, 5, 9, 11, 12, 14))
C_ORDER = (1, 2, 12, 13, 8, 6, 3, 4)

INCIDENCE = [[] for _ in range(VERTICES)]
for edge, (left, right) in enumerate(EDGES):
    INCIDENCE[left].append(edge)
    INCIDENCE[right].append(edge)


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    """Decode the small-order graph6 format."""
    assert record and ord(record[0]) != 126
    vertices = ord(record[0]) - 63
    bits = "".join(f"{ord(character) - 63:06b}" for character in record[1:])
    needed = vertices * (vertices - 1) // 2
    answer = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor] == "1":
                answer.append((left, right))
            cursor += 1
    assert all(bit == "0" for bit in bits[needed:])
    return vertices, tuple(sorted(answer))


def edge_components(selected) -> tuple[frozenset[int], ...]:
    """Return nonempty edge-components; omit isolated graph vertices."""
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


def factor_edge_set(state, pair) -> frozenset[int]:
    return frozenset().union(*factor_components(state, pair))


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
        - VERTICES // 2
    )


def factor_chain(state, source, target):
    """Return a lexicographically selected shortest factor-component chain."""
    factors = all_factors(state)
    starts = [
        index
        for index, (_, component) in enumerate(factors)
        if source in component
    ]
    goals = {
        index
        for index, (_, component) in enumerate(factors)
        if target in component
    }
    queue = deque(starts)
    predecessor = {index: None for index in starts}
    finish = None
    while queue:
        index = queue.popleft()
        if index in goals:
            finish = index
            break
        component = factors[index][1]
        for other, (_, candidate) in enumerate(factors):
            if other not in predecessor and component & candidate:
                predecessor[other] = index
                queue.append(other)
    assert finish is not None
    answer = []
    while finish is not None:
        answer.append(factors[finish])
        finish = predecessor[finish]
    return tuple(reversed(answer))


def factor_chain_distance(state, source, target):
    return len(factor_chain(state, source, target))


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


def terminal_plateau(initial):
    """Exhaust the equal-chi component mod S5 and count every legal exit."""
    level = chi(initial)
    start = canonical(initial)
    states = {start}
    queue = deque([start])
    deltas = Counter()
    while queue:
        state = queue.popleft()
        assert chi(state) == level
        for pair, component in all_factors(state):
            other = switched(state, pair, component)
            delta = chi(other) - level
            deltas[delta] += 1
            if delta == 0:
                other = canonical(other)
                if other not in states:
                    states.add(other)
                    queue.append(other)
    return states, deltas


def validate_flow(state):
    assert len(state) == len(EDGES)
    assert all(label.bit_count() == 2 for label in state)
    assert all(
        state[row[0]] ^ state[row[1]] ^ state[row[2]] == 0
        for row in INCIDENCE
    )


def validate_graph():
    assert decode_graph6(GRAPH6) == (VERTICES, EDGES)
    assert len(set(EDGES)) == len(EDGES)
    assert all(left != right for left, right in EDGES)
    assert all(len(row) == 3 for row in INCIDENCE)
    # A direct edge-deletion connectedness test proves bridgelessness.
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


def validate_cycle(circuit, order):
    assert set(circuit) == set(order)
    assert len(order) == len(set(order))
    wrapped = order[1:] + order[:1]
    assert all(
        set(EDGES[left]) & set(EDGES[right])
        for left, right in zip(order, wrapped)
    )


def first_marker_after_root_block(order, h, d):
    """Return H or D, after first leaving the root H-intersection block."""
    assert order[0] in h
    position = 1
    while position < len(order) and order[position] in h:
        position += 1
    for edge in order[position:]:
        if edge in d:
            return "D", edge
        if edge in h:
            return "H", edge
    raise AssertionError("D must meet C")


def validate_factor_law(before, after):
    """Check Y_R' = Y_R or Y_R triangle H for every coordinate pair R."""
    for pair in PAIRS:
        expected = factor_edge_set(before, pair)
        if len(set(pair) & set(Q)) == 1:
            expected ^= H
        assert factor_edge_set(after, pair) == expected


def main():
    validate_graph()
    validate_flow(STATE)

    assert len(set(P_SHARED) & set(Q)) == 1
    assert len(set(P_DISJOINT) & set(Q)) == 0
    for pair in (P_SHARED, P_DISJOINT):
        assert C in factor_components(STATE, pair)
    assert D in factor_components(STATE, Q)
    assert H in factor_components(STATE, Q)
    assert H != D
    assert ROOTS[0] in C & H
    assert ROOTS[1] in D
    assert C & D == {8}
    assert H & D == set()
    assert H & C == {1, 3, 12}
    assert edge_components(H & C) == (
        frozenset((1,)),
        frozenset((3,)),
        frozenset((12,)),
    )

    validate_cycle(C, C_ORDER)
    reverse = C_ORDER[:1] + tuple(reversed(C_ORDER[1:]))
    assert first_marker_after_root_block(C_ORDER, H, D) == ("H", 12)
    assert first_marker_after_root_block(reverse, H, D) == ("H", 3)
    assert C_ORDER.index(8) > C_ORDER.index(12)
    assert reverse.index(8) > reverse.index(3)

    assert factor_chain_distance(STATE, *ROOTS) == 2
    after = switched(STATE, Q, H)
    validate_factor_law(STATE, after)
    assert chi(STATE) == chi(after) == 0
    assert factor_chain_distance(after, *ROOTS) == 2
    assert not any(
        set(ROOTS) <= component
        for _, component in all_factors(after)
    )
    # The witness does not defeat a possible two-switch repair: the old C is
    # a (2,4)-component through the first root and rescues in one more neutral
    # move.
    assert C in factor_components(after, P_DISJOINT)
    repaired = switched(after, P_DISJOINT, C)
    assert chi(repaired) == 0
    assert factor_chain_distance(repaired, *ROOTS) == 1

    plateau, plateau_deltas = terminal_plateau(STATE)
    assert canonical(after) in plateau
    assert len(plateau) == 7
    assert not any(delta > 0 for delta in plateau_deltas)

    print("PASS")
    print(f"graph6: {GRAPH6}; roots: {ROOTS}")
    print("P shared/Q:", P_SHARED, Q, "; P disjoint/Q:", P_DISJOINT, Q)
    print("both directions: leave root H-block, re-enter H, then hit join 8")
    print("H-switch: chi 0 -> 0; exact distance 2 -> 2")
    print("one further neutral root-component switch repairs: distance 2 -> 1")
    print(
        "terminal equal-chi plateau mod S5:",
        len(plateau),
        "states; directed move deltas",
        dict(sorted(plateau_deltas.items())),
    )


if __name__ == "__main__":
    main()
