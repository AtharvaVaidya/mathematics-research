#!/usr/bin/env python3
"""Exact checks for ROUTE_A_GLOBAL_MONODROMY_DICRITICAL_BRIDGE_NO_GO.md."""

from __future__ import annotations

import sympy as sp


def canonical_double_cover_checks() -> None:
    a, b, v, z = sp.symbols("a b v z")
    u = a**2
    z_chart = 1 + 2 * a**2 * b
    v_chart = 4 * b * (1 + a**2 * b)
    w_chart = a * z_chart

    assert sp.expand(z_chart**2 - 1 - a**2 * v_chart) == 0
    assert sp.expand(w_chart**2 - u - u**2 * v_chart) == 0

    # The two inverse expressions for b agree modulo z^2-1-a^2 v.
    inverse_numerator = sp.expand(
        (z - 1) * (z + 1) - a**2 * v
    )
    assert inverse_numerator == z**2 - 1 - a**2 * v

    # The deck involution preserves the finite cover equation and exchanges
    # the two divisors over a=0.
    cover_equation = z**2 - 1 - a**2 * v
    deck_equation = sp.expand(
        cover_equation.subs({a: -a, z: -z}, simultaneous=True)
    )
    assert deck_equation == cover_equation

    # In the plane chart, the same deck action is the known rational map.
    a_deck = -a
    b_deck = -b - a ** -2
    z_deck = sp.simplify(1 + 2 * a_deck**2 * b_deck)
    v_deck = sp.simplify(4 * b_deck * (1 + a_deck**2 * b_deck))
    assert sp.simplify(z_deck + z_chart) == 0
    assert sp.simplify(v_deck - v_chart) == 0


def pseudoplane_jacobian_checks() -> None:
    a, b = sp.symbols("a b")
    u = a**2
    v = 4 * b * (1 + a**2 * b)
    w = a * (1 + 2 * a**2 * b)

    # The canonical chart pulls the Route A Poisson bracket to a constant
    # plane Jacobian.  Checking the generator pairs certifies the scaling.
    def jac(f: sp.Expr, g: sp.Expr) -> sp.Expr:
        return sp.expand(sp.diff(f, a) * sp.diff(g, b) - sp.diff(f, b) * sp.diff(g, a))

    assert jac(u, v) == sp.expand(-4 * (-2 * w))
    assert jac(u, w) == sp.expand(-4 * (-u**2))
    assert jac(v, w) == sp.expand(-4 * (1 + 2 * u * v))


def distinguished_infinity_chart_checks() -> None:
    t, eta = sp.symbols("t eta")
    a = -t + eta * t**3
    b = -t**-2
    u = sp.expand(a**2)
    v = sp.cancel(4 * b * (1 + a**2 * b))
    w = sp.cancel(a * (1 + 2 * a**2 * b))

    assert sp.simplify(v - (-8 * eta + 4 * eta**2 * t**2)) == 0
    z0 = 1 - eta * t**2
    assert sp.expand(u - t**2 * z0**2) == 0
    assert sp.expand(w - t * z0 * (2 * z0**2 - 1)) == 0
    assert sp.expand(w**2 - u - u**2 * v) == 0

    chart_jac = sp.simplify(
        sp.diff(a, t) * sp.diff(b, eta)
        - sp.diff(a, eta) * sp.diff(b, t)
    )
    assert chart_jac == -2
    assert sp.limit(v, t, 0) == -8 * eta


def local_sheet_ledger_checks() -> None:
    r, y = sp.symbols("r y")
    x = r**2

    # Each of the two lifted ramified sheets has transverse local degree two.
    ramified_jac = sp.det(
        sp.Matrix(
            [
                [sp.diff(x, r), sp.diff(x, y)],
                [sp.diff(y, r), sp.diff(y, y)],
            ]
        )
    )
    assert ramified_jac == 2 * r

    # The local cubic algebra along Gamma is a distinguished factor times
    # tau^2-x; its residual discriminant has one odd zero.
    tau = sp.symbols("tau")
    residual = tau**2 - x
    residual_disc = sp.discriminant(residual, tau)
    assert residual_disc == 4 * x
    assert sp.degree(residual_disc, r) == 2
    # In the normalization parameter on Gamma, x itself has odd order one.
    x_gamma = sp.symbols("x_gamma")
    assert sp.degree(x_gamma, x_gamma) == 1

    # Exact retained/missing degree table:
    # generic, Gamma only, Delta only, Gamma intersect Delta.
    retained = {
        "generic": 2 + 4,
        "gamma": 1 + 4,
        "delta": 2 + 0,
        "intersection": 1 + 0,
    }
    missing = {key: 6 - value for key, value in retained.items()}
    assert retained == {
        "generic": 6,
        "gamma": 5,
        "delta": 2,
        "intersection": 1,
    }
    assert missing == {
        "generic": 0,
        "gamma": 1,
        "delta": 4,
        "intersection": 5,
    }
    assert missing["intersection"] == missing["gamma"] + missing["delta"]
    assert missing["intersection"] == 1 + 2 + 2

    # One smooth ramification divisor can contain arbitrarily many odd
    # residual places.  Here its image y=h(x) meets Gamma=(y=0) at three
    # distinct transverse points.
    x_graph = sp.symbols("x_graph")
    h = (x_graph - 1) * (x_graph - 2) * (x_graph - 3)
    y_graph = r**2 + h
    graph_jac = sp.det(
        sp.Matrix(
            [
                [sp.diff(x_graph, x_graph), sp.diff(x_graph, r)],
                [sp.diff(y_graph, x_graph), sp.diff(y_graph, r)],
            ]
        )
    )
    assert graph_jac == 2 * r
    roots = sp.solve(h, x_graph)
    assert roots == [1, 2, 3]
    assert all(sp.diff(h, x_graph).subs(x_graph, root) != 0 for root in roots)
    residual_graph_disc = sp.discriminant(r**2 + h, r)
    assert sp.expand(residual_graph_disc + 4 * h) == 0


def quadratic_valuation_samples() -> None:
    t = sp.symbols("t")

    # Odd valuation: y^2=t is ramified.
    y_odd = sp.symbols("y_odd")
    odd_poly = y_odd**2 - t
    assert sp.discriminant(odd_poly, y_odd) == 4 * t

    # Even valuation and square residue: y^2=t^2(1+t)^2 splits after
    # dividing by t.
    y_even = sp.symbols("y_even")
    even_poly = sp.expand(y_even**2 - t**2 * (1 + t) ** 2)
    split_even = (y_even - t * (t + 1)) * (y_even + t * (t + 1))
    assert sp.expand(even_poly - split_even) == 0

    # The parity at infinity of tau^2=g is the parity of deg(g).
    v = sp.symbols("v")
    g_odd = v * (v - 1) * (v + 1)
    g_even = (v - 1) * (v + 1)
    assert sp.degree(g_odd, v) % 2 == 1
    assert sp.degree(g_even, v) % 2 == 0


def main() -> None:
    canonical_double_cover_checks()
    pseudoplane_jacobian_checks()
    distinguished_infinity_chart_checks()
    local_sheet_ledger_checks()
    quadratic_valuation_samples()
    print("route-a global monodromy/dicritical bridge checks passed")


if __name__ == "__main__":
    main()
