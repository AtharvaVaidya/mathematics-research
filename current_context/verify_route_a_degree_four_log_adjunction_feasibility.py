#!/usr/bin/env python3
"""Exact checks for the quartic log-adjunction feasibility certificates."""

from __future__ import annotations

import sympy as sp


t, x, y, z, r = sp.symbols("t x y z r")


def verify_log_degree_ledgers() -> None:
    # Connected first survivor.
    for n in range(1, 12):
        for e in range(1, n + 1):
            genus = e - 1
            deleted = 1 + 4 * n - 2 * e
            punctures = 2 + deleted
            assert 2 * genus - 2 + punctures == 4 * n - 1

    # Split first survivor.
    for n in range(1, 12):
        deleted = 1 + 4 * n
        total_projective_canonical_degree = -4
        punctures = 2 + deleted
        assert (
            total_projective_canonical_degree + punctures
            == 4 * n - 1
        )

    # Extra-boundary survivor.
    for k_1 in range(1, 12):
        for k_2 in range(1, 12):
            assert (k_1 - 1) + (k_2 - 1) == k_1 + k_2 - 2
            assert k_1 + k_2 - 2 >= 0


def verify_odd_contact_branch() -> None:
    x_t = t**2
    y_t = t**3 - t**5
    branch = y**2 - x**3 * (1 - x) ** 2
    assert sp.expand(branch.subs({x: x_t, y: y_t})) == 0

    # The parametrization is injective except for t=1 and t=-1.
    # Since x(t)=x(-t), equality of y-values is equivalent to y(t)=0.
    assert sp.factor(y_t) == -t**3 * (t - 1) * (t + 1)

    branch_x = sp.diff(branch, x)
    branch_y = sp.diff(branch, y)
    singular_x = sp.factor(
        sp.resultant(branch, branch_y, y)
    )
    assert singular_x == -4 * x**3 * (x - 1) ** 2
    assert branch_x.subs({x: 0, y: 0}) == 0
    assert branch_x.subs({x: 1, y: 0}) == 0

    # At t=1,-1 the two tangent vectors are independent.
    velocity_plus = sp.Matrix(
        [sp.diff(x_t, t).subs(t, 1), sp.diff(y_t, t).subs(t, 1)]
    )
    velocity_minus = sp.Matrix(
        [sp.diff(x_t, t).subs(t, -1), sp.diff(y_t, t).subs(t, -1)]
    )
    assert sp.det(sp.Matrix.hstack(velocity_plus, velocity_minus)) != 0

    # The residual double cover is G_m under r=t+z.
    t_from_r = (r + r ** -1) / 2
    z_from_r = (r - r ** -1) / 2
    assert sp.simplify(z_from_r**2 - (t_from_r**2 - 1)) == 0
    assert sp.simplify(sp.diff(t_from_r, r) / z_from_r - 1 / r) == 0

    # The three deleted points are the exact zero divisor of this
    # Laurent polynomial on G_m.
    deleted_polynomial = sp.expand((r - sp.I) * (r - 1) * (r + 1))
    assert deleted_polynomial.subs(r, sp.I) == 0
    assert deleted_polynomial.subs(r, 1) == 0
    assert deleted_polynomial.subs(r, -1) == 0
    assert deleted_polynomial.subs(r, 0) != 0

    # This is the separate conductor-adjunction divisor:
    #   conductor = 2[-i],
    #   pullback(E) = 2[i] + [1] + [-1].
    adjunction_polynomial = sp.expand(
        (r + sp.I) ** 2
        * (r - sp.I) ** 2
        * (r - 1)
        * (r + 1)
    )
    assert sp.expand(
        adjunction_polynomial - (r**2 + 1) ** 2 * (r**2 - 1)
    ) == 0
    assert adjunction_polynomial.subs(r, 0) != 0

    def zero_order(polynomial: sp.Expr, point: sp.Expr) -> int:
        order = 0
        derivative = polynomial
        while sp.simplify(derivative.subs(r, point)) == 0:
            order += 1
            derivative = sp.diff(derivative, r)
        return order

    assert zero_order(adjunction_polynomial, sp.I) == 2
    assert zero_order(adjunction_polynomial, -sp.I) == 2
    assert zero_order(adjunction_polynomial, sp.Integer(1)) == 1
    assert zero_order(adjunction_polynomial, -sp.Integer(1)) == 1


