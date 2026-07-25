#!/usr/bin/env python3
"""Exact checks for the delta=1 cusp-jet classification and countermodels."""

from __future__ import annotations

import sympy as sp


def bracket(
    left: sp.Expr,
    right: sp.Expr,
    z: sp.Symbol,
    w: sp.Symbol,
) -> sp.Expr:
    return sp.expand(
        sp.diff(left, z) * sp.diff(right, w)
        - sp.diff(left, w) * sp.diff(right, z)
    )


def verify_valuation_ledger() -> None:
    for m in range(2, 9):
        for n in range(m + 1, min(2 * m, 13)):
            for r in range(0, 8):
                valuations = (
                    n - 2 * m - 2,
                    n - 3 * m + 2 * r - 1,
                    n - 4 * m + 4 * r,
                )
                minimum_count = sum(
                    value == min(valuations) for value in valuations
                )
                if minimum_count < 2:
                    continue
                q3_valuations = (
                    n - 2 * m + r - 1,
                    n - 3 * m + 3 * r,
                )
                if min(q3_valuations) != -1:
                    continue
                assert 2 * r == m - 1
                assert 2 * n == 3 * m + 1

    candidates = [
        (m, (3 * m + 1) // 2, (m - 1) // 2)
        for m in range(2, 9)
        if m % 2 == 1 and (3 * m + 1) // 2 <= 12
    ]
    assert candidates == [(3, 5, 1), (5, 8, 2), (7, 11, 3)]


def model_data(
    m: int,
) -> tuple[
    sp.Symbol,
    sp.Symbol,
    sp.Symbol,
    sp.Symbol,
    sp.Expr,
    sp.Expr,
    sp.Expr,
]:
    w, z, C, b = sp.symbols("w z C b", nonzero=True)
    n = (3 * m + 1) // 2
    r = (m - 1) // 2
    lam = sp.Rational(n, m)
    condition = sp.factor(
        12
        + 12 * (lam - 2) * C**2
        + (lam - 2) * (lam - 3) * C**4
    )
    normalizer = sp.factor(
        lam
        * (lam - 1)
        * C
        * (1 + (lam - 2) * C**2 / 6)
    )
    P = w**m + C * w**r * z + z**2 / w
    Q = b * (
        w**n
        + lam * C * w**m * z
        + lam * (1 + (lam - 1) * C**2 / 2) * w**r * z**2
        + normalizer * z**3 / w
    )
    return w, z, C, b, condition, normalizer, sp.expand(bracket(P, Q, z, w))


def verify_exact_countermodels() -> None:
    for m in (3, 5, 7):
        w, z, C, b, condition, normalizer, jacobian = model_data(m)
        polynomial = sp.Poly(jacobian, z)

        # The only possible unwanted term is z^3, and it is a nonzero
        # scalar multiple of the quartic condition.
        coefficient3 = sp.factor(polynomial.coeff_monomial(z**3))
        assert sp.rem(
            sp.Poly(coefficient3 * w / b, C),
            sp.Poly(condition, C),
        ) == 0

        coefficient4 = sp.factor(polynomial.coeff_monomial(z**4))
        assert sp.simplify(coefficient4 - b * normalizer / w**3) == 0
        assert all(
            polynomial.coeff_monomial(z**degree) == 0
            for degree in range(3)
        )

        # A root of the quartic condition never kills the normalizer.
        resultant = sp.factor(sp.resultant(condition, normalizer, C))
        assert resultant != 0

        # In the quotient by condition and b*normalizer=1, J=z^4/w^3.
        normalized_difference = sp.expand(
            jacobian.subs(b, 1 / normalizer) - z**4 / w**3
        )
        numerator = sp.together(normalized_difference).as_numer_denom()[0]
        assert sp.rem(
            sp.Poly(numerator, C),
            sp.Poly(condition, C),
        ) == 0


def main() -> None:
    verify_valuation_ledger()
    verify_exact_countermodels()
    print("verified the three subquadratic Puiseux cusp types")
    print("verified exact five-block countermodels for all three types")
    print("verified the normalizing coefficient is nonzero on each model")
    print("RESULT: DELTA=1 CUSP-JET CHECKS PASS")


if __name__ == "__main__":
    main()
