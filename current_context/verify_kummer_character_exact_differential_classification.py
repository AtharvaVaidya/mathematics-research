#!/usr/bin/env python3
"""Exact checks for KUMMER_CHARACTER_EXACT_DIFFERENTIAL_CLASSIFICATION.md."""

from math import gcd

import sympy as sp


x, a, b, c = sp.symbols("x a b c", nonzero=True)


def check_equation(d, S, h):
    """Return the normalized numerator equation d*S'-(h'/h)S."""
    return sp.factor(d * sp.diff(S, x) - sp.diff(h, x) * S / h)


# The complete two-root family.  It includes a multiplicity above d.
d, n = sp.symbols("d n", integer=True, positive=True)
P2 = (x - a) * (x - b)
S2 = d * c * P2 / (n * (a - b))
h2 = (x - a) ** (d - n) * (x - b) ** (d + n)
assert sp.simplify(check_equation(d, S2, h2) - d * c) == 0


# Connected cubic genus-one example: weights (1, 1, -2),
# multiplicities (2, 2, 5).
d3 = 3
P3 = x * (x**2 - 1)
S3 = sp.Rational(3, 2) * c * P3
h3 = (x + 1) ** 2 * (x - 1) ** 2 * x**5
assert sp.simplify(check_equation(d3, S3, h3) - d3 * c) == 0
assert gcd(gcd(gcd(d3, 2), 2), 5) == 1
g3 = 1 + (d3 * (3 - 2) - sum(gcd(d3, m) for m in (2, 2, 5))) // 2
assert g3 == 1


# Connected quartic genus-one example relevant to the (12,8) cover:
# weights (1, 1, -2), multiplicities (3, 3, 6).
d4 = 4
S4 = 2 * c * P3
h4 = (x + 1) ** 3 * (x - 1) ** 3 * x**6
assert sp.simplify(check_equation(d4, S4, h4) - d4 * c) == 0
assert gcd(gcd(gcd(d4, 3), 3), 6) == 1
g4 = 1 + (d4 * (3 - 2) - sum(gcd(d4, m) for m in (3, 3, 6))) // 2
assert g4 == 1


# Verify the moment polynomial for the common three-root example.
roots = (-1, 1, 0)
weights = (1, 1, -2)
P = sp.prod(x - root for root in roots)
Q = sp.expand(
    sum(
        weight * sp.cancel(P / (x - root))
        for root, weight in zip(roots, weights)
    )
)
assert Q == 2
assert sum(weights) == 0
assert sum(weight * root for root, weight in zip(roots, weights)) == 0
assert sum(weight * root**2 for root, weight in zip(roots, weights)) == 2


# R=A^d up to a constant.  It has no finite critical point outside
# {-1, 0, 1}; infinity is the remaining critical point.
R = sp.cancel((x + 1) * (x - 1) / x**2)
assert sp.factor(sp.diff(R, x) / R - sp.Rational(2, 1) / P3) == 0
u = sp.symbols("u")
R_at_infinity = sp.series(R.subs(x, 1 / u), u, 0, 5)
assert R_at_infinity.removeO().coeff(u, 1) == 0
assert R_at_infinity.removeO().coeff(u, 2) != 0


# One-root family, including m>d.  The forbidden finite resonance m=d
# is visible as the only zero denominator.
m = sp.symbols("m", integer=True, nonnegative=True)
S1 = d * c * (x - a) / (d - m)
h1 = (x - a) ** m
assert sp.simplify(check_equation(d, S1, h1) - d * c) == 0


print("verified exact Kummer inverse-character differential classification")
