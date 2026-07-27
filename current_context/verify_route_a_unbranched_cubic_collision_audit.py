#!/usr/bin/env python3
"""Exact checks for ROUTE_A_UNBRANCHED_CUBIC_COLLISION_AUDIT.md.

Normalization, the class group, and the mandatory collision theorem are
theorem-level inputs.  This script verifies all explicit countermodels,
degree computations, brackets, and divisor factorizations.
"""

from __future__ import annotations

import sympy as sp


u, v, w = sp.symbols("u v w")
h_surface = w**2 - u - u**2 * v


def bracket(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    """Negative hypersurface Jacobian bracket used in Route A."""

    return sp.expand(
        -sp.det(
            sp.Matrix(
                [
                    [sp.diff(h_surface, z) for z in (u, v, w)],
                    [sp.diff(left, z) for z in (u, v, w)],
                    [sp.diff(right, z) for z in (u, v, w)],
                ]
            )
        )
    )


def reduce_surface(expression: sp.Expr) -> sp.Expr:
    return sp.rem(
        sp.Poly(sp.expand(expression), w),
        sp.Poly(h_surface, w),
    ).as_expr()


def class_table() -> None:
    # The values represent classes in Cl(B)=Z/2.  The group computation
    # itself is a theorem-level input.
    D = 1
    principal = 0
    assert (D + D) % 2 == principal

    # One retained mate must be nonprincipal.
    C = (-D) % 2
    assert C == D

    # With two retained mates, exactly one is nonprincipal.
    solutions = [
        (c1, c2)
        for c1 in (0, 1)
        for c2 in (0, 1)
        if (D + c1 + c2) % 2 == 0
    ]
    assert solutions == [(0, 1), (1, 0)]


def same_surface_one_plus_one_plus_one() -> None:
    s = sp.symbols("s")
    A = s * (1 + s) * (1 + 2 * s)
    q = -v - 2 * u * v**2

    assert bracket(w, q) == 1 + 6 * u * v + 6 * u**2 * v**2
    assert reduce_surface(bracket(w, q) - (1 + 6 * v * w**2)) == 0

    # The target relation A(s)+y*w^2=0 is cubic and has three simple
    # roots above w=0.
    assert sp.degree(A, s) == 3
    assert sp.factor(A) == s * (s + 1) * (2 * s + 1)
    A_prime = sp.diff(A, s)
    assert A_prime.subs(s, 0) == 1
    assert A_prime.subs(s, -1) == 1
    assert A_prime.subs(s, -sp.Rational(1, 2)) == -sp.Rational(1, 2)

    # In the Laurent chart, q=-A(s)/w^2.
    v_laurent = s * (1 + s) / w**2
    assert sp.cancel(q.subs({u: w**2 / (1 + s), v: v_laurent})
                     + A / w**2) == 0

    # The special fiber is D+H on S.
    assert sp.factor(h_surface.subs(w, 0)) == -u * (1 + u * v)
    assert q.subs({u: 0, w: 0}) == -v
    assert sp.simplify(q.subs({v: -1 / u, w: 0}) - v.subs(v, -1 / u)) == 0

    # The bracket is exactly one on both retained components.
    jac = bracket(w, q)
    assert jac.subs({u: 0, w: 0}) == 1
    assert sp.simplify(jac.subs({v: -1 / u, w: 0})) == 1

    # It is not a global Darboux pair.
    test_point = {u: 1, v: 1, w: sp.sqrt(2)}
    assert sp.simplify(h_surface.subs(test_point)) == 0
    assert sp.expand(jac.subs(test_point)) != 1


def exact_one_plus_two_model() -> None:
    t, y = sp.symbols("t y")
    x_pullback = t * (t**2 + y * t + 1)
    jac = sp.expand(sp.diff(x_pullback, t))
    assert jac == 3 * t**2 + 2 * y * t + 1

    # The target line x=0 has one linear and one quadratic prime.
    assert sp.factor(x_pullback) == t * (t**2 + t * y + 1)
    assert jac.subs(t, 0) == 1

    y_on_quadratic = -t - 1 / t
    jac_on_quadratic = sp.factor(jac.subs(y, y_on_quadratic))
    assert sp.expand(jac_on_quadratic - (t**2 - 1)) == 0

    # y=-(t+t^-1) has rational-map degree two on G_m.
    numerator, denominator = sp.fraction(sp.cancel(y_on_quadratic))
    assert max(sp.degree(numerator, t), sp.degree(denominator, t)) == 2

    # The linear component is disjoint from the ramification curve, while
    # the quadratic component meets it only at t=+/-1.
    assert sp.solve(
        [sp.Eq(t**2 + y * t + 1, 0), sp.Eq(jac, 0)],
        [t, y],
        dict=True,
    ) == [{t: -1, y: 2}, {t: 1, y: -2}]


def same_surface_one_plus_two_first_neighborhood() -> None:
    q2 = v + u * v**2 + u**2

    assert q2.subs({u: 0, w: 0}) == v
    assert sp.simplify(q2.subs({v: -1 / u, w: 0}) - u**2) == 0

    jac = bracket(w, q2)
    assert jac.subs({u: 0, w: 0}) == -1
    assert sp.simplify(jac.subs({v: -1 / u, w: 0})) == 2 * u**3

    # With w generic, q2 is a degree-five rational function of u.
    q2_laurent = sp.cancel(q2.subs(v, (w**2 - u) / u**2))
    numerator, denominator = sp.fraction(q2_laurent)
    assert sp.degree(numerator, u) == 5
    assert sp.degree(denominator, u) == 3
    assert sp.gcd(sp.Poly(numerator, u), sp.Poly(denominator, u)).degree() == 0


def smooth_collision_fiber() -> None:
    # dw never vanishes on S: h_u=h_v=0 has no point.
    h_u = sp.diff(h_surface, u)
    h_v = sp.diff(h_surface, v)
    basis = sp.groebner([h_surface, h_u, h_v], v, w, u, order="lex")
    assert list(basis) == [1]


def main() -> None:
    class_table()
    same_surface_one_plus_one_plus_one()
    exact_one_plus_two_model()
    same_surface_one_plus_two_first_neighborhood()
    smooth_collision_fiber()
    print("verified: unbranched cubic class table in Cl(B)=Z/2")
    print("verified: same-surface degree-three 1+1+1 countermodel")
    print("verified: exact etale-open degree-three 1+2 countermodel")
    print("verified: same-surface 1+2 class and first-neighborhood data")
    print("verified: normal/conormal geometry has no local zero of dw")
    print("RESULT: divisor classes, normal bundles, and conductors do not")
    print("        exclude the unbranched cubic D-collision")


if __name__ == "__main__":
    main()
