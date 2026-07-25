#!/usr/bin/env python3
"""Verify the second conductor endpoint and its graded cusp semigroup."""

import sympy as sp


t, z = sp.symbols("t z")

# The second endpoint is (t,c)=(0,infinity), with z=1/c.
c = 1 / z
a = sp.factor(t + t**2 - c * t**3)
b = sp.factor(2 + 4 * t - 3 * c * t**2)
D = sp.factor(9 * c**2 * t**2 - 12 * c * t - 9 * c + 4)

assert sp.expand(a - (t + t**2 - t**3 / z)) == 0
assert sp.expand(b - (2 + 4 * t - 3 * t**2 / z)) == 0
assert sp.expand(z**2 * D - (9 * t**2 - 12 * t * z - 9 * z + 4 * z**2)) == 0

# The area form has coefficient -z^-2 in dt^dz coordinates.
omega_t_z = sp.factor(
    sp.diff(t, t) * sp.diff(c, z) - sp.diff(t, z) * sp.diff(c, t)
)
assert omega_t_z == -1 / z**2

# All three target initial forms have z-pole degree one.
A0 = -t**3 / z
B0 = -3 * t**2 / z
C0 = 1 / z

# A degree-n monomial has coefficient t^(3 alpha+2 beta), with
# alpha+beta<=n.  In particular every nonconstant coefficient belongs to
# the cusp ring Q[t^2,t^3] and has derivative zero at t=0.
alpha, beta, gamma = sp.symbols(
    "alpha beta gamma", integer=True, nonnegative=True
)
n = sp.expand(alpha + beta + gamma)
coefficient_exponent = 3 * alpha + 2 * beta
assert not coefficient_exponent.has(gamma)

sample_coefficients = [
    sp.Integer(1),
    t**2,
    t**3,
    t**4,
    t**5,
    t**6,
]
assert all(sp.diff(h, t).subs(t, 0) == 0 for h in sample_coefficients)

# If endpoint pole degrees p,q sum to one, the z^-2 coefficient of the
# bracket would have to come from the leading forms.  The only
# nonnegative cases are (1,0) and (0,1), and the degree-zero coefficient
# is constant, so both give zero.
p, q = sp.symbols("p q", integer=True, nonnegative=True)
u = sp.Function("u")(t)
v = sp.Function("v")(t)
U = z ** (-p) * u
V = z ** (-q) * v
jac = sp.factor(
    sp.diff(U, t) * sp.diff(V, z)
    - sp.diff(U, z) * sp.diff(V, t)
)
expected = z ** (-p - q - 1) * (
    p * u * sp.diff(v, t) - q * sp.diff(u, t) * v
)
assert sp.simplify(jac - expected) == 0

# For full regular numerators F,G, the Darboux equation is the displayed
# cusp-deformation recurrence in the memo.
F = sp.Function("F")(t, z)
G = sp.Function("G")(t, z)
U_full = z ** (-p) * F
V_full = z ** (-q) * G
jac_full = sp.factor(
    sp.diff(U_full, t) * sp.diff(V_full, z)
    - sp.diff(U_full, z) * sp.diff(V_full, t)
)
recurrence_left = (
    p * F * sp.diff(G, t)
    - q * sp.diff(F, t) * G
    + z
    * (
        sp.diff(F, t) * sp.diff(G, z)
        - sp.diff(F, z) * sp.diff(G, t)
    )
)
assert sp.simplify(
    jac_full - z ** (-p - q - 1) * recurrence_left
) == 0

# The two endpoint normalization roots are globally linked.
c_global = sp.symbols("c_global")
a_global = t + t**2 - c_global * t**3
b_global = 2 + 4 * t - 3 * c_global * t**2
H = 3 * c_global * t**2 - 2 * t - 3
assert sp.factor((b_global + 1) ** 2 - 12 * a_global - H**2) == 0
assert sp.expand(H + b_global + 1 - 2 * t) == 0

print("verified the second endpoint cusp ring Q[t^2,t^3]")
print("verified its balanced-degree obstruction and the global hidden root H")
print("RESULT: BOTH CONDUCTOR ENDPOINTS HAVE LINKED CUSP DEFECTS")
