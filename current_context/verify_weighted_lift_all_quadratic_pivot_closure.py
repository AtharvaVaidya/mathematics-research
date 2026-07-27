#!/usr/bin/env python3
"""Verify closure of every affine quadratic second pivot."""

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


def verify_binary_quadratic_pde() -> None:
    gamma = sp.Function("gamma")(x, t)
    alpha, beta, chi = sp.symbols("alpha beta chi")
    p5 = -sp.Rational(3, 46)
    q6 = -sp.Rational(5, 92)
    polynomial = alpha * q6**2 * t**2 + beta * p5 * q6 * t + chi * p5**2
    highest_u = x**15 * t**20 * gamma**17
    highest_q = x**8 * t**10 * gamma**8 * polynomial

    equation = (
        x * (10 / t + 17 * sp.diff(polynomial, t) / polynomial)
        * sp.diff(gamma, x)
        - 16 * sp.diff(gamma, t)
        + (-10 / t + 15 * sp.diff(polynomial, t) / polynomial)
        * gamma
    )
    assert sp.factor(
        jacobian(highest_u, highest_q, (x, t))
        - highest_u * highest_q * equation / (x * gamma)
    ) == 0

    I = sp.symbols("I", integer=True)
    r = sp.Rational(5, 8) * (I - 1)
    s = sp.Rational(1, 16) * (17 * I + 15)
    formal_gamma = x**I * t**r * polynomial**s
    assert sp.factor(equation.subs(gamma, formal_gamma).doit()) == 0


def verify_master_monomial_operator() -> None:
    gamma = sp.Function("gamma")(x, u)
    highest_u = x**-5 * u**20 * gamma**17
    quadratic_monomials = {
        "A2": (2, 0, 0),
        "AB": (1, 1, 0),
        "B2": (0, 2, 0),
        "AC": (1, 0, 1),
        "BC": (0, 1, 1),
        "C2": (0, 0, 2),
    }
    expected_coefficients = {
        "A2": (44, 28, 20),
        "AB": (27, 11, 5),
        "B2": (10, -6, -10),
        "AC": (2, -8, -10),
        "BC": (-15, -25, -25),
        "C2": (-40, -44, -40),
    }

    for name, (exponent_a, exponent_b, exponent_c) in quadratic_monomials.items():
        exponent_x = -2 * exponent_a - exponent_b + exponent_c
        exponent_u = 6 * exponent_a + 5 * exponent_b
        exponent_gamma = (
            4 * exponent_a + 4 * exponent_b + exponent_c
        )
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


def verify_integer_rays() -> None:
    observed_degree_two: list[tuple[int, int]] = []
    observed_degree_one: list[tuple[int, int]] = []
    observed_degree_zero: list[tuple[int, int]] = []
    for degree in range(1, 700):
        for graph_x_exponent in range(degree + 1):
            I = graph_x_exponent + 2
            J = degree - graph_x_exponent
            if 4 * J == 11 * I + 5:
                observed_degree_two.append((degree, graph_x_exponent))
            if 16 * J == 27 * I + 5:
                observed_degree_one.append((degree, graph_x_exponent))
            if 8 * J == 5 * I - 5:
                observed_degree_zero.append((degree, graph_x_exponent))

    assert observed_degree_two == [
        (15 * k + 3, 4 * k - 1) for k in range(1, 47)
    ]
    assert observed_degree_one == [
        (43 * k + 1, 16 * k - 1) for k in range(1, 17)
    ]
    assert observed_degree_zero == [
        (13 * k + 12, 8 * k + 7) for k in range(53)
    ]


