#!/usr/bin/env python3
"""Exact checks for NONEQUIVARIANT_NODAL_PULLBACK_STRUCTURE_AND_LOCAL_MODEL.md."""

import sympy as sp


x, y, t = sp.symbols("x y t")
a = x**2 - 1
S = y * (y + 4 * a)

P = sp.expand(x**2 + (3 * x**2 - 2) * S / 8)
Q = sp.expand(
    x * a
    + sp.Rational(1, 2) * x * y
    + sp.Rational(9, 32) * x * (2 * a + y) * S
)
H = lambda u, v: u * (u - 1) ** 2 - v**2


def jacobian(f, g):
    return sp.expand(sp.diff(f, x) * sp.diff(g, y) - sp.diff(f, y) * sp.diff(g, x))


# Boundary and the two normalization branches.
assert sp.expand(P.subs(y, 0) - x**2) == 0
assert sp.expand(Q.subs(y, 0) - (x**3 - x)) == 0
assert sp.expand(P.subs(y, -4 * a) - x**2) == 0
assert sp.expand(Q.subs(y, -4 * a) + (x**3 - x)) == 0

# The Jacobian is exactly one modulo the nodal double-cover divisor.
J = jacobian(P, Q)
W = sp.cancel((J - 1) / S)
assert sp.denom(W) == 1
assert sp.expand(J - (1 + S * W)) == 0
expected_W = -sp.Rational(1, 64) * (
    54 * x**6
    - 108 * x**4 * y
    - 108 * x**4
    - 27 * x**2 * y**2
    + 72 * x**2 * y
    - 18 * x**2
    - 9 * y**2
    + 36 * y
    - 52
)
assert sp.expand(W - expected_W) == 0
assert sp.expand(J.subs(y, 0) - 1) == 0
assert sp.expand(J.subs(y, -4 * a) - 1) == 0
assert W != 0

# The nodal pullback is S times a unit whose restriction to D_0 is -1/4.
U = sp.cancel(H(P, Q) / S)
assert sp.denom(U) == 1
V = sp.cancel((U + sp.Rational(1, 4)) / S)
assert sp.denom(V) == 1
assert sp.expand(H(P, Q) - S * (-sp.Rational(1, 4) + S * V)) == 0
assert sp.expand(U.subs(y, 0) + sp.Rational(1, 4)) == 0
assert sp.expand(U.subs(y, -4 * a) + sp.Rational(1, 4)) == 0

# Universal boundary residual formula:
# H_u(gamma) P_y + H_v(gamma) Q_y = -(x^2-1) J on y=0.
py, qy = sp.symbols("p_y q_y")
boundary_J = 2 * x * qy - (3 * x**2 - 1) * py
boundary_R = (x**2 - 1) * ((3 * x**2 - 1) * py - 2 * x * qy)
assert sp.expand(boundary_R + (x**2 - 1) * boundary_J) == 0

# Algebraic idempotent identities in the universal fiber product.
Afun = sp.Function("A")
Bfun = sp.Function("B")
# The matrix/adjugate part is checked symbolically with independent entries.
A0, B0 = sp.symbols("A0 B0")
delta = t - x
T = t**2 + t * x + x**2 - 1
kappa = B0 * (t + x) - A0 * T
M = sp.Matrix([[A0, -(t + x)], [B0, -T]])
assert sp.expand(M.det() - kappa) == 0
assert (M.adjugate() * M - kappa * sp.eye(2)).applyfunc(sp.expand) == sp.zeros(2)

print("PASS: non-equivariant nodal pullback structure and local-model no-go")
