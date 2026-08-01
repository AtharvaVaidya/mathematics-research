#!/usr/bin/env python3
"""Independent finite replay of the relevant-cap structural arithmetic."""

from __future__ import annotations

from fractions import Fraction
from itertools import product


SIDES = (0, 1)


def spoke_crossings(root_status: str, inserted_side: int) -> int:
    if root_status == "cross":
        endpoints = (0, 1)
    elif root_status == "left":
        endpoints = (0, 0)
    elif root_status == "right":
        endpoints = (1, 1)
    else:
        raise AssertionError(root_status)
    return sum(endpoint != inserted_side for endpoint in endpoints)


def reconstructed_minimum(first: str, second: str) -> int:
    crossing_roots = (first == "cross") + (second == "cross")
    old_edges = 3 - crossing_roots
    return min(
        old_edges
        + spoke_crossings(first, u_side)
        + spoke_crossings(second, v_side)
        + (u_side != v_side)
        for u_side, v_side in product(SIDES, repeat=2)
    )


def cut_table() -> None:
    assert reconstructed_minimum("cross", "cross") == 3
    assert reconstructed_minimum("cross", "left") == 3
    assert reconstructed_minimum("cross", "right") == 3
    assert reconstructed_minimum("left", "left") == 3
    assert reconstructed_minimum("right", "right") == 3
    assert reconstructed_minimum("left", "right") == 4
    assert reconstructed_minimum("right", "left") == 4
    print("CUT_TABLE unique_noncyclic4_candidate=opposite_noncrossing PASS")


def local_walk_table() -> None:
    # Degree-three centers with k degree-two neighbours.
    degree_three = []
    for k in range(4):
        values = [1] * k + [2] * (3 - k)
        contribution = sum(
            values[i] * values[j]
            for i in range(3) for j in range(3) if i != j
        )
        degree_three.append(contribution)
    assert degree_three == [24, 16, 10, 6]
    assert all(value >= 24 - 8 * k
               for k, value in enumerate(degree_three))

    degree_two = []
    for k in range(3):
        values = [1] * k + [2] * (2 - k)
        contribution = sum(
            values[i] * values[j]
            for i in range(2) for j in range(2) if i != j
        )
        degree_two.append(contribution)
    assert degree_two == [8, 4, 2]
    assert degree_two == [8 - 5 * k + k * k for k in range(3)]
    print("WALK_LOCAL degree3=24,16,10,6 degree2=8,4,2 PASS")


def moore_arithmetic() -> None:
    # Directly replay every integer order in the forbidden interval.
    forbidden = []
    for n in range(9, 43):
        lower_walks = (3 * n - 3) + (6 * n - 12) + (12 * n - 36) + (24 * n - 96)
        assert lower_walks == 45 * n - 147
        if n * n < n + lower_walks:
            forbidden.append(n)
    assert forbidden == list(range(9, 43))

    discriminant = 46 * 46 - 4 * 147
    assert discriminant == 4 * 382
    assert 19 * 19 < 382 < 20 * 20
    # 23+sqrt(382) is strictly between 42 and 43.
    assert Fraction(42 - 23) ** 2 < 382 < Fraction(43 - 23) ** 2
    print("ORDER_BOUND n^2>=46n-147 implies n>=43 cap_order>=44 PASS")


def typed_set_algebra() -> None:
    # Physical pairs are the three edges of a triangle.  Port coverage is
    # equivalent to selecting at least two of them.
    pair_ports = ({0, 1}, {0, 2}, {1, 2})
    covering = []
    for mask in range(1 << 3):
        selected = [pair_ports[i] for i in range(3) if (mask >> i) & 1]
        if set().union(*selected) == {0, 1, 2}:
            covering.append(mask)
    assert covering == [3, 5, 6, 7]
    assert all(first & second for first in covering for second in covering)
    print("TAIT_EXTERNAL_COVER two_external_covers_always_intersect PASS")


if __name__ == "__main__":
    cut_table()
    local_walk_table()
    moore_arithmetic()
    typed_set_algebra()
    print("PASS")
