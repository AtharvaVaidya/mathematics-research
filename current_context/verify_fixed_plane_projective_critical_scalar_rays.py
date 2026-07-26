#!/usr/bin/env python3
"""Verify the projective critical-incidence audit on two scalar rays."""

from __future__ import annotations

import runpy
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
data = runpy.run_path(
    str(HERE / "verify_fixed_plane_sheet_loss_first_order_crt.py")
)

t, c = data["t"], data["c"]
D, K = data["D"], data["K"]
E = sp.expand(D * K)
U0 = data["U0"]
lam = sp.symbols("lam")


def leading_form(poly: sp.Expr) -> sp.Expr:
    """Return the top total-degree homogeneous part."""

    p = sp.Poly(poly, t, c)
    degree = p.total_degree()
    return sp.expand(
        sum(
            coefficient * t ** monomial[0] * c ** monomial[1]
            for monomial, coefficient in p.terms()
            if sum(monomial) == degree
        )
    )


assert sp.factor(leading_form(E) - 81 * c**4 * t**4) == 0
assert sp.factor(
    leading_form(U0) + sp.Rational(81, 2) * c**5 * t**6
) == 0
assert sp.factor(
    leading_form(E**2) - 6561 * c**8 * t**8
) == 0
assert sp.factor(
    leading_form(t * E**2) - 6561 * c**8 * t**9
) == 0

# The common support of the two leading partials is exactly the two
# coordinate points on the line at infinity for both scalar rays.
H_one = 6561 * c**8 * t**8
H_t = 6561 * c**8 * t**9
assert sp.factor(
    sp.gcd(sp.diff(H_one, t), sp.diff(H_one, c))
) == 52488 * c**7 * t**7
assert sp.factor(
    sp.gcd(sp.diff(H_t, t), sp.diff(H_t, c))
) == 6561 * c**7 * t**8


def moving_resultant_factor(phi: sp.Expr, lam_power: int, c_power: int):
    """Extract the unique moving factor from the exact t-resultant."""

    U = sp.expand(U0 + lam * E**2 * phi)
    U_t = sp.diff(U, t)
    U_c = sp.diff(U, c)
    resultant = sp.resultant(U_t, U_c, t)
    _, factors = sp.factor_list(resultant)

    found_lam = False
    found_c = False
    moving = []
    for factor, exponent in factors:
        if sp.expand(factor - lam) == 0:
            assert exponent == lam_power
            found_lam = True
        elif sp.expand(factor - c) == 0:
            assert exponent == c_power
            found_c = True
        else:
            moving.append((factor, exponent))

    assert found_lam and found_c
    assert len(moving) == 1
    moving_factor, moving_exponent = moving[0]
    assert moving_exponent == 1
    return U, U_t, U_c, sp.Poly(moving_factor, c)


# The old eliminant is used to identify the fourteen persistent
# branches in the lambda=0 specialization.
G0 = sp.groebner(
    [sp.diff(U0, t), sp.diff(U0, c)], t, c, order="lex"
)
old_eliminant = sp.Poly(G0.polys[-1].as_expr(), c).monic()
assert old_eliminant.degree() == 14
assert sp.gcd(old_eliminant, old_eliminant.diff()).degree() == 0


# Scalar E^2 ray.
U_one, F_one, G_one, P_one = moving_resultant_factor(
    sp.Integer(1), 2, 52
)
assert P_one.degree() == 21
assert sp.degree(P_one.as_expr(), lam) == 9
assert sp.Poly(P_one.as_expr().subs(lam, 0), c).monic() == old_eliminant

q = 104976 * lam**2 + 5751 * lam + 2
lc_one_quotient = sp.cancel(P_one.LC() / (lam**3 * q**2))
assert lc_one_quotient.is_Rational and lc_one_quotient != 0
assert sp.degree(P_one.nth(0), lam) == 0
assert P_one.nth(0) != 0

# At either root of q, c^21 vanishes but c^20 does not.
assert sp.gcd(
    sp.Poly(q, lam), sp.Poly(P_one.nth(20), lam)
).degree() == 0
assert sp.factor(sp.discriminant(q, lam) - 32234193) == 0