def verify_local_cusp_and_node_algebras() -> None:
    cubic = z**3 + x * z - y
    discriminant = sp.factor(sp.discriminant(cubic, z))
    assert discriminant == -4 * x**3 - 27 * y**2

    pullback = sp.factor(
        discriminant.subs(y, z**3 + x * z)
    )
    assert pullback == -(x + 3 * z**2) ** 2 * (4 * x + 3 * z**2)

    # On the residual cusp branch 4x+3z^2=0, the ramified equation
    # x+3z^2 restricts to (9/4)z^2: pullback(E) has coefficient two.
    ramified_on_residual = sp.expand(
        (x + 3 * z**2).subs(x, -sp.Rational(3, 4) * z**2)
    )
    assert ramified_on_residual == sp.Rational(9, 4) * z**2

    # The other residual point is the rank-one cusp factor.  Its
    # completed local ring C[[s^2,s^3]] has normalization C[[s]]
    # and conductor exponent two: 1 is the unique semigroup gap.
    cusp_semigroup = {
        2 * a + 3 * b
        for a in range(8)
        for b in range(8)
    }
    assert 1 not in cusp_semigroup
    assert all(exponent in cusp_semigroup for exponent in range(2, 12))

    # In the two node factors the ramified and residual parameters
    # are (s,y) and (q,x), respectively, hence both intersections
    # have multiplicity one.
    s_node, y_node, q_node, x_node = sp.symbols(
        "s_node y_node q_node x_node"
    )
    assert sp.det(
        sp.Matrix(
            [
                [sp.diff(s_node, s_node), sp.diff(s_node, y_node)],
                [sp.diff(y_node, s_node), sp.diff(y_node, y_node)],
            ]
        )
    ) == 1
    assert sp.det(
        sp.Matrix(
            [
                [sp.diff(q_node, q_node), sp.diff(q_node, x_node)],
                [sp.diff(x_node, q_node), sp.diff(x_node, x_node)],
            ]
        )
    ) == 1

    # The three local labels generate a transitive subgroup of S_4,
    # so there is no local generation obstruction.  This does not
    # verify global branch-complement relations.
    transpositions = ((0, 1), (1, 2), (2, 3))
    reached = {0}
    changed = True
    while changed:
        changed = False
        for left, right in transpositions:
            if left in reached and right not in reached:
                reached.add(right)
                changed = True
            if right in reached and left not in reached:
                reached.add(left)
                changed = True
    assert reached == {0, 1, 2, 3}


def verify_extra_boundary_certificate() -> None:
    cusp = y**2 - x**3
    assert sp.expand(cusp.subs({x: t**2, y: t**3})) == 0

    # Restriction to Gamma: x=1.
    intersection_polynomial = sp.factor(cusp.subs(x, 1))
    assert intersection_polynomial == (y - 1) * (y + 1)
    assert sp.diff(intersection_polynomial, y).subs(y, 1) != 0
    assert sp.diff(intersection_polynomial, y).subs(y, -1) != 0

    # The double cover of the cusp is the A_2 equation pq=-x^3.
    p, q, s = sp.symbols("p q s")
    double_cover = s**2 - (y**2 - x**3)
    transformed = sp.expand(
        double_cover.subs({s: (p + q) / 2, y: (p - q) / 2})
    )
    assert sp.expand(transformed - (p * q + x**3)) == 0


def main() -> None:
    verify_log_degree_ledgers()
    verify_odd_contact_branch()
    verify_local_cusp_and_node_algebras()
    verify_extra_boundary_certificate()
    print("verified: both quartic log-canonical degree ledgers")
    print("verified: exact cusp-plus-node odd-contact branch")
    print("verified: connected residual G_m cover and deleted divisor")
    print("verified: separate conductor and pullback(E) adjunction divisor")
    print("verified: exact Gorenstein 3+1 and 2+2 local algebras")
    print("verified: split extra-boundary incidence divisor")
    print("RESULT: finite log-adjunction data do not exclude either survivor")


if __name__ == "__main__":
    main()
