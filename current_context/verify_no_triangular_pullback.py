#!/usr/bin/env python3
"""Exact function-field check for NO_TRIANGULAR_COORDINATE_PULLBACK.md."""

import sympy as sp


A, B, C, T, lam = sp.symbols("A B C T lam")
HA, HB, HC = sp.symbols("HA HB HC")

minimal = C * T**3 - 2 * T**2 + B * T - 2 * A
r = sp.diff(minimal, T)
numerator = 8 * (T**3 * HA + 3 * T**2 * HB - HC) - lam * r**3

forced = {
    HA: lam * (9 * A * C - B) * (3 * B * C - 4) / (4 * B),
    HB: -lam * (12 * A - B**2) * (3 * B * C - 4) / (8 * B),
    HC: -lam * (12 * A - B**2) ** 2 / (8 * B),
}

remainder = sp.rem(
    sp.Poly(sp.together(numerator.subs(forced) * B), T),
    sp.Poly(minimal, T),
)
assert all(sp.factor(coefficient) == 0 for coefficient in remainder.all_coeffs())
print("verified: forced gradient makes the cubic remainder vanish")

curl_ab = sp.factor(sp.diff(forced[HA], B) - sp.diff(forced[HB], A))
expected_curl = (
    3 * lam * (12 * A * C + 5 * B**2 * C - 8 * B) / (4 * B**2)
)
assert sp.factor(curl_ab - expected_curl) == 0
assert curl_ab != 0
print("verified: forced gradient has nonzero mixed-partial defect")

print("all triangular-pullback checks passed")
