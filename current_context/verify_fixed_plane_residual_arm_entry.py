#!/usr/bin/env python3
"""Exact chart checks for FIXED_PLANE_RESIDUAL_ARM_ENTRY.md."""

import sympy as sp


x, y, u, w = sp.symbols("x y u w")

# (2,5) arm: C: y^2 - 3 y x^3 - 6 x^5, minimal residual H: y.
c25 = y**2 - 3 * y * x**3 - 6 * x**5
h25 = y

# Blow up y=xu, then u=xw.
c25_1 = sp.cancel(c25.subs(y, x * u) / x**2)
h25_1 = sp.cancel(h25.subs(y, x * u) / x)
assert sp.expand(c25_1 - (u**2 - 3 * u * x**2 - 6 * x**3)) == 0
assert h25_1 == u

c25_2 = sp.cancel(c25_1.subs(u, x * w) / x**2)
h25_2 = sp.cancel(h25_1.subs(u, x * w) / x)
assert sp.expand(c25_2 - (w**2 - 3 * w * x - 6 * x)) == 0
assert h25_2 == w

# At the next center C has tangent x=0 while H has tangent w=0.
assert sp.diff(c25_2, x).subs({x: 0, w: 0}) == -6
assert sp.diff(c25_2, w).subs({x: 0, w: 0}) == 0

# In the chart w=xW of the third blowup, H meets the new exceptional
# while C is absent there: this is the generic E3 exit.
W = sp.symbols("W")
c25_3_h_chart = sp.cancel(c25_2.subs(w, x * W) / x)
h25_3_h_chart = sp.cancel(h25_2.subs(w, x * W) / x)
assert c25_3_h_chart.subs(x, 0) == -6
assert h25_3_h_chart == W

# (2,3) arm and the homogenized minimal residual 3y-2x^2.
c23 = 9 * y**2 - 12 * y * x**2 - 9 * x**3 + 4 * x**4
h23 = 3 * y - 2 * x**2

# Blow up y=xu.
c23_1 = sp.cancel(c23.subs(y, x * u) / x**2)
h23_1 = sp.cancel(h23.subs(y, x * u) / x)
assert sp.expand(c23_1 - (9 * u**2 - 12 * u * x - 9 * x + 4 * x**2)) == 0
assert sp.expand(h23_1 - (3 * u - 2 * x)) == 0

# C has tangent x=0 and H has tangent 3u-2x=0, so they separate on F2.
assert sp.diff(c23_1, x).subs({x: 0, u: 0}) == -9
assert sp.diff(c23_1, u).subs({x: 0, u: 0}) == 0

# In the chart u=xW, C is absent from F2 while H meets it at W=2/3.
c23_2_h_chart = sp.cancel(c23_1.subs(u, x * W) / x)
h23_2_h_chart = sp.cancel(h23_1.subs(u, x * W) / x)
assert c23_2_h_chart.subs(x, 0) == -9
assert sp.solve(h23_2_h_chart.subs(x, 0), W) == [sp.Rational(2, 3)]

# Total attachment arithmetic.
d, delta, ell = sp.symbols("d delta ell", integer=True)
m = 2 * delta * ell - 1
I0 = 2 * d + m
Iinf = 2 * d - m
assert sp.expand(I0 + Iinf - 4 * d) == 0
assert sp.expand((I0 - Iinf) - (4 * delta * ell - 2)) == 0

print("fixed-plane residual arm-entry checks passed")
