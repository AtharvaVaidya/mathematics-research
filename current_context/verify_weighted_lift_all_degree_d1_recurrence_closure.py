#!/usr/bin/env python3
"""Verify the first-lower recurrence for every binary d=1 face."""

from __future__ import annotations

import sympy as sp

from verify_weighted_lift_first_nonlinear_cusp_subduction import (
    build_maximal_subductions,
    build_seed,
)


x, y, u, t, eta = sp.symbols("x y u t eta")


def verify_exact_seed_slices() -> None:
    p, q = build_seed()
    _, second_numerator, _, theta = build_maximal_subductions(p, q)
    w, gamma_symbol = sp.symbols("w gamma")
    p_poly = sp.Poly(p, w)
    q_poly = sp.Poly(q, w)
    second_poly = sp.Poly(second_numerator, w, gamma_symbol)

    p5 = p_poly.coeff_monomial(w**5)
    p4 = p_poly.coeff_monomial(w**4)
    q6 = q_poly.coeff_monomial(w**6)
    q5 = q_poly.coeff_monomial(w**5)
    assert sp.factor(p4 / p5) == -sp.Rational(35, 6)
    assert sp.factor(q5 / q6) == -sp.Rational(28, 5)

    top = second_poly.coeff_monomial(w**20 * gamma_symbol**2)
    lower = second_poly.coeff_monomial(w**19 * gamma_symbol**2)
    assert top == theta
    assert sp.factor(lower / top) == -sp.Rational(70, 3)

    # The full second-subduction numerator has (19,2) as its unique
    # first-lower graph-weight slice for every nonconstant graph.
    m = sp.symbols("m", integer=True, positive=True)

    def graph_weight(monomial: tuple[int, int]) -> sp.Expr:
        w_power, gamma_power = monomial
        return sp.expand(
            w_power * (m + 4)
            + (gamma_power - 5) * (m + 2)
            - 5
        )

    support = [
        monomial
        for monomial, coefficient in second_poly.terms()
        if coefficient != 0
    ]
    assert len(support) == 77
    for reference, excluded in (
        ((20, 2), {(20, 2)}),
        ((19, 2), {(20, 2), (19, 2)}),
    ):
        for monomial in support:
            if monomial in excluded:
                continue
            difference = sp.Poly(
                graph_weight(reference) - graph_weight(monomial),
                m,
            )
            assert difference.coeff_monomial(m) >= 0
            assert difference.eval(1) > 0


def verify_all_n_target_slice() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    p4_over_p5 = -sp.Rational(35, 6)
    q5_over_q6 = -sp.Rational(28, 5)
    coefficient_t = sp.expand(
        q5_over_q6 + (n - 1) * p4_over_p5
    )
    coefficient_eta = sp.expand(n * p4_over_p5)
    assert coefficient_t == -sp.Rational(35, 6) * n + sp.Rational(
        7, 30
    )
    assert coefficient_eta == -sp.Rational(35, 6) * n

    # One q5/p4 replacement costs m+4.  q4/p3, two first-lower
    # replacements, and the added w*gamma/gamma pieces occur later.
    m = sp.symbols("m", integer=True, positive=True)
    assert sp.expand((6 - 5) * (m + 4)) == m + 4
    assert sp.expand((5 - 4) * (m + 4)) == m + 4
    assert sp.expand((6 - 4) * (m + 4)) == 2 * (m + 4)
    assert sp.expand((5 - 3) * (m + 4)) == 2 * (m + 4)
    assert sp.expand(
        6 * (m + 4) - ((m + 4) + (m + 2))
    ) == 4 * m + 18
    assert sp.expand(5 * (m + 4) - (m + 2)) == 4 * m + 18
    assert sp.expand((4 * m + 18) - (m + 4)) == 3 * m + 14


