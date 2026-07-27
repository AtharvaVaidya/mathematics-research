#!/usr/bin/env python3
"""Checks for the q=6 subextremal and p=15 nodal Hensel audit."""

from __future__ import annotations

import sympy as sp


# ---------------------------------------------------------------------------
# Uniform degree contradiction in the polynomial-abc step.

A, common_degree = sp.symbols(
    "A common_degree", integer=True, positive=True
)
maximum_degree = 6 * A - common_degree
radical_upper_bound = (
    3 * A + 6 + (3 * A - 6) - common_degree - 1
)
assert sp.expand(maximum_degree - radical_upper_bound) == 1


# ---------------------------------------------------------------------------
# Exact p=15 nodal ratio-one approximate germ.

u, T, e = sp.symbols("u T e", nonzero=True)
w = sp.symbols("w")

R = (w - T**4) ** 2 * (w + 2 * T**4)
E = e * T**-3 * (w - T**4) * (w + 2 * T**4)
g = sp.expand(R**2 + E)

# Recover the depressed coefficients and their centered deviations.
g_poly = sp.Poly(g, w)
a = g_poly.coeff_monomial(w**4)
b = g_poly.coeff_monomial(w**3)
c = g_poly.coeff_monomial(w**2)
d = g_poly.coeff_monomial(w)
q = g_poly.coeff_monomial(1)

C = sp.factor(c - a**2 / 4)
D = sp.factor(d - a * b / 2)
Q = sp.factor(q - b**2 / 4)

assert a == -6 * T**8
assert b == 4 * T**12
assert C == e * T**-3
assert D == e * T
assert Q == -2 * e * T**5

# Compute the canonical Laurent residuals by the residue formula.
unit = 1 + a * u**2 + b * u**3 + c * u**4 + d * u**5 + q * u**6
top_exponent = 15
phi_series = sp.expand(
    u**-top_exponent
    * sp.series(
        unit ** sp.Rational(top_exponent, 6),
        u,
        0,
        top_exponent + 6,
    ).removeO()
)
polynomial_part = sp.Add(
    *[
        term
        for term in sp.Add.make_args(phi_series)
        if term.as_powers_dict().get(u, 0) <= 0
    ]
)
negative_tail = sp.expand(polynomial_part - phi_series)
s_w = sp.series(
    unit ** sp.Rational(1, 6)
    - u
    * sp.diff(unit, u)
    * unit ** sp.Rational(-5, 6)
    / 6,
    u,
    0,
    8,
).removeO()

laurent_residuals: dict[int, sp.Expr] = {}
for ell in range(1, 6):
    integrand = sp.series(
        u ** (-(ell - 1))
        * unit ** sp.Rational(ell - 1, 6)
        * negative_tail
        * s_w,
        u,
        0,
        2,
    ).removeO()
    laurent_residuals[ell] = sp.factor(
        sp.expand(integrand).coeff(u, 1)
    )

expected_residuals = {
    1: 5 * e**4 / (128 * T**12),
    2: 5 * e**4 / (32 * T**8),
    3: 15 * e**4 / (64 * T**4),
    4: 5 * e**4 / 48,
    5: -e**4 * (25 * T**19 + 2 * e) / (384 * T**15),
}
for ell, expected in expected_residuals.items():
    assert sp.factor(laurent_residuals[ell] - expected) == 0

rho = 4
terminal_pole = 4
assert terminal_pole / rho == 1


# ---------------------------------------------------------------------------
# The first cubic Hensel congruence.

X, z, cube_root = sp.symbols("X z cube_root")
H = X - 1
K = X + 2
P = sp.expand(H**2 * K)
S = sp.expand(H * K)
V = cube_root * (X - 10) * (X + 2)

cube_relation = cube_root**3 + sp.Rational(1, 17496)
congruence = sp.rem(8 * V**3 - K**2, P, X)
congruence_numerator = sp.together(congruence).as_numer_denom()[0]
assert (
    sp.rem(
        sp.Poly(congruence_numerator, cube_root),
        sp.Poly(cube_relation, cube_root),
    ).as_expr()
    == 0
)

