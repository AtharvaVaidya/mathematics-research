#!/usr/bin/env python3
"""Verify the first nonlinear cusp subduction of the degree-six lift."""

from __future__ import annotations

import sympy as sp


x, y, w, gamma = sp.symbols("x y w gamma")


def jacobian(first: sp.Expr, second: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(first, x) * sp.diff(second, y)
        - sp.diff(first, y) * sp.diff(second, x)
    )


def build_seed() -> tuple[sp.Expr, sp.Expr]:
    root_polynomial = sp.expand(
        w * (w + 1) * (w - 3) * (w - 4) * (w - 5) * (w + 4)
    )
    normalization = (
        sp.diff(root_polynomial, w).subs(w, 0)
        - sp.diff(root_polynomial, w).subs(w, 1)
    )
    assert normalization == -92
    H = sp.expand(root_polynomial / normalization)
    p = sp.expand(sp.diff(H, w) - sp.diff(H, w).subs(w, 0))
    q = sp.expand(w * sp.diff(H, w) - H)
    return p, q


def verify_exact_first_subduction(p: sp.Expr, q: sp.Expr) -> None:
    p_poly = sp.Poly(p, w)
    q_poly = sp.Poly(q, w)
    p5 = p_poly.coeff_monomial(w**5)
    p4 = p_poly.coeff_monomial(w**4)
    q6 = q_poly.coeff_monomial(w**6)
    q5 = q_poly.coeff_monomial(w**5)
    assert (p5, p4, q6, q5) == (
        -sp.Rational(3, 46),
        sp.Rational(35, 92),
        -sp.Rational(5, 92),
        sp.Rational(7, 23),
    )

    numerator = sp.expand(
        p5**6 * (q + w * gamma) ** 5
        - q6**5 * (p + gamma) ** 6
    )
    numerator_poly = sp.Poly(numerator, w, gamma)
    assert numerator_poly.coeff_monomial(w**30) == 0

    kappa = sp.factor(7 * p5**6 * q6**5)
    assert kappa != 0
    assert numerator_poly.coeff_monomial(w**29) == kappa
    assert sp.factor(
        5 * q5 / q6 - 6 * p4 / p5
    ) == 7

    # A numerator monomial w^i gamma^j contributes, after division by
    # x^6 gamma^6 and graph substitution, weight
    # i(m+4)+(j-6)(m+2)-6.  Verify uniformly for every integer m>=1
    # that w^29 is the unique largest-weight monomial.
    for (i, j), coefficient in numerator_poly.terms():
        if coefficient == 0 or (i, j) == (29, 0):
            continue
        slope = 29 - i - j
        value_at_m_one = 5 * (29 - i) - 3 * j
        assert slope >= 0
        assert value_at_m_one > 0


def build_maximal_subductions(
    p: sp.Expr, q: sp.Expr
) -> tuple[sp.Expr, sp.Expr, sp.Rational, sp.Rational]:
    p_poly = sp.Poly(p, w)
    q_poly = sp.Poly(q, w)
    p5 = p_poly.coeff_monomial(w**5)
    q6 = q_poly.coeff_monomial(w**6)
    Q = sp.expand(q + w * gamma)
    P = sp.expand(p + gamma)

    # First denominator slice: x^6 gamma^6.
    first_numerator = sp.expand(p5**6 * Q**5 - q6**5 * P**6)
    first_coefficients = (
        -sp.Rational(8505, 18948593792),
        -sp.Rational(79515, 151588750336),
        sp.Rational(1587485, 303177500672),
        -sp.Rational(1079635, 303177500672),
    )
    for r, target_coefficient in enumerate(first_coefficients, start=1):
        power = 30 - r
        monomial = sp.expand(Q ** (5 - r) * P**r)
        current = sp.Poly(
            first_numerator, w, gamma
        ).coeff_monomial(w**power)
        leading = sp.Poly(monomial, w, gamma).coeff_monomial(w**power)
        coefficient = sp.factor(-current / leading)
        assert coefficient == target_coefficient
        first_numerator = sp.expand(
            first_numerator + coefficient * monomial
        )
        assert (
            sp.Poly(first_numerator, w, gamma).coeff_monomial(w**power)
            == 0
        )

    lambda_zero = sp.Rational(
        258473511, 31221670147323559936
    )
    first_poly = sp.Poly(first_numerator, w, gamma)
    assert first_poly.coeff_monomial(w**25) == lambda_zero

    # Uniform graph weight after division by x^6 gamma^6.
    for (i, j), coefficient in first_poly.terms():
        if coefficient == 0 or (i, j) == (25, 0):
            continue
        slope = 25 - i - j
        value_at_m_one = 5 * (25 - i) - 3 * j
        assert slope >= 0
        assert value_at_m_one > 0

    # Second denominator slice: x^5 gamma^5.
    second_numerator = sp.expand(
        p5**5 * first_numerator - lambda_zero * P**5
    )
    second_coefficients = (
        -sp.Rational(
            10204102899, 11489574614215070056448
        ),
        sp.Rational(5559334317, 249773361178588479488),
        -sp.Rational(
            1028649031155, 11489574614215070056448
        ),
        sp.Rational(16337519127, 359049206694220939264),
    )
    for r, target_coefficient in enumerate(second_coefficients):
        power = 24 - r
        monomial = sp.expand(Q ** (4 - r) * P**r)
        current = sp.Poly(
            second_numerator, w, gamma
        ).coeff_monomial(w**power)
        leading = sp.Poly(monomial, w, gamma).coeff_monomial(w**power)
        coefficient = sp.factor(-current / leading)
        assert coefficient == target_coefficient
        second_numerator = sp.expand(
            second_numerator + coefficient * monomial
        )
        assert (
            sp.Poly(second_numerator, w, gamma).coeff_monomial(w**power)
            == 0
        )

    theta = -sp.Rational(
        36905625, 6077984970919772059860992
    )
    second_poly = sp.Poly(second_numerator, w, gamma)
    assert second_poly.coeff_monomial(w**20 * gamma**2) == theta

    # Uniform graph weight after division by x^5 gamma^5.
    for (i, j), coefficient in second_poly.terms():
        if coefficient == 0 or (i, j) == (20, 2):
            continue
        slope = 22 - i - j
        value_at_m_one = 5 * (20 - i) + 3 * (2 - j)
        assert slope >= 0
        assert value_at_m_one > 0

    return first_numerator, second_numerator, lambda_zero, theta


