#!/usr/bin/env python3
"""Exact checks for the power-index/principal-face bridge audit."""

from __future__ import annotations

import sympy as sp


def homogenized_bracket(
    first: sp.Expr,
    second: sp.Expr,
    X: sp.Symbol,
    tau: sp.Symbol,
    n: int,
    m: int,
) -> sp.Expr:
    return sp.expand(
        tau
        * (
            sp.diff(first, X) * sp.diff(second, tau)
            - sp.diff(first, tau) * sp.diff(second, X)
        )
        + n * first * sp.diff(second, X)
        - m * second * sp.diff(first, X)
    )


def verify_reciprocal_chain_rule() -> None:
    x, y, X, tau = sp.symbols("x y X tau")
    # Generic enough exact representatives to exercise every chain-rule
    # term, including mixed and inhomogeneous pieces.
    F = (
        2 * x**4
        + 3 * x**2 * y
        - 5 * x * y**2
        + 7 * y**3
        + 11 * x
        - 13 * y
        + 17
    )
    G = (
        19 * x**5
        - 23 * x**3 * y
        + 29 * x * y**3
        + 31 * y**4
        + 37 * x**2
        - 41 * x * y
        + 43
    )
    n, m = 6, 7
    substitution = {x: X / tau, y: 1 / tau}
    P = sp.cancel(tau**n * F.subs(substitution))
    Q = sp.cancel(tau**m * G.subs(substitution))
    affine_jacobian = sp.diff(F, x) * sp.diff(G, y) - sp.diff(
        F, y
    ) * sp.diff(G, x)
    expected = -tau ** (n + m - 2) * affine_jacobian.subs(
        substitution
    )
    assert sp.cancel(
        homogenized_bracket(P, Q, X, tau, n, m) - expected
    ) == 0


def verify_defect_one_bezout_equation() -> None:
    x, y = sp.symbols("x y")
    p0 = x**6 + 2 * x**3 - 1
    p1 = 3 * x**5 - 5 * x + 7
    q0 = x**7 - 11 * x**2 + 13
    q1 = 17 * x**6 + 19 * x - 23
    higher_f = y**2 * (29 * x**2 + 31 * y)
    higher_g = y**2 * (37 * x**3 - 41 * y)
    F = p0 + y * p1 + higher_f
    G = q0 + y * q1 + higher_g
    restricted_jacobian = sp.expand(
        (
            sp.diff(F, x) * sp.diff(G, y)
            - sp.diff(F, y) * sp.diff(G, x)
        ).subs(y, 0)
    )
    assert restricted_jacobian == sp.expand(
        sp.diff(p0, x) * q1 - p1 * sp.diff(q0, x)
    )


def verify_bounded_bezout_sufficiency() -> None:
    x = sp.symbols("x")
    # Maximal-degree, lower-degree, constant-derivative, and
    # zero-derivative representatives.
    cases = (
        (x**6 + x + 1, x**9 + x**2 + 3, 6, 9),
        (x**3 + 2 * x + 1, x**4 - x + 5, 8, 11),
        (3 * x + 7, x**5 + x + 1, 9, 7),
        (sp.Integer(11), 5 * x + 13, 6, 8),
        (7 * x - 2, sp.Integer(17), 8, 6),
    )
    scalar = sp.Integer(23)
    for p0, q0, n, m in cases:
        derivative_p = sp.diff(p0, x)
        derivative_q = sp.diff(q0, x)
        polynomial_gcd = sp.gcd(derivative_p, derivative_q)
        assert polynomial_gcd != 0
        assert sp.degree(polynomial_gcd, x) == 0
        if derivative_p == 0:
            assert sp.degree(derivative_q, x) == 0
            q1 = sp.Integer(0)
            p1 = sp.cancel(-scalar / derivative_q)
        elif derivative_q == 0:
            assert sp.degree(derivative_p, x) == 0
            q1 = sp.cancel(scalar / derivative_p)
            p1 = sp.Integer(0)
        else:
            coefficient_p, coefficient_q, gcd_value = sp.gcdex(
                derivative_p, derivative_q, x
            )
            assert sp.expand(
                coefficient_p * derivative_p
                + coefficient_q * derivative_q
                - gcd_value
            ) == 0
            q1 = sp.cancel(scalar * coefficient_p / gcd_value)
            p1 = sp.cancel(-scalar * coefficient_q / gcd_value)
        assert sp.expand(
            derivative_p * q1 - p1 * derivative_q - scalar
        ) == 0
        assert sp.degree(p1, x) <= n - 1
        assert sp.degree(q1, x) <= m - 1

    # Both derivatives zero cannot produce a nonzero scalar.
    assert sp.diff(sp.Integer(3), x) == 0
    assert sp.diff(sp.Integer(5), x) == 0


