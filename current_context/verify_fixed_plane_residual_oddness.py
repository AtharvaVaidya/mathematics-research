#!/usr/bin/env python3
"""Exact checks behind §1.15 of FIXED_SOURCE_PLANE_ROUTE.md."""

import sympy as sp


v, c, d, m = sp.symbols("v c d m", nonzero=True)
source_t = sp.symbols("source_t")
t_general = (v + 2) / (3 * c)
t_on_C = 3 * (v + 2) / v**2
D = v**2 - 9 * c

# The original conductor polynomial becomes v^2-9c.
D_original = (
    9 * c**2 * t_general**2 - 12 * c * t_general - 9 * c + 4
)
assert sp.factor(D_original - D) == 0

# dv ^ dc = 3c dt ^ dc and dD ^ dc = 2v dv ^ dc.
assert sp.diff((3 * c * source_t - 2) ** 2 - 9 * c, source_t) == (
    6 * c * (3 * c * source_t - 2)
)
area_Dc = sp.simplify(1 / (3 * c) / (2 * v))
assert area_Dc == 1 / (6 * c * v)
assert sp.simplify(area_Dc.subs(v, -v) + area_Dc) == 0

# Exact projective coordinates on the two conductor arms.
# At v=0 use T=1, so Z=1/t and C_hom=c/t.
Z_at_0 = sp.factor(1 / t_on_C)
C_at_0 = sp.factor(c.subs(c, v**2 / 9) / t_on_C)
assert sp.simplify(Z_at_0 - v**2 / (3 * (v + 2))) == 0
assert sp.simplify(C_at_0 - v**4 / (27 * (v + 2))) == 0

# At v=infinity put w=1/v and use C_hom=1.
w = sp.symbols("w", nonzero=True)
Z_at_inf = sp.factor((1 / c).subs(c, v**2 / 9).subs(v, 1 / w))
T_at_inf = sp.factor((t_on_C / c).subs(c, v**2 / 9).subs(v, 1 / w))
assert sp.simplify(Z_at_inf - 9 * w**2) == 0
assert sp.simplify(T_at_inf - 27 * w**3 * (2 * w + 1)) == 0

# If H|C=lambda*v^m and deg(H)=d, homogenization contributes Z^d.
I_0 = 2 * d + m
I_inf = 2 * d - m
assert sp.expand(I_0 + I_inf) == 4 * d

# For integral d and odd m, both intersection numbers have odd parity.
q = sp.symbols("q", integer=True)
assert sp.expand(I_0.subs(m, 2 * q + 1) - (2 * (d + q) + 1)) == 0
assert sp.expand(I_inf.subs(m, 2 * q + 1) - (2 * (d - q - 1) + 1)) == 0

# The minimal odd factor is already realized by a descended divisor.
a = t_on_C + t_on_C**2 - (v**2 / 9) * t_on_C**3
b = 2 + 4 * t_on_C - 3 * (v**2 / 9) * t_on_C**2
descended = 9 * b * (v**2 / 9) - 27 * a * (v**2 / 9) ** 2 - 8
assert sp.factor(descended) == 0  # D vanishes after restricting to C.

# Check the identity before restriction, where v=3ct-2 and D=v^2-9c.
a_general = t_general + t_general**2 - c * t_general**3
b_general = 2 + 4 * t_general - 3 * c * t_general**2
descended_general = 9 * b_general * c - 27 * a_general * c**2 - 8
assert sp.factor(descended_general - D * v) == 0

# If s is proportional to v^(2 delta), the target conormal unit can
# contain v^(m+1) only when m+1 is divisible by 2 delta.
ell = sp.symbols("ell", integer=True)
delta_positive = sp.symbols("delta_positive", integer=True, positive=True)
m_congruence = 2 * delta_positive * ell - 1
assert sp.expand(m_congruence + 1 - 2 * delta_positive * ell) == 0
assert sp.expand(
    (2 * d + m_congruence) - (2 * d - 1) - 2 * delta_positive * ell
) == 0
assert sp.expand(
    (2 * d - m_congruence) - (2 * d + 1) + 2 * delta_positive * ell
) == 0

print("fixed-plane residual oddness checks passed")
