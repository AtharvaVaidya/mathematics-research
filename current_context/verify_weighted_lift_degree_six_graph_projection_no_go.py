#!/usr/bin/env python3
"""Exact audit of the degree-six weighted-lift graph/projection no-go."""

from __future__ import annotations

import sympy as sp


x, y, z, w = sp.symbols("x y z w")


def jacobian(first: sp.Expr, second: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(first, x) * sp.diff(second, y)
        - sp.diff(first, y) * sp.diff(second, x)
    )


def build_seed() -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Rational]:
    roots = (0, -1, 3, 4, 5, -4)
    root_polynomial = sp.expand(sp.prod(w - root for root in roots))
    expected_root_polynomial = (
        w**6
        - 7 * w**5
        - 9 * w**4
        + 127 * w**3
        - 112 * w**2
        - 240 * w
    )
    assert root_polynomial == expected_root_polynomial

    normalization = (
        sp.diff(root_polynomial, w).subs(w, 0)
        - sp.diff(root_polynomial, w).subs(w, 1)
    )
    assert normalization == -92
    H = sp.expand(root_polynomial / normalization)
    H_prime_at_zero = sp.diff(H, w).subs(w, 0)
    assert H_prime_at_zero == sp.Rational(60, 23)

    p = sp.expand(sp.diff(H, w) - H_prime_at_zero)
    q = sp.expand(w * sp.diff(H, w) - H)
    expected_p = (
        -sp.Rational(3, 46) * w**5
        + sp.Rational(35, 92) * w**4
        + sp.Rational(9, 23) * w**3
        - sp.Rational(381, 92) * w**2
        + sp.Rational(56, 23) * w
    )
    expected_q = (
        -sp.Rational(5, 92) * w**6
        + sp.Rational(7, 23) * w**5
        + sp.Rational(27, 92) * w**4
        - sp.Rational(127, 46) * w**3
        + sp.Rational(28, 23) * w**2
    )
    assert p == expected_p
    assert q == expected_q
    assert sp.diff(q, w) == sp.expand(w * sp.diff(p, w))
    assert p.subs(w, 0) == 0
    assert p.subs(w, 1) == -1
    assert sp.integrate(p, (w, 0, 1)) == 0

    kappa = sp.diff(H, w, 2).subs(w, 1)
    a = sp.factor(-(1 + kappa) / (2 + kappa))
    assert kappa == -sp.Rational(80, 23)
    assert a == -sp.Rational(57, 34)
    return H, p, q, a


