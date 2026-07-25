#!/usr/bin/env python3
"""Exact elimination for NO_ELEMENTARY_COORDINATE_PULLBACK.md."""

import sympy as sp


x, y, z = sp.symbols("x y z")
A, B, C, T, lam = sp.symbols("A B C T lam")
HA, HB, HC = sp.symbols("HA HB HC")

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

expected = {
    x: (
        (sp.Rational(-16, 63), sp.Rational(-1, 63), sp.Rational(-17, 126)),
        sp.Rational(247, 147),
    ),
    y: (
        (sp.Rational(6, 47), sp.Rational(-1, 47), sp.Rational(-4, 47)),
        sp.Rational(-474, 2209),
    ),
    z: (
        (sp.Integer(1), sp.Rational(-1, 2), sp.Rational(-1, 8)),
        sp.Integer(-6),
    ),
}

specialization = {A: 0, B: 1, C: 0, lam: 1}

for variable in (x, y, z):
    column = [
        sp.diff(component, variable).subs(reconstruction)
        for component in source_map
    ]
    equation = sp.together(
        HA * column[0] + HB * column[1] + HC * column[2] - lam
    )
    numerator = sp.fraction(equation)[0]
    remainder = sp.Poly(sp.rem(numerator, minimal, T), T)
    coefficient_equations = [
        remainder.coeff_monomial(T**degree) for degree in range(3)
    ]
    solutions = sp.solve(
        coefficient_equations, (HA, HB, HC), dict=True, simplify=False
    )
    assert len(solutions) == 1
    forced = solutions[0]
    gradient_value = tuple(
        sp.factor(forced[partial].subs(specialization))
        for partial in (HA, HB, HC)
    )
    curl = sp.factor(sp.diff(forced[HA], B) - sp.diff(forced[HB], A))
    curl_value = sp.factor(curl.subs(specialization))
    assert gradient_value == expected[variable][0]
    assert curl_value == expected[variable][1]
    assert curl_value != 0
    print(
        f"verified: {variable}-elementary pullback has "
        f"nonzero exact curl {curl_value}"
    )

print("all elementary-pullback checks passed")
