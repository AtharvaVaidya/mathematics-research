#!/usr/bin/env python3
"""Exact checks for the two-boundary divisor-orbit audit."""

import sympy as sp


t, xi = sp.symbols("t xi", nonzero=True)
x, y = sp.symbols("x y")
a, c, d = sp.symbols("a c d", nonzero=True)

# The exact m=1 genuine reciprocal endpoint.
A = t**3 + t**2 + sp.Rational(6, 25) * t + sp.Rational(9, 250)
B = (
    t**4
    + sp.Rational(2, 3) * t**3
    + sp.Rational(6, 25) * t**2
    + sp.Rational(36, 875) * t
    + sp.Rational(18, 4375)
)
N = 7
assert sp.expand(3 * sp.diff(A, t) * B - 2 * A * sp.diff(B, t)) == t ** (N - 1)

# The affine target map has determinant one and preserves the exact form.
P0 = xi**2 * A
Q0 = xi**3 * B
P = P0 + a
Q = Q0 + c * P0 + d
wedge = sp.expand(
    sp.diff(P, xi) * sp.diff(Q, t) - sp.diff(P, t) * sp.diff(Q, xi)
)
assert wedge == -xi**4 * t ** (N - 1)

# The high-contact quotient has exact order N at t=0.
R = sp.cancel(B**2 / A**3)
assert sp.cancel(sp.diff(R, t) + t ** (N - 1) * B / A**4) == 0
A0 = A.subs(t, 0)
B0 = B.subs(t, 0)
kappa = -B0 / (N * A0**4)
series_R = sp.series(R, t, 0, N + 1).removeO()
assert sp.expand(series_R - R.subs(t, 0) - kappa * t**N) == 0

# Blow up the degenerate corner with epsilon=delta*t^N and T=t*u.
u, delta = sp.symbols("u delta")
left_divided = sp.cancel((R.subs(t, t * u) - R) / t**N)
left_at_corner = sp.factor(sp.limit(left_divided, t, 0))
assert sp.expand(left_at_corner - kappa * (u**N - 1)) == 0

eps = delta * t**N
right = sp.cancel(
    (B + c * eps * A + d * eps**3) ** 2 / (A + a * eps**2) ** 3
)
right_divided = sp.cancel((right - R) / t**N)
right_at_corner = sp.factor(sp.limit(right_divided, t, 0))
assert sp.expand(right_at_corner - 2 * c * B0 * delta / A0**2) == 0
assert sp.diff(kappa * (u**N - 1), u).subs(u, 1) != 0

# Every consecutive pair of sufficiently deep reciprocal rays, and its
# original-plane transform, is adjacent.
m = sp.symbols("m", integer=True, positive=True)
ell = sp.symbols("ell", integer=True, positive=True)
p_general = 2 * m + 1
N_general = 5 * m + 2
rho1 = N_general + ell
rho2 = N_general + ell + 1
assert sp.det(sp.Matrix([[rho1, 1], [rho2, 1]])) == -1
assert sp.expand(rho1 - N_general) == ell
assert sp.expand(rho2 - N_general) == ell + 1

v1 = (sp.expand(p_general - 2 * rho1), sp.expand(rho1 - m - 1))
v2 = (sp.expand(p_general - 2 * rho2), sp.expand(rho2 - m - 1))
assert v1 == (-8 * m - 3 - 2 * ell, 4 * m + 1 + ell)
assert v2 == (-8 * m - 5 - 2 * ell, 4 * m + 2 + ell)
assert sp.det(sp.Matrix([v1, v2])) == -1

# Reverse the endpoint and verify original-plane polynomiality and bracket.
w = sp.symbols("w")
U = sp.expand(w**3 * A.subs(t, 1 / w))
V = sp.expand(w**4 * B.subs(t, 1 / w))
z_xy = x * y
w_xy = x * y**2
P0_xy = sp.expand(z_xy**2 * U.subs(w, w_xy) / w_xy)
Q0_xy = sp.expand(z_xy**3 * V.subs(w, w_xy) / w_xy)
P_xy = sp.expand(P0_xy + a)
Q_xy = sp.expand(Q0_xy + c * P0_xy + d)
assert sp.denom(P_xy) == 1 and sp.denom(Q_xy) == 1
assert sp.expand(
    sp.diff(P_xy, x) * sp.diff(Q_xy, y)
    - sp.diff(P_xy, y) * sp.diff(Q_xy, x)
) == x**2

# The affine target orbit of the cusp singular point is infinite when a != 0.
j = sp.symbols("j", integer=True)
p_j = j * a
q_j = j * d + c * a * j * (j - 1) / 2
assert sp.expand(p_j.subs(j, j + 1) - (p_j + a)) == 0
assert sp.expand(q_j.subs(j, j + 1) - (q_j + c * p_j + d)) == 0

print("verified the genuine reciprocal Wronskian and affine symplectic deformation")
print("verified the exact corner equation after epsilon=delta*t^N")
print("verified normalized identity at two adjacent reciprocal boundary rays")
print("verified the two rays remain adjacent in the original (x,y)-plane")
print("verified polynomial original-plane support and Jacobian x^2")
print("verified the infinite affine orbit formula for the cusp singular point")
print("RESULT: two adjacent boundary orders do not force invariance of div(J)")
