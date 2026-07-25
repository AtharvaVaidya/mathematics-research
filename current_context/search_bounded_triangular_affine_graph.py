#!/usr/bin/env python3
"""Exact bounded triangular-target / affine-graph search for the 3D map.

For each triangular target orientation through (-1/4,0,0), this searches
every polynomial g through the stated degree bounds and every affine graph z=phi(x,y)
through the collision pair

    (0,0,-1/4), (1,-3/2,13/2).

The graph is required to be a component of the target-coordinate fiber and
to have nonzero constant normal derivative.  Either a solution would be an
explicit plane Keller counterexample carrying the known collision, or the
saturated coefficient ideal is [1].
"""

import sympy as sp


x, y, z = sp.symbols("x y z")
A, B, C = sp.symbols("A B C")

a = (1 + x * y) ** 3 * z + y**2 * (1 + x * y) * (4 + 3 * x * y)
b = y + 3 * x * (1 + x * y) ** 2 * z + 3 * x * y**2 * (4 + 3 * x * y)
c = 2 * x - 3 * x**2 * y - x**3 * z
U = A + sp.Rational(1, 4)

slope_y = sp.symbols("slope_y")
phi = (
    -sp.Rational(1, 4)
    + (sp.Rational(27, 4) + sp.Rational(3, 2) * slope_y) * x
    + slope_y * y
)


def orientation_basis(
    main_component: sp.Expr,
    first_other: sp.Expr,
    second_other: sp.Expr,
    prefix: str,
    degree_bound: int,
) -> tuple[int, sp.GroebnerBasis]:
    monomials = tuple(
        first_other**first_degree * second_other**second_degree
        for total_degree in range(1, degree_bound + 1)
        for first_degree in range(total_degree, -1, -1)
        for second_degree in (total_degree - first_degree,)
    )
    coefficients = sp.symbols(f"{prefix}0:{len(monomials)}")
    normal_value, saturation = sp.symbols(
        f"{prefix}_normal {prefix}_saturation"
    )
    target_coordinate = sp.expand(
        main_component
        + sum(
            coefficient * monomial
            for coefficient, monomial in zip(coefficients, monomials)
        )
    )
    source_coordinate = sp.expand(
        target_coordinate.subs({A: a, B: b, C: c})
    )
    graph_zero = sp.Poly(
        sp.expand(source_coordinate.subs(z, phi)), x, y
    )
    graph_normal = sp.Poly(
        sp.expand(
            sp.diff(source_coordinate, z).subs(z, phi) - normal_value
        ),
        x,
        y,
    )
    equations = [
        coefficient
        for coefficient in graph_zero.coeffs() + graph_normal.coeffs()
        if coefficient != 0
    ]
    variables = (
        *reversed(coefficients),
        normal_value,
        slope_y,
        saturation,
    )
    basis = sp.groebner(
        equations + [1 - saturation * normal_value],
        *variables,
        order="grevlex",
        method="f5b",
    )
    return len(equations), basis


for degree_bound in (3, 4):
    orientations = {
        "A+g(B,C)": orientation_basis(
            U, B, C, f"d{degree_bound}a", degree_bound
        ),
        "B+g(A+1/4,C)": orientation_basis(
            B, U, C, f"d{degree_bound}b", degree_bound
        ),
        "C+g(A+1/4,B)": orientation_basis(
            C, U, B, f"d{degree_bound}c", degree_bound
        ),
    }

    for name, (row_count, basis) in orientations.items():
        assert len(basis.polys) == 1 and basis.polys[0].as_expr() == 1
        print(
            f"degree<={degree_bound}",
            name,
            "rows",
            row_count,
            "saturated Groebner basis [1]",
        )

print(
    "verified through target degree 4: no triangular target coordinate has an affine graph "
    "through the selected collision pair with constant nonzero normal derivative"
)
