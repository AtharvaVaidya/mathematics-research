#!/usr/bin/env python3
"""Independent exhaustive audit of the neutralization dynamics.

This implementation works with literal transformed derivative words.  It
does not import ``analyze_dynamics.py`` or use its five-parameter formulas,
Tarjan algorithm, or shortest-cycle search.
"""

from __future__ import annotations

import itertools
from collections import Counter


PARTITION = tuple(map(int, "01234444413024"))
DERIVATIVE = tuple(map(int, "3111121" + "2111311"))
CIRCUITS = (tuple(range(7)), tuple(range(7, 14)))
GL = tuple((0,) + row for row in itertools.permutations((1, 2, 3)))
IDENTITY = (0, 1, 2, 3)

N = 18
EDGES = (
    tuple((i, (i + 1) % 7) for i in range(7))
    + tuple((7 + i, 7 + (i + 1) % 7) for i in range(7))
    + (
        (0, 11),
        (1, 9),
        (2, 12),
        (3, 10),
        (14, 4),
        (14, 5),
        (14, 15),
        (15, 6),
        (15, 16),
        (16, 13),
        (16, 17),
        (17, 7),
        (17, 8),
    )
)
M = len(EDGES)
TARGET_H = (1 << 14) - 1
ALL_EDGES = (1 << M) - 1


def inverse(mapping):
    result = [0] * 4
    for value in range(4):
        result[mapping[value]] = value
    return tuple(result)


def integrate(transitions):
    values = [0] * 14
    for circuit in CIRCUITS:
        value = 0
        for position in circuit:
            value ^= transitions[position]
            values[position] = value
        assert value == 0
    return tuple(values)


def literal_parities(transitions):
    values = integrate(transitions)
    parity = [[0] * 4 for _ in range(5)]
    for circuit in CIRCUITS:
        for local, position in enumerate(circuit):
            previous = circuit[local - 1]
            block = PARTITION[position]
            parity[block][values[previous]] ^= 1
            parity[block][values[position]] ^= 1
    assert all(len(set(row)) == 1 for row in parity)
    return tuple(row[0] for row in parity)


def row_sums(transitions):
    result = [[0, 0] for _ in range(5)]
    for circuit_index, circuit in enumerate(CIRCUITS):
        for position in circuit:
            result[PARTITION[position]][circuit_index] ^= transitions[position]
    assert all(row[0] == row[1] for row in result)
    return tuple(tuple(row) for row in result)


def normalized_states():
    result = set()
    for maps in itertools.product(GL, repeat=4):
        block_maps = (IDENTITY,) + maps
        transitions = tuple(
            block_maps[PARTITION[position]][DERIVATIVE[position]]
            for position in range(14)
        )
        if all(
            not __import__("functools").reduce(
                int.__xor__, (transitions[position] for position in circuit), 0
            )
            for circuit in CIRCUITS
        ):
            result.add(transitions)
    assert len(result) == 40
    return tuple(sorted(result))


STATES = normalized_states()
STATE_SET = set(STATES)


def dual_masks(transitions):
    q_values = literal_parities(transitions)
    sums = row_sums(transitions)
    result = []
    for mask in range(1, 1 << 5):
        left = [0, 0]
        right = 0
        for block in range(5):
            if mask & (1 << block):
                left[0] ^= sums[block][0]
                left[1] ^= sums[block][1]
                right ^= q_values[block]
        if left == [0, 0] and right == 1:
            result.append(mask)
    assert len(result) == 4
    return tuple(result)


def switched(transitions, mask, operator):
    changed = tuple(
        operator[value] if mask & (1 << PARTITION[position]) else value
        for position, value in enumerate(transitions)
    )
    if mask & 1:
        normalizer = inverse(operator)
        changed = tuple(normalizer[value] for value in changed)
    assert changed in STATE_SET
    return changed


def neutralization_graph():
    graph = {state: set() for state in STATES}
    certificates = 0
    for state in STATES:
        for mask in dual_masks(state):
            before = literal_parities(state)
            assert sum(before[block] for block in range(5) if mask >> block & 1) % 2
            for operator in GL:
                target = switched(state, mask, operator)
                after = literal_parities(target)
                if not (
                    sum(after[block] for block in range(5) if mask >> block & 1) % 2
                ):
                    graph[state].add(target)
                    certificates += 1
    assert certificates == 320
    assert sum(map(len, graph.values())) == 136
    return graph


