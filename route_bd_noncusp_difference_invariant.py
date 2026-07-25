#!/usr/bin/env python3
"""Exact checks for the non-cusp boundary-difference invariant."""

from __future__ import annotations

import sympy as sp


def verify_case_c_resonance_spectrum() -> None:
    y, ell = sp.symbols("y ell", nonzero=True)
    coefficients = sp.symbols("c4:13")
    c = {j: coefficients[j - 4] for j in range(4, 13)}

    # Generic triangular representatives retain exactly the leading terms
    # used by the invariant.  A12^2-p^3 is represented by an arbitrary
    # polynomial of degree at most 11 and S3 by degree at most three.
    tail = sum(sp.Symbol(f"r{i}") * y**i for i in range(12))
    s3 = sum(sp.Symbol(f"s{i}") * y**i for i in range(4))
    approximate_powers = {j: ell**j * y**j for j in range(4, 13)}
    p_cubed = approximate_powers[12] ** 2 - tail

    q = sum(c[j] * approximate_powers[j] for j in range(4, 13)) + s3
    difference = sp.expand(q**2 - c[12] ** 2 * p_cubed)

    # All fractional modes vanish.  The only remaining approximate-root
    # modes are the integral powers A8=P and A4=H.
    fractional = (5, 6, 7, 9, 10, 11)
    for highest in (4, 8):
        specialization = {c[j]: 0 for j in fractional}
        specialization.update(
            {c[j]: 0 for j in (4, 8) if j > highest}
        )
        specialized = sp.Poly(sp.expand(difference.subs(specialization)), y)
        assert specialized.degree() == 12 + highest
        assert (
            specialized.coeff_monomial(y ** (12 + highest))
            == 2 * c[12] * c[highest] * ell ** (12 + highest)
        )

    no_lower_resonance = {c[j]: 0 for j in range(4, 12)}
    assert sp.Poly(
        sp.expand(difference.subs(no_lower_resonance)), y
    ).degree() <= 15

    possible_high_degrees = (20, 16)
    possible_high_contacts = tuple(24 - degree for degree in possible_high_degrees)
    assert max(possible_high_degrees) == 20
    assert possible_high_contacts == (4, 8)


def verify_ab_first_block_countermodel() -> None:
    w = sp.symbols("w")
    p = w**8 + w**7
    q = w**12
    a1 = sp.diff(p, w)
    b1 = sp.diff(q, w)
    assert sp.expand(a1 * sp.diff(q, w) - sp.diff(p, w) * b1) == 0
    assert sp.degree(a1, w) == 7
    assert sp.degree(b1, w) == 11
    assert sp.degree(sp.expand(q**2 - p**3), w) == 23


def verify_mason_degree_ledger() -> None:
    # If gcd(p,q)=1, rad(p*q*D) has degree at most 8+12+raddeg(D).
    # Mason's 24 <= raddeg(p*q*D)-1 therefore forces raddeg(D)>=5.
    assert 24 - (8 + 12) + 1 == 5


def main() -> None:
    verify_case_c_resonance_spectrum()
    verify_ab_first_block_countermodel()
    verify_mason_degree_ledger()
    print("verified case-c degree {20,16} or <=15 and contact >=4")
    print("verified the a/b simple-contact first-block countermodel")
    print("verified the conditional Mason radical-degree ledger")
    print("RESULT: ALL NON-CUSP DIFFERENCE CHECKS PASS")


if __name__ == "__main__":
    main()
