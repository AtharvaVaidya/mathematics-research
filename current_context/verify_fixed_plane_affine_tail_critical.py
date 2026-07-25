#!/usr/bin/env python3
"""Exclude every affine K tail in the Q[a,b] boundary classification.

After scaling the nonzero linear boundary term, the two families are

    U_a = a + a^2*Delta*(k0+k1*a+k2*(b+1)),
    U_b = b + a^2*Delta*(k0+k1*a+k2*(b+1)).

The constant-tail stratum k1=k2=0 is checked separately.  Here exact
resultants and saturated coefficient ideals show that for every
(k1,k2)!=(0,0) the derivative resultant has a nonzero t-root.  The
top c-coefficient has no multiple nonzero root, so this resultant root
is a finite common root of U_t and U_c, hence a critical point.
"""

import sympy as sp


t, c = sp.symbols("t c")
k0, k1, k2, inverse = sp.symbols("k0 k1 k2 inverse")
a = t + t**2 - c * t**3
b = 2 + 4 * t - 3 * c * t**2
H = b + 1
delta = H**2 - 12 * a
K = k0 + k1 * a + k2 * H


def t_valuation(polynomial):
    dictionary = sp.Poly(polynomial, t).as_dict()
    return min(exponent[0] for exponent in dictionary)


for base, name, expected_valuation, secondary_exponent in (
    (a, "a", 59, 2),
    (b, "b", 54, 3),
):
    U = sp.expand(base + a**2 * delta * K)
    U_as_c = sp.Poly(U, c)
    assert U_as_c.degree() == 5
    assert sp.factor(U_as_c.LC()) == -9 * t**12 * (k1 * t + 3 * k2)

    resultant = sp.expand(
        sp.resultant(sp.diff(U, t), sp.diff(U, c), c)
    )
    valuation = t_valuation(resultant)
    assert valuation == expected_valuation
    residual = sp.Poly(sp.expand(resultant / t**valuation), t)
    coefficients = {
        exponent[0]: coefficient
        for exponent, coefficient in residual.as_dict().items()
    }

    # Chart k2!=0: the residual has a nonzero constant coefficient.
    constant = sp.factor(coefficients[0])
    constant_ratio = sp.factor(constant / k2**4)
    assert constant_ratio.is_number and constant_ratio != 0
    positive_coefficients = [
        coefficient
        for exponent, coefficient in coefficients.items()
        if exponent > 0
    ]
    saturated_k2 = sp.groebner(
        positive_coefficients + [inverse * k2 - 1],
        inverse,
        k0,
        k1,
        k2,
        order="grevlex",
    )
    assert list(saturated_k2) == [1]

    # Chart k2=0, k1!=0, k0!=0: the first surviving coefficient is
    # nonzero and the saturated ideal says some other coefficient survives.
    first = sp.factor(coefficients[secondary_exponent].subs(k2, 0))
    first_ratio = sp.factor(first / (k0**4 * k1))
    assert first_ratio.is_number and first_ratio != 0
    other_coefficients = [
        coefficient.subs(k2, 0)
        for exponent, coefficient in coefficients.items()
        if exponent != secondary_exponent and coefficient.subs(k2, 0) != 0
    ]
    saturated_k0_k1 = sp.groebner(
        other_coefficients + [inverse * k0 * k1 - 1],
        inverse,
        k0,
        k1,
        order="grevlex",
    )
    assert list(saturated_k0_k1) == [1]

    # Final chart k2=k0=0, k1!=0: at least two explicit t-powers survive.
    surviving_exponents = [
        exponent
        for exponent, coefficient in coefficients.items()
        if coefficient.subs({k2: 0, k0: 0}) != 0
    ]
    assert len(surviving_exponents) >= 2

    print(
        f"verified {name}-branch resultant: t-valuation {valuation}, "
        "nonmonomial on every nonconstant affine-K chart"
    )

print("verified u_5=-9*t^12*(k1*t+3*k2) has no multiple nonzero root")
print("RESULT: EVERY NONCONSTANT AFFINE K TAIL HAS A CRITICAL POINT")