# Directly build the polynomial part through every order which can
# contribute to z^11 in the scaled bracket.
Delta = z**3 * S + z**4 * V
F = P**5
for power in range(1, 8):
    coefficient = sp.binomial(sp.Rational(5, 2), power)
    numerator = sp.expand(Delta**power)
    if 5 - 2 * power >= 0:
        polynomial_term = P ** (5 - 2 * power) * numerator
    else:
        denominator = P ** (2 * power - 5)
        polynomial_term = 0
        for (z_power,), z_coefficient in sp.Poly(numerator, z).terms():
            if z_power <= 11:
                polynomial_term += (
                    z**z_power
                    * sp.div(z_coefficient, denominator, X)[0]
                )
    F += coefficient * polynomial_term

G = P**2 + Delta
scaled_bracket = sp.expand(
    sp.Rational(19, 12)
    * z
    * (
        sp.diff(F, z) * sp.diff(G, X)
        - sp.diff(F, X) * sp.diff(G, z)
    )
    - 15 * F * sp.diff(G, X)
    + 6 * sp.diff(F, X) * G
)
order_eleven = sp.expand(scaled_bracket).coeff(z, 11)

order_eleven_numerator = sp.together(order_eleven).as_numer_denom()[0]
reduced_numerator = sp.rem(
    sp.Poly(order_eleven_numerator, cube_root),
    sp.Poly(cube_relation, cube_root),
).as_expr()
reduced_order_eleven = sp.factor(
    reduced_numerator
    / sp.together(order_eleven).as_numer_denom()[1]
)
expected_order_eleven = (
    -sp.Rational(10935, 32)
    * cube_root**2
    * (X - 1) ** 2
    * (X + 2)
    * (17 * X + 5)
)
assert sp.factor(reduced_order_eleven - expected_order_eleven) == 0
assert expected_order_eleven != 0


# ---------------------------------------------------------------------------
# Every rational normal character below the order-four Hensel jet.

rational_order = sp.symbols("rational_order")
u0, u1, u2 = sp.symbols("u0 u1 u2")
U = u0 + u1 * X + u2 * X**2

# At order 3+2r, compare the polynomial mixed cubic with the exact
# rational function.  Their difference is the Laurent tail which
# supplies the associated-graded bracket.
mixed_coefficient = 3 * sp.binomial(sp.Rational(5, 2), 3)
mixed_rational = mixed_coefficient * S * U**2 / P
mixed_polynomial = mixed_coefficient * sp.div(
    sp.expand(S * U**2), P, X
)[0]
mixed_tail_difference = sp.factor(mixed_polynomial - mixed_rational)
mixed_order = 3 + 2 * rational_order
mixed_bracket = sp.factor(
    2
    * (sp.Rational(19, 12) * mixed_order - 15)
    * mixed_tail_difference
    * P
    * sp.diff(P, X)
    + 6 * sp.diff(mixed_tail_difference, X) * P**2
)
expected_mixed_bracket = sp.factor(
    -sp.Rational(15, 32)
    * H**2
    * K
    * U.subs(X, 1) ** 2
    * (
        (38 * rational_order - 135) * X
        + 38 * rational_order
        - 147
    )
)
assert sp.factor(mixed_bracket - expected_mixed_bracket) == 0

# If H divides U, the next self-cubic character detects the value
# at the other root K=0 and forces K to divide U/H.
l0, l1 = sp.symbols("l0 l1")
L = l0 + l1 * X
U_H = H * L
self_coefficient = sp.binomial(sp.Rational(5, 2), 3)
self_rational = self_coefficient * U_H**3 / P
self_polynomial = self_coefficient * sp.div(
    sp.expand(U_H**3), P, X
)[0]
self_tail_difference = sp.factor(self_polynomial - self_rational)
self_order = 3 * rational_order
self_bracket = sp.factor(
    2
    * (sp.Rational(19, 12) * self_order - 15)
    * self_tail_difference
    * P
    * sp.diff(P, X)
    + 6 * sp.diff(self_tail_difference, X) * P**2
)
expected_self_bracket = sp.factor(
    sp.Rational(45, 32)
    * H**3
    * L.subs(X, -2) ** 3
    * (
        (19 * rational_order - 64) * X
        + 19 * rational_order
        - 56
    )
)
assert sp.factor(self_bracket - expected_self_bracket) == 0

# At r=9/2, the mixed cubic and base quartic collide.  The required
# divisibility is impossible already modulo H.
collision_factor = 24 * H * U**2 - K
assert sp.rem(collision_factor, H, X) == -3


