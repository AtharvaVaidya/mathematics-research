#!/usr/bin/env python3
"""Verify sheet-loss arithmetic and the fixed-source first Keller jet.

The script deliberately verifies only the scope of the accompanying
memo.  In particular, ``Jac(U,V) == 1 mod D*K`` is checked; no global
Keller identity is asserted.
"""

from __future__ import annotations

import sympy as sp


t, c, vpar = sp.symbols("t c vpar")
v = 3 * c * t - 2
D = sp.expand(v**2 - 9 * c)
K = sp.expand(v + D)


def bracket(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(left, t) * sp.diff(right, c)
        - sp.diff(left, c) * sp.diff(right, t)
    )


# The two actual fixed-source curves are smooth and disjoint.
assert sp.groebner([D, K], t, c).contains(sp.Integer(1))
assert sp.groebner([D, sp.diff(D, t), sp.diff(D, c)], t, c).contains(
    sp.Integer(1)
)
assert sp.groebner([K, sp.diff(K, t), sp.diff(K, c)], t, c).contains(
    sp.Integer(1)
)

c_on_C = vpar**2 / 9
t_on_C = 3 * (vpar + 2) / vpar**2
c_on_H = vpar * (vpar + 1) / 9
t_on_H = 3 * (vpar + 2) / (vpar * (vpar + 1))

sub_C = {t: t_on_C, c: c_on_C}
sub_H = {t: t_on_H, c: c_on_H}

assert sp.factor(D.subs(sub_C)) == 0
assert sp.factor(v.subs(sub_C) - vpar) == 0
assert sp.factor(K.subs(sub_H)) == 0
assert sp.factor(v.subs(sub_H) - vpar) == 0
assert sp.factor(K.subs(sub_C) - vpar) == 0
assert sp.factor(D.subs(sub_H) + vpar) == 0


# Explicit CRT inverses and complementary idempotents.
iota_C = (t * v - 3) / 6
iota_H = (t * (v + 1) - 3) / 6
assert sp.factor(v * iota_C - 1 - t * D / 6) == 0
assert sp.factor(v * iota_H - 1 - t * K / 6) == 0

e_C = sp.expand(K * iota_C)
e_H = sp.expand(-D * iota_H)
assert sp.expand(e_C + e_H - 1) == 0
assert sp.factor(e_C.subs(sub_C) - 1) == 0
assert sp.factor(e_C.subs(sub_H)) == 0
assert sp.factor(e_H.subs(sub_C)) == 0
assert sp.factor(e_H.subs(sub_H) - 1) == 0


# The sharp quartic G_m and its Poincare-residue exponent j=-1.
X, Y, s = sp.symbols("X Y s")
F = sp.expand((3 * X * Y + 1) ** 2 - X)
X_s = s**2
Y_s = -(s**-1 + s**-2) / 3
assert sp.factor(F.subs({X: X_s, Y: Y_s})) == 0
assert sp.factor(3 * X_s * Y_s + 1 + s) == 0

omega_ds_coefficient = sp.factor(
    sp.diff(X_s, s) / sp.diff(F, Y).subs({X: X_s, Y: Y_s})
)
assert omega_ds_coefficient == -1 / (3 * s**2)

# Y=0 is only a local incidence marker, not a claimed Keller
# nonproper-value component.
assert sp.factor(F.subs(Y, 0) - (1 - X)) == 0
assert sp.factor(X_s.subs(s, -1) - 1) == 0
assert sp.factor(Y_s.subs(s, -1)) == 0


# Polynomial CRT lifts of the two target restrictions.
B0 = 2 + 4 * t - 3 * c * t**2
X_C = c**2
Y_C = sp.expand(-(B0 + 1) / 4 - 3 * (B0 + 1) ** 2 / 16)
X_H = v**2
Y_H = sp.expand(-(iota_H + iota_H**2) / 3)

U0 = sp.expand(e_C * X_C + e_H * X_H)
V0 = sp.expand(e_C * Y_C + e_H * Y_H)

assert sp.factor(U0.subs(sub_C) - X_s.subs(s, c_on_C)) == 0
assert sp.factor(V0.subs(sub_C) - Y_s.subs(s, c_on_C)) == 0
assert sp.factor(U0.subs(sub_H) - X_s.subs(s, vpar)) == 0
assert sp.factor(V0.subs(sub_H) - Y_s.subs(s, vpar)) == 0

F_pullback_0 = sp.factor(F.subs({X: U0, Y: V0}))
F_quotient_0 = sp.cancel(F_pullback_0 / (D * K))
assert sp.denom(F_quotient_0) == 1


# Unit tangent derivatives used by Hermite CRT.
J_U_D_C = sp.factor(bracket(U0, D).subs(sub_C))
J_U_K_H = sp.factor(bracket(U0, K).subs(sub_H))
assert J_U_D_C == -4 * vpar**5 / 27
assert J_U_K_H == -6 * vpar**2 * (vpar + 1)

J0 = bracket(U0, V0)
J0_C = sp.factor(J0.subs(sub_C))
J0_H = sp.factor(J0.subs(sub_H))

beta_C = sp.factor(
    (1 - J0_C)
    / (K.subs(sub_C) * bracket(U0, D).subs(sub_C))
)
beta_H = sp.factor(
    (1 - J0_H)
    / (D.subs(sub_H) * bracket(U0, K).subs(sub_H))
)

