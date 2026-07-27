#!/usr/bin/env python3
"""Exact checks for the reflection-equivariant Keller-map literature audit."""

from __future__ import annotations

import sympy as sp


x, y, s, z, t = sp.symbols("x y s z t")


# ---------------------------------------------------------------------------
# Reflection quotient identity.

P = sp.Function("P")(s, y)
Q = sp.Function("Q")(s, y)

H_odd = x * Q.subs(s, x**2)
H_even = P.subs(s, x**2)
J_H = sp.det(
    sp.Matrix(
        [
            [sp.diff(H_odd, x), sp.diff(H_odd, y)],
            [sp.diff(H_even, x), sp.diff(H_even, y)],
        ]
    )
)

quotient_first = s * Q**2
quotient_second = P
J_quotient = sp.det(
    sp.Matrix(
        [
            [sp.diff(quotient_first, s), sp.diff(quotient_first, y)],
            [sp.diff(quotient_second, s), sp.diff(quotient_second, y)],
        ]
    )
)

assert sp.simplify(J_quotient - Q * J_H.subs(x**2, s)) == 0


# ---------------------------------------------------------------------------
# Linear conjugacy: exchange becomes a coordinate reflection.

# In column-vector convention, (U,V)^T = C (X,Y)^T.
C = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2)], [-1, 1]])
exchange = sp.Matrix([[0, 1], [1, 0]])
reflection = sp.simplify(C * exchange * C.inv())
assert reflection == sp.diag(1, -1)


# ---------------------------------------------------------------------------
# Moskowicz--Valqui normal form and its translation to the parity notation.

c, lam = sp.symbols("c lambda", nonzero=True)
A = sp.Function("A")
F_normal = -c * y / lam + A(x**2)
G_normal = lam * x
J_normal = sp.det(
    sp.Matrix(
        [
            [sp.diff(F_normal, x), sp.diff(F_normal, y)],
            [sp.diff(G_normal, x), sp.diff(G_normal, y)],
        ]
    )
)
assert sp.simplify(J_normal - c) == 0


# ---------------------------------------------------------------------------
# Affine-surface countermodel to automatic etale descent.

# On G_m x A^1, f(z,y)=(z^2,y) is etale because 2z is a unit.
J_cover = sp.det(sp.Matrix([[sp.diff(z**2, z), 0], [0, 1]]))
assert J_cover == 2 * z

# t=z+z^{-1}; the induced quotient coordinate is z^2+z^{-2}=t^2-2.
assert sp.expand((z + z**-1) ** 2 - 2 - (z**2 + z**-2)) == 0
J_descended = sp.det(sp.Matrix([[sp.diff(t**2 - 2, t), 0], [0, 1]]))
assert J_descended == 2 * t
assert J_descended.subs(t, 0) == 0

# The free orbit {i,-i} maps to the fixed point z=-1.
assert sp.I**2 == -1
assert (-sp.I) ** 2 == -1
assert 1 / sp.I == -sp.I


print("verified: reflection quotient Jacobian equals Q times the Keller Jacobian")
print("verified: exchange involution is linearly conjugate to diag(1,-1)")
print("verified: Moskowicz--Valqui normal form has the prescribed Jacobian")
print("verified: etale inversion-equivariant surface map descends to a ramified map")