def verify_toric_jacobians() -> None:
    p5 = -sp.Rational(3, 46)
    q6 = -sp.Rational(5, 92)
    kappa = sp.factor(7 * p5**6 * q6**5)
    graph_top = sp.Function("graph_top")(x, y)
    C0 = x**3 * graph_top
    A0 = q6 * y**6 * C0**4
    B0 = p5 * y**5 * C0**4
    E0 = kappa * y**29 * C0**23

    # The genuine relation needs C^4.  A^5 and B^6 alone have
    # different exponent vectors.
    assert sp.expand(p5**6 * A0**5 * C0**4 - q6**5 * B0**6) == 0
    assert (5 * 6, 5 * 4) != (6 * 5, 6 * 4)
    assert 29 * 4 - 23 * 5 == 1

    assert sp.expand(
        jacobian(E0, C0)
        + 29
        * kappa
        * y**28
        * C0**23
        * sp.diff(C0, x)
    ) == 0
    assert sp.expand(
        jacobian(E0, B0)
        + kappa
        * p5
        * y**33
        * C0**26
        * sp.diff(C0, x)
    ) == 0
    assert sp.expand(
        jacobian(E0, A0)
        - 22
        * kappa
        * q6
        * y**34
        * C0**26
        * sp.diff(C0, x)
    ) == 0

    m = sp.symbols("m", integer=True, positive=True)
    degree_C = m + 3
    degree_A = 4 * m + 18
    degree_B = 4 * m + 17
    degree_E = 23 * m + 98
    assert sp.expand(degree_E + degree_C - 2) == 24 * m + 99
    assert sp.expand(degree_E + degree_B - 2) == 27 * m + 113
    assert sp.expand(degree_E + degree_A - 2) == 27 * m + 114


def verify_maximal_subduction_jacobians(
    lambda_zero: sp.Rational, theta: sp.Rational
) -> None:
    p5 = -sp.Rational(3, 46)
    q6 = -sp.Rational(5, 92)
    graph_top = sp.Function("graph_top")(x, y)
    C0 = x**3 * graph_top
    A0 = q6 * y**6 * C0**4
    B0 = p5 * y**5 * C0**4
    T0 = lambda_zero * y**25 * C0**19

    assert sp.expand(
        jacobian(T0, C0)
        + 25
        * lambda_zero
        * y**24
        * C0**19
        * sp.diff(C0, x)
    ) == 0
    assert sp.expand(
        jacobian(T0, B0)
        + 5
        * lambda_zero
        * p5
        * y**29
        * C0**22
        * sp.diff(C0, x)
    ) == 0
    assert sp.expand(
        jacobian(T0, A0)
        - 14
        * lambda_zero
        * q6
        * y**30
        * C0**22
        * sp.diff(C0, x)
    ) == 0

    # The vector (25,19) is outside the original initial semigroup.
    solutions = []
    for exponent_a in range(6):
        for exponent_b in range(6):
            exponent_c = 19 - 4 * exponent_a - 4 * exponent_b
            if (
                6 * exponent_a + 5 * exponent_b == 25
                and exponent_c >= 0
            ):
                solutions.append((exponent_a, exponent_b, exponent_c))
    assert solutions == []

    # The second subduction exposes x explicitly.
    g = graph_top
    U0 = theta * x**49 * y**20 * g**17
    expected_with_C = (
        -2
        * theta
        * x**51
        * y**19
        * g**17
        * (
            30 * g
            + 10 * x * sp.diff(g, x)
            + y * sp.diff(g, y)
        )
    )
    expected_with_B = (
        theta
        * p5
        * x**60
        * y**24
        * g**20
        * (
            5 * g
            + 5 * x * sp.diff(g, x)
            - 8 * y * sp.diff(g, y)
        )
    )
    expected_with_A = (
        theta
        * q6
        * x**60
        * y**25
        * g**20
        * (
            54 * g
            + 22 * x * sp.diff(g, x)
            - 8 * y * sp.diff(g, y)
        )
    )
    assert sp.expand(jacobian(U0, C0) - expected_with_C) == 0
    assert sp.expand(jacobian(U0, B0) - expected_with_B) == 0
    assert sp.expand(jacobian(U0, A0) - expected_with_A) == 0

    # Solve the two diagonal resonance equations exactly.
    resonant_b = []
    resonant_a = []
    for degree in range(1, 200):
        for x_exponent in range(degree + 1):
            if 13 * x_exponent == 8 * degree - 5:
                resonant_b.append((degree, x_exponent))
            if 15 * x_exponent == 4 * degree - 27:
                resonant_a.append((degree, x_exponent))
    assert resonant_b == [
        (13 * k + 12, 8 * k + 7) for k in range(15)
    ]
    assert resonant_a == [
        (15 * k + 3, 4 * k - 1) for k in range(1, 14)
    ]


