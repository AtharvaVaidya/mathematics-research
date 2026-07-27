#!/usr/bin/env python3
"""Verify the general binary first-lower double-pole obstruction."""

from __future__ import annotations

import sympy as sp

from verify_weighted_lift_first_nonlinear_cusp_subduction import (
    build_maximal_subductions,
    build_seed,
)


x, t = sp.symbols("x t", nonzero=True)


def logarithmic_determinant(
    first_x: sp.Expr,
    first_t: sp.Expr,
    first_gamma: sp.Expr,
    first_extra_t: sp.Expr,
    second_x: sp.Expr,
    second_t: sp.Expr,
    second_gamma: sp.Expr,
    second_extra_t: sp.Expr,
    logarithmic_gamma_x: sp.Expr,
    logarithmic_gamma_t: sp.Expr,
) -> sp.Expr:
    first_log_x = first_x / x + first_gamma * logarithmic_gamma_x
    first_log_t = (
        first_t / t
        + first_gamma * logarithmic_gamma_t
        + first_extra_t
    )
    second_log_x = second_x / x + second_gamma * logarithmic_gamma_x
    second_log_t = (
        second_t / t
        + second_gamma * logarithmic_gamma_t
        + second_extra_t
    )
    return sp.factor(
        first_log_x * second_log_t - first_log_t * second_log_x
    )


def verify_exact_seed_slices() -> None:
    p, q = build_seed()
    _, second_numerator, _, theta = build_maximal_subductions(p, q)
    w, gamma = sp.symbols("w gamma")
    second_poly = sp.Poly(second_numerator, w, gamma)
    assert second_poly.coeff_monomial(w**20 * gamma**2) == theta
    assert sp.factor(
        second_poly.coeff_monomial(w**19 * gamma**2) / theta
    ) == -sp.Rational(70, 3)

    p_poly = sp.Poly(p, w)
    q_poly = sp.Poly(q, w)
    p5 = p_poly.coeff_monomial(w**5)
    p4 = p_poly.coeff_monomial(w**4)
    q6 = q_poly.coeff_monomial(w**6)
    q5 = q_poly.coeff_monomial(w**5)
    alpha = sp.factor(q5 / q6)
    beta = sp.factor(p4 / p5)
    assert alpha == -sp.Rational(28, 5)
    assert beta == -sp.Rational(35, 6)
    assert sp.factor(alpha - beta) == sp.Rational(7, 30)

    n, j = sp.symbols("n j", integer=True)
    coefficient_multiplier = sp.expand(j * alpha + (n - j) * beta)
    assert sp.factor(
        coefficient_multiplier
        - (-sp.Rational(35, 6) * n + sp.Rational(7, 30) * j)
    ) == 0


def verify_general_forcing_formula() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    source_i = sp.symbols("I", integer=True, positive=True)
    polynomial = sp.Function("P")(t)
    polynomial_prime = sp.diff(polynomial, t)
    first_lower_polynomial = sp.Rational(7, 30) * (
        t * polynomial_prime - 25 * n * polynomial
    )

    exponent_r = sp.Rational(5, 8) * (source_i - 1)
    exponent_s = (17 * source_i + 15) / (8 * n)
    logarithmic_gamma_x = source_i / x
    logarithmic_gamma_t = (
        exponent_r / t + exponent_s * polynomial_prime / polynomial
    )

    first_determinant = logarithmic_determinant(
        14,
        19,
        16,
        0,
        4 * n,
        5 * n,
        4 * n,
        polynomial_prime / polynomial,
        logarithmic_gamma_x,
        logarithmic_gamma_t,
    )
    second_determinant = logarithmic_determinant(
        15,
        20,
        17,
        0,
        4 * n - 1,
        5 * n - 1,
        4 * n - 1,
        sp.diff(first_lower_polynomial, t) / first_lower_polynomial,
        logarithmic_gamma_x,
        logarithmic_gamma_t,
    )
    forcing = sp.factor(
        -sp.Rational(70, 3) / t * first_determinant
        + first_lower_polynomial
        / (t * polynomial)
        * second_determinant
    )

    omega = (
        25 * n**2 * (1 - source_i) * polynomial**2
        + 4
        * n
        * (17 * source_i + 15)
        * t**2
        * polynomial
        * sp.diff(polynomial, t, 2)
        + 20
        * n
        * (3 * source_i + 5)
        * t
        * polynomial
        * polynomial_prime
        + (17 * source_i + 15)
        * (1 - 4 * n)
        * t**2
        * polynomial_prime**2
    )
    expected = 7 * omega / (
        120 * n * x * t**2 * polynomial**2
    )
    assert sp.factor(forcing - expected) == 0

    z = sp.Function("z")(t)
    logarithmic_form = (
        25 * n**2 * (1 - source_i)
        + 4 * n * (17 * source_i + 15) * t * sp.diff(z, t)
        + 8 * n * (5 - source_i) * z
        + (17 * source_i + 15) * z**2
    )
    # SymPy does not combine the quotient substitutions reliably in
    # an expanded expression, so verify the logarithmic identity after
    # clearing P^2 directly.
    z_from_polynomial = t * polynomial_prime / polynomial
    assert sp.factor(
        omega / polynomial**2
        - logarithmic_form.subs(z, z_from_polynomial).doit()
    ) == 0