F_one_t = sp.Poly(F_one, t)
G_one_t = sp.Poly(G_one, t)
assert F_one_t.degree() == 7
assert G_one_t.degree() == 8
assert sp.factor(F_one_t.LC() - 52488 * c**8 * lam) == 0
assert sp.factor(G_one_t.LC() - 52488 * c**7 * lam) == 0
assert sp.factor(F_one.subs(c, 0) - sp.Rational(8, 3)) == 0


# Scalar t E^2 ray.
U_t_ray, F_t_ray, G_t_ray, P_t_ray = moving_resultant_factor(
    t, 3, 64
)
assert P_t_ray.degree() == 21
assert sp.degree(P_t_ray.as_expr(), lam) == 10
assert sp.Poly(P_t_ray.as_expr().subs(lam, 0), c).monic() == old_eliminant

lc_t_quotient = sp.cancel(P_t_ray.LC() / lam**4)
assert lc_t_quotient.is_Rational and lc_t_quotient != 0
endpoint_t = (8 * lam - 9) * (24 * lam + 1) ** 2 * (
    972 * lam + 1
)
constant_t_quotient = sp.cancel(P_t_ray.nth(0) / endpoint_t)
assert constant_t_quotient.is_Rational and constant_t_quotient != 0

F_t_as_t = sp.Poly(F_t_ray, t)
G_t_as_t = sp.Poly(G_t_ray, t)
assert F_t_as_t.degree() == 8
assert G_t_as_t.degree() == 9
assert sp.factor(F_t_as_t.LC() - 59049 * c**8 * lam) == 0
assert sp.factor(G_t_as_t.LC() - 52488 * c**7 * lam) == 0

assert sp.factor(
    F_t_ray.subs(c, 0) - sp.Rational(8, 3) * (24 * lam + 1)
) == 0
assert sp.factor(
    G_t_ray.subs(c, 0)
    + 6
    * (
        160 * lam * t**2
        + 144 * lam * t
        + 4 * t**2
        + 9 * t
        + 3
    )
) == 0


def c_order_at(parameter: sp.Rational) -> int:
    specialized = sp.Poly(P_t_ray.as_expr().subs(lam, parameter), c)
    return next(
        exponent
        for exponent in range(specialized.degree() + 1)
        if specialized.nth(exponent) != 0
    )


assert c_order_at(sp.Rational(9, 8)) == 2
assert c_order_at(-sp.Rational(1, 24)) == 2
assert c_order_at(-sp.Rational(1, 972)) == 1

# The c=0 endpoint is projective at 9/8 and -1/972.
assert F_t_ray.subs({c: 0, lam: sp.Rational(9, 8)}) != 0
assert F_t_ray.subs({c: 0, lam: -sp.Rational(1, 972)}) != 0

# At -1/24 it instead consists of two simple affine critical points.
special_parameter = -sp.Rational(1, 24)
special_U = sp.expand(U_t_ray.subs(lam, special_parameter))
special_c_equation = sp.factor(sp.diff(special_U, c).subs(c, 0))
assert sp.expand(
    special_c_equation - 2 * (8 * t**2 - 9 * t - 9)
) == 0
assert sp.discriminant(special_c_equation, t) != 0
special_hessian = sp.factor(
    sp.det(sp.hessian(special_U, (t, c))).subs(c, 0)
)
assert special_hessian == -4 * (16 * t - 9) ** 2
assert sp.resultant(
    special_c_equation, special_hessian, t
) != 0
for critical_t in (
    (9 + 3 * sp.sqrt(41)) / 16,
    (9 - 3 * sp.sqrt(41)) / 16,
):
    assert sp.simplify(special_c_equation.subs(t, critical_t)) == 0
    assert sp.simplify(special_hessian.subs(t, critical_t)) == -1476

# Bezout ledgers for the two nonzero scalar rays.
assert 15**2 == 21 + 204
assert 15**2 == 20 + 205
assert 16**2 == 21 + 235
assert 16**2 == 19 + 237
assert 16**2 == 20 + 236


print("verified the general leading-form support criterion at infinity")
print("verified the exact E^2-ray resultant and its two escape values")
print("verified the exact t*E^2-ray resultant and all three endpoints")
print("verified two finite simple c=0 points at lambda=-1/24")
print("every polynomial on either scalar ray has an affine critical point")
print("leading homogeneous data alone do not prevent escape to infinity")
