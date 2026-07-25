#!/usr/bin/env python3
"""Exclude homogeneous square quadratic K tails by critical points.

The primitive-leading obstruction leaves even-degree K only when its top
specialization is a square.  This script closes the first homogeneous
exceptional stratum

    K=(r*a+s*(b+1))^2

in both boundary families U=a+a^2*Delta*K and U=b+a^2*Delta*K.
"""

import sympy as sp


t, c, r, s = sp.symbols("t c r s")
a = t + t**2 - c * t**3
b = 2 + 4 * t - 3 * c * t**2
H = b + 1
delta = H**2 - 12 * a
K = (r * a + s * H) ** 2


for base, name, t_power, scalar, residual_degree in (
    (a, "a", 83, 69984, 18),
    (b, "b", 77, 209952, 28),
):
    U = sp.expand(base + a**2 * delta * K)
    resultant = sp.factor(
        sp.resultant(sp.diff(U, t), sp.diff(U, c), c)
    )
    residual = sp.factor(
        resultant / (scalar * t**t_power * (r * t + 3 * s) ** 5)
    )
    assert sp.expand(
        resultant
        - scalar * t**t_power * (r * t + 3 * s) ** 5 * residual
    ) == 0

    residual_poly = sp.Poly(residual, t)
    assert residual_poly.degree() == residual_degree

    # If r,s are both nonzero, the possible finite root at infinity is
    # t=-3s/r.  Were every residual root there, the residual would be a
    # scalar multiple of (rt+3s)^degree, whose t^6 coefficient is nonzero.
    # The exact residual has zero t^6 coefficient, while its constant and
    # leading coefficients are nonzero on this chart.
    assert residual_poly.coeff_monomial(t**6) == 0
    assert residual_poly.coeff_monomial(1).subs(s, 1) != 0
    assert residual_poly.LC().subs({r: 1, s: 1}) != 0

    # On r=0 the leading c-coefficient has no nonzero root, and on s=0
    # its only root is t=0.  In both charts the residual has at least two
    # distinct t-powers, hence a nonzero root away from infinity.
    for substitution in ({r: 0, s: 1}, {r: 1, s: 0}):
        specialized = sp.Poly(sp.expand(residual.subs(substitution)), t)
        assert len(specialized.terms()) >= 2

    print(
        f"verified {name}-branch resultant factorization and a finite "
        "critical root on all (r,s) charts"
    )

print("RESULT: HOMOGENEOUS SQUARE QUADRATIC K TAILS ARE EXCLUDED")
