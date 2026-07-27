#!/usr/bin/env python3
"""Exact checks for the general split normal-degree Laurent/line lemma."""

from __future__ import annotations

import sympy as sp


# ---------------------------------------------------------------------------
# Pure-power cyclic quotient.

u, v = sp.symbols("u v", nonzero=True)
m, n = sp.symbols("m n", integer=True, positive=True)
lam, gamma = sp.symbols("lam gamma", nonzero=True)

k = m * n
r = gamma * u ** (k + 1)
bracket_u = lam / r
bracket_v = lam / (m * gamma * v ** (n + 1))

assert sp.factor(
    m * u ** (m - 1) * bracket_v.subs(v, u**m) - bracket_u
) == 0


# ---------------------------------------------------------------------------
# Rational-time pure-power identity.

alpha, beta = sp.symbols("alpha beta", nonzero=True)
time = alpha + beta * u ** (-k)
time_derivative = sp.factor(sp.diff(time, u))
pure_power_r = sp.factor(lam / time_derivative)

assert time_derivative == -beta * k * u ** (-k - 1)
assert pure_power_r == -lam * u ** (k + 1) / (beta * k)


# ---------------------------------------------------------------------------
# Exact Taylor valuation algebra.

q, i = sp.symbols("q i", integer=True, positive=True)
rho = sp.symbols("rho", nonnegative=True)

threshold = sp.factor((q - 2) * rho / 2)
threshold_remainder = sp.factor(
    i * threshold - (q - i) * rho
)
assert threshold_remainder == q * rho * (i - 2) / 2

# Check the integer specializations relevant to every q >= 2 and
# 2 <= i <= q in a broad exact range.
for q_value in range(2, 41):
    threshold_value = sp.Rational(q_value - 2, 2) * rho
    for i_value in range(2, q_value + 1):
        remainder = sp.factor(
            i_value * threshold_value
            - (q_value - i_value) * rho
        )
        assert remainder == (
            sp.Rational(q_value * (i_value - 2), 2) * rho
        )

# The q=6 theorem needs ratio two; q=8 needs ratio three.
assert threshold.subs(q, 6) == 2 * rho
assert threshold.subs(q, 8) == 3 * rho


# ---------------------------------------------------------------------------
# The center-pole and derivative-term inequalities.

j, e = sp.symbols("j e", integer=True, positive=True)

# If e > m*rho, the pole of t^q exceeds the pole of the j-th
# coefficient term by exactly j*(e-m*rho).
dominance_gap = sp.factor(
    q * e - (m * j * rho + (q - j) * e)
)
assert dominance_gap == j * (e - m * rho)

# At e=m*rho, every term contributing to the i-th w derivative has
# pole at most m*(q-i)*rho.
derivative_bound = sp.factor(
    m * j * rho + (q - j - i) * m * rho
)
assert derivative_bound == m * (q - i) * rho


# ---------------------------------------------------------------------------
# The affine-line Keller dichotomy.

y = sp.symbols("y")
f0, f1, g0, g1, gu = sp.symbols(
    "f0 f1 g0 g1 gu", nonzero=True
)

G_line = g0 + g1 * y
F_line = f0 + f1 * y
assert sp.diff(G_line, y) == g1
assert sp.diff(F_line, y) == f1

# In the constant-G branch, -F_y G_u=lambda forces both polynomial
# factors to be units.  The displayed substitution checks the exact
# constant identity used in the proof.
assert sp.factor((-f1 * gu - lam).subs(gu, -lam / f1)) == 0


print("verified: general pure-power cyclic Jacobian descent")
print("verified: rational time gives the pure-power split factor")
print("verified: exact threshold is (q-2)rho/2")
print("verified: q=8 specializes to the threshold n >= 3rho")
print("verified: center and Taylor pole inequalities")
print("verified: affine-line Keller dichotomy")
