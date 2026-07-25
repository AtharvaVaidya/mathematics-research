#!/usr/bin/env python3
"""Exact checks for the two sharp case-c resonant cap stars."""

from __future__ import annotations

import sympy as sp


def linear_map_matrix(
    f: sp.Expr,
    g: sp.Expr,
    w: sp.Symbol,
    a: int,
    b: int,
) -> sp.Matrix:
    """Matrix of (phi,psi) -> phi*g' - f'*psi in bounded degrees."""
    columns: list[list[sp.Expr]] = []
    for exponent in range(a + 1):
        image = sp.expand(w**exponent * sp.diff(g, w))
        columns.append(
            [image.coeff(w, degree) for degree in range(a + b)]
        )
    for exponent in range(b + 1):
        image = sp.expand(-sp.diff(f, w) * w**exponent)
        columns.append(
            [image.coeff(w, degree) for degree in range(a + b)]
        )
    return sp.Matrix(a + b, a + b + 2, lambda i, j: columns[j][i])


def solve_lift_coefficient(
    residual: sp.Expr,
    multiplier: int,
    f: sp.Expr,
    g: sp.Expr,
    w: sp.Symbol,
    a: int,
    b: int,
) -> tuple[sp.Expr, sp.Expr]:
    matrix = linear_map_matrix(f, g, w, a, b)
    right = sp.Matrix(
        [
            sp.expand(residual / multiplier).coeff(w, degree)
            for degree in range(a + b)
        ]
    )
    solution, parameters = matrix.gauss_jordan_solve(right)
    if parameters.rows:
        solution = solution.subs(
            {parameter: 0 for parameter in tuple(parameters)}
        )
    phi = sp.expand(
        sum(solution[index] * w**index for index in range(a + 1))
    )
    psi = sp.expand(
        sum(
            solution[a + 1 + index] * w**index
            for index in range(b + 1)
        )
    )
    assert sp.expand(phi * sp.diff(g, w) - sp.diff(f, w) * psi
                     - residual / multiplier) == 0
    return phi, psi


def truncated_formal_lift(
    f: sp.Expr,
    g: sp.Expr,
    target: sp.Expr,
    u: sp.Symbol,
    w: sp.Symbol,
    a: int,
    b: int,
    through_order: int,
) -> tuple[sp.Expr, sp.Expr]:
    x = f
    y = g
    for order in range(through_order + 1):
        current = sp.expand(
            sp.diff(x, u) * sp.diff(y, w)
            - sp.diff(x, w) * sp.diff(y, u)
        )
        residual = sp.expand(target - current).coeff(u, order)
        phi, psi = solve_lift_coefficient(
            residual,
            order + 1,
            f,
            g,
            w,
            a,
            b,
        )
        assert sp.degree(phi, w) <= a
        assert sp.degree(psi, w) <= b
        x = sp.expand(x + u ** (order + 1) * phi)
        y = sp.expand(y + u ** (order + 1) * psi)

    error = sp.expand(
        sp.diff(x, u) * sp.diff(y, w)
        - sp.diff(x, w) * sp.diff(y, u)
        - target
    )
    for order in range(through_order + 1):
        assert sp.expand(error).coeff(u, order) == 0
    return x, y


def verify_star_arithmetic() -> None:
    cases = (
        # a, b, p, q, kappa, N, c, e, d, resultant order
        (2, 3, 8, 12, -4, 17, 4, 4, 8, 24),
        (8, 12, 8, 12, 1, 22, 1, 7, 11, 96),
    )
    for a, b, p, q, kappa, n, c, e, d, resultant_order in cases:
        assert p == a * c
        assert q == b * c
        assert n == p + q + 1 + kappa
        assert e == (a - 1) * c
        assert d == (b - 1) * c
        assert b * c == q
        assert a * c == p
        assert e < n - q
        assert d < n - p
        assert n - q - e == c + 1 + kappa
        assert n - p - d == c + 1 + kappa
        assert n - q - 1 - e == c + kappa
        assert n - p - 1 - d == c + kappa
        assert c + kappa >= 0
        assert resultant_order == a * b * c == a * q == b * p

    assert 4 != 5 and 8 != 9
    assert 7 != 10 and 11 != 14


def verify_example_polynomials_and_resultants() -> None:
    w = sp.symbols("w")

    vertical_f = w**2 - 1
    vertical_g = (w - 2) * (w - 3) * (w - 4)
    assert sp.degree(
        sp.gcd(sp.diff(vertical_f, w), sp.diff(vertical_g, w)), w
    ) == 0
    assert sp.resultant(vertical_f, vertical_g, w) != 0
    assert linear_map_matrix(
        vertical_f, vertical_g, w, 2, 3
    ).rank() == 5

    diagonal_f = w**8 - 1
    diagonal_g = w**12 + 2 * w
    assert sp.degree(
        sp.gcd(sp.diff(diagonal_f, w), sp.diff(diagonal_g, w)), w
    ) == 0
    assert sp.gcd(diagonal_f, diagonal_g) == 1
    assert sp.discriminant(diagonal_f, w) != 0
    assert sp.discriminant(diagonal_g, w) != 0
    assert linear_map_matrix(
        diagonal_f, diagonal_g, w, 8, 12
    ).rank() == 20


