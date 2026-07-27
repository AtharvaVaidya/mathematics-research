#!/usr/bin/env python3
"""Exact checks for the repeated-root Kummer nonlinear audit."""

from __future__ import annotations

from math import gcd, lcm

import sympy as sp


x, tau, h = sp.symbols("x tau h")


def bracket(P: sp.Expr, Q: sp.Expr, n: int, m: int) -> sp.Expr:
    return sp.expand(
        tau * (sp.diff(P, x) * sp.diff(Q, tau) - sp.diff(P, tau) * sp.diff(Q, x))
        + n * P * sp.diff(Q, x)
        - m * Q * sp.diff(P, x)
    )


def positive_compositions(total: int):
    if total == 0:
        yield ()
        return
    for first in range(1, total + 1):
        for tail in positive_compositions(total - first):
            yield (first,) + tail


def verify_kummer_period_factorization() -> None:
    for g in range(2, 11):
        for multiplicities in positive_compositions(g):
            d = g
            period = 1
            for e in multiplicities:
                d = gcd(d, e)
                period = lcm(period, g // gcd(g, e))
            kappa = g // d
            assert period == kappa
            assert all(e % d == 0 for e in multiplicities)
            assert sum(e // d for e in multiplicities) == kappa


def verify_exact_kummer_cone() -> None:
    # The smallest two-factor example: g=4, d=2, kappa=2,
    # H=X(X-1), p=4, q=6.
    H = x * (x - 1)
    kappa = 2
    p, q = 4, 6
    T = tau**kappa
    A = sp.symbols(f"A0:{p + 1}")
    B = sp.symbols(f"B0:{q + 1}")
    P = sum(A[r] * T**r * H ** (p - r) for r in range(p + 1))
    Q = sum(B[s] * T**s * H ** (q - s) for s in range(q + 1))
    assert bracket(P, Q, kappa * p, kappa * q) == 0

    for r in range(p + 1):
        assert sp.degree(H ** (p - r), x) == kappa * (p - r)
    for s in range(q + 1):
        assert sp.degree(H ** (q - s), x) == kappa * (q - s)


def verify_defect_bilinear_identity() -> None:
    n, m = 8, 12
    r, s = 3, 4
    pr = x ** (n - r) + 2 * x + 3
    qs = x ** (m - s) - x**2 + 5
    Pr = tau ** (n - r) * pr.subs(x, x / tau)
    Qs = tau ** (m - s) * qs.subs(x, x / tau)
    Pr = sp.cancel(Pr)
    Qs = sp.cancel(Qs)
    dehomogenized = r * pr * sp.diff(qs, x) - s * qs * sp.diff(pr, x)
    expected = sp.cancel(
        tau ** (n + m - r - s - 1) * dehomogenized.subs(x, x / tau)
    )
    assert sp.expand(bracket(Pr, Qs, n, m) - expected) == 0


def verify_top_form_escape() -> None:
    for kappa in range(2, 7):
        z = x**kappa
        p0 = 1 + 2 * z + 3 * z**2 + z**4
        q0 = 2 - z + 5 * z**3 + z**5
        assert sp.rem(sp.diff(p0, x), x ** (kappa - 1), domain=sp.QQ) == 0
        assert sp.rem(sp.diff(q0, x), x ** (kappa - 1), domain=sp.QQ) == 0
        p1 = sum(sp.symbols(f"u{kappa}_0:{8}")[i] * x**i for i in range(8))
        q1 = sum(sp.symbols(f"v{kappa}_0:{8}")[i] * x**i for i in range(8))
        bezout_left = sp.expand(p1 * sp.diff(q0, x) - q1 * sp.diff(p0, x))
        assert sp.rem(bezout_left, x ** (kappa - 1), x) == 0


def polynomial_coefficients(poly: sp.Expr) -> list[sp.Expr]:
    P = sp.Poly(sp.expand(poly), x)
    return [P.coeff_monomial(x**i) for i in range(P.degree() + 1)]


def verify_degree_46_branch() -> None:
    n, m = 4, 6
    p: list[sp.Expr] = [sp.Integer(0)] * (n + m + 1)
    q: list[sp.Expr] = [sp.Integer(0)] * (n + m + 1)
    p[0] = x**4 + x
    q[0] = x**6 + x**5
    assert sp.gcd(sp.diff(p[0], x), sp.diff(q[0], x)) == 1

    # The bounded defect-one endpoint map has rank nine in a
    # ten-dimensional domain, so its solution set is an affine line.
    a1_all = sp.symbols("a1_all_0:4")
    b1_all = sp.symbols("b1_all_0:6")
    p1_all = sum(value * x**i for i, value in enumerate(a1_all))
    q1_all = sum(value * x**i for i, value in enumerate(b1_all))
    equations1 = polynomial_coefficients(
        p1_all * sp.diff(q[0], x) - q1_all * sp.diff(p[0], x) + 1
    )
    matrix1, rhs1 = sp.linear_eq_to_matrix(
        equations1, a1_all + b1_all
    )
    assert matrix1.shape == (9, 10)
    assert matrix1.rank() == 9
    assert matrix1.row_join(rhs1).rank() == 9
    assert len(a1_all + b1_all) - matrix1.rank() == 1

    p[1] = (
        sp.Rational(2, 3) * h * x**3
        + sp.Rational(1, 6) * h
        - sp.Rational(400, 71) * x**2
        + sp.Rational(144, 71) * x
        - sp.Rational(120, 71)
    )
    q[1] = (
        h * x**5
        + sp.Rational(5, 6) * h * x**4
        - sp.Rational(600, 71) * x**4
        - 4 * x**3
        + 1
    )
    assert sp.expand(p[1] * sp.diff(q[0], x) - q[1] * sp.diff(p[0], x)) == -1

    # Solve the defect-two endpoint equation exactly.
    a2 = sp.symbols("a2_0:3")
    b2 = sp.symbols("b2_0:5")
    p2 = sum(value * x**i for i, value in enumerate(a2))
    q2 = sum(value * x**i for i, value in enumerate(b2))
    source2 = sp.expand(p[1] * sp.diff(q[1], x) - q[1] * sp.diff(p[1], x))
    equations2 = polynomial_coefficients(
        2 * (p2 * sp.diff(q[0], x) - q2 * sp.diff(p[0], x)) + source2
    )
    solutions2 = sp.solve(equations2, a2 + b2, dict=True, simplify=False)
    assert len(solutions2) == 1
    p[2] = sp.expand(p2.subs(solutions2[0]))
    q[2] = sp.expand(q2.subs(solutions2[0]))

    # At defect three the endpoint map has a one-dimensional cokernel.
    a3 = sp.symbols("a3_0:2")
    b3 = sp.symbols("b3_0:4")
    p3 = sum(value * x**i for i, value in enumerate(a3))
    q3 = sum(value * x**i for i, value in enumerate(b3))
    source3 = sp.expand(
        p[1] * sp.diff(q[2], x)
        - 2 * q[2] * sp.diff(p[1], x)
        + 2 * p[2] * sp.diff(q[1], x)
        - q[1] * sp.diff(p[2], x)
    )
    defect3 = 3 * (p3 * sp.diff(q[0], x) - q3 * sp.diff(p[0], x)) + source3
    coefficients3 = polynomial_coefficients(defect3)
    matrix, rhs = sp.linear_eq_to_matrix(coefficients3, a3 + b3)
    assert matrix.shape == (7, 6)
    assert matrix.rank() == 6
    assert matrix.row_join(rhs).rank() == 7
    left_kernel = matrix.T.nullspace()
    assert len(left_kernel) == 1
    obstruction = sp.factor((left_kernel[0].T * rhs)[0])
    assert obstruction == -sp.Rational(245844523008, 25411681)
    assert h not in obstruction.free_symbols


def main() -> None:
    verify_kummer_period_factorization()
    verify_exact_kummer_cone()
    verify_defect_bilinear_identity()
    verify_top_form_escape()
    verify_degree_46_branch()
    print("verified: Kummer period equals g/gcd(g,e_i)")
    print("verified: exact pure-Kummer cone has zero bracket")
    print("verified: total-defect recurrence and top-form escape")
    print("verified: the split degree-(4,6) branch fails at defect three")


if __name__ == "__main__":
    main()
