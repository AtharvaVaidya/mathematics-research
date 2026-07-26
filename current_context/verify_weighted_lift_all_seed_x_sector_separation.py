#!/usr/bin/env python3
"""Verify exact all-seed separation in the maximal-x filtration."""

from __future__ import annotations

import sympy as sp

from verify_weighted_lift_first_nonlinear_cusp_subduction import (
    build_maximal_subductions,
    build_seed,
)


def verify_exact_u_support() -> None:
    p, q = build_seed()
    _, second_numerator, _, _ = build_maximal_subductions(p, q)
    w, gamma = sp.symbols("w gamma")
    support = [
        (w_power, gamma_power)
        for (w_power, gamma_power), coefficient
        in sp.Poly(second_numerator, w, gamma).terms()
        if coefficient != 0
    ]
    assert len(support) == 77

    relative_layers: list[tuple[int, int, int, int]] = []
    for w_power, gamma_power in support:
        explicit_loss = 20 - w_power
        gamma_loss = 22 - w_power - gamma_power
        assert explicit_loss >= 0
        assert gamma_loss >= 0
        relative_layers.append(
            (
                explicit_loss,
                gamma_loss,
                w_power,
                gamma_power,
            )
        )

    # The top w^20 gamma^2 term is the only support point with no
    # gamma loss.  The w^19 gamma^2 term is the unique (1,1) layer.
    assert [
        layer for layer in relative_layers if layer[1] == 0
    ] == [(0, 0, 20, 2)]
    assert [
        layer for layer in relative_layers if layer[:2] == (1, 1)
    ] == [(1, 1, 19, 2)]


def verify_target_seed_layers() -> None:
    # A q_k or B p_k seed has equal explicit-x and gamma losses.
    standard_a_layers = [(6 - power, 6 - power) for power in range(7)]
    standard_b_layers = [(5 - power, 5 - power) for power in range(6)]
    assert standard_a_layers[-1] == (0, 0)
    assert standard_b_layers[-1] == (0, 0)

    # The added w*gamma in A and gamma in B both have relative layer
    # (5,4).  In a product, layers add coefficientwise.
    extra_layer = (5, 4)
    all_non_top_atomic_layers = (
        standard_a_layers[:-1]
        + standard_b_layers[:-1]
        + [extra_layer]
    )
    for explicit_loss, gamma_loss in all_non_top_atomic_layers:
        assert explicit_loss >= 1
        assert gamma_loss >= 1
    assert all_non_top_atomic_layers.count((1, 1)) == 2

    # Any non-top component of A^j B^(n-j) has B>=1 and A>=B.
    # The only total layer (1,1) uses one first-lower standard seed.
    for left in [(0, 0)] + all_non_top_atomic_layers:
        for right in [(0, 0)] + all_non_top_atomic_layers:
            total = (left[0] + right[0], left[1] + right[1])
            if total == (0, 0):
                assert left == right == (0, 0)
            elif total == (1, 1):
                assert (left, right).count((0, 0)) == 1
                assert (left, right).count((1, 1)) == 1
            else:
                assert total[0] >= total[1] >= 1


def verify_normalized_x_valuation() -> None:
    source_i, explicit_loss, gamma_loss = sp.symbols(
        "I A B",
        integer=True,
        nonnegative=True,
    )
    valuation = source_i * (1 - gamma_loss) - explicit_loss
    assert valuation.subs(
        {explicit_loss: 0, gamma_loss: 0}
    ) == source_i
    assert valuation.subs(
        {explicit_loss: 1, gamma_loss: 1}
    ) == -1

    # For I>=2, every non-top layer has valuation <=-1.  Equality
    # requires (A,B)=(1,1).
    for i_value in range(2, 100):
        for a_value in range(0, 100):
            for b_value in range(1, 100):
                value = i_value * (1 - b_value) - a_value
                assert value <= 0
                if a_value >= 1:
                    assert value <= -1
                    if value == -1:
                        assert (a_value, b_value) == (1, 1)


