#!/usr/bin/env python3
"""Verify the quadratic/cubic lower-tier correction audit."""

from __future__ import annotations

import sympy as sp


def pure_forcing(
    n: int,
    c: int,
    d: int,
    source_i: sp.Expr,
) -> tuple[sp.Expr, sp.Expr]:
    determinant_u = (source_i + 1) * (c - d - n)
    determinant_v = (
        -(17 * source_i + 15)
        * (c - d - n)
        / (c + 4 * n)
    )
    target_ratio = -sp.Rational(35, 6) * n + sp.Rational(7, 30) * d
    omega = sp.factor(
        -sp.Rational(70, 3) * determinant_u
        + target_ratio * determinant_v
    )
    return omega, sp.factor(determinant_v)


def verify_quadratic_collision() -> None:
    k = sp.symbols("k", integer=True, nonnegative=True)
    source_i = 5 * k + 5
    omega, determinant_v = pure_forcing(1, 1, 1, source_i)
    assert sp.factor(
        omega - sp.Rational(14, 15) * (23 * k + 30)
    ) == 0
    assert sp.factor(determinant_v - (17 * k + 20)) == 0

    cancel_b = -14 * (23 * k + 30) / (
        15 * (17 * k + 20)
    )
    assert sp.factor(omega + cancel_b * determinant_v) == 0
    original_b_over_ac = sp.factor(sp.Rational(5, 6) * cancel_b)
    assert sp.factor(
        original_b_over_ac
        + 7 * (23 * k + 30) / (9 * (17 * k + 20))
    ) == 0

    graph_degree = 6 * k + 3
    degree_ac = 5 * graph_degree + 21
    degree_b = 4 * graph_degree + 17
    assert sp.expand(degree_ac - degree_b) == graph_degree + 4

    binary_i = sp.symbols("I", integer=True, positive=True)
    omega_b2, _ = pure_forcing(2, 0, 0, binary_i)
    assert sp.factor(
        omega_b2 + sp.Rational(35, 12) * (binary_i - 1)
    ) == 0
    for i_value in range(2, 50):
        assert omega_b2.subs(binary_i, i_value) != 0


def verify_cubic_collision() -> None:
    k = sp.symbols("k", integer=True, nonnegative=True)
    source_i = 18 * k + 15
    omega, determinant_v = pure_forcing(2, 1, 1, source_i)
    assert sp.factor(
        omega - sp.Rational(14, 15) * (67 * k + 65)
    ) == 0
    assert sp.factor(
        determinant_v - 4 * (17 * k + 15)
    ) == 0

    cancel_b2 = -7 * (67 * k + 65) / (
        30 * (17 * k + 15)
    )
    assert sp.factor(omega + cancel_b2 * determinant_v) == 0
    original_b2_over_abc = sp.factor(
        sp.Rational(5, 6) * cancel_b2
    )
    assert sp.factor(
        original_b2_over_abc
        + 7 * (67 * k + 65) / (36 * (17 * k + 15))
    ) == 0

    graph_degree = 25 * k + 18
    degree_abc = 9 * graph_degree + 38
    degree_b2 = 8 * graph_degree + 34
    assert sp.expand(degree_abc - degree_b2) == graph_degree + 4

    binary_i = sp.symbols("I", integer=True, positive=True)
    omega_b3, _ = pure_forcing(3, 0, 0, binary_i)
    assert sp.factor(
        omega_b3 + sp.Rational(35, 8) * (binary_i - 1)
    ) == 0
    for i_value in range(2, 50):
        assert omega_b3.subs(binary_i, i_value) != 0


def verify_polynomial_coefficient_solvability() -> None:
    for n_value, c_value, d_value in ((1, 1, 1), (2, 1, 1)):
        derivative_weight = 8 * n_value + 2 * c_value
        pole_weight = 10 * n_value + 2 * d_value
        for output_degree in range(-1, 100):
            multiplier = (
                derivative_weight * (output_degree + 1)
                + pole_weight
            )
            assert multiplier > 0

    # Deleting one C is the unique target-degree-lowering move whose
    # maximal-x loss equals the first-lower seed loss I+1.
    for delta_n in range(-3, 4):
        for delta_c in range(-3, 4):
            if delta_n + delta_c < 1:
                continue
            if 4 * delta_n + delta_c == 1:
                assert (delta_n, delta_c) == (0, 1)


def main() -> None:
    verify_quadratic_collision()
    verify_cubic_collision()
    verify_polynomial_coefficient_solvability()
    print("verified: pure B^2 and B^3 first-lower repairs")
    print("verified: exact AC+B and ABC+B^2 cancellation parameters")
    print("verified: both cancelling monomials occur at drop m+4")
    print("verified: tuned x^-1 equations admit polynomial coefficients")
    print("RESULT: quadratic and cubic all-lower-tier claims retain open chains")


if __name__ == "__main__":
    main()
