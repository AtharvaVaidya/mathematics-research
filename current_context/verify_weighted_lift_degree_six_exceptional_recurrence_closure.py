#!/usr/bin/env python3
"""Verify closure of the n=6,d=1 exceptional binary target family."""

from __future__ import annotations

import sympy as sp

from verify_weighted_lift_first_nonlinear_cusp_subduction import (
    build_maximal_subductions,
    build_seed,
)


x, y, u, t, eta = sp.symbols("x y u t eta")


def jacobian(
    first: sp.Expr,
    second: sp.Expr,
    variables: tuple[sp.Symbol, sp.Symbol],
) -> sp.Expr:
    first_variable, second_variable = variables
    return sp.expand(
        sp.diff(first, first_variable) * sp.diff(second, second_variable)
        - sp.diff(first, second_variable) * sp.diff(second, first_variable)
    )


def verify_exact_seed_ratios() -> None:
    p, q = build_seed()
    _, second_numerator, _, theta = build_maximal_subductions(p, q)
    w, gamma_symbol = sp.symbols("w gamma")

    second_poly = sp.Poly(second_numerator, w, gamma_symbol)
    top = second_poly.coeff_monomial(w**20 * gamma_symbol**2)
    lower = second_poly.coeff_monomial(w**19 * gamma_symbol**2)
    assert top == theta
    assert sp.factor(lower / top) == -sp.Rational(70, 3)

    p_poly = sp.Poly(p, w)
    q_poly = sp.Poly(q, w)
    p5 = p_poly.coeff_monomial(w**5)
    p4 = p_poly.coeff_monomial(w**4)
    q6 = q_poly.coeff_monomial(w**6)
    q5 = q_poly.coeff_monomial(w**5)
    assert sp.factor(q5 / q6) == -sp.Rational(28, 5)
    assert sp.factor(p4 / p5) == -sp.Rational(35, 6)
    assert sp.factor(q5 / q6 + 5 * p4 / p5) == -sp.Rational(
        1043, 30
    )
    assert sp.factor(6 * p4 / p5) == -35

    # Audit the full 77-term U-numerator support.  After division by
    # x^5*gamma^5, w^i*gamma^j has graph weight below.  The displayed
    # (19,2) term is uniquely second for every integer m>=1, although
    # later terms need not be another full m+4 below it.
    m = sp.symbols("m", integer=True, positive=True)

    def u_graph_weight(monomial: tuple[int, int]) -> sp.Expr:
        w_power, gamma_power = monomial
        return sp.expand(
            w_power * (m + 4)
            + (gamma_power - 5) * (m + 2)
            - 5
        )

    top_monomial = (20, 2)
    lower_monomial = (19, 2)
    support = [
        monomial
        for monomial, coefficient in second_poly.terms()
        if coefficient != 0
    ]
    assert len(support) == 77
    for reference, excluded in (
        (top_monomial, {top_monomial}),
        (lower_monomial, {top_monomial, lower_monomial}),
    ):
        for monomial in support:
            if monomial in excluded:
                continue
            difference = sp.Poly(
                u_graph_weight(reference) - u_graph_weight(monomial),
                m,
            )
            assert difference.coeff_monomial(m) >= 0
            assert difference.eval(1) > 0

    # In Q6, q5 and p4 cost exactly m+4.  The next seed powers and
    # products of two first-lower replacements cost at least 2(m+4).
    # The added w*gamma and gamma pieces of A and B cost 4m+18.
    assert sp.expand((6 - 5) * (m + 4)) == m + 4
    assert sp.expand((6 - 4) * (m + 4)) == 2 * (m + 4)
    assert sp.expand((5 - 3) * (m + 4)) == 2 * (m + 4)
    assert sp.expand(
        6 * (m + 4) - ((m + 4) + (m + 2))
    ) == 4 * m + 18
    assert sp.expand(
        5 * (m + 4) - (m + 2)
    ) == 4 * m + 18
    assert sp.expand(4 * m + 18 - (m + 4)) == 3 * m + 14


