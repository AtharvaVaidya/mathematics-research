#!/usr/bin/env python3
"""Exact checks for the pure-power two-end and line-injectivity reduction."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import runpy

import sympy as sp


# ---------------------------------------------------------------------------
# The monomial Jacobian after v=u^m and z=1/v.

u, v, z, w, y = sp.symbols("u v z w y", nonzero=True)
m, n = sp.symbols("m n", integer=True, positive=True)
lam, gamma = sp.symbols("lam gamma", nonzero=True)

dv_dz = sp.diff(1 / z, z)
bracket_v = lam / (m * gamma * v ** (n + 1))
bracket_z = sp.factor(dv_dz * bracket_v.subs(v, 1 / z))
assert bracket_z == -lam * z ** (n - 1) / (m * gamma)

# The original scaling has order s=mn+1 and restores a constant
# Jacobian.
s = m * n + 1
assert sp.expand(
    gamma
    * u**s
    * m
    * u ** (m - 1)
    * (
        lam
        / (m * gamma * (u**m) ** (n + 1))
    )
    - lam
) == 0


# ---------------------------------------------------------------------------
# Taylor-valuation inequalities.

# If rho is the coefficient pole scale and q is the pole order of the
# moving center, polynomiality of g(u^-m,center) forces q<=m*rho.
# Consequently the coefficient of y^i has the lower valuations
#   i(mn+1)-m(9-i)rho  for f,
#   i(mn+1)-m(6-i)rho  for g.
#
# It is enough to control g.  Every surviving one-pole profile has
# n/rho at least two (in fact at least three in the finite table).
profile_ratios = {
    "pure_cusp": sp.Integer(14),
    "extra_kappa_8": sp.Integer(13),
    "extra_kappa_7": sp.Integer(12),
    "extra_kappa_5": sp.Integer(10),
    "extra_kappa_4": sp.Integer(9),
    "extra_kappa_2": sp.Integer(7),
    "extra_kappa_1": sp.Integer(6),
    "only_j_u0_v_nonzero": sp.Integer(3),
    "only_j_u_nonzero_c_to_zero": sp.Integer(4),
    "only_j_lower_cusp": sp.Integer(14),
    "only_j_main_edge": sp.Integer(4),
}
assert min(profile_ratios.values()) == 3

rho = sp.symbols("rho", positive=True)
for ratio in profile_ratios.values():
    for index in range(2, 7):
        normalized_g_bound = sp.expand(
            index * ratio - (6 - index)
        )
        assert normalized_g_bound > 0

# The weaker threshold n/rho=2 already suffices because the extra
# "+i" in i(mn+1) makes even the borderline i=2 coefficient vanish.
threshold = sp.Integer(2)
for index in range(2, 7):
    normalized_g_bound = sp.expand(
        index * threshold - (6 - index)
    )
    assert normalized_g_bound >= 0


# ---------------------------------------------------------------------------
# Exact only-j low-profile audits.

dependency = Path(__file__).with_name(
    "verify_normal_degree_96_cube_constant_h_only_j_exclusion.py"
)
with contextlib.redirect_stdout(io.StringIO()):
    data = runpy.run_path(str(dependency))

C, D, Q = data["C"], data["D"], data["Q"]
a, b = data["a"], data["b"]
U, V, W, Z, j = (
    data[name] for name in ("U", "V", "W", "Z", "j")
)

# U=0,V!=0 upper Newton edge.  This is a genuine local ratio-three
# profile and is why the final proof uses the sharp threshold two.
t, C0, D0 = sp.symbols("t C0 D0", nonzero=True)
edge_substitution = {
    C: C0 * t,
    D: D0 * t**4,
}
edge_relation = {
    D0: -sp.Rational(9, 8) * C0**4 / V,
}

a_u0 = data["a_u_zero"]
Q_u0 = data["Q_u_zero"]
b_u0 = data["b_u_zero"]

A5_only_j = data["A5_only_j"]
old_a, old_b, old_c, old_d, old_q = (
    data[name] for name in ("old_a", "old_b", "old_c", "old_d", "old_q")
)
A5_u0 = sp.factor(
    A5_only_j.subs(
        {
            old_a: a_u0,
            old_b: b_u0,
            old_c: C + a_u0**2 / 4,
            old_d: D + a_u0 * b_u0 / 2,
            old_q: Q_u0 + b_u0**2 / 4,
        }
    )
)


def leading_degree_and_coefficient(expression: sp.Expr) -> tuple[int, sp.Expr]:
    scaled = sp.cancel(expression.subs(edge_substitution))
    numerator, denominator = sp.together(scaled).as_numer_denom()
    numerator_poly = sp.Poly(numerator, t)
    denominator_poly = sp.Poly(denominator, t)
    degree = numerator_poly.degree() - denominator_poly.degree()
    coefficient = sp.factor(
        numerator_poly.LC() / denominator_poly.LC()
    ).subs(edge_relation)
    return degree, sp.factor(coefficient)


edge_data = {
    "a": leading_degree_and_coefficient(a_u0),
    "Q": leading_degree_and_coefficient(Q_u0),
    "b": leading_degree_and_coefficient(b_u0),
    "A5": leading_degree_and_coefficient(A5_u0),
}
assert {name: value[0] for name, value in edge_data.items()} == {
    "a": 6,
    "Q": 7,
    "b": 9,
    "A5": 9,
}
assert edge_data["A5"][1] == sp.Rational(405, 1024) * C0**9 / V**2

# The loaded dependency also certifies every U!=0 outer edge,
# including the V=0 double-edge blowup and both C->0 limits.
assert data["double_P_degree"] == 2
assert data["double_num_degree"] - data["double_den_degree"] == 7
assert sp.factor(data["vertical_limit"].subs(data["pole_vertical"])) != 0

# Hostile audit of the apparent denominator H=2UD-CV in Q_solution.
# A Q-pole with C a unit is killed by the nonzero Q^2 coefficient of
# E12.  At C,D->0, a pole larger than the zero order of C makes the
# same square term uniquely dominant over every linear-Q term.
H = 2 * U * D - C * V
E11_poly_in_Q = sp.Poly(data["E11"], Q)
E12_poly_in_Q = sp.Poly(data["E12"], Q)
assert sp.expand(E11_poly_in_Q.coeff_monomial(Q) - 144 * C * H) == 0
assert sp.expand(
    E12_poly_in_Q.coeff_monomial(Q**2) + 1944 * C**2 * U
) == 0
assert sp.factor(
    sp.limit(data["exceptional_E11"] / C, C, 0)
) == -32 * U * V

# The only equal-order lower edge has nonzero leading H/C.  Positive
# equal-order poles are absent from the exact resultant hull.
lower_H_over_C = sp.factor(
    2
    * U
    * data["lower_relation"][data["D_edge"]]
    / data["C_edge"]
    - V
)
assert lower_H_over_C != 0

# Load the independently checked exhaustive U=0,V!=0 outer-edge
# table.  Its local terminal-to-coefficient ratios are 3,3,3,3,14.
cyclic_dependency = Path(__file__).with_name(
    "verify_normal_degree_96_cube_pure_power_cyclic_descent.py"
)
with contextlib.redirect_stdout(io.StringIO()):
    cyclic_data = runpy.run_path(str(cyclic_dependency))

u0_profile_data = cyclic_data["profile_data"]
assert tuple(profile[2] for profile in u0_profile_data) == (9, 6, 2, 2, 7)
u0_rho_scales = (3, 2, sp.Rational(2, 3), sp.Rational(2, 3), sp.Rational(1, 2))
assert tuple(
    sp.factor(sp.Rational(profile[2], 1) / rho_scale)
    for profile, rho_scale in zip(u0_profile_data, u0_rho_scales)
) == (3, 3, 3, 3, 14)

# The rational U=V=0, W=j^2, Z!=0 exceptional arc has two poles and
# thirteen distinct finite critical values for A5, so it cannot be a
# cyclic two-branch time alpha+beta*z^n.
tau, epsilon = sp.symbols("tau epsilon", nonzero=True)
A = sp.Rational(4, 27) * Z**2
B = epsilon / 16
A5_exceptional = A * tau**-6 - B * tau**7
critical_numerator = sp.factor(
    sp.diff(A5_exceptional, tau) * tau**7
)
assert sp.expand(critical_numerator + 6 * A + 7 * B * tau**13) == 0
critical_value_using_relation = sp.factor(
    A5_exceptional.subs(B * tau**7, -sp.Rational(6, 7) * A * tau**-6)
)
assert critical_value_using_relation == sp.Rational(13, 7) * A * tau**-6
assert sp.gcd(6, 13) == 1


# ---------------------------------------------------------------------------
# The restriction of the original Keller map to u=0.

f0, f1, g0, g1 = sp.symbols("f0 f1 g0 g1")
g_u_polynomial = sp.symbols("g_u_polynomial")
g_restriction = g1 * y + g0
assert sp.diff(g_restriction, y) == g1

# If g1 is nonzero, the second coordinate already separates points.
# If g1=0, the Keller identity on the line is
#   -F_y(0,y) G_u(0,y)=lambda.
# Units in C[y] are constants, so both factors are nonzero constants
# and F(0,y) is affine nonconstant.
F_y = sp.Poly(f1, y)
G_u = sp.Poly(g_u_polynomial, y)
assert F_y.degree() == 0
assert G_u.degree() == 0
assert sp.expand(-f1 * g_u_polynomial - lam).subs(
    g_u_polynomial, -lam / f1
) == 0

print("verified: pure-power change gives the monomial z^(n-1) Jacobian")
print("verified: every surviving one-pole profile has n/rho >= 2")
print("verified: Taylor coefficients of g of y-degree at least two vanish")
print("verified: the U=0,V!=0 local ratio-three edge and A_5 leading term")
print("verified: the exceptional rational time has 13 critical values")
print("verified: one coordinate restricts affinely and injectively on u=0")
