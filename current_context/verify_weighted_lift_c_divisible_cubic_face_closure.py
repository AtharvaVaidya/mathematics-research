#!/usr/bin/env python3
"""Verify closure of every C-divisible cubic target face."""

from __future__ import annotations

import sympy as sp


x, y, u, t = sp.symbols("x y u t")


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


def verify_master_monomial_operator() -> None:
    gamma = sp.Function("gamma")(x, u)
    highest_u = x**-5 * u**20 * gamma**17
    cubic_monomials = {
        "A2C": (2, 0, 1),
        "ABC": (1, 1, 1),
        "B2C": (0, 2, 1),
        "AC2": (1, 0, 2),
        "BC2": (0, 1, 2),
        "C3": (0, 0, 3),
    }
    expected_coefficients = {
        "A2C": (24, 6, 0),
        "ABC": (7, -11, -15),
        "B2C": (-10, -28, -30),
        "AC2": (-18, -30, -30),
        "BC2": (-35, -47, -45),
        "C3": (-60, -66, -60),
    }

    for name, (exponent_a, exponent_b, exponent_c) in cubic_monomials.items():
        exponent_x = -2 * exponent_a - exponent_b + exponent_c
        exponent_u = 6 * exponent_a + 5 * exponent_b
        exponent_gamma = 4 * exponent_a + 4 * exponent_b + exponent_c
        highest_pivot = (
            x**exponent_x
            * u**exponent_u
            * gamma**exponent_gamma
        )
        coefficient_x = (
            22 * exponent_a + 5 * exponent_b - 20 * exponent_c
        )
        coefficient_u = (
            14 * exponent_a - 3 * exponent_b - 22 * exponent_c
        )
        coefficient_zero = (
            10 * exponent_a - 5 * exponent_b - 20 * exponent_c
        )
        assert (
            coefficient_x,
            coefficient_u,
            coefficient_zero,
        ) == expected_coefficients[name]
        operator = (
            coefficient_x * x * sp.diff(gamma, x)
            + coefficient_u * u * sp.diff(gamma, u)
            + coefficient_zero * gamma
        )
        assert sp.expand(
            x * jacobian(highest_u, highest_pivot, (x, u))
            - highest_u * highest_pivot * operator / (u * gamma)
        ) == 0


def verify_first_characteristic_block() -> None:
    gamma = sp.Function("gamma")(x, t)
    alpha, beta, chi = sp.symbols("alpha beta chi")
    p5 = -sp.Rational(3, 46)
    q6 = -sp.Rational(5, 92)
    polynomial = alpha * q6**2 * t**2 + beta * p5 * q6 * t + chi * p5**2
    highest_u = x**15 * t**20 * gamma**17
    highest_pivot = x**9 * t**10 * gamma**9 * polynomial
    equation = (
        x * (-10 / t + 17 * sp.diff(polynomial, t) / polynomial)
        * sp.diff(gamma, x)
        - 18 * sp.diff(gamma, t)
        + (-30 / t + 15 * sp.diff(polynomial, t) / polynomial)
        * gamma
    )
    assert sp.factor(
        jacobian(highest_u, highest_pivot, (x, t))
        - highest_u * highest_pivot * equation / (x * gamma)
    ) == 0

    sector_i = sp.symbols("sector_i", integer=True)
    r = -sp.Rational(1, 9) * (5 * sector_i + 15)
    s = sp.Rational(1, 18) * (17 * sector_i + 15)
    formal_gamma = x**sector_i * t**r * polynomial**s
    assert sp.factor(equation.subs(gamma, formal_gamma).doit()) == 0


def verify_resonant_rays_and_obstructions() -> None:
    observed_degree_two: list[tuple[int, int]] = []
    observed_degree_one: list[tuple[int, int]] = []
    for degree in range(1, 900):
        for graph_x_exponent in range(degree + 1):
            sector_i = graph_x_exponent + 2
            sector_j = degree - graph_x_exponent
            if 3 * sector_j == 4 * sector_i:
                observed_degree_two.append((degree, graph_x_exponent))
            if 7 * sector_i == 18 * sector_j + 15:
                observed_degree_one.append((degree, graph_x_exponent))

    assert observed_degree_two == [
        (7 * ray_k - 2, 3 * ray_k - 2) for ray_k in range(1, 129)
    ]
    assert observed_degree_one == [
        (25 * ray_k + 18, 18 * ray_k + 13) for ray_k in range(36)
    ]

    for ray_k in range(1, 30):
        sector_i = 3 * ray_k
        sector_j = 4 * ray_k
        forbidden_coefficient = sp.binomial(sector_j, sector_i - 1)
        assert forbidden_coefficient != 0
        assert sector_j - sector_i + 1 == ray_k + 1
        obstruction_drop = (
            sector_i + sector_j - (1 + ray_k + 1)
        )
        assert obstruction_drop == 6 * ray_k - 2
        assert obstruction_drop < (7 * ray_k - 2) + 4

    for ray_k in range(30):
        sector_i = 18 * ray_k + 15
        sector_j = 7 * ray_k + 5
        exponent_r = -10 * ray_k - 10
        exponent_s = 17 * ray_k + 15
        assert exponent_r + exponent_s == sector_j
        forbidden_coefficient = sp.binomial(exponent_s, sector_j + 1)
        assert forbidden_coefficient != 0
        assert sector_j + 1 < (25 * ray_k + 18) + 4


