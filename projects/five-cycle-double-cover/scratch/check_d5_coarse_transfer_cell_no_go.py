#!/usr/bin/env python3
"""Literal coarse-cell no-go inside the order-12 capped ladder."""

from __future__ import annotations

from collections import deque


A, B, C = 0b00011, 0b00101, 0b00110  # 01,02,12
EDGES = (
    (0, 2), (1, 2), (0, 3), (1, 3), (2, 3), (0, 4),
    (1, 5), (4, 5), (6, 7), (4, 6), (5, 7), (6, 8),
    (7, 9), (8, 10), (9, 10), (8, 11), (9, 11), (10, 11),
)
STATE = (
    A, C, C, A, B, B, B, C, C, A, A, B, B, A, C, C, A, B,
)
ROOTS = (1, 14)
Y01 = A


INCIDENCE = [[] for _ in range(12)]
for edge, (left, right) in enumerate(EDGES):
    INCIDENCE[left].append(edge)
    INCIDENCE[right].append(edge)


def factor_components(pair_mask):
    unseen = {
        edge
        for edge, label in enumerate(STATE)
        if (label & pair_mask).bit_count() == 1
    }
    answer = []
    while unseen:
        first = unseen.pop()
        component = {first}
        stack = [first]
        while stack:
            edge = stack.pop()
            for vertex in EDGES[edge]:
                for other in INCIDENCE[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        component.add(other)
                        stack.append(other)
        answer.append(tuple(sorted(component)))
    return tuple(sorted(answer))


def main():
    assert all(len(row) == 3 for row in INCIDENCE)
    assert all(
        STATE[row[0]] ^ STATE[row[1]] ^ STATE[row[2]] == 0
        for row in INCIDENCE
    )
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
        assert len(seen) == 12

    # Coarse ports are B,B; the exposed middle cut is A.
    assert STATE[5] == STATE[6] == B
    assert STATE[11] == STATE[12] == B
    assert STATE[9] == STATE[10] == A
    assert (B & Y01).bit_count() == 1
    assert (C & Y01).bit_count() == 1
    assert (A & Y01).bit_count() != 1

    components = factor_components(Y01)
    assert components == (
        (1, 2, 4, 5, 6, 7),
        (8, 11, 12, 14, 15, 17),
    )
    assert not any(all(root in component for root in ROOTS) for component in components)
    print(
        "PASS: both coarse B ports are Y01-active but separate C-rung "
        "U-turns block transfer; refined cut word is B,A,B"
    )


if __name__ == "__main__":
    main()
