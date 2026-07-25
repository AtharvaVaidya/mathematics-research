#!/usr/bin/env python3
"""Exact checks for the July-2026 three-dimensional counterexample.

This file does not claim a plane counterexample.  It verifies the new
three-dimensional construction, its two-dimensional invariant quotient,
and the obstruction to obtaining a plane map by the most direct slice.
"""

from fractions import Fraction

import sympy as sp


x, y, z = sp.symbols("x y z")

a = (1 + x * y) ** 3 * z + y**2 * (1 + x * y) * (4 + 3 * x * y)
b = y + 3 * x * (1 + x * y) ** 2 * z + 3 * x * y**2 * (4 + 3 * x * y)
c = 2 * x - 3 * x**2 * y - x**3 * z

jacobian_3d = sp.factor(
    sp.det(
        sp.Matrix(
            [
                [sp.diff(component, variable) for variable in (x, y, z)]
                for component in (a, b, c)
            ]
        )
    )
)
assert jacobian_3d == -2

collision_points = (
    (Fraction(0), Fraction(0), Fraction(-1, 4)),
    (Fraction(1), Fraction(-3, 2), Fraction(13, 2)),
    (Fraction(-1), Fraction(3, 2), Fraction(13, 2)),
)
collision_images = {
    tuple(
        sp.Rational(value.numerator, value.denominator)
        for value in (
            component.subs(dict(zip((x, y, z), point)))
            for component in (a, b, c)
        )
    )
    for point in collision_points
}
assert collision_images == {(sp.Rational(-1, 4), sp.Integer(0), sp.Integer(0))}

# Quotient by the hyperbolic G_m-action.  Source invariants are
# u=xy and v=x^2 z; target invariants are P=bc and Q=ac^2.
u, v = sp.symbols("u v")
L = 2 - 3 * u - v
M = v * (1 + u) ** 2 + u**2 * (4 + 3 * u)
P = sp.expand(L * (u + 3 * M))
Q = sp.expand(L**2 * (1 + u) * M)
jacobian_quotient = sp.factor(
    sp.det(
        sp.Matrix(
            [
                [sp.diff(P, u), sp.diff(P, v)],
                [sp.diff(Q, u), sp.diff(Q, v)],
            ]
        )
    )
)
assert sp.expand(jacobian_quotient - 2 * L**2) == 0
assert sp.expand(P.subs(v, 2 - 3 * u)) == 0
assert sp.expand(Q.subs(v, 2 - 3 * u)) == 0

# The target slice c=0 has reducible inverse image x*L=0.  On x=0 the
# restriction is the triangular plane automorphism (y,z)->(z+4y^2,y).
assert sp.expand(a.subs(x, 0) - (z + 4 * y**2)) == 0
assert sp.expand(b.subs(x, 0) - y) == 0
assert sp.expand(c.subs(x, 0)) == 0

# The other component L=0 has coordinates (x,u) with x invertible,
# y=u/x and z=(2-3u)/x^2.  Its map to (a,b) is Laurent, not polynomial
# on A^2, and its ordinary coordinate Jacobian is 2/x^4.
a_on_L = (u + 1) * (u + 2) / x**2
b_on_L = (4 * u + 6) / x
jacobian_slice = sp.factor(
    sp.det(
        sp.Matrix(
            [
                [sp.diff(a_on_L, x), sp.diff(a_on_L, u)],
                [sp.diff(b_on_L, x), sp.diff(b_on_L, u)],
            ]
        )
    )
)
assert jacobian_slice == 2 / x**4
direct_substitution = {
    y: u / x,
    z: (2 - 3 * u) / x**2,
}
assert sp.factor(a.subs(direct_substitution) - a_on_L) == 0
assert sp.factor(b.subs(direct_substitution) - b_on_L) == 0
assert sp.factor(c.subs(direct_substitution)) == 0

print("three-dimensional determinant:", jacobian_3d)
print("common collision image:", next(iter(collision_images)))
print("quotient determinant:", jacobian_quotient)
print("L=0 slice determinant in (x,u):", jacobian_slice)
print("all exact checks passed")