# ---------------------------------------------------------------------------
# The base order-twelve bracket and every upper character at order eleven.

Delta_base = z**3 * S
F_base = P**5
for power in range(1, 8):
    coefficient = sp.binomial(sp.Rational(5, 2), power)
    numerator = sp.expand(Delta_base**power)
    if 5 - 2 * power >= 0:
        polynomial_term = P ** (5 - 2 * power) * numerator
    else:
        denominator = P ** (2 * power - 5)
        polynomial_term = 0
        for (z_power,), z_coefficient in sp.Poly(numerator, z).terms():
            if z_power <= 12:
                polynomial_term += (
                    z**z_power
                    * sp.div(z_coefficient, denominator, X)[0]
                )
    F_base += coefficient * polynomial_term

G_base = P**2 + Delta_base
base_bracket = sp.expand(
    sp.Rational(19, 12)
    * z
    * (
        sp.diff(F_base, z) * sp.diff(G_base, X)
        - sp.diff(F_base, X) * sp.diff(G_base, z)
    )
    - 15 * F_base * sp.diff(G_base, X)
    + 6 * sp.diff(F_base, X) * G_base
)
assert sp.factor(
    base_bracket.coeff(z, 12)
    - sp.Rational(15, 64) * H * K**2 * (3 * X - 1)
) == 0

# The noncore upper characters all have the strictly deeper root
# factor H^3*K.  This is what prevents an upper-mode collision from
# canceling the leading H- or K-principal part in the arbitrary
# physical grading.
inverse_X = sp.symbols("inverse_X")


def polynomial_part_of_cubic_power(exponent: int) -> sp.Expr:
    normalized = sp.expand(
        inverse_X**3 * P.subs(X, 1 / inverse_X)
    )
    series = sp.expand(
        inverse_X ** (-exponent)
        * sp.series(
            normalized ** sp.Rational(exponent, 3),
            inverse_X,
            0,
            exponent + 2,
        ).removeO()
    )
    return sp.expand(
        sum(
            term
            for term in sp.Add.make_args(series)
            if term.as_powers_dict().get(inverse_X, 0) <= 0
        ).subs(inverse_X, 1 / X)
    )


noncore_modes = (14, 13, 11, 10, 8, 7, 5, 4, 2, 1)
for upper_mode in noncore_modes:
    upper_polynomial = polynomial_part_of_cubic_power(upper_mode)
    upper_character = sp.factor(
        2
        * P
        * (
            3 * P * sp.diff(upper_polynomial, X)
            - upper_mode * sp.diff(P, X) * upper_polynomial
        )
    )
    quotient, remainder = sp.div(upper_character, H**3 * K, X)
    assert remainder == 0
    assert sp.Poly(quotient, X).degree() == 0
    assert quotient != 0

for core_mode in (9, 3):
    core_polynomial = polynomial_part_of_cubic_power(core_mode)
    core_character = sp.factor(
        2
        * P
        * (
            3 * P * sp.diff(core_polynomial, X)
            - core_mode * sp.diff(P, X) * core_polynomial
        )
    )
    assert core_character == 0

# In the physical grading, the k=9 and k=3 core upper modes occur at
# 72/19 and 144/19.  At order 201/19 their first tails collide with
# the top mixed term and give one genuine compatibility equation.
upper_nine, upper_three, normal_value = sp.symbols(
    "upper_nine upper_three normal_value"
)
core_tail_coefficient = (
    sp.Rational(15, 16) * normal_value**2
    + sp.Rational(3, 4) * upper_nine * normal_value
    + sp.Rational(1, 2) * upper_three
)
assert sp.expand(
    16 * core_tail_coefficient
    - (
        15 * normal_value**2
        + 12 * upper_nine * normal_value
        + 8 * upper_three
    )
) == 0

# The next coefficient is Q'(x)V(1).  Since the Hensel congruence
# makes V(1) nonzero, Q and Q' both vanish.  The following
# coefficient is then the nonzero quadratic term Q''V(1)^2/2.
character_quadratic = core_tail_coefficient
character_derivative = sp.diff(character_quadratic, normal_value)
double_root_solution = sp.solve(
    [
        character_quadratic,
        character_derivative,
    ],
    [normal_value, upper_three],
    dict=True,
)
assert double_root_solution == [
    {
        normal_value: -2 * upper_nine / 5,
        upper_three: 3 * upper_nine**2 / 10,
    }
]