def verify_reduced_ray_pde() -> None:
    u = sp.symbols("u")
    gamma_function = sp.Function("gamma")(x, u)
    highest_U_sector = x**-5 * u**20 * gamma_function**17
    highest_B_sector = x**-1 * u**5 * gamma_function**4
    jacobian_xu = sp.expand(
        sp.diff(highest_U_sector, x)
        * sp.diff(highest_B_sector, u)
        - sp.diff(highest_U_sector, u)
        * sp.diff(highest_B_sector, x)
    )
    euler_defect = (
        5 * x * sp.diff(gamma_function, x)
        - 3 * u * sp.diff(gamma_function, u)
        - 5 * gamma_function
    )
    expected = sp.expand(
        highest_U_sector
        * highest_B_sector
        * euler_defect
        / (u * gamma_function)
    )
    assert sp.expand(x * jacobian_xu - expected) == 0

    k = sp.symbols("k", integer=True, nonnegative=True)
    x_exponent = 3 * k + 4
    u_exponent = 5 * k + 5
    assert sp.expand(
        5 * x_exponent - 3 * u_exponent - 5
    ) == 0

    # The k=0 polynomial graph begins with precisely the two forced
    # homogeneous pieces from expansion of x^2(1+xy)^5.
    candidate = sp.expand(x**2 * (1 + x * y) ** 5)
    candidate_poly = sp.Poly(candidate, x, y)
    degree_twelve = sum(
        coefficient * x**monomial[0] * y**monomial[1]
        for monomial, coefficient in candidate_poly.terms()
        if sum(monomial) == 12
    )
    degree_eleven = sum(
        coefficient * x**monomial[0] * y**monomial[1]
        for monomial, coefficient in candidate_poly.terms()
        if sum(monomial) == 11
    )
    degree_ten = sum(
        coefficient * x**monomial[0] * y**monomial[1]
        for monomial, coefficient in candidate_poly.terms()
        if sum(monomial) == 10
    )
    assert degree_twelve == x**7 * y**5
    assert degree_eleven == 0
    assert degree_ten == 5 * x**6 * y**4


def verify_raw_binomial_pairs() -> None:
    m = sp.symbols("m", integer=True, positive=True)
    degree_A = 4 * m + 18
    degree_B = 4 * m + 17
    degree_J_AB = 8 * m + 33
    degree_J_AC = 5 * m + 19
    degree_J_BC = 5 * m + 18

    # J(A^5-lambda B^6,B)=5 A^4 J(A,B).
    raw_with_B = 4 * degree_A + degree_J_AB
    assert sp.expand(raw_with_B) == 24 * m + 105

    # In J(A^5-lambda B^6,C), the B^6 term strictly dominates
    # the A^5 term whenever lambda is nonzero.
    a_term = 4 * degree_A + degree_J_AC
    b_term = 5 * degree_B + degree_J_BC
    assert sp.expand(a_term) == 21 * m + 91
    assert sp.expand(b_term) == 25 * m + 103
    assert sp.expand(b_term - a_term) == 4 * m + 12


def main() -> None:
    p, q = build_seed()
    verify_exact_first_subduction(p, q)
    _, _, lambda_zero, theta = build_maximal_subductions(p, q)
    verify_toric_jacobians()
    verify_maximal_subduction_jacobians(lambda_zero, theta)
    verify_reduced_ray_pde()
    verify_raw_binomial_pairs()
    print("verified: A^5 and B^6 alone do not have matching top degree")
    print("verified: the primitive top relation is A^5 C^4 versus B^6")
    print("verified: exact next form is kappa*y^29*C_top^23")
    print("verified: the new exponent has determinant one with B_top")
    print("verified: pairing the cusp residual with A, B, or C fails")
    print("verified: maximal first slice has top y^25*C_top^19")
    print("verified: second slice exposes x^49*y^20*g_top^17")
    print("verified: only two sparse Newton rays survive with A or B")
    print("verified: the B-ray is an exact weighted-Euler PDE ansatz")
    print("RESULT: first nonlinear cusp subduction structurally reduced")


if __name__ == "__main__":
    main()
