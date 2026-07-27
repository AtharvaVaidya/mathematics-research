#!/usr/bin/env python3
"""Verify closure of every quartic target with arbitrary cubic lower terms."""

from __future__ import annotations

import sympy as sp

import verify_weighted_lift_first_nonlinear_cusp_subduction as nonlinear


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


def verify_quartic_rays() -> None:
    # Binary quartic d=4,3,2,1,0.
    scan_graph_rays(
        lambda I, J: 4 * J == 11 * I + 5,
        lambda k: None if k == 0 else (15 * k + 3, 4 * k - 1),
        1200,
    )
    scan_graph_rays(
        lambda I, J: 32 * J == 71 * I + 25,
        lambda k: None if k == 0 else (103 * k + 2, 32 * k - 1),
        1200,
    )
    scan_graph_rays(
        lambda I, J: 16 * J == 27 * I + 5,
        lambda k: None if k == 0 else (43 * k + 1, 16 * k - 1),
        1200,
    )
    scan_graph_rays(
        lambda I, J: 32 * J == 37 * I - 5,
        lambda k: None if k == 0 else (69 * k, 32 * k - 1),
        1200,
    )
    scan_graph_rays(
        lambda I, J: 8 * J == 5 * I - 5,
        lambda k: (13 * k + 12, 8 * k + 7),
        1200,
    )

    # C*binary-cubic d=3,2,1.
    scan_graph_rays(
        lambda I, J: 13 * J == 23 * I + 5,
        lambda k: (36 * k + 15, 13 * k + 4),
        1200,
    )
    scan_graph_rays(
        lambda I, J: 26 * J == 29 * I - 5,
        lambda k: (55 * k + 38, 26 * k + 17),
        1200,
    )
    scan_graph_rays(
        lambda I, J: 13 * J == 6 * I - 10,
        lambda k: (19 * k + 6, 13 * k + 4),
        1200,
    )

    # C^2*A^2 repeats the old AC ray.
    scan_graph_rays(
        lambda I, J: 5 * J == I - 5,
        lambda k: (6 * k + 3, 5 * k + 3),
        1200,
    )


def verify_quartic_characteristics() -> None:
    coefficients = sp.symbols("p0:5")
    for number_ab, number_c in ((4, 0), (3, 1), (2, 2), (1, 3)):
        polynomial = sum(
            coefficients[index] * t**index
            for index in range(number_ab + 1)
        )
        characteristic_data(number_ab, number_c, polynomial)
    _, pure_c_r, _ = characteristic_data(0, 4, sp.Integer(1))
    symbol_i = next(iter(pure_c_r.free_symbols))
    assert pure_c_r == -10 * symbol_i - 10


def verify_descending_obstructions() -> None:
    # (I,J,forbidden drop,next lower target gap,next seed gap).
    rows = (
        (lambda k: (4 * k + 1, 11 * k + 4, 15 * k + 3), 1),
        (lambda k: (32 * k + 1, 71 * k + 3, 103 * k + 2), 1),
        (lambda k: (16 * k + 1, 27 * k + 2, 43 * k + 1), 1),
        (lambda k: (32 * k + 1, 37 * k + 1, 69 * k), 1),
    )
    for parameterization, first_k in rows:
        for k in range(first_k, 10):
            source_i, source_j, degree = parameterization(k)
            assert source_j > source_i
            assert sp.binomial(source_j, source_i - 1) != 0
            forbidden_drop = 2 * (source_i - 1)
            assert forbidden_drop < degree + 4

    # C*A^3 and C*A^2B descending rows.
    for k in range(10):
        for source_i, source_j, degree, lower_gap in (
            (13 * k + 6, 23 * k + 11, 36 * k + 15, 36 * k + 18),
            (26 * k + 19, 29 * k + 21, 55 * k + 38, 55 * k + 40),
        ):
            assert source_j > source_i
            assert sp.binomial(source_j, source_i - 1) != 0
            assert 2 * (source_i - 1) < lower_gap
            assert 2 * (source_i - 1) < degree + 4


def verify_c_ab2_negative_tail() -> None:
    # C*AB^2-leading face: I=13k+6,J=6k+2.
    eta = sp.symbols("eta", nonzero=True)
    for k in range(12):
        source_i = 13 * k + 6
        source_j = 6 * k + 2
        exponent_r = -sp.Rational(5 * k + 5, 2)
        exponent_s = sp.Rational(17 * k + 9, 2)
        assert exponent_r + exponent_s == source_j
        coefficient_t_minus_one = (
            sp.binomial(exponent_s, source_j + 1)
            * eta ** (source_j + 1)
        )
        assert coefficient_t_minus_one != 0
        degree = 19 * k + 6
        assert source_j + 1 < degree + 1


