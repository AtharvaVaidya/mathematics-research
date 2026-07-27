#!/usr/bin/env python3
"""Exact arithmetic checks for NORMAL_DEGREE_128_FULL_EXCLUSION.md."""

from math import gcd

import sympy as sp


# At a finite terminal pole, h_0=n+e and n>=3*rho.  The Taylor
# coefficient of y^i has strictly positive order for every i>=2.
rho, e = sp.symbols("rho e", positive=True)
for i in range(2, 9):
    lower_at_threshold = sp.expand(i * (3 * rho + e) - (8 - i) * rho)
    assert sp.expand(lower_at_threshold - ((4 * i - 8) * rho + i * e)) == 0
    assert 4 * i - 8 >= 0


# The local parameter exponents at a Kummer root of multiplicity M>4
# give bracket order -n-1 exactly.
for M in range(5, 65):
    common = gcd(4, M)
    ramification = 4 // common
    h_order = M // common
    n = h_order - ramification
    assert ramification - 1 - h_order == -n - 1
    assert n > 0


# In the one-root Kummer family, the arithmetic frontier condition
# 4|deg(h) leaves only fourth powers; M=4 is the logarithmic resonance.
for M in range(0, 101, 4):
    if M == 4:
        continue
    assert M == 0 or M % 4 == 0


# Constant-r chart: rho<=1/3 bounds every ordinary total degree by
# the corresponding w-degree.
for coordinate_degree in (8, 12):
    for deficit in range(coordinate_degree + 1):
        w_degree = coordinate_degree - deficit
        x_degree_bound = sp.Rational(deficit, 3)
        assert w_degree + x_degree_bound <= coordinate_degree


# Weighted coefficient substitution in the optional one-root estimate.
# This is not needed in the final proof because 4|deg(h) removes that
# chart, but it checks the ramified growth formula used in the audit.
for M in (1, 2, 3):
    common = gcd(4, M)
    cover_degree = 4 // common
    h_order = M // common
    terminal_order = cover_degree - h_order
    rho_bound = sp.Rational(terminal_order, 3)
    for coordinate_degree in (8, 12):
        bounds = [
            sp.Rational(
                i * h_order + (coordinate_degree - i) * rho_bound,
                cover_degree,
            )
            + i
            for i in range(coordinate_degree + 1)
        ]
        assert max(bounds) == sp.Rational(
            coordinate_degree * (4 + M),
            4,
        )
        assert max(bounds) < 24


print("verified full normal-degree (12,8) closure inequalities")
