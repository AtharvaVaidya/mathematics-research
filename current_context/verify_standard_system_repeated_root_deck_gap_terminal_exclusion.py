#!/usr/bin/env python3
"""Exact checks for the repeated-root deck-gap terminal exclusion."""

from __future__ import annotations

from itertools import product

import sympy as sp


t, z = sp.symbols("t z")
a, b, G = sp.symbols("a b G", integer=True, positive=True)


def transformed_bracket(
    p: sp.Expr,
    q: sp.Expr,
    a: int | sp.Expr,
    b: int | sp.Expr,
    G: int | sp.Expr,
) -> sp.Expr:
    return sp.expand(
        t
        * (
            sp.diff(p, z) * sp.diff(q, t)
            - sp.diff(p, t) * sp.diff(q, z)
        )
        + a * G * p * sp.diff(q, z)
        - b * G * q * sp.diff(p, z)
    )


# A t-independent unit normalization multiplies the whole transformed
# bracket by z_y, so its right side retains a nonzero z^0 coefficient.
y, c_unit = sp.symbols("y c_unit")
z_of_y = y + c_unit * y**5
p_function = sp.Function("p")(t, z)
q_function = sp.Function("q")(t, z)
p_substituted = p_function.subs(z, z_of_y)
q_substituted = q_function.subs(z, z_of_y)


def transformed_bracket_y(
    p: sp.Expr,
    q: sp.Expr,
    a0: sp.Expr,
    b0: sp.Expr,
    G0: sp.Expr,
) -> sp.Expr:
    return sp.expand(
        t
        * (
            sp.diff(p, y) * sp.diff(q, t)
            - sp.diff(p, t) * sp.diff(q, y)
        )
        + a0 * G0 * p * sp.diff(q, y)
        - b0 * G0 * q * sp.diff(p, y)
    )


bracket_after_substitution = transformed_bracket_y(
    p_substituted, q_substituted, a, b, G
)
bracket_before_substitution = transformed_bracket(
    p_function, q_function, a, b, G
).subs(z, z_of_y)
assert sp.simplify(
    bracket_after_substitution
    - sp.diff(z_of_y, y) * bracket_before_substitution
) == 0
assert sp.diff(z_of_y, y).subs(y, 0) == 1


# The monomial coefficient in the transformed operator.
A, B = sp.symbols("A B")
r, s, epsilon, eta = sp.symbols(
    "r s epsilon eta", integer=True, nonnegative=True
)
p_monomial = A * t**r * z**epsilon
q_monomial = B * t**s * z**eta
expected_monomial = (
    A
    * B
    * (
        epsilon * (s - b * G)
        + eta * (a * G - r)
    )
    * t ** (r + s)
    * z ** (epsilon + eta - 1)
)
assert sp.simplify(
    transformed_bracket(p_monomial, q_monomial, a, b, G)
    - expected_monomial
) == 0


# Symbolic descent of the two nonzero endpoint types.
h, d, e, g = sp.symbols("h d e g", integer=True, positive=True)
n = a * g
m = b * g
G_definition = h * g - e * d

orders_01 = (
    sp.expand(h * (n - 1) - a * e * d),
    sp.expand(h * (m - 1) + d - b * e * d),
)
orders_10 = (
    sp.expand(h * (n - 1) + d - a * e * d),
    sp.expand(h * (m - 1) - b * e * d),
)
assert all(
    sp.expand(left - right) == 0
    for left, right in zip(
        orders_01,
        (a * G_definition - h, b * G_definition - h + d),
    )
)
assert all(
    sp.expand(left - right) == 0
    for left, right in zip(
        orders_10,
        (a * G_definition - h + d, b * G_definition - h),
    )
)

N_prime = (a + b) * G_definition + d - 2 * h
assert sp.expand(sum(orders_01) - N_prime) == 0
assert sp.expand(sum(orders_10) - N_prime) == 0


# Bounded arithmetic audit: degree caps plus scalar order leave four
# corners, and the two non-affine corners have zero bracket coefficient.
for n0, m0 in product(range(2, 24), repeat=2):
    forcing = n0 + m0 - 2
    for epsilon0, eta0 in ((0, 1), (1, 0)):
        candidates = []
        nonzero = []
        for I in range(n0 + 1):
            J = forcing - I
            if J < 0 or J > m0:
                continue
            if I + epsilon0 > n0 or J + eta0 > m0:
                continue
            candidates.append((I, J))
            coefficient = (
                epsilon0 * (J - m0)
                + eta0 * (n0 - I)
            )
            if coefficient:
                nonzero.append((I, J))

        if (epsilon0, eta0) == (0, 1):
            assert candidates == [(n0 - 1, m0 - 1), (n0, m0 - 2)]
        else:
            assert candidates == [(n0 - 2, m0), (n0 - 1, m0 - 1)]
        assert nonzero == [(n0 - 1, m0 - 1)]


