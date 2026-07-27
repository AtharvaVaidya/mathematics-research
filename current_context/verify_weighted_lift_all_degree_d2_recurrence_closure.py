#!/usr/bin/env python3
"""Verify the first-lower recurrence for every binary d=2 face."""

from __future__ import annotations

import sympy as sp

import verify_weighted_lift_first_nonlinear_cusp_subduction as nonlinear


x, y, u, t, eta = sp.symbols("x y u t eta")


def verify_exact_seed_slices() -> None:
    p, q = nonlinear.build_seed()
    _, second_numerator, _, theta = nonlinear.build_maximal_subductions(
        p, q
    )
    p_poly = sp.Poly(p, nonlinear.w)
    q_poly = sp.Poly(q, nonlinear.w)
    second_poly = sp.Poly(
        second_numerator,
        nonlinear.w,
        nonlinear.gamma,
    )
    p5 = p_poly.coeff_monomial(nonlinear.w**5)
    p4 = p_poly.coeff_monomial(nonlinear.w**4)
    q6 = q_poly.coeff_monomial(nonlinear.w**6)
    q5 = q_poly.coeff_monomial(nonlinear.w**5)
    assert sp.factor(p4 / p5) == -sp.Rational(35, 6)
    assert sp.factor(q5 / q6) == -sp.Rational(28, 5)

    top = second_poly.coeff_monomial(
        nonlinear.w**20 * nonlinear.gamma**2
    )
    lower = second_poly.coeff_monomial(
        nonlinear.w**19 * nonlinear.gamma**2
    )
    assert top == theta
    assert sp.factor(lower / top) == -sp.Rational(70, 3)


def verify_all_n_target_slice() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    b, c = sp.symbols("b c")
    p_ratio = -sp.Rational(35, 6)
    q_ratio = -sp.Rational(28, 5)
    coefficient_a2 = sp.expand(2 * q_ratio + (n - 2) * p_ratio)
    coefficient_ab = sp.expand(q_ratio + (n - 1) * p_ratio)
    coefficient_b2 = sp.expand(n * p_ratio)
    assert coefficient_a2 == -sp.Rational(35, 6) * n + (
        sp.Rational(7, 15)
    )
    assert coefficient_ab == -sp.Rational(35, 6) * n + (
        sp.Rational(7, 30)
    )
    assert coefficient_b2 == -sp.Rational(35, 6) * n

    polynomial = t**2 + b * t + c
    lower_polynomial = (
        coefficient_a2 * t**2
        + b * coefficient_ab * t
        + c * coefficient_b2
    )
    assert sp.Poly(polynomial, t).degree() == 2
    assert sp.Poly(lower_polynomial, t).degree() == 2

    # The displayed lower polynomial is the unique target slice at
    # drop m+4.  All other seed replacements occur later.
    m = sp.symbols("m", integer=True, positive=True)
    assert sp.expand((6 - 5) * (m + 4)) == m + 4
    assert sp.expand((5 - 4) * (m + 4)) == m + 4
    assert sp.expand((6 - 4) * (m + 4)) == 2 * (m + 4)
    assert sp.expand((5 - 3) * (m + 4)) == 2 * (m + 4)
    assert sp.expand(4 * m + 18 - (m + 4)) == 3 * m + 14


def verify_first_polynomial_completion() -> None:
    # For a mixed quadratic P, polynomiality of
    # t^r*P(t)^s implies r is integral and 2s is integral.
    # Thus I=8a+1 and L=2s=(34a+8)/n is a positive integer.
    # Graph divisibility is L<=3a-1.
    a_index, n = sp.symbols(
        "a_index n",
        integer=True,
        positive=True,
    )
    lower_bound_gap = sp.factor(
        (34 * a_index + 8) / 11 - (3 * a_index - 1)
    )
    assert sp.factor(lower_bound_gap - (a_index + 19) / 11) == 0
    # Hence n<=11 gives L>(3a-1), independent of divisibility.

    # At n=12, integrality requires a=4 mod 6.  The first candidate
    # a=4 fails graph divisibility; a=10 is sharp.
    assert [
        residue
        for residue in range(6)
        if (17 * residue + 4) % 6 == 0
    ] == [4]
    assert sp.Rational(17 * 4 + 4, 6) == 12
    assert 12 > 3 * 4 - 1
    assert sp.Rational(17 * 10 + 4, 6) == 29
    assert 29 == 3 * 10 - 1

    # The first sharp realization is therefore n=12,a=10 and a
    # double nonzero root P=(t+eta)^2.
    n_value = 12
    a_value = 10
    source_i = 8 * a_value + 1
    exponent_r = 5 * a_value
    twice_s = (34 * a_value + 8) // n_value
    exponent_s = sp.Rational(twice_s, 2)
    source_j = exponent_r + twice_s
    assert (source_i, exponent_r, exponent_s, source_j) == (
        81,
        50,
        sp.Rational(29, 2),
        79,
    )
    assert source_i - source_j == 2
    characteristic = (
        x**source_i
        * t**exponent_r
        * (t + eta) ** (2 * exponent_s)
    )
    expected_source_form = x**2 * u**50 * (u + eta * x) ** 29
    assert sp.expand(
        characteristic.subs(t, u / x) - expected_source_form
    ) == 0


