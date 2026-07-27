#!/usr/bin/env python3
"""Verify the two degree-six ternary boundary Wronskian closures."""

from __future__ import annotations

import sympy as sp

import verify_weighted_lift_first_nonlinear_cusp_subduction as nonlinear


u, f_symbol = sp.symbols("u f")


def boundary_functions() -> tuple[
    sp.Expr,
    sp.Expr,
    sp.Expr,
    sp.Expr,
    sp.Expr,
    sp.Expr,
]:
    p, q = nonlinear.build_seed()
    _, second_numerator, _, theta = nonlinear.build_maximal_subductions(
        p, q
    )
    boundary_w = u * f_symbol
    boundary_a = sp.cancel(
        (
            q.subs(nonlinear.w, boundary_w)
            + boundary_w * f_symbol
        )
        / f_symbol**2
    )
    boundary_b = sp.cancel(
        (
            p.subs(nonlinear.w, boundary_w)
            + f_symbol
        )
        / f_symbol
    )
    boundary_h = sp.cancel(
        second_numerator.subs(
            {
                nonlinear.w: boundary_w,
                nonlinear.gamma: f_symbol,
            }
        )
        / f_symbol**5
    )
    assert sp.denom(boundary_a) == 1
    assert sp.denom(boundary_b) == 1
    assert sp.denom(boundary_h) == 1
    return p, q, theta, boundary_a, boundary_b, boundary_h


def weighted_top(
    polynomial: sp.Expr,
    f_degree: int,
) -> tuple[int, tuple[int, int], sp.Expr]:
    poly = sp.Poly(polynomial, u, f_symbol)
    records = [
        (
            u_degree + f_degree * f_degree_in_term,
            (u_degree, f_degree_in_term),
            coefficient,
        )
        for (
            u_degree,
            f_degree_in_term,
        ), coefficient in poly.terms()
        if coefficient != 0
    ]
    maximum = max(record[0] for record in records)
    top_records = [
        record for record in records if record[0] == maximum
    ]
    assert len(top_records) == 1
    return top_records[0]


def verify_exact_boundary_tops() -> None:
    p, q, theta, boundary_a, boundary_b, boundary_h = (
        boundary_functions()
    )
    p5 = sp.Poly(p, nonlinear.w).coeff_monomial(
        nonlinear.w**5
    )
    q6 = sp.Poly(q, nonlinear.w).coeff_monomial(
        nonlinear.w**6
    )
    for f_degree in range(1, 23):
        degree_a, monomial_a, coefficient_a = weighted_top(
            boundary_a,
            f_degree,
        )
        degree_b, monomial_b, coefficient_b = weighted_top(
            boundary_b,
            f_degree,
        )
        degree_h, monomial_h, coefficient_h = weighted_top(
            boundary_h,
            f_degree,
        )
        assert degree_a == 6 + 4 * f_degree
        assert degree_b == 5 + 4 * f_degree
        assert degree_h == 20 + 17 * f_degree
        assert monomial_a == (6, 4)
        assert monomial_b == (5, 4)
        assert monomial_h == (20, 17)
        assert coefficient_a == q6
        assert coefficient_b == p5
        assert coefficient_h == theta


def verify_same_boundary_exhaustion() -> None:
    by_boundary_exponent: dict[int, list[tuple[int, int, int]]] = {}
    for a_degree in range(7):
        for b_degree in range(7 - a_degree):
            c_degree = 6 - a_degree - b_degree
            boundary_exponent = (
                -2 * a_degree - b_degree + c_degree
            )
            by_boundary_exponent.setdefault(
                boundary_exponent,
                [],
            ).append((a_degree, b_degree, c_degree))
    assert by_boundary_exponent[-4] == [
        (0, 5, 1),
        (2, 2, 2),
    ]
    assert by_boundary_exponent[-5] == [
        (1, 4, 1),
        (3, 1, 2),
    ]


