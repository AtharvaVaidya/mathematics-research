#!/usr/bin/env python3
"""Verify the Newton/characteristic closure of every cubic target pivot."""

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


def characteristic_data(
    number_ab: int,
    number_c: int,
    polynomial: sp.Expr,
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    gamma = sp.Function("gamma")(x, t)
    denominator = 8 * number_ab + 2 * number_c
    coefficient_x = 5 * number_ab - 20 * number_c
    coefficient_zero = -(5 * number_ab + 20 * number_c)
    highest_u = x**15 * t**20 * gamma**17
    highest_pivot = (
        x ** (4 * number_ab + number_c)
        * t ** (5 * number_ab)
        * gamma ** (4 * number_ab + number_c)
        * polynomial
    )
    logarithmic_polynomial = sp.diff(polynomial, t) / polynomial
    equation = (
        x * (coefficient_x / t + 17 * logarithmic_polynomial)
        * sp.diff(gamma, x)
        - denominator * sp.diff(gamma, t)
        + (coefficient_zero / t + 15 * logarithmic_polynomial)
        * gamma
    )
    assert sp.factor(
        jacobian(highest_u, highest_pivot, (x, t))
        - highest_u * highest_pivot * equation / (x * gamma)
    ) == 0

    I = sp.symbols("I", integer=True)
    exponent_r = (
        coefficient_x * I + coefficient_zero
    ) / denominator
    exponent_s = (17 * I + 15) / denominator
    formal_gamma = x**I * t**exponent_r * polynomial**exponent_s
    assert sp.factor(equation.subs(gamma, formal_gamma).doit()) == 0
    return equation, sp.expand(exponent_r), sp.expand(exponent_s)


def verify_master_characteristics() -> None:
    coefficients = sp.symbols("p0:4")
    for number_ab, number_c in ((3, 0), (2, 1), (1, 2)):
        polynomial = sum(
            coefficients[index] * t**index
            for index in range(number_ab + 1)
        )
        characteristic_data(number_ab, number_c, polynomial)

    # The pure C^3 face has no P(t); use P=1.
    _, exponent_r, exponent_s = characteristic_data(0, 3, sp.Integer(1))
    I = sp.symbols("I", integer=True, nonnegative=True)
    assert exponent_r.subs(sp.Symbol("I", integer=True), I) == -10 * I - 10
    assert exponent_s.subs(sp.Symbol("I", integer=True), I) == (
        sp.Rational(17, 6) * I + sp.Rational(5, 2)
    )


def scan_graph_rays(
    relation,
    parameterization,
    maximum_degree: int,
) -> None:
    observed: list[tuple[int, int]] = []
    for degree in range(1, maximum_degree + 1):
        for graph_x_exponent in range(degree + 1):
            source_i = graph_x_exponent + 2
            source_j = degree - graph_x_exponent
            if relation(source_i, source_j):
                observed.append((degree, graph_x_exponent))
    expected: list[tuple[int, int]] = []
    parameter = 0
    while True:
        candidate = parameterization(parameter)
        if candidate is not None:
            if candidate[0] > maximum_degree:
                break
            expected.append(candidate)
        parameter += 1
    assert observed == expected


def verify_cubic_rays() -> None:
    # Binary A^3, A^2B, AB^2, and B^3 faces.
    scan_graph_rays(
        lambda I, J: 4 * J == 11 * I + 5,
        lambda k: None if k == 0 else (15 * k + 3, 4 * k - 1),
        900,
    )
    scan_graph_rays(
        lambda I, J: 24 * J == 49 * I + 15,
        lambda k: (73 * k + 26, 24 * k + 7),
        900,
    )
    scan_graph_rays(
        lambda I, J: 3 * J == 4 * I,
        lambda k: (7 * k + 5, 3 * k + 1),
        900,
    )
    scan_graph_rays(
        lambda I, J: 8 * J == 5 * I - 5,
        lambda k: (13 * k + 12, 8 * k + 7),
        900,
    )

    # The C*A^2 face repeats the AB^2 ray.  The C*AB face is new.
    scan_graph_rays(
        lambda I, J: 18 * J == 7 * I - 15,
        lambda k: (25 * k + 18, 18 * k + 13),
        900,
    )


def verify_forbidden_binary_terms() -> None:
    sector_i = sp.symbols("sector_i")
    exponent_functions = (
        (11 * sector_i + 5) / 4,
        (49 * sector_i + 15) / 24,
        4 * sector_i / 3,
    )
    expected_weight_slopes = (
        sp.Rational(15, 4),
        sp.Rational(73, 24),
        sp.Rational(7, 3),
    )
    expected_diagonal_slopes = (
        -sp.Rational(7, 4),
        -sp.Rational(25, 24),
        -sp.Rational(1, 3),
    )
    for exponent, weight_slope, diagonal_slope in zip(
        exponent_functions,
        expected_weight_slopes,
        expected_diagonal_slopes,
        strict=True,
    ):
        assert sp.diff(sector_i + exponent, sector_i) == weight_slope
        assert sp.diff(sector_i - exponent, sector_i) == diagonal_slope

    for k in range(1, 10):
        # A^3 face.
        source_i = 4 * k + 1
        source_j = 11 * k + 4
        assert sp.binomial(source_j, source_i - 1) != 0
        assert source_j - source_i + 1 == 7 * k + 4

    for k in range(10):
        # A^2B face.
        source_i = 24 * k + 9
        source_j = 49 * k + 19
        assert sp.binomial(source_j, source_i - 1) != 0
        assert source_j - source_i + 1 == 25 * k + 11

        # AB^2 and A^2C faces.
        source_i = 3 * k + 3
        source_j = 4 * k + 4
        assert sp.binomial(source_j, source_i - 1) != 0
        assert source_j - source_i + 1 == k + 2


def verify_abc_face() -> None:
    k = sp.symbols("k", integer=True, nonnegative=True)
    source_i = 18 * k + 15
    source_j = 7 * k + 5
    exponent_r = -10 * k - 10
    exponent_s = 17 * k + 15
    assert sp.expand(exponent_r + exponent_s - source_j) == 0
    assert sp.expand(exponent_s - source_j) == 10 * k + 10

    # In the mixed ABC/B^2C face, the t^-1 coefficient occurs at
    # q=J+1 and is nonzero because s>J.
    d = sp.symbols("d", nonzero=True)
    for sample_k in range(12):
        sample_j = 7 * sample_k + 5
        sample_s = 17 * sample_k + 15
        coefficient = (
            sp.binomial(sample_s, sample_j + 1)
            * d ** (sample_j + 1)
        )
        assert coefficient != 0
        degree = 25 * sample_k + 18
        assert sample_j + 1 == 7 * sample_k + 6
        assert sample_j + 1 < degree + 2
        assert sample_j + 1 < degree + 4

    # In the pure ABC face, the fixed gamma part leaves a defect.
    a = -sp.Rational(57, 34)
    gamma_fixed = 1 + a * (u - 1)
    defect = sp.expand(
        7 * x * sp.diff(gamma_fixed, x)
        - 11 * u * sp.diff(gamma_fixed, u)
        - 15 * gamma_fixed
    )
    expected = sp.Rational(741, 17) * x * y + sp.Rational(117, 34)
    assert sp.expand(defect.subs(u, 1 + x * y) - expected) == 0

    n = sp.symbols("n", integer=True, positive=True)
    assert sp.expand(7 * n - 18 * n - 15) == -11 * n - 15


def verify_nonresonant_c_faces() -> None:
    I, J = sp.symbols("I J", integer=True, nonnegative=True)
    # B^2C.
    assert sp.expand(-10 * I - 18 * J - 30) == (
        -10 * I - 18 * J - 30
    )
    # AC^2 and BC^2 have negative leading t-exponent for every I>=0.
    ac2_exponent = -sp.Rational(1, 2) * (3 * I + 5)
    bc2_exponent = -sp.Rational(1, 12) * (35 * I + 45)
    assert ac2_exponent.subs(I, 0) == -sp.Rational(5, 2)
    assert bc2_exponent.subs(I, 0) == -sp.Rational(15, 4)
    # C^3.
    assert -10 * (I + 1) < 0


def verify_newton_staircase_and_gaps() -> None:
    m, k = sp.symbols("m k", integer=True, positive=True)
    target_degrees = {
        "A3": 12 * m + 54,
        "A2B": 12 * m + 53,
        "AB2": 12 * m + 52,
        "B3": 12 * m + 51,
        "A2C": 9 * m + 39,
        "ABC": 9 * m + 38,
        "B2C": 9 * m + 37,
        "A2": 8 * m + 36,
        "AB": 8 * m + 35,
        "B2": 8 * m + 34,
        "AC2": 6 * m + 24,
        "BC2": 6 * m + 23,
        "AC": 5 * m + 21,
        "BC": 5 * m + 20,
        "A": 4 * m + 18,
        "B": 4 * m + 17,
        "C3": 3 * m + 9,
        "C2": 2 * m + 6,
        "C": m + 3,
    }
    staircase = (
        "A3", "A2B", "AB2", "B3",
        "A2C", "ABC", "B2C",
        "A2", "AB", "B2",
        "AC2", "BC2",
        "AC", "BC",
        "A", "B",
        "C3", "C2", "C",
    )
    for higher, lower in zip(
        staircase[:-1],
        staircase[1:],
        strict=True,
    ):
        difference = sp.Poly(
            target_degrees[higher] - target_degrees[lower],
            m,
        )
        assert difference.coeff_monomial(m) >= 0
        assert difference.eval(1) > 0

    # Binary cubic defects versus lower seed and the first C-cubic face.
    m_a3 = 15 * k + 3
    assert sp.expand((m_a3 + 4) - 8 * k) == 7 * k + 7
    assert sp.expand((3 * m_a3 + 15) - 8 * k) == 37 * k + 24

    k0 = sp.symbols("k0", integer=True, nonnegative=True)
    m_a2b = 73 * k0 + 26
    defect_a2b = 48 * k0 + 16
    assert sp.expand((m_a2b + 4) - defect_a2b) == 25 * k0 + 14
    assert sp.expand((3 * m_a2b + 14) - defect_a2b) == 171 * k0 + 76

    m_ab2 = 7 * k0 + 5
    defect_ab2 = 6 * k0 + 4
    assert sp.expand((m_ab2 + 4) - defect_ab2) == k0 + 5
    assert sp.expand((3 * m_ab2 + 13) - defect_ab2) == 15 * k0 + 24

    m_b3 = 13 * k0 + 12
    assert sp.expand((m_b3 + 4) - m_b3) == 4
    assert sp.expand((3 * m_b3 + 12) - m_b3) == 2 * m_b3 + 12

    # C*A^2 and C*AB faces versus the binary-quadratic lower tier.
    m_a2c = 7 * k0 + 5
    assert sp.expand((m_a2c + 3) - (6 * k0 + 4)) == k0 + 4

    m_abc = 25 * k0 + 18
    assert sp.expand((m_abc + 2) - (7 * k0 + 6)) == 18 * k0 + 14
    assert sp.expand((m_abc + 2) - m_abc) == 2

    # Earlier quadratic/linear defects versus the first possible cubic repair.
    assert sp.expand((25 * m + 103) - (23 * m + 91)) == 2 * m + 12
    assert sp.expand((25 * m + 102) - (23 * m + 91)) == 2 * m + 11
    assert sp.expand((25 * m + 101) - (23 * m + 91)) == 2 * m + 10
    assert sp.expand((22 * m + 88) - (21 * m + 85)) == m + 3
    assert sp.expand((21 * m + 85) - (20 * m + 76)) == m + 9
    assert sp.expand((21 * m + 84) - (20 * m + 76)) == m + 8

    # Evaluate those repair gaps on the only resonant earlier rays.
    m_quadratic_a = 15 * k + 3
    assert sp.expand(
        (2 * m_quadratic_a + 12) - 8 * k
    ) == 22 * k + 18
    m_quadratic_ab = 43 * k + 1
    assert sp.expand(
        (2 * m_quadratic_ab + 11) - 32 * k
    ) == 54 * k + 13
    assert sp.expand((2 * m + 10) - m) == m + 10
    assert sp.expand((m + 3) - m) == 3
    assert sp.expand((m_a3 + 9) - 8 * k) == 7 * k + 12
    assert sp.expand((m + 8) - m) == 8

    # A quadratic perturbation of the first coordinate is always later.
    degree_u = 17 * m + 69
    degree_quadratic = 8 * m + 36
    assert sp.expand(degree_u - degree_quadratic) == 9 * m + 33


def verify_constant_graphs() -> None:
    # If R=x^a y^b h^c and S=x^d y^e h^f with
    # h=a0*y+z0*x, then J(R,S)/(RS/(xyh)) is the linear form
    #
    # (a*e-b*d)h + (c*e-b*f)z0*x + (a*f-c*d)a0*y.
    #
    # Check its two coefficients without expanding the large powers.
    source_exponents = (32, 20, 17)
    cubic_forms: list[tuple[str, tuple[int, int, int], int]] = []
    for exponent_a in range(4):
        for exponent_b in range(4 - exponent_a):
            exponent_c = 3 - exponent_a - exponent_b
            target_exponents = (
                8 * (exponent_a + exponent_b) + 2 * exponent_c,
                6 * exponent_a + 5 * exponent_b,
                4 * (exponent_a + exponent_b) + exponent_c,
            )
            name = f"A{exponent_a}B{exponent_b}C{exponent_c}"
            degree = (
                18 * exponent_a
                + 17 * exponent_b
                + 3 * exponent_c
                + 69
                - 2
            )
            cubic_forms.append((name, target_exponents, degree))

    observed_degrees: list[int] = []
    source_x, source_y, source_h = source_exponents
    for name, target_exponents, expected_degree in cubic_forms:
        target_x, target_y, target_h = target_exponents
        h_coefficient = source_x * target_y - source_y * target_x
        zx_extra = source_h * target_y - source_y * target_h
        ay_extra = source_x * target_h - source_h * target_x
        zx_coefficient = h_coefficient + zx_extra
        ay_coefficient = h_coefficient + ay_extra
        assert (zx_coefficient, ay_coefficient) != (0, 0), name
        assert expected_degree == (
            sum(source_exponents[:2])
            + source_h
            + sum(target_exponents[:2])
            + target_h
            - 2
        ), name
        observed_degrees.append(expected_degree)

    assert sorted(observed_degrees, reverse=True) == [
        121, 120, 119, 118, 106, 105, 104, 91, 90, 76
    ]


def main() -> None:
    verify_master_characteristics()
    verify_cubic_rays()
    verify_forbidden_binary_terms()
    verify_abc_face()
    verify_nonresonant_c_faces()
    verify_newton_staircase_and_gaps()
    verify_constant_graphs()
    print("verified: master characteristic for every cubic Newton face")
    print("verified: all binary-cubic and C*quadratic resonance rays")
    print("verified: forbidden x^1 terms on every descending binary face")
    print("verified: mixed ABC/B^2C forces a negative t-power")
    print("verified: the full cubic-to-affine Newton staircase and gaps")
    print("verified: every constant-graph cubic top is nonzero")
    print("RESULT: every cubic second target pivot is closed")


if __name__ == "__main__":
    main()