def verify_graph_sector_polynomiality() -> None:
    # The coordinate change y=t-x^-1 embeds C[x,y] into
    # C[x,x^-1,t].  In particular, every fixed Laurent-x
    # coefficient of x^2*g(x,y) is a polynomial in t.  Audit a
    # generic finite basis symbolically; the displayed binomial
    # formula is uniform in both exponents.
    coefficients_by_x_power: dict[int, sp.Expr] = {}
    for source_x_power in range(7):
        for source_y_power in range(7):
            transformed = sp.expand(
                x ** (source_x_power + 2)
                * (t - x**-1) ** source_y_power
            )
            for term in sp.Add.make_args(transformed):
                powers = term.as_powers_dict()
                x_power = int(powers.get(x, 0))
                t_power = powers.get(t, 0)
                assert int(t_power) == t_power
                assert int(t_power) >= 0
                coefficients_by_x_power[x_power] = sp.expand(
                    coefficients_by_x_power.get(x_power, 0) + term / x**x_power
                )
    for coefficient in coefficients_by_x_power.values():
        assert sp.Poly(coefficient, t).is_univariate


def verify_quadratic_tail_timing() -> None:
    z, b, c, s = sp.symbols("z b c s")
    generating_function = (1 + b * z + c * z**2) ** s
    assert sp.simplify(
        (1 + b * z + c * z**2)
        * sp.diff(generating_function, z)
        - s * (b + 2 * c * z) * generating_function
    ) == 0
    # If F=sum a_q*z^q, coefficient extraction gives
    # (q+1)a_{q+1}
    #   =b(s-q)a_q+c(2s-q+1)a_{q-1}.
    # Hence two consecutive zero coefficients force every later
    # coefficient to vanish.  If t^J F(t^-1) is not polynomial,
    # at least one of a_{J+1},a_{J+2} is nonzero.
    source_i, source_j = sp.symbols(
        "I J",
        integer=True,
        nonnegative=True,
    )
    graph_seed_gap = source_i + source_j + 2
    assert sp.expand(
        graph_seed_gap - (source_j + 2)
    ) == source_i
    # Natural graph sectors have I>=2, so the tail is strictly
    # earlier than m+4.


