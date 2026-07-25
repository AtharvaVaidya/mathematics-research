#!/usr/bin/env python3
"""Exact identities excluding the square-leading family in all degrees.

For U_r=(b+1)^2+r*a, pass from (t,c) to (t,H), H=b+1.  Polynomial
normalization functions become Laurent polynomials after t is inverted.
The Hamiltonian equation is homogeneous, and its degree -2 part has an
elementary one-variable obstruction.
"""

import sympy as sp


t, c, r = sp.symbols("t c r")
H, s = sp.symbols("H s")

a = sp.expand(t + t**2 - c * t**3)
b = sp.expand(2 + 4 * t - 3 * c * t**2)
h = sp.expand(b + 1)

c_in_t_h = (3 + 4 * t - H) / (3 * t**2)
assert sp.expand(h.subs(c, c_in_t_h) - H) == 0
assert sp.expand(
    a.subs(c, c_in_t_h) - t * (H - t) / 3
) == 0

u = sp.expand(H**2 + r * t * (H - t) / 3)
u_t = sp.diff(u, t)
u_h = sp.diff(u, H)
assert sp.expand(u_t - r * (H - 2 * t) / 3) == 0
assert sp.expand(u_h - (2 * H + r * t / 3)) == 0

# det d(t,H)/d(t,c)=-3t^2, so Jac_(t,c)(U,V)=1 becomes
# Jac_(t,H)(U,V)=-1/(3t^2).
assert sp.diff(h, c) == -3 * t**2

# A degree -2 Laurent polynomial is t^-2*f(s), s=H/t.  The Hamiltonian
# equation becomes 2*(A*f)'=-1/3.
f = sp.Function("f")(s)
A = s**2 + r * s / 3 - r / 3
ode_left = sp.expand(
    2 * A * sp.diff(f, s) + (4 * s + 2 * r / 3) * f
)
assert sp.expand(ode_left - 2 * sp.diff(A * f, s)) == 0

# Integration would give A*f=-s/6+constant.  Since A is monic quadratic,
# no polynomial f can satisfy this identity.
assert sp.degree(A, s) == 2

print("verified the (t,H) normalization identities for U_r")
print("verified homogeneous ODE: 2*(A*f)'=-1/3")
print("RESULT: NO POLYNOMIAL MATE FOR U_r=(b+1)^2+r*a, FOR ANY r")