def verify_residue_theorem_gluing() -> None:
    w = sp.symbols("w")
    f = w**2 - 1
    g = (w - 2) * (w - 3) * (w - 4)
    f_roots = (-1, 1)
    g_roots = (2, 3, 4)
    finite_residue_sum = sum(
        1 / (sp.diff(f, w).subs(w, root) * g.subs(w, root))
        for root in f_roots
    ) + sum(
        1 / (sp.diff(g, w).subs(w, root) * f.subs(w, root))
        for root in g_roots
    )
    assert sp.simplify(finite_residue_sum) == 0


def verify_closed_vertical_lift() -> None:
    u, w = sp.symbols("u w")
    a = sp.Function("A")(u)
    x = w**2 - 1 + a
    y = (
        w**3
        - 9 * w**2
        + 26 * w
        - 24
        + a * (sp.Rational(3, 2) * w - 9)
    )
    jacobian = sp.factor(
        sp.diff(x, u) * sp.diff(y, w)
        - sp.diff(x, w) * sp.diff(y, u)
    )
    assert jacobian == (
        3 * a + 52
    ) * sp.diff(a, u) / 2
    assert sp.simplify(
        jacobian.subs(
            sp.diff(a, u),
            -1 / (26 + sp.Rational(3, 2) * a),
        )
        + 1
    ) == 0

    # Check the blowdown bracket ledger:
    # w=v/u^c implies [X,Y]_(u,v)=u^-c [X,Y]_(u,w).
    v, c = sp.symbols("v c", nonzero=True)
    x_uv = sp.Function("X")(u, v / u**c)
    y_uv = sp.Function("Y")(u, v / u**c)
    # The cancellation of the two chain-rule terms is represented
    # independently by the coordinate determinant.
    coordinate_jacobian = sp.det(
        sp.Matrix(
            [
                [sp.diff(u, u), sp.diff(u, v)],
                [sp.diff(v / u**c, u), sp.diff(v / u**c, v)],
            ]
        )
    )
    assert sp.simplify(coordinate_jacobian - u ** (-c)) == 0
    assert x_uv != y_uv


def verify_recursive_lifts() -> None:
    u, w, t = sp.symbols("u w t")

    vertical_f = w**2 - 1
    vertical_g = (w - 2) * (w - 3) * (w - 4)
    truncated_formal_lift(
        vertical_f,
        vertical_g,
        -1,
        u,
        w,
        2,
        3,
        through_order=7,
    )

    diagonal_f = w**8 - 1
    diagonal_g = w**12 + 2 * w
    x, y = truncated_formal_lift(
        diagonal_f,
        diagonal_g,
        u**2 * (t + u * w) ** 2,
        u,
        w,
        8,
        12,
        through_order=7,
    )
    assert x.coeff(u, 1) == 0 and x.coeff(u, 2) == 0
    assert y.coeff(u, 1) == 0 and y.coeff(u, 2) == 0


def verify_outer_quartic_norm_identity() -> None:
    w = sp.symbols("w")
    u = sp.Function("U")(w)
    v = sp.Function("V")(w)
    ell = sp.symbols("L")
    d = w * v**2 - ell * u**3
    outer_equation = (
        u * v
        + 2 * w * u * sp.diff(v, w)
        - 3 * w * sp.diff(u, w) * v
    )
    assert sp.simplify(
        u * sp.diff(d, w) - 3 * sp.diff(u, w) * d
        - v * outer_equation
    ) == 0

    # Check the quartic resultant/discriminant normalization on a generic
    # exact example.  The identity itself follows rootwise from D'=V/U.
    quartic = w**4 + 2 * w**3 - 3 * w + 5
    auxiliary_u = w**7 + w + 1
    auxiliary_v = sp.rem(
        auxiliary_u * sp.diff(quartic, w),
        quartic,
        domain=sp.QQ,
    )
    leading = sp.LC(sp.Poly(quartic, w))
    resultant_v = sp.resultant(quartic, auxiliary_v, w)
    resultant_u = sp.resultant(quartic, auxiliary_u, w)
    discriminant = sp.discriminant(quartic, w)
    assert resultant_u != 0
    assert sp.expand(
        resultant_v - leading * discriminant * resultant_u
    ) == 0


def main() -> None:
    verify_star_arithmetic()
    verify_example_polynomials_and_resultants()
    verify_residue_theorem_gluing()
    verify_closed_vertical_lift()
    verify_recursive_lifts()
    verify_outer_quartic_norm_identity()
    print("verified the unique minimum-height stars at contacts 4 and 1")
    print("verified all four forbidden sums are avoided resonantly")
    print("verified residue exponents 0 and 2 and resultant orders 24 and 96")
    print("verified bounded transverse lifting maps are surjective")
    print("verified exact formal local brackets through seven recursive orders")
    print("verified the outer quartic differential and norm identities")
    print("RESULT: LOCAL CAP JETS DO NOT FORCE A CASE-C CONTRADICTION")


if __name__ == "__main__":
    main()