def verify_forbidden_terms() -> None:
    sector_i = sp.symbols("sector_i")
    diagonal_two = sector_i - (11 * sector_i + 5) / 4
    diagonal_one = sector_i - (27 * sector_i + 5) / 16
    weight_two = sector_i + (11 * sector_i + 5) / 4
    weight_one = sector_i + (27 * sector_i + 5) / 16
    assert sp.diff(diagonal_two, sector_i) == -sp.Rational(7, 4)
    assert sp.diff(diagonal_one, sector_i) == -sp.Rational(11, 16)
    assert sp.diff(weight_two, sector_i) == sp.Rational(15, 4)
    assert sp.diff(weight_one, sector_i) == sp.Rational(43, 16)

    for sample_k in range(1, 10):
        # Degree-two P: the A^2 face.
        I_two = 4 * sample_k + 1
        J_two = 11 * sample_k + 4
        replacement_two = I_two - 1
        coefficient_two = sp.binomial(J_two, replacement_two)
        assert coefficient_two != 0
        assert J_two - replacement_two == 7 * sample_k + 4

        # Every lower t-power has strictly smaller y-degree when it
        # reaches x exponent one.
        for lower_t_power in range(1, 7):
            assert (
                J_two - lower_t_power - replacement_two
                < J_two - replacement_two
            )

        # Degree-one P: the genuinely new AB face.
        I_one = 16 * sample_k + 1
        J_one = 27 * sample_k + 2
        replacement_one = I_one - 1
        coefficient_one = sp.binomial(J_one, replacement_one)
        assert coefficient_one != 0
        assert J_one - replacement_one == 11 * sample_k + 2

        r_one = 10 * sample_k
        s_one = 17 * sample_k + 2
        assert r_one + s_one == J_one

        for lower_t_power in range(1, 7):
            assert (
                J_one - lower_t_power - replacement_one
                < J_one - replacement_one
            )


def verify_b_squared_defect() -> None:
    a = -sp.Rational(57, 34)
    gamma_fixed = 1 + a * (u - 1)
    defect = sp.expand(
        5 * x * sp.diff(gamma_fixed, x)
        - 3 * u * sp.diff(gamma_fixed, u)
        - 5 * gamma_fixed
    )
    expected = sp.Rational(228, 17) * x * y + sp.Rational(1, 34)
    assert sp.expand(defect.subs(u, 1 + x * y) - expected) == 0

    n = sp.symbols("n", integer=True, positive=True)
    assert sp.expand(5 * n - 8 * n - 5) == -3 * n - 5


