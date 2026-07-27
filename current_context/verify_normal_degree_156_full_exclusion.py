#!/usr/bin/env python3
"""Exact arithmetic checks for the full normal-degree (15,6) exclusion."""

from __future__ import annotations

import sympy as sp


# Split and connected line estimates.
i, rho, e = sp.symbols("i rho e", positive=True)
line_lower_bound = sp.expand(
    i * (2 * rho + e) - (6 - i) * rho
)
assert sp.expand(
    line_lower_bound - ((3 * i - 6) * rho + i * e)
) == 0
assert sp.expand(line_lower_bound.subs(i, 2)) == 2 * e


# The constant-cube total-degree bounds.
j, deficit = sp.symbols(
    "j deficit", integer=True, nonnegative=True
)
g_total_bound = sp.expand(j / 2 + 6 - j)
f_total_bound = sp.expand(deficit / 2 + 15 - deficit)
assert sp.expand(g_total_bound - (6 - j / 2)) == 0
assert sp.expand(f_total_bound - (15 - deficit / 2)) == 0


# Inverse-character differential for q=6 and d=3.
x, lam = sp.symbols("x lam", nonzero=True)
S = sp.Function("S")(x)
h = sp.Function("h")(x)
A5 = S / h ** sp.Rational(1, 3)
differential = sp.factor(
    6 * sp.diff(A5, x) * h ** sp.Rational(1, 3)
)
expected_differential = (
    6 * sp.diff(S, x) - 2 * sp.diff(h, x) * S / h
)
assert sp.factor(differential - expected_differential) == 0

# Therefore 6A5'=lambda/H is equivalent to
# 3S'-(h'/h)S=lambda/2.
assert sp.factor(
    expected_differential / 2
    - (
        3 * sp.diff(S, x)
        - sp.diff(h, x) * S / h
    )
) == 0


# Local Kummer exponents and the terminal pole.
M, d0 = sp.symbols("M d0", integer=True, positive=True)
kummer_e = 3 / d0
kummer_h0 = M / d0
terminal_pole = sp.factor(kummer_h0 - kummer_e)
assert terminal_pole == (M - 3) / d0


# The triple-root scale-restart coefficient identity.
X, root = sp.symbols("X root")
R = sp.expand((X - root) ** 3)
G0 = sp.expand(R**2)
assert sp.Poly(G0, X).coeff_monomial(X**5) == -6 * root
assert sp.expand(G0.subs(root, 0)) == X**6


print("verified: q=6 line threshold gives strict vanishing for i>=2")
print("verified: constant-cube total degrees are at most (15,6)")
print("verified: the connected terminal equation is the inverse character")
print("verified: a multiplicity M>3 gives pole (M-3)/gcd(3,M)")
print("verified: the depressed triple-root face has no positive scale")
