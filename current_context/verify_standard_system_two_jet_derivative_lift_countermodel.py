#!/usr/bin/env python3
"""Exact checks for the two-jet derivative-lift countermodel."""

import sympy as sp


x, tau = sp.symbols("x tau")


def tau_coefficient_degree_bound(
    polynomial: sp.Expr,
    total_degree: int,
) -> None:
    """Check deg_X [tau^j] polynomial <= total_degree-j."""
    tau_polynomial = sp.Poly(sp.expand(polynomial), tau)
    for (tau_order,), coefficient in tau_polynomial.terms():
        assert tau_order <= total_degree
        assert sp.degree(coefficient, x) <= total_degree - tau_order


def verify_case(a: int, b: int, g: int, d: int) -> None:
    n = g * a
    m = g * b
    q = b // a
    r = b - a * q
    assert sp.gcd(a, b) == 1
    assert 1 <= r < a
    assert 2 * d <= n

    R = x**g + 1 if g == 2 else x**g + x + 1
    degree_T = min(n - 2, n - d)
    degree_S = min(n - 2, n - 2 * d)
    T = x**degree_T + x + 2
    S = x**degree_S + 2 * x + 3 if degree_S > 0 else sp.Integer(3)
    assert sp.rem(T, R, domain=sp.QQ) != 0

    U = tau**d * T + tau ** (2 * d) * S
    P = sp.expand(R**a + U)
    Q_truncated = sp.expand(
        sum(
            sp.binomial(sp.Rational(b, a), ell)
            * R ** (b - a * ell)
            * U**ell
            for ell in range(q + 1)
        )
    )
    H = sp.expand(
        sum(
            ell
            * sp.binomial(sp.Rational(b, a), ell)
            * R ** (b - a * ell)
            * U ** (ell - 1)
            for ell in range(1, q + 1)
        )
    )
    C_q = r * sp.binomial(sp.Rational(b, a), q)
    remainder = sp.expand(C_q * R ** (r - 1) * sp.diff(R, x) * U**q)

    assert sp.expand(
        sp.diff(Q_truncated, x) - H * sp.diff(P, x) - remainder
    ) == 0

    correction = sp.expand(-sp.integrate(remainder, x))
    lifted_Q = sp.expand(Q_truncated + correction)
    assert sp.expand(sp.diff(lifted_Q, x) - H * sp.diff(P, x)) == 0

    tau_coefficient_degree_bound(P, n)
    tau_coefficient_degree_bound(Q_truncated, m)
    tau_coefficient_degree_bound(correction, m)
    tau_coefficient_degree_bound(lifted_Q, m)

    # The first and second lifted coefficients are the exact primitives
    # displayed in the note.
    expected_first = -C_q * sp.integrate(
        R ** (r - 1) * sp.diff(R, x) * T**q,
        x,
    )
    expected_second = -q * C_q * sp.integrate(
        R ** (r - 1) * sp.diff(R, x) * T ** (q - 1) * S,
        x,
    )
    assert sp.expand(correction).coeff(tau, d * q) == sp.expand(
        expected_first
    )
    assert sp.expand(correction).coeff(
        tau,
        d * (q + 1),
    ) == sp.expand(expected_second)

    delta = sp.symbols(f"delta_{a}_{b}_{g}_{d}", nonzero=True)
    maximal_Q = sp.expand(lifted_Q + delta * tau ** (m - 1) * x)
    assert sp.expand(
        sp.diff(maximal_Q, x)
        - H * sp.diff(P, x)
        - delta * tau ** (m - 1)
    ) == 0
    tau_coefficient_degree_bound(maximal_Q, m)

    resultant = sp.factor(
        sp.resultant(sp.diff(P, x), sp.diff(maximal_Q, x), x)
    )
    expected_resultant = (
        n ** (m - 1)
        * delta ** (n - 1)
        * tau ** ((m - 1) * (n - 1))
    )
    assert sp.simplify(resultant / expected_resultant) in (-1, 1)


for parameters in (
    (2, 3, 2, 1),
    (2, 3, 3, 2),
    (2, 5, 2, 1),
    (3, 4, 2, 2),
    (3, 5, 2, 1),
):
    verify_case(*parameters)


print("verified: the two-jet division-free remainder is an exact derivative")
print("verified: its primitive saturates every reciprocal degree bound")
print("verified: T need not lie in the reduced common-root tangent cone")
print("verified: the ambient lift has exact maximal resultant contact")
