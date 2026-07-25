#!/usr/bin/env python3
"""Audit the normalized negative-tail obstruction on the r2 chart."""

from __future__ import annotations

import sympy as sp


def bracket(
    p_grade: int,
    p: sp.Expr,
    q_grade: int,
    q: sp.Expr,
    h: sp.Symbol,
) -> sp.Expr:
    return sp.expand(
        q_grade * sp.diff(p, h) * q
        - p_grade * p * sp.diff(q, h)
    )


def solve_euler(
    order: int,
    forcing: sp.Expr,
    h: sp.Symbol,
) -> sp.Expr:
    """Solve L_order(n)=-forcing with zero h^-order resonance."""
    solution = 0
    for term in sp.Add.make_args(sp.expand(forcing)):
        coefficient, exponent = term.as_coeff_exponent(h)
        input_exponent = exponent - 7
        multiplier = -8 * (order + input_exponent)
        assert multiplier != 0, (order, exponent, term)
        solution += -coefficient * h**input_exponent / multiplier
    return sp.expand(solution)


def main() -> None:
    h, t = sp.symbols("h t", nonzero=True)
    r2, r3, r4 = sp.symbols("r2 r3 r4")
    s0, s1, s2, s3 = sp.symbols("s0 s1 s2 s3")
    w0, w1, w2 = sp.symbols("w0 w1 w2")
    r = r2 * h**2 + r3 * h**3 + r4 * h**4
    s = s0 + s1 * h + s2 * h**2 + s3 * h**3
    w = w0 + w1 * h + w2 * h**2
    p8 = h**8
    p7 = h**4 * r
    p6 = sp.expand(r**2 / 4 + h**4 * s)
    p5 = sp.expand(r * s / 2 + h**4 * w)
    n10 = (
        -sp.Rational(1, 40) * h**-5
        - t * h**-6 / 16
        - t**2 * h**-7 / 24
    )
    target = bracket(8, p8, -10, n10, h)
    assert sp.expand(target - (h + t) ** 2) == 0

    forcing11 = bracket(7, p7, -10, n10, h)
    n11 = solve_euler(11, forcing11, h)
    equation11 = sp.expand(
        bracket(8, p8, -11, n11, h) + forcing11
    )
    assert equation11 == 0

    forcing12 = sp.expand(
        bracket(7, p7, -11, n11, h)
        + bracket(6, p6, -10, n10, h)
    )
    n12 = solve_euler(12, forcing12, h)
    equation12 = sp.expand(
        bracket(8, p8, -12, n12, h) + forcing12
    )
    assert equation12 == 0

    forcing13 = sp.expand(
        bracket(7, p7, -12, n12, h)
        + bracket(6, p6, -11, n11, h)
        + bracket(5, p5, -10, n10, h)
    )
    obstruction = sp.factor(forcing13.coeff(h, -6))
    K = r2**2 / 4 + s0
    L = r2 * s0 / 2
    expected = (
        -sp.Rational(5, 1024)
        * t**2
        * (-48 * K * r2 + 128 * L + 11 * r2**3)
    )
    assert sp.expand(obstruction - expected) == 0
    simplified = sp.factor(obstruction)
    expected_simplified = (
        -sp.Rational(5, 1024)
        * r2
        * t**2
        * (16 * s0 - r2**2)
    )
    assert sp.expand(simplified - expected_simplified) == 0
    print("n11 =", n11)
    print("n12 =", n12)
    print("L13 cokernel h^-6 =", simplified)


if __name__ == "__main__":
    main()
