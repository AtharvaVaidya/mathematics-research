#!/usr/bin/env python3
"""Compact exact form of the remaining case-c lower equations.

On a chart where H is polynomial and the fractional resonances have
vanished, the upper blocks have the form

    P_+ = H^2 + R,
    Q_+ = H^3 + (3/2)*H*R + c8*P_+ + c4*H + S,

with deg_y(R),deg_y(S)<=3.  This verifier proves the cancellation

    [P_+,Q_+] = [P_+,S] - ((3/2)*R+c4)*[H,R].

It also restores the fixed base blocks X=z*y^-1 and B=z^2*y^-1 and
checks the resulting exact residual formula.  This is a reduction of the
remaining equations, not a proof that R or S vanishes.
"""

from __future__ import annotations

import sympy as sp


def verify_lower_remainder_identity() -> dict[str, sp.Expr]:
    y, z = sp.symbols("y z")
    c8, c4 = sp.symbols("c8 c4")
    h_coefficients = sp.symbols("H0:5")
    r_coefficients = sp.symbols("R0:4")
    s_coefficients = sp.symbols("S0:4")
    dh_coefficients = sp.symbols("dH0:5")
    dr_coefficients = sp.symbols("dR0:4")
    ds_coefficients = sp.symbols("dS0:4")
    variables = h_coefficients + r_coefficients + s_coefficients
    derivatives = dh_coefficients + dr_coefficients + ds_coefficients

    H = sum(h_coefficients[index] * y**index for index in range(5))
    R = sum(r_coefficients[index] * y**index for index in range(4))
    S = sum(s_coefficients[index] * y**index for index in range(4))
    P_plus = sp.expand(H**2 + R)
    Q_plus = sp.expand(
        H**3
        + sp.Rational(3, 2) * H * R
        + c8 * P_plus
        + c4 * H
        + S
    )

    def derivative(expression: sp.Expr) -> sp.Expr:
        return sp.expand(
            sp.diff(expression, z)
            + sum(
                sp.diff(expression, variable) * differential
                for variable, differential in zip(
                    variables, derivatives
                )
            )
        )

    def bracket(left: sp.Expr, right: sp.Expr) -> sp.Expr:
        # This is the compressed case-c bracket
        # y*(left_z*right_y-left_y*right_z).
        return sp.expand(
            y
            * (
                derivative(left) * sp.diff(right, y)
                - sp.diff(left, y) * derivative(right)
            )
        )

    upper = sp.expand(bracket(P_plus, Q_plus))
    reduced_upper = sp.expand(
        bracket(P_plus, S)
        - (sp.Rational(3, 2) * R + c4) * bracket(H, R)
    )
    assert sp.expand(upper - reduced_upper) == 0

    X = z / y
    B = z**2 / y
    full_residual = sp.expand(
        bracket(X + P_plus, B + Q_plus) - z**2 / y**2
    )
    reduced_full = sp.expand(
        bracket(X, Q_plus)
        + bracket(P_plus, B)
        + reduced_upper
    )
    assert sp.expand(full_residual - reduced_full) == 0

    # The bottom E_-1 identity is retained exactly.  It is the
    # coefficient of y^-1 in the two base cross-terms.
    p0 = sp.Poly(P_plus, y).coeff_monomial(1)
    q0 = sp.Poly(Q_plus, y).coeff_monomial(1)
    bottom = sp.expand(full_residual.coeff(y, -1))
    expected_bottom = sp.expand(
        z * derivative(q0) - z**2 * derivative(p0)
    )
    assert sp.expand(bottom - expected_bottom) == 0
    return {
        "upper_reduction": reduced_upper,
        "full_reduction": reduced_full,
        "bottom": bottom,
    }


def verify_top_remainder_row() -> dict[str, sp.Expr]:
    """Solve the E11 equation for sigma3=[y^3]S."""
    h, t, kappa = sp.symbols("h t kappa")
    sigma3 = (
        kappa * h**3
        + sp.Rational(3, 2) * t * h**4
        + sp.Rational(3, 2) * h**5
    )
    top_row = sp.expand(
        (h + t) * sp.diff(h**12, h)
        + 12 * h**12
        + 3 * sp.diff(h**8, h) * sigma3
        - 8 * h**8 * sp.diff(sigma3, h)
    )
    assert top_row == 0

    # Converse over the polynomial ring: on a monomial a_n*h^n, the
    # sigma part of E11 is 8*(3-n)*a_n*h^(n+7).  Hence n=3 is the only
    # kernel degree; the h^11 and h^12 target terms uniquely give the
    # displayed n=4,5 coefficients.
    coefficients = sp.symbols("a0:13")
    generic = sum(
        coefficients[index] * h**index for index in range(13)
    )
    generic_row = sp.Poly(
        sp.expand(
            (h + t) * sp.diff(h**12, h)
            + 12 * h**12
            + 3 * sp.diff(h**8, h) * generic
            - 8 * h**8 * sp.diff(generic, h)
        ),
        h,
    )
    for index in range(13):
        if index == 3:
            continue
        expected = sp.Integer(0)
        if index == 4:
            expected = sp.Rational(3, 2) * t
        elif index == 5:
            expected = sp.Rational(3, 2)
        equation_degree = index + 7
        equation = generic_row.coeff_monomial(h**equation_degree)
        assert sp.solve(equation, coefficients[index]) == [expected]
    assert generic_row.as_expr().coeff(coefficients[3]) == 0
    return {
        "sigma3": sigma3,
        "E11": top_row,
    }


def verify_terminal_euler_lemma() -> dict[str, sp.Expr]:
    """Check the arbitrary-order highest-grade Euler operator.

    If a formal centralizer and Q first differ in degree y^-m, only
    p8=h^8 can contribute to the highest bracket grade 8-m.  On a
    Laurent monomial n_k*h^k*y^-m the resulting multiplier is
    -8*(m+k).  Thus the unique Laurent resonance is h^-m; there is no
    polynomial resonance for m>0.
    """
    h, m, k, n_k = sp.symbols(
        "h m k n_k", integer=True
    )
    coefficient = n_k * h**k
    operator = sp.expand(
        -m * sp.diff(h**8, h) * coefficient
        - 8 * h**8 * sp.diff(coefficient, h)
    )
    expected = -8 * (m + k) * n_k * h ** (k + 7)
    assert sp.simplify(operator - expected) == 0

    # At m=10 the bracket target is z^2=(h+t)^2.  It is wholly
    # nonresonant: the missing output monomial is h^(7-m)=h^-3.
    t, lambda10 = sp.symbols("t lambda10")
    target_particular = (
        -sp.Rational(1, 40) * h**-5
        - t * h**-6 / 16
        - t**2 * h**-7 / 24
        + lambda10 * h**-10
    )
    target_row = sp.expand(
        -10 * sp.diff(h**8, h) * target_particular
        - 8 * h**8 * sp.diff(target_particular, h)
    )
    assert sp.expand(target_row - (h + t) ** 2) == 0

    # The vertex-compatible terminal witness below is not a solution.
    # For R=c4=0 its first omitted formal coefficient is at y^-6.
    witness_n6 = -sp.Rational(3, 8) * (h + t) ** 2 / h**4
    witness_e2 = sp.expand(
        -6 * sp.diff(h**8, h) * witness_n6
        - 8 * h**8 * sp.diff(witness_n6, h)
    )
    assert sp.factor(witness_e2) == (
        6 * h**3 * (h + t) * (2 * h + t)
    )
    return {
        "operator": operator,
        "multiplier": -8 * (m + k),
        "resonance_degree": -m,
        "target_particular": target_particular,
        "target_cokernel_degree": sp.Integer(-3),
        "terminal_witness_E2": witness_e2,
    }


def verify_negative_tail_obstruction() -> dict[str, sp.Expr]:
    """Close the normalized negative formal tail on the r0-unit chart.

    Subtracting scalar multiples of P^(-m/8) removes the unique
    homogeneous resonance at each order m.  After orders 1,...,9 have
    been normalized away, the target at order 10 fixes n10 modulo its
    h^-10 resonance.  Removing that resonance leaves an unavoidable
    cokernel coefficient in the next order.
    """
    h, t, lambda10 = sp.symbols("h t lambda10")
    r = sp.symbols("r0:5")
    p7 = h**4 * sum(r[index] * h**index for index in range(5))
    n10 = (
        -sp.Rational(1, 40) * h**-5
        - t * h**-6 / 16
        - t**2 * h**-7 / 24
        + lambda10 * h**-10
    )

    target_row = sp.expand(
        -10 * sp.diff(h**8, h) * n10
        - 8 * h**8 * sp.diff(n10, h)
    )
    assert sp.expand(target_row - (h + t) ** 2) == 0

    # At grade -3, only (p8,n11) and (p7,n10) remain.  The p8
    # operator on h^k has multiplier -8*(11+k) and therefore misses
    # h^-4 (the image corresponding to its h^-11 kernel).
    next_forcing = sp.expand(
        -10 * sp.diff(p7, h) * n10
        - 7 * p7 * sp.diff(n10, h)
    )
    obstruction = sp.factor(next_forcing.coeff(h, -4))
    assert obstruction == -sp.Rational(3, 8) * r[0] * t**2
    assert not obstruction.has(lambda10)
    return {
        "n10": n10,
        "next_forcing": next_forcing,
        "cokernel_obstruction": obstruction,
    }