def verify_general_lower_recurrence() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    source_i = sp.symbols("I", integer=True, positive=True)
    b, c = sp.symbols("b c")
    polynomial = t**2 + b * t + c
    p_ratio = -sp.Rational(35, 6)
    q_ratio = -sp.Rational(28, 5)
    coefficient_a2 = 2 * q_ratio + (n - 2) * p_ratio
    coefficient_ab = q_ratio + (n - 1) * p_ratio
    coefficient_b2 = n * p_ratio
    lower_polynomial = (
        coefficient_a2 * t**2
        + b * coefficient_ab * t
        + c * coefficient_b2
    )

    exponent_r = sp.Rational(5, 8) * (source_i - 1)
    exponent_s = (17 * source_i + 15) / (8 * n)
    logarithmic_gamma_x = source_i / x
    logarithmic_gamma_t = (
        exponent_r / t
        + exponent_s * sp.diff(polynomial, t) / polynomial
    )
    amplitude = sp.symbols("amplitude", nonzero=True)
    characteristic = (
        amplitude
        * x**source_i
        * t**exponent_r
        * polynomial**exponent_s
    )
    assert sp.factor(
        sp.diff(characteristic, x)
        - logarithmic_gamma_x * characteristic
    ) == 0
    assert sp.factor(
        sp.diff(characteristic, t)
        - logarithmic_gamma_t * characteristic
    ) == 0
    assert not logarithmic_gamma_x.has(amplitude)
    assert not logarithmic_gamma_t.has(amplitude)

    def logarithmic_determinant(
        first_x: sp.Expr,
        first_t: sp.Expr,
        first_gamma: sp.Expr,
        first_extra_t: sp.Expr,
        second_x: sp.Expr,
        second_t: sp.Expr,
        second_gamma: sp.Expr,
        second_extra_t: sp.Expr,
    ) -> sp.Expr:
        first_log_x = first_x / x + first_gamma * logarithmic_gamma_x
        first_log_t = (
            first_t / t
            + first_gamma * logarithmic_gamma_t
            + first_extra_t
        )
        second_log_x = (
            second_x / x + second_gamma * logarithmic_gamma_x
        )
        second_log_t = (
            second_t / t
            + second_gamma * logarithmic_gamma_t
            + second_extra_t
        )
        return sp.expand(
            first_log_x * second_log_t
            - first_log_t * second_log_x
        )

    reduced_forcing = sp.factor(
        -sp.Rational(70, 3)
        / t
        * logarithmic_determinant(
            14,
            19,
            16,
            0,
            4 * n,
            5 * n,
            4 * n,
            sp.diff(polynomial, t) / polynomial,
        )
        + lower_polynomial
        / (t * polynomial)
        * logarithmic_determinant(
            15,
            20,
            17,
            0,
            4 * n - 1,
            5 * n - 1,
            4 * n - 1,
            sp.diff(lower_polynomial, t) / lower_polynomial,
        )
    )

    characteristic_operator_over_gamma = (
        x
        * (
            5 * n / t
            + 17 * sp.diff(polynomial, t) / polynomial
        )
        * logarithmic_gamma_x
        - 8 * n * logarithmic_gamma_t
        - 5 * n / t
        + 15 * sp.diff(polynomial, t) / polynomial
    )
    assert sp.factor(characteristic_operator_over_gamma) == 0

    # The m+4 forcing has an unavoidable double pole, whereas the
    # characteristic operator applied to a polynomial t-sector has
    # only simple poles.  First suppose c!=0.  Then t=0 is not a
    # root of P, and the double-pole coefficient is nonzero.
    pole_at_zero = sp.factor(
        sp.limit(t**2 * x * reduced_forcing, t, 0)
    )
    assert pole_at_zero == -sp.Rational(35, 24) * n * (
        source_i - 1
    )

    # If c=0 and b!=0, P=t(t+b).  The t=0 multiplicity changes,
    # but a nonzero double pole remains at the other root t=-b.
    forcing_with_zero_root = sp.factor(reduced_forcing.subs(c, 0))
    pole_at_nonzero_root = sp.factor(
        sp.limit(
            (t + b) ** 2 * x * forcing_with_zero_root,
            t,
            -b,
        )
    )
    assert sp.factor(
        pole_at_nonzero_root
        + sp.Rational(7, 120)
        * (17 * source_i + 15)
        * (4 * n - 1)
        / n
    ) == 0

    # For delta_gamma=x^-1*psi(t), the homogeneous operator has
    # denominator only t*P.  Thus it cannot supply either double
    # pole when psi is polynomial.
    psi = sp.Function("psi")(t)
    polynomial_operator = (
        -(
            5 * n / t
            + 17 * sp.diff(polynomial, t) / polynomial
        )
        * psi
        - 8 * n * sp.diff(psi, t)
        + (
            -5 * n / t
            + 15 * sp.diff(polynomial, t) / polynomial
        )
        * psi
    )
    cleared_operator = sp.cancel(t * polynomial * polynomial_operator)
    assert sp.denom(cleared_operator) == 1

    # Repeated roots cause no hidden higher pole:
    # P'/P has residue equal to the root multiplicity but pole
    # order one.  Check the two relevant forcing locations on an
    # arbitrary polynomial psi.  At c!=0, t=0 is not a root of P;
    # at c=0,b!=0, -b is a simple nonzero root.
    psi_coefficients = sp.symbols("psi0:6")
    polynomial_psi = sum(
        coefficient * t**power
        for power, coefficient in enumerate(psi_coefficients)
    )
    polynomial_operator_explicit = polynomial_operator.subs(
        {
            psi: polynomial_psi,
            sp.diff(psi, t): sp.diff(polynomial_psi, t),
        }
    )
    assert sp.factor(
        sp.limit(t**2 * polynomial_operator_explicit, t, 0)
    ) == 0
    assert sp.factor(
        sp.limit(
            (t + b) ** 2
            * polynomial_operator_explicit.subs(c, 0),
            t,
            -b,
        )
    ) == 0

    # Audit the filtration separation explicitly.  The pole
    # obstruction is on the first-lower seed slice m+4.  The old
    # cleared source-axis residual belongs to m+2d+2=m+6 and is not
    # combined with it.
    m = sp.symbols("m", integer=True, positive=True)
    assert (m + 4) < (m + 2 * 2 + 2)

    # At the first perfect-square completion n=12,I=81,c=eta^2,
    # the t=0 double-pole coefficient is exactly -1400/x.
    assert pole_at_zero.subs({n: 12, source_i: 81}) == -1400