def verify_c2_quadratic_pole() -> None:
    # On I=5k+5,J=k, any t-adic order e<2 gives a negative exponent.
    for k in range(12):
        source_i = 5 * k + 5
        source_j = k
        exponent_r = -sp.Rational(15 * k + 20, 2)
        exponent_s = sp.Rational(17 * k + 20, 4)
        assert exponent_r + 2 * exponent_s == source_j
        assert exponent_r < 0
        assert exponent_r + exponent_s < 0

    # Coefficients of (1+b*z+c*z^2)^s obey a second-order recurrence.
    # Certify its generating-function differential equation exactly:
    #
    # (q+1)a_{q+1}
    #   = b(s-q)a_q+c(2s-q+1)a_{q-1}.
    #
    # If c!=0, a_{J+1}=a_{J+2}=0 first forces a_J=0 (put
    # q=J+1), then forces a_{J-1},...,a_0=0 by descending q.
    # Every c-multiplier in that descent is at least 2s-J>0.
    # This contradicts a_0=1.  If c=0 and b!=0, a_{J+1} is a
    # nonzero generalized binomial coefficient because s>J.
    z, b, c, s = sp.symbols("z b c s")
    generating_function = (1 + b * z + c * z**2) ** s
    assert sp.simplify(
        (1 + b * z + c * z**2) * sp.diff(generating_function, z)
        - s * (b + 2 * c * z) * generating_function
    ) == 0
    k = sp.symbols("k", integer=True, nonnegative=True)
    exponent_s = sp.Rational(1, 4) * (17 * k + 20)
    source_j = k
    assert sp.expand(2 * exponent_s - source_j) == (
        sp.Rational(15, 2) * k + 10
    )
    assert sp.expand(exponent_s - source_j) == (
        sp.Rational(13, 4) * k + 5
    )
    # The latest possible negative coefficient is a_{J+2}; it
    # precedes the C^2 A^2 -> C A^2 target-tier gap m+3.
    degree = 6 * k + 3
    assert sp.expand((degree + 3) - (source_j + 2)) == 5 * k + 4


def verify_pure_boundary_jet() -> None:
    a = -sp.Rational(57, 34)
    assert a.is_integer is False
    number_ab, number_c, d = sp.symbols(
        "number_ab number_c d",
        integer=True,
        nonnegative=True,
    )
    coefficient_u = (
        17 * d - 3 * number_ab - 22 * number_c
    )
    coefficient_zero = (
        15 * d - 5 * number_ab - 20 * number_c
    )
    # If both Euler coefficients vanished, the following exact
    # elimination identity would give 4*n+c=0.  Nonnegativity then
    # forces n=c=0, and either equation gives d=0.
    assert sp.expand(
        17 * coefficient_zero - 15 * coefficient_u
    ) == -10 * (4 * number_ab + number_c)
    for n_value in range(5):
        c_value = 4 - n_value
        for d_value in range(n_value + 1):
            pair = (
                coefficient_u.subs(
                    {
                        number_ab: n_value,
                        number_c: c_value,
                        d: d_value,
                    }
                ),
                coefficient_zero.subs(
                    {
                        number_ab: n_value,
                        number_c: c_value,
                        d: d_value,
                    }
                ),
            )
            assert pair != (0, 0)
    # If coefficient_u=0, a nonzero coefficient_zero gives no solution;
    # otherwise a polynomial solution is c*u^N, whose jets force N=a.
    # The fixed graph jet has f(1)=1 and f'(1)=a, while c*u^N
    # would require N=a, which is not a nonnegative integer.