def verify_weighted_residue_obstruction() -> dict[str, sp.Expr]:
    """Package the tail cokernel as a weighted-face residue.

    If r_j is the first nonzero coefficient of r, put
    q=T/h^(4-j).  On the relevant square face,

        P_face=h^(8*j-24)*p(q),  p=q^-8*a(q)^2.

    For a homogeneous target component, the mate equation has integrating
    factor p^alpha.  A q^-1 term in the resulting differential is the
    coordinate-free logarithmic obstruction; adding a function of P
    changes only the integration constant and cannot remove it.
    """
    q, t = sp.symbols("q t")
    r0, r2, s0 = sp.symbols("r0 r2 s0")

    # j=0: a=1+r0*q/2, D=24, beta=alpha-1=3/8.
    # The t^2 target gives (t^2/24)q^-2*a^(3/4)dq.
    residue_r0 = sp.expand(
        t**2
        / 24
        * sp.Rational(3, 4)
        * r0
        / 2
    )
    obstruction_r0 = sp.expand(-24 * residue_r0)
    assert obstruction_r0 == -sp.Rational(3, 8) * r0 * t**2

    # j=2: a=1+(r2/2)q+(s0/2)q^2, D=8, beta=5/8.
    # The residue is (t^2/8)[q^3]a^(5/4).
    c = r2 / 2
    d = s0 / 2
    a_q3 = (
        sp.Rational(5, 4) * sp.Rational(1, 4) * c * d
        + sp.binomial(sp.Rational(5, 4), 3) * c**3
    )
    residue_r2 = sp.factor(t**2 * a_q3 / 8)
    obstruction_r2 = sp.factor(-8 * residue_r2)
    assert obstruction_r2 == (
        5 * r2 * t**2 * (r2**2 - 16 * s0) / 1024
    )
    assert sp.factor(obstruction_r2.subs(s0, 0)) == (
        5 * r2**3 * t**2 / 1024
    )
    assert sp.factor(
        obstruction_r2.subs(s0, r2**2 / 8)
    ) == -5 * r2**3 * t**2 / 1024

    # j=1 has no logarithmic face residue for any of the three
    # h^2+2*t*h+t^2 target components.  In particular, the apparent
    # repeated-p7 resonance cancels against the mandatory p6 square
    # contribution.
    r1 = sp.symbols("r1")
    a1 = 1 + r1 * q / 2
    t_component_integrand = sp.expand(
        t * q**-3 * a1 / 8
    )
    assert t_component_integrand.coeff(q, -1) == 0
    return {
        "r0_residue": residue_r0,
        "r0_obstruction": obstruction_r0,
        "r2_residue": residue_r2,
        "r2_obstruction": obstruction_r2,
        "r1_t_residue": sp.Integer(0),
    }


def verify_r1_hyperelliptic_obstruction() -> dict[str, sp.Expr]:
    """Audit the nonresidue obstruction on the lowest-r1 face.

    The weighted face differential becomes a nonzero scalar multiple of
    x^14*dx/y^5 on y^2=x^8-1.  Hermite reduction leaves the nonexact
    second-kind class (7/16)*x^6*dx/y.
    """
    x = sp.symbols("x")
    f = x**8 - 1
    f_prime = sp.diff(f, x)
    r_term = -x**7 / 12
    s_term = -x**7 / 4

    # Put every differential over y^5, using y^2=f:
    # d(R/y^3)=(R'*f-(3/2)R*f')dx/y^5,
    # d(S/y)=(S'*f-(1/2)S*f')*f dx/y^5.
    exact_r = sp.diff(r_term, x) * f - sp.Rational(3, 2) * (
        r_term * f_prime
    )
    exact_s = (
        sp.diff(s_term, x) * f
        - sp.Rational(1, 2) * s_term * f_prime
    ) * f
    remainder = sp.Rational(7, 16) * x**6 * f**2
    assert sp.expand(
        exact_r + sp.Rational(7, 12) * exact_s + remainder - x**14
    ) == 0

    # At a finite branch point, x-a is a unit times y^2, so
    # x^6*dx/y is regular.  At either infinity u=1/x it starts with
    # +/-u^-4 du and has no u^-1 term.  If it were df, involution
    # averaging would give an anti-invariant primitive regular on the
    # affine curve, hence y*B(x) with B polynomial.  But for B=x^n:
    #
    # d(y*x^n)=((n+4)x^(n+7)-n*x^(n-1))*dx/y.
    #
    # Its leading degree is n+7>=7 and cannot produce x^6.
    n = sp.symbols("n", integer=True, nonnegative=True)
    monomial_numerator = sp.expand(
        n * x ** (n - 1) * f
        + sp.Rational(1, 2) * x**n * f_prime
    )
    assert sp.simplify(
        monomial_numerator
        - ((n + 4) * x ** (n + 7) - n * x ** (n - 1))
    ) == 0
    return {
        "curve": sp.Symbol("y") ** 2 - f,
        "hermite_remainder": sp.Rational(7, 16) * x**6,
        "primitive_monomial_numerator": monomial_numerator,
    }


def verify_next_remainder_row() -> dict[str, sp.Expr]:
    """Use E10 to kill the low coefficients of rho3 and kappa."""
    h, t, kappa = sp.symbols("h t kappa")
    r = sp.symbols("r0:5")
    u = sp.symbols("u0:7")
    v = sp.symbols("v0:10")
    r_poly = sum(r[index] * h**index for index in range(5))
    rho3 = sum(u[index] * h**index for index in range(7))
    sigma3 = (
        kappa * h**3
        + sp.Rational(3, 2) * t * h**4
        + sp.Rational(3, 2) * h**5
    )
    sigma2 = sum(v[index] * h**index for index in range(10))
    p7 = h**4 * r_poly
    q11 = sp.Rational(3, 2) * h**8 * r_poly

    # Degree ten of the compact residual:
    #   [X,Q+] contributes q11,
    #   [P+,S] contributes (p8,sigma2) and (p7,sigma3),
    #   -(3/2 R)[H,R] contributes its rho3 top term.
    equation10 = sp.expand(
        (h + t) * sp.diff(q11, h)
        + 11 * q11
        + 3 * sp.diff(p7, h) * sigma3
        - 7 * p7 * sp.diff(sigma3, h)
        + 2 * sp.diff(h**8, h) * sigma2
        - 8 * h**8 * sp.diff(sigma2, h)
        - 18 * h**3 * rho3**2
        + 6 * h**4 * rho3 * sp.diff(rho3, h)
    )
    expected_low = {
        3: -18 * u[0] ** 2,
        5: -12 * (2 * u[0] * u[2] + u[1] ** 2),
        6: -9
        * (
            kappa * r[0]
            + 2 * u[0] * u[3]
            + 2 * u[1] * u[2]
        ),
    }
    for degree, expected in expected_low.items():
        assert sp.expand(equation10.coeff(h, degree) - expected) == 0

    # The sigma2 Euler operator starts at h^7.  Thus the displayed low
    # rows first give u0=0, then u1=0, and finally kappa*r0=0.
    after_u0 = sp.factor(equation10.coeff(h, 5).subs(u[0], 0))
    after_u1 = sp.factor(
        equation10.coeff(h, 6).subs({u[0]: 0, u[1]: 0})
    )
    assert after_u0 == -12 * u[1] ** 2
    assert after_u1 == -9 * kappa * r[0]

    # The resonant h^9 coefficient of the sigma2 operator vanishes; the
    # remaining forcing satisfies that compatibility identically.
    assert equation10.coeff(h, 9) == 0
    return {
        "E10_h3": equation10.coeff(h, 3),
        "E10_h5_after_u0": after_u0,
        "E10_h6_after_u0_u1": after_u1,
    }