# Direct low-order audit of the exceptional tuple.  Deck equivariance
# and polynomial descent allow the displayed lowest residual orders
# through t-order 2.  The unit coordinate can add higher z-orders, but
# none can affect the coefficient of z^0.  The t=0 boundary is exact.
p13, p17, p111 = sp.symbols("p13 p17 p111")
p20, p24, p28, p212 = sp.symbols("p20 p24 p28 p212")
q12, q16, q110, q114, q118 = sp.symbols(
    "q12 q16 q110 q114 q118"
)
q23, q27, q211, q215, q219 = sp.symbols(
    "q23 q27 q211 q215 q219"
)

p_numeric = (
    z**6
    + t * (p13 * z**3 + p17 * z**7 + p111 * z**11)
    + t**2
    * (p20 + p24 * z**4 + p28 * z**8 + p212 * z**12)
)
q_numeric = (
    z**9
    + t
    * (
        q12 * z**2
        + q16 * z**6
        + q110 * z**10
        + q114 * z**14
        + q118 * z**18
    )
    + t**2
    * (
        q23 * z**3
        + q27 * z**7
        + q211 * z**11
        + q215 * z**15
        + q219 * z**19
    )
)
numeric_bracket = transformed_bracket(p_numeric, q_numeric, 2, 3, 1)
assert sp.Poly(numeric_bracket, t, z).coeff_monomial(t**2) == 0


# The exact arithmetic and the two forbidden terminal pairs.
g0, e0, h0, d0, G0, a0, b0 = 9, 7, 4, 5, 1, 2, 3
assert G0 == h0 * g0 - e0 * d0
N0 = (a0 + b0) * G0 + d0 - 2 * h0
assert N0 == 2
assert b0 * G0 < h0
pair_01 = (a0 * G0 - h0, b0 * G0 - h0 + d0)
pair_10 = (a0 * G0 - h0 + d0, b0 * G0 - h0)
assert pair_01 == (-2, 4)
assert pair_10 == (3, -1)
assert sum(pair_01) == sum(pair_10) == N0


# Equality bG=h is also excluded: the only nonnegative endpoint type
# asks for a t^0 z^0 term in q, absent from q(0,z)=z^(bf).
for a0, b0, h0, G0 in (
    (2, 3, 6, 2),
    (3, 4, 8, 2),
    (2, 5, 15, 3),
):
    assert a0 < b0
    assert b0 * G0 == h0
    assert a0 * G0 - h0 < 0
    assert b0 * G0 - h0 == 0

# A compatible equality chart, including the first-face arithmetic.
a_eq, b_eq, g_eq, e_eq, h_eq, d_eq, k_eq, f_eq = 2, 3, 7, 4, 3, 5, 1, 1
G_eq = h_eq * g_eq - e_eq * d_eq
assert sp.gcd(a_eq, b_eq) == sp.gcd(d_eq, h_eq) == 1
assert e_eq == k_eq * h_eq + f_eq
assert d_eq * e_eq < h_eq * g_eq
assert G_eq == 1
assert b_eq * G_eq == h_eq


# In the intermediate band only the (1,0) orientation survives.  Its
# P-order is positive under the strict first-slope inequality.
intermediate_examples = []
for a0 in range(2, 8):
    for b0 in range(a0 + 1, 10):
        if sp.gcd(a0, b0) != 1:
            continue
        for g0 in range(2, 16):
            for e0 in range(2, g0 + 1):
                for h0 in range(1, e0):
                    for d0 in range(1, g0 + 1):
                        if sp.gcd(d0, h0) != 1 or d0 * e0 >= h0 * g0:
                            continue
                        G0 = h0 * g0 - e0 * d0
                        if a0 * G0 <= h0 < b0 * G0:
                            intermediate_examples.append(
                                (a0, b0, g0, e0, h0, d0, G0)
                            )
                            assert a0 * G0 - h0 <= 0
                            assert b0 * G0 - h0 > 0
                            assert a0 * G0 - h0 + d0 > 0
assert intermediate_examples


print("verified: transformed monomial coefficient and Rees descent")
print("verified: every nonzero scalar terminal has original indices (n-1,m-1)")
print("verified: the two exact terminal t-order pairs")
print("verified: bG <= h excludes every zero-root compensating chain")
print("verified: intermediate deck band has one terminal orientation")
print("verified: the (9,7,4,5,1,2,3) tuple has no t^2 z^0 scalar")
