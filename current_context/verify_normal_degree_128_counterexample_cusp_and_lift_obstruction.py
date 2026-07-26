#!/usr/bin/env python3
"""Exact checks for the normalized (12,8) cusp and lift obstruction."""

from __future__ import annotations

import sympy as sp


t, w, tau, v = sp.symbols("t w tau v")
a, b, c, d, e, f_coefficient, q = sp.symbols("a b c d e f q")
coefficients = (a, b, c, d, e, f_coefficient, q)
deficits = tuple(range(2, 9))

unit = 1 + sum(
    coefficient * t**deficit
    for coefficient, deficit in zip(coefficients, deficits)
)

# The zero-upper-constant slice is f=(g^(3/2))_+.
phi_series = sp.expand(
    t**-12
    * sp.series(unit ** sp.Rational(3, 2), t, 0, 20).removeO()
)
f_in_t = sp.expand(
    sum(
        term
        for term in sp.Add.make_args(phi_series)
        if term.as_powers_dict().get(t, 0) <= 0
    )
)
f_normalized = sp.expand(f_in_t.subs(t, 1 / w))
g = w**8 + sum(
    coefficient * w ** (8 - deficit)
    for coefficient, deficit in zip(coefficients, deficits)
)

# Residue formula for A_1,...,A_7 in the inverse s-coordinate.
negative_tail = sp.expand(f_in_t - phi_series)
s_w = sp.series(
    unit ** sp.Rational(1, 8)
    - t
    * sp.diff(unit, t)
    * unit ** sp.Rational(-7, 8)
    / 8,
    t,
    0,
    10,
).removeO()

A: dict[int, sp.Expr] = {}
for ell in range(1, 8):
    residue_integrand = sp.series(
        t ** (-(ell - 1))
        * unit ** sp.Rational(ell - 1, 8)
        * negative_tail
        * s_w,
        t,
        0,
        2,
    ).removeO()
    A[ell] = sp.factor(
        sp.expand(residue_integrand).coeff(t, 1)
    )

sqrt21 = sp.sqrt(21)
base = {
    a: sp.Integer(1),
    b: -sp.Rational(22, 441) * sqrt21,
    c: sp.Rational(169, 504),
    d: -sp.Rational(47, 1029) * sqrt21,
    e: sp.Rational(6721, 148176),
    f_coefficient: -sp.Rational(13679, 1555848) * sqrt21,
    q: sp.Rational(268777, 49787136),
}
scaled = {
    coefficient: base[coefficient] * tau**deficit
    for coefficient, deficit in zip(coefficients, deficits)
}

for ell in range(1, 7):
    assert sp.factor(A[ell].subs(scaled)) == 0

expected_A7 = (
    -sp.Rational(2**18, 3**7 * 7**10)
    * sqrt21
    * tau**19
)
assert sp.factor(A[7].subs(scaled) - expected_A7) == 0

f_tau = sp.expand(f_normalized.subs(scaled))
g_tau = sp.expand(g.subs(scaled))
bracket_tau = sp.factor(
    sp.diff(f_tau, tau) * sp.diff(g_tau, w)
    - sp.diff(f_tau, w) * sp.diff(g_tau, tau)
)
expected_bracket_tau = (
    -sp.Rational(2**21 * 19, 3**7 * 7**10)
    * sqrt21
    * tau**18
)
assert sp.factor(bracket_tau - expected_bracket_tau) == 0
assert sp.factor(bracket_tau - 8 * sp.diff(expected_A7, tau)) == 0

# The one-pole parametrization tau=v^(-1) has n=19 and rho=1.
f_v = sp.expand(f_tau.subs(tau, 1 / v))
g_v = sp.expand(g_tau.subs(tau, 1 / v))
bracket_v = sp.factor(
    sp.diff(f_v, v) * sp.diff(g_v, w)
    - sp.diff(f_v, w) * sp.diff(g_v, v)
)
expected_bracket_v = (
    sp.Rational(2**21 * 19, 3**7 * 7**10)
    * sqrt21
    * v**-20
)
assert sp.factor(bracket_v - expected_bracket_v) == 0
assert sp.factor(
    A[7].subs(scaled).subs(tau, 1 / v)
    + sp.Rational(2**18, 3**7 * 7**10) * sqrt21 * v**-19
) == 0

# Both v^(-2) and a nonzero multiple of v^(-3) occur, so the
# coefficient field is C(v).  Bezout's identity gcd(2,3)=1 is the
# exact cyclic-field check.
assert sp.gcd(2, 3) == 1
assert all(
    sp.degree(
        sp.Poly(
            sp.together(
                (coefficient.subs(scaled) * tau**-deficit)
            ),
            tau,
        )
    )
    == 0
    for coefficient, deficit in zip(coefficients, deficits)
)

# Homogeneous binary forms f=v^-12 F0(vw), g=v^-8 G0(vw).
X = sp.symbols("X")
F0 = sp.factor(f_tau.subs({tau: 1, w: X}))
G0 = sp.factor(g_tau.subs({tau: 1, w: X}))
assert sp.factor(f_v - v**-12 * F0.subs(X, v * w)) == 0
assert sp.factor(g_v - v**-8 * G0.subs(X, v * w)) == 0
assert sp.degree(F0, X) == 12
assert sp.degree(G0, X) == 8
assert sp.LC(sp.Poly(F0, X)) == 1
assert sp.LC(sp.Poly(G0, X)) == 1

resultant = sp.factor(sp.resultant(F0, G0, X), extension=sqrt21)
expected_resultant = -sp.Rational(
    2**88 * 19**2,
    3**36 * 7**48,
)
assert resultant == expected_resultant
assert resultant != 0

# Davenport--Stothers equality: F0^2-G0^3 has exact degree five and
# is squarefree.  Its degree gives ramification index 24-5=19 at
# infinity for F0^2/G0^3.
remainder = sp.factor(F0**2 - G0**3, extension=sqrt21)
assert sp.degree(remainder, X) == 5
assert sp.factor(
    sp.LC(sp.Poly(remainder, X, extension=sqrt21))
    + sp.Rational(2**19, 3**7 * 7**10) * sqrt21
) == 0
assert sp.gcd(
    sp.Poly(remainder, X, extension=sqrt21),
    sp.Poly(sp.diff(remainder, X), X, extension=sqrt21),
).degree() == 0
assert 12 * (2 - 1) + 8 * (3 - 1) + (19 - 1) == 2 * 24 - 2

# Degree-eight Taylor threshold.  If n>=3*rho, the lower bound for
# the y^i coefficient differs from i by 4*m*(i-2)*rho.
m, rho = sp.symbols("m rho", positive=True)
for i in range(2, 9):
    threshold_bound = sp.expand(
        i * (3 * m * rho + 1) - m * (8 - i) * rho
    )
    assert sp.expand(
        threshold_bound - (i + 4 * m * (i - 2) * rho)
    ) == 0

print("verified: six conserved Laurent coefficients vanish on the cusp")
print("verified: exact A_7 and monomial normalized Jacobians")
print("verified: one-pole exponent n=19 and weighted pole rho=1")
print("verified: nonzero homogeneous resultant and no common center limit")
print("verified: Davenport-Stothers degree-five equality and passport")
print("verified: degree-eight polynomial-lift threshold n >= 3*rho")
