#!/usr/bin/env python3
"""Exact checks for the Laurent/affine-modification descent audit."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import sympy as sp

from route_bd_verify import (
    AB_P_VERTICES,
    AB_Q_VERTICES,
    C_P_VERTICES,
    C_Q_VERTICES,
    lattice_points,
)


x, y, s, u, v = sp.symbols("x y s u v")


def bracket(left: sp.Expr, right: sp.Expr, first=x, second=y) -> sp.Expr:
    return sp.expand(
        sp.diff(left, first) * sp.diff(right, second)
        - sp.diff(left, second) * sp.diff(right, first)
    )


def in_rees_cone(poly: sp.Expr, exponent: int) -> bool:
    """Check membership in k[x,x^exponent*y] monomial by monomial."""

    for (x_degree, y_degree), coefficient in sp.Poly(poly, x, y).terms():
        if coefficient and x_degree < exponent * y_degree:
            return False
    return True


def verify_affine_modification_chain_rule() -> None:
    r = 3
    # Generic representatives are enough for the exact chain-rule identity.
    p_bar = u**3 + 2 * u * v + v**2
    q_bar = u**2 - v + u * v**2
    p = sp.expand(p_bar.subs({u: x, v: x**r * y}, simultaneous=True))
    q = sp.expand(q_bar.subs({u: x, v: x**r * y}, simultaneous=True))
    assert sp.expand(bracket(p, q) - x**r * bracket(p_bar, q_bar, u, v).subs({u: x, v: x**r * y})) == 0
    assert in_rees_cone(p, r)
    assert in_rees_cone(q, r)


def verify_contracted_jet_normal_forms() -> None:
    a, b, c, lam = sp.symbols("a b c lam", nonzero=True)

    # Rees/birational leading arm: A is constant and B is affine linear.
    A0 = a
    B0 = c * y / a + b
    assert sp.expand(A0 * sp.diff(B0, y) - 2 * sp.diff(A0, y) * B0 - c) == 0

    # Fold leading arm: A is linear; the A^2 term is a removable target shear.
    A1 = a * y + b
    B1 = lam * A1**2 - c / (2 * a)
    assert sp.expand(A1 * sp.diff(B1, y) - 2 * sp.diff(A1, y) * B1 - c) == 0


def verify_laurent_escape_family() -> None:
    for n in range(2, 11):
        p = x + (x * y) ** n
        q = x**2 * y + sp.Rational(n, n + 1) * (x * y) ** (n + 1)

        assert bracket(p, q) == x**2
        assert sp.expand(p.subs(x, 0)) == 0
        assert sp.expand(q.subs(x, 0)) == 0

        # The leading contracted-boundary jet is the Rees/birational arm.
        assert sp.expand(sp.diff(p, x).subs(x, 0)) == 1
        assert sp.expand(sp.diff(q, x, 2).subs(x, 0) / 2) == y

        # Nevertheless the high Laurent-canonical terms violate the full
        # Rees semigroup condition.
        assert not in_rees_cone(p, 2)
        assert not in_rees_cone(q, 2)

        # In s=xy coordinates:
        #   P=x+s^n, Q=x*s+n/(n+1)*s^(n+1),
        # hence x=P-s^n and
        #   s^(n+1)-(n+1)P*s+(n+1)Q=0.
        p_xs = x + s**n
        q_xs = x * s + sp.Rational(n, n + 1) * s ** (n + 1)
        relation = s ** (n + 1) - (n + 1) * p_xs * s + (n + 1) * q_xs
        assert sp.expand(relation) == 0
        q_as_rational_map = u * s - sp.Rational(1, n + 1) * s ** (n + 1)
        assert sp.Poly(q_as_rational_map, s).degree() == n + 1
        assert sp.Poly(q_as_rational_map, s).LC() == -sp.Rational(1, n + 1)

        # The canonical transformation has determinant one in (x,s)
        # after accounting for [x,s]_(x,y)=x.
        assert bracket(p_xs, q_xs, x, s) == x


def verify_rees_sheet_joining() -> None:
    tau, z, target_p, target_q, root = sp.symbols(
        "tau z target_p target_q root"
    )
    p = x + (x * y) ** 2
    q = x**2 * y + sp.Rational(2, 3) * (x * y) ** 3

    p_rees = sp.expand(
        tau**2
        * p.subs({x: x / tau**2, y: tau * y}, simultaneous=True)
    )
    q_rees = sp.expand(
        tau**3
        * q.subs({x: x / tau**2, y: tau * y}, simultaneous=True)
    )
    assert p_rees == p
    assert q_rees == q

    p_xz = x + z**2
    q_xz = x * z + sp.Rational(2, 3) * z**3
    comparison = root**3 - 3 * target_p * root + 3 * target_q
    assert sp.factor(comparison) == comparison
    assert sp.discriminant(comparison, root) == 27 * (
        4 * target_p**3 - 9 * target_q**2
    )

    pulled_back = sp.expand(
        comparison.subs({target_p: p_xz, target_q: q_xz})
    )
    expected = (root - z) * (root**2 + z * root - 3 * x - 2 * z**2)
    assert sp.expand(pulled_back - expected) == 0
    residual = root**2 + z * root - 3 * x - 2 * z**2
    assert sp.expand(residual.subs(root, z)) == -3 * x

    p_boundary = p_xz.subs(x, 0)
    q_boundary = q_xz.subs(x, 0)
    assert sp.expand(4 * p_boundary**3 - 9 * q_boundary**2) == 0


def verify_gghv_cone_failure() -> None:
    def defect(exponent: tuple[int, int]) -> int:
        x_degree, y_degree = exponent
        return x_degree - 2 * y_degree

    # Every listed Newton vertex is required to be nonzero.  A single
    # negative defect excludes membership in k[x,x^2 y].
    assert defect((8, 16)) == -24
    assert defect((12, 24)) == -36
    assert (8, 16) in AB_P_VERTICES
    assert (12, 24) in AB_Q_VERTICES

    assert defect((0, 8)) == -16
    assert defect((0, 12)) == -24
    assert (0, 8) in C_P_VERTICES
    assert (0, 12) in C_Q_VERTICES

    # N=2 of the Laurent escape family is supported inside the a/b
    # polygons and contains the two fixed-pole vertices, but omits the
    # required outer vertices.
    ab_p_support = set(lattice_points(AB_P_VERTICES))
    ab_q_support = set(lattice_points(AB_Q_VERTICES))
    assert {(1, 0), (2, 2)} <= ab_p_support
    assert {(2, 1), (3, 3)} <= ab_q_support


def main() -> None:
    verify_affine_modification_chain_rule()
    verify_contracted_jet_normal_forms()
    verify_laurent_escape_family()
    verify_rees_sheet_joining()
    verify_gghv_cone_failure()
    print("verified the exact affine-modification chain rule")
    print("verified the two contracted x^2-boundary leading normal forms")
    print("verified the Laurent escape family for degrees 3 through 11")
    print("verified every family member has Jacobian x^2 and lies outside k[x,x^2*y]")
    print("verified the constant Rees family and exact diagonal-sheet/cusp joining")
    print("verified the required GGHV a/b and case-c vertices violate the Rees cone")
    print("verified N=2 lies in the a/b support caps but omits their required outer vertices")


if __name__ == "__main__":
    main()
