#!/usr/bin/env python3
"""Exact symbolic resultant for the first resonant defect chamber.

For the resonant family

    E = 9 or 11, s=(E+1)/2,

the first permitted obstruction is at defect five and the next one
is at defect seven.  Sparse affine-exponent division in symbolic E
gives the two homogeneous polynomials below.  This verifier checks:

1. their exact specializations against the ordinary filtered
   recurrence at E=9,11;
2. their symbolic resultant;
3. positivity after shifting the sole nontrivial resultant factor
   by E -> E+9.
"""

from __future__ import annotations

import sympy as sp


x, ell, u, E, z = sp.symbols("x ell u E z", nonzero=True)


def p5_polynomial() -> sp.Expr:
    """The homogeneous defect-five numerator after scalar factors."""
    coefficients = (
        43008 * E**12,
        10752 * E**10 * (23 * E + 11),
        1152 * E**8 * (505 * E**2 + 542 * E + 133),
        192
        * E**6
        * (3016 * E**3 + 5493 * E**2 + 3168 * E + 563),
        48
        * E**4
        * (
            4349 * E**4
            + 12320 * E**3
            + 12726 * E**2
            + 5584 * E
            + 861
        ),
        (E + 1)
        * (3 * E + 1) ** 2
        * (
            1377 * E**4
            + 3915 * E**3
            + 3771 * E**2
            + 885 * E
            - 268
        ),
    )
    return sp.expand(
        sum(
            coefficient * ell ** (15 - 3 * power) * u**power
            for power, coefficient in enumerate(coefficients)
        )
    )


def q7_polynomial() -> sp.Expr:
    """The homogeneous defect-seven numerator after scalar factors."""
    coefficients = (
        77856768 * E**18,
        19464192 * E**16 * (39 * E + 17),
        196608
        * E**14
        * (16725 * E**2 + 15731 * E + 3465),
        12288
        * E**12
        * (
            633273 * E**3
            + 956767 * E**2
            + 458551 * E
            + 69209
        ),
        3072
        * E**10
        * (
            3426555 * E**4
            + 7407348 * E**3
            + 5780286 * E**2
            + 1911700 * E
            + 225007
        ),
        768
        * E**8
        * (
            10209383 * E**5
            + 29735661 * E**4
            + 33759058 * E**3
            + 18488862 * E**2
            + 4839319 * E
            + 481893
        ),
        384
        * E**6
        * (
            7455867 * E**6
            + 28300528 * E**5
            + 44248915 * E**4
            + 36116076 * E**3
            + 16056205 * E**2
            + 3650276 * E
            + 329573
        ),
        32
        * E**3
        * (3 * E + 1)
        * (
            4048299 * E**7
            + 18362691 * E**6
            + 35326848 * E**5
            + 36588378 * E**4
            + 21269415 * E**3
            + 6482635 * E**2
            + 796206 * E
            + 536
        ),
        (E + 1)
        * (3 * E + 1) ** 3
        * (
            315657 * E**6
            + 1347840 * E**5
            + 2502765 * E**4
            + 2500584 * E**3
            + 1312995 * E**2
            + 230552 * E
            - 41305
        ),
    )
    return sp.expand(
        sum(
            coefficient * ell ** (24 - 3 * power) * u**power
            for power, coefficient in enumerate(coefficients)
        )
    )


P5 = p5_polynomial()
Q7 = q7_polynomial()
assert sp.Poly(P5, u).degree() == 5
assert sp.Poly(Q7, u).degree() == 8


def filtered_obstructions(e_value: int) -> tuple[sp.Expr, sp.Expr]:
    """Compute the ordinary exact defect-five/seven coordinates."""
    s_value = (e_value + 1) // 2
    g_value = s_value + e_value
    d = x**s_value * (x**e_value + ell)
    d1 = sp.diff(d, x)
    field = sp.QQ.frac_field(ell, u)
    A = u + 2 * d * d1
    B = 3 * d**2 * d1
    inverse_a = sp.invert(A, B, domain=field)
    p = [d**2 + u * x, -4 * d1 / (3 * u**2)]
    q = [d**3, 1 / u - 2 * d * d1 / u**2]
    values: dict[int, sp.Expr] = {}

    for defect in range(2, 8):
        h = -sum(
            j * sp.diff(p[i], x) * q[j]
            - i * p[i] * sp.diff(q[j], x)
            for i in range(1, defect)
            for j in [defect - i]
        ) / defect
        q_new = sp.rem(
            sp.expand(inverse_a * h),
            B,
            x,
            domain=field,
        )
        p_new = sp.cancel((A * q_new - h) / B)
        assert p_new.is_polynomial(x)
        p.append(p_new)
        q.append(q_new)
        if defect == 5:
            values[5] = sp.Poly(q_new, x).coeff_monomial(
                x ** (5 * e_value - 6)
            )
        if defect == 7:
            values[7] = sp.Poly(q_new, x).coeff_monomial(
                x ** (5 * e_value - 9)
            )

    return sp.factor(values[5]), sp.factor(values[7])


for e_value in (9, 11):
    actual5, actual7 = filtered_obstructions(e_value)
    expected5 = (
        -ell
        * (3 * E + 1)
        * P5
        / (972 * u**18)
    ).subs(E, e_value)
    expected7 = (
        ell
        * (3 * E + 1)
        * Q7
        / (104976 * u**26)
    ).subs(E, e_value)
    assert sp.factor(actual5 - expected5) == 0
    assert sp.factor(actual7 - expected7) == 0


# Exact symbolic resultant.  The scalar and three elementary factors
# are separated; the remaining factor has degree 52.
p5_univariate = P5.subs(ell, 1)
q7_univariate = Q7.subs(ell, 1)
resultant = sp.resultant(p5_univariate, q7_univariate, u)
factorization = sp.factor_list(resultant, E)
factor_degrees = sorted(
    (sp.degree(factor, E), multiplicity)
    for factor, multiplicity in factorization[1]
)
assert factor_degrees == [(1, 1), (1, 3), (1, 90), (52, 1)]

linear_factors = {
    sp.Poly(factor, E).monic().as_expr(): multiplicity
    for factor, multiplicity in factorization[1]
    if sp.degree(factor, E) == 1
}
assert linear_factors == {
    E: 90,
    E + 1: 1,
    E + sp.Rational(1, 3): 3,
}

residual = next(
    factor
    for factor, multiplicity in factorization[1]
    if sp.degree(factor, E) == 52
)
shifted = sp.Poly(sp.expand(residual.subs(E, z + 9)), z)
assert shifted.degree() == 52
assert all(coefficient > 0 for coefficient in shifted.all_coeffs())

# Hence the resultant is nonzero on every real E>=9, in particular
# at the two integer values for which defects five and seven are the
# first consecutive permitted characters.
for e_value in (9, 11):
    assert resultant.subs(E, e_value) != 0
    specialized_p = sp.Poly(p5_univariate.subs(E, e_value), u)
    specialized_q = sp.Poly(q7_univariate.subs(E, e_value), u)
    assert sp.gcd(specialized_p, specialized_q).degree() == 0

print("verified: symbolic defect-five and defect-seven formulas")
print("verified: exact ordinary recurrence specializations E=9,11")
print("verified: resultant has one residual degree-52 factor")
print("verified: shifted residual is coefficientwise positive for E>=9")
print("verified: the first two permitted classes are coprime at E=9,11")
