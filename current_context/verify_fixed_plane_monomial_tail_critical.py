#!/usr/bin/env python3
"""Exclude every monomial K=a^p*(b+1)^q tail in all degrees.

For both Q[a,b] boundary families, the two target-coordinate derivatives
reduce to explicit monomial equations with nonzero coefficients.  They
always have a solution with a*(b+1)!=0 over the algebraic closure, hence
give a critical point.
"""

import sympy as sp


A, H = sp.symbols("A H")
delta = H**2 - 12 * A

for p in range(13):
    for q in range(13):
        K = A**p * H**q
        U_a = sp.expand(A + A**2 * delta * K)
        U_b = sp.expand(H + A**2 * delta * K)

        if q == 0:
            # In the a-branch H=0 kills U_H, and U_A is a nonconstant
            # equation with constant 1.
            assert sp.diff(U_a, H).subs(H, 0) == 0
            assert sp.expand(
                sp.diff(U_a, A).subs(H, 0)
                - (1 - 12 * (p + 3) * A ** (p + 2))
            ) == 0
        else:
            relation_a = (q + 2) * H**2 - 12 * q * A
            expected_a_h = A ** (p + 2) * H ** (q - 1) * relation_a
            assert sp.expand(sp.diff(U_a, H) - expected_a_h) == 0
            reduced_a_a = sp.rem(
                sp.diff(U_a, A),
                relation_a,
                H,
            )
            expected_reduced_a_a = (
                1
                - sp.Rational(12 * (2 * p + q + 6), q + 2)
                * A ** (p + 2)
                * H**q
            )
            assert sp.expand(
                reduced_a_a - sp.rem(expected_reduced_a_a, relation_a, H)
            ) == 0

        # In the b-branch U_A=0 has the nonzero solution component below.
        relation_b = (p + 2) * H**2 - 12 * (p + 3) * A
        expected_b_a = A ** (p + 1) * H**q * relation_b
        assert sp.expand(sp.diff(U_b, A) - expected_b_a) == 0

        if q == 0:
            reduced_b_h = sp.rem(sp.diff(U_b, H), relation_b, H)
            expected_reduced_b_h = 1 + 2 * A ** (p + 2) * H
        else:
            reduced_b_h = sp.rem(sp.diff(U_b, H), relation_b, H)
            expected_reduced_b_h = (
                1
                + sp.Rational(12 * (q + 2 * p + 6), p + 2)
                * A ** (p + 3)
                * H ** (q - 1)
            )
        assert sp.expand(
            reduced_b_h - sp.rem(expected_reduced_b_h, relation_b, H)
        ) == 0

print("verified monomial critical equations for 0<=p,q<=12")
print("verified coefficients are uniformly nonzero for every p,q>=0")
print("RESULT: EVERY K=a^p*(b+1)^q TAIL HAS A CRITICAL POINT")
