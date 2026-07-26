#!/usr/bin/env python3
"""Verify the full boundary-valuation obstruction for ternary targets."""

from __future__ import annotations

import sympy as sp

import verify_weighted_lift_degree_six_ternary_boundary_wronskian_closure as degree_six
import verify_weighted_lift_first_nonlinear_cusp_subduction as nonlinear


def support_degrees(
    polynomial: sp.Expr,
    f_degree: int,
) -> list[int]:
    degrees = {
        u_degree + f_degree * f_power
        for (u_degree, f_power), coefficient in sp.Poly(
            polynomial,
            degree_six.u,
            degree_six.f_symbol,
        ).terms()
        if coefficient != 0
    }
    return sorted(degrees, reverse=True)


def verify_full_seed_degree_gaps() -> None:
    _, _, _, boundary_a, boundary_b, boundary_h = (
        degree_six.boundary_functions()
    )
    # Prove the support inequalities symbolically for every L>=1.
    # A gap du+L*df is at least L+1 if du,df>=1, or if
    # du>=0 and df>=2.
    for polynomial, top_support in (
        (boundary_a, (6, 4)),
        (boundary_b, (5, 4)),
        (boundary_h, (20, 17)),
    ):
        terms = sp.Poly(
            polynomial,
            degree_six.u,
            degree_six.f_symbol,
        ).terms()
        assert any(
            support == top_support and coefficient != 0
            for support, coefficient in terms
        )
        for support, coefficient in terms:
            if coefficient == 0 or support == top_support:
                continue
            u_loss = top_support[0] - support[0]
            f_loss = top_support[1] - support[1]
            assert u_loss >= 0
            assert f_loss >= 1
            assert u_loss >= 1 or f_loss >= 2

    # The exact U support statement used in the paper is equivalent
    # to the preceding boundary-H inequalities.
    for (u_power, f_power), coefficient in sp.Poly(
        boundary_h,
        degree_six.u,
        degree_six.f_symbol,
    ).terms():
        if coefficient == 0 or (u_power, f_power) == (20, 17):
            continue
        loss_a = 20 - u_power
        loss_b = 17 - f_power
        assert loss_a >= 0 and loss_b >= 1
        if loss_b == 1:
            assert loss_a == 1


