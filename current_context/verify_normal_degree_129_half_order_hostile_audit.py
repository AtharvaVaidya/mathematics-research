#!/usr/bin/env python3
"""Exact checks for NORMAL_DEGREE_129_HALF_ORDER_HOSTILE_AUDIT.md."""

import sympy as sp


X, u = sp.symbols("X u")
P = X**3 - 1
S_plus = -sp.Rational(1, 2) * X**2 * (X**3 - 3)
S_mixed = -(
    3 * X**5
    - 2 * X**4
    + 2 * X**3
    - 9 * X**2
    + 14 * X
    + 10
) / 18

assert sp.rem(S_plus**2 - X, P**2, X) == 0
assert sp.rem(S_mixed**2 - X, P**2, X) == 0


def polynomial_part(rational):
    rational = sp.cancel(rational)
    numerator, denominator = sp.fraction(rational)
    return sp.div(numerator, denominator, X)[0]


def four_thirds_part(delta, order):
    """Polynomial part of (P^3+delta)^(4/3), as a u-series."""
    v = delta / P**3
    expansion = sp.series(
        P**4
        * sum(
            sp.binomial(sp.Rational(4, 3), q) * v**q
            for q in range(order + 1)
        ),
        u,
        0,
        order + 1,
    ).removeO().expand()
    return sp.expand(
        sum(
            u**n * polynomial_part(expansion.coeff(u, n))
            for n in range(order + 1)
        )
    )


def bracket(f, g):
    # u=t^17, so t*d/dt=17*u*d/du.
    return sp.expand(
        17
        * u
        * (
            sp.diff(f, u) * sp.diff(g, X)
            - sp.diff(f, X) * sp.diff(g, u)
        )
        - 24 * f * sp.diff(g, X)
        + 18 * sp.diff(f, X) * g
    )


def forcing_at_three(S):
    g = P**3 + u * S
    f = four_thirds_part(u * S, 3)
    return sp.factor(bracket(f, g).coeff(u, 3))


# The two cokernel pairs annihilate their respective monomial images.
def coefficient(poly, degree):
    return sp.Poly(sp.expand(poly), X).coeff_monomial(X**degree)


def lambda_51_0(poly):
    return sp.factor(
        391 * coefficient(poly, 0)
        + 46 * coefficient(poly, 3)
        + 16 * coefficient(poly, 6)
    )


def lambda_51_1(poly):
    return sp.factor(
        95 * coefficient(poly, 1)
        + 20 * coefficient(poly, 4)
        + 8 * coefficient(poly, 7)
    )


def lambda_68_0(poly):
    return sp.factor(
        85 * coefficient(poly, 0)
        + 5 * coefficient(poly, 3)
        + coefficient(poly, 6)
    )


def lambda_68_1(poly):
    return sp.factor(
        189 * coefficient(poly, 1)
        + 21 * coefficient(poly, 4)
        + 5 * coefficient(poly, 7)
    )


R_coeffs = sp.symbols("r0:6")
R_generic = sum(R_coeffs[i] * X**i for i in range(6))
image_51 = sp.expand(2 * P * sp.diff(R_generic, X) + 5 * sp.diff(P, X) * R_generic)
image_68 = sp.expand(P * sp.diff(R_generic, X) + sp.Rational(16, 3) * sp.diff(P, X) * R_generic)
assert lambda_51_0(image_51) == 0
assert lambda_51_1(image_51) == 0
assert lambda_68_0(image_68) == 0
assert lambda_68_1(image_68) == 0


# Mixed orbit: the cubic forcing is outside the order-51 image.
K_mixed = forcing_at_three(S_mixed)
expected_mixed = (
    450 * X**7
    - 690 * X**6
    + 1316 * X**5
    - 3980 * X**4
    + 2620 * X**3
    - 2531 * X**2
    + 4076 * X
    - 2260
) / 4374
assert sp.factor(K_mixed - expected_mixed) == 0
assert lambda_51_0(K_mixed) == -sp.Rational(43010, 243)
assert lambda_51_1(K_mixed) == sp.Rational(17290, 243)


