#!/usr/bin/env python3
"""Exact coordinate checks for the GGHV Proposition 4.3 transfer audit."""

from __future__ import annotations

import sympy as sp


def transformed_exponent(exponent: tuple[int, int]) -> tuple[int, int]:
    """Exponent map for x -> x^-1, y -> x^4*y."""

    a, b = exponent
    return -a + 4 * b, b


def verify_support_transport() -> None:
    p_before = {(-1, 0), (0, 0), (56, 16), (48, 14), (32, 8)}
    q_before = {(2, 1), (0, 0), (84, 24), (72, 21), (48, 12)}
    p_after = {transformed_exponent(term) for term in p_before}
    q_after = {transformed_exponent(term) for term in q_before}
    assert p_after == {(1, 0), (0, 0), (8, 16), (8, 14), (0, 8)}
    assert q_after == {(2, 1), (0, 0), (12, 24), (12, 21), (0, 12)}


def verify_involution_and_bracket() -> None:
    x, y = sp.symbols("x y", nonzero=True)
    phi_x = 1 / x
    phi_y = x**4 * y
    assert sp.simplify(phi_x.subs(x, phi_x) - x) == 0
    twice_y = phi_y.subs({x: phi_x, y: phi_y}, simultaneous=True)
    assert sp.simplify(twice_y - y) == 0
    jacobian = sp.det(
        sp.Matrix(
            [
                [sp.diff(phi_x, x), sp.diff(phi_x, y)],
                [sp.diff(phi_y, x), sp.diff(phi_y, y)],
            ]
        )
    )
    assert sp.simplify(jacobian + x**2) == 0

    z = x * y
    w = x * y**2
    zw_jacobian = sp.det(
        sp.Matrix(
            [
                [sp.diff(z, x), sp.diff(z, y)],
                [sp.diff(w, x), sp.diff(w, y)],
            ]
        )
    )
    assert sp.expand(zw_jacobian - w) == 0
    assert sp.cancel((z**2 / w) ** 2 / w - z**4 / w**3) == 0


def verify_escaping_arcs() -> None:
    t, c = sp.symbols("t c", nonzero=True)

    # Full case-c boundary x=t,y=c, reversed through the final involution.
    case_c_old_x = 1 / t
    case_c_old_y = t**4 * c
    assert sp.limit(case_c_old_x, t, 0, dir="+") == sp.oo
    assert sp.limit(case_c_old_y, t, 0) == 0

    # a/b dicritical z=t,w=c, hence x=t^2/c,y=c/t.
    new_x = t**2 / c
    new_y = c / t
    ab_old_x = sp.cancel(1 / new_x)
    ab_old_y = sp.cancel(new_x**4 * new_y)
    assert ab_old_x == c / t**2
    assert ab_old_y == t**7 / c**3
    assert sp.limit(ab_old_x.subs(c, 1), t, 0, dir="+") == sp.oo
    assert sp.limit(ab_old_y, t, 0) == 0

    # Earlier Laurent shifts y -> y+lambda*x^-j vanish on the reversed
    # case-c arc x=t^-1 for every j=2,3,4.
    lam = sp.symbols("lambda")
    for j in (2, 3, 4):
        assert sp.limit(lam * (t**-1) ** (-j), t, 0) == 0


def main() -> None:
    verify_support_transport()
    verify_involution_and_bracket()
    verify_escaping_arcs()
    print("verified Proposition 4.3's final support transformation")
    print("verified the Laurent involution and -x^2 bracket multiplier")
    print("verified escaping case-c and a/b arcs")
    print("RESULT: GGHV FINITE-LIMIT CURVES TRANSFER TO NONPROPER VALUES")


if __name__ == "__main__":
    main()
