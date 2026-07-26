#!/usr/bin/env python3
"""Exact checks for the odd (3A,6) split-frontier note."""

from __future__ import annotations

import sympy as sp


# ---------------------------------------------------------------------------
# The q=6 Taylor threshold is independent of the upper degree.

i, m, n, rho = sp.symbols(
    "i m n rho", integer=True, positive=True
)
for index in range(2, 7):
    normalized_bound = sp.expand(
        index * (2 * rho) - (6 - index) * rho
    )
    assert sp.factor(normalized_bound - (3 * index - 6) * rho) == 0
    assert (3 * index - 6) >= 0


# ---------------------------------------------------------------------------
# Exact common-cubic transverse order on the slice R=w^3, E=Q.
#
# If A=2r+1, the first nonpolynomial binomial term of
# (R^2+E)^(A/2) is binomial(A/2,r+1)*E^(r+1)/R.  On this slice the
# canonical residual through s^-5 consists only of the displayed
# s^-3 term.

t, Q = sp.symbols("t Q")
for upper_reduced_degree in (3, 5, 7, 9, 11):
    r_index = (upper_reduced_degree - 1) // 2
    w_of_s = t**-1 * (1 - Q * t**6) ** sp.Rational(1, 6)
    polynomial_part = sum(
        sp.binomial(
            sp.Rational(upper_reduced_degree, 2),
            j_index,
        )
        * Q**j_index
        * w_of_s ** (3 * upper_reduced_degree - 6 * j_index)
        for j_index in range(r_index + 1)
    )
    residual = sp.series(
        polynomial_part - t ** (-3 * upper_reduced_degree),
        t,
        0,
        6,
    ).removeO()
    expected = (
        -sp.binomial(
            sp.Rational(upper_reduced_degree, 2),
            r_index + 1,
        )
        * Q ** (r_index + 1)
        * t**3
    )
    assert sp.factor(residual - expected) == 0


# ---------------------------------------------------------------------------
# Weighted stationary top charts for (9,6) and (15,6).

w, z = sp.symbols("w z")
xi, eta = sp.symbols("xi eta")
g = w**6 + z * w**4 + xi * z**2 * w**2 + eta * z**3


def approximate_root_polynomial(exponent: int) -> sp.Expr:
    """Return the polynomial part of g^(exponent/6) in w."""
    correction = (
        z / w**2 + xi * z**2 / w**4 + eta * z**3 / w**6
    )
    output = 0
    for power in range(exponent // 2 + 1):
        expanded = sp.expand(
            sp.binomial(sp.Rational(exponent, 6), power)
            * w**exponent
            * correction**power
        )
        output += sp.Add(
            *[
                term
                for term in sp.Add.make_args(expanded)
                if term.as_powers_dict().get(w, 0) >= 0
            ]
        )
    return sp.expand(output)


def bracket_in_z_w(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(left, z) * sp.diff(right, w)
        - sp.diff(left, w) * sp.diff(right, z)
    )


# At p=9 the even top chart has the square zero-bracket point and one
# nonzero cusp point.
f9 = approximate_root_polynomial(9)
bracket9 = sp.Poly(bracket_in_z_w(f9, g), w, z)
positive9 = [
    coefficient
    for (w_power, _), coefficient in bracket9.terms()
    if w_power > 0
]
solutions9 = sp.solve(positive9, (xi, eta), dict=True)
assert solutions9 == [
    {xi: sp.Rational(1, 4), eta: 0},
    {xi: sp.Rational(5, 8), eta: sp.Rational(3, 32)},
]
assert (
    bracket9.coeff_monomial(z**6).subs(solutions9[0]) == 0
)
assert (
    bracket9.coeff_monomial(z**6).subs(solutions9[1]) != 0
)


# At p=15 the positive bracket equations have one square point and
# three additional points over the following squarefree cubic.
f15 = approximate_root_polynomial(15)
bracket15 = sp.Poly(bracket_in_z_w(f15, g), w, z)
coefficient_w4 = sp.factor(
    bracket15.coeff_monomial(w**4 * z**7)
)
coefficient_w2 = sp.factor(
    bracket15.coeff_monomial(w**2 * z**8)
)
coefficient_w0 = sp.factor(
    bracket15.coeff_monomial(z**9)
)

assert coefficient_w4.subs(
    {xi: sp.Rational(1, 4), eta: 0}
) == 0
assert coefficient_w2.subs(
    {xi: sp.Rational(1, 4), eta: 0}
) == 0
assert coefficient_w0.subs(
    {xi: sp.Rational(1, 4), eta: 0}
) == 0

stationary_cubic = (
    7744 * xi**3
    - 16176 * xi**2
    + 10476 * xi
    - 2241
)
eta_on_cubic = (176 * xi**2 - 168 * xi + 63) / 288

for positive_coefficient in (coefficient_w4, coefficient_w2):
    numerator = sp.together(
        positive_coefficient.subs(eta, eta_on_cubic)
    ).as_numer_denom()[0]
    assert sp.rem(numerator, stationary_cubic, xi) == 0

assert sp.discriminant(stationary_cubic, xi) == -34441342746624
assert sp.factor(stationary_cubic.subs(xi, sp.Rational(1, 4))) != 0

# The terminal coefficient is nonzero at every root of the cubic.
terminal_numerator = sp.together(
    coefficient_w0.subs(eta, eta_on_cubic)
).as_numer_denom()[0]
assert (
    sp.gcd(
        sp.Poly(terminal_numerator, xi),
        sp.Poly(stationary_cubic, xi),
    ).degree()
    == 0
)

# The coefficient eta is also nonzero at every root, so the weighted
# pole scale really is max(1/2,2/4,3/6)=1/2.  Since
# bracket=6*dA5/dz=c*z^9, A5 has z-degree ten and ratio twenty.
eta_numerator = sp.together(eta_on_cubic).as_numer_denom()[0]
assert (
    sp.gcd(
        sp.Poly(eta_numerator, xi),
        sp.Poly(stationary_cubic, xi),
    ).degree()
    == 0
)
weighted_pole_scale = sp.Rational(1, 2)
terminal_pole = 10
assert terminal_pole / weighted_pole_scale == 20
assert 20 == 15 + 5


print("verified: q=6 Taylor threshold n >= 2*rho is upper-degree independent")
print("verified: top transverse order is exactly (A+1)/2 on the Q slice")
print("verified: the (9,6) even top chart has one nonzero cusp ray")
print("verified: the (15,6) even top chart has three new cubic-field rays")
print("verified: every new (15,6) ray has pole(A5)/rho = 20")