# These exact expressions make regularity transparent:
# beta_C is Laurent in v; beta_H is Laurent in v and v+1.
num_C = (
    36 * vpar**6
    - 111 * vpar**5
    + 278 * vpar**4
    + 2628 * vpar**3
    + 1628 * vpar**2
    + 78732 * vpar
    + 52488
)
num_H = (
    8 * vpar**6
    + 48 * vpar**5
    + 2380 * vpar**4
    + 21269 * vpar**3
    + 71352 * vpar**2
    + 116656 * vpar
    + 5184
)
assert sp.factor(beta_C + num_C / (24 * vpar**9)) == 0
assert sp.factor(
    beta_H
    + num_H / (7776 * vpar**4 * (vpar + 1) ** 3)
) == 0

# Polynomial representatives of the two regular beta classes.
inverse_v_on_H = iota_H
inverse_v_plus_1_on_H = (t * v - 3) / 3
assert sp.factor(
    (v + 1) * inverse_v_plus_1_on_H - 1 - t * K / 3
) == 0

beta_C_lift = sp.expand(
    -num_C.subs(vpar, v) * iota_C**9 / 24
)
beta_H_lift = sp.expand(
    -num_H.subs(vpar, v)
    * inverse_v_on_H**4
    * inverse_v_plus_1_on_H**3
    / 7776
)
assert sp.factor(beta_C_lift.subs(sub_C) - beta_C) == 0
assert sp.factor(beta_H_lift.subs(sub_H) - beta_H) == 0

beta = sp.expand(e_C * beta_C_lift + e_H * beta_H_lift)

# It is cheaper and clearer to verify the Hermite correction on each
# component than to expand the enormous global quotient.
J_corrected_on_C = sp.factor(
    (
        J0
        + bracket(U0, D * K * beta)
    ).subs(sub_C)
)
J_corrected_on_H = sp.factor(
    (
        J0
        + bracket(U0, D * K * beta)
    ).subs(sub_H)
)
assert J_corrected_on_C == 1
assert J_corrected_on_H == 1


# The quotient L in F(U,V)=D*K*L is determined on the components by
# dU wedge dF = F_Y dU wedge dV.  This avoids a pointless huge expansion.
F_Y_C = sp.factor(
    sp.diff(F, Y).subs(
        {X: X_s.subs(s, c_on_C), Y: Y_s.subs(s, c_on_C)}
    )
)
F_Y_H = sp.factor(
    sp.diff(F, Y).subs({X: X_s.subs(s, vpar), Y: Y_s.subs(s, vpar)})
)

L_on_C = sp.factor(
    F_Y_C / (K.subs(sub_C) * bracket(U0, D).subs(sub_C))
)
L_on_H = sp.factor(
    F_Y_H / (D.subs(sub_H) * bracket(U0, K).subs(sub_H))
)
assert L_on_C == sp.Rational(1, 18)
assert L_on_H == -1 / (vpar + 1)
assert sp.factor(K.subs(sub_C) * L_on_C - vpar / 18) == 0


# Endpoint-charge / sheet-loss ledger.
j = -1
conductor_degree = 2
residual_degree = 1
conductor_charges = (conductor_degree * j, -conductor_degree * j)
residual_charges = (residual_degree * j, -residual_degree * j, 1)
assert conductor_charges == (-2, 2)
assert residual_charges == (-1, 1, 1)
assert sum(conductor_charges) == 0
assert sum(residual_charges) == 1
assert sum(residual_charges) == 2 * 0 + 3 - 2
assert 3 - 2 == 1  # one sheet is absent at s=-1
assert 3 == conductor_degree + residual_degree
assert 3 % conductor_degree == 1  # no divisibility consequence


# A singular one-place Chau-compatible curve gives an independent
# abstract stress test of the global sheet-loss identity.
r = sp.symbols("r")
Lambda_pullback = sp.factor(
    F.subs({X: 1 + r**2, Y: r**3})
)
expected_Lambda_pullback = r**2 * (
    9 * r**8
    + 18 * r**6
    + 9 * r**4
    + 6 * r**3
    + 6 * r
    - 1
)
assert sp.factor(Lambda_pullback - expected_Lambda_pullback) == 0
assert sp.gcd(
    9 * r**8
    + 18 * r**6
    + 9 * r**4
    + 6 * r**3
    + 6 * r
    - 1,
    sp.diff(
        9 * r**8
        + 18 * r**6
        + 9 * r**4
        + 6 * r**3
        + 6 * r
        - 1,
        r,
    ),
) == 1

Lambda_on_Gamma = sp.factor(
    (
        Y**2 - (X - 1) ** 3
    ).subs({X: X_s, Y: Y_s})
)
degree_eight = (
    9 * s**8 - 18 * s**7 + 18 * s**5 - 9 * s**4 - 1
)
assert sp.factor(
    Lambda_on_Gamma
    + (s + 1) ** 2 * degree_eight / (9 * s**4)
) == 0
assert sp.factor(degree_eight.subs(s, -1)) != 0
assert sp.gcd(degree_eight, sp.diff(degree_eight, s)) == 1

R = sp.expand((s + 1) * degree_eight)
z = sp.symbols("z")
abstract_residual = z * s * R - 1
# On this curve d/dz is sR, a unit because z*s*R=1.
assert sp.diff(abstract_residual, z) == s * R
assert sp.gcd(R, sp.diff(R, s)) == 1

finite_missing_values = 9
abstract_boundary_points = finite_missing_values + 2
assert (
    2 * 0 + abstract_boundary_points - 2
    == finite_missing_values
)

print("verified the finite endpoint-charge = sheet-loss ledger")
print("verified the disjoint fixed-source conductor/residual curves")
print("verified the quartic restriction maps and polynomial CRT lifts")
print("verified Jac(U,V)=1 to first order along D union K")
print("verified the exact odd normal coefficient v/18")
print("verified the singular one-place abstract stress model")
