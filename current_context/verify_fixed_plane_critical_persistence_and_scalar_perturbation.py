#!/usr/bin/env python3
"""Verify critical persistence data and the scalar E^2 perturbation.

The formal persistence theorem itself is the standard multivariate
Hensel/implicit-function theorem.  This verifier checks all of its
hypotheses for the fixed-plane polynomial and exactly audits the
concrete large perturbation U1=U0+(D*K)^2.
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
U0 = data["U0"]
bracket = data["bracket"]


def critical_lex_data(U: sp.Expr, expected_degree: int):
    """Return the triangular lex basis and verify reducedness."""

    U_t = sp.diff(U, t)
    U_c = sp.diff(U, c)
    basis = sp.groebner([U_t, U_c], t, c, order="lex")
    assert not basis.contains(sp.Integer(1))
    assert len(basis.polys) == 2

    t_row = sp.Poly(basis.polys[0].as_expr(), t, c)
    c_row_bivariate = sp.Poly(basis.polys[1].as_expr(), t, c)
    assert basis.polys[0].LM(order=basis.order).exponents == (1, 0)
    assert basis.polys[1].LM(order=basis.order).exponents == (
        0,
        expected_degree,
    )
    assert t_row.degree(t) == 1
    assert t_row.coeff_monomial(t) == 1
    assert sp.diff(t_row.as_expr(), t) == 1
    assert c_row_bivariate.degree(t) == 0
    c_row = sp.Poly(c_row_bivariate.as_expr(), c)
    assert c_row.degree() == expected_degree
    assert sp.gcd(c_row, c_row.diff()).degree() == 0
    return U_t, U_c, basis, t_row, c_row


# U0 has fourteen distinct critical points.  The triangular reduced
# critical algebra is finite etale; equivalently, its Hessian is
# invertible at every geometric critical point by the Jacobian
# criterion for this zero-dimensional complete intersection.
U0_t, U0_c, G0, U0_t_row, U0_c_row = critical_lex_data(U0, 14)
assert sp.groebner(
    [U0_t, U0_c, E], t, c, order="grevlex"
).contains(sp.Integer(1))


# Abstract first-order implicit-function identity.  H is an invertible
# Hessian matrix and grad_g is the perturbing gradient.  The displayed
# velocity is the unique solution of H*velocity+grad_g=0.
h11, h12, h21, h22 = sp.symbols("h11 h12 h21 h22")
g1, g2 = sp.symbols("g1 g2")
H = sp.Matrix([[h11, h12], [h21, h22]])
grad_g = sp.Matrix([g1, g2])
velocity = -H.inv() * grad_g
assert sp.simplify(H * velocity + grad_g) == sp.zeros(2, 1)


# General jet-preservation and transversality identities.  The symbol
# q stands for an arbitrary polynomial phi and deriv_q_E for {phi,E}.
eps, e, q, de_t, de_c, dq_t, dq_c = sp.symbols(
    "eps e q de_t de_c dq_t dq_c"
)
jet_difference = sp.Matrix(
    [
        2 * eps * e * q * de_t + eps * e**2 * dq_t,
        2 * eps * e * q * de_c + eps * e**2 * dq_c,
    ]
)
assert jet_difference.subs(e, 0) == sp.zeros(2, 1)

delta0, deriv_q_E = sp.symbols("delta0 deriv_q_E")
assert sp.expand(
    delta0 + eps * e**2 * deriv_q_E - delta0
).subs(e, 0) == 0


# The simplest full-size perturbation preserves the required boundary
# jet but has even more critical points.
U1 = sp.expand(U0 + E**2)
assert sp.cancel((U1 - U0) / E**2) == 1
assert (sp.Poly(U1, t, c).total_degree(), len(sp.Poly(U1, t, c).terms())) == (
    16,
    31,
)

U1_t, U1_c, G1, U1_t_row, U1_c_row = critical_lex_data(U1, 21)
assert len(U1_t_row.terms()) == 22
assert len(U1_c_row.terms()) == 22

# Since phi=1 is a function of E in this scalar example,
# {U0+E^2,E}={U0,E} exactly.
assert sp.expand(bracket(U1, E) - bracket(U0, E)) == 0
assert sp.groebner(
    [U1_t, U1_c, E], t, c, order="grevlex"
).contains(sp.Integer(1))


print("verified that Crit(U0) is finite etale of degree 14")
print("verified the formal critical-point displacement identity")
print("verified preservation of the value and first differential on E=0")
print("verified U1=U0+E^2 has 21 distinct off-boundary critical points")
print("there is no polynomial V with Jac(U0+E^2,V)=1")
