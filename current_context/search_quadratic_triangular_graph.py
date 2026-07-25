#!/usr/bin/env python3
"""Exact search for an affine graph descent of the 3D counterexample.

This checks the most economical unresolved nonlinear descent.  Let

    H(A,B,C) = A + g(B,C)

with g a quadratic having g(0,0)=0, so H=-1/4 contains the verified target
collision.  If the source fiber contains a graph z=phi(x,y), then its
restriction is A^2.  The restricted map to (B,C) is Keller precisely when

    (H o F)(x,y,phi) = -1/4,
    d/dz (H o F)(x,y,phi) = a nonzero constant.

We impose these identities for an affine phi containing the collision pair
(0,0,-1/4),(1,-3/2,13/2), and eliminate every coefficient exactly.
"""

import sympy as sp


x, y, z = sp.symbols("x y z")
A, B, C = sp.symbols("A B C")

a = (1 + x * y) ** 3 * z + y**2 * (1 + x * y) * (4 + 3 * x * y)
b = y + 3 * x * (1 + x * y) ** 2 * z + 3 * x * y**2 * (4 + 3 * x * y)
c = 2 * x - 3 * x**2 * y - x**3 * z

g10, g01, g20, g11, g02 = sp.symbols("g10 g01 g20 g11 g02")
normal_derivative, slope_y = sp.symbols("normal_derivative slope_y")
g = g10 * B + g01 * C + g20 * B**2 + g11 * B * C + g02 * C**2

# The two collision conditions determine the constant and x slope.
phi = (
    -sp.Rational(1, 4)
    + (sp.Rational(27, 4) + sp.Rational(3, 2) * slope_y) * x
    + slope_y * y
)

h = sp.expand(a + g.subs({B: b, C: c}) + sp.Rational(1, 4))

# A graph component with constant restricted Jacobian is much more rigid
# than its degree suggests.  Write h=A2*z^2+A1*z+A0.  If z=phi is a root
# and h_z(phi)=k is constant, then the z-discriminant is identically k^2.
# At x=y=0 we have h=z+1/4, so necessarily k^2=1.
h_as_z = sp.Poly(h, z)
A2, A1, A0 = h_as_z.all_coeffs()
discriminant = sp.Poly(sp.expand(A1**2 - 4 * A2 * A0 - 1), x, y)
discriminant_equations = [
    coefficient for coefficient in discriminant.coeffs() if coefficient != 0
]
discriminant_basis = sp.groebner(
    discriminant_equations,
    g20,
    g11,
    g02,
    g10,
    g01,
    order="grevlex",
    method="f5b",
)
assert (
    len(discriminant_basis.polys) == 1
    and discriminant_basis.polys[0].as_expr() == 1
)


def saturated_constant_discriminant(
    main_component: sp.Expr,
    first_other: sp.Expr,
    second_other: sp.Expr,
    prefix: str,
) -> tuple[int, sp.GroebnerBasis]:
    """Search every quadratic triangular orientation.

    The fiber is normalized to pass through the common target value by
    using the shifted coordinate A+1/4.  Saturation retains only a nonzero
    constant normal derivative.
    """

    linear_first, linear_second, quad_first, mixed, quad_second = sp.symbols(
        f"{prefix}10 {prefix}01 {prefix}20 {prefix}11 {prefix}02"
    )
    saturation = sp.symbols(f"{prefix}_saturation")
    target_coordinate = sp.expand(
        main_component
        + linear_first * first_other
        + linear_second * second_other
        + quad_first * first_other**2
        + mixed * first_other * second_other
        + quad_second * second_other**2
    )
    source_coordinate = sp.expand(
        target_coordinate.subs({A: a, B: b, C: c})
    )
    coefficients_in_z = sp.Poly(source_coordinate, z).all_coeffs()
    if len(coefficients_in_z) == 3:
        leading, middle, constant = coefficients_in_z
        source_discriminant = sp.expand(middle**2 - 4 * leading * constant)
    elif len(coefficients_in_z) == 2:
        middle, _constant = coefficients_in_z
        source_discriminant = sp.expand(middle**2)
    else:
        raise AssertionError("unexpected z-degree in triangular coordinate")

    discriminant_poly = sp.Poly(source_discriminant, x, y)
    constant_value = discriminant_poly.coeff_monomial(1)
    nonconstant_rows = [
        coefficient
        for monomial, coefficient in discriminant_poly.terms()
        if monomial != (0, 0) and coefficient != 0
    ]
    variables_for_basis = (
        quad_first,
        mixed,
        quad_second,
        linear_first,
        linear_second,
        saturation,
    )
    saturated_basis = sp.groebner(
        nonconstant_rows + [1 - saturation * constant_value],
        *variables_for_basis,
        order="grevlex",
        method="f5b",
    )
    return len(nonconstant_rows), saturated_basis