def verify_root_multiplicity_coefficient() -> None:
    n, source_i, multiplicity = sp.symbols(
        "n I e", integer=True, positive=True
    )
    alpha, tau = sp.symbols("alpha tau", nonzero=True)
    regular_zero, regular_one = sp.symbols("regular_zero regular_one")

    # The regular part is retained to first order.  It cannot affect
    # the coefficient of tau^-2.
    local_t = alpha + tau
    local_z = multiplicity * local_t / tau + regular_zero + regular_one * tau
    local_z_prime = sp.diff(local_z, tau)
    bracket = (
        25 * n**2 * (1 - source_i)
        + 4
        * n
        * (17 * source_i + 15)
        * local_t
        * local_z_prime
        + 8 * n * (5 - source_i) * local_z
        + (17 * source_i + 15) * local_z**2
    )
    double_coefficient = sp.factor(
        sp.limit(
            tau**2 * 7 * bracket / (120 * n * x * local_t**2),
            tau,
            0,
        )
    )
    expected = (
        7
        * (17 * source_i + 15)
        * multiplicity
        * (multiplicity - 4 * n)
        / (120 * n * x)
    )
    assert sp.factor(double_coefficient - expected) == 0

    for target_degree in range(1, 40):
        for degree in range(target_degree + 1):
            for root_multiplicity in range(1, degree + 1):
                assert root_multiplicity - 4 * target_degree != 0


def verify_degree_six_specialization() -> None:
    eta, k = sp.symbols("eta k", nonzero=True)
    n = sp.Integer(6)
    source_i = 48 * k + 33
    polynomial = t + eta
    polynomial_prime = sp.diff(polynomial, t)
    omega = (
        25 * n**2 * (1 - source_i) * polynomial**2
        + 4
        * n
        * (17 * source_i + 15)
        * t**2
        * polynomial
        * sp.diff(polynomial, t, 2)
        + 20
        * n
        * (3 * source_i + 5)
        * t
        * polynomial
        * polynomial_prime
        + (17 * source_i + 15)
        * (1 - 4 * n)
        * t**2
        * polynomial_prime**2
    )
    forcing = sp.factor(
        7 * omega / (120 * n * x * t**2 * polynomial**2)
    )
    expected = (
        -sp.Rational(7, 15)
        * (
            (900 * k + 600) * eta**2
            + (1440 * k + 940) * eta * t
            + (931 * k + 616) * t**2
        )
        / (x * t**2 * (t + eta) ** 2)
    )
    assert sp.factor(forcing - expected) == 0

    double_coefficient = sp.factor(
        sp.limit((t + eta) ** 2 * forcing, t, -eta)
    )
    assert sp.factor(
        double_coefficient + 161 * (17 * k + 12) / (15 * x)
    ) == 0


def verify_sharp_scope_examples() -> None:
    n, source_i, degree = sp.symbols(
        "n I d", integer=True, positive=True
    )
    monomial_coefficient = sp.factor(
        25 * n**2 * (1 - source_i)
        + 8 * n * (5 - source_i) * degree
        + (17 * source_i + 15) * degree**2
    )
    assert monomial_coefficient == (
        degree + n
    ) * (
        17 * source_i * degree
        - 25 * source_i * n
        + 15 * degree
        + 25 * n
    )
    # P=t^n, I=5 gives J=15 and kills the t^-2 coefficient.  This
    # demonstrates why the nonzero-root hypothesis is not cosmetic.
    assert monomial_coefficient.subs(
        {degree: n, source_i: 5}
    ) == 0
    resonance_j = (
        (5 * n + 17 * n) * 5 + 15 * n - 5 * n
    ) / (8 * n)
    assert sp.factor(resonance_j - 15) == 0


def main() -> None:
    verify_exact_seed_slices()
    verify_general_forcing_formula()
    verify_root_multiplicity_coefficient()
    verify_degree_six_specialization()
    verify_sharp_scope_examples()
    print("verified: exact all-n first-lower target slice")
    print("verified: general normalized forcing formula")
    print("verified: every nonzero binary-face root gives a double pole")
    print("verified: degree-six specialization and sharp scope examples")
    print("RESULT: every mixed polynomial binary characteristic is closed")


if __name__ == "__main__":
    main()
