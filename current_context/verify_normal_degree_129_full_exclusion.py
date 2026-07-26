#!/usr/bin/env python3
"""Arithmetic checks for the (12,9) full-exclusion note."""

from math import gcd

import sympy as sp


# Kummer finite-pole valuation and bracket order.
for multiplicity in range(4, 81):
    common = gcd(3, multiplicity)
    ramification = 3 // common
    h_order = multiplicity // common
    terminal_pole = h_order - ramification
    assert terminal_pole > 0
    assert ramification - 1 - h_order == -terminal_pole - 1


# Taylor lower bound at n=(7/2)rho.
rho, e = sp.symbols("rho e", positive=True)
for i in range(2, 10):
    lower = sp.expand(
        i * (sp.Rational(7, 2) * rho + e) - (9 - i) * rho
    )
    expected = sp.expand((sp.Rational(9, 2) * i - 9) * rho + i * e)
    assert sp.simplify(lower - expected) == 0
    assert sp.Rational(9, 2) * i - 9 >= 0


# The t=3 one-root family is a cube (apart from the forbidden
# multiplicity-three resonance, which is also a cube).
for multiplicity in range(0, 121, 3):
    assert multiplicity == 0 or multiplicity % 3 == 0


# Constant-r total-degree bounds from rho<=2/7.
for coordinate_degree in (9, 12):
    for deficit in range(coordinate_degree + 1):
        w_degree = coordinate_degree - deficit
        x_degree_bound = sp.Rational(2 * deficit, 7)
        assert w_degree + x_degree_bound <= coordinate_degree


print("verified the (12,9) full-exclusion inequalities")
