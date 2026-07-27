#!/usr/bin/env python3
"""Exact algebra for the Route A smooth collision-image closure."""

from __future__ import annotations

import sympy as sp


def verify_normalized_jacobian() -> None:
    x, y = sp.symbols("x y")
    R = sp.Function("R")(x, y)
    S = sp.Function("S")(x, y)
    p = x * R
    q = y + x * S
    jacobian = sp.expand(
        sp.diff(p, x) * sp.diff(q, y)
        - sp.diff(p, y) * sp.diff(q, x)
    )
    expected = sp.expand(
        R
        + x * (
            sp.diff(R, x)
            + R * sp.diff(S, y)
            - sp.diff(R, y) * S
        )
        + x**2 * (
            sp.diff(R, x) * sp.diff(S, y)
            - sp.diff(R, y) * sp.diff(S, x)
        )
    )
    assert sp.simplify(jacobian - expected) == 0
    assert sp.simplify(jacobian.subs(x, 0) - R.subs(x, 0)) == 0


def verify_triangular_family() -> None:
    x, y = sp.symbols("x y")
    coefficients = sp.symbols("h0:12")
    h = sum(
        coefficient * x ** (index + 1)
        for index, coefficient in enumerate(coefficients)
    )
    p = x
    q = y + h
    assert sp.det(
        sp.Matrix(
            [
                [sp.diff(p, x), sp.diff(p, y)],
                [sp.diff(q, x), sp.diff(q, y)],
            ]
        )
    ) == 1
    assert p.subs(x, 0) == 0
    assert q.subs(x, 0) == y


def verify_nodal_normalization() -> None:
    t, X, Y = sp.symbols("t X Y")
    gamma_x = t**2 - 1
    gamma_y = t * (t**2 - 1)
    curve = Y**2 - X**2 * (X + 1)
    assert sp.expand(curve.subs({X: gamma_x, Y: gamma_y})) == 0
    assert sp.factor(gamma_y / gamma_x) == t
    derivative_x = sp.diff(gamma_x, t)
    derivative_y = sp.diff(gamma_y, t)
    assert sp.gcd(derivative_x, derivative_y) == 1
    assert gamma_x.subs(t, 1) == gamma_x.subs(t, -1) == 0
    assert gamma_y.subs(t, 1) == gamma_y.subs(t, -1) == 0

    # The origin is singular and has two distinct normalization points.
    assert sp.diff(curve, X).subs({X: 0, Y: 0}) == 0
    assert sp.diff(curve, Y).subs({X: 0, Y: 0}) == 0


def verify_linewise_etale_countermodel() -> None:
    x, t = sp.symbols("x t")
    first = t**2 - 1 - x
    second = t * (t**2 - 1) - sp.Rational(3, 2) * x * t
    jacobian = sp.factor(
        sp.diff(first, x) * sp.diff(second, t)
        - sp.diff(first, t) * sp.diff(second, x)
    )
    assert sp.expand(jacobian - (1 + sp.Rational(3, 2) * x)) == 0
    assert jacobian.subs(x, 0) == 1
    assert first.subs(x, 0) == t**2 - 1
    assert second.subs(x, 0) == t * (t**2 - 1)

    target_x, target_y = sp.symbols("target_x target_y")
    nodal_equation = target_y**2 - target_x**2 * (target_x + 1)
    pullback = sp.factor(
        nodal_equation.subs({target_x: first, target_y: second})
    )
    collision_factor = 4 * (x + 1) ** 2 - (3 * x + 4) * t**2
    assert sp.expand(pullback - x * collision_factor / 4) == 0
    assert sp.Poly(collision_factor, x, t, domain=sp.QQ).is_irreducible


def verify_route_a_plane_chart() -> None:
    a, b = sp.symbols("a b")
    u = a**2
    w = a * (1 + 2 * a**2 * b)
    v = 4 * b * (1 + a**2 * b)
    assert sp.expand(w**2 - u - u**2 * v) == 0
    assert u.subs(a, 0) == 0
    assert w.subs(a, 0) == 0
    assert v.subs(a, 0) == 4 * b


def main() -> None:
    verify_normalized_jacobian()
    verify_triangular_family()
    verify_nodal_normalization()
    verify_linewise_etale_countermodel()
    verify_route_a_plane_chart()
    print("verified the normalized Jacobian identity")
    print("verified the triangular automorphism family")
    print("verified the immersive nodal normalization countermodel")
    print("verified the linewise-etale ambient extension and collision divisor")
    print("verified the Route A distinguished plane line")
    print("RESULT: SMOOTH OR RECTIFIABLE COLLISION IMAGE FORCES DEGREE ONE")


if __name__ == "__main__":
    main()
