#!/usr/bin/env python3
"""Exact checks for NONEQUIVARIANT_NORMAL_DEGREE_FOUR_EXCLUSION.md."""

from __future__ import annotations

import sympy as sp


x, y, z, w = sp.symbols("x y z w")


# ---------------------------------------------------------------------------
# General leading-degree reductions.

u4 = sp.Function("u4")(x)
v4 = sp.Function("v4")(x)
v3 = sp.Function("v3")(x)
v2 = sp.Function("v2")(x)
v1 = sp.Function("v1")(x)

assert sp.expand(
    4 * sp.diff(u4, x) * v4 - 4 * u4 * sp.diff(v4, x)
) == 4 * (sp.diff(u4, x) * v4 - u4 * sp.diff(v4, x))

c = sp.symbols("c", nonzero=True)
assert sp.simplify(
    2 * sp.diff(c * v2**2, x) * v2
    - 4 * c * v2**2 * sp.diff(v2, x)
) == 0
assert sp.simplify(
    sp.diff(c * v1**4, x) * v1
    - 4 * c * v1**4 * sp.diff(v1, x)
) == 0
assert sp.simplify(
    3 * sp.diff(c * v3**4, x) * v3**3
    - 4 * c * v3**4 * sp.diff(v3**3, x)
) == 0

# Symbolic target shears really remove the top normal term.
aa0, aa1, aa2, aa3 = sp.symbols("aa0:4")
bb0, bb1 = sp.symbols("bb0:2")
U41 = c * bb1**4 * y**4 + aa3 * y**3 + aa2 * y**2 + aa1 * y + aa0
V1 = bb1 * y + bb0
assert sp.Poly(sp.expand(U41 - c * V1**4), y).degree() <= 3

cc0, cc1, cc2 = sp.symbols("cc0:3")
U42 = c * cc2**2 * y**4 + aa3 * y**3 + aa2 * y**2 + aa1 * y + aa0
V2 = cc2 * y**2 + cc1 * y + cc0
assert sp.Poly(sp.expand(U42 - c * V2**2), y).degree() <= 3


# ---------------------------------------------------------------------------
# General monic (4,3) pair and the exact depression.

A0 = sp.Function("A0")(x)
B0 = sp.Function("B0")(x)
C0 = sp.Function("C0")(x)
P0 = sp.Function("P0")(x)
D0 = sp.Function("D0")(x)
E0 = sp.Function("E0")(x)
Q0 = sp.Function("Q0")(x)

F_general = z**4 + A0 * z**3 + B0 * z**2 + C0 * z + P0
G_general = z**3 + D0 * z**2 + E0 * z + Q0
J_general = sp.Poly(
    sp.expand(
        sp.diff(F_general, x) * sp.diff(G_general, z)
        - sp.diff(F_general, z) * sp.diff(G_general, x)
    ),
    z,
)
assert sp.simplify(
    J_general.coeff_monomial(z**5)
    - (3 * sp.diff(A0, x) - 4 * sp.diff(D0, x))
) == 0

t = sp.Function("t")(x)
a_const = sp.symbols("a_const")
B = sp.Function("B")(x)
C = sp.Function("C")(x)
P = sp.Function("P")(x)
E = sp.Function("E")(x)
Q = sp.Function("Q")(x)

f_depressed = w**4 + B * w**2 + C * w + P
g_depressed = w**3 + E * w + Q

# Inverse reconstruction: w=z+t, F=f+a*g, G=g.
F_reconstructed = sp.expand(f_depressed.subs(w, z + t) + a_const * g_depressed.subs(w, z + t))
G_reconstructed = sp.expand(g_depressed.subs(w, z + t))
assert sp.Poly(F_reconstructed, z).coeff_monomial(z**3) == 4 * t + a_const
assert sp.Poly(G_reconstructed, z).coeff_monomial(z**2) == 3 * t

J_reconstructed = sp.expand(
    sp.diff(F_reconstructed, x) * sp.diff(G_reconstructed, z)
    - sp.diff(F_reconstructed, z) * sp.diff(G_reconstructed, x)
)
J_depressed = sp.expand(
    sp.diff(f_depressed, x) * sp.diff(g_depressed, w)
    - sp.diff(f_depressed, w) * sp.diff(g_depressed, x)
)
assert sp.simplify(J_reconstructed - J_depressed.subs(w, z + t)) == 0

# Exact return to polynomial \((x,y)\)-coefficients.
h = sp.Function("h")(x)
DD = sp.Function("DD")(x)
G_xy = sp.expand(g_depressed.subs(w, h * y + DD / 3))
Fcore_xy = sp.expand(f_depressed.subs(w, h * y + DD / 3))
G_xy_poly = sp.Poly(G_xy, y)
Fcore_xy_poly = sp.Poly(Fcore_xy, y)
expected_G_xy = {
    3: h**3,
    2: h**2 * DD,
    1: h * (DD**2 / 3 + E),
    0: DD**3 / 27 + E * DD / 3 + Q,
}
expected_Fcore_xy = {
    4: h**4,
    3: 4 * h**3 * DD / 3,
    2: h**2 * (2 * DD**2 / 3 + B),
    1: h * (4 * DD**3 / 27 + 2 * B * DD / 3 + C),
    0: DD**4 / 81 + B * DD**2 / 9 + C * DD / 3 + P,
}
for degree, coefficient in expected_G_xy.items():
    assert sp.simplify(G_xy_poly.coeff_monomial(y**degree) - coefficient) == 0
