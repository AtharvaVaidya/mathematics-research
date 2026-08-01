#!/usr/bin/env python3
"""Check an order-14 no-go to a restricted one-step blocker descent.

The source is in a genuine terminal equal-chi plateau and has rooted
metric (d,b*)=(2,1), where b* is the least foreign-Q block count over
eligible shortest first-pair choices with |P intersection Q|=1.

For every minimizing choice, switching its root Q-component H or its
first blocker J either lowers chi or raises d.  Nevertheless an
unrelated neutral 24-switch immediately gives d=1.  Thus this is only
a no-go to the restricted H/J one-step rule, not to plateau descent
and not to FiveCDC.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, permutations


GRAPH6 = "M??CEB@W_sE_J?F??"
VERTICES = 14
EDGES = (
    (0, 6), (0, 7), (0, 8),
    (1, 7), (1, 8), (1, 9),
    (2, 9), (2, 11), (2, 12),
    (3, 10), (3, 11), (3, 13),
    (4, 10), (4, 12), (4, 13),
    (5, 11), (5, 12), (5, 13),
    (6, 9), (6, 10), (7, 8),
)
STATE = tuple(
    int(label, 16)
    for label in (
        "03", "05", "06", "06", "05", "03", "05",
        "09", "0c", "03", "05", "06", "06", "05",
        "03", "0c", "09", "05", "06", "05", "03",
    )
)
ROOTS = (16, 3)
PAIRS = tuple(combinations(range(5), 2))

C = frozenset((6, 7, 10, 11, 12, 13, 16, 17, 18, 19))
H = frozenset((7, 8, 15, 16))
D = frozenset((0, 2, 3, 5, 18, 20))
J = frozenset((9, 11, 12, 14))
C_ORDER = (16, 13, 12, 19, 18, 6, 7, 10, 11, 17)
RESCUE_PAIR = (2, 4)
RESCUE_COMPONENT = frozenset((6, 8, 12, 13, 18, 19))

INCIDENCE = [[] for _ in range(VERTICES)]
for edge, (left, right) in enumerate(EDGES):
    INCIDENCE[left].append(edge)
    INCIDENCE[right].append(edge)


def decode_graph6(record):
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


def edge_components(selected):
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


def factor_components(state, pair):
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


def chi(state):
    return (
        sum(
            len(
                edge_components(
                    edge
                    for edge, label in enumerate(state)
                    if (label >> coordinate) & 1
                )
            )
            for coordinate in range(5)
        )
        - len(EDGES)
        + VERTICES
    )


def coordinate_components(state, coordinate):
    return edge_components(
        edge
        for edge, label in enumerate(state)
        if (label >> coordinate) & 1
    )


def circuit_order(component, root):
    def adjacent(edge):
        return sorted(
            other
            for other in component
            if other != edge
            and set(EDGES[edge]) & set(EDGES[other])
        )

    assert all(len(adjacent(edge)) == 2 for edge in component)
    answer = [root]
    previous = root
    current = adjacent(root)[0]
    while current != root:
        answer.append(current)
        choices = adjacent(current)
        following = choices[0] if choices[0] != previous else choices[1]
        previous, current = current, following
    assert len(answer) == len(component)
    return tuple(answer)


def factor_distances(rows, target):
    starts = [
        index
        for index, (_, component) in enumerate(rows)
        if target in component
    ]
    distance = {index: 1 for index in starts}
    queue = deque(starts)
    while queue:
        current = queue.popleft()
        for other, (_, component) in enumerate(rows):
            if other not in distance and rows[current][1] & component:
                distance[other] = distance[current] + 1
                queue.append(other)
    return distance


def metric_and_profiles(state, roots):
    """Return (d,b*,minimizing profiles); no eligible profile means b*=0."""
    rows = all_factors(state)
    to_target = factor_distances(rows, roots[1])
    source_rows = [
        index
        for index, (_, component) in enumerate(rows)
        if roots[0] in component
    ]
    distance = min(to_target[index] for index in source_rows)
    if distance <= 1:
        return distance, 0, ()

    profiles = []
    for first in source_rows:
        pair_p, circuit = rows[first]
        for second, (pair_q, target_component) in enumerate(rows):
            if not circuit & target_component:
                continue
            if 1 + to_target[second] != distance:
                continue

            # Exact shared-coordinate eligibility required by the lemma.
            if len(set(pair_p) & set(pair_q)) != 1:
                continue

            root_q_rows = [
                index
                for index, (pair, component) in enumerate(rows)
                if pair == pair_q and roots[0] in component
            ]
            assert len(root_q_rows) <= 1
            if not root_q_rows or root_q_rows[0] == second:
                continue
            root_q = root_q_rows[0]
            root_component = rows[root_q][1]

            owner = {}
            for index, (pair, component) in enumerate(rows):
                if pair != pair_q:
                    continue
                for edge in circuit & component:
                    assert edge not in owner
                    owner[edge] = index

            order = circuit_order(circuit, roots[0])
            n = len(order)
            scans = []
            for step in (1, -1):
                cursor = step
                while owner.get(order[cursor % n]) == root_q:
                    cursor += step
                    assert abs(cursor) <= n
                blockers = []
                previous_owner = object()
                while abs(cursor) <= n:
                    edge = order[cursor % n]
                    current_owner = owner.get(edge)
                    if current_owner != previous_owner:
                        if current_owner == second:
                            scans.append((tuple(blockers), edge))
                            break
                        if current_owner is not None and current_owner != root_q:
                            blockers.append(current_owner)
                    previous_owner = current_owner
                    cursor += step
                else:
                    raise AssertionError("target Q-component absent from C")

            profiles.append(
                {
                    "P": pair_p,
                    "Q": pair_q,
                    "C": circuit,
                    "H": root_component,
                    "D": target_component,
                    "scans": tuple(scans),
                    "blocker": min(len(scan[0]) for scan in scans),
                    "rows": rows,
                }
            )

    if not profiles:
        return distance, 0, ()
    minimum = min(profile["blocker"] for profile in profiles)
    return (
        distance,
        minimum,
        tuple(profile for profile in profiles if profile["blocker"] == minimum),
    )


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
    level = chi(initial)
    start = canonical(initial)
    states = {start}
    queue = deque([start])
    deltas = Counter()
    while queue:
        state = queue.popleft()
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
    validate_graph()
    validate_flow(STATE)
    assert circuit_order(C, ROOTS[0]) == C_ORDER
    assert C in factor_components(STATE, (0, 1))
    assert C in factor_components(STATE, (2, 3))
    for pair in ((0, 2), (1, 3)):
        assert set(factor_components(STATE, pair)) == {H, D, J}
    assert ROOTS[0] in C & H
    assert ROOTS[1] in D
    assert C & D == {18}
    assert C & H == {7, 16}
    assert C & J == {11, 12}

    distance, blocker, profiles = metric_and_profiles(STATE, ROOTS)
    assert (distance, blocker) == (2, 1)
    assert len(profiles) == 4
    assert {profile["P"] for profile in profiles} == {(0, 1), (2, 3)}
    assert {profile["Q"] for profile in profiles} == {(0, 2), (1, 3)}
    assert all(len(set(profile["P"]) & set(profile["Q"])) == 1 for profile in profiles)
    assert all(profile["C"] == C for profile in profiles)
    assert all(profile["H"] == H and profile["D"] == D for profile in profiles)

    # Every minimizing H/J move: Q=02 loses chi; Q=13 is neutral but
    # raises the primary distance.  Hence none decreases (d,b*).
    candidate_outcomes = {}
    for pair in ((0, 2), (1, 3)):
        for name, component in (("H", H), ("J", J)):
            other = switched(STATE, pair, component)
            candidate_outcomes[(pair, name)] = (
                chi(other) - chi(STATE),
                metric_and_profiles(other, ROOTS)[:2],
            )
    assert candidate_outcomes == {
        ((0, 2), "H"): (-2, (2, 1)),
        ((0, 2), "J"): (-2, (2, 1)),
        ((1, 3), "H"): (0, (3, 0)),
        ((1, 3), "J"): (0, (3, 0)),
    }

    assert RESCUE_COMPONENT in factor_components(STATE, RESCUE_PAIR)
    assert coordinate_components(STATE, 4) == ()
    assert set(coordinate_components(STATE, 2)) == {
        frozenset((1, 2, 3, 4)),
        RESCUE_COMPONENT,
        frozenset((10, 11, 15, 17)),
    }
    assert set(factor_components(STATE, (0, 2))) == {H, J, D}
    assert RESCUE_COMPONENT & H == {8}
    assert RESCUE_COMPONENT & J == {12}
    assert RESCUE_COMPONENT & D == {18}
    rescued = switched(STATE, RESCUE_PAIR, RESCUE_COMPONENT)
    assert RESCUE_COMPONENT in coordinate_components(rescued, 4)
    assert RESCUE_COMPONENT not in coordinate_components(rescued, 2)
    assert chi(rescued) == chi(STATE) == 1
    assert metric_and_profiles(rescued, ROOTS)[:2] == (1, 0)
    assert frozenset((0, 2, 3, 5, 6, 7, 9, 11, 13, 14, 15, 16, 19, 20)) in (
        factor_components(rescued, (0, 2))
    )

    source_deltas = Counter(
        chi(switched(STATE, pair, component)) - chi(STATE)
        for pair, component in all_factors(STATE)
    )
    assert source_deltas == {0: 18, -2: 2}

    plateau, plateau_deltas = terminal_plateau(STATE)
    assert len(plateau) == 236
    assert plateau_deltas == {0: 4248, -2: 336}
    assert canonical(rescued) in plateau
    assert not any(delta > 0 for delta in plateau_deltas)

    print("PASS")
    print(f"graph6: {GRAPH6}; endpoint-sorted roots: {ROOTS}")
    print("source: chi 1, (d,b*)=(2,1), terminal plateau size 236")
    print("all minimizing H/J moves: chi loss or distance 2 -> 3")
    print("shortest neutral rescue: one 24-switch, (d,b*) (2,1) -> (1,0)")


if __name__ == "__main__":
    main()
