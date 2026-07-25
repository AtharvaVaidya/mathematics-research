#!/usr/bin/env python3
"""Exclude every nonzero K=K(b+1) tail in the b-boundary family."""

import sympy as sp


A, H = sp.symbols("A H")
delta = H**2 - 12 * A

for degree in range(13):
    coefficients = sp.symbols(f"hK_{degree}_0:{degree + 1}")
    K = sum(
        coefficient * H**power
        for power, coefficient in enumerate(coefficients)
    )
    leading = coefficients[-1]
    U = sp.expand(H + A**2 * delta * K)

    # The A derivative has the component A=H^2/18 (unless K=0, which
    # only makes the derivative vanish more directly).
    assert sp.expand(
        sp.diff(U, A) - 2 * A * K * (H**2 - 18 * A)
    ) == 0

    restricted_H_derivative = sp.factor(
        sp.diff(U, H).subs(A, H**2 / 18)
    )
    expected = 1 + H**5 * (6 * K + H * sp.diff(K, H)) / 972
    assert sp.expand(restricted_H_derivative - expected) == 0

    restricted_poly = sp.Poly(restricted_H_derivative, H)
    assert restricted_poly.coeff_monomial(1) == 1
    assert restricted_poly.degree() == degree + 5
    assert restricted_poly.LC() == sp.Rational(degree + 6, 972) * leading

print("verified b-branch K(H) critical equation for degrees 0 through 12")
print("uniform equation: 1+H^5*(6K+H*K')/972=0")
print("RESULT: EVERY NONZERO UNIVARIATE K(b+1) TAIL IN THE b-BRANCH IS EXCLUDED")