def verify_linear_c4_mixture() -> None:
    gamma = sp.Function("gamma")(x, t)
    alpha, beta, rho = sp.symbols("alpha beta rho")
    polynomial = alpha * t**6 + beta * t**5 + rho
    highest_u = x**15 * t**20 * gamma**17
    highest_pivot = x**4 * gamma**4 * polynomial
    equation = (
        x * (-80 / t + 17 * sp.diff(polynomial, t) / polynomial)
        * sp.diff(gamma, x)
        - 8 * sp.diff(gamma, t)
        + (-80 / t + 15 * sp.diff(polynomial, t) / polynomial)
        * gamma
    )
    assert sp.factor(
        jacobian(highest_u, highest_pivot, (x, t))
        - highest_u * highest_pivot * equation / (x * gamma)
    ) == 0

    # Certify the exact coefficient recurrence for the A-leading
    # completion F=(1+b*z+c*z^6)^s:
    #
    # (q+1)a_{q+1}
    #   = b(s-q)a_q+c(6s-q+5)a_{q-5}.
    #
    # If c!=0 and a_{J+1},...,a_{J+6} all vanished, q=J+5
    # would force a_J=0.  Descending q then forces every coefficient
    # through a_0 to vanish; all c-multipliers are >=6s-J>0.
    z, b, c, s = sp.symbols("z b c s")
    generating_function = (1 + b * z + c * z**6) ** s
    assert sp.simplify(
        (1 + b * z + c * z**6) * sp.diff(generating_function, z)
        - s * (b + 6 * c * z**5) * generating_function
    ) == 0

    # A-leading: among the first six coefficients after degree J,
    # one is nonzero when rho!=0.  Independently, its leading
    # t^J term already gives the descending x^1 obstruction.
    k = sp.symbols("k", integer=True, positive=True)
    source_i_a = 4 * k + 1
    source_j_a = 11 * k + 4
    exponent_s_a = (17 * k + 8) / 2
    assert sp.expand(6 * exponent_s_a - source_j_a) == 40 * k + 20
    assert sp.expand((15 * k + 3 + 4) - (source_j_a + 6)) == 4 * k - 3
    assert sp.expand(source_j_a - source_i_a) == 7 * k + 3

    # B-leading with rho!=0: F=(1+c*z^5)^s has support on multiples
    # of five.  Since J=5(k+1), its first coefficient after J is
    # a_{J+5}=binomial(s,k+2)c^(k+2), and s>=k+2.
    k0 = sp.symbols("k0", integer=True, nonnegative=True)
    source_j_b = 5 * k0 + 5
    exponent_s_b = 17 * k0 + 21
    assert sp.binomial(exponent_s_b, k0 + 2) != 0
    assert sp.expand(exponent_s_b - (k0 + 2)) == 16 * k0 + 19
    assert sp.expand((13 * k0 + 12 + 4) - (source_j_b + 5)) == 8 * k0 + 6

    # If alpha=beta=0, the pure C^4 characteristic has J=-10I-10,
    # so no graph sector I>=2,J>=0 can resonate.  The remaining
    # rho=0 cases are precisely the already closed A/B linear face.


def verify_newton_staircase() -> None:
    m = sp.symbols("m", integer=True, positive=True)
    degrees = (
        16 * m + 72, 16 * m + 71, 16 * m + 70,
        16 * m + 69, 16 * m + 68,
        13 * m + 57, 13 * m + 56, 13 * m + 55, 13 * m + 54,
        12 * m + 54, 12 * m + 53, 12 * m + 52, 12 * m + 51,
        10 * m + 42, 10 * m + 41, 10 * m + 40,
        9 * m + 39, 9 * m + 38, 9 * m + 37,
        8 * m + 36, 8 * m + 35, 8 * m + 34,
        7 * m + 27, 7 * m + 26,
        6 * m + 24, 6 * m + 23,
        5 * m + 21, 5 * m + 20,
        4 * m + 18, 4 * m + 17, 4 * m + 12,
        3 * m + 9, 2 * m + 6, m + 3,
    )
    for higher, lower in zip(degrees[:-1], degrees[1:], strict=True):
        difference = sp.Poly(higher - lower, m)
        assert difference.coeff_monomial(m) >= 0
        assert difference.eval(1) > 0

    # A cubic first-coordinate perturbation lies later by 5m+15.
    assert sp.expand((17 * m + 69) - (12 * m + 54)) == 5 * m + 15


