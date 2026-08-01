#!/usr/bin/env python3
"""Check an order-12 positive blocker with no fresh coordinate.

This standard-library replay reuses the generic graph/flow/metric
routines from the independently frozen order-14 checker, after
replacing only its literal graph data.
"""

from __future__ import annotations

from collections import Counter

import check_d5_cyclic_block_one_step_no_go_order14 as core


core.GRAPH6 = "K?ABCiKU@oKO"
core.VERTICES = 12
core.EDGES = (
    (0, 5), (0, 7), (0, 8),
    (1, 6), (1, 9), (1, 11),
    (2, 6), (2, 10), (2, 11),
    (3, 7), (3, 9), (3, 10),
    (4, 8), (4, 9), (4, 10),
    (5, 7), (5, 8), (6, 11),
)
core.STATE = tuple(
    int(label, 16)
    for label in (
        "03", "05", "06", "05", "14", "11",
        "0c", "14", "18", "14", "05", "11",
        "14", "11", "05", "11", "12", "09",
    )
)
core.ROOTS = (3, 15)
core.INCIDENCE = [[] for _ in range(core.VERTICES)]
for edge, (left, right) in enumerate(core.EDGES):
    core.INCIDENCE[left].append(edge)
    core.INCIDENCE[right].append(edge)

C = frozenset((0, 1, 3, 4, 7, 8, 9, 10, 12, 14, 16, 17))
H = frozenset((3, 5, 17))
D = frozenset((1, 2, 15, 16))


def main():
    core.validate_graph()
    core.validate_flow(core.STATE)
    assert core.chi(core.STATE) == 1
    used = 0
    for label in core.STATE:
        used |= label
    assert used == 0b11111
    assert not [coordinate for coordinate in range(5) if not (used >> coordinate) & 1]

    distance, blocker, profiles = core.metric_and_profiles(
        core.STATE, core.ROOTS
    )
    assert (distance, blocker) == (2, 1)
    assert len(profiles) == 7
    assert all(
        len(set(profile["P"]) & set(profile["Q"])) == 1
        for profile in profiles
    )
    assert {
        (profile["P"], profile["Q"])
        for profile in profiles
    } == {
        ((0, 4), (0, 1)),
        ((0, 4), (0, 3)),
        ((0, 4), (2, 4)),
        ((1, 2), (0, 1)),
        ((1, 2), (2, 4)),
        ((2, 3), (0, 3)),
        ((2, 3), (2, 4)),
    }
    assert any(
        profile["P"] == (0, 4)
        and profile["Q"] == (0, 1)
        and profile["C"] == C
        and profile["H"] == H
        and profile["D"] == D
        for profile in profiles
    )

    # The fresh-coordinate hypothesis is absent, but plateau descent is not
    # obstructed: this neutral root-H switch immediately gives d=1.
    rescued = core.switched(core.STATE, (0, 1), H)
    assert core.chi(rescued) == 1
    assert core.metric_and_profiles(rescued, core.ROOTS)[:2] == (1, 0)

    plateau, deltas = core.terminal_plateau(core.STATE)
    assert len(plateau) == 72
    assert deltas == Counter({0: 1224})

    print("PASS")
    print(f"graph6: {core.GRAPH6}; endpoint-sorted roots: {core.ROOTS}")
    print("terminal plateau: chi 1, 72 states mod S5, all 1224 moves neutral")
    print("(d,b*)=(2,1), but all five coordinates are used")
    print("no-fresh existence claim fails; a neutral H-switch still gives d=1")


if __name__ == "__main__":
    main()