def build_map(
    p: sp.Expr, q: sp.Expr, a: sp.Rational
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    u = 1 + x * y
    gamma = 1 + a * x * y + x**2 * z
    hidden_w = sp.expand(u * gamma)
    alpha = sp.expand(u + q.subs(w, hidden_w) / gamma**2)
    beta = sp.expand(1 + p.subs(w, hidden_w) / gamma)
    A = sp.cancel(alpha / x**2)
    B = sp.cancel(beta / x)
    C = sp.expand(x * gamma)
    assert sp.denom(A) == 1
    assert sp.denom(B) == 1
    A, B = sp.expand(A), sp.expand(B)
    assert tuple(
        sp.Poly(component, x, y, z).total_degree()
        for component in (A, B, C)
    ) == (22, 21, 4)

    determinant = sp.factor(
        sp.det(
            sp.Matrix(
                [
                    [
                        sp.diff(component, variable)
                        for variable in (x, y, z)
                    ]
                    for component in (A, B, C)
                ]
            )
        )
    )
    assert determinant == 1
    return A, B, C


def verify_six_point_fiber(
    H: sp.Expr,
    a: sp.Rational,
    components: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> None:
    roots = (0, -1, 3, 4, 5, -4)
    target = (0, -sp.Rational(60, 23), 1)
    points: list[tuple[sp.Expr, sp.Expr, sp.Expr]] = []
    for root in roots:
        gamma = -sp.diff(H, w).subs(w, root)
        source_x = sp.factor(1 / gamma)
        source_y = sp.factor(sp.Rational(root) - gamma)
        source_v = sp.factor(source_x * source_y)
        source_z = sp.factor(
            (gamma - 1 - a * source_v) * gamma**2
        )
        point = (source_x, source_y, source_z)
        image = tuple(
            sp.factor(
                component.subs(dict(zip((x, y, z), point, strict=True)))
            )
            for component in components
        )
        assert image == target
        points.append(point)

    assert len(set(points)) == 6
    assert len({point[0] for point in points}) == 6
    assert len({point[2] for point in points}) == 6

    # Since all x-coordinates are distinct, a univariate polynomial graph
    # contains the entire six-point collision fiber.
    collision_graph = sp.interpolate(
        [(point[0], point[2]) for point in points],
        x,
    )
    assert sp.degree(collision_graph, x) <= 5
    for source_x, _source_y, source_z in points:
        assert sp.factor(collision_graph.subs(x, source_x) - source_z) == 0


def verify_projection_sign_convention() -> None:
    ua, ub, uc, va, vb, vc = sp.symbols("ua ub uc va vb vc")
    Ag = sp.Function("Ag")(x, y)
    Bg = sp.Function("Bg")(x, y)
    Cg = sp.Function("Cg")(x, y)
    first = ua * Ag + ub * Bg + uc * Cg
    second = va * Ag + vb * Bg + vc * Cg
    lambda_a = ub * vc - uc * vb
    lambda_b = uc * va - ua * vc
    lambda_c = ua * vb - ub * va
    expected = (
        lambda_a * jacobian(Bg, Cg)
        + lambda_b * jacobian(Cg, Ag)
        + lambda_c * jacobian(Ag, Bg)
    )
    assert sp.expand(jacobian(first, second) - expected) == 0


def verify_top_form_identities() -> None:
    d = 5
    r = d - 1
    p_lead = -sp.Rational(3, 46)
    q_lead = -sp.Rational(5, 92)

    graph_top = sp.Function("graph_top")(x, y)
    C_top = x**3 * graph_top
    B_top = p_lead * y**d * C_top**r
    A_top = q_lead * y ** (d + 1) * C_top**r

    assert sp.expand(
        jacobian(A_top, B_top)
        + (q_lead / p_lead) * B_top * sp.diff(B_top, x)
    ) == 0
    assert sp.expand(
        jacobian(C_top, A_top)
        - q_lead
        * (d + 1)
        * y**d
        * C_top**r
        * sp.diff(C_top, x)
    ) == 0
    assert sp.expand(
        jacobian(B_top, C_top)
        + p_lead
        * d
        * y ** (d - 1)
        * C_top**r
        * sp.diff(C_top, x)
    ) == 0

    m = sp.symbols("m", integer=True, positive=True)
    degree_AB = 8 * d - 7 + 2 * (d - 1) * m
    degree_CA = 4 * d - 1 + d * m
    degree_BC = 4 * d - 2 + d * m
    assert sp.simplify(degree_AB - degree_CA) == 14 + 3 * m
    assert sp.simplify(degree_CA - degree_BC) == 1

    # Constant graphs use C_top=x^2(a*y+z0*x); the same identities hold.
    z0 = sp.symbols("z0")
    a = -sp.Rational(57, 34)
    constant_C_top = x**2 * (a * y + z0 * x)
    constant_B_top = p_lead * y**d * constant_C_top**r
    constant_A_top = q_lead * y ** (d + 1) * constant_C_top**r
    assert sp.expand(
        sp.diff(constant_C_top, x)
        - (2 * a * x * y + 3 * z0 * x**2)
    ) == 0
    assert sp.expand(
        jacobian(constant_A_top, constant_B_top)
        + (q_lead / p_lead)
        * constant_B_top
        * sp.diff(constant_B_top, x)
    ) == 0
    assert sp.expand(
        jacobian(constant_C_top, constant_A_top)
        - q_lead
        * (d + 1)
        * y**d
        * constant_C_top**r
        * sp.diff(constant_C_top, x)
    ) == 0
    assert sp.expand(
        jacobian(constant_B_top, constant_C_top)
        + p_lead
        * d
        * y ** (d - 1)
        * constant_C_top**r
        * sp.diff(constant_C_top, x)
    ) == 0


def main() -> None:
    H, p, q, a = build_seed()
    components = build_map(p, q, a)
    verify_six_point_fiber(H, a, components)
    verify_projection_sign_convention()
    verify_top_form_identities()
    print("verified: exact degree-five seed and a=-57/34")
    print("verified: the weighted lift is polynomial with degrees (22,21,4)")
    print("verified: the three-dimensional Jacobian is 1")
    print("verified: six exact rational preimages share one target")
    print("verified: one polynomial graph contains all six preimages")
    print("verified: linear-projection sign convention")
    print("verified: separated nonzero highest-Jacobian identities")
    print("RESULT: no polynomial graph plus linear projection is plane Keller")


if __name__ == "__main__":
    main()