U = A + sp.Rational(1, 4)
orientation_results = {
    "A+g(B,C)": saturated_constant_discriminant(U, B, C, "oa"),
    "B+g(A+1/4,C)": saturated_constant_discriminant(B, U, C, "ob"),
    "C+g(A+1/4,B)": saturated_constant_discriminant(C, U, B, "oc"),
}
for orientation, (_row_count, orientation_basis) in orientation_results.items():
    assert (
        len(orientation_basis.polys) == 1
        and orientation_basis.polys[0].as_expr() == 1
    ), f"unresolved constant-discriminant orientation: {orientation}"


def collision_line_component_basis(
    main_component: sp.Expr,
    first_other: sp.Expr,
    second_other: sp.Expr,
    prefix: str,
) -> tuple[int, sp.GroebnerBasis]:
    """Test the vertical A2 given by y=-3*x/2 through two collision points."""

    linear_first, linear_second, quad_first, mixed, quad_second = sp.symbols(
        f"{prefix}10 {prefix}01 {prefix}20 {prefix}11 {prefix}02"
    )
    normal_value, saturation = sp.symbols(
        f"{prefix}_normal {prefix}_saturation"
    )
    target_coordinate = sp.expand(
        main_component
        + linear_first * first_other
        + linear_second * second_other
        + quad_first * first_other**2
        + mixed * first_other * second_other
        + quad_second * second_other**2
    )
    source_coordinate = sp.expand(
        target_coordinate.subs({A: a, B: b, C: c})
    )
    collision_line = {y: -sp.Rational(3, 2) * x}
    zero_rows = sp.Poly(
        sp.expand(source_coordinate.subs(collision_line)), x, z
    ).coeffs()
    normal_rows = sp.Poly(
        sp.expand(
            sp.diff(source_coordinate, y).subs(collision_line)
            - normal_value
        ),
        x,
        z,
    ).coeffs()
    equations_for_line = [
        coefficient
        for coefficient in zero_rows + normal_rows
        if coefficient != 0
    ]
    variables_for_basis = (
        quad_first,
        mixed,
        quad_second,
        linear_first,
        linear_second,
        normal_value,
        saturation,
    )
    line_basis = sp.groebner(
        equations_for_line + [1 - saturation * normal_value],
        *variables_for_basis,
        order="grevlex",
        method="f5b",
    )
    return len(equations_for_line), line_basis


line_results = {
    "A+g(B,C)": collision_line_component_basis(U, B, C, "la"),
    "B+g(A+1/4,C)": collision_line_component_basis(B, U, C, "lb"),
    "C+g(A+1/4,B)": collision_line_component_basis(C, U, B, "lc"),
}
for orientation, (_row_count, line_basis) in line_results.items():
    assert (
        len(line_basis.polys) == 1 and line_basis.polys[0].as_expr() == 1
    ), f"unresolved collision-line component: {orientation}"

h_on_graph = sp.Poly(sp.expand(h.subs(z, phi)), x, y)
normal_on_graph = sp.Poly(
    sp.expand(sp.diff(h, z).subs(z, phi) - normal_derivative), x, y
)
equations = [
    coefficient
    for coefficient in h_on_graph.coeffs() + normal_on_graph.coeffs()
    if coefficient != 0
]

variables = (
    g20,
    g11,
    g02,
    g10,
    g01,
    normal_derivative,
    slope_y,
)
basis = sp.groebner(equations, *variables, order="grevlex", method="f5b")
assert len(basis.polys) == 1 and basis.polys[0].as_expr() == 1

print("affine graph / quadratic triangular target equations:", len(equations))
print("exact Groebner basis: [1]")
print(
    "universal constant-discriminant equations:",
    len(discriminant_equations),
    "with exact Groebner basis [1]",
)
print(
    "all three quadratic triangular orientations have saturated "
    "constant-discriminant basis [1]"
)
print(
    "the vertical collision line y=-3*x/2 is excluded in all three "
    "orientations by saturated basis [1]"
)
print(
    "verified: no polynomial graph component can have constant normal "
    "derivative for any quadratic triangular target coordinate"
)
