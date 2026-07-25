#!/usr/bin/env python3
"""Exact projective certificate for NO_CONSTANT_DIRECTION_PULLBACK.md."""

import sympy as sp


x, y, z = sp.symbols("x y z")
A, B, C, T = sp.symbols("A B C T")
HA, HB, HC = sp.symbols("HA HB HC")
alpha, beta, gamma = sp.symbols("alpha beta gamma")

e = 1 + x * y
source_map = (
    e**3 * z + y**2 * e * (4 + 3 * x * y),
    y + 3 * x * e**2 * z + 3 * x * y**2 * (4 + 3 * x * y),
    2 * x - 3 * x**2 * y - x**3 * z,
)

minimal = C * T**3 - 2 * T**2 + B * T - 2 * A
r = sp.diff(minimal, T)
reconstruction = {
    x: 2 / r,
    y: T - r / 2,
    z: sp.Rational(5, 4) * r**2 - sp.Rational(3, 2) * T * r - C * r**3 / 8,
}

columns = [
    [
        sp.diff(component, variable).subs(reconstruction)
        for component in source_map
    ]
    for variable in (x, y, z)
]
directional_column = [
    alpha * columns[0][index]
    + beta * columns[1][index]
    + gamma * columns[2][index]
    for index in range(3)
]

chain_equation = sp.together(
    HA * directional_column[0]
    + HB * directional_column[1]
    + HC * directional_column[2]
    - 1
)
numerator = sp.fraction(chain_equation)[0]
remainder = sp.Poly(sp.rem(numerator, minimal, T), T)
equations = [
    remainder.coeff_monomial(T**degree) for degree in range(3)
]
matrix, rhs = sp.linear_eq_to_matrix(equations, (HA, HB, HC))

determinant = matrix.det()
adjugate_rhs = matrix.adjugate() * rhs
curl_numerator_rational = (
    sp.diff(adjugate_rhs[0], B) * determinant
    - adjugate_rhs[0] * sp.diff(determinant, B)
    - sp.diff(adjugate_rhs[1], A) * determinant
    + adjugate_rhs[1] * sp.diff(determinant, A)
)
curl_numerator = sp.together(curl_numerator_rational).as_numer_denom()[0]

target_points = ((-2, 1, -2), (-2, 1, -1), (-2, 1, 1))
quintics = []
for target_point in target_points:
    specialized = curl_numerator.subs(dict(zip((A, B, C), target_point)))
    polynomial = sp.Poly(specialized, alpha, beta, gamma)
    primitive = polynomial.primitive()[1]
    assert primitive.total_degree() == 5
    assert len(primitive.terms()) == 21
    quintics.append(primitive.as_expr())
    print(
        f"verified: target {target_point} gives "
        "a 21-term homogeneous quintic"
    )

for chart_variable in (alpha, beta, gamma):
    other_variables = tuple(
        variable
        for variable in (alpha, beta, gamma)
        if variable != chart_variable
    )
    chart_equations = [
        polynomial.subs(chart_variable, 1) for polynomial in quintics
    ]
    basis = sp.groebner(
        chart_equations, *other_variables, order="grevlex", method="f5b"
    )
    assert len(basis.polys) == 1
    assert basis.polys[0].as_expr() == 1
    print(f"verified: projective chart {chart_variable}=1 has basis [1]")

print("all constant-direction pullback checks passed")