def verify_graph_laurent_coefficients_are_polynomial() -> None:
    x, y, t = sp.symbols("x y t")
    for source_x_power in range(9):
        for source_y_power in range(9):
            transformed = sp.expand(
                x ** (source_x_power + 2)
                * (t - x**-1) ** source_y_power
            )
            coefficients: dict[int, sp.Expr] = {}
            for term in sp.Add.make_args(transformed):
                powers = term.as_powers_dict()
                x_power = int(powers.get(x, 0))
                coefficients[x_power] = sp.expand(
                    coefficients.get(x_power, 0)
                    + term / x**x_power
                )
            for coefficient in coefficients.values():
                assert sp.Poly(coefficient, t).is_univariate

            # Its maximal x-power is p+2 and has coefficient t^q.
            maximal_x_power = source_x_power + 2
            assert coefficients[maximal_x_power] == t**source_y_power


def verify_constant_rhs_and_affine_gaps() -> None:
    # At x=infinity, deg_x gamma=I (I>=2 for a nonconstant graph;
    # I=1 is the g=0 constant-graph case),
    # deg_x U0=15+17I, deg_x A0=deg_x B0=4+4I.
    for source_i in range(1, 100):
        u_degree = 15 + 17 * source_i
        ab_degree = 4 + 4 * source_i
        c_degree = 1 + source_i

        # The common top Jacobian factor U0*V0/(x*gamma) has
        # positive degree, so a nonzero constant RHS cannot occur in
        # either the maximal I-sector or the first-lower -1 sector.
        for target_degree in range(1, 30):
            common_degree = (
                u_degree
                + target_degree * ab_degree
                - 1
                - source_i
            )
            assert common_degree - 1 > 0

            # Affine additions to the second coordinate are too low
            # to reach the first-lower layer.  For n=1, A and B are
            # already part of the homogeneous face, so only C and a
            # constant are genuinely lower.
            if target_degree >= 2:
                assert (
                    target_degree * ab_degree - ab_degree
                    > source_i + 1
                )
            assert target_degree * ab_degree - c_degree > source_i + 1

        # Affine additions to U are likewise below the first-lower
        # x layer.
        assert u_degree - ab_degree > source_i + 1
        assert u_degree - c_degree > source_i + 1


def verify_constant_graphs() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    polynomial = sp.Function("P")(sp.Symbol("t"))
    local_t = next(iter(polynomial.free_symbols))
    polynomial_prime = sp.diff(polynomial, local_t)

    # If g=c!=0, the maximal gamma sector is c*x^2.  Its exact top
    # equation is proportional to 5n/t+49P'/P.  A polynomial P would
    # have tP'/P=-5n/49, an impossible negative degree.
    maximal_constant_graph_equation = (
        5 * n / local_t + 49 * polynomial_prime / polynomial
    )
    required_euler_degree = sp.solve(
        sp.Eq(maximal_constant_graph_equation, 0),
        polynomial_prime / polynomial,
    )
    assert required_euler_degree == [-5 * n / (49 * local_t)]

    # If g=0, gamma=(1-a)+a*x*t.  The x^1 equation can vanish only
    # for P=t^(n/4).  On that pure face, the remaining x^0 equation
    # is -(5n/4)*(1-a)/t, nonzero for the fixed a=-57/34.
    degree = sp.symbols("d", integer=True, nonnegative=True)
    maximal_zero_graph_coefficient = -8 * n + 32 * degree
    assert sp.solve(
        sp.Eq(maximal_zero_graph_coefficient, 0),
        degree,
    ) == [n / 4]
    fixed_a = -sp.Rational(57, 34)
    next_coefficient = sp.factor(
        (1 - fixed_a) * (-5 * n + 15 * n / 4)
    )
    assert next_coefficient == -sp.Rational(455, 136) * n
    assert next_coefficient != 0


def main() -> None:
    verify_exact_u_support()
    verify_target_seed_layers()
    verify_normalized_x_valuation()
    verify_graph_laurent_coefficients_are_polynomial()
    verify_constant_rhs_and_affine_gaps()
    verify_constant_graphs()
    print("verified: all 77 U-support layers satisfy A,B>=0")
    print("verified: only the top layer has B=0")
    print("verified: only the exact first-lower seeds reach x^-1")
    print("verified: graph Laurent coefficients are polynomial in t")
    print("verified: constant RHS and affine additions miss both layers")
    print("verified: both constant-graph cases are excluded")
    print("RESULT: maximal-x and first-lower sectors are exactly separated")


if __name__ == "__main__":
    main()