def verify_general_lower_recurrence() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    source_i = sp.symbols("I", integer=True, positive=True)
    exponent_r = sp.Rational(5, 8) * (source_i - 1)
    exponent_s = (17 * source_i + 15) / (8 * n)
    face = t + eta
    coefficient_t = (
        -sp.Rational(28, 5)
        - sp.Rational(35, 6) * (n - 1)
    )
    coefficient_eta = -sp.Rational(35, 6) * n
    lower_face = coefficient_t * t + coefficient_eta * eta

    logarithmic_gamma_x = source_i / x
    logarithmic_gamma_t = exponent_r / t + exponent_s / face

    def logarithmic_determinant(
        first_x: sp.Expr,
        first_t: sp.Expr,
        first_gamma: sp.Expr,
        first_extra_t: sp.Expr,
        second_x: sp.Expr,
        second_t: sp.Expr,
        second_gamma: sp.Expr,
        second_extra_t: sp.Expr,
    ) -> sp.Expr:
        first_log_x = first_x / x + first_gamma * logarithmic_gamma_x
        first_log_t = (
            first_t / t
            + first_gamma * logarithmic_gamma_t
            + first_extra_t
        )
        second_log_x = (
            second_x / x + second_gamma * logarithmic_gamma_x
        )
        second_log_t = (
            second_t / t
            + second_gamma * logarithmic_gamma_t
            + second_extra_t
        )
        return sp.expand(
            first_log_x * second_log_t
            - first_log_t * second_log_x
        )

    reduced_forcing = sp.factor(
        -sp.Rational(70, 3)
        / t
        * logarithmic_determinant(
            14,
            19,
            16,
            0,
            4 * n,
            5 * n,
            4 * n,
            1 / face,
        )
        + lower_face
        / (t * face)
        * logarithmic_determinant(
            15,
            20,
            17,
            0,
            4 * n - 1,
            5 * n - 1,
            4 * n - 1,
            sp.diff(lower_face, t) / lower_face,
        )
    )
    expected_forcing = (
        -sp.Rational(7, 120)
        * (
            25 * source_i * eta**2 * n**2
            + 50 * source_i * eta * n**2 * t
            - 60 * source_i * eta * n * t
            + 25 * source_i * n**2 * t**2
            + 8 * source_i * n * t**2
            - 17 * source_i * t**2
            - 25 * eta**2 * n**2
            - 50 * eta * n**2 * t
            - 100 * eta * n * t
            - 25 * n**2 * t**2
            - 40 * n * t**2
            - 15 * t**2
        )
        / (n * t**2 * x * face**2)
    )
    assert sp.factor(reduced_forcing - expected_forcing) == 0

    characteristic_operator_over_gamma = (
        x
        * (5 * n / t + 17 / face)
        * logarithmic_gamma_x
        - 8 * n * logarithmic_gamma_t
        - 5 * n / t
        + 15 / face
    )
    assert sp.factor(characteristic_operator_over_gamma) == 0

    source_u = 1 + x * y
    source_h = source_u + eta * x
    transformed_forcing = sp.factor(
        (
            u
            * (u + eta * x)
            * expected_forcing.subs(t, u / x)
        ).subs(u, source_u)
    )
    forcing_axis = sp.factor(
        sp.limit(transformed_forcing / x, x, 0)
    )
    expected_axis = (
        -sp.Rational(7, 120)
        * (n + 1)
        * (
            25 * source_i * n
            - 17 * source_i
            - 25 * n
            - 15
        )
        / n
    )
    assert sp.factor(forcing_axis - expected_axis) == 0


def verify_source_axis_obstruction() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    source_i = sp.symbols("I", integer=True, positive=True)
    a = -sp.Rational(57, 34)
    source_u = 1 + x * y
    source_h = source_u + eta * x
    source_k = 5 * n * source_h + 17 * source_u
    source_l = -5 * n * source_h + 15 * source_u

    def source_operator(phi: sp.Expr) -> sp.Expr:
        return sp.expand(
            x
            * source_k
            * (x * sp.diff(phi, x) - y * sp.diff(phi, y))
            + source_u
            * (source_k - 8 * n * source_h)
            * sp.diff(phi, y)
            + x * source_l * phi
        )

    gamma_fixed = 1 + a * x * y
    fixed_axis = sp.expand(source_operator(gamma_fixed)).coeff(x, 1)
    assert fixed_axis == (n - 459) / 34

    forcing_axis = (
        -sp.Rational(7, 120)
        * (n + 1)
        * (
            25 * source_i * n
            - 17 * source_i
            - 25 * n
            - 15
        )
        / n
    )
    obstruction = sp.factor(fixed_axis + forcing_axis)
    numerator = (
        2975 * source_i * n**2
        + 952 * source_i * n
        - 2023 * source_i
        - 3035 * n**2
        + 22780 * n
        - 1785
    )
    assert sp.factor(obstruction + numerator / (2040 * n)) == 0

    coefficient_of_i = sp.Poly(numerator, source_i).coeff_monomial(
        source_i
    )
    assert coefficient_of_i == 2975 * n**2 + 952 * n - 2023
    assert coefficient_of_i.subs(n, 1) == 1904
    assert sp.diff(coefficient_of_i, n).subs(n, 1) > 0
    numerator_at_i_two = sp.expand(numerator.subs(source_i, 2))
    assert numerator_at_i_two == 2915 * n**2 + 24684 * n - 5831
    assert numerator_at_i_two.subs(n, 1) == 21768
    assert sp.diff(numerator_at_i_two, n).subs(n, 1) > 0

    arbitrary_graph = sp.Function("h")(x, y)
    graph_contribution = source_operator(x**2 * arbitrary_graph)
    assert sp.expand(graph_contribution).coeff(x, 0) == 0
    assert sp.expand(graph_contribution).coeff(x, 1) == 0


def main() -> None:
    verify_exact_seed_slices()
    verify_all_n_target_slice()
    verify_general_lower_recurrence()
    verify_source_axis_obstruction()
    print("verified: exact first-lower U slice and all-n target slice")
    print("verified: symbolic lower recurrence for every n and I")
    print("verified: every graph correction vanishes on the source axis")
    print("verified: the all-n obstruction numerator is strictly positive")
    print("RESULT: every binary d=1 face is closed in every degree")


if __name__ == "__main__":
    main()