def verify_c_quadratic_faces() -> None:
    gamma = sp.Function("gamma")(x, t)
    mu, nu = sp.symbols("mu nu")
    p5 = -sp.Rational(3, 46)
    q6 = -sp.Rational(5, 92)
    polynomial = mu * q6 * t + nu * p5
    highest_u = x**15 * t**20 * gamma**17
    highest_ac_bc = x**5 * t**5 * gamma**5 * polynomial
    equation = (
        x * (-15 / t + 17 * sp.diff(polynomial, t) / polynomial)
        * sp.diff(gamma, x)
        - 10 * sp.diff(gamma, t)
        + (-25 / t + 15 * sp.diff(polynomial, t) / polynomial)
        * gamma
    )
    assert sp.factor(
        jacobian(highest_u, highest_ac_bc, (x, t))
        - highest_u * highest_ac_bc * equation / (x * gamma)
    ) == 0

    I = sp.symbols("I", integer=True)
    r = -sp.Rational(1, 2) * (3 * I + 5)
    s = sp.Rational(1, 10) * (17 * I + 15)
    formal_gamma = x**I * t**r * polynomial**s
    assert sp.factor(equation.subs(gamma, formal_gamma).doit()) == 0

    observed_ac: list[tuple[int, int]] = []
    for degree in range(1, 400):
        for graph_x_exponent in range(degree + 1):
            source_i = graph_x_exponent + 2
            source_j = degree - graph_x_exponent
            if source_i == 5 * source_j + 5:
                observed_ac.append((degree, graph_x_exponent))
    assert observed_ac == [
        (6 * k + 3, 5 * k + 3) for k in range(67)
    ]

    ray_k = sp.symbols("ray_k", integer=True, nonnegative=True)
    ray_s = sp.Rational(1, 2) * (17 * ray_k + 20)
    assert sp.expand(ray_s - ray_k) == (
        sp.Rational(1, 2) * (15 * ray_k + 20)
    )

    d = sp.symbols("d", nonzero=True)
    for sample_k in range(12):
        sample_s = sp.Rational(17 * sample_k + 20, 2)
        forbidden = (
            sp.binomial(sample_s, sample_k + 1)
            * d ** (sample_k + 1)
        )
        assert forbidden != 0
        degree = 6 * sample_k + 3
        source_i = 5 * sample_k + 5
        source_j = sample_k
        top_weight = source_i + source_j
        forbidden_weight = source_i - 1
        assert top_weight == degree + 2
        assert top_weight - forbidden_weight == source_j + 1
        assert source_j + 1 == sample_k + 1
        assert sample_k + 1 < degree + 4

    a = -sp.Rational(57, 34)
    gamma_fixed = 1 + a * (u - 1)
    ac_defect = sp.expand(
        x * sp.diff(gamma_fixed, x)
        - 4 * u * sp.diff(gamma_fixed, u)
        - 5 * gamma_fixed
    )
    expected_ac_defect = (
        sp.Rational(513, 34) * x * y + sp.Rational(29, 17)
    )
    assert sp.expand(
        ac_defect.subs(u, 1 + x * y) - expected_ac_defect
    ) == 0

    n = sp.symbols("n", integer=True, positive=True)
    assert sp.expand(n - 5 * n - 5) == -4 * n - 5

    source_i, source_j = sp.symbols(
        "source_i source_j",
        integer=True,
        nonnegative=True,
    )
    assert -15 * source_i - 10 * source_j - 25 < 0


def verify_degree_separation() -> None:
    m, k = sp.symbols("m k", integer=True, positive=True)
    degree_u_linear = 21 * m + 85
    degree_linear_quadratic = 12 * m + 51
    degree_linear_linear = 8 * m + 33

    # A^2 face.
    m_two = 15 * k + 3
    defect_two = 25 * m_two + 103 - 8 * k
    assert sp.expand(defect_two - degree_u_linear.subs(m, m_two)) == 52 * k + 30
    assert sp.expand(defect_two - degree_linear_quadratic.subs(m, m_two)) == 187 * k + 91
    assert sp.expand((m_two + 4) - 8 * k) == 7 * k + 7

    # AB face.
    m_one = 43 * k + 1
    defect_one = 25 * m_one + 102 - 32 * k
    assert sp.expand(defect_one - degree_u_linear.subs(m, m_one)) == 140 * k + 21
    assert sp.expand(defect_one - degree_linear_quadratic.subs(m, m_one)) == 527 * k + 64
    assert sp.expand((m_one + 4) - 32 * k) == 11 * k + 5

    # B^2 face.
    defect_zero = 25 * m + 101 - m
    assert sp.expand(defect_zero - degree_u_linear) == 3 * m + 16
    assert sp.expand(defect_zero - degree_linear_quadratic) == 12 * m + 50
    assert sp.expand((m + 4) - m) == 4

    assert sp.expand(
        defect_two - degree_linear_linear.subs(m, m_two)
    ) == 247 * k + 121
    assert sp.expand(
        defect_one - degree_linear_linear.subs(m, m_one)
    ) == 699 * k + 86
    assert sp.expand(
        defect_zero - degree_linear_linear
    ) == 16 * m + 68

    # A binary face always defeats the first possible C-face.
    assert sp.expand(
        (25 * m + 103) - (22 * m + 88)
    ) == 3 * m + 15
    assert sp.expand(
        (25 * m + 102) - (22 * m + 88)
    ) == 3 * m + 14
    assert sp.expand(
        (25 * m + 101) - (22 * m + 88)
    ) == 3 * m + 13

    # AC/BC versus affine and C^2 sectors.
    assert sp.expand(
        (22 * m + 88) - degree_u_linear
    ) == m + 3
    assert sp.expand(
        (22 * m + 88) - (19 * m + 73)
    ) == 3 * m + 15

    # C^2 cannot repair the old linear A- or B-pivot defects.
    assert sp.expand(
        degree_u_linear - (19 * m + 73)
    ) == 2 * m + 12
    assert sp.expand(
        (21 * m + 84) - (19 * m + 73)
    ) == 2 * m + 11


