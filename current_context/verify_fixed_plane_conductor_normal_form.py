#!/usr/bin/env python3
"""Verify the localized pinch normal form of the fixed-plane target ring.

The normal form replaces the original three target generators by an even
coordinate x=v^2 and the conductor-odd coordinate y=v*(v^2-9c).  It turns
the Darboux equation into two explicit boundary equations on x=9c.
"""

import sympy as sp


t, c, v, x = sp.symbols("t c v x", nonzero=True)
a = t + t**2 - c * t**3
b = 2 + 4 * t - 3 * c * t**2
v_tc = 3 * c * t - 2
D_tc = sp.expand(v_tc**2 - 9 * c)

# The involution exchanges the two normalization branches over the
# conductor and fixes b,c.
tau_t = 4 / (3 * c) - t
assert sp.factor(b.subs(t, tau_t) - b) == 0
assert sp.factor(v_tc.subs(t, tau_t) + v_tc) == 0
assert sp.factor(
    a.subs(t, tau_t) - a - 2 * v_tc * D_tc / (27 * c**2)
) == 0

# After localizing at c, the target ring is
#
#   Q[c^+-1,x,y]/(y^2-x*(x-9c)^2),
#
# with x=v^2 and y=v*(x-9c).
t_vc = (v + 2) / (3 * c)
a_vc = sp.factor(a.subs(t, t_vc))
b_vc = sp.factor(b.subs(t, t_vc))
D = x - 9 * c
y = v * D
assert sp.factor(b_vc.subs(v**2, x) - (4 + 6 * c - x) / (3 * c)) == 0
assert sp.factor(
    a_vc - (18 * c - 3 * v**2 + 4 - v * (v**2 - 9 * c)) / (27 * c**2)
) == 0
assert sp.expand(y**2 - x * D**2).subs(v**2, x) == 0

# The area coefficient in (v,c) coordinates is 1/(3c):
# Jac_(t,c)=3c*Jac_(v,c).
U_v, U_c, V_v, V_c = sp.symbols("U_v U_c V_v V_c")
assert sp.det(sp.Matrix([[sp.diff(v_tc, t), sp.diff(v_tc, c)], [0, 1]])) == 3 * c

# Write arbitrary target-ring elements as
#
#   U=F(c,x)+y*G(c,x),  V=P(c,x)+y*Q(c,x).
#
# The following independent jet symbols encode their derivatives.  On the
# conductor D=0 (x=9c), the odd and even parts of Jac_(v,c) give the two
# displayed boundary equations in the memo.
Fx, Fc, G, Gx, Gc = sp.symbols("Fx Fc G Gx Gc")
Px, Pc, Q, Qx, Qc = sp.symbols("Px Pc Q Qx Qc")
y_v = 3 * x - 9 * c
y_c = -9 * v
U_v_expr = 2 * v * Fx + y_v * G + 2 * v * y * Gx
U_c_expr = Fc + y_c * G + y * Gc
V_v_expr = 2 * v * Px + y_v * Q + 2 * v * y * Qx
V_c_expr = Pc + y_c * Q + y * Qc
J = sp.expand(U_v_expr * V_c_expr - U_c_expr * V_v_expr)
J = sp.expand(J.subs(v**4, x**2).subs(v**3, v * x).subs(v**2, x))
J_even = sp.factor((J + J.subs(v, -v)) / 2)
J_odd_over_v = sp.factor((J - J.subs(v, -v)) / (2 * v))
J_even_C = sp.factor(J_even.subs(x, 9 * c))
J_odd_C = sp.factor(J_odd_over_v.subs(x, 9 * c))
assert sp.factor(
    J_even_C - 18 * c * (G * (Pc + 9 * Px) - Q * (Fc + 9 * Fx))
) == 0
assert sp.factor(J_odd_C - 2 * (Fx * Pc - Fc * Px)) == 0

# Thus a normalized Darboux pair must satisfy on x=9c
#
#   Fx*Pc-Fc*Px = 0,
#   G*(Pc+9Px)-Q*(Fc+9Fx) = 1/(54c^2).

# The conductor parametrization also fixes the odd boundary value of the
# global symplectic primitive dS=U*dV-t*dc.
c_of_v = v**2 / 9
t_on_C = 3 * (v + 2) / v**2
t_on_C_tau = t_on_C.subs(v, -v)
dc_dv = sp.diff(c_of_v, v)
assert sp.factor((t_on_C - t_on_C_tau) * dc_dv) == sp.Rational(4, 3)

print("verified the conductor involution and localized pinch presentation")
print("verified the even/odd Darboux boundary equations on x=9c")
print("verified the forced odd symplectic-primitive boundary derivative")
print("RESULT: EXACT FIXED-PLANE CONDUCTOR NORMAL FORM PASSES")
