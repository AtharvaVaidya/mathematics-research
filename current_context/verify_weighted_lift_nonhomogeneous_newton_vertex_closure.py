#!/usr/bin/env python3
"""Verify the nonhomogeneous Newton-vertex closure identities."""

from __future__ import annotations

import sympy as sp


def invariants(
    a: sp.Expr,
    b: sp.Expr,
    c: sp.Expr,
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    beta = -2 * a - b + c
    height = 6 * a + 5 * b
    gamma_power = 4 * a + 4 * b + c
    return beta, height, gamma_power


def verify_regular_filtration() -> None:
    a, b, c, L, r = sp.symbols(
        "a b c L r",
        integer=True,
        nonnegative=True,
    )
    beta, height, gamma_power = invariants(a, b, c)
    assert sp.expand(gamma_power - height - beta) == 0

    degree = height + gamma_power * L
    lower_degree = height - r + (gamma_power - r) * L
    assert sp.expand(degree - lower_degree - r * (L + 1)) == 0

    coefficient_L = -5 * gamma_power - 17 * beta
    coefficient_constant = -5 * height - 20 * beta
    assert sp.expand(
        coefficient_L - (14 * a - 3 * b - 22 * c)
    ) == 0
    assert sp.expand(
        coefficient_constant - (10 * a - 5 * b - 20 * c)
    ) == 0
    assert sp.expand(
        17 * coefficient_constant
        - 15 * coefficient_L
        + 10 * gamma_power
    ) == 0


def verify_polar_endpoints() -> None:
    rho, L = sp.symbols("rho L", integer=True)
    q_min, q_max = sp.symbols(
        "q_min q_max",
        integer=True,
        positive=True,
    )
    alpha = -5 + 17 * rho
    E = alpha * q_min / 17
    degree_h = 20 + 17 * L
    degree_v = (L + rho + 1) * q_max - E
    infinity_coefficient = sp.expand(
        alpha * degree_v - E * degree_h
    )
    expected = alpha * (
        (L + rho + 1) * (q_max - q_min)
        + sp.Rational(2, 17) * q_min
    )
    assert sp.factor(infinity_coefficient - expected) == 0

    # The bracket in the endpoint coefficient is positive under the
    # graph constraints L+rho+1>=3 and q_max>=q_min>0.
    for rho_value in range(-12, 0):
        for L_value in range(-rho_value + 2, -rho_value + 15):
            assert L_value + rho_value + 1 >= 3
            for q_min_value in range(1, 12):
                for q_max_value in range(q_min_value, 14):
                    bracket = (
                        (L_value + rho_value + 1)
                        * (q_max_value - q_min_value)
                        + sp.Rational(2, 17) * q_min_value
                    )
                    assert bracket > 0


def verify_remove_one_c() -> None:
    a, b, c, rho = sp.symbols(
        "a b c rho",
        integer=True,
    )
    top = invariants(a, b, c)
    lower = invariants(a - 1, b + 1, c - 1)
    assert sp.expand(lower[0] - top[0]) == 0
    assert sp.expand(lower[1] - top[1]) == -1
    assert sp.expand(lower[2] - top[2]) == -1
    top_E = top[0] + rho * top[2]
    lower_E = lower[0] + rho * lower[2]
    assert sp.expand(lower_E - top_E) == -rho

    examples = (
        ((1, 0, 1), (-8, -10)),
        ((1, 1, 1), (-11, -15)),
        ((1, 2, 1), (-14, -20)),
        ((2, 0, 2), (-16, -20)),
    )
    for exponents, expected in examples:
        beta, height, gamma_power = invariants(*exponents)
        coefficient_L = -5 * gamma_power - 17 * beta
        coefficient_constant = -5 * height - 20 * beta
        assert (coefficient_L, coefficient_constant) == expected
        assert coefficient_L < 0
        assert coefficient_constant < 0


def verify_cusp_kernel() -> None:
    da, db, dc = sp.symbols("da db dc", integer=True)
    matrix = sp.Matrix(
        [
            [-2, -1, 1],
            [6, 5, 0],
        ]
    )
    kernel = matrix.nullspace()
    assert len(kernel) == 1
    primitive = kernel[0]
    denominator = sp.ilcm(
        *[sp.denom(coefficient) for coefficient in primitive]
    )
    integer_vector = tuple(
        int(coefficient * denominator)
        for coefficient in primitive
    )
    assert integer_vector == (5, -6, 4)

    rho = sp.symbols("rho", integer=True, negative=True)
    beta_delta = -2 * da - db + dc
    q_delta = 4 * da + 4 * db + dc
    E_delta = beta_delta + rho * q_delta
    polar_matrix = sp.Matrix(
        [
            [
                sp.diff(E_delta, variable)
                for variable in (da, db, dc)
            ],
            [
                sp.diff(q_delta, variable)
                for variable in (da, db, dc)
            ],
        ]
    )
    polar_kernel = polar_matrix.nullspace()
    assert len(polar_kernel) == 1
    normalized = sp.simplify(
        polar_kernel[0] / polar_kernel[0][0] * 5
    )
    assert tuple(normalized) == (5, -6, 4)

    # The primitive relation really equates the three boundary
    # exponent components (x-order, u-power, f-power).
    C = sp.Matrix([1, 0, 1])
    B = sp.Matrix([-1, 5, 4])
    A = sp.Matrix([-2, 6, 4])
    assert 5 * A + 4 * C == 6 * B


def verify_degree_eight_cutoff() -> None:
    seen: dict[tuple[int, int], tuple[int, int, int]] = {}
    for total_degree in range(9):
        for a in range(total_degree + 1):
            for b in range(total_degree - a + 1):
                c = total_degree - a - b
                beta, height, _ = invariants(a, b, c)
                key = (int(beta), int(height))
                assert key not in seen
                seen[key] = (a, b, c)

    # Degree nine is sharp: B^6 and A^5 C^4 are the primitive pair.
    beta_b6, height_b6, _ = invariants(0, 6, 0)
    beta_a5c4, height_a5c4, _ = invariants(5, 0, 4)
    assert (beta_b6, height_b6) == (
        beta_a5c4,
        height_a5c4,
    )
    assert sum((0, 6, 0)) == 6
    assert sum((5, 0, 4)) == 9


def verify_first_coordinate_scope() -> None:
    # At a regular boundary, degree <=2 perturbations are strictly
    # later than U, whereas cubic A^3 precedes and A^2 B ties.
    alpha_regular = -5
    degree_two_betas = []
    for total_degree in range(1, 3):
        for a in range(total_degree + 1):
            for b in range(total_degree - a + 1):
                c = total_degree - a - b
                degree_two_betas.append(invariants(a, b, c)[0])
    assert min(degree_two_betas) == -4
    assert min(degree_two_betas) > alpha_regular
    assert invariants(3, 0, 0)[0] == -6
    assert invariants(2, 1, 0)[0] == -5

    # If A^3 precedes U, its regular-boundary Wronskian with each
    # remove-one-C top monomial is already nonzero.
    L = sp.symbols("L", integer=True, positive=True)
    first_alpha = -6
    first_degree = 18 + 12 * L
    chain_tops = (
        ((1, 0, 1), -18),
        ((1, 1, 1), -30),
        ((1, 2, 1), -42),
        ((2, 0, 2), -36),
    )
    for exponents, expected_factor in chain_tops:
        beta, height, q = invariants(*exponents)
        target_degree = height + q * L
        wronskian_coefficient = sp.expand(
            first_alpha * target_degree - beta * first_degree
        )
        assert sp.factor(
            wronskian_coefficient - expected_factor * (L + 1)
        ) == 0

    # If A^3 is absent, A^2 B is the only cubic term tied with U in
    # x-order, and it is separated in u-degree by 3+5L.
    degree_u = 20 + 17 * L
    degree_a2b = 17 + 12 * L
    assert sp.expand(degree_u - degree_a2b) == 3 + 5 * L
    assert sp.expand((3 + 5 * L) - L) == 3 + 4 * L

    # At a pole boundary, every monomial of degree <=3 is later than
    # U.  Audit a representative finite range of negative rho; the
    # symbolic difference is affine and only grows as rho decreases.
    for rho in range(-20, 0):
        alpha = -5 + 17 * rho
        for total_degree in range(1, 4):
            for a in range(total_degree + 1):
                for b in range(total_degree - a + 1):
                    c = total_degree - a - b
                    beta, _, q = invariants(a, b, c)
                    assert beta + rho * q > alpha


def main() -> None:
    verify_regular_filtration()
    verify_polar_endpoints()
    verify_remove_one_c()
    verify_cusp_kernel()
    verify_degree_eight_cutoff()
    verify_first_coordinate_scope()
    print("verified: regular nonhomogeneous Newton-vertex filtration")
    print("verified: polar two-endpoint Wronskian separation")
    print("verified: all-degree remove-one-C chains")
    print("verified: primitive cusp kernel (5,-6,4)")
    print("verified: arbitrary nonhomogeneous target cutoff degree eight")
    print("verified: cubic first-coordinate bifiltration on four chains")


if __name__ == "__main__":
    main()
