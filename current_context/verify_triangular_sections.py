#!/usr/bin/env python3
"""Exact checks for TRIANGULAR_SECTION_NO_GO.md."""

import sympy as sp


x, y, z, t = sp.symbols("x y z t")
e = 1 + x * y

a = e**3 * z + y**2 * e * (4 + 3 * x * y)
b = y + 3 * x * e**2 * z + 3 * x * y**2 * (4 + 3 * x * y)
c = 2 * x - 3 * x**2 * y - x**3 * z

# Treat t as an independent symbol. Substitution t=h(b,c) preserves the
# polynomial identity for every h.
pulled_graph = sp.expand(2 * a + 2 * t**2 - b * t - c * t**3)
D = e - x * t
R = sp.div(sp.Poly(pulled_graph, z), sp.Poly(D, z))[0].as_expr()
assert sp.expand(pulled_graph - D * R) == 0

expected_R = (
    -t**2 * x**2 * z
    - 3 * t**2 * x * y
    + 2 * t**2
    - t * x**2 * y * z
    - 3 * t * x * y**2
    - t * x * z
    - t * y
    + 2 * x**2 * y**2 * z
    + 6 * x * y**3
    + 4 * x * y * z
    + 8 * y**2
    + 2 * z
)
assert sp.expand(R - expected_R) == 0

points = (
    {x: 0, y: 0, z: sp.Rational(-1, 4)},
    {x: 1, y: sp.Rational(-3, 2), z: sp.Rational(13, 2)},
    {x: -1, y: sp.Rational(3, 2), z: sp.Rational(13, 2)},
)
expected = {
    sp.Rational(1, 2): ((1, 0), (-1, 0), (0, 2)),
    sp.Rational(-1, 2): ((1, 0), (0, 2), (-1, 0)),
}
for t_value, pairs in expected.items():
    for point, (d_value, r_value) in zip(points, pairs):
        substitution = dict(point)
        substitution[t] = t_value
        assert sp.simplify(D.subs(substitution)) == d_value
        assert sp.simplify(R.subs(substitution)) == r_value

# Verify directly that the target graph makes s=c*t a root of the quotient
# cubic after a=t^2-b*t/2-c*t^3/2.
B, C, s = sp.symbols("B C s")
A_on_graph = C * t**3 / 2 - t**2 + B * t / 2
cubic = s**3 - 2 * s**2 + B * C * s - 2 * A_on_graph * C**2
assert sp.expand(cubic.subs(s, C * t)) == 0

print("verified: universal triangular-section factorization")
print("verified: residual factor R_t")
print("verified: collision distribution for t(0,0)=+/-1/2")
print("verified: s=C*t is a root of the quotient cubic")
print("all triangular-section checks passed")
