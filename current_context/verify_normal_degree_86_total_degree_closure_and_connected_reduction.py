#!/usr/bin/env python3
"""Exact checks for the degree-(8,6) closure and connected reduction."""

from __future__ import annotations

import math

import sympy as sp


# ---------------------------------------------------------------------------
# Arithmetic criteria.


def criterion_value(value: int) -> bool:
    return value in (1, 4) or sp.isprime(value)


narrow_theorem_27_gaps: list[tuple[int, int, int, int, int]] = []
for maximum in range(2, 9):
    for m in range(2, maximum + 1):
        for n in range(1, m):
            if m != maximum:
                continue
            common = math.gcd(m, n)
            a0, b0 = m // common, n // common
            for t0 in range(1, common + 1):
                if common % t0:
                    continue
                left, right = a0 * t0, b0 * t0
                if not criterion_value(left) and not criterion_value(right):
                    narrow_theorem_27_gaps.append((m, n, t0, left, right))

assert narrow_theorem_27_gaps == [(8, 6, 2, 8, 6)]

# Add the total-degree gcd-p/2p criterion and remove b=1 power-shear
# charts.  The first surviving pair is then (9,6), d=t=3.
full_uncovered: list[tuple[int, int, int, int, int]] = []
for maximum in range(2, 10):
    for m in range(2, maximum + 1):
        for n in range(1, m):
            if m != maximum:
                continue
            common = math.gcd(m, n)
            a0, b0 = m // common, n // common
            if b0 == 1:
                continue
            for t0 in range(1, common + 1):
                if common % t0:
                    continue
                left, right = a0 * t0, b0 * t0
                covered = (
                    t0 in (1, 2)
                    or criterion_value(left)
                    or criterion_value(right)
                )
                if not covered:
                    full_uncovered.append((m, n, t0, left, right))

assert full_uncovered == [(9, 6, 3, 9, 6)]


# ---------------------------------------------------------------------------
# The depressed connected-cover coefficient system.

w = sp.symbols("w")
a, b, c, d, q, j, eps = sp.symbols("a b c d q j eps")
ap, bp, cp, dp, qp = sp.symbols("ap bp cp dp qp")
variables = (a, b, c, d, q)
derivatives = (ap, bp, cp, dp, qp)
velocity = dict(zip(variables, derivatives))


def deriv(expression: sp.Expr) -> sp.Expr:
    return sp.expand(
        sum(sp.diff(expression, variable) * velocity[variable] for variable in variables)
    )


A = sp.Rational(4, 3) * a
B = sp.Rational(4, 3) * b
C = sp.Rational(4, 3) * c + sp.Rational(2, 9) * a**2 + j
D = sp.Rational(4, 3) * d + sp.Rational(4, 9) * a * b
E = (
    sp.Rational(4, 3) * q
    - sp.Rational(4, 81) * a**3
    + sp.Rational(4, 9) * a * c
    + sp.Rational(2, 3) * a * j
    + sp.Rational(2, 9) * b**2
    + eps
)
L1 = (
    -sp.Rational(4, 27) * a**2 * b
    + sp.Rational(4, 9) * a * d
    + sp.Rational(4, 9) * b * c
    + sp.Rational(2, 3) * b * j
)
P = (
    5 * a**4
    - 36 * a**2 * c
    - 27 * a**2 * j
    - 36 * a * b**2
    + 81 * a * eps
    + 108 * a * q
    + 108 * b * d
    + 54 * c**2
    + 162 * c * j
) / 243

f = w**8 + A * w**6 + B * w**5 + C * w**4 + D * w**3 + E * w**2 + L1 * w + P
g = w**6 + a * w**4 + b * w**3 + c * w**2 + d * w + q

fx = deriv(f)
gx = deriv(g)
bracket = sp.Poly(sp.expand(fx * sp.diff(g, w) - sp.diff(f, w) * gx), w)

# The seven upper coefficients have been integrated completely.
for power in range(11, 4, -1):
    assert sp.expand(bracket.coeff_monomial(w**power)) == 0


# The same normal form is the polynomial part of a fractional-power
# approximate root.
t = sp.symbols("t")
unit = 1 + a * t**2 + b * t**3 + c * t**4 + d * t**5 + q * t**6
psi = sp.expand(
    t**-8 * sp.series(unit ** sp.Rational(4, 3), t, 0, 13).removeO()
    + j * t**-4 * sp.series(unit ** sp.Rational(2, 3), t, 0, 13).removeO()
    + eps * t**-2 * sp.series(unit ** sp.Rational(1, 3), t, 0, 13).removeO()
)
polynomial_part_in_t = 0
for term in sp.Add.make_args(psi):
    exponent = term.as_powers_dict().get(t, 0)
    if exponent <= 0:
        polynomial_part_in_t += term
assert sp.expand(polynomial_part_in_t.subs(t, 1 / w) - f) == 0


# ---------------------------------------------------------------------------
# Four exact weighted first integrals.

