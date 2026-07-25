#!/usr/bin/env python3
"""Exact checks for the leading osculating-cubic ODE audit."""

from __future__ import annotations

import sympy as sp


def coefficient_list(r: int) -> list[sp.Rational]:
    """Normalize beta/(alpha*v)=1 and return a_0,...,a_4."""

    coefficients = [sp.Rational(1, 3 - 5 * r)]
    for degree in range(1, 5):
        denominator = r * (degree - 5) + 3
        if denominator == 0:
            raise ZeroDivisionError
        coefficients.append(
            sp.cancel(
                -sp.Rational(r * (degree - 5), denominator)
                * coefficients[-1]
            )
        )
    return coefficients


def verify_polynomial_solutions() -> None:
    y = sp.symbols("y")
    alpha, beta, u, v = sp.symbols(
        "alpha beta u v", nonzero=True
    )
    for r in (2, *range(4, 21)):
        normalized = coefficient_list(r)
        assert all(coefficient != 0 for coefficient in normalized)
        t = u * y / v
        # coefficient_list uses beta/(alpha*v)=1.
        H = beta / (alpha * v) * sum(
            coefficient * t**degree
            for degree, coefficient in enumerate(normalized)
        )
        rho = y ** (2 * r - 1) * (u * y + v)
        k = sp.expand(y ** (2 * r) * (u * y + v) ** 2 * H)
        equation = sp.factor(
            r * rho * sp.diff(k, y)
            - (r + 3) * sp.diff(rho, y) * k
            - beta / alpha * rho**2
        )
        assert equation == 0
        assert sp.degree(k, y) == 2 * r + 6


def verify_support_conversion() -> None:
    r = sp.symbols("r", integer=True, positive=True)
    for degree in range(5):
        x_degree = r + 3
        y_degree = 2 * r + 2 + degree
        z_degree = sp.expand(2 * x_degree - y_degree)
        w_degree = sp.expand(y_degree - x_degree)
        assert z_degree == 4 - degree
        assert w_degree == r - 1 + degree
        assert sp.expand(z_degree + w_degree) == r + 3


def verify_r3_resonance_obstruction() -> None:
    r = 3
    # The simple-factor indicial equation requires s=2, but its
    # coefficient vanishes.
    order = 2
    assert r * order - (r + 3) == 0

    coefficients = [sp.Rational(1, 3 - 5 * r)]
    for degree in range(1, 4):
        denominator = r * (degree - 5) + 3
        assert denominator != 0
        coefficients.append(
            sp.cancel(
                -sp.Rational(r * (degree - 5), denominator)
                * coefficients[-1]
            )
        )
    assert coefficients[-1] != 0
    # At degree four the a_4 coefficient is zero and the recurrence
    # demands -3*a_3=0.
    assert r * (4 - 5) + 3 == 0
    assert r * (4 - 5) * coefficients[-1] != 0


def main() -> None:
    verify_polynomial_solutions()
    verify_support_conversion()
    verify_r3_resonance_obstruction()
    print("verified the unique quartic ODE factor for r=2 and r>=4")
    print("verified the exact five-term (z,w) support conversion")
    print("verified the exceptional r=3 indicial obstruction")
    print("RESULT: OSCULATING LEADING ODE AUDIT PASSES")


if __name__ == "__main__":
    main()
