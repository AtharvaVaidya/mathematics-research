#!/usr/bin/env python3
"""Verify the corrected pure-face audit for the quartic theorem."""

from __future__ import annotations

import sympy as sp


def verify_general_pure_first_lower_coefficient() -> None:
    n, c, d, source_i = sp.symbols(
        "n c d I",
        integer=True,
        positive=True,
    )
    source_j = (
        (5 * n - 20 * c + 17 * d) * source_i
        - (5 * n + 20 * c)
        + 15 * d
    ) / (8 * n + 2 * c)

    determinant_u = sp.factor(
        (14 + 16 * source_i)
        * (5 * n + d + (4 * n + c) * source_j)
        - (19 + 16 * source_j)
        * (4 * n + c)
        * (source_i + 1)
    )
    determinant_v = sp.factor(
        (15 + 17 * source_i)
        * (
            5 * n
            + d
            - 1
            + (4 * n + c - 1) * source_j
        )
        - (20 + 17 * source_j)
        * (4 * n + c - 1)
        * (source_i + 1)
    )
    expected_u = (source_i + 1) * (c - d - n)
    expected_v = (
        -(17 * source_i + 15)
        * (c - d - n)
        / (c + 4 * n)
    )
    assert sp.factor(determinant_u - expected_u) == 0
    assert sp.factor(determinant_v - expected_v) == 0

    target_ratio = -sp.Rational(35, 6) * n + sp.Rational(7, 30) * d
    forcing = sp.factor(
        -sp.Rational(70, 3) * determinant_u
        + target_ratio * determinant_v
    )
    expected_forcing = sp.factor(
        -7
        * (c - d - n)
        * (
            100 * source_i * c
            + 17 * source_i * d
            - 25 * source_i * n
            + 100 * c
            + 15 * d
            + 25 * n
        )
        / (30 * (c + 4 * n))
    )
    assert sp.factor(forcing - expected_forcing) == 0


def verify_repaired_and_colliding_faces() -> None:
    source_i, k = sp.symbols(
        "I k",
        integer=True,
        nonnegative=True,
    )

    # Pure B^4 and the pure linear B-ray have nonzero forcing for I>=2.
    omega_b4 = -sp.Rational(35, 6) * (source_i - 1)
    omega_b = -sp.Rational(35, 24) * (source_i - 1)
    for i_value in range(2, 50):
        assert omega_b4.subs(source_i, i_value) != 0
        assert omega_b.subs(source_i, i_value) != 0

    # AB^2*C: a normalized B^3 coefficient cancels the exact forcing.
    determinant_ab2c = 3 * (17 * source_i + 15) / 13
    omega_ab2c = 7 * (21 * source_i + 95) / 65
    cancel_b3 = -7 * (21 * source_i + 95) / (
        15 * (17 * source_i + 15)
    )
    assert sp.factor(
        omega_ab2c + cancel_b3 * determinant_ab2c
    ) == 0
    assert sp.factor(
        cancel_b3.subs(source_i, 13 * k + 6)
        + 7 * (21 * k + 17) / (15 * (17 * k + 9))
    ) == 0
    original_b3_over_ab2c = sp.factor(
        sp.Rational(5, 6)
        * cancel_b3.subs(source_i, 13 * k + 6)
    )
    assert sp.factor(
        original_b3_over_ab2c
        + 7 * (21 * k + 17) / (18 * (17 * k + 9))
    ) == 0

    # A^2*C^2: set the B^2*C coefficient to zero, then a normalized
    # A*B*C coefficient cancels the exact double pole.
    determinant_a2c2 = (17 * source_i + 15) / 5
    omega_a2c2 = 28 * (23 * source_i + 35) / 75
    cancel_abc = -28 * (23 * source_i + 35) / (
        15 * (17 * source_i + 15)
    )
    assert sp.factor(
        omega_a2c2 + cancel_abc * determinant_a2c2
    ) == 0
    assert sp.factor(
        cancel_abc.subs(source_i, 5 * k + 5)
        + 28 * (23 * k + 30) / (15 * (17 * k + 20))
    ) == 0
    original_abc_over_a2c2 = sp.factor(
        sp.Rational(5, 6)
        * cancel_abc.subs(source_i, 5 * k + 5)
    )
    assert sp.factor(
        original_abc_over_a2c2
        + 14 * (23 * k + 30) / (9 * (17 * k + 20))
    ) == 0

    # The omitted B^2*C term has a nonzero t^-3 determinant.
    determinant_b2c = -4 * (17 * source_i + 15) / 5
    for i_value in range(2, 50):
        assert determinant_b2c.subs(source_i, i_value) != 0


def verify_polynomial_solvability_after_tuning() -> None:
    # L_-1 maps C[t] bijectively onto t^-1*C[t] on both problematic
    # faces: every diagonal multiplier is nonzero.
    for n_value, c_value, d_value in ((3, 1, 1), (2, 2, 2)):
        derivative_weight = 8 * n_value + 2 * c_value
        pole_weight = 10 * n_value + 2 * d_value
        for output_degree in range(-1, 100):
            multiplier = (
                derivative_weight * (output_degree + 1)
                + pole_weight
            )
            assert multiplier > 0

    # Removing one C and retaining the same n is the unique
    # degree-lower target move with maximal-x loss I+1.
    for delta_n in range(-4, 5):
        for delta_c in range(-4, 5):
            if delta_n + delta_c < 1:
                continue
            if 4 * delta_n + delta_c == 1:
                assert (delta_n, delta_c) == (0, 1)


def verify_timing() -> None:
    k = sp.symbols("k", integer=True, nonnegative=True)

    # The cancelling B^3 and ABC terms occur at the same scalar drop
    # m+4 as the exact first-lower seed.
    m_ab2c = 19 * k + 6
    degree_ab2c = 13 * m_ab2c + 55
    degree_b3 = 12 * m_ab2c + 51
    assert sp.expand(degree_ab2c - degree_b3) == m_ab2c + 4

    m_a2c2 = 6 * k + 3
    degree_a2c2 = 10 * m_a2c2 + 42
    degree_abc = 9 * m_a2c2 + 38
    assert sp.expand(degree_a2c2 - degree_abc) == m_a2c2 + 4

    # B^4 is safely separated from every cubic target face.
    m = sp.symbols("m", integer=True, positive=True)
    assert sp.expand(
        (16 * m + 68) - (13 * m + 57) - (m + 4)
    ) == 2 * m + 7
    assert sp.expand((5 * m + 15) - (m + 4)) == 4 * m + 11


def main() -> None:
    verify_general_pure_first_lower_coefficient()
    verify_repaired_and_colliding_faces()
    verify_polynomial_solvability_after_tuning()
    verify_timing()
    print("verified: general C-divisible pure first-lower coefficient")
    print("verified: pure B^4 and linear B are reclosed")
    print("verified: exact B^3 and ABC cancellation parameters")
    print("verified: tuned x^-1 equations admit polynomial coefficients")
    print("RESULT: two quartic rays and inherited lower-tier chains remain open")


if __name__ == "__main__":
    main()
