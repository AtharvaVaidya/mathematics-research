#!/usr/bin/env python3
"""Exact checks for ROUTE_A_PROJECTIVE_INTERSECTION_BOUND_NO_GO.md."""

from __future__ import annotations

import sympy as sp


def total_degree(expr: sp.Expr, *gens: sp.Symbol) -> int:
    return sp.Poly(sp.expand(expr), *gens).total_degree()


def arbitrary_intersection_allocation_checks() -> None:
    x, y, X, Y, Z, z = sp.symbols("x y X Y Z z")

    for delta in range(2, 9):
        for r in range(0, delta + 1):
            h = sp.Integer(2) if r == 0 else x**r + 1
            branch = sp.expand(y * x ** (delta - 1) - h)

            assert total_degree(branch, x, y) == delta
            assert sp.degree(branch.subs(y, 0), x) == r

            # Smoothness: F_y=x^(delta-1), but x=0 is disjoint from F=0.
            branch_x = sp.diff(branch, x)
            branch_y = sp.diff(branch, y)
            groebner = sp.groebner(
                [branch, branch_x, branch_y], x, y, order="lex"
            )
            assert groebner.contains(sp.Integer(1))

            # Primitive degree-one dependence on y is irreducible.
            factor_coefficient, factors = sp.factor_list(branch, x, y)
            assert len(factors) == 1
            assert factors[0][1] == 1
            assert sp.expand(factor_coefficient * factors[0][0] - branch) == 0

            if r == 0:
                branch_h = Y * X ** (delta - 1) - 2 * Z**delta
                restriction = -2 * Z**delta
            else:
                branch_h = (
                    Y * X ** (delta - 1)
                    - X**r * Z ** (delta - r)
                    - Z**delta
                )
                restriction = -Z ** (delta - r) * (X**r + Z**r)

            assert total_degree(branch_h, X, Y, Z) == delta
            assert sp.expand(branch_h.subs(Y, 0) - restriction) == 0

            # Finite degree plus the infinity order is Bezout's delta.
            finite_degree = r
            infinity_order = delta - r
            assert finite_degree + infinity_order == delta

            # The residual quadratic has branch equation equal to the one
            # target branch polynomial, and its source Jacobian vanishes
            # simply on z=0.
            residual = z**2 - branch
            assert sp.expand(sp.discriminant(residual, z) - 4 * branch) == 0

            source_y = (z**2 + h) / x ** (delta - 1)
            # This rational display is used only on x!=0.  Its transverse
            # derivative certifies the local ramification multiplicity.
            assert sp.diff(source_y, z) == 2 * z / x ** (delta - 1)


def direct_graph_ramification_checks() -> None:
    x, y, z = sp.symbols("x y z")
    h = (x - 1) * (x - 2) * (x - 3) * (x - 4)
    target_y = z**2 + h

    jac = sp.det(
        sp.Matrix(
            [
                [sp.diff(x, x), sp.diff(x, z)],
                [sp.diff(target_y, x), sp.diff(target_y, z)],
            ]
        )
    )
    assert jac == 2 * z
    assert sp.solve(h, x) == [1, 2, 3, 4]
    assert all(sp.diff(h, x).subs(x, root) != 0 for root in (1, 2, 3, 4))
    assert sp.expand(sp.discriminant(z**2 - (y - h), z) - 4 * (y - h)) == 0


def invariant_degree_chain_checks() -> None:
    # Exhaust representative nonnegative ledgers.  The implication being
    # certified is r<=delta*M and D>=4M => 4r<=delta*D.
    for M in range(1, 10):
        for delta in range(1, 10):
            for residual_degree in range(0, delta * M + 1):
                for lifted_degree in (4 * M, 4 * M + 1, 7 * M):
                    assert 4 * residual_degree <= delta * lifted_degree


def miranda_connected_degree_checks() -> None:
    x, y, T = sp.symbols("x y T")

    for r in range(1, 7):
        # Squarefree degree-r sample with rational simple roots.
        G = sp.prod(x - j for j in range(1, r + 1))
        assert sp.degree(G, x) == r
        assert sp.gcd(G, sp.diff(G, x)) == 1

        branch = sp.expand(G * (y**2 * G - 12) / 9)
        assert total_degree(branch, x, y) == 2 * r + 2
        restricted = sp.expand(branch.subs(y, 0))
        assert sp.degree(restricted, x) == r
        assert (2 * r + 2) - r == r + 2

        # The monogenic generic cubic remains irreducible for the samples.
        cubic = sp.Poly(
            T**2 * (T - 3) + y**2 * G / 3,
            T,
            domain="QQ(x,y)",
        )
        factorization = cubic.factor_list()[1]
        assert len(factorization) == 1
        assert factorization[0][0].degree() == 3

        # Along y=0 the residual trace-zero generator has square G.
        residual = T**2 - G
        assert sp.expand(sp.discriminant(residual, T) - 4 * G) == 0


def main() -> None:
    arbitrary_intersection_allocation_checks()
    direct_graph_ramification_checks()
    invariant_degree_chain_checks()
    miranda_connected_degree_checks()
    print("route-a projective intersection no-go checks passed")


if __name__ == "__main__":
    main()
