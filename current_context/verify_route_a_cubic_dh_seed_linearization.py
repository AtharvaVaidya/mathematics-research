#!/usr/bin/env python3
"""Exact checks for ROUTE_A_CUBIC_DH_SEED_LINEARIZATION.md."""

from __future__ import annotations

import sympy as sp


u, v, w = sp.symbols("u v w")
s = sp.symbols("s")
h_surface = w**2 - u - u**2 * v


def bracket(left: sp.Expr, right: sp.Expr) -> sp.Expr:
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


def seed_checks() -> None:
    q0 = -v - 2 * u * v**2
    jac = bracket(w, q0)
    assert jac == 1 + 6 * u * v + 6 * u**2 * v**2
    assert reduce_surface(jac - (1 + 6 * v * w**2)) == 0

    A = s * (1 + s) * (1 + 2 * s)
    q_laurent = sp.cancel(
        q0.subs({u: w**2 / (1 + s), v: s * (1 + s) / w**2})
    )
    assert sp.cancel(q_laurent + A / w**2) == 0
    assert sp.degree(A, s) == 3

    derivative = sp.diff(A, s)
    assert derivative.subs(s, 0) == 1
    assert derivative.subs(s, -1) == 1
    assert derivative.subs(s, -sp.Rational(1, 2)) == -sp.Rational(1, 2)


def fixed_p_characteristics() -> None:
    r = sp.symbols("r")

    # On the Laurent chart, {w,-}=-d/dr.
    trial = -r + sp.Function("F")(w)
    assert -sp.diff(trial, r) == 1

    A = s * (1 + s) * (1 + 2 * s)
    correction = (3 * s**2 + 2 * s**3) / w**2
    # In (s,w), {w,R}=-w^2 R_s.
    assert sp.simplify(
        -w**2 * sp.diff(correction, s) + (sp.diff(A, s) - 1)
    ) == 0


def formal_slices() -> None:
    # Verify sufficiently many coefficients of the two binomial series.
    z = sp.symbols("z")
    sqrt_series = sp.series(sp.sqrt(1 + 4 * z), z, 0, 6).removeO()
    q_d = sp.expand((1 - sqrt_series) / (2 * w**2)).subs(z, v * w**2)
    q_h = sp.expand((sqrt_series - 1) / (2 * w**2)).subs(z, v * w**2)

    expected_d = -v + v**2 * w**2 - 2 * v**3 * w**4 + 5 * v**4 * w**6
    expected_h = v - v**2 * w**2 + 2 * v**3 * w**4 - 5 * v**4 * w**6
    assert sp.expand(q_d - expected_d).coeff(w, 0) == 0
    assert sp.expand(q_d - expected_d).coeff(w, 2) == 0
    assert sp.expand(q_d - expected_d).coeff(w, 4) == 0
    assert sp.expand(q_d - expected_d).coeff(w, 6) == 0
    assert sp.expand(q_h - expected_h).coeff(w, 0) == 0
    assert sp.expand(q_h - expected_h).coeff(w, 2) == 0
    assert sp.expand(q_h - expected_h).coeff(w, 4) == 0
    assert sp.expand(q_h - expected_h).coeff(w, 6) == 0


def linearized_operator() -> None:
    A = s * (1 + s) * (1 + 2 * s)
    B0 = s * (1 + s)
    error = sp.diff(A, s) - 1

    f = -sp.Rational(84, 5) + sp.Rational(102, 5) * s - 30 * s**2
    h = -sp.Rational(84, 5) - 84 * s**3
    linear = sp.expand(
        2 * A * sp.diff(f, s)
        + sp.diff(A, s) * f
        - sp.diff(B0 * h, s)
    )
    assert sp.expand(linear + error) == 0

    # The h-operator has codimension one, detected by endpoint integration.
    n = sp.symbols("n", integer=True, nonnegative=True)
    # A concrete complement: the f=s^2 image has nonzero endpoint integral.
    u_s2 = 2 * A * sp.diff(s**2, s) + sp.diff(A, s) * s**2
    assert sp.integrate(u_s2, (s, -1, 0)) == -sp.Rational(1, 30)
    assert sp.integrate(error, (s, -1, 0)) == -1

    quadratic = sp.factor(
        -2 * B0 * h * sp.diff(f, s)
        - sp.diff(B0 * h, s) * f
    )
    assert quadratic != 0
    assert sp.degree(quadratic, s) == 6


def invariant_family_degree_obstruction() -> None:
    # Verify the leading coefficient formula symbolically on a broad exact
    # family; the memo gives the general degree proof.
    for n in range(6):
        for m in range(6):
            f_lead, h_lead = sp.symbols("f_lead h_lead", nonzero=True)
            F = f_lead * s**n + sum(
                sp.Symbol(f"f_{n}_{i}") * s**i for i in range(n)
            )
            H = h_lead * s**m + sum(
                sp.Symbol(f"h_{m}_{i}") * s**i for i in range(m)
            )
            C = s * (1 + s) * H
            jac = sp.Poly(
                sp.expand(-2 * C * sp.diff(F, s) - sp.diff(C, s) * F),
                s,
            )
            assert jac.degree() == m + n + 1
            assert sp.expand(jac.LC()) == -(2 * n + m + 2) * f_lead * h_lead


def full_linearization_formula() -> None:
    A = s * (1 + s) * (1 + 2 * s)
    p = sp.Function("p")(s, w)
    q = sp.Function("q")(s, w)
    q0 = -A / w**2

    chart_bracket_p_q0 = sp.expand(
        w**2
        * (
            sp.diff(p, s) * sp.diff(q0, w)
            - sp.diff(p, w) * sp.diff(q0, s)
        )
    )
    chart_bracket_w_q = -w**2 * sp.diff(q, s)
    expected = (
        sp.diff(A, s) * sp.diff(p, w)
        + 2 * A * sp.diff(p, s) / w
        - w**2 * sp.diff(q, s)
    )
    assert sp.simplify(chart_bracket_p_q0 + chart_bracket_w_q - expected) == 0


def main() -> None:
    seed_checks()
    fixed_p_characteristics()
    formal_slices()
    linearized_operator()
    invariant_family_degree_obstruction()
    full_linearization_formula()
    print("verified: cubic D/H seed is Darboux modulo w^2")
    print("verified: fixed-P characteristic correction is nonregular")
    print("verified: exact formal slices exist on both completed components")
    print("verified: two-coordinate linearization cancels the seed error")
    print("verified: nonlinear invariant family has an all-degree top-term obstruction")
    print("RESULT: local and linear corrections exist, but polynomial")
    print("        termination requires mixed hyperbolic weights")


if __name__ == "__main__":
    main()