def verify_principal_laurent_edge() -> None:
    u = sp.symbols("u")
    alpha = sp.Rational(2, 3)
    rho = sp.Rational(2, 9)
    sigma = sp.Rational(1, 9)
    A = u + u**2
    B = -9 - 18 * u
    weighted_wronskian = sp.expand(
        rho * A * sp.diff(B, u) - sigma * sp.diff(A, u) * B
    )
    assert rho + sigma + alpha == 1
    assert weighted_wronskian == 1

    # Work on the ninth-root cover x=r^9 so every exponent is integral.
    r, y = sp.symbols("r y", nonzero=True)
    edge_f = r**8 * y + r**14 * y**2
    edge_g = -9 * r - 18 * r**7 * y
    jacobian_r_y = sp.expand(
        sp.diff(edge_f, r) * sp.diff(edge_g, y)
        - sp.diff(edge_f, y) * sp.diff(edge_g, r)
    )
    assert jacobian_r_y == 9 * r**8
    # dx/dr=9r^8 for x=r^9.
    assert sp.cancel(jacobian_r_y / (9 * r**8)) == 1

    # The f-edge points are (8/9,1) and (14/9,2).
    geometric_slope = sp.Rational(1, 2) / sp.Rational(1, 3)
    x_intercept = sp.Rational(8, 9) - sp.Rational(2, 3)
    assert geometric_slope == sp.Rational(3, 2)
    assert x_intercept == rho


def verify_reciprocal_terminal_pairings() -> None:
    X, tau = sp.symbols("X tau")
    A, B = sp.symbols("A B", nonzero=True)
    for n in range(2, 10):
        for m in range(2, 10):
            forcing = tau ** (n + m - 2)
            constant_linear = homogenized_bracket(
                A * tau ** (n - 1),
                B * tau ** (m - 1) * X,
                X,
                tau,
                n,
                m,
            )
            linear_constant = homogenized_bracket(
                A * tau ** (n - 1) * X,
                B * tau ** (m - 1),
                X,
                tau,
                n,
                m,
            )
            assert sp.expand(constant_linear - A * B * forcing) == 0
            assert sp.expand(linear_constant + A * B * forcing) == 0


def verify_arbitrary_anchor_terminal() -> None:
    t, z = sp.symbols("t z")
    a, b, G, r, s = 2, 3, 5, 7, 11

    def transformed_bracket(first: sp.Expr, second: sp.Expr) -> sp.Expr:
        return sp.expand(
            t
            * (
                sp.diff(first, z) * sp.diff(second, t)
                - sp.diff(first, t) * sp.diff(second, z)
            )
            + a * G * first * sp.diff(second, z)
            - b * G * second * sp.diff(first, z)
        )

    first = t**r
    second = t**s * z
    assert transformed_bracket(first, second) == (a * G - r) * t ** (
        r + s
    )


def main() -> None:
    verify_reciprocal_chain_rule()
    verify_defect_one_bezout_equation()
    verify_bounded_bezout_sufficiency()
    verify_principal_laurent_edge()
    verify_reciprocal_terminal_pairings()
    verify_arbitrary_anchor_terminal()
    print("verified: reciprocal homogenization converts the Keller bracket exactly")
    print("verified: the terminal equation is the ordinary defect-one Bezout identity")
    print("verified: a nontrivial admissible principal Laurent edge has Jacobian one")
    print("verified: both reciprocal endpoint pairings supply the scalar exactly")
    print("RESULT: power-index descent terminates in an unresolved principal category")


if __name__ == "__main__":
    main()