def verify_e9_remainder_row() -> dict[str, sp.Expr]:
    """Use the first E9 endpoint to prove h^3 divides rho3."""
    h, t, lam = sp.symbols("h t lambda")
    r = sp.symbols("r0:5")
    s = sp.symbols("s0:4")
    u = sp.symbols("u2:7")
    a = sp.symbols("a0:6")
    r_poly = sum(r[index] * h**index for index in range(5))
    s_poly = sum(s[index] * h**index for index in range(4))
    rho3 = sum(u[index - 2] * h**index for index in range(2, 7))
    rho2 = sum(a[index] * h**index for index in range(6))
    sigma3 = (
        sp.Rational(3, 2) * t * h**4
        + sp.Rational(3, 2) * h**5
    )

    # These are the h^7,h^8 solutions of E10 after u0=u1=kappa=0.
    sigma2_0 = sp.Rational(3, 8) * (
        2 * r[0] * t + u[0] ** 2
    )
    sigma2_1 = sp.Rational(3, 4) * (
        r[0] + r[1] * t + u[0] * u[1]
    )
    sigma2_3 = sp.Rational(3, 4) * (
        r[2] + r[3] * t + u[0] * u[3] + u[1] * u[2]
    )
    sigma2_4 = sp.Rational(3, 8) * (
        2 * r[3]
        + 2 * r[4] * t
        + 2 * u[0] * u[4]
        + 2 * u[1] * u[3]
        + u[2] ** 2
    )
    sigma2_5 = sp.Rational(3, 4) * (
        r[4] + u[1] * u[4] + u[2] * u[3]
    )
    sigma2_6 = sp.Rational(3, 8) * (
        2 * u[2] * u[4] + u[3] ** 2
    )
    sigma2_7 = sp.Rational(3, 4) * u[3] * u[4]
    sigma2_8 = sp.Rational(3, 8) * u[4] ** 2
    sigma2 = (
        sigma2_0
        + sigma2_1 * h
        + lam * h**2
        + sigma2_3 * h**3
        + sigma2_4 * h**4
        + sigma2_5 * h**5
        + sigma2_6 * h**6
        + sigma2_7 * h**7
        + sigma2_8 * h**8
    )

    p8 = h**8
    p7 = h**4 * r_poly
    p6 = r_poly**2 / 4 + h**4 * s_poly
    q10 = (
        sp.Rational(3, 4) * h**4 * r_poly**2
        + sp.Rational(3, 2) * h**8 * s_poly
    )
    bracket7 = (
        3 * sp.diff(h**4, h) * rho3
        - 4 * h**4 * sp.diff(rho3, h)
    )
    h3 = r_poly / 2
    bracket6 = (
        3 * sp.diff(h3, h) * rho3
        - 3 * h3 * sp.diff(rho3, h)
        + 2 * sp.diff(h**4, h) * rho2
        - 4 * h**4 * sp.diff(rho2, h)
    )

    # The sigma1 Euler operator begins at h^7, so it cannot change the
    # h^3 or h^5 coefficients used below.
    equation9_low = sp.expand(
        (h + t) * sp.diff(q10, h)
        + 10 * q10
        + 3 * sp.diff(p6, h) * sigma3
        - 6 * p6 * sp.diff(sigma3, h)
        + 2 * sp.diff(p7, h) * sigma2
        - 7 * p7 * sp.diff(sigma2, h)
        - sp.Rational(3, 2)
        * (rho2 * bracket7 + rho3 * bracket6)
    )
    endpoint = sp.factor(equation9_low.coeff(h, 3))
    assert endpoint == sp.Rational(15, 2) * r[0] * u[0] ** 2

    next_row = sp.factor(
        equation9_low.coeff(h, 5).subs(u[0], 0)
    )
    expected_next = (
        sp.Rational(3, 4)
        * r[0]
        * (
            -8 * lam
            + 6 * r[1]
            + 6 * r[2] * t
            + 9 * u[1] ** 2
        )
    )
    assert sp.expand(next_row - expected_next) == 0
    lambda_value = (
        6 * r[1] + 6 * r[2] * t + 9 * u[1] ** 2
    ) / 8
    assert sp.expand(next_row.subs(lam, lambda_value)) == 0
    resonance = sp.factor(
        equation9_low.coeff(h, 8).subs(
            {u[0]: 0, lam: lambda_value}
        )
    )
    assert resonance == 0
    tau2_forcing = sp.factor(
        equation9_low.coeff(h, 9).subs(
            {
                u[0]: 0,
                u[1]: 0,
                lam: lambda_value.subs(u[1], 0),
            }
        )
    )
    tau2_value = sp.factor(tau2_forcing / 8)
    expected_tau2 = (
        sp.Rational(3, 16)
        * (
            4 * a[0] * u[4]
            + 4 * a[1] * u[3]
            + 4 * a[2] * u[2]
            - 2 * r[0] * u[2] * u[4]
            - r[0] * u[3] ** 2
            - 2 * r[1] * u[2] * u[3]
            - r[2] * u[2] ** 2
            + 4 * s[1]
            + 4 * s[2] * t
        )
    )
    assert sp.expand(tau2_value - expected_tau2) == 0
    tau3_forcing = sp.factor(
        equation9_low.coeff(h, 10).subs(
            {
                u[0]: 0,
                u[1]: 0,
                lam: lambda_value.subs(u[1], 0),
            }
        )
    )
    tau3_value = sp.factor(tau3_forcing / 16)
    expected_tau3 = (
        sp.Rational(3, 16)
        * (
            4 * a[1] * u[4]
            + 4 * a[2] * u[3]
            + 4 * a[3] * u[2]
            - 2 * r[0] * u[3] * u[4]
            - 2 * r[1] * u[2] * u[4]
            - r[1] * u[3] ** 2
            - 2 * r[2] * u[2] * u[3]
            - r[3] * u[2] ** 2
            + 4 * s[2]
            + 4 * s[3] * t
        )
    )
    assert sp.expand(tau3_value - expected_tau3) == 0
    tau4_forcing = sp.factor(
        equation9_low.coeff(h, 11).subs(
            {
                u[0]: 0,
                u[1]: 0,
                lam: lambda_value.subs(u[1], 0),
            }
        )
    )
    tau4_value = sp.factor(tau4_forcing / 24)
    expected_tau4 = (
        sp.Rational(3, 16)
        * (
            4 * a[2] * u[4]
            + 4 * a[3] * u[3]
            + 4 * a[4] * u[2]
            - r[0] * u[4] ** 2
            - 2 * r[1] * u[3] * u[4]
            - 2 * r[2] * u[2] * u[4]
            - r[2] * u[3] ** 2
            - 2 * r[3] * u[2] * u[3]
            - r[4] * u[2] ** 2
            + 4 * s[3]
        )
    )
    assert sp.expand(tau4_value - expected_tau4) == 0
    tau5_forcing = sp.factor(
        equation9_low.coeff(h, 12).subs(
            {
                u[0]: 0,
                u[1]: 0,
                lam: lambda_value.subs(u[1], 0),
            }
        )
    )
    tau5_value = sp.factor(tau5_forcing / 32)
    expected_tau5 = (
        sp.Rational(3, 16)
        * (
            4 * a[3] * u[4]
            + 4 * a[4] * u[3]
            + 4 * a[5] * u[2]
            - r[1] * u[4] ** 2
            - 2 * r[2] * u[3] * u[4]
            - 2 * r[3] * u[2] * u[4]
            - r[3] * u[3] ** 2
            - 2 * r[4] * u[2] * u[3]
        )
    )
    assert sp.expand(tau5_value - expected_tau5) == 0
    tau6_forcing = sp.factor(
        equation9_low.coeff(h, 13).subs(
            {
                u[0]: 0,
                u[1]: 0,
                lam: lambda_value.subs(u[1], 0),
            }
        )
    )
    tau6_value = sp.factor(tau6_forcing / 40)
    expected_tau6 = (
        sp.Rational(3, 16)
        * (
            4 * a[4] * u[4]
            + 4 * a[5] * u[3]
            - r[2] * u[4] ** 2
            - 2 * r[3] * u[3] * u[4]
            - 2 * r[4] * u[2] * u[4]
            - r[4] * u[3] ** 2
        )
    )
    assert sp.expand(tau6_value - expected_tau6) == 0
    tau7_forcing = sp.factor(
        equation9_low.coeff(h, 14).subs(
            {
                u[0]: 0,
                u[1]: 0,
                lam: lambda_value.subs(u[1], 0),
            }
        )
    )
    tau7_value = sp.factor(tau7_forcing / 48)
    expected_tau7 = (
        sp.Rational(3, 16)
        * u[4]
        * (
            4 * a[5]
            - r[3] * u[4]
            - 2 * r[4] * u[3]
        )
    )
    assert sp.expand(tau7_value - expected_tau7) == 0
    tau8_forcing = sp.factor(
        equation9_low.coeff(h, 15).subs(
            {
                u[0]: 0,
                u[1]: 0,
                lam: lambda_value.subs(u[1], 0),
            }
        )
    )
    tau8_value = sp.factor(tau8_forcing / 56)
    expected_tau8 = -sp.Rational(3, 16) * r[4] * u[4] ** 2
    assert sp.expand(tau8_value - expected_tau8) == 0
    assert equation9_low.coeff(h, 16) == 0
    return {
        "E9_h3": endpoint,
        "E9_h5_after_u2": next_row,
        "lambda_value": lambda_value,
        "E9_h8_after_u2": resonance,
        "tau2_value": tau2_value,
        "tau3_value": tau3_value,
        "tau4_value": tau4_value,
        "tau5_value": tau5_value,
        "tau6_value": tau6_value,
        "tau7_value": tau7_value,
        "tau8_value": tau8_value,
    }


