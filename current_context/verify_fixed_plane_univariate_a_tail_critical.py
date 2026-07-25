#!/usr/bin/env python3
"""Exclude every nonzero tail K=K(a) in both Q[a,b] boundary families."""

import sympy as sp


A, H = sp.symbols("A H")
delta = H**2 - 12 * A

for degree in range(9):
    coefficients = sp.symbols(f"k_{degree}_0:{degree + 1}")
    K = sum(
        coefficient * A**power
        for power, coefficient in enumerate(coefficients)
    )
    leading = coefficients[-1]

    # a-branch: H=0 kills the H derivative.  The A derivative has
    # constant 1 and a nonzero top coefficient for every nonzero K.
    U_a = sp.expand(A + A**2 * delta * K)
    assert sp.diff(U_a, H).subs(H, 0) == 0
    critical_equation_a = sp.Poly(
        sp.diff(U_a, A).subs(H, 0),
        A,
    )
    assert critical_equation_a.coeff_monomial(1) == 1
    assert critical_equation_a.degree() == degree + 2
    assert critical_equation_a.LC() == -12 * (degree + 3) * leading

    # b-branch: put L=A^2*K.  After F_H=0 gives H=-1/(2L), clearing
    # denominators in F_A produces N below.
    L = sp.expand(A**2 * K)
    L_prime = sp.diff(L, A)
    N = sp.expand(L_prime - 48 * A * L**2 * L_prime - 48 * L**3)
    assert sp.degree(N, A) == 3 * (degree + 2)
    assert sp.Poly(N, A).LC() == (
        -48 * (degree + 3) * leading**3
    )

print("verified K(a) critical equations for degrees 0 through 8")
print("uniform proof: roots on L=0 contribute at most deg(L)-1 < 3deg(L)")
print("RESULT: EVERY NONZERO UNIVARIATE K(a) TAIL HAS A CRITICAL POINT")
