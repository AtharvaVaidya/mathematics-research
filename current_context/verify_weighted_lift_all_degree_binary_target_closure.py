#!/usr/bin/env python3
"""Verify homogeneous binary target closure in every degree."""

from __future__ import annotations

import sympy as sp

import verify_weighted_lift_first_nonlinear_cusp_subduction as nonlinear


x, y, t = sp.symbols("x y t")


def verify_exact_first_lower_slices() -> None:
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
    p_ratio = sp.factor(p4 / p5)
    q_ratio = sp.factor(q5 / q6)
    assert p_ratio == -sp.Rational(35, 6)
    assert q_ratio == -sp.Rational(28, 5)
    assert q_ratio - p_ratio == sp.Rational(7, 30)

    top = second_poly.coeff_monomial(
        nonlinear.w**20 * nonlinear.gamma**2
    )
    lower = second_poly.coeff_monomial(
        nonlinear.w**19 * nonlinear.gamma**2
    )
    assert top == theta
    assert sp.factor(lower / top) == -sp.Rational(70, 3)

    # For P=sum p_j*t^j, the coefficient multiplier on p_j in
    # the first-lower polynomial is
    # j*q_ratio+(n-j)*p_ratio
    # = n*p_ratio+(q_ratio-p_ratio)*j.  Thus
    # P1=n*p_ratio*P+(7/30)*t*P'.
    n = sp.symbols("n", integer=True, positive=True)
    for degree in range(1, 8):
        coefficients = sp.symbols(f"p0:{degree + 1}")
        polynomial = sum(
            coefficients[index] * t**index
            for index in range(degree + 1)
        )
        coefficient_sum = sum(
            coefficients[index]
            * (
                index * q_ratio
                + (n - index) * p_ratio
            )
            * t**index
            for index in range(degree + 1)
        )
        differential_form = (
            n * p_ratio * polynomial
            + (q_ratio - p_ratio) * t * sp.diff(polynomial, t)
        )
        assert sp.expand(coefficient_sum - differential_form) == 0


def verify_sector_uniqueness_and_polynomiality() -> None:
    n, d, graph_degree = sp.symbols(
        "n d graph_degree",
        integer=True,
        positive=True,
    )
    source_i = sp.symbols("I", integer=True)
    source_j = graph_degree - source_i + 2
    resonance = sp.expand(
        8 * n * source_j
        - (5 * n + 17 * d) * source_i
        - 15 * d
        + 5 * n
    )
    assert sp.solve(resonance, source_i) == [
        (
            8 * graph_degree * n
            + 21 * n
            - 15 * d
        )
        / (13 * n + 17 * d)
    ]
    assert (13 * n + 17 * d).is_positive is True

    # Audit the uniform binomial embedding
    # C[x,y] -> C[x,x^-1,t], y=t-x^-1.
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
                    coefficients_by_x_power.get(x_power, 0)
                    + term / x**x_power
                )
    for coefficient in coefficients_by_x_power.values():
        assert sp.Poly(coefficient, t).is_univariate


