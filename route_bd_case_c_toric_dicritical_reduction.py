#!/usr/bin/env python3
"""Exact normal-fan and face checks for the case-c dicritical reduction."""

from __future__ import annotations

from math import gcd

import sympy as sp

from route_bd_verify import (
    C_P_VERTICES,
    C_Q_VERTICES,
    convex_hull,
    lattice_points,
)


def primitive(vector: tuple[int, int]) -> tuple[int, int]:
    divisor = gcd(abs(vector[0]), abs(vector[1]))
    return (vector[0] // divisor, vector[1] // divisor)


def inward_normals(vertices: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    hull = convex_hull(vertices)
    result = []
    for index, left in enumerate(hull):
        right = hull[(index + 1) % len(hull)]
        edge = (right[0] - left[0], right[1] - left[1])
        result.append(primitive((-edge[1], edge[0])))
    return tuple(result)


def minimizing_face(
    support: tuple[tuple[int, int], ...],
    valuation: tuple[int, int],
) -> tuple[tuple[int, int], ...]:
    values = {
        point: valuation[0] * point[0] + valuation[1] * point[1]
        for point in support
    }
    minimum = min(values.values())
    return tuple(point for point in support if values[point] == minimum)


def verify_normal_fans() -> None:
    p_normals = inward_normals(C_P_VERTICES)
    q_normals = inward_normals(C_Q_VERTICES)
    assert p_normals == ((0, 1), (-2, 1), (-1, 0), (1, -1), (1, 0))
    assert q_normals == ((-1, 2), (-2, 1), (-1, 0), (1, -1), (1, 0))

    p_support = lattice_points(C_P_VERTICES)
    q_support = lattice_points(C_Q_VERTICES)
    candidate_rays = []
    for normal in set(p_normals).intersection(q_normals):
        p_face = minimizing_face(p_support, normal)
        q_face = minimizing_face(q_support, normal)
        p_minimum = sum(a * b for a, b in zip(normal, p_face[0]))
        q_minimum = sum(a * b for a, b in zip(normal, q_face[0]))
        if p_minimum < 0 or q_minimum < 0:
            candidate_rays.append(normal)
    assert sorted(candidate_rays) == [(-2, 1), (-1, 0), (1, -1)]

    expected_faces = {
        (-2, 1): (
            tuple((u, 2 * u - 2) for u in range(1, 9)),
            tuple((u, 2 * u - 3) for u in range(2, 13)),
        ),
        (-1, 0): (
            ((8, 14), (8, 15), (8, 16)),
            ((12, 21), (12, 22), (12, 23), (12, 24)),
        ),
        (1, -1): (
            tuple((u, u + 8) for u in range(9)),
            tuple((u, u + 12) for u in range(13)),
        ),
    }
    for normal, (expected_p, expected_q) in expected_faces.items():
        assert minimizing_face(p_support, normal) == expected_p
        assert minimizing_face(q_support, normal) == expected_q


def verify_forced_face_forms() -> None:
    y, z, s, t, a, b = sp.symbols("y z s t a b", nonzero=True)

    right_p = sp.expand(a * y**14 * (y - s) ** 2)
    right_q = sp.expand(b * y**21 * (y - s) ** 3)
    assert {term[0] for term in sp.Poly(right_p, y).terms()} == {(14,), (15,), (16,)}
    assert {term[0] for term in sp.Poly(right_q, y).terms()} == {
        (21,),
        (22,),
        (23,),
        (24,),
    }
    assert sp.diff(right_p, y).subs(y, s) == 0
    assert sp.diff(right_p, y, 2).subs(y, s) != 0
    assert all(sp.diff(right_q, y, order).subs(y, s) == 0 for order in range(3))
    assert sp.diff(right_q, y, 3).subs(y, s) != 0

    top_p = sp.expand(a * (z - t) ** 8)
    top_q = sp.expand(b * (z - t) ** 12)
    assert sp.degree(top_p, z) == 8
    assert sp.degree(top_q, z) == 12
    assert all(sp.diff(top_p, z, order).subs(z, t) == 0 for order in range(8))
    assert sp.diff(top_p, z, 8).subs(z, t) != 0
    assert all(sp.diff(top_q, z, order).subs(z, t) == 0 for order in range(12))
    assert sp.diff(top_q, z, 12).subs(z, t) != 0

    # The outer Bezout identity forbids a common root U=V=0.
    U0, V0, Up0, Vp0, w0 = sp.symbols("U0 V0 Up0 Vp0 w0")
    outer_left = U0 * V0 + 2 * w0 * U0 * Vp0 - 3 * w0 * Up0 * V0
    assert outer_left.subs({U0: 0, V0: 0}) == 0


def main() -> None:
    verify_normal_fans()
    verify_forced_face_forms()
    print("verified exactly three common negative toric face normals")
    print("verified outer coprimality removes (-2,1)")
    print("verified surviving basepoints have multiplicities (2,3) and (8,12)")


if __name__ == "__main__":
    main()
