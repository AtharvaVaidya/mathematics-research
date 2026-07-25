#!/usr/bin/env python3
"""Exact algebra checks for LINEAR_SECTION_NO_GO.md."""

import sympy as sp


x, y, z = sp.symbols("x y z")
alpha, beta, gamma, r = sp.symbols("alpha beta gamma r")
e = 1 + x * y

a = e**3 * z + y**2 * e * (4 + 3 * x * y)
b = y + 3 * x * e**2 * z + 3 * x * y**2 * (4 + 3 * x * y)
c = 2 * x - 3 * x**2 * y - x**3 * z

section = sp.expand(alpha * a + beta * b + gamma * c + alpha / 4)
A = sp.expand(alpha * e**3 + 3 * beta * x * e**2 - gamma * x**3)
C = sp.expand(
    alpha * y**2 * e * (4 + 3 * x * y)
    + beta * (y + 3 * x * y**2 * (4 + 3 * x * y))
    + gamma * (2 * x - 3 * x**2 * y)
    + alpha / 4
)
assert sp.expand(section - (A * z + C)) == 0

# For alpha != 0, each reduced component A=0 has e=r*x where
# alpha*r^3+3*beta*r^2-gamma=0.
component_substitution = {y: r - 1 / x}
assert sp.factor(A.subs(component_substitution)) == x**3 * (
    alpha * r**3 + 3 * beta * r**2 - gamma
)
assert sp.simplify(e.subs(component_substitution) - r * x) == 0

# For alpha=0, beta!=0, the x=0 component has exactly the center y=0.
assert sp.expand(C.subs({alpha: 0, x: 0}) - beta * y) == 0
assert sp.expand(
    A.subs(alpha, 0) - x * (3 * beta * e**2 - gamma * x**2)
) == 0

# Direct nonconstant unit identity on b=0.
unit_partner = (
    3 * x**3 * y * z
    + 9 * x**2 * y**2
    + 3 * x**2 * z
    + 3 * x * y
    - 2
)
assert sp.expand(e * unit_partner + 2 - x * b) == 0

# The three exact collision points lie in every displayed section.
points = (
    {x: 0, y: 0, z: sp.Rational(-1, 4)},
    {x: 1, y: sp.Rational(-3, 2), z: sp.Rational(13, 2)},
    {x: -1, y: sp.Rational(3, 2), z: sp.Rational(13, 2)},
)
for point in points:
    assert sp.expand(section.subs(point)) == 0

# The c=0 section is reducible.
assert sp.factor(c) == -x * (3 * x * y + x**2 * z - 2)

print("verified: general section equation A*z+C")
print("verified: alpha!=0 divisor components are copies of G_m")
print("verified: alpha=0,beta!=0 line center and divisor factorization")
print("verified: explicit nonconstant unit on b=0")
print("verified: all three collision points lie on every linear section")
print("verified: c=0 section is reducible")
print("all linear-section algebra checks passed")