def verify_e8_remainder_row() -> dict[str, sp.Expr]:
    """Use E8[h] to prove h^4 divides rho3."""
    h, t, mu = sp.symbols("h t mu")
    r = sp.symbols("r0:5")
    s = sp.symbols("s0:4")
    w = sp.symbols("w0:3")
    u = sp.symbols("u3:7")
    a = sp.symbols("a0:6")
    b = sp.symbols("b0:5")
    d = sp.symbols("d0:5")
    v = sp.symbols("v0:3")
    g = sp.symbols("g0:7")
    c8, c4 = sp.symbols("c8 c4")
    r_poly = sum(r[index] * h**index for index in range(5))
    s_poly = sum(s[index] * h**index for index in range(4))
    w_poly = sum(w[index] * h**index for index in range(3))
    rho3 = sum(u[index - 3] * h**index for index in range(3, 7))
    rho2 = sum(a[index] * h**index for index in range(6))
    rho1 = sum(b[index] * h**index for index in range(5))
    rho0 = sum(d[index] * h**index for index in range(5))
    h0 = sum(v[index] * h**index for index in range(3)) / 2
    sigma0 = sum(g[index] * h**index for index in range(7))
    sigma3 = (
        sp.Rational(3, 2) * t * h**4
        + sp.Rational(3, 2) * h**5
    )

    # E10 fixes these coefficients, and E9 fixes the h^2 resonance.
    sigma2 = (
        sp.Rational(3, 4) * r[0] * t
        + sp.Rational(3, 4) * (r[0] + r[1] * t) * h
        + (
            6 * r[1] + 6 * r[2] * t + 9 * u[0] ** 2
        )
        * h**2
        / 8
        + sp.Rational(3, 4)
        * (r[2] + r[3] * t + u[0] * u[1])
        * h**3
        + sp.Rational(3, 8)
        * (
            2 * r[3]
            + 2 * r[4] * t
            + 2 * u[0] * u[2]
            + u[1] ** 2
        )
        * h**4
        + sp.Rational(3, 4)
        * (
            r[4]
            + u[0] * u[3]
            + u[1] * u[2]
        )
        * h**5
        + sp.Rational(3, 8)
        * (
            2 * u[1] * u[3]
            + u[2] ** 2
        )
        * h**6
        + sp.Rational(3, 4) * u[2] * u[3] * h**7
        + sp.Rational(3, 8) * u[3] ** 2 * h**8
    )

    p5 = r_poly * s_poly / 2 + h**4 * w_poly
    p6 = r_poly**2 / 4 + h**4 * s_poly
    q9 = (
        r_poly**3 / 8
        + sp.Rational(3, 2) * h**4 * r_poly * s_poly
        + sp.Rational(3, 2) * h**8 * w_poly
    )
    h2 = s_poly / 2
    h3 = r_poly / 2
    bracket7 = (
        3 * sp.diff(h**4, h) * rho3
        - 4 * h**4 * sp.diff(rho3, h)
    )
    bracket6 = (
        3 * sp.diff(h3, h) * rho3
        - 3 * h3 * sp.diff(rho3, h)
        + 2 * sp.diff(h**4, h) * rho2
        - 4 * h**4 * sp.diff(rho2, h)
    )
    bracket5 = (
        3 * sp.diff(h2, h) * rho3
        - 2 * h2 * sp.diff(rho3, h)
        + 2 * sp.diff(h3, h) * rho2
        - 3 * h3 * sp.diff(rho2, h)
        + sp.diff(h**4, h) * rho1
        - 4 * h**4 * sp.diff(rho1, h)
    )

    # The sigma1 and sigma0 operators begin at h^4 and h^8 in E8, so
    # they cannot alter the h^1 endpoint.
    equation8_low = sp.expand(
        (h + t) * sp.diff(q9, h)
        + 9 * q9
        + 3 * sp.diff(p5, h) * sigma3
        - 5 * p5 * sp.diff(sigma3, h)
        + 2 * sp.diff(p6, h) * sigma2
        - 6 * p6 * sp.diff(sigma2, h)
        - sp.Rational(3, 2)
        * (
            rho1 * bracket7
            + rho2 * bracket6
            + rho3 * bracket5
        )
    )
    endpoint = sp.factor(equation8_low.coeff(h, 1))
    assert endpoint == (
        -sp.Rational(27, 8) * r[0] ** 2 * u[0] ** 2
    )
    # E9[h^7] fixes the constant coefficient of sigma1.  It first
    # enters E8 at h^3 and must be restored before reading the rho2 row.
    tau0 = sp.Rational(3, 16) * (
        4 * a[0] * u[1]
        - r[0] * u[1] ** 2
        + 4 * s[0] * t
    )
    p7 = h**4 * r_poly
    sigma1 = tau0 + mu * h
    sigma1_contribution = sp.expand(
        sp.diff(p7, h) * sigma1
        - 7 * p7 * sp.diff(sigma1, h)
    )
    rho2_boundary = sp.factor(
        (
            equation8_low
            + sigma1_contribution
        ).coeff(h, 3).subs(u[0], 0)
    )
    expected_boundary = -3 * (
        2 * a[0] - r[0] * u[1]
    ) ** 2
    assert sp.expand(rho2_boundary - expected_boundary) == 0

    # Impose a0=r0*u4/2.  The h^5 coefficient of sigma2 cancels the
    # apparent r4+u4*u5 terms; the next E8 row fixes mu.
    closed = {
        u[0]: 0,
        a[0]: r[0] * u[1] / 2,
    }
    mu_row = sp.factor(
        (
            equation8_low
            + sigma1_contribution
        ).coeff(h, 4).subs(closed)
    )
    expected_mu_row = (
        sp.Rational(3, 16)
        * r[0]
        * (
            12 * a[1] * u[1]
            - 16 * mu
            - 3 * r[1] * u[1] ** 2
            + 12 * s[0]
            + 12 * s[1] * t
        )
    )
    assert sp.expand(mu_row - expected_mu_row) == 0
    mu_value = (
        12 * a[1] * u[1]
        - 3 * r[1] * u[1] ** 2
        + 12 * s[0]
        + 12 * s[1] * t
    ) / 16
    assert sp.expand(mu_row.subs(mu, mu_value)) == 0

    # The first E7 coefficient after the same substitutions is absorbed
    # identically by this allowed sigma1 resonance.
    e7_h0 = (
        -sp.Rational(3, 32)
        * (
            16 * a[0] ** 2 * r[1]
            - 24 * a[0] * a[1] * r[0]
            - 4 * a[0] * r[0] * r[1] * u[1]
            + 16 * mu * r[0] ** 2
            + r[0] ** 2 * r[1] * u[1] ** 2
            - 12 * r[0] ** 2 * s[0]
            - 12 * r[0] ** 2 * s[1] * t
        )
    )
    e7_after_pair = sp.factor(
        e7_h0.subs(
            {
                a[0]: r[0] * u[1] / 2,
                mu: mu_value,
            }
        )
    )
    assert e7_after_pair == 0

    # E9[h^9] fixes the next nonresonant sigma1 coefficient.
    tau2_value = (
        sp.Rational(3, 16)
        * (
            4 * a[1] * u[2]
            + 4 * a[2] * u[1]
            - r[0] * u[2] ** 2
            - 2 * r[1] * u[1] * u[2]
            - r[2] * u[1] ** 2
            + 4 * s[1]
            + 4 * s[2] * t
        )
    )
    tau3_value = (
        sp.Rational(3, 16)
        * (
            4 * a[1] * u[3]
            + 4 * a[2] * u[2]
            + 4 * a[3] * u[1]
            - 2 * r[0] * u[2] * u[3]
            - 2 * r[1] * u[1] * u[3]
            - r[1] * u[2] ** 2
            - 2 * r[2] * u[1] * u[2]
            - r[3] * u[1] ** 2
            + 4 * s[2]
            + 4 * s[3] * t
        )
    )
    tau4_value = (
        sp.Rational(3, 16)
        * (
            4 * a[2] * u[3]
            + 4 * a[3] * u[2]
            + 4 * a[4] * u[1]
            - r[0] * u[3] ** 2
            - 2 * r[1] * u[2] * u[3]
            - 2 * r[2] * u[1] * u[3]
            - r[2] * u[2] ** 2
            - 2 * r[3] * u[1] * u[2]
            - r[4] * u[1] ** 2
            + 4 * s[3]
        )
    )
    tau5_value = (
        sp.Rational(3, 16)
        * (
            4 * a[3] * u[3]
            + 4 * a[4] * u[2]
            + 4 * a[5] * u[1]
            - r[1] * u[3] ** 2
            - 2 * r[2] * u[2] * u[3]
            - 2 * r[3] * u[1] * u[3]
            - r[3] * u[2] ** 2
            - 2 * r[4] * u[1] * u[2]
        )
    )
    tau6_value = (
        sp.Rational(3, 16)
        * (
            4 * a[4] * u[3]
            + 4 * a[5] * u[2]
            - r[2] * u[3] ** 2
            - 2 * r[3] * u[2] * u[3]
            - 2 * r[4] * u[1] * u[3]
            - r[4] * u[2] ** 2
        )
    )
    tau7_value = (
        sp.Rational(3, 16)
        * u[3]
        * (
            4 * a[5]
            - r[3] * u[3]
            - 2 * r[4] * u[2]
        )
    )
    tau8_value = -sp.Rational(3, 16) * r[4] * u[3] ** 2
    e7_h1_without_tau2 = (
        -sp.Rational(1, 32)
        * (
            96 * a[0] ** 2 * r[2]
            + 24 * a[0] * a[1] * r[1]
            - 144 * a[0] * a[2] * r[0]
            - 24 * a[0] * r[0] * r[2] * u[1]
            - 12 * a[0] * r[1] ** 2 * u[1]
            - 72 * a[1] ** 2 * r[0]
            + 80 * mu * r[0] * r[1]
            + 6 * r[0] ** 2 * r[2] * u[1] ** 2
            - 72 * r[0] ** 2 * s[1]
            - 72 * r[0] ** 2 * s[2] * t
            + 3 * r[0] * r[1] ** 2 * u[1] ** 2
            - 60 * r[0] * r[1] * s[0]
            - 60 * r[0] * r[1] * s[1] * t
        )
    )
    # The tau2 term in p6' sigma1-6 p6 sigma1' contributes
    # -3*r0^2*tau2 to E7[h].
    e7_h1 = sp.factor(
        (
            e7_h1_without_tau2
            - 3 * r[0] ** 2 * tau2_value
        ).subs(
            {
                a[0]: r[0] * u[1] / 2,
                mu: mu_value,
            }
        )
    )
    expected_e7_h1 = (
        sp.Rational(9, 16)
        * r[0]
        * (
            -2 * a[1]
            + r[0] * u[2]
            + r[1] * u[1]
        )
        ** 2
    )
    assert sp.expand(e7_h1 - expected_e7_h1) == 0

    # Direct full-expression audit of the paired rows.  Include every
    # solved sigma coefficient through the target h-degree, plus generic
    # sigma0 and all four coefficients of R.
    h1 = w_poly / 2
    bracket4 = (
        3 * sp.diff(h1, h) * rho3
        - h1 * sp.diff(rho3, h)
        + 2 * sp.diff(h2, h) * rho2
        - 2 * h2 * sp.diff(rho2, h)
        + sp.diff(h3, h) * rho1
        - 3 * h3 * sp.diff(rho1, h)
        - 4 * h**4 * sp.diff(rho0, h)
    )
    p4 = (
        s_poly**2 / 4
        + r_poly * w_poly / 2
        + 2 * h**4 * h0
    )
    q8 = (
        3 * h**8 * h0
        + sp.Rational(3, 2) * h**4 * r_poly * w_poly
        + sp.Rational(3, 4) * h**4 * s_poly**2
        + sp.Rational(3, 8) * r_poly**2 * s_poly
        + c8 * h**8
    )
    sigma1_full = (
        tau0
        + mu * h
        + tau2_value * h**2
        + tau3_value * h**3
        + tau4_value * h**4
        + tau5_value * h**5
        + tau6_value * h**6
        + tau7_value * h**7
        + tau8_value * h**8
    )
    equation7_full = sp.expand(
        (h + t) * sp.diff(q8, h)
        + 8 * q8
        - (h + t) ** 2 * sp.diff(h**8, h)
        - 16 * (h + t) * h**8
        + 3 * sp.diff(p4, h) * sigma3
        - 4 * p4 * sp.diff(sigma3, h)
        + 2 * sp.diff(p5, h) * sigma2
        - 5 * p5 * sp.diff(sigma2, h)
        + sp.diff(p6, h) * sigma1_full
        - 6 * p6 * sp.diff(sigma1_full, h)
        - 7 * p7 * sp.diff(sigma0, h)
        - sp.Rational(3, 2)
        * (
            rho0 * bracket7
            + rho1 * bracket6
            + rho2 * bracket5
            + rho3 * bracket4
        )
        - c4 * bracket7
    )
    assert sp.expand(equation7_full.coeff(h, 0) - e7_h0) == 0
    direct_h1_difference = sp.expand(
        equation7_full.coeff(h, 1).subs(u[0], 0)
        - (
            e7_h1_without_tau2
            - 3 * r[0] ** 2 * tau2_value
        )
    )
    assert direct_h1_difference == 0, sp.factor(
        direct_h1_difference
    )

    a1_value = (r[0] * u[2] + r[1] * u[1]) / 2
    assert sp.expand(e7_h1.subs(a[1], a1_value)) == 0
    e7_h2 = sp.factor(
        equation7_full.coeff(h, 2)
        .subs(u[0], 0)
        .subs(a[0], r[0] * u[1] / 2)
        .subs(mu, mu_value)
        .subs(a[1], a1_value)
    )
    assert e7_h2 == 0
    e7_h3 = sp.factor(
        equation7_full.coeff(h, 3)
        .subs(u[0], 0)
        .subs(a[0], r[0] * u[1] / 2)
        .subs(mu, mu_value)
        .subs(a[1], a1_value)
    )
    expected_e7_h3 = (
        sp.Rational(9, 8)
        * r[0]
        * (
            -2 * a[2]
            + r[0] * u[3]
            + r[1] * u[2]
            + r[2] * u[1]
        )
        ** 2
    )
    assert sp.expand(e7_h3 - expected_e7_h3) == 0
    a2_value = (
        r[0] * u[3] + r[1] * u[2] + r[2] * u[1]
    ) / 2
    assert sp.expand(e7_h3.subs(a[2], a2_value)) == 0

    # The sigma0 operator in E8 is -8*h^8*sigma0'.  Its h^8,h^9
    # coefficients therefore fix g1,g2 before those variables enter
    # E7[h^4],E7[h^5].  Use the full solved sigma1 polynomial through
    # h^6; omitting tau5 or tau6 changes these two rows.
    equation8_with_sigma1 = sp.expand(
        equation8_low
        + sp.diff(p7, h) * sigma1_full
        - 7 * p7 * sp.diff(sigma1_full, h)
    )

    def close_through_a2(expression: sp.Expr) -> sp.Expr:
        return (
            expression.subs(u[0], 0)
            .subs(a[0], r[0] * u[1] / 2)
            .subs(mu, mu_value)
            .subs(a[1], a1_value)
            .subs(a[2], a2_value)
        )

    g1_value = sp.factor(
        close_through_a2(equation8_with_sigma1.coeff(h, 8)) / 8
    )
    g2_value = sp.factor(
        close_through_a2(equation8_with_sigma1.coeff(h, 9)) / 16
    )
    equation8_full = sp.expand(
        equation8_with_sigma1
        - 8 * h**8 * sp.diff(sigma0, h)
    )
    assert sp.expand(
        close_through_a2(equation8_full.coeff(h, 8)).subs(
            g[1], g1_value
        )
    ) == 0
    assert sp.expand(
        close_through_a2(equation8_full.coeff(h, 9)).subs(
            g[2], g2_value
        )
    ) == 0

    e7_h4 = sp.factor(
        close_through_a2(equation7_full.coeff(h, 4)).subs(
            g[1], g1_value
        )
    )
    e7_h5 = sp.factor(
        close_through_a2(equation7_full.coeff(h, 5))
        .subs(g[1], g1_value)
        .subs(g[2], g2_value)
    )
    expected_e7_h5 = (
        sp.Rational(3, 8)
        * r[0]
        * (
            -2 * a[3]
            + r[1] * u[3]
            + r[2] * u[2]
            + r[3] * u[1]
        )
        ** 2
    )
    assert e7_h4 == 0
    assert sp.expand(e7_h5 - expected_e7_h5) == 0
    a3_value = (
        r[1] * u[3] + r[2] * u[2] + r[3] * u[1]
    ) / 2
    assert sp.expand(e7_h5.subs(a[3], a3_value)) == 0

    def close_through_a3(expression: sp.Expr) -> sp.Expr:
        return close_through_a2(expression).subs(a[3], a3_value)

    g3_value = sp.factor(
        close_through_a3(equation8_with_sigma1.coeff(h, 10)) / 24
    )
    g4_value = sp.factor(
        close_through_a3(equation8_with_sigma1.coeff(h, 11)) / 32
    )
    assert sp.expand(
        close_through_a3(equation8_full.coeff(h, 10)).subs(
            g[3], g3_value
        )
    ) == 0
    assert sp.expand(
        close_through_a3(equation8_full.coeff(h, 11)).subs(
            g[4], g4_value
        )
    ) == 0
    e7_h6 = sp.factor(
        close_through_a3(equation7_full.coeff(h, 6))
        .subs(g[1], g1_value)
        .subs(g[2], g2_value)
        .subs(g[3], g3_value)
        .subs(a[3], a3_value)
    )
    e7_h7 = sp.factor(
        close_through_a3(equation7_full.coeff(h, 7))
        .subs(g[1], g1_value)
        .subs(g[2], g2_value)
        .subs(g[3], g3_value)
        .subs(g[4], g4_value)
        .subs(a[3], a3_value)
    )
    g5_value = sp.factor(
        close_through_a3(equation8_with_sigma1.coeff(h, 12)) / 40
    )
    g6_value = sp.factor(
        close_through_a3(equation8_with_sigma1.coeff(h, 13)) / 48
    )
    assert sp.expand(
        close_through_a3(equation8_full.coeff(h, 12)).subs(
            g[5], g5_value
        )
    ) == 0
    assert sp.expand(
        close_through_a3(equation8_full.coeff(h, 13)).subs(
            g[6], g6_value
        )
    ) == 0

    def substitute_solved_g(expression: sp.Expr) -> sp.Expr:
        return (
            expression.subs(g[1], g1_value)
            .subs(g[2], g2_value)
            .subs(g[3], g3_value)
            .subs(g[4], g4_value)
            .subs(g[5], g5_value)
            .subs(g[6], g6_value)
            .subs(a[3], a3_value)
        )

    e8_h14 = sp.factor(
        substitute_solved_g(
            close_through_a3(equation8_full.coeff(h, 14))
        )
    )
    e8_h15 = sp.factor(
        substitute_solved_g(
            close_through_a3(equation8_full.coeff(h, 15))
        )
    )
    e7_h8 = sp.factor(
        substitute_solved_g(
            close_through_a3(equation7_full.coeff(h, 8))
        )
    )
    e7_h9 = sp.factor(
        substitute_solved_g(
            close_through_a3(equation7_full.coeff(h, 9))
        )
    )
    e7_h10 = sp.factor(
        substitute_solved_g(
            close_through_a3(equation7_full.coeff(h, 10))
        )
    )
    e7_h11 = sp.factor(
        substitute_solved_g(
            close_through_a3(equation7_full.coeff(h, 11))
        )
    )

    # Package the four established relations as successive coefficients
    # of Delta2=2*h^4*rho2-r*rho3.  This is only a verified coefficient
    # pattern at this stage, not yet a uniform proof that Delta2=0.
    delta2 = sp.expand(
        2 * h**4 * rho2 - r_poly * rho3
    ).subs(u[0], 0)
    delta_shifted = sp.expand(delta2 / h**4)
    assert (
        delta_shifted.coeff(h, 0)
        == 2 * a[0] - r[0] * u[1]
    )
    assert (
        delta_shifted.coeff(h, 1)
        == 2 * a[1] - r[0] * u[2] - r[1] * u[1]
    )
    assert (
        delta_shifted.coeff(h, 2)
        == (
            2 * a[2]
            - r[0] * u[3]
            - r[1] * u[2]
            - r[2] * u[1]
        )
    )
    assert (
        delta_shifted.coeff(h, 3)
        == (
            2 * a[3]
            - r[1] * u[3]
            - r[2] * u[2]
            - r[3] * u[1]
        )
    )

    # The terminal E8 compatibility below forces u6=0 on r4!=0.
    # Construct the next complete compact row E6 so that the remaining
    # Delta2 coefficients can be paired with the rho1/rho0 equations.
    y = sp.symbols("y")
    h_components = {
        4: h**4,
        3: h3,
        2: h2,
        1: h1,
        0: h0,
    }
    rho_components = {
        3: rho3,
        2: rho2,
        1: rho1,
        0: rho0,
    }
    h_full = sum(
        coefficient * y**degree
        for degree, coefficient in h_components.items()
    )
    r_full = sum(
        coefficient * y**degree
        for degree, coefficient in rho_components.items()
    )
    s_full = (
        sigma3 * y**3
        + sigma2 * y**2
        + sigma1_full * y
        + sigma0
    )
    p_plus = sp.expand(h_full**2 + r_full)
    q_plus = sp.expand(
        h_full**3
        + sp.Rational(3, 2) * h_full * r_full
        + c8 * p_plus
        + c4 * h_full
        + s_full
    )
    p3 = sp.Poly(p_plus, y).coeff_monomial(y**3)
    q7 = sp.Poly(q_plus, y).coeff_monomial(y**7)
    assert sp.expand(
        sp.Poly(p_plus, y).coeff_monomial(y**7) - p7
    ) == 0

    def h_r_bracket(grade: int) -> sp.Expr:
        return sp.expand(
            sum(
                j * sp.diff(h_components[i], h) * rho_components[j]
                - i * h_components[i] * sp.diff(rho_components[j], h)
                for i in h_components
                for j in rho_components
                if i + j == grade
            )
        )

    bracket3 = h_r_bracket(3)
    equation6_full = sp.expand(
        (h + t) * sp.diff(q7, h)
        + 7 * q7
        - (h + t) ** 2 * sp.diff(p7, h)
        - 14 * (h + t) * p7
        + 3 * sp.diff(p3, h) * sigma3
        - 3 * p3 * sp.diff(sigma3, h)
        + 2 * sp.diff(p4, h) * sigma2
        - 4 * p4 * sp.diff(sigma2, h)
        + sp.diff(p5, h) * sigma1_full
        - 5 * p5 * sp.diff(sigma1_full, h)
        - 6 * p6 * sp.diff(sigma0, h)
        - sp.Rational(3, 2)
        * (
            rho0 * bracket6
            + rho1 * bracket5
            + rho2 * bracket4
            + rho3 * bracket3
        )
        - c4 * bracket6
    )

    def close_terminal(expression: sp.Expr) -> sp.Expr:
        return sp.factor(
            substitute_solved_g(close_through_a3(expression))
            .subs(a[3], a3_value)
            .subs(u[3], 0)
        )

    equation6_terminal = sp.expand(close_terminal(equation6_full))
    equation6_coefficients = tuple(
        sp.factor(equation6_terminal.coeff(h, degree))
        for degree in range(16)
    )

    assert e8_h15 == 6 * r[4] ** 2 * u[3] ** 2
    expected_e8_h14 = (
        sp.Rational(21, 2)
        * u[3]
        * (
            -2 * a[5] * r[4]
            + r[3] * r[4] * u[3]
            + r[4] ** 2 * u[2]
            - s[3] * u[3]
        )
    )
    assert sp.expand(e8_h14 - expected_e8_h14) == 0

    # On the universal r4-unit chart, E8[h^15] gives u6=0.  The top
    # E6 row then kills d5, while the first E7/E6 pair relates d4 to
    # the leading rho1 coefficient instead of killing d4 by itself.
    d4_expression = (
        2 * a[4] - r[3] * u[2] - r[4] * u[1]
    )
    d5_expression = 2 * a[5] - r[4] * u[2]
    d6_expression = -r[4] * u[3]
    e6_h13 = equation6_coefficients[13]
    expected_e6_h13 = (
        -sp.Rational(27, 32)
        * r[4] ** 2
        * d5_expression**2
    )
    assert sp.expand(e6_h13 - expected_e6_h13) == 0
    a5_value = r[4] * u[2] / 2
    assert sp.expand(e6_h13.subs(a[5], a5_value)) == 0

    e7_h7_terminal = sp.factor(e7_h7.subs(u[3], 0))
    e6_h3 = equation6_coefficients[3]
    ell0 = 2 * b[0] - s[0] * u[1]
    paired_d4 = sp.factor(
        r[0] * e7_h7_terminal - 2 * e6_h3
    )
    expected_paired_d4 = (
        sp.Rational(3, 4)
        * (r[0] * d4_expression - 2 * ell0) ** 2
    )
    assert sp.expand(paired_d4 - expected_paired_d4) == 0
    b0_value = (
        r[0] * d4_expression + 2 * s[0] * u[1]
    ) / 4
    assert sp.expand(
        paired_d4.subs(b[0], b0_value)
    ) == 0

    # The transferred square is the leading coefficient of the next
    # convolution defect
    #
    #   Delta1=4*h^4*rho1-2*s*rho3-r*(Delta2/h^4).
    #
    # Once d5=d6=0, Delta2/h^4=d4*h^4, so its h^4 coefficient is
    # exactly 4*b0-2*s0*u4-r0*d4.
    delta2_closed = sp.expand(
        delta_shifted
        .subs(a[0], r[0] * u[1] / 2)
        .subs(a[1], a1_value)
        .subs(a[2], a2_value)
        .subs(a[3], a3_value)
        .subs(u[3], 0)
        .subs(a[5], a5_value)
    )
    assert sp.expand(delta2_closed - d4_expression * h**4) == 0
    delta1 = sp.expand(
        4 * h**4 * rho1
        - 2 * s_poly * rho3
        - r_poly * delta2_closed
    ).subs({u[0]: 0, u[3]: 0})
    delta1_lead = sp.factor(delta1.coeff(h, 4))
    expected_delta1_lead = (
        4 * b[0] - 2 * s[0] * u[1] - r[0] * d4_expression
    )
    assert sp.expand(delta1_lead - expected_delta1_lead) == 0
    assert sp.expand(delta1_lead.subs(b[0], b0_value)) == 0

    # Construct the next complete row E5 directly.  This retains the
    # fixed-base terms, c8/c4 resonances, and every coefficient of R,S.
    p2 = sp.Poly(p_plus, y).coeff_monomial(y**2)
    q6 = sp.Poly(q_plus, y).coeff_monomial(y**6)
    bracket2 = h_r_bracket(2)
    equation5_full = sp.expand(
        (h + t) * sp.diff(q6, h)
        + 6 * q6
        - (h + t) ** 2 * sp.diff(p6, h)
        - 12 * (h + t) * p6
        + 3 * sp.diff(p2, h) * sigma3
        - 2 * p2 * sp.diff(sigma3, h)
        + 2 * sp.diff(p3, h) * sigma2
        - 3 * p3 * sp.diff(sigma2, h)
        + sp.diff(p4, h) * sigma1_full
        - 4 * p4 * sp.diff(sigma1_full, h)
        - 5 * p5 * sp.diff(sigma0, h)
        - sp.Rational(3, 2)
        * (
            rho0 * bracket5
            + rho1 * bracket4
            + rho2 * bracket3
            + rho3 * bracket2
        )
        - c4 * bracket5
    )

    def close_delta1(expression: sp.Expr) -> sp.Expr:
        return (
            substitute_solved_g(close_through_a3(expression))
            .subs(a[3], a3_value)
            .subs(u[3], 0)
            .subs(a[5], a5_value)
            .subs(b[0], b0_value)
        )

    equation6_delta1_coefficients = tuple(
        sp.factor(
            equation6_coefficients[degree]
            .subs(a[5], a5_value)
            .subs(b[0], b0_value)
        )
        for degree in range(16)
    )
    equation5_delta1_coefficients = tuple(
        sp.factor(
            close_delta1(equation5_full.coeff(h, degree))
        )
        for degree in range(16)
    )
    delta1_h5 = sp.factor(
        delta1.coeff(h, 5).subs(b[0], b0_value)
    )
    paired_delta1_h5 = sp.factor(
        6 * r[0] * equation5_delta1_coefficients[1]
        - 6 * r[1] * equation5_delta1_coefficients[0]
        - r[0] ** 2 * equation6_delta1_coefficients[5]
    )
    expected_paired_delta1_h5 = (
        sp.Rational(27, 32) * r[0] ** 2 * delta1_h5**2
    )
    assert sp.expand(
        paired_delta1_h5 - expected_paired_delta1_h5
    ) == 0
    b1_value = (
        r[1] * d4_expression
        + 2 * s[0] * u[2]
        + 2 * s[1] * u[1]
    ) / 4
    assert sp.expand(delta1_h5.subs(b[1], b1_value)) == 0

    delta1_closed = sp.expand(
        delta1.subs(b[0], b0_value).subs(b[1], b1_value)
    )
    assert all(
        delta1_closed.coeff(h, degree) == 0
        for degree in range(6)
    )
    delta0 = sp.expand(
        8 * h**4 * rho0
        - 4 * w_poly * rho3.subs({u[0]: 0, u[3]: 0})
        - 2 * s_poly * delta2_closed
        - r_poly * sp.expand(delta1_closed / h**4)
    )
    delta1_h6 = sp.factor(delta1_closed.coeff(h, 6))
    delta1_h7 = sp.factor(delta1_closed.coeff(h, 7))
    delta1_h8 = sp.factor(delta1_closed.coeff(h, 8))
    assert sp.expand(
        delta0.coeff(h, 2) + r[0] * delta1_h6
    ) == 0
    assert sp.expand(
        delta0.coeff(h, 3)
        + r[0] * delta1_h7
        + r[1] * delta1_h6
    ) == 0

    # Uniform defect invariant.  For the reversed coefficient
    # polynomials A(T)=T^4*H(1/T) and B(T)=T^3*R(1/T), the defects are
    # scaled numerators of the formal quotient coefficients B/A.
    formal_delta2 = sp.expand(
        2 * h**4 * rho2 - r_poly * rho3
    )
    formal_delta1 = sp.expand(
        4 * h**4 * rho1
        - 2 * s_poly * rho3
        - r_poly * formal_delta2 / h**4
    )
    formal_delta0 = sp.expand(
        8 * h**4 * rho0
        - 4 * w_poly * rho3
        - 2 * s_poly * formal_delta2 / h**4
        - r_poly * formal_delta1 / h**4
    )
    quotient_c0 = rho3 / h**4
    quotient_c1 = sp.expand(
        (rho2 - h3 * quotient_c0) / h**4
    )
    quotient_c2 = sp.expand(
        (
            rho1
            - h3 * quotient_c1
            - h2 * quotient_c0
        )
        / h**4
    )
    quotient_c3 = sp.expand(
        (
            rho0
            - h3 * quotient_c2
            - h2 * quotient_c1
            - h1 * quotient_c0
        )
        / h**4
    )
    z = h + t
    quotient_c4 = sp.expand(
        (
            z
            - h3 * quotient_c3
            - h2 * quotient_c2
            - h1 * quotient_c1
            - h0 * quotient_c0
        )
        / h**4
    )
    formal_delta_minus1 = sp.expand(
        16 * h**4 * z
        - 16 * h0 * rho3
        - 2 * h3 * formal_delta0 / h**4
        - 4 * h2 * formal_delta1 / h**4
        - 8 * h1 * formal_delta2 / h**4
    )
    assert sp.cancel(
        quotient_c1 - formal_delta2 / (2 * h**8)
    ) == 0
    assert sp.cancel(
        quotient_c2 - formal_delta1 / (4 * h**8)
    ) == 0
    assert sp.cancel(
        quotient_c3 - formal_delta0 / (8 * h**8)
    ) == 0
    assert sp.cancel(
        quotient_c4 - formal_delta_minus1 / (16 * h**8)
    ) == 0

    # The remaining Delta1 coefficients are top-down coupled to rho0.
    # Construct E4 exactly before reading the finite boundary.
    p1 = sp.Poly(p_plus, y).coeff_monomial(y)
    q5 = sp.Poly(q_plus, y).coeff_monomial(y**5)
    bracket1 = h_r_bracket(1)
    equation4_full = sp.expand(
        (h + t) * sp.diff(q5, h)
        + 5 * q5
        - (h + t) ** 2 * sp.diff(p5, h)
        - 10 * (h + t) * p5
        + 3 * sp.diff(p1, h) * sigma3
        - p1 * sp.diff(sigma3, h)
        + 2 * sp.diff(p2, h) * sigma2
        - 2 * p2 * sp.diff(sigma2, h)
        + sp.diff(p3, h) * sigma1_full
        - 3 * p3 * sp.diff(sigma1_full, h)
        - 4 * p4 * sp.diff(sigma0, h)
        - sp.Rational(3, 2)
        * (
            rho0 * bracket4
            + rho1 * bracket3
            + rho2 * bracket2
            + rho3 * bracket1
        )
        - c4 * bracket4
    )

    def close_delta1_h5(expression: sp.Expr) -> sp.Expr:
        return close_delta1(expression).subs(b[1], b1_value)

    equation4_high_coefficients = {
        degree: sp.factor(
            close_delta1_h5(equation4_full.coeff(h, degree))
        )
        for degree in range(16)
    }

    # One further exact row for the changed regime.
    p0 = sp.Poly(p_plus, y).coeff_monomial(1)
    q4 = sp.Poly(q_plus, y).coeff_monomial(y**4)
    bracket0 = h_r_bracket(0)
    assert bracket0 == 0
    equation3_full = sp.expand(
        (h + t) * sp.diff(q4, h)
        + 4 * q4
        - (h + t) ** 2 * sp.diff(p4, h)
        - 8 * (h + t) * p4
        + 3 * sp.diff(p0, h) * sigma3
        + 2 * sp.diff(p1, h) * sigma2
        - p1 * sp.diff(sigma2, h)
        + sp.diff(p2, h) * sigma1_full
        - 2 * p2 * sp.diff(sigma1_full, h)
        - 3 * p3 * sp.diff(sigma0, h)
        - sp.Rational(3, 2)
        * (
            rho0 * bracket3
            + rho1 * bracket2
            + rho2 * bracket1
            + rho3 * bracket0
        )
        - c4 * bracket3
    )
    equation3_low_coefficients = {
        degree: sp.factor(
            close_delta1_h5(equation3_full.coeff(h, degree))
        )
        for degree in range(8)
    }

    # Uniform cube-truncation identity.  Since
    # R_full/H=T*C(T), the nonnegative-y part of
    # (H^2+R_full)^(3/2) beyond H^3+(3/2)H*R is governed by
    # (3/8)*T^2*H*C^2.  These four formulas recover every solved
    # sigma coefficient at once; sigma0 retains only its constant
    # Euler resonance.
    ac2_0 = h**4 * quotient_c0**2
    ac2_1 = (
        h3 * quotient_c0**2
        + 2 * h**4 * quotient_c0 * quotient_c1
    )
    ac2_2 = (
        h2 * quotient_c0**2
        + 2 * h3 * quotient_c0 * quotient_c1
        + h**4
        * (
            quotient_c1**2
            + 2 * quotient_c0 * quotient_c2
        )
    )
    ac2_3 = (
        h1 * quotient_c0**2
        + 2 * h2 * quotient_c0 * quotient_c1
        + h3
        * (
            quotient_c1**2
            + 2 * quotient_c0 * quotient_c2
        )
        + h**4
        * (
            2 * quotient_c0 * quotient_c3
            + 2 * quotient_c1 * quotient_c2
        )
    )
    # Use B=A*C once more.  This form makes regularity transparent:
    # after c0 and c1 are polynomial and h^2*c2 is polynomial, the
    # terminal coefficient has no h-pole.
    ac2_3_reduced = (
        2 * rho0 * quotient_c0
        - h1 * quotient_c0**2
        + h3 * quotient_c1**2
        + 2 * h**4 * quotient_c1 * quotient_c2
    )
    assert sp.cancel(ac2_3 - ac2_3_reduced) == 0
    predicted_sigma3 = sp.Rational(3, 2) * z * h**4
    predicted_sigma2 = (
        sp.Rational(3, 2) * z * h3
        + sp.Rational(3, 8) * ac2_0
    )
    predicted_sigma1 = (
        sp.Rational(3, 2) * z * h2
        + sp.Rational(3, 8) * ac2_1
    )
    predicted_sigma0 = (
        sp.Rational(3, 2) * z * h1
        + sp.Rational(3, 8) * ac2_2
    )
    assert sp.cancel(
        close_delta1_h5(sigma3 - predicted_sigma3)
    ) == 0
    assert sp.cancel(
        close_delta1_h5(sigma2 - predicted_sigma2)
    ) == 0
    assert sp.cancel(
        close_delta1_h5(sigma1_full - predicted_sigma1)
    ) == 0
    sigma0_cube_difference = sp.cancel(
        close_delta1_h5(sigma0 - predicted_sigma0)
    )
    assert sp.cancel(sp.diff(sigma0_cube_difference, h)) == 0

    predicted_base_coefficient = sp.expand(
        sp.Rational(3, 2) * z * h0
        + sp.Rational(3, 8) * ac2_3_reduced
        + c8 * z
        + sp.Rational(1, 2) * c4 * quotient_c0
    )
    base_cube_mismatch = sp.cancel(
        close_delta1_h5(z**2 - predicted_base_coefficient)
    )
    # Rational scalar denominators are harmless; the point is that no
    # power of h survives.
    assert not sp.denom(sp.together(base_cube_mismatch)).has(h)

    # Add the bracket-invisible constant to the formal centralizer so
    # that its y^0 coefficient agrees with sigma0.  Then Q-F begins in
    # degree y^-1 with exactly base_cube_mismatch.  Its complete E7
    # identity is the highest-grade Euler operator on that mismatch.
    # This conclusion is support-triangular: no coefficient below y^-1
    # can contribute to grade 7.
    terminal_euler_row = sp.expand(
        -sp.diff(h**8, h) * base_cube_mismatch
        - 8 * h**8 * sp.diff(base_cube_mismatch, h)
    )

    # The terminal equation itself is compatible with both endpoint
    # units and every required Newton vertex.  Set R=0 and take
    # H_0=2*(z-c8)/3 with c8 nonzero.  Then [z^0]p0=4*c8^2/9 is also
    # nonzero; an additive centralizer constant supplies [z^0]q0.
    terminal_compatibility_witness = {
        u[1]: 0,
        u[2]: 0,
        a[4]: 0,
        b[2]: 0,
        b[3]: 0,
        b[4]: 0,
        d[0]: 0,
        d[1]: 0,
        d[2]: 0,
        d[3]: 0,
        d[4]: 0,
        v[0]: sp.Rational(4, 3) * (t - c8),
        v[1]: sp.Rational(4, 3),
        v[2]: 0,
        c4: 0,
    }
    assert sp.cancel(
        base_cube_mismatch.subs(terminal_compatibility_witness)
    ) == 0
    return {
        "E8_h1": endpoint,
        "E8_h3_after_u3": rho2_boundary,
        "tau0": tau0,
        "mu_value": mu_value,
        "E7_h0_after_pair": e7_after_pair,
        "tau2_value": tau2_value,
        "E7_h1": e7_h1,
        "a1_value": a1_value,
        "tau3_value": tau3_value,
        "E7_h2": e7_h2,
        "tau4_value": tau4_value,
        "E7_h3": e7_h3,
        "a2_value": a2_value,
        "g1_value": g1_value,
        "g2_value": g2_value,
        "E7_h4": e7_h4,
        "E7_h5": e7_h5,
        "a3_value": a3_value,
        "g3_value": g3_value,
        "g4_value": g4_value,
        "E7_h6": e7_h6,
        "E7_h7": e7_h7,
        "g5_value": g5_value,
        "g6_value": g6_value,
        "E8_h14": e8_h14,
        "E8_h15": e8_h15,
        "E7_h8": e7_h8,
        "E7_h9": e7_h9,
        "E7_h10": e7_h10,
        "E7_h11": e7_h11,
        "delta2": delta2,
        "E6_coefficients": equation6_coefficients,
        "d4_expression": d4_expression,
        "d5_expression": d5_expression,
        "d6_expression": d6_expression,
        "E6_h13": e6_h13,
        "a5_value": a5_value,
        "paired_d4": paired_d4,
        "b0_value": b0_value,
        "delta1": delta1,
        "delta1_lead": delta1_lead,
        "E6_delta1_coefficients": equation6_delta1_coefficients,
        "E5_delta1_coefficients": equation5_delta1_coefficients,
        "delta1_h5": delta1_h5,
        "paired_delta1_h5": paired_delta1_h5,
        "b1_value": b1_value,
        "delta0": delta0,
        "delta1_h6": delta1_h6,
        "delta1_h7": delta1_h7,
        "delta1_h8": delta1_h8,
        "E4_high_coefficients": equation4_high_coefficients,
        "E3_low_coefficients": equation3_low_coefficients,
        "formal_delta2": formal_delta2,
        "formal_delta1": formal_delta1,
        "formal_delta0": formal_delta0,
        "formal_delta_minus1": formal_delta_minus1,
        "ac2_3_reduced": ac2_3_reduced,
        "base_cube_mismatch": base_cube_mismatch,
        "terminal_euler_row": terminal_euler_row,
    }