def verify_degree_and_wronskian_obstructions() -> None:
    p, q, theta, boundary_a, boundary_b, boundary_h = (
        boundary_functions()
    )
    p5 = sp.Poly(p, nonlinear.w).coeff_monomial(
        nonlinear.w**5
    )
    q6 = sp.Poly(q, nonlinear.w).coeff_monomial(
        nonlinear.w**6
    )
    leading_f = sp.symbols("c", nonzero=True)
    lam, mu = sp.symbols("lambda mu")

    # The exact Newton degrees prove the counterterm gap for all
    # L>=1.  Check every graph-compatible L in the two cases.
    for f_degree in range(1, 23):
        degree_h = 20 + 17 * f_degree
        degree_k4 = 25 + 21 * f_degree
        degree_k4_counter = 22 + 18 * f_degree
        degree_k5 = 26 + 21 * f_degree
        degree_k5_counter = 23 + 18 * f_degree
        assert degree_k4 - degree_k4_counter == (
            3 + 3 * f_degree
        )
        assert degree_k5 - degree_k5_counter == (
            3 + 3 * f_degree
        )
        assert (
            -5 * degree_k4 + 4 * degree_h
        ) == -45 - 37 * f_degree
        assert (
            degree_h - degree_k5
        ) == -6 - 4 * f_degree

    # Directly substitute a generic leading monomial into the exact
    # full seed at the endpoints and overlap of the allowed ranges.
    # Lower coefficients of f cannot change these leading terms.
    for f_degree in (1, 4, 22):
        boundary_f = leading_f * u**f_degree
        substitutions = {f_symbol: boundary_f}
        exact_a = sp.expand(boundary_a.subs(substitutions))
        exact_b = sp.expand(boundary_b.subs(substitutions))
        exact_h = sp.expand(boundary_h.subs(substitutions))
        exact_k4 = sp.expand(
            boundary_f * exact_b**5
            + lam
            * boundary_f**2
            * exact_a**2
            * exact_b**2
        )
        exact_k5 = sp.expand(
            boundary_f * exact_a * exact_b**4
            + mu
            * boundary_f**2
            * exact_a**3
            * exact_b
        )
        wronskian_4 = sp.Poly(
            sp.expand(
                -5 * exact_h * sp.diff(exact_k4, u)
                + 4 * sp.diff(exact_h, u) * exact_k4
            ),
            u,
        )
        wronskian_5 = sp.Poly(
            sp.expand(
                5
                * (
                    sp.diff(exact_h, u) * exact_k5
                    - exact_h * sp.diff(exact_k5, u)
                )
            ),
            u,
        )
        assert wronskian_4.degree() == 44 + 38 * f_degree
        assert wronskian_5.degree() == 45 + 38 * f_degree
        expected_4 = (
            theta
            * p5**5
            * leading_f**38
            * (-45 - 37 * f_degree)
        )
        expected_5 = (
            5
            * theta
            * q6
            * p5**4
            * leading_f**38
            * (-6 - 4 * f_degree)
        )
        assert sp.factor(wronskian_4.LC() - expected_4) == 0
        assert sp.factor(wronskian_5.LC() - expected_5) == 0
        assert not wronskian_4.LC().has(lam)
        assert not wronskian_5.LC().has(mu)


def verify_characteristic_and_degree_bounds() -> None:
    # General ternary pure characteristic formulas at N=5,ell=1.
    binary_degree = 5
    c_exponent = 1
    target_weight = 4 * binary_degree + c_exponent
    for a_degree, source_i, expected_j, expected_m in (
        (0, 9, 0, 7),
        (1, 30, 15, 43),
    ):
        exponent_r = sp.Rational(
            5
            * (
                (binary_degree - 4 * c_exponent) * source_i
                - (binary_degree + 4 * c_exponent)
            ),
            2 * target_weight,
        )
        exponent_s = sp.Rational(
            17 * source_i + 15,
            2 * target_weight,
        )
        source_j = sp.factor(
            exponent_r + a_degree * exponent_s
        )
        assert source_j == expected_j
        assert source_i + source_j - 2 == expected_m
        boundary_degree_bound = (expected_m + 2) // 2
        if a_degree == 0:
            assert boundary_degree_bound == 4
        else:
            assert boundary_degree_bound == 22


def main() -> None:
    verify_exact_boundary_tops()
    verify_same_boundary_exhaustion()
    verify_degree_and_wronskian_obstructions()
    verify_characteristic_and_degree_bounds()
    print("verified: exact full-seed boundary polynomials")
    print("verified: every degree-six same-boundary counterterm")
    print("verified: counterterms are lower by 3+3L")
    print("verified: CB^5 boundary Wronskian is nonzero")
    print("verified: CAB^4 boundary Wronskian is nonzero")
    print("RESULT: both first degree-six ternary pure faces are closed")


if __name__ == "__main__":
    main()