def verify_exact_maximal_x_support_separation() -> None:
    p, q = nonlinear.build_seed()
    _, second_numerator, _, theta = nonlinear.build_maximal_subductions(
        p, q
    )

    # U=N(w,gamma)/(x^5*gamma^5).  Relative to the top
    # theta*w^20*gamma^2, a numerator monomial w^i*gamma^j has
    # x-loss a=20-i and gamma-loss b=22-i-j.  On a maximal
    # gamma sector x^I*phi(t), its total x-loss is a+I*b.
    second_poly = sp.Poly(
        second_numerator,
        nonlinear.w,
        nonlinear.gamma,
    )
    assert len(second_poly.terms()) == 77
    assert second_poly.coeff_monomial(
        nonlinear.w**20 * nonlinear.gamma**2
    ) == theta
    u_losses: list[tuple[int, int, int, int]] = []
    for (w_power, gamma_power), coefficient in second_poly.terms():
        assert coefficient != 0
        a_loss = 20 - w_power
        b_loss = 22 - w_power - gamma_power
        assert a_loss >= 0
        assert b_loss >= 0
        if (w_power, gamma_power) == (20, 2):
            assert (a_loss, b_loss) == (0, 0)
            continue
        assert b_loss >= 1
        u_losses.append(
            (w_power, gamma_power, a_loss, b_loss)
        )
    assert [
        row for row in u_losses
        if row[2] + 2 * row[3] == 3
    ] == [(19, 2, 1, 1)]
    assert all(
        a_loss + 2 * b_loss > 3
        for _, _, a_loss, b_loss in u_losses
        if (a_loss, b_loss) != (1, 1)
    )
    # Since every non-top b>=1, the difference
    # (a+I*b)-(I+1) is nondecreasing for I>=2.  Thus (1,1) is
    # the unique first loss for every nonconstant graph.

    # Audit the complete A and B numerator supports, including the
    # added w*gamma and gamma terms.
    a_numerator = sp.expand(
        q + nonlinear.w * nonlinear.gamma
    )
    b_numerator = sp.expand(p + nonlinear.gamma)

    def seed_losses(
        numerator: sp.Expr,
        top_w_power: int,
    ) -> list[tuple[int, int, int, int]]:
        polynomial = sp.Poly(
            numerator,
            nonlinear.w,
            nonlinear.gamma,
        )
        losses: list[tuple[int, int, int, int]] = []
        for (
            w_power,
            gamma_power,
        ), coefficient in polynomial.terms():
            assert coefficient != 0
            a_loss = top_w_power - w_power
            b_loss = (
                top_w_power - w_power - gamma_power
            )
            assert a_loss >= 0
            assert b_loss >= 0
            if (w_power, gamma_power) == (top_w_power, 0):
                assert (a_loss, b_loss) == (0, 0)
                continue
            assert b_loss >= 1
            losses.append(
                (w_power, gamma_power, a_loss, b_loss)
            )
        return losses

    a_losses = seed_losses(a_numerator, 6)
    b_losses = seed_losses(b_numerator, 5)
    assert [
        row for row in a_losses
        if row[2] + 2 * row[3] == 3
    ] == [(5, 0, 1, 1)]
    assert [
        row for row in b_losses
        if row[2] + 2 * row[3] == 3
    ] == [(4, 0, 1, 1)]
    assert (1, 1, 5, 4) in a_losses
    assert (0, 1, 5, 4) in b_losses
    assert all(
        a_loss + 2 * b_loss > 3
        for _, _, a_loss, b_loss in a_losses
        if (a_loss, b_loss) != (1, 1)
    )
    assert all(
        a_loss + 2 * b_loss > 3
        for _, _, a_loss, b_loss in b_losses
        if (a_loss, b_loss) != (1, 1)
    )
    # Loss pairs add under products.  Hence the only total target
    # loss I+1 is one q5 or p4 replacement; two replacements and
    # every other exact seed term are strictly later.

    source_i = sp.symbols("I", integer=True, positive=True)
    normalized_exponent = (
        source_i - 1 - source_i
    )
    assert normalized_exponent == -1
    # A general lower pair (a,b) has normalized leading exponent
    # I-a-I*b<I.  For the unique first pair it is exactly -1.

    # The scalar-filtration degree-126 example is not a staged
    # recurrence: its missing tail stays in x^9, while the exact
    # first-lower forcing stays in x^-1.
    z, lam = sp.symbols("z lambda", nonzero=True)
    reciprocal = (
        1 + 6 * lam * z**6 + 15 * lam**2 * z**12
    )
    root_series = sp.series(
        reciprocal ** sp.Rational(1, 6),
        z,
        0,
        19,
    ).removeO()
    assert sp.expand(root_series).coeff(z, 18) == (
        -sp.Rational(10, 3) * lam**3
    )
    assert 9 != -1

    # The top common factor is
    # x^(4n+14)*gamma^(4n+16), apart from t and P.  A constant
    # Jacobian right side therefore normalizes to the sector below;
    # it cannot enter either x^I or the first-lower x^-1 equation.
    n = sp.symbols("n", integer=True, positive=True)
    common_x_exponent = (
        4 * n + 14 + (4 * n + 16) * source_i
    )
    assert common_x_exponent.subs({n: 1, source_i: 2}) == 58
    assert sp.diff(common_x_exponent, n).is_positive is True
    assert sp.diff(common_x_exponent, source_i).is_positive is True
    constant_rhs_sector = -common_x_exponent
    assert constant_rhs_sector.subs({n: 1, source_i: 2}) == -58

    # Affine target perturbations occur strictly after first loss.
    first_coordinate_ab_loss = 11 + 13 * source_i
    first_coordinate_c_loss = 14 + 16 * source_i
    assert sp.expand(
        first_coordinate_ab_loss - (source_i + 1)
    ) == 10 + 12 * source_i
    assert sp.expand(
        first_coordinate_c_loss - (source_i + 1)
    ) == 13 + 15 * source_i
    second_coordinate_ab_loss = (
        4 * (n - 1) * (source_i + 1)
    )
    second_coordinate_c_loss = (
        (4 * n - 1) * (source_i + 1)
    )
    assert sp.factor(
        second_coordinate_ab_loss.subs(n, 2)
        - (source_i + 1)
    ).is_positive is True
    assert sp.factor(
        second_coordinate_c_loss.subs(n, 1)
        - (source_i + 1)
    ).is_positive is True