# Equal-sign orbit: unique first lift, followed by the order-68
# cokernel obstruction.
v = sp.symbols("v0:6")
V = sum(v[i] * X**i for i in range(6))
delta = u * S_plus + u**2 * V
g = P**3 + delta
f = four_thirds_part(delta, 4)
B = bracket(f, g)
equations_51 = sp.Poly(B.coeff(u, 3), X).all_coeffs()
solutions_51 = sp.solve(equations_51, v, dict=True)
expected_solution = {
    v[0]: 0,
    v[1]: -sp.Rational(11, 144),
    v[2]: 0,
    v[3]: 0,
    v[4]: sp.Rational(1, 16),
    v[5]: 0,
}
assert solutions_51 == [expected_solution]

K_plus = sp.factor(B.coeff(u, 4).subs(expected_solution))
expected_plus = X * (1323 * X**6 - 5139 * X**3 + 3776) / 1296
assert sp.factor(K_plus - expected_plus) == 0
assert lambda_68_0(K_plus) == 0
assert lambda_68_1(K_plus) == sp.Rational(945, 2)


# The surviving k upper term is neutralized by S_18=-3k/4.
t, k = sp.symbols("t k")
S18 = -sp.Rational(3, 4) * k
g_k = P**3 + t**17 * S_plus + t**18 * S18
delta_k = t**17 * S_plus + t**18 * S18
quadratic_k = sp.div(sp.expand(delta_k**2), P**2, X)[0]
cubic_k = sp.div(sp.expand(delta_k**3), P**5, X)[0]
f_k = (
    P**4
    + sp.Rational(4, 3) * P * delta_k
    + sp.Rational(2, 9) * quadratic_k
    - sp.Rational(4, 81) * cubic_k
    + k * t**18 * P
)
B_k = sp.expand(
    t
    * (
        sp.diff(f_k, t) * sp.diff(g_k, X)
        - sp.diff(f_k, X) * sp.diff(g_k, t)
    )
    - 24 * f_k * sp.diff(g_k, X)
    + 18 * sp.diff(f_k, X) * g_k
)
assert B_k.coeff(t, 35) == 0


# With C=2c+3j=0, the forced c- and k-dependent intermediate jets
# cancel every coefficient below the same order-68 obstruction.
c = sp.symbols("c")
V_exact = X * (9 * X**3 - 11) / 144
S29 = c * X**2 * (5 * X**3 - 11) / 48
S41 = -7 * c**2 * X**2 * (9 * X**3 - 19) / 2304
S46 = -c * X * (35 * X**3 - 52) / 864
delta_full = (
    c * t**12 * P
    + t**17 * S_plus
    - sp.Rational(3, 4) * k * t**18
    + t**29 * S29
    + t**34 * V_exact
    + t**41 * S41
    + t**46 * S46
)
g_full = P**3 + delta_full


def quotient_in_x(numerator, denominator):
    return sp.div(sp.expand(numerator), denominator, X)[0]


root_part = P**4 + sp.Rational(4, 3) * P * delta_full
for q in range(2, 6):
    root_part += sp.binomial(sp.Rational(4, 3), q) * quotient_in_x(
        delta_full**q, P ** (3 * q - 4)
    )

two_thirds_part = P**2 + sp.Rational(2, 3) * quotient_in_x(
    delta_full, P
)
for q in range(2, 5):
    two_thirds_part += sp.binomial(sp.Rational(2, 3), q) * quotient_in_x(
        delta_full**q, P ** (3 * q - 2)
    )

one_third_part = P + sp.Rational(1, 3) * quotient_in_x(
    delta_full, P**2
)
for q in range(2, 4):
    one_third_part += sp.binomial(sp.Rational(1, 3), q) * quotient_in_x(
        delta_full**q, P ** (3 * q - 1)
    )

f_full = (
    root_part
    - sp.Rational(2, 3) * c * t**12 * two_thirds_part
    + k * t**18 * one_third_part
)
B_full = sp.expand(
    t
    * (
        sp.diff(f_full, t) * sp.diff(g_full, X)
        - sp.diff(f_full, X) * sp.diff(g_full, t)
    )
    - 24 * f_full * sp.diff(g_full, X)
    + 18 * sp.diff(f_full, X) * g_full
)
for order in range(1, 68):
    expected = 4 if order == 34 else 0
    assert sp.factor(B_full.coeff(t, order) - expected) == 0
assert sp.factor(B_full.coeff(t, 68) - expected_plus) == 0


print("verified hostile audit of the (12,9) half-order resonance")
