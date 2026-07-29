#!/usr/bin/env python3
"""Independent brute-force audit of the two local frontier lemmas.

This implementation shares no code with verify.py.  It directly scans all
3^9 assignments on K_{3,3}, derives the edge-deleted pole, and checks the
two-terminal cut parity from incidence counts rather than the classifier.
"""

from __future__ import annotations

import itertools


K33 = tuple((u, v) for u in range(3) for v in range(3, 6))
MISSING = K33.index((0, 3))


def valid_k33(row):
    for vertex in range(6):
        seen = {
            row[index]
            for index, edge in enumerate(K33)
            if vertex in edge
        }
        if seen != {1, 2, 3}:
            return False
    return True


def k33_audit():
    colourings = tuple(
        row
        for row in itertools.product((1, 2, 3), repeat=9)
        if valid_k33(row)
    )
    assert len(colourings) == 12
    pole_rows = set()
    for row in colourings:
        terminal = row[MISSING]
        pole_rows.add(
            (terminal, terminal)
            + row[:MISSING]
            + row[MISSING + 1 :]
        )
    assert len(pole_rows) == 12

    canonical = {
        min(
            tuple(permutation[value - 1] for value in row)
            for permutation in itertools.permutations((1, 2, 3))
        )
        for row in colourings
    }
    assert len(canonical) == 2
    return len(colourings), len(canonical)


def matchings(items):
    if not items:
        yield ()
        return
    root = items[0]
    for offset in range(1, len(items)):
        mate = items[offset]
        remainder = items[1:offset] + items[offset + 1 :]
        for tail in matchings(remainder):
            yield ((root, mate),) + tail


def direct_cut_check(order, matching):
    # The alternating support edge colours are 0,1,0,1,... up to translation.
    edge_colour = tuple(index & 1 for index in range(order))
    for first, second in matching:
        parity = [0, 0, 0, 0]
        for vertex in (first, second):
            parity[edge_colour[(vertex - 1) % order]] ^= 1
            parity[edge_colour[vertex]] ^= 1
        # An edge internal to the two-vertex block was counted twice, which
        # changes its integer count by two and hence not its parity.
        if any(parity):
            return False
    return True


def pairing_audit():
    total = 0
    by_order = {}
    for order in range(2, 15, 2):
        count = 0
        for matching in matchings(tuple(range(order))):
            assert direct_cut_check(order, matching)
            count += 1
        by_order[order] = count
        total += count
    assert by_order == {
        2: 1,
        4: 3,
        6: 15,
        8: 105,
        10: 945,
        12: 10395,
        14: 135135,
    }
    return total


def main():
    colourings, orbits = k33_audit()
    pairings_checked = pairing_audit()
    print(
        f"K33_DIRECT assignments=19683 proper={colourings}"
        f" global_colour_orbits={orbits}"
    )
    print(
        f"PAIRING_INCIDENCE_AUDIT checked={pairings_checked}"
        " support_orders=2,4,6,8,10,12,14 all_clean=yes"
    )
    print("PASS: independent local audit")


if __name__ == "__main__":
    main()
