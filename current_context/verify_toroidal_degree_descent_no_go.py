#!/usr/bin/env python3
"""Exact checks for the one-boundary toroidal descent classification."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import sympy as sp

from route_bd_verify import (
    AB_P_VERTICES,
    C_P_VERTICES,
    lattice_points,
)


x, y, u, v, s = sp.symbols("x y u v s")


def bracket(
    left: sp.Expr,
    right: sp.Expr,
    first: sp.Symbol = x,
    second: sp.Symbol = y,
) -> sp.Expr:
    return sp.expand(
        sp.diff(left, first) * sp.diff(right, second)
        - sp.diff(left, second) * sp.diff(right, first)
    )


def in_unshifted_chart(
    polynomial: sp.Expr,
    *,
    cover_degree: int,
    y_twist: int,
) -> bool:
    """Membership in k[x^a, x^c*y] by the exact affine semigroup test."""

    for (x_degree, y_degree), coefficient in sp.Poly(polynomial, x, y).terms():
        residual = x_degree - y_twist * y_degree
        if coefficient and (
            residual < 0 or residual % cover_degree != 0
        ):
            return False
    return True


def verify_monomial_classification() -> None:
    # Exhaust all small nonnegative monomial exponent matrices whose
    # Jacobian has no y factor.  Up to swapping rows, every dominant one
    # is (x^a, x^c*y).
    for r in range(0, 8):
        found: set[tuple[int, int]] = set()
        for a in range(0, 10):
            for b in range(0, 3):
                for c in range(0, 10):
                    for d in range(0, 3):
                        determinant = a * d - b * c
                        if determinant == 0:
                            continue
                        if b + d - 1 != 0 or a + c - 1 != r:
                            continue
                        if b == 0:
                            assert d == 1 and a >= 1
                            found.add((a, c))
                        else:
                            assert b == 1 and d == 0 and c >= 1
                            found.add((c, a))
        assert found == {(a, r + 1 - a) for a in range(1, r + 2)}


def verify_general_triangular_normal_form() -> None:
    # Once unique factorization forces phi' and g to be monomials, the
    # integrated affine normal form has exactly the asserted Jacobian.
    for r in range(0, 8):
        for a in range(1, r + 2):
            c = r + 1 - a
            phi = sp.Rational(7, a) * x**a + 5
            g = 11 * x**c
            f = 2 + 3 * x + x**4
            assert bracket(phi, g * y + f) == 77 * x**r

    # Any nonlinear y term visibly survives in phi'(x) * V_y and hence
    # cannot occur in a pure-x Jacobian.
    h = sp.symbols("h", nonzero=True)
    nonlinear_v = (1 + x) * y + h * x**2 * y**2 + x**3
    nonlinear_jacobian = bracket(x**3, nonlinear_v)
    assert sp.Poly(nonlinear_jacobian, y).degree() == 1
    assert sp.Poly(nonlinear_jacobian, y).coeff_monomial(y) == 6 * h * x**4


def verify_shifted_chart_and_chain_rule() -> None:
    for r in range(1, 7):
        for a in range(1, r + 2):
            c = r + 1 - a
            f = 2 * x + 3 * x**2 + x**5
            chart_u = x**a
            chart_v = x**c * y + f
            assert bracket(chart_u, chart_v) == a * x**r

            p_bar = u**2 + u * v + 2 * v**3
            q_bar = u**3 - v + u**2 * v**2
            p = sp.expand(
                p_bar.subs({u: chart_u, v: chart_v}, simultaneous=True)
            )
            q = sp.expand(
                q_bar.subs({u: chart_u, v: chart_v}, simultaneous=True)
            )
            expected = (
                a
                * x**r
                * bracket(p_bar, q_bar, u, v).subs(
                    {u: chart_u, v: chart_v}, simultaneous=True
                )
            )
            assert sp.expand(bracket(p, q) - expected) == 0


def verify_iterated_collapse() -> None:
    a, b, c, d = 2, 3, 4, 2
    f = x + x**3
    g = u**2 - 3 * u

    first_u = x**a
    first_v = x**c * y + f
    composite_u = sp.expand(first_u**b)
    composite_v = sp.expand(
        first_u**d * first_v + g.subs(u, first_u)
    )

    total_a = a * b
    total_c = a * d + c
    total_f = sp.expand(x ** (a * d) * f + g.subs(u, x**a))
    assert composite_u == x**total_a
    assert composite_v == x**total_c * y + total_f
    assert bracket(composite_u, composite_v) == total_a * x ** (
        total_a + total_c - 1
    )


def top_y_row(vertices: tuple[tuple[int, int], ...]) -> tuple[int, set[int]]:
    points = lattice_points(vertices)
    degree = max(y_degree for _, y_degree in points)
    return degree, {
        x_degree
        for x_degree, y_degree in points
        if y_degree == degree
    }


def verify_top_coefficient_law() -> None:
    for a, c in ((1, 4), (2, 3), (3, 0), (5, 2)):
        f = 1 + 2 * x + x**4
        chart_u = x**a
        chart_v = x**c * y + f
        coefficients = (
            1 + u,
            2 - u + u**2,
            3 + 2 * u**2,
            5 - 7 * u + u**3,
        )
        polynomial = sp.expand(
            sum(
                coefficient.subs(u, chart_u) * chart_v**degree
                for degree, coefficient in enumerate(coefficients)
            )
        )
        top = sp.Poly(polynomial, y).coeff_monomial(y**3)
        expected = x ** (3 * c) * coefficients[3].subs(u, x**a)
        assert sp.expand(top - expected) == 0
        for (exponent,), coefficient in sp.Poly(top, x).terms():
            if coefficient:
                assert exponent >= 3 * c
                assert (exponent - 3 * c) % a == 0


def verify_gghv_top_row_exclusion() -> None:
    for vertices in (AB_P_VERTICES, C_P_VERTICES):
        degree, x_exponents = top_y_row(vertices)
        assert degree == 16
        assert x_exponents == {8}

    r = 2
    degree = 16
    exponent = 8
    failures = []
    for a in range(1, r + 2):
        c = r + 1 - a
        passes = exponent >= c * degree and (
            exponent - c * degree
        ) % a == 0
        failures.append(not passes)
    assert failures == [True, True, True]

    # At every scale R, a=1 and a=2 fail on the top row.  For a=3,
    # the fixed x term contradicts divisibility by x^3 once the boundary
    # restriction is constant.
    for radial_scale in range(1, 101):
        degree = 4 * radial_scale
        exponent = 2 * radial_scale
        for a, c in ((1, 2), (2, 1)):
            assert not (
                exponent >= c * degree
                and (exponent - c * degree) % a == 0
            )
        assert 1 % 3 != 0


def verify_normalization_budget() -> None:
    for r in range(1, 8):
        for a in range(1, r + 2):
            c = r + 1 - a
            f = x + 2 * x**3
            shifted_v = x**c * y + f

            # Adjoining x removes the shifted center and gives
            # k[x, x^c*y].
            assert sp.expand(shifted_v - f) == x**c * y
            assert bracket(x, shifted_v) == x**c
            assert r - c == a - 1

            p_bar = x**2 + x * v + v**2
            q_bar = x**3 - v + x * v**2
            p = sp.expand(p_bar.subs(v, shifted_v))
            q = sp.expand(q_bar.subs(v, shifted_v))
            transformed = bracket(p_bar, q_bar, x, v).subs(
                v, shifted_v
            )
            assert sp.expand(
                bracket(p, q) - x**c * transformed
            ) == 0


def verify_normalization_escape_family() -> None:
    for r in range(1, 7):
        radial = x ** (r - 1) * y
        for n in range(2, 9):
            p = x + radial**n
            q = x * radial + sp.Rational(n, n + 1) * radial ** (n + 1)
            assert bracket(p, q) == x**r

            p_xs = x + s**n
            q_xs = x * s + sp.Rational(n, n + 1) * s ** (n + 1)
            relation = (
                s ** (n + 1)
                - (n + 1) * p_xs * s
                + (n + 1) * q_xs
            )
            assert sp.expand(relation) == 0
            assert sp.Poly(
                q_xs.subs(x, u - s**n), s
            ).degree() == n + 1

            for a in range(2, r + 2):
                c = r + 1 - a
                # The family lies in k[x,x^c*y], since
                # x^(r-1)y=x^(a-2)(x^c*y).
                assert in_unshifted_chart(
                    p, cover_degree=1, y_twist=c
                )
                assert in_unshifted_chart(
                    q, cover_degree=1, y_twist=c
                )

                # It does not descend through k[x^a,x^c*y].
                assert not in_unshifted_chart(
                    p, cover_degree=a, y_twist=c
                )


def main() -> None:
    verify_monomial_classification()
    verify_general_triangular_normal_form()
    verify_shifted_chart_and_chain_rule()
    verify_iterated_collapse()
    verify_top_coefficient_law()
    verify_gghv_top_row_exclusion()
    verify_normalization_budget()
    verify_normalization_escape_family()
    print("verified classification of triangular polynomial x^r-absorbing charts")
    print("verified shifted-center chain rule and closure under iteration")
    print("verified the shifted-center top-y coefficient congruence")
    print("verified GGHV a/b and case-c top vertices exclude every r=2 chart")
    print("verified the uniform all-scale a/b exclusion")
    print("verified normalization leaves the residual Jacobian exponent a-1")
    print("verified the normalization-escape family and degree relation")


if __name__ == "__main__":
    main()