I9 = (
    20 * a**3 * b
    - 36 * a**2 * d
    - 72 * a * b * c
    - 54 * a * b * j
    - 12 * b**3
    + 81 * b * eps
    + 108 * b * q
    + 108 * c * d
    + 162 * d * j
)
I10 = (
    8 * a**5
    - 60 * a**3 * c
    - 36 * a**3 * j
    - 90 * a**2 * b**2
    + 81 * a**2 * eps
    + 108 * a**2 * q
    + 216 * a * b * d
    + 108 * a * c**2
    + 162 * a * c * j
    + 108 * b**2 * c
    + 81 * b**2 * j
    - 243 * c * eps
    - 324 * c * q
    - 162 * d**2
    - 486 * j * q
)
I11 = (
    20 * a**4 * b
    - 28 * a**3 * d
    - 96 * a**2 * b * c
    - 54 * a**2 * b * j
    - 36 * a * b**3
    + 81 * a * b * eps
    + 108 * a * b * q
    + 108 * a * c * d
    + 54 * a * d * j
    + 72 * b**2 * d
    + 72 * b * c**2
    + 108 * b * c * j
    - 162 * d * eps
    - 216 * d * q
) / 81
I12 = -(
    40 * a**6
    - 360 * a**4 * c
    - 162 * a**4 * j
    - 720 * a**3 * b**2
    + 324 * a**3 * eps
    + 432 * a**3 * q
    + 1620 * a**2 * b * d
    + 972 * a**2 * c**2
    + 972 * a**2 * c * j
    + 1944 * a * b**2 * c
    + 972 * a * b**2 * j
    - 1458 * a * c * eps
    - 1944 * a * c * q
    - 972 * a * d**2
    + 162 * b**4
    - 729 * b**2 * eps
    - 972 * b**2 * q
    - 2916 * b * c * d
    - 1458 * b * d * j
    - 648 * c**3
    - 1458 * c**2 * j
    + 4374 * eps * q
    + 2916 * q**2
) / 2187

R4 = bracket.coeff_monomial(w**4)
R3 = bracket.coeff_monomial(w**3)
R2 = bracket.coeff_monomial(w**2)
R1 = bracket.coeff_monomial(w)
R0 = bracket.coeff_monomial(1)

assert sp.expand(R4 + sp.Rational(2, 81) * deriv(I9)) == 0
assert sp.expand(R3 - sp.Rational(2, 243) * deriv(I10)) == 0
assert sp.expand(R2 - deriv(I11) + a * deriv(I9) / 81) == 0
assert sp.expand(
    R1
    - deriv(I12)
    + sp.Rational(2, 243) * b * deriv(I9)
    - sp.Rational(2, 729) * a * deriv(I10)
) == 0
assert sp.expand(R0 + L1 * qp - deriv(P) * d) == 0


# Weighted homogeneity.
weight_map = {a: 2, b: 3, c: 4, d: 5, q: 6, j: 4, eps: 6}


def monomial_weight(term: sp.Expr) -> int:
    powers = term.as_powers_dict()
    return sum(weight_map[symbol] * int(powers.get(symbol, 0)) for symbol in weight_map)


for expression, expected in ((I9, 9), (I10, 10), (I11, 11), (I12, 12)):
    terms = sp.Poly(expression, *weight_map).terms()
    assert terms
    for exponents, _ in terms:
        observed = sum(weight * exponent for weight, exponent in zip(weight_map.values(), exponents))
        assert observed == expected


# Connected-cover parity: a,c,q,j,eps are even and b,d are odd.
def parity(expression: sp.Expr) -> set[int]:
    outcomes: set[int] = set()
    polynomial = sp.Poly(expression, a, b, c, d, q, j, eps)
    for exponents, _ in polynomial.terms():
        b_exponent = exponents[1]
        d_exponent = exponents[3]
        outcomes.add((b_exponent + d_exponent) % 2)
    return outcomes


assert parity(I9) == {1}
assert parity(I10) == {0}
assert parity(I11) == {1}
assert parity(I12) == {0}


# ---------------------------------------------------------------------------
# Exact two-channel decomposition before specializing the coefficients.

u = sp.symbols("u")
P0 = sp.Function("P0")
P1 = sp.Function("P1")
Q0 = sp.Function("Q0")
Q1 = sp.Function("Q1")

# An algebraic expansion with independent placeholders checks the universal
# even/odd formulas without invoking any parity assumption.
p0x, p0u, p1x, lp1 = sp.symbols("p0x p0u p1x lp1")
q0x, q0u, q1x, lq1 = sp.symbols("q0x q0u q1x lq1")
even_channel = p0x * lq1 + 2 * u * p1x * q0u - lp1 * q0x - 2 * u * p0u * q1x
odd_channel = 2 * (p0x * q0u - p0u * q0x) + p1x * lq1 - lp1 * q1x

# Direct multiplication of (P0+wP1)_x(P0+wP1)_w-type expressions.
direct = sp.expand(
    (p0x + w * p1x) * (2 * w * q0u + lq1)
    - (2 * w * p0u + lp1) * (q0x + w * q1x)
)
reduced = sp.rem(sp.Poly(direct - even_channel - w * odd_channel, w), sp.Poly(w**2 - u, w))
assert reduced.as_expr() == 0


# ---------------------------------------------------------------------------
# Square-chart countercheck: the residual constant is not killed by descent.

x, y, z = sp.symbols("x y z")
F_square = (x * y) ** 8 + (x * y) ** 7
G_square = (x * y) ** 6
normalized_f = sp.expand(F_square.subs(y, z / x))
normalized_g = sp.expand(G_square.subs(y, z / x))
assert normalized_f == z**8 + z**7
assert normalized_g == z**6
assert sp.Poly(normalized_f, z).coeff_monomial(z**7) == 1

print("verified: (8,6) is only a gap in the narrow one-coordinate criterion")
print("verified: the total-degree criterion closes (8,6)")
print("verified: the first full arithmetic frontier is (9,6), t=3")
print("verified: seven upper equations integrate to the displayed normal form")
print("verified: four exact first integrals have weights 9,10,11,12")
print("verified: the terminal equation is -L1*q' + P'*d = lambda/H")
print("verified: the square-h chart admits a nonzero residual constant")