def verify_reduced_lower_seed_equation() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    source_i = 48 * k + 33
    exponent_r = 30 * k + 20
    exponent_s = 17 * k + 12
    face = t + eta
    lower_face = -sp.Rational(1043, 30) * t - 35 * eta

    logarithmic_gamma_x = source_i / x
    logarithmic_gamma_t = exponent_r / t + exponent_s / face

    def logarithmic_determinant(
        first_x: int,
        first_t: int,
        first_gamma: int,
        first_extra_t: sp.Expr,
        second_x: int,
        second_t: int,
        second_gamma: int,
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
        return first_log_x * second_log_t - first_log_t * second_log_x

    # After division by U0*V0/(x*gamma), the product prefactors of
    # J(U1,V0) and J(U0,V1) reduce respectively to
    # (-70/3)/t and lower_face/(t*face).
    reduced = sp.factor(
        -sp.Rational(70, 3)
        / t
        * logarithmic_determinant(
            14, 19, 16, 0, 24, 30, 24, 1 / face
        )
        + lower_face
        / (t * face)
        * logarithmic_determinant(
            15,
            20,
            17,
            0,
            23,
            29,
            23,
            -sp.Rational(1043, 30) / lower_face,
        )
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
    assert sp.factor(reduced - expected) == 0

    characteristic_operator_over_gamma = (
        x * (30 / t + 17 / face) * logarithmic_gamma_x
        - 48 * logarithmic_gamma_t
        - 30 / t
        + 15 / face
    )
    assert sp.factor(characteristic_operator_over_gamma) == 0


def verify_source_axis_obstruction() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    a = -sp.Rational(57, 34)
    source_u = 1 + x * y
    source_h = source_u + eta * x
    source_k = 47 * source_u + 30 * eta * x
    source_l = -15 * source_u - 30 * eta * x

    def source_operator(phi: sp.Expr) -> sp.Expr:
        return sp.expand(
            x
            * source_k
            * (x * sp.diff(phi, x) - y * sp.diff(phi, y))
            + source_u
            * (source_k - 48 * source_h)
            * sp.diff(phi, y)
            + x * source_l * phi
        )

    gamma_fixed = 1 + a * x * y
    fixed_residue = sp.expand(source_operator(gamma_fixed)).coeff(x, 1)
    assert fixed_residue == -sp.Rational(453, 34)

    forcing = (
        -sp.Rational(7, 15)
        * x
        * (
            (931 * k + 616) * source_u**2
            + (1440 * k + 940) * eta * source_u * x
            + (900 * k + 600) * eta**2 * x**2
        )
        / (source_u * source_h)
    )
    forcing_residue = sp.simplify(sp.limit(forcing / x, x, 0))
    assert forcing_residue == -sp.Rational(7, 15) * (931 * k + 616)

    obstruction = sp.factor(fixed_residue + forcing_residue)
    expected_obstruction = -(221578 * k + 153403) / 510
    assert sp.factor(obstruction - expected_obstruction) == 0
    for sample_k in range(1, 100):
        assert obstruction.subs(k, sample_k) != 0

    arbitrary_graph = sp.Function("h")(x, y)
    graph_contribution = source_operator(x**2 * arbitrary_graph)
    quotient = sp.simplify(graph_contribution / x**2)
    assert not quotient.has(sp.zoo, sp.nan)
    assert sp.expand(graph_contribution).coeff(x, 0) == 0
    assert sp.expand(graph_contribution).coeff(x, 1) == 0


def main() -> None:
    verify_exact_seed_ratios()
    verify_reduced_lower_seed_equation()
    verify_source_axis_obstruction()
    print("verified: exact U and degree-six target lower-seed ratios")
    print("verified: the first lower recurrence reduces to one forcing term")
    print("verified: every graph correction vanishes on the source-axis jet")
    print("verified: residual = -(221578*k+153403)/510")
    print("RESULT: the first degree-six exceptional binary face is closed")


if __name__ == "__main__":
    main()