def verify_abc_fixed_defect() -> None:
    a = -sp.Rational(57, 34)
    gamma_fixed = 1 + a * (u - 1)
    defect = sp.expand(
        7 * x * sp.diff(gamma_fixed, x)
        - 11 * u * sp.diff(gamma_fixed, u)
        - 15 * gamma_fixed
    )
    expected = sp.Rational(741, 17) * x * y + sp.Rational(117, 34)
    assert sp.expand(defect.subs(u, 1 + x * y) - expected) == 0

    for degree in range(2, 200):
        assert -11 * degree - 15 != 0


def verify_second_characteristic_block() -> None:
    gamma = sp.Function("gamma")(x, t)
    mu, nu = sp.symbols("mu nu")
    p5 = -sp.Rational(3, 46)
    q6 = -sp.Rational(5, 92)
    polynomial = mu * q6 * t + nu * p5
    highest_u = x**15 * t**20 * gamma**17
    highest_pivot = x**6 * t**5 * gamma**6 * polynomial
    equation = (
        x * (-35 / t + 17 * sp.diff(polynomial, t) / polynomial)
        * sp.diff(gamma, x)
        - 12 * sp.diff(gamma, t)
        + (-45 / t + 15 * sp.diff(polynomial, t) / polynomial)
        * gamma
    )
    assert sp.factor(
        jacobian(highest_u, highest_pivot, (x, t))
        - highest_u * highest_pivot * equation / (x * gamma)
    ) == 0

    sector_i = sp.symbols("sector_i", integer=True)
    r = -sp.Rational(1, 12) * (35 * sector_i + 45)
    s = sp.Rational(1, 12) * (17 * sector_i + 15)
    formal_gamma = x**sector_i * t**r * polynomial**s
    assert sp.factor(equation.subs(gamma, formal_gamma).doit()) == 0
    assert sp.simplify(r + s) == -(3 * sector_i + 5) / 2

    # Both possible leading exponents are negative for every graph sector I >= 2.
    for sample_i in range(2, 200):
        degree_one_exponent = -sp.Rational(3 * sample_i + 5, 2)
        degree_zero_exponent = -sp.Rational(35 * sample_i + 45, 12)
        assert degree_one_exponent < 0
        assert degree_zero_exponent < 0
        for sample_j in range(200):
            assert -60 * sample_i - 6 * sample_j - 60 < 0


def verify_degree_separation() -> None:
    m = sp.symbols("m", integer=True, positive=True)
    degrees = {
        "A2C": 9 * m + 39,
        "ABC": 9 * m + 38,
        "B2C": 9 * m + 37,
        "AC2": 6 * m + 24,
        "BC2": 6 * m + 23,
        "C3": 3 * m + 9,
    }
    ordered = list(degrees.values())
    for left, right in zip(ordered, ordered[1:]):
        assert sp.simplify(left - right).subs(m, 1) > 0

    for ray_k in range(1, 30):
        ray_m = 7 * ray_k - 2
        assert 6 * ray_k - 2 < ray_m + 4
        assert 6 * ray_k - 2 < 3 * ray_m + 15
        assert 6 * ray_k - 2 < 13 * ray_m + 51
    for ray_k in range(30):
        ray_m = 25 * ray_k + 18
        assert 7 * ray_k + 6 < ray_m + 4
        assert ray_m < ray_m + 4
        assert ray_m < 3 * ray_m + 14
        assert 7 * ray_k + 6 < 13 * ray_m + 51
        assert ray_m < 13 * ray_m + 51


def verify_constant_graphs() -> None:
    a, z0, theta = sp.symbols("a z0 theta", nonzero=True)
    h = a * y + z0 * x
    highest_u = theta * x**32 * y**20 * h**17
    exponent_pairs = [
        (12, 9),
        (11, 9),
        (10, 9),
        (6, 6),
        (5, 6),
        (0, 3),
    ]
    expected_y_coefficients = [6, -26, -58, -60, -92, -126]
    for (exponent_y, exponent_c), expected_y_coefficient in zip(
        exponent_pairs,
        expected_y_coefficients,
    ):
        highest_pivot = y**exponent_y * (x**2 * h) ** exponent_c
        expected = (
            theta
            * x ** (31 + 2 * exponent_c)
            * y ** (19 + exponent_y)
            * h ** (16 + exponent_c)
            * (
                (32 * exponent_y - 42 * exponent_c) * a * y
                + (49 * exponent_y - 60 * exponent_c) * z0 * x
            )
        )
        assert sp.factor(jacobian(highest_u, highest_pivot, (x, y)) - expected) == 0
        assert 32 * exponent_y - 42 * exponent_c == expected_y_coefficient
        assert expected_y_coefficient != 0


def main() -> None:
    verify_master_monomial_operator()
    verify_first_characteristic_block()
    verify_resonant_rays_and_obstructions()
    verify_abc_fixed_defect()
    verify_second_characteristic_block()
    verify_degree_separation()
    verify_constant_graphs()
    print("weighted-lift C-divisible cubic-face closure: exact checks passed")


if __name__ == "__main__":
    main()
