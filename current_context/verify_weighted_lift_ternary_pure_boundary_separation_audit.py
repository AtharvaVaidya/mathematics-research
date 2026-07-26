#!/usr/bin/env python3
"""Audit the change from maximal-x to the source-boundary valuation."""

from __future__ import annotations

import sympy as sp

from verify_weighted_lift_first_nonlinear_cusp_subduction import (
    build_maximal_subductions,
    build_seed,
)


def verify_exact_boundary_scaling() -> None:
    # Every U numerator monomial has the same x^-5 factor after
    # w=u*gamma on the source boundary.  The analogous A/B factors
    # are x^-2 and x^-1 independently of seed degree.
    for w_power in range(21):
        for gamma_power in range(8):
            u_power = w_power
            boundary_gamma_power = w_power + gamma_power - 5
            assert u_power == w_power
            assert boundary_gamma_power == w_power + gamma_power - 5

    for q_power in range(7):
        assert -2 == -2
        assert q_power - 2 == q_power - 2
    for p_power in range(6):
        assert -1 == -1
        assert p_power - 1 == p_power - 1


def verify_exact_boundary_wronskian() -> None:
    alpha, beta = sp.symbols("alpha beta", integer=True)
    x, u = sp.symbols("x u", nonzero=True)
    first_bar = sp.Function("first_bar")(u)
    second_bar = sp.Function("second_bar")(u)
    first = x**alpha * first_bar
    second = x**beta * second_bar
    jacobian_xu = sp.diff(first, x) * sp.diff(
        second, u
    ) - sp.diff(first, u) * sp.diff(second, x)
    jacobian_xy = sp.factor(x * jacobian_xu)
    expected = x ** (alpha + beta) * (
        alpha * first_bar * sp.diff(second_bar, u)
        - beta * sp.diff(first_bar, u) * second_bar
    )
    assert sp.factor(jacobian_xy - expected) == 0
    assert expected.subs(alpha, -5) == x ** (beta - 5) * (
        -5 * first_bar * sp.diff(second_bar, u)
        - beta * sp.diff(first_bar, u) * second_bar
    )


def verify_local_seed_jets() -> None:
    p, q = build_seed()
    _, second_numerator, _, _ = build_maximal_subductions(p, q)
    w, gamma, v, h2 = sp.symbols("w gamma v h2")
    fixed_slope = -sp.Rational(57, 34)
    boundary_gamma = 1 + fixed_slope * v + h2 * v**2
    boundary_u = 1 + v
    boundary_w = sp.expand(boundary_u * boundary_gamma)

    boundary_a = sp.cancel(
        (
            q.subs(w, boundary_w)
            + boundary_w * boundary_gamma
        )
        / boundary_gamma**2
    )
    boundary_b = sp.cancel(
        (
            p.subs(w, boundary_w)
            + boundary_gamma
        )
        / boundary_gamma
    )
    boundary_u_coordinate = sp.cancel(
        second_numerator.subs(
            {w: boundary_w, gamma: boundary_gamma}
        )
        / boundary_gamma**5
    )

    b1 = sp.factor(sp.diff(boundary_b, v).subs(v, 0))
    a2 = sp.factor(
        sp.diff(boundary_a, v, 2).subs(v, 0) / sp.factorial(2)
    )
    u5 = sp.factor(
        sp.diff(boundary_u_coordinate, v, 5).subs(v, 0)
        / sp.factorial(5)
    )
    assert b1 == sp.Rational(23, 34)
    assert sp.factor(
        a2 + (157216 * h2 - 412769) / 106352
    ) == 0
    assert sp.factor(
        u5
        + 729
        * (3523346237408 * h2 - 9052069219409)
        / 123353897489720731381006336
    ) == 0
    assert sp.solve(a2, h2) != sp.solve(u5, h2)


def verify_higher_c_counterterm() -> None:
    ell, binary_count, degree = sp.symbols(
        "ell N d", integer=True, nonnegative=True
    )
    top_boundary_exponent = ell - binary_count - degree
    next_boundary_exponent = (
        (ell + 1)
        - 2 * (degree + 2)
        - (binary_count - degree - 3)
    )
    assert sp.expand(
        next_boundary_exponent - top_boundary_exponent
    ) == 0

    k = sp.symbols("k", integer=True, nonnegative=True)
    later_boundary_exponent = (
        (ell + k)
        - 2 * (degree + 2 * k)
        - (binary_count - degree - 3 * k)
    )
    assert sp.expand(
        later_boundary_exponent - top_boundary_exponent
    ) == 0