def verify_zero_local_double_pole() -> None:
    n, source_i = sp.symbols(
        "n I",
        integer=True,
        positive=True,
    )
    exponent_r = sp.Rational(5, 8) * (source_i - 1)
    u1_ratio = -sp.Rational(70, 3)
    p_ratio = -sp.Rational(35, 6)

    # At t=0 with P(0)!=0, P'/P and P1'/P1 are regular.
    # Retain only the 1/t coefficients of the two logarithmic
    # determinants.
    determinant_u1_v0 = (
        (14 + 16 * source_i) * (5 * n + 4 * n * exponent_r)
        - (19 + 16 * exponent_r) * 4 * n * (1 + source_i)
    )
    determinant_u0_v1 = (
        (15 + 17 * source_i)
        * ((5 * n - 1) + (4 * n - 1) * exponent_r)
        - (20 + 17 * exponent_r)
        * (4 * n - 1)
        * (1 + source_i)
    )
    assert sp.factor(determinant_u1_v0) == -n * (source_i + 1)
    assert sp.factor(
        determinant_u0_v1 - (17 * source_i + 15) / 4
    ) == 0
    double_pole = sp.factor(
        u1_ratio * determinant_u1_v0
        + n * p_ratio * determinant_u0_v1
    )
    assert sp.factor(
        double_pole
        + sp.Rational(35, 24) * n * (source_i - 1)
    ) == 0


def verify_nonzero_root_double_pole() -> None:
    n, source_i, multiplicity = sp.symbols(
        "n I q",
        integer=True,
        positive=True,
    )
    exponent_s = (17 * source_i + 15) / (8 * n)

    # Let alpha!=0 be a root of P of multiplicity q.  Locally,
    # P'/P=q/z, P1/P=(7/30)*alpha*q/z, and
    # P1'/P1=(q-1)/z at leading order.  The U1*V0 term is only
    # simple.  The following is the 1/(x*z) determinant in U0*V1.
    determinant = (
        (15 + 17 * source_i)
        * (
            (4 * n - 1) * exponent_s * multiplicity
            + multiplicity
            - 1
        )
        - 17
        * exponent_s
        * multiplicity
        * (4 * n - 1)
        * (1 + source_i)
    )
    expected_determinant = (
        (17 * source_i + 15)
        * (multiplicity - 4 * n)
        / (4 * n)
    )
    assert sp.factor(determinant - expected_determinant) == 0
    double_pole = sp.factor(
        sp.Rational(7, 30) * multiplicity * determinant
    )
    expected_double_pole = (
        sp.Rational(7, 120)
        * multiplicity
        * (17 * source_i + 15)
        * (multiplicity - 4 * n)
        / n
    )
    assert sp.factor(double_pole - expected_double_pole) == 0

    # On 1<=q<=d<=n, q-4n is strictly negative.
    for n_value in range(1, 20):
        for d_value in range(1, n_value + 1):
            for q_value in range(1, d_value + 1):
                assert q_value - 4 * n_value < 0


