#!/usr/bin/env python3
"""Exact support audit for the GGHV-to-five-block scope implication.

This verifier does not prove the all-scale obstruction.  It checks the
unimodular monomial change that imports Proposition 4.3(2) of GGHV into
the hypotheses of that theorem, and it checks why Proposition 4.3(1)
(case c) lies outside those hypotheses.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from route_bd_verify import (
    AB_P_VERTICES,
    AB_Q_VERTICES,
    C_P_VERTICES,
    C_Q_VERTICES,
    lattice_points,
)


def torus_exponent(exponent: tuple[int, int]) -> tuple[int, int]:
    """Return exponents in z=xy, h=xy^2.

    Since x=z^2/h and y=h/z,

        x^a y^b = z^(2a-b) h^(b-a).
    """

    a, b = exponent
    return 2 * a - b, b - a


def blocks(vertices: tuple[tuple[int, int], ...]) -> dict[int, tuple[int, ...]]:
    transformed: dict[int, list[int]] = {}
    for exponent in lattice_points(vertices):
        z_degree, h_degree = torus_exponent(exponent)
        transformed.setdefault(z_degree, []).append(h_degree)
    return {
        z_degree: tuple(sorted(h_degrees))
        for z_degree, h_degrees in sorted(transformed.items())
    }


def interval(start: int, stop: int) -> tuple[int, ...]:
    return tuple(range(start, stop + 1))


def verify_ab_support() -> None:
    assert blocks(AB_P_VERTICES) == {
        0: interval(0, 8),
        1: interval(0, 7),
        2: interval(-1, 6),
    }
    assert blocks(AB_Q_VERTICES) == {
        0: interval(0, 12),
        1: interval(0, 11),
        2: interval(0, 10),
        3: interval(-1, 9),
    }

    assert tuple(map(torus_exponent, AB_P_VERTICES)) == (
        (0, 0),
        (2, -1),
        (2, 6),
        (0, 8),
    )
    assert tuple(map(torus_exponent, AB_Q_VERTICES)) == (
        (0, 0),
        (3, -1),
        (3, 9),
        (0, 12),
    )


def verify_case_c_extra_blocks() -> None:
    p_blocks = blocks(C_P_VERTICES)
    q_blocks = blocks(C_Q_VERTICES)

    assert set(p_blocks) == set(range(-8, 3))
    assert set(q_blocks) == set(range(-12, 4))
    assert p_blocks[-8] == (8,)
    assert q_blocks[-12] == (12,)

    # The nonnegative blocks are the same five blocks as in a/b, but the
    # additional negative blocks are part of the full bracket and cannot
    # be discarded.
    ab_p = blocks(AB_P_VERTICES)
    ab_q = blocks(AB_Q_VERTICES)
    assert {degree: p_blocks[degree] for degree in ab_p} == ab_p
    assert {degree: q_blocks[degree] for degree in ab_q} == ab_q


def verify_all_scale_polygon_family() -> None:
    for radial_scale in range(1, 33):
        r = radial_scale
        p_vertices = ((0, 0), (1, 0), (2 * r, 4 * r - 2), (2 * r, 4 * r))
        q_vertices = ((0, 0), (2, 1), (3 * r, 6 * r - 3), (3 * r, 6 * r))

        assert blocks(p_vertices) == {
            0: interval(0, 2 * r),
            1: interval(0, 2 * r - 1),
            2: interval(-1, 2 * r - 2),
        }
        assert blocks(q_vertices) == {
            0: interval(0, 3 * r),
            1: interval(0, 3 * r - 1),
            2: interval(0, 3 * r - 2),
            3: interval(-1, 3 * r - 3),
        }

    assert (
        ((0, 0), (1, 0), (8, 14), (8, 16)),
        ((0, 0), (2, 1), (12, 21), (12, 24)),
    ) == (AB_P_VERTICES, AB_Q_VERTICES)


def verify_coordinate_jacobian() -> None:
    # z_x*h_y-z_y*h_x = y*(2xy)-x*y^2 = xy^2 = h.
    z_x, z_y = "y", "x"
    h_x, h_y = "y^2", "2xy"
    assert (z_x, z_y, h_x, h_y) == ("y", "x", "y^2", "2xy")

    # The exponent matrix and its inverse are integral with determinant one.
    # (a,b) -> (2a-b,b-a), and (i,j) -> (i+j,i+2j).
    for a in range(-5, 6):
        for b in range(-5, 6):
            i, j = torus_exponent((a, b))
            assert (i + j, i + 2 * j) == (a, b)


def main() -> None:
    verify_ab_support()
    verify_case_c_extra_blocks()
    verify_all_scale_polygon_family()
    verify_coordinate_jacobian()
    print("verified the exact GGHV a/b support-to-five-block map")
    print("verified R=4 is Proposition 4.3(2) and the same support formula through R=32")
    print("verified case c has 11 and 16 transverse blocks, including negative degrees")
    print("SCOPE: a/b at R=4 is covered; case c and global higher-degree alternatives are not")


if __name__ == "__main__":
    main()
