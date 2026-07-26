#!/usr/bin/env python3
"""Verify the all-order Hensel mechanism and its second-order instance.

This imports and reruns the exact first-order verifier, constructs the
inverse of ``Jac(U, D*K)`` modulo ``D*K``, and checks the explicit
second-order polynomial.  It does not claim that the compatible formal
series terminates or algebraizes to a polynomial Keller pair.
"""

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
U, V0 = data["U0"], data["V0"]
beta = data["beta"]
bracket = data["bracket"]


# The exact first-order polynomial and its residual Jacobian coefficient.
V1 = sp.expand(V0 + E * beta)
J1 = bracket(U, V1)
q1 = sp.cancel((J1 - 1) / E)
assert sp.denom(q1) == 1
q1 = sp.expand(q1)


# A polynomial inverse of delta={U,E} modulo E, assembled componentwise.
iota_C = data["iota_C"]
iota_H = data["iota_H"]
eta_H = data["inverse_v_plus_1_on_H"]
e_C = data["e_C"]
e_H = data["e_H"]

inverse_delta_C = sp.expand(-sp.Rational(27, 4) * iota_C**6)
inverse_delta_H = sp.expand(
    sp.Rational(1, 6) * iota_H**3 * eta_H
)
a = sp.expand(e_C * inverse_delta_C + e_H * inverse_delta_H)
delta = bracket(U, E)

assert sp.factor(delta.subs(data["sub_C"])) == (
    -sp.Rational(4, 27) * data["vpar"] ** 6
)
assert sp.factor(delta.subs(data["sub_H"])) == (
    6 * data["vpar"] ** 3 * (data["vpar"] + 1)
)

inverse_error_quotient = sp.cancel((a * delta - 1) / E)
assert sp.denom(inverse_error_quotient) == 1


# The m=1 Hensel step: V2=V1+E^2*gamma with gamma=-a*q1/2.
gamma = sp.expand(-a * q1 / 2)
V2 = sp.expand(V1 + E**2 * gamma)
J2 = bracket(U, V2)
q2 = sp.cancel((J2 - 1) / E**2)
assert sp.denom(q2) == 1

# Check the displayed recurrence certificate before simplification.
certificate_rhs = sp.expand(
    E * q1 * (1 - a * delta)
    - E**2 * bracket(U, a * q1) / 2
)
assert sp.expand(J2 - 1 - certificate_rhs) == 0


# These exact size checks guard against accidentally verifying a
# truncated or otherwise different polynomial.
expected_sizes = {
    "q1": (55, 266),
    "a": (25, 53),
    "gamma": (80, 521),
    "V2": (96, 749),
}
for name, polynomial in {
    "q1": q1,
    "a": a,
    "gamma": gamma,
    "V2": V2,
}.items():
    poly = sp.Poly(polynomial, t, c)
    assert (poly.total_degree(), len(poly.terms())) == expected_sizes[name]


# Abstract algebra behind every later step.  Here d(aq) is a placeholder
# for the derivation {U,aq}; the identity is the Leibniz expansion used
# in the memo.
m = sp.symbols("m", integer=True, positive=True)
e, q, a0, dlt, d_aq = sp.symbols("e q a0 dlt d_aq")
correction_bracket = (
    -(m + 1) * e**m * a0 * q * dlt / (m + 1)
    - e ** (m + 1) * d_aq / (m + 1)
)
recurrence_rhs = (
    e**m * q * (1 - a0 * dlt)
    - e ** (m + 1) * d_aq / (m + 1)
)
assert sp.simplify(e**m * q + correction_bracket - recurrence_rhs) == 0


# The particular polynomial U has a global critical locus away from E.
# Hence its formal Keller lift cannot algebraize to a global polynomial
# second coordinate.
U_t = sp.diff(U, t)
U_c = sp.diff(U, c)
critical_basis = sp.groebner([U_t, U_c], t, c, order="lex")
assert not critical_basis.contains(sp.Integer(1))
assert len(critical_basis.polys) == 2

critical_t_row = sp.Poly(critical_basis.polys[0].as_expr(), t, c)
critical_c_row = sp.Poly(critical_basis.polys[1].as_expr(), t, c)
assert critical_basis.polys[0].LM(order=critical_basis.order).exponents == (
    1,
    0,
)
assert critical_basis.polys[1].LM(order=critical_basis.order).exponents == (
    0,
    14,
)
assert critical_t_row.degree(t) == 1
assert critical_t_row.coeff_monomial(t) == 1
assert sp.diff(critical_t_row.as_expr(), t) == 1
assert critical_c_row.degree(t) == 0
assert critical_c_row.degree(c) == 14

critical_eliminant = sp.Poly(
    sp.expand(129600 * critical_c_row.as_expr()), c
)
expected_eliminant = sp.Poly(
    129600 * c**14
    - 16086645 * c**13
    + 762804802 * c**12
    - 17935387965 * c**11
    + 234413004346 * c**10
    - 1767283629696 * c**9
    + 7546547140810 * c**8
    - 17058892809204 * c**7
    + 19276910317992 * c**6
    - 11149073947836 * c**5
    + 2118379838400 * c**4
    - 155004753276 * c**3
    + 3161279664 * c**2
    + 95831424 * c
    - 3359232,
    c,
)
assert critical_eliminant == expected_eliminant
assert sp.gcd(critical_eliminant, critical_eliminant.diff()).degree() == 0

# The critical scheme is disjoint from the formal divisor.
assert sp.groebner(
    [U_t, U_c, E], t, c, order="grevlex"
).contains(sp.Integer(1))


print("verified that Jac(U,D*K) is a unit modulo D*K")
print("verified the exact polynomial second-order Hensel correction")
print("verified Jac(U,V2)=1 modulo D^2*K^2")
print("verified the compatible all-order recurrence identity")
print("verified 14 distinct critical points of U, all away from D*K=0")
print("there is no global polynomial V with Jac(U,V)=1")