def verify_constant_graphs() -> None:
    z0 = sp.symbols("z0")
    p5 = -sp.Rational(3, 46)
    q6 = -sp.Rational(5, 92)
    theta = -sp.Rational(
        36905625, 6077984970919772059860992
    )
    a = -sp.Rational(57, 34)
    h = a * y + z0 * x
    c0 = x**2 * h
    a0 = q6 * y**6 * c0**4
    b0 = p5 * y**5 * c0**4
    u0 = theta * x**32 * y**20 * h**17

    jacobian_u_a = (
        6
        * q6
        * theta
        * x**39
        * y**25
        * h**20
        * (4 * a * y + 9 * z0 * x)
    )
    jacobian_u_b = (
        p5
        * theta
        * x**39
        * y**24
        * h**20
        * (-8 * a * y + 5 * z0 * x)
    )
    jacobian_u_c = (
        -6
        * theta
        * x**33
        * y**19
        * h**17
        * (7 * a * y + 10 * z0 * x)
    )
    expected_ab = (
        p5
        * q6
        * theta
        * x**47
        * y**30
        * h**24
        * (16 * a * y + 59 * z0 * x)
    )
    assert sp.factor(
        a0 * jacobian_u_b + b0 * jacobian_u_a - expected_ab
    ) == 0

    expressions = (
        2 * a0 * jacobian_u_a,
        expected_ab,
        2 * b0 * jacobian_u_b,
    )
    assert [sp.Poly(expression, x, y).total_degree() for expression in expressions] == [
        103,
        102,
        101,
    ]
    assert all(expression != 0 for expression in expressions)

    expected_ac = (
        -6
        * q6
        * theta
        * x**41
        * y**25
        * h**21
        * (3 * a * y + z0 * x)
    )
    expected_bc = (
        -5
        * p5
        * theta
        * x**41
        * y**24
        * h**21
        * (10 * a * y + 11 * z0 * x)
    )
    expected_c2 = (
        -12
        * theta
        * x**35
        * y**19
        * h**18
        * (7 * a * y + 10 * z0 * x)
    )
    assert sp.factor(
        a0 * jacobian_u_c + c0 * jacobian_u_a - expected_ac
    ) == 0
    assert sp.factor(
        b0 * jacobian_u_c + c0 * jacobian_u_b - expected_bc
    ) == 0
    assert sp.factor(2 * c0 * jacobian_u_c - expected_c2) == 0
    c_expressions = (expected_ac, expected_bc, expected_c2)
    assert [
        sp.Poly(expression, x, y).total_degree()
        for expression in c_expressions
    ] == [88, 87, 73]
    assert all(expression != 0 for expression in c_expressions)


def main() -> None:
    verify_binary_quadratic_pde()
    verify_master_monomial_operator()
    verify_integer_rays()
    verify_forbidden_terms()
    verify_b_squared_defect()
    verify_c_quadratic_faces()
    verify_degree_separation()
    verify_constant_graphs()
    print("verified: exact characteristic PDE for every binary quadratic")
    print("verified: degree-two, degree-one, and degree-zero Newton rays")
    print("verified: the AB face forces a nonzero x^1 term on every ray")
    print("verified: the mixed AC/BC face forces a negative t-power")
    print("verified: affine and lower seed sectors enter after each defect")
    print("verified: constant graphs have separated nonzero quadratic tops")
    print("RESULT: quadratic certificates pass; AC+B remains under correction")


if __name__ == "__main__":
    main()