def reachability(graph, root):
    seen = {root}
    frontier = [root]
    while frontier:
        state = frontier.pop()
        for target in graph[state]:
            if target not in seen:
                seen.add(target)
                frontier.append(target)
    return seen


def cycle_basis():
    adjacency = [[] for _ in range(N)]
    for edge, (first, second) in enumerate(EDGES):
        adjacency[first].append((second, edge))
        adjacency[second].append((first, edge))

    parent = [-1] * N
    parent_edge = [-1] * N
    parent[0] = 0
    queue = [0]
    tree = set()
    for vertex in queue:
        for neighbour, edge in adjacency[vertex]:
            if parent[neighbour] < 0:
                parent[neighbour] = vertex
                parent_edge[neighbour] = edge
                tree.add(edge)
                queue.append(neighbour)
    assert len(queue) == N

    basis = []
    for chord, (first, second) in enumerate(EDGES):
        if chord in tree:
            continue
        first_ancestors = {}
        mask = 0
        vertex = first
        while True:
            first_ancestors[vertex] = mask
            if vertex == 0:
                break
            mask ^= 1 << parent_edge[vertex]
            vertex = parent[vertex]
        mask = 1 << chord
        vertex = second
        while vertex not in first_ancestors:
            mask ^= 1 << parent_edge[vertex]
            vertex = parent[vertex]
        mask ^= first_ancestors[vertex]
        basis.append(mask)
    assert len(basis) == 10
    return tuple(basis)


def cycles():
    result = [0]
    for basis_vector in cycle_basis():
        result += [mask ^ basis_vector for mask in result]
    assert len(result) == len(set(result)) == 1024
    return tuple(result)


CYCLES = cycles()


def exchange_profile(transitions, relative_shift):
    values = integrate(transitions)
    low = values[:7] + tuple(value ^ relative_shift for value in values[7:])
    profile = []
    for colour in range(4):
        forbidden = sum(
            (low[edge] == colour) << edge for edge in range(14)
        )
        gains = [
            (cycle & TARGET_H).bit_count()
            - (cycle & (ALL_EDGES ^ TARGET_H)).bit_count()
            for cycle in CYCLES
            if not cycle & forbidden
        ]
        profile.append(max(gains))
    return tuple(profile)


def main():
    graph = neutralization_graph()
    assert all(len(reachability(graph, state)) == 40 for state in STATES)

    exchange_profiles = [
        exchange_profile(state, shift) for state in STATES for shift in range(4)
    ]
    assert all(max(profile) > 0 for profile in exchange_profiles)
    max_gain_histogram = Counter(max(profile) for profile in exchange_profiles)
    minimax_histogram = Counter(
        min(max(exchange_profile(state, shift)) for shift in range(4))
        for state in STATES
    )
    assert max_gain_histogram == {3: 18, 4: 86, 5: 40, 6: 12, 7: 4}
    assert minimax_histogram == {3: 10, 4: 30}

    cycle = (
        (
            tuple(map(int, "3111121" + "2111311")),
            0b00110,
            (0, 2, 1, 3),
            tuple(map(int, "3221121" + "2121321")),
        ),
        (
            tuple(map(int, "3221121" + "2121321")),
            0b01011,
            (0, 2, 1, 3),
            tuple(map(int, "3211212" + "1221312")),
        ),
        (
            tuple(map(int, "3211212" + "1221312")),
            0b00111,
            (0, 2, 1, 3),
            tuple(map(int, "3212121" + "2122311")),
        ),
        (
            tuple(map(int, "3212121" + "2122311")),
            0b01010,
            (0, 2, 1, 3),
            tuple(map(int, "3111121" + "2111311")),
        ),
    )
    for source, mask, operator, target in cycle:
        assert mask in dual_masks(source)
        assert switched(source, mask, operator) == target
        after = literal_parities(target)
        assert not (
            sum(after[block] for block in range(5) if mask >> block & 1) % 2
        )

    print("PASS: independent literal-word audit")
    print("states=40 dual_witnesses_per_state=4")
    print("directed_certificates=320 unique_directed_edges=136")
    print("all_states_mutually_reachable=true")
    print("explicit_neutralization_cycle_length=4")
    print("exchange_valid_state_translations=0")
    print("exchange_max_gain_histogram=3:18,4:86,5:40,6:12,7:4")
    print("exchange_minimax_histogram=3:10,4:30")


if __name__ == "__main__":
    main()
