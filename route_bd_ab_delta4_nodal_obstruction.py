#!/usr/bin/env python3
"""Exact checks for the nodal delta=4 fourth-jet obstruction."""

from __future__ import annotations

import sympy as sp


def verify_nodal_graph_derivatives() -> None:
    X, c, h = sp.symbols("X c h", nonzero=True)
    g = (X - c**2) * sp.sqrt(X)
    derivatives = [
        sp.powdenest(
            sp.diff(g, X, order).subs(X, h**2),
            force=True,
        )
        for order in (2, 3, 4)
    ]
    expected = [
        (3 * h**2 + c**2) / (4 * h**3),
        -3 * (h**2 + c**2) / (8 * h**5),
        3 * (3 * h**2 + 5 * c**2) / (16 * h**7),
    ]
    assert all(
        sp.simplify(actual - target) == 0
        for actual, target in zip(derivatives, expected)
    )
    assert sp.simplify(derivatives[0].subs(h, c) - 1 / c) == 0


def verify_fourth_taylor_coefficient_and_factorization() -> None:
    z = sp.symbols("z")
    h, c, p1, p2 = sp.symbols("h c p1 p2", nonzero=True)
    delta = p1 * z + p2 * z**2
    # Formal square-root expansion selects sqrt(h^2)=h.
    square_root = h * sp.series(
        (1 + delta / h**2) ** sp.Rational(1, 2),
        z,
        0,
        5,
    ).removeO()
    graph = sp.expand((h**2 + delta - c**2) * square_root)
    fourth = sp.factor(graph.coeff(z, 4))

    expected = (
        (3 * h**2 + c**2) * p2**2 / (8 * h**3)
        - 3 * (h**2 + c**2) * p1**2 * p2 / (16 * h**5)
        + (3 * h**2 + 5 * c**2) * p1**4 / (128 * h**7)
    )
    assert sp.simplify(fourth - expected) == 0

    cleared = sp.factor(128 * h**7 * fourth)
    factored = sp.factor(
        (p1**2 - 4 * h**2 * p2)
        * (
            (3 * h**2 + 5 * c**2) * p1**2
            - 4 * h**2 * (3 * h**2 + c**2) * p2
        )
    )
    assert sp.expand(cleared - factored) == 0


def verify_uncancelled_double_pole() -> None:
    w = sp.symbols("w")
    a, c, lam = sp.symbols("a c lam", nonzero=True)
    p10, p11, a20, a21 = sp.symbols("p10 p11 a20 a21")
    h = c + a * w**4
    p1 = p10 + p11 * w
    p2 = lam / w + a20 + a21 * w

    fourth = (
        (3 * h**2 + c**2) * p2**2 / (8 * h**3)
        - 3 * (h**2 + c**2) * p1**2 * p2 / (16 * h**5)
        + (3 * h**2 + 5 * c**2) * p1**4 / (128 * h**7)
    )
    double_pole_coefficient = sp.simplify(
        sp.limit(w**2 * fourth, w, 0)
    )
    assert double_pole_coefficient == lam**2 / (2 * c)
    assert double_pole_coefficient != 0


def main() -> None:
    verify_nodal_graph_derivatives()
    verify_fourth_taylor_coefficient_and_factorization()
    verify_uncancelled_double_pole()
    print("verified the nodal graph derivatives through fourth order")
    print("verified the exact factored fourth-jet condition")
    print("verified the uncancelled fixed-pole coefficient lambda^2/(2c)")
    print("RESULT: DELTA=4 NODAL OBSTRUCTION PASSES")


if __name__ == "__main__":
    main()
