#!/usr/bin/env python3
"""Verify the exact formal Darboux solution at the fixed-plane conductor.

This check shows that the completed pinch ring itself has no symplectic,
parity, or residue obstruction.  The formal logarithm is expanded only to
identify ring membership; all differential identities are checked exactly
using its closed form.
"""

import sympy as sp


v, s = sp.symbols("v s", nonzero=True)

# Here s=x-9c=v^2-9c is the conductor equation.  In the normalization
# completed along s=0, both v and c are units.
x = v**2
c = (v**2 - s) / 9
t = 3 * (v + 2) / (v**2 - s)

# p has zero constant term and therefore denotes an honest s-adic series:
#
#   p = -(1/3) sum_{n>=1} s^n/(n*v^(2n)).
p = sp.log(1 - s / v**2) / 3
U = x
V = p / (2 * v) - sp.Rational(2, 3) / x


def jac(f, g):
    return sp.factor(
        sp.diff(f, v) * sp.diff(g, s) - sp.diff(f, s) * sp.diff(g, v)
    )


# The (t,c) area form in (v,s) coordinates and the formal pair agree.
assert sp.simplify(jac(U, V) + 1 / (3 * (v**2 - s))) == 0
assert sp.simplify(jac(t, c) + 1 / (3 * (v**2 - s))) == 0

# The Liouville difference is not merely closed: it has an explicit formal
# primitive.  Its boundary value gives exactly the forced odd part (8d).
S = -(v + 4) * p / 2 - sp.Rational(2, 3) * v
assert sp.simplify(
    U * sp.diff(V, v) - t * sp.diff(c, v) - sp.diff(S, v)
) == 0
assert sp.simplify(
    U * sp.diff(V, s) - t * sp.diff(c, s) - sp.diff(S, s)
) == 0
assert sp.simplify(S.subs(s, 0) - S.subs({s: 0, v: -v}) + 4 * v / 3) == 0

# The logarithmic expression belongs to the completed target ring.  With
# y=v*s its series is
#
#   V=-2/(3x)-sum_{n>=1} y*s^(n-1)/(6*n*x^(n+1)).
#
# Check the first several coefficients directly.
y = v * s
series_closed = sp.series(V, s, 0, 8).removeO()
series_target = -sp.Rational(2, 3) / x - sum(
    y * s ** (n - 1) / (6 * n * x ** (n + 1)) for n in range(1, 8)
)
assert sp.simplify(series_closed - series_target) == 0

# Its conductor restrictions satisfy both the residue constraint and the
# two first-jet equations (8b)--(8c).
c_boundary = sp.symbols("c_boundary", nonzero=True)
u = 9 * c_boundary
w = -sp.Rational(2, 27) / c_boundary
assert sp.residue(
    u * sp.diff(w, c_boundary), c_boundary, 0
) == sp.Rational(2, 3)

Fx = sp.Integer(1)
Fc = sp.Integer(0)
Px = sp.Rational(2, 3) / (9 * c_boundary) ** 2
Pc = sp.Integer(0)
G = sp.Integer(0)
Q = -sp.Rational(1, 6) / (9 * c_boundary) ** 2
assert sp.simplify(Fx * Pc - Fc * Px) == 0
assert sp.simplify(
    G * (Pc + 9 * Px)
    - Q * (Fc + 9 * Fx)
    - 1 / (54 * c_boundary**2)
) == 0

# The conductor involution extends formally and fixes U,V.  It reverses
# both v and the normal coordinate to first order, as symplecticity demands.
v_iota = -v
s_iota = -s * v**2 / (v**2 - s)
p_iota = sp.log(1 - s_iota / v_iota**2) / 3
U_iota = v_iota**2
V_iota = p_iota / (2 * v_iota) - sp.Rational(2, 3) / v_iota**2
assert sp.simplify(U_iota - U) == 0
assert sp.simplify(sp.diff(s_iota, s).subs(s, 0) + 1) == 0

# SymPy does not automatically normalize opposite formal logarithms, so
# verify the identity at the rational-argument level and then use p_iota=-p.
assert sp.simplify(
    (1 - s_iota / v_iota**2) * (1 - s / v**2) - 1
) == 0
assert sp.simplify((-p) / (2 * v_iota) - sp.Rational(2, 3) / v_iota**2 - V) == 0

# Applying the involution twice returns the original normal coordinate.
s_iota_twice = sp.factor(
    -s_iota * v_iota**2 / (v_iota**2 - s_iota)
)
assert sp.simplify(s_iota_twice - s) == 0

print("verified the exact formal Darboux pair in the completed pinch ring")
print("verified its exact primitive, residue, boundary jets, and deck involution")
print("RESULT: THE CONDUCTOR-FORMAL PROBLEM IS UNOBSTRUCTED")
