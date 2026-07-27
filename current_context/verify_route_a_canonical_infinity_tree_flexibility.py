#!/usr/bin/env python3
"""Exact checks for ROUTE_A_CANONICAL_INFINITY_TREE_FLEXIBILITY.md."""

from __future__ import annotations

from math import gcd

import sympy as sp


def order_at_zero(expr: sp.Expr, t: sp.Symbol) -> int:
    expr = sp.cancel(expr)
    numerator, denominator = sp.fraction(expr)
    p_num = sp.Poly(sp.expand(numerator), t)
    p_den = sp.Poly(sp.expand(denominator), t)
    num_order = min(monomial[0] for monomial, coeff in p_num.terms() if coeff)
    den_order = min(monomial[0] for monomial, coeff in p_den.terms() if coeff)
    return num_order - den_order


def fixed_arm_checks() -> None:
    t, c = sp.symbols("t c")

    charts = {
        "B_infty": (c, t),
        "E1": (t, t * c),
        "E2": (t, t**2 * c),
        "E3": (t, -t**2 + t**3 * c),
        "D_minus": (t, -t**2 + t**4 * c),
    }
    expected_form_orders = {
        "B_infty": -2,
        "E1": -1,
        "E2": -2,
        "E3": -1,
        "D_minus": 0,
    }
    expected_generator_orders = {
        "B_infty": (0, -2, -1),
        "E1": (2, -1, 1),
        "E2": (2, -2, 1),
        "E3": (2, -1, 1),
        "D_minus": (2, 0, 1),
    }

    # Substitute a non-special generic value after differentiating in c.
    generic_value = sp.Rational(2, 3)
    for name, (a, s) in charts.items():
        jac = sp.det(
            sp.Matrix(
                [
                    [sp.diff(a, t), sp.diff(a, c)],
                    [sp.diff(s, t), sp.diff(s, c)],
                ]
            )
        )
        volume_coefficient = sp.cancel(-jac / s**2)
        form_order = order_at_zero(volume_coefficient.subs(c, generic_value), t)
        assert form_order == expected_form_orders[name]

        u = a**2
        v = sp.cancel(4 * (s + a**2) / s**2)
        w = sp.cancel(a * (s + 2 * a**2) / s)
        orders = tuple(
            order_at_zero(expr.subs(c, generic_value), t)
            for expr in (u, v, w)
        )
        assert orders == expected_generator_orders[name]

    canonical_labels = tuple(
        1 + expected_form_orders[name] for name in charts
    )
    assert canonical_labels == (-1, 0, -1, 0, 1)


def graph_and_self_intersection_checks() -> None:
    weights = {"B": 0}
    edges: set[frozenset[str]] = set()

    # Blow up a smooth point of B.
    weights["B"] -= 1
    weights["E1"] = -1
    edges.add(frozenset(("B", "E1")))

    # Blow up B intersect E1 and insert E2.
    edges.remove(frozenset(("B", "E1")))
    weights["B"] -= 1
    weights["E1"] -= 1
    weights["E2"] = -1
    edges.add(frozenset(("B", "E2")))
    edges.add(frozenset(("E2", "E1")))

    # Blow up a smooth point of E2.
    weights["E2"] -= 1
    weights["E3"] = -1
    edges.add(frozenset(("E2", "E3")))

    # Blow up a smooth point of E3 and call the result D_minus.
    weights["E3"] -= 1
    weights["D_minus"] = -1
    edges.add(frozenset(("E3", "D_minus")))

    assert weights == {
        "B": -2,
        "E1": -2,
        "E2": -2,
        "E3": -2,
        "D_minus": -1,
    }
    assert edges == {
        frozenset(("B", "E2")),
        frozenset(("E2", "E1")),
        frozenset(("E2", "E3")),
        frozenset(("E3", "D_minus")),
    }


def key_polynomial_and_dicritical_parameter_checks() -> None:
    t, eta = sp.symbols("t eta")
    a = -t + eta * t**3
    s = -t**2
    q3 = sp.cancel((s + a**2) / a**4)
    v = sp.cancel(4 * (s + a**2) / s**2)

    assert sp.limit(q3, t, 0) == -2 * eta
    assert sp.limit(v, t, 0) == -8 * eta
    assert sp.limit(v / 4 - q3, t, 0) == 0

    # The key polynomial gains two extra orders beyond a^2.
    assert order_at_zero(a.subs(eta, 1), t) == 1
    assert order_at_zero(s, t) == 2
    assert order_at_zero((s + a**2).subs(eta, 1), t) == 4


def euclidean_quotients(a: int, b: int) -> list[int]:
    result: list[int] = []
    while b:
        result.append(a // b)
        a, b = b, a % b
    return result


def plane_branch_multiplicity_sequence(
    large: int, small: int
) -> list[int]:
    sequence: list[int] = []
    while small:
        quotient, remainder = divmod(large, small)
        sequence.extend([small] * quotient)
        large, small = small, remainder
    return sequence


def minimal_target_tree_family_checks() -> None:
    x, y, X, Y, Z, t, q, tau = sp.symbols(
        "x y X Y Z t q tau"
    )

    for k in range(2, 11):
        r = k + 1
        delta = 2 * k + 1
        assert gcd(r, delta) == 1

        affine = sp.expand((y + 1) ** delta - x**r)
        assert sp.Poly(affine, x, y).total_degree() == delta
        assert sp.expand(
            affine.subs({x: t**delta, y: t**r - 1})
        ) == 0

        # The origin of the parameter maps to an affine singular point.
        assert affine.subs({x: 0, y: -1}) == 0
        assert sp.diff(affine, x).subs({x: 0, y: -1}) == 0
        assert sp.diff(affine, y).subs({x: 0, y: -1}) == 0

        restricted = sp.expand(affine.subs(y, 0))
        assert sp.degree(restricted, x) == r
        assert sp.gcd(restricted, sp.diff(restricted, x)) == 1

        homogeneous = sp.expand((Y + Z) ** delta - X**r * Z**k)
        assert sp.Poly(homogeneous, X, Y, Z).total_degree() == delta
        on_gamma = sp.expand(homogeneous.subs(Y, 0))
        expected = sp.expand(Z**k * (Z**r - X**r))
        assert on_gamma == expected
        assert r + k == delta

        z_local = q**delta
        y_local = q**k - q**delta
        assert order_at_zero(z_local, q) == delta
        assert order_at_zero(y_local, q) == k
        assert euclidean_quotients(delta, k) == [2, k]
        multiplicities = plane_branch_multiplicity_sequence(delta, k)
        assert multiplicities == [k, k] + [1] * k
        assert len(multiplicities) == k + 2

        residual = tau**2 - affine
        assert sp.expand(sp.discriminant(residual, tau) - 4 * affine) == 0
        residual_on_gamma = sp.expand(
            sp.discriminant(residual, tau).subs(y, 0)
        )
        assert sp.degree(residual_on_gamma, x) == r


def main() -> None:
    fixed_arm_checks()
    graph_and_self_intersection_checks()
    key_polynomial_and_dicritical_parameter_checks()
    minimal_target_tree_family_checks()
    print("route-a canonical infinity-tree flexibility checks passed")


if __name__ == "__main__":
    main()