def main() -> None:
    result = verify_lower_remainder_identity()
    top = verify_top_remainder_row()
    terminal = verify_terminal_euler_lemma()
    tail = verify_negative_tail_obstruction()
    weighted_tail = verify_weighted_residue_obstruction()
    r1_tail = verify_r1_hyperelliptic_obstruction()
    next_row = verify_next_remainder_row()
    e9 = verify_e9_remainder_row()
    e8 = verify_e8_remainder_row()
    print("P_+=H^2+R, Q_+=H^3+(3/2)HR+c8*P_++c4*H+S")
    print("[P_+,Q_+]=[P_+,S]-((3/2)R+c4)[H,R]")
    print("restored base residual: [X,Q_+]+[P_+,B]+upper reduction")
    print("bottom row: z*q0_prime-z^2*p0_prime = 0")
    print("E11 forces [y^3]S =", top["sigma3"])
    print(
        "E10 low descent:",
        next_row["E10_h3"],
        next_row["E10_h5_after_u0"],
        next_row["E10_h6_after_u0_u1"],
    )
    print("on r0!=0: h^2 divides [y^3]R and kappa=0")
    print("E9 endpoint:", e9["E9_h3"])
    print("on r0!=0: h^3 divides [y^3]R")
    print("remaining sigma2 resonance:", e9["lambda_value"])
    print("E9 resonance after u2=0:", e9["E9_h8_after_u2"])
    print("E8 endpoint:", e8["E8_h1"])
    print("on r0!=0: h^4 divides [y^3]R")
    print("rho2 square:", e8["E8_h3_after_u3"])
    print("sigma1 resonance:", e8["mu_value"])
    print("paired E7 residual:", e8["E7_h0_after_pair"])
    print("next sigma1 coefficient:", e8["tau2_value"])
    print("E7 h1 square:", e8["E7_h1"])
    print("forced a1:", e8["a1_value"])
    print("following sigma1 coefficient:", e8["tau3_value"])
    print("E7 h2 after a1:", e8["E7_h2"])
    print("next following sigma1 coefficient:", e8["tau4_value"])
    print("E7 h3 after a1:", e8["E7_h3"])
    print("forced a2:", e8["a2_value"])
    print("E7 h4 after solved sigma0:", e8["E7_h4"])
    print("E7 h5 after solved sigma0:", e8["E7_h5"])
    print("forced a3:", e8["a3_value"])
    print("E7 h6 after solved sigma0:", e8["E7_h6"])
    print("E8 h15 compatibility:", e8["E8_h15"])
    print("on r4!=0: u6=0 and d6=0")
    print("E6 h13 d5 square:", e8["E6_h13"])
    print("forced a5:", e8["a5_value"])
    print("paired E7 h7/E6 h3 d4 square:", e8["paired_d4"])
    print("forced leading rho1 relation:", e8["b0_value"])
    print("paired E6/E5 Delta1 h5 square:", e8["paired_delta1_h5"])
    print("forced next rho1 relation:", e8["b1_value"])
    print(
        "arbitrary terminal Euler multiplier:",
        terminal["multiplier"],
        "with unique Laurent resonance degree",
        terminal["resonance_degree"],
    )
    print("normalized tail obstruction:", tail["cokernel_obstruction"])
    print(
        "weighted r2 tail obstruction:",
        weighted_tail["r2_obstruction"],
    )
    print("weighted r1 Hermite remainder:", r1_tail["hermite_remainder"])
    print("RESULT: EXACT LOWER-REMAINDER IDENTITY PASSES")


if __name__ == "__main__":
    main()
