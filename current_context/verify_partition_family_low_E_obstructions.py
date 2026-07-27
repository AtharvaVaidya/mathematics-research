#!/usr/bin/env python3
"""Exact exceptional-range audit for the saturated E-partition family.

Together with ``verify_partition_family_uniform_obstruction.py``, this
excludes every integer E >= 2 for

    g=2(E+1), d=x^(E+2)(x^E+ell),
    p0=d^2+u*x, q0=d^3,

where ell*u is nonzero.
"""

from __future__ import annotations

import sympy as sp


x, ell, u = sp.symbols("x ell u", nonzero=True)
coefficient_field = sp.QQ.frac_field(ell, u)
u_polynomial_field = sp.QQ.frac_field(ell)


def obstruction_closure(e_value: int) -> int:
    g_value = 2 * (e_value + 1)
    d = x ** (g_value - e_value) * (x**e_value + ell)
    d1 = sp.diff(d, x)
    A = u + 2 * d * d1
    B = 3 * d**2 * d1
    inverse_a = sp.invert(A, B, domain=coefficient_field)

    p = [d**2 + u * x, -4 * d1 / (3 * u**2)]
    q = [d**3, 1 / u - 2 * d * d1 / u**2]
    common_factor: sp.Poly | None = None

    for defect in range(2, 6):
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
            domain=coefficient_field,
        )
        p_new = sp.cancel((A * q_new - h) / B)
        assert p_new.is_polynomial(x)

        q_polynomial = sp.Poly(q_new, x)
        forbidden = [
            sp.factor(q_polynomial.coeff_monomial(x**power))
            for power in range(
                3 * g_value - defect + 1,
                3 * g_value - 1,
            )
        ]
        for value in forbidden:
            if value == 0:
                continue
            numerator = sp.cancel(value).as_numer_denom()[0]
            polynomial = sp.Poly(
                numerator,
                u,
                domain=u_polynomial_field,
            )
            common_factor = (
                polynomial
                if common_factor is None
                else sp.gcd(common_factor, polynomial)
            )
        if common_factor is not None:
            common_factor = sp.monic(common_factor)
            if common_factor.degree() == 0:
                return defect

        p.append(sp.factor(p_new))
        q.append(sp.factor(q_new))

    raise AssertionError(("survived exceptional audit", e_value, common_factor))


expected_closure = {
    2: 3,
    3: 5,
    4: 4,
    5: 3,
    6: 5,
    7: 4,
    8: 4,
    9: 5,
}

for e_value, expected in expected_closure.items():
    actual = obstruction_closure(e_value)
    assert actual == expected, (e_value, actual, expected)
    print(f"verified: E={e_value} is excluded by defect {actual}")
