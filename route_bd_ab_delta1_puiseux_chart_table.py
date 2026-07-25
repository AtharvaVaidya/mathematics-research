#!/usr/bin/env python3
"""Exact ledger for all marked delta=1 Puiseux projection charts.

This verifier records necessary valuation conditions.  A cell marked
"surviving" is not asserted to lift to the full five-block system.
"""

from __future__ import annotations

import sympy as sp


def leading_fractional_charts() -> None:
    candidates: list[tuple[int, int, int]] = []
    for m in range(2, 9):
        for n in range(m + 1, min(2 * m, 13)):
            for r in range(0, 9):
                z4 = (
                    n - 2 * m - 2,
                    n - 3 * m + 2 * r - 1,
                    n - 4 * m + 4 * r,
                )
                if sum(value == min(z4) for value in z4) < 2:
                    continue
                q3 = (
                    n - 2 * m + r - 1,
                    n - 3 * m + 3 * r,
                )
                if min(q3) != -1:
                    continue
                candidates.append((m, n, r))
    assert candidates == [(3, 5, 1), (5, 8, 2), (7, 11, 3)]


def vertical_projection_is_impossible() -> None:
    # Put n=ord(B-B0)<m=ord(A-A0), and s=ord(q1).
    # The fixed pole of p2 forces m-2n+2s=-1.
    survivors: list[tuple[int, int, int, int]] = []
    for n in range(2, 13):
        for m in range(n + 1, 9):
            for s in range(0, 13):
                if m - 2 * n + 2 * s != -1:
                    continue
                for order_q2 in range(0, 13):
                    z3 = (
                        m - n - 1,
                        m - 2 * n + s + order_q2,
                        m - 3 * n + 3 * s,
                    )
                    if sum(value == min(z3) for value in z3) >= 2:
                        survivors.append((m, n, s, order_q2))
    assert survivors == []

    m, n, s, order_q2 = sp.symbols("m n s order_q2", integer=True)
    solved_s = sp.solve(sp.Eq(m - 2 * n + 2 * s, -1), s)[0]
    z3_first = m - n - 1
    z3_second = m - 2 * n + s + order_q2
    z3_third = m - 3 * n + 3 * s
    assert sp.simplify(
        (z3_first - z3_third).subs(s, solved_s)
        - (3 * m - 2 * n + 1) / 2
    ) == 0
    assert sp.simplify(
        (z3_second - z3_third).subs(s, solved_s)
        - (m - n + order_q2 + 1)
    ) == 0


def quadratic_analytic_exception() -> None:
    # When g''(0) is a unit, q3's fixed pole forces ord(p1)=0.
    # Balancing g''p2^2 (valuation -2) against the first nonanalytic
    # contribution to g'''' forces N-4m=-2.
    possible = [
        (m, 4 * m - 2)
        for m in range(3, 9)
        if 4 * m - 2 <= 24
    ]
    assert possible == [(3, 10), (4, 14), (5, 18), (6, 22)]

    # Degree-(8,12) contact rules out m=5 and m=6.  Source and target
    # scalings normalize the leading and top A coefficients and the
    # quadratic graph coefficient to one.
    w = sp.symbols("w")

    a6, a7, cubic = sp.symbols("a6 a7 cubic")
    A5 = w**5 + a6 * w**6 + a7 * w**7 + w**8
    R5 = sp.Poly(sp.expand(A5**2 + cubic * A5**3), w)
    equations5 = [R5.coeff_monomial(w**degree) for degree in range(13, 18)]
    assert sp.groebner(equations5, a6, a7, cubic).contains(
        sp.Poly(1, a6, a7, cubic)
    )

    a7, cubic = sp.symbols("a7 cubic")
    A6 = w**6 + a7 * w**7 + w**8
    R6 = sp.Poly(sp.expand(A6**2 + cubic * A6**3), w)
    equations6 = [R6.coeff_monomial(w**degree) for degree in range(13, 22)]
    assert sp.groebner(equations6, a7, cubic).contains(sp.Poly(1, a7, cubic))

    # The remaining m=3 and m=4 cells are populated by primitive boundary
    # parametrizations of the required global degrees.  These are not
    # asserted to satisfy the osculating cubic or the five-block equations.
    models = (
        (3, w**3 + w**7 + w**8, w**6 + w**12, 10, 21128962752),
        (
            4,
            w**4 + w**7 + w**8,
            w**8 + 2 * w**11 + 2 * w**12,
            14,
            1310720,
        ),
    )
    for m, A, B, contact, expected_resultant in models:
        remainder = sp.Poly(sp.expand(B - A**2), w)
        # Poly.terms is descending; use the trailing nonzero degree.
        assert min(degree[0] for degree, coefficient in remainder.terms()) == contact
        derivative_A = sp.cancel(sp.diff(A, w) / w ** (m - 1))
        derivative_B = sp.cancel(sp.diff(B, w) / w ** (2 * m - 1))
        assert sp.factor(sp.resultant(derivative_A, derivative_B, w)) == (
            expected_resultant
        )
        assert sp.degree(A, w) == 8
        assert sp.degree(B, w) == 12


def main() -> None:
    leading_fractional_charts()
    vertical_projection_is_impossible()
    quadratic_analytic_exception()
    print("verified the three leading-fractional survivor cells")
    print("verified every vertical/opposite-projection cell is impossible")
    print("verified only m=3,4 survive the analytic-quadratic contact ledger")
    print("verified primitive degree-(8,12) boundary models populate both cells")
    print("RESULT: FIVE EXPLICIT PUISEUX CELLS REMAIN")


if __name__ == "__main__":
    main()
