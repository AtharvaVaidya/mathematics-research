#!/usr/bin/env python3
"""Verify the next exact SAGBI saturation generator."""

from __future__ import annotations

import sympy as sp

import verify_weighted_lift_degree_six_ternary_boundary_wronskian_closure as boundary
import verify_weighted_lift_first_nonlinear_cusp_subduction as nonlinear


def build_boundary_subduction() -> tuple[
    sp.Expr,
    sp.Expr,
    tuple[sp.Rational, sp.Rational, sp.Rational],
]:
    u = boundary.u
    f = boundary.f_symbol
    p, q, _, template_a, template_b, _ = (
        boundary.boundary_functions()
    )
    p5 = sp.Poly(p, nonlinear.w).coeff_monomial(nonlinear.w**5)
    q6 = sp.Poly(q, nonlinear.w).coeff_monomial(nonlinear.w**6)
    _, _, lambda_zero, _ = nonlinear.build_maximal_subductions(p, q)

    first_coefficients = (
        -sp.Rational(8505, 18948593792),
        -sp.Rational(79515, 151588750336),
        sp.Rational(1587485, 303177500672),
        -sp.Rational(1079635, 303177500672),
    )
    first_relation = sp.expand(
        p5**6 * template_a**5 * f**4
        - q6**5 * template_b**6
    )
    template_t = sp.expand(
        first_relation
        + first_coefficients[0] * template_a**4 * template_b * f**3
        + first_coefficients[1] * template_a**3 * template_b**2 * f**2
        + first_coefficients[2] * template_a**2 * template_b**3 * f
        + first_coefficients[3] * template_a * template_b**4
    )
    assert sp.Poly(template_t, u, f).coeff_monomial(
        u**25 * f**19
    ) == lambda_zero

    saturation = sp.expand(
        q6**5 * template_b * template_t
        - p5 * lambda_zero * template_a**5 * f**3
    )
    corrections = (
        -sp.Rational(
            1289186932405,
            367666387654882241806336,
        ),
        sp.Rational(
            967724214885,
            183833193827441120903168,
        ),
        sp.Rational(
            280059055635,
            367666387654882241806336,
        ),
    )
    completed = sp.expand(
        saturation
        + corrections[0] * template_a**4 * template_b * f**2
        + corrections[1] * template_a**3 * template_b**2 * f
        + corrections[2] * template_a**2 * template_b**3
    )
    return completed, template_t, corrections


def verify_frontier() -> None:
    completed, _, _ = build_boundary_subduction()
    u = boundary.u
    f = boundary.f_symbol
    polynomial = sp.Poly(completed, u, f)

    # The three reducible leading pairs have been cancelled.
    for i, j in ((29, 22), (28, 21), (27, 20)):
        assert polynomial.coeff_monomial(u**i * f**j) == 0

    coefficient_19 = -sp.Rational(
        124730099934975,
        18931415844142301862996144553984,
    )
    coefficient_20 = sp.Rational(
        1423828125,
        8946793877193904472115380224,
    )
    assert polynomial.coeff_monomial(u**26 * f**19) == coefficient_19
    assert polynomial.coeff_monomial(u**25 * f**20) == coefficient_20

    terms = [
        (i, j)
        for (i, j), coefficient in polynomial.terms()
        if coefficient != 0
    ]
    pareto = [
        (i, j)
        for i, j in terms
        if not any(
            i2 >= i
            and j2 >= j
            and (i2 > i or j2 > j)
            for i2, j2 in terms
        )
    ]
    assert pareto == [(26, 19), (25, 20)]

    for graph_degree in range(2, 30):
        weighted_degrees = {
            (i, j): i + graph_degree * j
            for i, j in terms
        }
        maximum = max(weighted_degrees.values())
        assert [
            pair
            for pair, degree in weighted_degrees.items()
            if degree == maximum
        ] == [(25, 20)]

    fixed_leading = -sp.Rational(57, 34)
    tied_coefficient = sp.factor(
        coefficient_19 + fixed_leading * coefficient_20
    )
    assert tied_coefficient == -sp.Rational(
        2206277077800825,
        321834069350419131670934457417728,
    )
    assert tied_coefficient != 0


def verify_full_exponent_semigroup() -> None:
    C = sp.Matrix([1, 0, 1])
    B = sp.Matrix([-1, 5, 4])
    A = sp.Matrix([-2, 6, 4])
    T = sp.Matrix([-6, 25, 19])
    U = sp.Matrix([-5, 20, 17])
    assert B + U == sp.Matrix([-6, 25, 21])
    assert B + U != T
    assert B + T == 5 * A + 3 * C

    matrix = sp.Matrix.hstack(C, B, A, T, U)
    targets = (
        sp.Matrix([-7, 25, 20]),
        sp.Matrix([-7, 26, 19]),
    )
    for target in targets:
        found = False
        for c in range(30):
            for b in range(15):
                for a in range(15):
                    for t in range(5):
                        for v in range(5):
                            exponents = sp.Matrix([c, b, a, t, v])
                            if matrix * exponents == target:
                                found = True
        assert not found


def main() -> None:
    verify_frontier()
    verify_full_exponent_semigroup()
    print("verified: false projected BU~T relation")
    print("verified: exact BT~A^5 C^3 saturation subduction")
    print("verified: new two-vector regular-boundary frontier")
    print("verified: frontier lies outside <A,B,C,T,U>")


if __name__ == "__main__":
    main()
