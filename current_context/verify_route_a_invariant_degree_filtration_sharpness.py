#!/usr/bin/env python3
"""Exact checks for ROUTE_A_INVARIANT_DEGREE_FILTRATION_SHARPNESS.md."""

import sympy as sp


a, b, z = sp.symbols("a b z")
u = a**2
v = 4 * b * (1 + a**2 * b)
w = a * (1 + 2 * a**2 * b)


def total_degree(poly):
    return sp.Poly(sp.expand(poly), a, b).total_degree()


# The quadratic pseudoplane relation and deck invariance.
assert sp.expand(w**2 - u - u**2 * v) == 0
sigma_a = -a
sigma_b = -b - a**-2
for generator in (u, v, w):
    transformed = sp.cancel(generator.subs({a: sigma_a, b: sigma_b}, simultaneous=True))
    assert sp.cancel(transformed - generator) == 0

# In z=a^2 b coordinates the involution is (a,z) -> (-a,-z-1).
assert sp.expand((sigma_a**2) * sigma_b + z + 1).subs(b, z / a**2) == 0
assert sp.cancel(v.subs(b, z / a**2) - 4 * a**-2 * z * (z + 1)) == 0
assert sp.expand(w.subs(b, z / a**2) - a * (2 * z + 1)) == 0

# Reduced-basis degree and distinct-leading-monomial checks on a finite
# rectangle.  The formulas themselves prove the unrestricted statement.
seen = {}
for i in range(6):
    for j in range(6):
        even_monomial = sp.expand(u**i * v**j)
        odd_monomial = sp.expand(w * u**i * v**j)
        assert total_degree(even_monomial) == 2 * i + 4 * j
        assert total_degree(odd_monomial) == 4 + 2 * i + 4 * j

        even_lead = (2 * i + 2 * j, 2 * j)
        odd_lead = (3 + 2 * i + 2 * j, 1 + 2 * j)
        assert even_lead not in seen
        seen[even_lead] = ("A", i, j)
        assert odd_lead not in seen
        seen[odd_lead] = ("wC", i, j)

# Equality block: a^(-2m)[z(z+1)]^m is exactly (v/4)^m.
for m in range(1, 8):
    equality_block = sp.expand(a ** (-2 * m) * (z * (z + 1)) ** m)
    v_block = sp.expand((v.subs(b, z / a**2) / 4) ** m)
    assert sp.cancel(equality_block - v_block) == 0
    assert total_degree((v / 4) ** m) == 4 * m

# Sharp nodal first-neighborhood model.
H1 = sp.expand(v**2 / 16 - 1 - w)
H2 = sp.expand(v**3 / 64 - v / 4 - sp.Rational(3, 8) * v * w)

gamma1 = sp.expand(H1.subs(a, 0))
gamma2 = sp.expand(H2.subs(a, 0))
assert gamma1 == b**2 - 1
assert sp.expand(gamma2 - b * (b**2 - 1)) == 0
assert (gamma1.subs(b, 1), gamma2.subs(b, 1)) == (0, 0)
assert (gamma1.subs(b, -1), gamma2.subs(b, -1)) == (0, 0)
assert sp.gcd(sp.diff(gamma1, b), sp.diff(gamma2, b)) == 1

rho1 = sp.Integer(-1)
rho2 = -sp.Rational(3, 2) * b
boundary_bezout = sp.expand(rho1 * sp.diff(gamma2, b) - sp.diff(gamma1, b) * rho2)
assert boundary_bezout == 1

J = sp.factor(
    sp.diff(H1, a) * sp.diff(H2, b)
    - sp.diff(H1, b) * sp.diff(H2, a)
)
expected_J = sp.factor(
    sp.Rational(1, 2)
    * (6 * a**3 * b + 3 * a + 2)
    * (8 * a**4 * b**2 + 8 * a**2 * b + 1)
)
assert sp.expand(J - expected_J) == 0
assert sp.expand(J.subs(a, 0)) == 1
assert total_degree(H1) == 8
assert total_degree(H2) == 12

# Extract and compare top homogeneous forms.
def homogeneous_part(poly, degree):
    expanded = sp.Poly(sp.expand(poly), a, b)
    return sp.Add(
        *[
            coefficient * a**powers[0] * b**powers[1]
            for powers, coefficient in expanded.terms()
            if sum(powers) == degree
        ]
    )


H1_top = sp.expand(homogeneous_part(H1, 8))
H2_top = sp.expand(homogeneous_part(H2, 12))
assert H1_top == a**4 * b**4
assert H2_top == a**6 * b**6
assert sp.expand(H1_top**3 - H2_top**2) == 0

# Cubic elimination over C(v,w): with r=v/4 and target x,y,
# x=r^2-1-w and y=r(r^2-1)-(3/2)rw.
r, x, y = sp.symbols("r x y")
w_from_x = r**2 - 1 - x
y_expression = sp.expand(r * (r**2 - 1) - sp.Rational(3, 2) * r * w_from_x)
assert sp.expand(2 * y_expression - (-r**3 + (1 + 3 * x) * r)) == 0
assert sp.expand(r**3 - (1 + 3 * x) * r + 2 * y) != 0

print("route A invariant degree-filtration sharpness checks passed")
