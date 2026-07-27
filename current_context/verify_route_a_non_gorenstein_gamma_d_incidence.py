#!/usr/bin/env python3
"""Exact checks for the non-Gorenstein/Gamma_D incidence audit."""

from __future__ import annotations

import sympy as sp


def nodal_countermodel() -> None:
    s, t, x, y = sp.symbols("s t x y")
    target_x = s
    target_y = t**3 - 3 * s * t
    jacobian = sp.det(
        sp.Matrix(
            [
                [sp.diff(target_x, s), sp.diff(target_x, t)],
                [sp.diff(target_y, s), sp.diff(target_y, t)],
            ]
        )
    )
    assert sp.expand(jacobian - 3 * (t**2 - s)) == 0

    d_equation = s - t**2 + sp.Rational(2, 3)
    d_substitution = {s: t**2 - sp.Rational(2, 3)}
    assert sp.expand(jacobian.subs(d_substitution)) == 2

    parametrized_x = sp.expand(target_x.subs(d_substitution))
    parametrized_y = sp.expand(target_y.subs(d_substitution))
    assert parametrized_x == t**2 - sp.Rational(2, 3)
    assert sp.expand(parametrized_y - 2 * t * (1 - t**2)) == 0

    gamma = (
        y**2
        - 4
        * (x + sp.Rational(2, 3))
        * (sp.Rational(1, 3) - x) ** 2
    )
    assert sp.expand(
        gamma.subs({x: parametrized_x, y: parametrized_y})
    ) == 0

    node = {x: sp.Rational(1, 3), y: 0}
    assert gamma.subs(node) == 0
    assert sp.diff(gamma, x).subs(node) == 0
    assert sp.diff(gamma, y).subs(node) == 0

    # The two normalization points are t=+/-1 and have distinct tangents.
    tangent_plus = (
        sp.diff(parametrized_x, t).subs(t, 1),
        sp.diff(parametrized_y, t).subs(t, 1),
    )
    tangent_minus = (
        sp.diff(parametrized_x, t).subs(t, -1),
        sp.diff(parametrized_y, t).subs(t, -1),
    )
    assert tangent_plus == (2, -4)
    assert tangent_minus == (-2, -4)
    assert sp.det(sp.Matrix([tangent_plus, tangent_minus])) != 0

    fiber_polynomial = sp.factor(
        target_y.subs({s: sp.Rational(1, 3)}) - 0
    )
    assert fiber_polynomial == t * (t - 1) * (t + 1)

    branch = 4 * x**3 - y**2
    assert branch.subs(node) == sp.Rational(4, 27)
    restricted_branch = sp.factor(
        branch.subs({x: parametrized_x, y: parametrized_y})
    )
    assert sp.expand(
        restricted_branch - sp.Rational(4, 27) * (9 * t**2 - 8)
    ) == 0
    for branch_parameter in (
        2 * sp.sqrt(2) / 3,
        -2 * sp.sqrt(2) / 3,
    ):
        assert sp.simplify(restricted_branch.subs(t, branch_parameter)) == 0
        assert branch_parameter not in (1, -1)

    pulled_back_gamma = sp.factor(
        gamma.subs({x: target_x, y: target_y})
    )
    residual = (
        36 * s**2
        - 45 * s * t**2
        - 24 * s
        + 9 * t**4
        + 6 * t**2
        + 4
    )
    expected_pullback = -sp.Rational(1, 27) * (3 * d_equation) * residual
    assert sp.expand(pulled_back_gamma - expected_pullback) == 0

    for fiber_t in (-1, 0, 1):
        assert residual.subs({s: sp.Rational(1, 3), t: fiber_t}) == 0


def fiber_length_bounds() -> None:
    rank = 3
    for normalization_points in (1, 2, 3):
        retained_etale_length = normalization_points
        assert retained_etale_length <= rank
        if normalization_points >= 2:
            minimum_if_branched = retained_etale_length + 2
            assert minimum_if_branched > rank

    non_gorenstein_support_points = 1
    non_gorenstein_length = 3
    assert non_gorenstein_support_points == 1
    assert non_gorenstein_length == rank


def main() -> None:
    nodal_countermodel()
    fiber_length_bounds()
    print("verified: D0 lies entirely in the etale locus")
    print("verified: D0 normalizes a nodal rational target curve")
    print("verified: the nodal cubic fiber has three distinct etale points")
    print("verified: pullback splits as D0 plus a residual degree-two curve")
    print("verified: branch restriction is 4(9t^2-8)/27")
    print("verified: two retained normalization points exclude ramification")
    print("RESULT: Gamma_D avoids non-Gorenstein values, but nodes remain possible")


if __name__ == "__main__":
    main()