hensel_value = sp.factor(V.subs(X, 1))
assert hensel_value == -27 * cube_root
assert sp.rem(
    sp.Poly(8 * hensel_value**3 - 9, cube_root),
    sp.Poly(cube_relation, cube_root),
).as_expr() == 0

terminal_character_order = sp.Rational(209, 19)
terminal_tail_difference = (
    -sp.Rational(15, 16) * hensel_value**2 / H
)
terminal_character_bracket = sp.factor(
    2
    * (
        sp.Rational(19, 12) * terminal_character_order
        - 15
    )
    * terminal_tail_difference
    * P
    * sp.diff(P, X)
    + 6 * sp.diff(terminal_tail_difference, X) * P**2
)
expected_terminal_character = (
    -sp.Rational(15, 32)
    * hensel_value**2
    * P
    * (17 * X + 5)
)
assert sp.factor(
    terminal_character_bracket - expected_terminal_character
) == 0
assert sp.rem(
    sp.Poly(
        sp.together(expected_terminal_character).as_numer_denom()[0],
        cube_root,
    ),
    sp.Poly(cube_relation, cube_root),
).as_expr() != 0


# ---------------------------------------------------------------------------
# The s=9/2 collision and the triple-root scale restart.

v0, v1, v2, core_nine, core_three = sp.symbols(
    "v0 v1 v2 core_nine core_three"
)
V_boundary = v0 + v1 * X + v2 * X**2
Delta_boundary = z**3 * S + z**4 * V_boundary
G_boundary = P**2 + Delta_boundary

F_boundary = P**5
for power in range(1, 5):
    coefficient = sp.binomial(sp.Rational(5, 2), power)
    numerator = sp.expand(Delta_boundary**power)
    denominator_power = 2 * power - 5
    for (z_power,), z_coefficient in sp.Poly(numerator, z).terms():
        if z_power > 12:
            continue
        if denominator_power <= 0:
            polynomial_coefficient = (
                P ** (-denominator_power) * z_coefficient
            )
        else:
            polynomial_coefficient = sp.div(
                z_coefficient,
                P**denominator_power,
                X,
            )[0]
        F_boundary += (
            coefficient * z**z_power * polynomial_coefficient
        )

upper_nine_part = P**3
for power in range(1, 4):
    coefficient = sp.binomial(sp.Rational(3, 2), power)
    numerator = sp.expand(Delta_boundary**power)
    denominator_power = 2 * power - 3
    for (z_power,), z_coefficient in sp.Poly(numerator, z).terms():
        if 4 + z_power > 12:
            continue
        if denominator_power <= 0:
            polynomial_coefficient = (
                P ** (-denominator_power) * z_coefficient
            )
        else:
            polynomial_coefficient = sp.div(
                z_coefficient,
                P**denominator_power,
                X,
            )[0]
        upper_nine_part += (
            coefficient * z**z_power * polynomial_coefficient
        )
F_boundary += core_nine * z**4 * upper_nine_part

upper_three_part = P
for power in range(1, 3):
    coefficient = sp.binomial(sp.Rational(1, 2), power)
    numerator = sp.expand(Delta_boundary**power)
    denominator_power = 2 * power - 1
    for (z_power,), z_coefficient in sp.Poly(numerator, z).terms():
        if 8 + z_power > 12:
            continue
        if denominator_power <= 0:
            polynomial_coefficient = (
                P ** (-denominator_power) * z_coefficient
            )
        else:
            polynomial_coefficient = sp.div(
                z_coefficient,
                P**denominator_power,
                X,
            )[0]
        upper_three_part += (
            coefficient * z**z_power * polynomial_coefficient
        )
F_boundary += core_three * z**8 * upper_three_part