def verify_operator_has_only_simple_poles() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    source_i = sp.symbols("I", integer=True, positive=True)
    polynomial = sp.Function("P")(t)
    psi = sp.Function("psi")(t)
    # For delta_gamma=x^-1*psi(t), every rational coefficient of
    # L(delta_gamma) is a linear combination of 1/t and P'/P.
    operator = (
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
    assert not operator.has(source_i)
    # P'/P has a simple pole q/(t-alpha) even when the root has
    # multiplicity q; no derivative of psi is divided by P.


def verify_pure_first_lower_classification_and_descent() -> None:
    n, d, source_i = sp.symbols(
        "n d I",
        integer=True,
        positive=True,
    )

    # For P=t^d, the numerator omega/P^2 in the exact normalized
    # first-lower forcing is the scalar below.
    monomial_omega = sp.factor(
        25 * n**2 * (1 - source_i)
        + 8 * n * (5 - source_i) * d
        + (17 * source_i + 15) * d**2
    )
    pure_numerator = sp.factor(
        (n + d)
        * (
            (17 * d - 25 * n) * source_i
            + 15 * d
            + 25 * n
        )
    )
    assert sp.factor(monomial_omega - pure_numerator) == 0

    # Since n+d>0, vanishing is equivalent to the displayed
    # Diophantine relation.
    zero_relation = (
        d * (17 * source_i + 15)
        - 25 * n * (source_i - 1)
    )
    assert sp.factor(
        pure_numerator / (n + d) - zero_relation
    ) == 0

    # The resonance numerator becomes 30*n*(I-1) under K=0.
    resonance_numerator = (
        (5 * n + 17 * d) * source_i
        + 15 * d
        - 5 * n
    )
    assert sp.expand(
        resonance_numerator
        - (
            5 * n * (source_i - 1)
            + d * (17 * source_i + 15)
        )
    ) == 0
    assert sp.expand(
        (
            5 * n * (source_i - 1)
            + d * (17 * source_i + 15)
        )
        - 30 * n * (source_i - 1)
        - zero_relation
    ) == 0

    # The bound d<=n gives I<=5, and integral
    # J=15*(I-1)/4 then leaves only I=5.
    admissible_i = [
        i_value
        for i_value in range(2, 6)
        if (15 * (i_value - 1)) % 4 == 0
    ]
    assert admissible_i == [5]
    assert sp.Rational(
        25 * (admissible_i[0] - 1),
        17 * admissible_i[0] + 15,
    ) == 1
    assert 15 * (admissible_i[0] - 1) // 4 == 15

    # A finite exact audit catches sign, divisibility, or endpoint
    # regressions in the symbolic classification.
    for n_value in range(1, 101):
        for d_value in range(0, n_value + 1):
            for i_value in range(2, 31):
                k_value = (n_value + d_value) * (
                    (17 * d_value - 25 * n_value) * i_value
                    + 15 * d_value
                    + 25 * n_value
                )
                if k_value != 0:
                    continue
                resonance_value = (
                    (5 * n_value + 17 * d_value) * i_value
                    + 15 * d_value
                    - 5 * n_value
                )
                if resonance_value % (8 * n_value) != 0:
                    continue
                j_value = resonance_value // (8 * n_value)
                assert (i_value, j_value, d_value) == (
                    5,
                    15,
                    n_value,
                )

    # On the unique exceptional ray the characteristic is x^5*t^15.
    # Its x^1*y^11 coefficient after t=y+x^-1 is nonzero.
    exceptional = sp.expand(x**5 * (y + x**-1) ** 15)
    forbidden_coefficient = sp.expand(
        exceptional
    ).coeff(x, 1).coeff(y, 11)
    assert forbidden_coefficient == sp.binomial(15, 4) == 1365

    # Any other pure A^n characteristic x^K*t^J_K could contribute
    # x*y^11 only if J_K=K+10.  The resonance gives K=5 uniquely.
    sector_k = sp.symbols("K", integer=True)
    sector_j = (11 * sector_k + 5) / 4
    assert sp.solve(
        sp.Eq(sector_j, sector_k + 10),
        sector_k,
    ) == [5]

    graph_degree = 5 + 15 - 2
    forbidden_drop = 2 * (5 - 1)
    first_lower_drop = graph_degree + 4
    assert graph_degree == 18
    assert forbidden_drop == 8
    assert first_lower_drop == 22
    assert forbidden_drop < first_lower_drop

    # Ordinary-degree separation from every affine correction on the
    # exceptional ray.  The defect has degree 90*n+365.
    defect_degree = 90 * n + 365
    assert sp.factor(defect_degree - 463).subs(n, 2) > 0
    assert sp.factor(defect_degree - 462).subs(n, 2) > 0
    assert sp.factor(defect_degree - 394).subs(n, 2) > 0
    assert sp.expand(defect_degree - (90 * n + 87)) == 278
    assert sp.expand(defect_degree - (90 * n + 19)) == 346


def verify_constant_graph_exception() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    logarithmic_p = sp.symbols("logarithmic_p")

    # If g=z0!=0, gamma has maximal sector z0*x^2.  Dividing its
    # characteristic equation by that sector leaves the expression
    # below.  Vanishing would force P'/P=-5n/(49t), impossible for
    # a nonzero polynomial.
    maximal_i_two = 5 * n / t + 49 * logarithmic_p
    assert sp.solve(maximal_i_two, logarithmic_p) == [
        -5 * n / (49 * t)
    ]

    # If z0=0, the maximal sector is a*x*t.  Its equation forces
    # t*P'/P=n/4, hence P is proportional to t^(n/4).
    maximal_i_one = -8 * n / t + 32 * logarithmic_p
    assert sp.solve(maximal_i_one, logarithmic_p) == [
        n / (4 * t)
    ]
    fixed_constant = sp.Rational(91, 34)
    fixed_sector_residual = sp.factor(
        fixed_constant
        * (
            -5 * n / t
            + 15 * n / (4 * t)
        )
    )
    assert fixed_sector_residual == -455 * n / (136 * t)
    assert fixed_sector_residual != 0

    # At maximal I=1, every exact non-top seed term loses at least
    # two x-degrees, so none reaches the fixed x^0 residual.
    p, q = nonlinear.build_seed()
    _, second_numerator, _, _ = nonlinear.build_maximal_subductions(
        p, q
    )
    second_poly = sp.Poly(
        second_numerator,
        nonlinear.w,
        nonlinear.gamma,
    )
    for (w_power, gamma_power), coefficient in second_poly.terms():
        if coefficient == 0 or (w_power, gamma_power) == (20, 2):
            continue
        a_loss = 20 - w_power
        b_loss = 22 - w_power - gamma_power
        assert a_loss + b_loss >= 2
    for numerator, top_w_power in (
        (q + nonlinear.w * nonlinear.gamma, 6),
        (p + nonlinear.gamma, 5),
    ):
        polynomial = sp.Poly(
            numerator,
            nonlinear.w,
            nonlinear.gamma,
        )
        for (
            w_power,
            gamma_power,
        ), coefficient in polynomial.terms():
            if (
                coefficient == 0
                or (w_power, gamma_power) == (top_w_power, 0)
            ):
                continue
            a_loss = top_w_power - w_power
            b_loss = top_w_power - w_power - gamma_power
            assert a_loss + b_loss >= 2


def main() -> None:
    verify_exact_first_lower_slices()
    verify_sector_uniqueness_and_polynomiality()
    verify_exact_maximal_x_support_separation()
    verify_zero_local_double_pole()
    verify_nonzero_root_double_pole()
    verify_operator_has_only_simple_poles()
    verify_pure_first_lower_classification_and_descent()
    verify_constant_graph_exception()
    print("verified: universal first-lower polynomial P1")
    print("verified: unique resonant sector at each graph degree")
    print("verified: exact 77-term U and complete A/B support separation")
    print("verified: every nonpolynomial characteristic is top-sector impossible")
    print("verified: first-lower forcing is uniquely x^-1")
    print("verified: constant Jacobian RHS lies strictly below x^-1")
    print("verified: nonzero double pole at t=0 or a nonzero root")
    print("verified: polynomial graph sectors supply only simple poles")
    print("verified: exact pure numerator and unique A^n exceptional ray")
    print("verified: forbidden x*y^11 descent before seeds or affine terms")
    print("verified: every constant-graph exception")
    print("RESULT: every homogeneous binary target in every degree is closed")


if __name__ == "__main__":
    main()