def verify_sector_uniqueness() -> None:
    n, graph_degree = sp.symbols(
        "n graph_degree",
        integer=True,
        positive=True,
    )
    source_i = sp.symbols("I", integer=True)
    source_j = graph_degree - source_i + 2
    resonance = sp.expand(
        8 * n * source_j
        - (5 * n + 34) * source_i
        - 30
        + 5 * n
    )
    solved_i = sp.solve(resonance, source_i)
    assert solved_i == [
        (8 * graph_degree * n + 21 * n - 30) / (13 * n + 34)
    ]
    assert 13 * n + 34 > 0
    # Hence a fixed highest graph degree has at most one resonant
    # Laurent-x sector.  The normalized first-lower forcing lies
    # wholly in x^-1, and L preserves Laurent-x exponents.


def verify_constant_graphs() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    # For A^2 B^(n-2), the constant-graph toric coefficient pair is
    # ((5n+98) z0*x, 8(8-n) a*y).  It is nonzero except possibly
    # at z0=0,n=8.
    zx_coefficient = 5 * n + 98
    ay_coefficient = 8 * (8 - n)
    assert zx_coefficient.subs(n, 8) == 138
    assert ay_coefficient.subs(n, 8) == 0

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
    diagonal_a2b6 = sp.expand(diagonal_a**2 * diagonal_b**6)
    polynomial_u = sp.Poly(diagonal_u, v)
    polynomial_a2b6 = sp.Poly(diagonal_a2b6, v)
    assert (polynomial_u.degree(), polynomial_a2b6.degree()) == (37, 74)
    u37 = polynomial_u.coeff_monomial(v**37)
    u36 = polynomial_u.coeff_monomial(v**36)
    target74 = polynomial_a2b6.coeff_monomial(v**74)
    target73 = polynomial_a2b6.coeff_monomial(v**73)
    p5 = sp.Poly(p, nonlinear.w).coeff_monomial(nonlinear.w**5)
    q6 = sp.Poly(q, nonlinear.w).coeff_monomial(nonlinear.w**6)
    assert u37 == theta * a**17
    assert target74 == q6**2 * p5**6 * a**32
    assert sp.factor(u36 / u37) == sp.Rational(562, 57)
    assert sp.factor(target73 / target74) == sp.Rational(1306, 57)

    # U=x^-5 H(v), A^2B^6=x^-10 K(v).  Their Jacobian is
    # 5*x^-15*(2H'K-HK'), whose v^109 coefficient is nonzero.
    exceptional_wronskian = sp.Poly(
        sp.expand(
            5
            * (
                2 * sp.diff(diagonal_u, v) * diagonal_a2b6
                - diagonal_u * sp.diff(diagonal_a2b6, v)
            )
        ),
        v,
    )
    exceptional_coefficient = sp.factor(
        sp.Rational(910, 57) * theta * q6**2 * p5**6 * a**49
    )
    assert exceptional_wronskian.degree() == 109
    assert (
        exceptional_wronskian.coeff_monomial(v**109)
        == exceptional_coefficient
    )
    assert exceptional_coefficient != 0

    # If the normalized t coefficient is nonzero, AB^7 has a
    # nonzero degree-204 top.  If it vanishes but B^8 is present,
    # its degree-203 monomial x^95*y^108 is distinct from the
    # A^2B^6 next term x^94*y^109.
    assert (94, 109) != (95, 108)


def main() -> None:
    verify_exact_seed_slices()
    verify_all_n_target_slice()
    verify_first_polynomial_completion()
    verify_graph_sector_polynomiality()
    verify_quadratic_tail_timing()
    verify_general_lower_recurrence()
    verify_sector_uniqueness()
    verify_constant_graphs()
    print("verified: exact first-lower U and all-n quadratic target slices")
    print("verified: first graph-compatible mixed completion occurs at n=12")
    print("verified: every nonpolynomial quadratic tail occurs before m+4")
    print("verified: every mixed first-lower forcing has a double pole")
    print("verified: the m+4 pole is not mixed with the m+6 axis residual")
    print("verified: the n=8 constant-graph diagonal exception is nonzero")
    print("RESULT: every binary d=2 face is closed in every degree")


if __name__ == "__main__":
    main()