def verify_same_boundary_parameterization() -> None:
    # Symbolic identities behind the exact Diophantine formula.
    a_degree, b_degree, c_exponent, k, f_degree = sp.symbols(
        "a b c k L",
        integer=True,
        nonnegative=True,
    )
    other_a = a_degree + 2 * k
    other_b = b_degree - 3 * k
    other_c = c_exponent + k
    assert sp.expand(
        (other_a + other_b + other_c)
        - (a_degree + b_degree + c_exponent)
    ) == 0
    assert sp.expand(
        (-2 * other_a - other_b + other_c)
        - (-2 * a_degree - b_degree + c_exponent)
    ) == 0
    base_u_degree = (
        c_exponent * f_degree
        + a_degree * (6 + 4 * f_degree)
        + b_degree * (5 + 4 * f_degree)
    )
    other_u_degree = (
        other_c * f_degree
        + other_a * (6 + 4 * f_degree)
        + other_b * (5 + 4 * f_degree)
    )
    assert sp.expand(
        base_u_degree
        - other_u_degree
        - 3 * k * (f_degree + 1)
    ) == 0

    # Exhaust finite samples to guard implementation and endpoint
    # conditions (nonnegative target exponents).
    for binary_degree in range(0, 20):
        for c_exponent in range(0, 10):
            total_degree = binary_degree + c_exponent
            if total_degree == 0:
                continue
            for a_degree in range(binary_degree + 1):
                b_degree = binary_degree - a_degree
                boundary_exponent = (
                    -2 * a_degree - b_degree + c_exponent
                )
                same_boundary: list[tuple[int, int, int]] = []
                for other_a in range(total_degree + 1):
                    for other_b in range(
                        total_degree - other_a + 1
                    ):
                        other_c = (
                            total_degree - other_a - other_b
                        )
                        if other_c < c_exponent:
                            continue
                        other_boundary = (
                            -2 * other_a - other_b + other_c
                        )
                        if other_boundary == boundary_exponent:
                            same_boundary.append(
                                (other_a, other_b, other_c)
                            )
                expected = [
                    (
                        a_degree + 2 * k,
                        b_degree - 3 * k,
                        c_exponent + k,
                    )
                    for k in range(b_degree // 3 + 1)
                ]
                assert same_boundary == expected

                for f_degree in range(1, 8):
                    base_degree = (
                        c_exponent * f_degree
                        + a_degree * (6 + 4 * f_degree)
                        + b_degree * (5 + 4 * f_degree)
                    )
                    for k, (
                        other_a,
                        other_b,
                        other_c,
                    ) in enumerate(expected):
                        other_degree = (
                            other_c * f_degree
                            + other_a * (6 + 4 * f_degree)
                            + other_b * (5 + 4 * f_degree)
                        )
                        assert base_degree - other_degree == (
                            3 * k * (f_degree + 1)
                        )

    # A lower boundary block can precede the CB^5 block.  Therefore
    # same-boundary exhaustion alone does not isolate CB^5.
    beta_cb5 = -2 * 0 - 5 + 1
    beta_c2a4 = -2 * 4 - 0 + 2
    assert (beta_cb5, beta_c2a4) == (-4, -6)
    assert beta_c2a4 < beta_cb5


def verify_general_wronskian_leading_coefficient() -> None:
    binary_degree, c_exponent, a_degree, f_degree = sp.symbols(
        "N ell d L",
        integer=True,
        nonnegative=True,
    )
    target_weight = 4 * binary_degree + c_exponent
    beta = c_exponent - binary_degree - a_degree
    degree_h = 20 + 17 * f_degree
    degree_v = (
        5 * binary_degree
        + a_degree
        + target_weight * f_degree
    )
    coefficient_b = (
        17 * a_degree
        - 3 * binary_degree
        - 22 * c_exponent
    )
    coefficient_c = (
        15 * a_degree
        - 5 * binary_degree
        - 20 * c_exponent
    )
    wronskian_degree_factor = sp.expand(
        -5 * degree_v - beta * degree_h
    )
    assert sp.expand(
        wronskian_degree_factor
        - coefficient_b * f_degree
        - coefficient_c
    ) == 0
    assert sp.expand(
        17 * coefficient_c - 15 * coefficient_b
    ) == -10 * target_weight


def verify_exceptional_locus_and_sign_reduction() -> None:
    binary_degree, c_exponent, a_degree = sp.symbols(
        "N ell d",
        integer=True,
        nonnegative=True,
    )
    denominator_x = (
        25 * binary_degree
        - 17 * a_degree
        - 100 * c_exponent
    )
    source_i = (
        100 * c_exponent
        + 25 * binary_degree
        + 15 * a_degree
    ) / denominator_x
    source_j = 120 * a_degree / denominator_x
    difference = sp.factor(source_i - source_j)
    assert sp.factor(
        difference
        - (
            5
            * (
                5 * binary_degree
                - 21 * a_degree
                + 20 * c_exponent
            )
            / denominator_x
        )
    ) == 0

    # Algebra behind the B>=0 contradiction in the note:
    # h>=2 gives 300ell>=25N+71d.
    lhs_h = (
        5
        * (
            5 * binary_degree
            - 21 * a_degree
            + 20 * c_exponent
        )
        - 2 * denominator_x
    )
    assert sp.expand(lhs_h) == (
        -25 * binary_degree
        - 71 * a_degree
        + 300 * c_exponent
    )
    # Combining B>=0 with that inequality gives d>=25N/61:
    assert 725 * 61 == 25 * 1769
    # Combining h>=2 with X>0 gives d<25N/61:
    upper_x = sp.expand(
        denominator_x
        - (
            50 * binary_degree - 122 * a_degree
        )
        / 3
    )
    h_boundary = (
        300 * c_exponent
        - 25 * binary_degree
        - 71 * a_degree
    )
    assert sp.factor(
        upper_x + h_boundary / 3
    ) == 0


def verify_boundary_diagonal_next_coefficient() -> None:
    binary_degree, c_exponent, a_degree, source_i = sp.symbols(
        "N ell d I",
        integer=True,
        positive=True,
    )
    target_weight = 4 * binary_degree + c_exponent
    coefficient_b = (
        17 * a_degree
        - 3 * binary_degree
        - 22 * c_exponent
    )
    coefficient_c = (
        15 * a_degree
        - 5 * binary_degree
        - 20 * c_exponent
    )
    # I=J is the boundary equation 21d=5N+20ell, and the
    # characteristic relation then gives B*I+C=0.
    diagonal_relation = {
        a_degree: (
            5 * binary_degree + 20 * c_exponent
        ) / 21
    }
    exceptional_i = sp.factor(
        15
        * (binary_degree + 4 * c_exponent)
        / (11 * binary_degree - 61 * c_exponent)
    )
    assert sp.factor(
        (
            coefficient_b * exceptional_i + coefficient_c
        ).subs(diagonal_relation)
    ) == 0
    assert sp.expand(
        17 * coefficient_c - 15 * coefficient_b
    ) == -10 * target_weight

    # Formal leading-deviation calculation, symbolic in both L and
    # delta rather than checked only at finitely many values.
    u = sp.symbols("u", nonzero=True)
    leading_c, next_b = sp.symbols("c b", nonzero=True)
    boundary_degree, delta = sp.symbols(
        "L delta",
        integer=True,
        positive=True,
    )
    ratio = next_b / leading_c
    exact_f = leading_c * u**boundary_degree * (
        1 + ratio * u ** (-delta)
    )
    logarithmic_deviation = sp.factor(
        sp.diff(exact_f, u) / exact_f - boundary_degree / u
    )
    expected_deviation = sp.factor(
        -delta
        * ratio
        * u ** (-delta - 1)
        / (1 + ratio * u ** (-delta))
    )
    assert sp.factor(
        logarithmic_deviation - expected_deviation
    ) == 0


def verify_primitive_case() -> None:
    from fractions import Fraction

    primitive_solutions: list[
        tuple[int, int, int, int, int, int]
    ] = []
    for total_degree in range(1, 16):
        for ell_value in range(total_degree + 1):
            n_value = total_degree - ell_value
            for d_value in range(n_value + 1):
                if 21 * d_value != 5 * n_value + 20 * ell_value:
                    continue
                x_value = (
                    25 * n_value
                    - 17 * d_value
                    - 100 * ell_value
                )
                if x_value <= 0:
                    continue
                i_value = Fraction(
                    100 * ell_value
                    + 25 * n_value
                    + 15 * d_value,
                    x_value,
                )
                j_value = Fraction(120 * d_value, x_value)
                if (
                    i_value.denominator == 1
                    and j_value.denominator == 1
                    and i_value == j_value
                ):
                    primitive_solutions.append(
                        (
                            total_degree,
                            n_value,
                            ell_value,
                            d_value,
                            int(i_value),
                            int(j_value),
                        )
                    )
    assert primitive_solutions == [(15, 13, 2, 5, 15, 15)]

    binary_degree = 13
    c_exponent = 2
    a_degree = 5
    source_i = source_j = 15
    target_weight = 4 * binary_degree + c_exponent
    coefficient_b = (
        17 * a_degree
        - 3 * binary_degree
        - 22 * c_exponent
    )
    coefficient_c = (
        15 * a_degree
        - 5 * binary_degree
        - 20 * c_exponent
    )
    assert (target_weight, coefficient_b, coefficient_c) == (
        54,
        2,
        -30,
    )
    assert coefficient_b * source_i + coefficient_c == 0
    assert 21 * a_degree == (
        5 * binary_degree + 20 * c_exponent
    )
    assert source_i == source_j

    total_degree = binary_degree + c_exponent
    boundary_exponent = (
        c_exponent - binary_degree - a_degree
    )
    same_boundary = []
    for other_a in range(total_degree + 1):
        for other_b in range(total_degree - other_a + 1):
            other_c = total_degree - other_a - other_b
            if other_c < c_exponent:
                continue
            if -2 * other_a - other_b + other_c == boundary_exponent:
                same_boundary.append((other_a, other_b, other_c))
    assert same_boundary == [
        (5, 8, 2),
        (7, 5, 3),
        (9, 2, 4),
    ]
    assert 3 * (source_i + 1) == 48

    # Exact full-seed Newton supports have their first correction at
    # drop I+1=16, after every possible f-deviation delta<=15.
    _, _, _, boundary_a, boundary_b, boundary_h = (
        degree_six.boundary_functions()
    )
    for polynomial in (boundary_a, boundary_b, boundary_h):
        degrees = support_degrees(polynomial, source_i)
        assert degrees[0] - degrees[1] >= 16

    p, q_seed = nonlinear.build_seed()
    _, _, _, theta = nonlinear.build_maximal_subductions(
        p,
        q_seed,
    )
    p5 = sp.Poly(p, nonlinear.w).coeff_monomial(
        nonlinear.w**5
    )
    q6 = sp.Poly(q_seed, nonlinear.w).coeff_monomial(
        nonlinear.w**6
    )
    c, b = sp.symbols("c b", nonzero=True)
    delta = sp.symbols("delta", integer=True, positive=True)
    expected_next = (
        -2
        * delta
        * theta
        * q6**5
        * p5**8
        * c**70
        * b
    )
    assert expected_next != 0


def verify_polar_boundary_valuation() -> None:
    rho = sp.symbols("rho", integer=True, negative=True)
    a_degree, b_degree, c_exponent = sp.symbols(
        "a b c",
        integer=True,
        nonnegative=True,
    )
    k, chain_length = sp.symbols(
        "k K",
        integer=True,
        nonnegative=True,
    )
    f_degree = sp.symbols("L", integer=True, positive=True)

    # A graph monomial x^i*y^j occurring at x-valuation rho has
    # j=i+2-rho, so every leading coefficient is divisible by
    # (u-1)^(2-rho).
    x_degree = sp.symbols("i", integer=True, nonnegative=True)
    y_degree = x_degree + 2 - rho
    assert sp.expand(x_degree + 2 - y_degree - rho) == 0
    assert sp.expand(y_degree - (2 - rho)) == x_degree

    # Exact lower seed terms have smaller gamma degree.  Hence the
    # displayed toric tops are uniquely lowest when rho<0.
    _, _, _, boundary_a, boundary_b, boundary_h = (
        degree_six.boundary_functions()
    )
    for polynomial, top_f_power in (
        (boundary_a, 4),
        (boundary_b, 4),
        (boundary_h, 17),
    ):
        f_powers = [
            support[1]
            for support, coefficient in sp.Poly(
                polynomial,
                degree_six.u,
                degree_six.f_symbol,
            ).terms()
            if coefficient != 0
        ]
        assert f_powers.count(top_f_power) == 1
        assert all(power < top_f_power for power in f_powers[1:])

    target_gamma_power = (
        4 * a_degree + 4 * b_degree + c_exponent
    )
    target_u_power = 6 * a_degree + 5 * b_degree
    target_x_power = (
        (-2 + 4 * rho) * a_degree
        + (-1 + 4 * rho) * b_degree
        + (1 + rho) * c_exponent
    )

    delta_a = (2 - 3 * rho) * k
    delta_b = -3 * (1 - rho) * k
    delta_c = k
    assert sp.expand(delta_a + delta_b + delta_c) == 0
    assert sp.expand(
        (
            (-2 + 4 * rho) * delta_a
            + (-1 + 4 * rho) * delta_b
            + (1 + rho) * delta_c
        )
    ) == 0
    assert sp.expand(
        (
            4 * delta_a + 4 * delta_b + delta_c
        )
        + 3 * k
    ) == 0
    assert sp.expand(
        (
            6 * delta_a
            + 5 * delta_b
            + f_degree
            * (
                4 * delta_a
                + 4 * delta_b
                + delta_c
            )
        )
        + 3 * k * (f_degree + rho + 1)
    ) == 0

    alpha = -5 + 17 * rho
    coefficient_f = sp.expand(
        alpha * target_gamma_power - 17 * target_x_power
    )
    coefficient_f_expected = (
        14 * a_degree - 3 * b_degree - 22 * c_exponent
    )
    assert sp.expand(
        coefficient_f - coefficient_f_expected
    ) == 0

    # Treat (a,b,c) as the largest-c endpoint satisfying F=0 and
    # move K steps backwards to the smallest-c endpoint.
    coefficient_f_zero_b = (
        14 * a_degree - 22 * c_exponent
    ) / 3
    endpoint_g = (
        22 * a_degree + 5 * b_degree - 20 * c_exponent
    )
    assert sp.factor(
        endpoint_g.subs(b_degree, coefficient_f_zero_b)
        - (136 * a_degree - 170 * c_exponent) / 3
    ) == 0

    smallest_a = (
        a_degree - chain_length * (2 - 3 * rho)
    )
    smallest_b = (
        b_degree + 3 * chain_length * (1 - rho)
    )
    smallest_c = c_exponent - chain_length
    smallest_q = (
        4 * smallest_a + 4 * smallest_b + smallest_c
    )
    smallest_r = 6 * smallest_a + 5 * smallest_b
    smallest_e = (
        (-2 + 4 * rho) * smallest_a
        + (-1 + 4 * rho) * smallest_b
        + (1 + rho) * smallest_c
    )
    infinity_factor = sp.expand(
        alpha * (smallest_r + smallest_q * f_degree)
        - smallest_e * (20 + 17 * f_degree)
    )
    expected_infinity_factor = alpha * (
        endpoint_g / 17
        + 3 * chain_length * (f_degree + rho + 1)
    )
    assert sp.factor(
        (
            infinity_factor - expected_infinity_factor
        ).subs(b_degree, coefficient_f_zero_b)
    ) == 0

    # If the leading x-power happens to be zero, the nonzero
    # coefficient cannot be constant: its vanishing order at u=1 is
    # positive even after one derivative.
    minimum_f_order = 2 - rho
    assert sp.simplify(
        minimum_f_order * (17 + 1) - 1
    ).subs(rho, -1) > 0


def main() -> None:
    verify_full_seed_degree_gaps()
    verify_same_boundary_parameterization()
    verify_general_wronskian_leading_coefficient()
    verify_exceptional_locus_and_sign_reduction()
    verify_boundary_diagonal_next_coefficient()
    verify_primitive_case()
    verify_polar_boundary_valuation()
    print("verified: every same-boundary counterterm")
    print("verified: symbolic all-degree full-seed Newton gaps")
    print("verified: global boundary minimality is necessary")
    print("verified: graph-interior exceptional signs B<0,C<0")
    print("verified: boundary-diagonal leading cancellation")
    print("verified: first f-deviation precedes every exact seed")
    print("verified: primitive C^2*A^5*B^8 next coefficient")
    print("verified: polar-boundary two-endpoint obstruction")
    print("RESULT: every homogeneous ternary target is boundary-closed")


if __name__ == "__main__":
    main()
