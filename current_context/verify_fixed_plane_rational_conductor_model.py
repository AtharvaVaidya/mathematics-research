#!/usr/bin/env python3
"""Verify a rational Darboux model descending across the conductor.

The model passes the full conductor and formal-exactness tests but retains
a nonzero global logarithmic Liouville class.  It isolates the obstruction
that any polynomial solution would still have to remove.
"""

import sympy as sp


v, c = sp.symbols("v c", nonzero=True)
x = v**2
y = v * (v**2 - 9 * c)
t = (v + 2) / (3 * c)


def jac(f, g):
    return sp.factor(
        sp.diff(f, v) * sp.diff(g, c) - sp.diff(f, c) * sp.diff(g, v)
    )


# A rational canonical chart adapted to the conductor.  First
#
#   q=cv, p=-1/(3c),  {q,p}=1/(3c).
#
# The monomial change Q=q^3*p^4, P=-q^-2*p^-3 has unit Jacobian.
q = c * v
p = -1 / (3 * c)
Q = sp.factor(q**3 * p**4)
P = sp.factor(-q**-2 * p**-3)
assert sp.factor(Q - v**3 / (81 * c)) == 0
assert sp.factor(P - 27 * c / x) == 0
assert jac(q, p) == 1 / (3 * c)
assert jac(Q, P) == 1 / (3 * c)

# On the conductor P=3 and Q changes sign.  Squaring Q and dividing the
# vanishing normal coordinate P-3 by Q makes both functions descend.
A = sp.factor(Q**2)
B0 = sp.factor((P - 3) / (2 * Q))
assert sp.factor(A - x**3 / (6561 * c**2)) == 0
assert sp.factor(B0 + 243 * c * y / (2 * x**3)) == 0
assert jac(A, B0) == 1 / (3 * c)

# The canonical shear fixes the Jacobian and supplies exactly the boundary
# residue forced by the polynomial primitive parity equation.
B = sp.factor(B0 - sp.Rational(2, 3) / A)
assert jac(A, B) == 1 / (3 * c)
assert sp.factor(A.subs(c, v**2 / 9) - v**2 / 81) == 0
assert sp.factor(B.subs(c, v**2 / 9) + 54 / v**2) == 0

c_boundary = sp.symbols("c_boundary", nonzero=True)
u = c_boundary / 9
w = -6 / c_boundary
assert sp.residue(
    u * sp.diff(w, c_boundary), c_boundary, 0
) == sp.Rational(2, 3)

# The remaining Liouville class is a global logarithmic residue.  It
# vanishes formally at the conductor because x/c restricts there to 9,
# but it is not the differential of a rational function.
S_rational = -sp.Rational(5, 6) * v + v**3 / (54 * c)
log_argument = x / c
for coordinate in (v, c):
    beta_coefficient = A * sp.diff(B, coordinate)
    if coordinate == c:
        beta_coefficient -= t
    assert sp.factor(
        beta_coefficient
        - sp.diff(S_rational, coordinate)
        - 2 * sp.diff(sp.log(log_argument), coordinate)
    ) == 0

beta_v = sp.factor(A * sp.diff(B, v))
assert sp.residue(beta_v, v, 0) == 4

print("verified a rational Darboux pair descending across the conductor")
print("verified its forced boundary residue and nonzero 2*dlog(x/c) class")
print("RESULT: RATIONALITY IS POSSIBLE; GLOBAL EXACTNESS REMAINS OBSTRUCTED")
