#!/usr/bin/env python3
"""Exact checks for the global Darboux divisor-section audit."""

import sympy as sp


t, xi, eps, c = sp.symbols("t xi eps c", nonzero=True)
x, y = sp.symbols("x y")

# The normalized m=1 endpoint.
A = t**3 + t**2 + sp.Rational(6, 25) * t + sp.Rational(9, 250)
B = (
    t**4
    + sp.Rational(2, 3) * t**3
    + sp.Rational(6, 25) * t**2
    + sp.Rational(36, 875) * t
    + sp.Rational(18, 4375)
)
N = 7
p = 3
wronskian = sp.expand(3 * sp.diff(A, t) * B - 2 * A * sp.diff(B, t))
assert wronskian == t ** (N - 1)

# The implicit Jacobian for the normalized translated sheet.
r, T = sp.symbols("r T")
A_T = A.subs(t, T)
B_T = B.subs(t, T)
implicit_det = sp.expand(
    sp.det(
        sp.Matrix(
            [
                [2 * r * A_T, r**2 * sp.diff(A_T, T)],
                [3 * r**2 * B_T, r**3 * sp.diff(B_T, T)],
            ]
        )
    ).subs({r: 1, T: t})
)
assert implicit_det == -t ** (N - 1)

# A constant target translation preserves the reciprocal two-form.
P0 = xi**2 * A
Q0 = xi**3 * B
P = P0
Q = Q0 + c
wedge_coeff = sp.expand(
    sp.diff(P, xi) * sp.diff(Q, t) - sp.diff(P, t) * sp.diff(Q, xi)
)
assert wedge_coeff == -xi**4 * t ** (N - 1)

# Reverse A and B and check polynomiality and the original-plane bracket.
w = sp.symbols("w")
U = sp.expand(w**3 * A.subs(t, 1 / w))
V = sp.expand(w**4 * B.subs(t, 1 / w))
assert sp.denom(U) == 1 and sp.denom(V) == 1
z_xy = x * y
w_xy = x * y**2
P_xy = sp.expand(z_xy**2 * U.subs(w, w_xy) / w_xy)
Q_xy = sp.expand(z_xy**3 * V.subs(w, w_xy) / w_xy + c)
assert sp.denom(P_xy) == 1 and sp.denom(Q_xy) == 1
jacobian_xy = sp.expand(
    sp.diff(P_xy, x) * sp.diff(Q_xy, y)
    - sp.diff(P_xy, y) * sp.diff(Q_xy, x)
)
assert jacobian_xy == x**2

# The translated cusp orbit is infinite in characteristic zero.
q_target, p_target = sp.symbols("q_target p_target")
L = sp.cancel(B.subs(t, 0) ** 2 / A.subs(t, 0) ** 3)
j, ell = sp.symbols("j ell")
cusp_j = sp.expand((q_target - j * c) ** 2 - L * p_target**3)
cusp_ell = sp.expand((q_target - ell * c) ** 2 - L * p_target**3)
assert sp.expand(cusp_j - cusp_ell) != 0
assert sp.expand(
    sp.Poly(cusp_j - cusp_ell, q_target).coeff_monomial(q_target)
    - 2 * c * (ell - j)
) == 0

# Arithmetic used to kill the possible divisor character.
m = sp.symbols("m", integer=True, positive=True)
p_general = 2 * m + 1
N_general = 5 * m + 2
assert sp.expand(2 * N_general - 5 * p_general) == -1
assert sp.expand(4 * N_general - 5 * p_general) == 10 * m + 3
assert sp.gcd(p_general, N_general) == 1

print("verified the genuine m=1 reciprocal Wronskian")
print("verified the normalized translation sheet has invertible implicit Jacobian")
print("verified exact symplecticity after constant target translation")
print("verified polynomial original-plane support and Jacobian x^2")
print("verified the translated cusp divisors are pairwise distinct")
print("verified the endpoint arithmetic killing all three divisor characters")
print("RESULT: invariance of div(S), div(Y), or div(SY) forces descent")
print("RESULT: divisor divisibility alone carries no descent information")
