#!/usr/bin/env python3
"""Verify a target-ring Liouville form for the fixed-plane normalization.

The normalized area form is not obstructed at the level of algebraic
de Rham exactness: it has an explicit primitive with coefficients in the
singular target ring.  The unresolved issue is the much stronger
factorization of such a primitive, up to an exact form, as U*dV.
"""

import sympy as sp


t, c = sp.symbols("t c")
A, B, C = sp.symbols("A B C")

a = t + t**2 - c * t**3
b = 2 + 4 * t - 3 * c * t**2

p = (27 * A * C**2 - 15 * B * C + 16) / 6
q = (3 * B**2 * C - 4 * B - 3 * C) / 12
r = (12 * A * B - B**3 + 3 * B + 2) / 12

target_substitution = {A: a, B: b, C: c}
p_tc = sp.expand(p.subs(target_substitution))
q_tc = sp.expand(q.subs(target_substitution))
r_tc = sp.expand(r.subs(target_substitution))

# Pull back alpha=p*dA+q*dB+r*dC and compare its two coefficients.
alpha_t = sp.expand(p_tc * sp.diff(a, t) + q_tc * sp.diff(b, t))
alpha_c = sp.expand(
    p_tc * sp.diff(a, c) + q_tc * sp.diff(b, c) + r_tc
)
assert sp.factor(alpha_t + 2 * c) == 0
assert sp.factor(alpha_c + t) == 0

# Therefore alpha=-2c*dt-t*dc and d(alpha)=dt wedge dc.
area_coefficient = sp.diff(alpha_c, t) - sp.diff(alpha_t, c)
assert sp.factor(area_coefficient - 1) == 0

# The normalization coordinate is a rational target function.  This
# records precisely where the obvious canonical primitive t*dc leaves
# the target ring.
D = 4 - 3 * b * c - 3 * c
N = b - 2 - 9 * c * a
assert sp.factor(N - t * D) == 0

print("verified the target-ring Liouville form alpha=-2c*dt-t*dc")
print("verified d(alpha)=dt wedge dc and t=(b-2-9ca)/(4-3bc-3c)")
print("RESULT: EXACT FIXED-PLANE LIOUVILLE FORM PASSES")
