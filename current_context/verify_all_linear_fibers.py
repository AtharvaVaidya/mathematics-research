#!/usr/bin/env python3
"""Exact algebra checks for ALL_LINEAR_FIBERS_NO_GO.md."""

import sympy as sp


x, y, z = sp.symbols("x y z")
alpha, beta, gamma, tau = sp.symbols("alpha beta gamma tau")
e = 1 + x * y

a = e**3 * z + y**2 * e * (4 + 3 * x * y)
b = y + 3 * x * e**2 * z + 3 * x * y**2 * (4 + 3 * x * y)
c = 2 * x - 3 * x**2 * y - x**3 * z

A = alpha * e**3 + 3 * beta * x * e**2 - gamma * x**3
C = (
    alpha * y**2 * e * (4 + 3 * x * y)
    + beta * (y + 3 * x * y**2 * (4 + 3 * x * y))
    + gamma * (2 * x - 3 * x**2 * y)
    - tau
)

assert sp.expand(alpha * a + beta * b + gamma * c - tau - (A * z + C)) == 0
print("verified: arbitrary linear fiber equation")

r = sp.symbols("r")
assert sp.expand(
    A.subs(e, r * x) - x**3 * (alpha * r**3 + 3 * beta * r**2 - gamma)
) == 0
print("verified: alpha-nonzero divisor factorization")

B = 3 * beta * e**2 - gamma * x**2
assert sp.expand(A.subs(alpha, 0) - x * B) == 0
assert sp.expand(C.subs({alpha: 0, x: 0}) - (beta * y - tau)) == 0
print("verified: unique moving center on x=0")

t = sp.symbols("t", nonzero=True)
z_on_c_level = (2 - 3 * x * y - t / x) / x**2
assert sp.factor(c.subs(z, z_on_c_level) - t) == 0
assert sp.expand(a.subs(x, 0) - (z + 4 * y**2)) == 0
assert sp.expand(b.subs(x, 0) - y) == 0
print("verified: c-level parametrization and flat triangular component")

print("all arbitrary-linear-fiber algebra checks passed")
