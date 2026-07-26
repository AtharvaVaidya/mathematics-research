#!/usr/bin/env python3
"""Exact checks for the constant-h, only-j cube-chart exclusion."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import runpy

import sympy as sp


C, D, Q = sp.symbols("C D Q")
a, b = sp.symbols("a b")
U, V, W, Z, j = sp.symbols("U V W Z j")

I10 = sp.Rational(3, 8) * (
    3 * C**2 * a - 12 * C * Q - 8 * C * j - 6 * D**2
)
I11 = sp.Rational(3, 8) * (
    3 * C**2 * b + 6 * C * D * a - 12 * D * Q - 8 * D * j
)
I12 = sp.Rational(1, 8) * (
    3 * C**3
    - 3 * C**2 * a**2
    + 18 * C * D * b
    + 12 * C * Q * a
    + 8 * C * a * j
    + 6 * D**2 * a
    - 18 * Q**2
    - 24 * Q * j
)
I13 = sp.Rational(9, 8) * C**2 * D - b * I10 / 3 - a * I11 / 6


# U=0, V!=0: after C is shown constant, exact elimination leaves
# a genuine quartic in D.
a_u_zero = sp.factor(
    6 * (sp.Rational(9, 8) * C**2 * D - Z) / V
)
Q_u_zero = sp.factor(
    (3 * C**2 * a_u_zero - 8 * C * j - 6 * D**2) / (12 * C)
)
b_u_zero = sp.factor(
    (
        sp.Rational(8, 3) * V
        - 6 * C * D * a_u_zero
        + 12 * D * Q_u_zero
        + 8 * D * j
    )
    / (3 * C**2)
)
quartic = sp.factor(
    sp.together(
        I12.subs(
            {a: a_u_zero, b: b_u_zero, Q: Q_u_zero}
        )
        - W
    ).as_numer_denom()[0]
)
expected_quartic = (
    -6561 * C**8 * D**2
    + 11664 * C**6 * D * Z
    + 384 * C**5 * V**2
    - 11664 * C**4 * D**3 * V
    - 5184 * C**4 * Z**2
    + 10368 * C**2 * D**2 * V * Z
    - 1024 * C**2 * V**2 * W
    + 1024 * C**2 * V**2 * j**2
    + 2048 * C * D * V**3
    - 5184 * D**4 * V**2
)
assert sp.expand(quartic - expected_quartic) == 0
assert sp.Poly(quartic, D).LC() == -5184 * V**2


# U!=0: solve I10 and the exact I13 identity for a,b.
a_solution = sp.factor(
    (sp.Rational(8, 3) * U + 12 * C * Q + 8 * C * j + 6 * D**2)
    / (3 * C**2)
)
b_solution = sp.factor(
    sp.Rational(27, 8) * C**2 * D / U
    - V * a_solution / (2 * U)
    - 3 * Z / U
)
assert sp.factor(I10.subs(a, a_solution) - U) == 0
assert sp.factor(
    I13.subs({a: a_solution, b: b_solution, I10: U, I11: V})
    - Z
) == 0

E11 = sp.factor(
    sp.together(
        I11.subs({a: a_solution, b: b_solution}) - V
    ).as_numer_denom()[0]
)
E12 = sp.factor(
    sp.together(
        I12.subs({a: a_solution, b: b_solution}) - W
    ).as_numer_denom()[0]
)
expected_E11 = (
    243 * C**5 * D
    - 216 * C**3 * Z
    - 144 * C**2 * Q * V
    - 96 * C**2 * V * j
    - 72 * C * D**2 * V
    + 288 * C * D * Q * U
    + 192 * C * D * U * j
    - 96 * C * U * V
    + 288 * D**3 * U
    + 128 * D * U**2
)
expected_E12 = (
    6561 * C**5 * D**2
    + 324 * C**5 * U
    - 5832 * C**3 * D * Z
    - 3888 * C**2 * D * Q * V
    - 2592 * C**2 * D * V * j
    - 1944 * C**2 * Q**2 * U
    - 2592 * C**2 * Q * U * j
    - 864 * C**2 * U * W
    - 1944 * C * D**3 * V
    - 864 * C * D * U * V
    - 1152 * C * Q * U**2
    - 768 * C * U**2 * j
    - 576 * D**2 * U**2
    - 256 * U**3
)
assert sp.expand(E11 - expected_E11) == 0
assert sp.expand(E12 - expected_E12) == 0

resultant = sp.factor(sp.resultant(E11, E12, Q))
P = sp.factor(resultant / (648 * C**2 * U))
assert sp.expand(resultant - 648 * C**2 * U * P) == 0

# The unique upper Newton edge for weights wt(C,D)=(2,5).
P_poly = sp.Poly(P, C, D)
weighted_terms: dict[int, sp.Expr] = {}
for (c_power, d_power), coefficient in P_poly.terms():
    weight = 2 * c_power + 5 * d_power
    weighted_terms[weight] = (
        weighted_terms.get(weight, 0)
        + coefficient * C**c_power * D**d_power
    )
assert max(weighted_terms) == 30
expected_top = -243 * D**2 * (27 * C**5 - 32 * U * D**2) ** 2
assert sp.factor(weighted_terms[30] - expected_top) == 0
assert all(weight < 30 for weight in weighted_terms if weight != 30)


# Exceptional coefficient 2UD-CV.
exceptional_D = C * V / (2 * U)
exceptional_E11 = sp.factor(E11.subs(D, exceptional_D))
expected_exceptional = (
    C
    * (
        243 * C**5 * U * V
        - 432 * C**2 * U**2 * Z
        + 36 * C**2 * V**3
        - 64 * U**3 * V
    )
    / (2 * U**2)
)
assert sp.factor(exceptional_E11 - expected_exceptional) == 0


# Load the already verified full-cube Laurent residue A_5 without
# duplicating its formal-series implementation.
dependency_path = Path(__file__).with_name(
    "verify_normal_degree_96_cube_laurent_time_reduction.py"
)
with contextlib.redirect_stdout(io.StringIO()):
    cube_data = runpy.run_path(str(dependency_path))

A5 = cube_data["A"][5]
old_a, old_b, old_c, old_d, old_q = (
    cube_data[name] for name in ("a", "b", "c", "d", "q")
)
only_j = {
    cube_data["kappa8"]: 0,
    cube_data["kappa7"]: 0,
    cube_data["kappa5"]: 0,
    cube_data["kappa4"]: 0,
    cube_data["kappa2"]: 0,
    cube_data["kappa1"]: 0,
    cube_data["j"]: j,
}
A5_only_j = sp.factor(A5.subs(only_j))


# D=0 lower cusp.
lower_cusp_a = sp.factor(
    (sp.Rational(8, 3) * U + 12 * C * Q + 8 * C * j)
    / (3 * C**2)
)
lower_cusp_substitution = {
    old_a: lower_cusp_a,
    old_b: 0,
    old_c: C + lower_cusp_a**2 / 4,
    old_d: 0,
    old_q: Q,
}
lower_cusp_A5 = sp.factor(A5_only_j.subs(lower_cusp_substitution))

v = sp.symbols("v")
C0, D0, Q0 = sp.symbols("C0 D0 Q0", nonzero=True)
scaled_lower_cusp = sp.cancel(
    lower_cusp_A5.subs({C: C0 * v**2, Q: Q0 * v**3})
)
lower_num, lower_den = sp.together(scaled_lower_cusp).as_numer_denom()
lower_num_poly = sp.Poly(lower_num, v)
lower_den_poly = sp.Poly(lower_den, v)
assert lower_num_poly.degree() - lower_den_poly.degree() == 7
lower_lead = sp.factor(lower_num_poly.LC() / lower_den_poly.LC())
assert lower_lead == -C0**2 * Q0 / 16


# Main (2,5)-Newton branch.  Solve E11 for Q; the denominator is
# nonzero outside the exceptional branch already checked.
Q_solution = sp.factor(sp.solve(E11, Q)[0])
a_cd = sp.factor(a_solution.subs(Q, Q_solution))
b_cd = sp.factor(b_solution.subs(Q, Q_solution))
main_substitution = {
    old_a: a_cd,
    old_b: b_cd,
    old_c: C + a_cd**2 / 4,
    old_d: D + a_cd * b_cd / 2,
    old_q: Q_solution + b_cd**2 / 4,
}
main_A5 = sp.factor(A5_only_j.subs(main_substitution))
scaled_main = sp.cancel(
    main_A5.subs({C: C0 * v**2, D: D0 * v**5})
)
main_num, main_den = sp.together(scaled_main).as_numer_denom()
main_num_poly = sp.Poly(main_num, v)
main_den_poly = sp.Poly(main_den, v)
assert main_num_poly.degree() - main_den_poly.degree() == 12
main_lead = sp.factor(main_num_poly.LC() / main_den_poly.LC())
main_lead_on_edge = sp.factor(
    main_lead.subs(D0**2, sp.Rational(27, 32) * C0**5 / U)
)
assert main_lead_on_edge == sp.Rational(567, 2048) * C0**6 / U

print("verified: centered invariant identity and elementary-level splits")
print("verified: exact U!=0 elimination and unique (2,5) Newton edge")
print("verified: exceptional denominator branch")
print("verified: lower-cusp A_5 has nonzero degree-7 leading term")
print("verified: main Newton branch A_5 has nonzero degree-12 leading term")
print("verified: constant-h only-j cube chart is excluded")
