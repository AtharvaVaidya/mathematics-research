#!/usr/bin/env python3
"""Standalone semantic replay of the sharp order-14 delimiter and escape."""

from __future__ import annotations

from collections import deque
from itertools import combinations, permutations


ROW = "M?AACGohBAJ?AgE_?"
CAP = 0
ROOT = 19
LABELS = tuple((1 << a) | (1 << b) for a, b in combinations(range(5), 2))
START = tuple(int(x, 16) for x in (
    "03 0c 05 06 06 14 06 03 05 06 05 03 0a 06 0c 06 14 12 12 0a 18"
).split())
MISSING = 0
COMPLEMENT_CIRCUIT = (1, 12, 13, 18, 20)
AFTER_COMPLEMENT = tuple(int(x, 16) for x in (
    "03 05 0a 09 09 0c 09 03 0a 09 0a 03 0c 14 18 09 0c 05 18 11 09"
).split())
KEMPE_PATH = (
    (0x05, (0, 3, 4, 5, 6, 7, 9, 11, 12, 13),
     "03 05 0a 09 09 0c 09 03 0a 09 0a 03 0c 14 18 0c 09 05 18 14 0c"),
    (0x12, (0, 2, 7, 8, 10, 11),
     "03 05 0a 09 09 0c 09 03 0a 09 0a 03 0c 06 0a 0c 09 05 0a 06 0c"),
    (0x0C, (1, 4, 9, 10, 16, 17),
     "03 05 06 05 09 0c 05 03 06 09 0a 03 0c 0a 06 0c 09 05 06 0a 0c"),
    (0x18, (4, 5, 9, 10, 12, 13),
     "03 05 06 05 09 0c 05 03 06 09 0a 03 0c 0a 06 14 11 05 06 12 14"),
)
KEMPE_PATH = tuple(
    (pair, component, tuple(int(x, 16) for x in word.split()))
    for pair, component, word in KEMPE_PATH
)


def decode_graph6(row):
    values = [ord(char) - 63 for char in row]
    n = values[0]
    bits = []
    for value in values[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    incidence = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    assert all(len(row) == 3 for row in incidence)
    return n, tuple(edges), tuple(tuple(row) for row in incidence)


def permute_label(label, permutation):
    return sum(1 << permutation[i] for i in range(5) if (label >> i) & 1)


def canonical(state):
    return min(
        tuple(permute_label(label, permutation) for label in state)
        for permutation in permutations(range(5))
    )


def check_flow(state, incidence):
    assert all(label in LABELS for label in state)
    assert all(state[a] ^ state[b] ^ state[c] == 0 for a, b, c in incidence)


def components(state, pair, edges, incidence):
    active = {edge for edge, label in enumerate(state) if (label & pair).bit_count() == 1}
    answer = []
    while active:
        start = min(active)
        active.remove(start)
        found = {start}
        stack = [start]
        while stack:
            edge = stack.pop()
            for vertex in edges[edge]:
                local = [other for other in incidence[vertex]
                         if (state[other] & pair).bit_count() == 1]
                assert len(local) in (0, 2)
                for other in local:
                    if other in active:
                        active.remove(other)
                        found.add(other)
                        stack.append(other)
        answer.append(tuple(sorted(found)))
    return tuple(answer)


def transpose(label, pair):
    first, second = (i for i in range(5) if (pair >> i) & 1)
    if ((label >> first) & 1) == ((label >> second) & 1):
        return label
    return label ^ pair


def switched(state, pair, component):
    support = set(component)
    return canonical(tuple(
        transpose(label, pair) if edge in support else label
        for edge, label in enumerate(state)
    ))


def fixed_typed(state, edges, incidence):
    physical = {(0, 1): 0, (0, 2): 1, (1, 2): 2}
    typed = external = 0
    for pair in LABELS:
        for component in components(state, pair, edges, incidence):
            if ROOT not in component:
                continue
            slots = tuple(i for i, edge in enumerate(incidence[CAP]) if edge in component)
            if len(slots) != 2:
                continue
            inactive = next(i for i in range(3) if i not in slots)
            inactive_label = state[incidence[CAP][inactive]]
            assert pair == inactive_label or not (pair & inactive_label)
            mode = int(pair != inactive_label)
            index = physical[slots]
            typed |= 1 << (2 * index + mode)
            if mode:
                external |= 1 << index
    return typed, external


def orbit(initial, edges, incidence):
    initial = canonical(initial)
    answer = {initial}
    queue = deque([initial])
    while queue:
        state = queue.popleft()
        for pair in LABELS:
            for component in components(state, pair, edges, incidence):
                other = switched(state, pair, component)
                if other not in answer:
                    answer.add(other)
                    queue.append(other)
    return answer


def main():
    n, edges, incidence = decode_graph6(ROW)
    assert n == 14 and len(edges) == 21
    check_flow(START, incidence)
    assert fixed_typed(START, edges, incidence) == (0, 0)

    circuit = set(COMPLEMENT_CIRCUIT)
    assert circuit.isdisjoint({ROOT, *incidence[CAP]})
    degree = [0] * n
    for edge in circuit:
        left, right = edges[edge]
        degree[left] += 1
        degree[right] += 1
        assert not ((START[edge] >> MISSING) & 1)
    assert sorted(value for value in degree if value) == [2] * 5
    shift = 31 ^ (1 << MISSING)
    raw = tuple(label ^ shift if edge in circuit else label
                for edge, label in enumerate(START))
    check_flow(raw, incidence)
    assert canonical(raw) == AFTER_COMPLEMENT
    assert fixed_typed(AFTER_COMPLEMENT, edges, incidence) == (0, 0)

    bad_orbit = orbit(START, edges, incidence)
    assert len(bad_orbit) == 432
    assert AFTER_COMPLEMENT not in bad_orbit
    assert all(fixed_typed(state, edges, incidence)[1].bit_count() < 2
               for state in bad_orbit)

    state = AFTER_COMPLEMENT
    for pair, component, expected in KEMPE_PATH:
        assert component in components(state, pair, edges, incidence)
        state = switched(state, pair, component)
        assert state == expected
        check_flow(state, incidence)
    assert fixed_typed(state, edges, incidence) == (10, 3)
    assert state in orbit(AFTER_COMPLEMENT, edges, incidence)
    print("LITERAL graph6=M?AACGohBAJ?AgE_? cap=0 root=19 "
          "bad_kempe_orbit=432 complement_cycle=5 support_disjoint=1 "
          "immediate_external=0 kempe_steps=4 final_typed=10 final_external=3 PASS")


if __name__ == "__main__":
    main()
