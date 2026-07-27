#!/usr/bin/env python3
"""Verify the general mixed-linear-pivot closure after second subduction."""

from __future__ import annotations

import sympy as sp


x, y, u = sp.symbols("x y u")


def jacobian_xy(first: sp.Expr, second: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(first, x) * sp.diff(second, y)
        - sp.diff(first, y) * sp.diff(second, x)
    )


def jacobian_xu(first: sp.Expr, second: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(first, x) * sp.diff(second, u)
        - sp.diff(first, u) * sp.diff(second, x)
    )


def verify_coupled_operator() -> None:
    gamma = sp.Function("gamma")(x, u)
    highest_u = x**-5 * u**20 * gamma**17
    highest_a = x**-2 * u**6 * gamma**4
    highest_b = x**-1 * u**5 * gamma**4
    operator_a = (
        11 * x * sp.diff(gamma, x)
        + 7 * u * sp.diff(gamma, u)
        + 5 * gamma
    )
    operator_b = (
        5 * x * sp.diff(gamma, x)
        - 3 * u * sp.diff(gamma, u)
        - 5 * gamma
    )

    assert sp.expand(
        x * jacobian_xu(highest_u, highest_a)
        - 2
        * highest_u
        * highest_a
        * operator_a
        / (u * gamma)
    ) == 0
    assert sp.expand(
        x * jacobian_xu(highest_u, highest_b)
        - highest_u
        * highest_b
        * operator_b
        / (u * gamma)
    ) == 0

    alpha, beta = sp.symbols("alpha beta", nonzero=True)
    p5 = -sp.Rational(3, 46)
    q6 = -sp.Rational(5, 92)
    rho = sp.factor(beta * p5 / (2 * alpha * q6))
    mixed = sp.expand(
        alpha * q6 * x * jacobian_xu(highest_u, highest_a)
        + beta * p5 * x * jacobian_xu(highest_u, highest_b)
    )
    common = (
        2
        * alpha
        * q6
        * highest_u
        * x**-2
        * u**5
        * gamma**4
        / (u * gamma)
    )
    assert sp.simplify(
        mixed - common * (u * operator_a + rho * x * operator_b)
    ) == 0


def verify_mixed_a_characteristic() -> None:
    k, rho = sp.symbols(
        "k rho", integer=True, positive=True, nonzero=True
    )
    source_i = 4 * k + 1
    source_j = 11 * k + 4
    exponent_r = sp.Rational(5, 2) * k
    exponent_s = sp.Rational(17, 2) * k + 4
    assert sp.expand(11 * source_i + 5 - 4 * source_j) == 0
    assert sp.expand(exponent_r + exponent_s - source_j) == 0

    formal_gamma = (
        x ** (source_i - source_j)
        * u**exponent_r
        * (u + 2 * rho * x) ** exponent_s
    )

    def operator_a(expression: sp.Expr) -> sp.Expr:
        return sp.expand(
            11 * x * sp.diff(expression, x)
            + 7 * u * sp.diff(expression, u)
            + 5 * expression
        )

    def operator_b(expression: sp.Expr) -> sp.Expr:
        return sp.expand(
            5 * x * sp.diff(expression, x)
            - 3 * u * sp.diff(expression, u)
            - 5 * expression
        )

    assert sp.factor(
        u * operator_a(formal_gamma)
        + rho * x * operator_b(formal_gamma)
    ) == 0

    # Generalized Vandermonde: the x^1 term can use no 2*rho*x
    # choice, so its coefficient is independent of rho.
    for sample_k in range(1, 9):
        I = 4 * sample_k + 1
        J = 11 * sample_k + 4
        r = sp.Rational(5, 2) * sample_k
        s = sp.Rational(17, 2) * sample_k + 4
        number_of_replacements = I - 1
        coefficient = sp.simplify(
            sum(
                sp.binomial(r, j)
                * sp.binomial(s, number_of_replacements - j)
                for j in range(number_of_replacements + 1)
            )
        )
        assert coefficient == sp.binomial(J, number_of_replacements)
        assert coefficient != 0
        assert J - number_of_replacements == 7 * sample_k + 4
        # If q copies of the mixed 2*rho*x piece are also used, the
        # x-exponent remains one but the y-exponent drops by q.  Hence
        # none can cancel the highest-y q=0 monomial checked above.
        for mixed_choices in range(1, min(6, J - number_of_replacements + 1)):
            y_degree = (
                J - number_of_replacements - mixed_choices
            )
            assert y_degree == 7 * sample_k + 4 - mixed_choices
            assert y_degree < 7 * sample_k + 4

    m = 15 * k + 3
    forbidden_drop = 8 * k
    assert sp.expand((m + 4) - forbidden_drop) == 7 * k + 7
    assert sp.expand((3 * m + 15) - forbidden_drop) == 37 * k + 24
    defect_degree = 21 * m + 85 - forbidden_drop
    linear_linear_degree = 8 * m + 33
    assert sp.expand(
        defect_degree - linear_linear_degree
    ) == 187 * k + 91


def verify_b_c_separation() -> None:
    m = sp.symbols("m", integer=True, positive=True)
    degree_ua = 21 * m + 85
    degree_ub = 21 * m + 84
    degree_uc = 18 * m + 70
    degree_linear_linear = 8 * m + 33
    assert sp.expand(degree_ua - degree_ub) == 1
    assert sp.expand(degree_ub - degree_uc) == 3 * m + 14

    b_defect_degree = degree_ub - m
    assert sp.expand(b_defect_degree - degree_uc) == 2 * m + 14
    assert sp.expand(
        b_defect_degree - degree_linear_linear
    ) == 12 * m + 51


def verify_constant_graphs() -> None:
    z0 = sp.symbols("z0")
    p5 = -sp.Rational(3, 46)
    q6 = -sp.Rational(5, 92)
    theta = -sp.Rational(
        36905625, 6077984970919772059860992
    )
    a = -sp.Rational(57, 34)
    h = a * y + z0 * x
    c0 = x**2 * h
    a0 = q6 * y**6 * c0**4
    b0 = p5 * y**5 * c0**4
    u0 = theta * x**32 * y**20 * h**17

    expected_a = (
        6
        * q6
        * theta
        * x**39
        * y**25
        * h**20
        * (4 * a * y + 9 * z0 * x)
    )
    expected_b = (
        p5
        * theta
        * x**39
        * y**24
        * h**20
        * (-8 * a * y + 5 * z0 * x)
    )
    expected_c = (
        -6
        * theta
        * x**33
        * y**19
        * h**17
        * (7 * a * y + 10 * z0 * x)
    )
    assert sp.factor(jacobian_xy(u0, a0) - expected_a) == 0
    assert sp.factor(jacobian_xy(u0, b0) - expected_b) == 0
    assert sp.factor(jacobian_xy(u0, c0) - expected_c) == 0

    for expression, degree in (
        (expected_a, 85),
        (expected_b, 84),
        (expected_c, 70),
    ):
        assert expression != 0
        assert sp.Poly(expression, x, y).total_degree() == degree


def main() -> None:
    verify_coupled_operator()
    verify_mixed_a_characteristic()
    verify_b_c_separation()
    verify_constant_graphs()
    print("verified: exact coupled A/B weighted-Euler operator")
    print("verified: characteristic solution on every mixed A-ray")
    print("verified: the forced x^1 coefficient is rho-independent")
    print("verified: C and linear corrections enter after the A-ray defect")
    print("verified: constant graphs have separated nonzero top forms")
    print("RESULT: use the final binary verifier for the corrected B/C proof")


if __name__ == "__main__":
    main()