def verify_constant_graphs() -> None:
    source_exponents = (32, 20, 17)
    observed_degrees: list[int] = []
    exceptional_monomials: list[tuple[int, int, int]] = []
    for exponent_a in range(5):
        for exponent_b in range(5 - exponent_a):
            exponent_c = 4 - exponent_a - exponent_b
            target_exponents = (
                8 * (exponent_a + exponent_b) + 2 * exponent_c,
                6 * exponent_a + 5 * exponent_b,
                4 * (exponent_a + exponent_b) + exponent_c,
            )
            source_x, source_y, source_h = source_exponents
            target_x, target_y, target_h = target_exponents
            h_coefficient = source_x * target_y - source_y * target_x
            zx_coefficient = (
                h_coefficient + source_h * target_y - source_y * target_h
            )
            ay_coefficient = (
                h_coefficient + source_x * target_h - source_h * target_x
            )
            assert (zx_coefficient, ay_coefficient) != (0, 0)
            if ay_coefficient == 0:
                exceptional_monomials.append(
                    (exponent_a, exponent_b, exponent_c)
                )
                assert zx_coefficient != 0
            target_degree = (
                18 * exponent_a + 17 * exponent_b + 3 * exponent_c
            )
            observed_degrees.append(69 + target_degree - 2)
    # Every top remains nonzero at z0=0 except AB^3.  Its leading
    # homogeneous form is proportional to U0, so certify the next
    # exact diagonal coefficient from the seed instead of silently
    # assuming the toric top is nonzero.
    assert exceptional_monomials == [(1, 3, 0)]
    assert sorted(observed_degrees, reverse=True) == [
        139, 138, 137, 136, 135,
        124, 123, 122, 121,
        109, 108, 107,
        94, 93,
        79,
    ]

    p, q = nonlinear.build_seed()
    _, second_numerator, _, theta = nonlinear.build_maximal_subductions(
        p, q
    )
    v = sp.symbols("v")
    a = -sp.Rational(57, 34)
    gamma_diagonal = 1 + a * v
    w_diagonal = (1 + v) * gamma_diagonal
    diagonal_a = sp.cancel(
        (
            q.subs(nonlinear.w, w_diagonal)
            + w_diagonal * gamma_diagonal
        )
        / gamma_diagonal**2
    )
    diagonal_b = sp.cancel(
        (
            p.subs(nonlinear.w, w_diagonal)
            + gamma_diagonal
        )
        / gamma_diagonal
    )
    diagonal_u = sp.cancel(
        second_numerator.subs(
            {
                nonlinear.w: w_diagonal,
                nonlinear.gamma: gamma_diagonal,
            }
        )
        / gamma_diagonal**5
    )
    diagonal_ab3 = sp.expand(diagonal_a * diagonal_b**3)
    polynomial_u = sp.Poly(diagonal_u, v)
    polynomial_ab3 = sp.Poly(diagonal_ab3, v)
    assert (polynomial_u.degree(), polynomial_ab3.degree()) == (37, 37)
    coefficient_u_37 = polynomial_u.coeff_monomial(v**37)
    coefficient_u_36 = polynomial_u.coeff_monomial(v**36)
    coefficient_ab3_37 = polynomial_ab3.coeff_monomial(v**37)
    coefficient_ab3_36 = polynomial_ab3.coeff_monomial(v**36)
    p5 = sp.Poly(p, nonlinear.w).coeff_monomial(nonlinear.w**5)
    q6 = sp.Poly(q, nonlinear.w).coeff_monomial(nonlinear.w**6)
    assert coefficient_u_37 == theta * a**17
    assert coefficient_ab3_37 == q6 * p5**3 * a**16
    assert sp.factor(coefficient_u_36 / coefficient_u_37) == (
        sp.Rational(562, 57)
    )
    assert sp.factor(coefficient_ab3_36 / coefficient_ab3_37) == (
        sp.Rational(653, 57)
    )

    # On z=0, U=x^-5 H(v) and AB^3=x^-5 K(v), v=xy.  Hence
    # J(U,AB^3)=5*x^-10*(H'K-HK').  Its v^72 coefficient is
    # 5*(H_37*K_36-H_36*K_37), which is the displayed nonzero
    # multiple of the certified leading constants.
    exceptional_coefficient = sp.factor(
        5
        * (
            coefficient_u_37 * coefficient_ab3_36
            - coefficient_u_36 * coefficient_ab3_37
        )
    )
    exceptional_wronskian = sp.Poly(
        sp.expand(
            5
            * (
                sp.diff(diagonal_u, v) * diagonal_ab3
                - diagonal_u * sp.diff(diagonal_ab3, v)
            )
        ),
        v,
    )
    assert exceptional_wronskian.degree() == 72
    assert (
        exceptional_wronskian.coeff_monomial(v**72)
        == exceptional_coefficient
    )
    assert exceptional_coefficient == sp.factor(
        sp.Rational(455, 57) * theta * q6 * p5**3 * a**33
    )
    assert exceptional_coefficient != 0


def main() -> None:
    verify_quartic_characteristics()
    verify_quartic_rays()
    verify_descending_obstructions()
    verify_c_ab2_negative_tail()
    verify_c2_quadratic_pole()
    verify_pure_boundary_jet()
    verify_linear_c4_mixture()
    verify_newton_staircase()
    verify_constant_graphs()
    print("verified: every quartic Newton-face characteristic")
    print("verified: all binary and C*binary quartic resonance rays")
    print("verified: descending/pole certificates and legacy Euler coefficients")
    print("verified: the mixed A/B versus C^4 face has a short tail")
    print("verified: exact quartic-to-affine Newton staircase")
    print("verified: fourteen constant tops and the exact AB^3 next diagonal")
    print("RESULT: quartic certificates pass; use the correction audit for pure faces")


if __name__ == "__main__":
    main()