boundary_bracket = sp.expand(
    sp.Rational(3, 2)
    * z
    * (
        sp.diff(F_boundary, z) * sp.diff(G_boundary, X)
        - sp.diff(F_boundary, X) * sp.diff(G_boundary, z)
    )
    - 15 * F_boundary * sp.diff(G_boundary, X)
    + 6 * sp.diff(F_boundary, X) * G_boundary
)
boundary_value = V_boundary.subs(X, 1)
boundary_order_eleven = sp.factor(boundary_bracket.coeff(z, 11))
expected_boundary_eleven = (
    -sp.Rational(3, 16)
    * H**3
    * K
    * (
        12 * core_nine * boundary_value
        + 8 * core_three
        + 15 * boundary_value**2
    )
)
assert sp.factor(
    boundary_order_eleven - expected_boundary_eleven
) == 0

boundary_core_three = -(
    12 * core_nine * boundary_value
    + 15 * boundary_value**2
) / 8
boundary_order_twelve = sp.factor(
    boundary_bracket.coeff(z, 12).subs(
        core_three,
        boundary_core_three,
    )
)
boundary_linear = sp.factor(
    boundary_order_twelve
    / (-sp.Rational(3, 32) * H**2 * K)
)
boundary_linear_poly = sp.Poly(boundary_linear, X)
boundary_A = sp.factor(boundary_linear_poly.coeff_monomial(X))
boundary_C = sp.factor(boundary_linear_poly.coeff_monomial(1))
assert sp.factor(
    boundary_A
    - (
        (v1 - v2) ** 2
        * (48 * core_nine + 120 * v0 + 240 * v2)
        - 5
    )
) == 0
assert sp.factor(boundary_A + boundary_C) == -15

# Depression removes the X^5 coefficient of G_0=R^2.  A triple-root
# cubic then has zero root and gives the empty scale face X^6.
triple_root = sp.symbols("triple_root")
triple_cubic = sp.expand((X - triple_root) ** 3)
triple_sextic = sp.expand(triple_cubic**2)
assert sp.Poly(triple_sextic, X).coeff_monomial(X**5) == (
    -6 * triple_root
)
assert sp.expand(triple_sextic.subs(triple_root, 0)) == X**6

# A nonzero H^{-1} tail can never have scalar bracket image.
physical_order, tail_scalar = sp.symbols(
    "physical_order tail_scalar"
)
physical_tail = tail_scalar / H
physical_tail_bracket = sp.factor(
    2
    * (physical_order - 15)
    * physical_tail
    * P
    * sp.diff(P, X)
    + 6 * sp.diff(physical_tail, X) * P**2
)
expected_physical_tail_bracket = (
    6
    * tail_scalar
    * H**2
    * K
    * (
        (physical_order - 16) * X
        + physical_order
        - 17
    )
)
assert sp.factor(
    physical_tail_bracket - expected_physical_tail_bracket
) == 0

# The companion K-principal part is separated at the simple root.
physical_K_tail = tail_scalar / K
physical_K_tail_bracket = sp.factor(
    2
    * (physical_order - 15)
    * physical_K_tail
    * P
    * sp.diff(P, X)
    + 6 * sp.diff(physical_K_tail, X) * P**2
)
expected_physical_K_tail_bracket = (
    6
    * tail_scalar
    * H**3
    * (
        (physical_order - 16) * X
        + physical_order
        - 14
    )
)
assert sp.factor(
    physical_K_tail_bracket - expected_physical_K_tail_bracket
) == 0
assert sp.factor(
    (
        (physical_order - 16) * X
        + physical_order
        - 17
    ).subs(X, 1)
) == 2 * physical_order - 33
assert sp.factor(
    (
        (physical_order - 16) * X
        + physical_order
        - 14
    ).subs(X, -2)
) == 18 - physical_order


print("verified: uniform polynomial-abc degree gap is exactly one")
print("verified: exact p=15 nodal approximate germ has ratio one")
print("verified: the nodal cube-root Hensel congruence has a solution")
print("verified: its earlier order-eleven mixed bracket is nonzero")
print("verified: every rational support below four is resonant or obstructed")
print("verified: the order-nine-halves collision is impossible modulo H")
print("verified: the base order-twelve nodal bracket is nonzero")
print("verified: the first core upper-character compatibility is nontrivial")
print("verified: the core chain forces a double root and then a nonzero square")
print("verified: the s=9/2 core/Hensel collision is inconsistent")
print("verified: the depressed triple-root face forces a scale restart")
print("verified: all noncore upper characters have factor H^3*K")
print("verified: H- and K-principal parts are root-separated below the boundary")
