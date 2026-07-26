#!/usr/bin/env python3
"""Exact checks for the standard-system Sylvester correction audit."""

import sympy as sp


x, epsilon = sp.symbols("x epsilon")


def first_truncation(R: sp.Expr, T: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    """Return the derivatives of the a=2,b=3 first binomial truncation."""
    P = R**2 + epsilon * T
    Q = R**3 + sp.Rational(3, 2) * epsilon * R * T
    return sp.diff(P, x), sp.diff(Q, x)


def polynomial_binomial_truncation(
    a: int,
    b: int,
    R: sp.Expr,
    T: sp.Expr,
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """Return A=P', B=Q_q', and the division-free multiplier H."""
    q = b // a
    P = R**a + epsilon * T
    Q = sum(
        sp.binomial(sp.Rational(b, a), ell)
        * epsilon**ell
        * R ** (b - a * ell)
        * T**ell
        for ell in range(q + 1)
    )
    H = sum(
        ell
        * sp.binomial(sp.Rational(b, a), ell)
        * epsilon ** (ell - 1)
        * R ** (b - a * ell)
        * T ** (ell - 1)
        for ell in range(1, q + 1)
    )
    return sp.diff(P, x), sp.diff(Q, x), H


def epsilon_order(polynomial: sp.Expr) -> int:
    """Return the least epsilon exponent of a nonzero polynomial."""
    return min(
        monomial[0]
        for monomial, _coefficient in sp.Poly(polynomial, epsilon).terms()
    )


# The derivative remainder is linear although the first Laurent pole in
# (R^2+epsilon*T)^(3/2) is quadratic.
generic_R = sp.Function("R")(x)
generic_T = sp.Function("T")(x)
generic_A, generic_B = first_truncation(generic_R, generic_T)
assert sp.simplify(
    generic_B
    - sp.Rational(3, 2) * generic_R * generic_A
    - sp.Rational(3, 2)
    * epsilon
    * sp.diff(generic_R, x)
    * generic_T
) == 0


# The general polynomial truncation has the exact telescoping
# remainder from the audit.  Several coprime pairs guard the binomial
# endpoint and all intermediate cancellations.
for general_a, general_b in (
    (2, 3),
    (2, 5),
    (3, 4),
    (3, 5),
    (3, 7),
    (4, 5),
):
    general_q = general_b // general_a
    general_r = general_b - general_a * general_q
    test_R = x**3 + 2 * x + 1
    test_T = x ** (3 * general_a - 2) + x + 2
    test_A, test_B, test_H = polynomial_binomial_truncation(
        general_a,
        general_b,
        test_R,
        test_T,
    )
    expected_remainder = (
        sp.binomial(sp.Rational(general_b, general_a), general_q)
        * general_r
        * epsilon**general_q
        * test_R ** (general_r - 1)
        * sp.diff(test_R, x)
        * test_T**general_q
    )
    assert sp.expand(test_B - test_H * test_A - expected_remainder) == 0


# Exact generic g=2 calculation.
r, u, v, w = sp.symbols("r u v w", nonzero=True)
quadratic_R = x**2 + r
quadratic_T = u * x**2 + v * x + w
quadratic_A, quadratic_B = first_truncation(
    quadratic_R,
    quadratic_T,
)
quadratic_resultant = sp.factor(
    sp.resultant(quadratic_A, quadratic_B, x)
)
quadratic_bracket = (
    4 * epsilon**2 * u**4 * w
    - epsilon**2 * u**3 * v**2
    + 16 * epsilon * r * u**3 * w
    - 4 * epsilon * r * u**2 * v**2
    - 16 * epsilon * u**2 * w**2
    + 20 * epsilon * u * v**2 * w
    - 4 * epsilon * v**4
    + 16 * r**2 * u**2 * w
    - 32 * r * u * w**2
    + 16 * r * v**2 * w
    + 16 * w**3
)
assert quadratic_resultant == (
    432 * epsilon**4 * v * quadratic_bracket
)
quadratic_lead = sp.factor(
    sp.expand(quadratic_resultant).coeff(epsilon, 4)
)
assert sp.simplify(
    quadratic_lead
    - 6912 * v * w * ((r * u - w) ** 2 + r * v**2)
) == 0
assert sp.expand(quadratic_resultant).coeff(epsilon, 3) == 0


# Exact g=3 specialization.
cubic_R = x**3 + 1
cubic_T = x**2 + x + 1
cubic_A, cubic_B = first_truncation(cubic_R, cubic_T)
cubic_resultant = sp.factor(sp.resultant(cubic_A, cubic_B, x))
assert cubic_resultant == (
    sp.Rational(14348907, 2)
    * epsilon**7
    * (epsilon**2 - 12 * epsilon + 48)
)

tau = sp.symbols("tau")
cubic_reciprocal = sp.factor(cubic_resultant.subs(epsilon, tau**4))
assert cubic_reciprocal == (
    sp.Rational(14348907, 2)
    * tau**28
    * (tau**8 - 12 * tau**4 + 48)
)


# Root-factor mechanism for the cubic example: the explicit epsilon^5
# from deg(P_X)=5 is supplemented by epsilon^2 from the R' cluster,
# while the T factor is a unit at epsilon=0.
cubic_R_prime_resultant = sp.factor(
    sp.resultant(cubic_A, sp.diff(cubic_R, x), x)
)
cubic_T_resultant = sp.factor(
    sp.resultant(cubic_A, cubic_T, x)
)
assert cubic_R_prime_resultant == 243 * epsilon**2
assert cubic_T_resultant.subs(epsilon, 0) != 0


# Independent exact specializations of the general generic valuation
# ord_epsilon Res(P',Q_q') = gb-floor(b/a)-1.
for sample_a, sample_b, sample_g in (
    (2, 5, 2),
    (3, 4, 2),
    (3, 5, 2),
    (2, 5, 3),
):
    sample_R = x**sample_g + 1
    sample_T = x ** (sample_g * sample_a - 2) + x + 2
    assert sp.gcd(sample_R * sp.diff(sample_R, x), sample_T) == 1
    assert (
        sp.gcd(
            sample_R * sp.diff(sample_R, x),
            sp.diff(sample_T, x),
        )
        == 1
    )
    sample_A, sample_B, _sample_H = polynomial_binomial_truncation(
        sample_a,
        sample_b,
        sample_R,
        sample_T,
    )
    assert sp.degree(sample_A, x) == sample_g * sample_a - 1
    assert sp.degree(sample_B, x) == sample_g * sample_b - 1
    sample_resultant = sp.factor(sp.resultant(sample_A, sample_B, x))
    assert epsilon_order(sample_resultant) == (
        sample_g * sample_b - sample_b // sample_a - 1
    )


print("verified: the derivative remainder is already epsilon-linear")
print("verified: the general division-free binomial telescoping identity")
print("verified: generic contact gb-floor(b/a)-1 in four further cases")
print("verified: generic g=2 contact is four, not six")
print("verified: the g=3 example has epsilon-contact seven")
print("verified: epsilon=tau^4 gives resultant contact twenty-eight")