for degree, coefficient in expected_Fcore_xy.items():
    assert sp.simplify(
        Fcore_xy_poly.coeff_monomial(y**degree) - coefficient
    ) == 0


# ---------------------------------------------------------------------------
# Depressed coefficient system and all first integrals.

Jd = sp.Poly(J_depressed, w)
expected = {
    4: 3 * sp.diff(B, x) - 4 * sp.diff(E, x),
    3: 3 * sp.diff(C, x) - 4 * sp.diff(Q, x),
    2: -2 * B * sp.diff(E, x) + E * sp.diff(B, x) + 3 * sp.diff(P, x),
    1: -2 * B * sp.diff(Q, x) - C * sp.diff(E, x) + E * sp.diff(C, x),
    0: -C * sp.diff(Q, x) + E * sp.diff(P, x),
}
for degree, coefficient in expected.items():
    assert sp.simplify(Jd.coeff_monomial(w**degree) - coefficient) == 0

k, ell, M, N, Delta = sp.symbols("k ell M N Delta")
B_int = (4 * E + k) / 3
C_int = (4 * Q + ell) / 3
P_int = 2 * E**2 / 9 + 2 * k * E / 9 + M

assert sp.simplify(expected[4].subs(B, B_int)) == 0
assert sp.simplify(expected[3].subs(C, C_int)) == 0
assert sp.simplify(
    expected[2].subs({B: B_int, P: P_int}).doit()
) == 0
assert sp.simplify(
    expected[1].subs({B: B_int, C: C_int}).doit()
    + sp.diff(4 * E * Q + 2 * k * Q + ell * E, x) / 3
) == 0

r = sp.Function("r")(x)
Delta_def = ell * k + 2 * N
E_r = (r - k) / 2
Q_r = -ell / 4 + Delta_def / (4 * r)
B_r = (2 * r - k) / 3
C_r = Delta_def / (3 * r)
P_r = (r**2 - k**2) / 18 + M

assert sp.simplify(4 * E_r * Q_r + 2 * k * Q_r + ell * E_r - N) == 0
assert sp.simplify(B_int.subs(E, E_r) - B_r) == 0
assert sp.simplify(C_int.subs(Q, Q_r) - C_r) == 0
assert sp.simplify(P_int.subs(E, E_r) - P_r) == 0

generic_constant = sp.simplify(
    (-C * sp.diff(Q, x) + E * sp.diff(P, x)).subs(
        {C: C_r, Q: Q_r, E: E_r, P: P_r}
    ).doit()
)
H_r = r**3 / 54 - k * r**2 / 36 - Delta_def**2 / (24 * r**2)
assert sp.simplify(generic_constant - sp.diff(H_r, x)) == 0
assert sp.simplify(
    generic_constant
    - sp.diff(r, x)
    * (r * (r - k) / 18 + Delta_def**2 / (12 * r**3))
) == 0

# Degenerate r=0 chart.
Qd = sp.Function("Qd")(x)
Ed = -k / 2
Bd = -k / 3
Cd = (4 * Qd + ell) / 3
Pd = M - k**2 / 18
degenerate_constant = -Cd * sp.diff(Qd, x) + Ed * sp.diff(Pd, x)
degenerate_first_integral = -2 * Qd**2 / 3 - ell * Qd / 3
assert sp.simplify(
    degenerate_constant - sp.diff(degenerate_first_integral, x)
) == 0
assert sp.expand(
    degenerate_first_integral
    - (ell**2 / 24 - sp.Rational(2, 3) * (Qd + ell / 4) ** 2)
) == 0


# ---------------------------------------------------------------------------
# Terminal local leading coefficients in every valuation chart.

rho, dlead = sp.symbols("rho dlead", nonzero=True)

# Generic chart, r has a pole:
# q0 cancellation gives rho/dlead^2=-2/9.
u_ratio = sp.symbols("u_ratio")
generic_r_pole_lead = (
    sp.Rational(1, 81)
    + sp.Rational(2, 27) * u_ratio
    + sp.Rational(1, 18) * u_ratio**2
)
assert sp.simplify(
    generic_r_pole_lead.subs(u_ratio, -sp.Rational(2, 9))
    + sp.Rational(1, 729)
) == 0

# Generic chart, r has a zero:
# q0 cancellation gives Delta/(rho*dlead^3)=-4/27.
v_ratio = sp.symbols("v_ratio")
generic_r_zero_lead = sp.Rational(1, 81) + v_ratio / 9
assert sp.simplify(
    generic_r_zero_lead.subs(v_ratio, -sp.Rational(4, 27))
    + sp.Rational(1, 243)
) == 0

# Degenerate r=0 chart:
# q0 cancellation gives rho/dlead^3=-1/27.
degenerate_lead = sp.Rational(1, 81) + 4 * u_ratio / 9
assert sp.simplify(
    degenerate_lead.subs(u_ratio, -sp.Rational(1, 27))
    + sp.Rational(1, 243)
) == 0


print("verified: degree-four leading equations and target-shear reductions")
print("verified: rational translation and constant target shear preserve the bracket")
print("verified: exact reverse translation to all polynomial coefficients")
print("verified: complete depressed (4,3) coefficient system and first integrals")
print("verified: generic r-chart derivative is d(H(r))/dx")
print("verified: degenerate r=0 chart has the separate quadratic first integral")
print("verified: all three terminal boundary-pole coefficients are nonzero")