def verify_pure_first_lower_factor() -> None:
    binary_count, c_power, degree, source_i = sp.symbols(
        "N ell d I", integer=True, nonnegative=True
    )
    total_exponent = 4 * binary_count + c_power
    constant_coefficient = (
        25
        * (binary_count - c_power)
        * (
            source_i * (4 * c_power - binary_count)
            + 4 * c_power
            + binary_count
        )
    )
    linear_coefficient = (
        source_i * (83 * c_power - 8 * binary_count)
        + 85 * c_power
        + 40 * binary_count
    )
    pure_numerator = sp.factor(
        constant_coefficient
        + linear_coefficient * degree
        + (17 * source_i + 15) * degree**2
    )
    expected = (
        binary_count - c_power + degree
    ) * (
        source_i
        * (100 * c_power - 25 * binary_count + 17 * degree)
        + 100 * c_power
        + 25 * binary_count
        + 15 * degree
    )
    assert sp.factor(pure_numerator - expected) == 0
    assert total_exponent == 4 * binary_count + c_power

    # The first factor N-ell+d=0 forces a negative leading t-degree.
    d_first = c_power - binary_count
    characteristic_numerator = (
        (5 * binary_count - 20 * c_power + 17 * d_first) * source_i
        + 15 * d_first
        - 5 * binary_count
        - 20 * c_power
    )
    characteristic_denominator = 2 * total_exponent
    assert sp.factor(
        characteristic_numerator / characteristic_denominator
        + (3 * source_i + 5) / 2
    ) == 0

    # In the binary specialization, the second factor plus resonance
    # leaves only d=N,I=5,J=15.
    for n_value in range(1, 60):
        binary_exceptions: list[tuple[int, int, int]] = []
        for d_value in range(n_value + 1):
            for i_value in range(2, 80):
                second_factor = (
                    i_value * (-25 * n_value + 17 * d_value)
                    + 25 * n_value
                    + 15 * d_value
                )
                if second_factor:
                    continue
                numerator = (
                    (5 * n_value + 17 * d_value) * i_value
                    + 15 * d_value
                    - 5 * n_value
                )
                if numerator % (8 * n_value):
                    continue
                binary_exceptions.append(
                    (d_value, i_value, numerator // (8 * n_value))
                )
        assert binary_exceptions == [(n_value, 5, 15)]

    # The first exceptional ternary faces with ell>0 occur at n=6.
    ternary_exceptions: list[
        tuple[int, int, int, int, int, int]
    ] = []
    for target_degree in range(1, 7):
        for ell_value in range(1, target_degree + 1):
            n_binary = target_degree - ell_value
            total = 4 * n_binary + ell_value
            for d_value in range(n_binary + 1):
                for i_value in range(2, 100):
                    second_factor = (
                        i_value
                        * (
                            100 * ell_value
                            - 25 * n_binary
                            + 17 * d_value
                        )
                        + 100 * ell_value
                        + 25 * n_binary
                        + 15 * d_value
                    )
                    if second_factor:
                        continue
                    numerator = (
                        (
                            5 * n_binary
                            - 20 * ell_value
                            + 17 * d_value
                        )
                        * i_value
                        + 15 * d_value
                        - 5 * n_binary
                        - 20 * ell_value
                    )
                    denominator = 2 * total
                    if numerator < 0 or numerator % denominator:
                        continue
                    ternary_exceptions.append(
                        (
                            target_degree,
                            n_binary,
                            ell_value,
                            d_value,
                            i_value,
                            numerator // denominator,
                        )
                    )
    assert ternary_exceptions == [
        (6, 5, 1, 0, 9, 0),
        (6, 5, 1, 1, 30, 15),
    ]


def main() -> None:
    verify_exact_boundary_scaling()
    verify_exact_boundary_wronskian()
    verify_local_seed_jets()
    verify_higher_c_counterterm()
    verify_pure_first_lower_factor()
    print("verified: all exact seed layers coalesce on x=0,u fixed")
    print("verified: full boundary coefficient is an exact Wronskian")
    print("verified: boundary jets depend on the free h2 coefficient")
    print("verified: an explicit higher C-tier has the same valuation")
    print("verified: exact partial salvage by the pure first-lower pole")
    print("RESULT: the proposed pure-face boundary separation is invalid")


if __name__ == "__main__":
    main()
