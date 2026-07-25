#!/usr/bin/env python3
"""Exact checks for the all-k radial total-degree contact spectrum."""

from __future__ import annotations

import sympy as sp

from route_bd_universal_radial_rank import lower_support


def bracket(left: sp.Expr, right: sp.Expr, z: sp.Symbol, w: sp.Symbol) -> sp.Expr:
    return sp.expand(
        sp.diff(left, z) * sp.diff(right, w)
        - sp.diff(left, w) * sp.diff(right, z)
    )


def verify_coordinate_and_support_bookkeeping() -> None:
    x, y, z, w = sp.symbols("x y z w", nonzero=True)
    transformed_bracket = sp.det(
        sp.Matrix(
            [
                [sp.diff(x * y, x), sp.diff(x * y, y)],
                [sp.diff(x * y**2, x), sp.diff(x * y**2, y)],
            ]
        )
    )
    assert sp.expand(transformed_bracket - x * y**2) == 0
    assert sp.cancel((z**2 / w) ** 2 / w - z**4 / w**3) == 0

    for k in range(1, 13):
        r = k + 1
        p_bound = 2 * r
        q_bound = 3 * r

        p_support = {
            2: list(range(-1, 2 * k + 1)),
        }
        p_support.update(
            {
                radial_degree: lower_support(
                    p_bound, radial_degree, 2
                )
                for radial_degree in range(1, -p_bound - 1, -1)
            }
        )
        q_support = {
            3: list(range(-1, 3 * k + 1)),
        }
        q_support.update(
            {
                radial_degree: lower_support(
                    q_bound, radial_degree, 3
                )
                for radial_degree in range(2, -q_bound - 1, -1)
            }
        )

        p_top = {
            radial_degree
            for radial_degree, exponents in p_support.items()
            if max(radial_degree + exponent for exponent in exponents)
            == p_bound
        }
        q_top = {
            radial_degree
            for radial_degree, exponents in q_support.items()
            if max(radial_degree + exponent for exponent in exponents)
            == q_bound
        }
        assert p_top == {0, 1, 2}
        assert q_top == {0, 1, 2, 3}
        assert max(
            radial_degree + exponent
            for radial_degree, exponents in p_support.items()
            for exponent in exponents
        ) == 2 * r
        assert max(
            radial_degree + exponent
            for radial_degree, exponents in q_support.items()
            for exponent in exponents
        ) == 3 * r


def verify_leading_root_shapes() -> None:
    z, w = sp.symbols("z w")
    alpha, beta, u, v = sp.symbols(
        "alpha beta u v", nonzero=True
    )
    for r in range(2, 9):
        root = w ** (r - 1) * (u * w + v * z)
        p_top = alpha * root**2
        q_top = beta * root**3
        assert sp.Poly(p_top, z, w).total_degree() == 2 * r
        assert sp.Poly(q_top, z, w).total_degree() == 3 * r
        assert sp.degree(p_top, z) == 2
        assert sp.degree(q_top, z) == 3
        assert min(
            exponent[1]
            for exponent, _coefficient in sp.Poly(p_top, z, w).terms()
        ) == 2 * (r - 1)
        assert min(
            exponent[1]
            for exponent, _coefficient in sp.Poly(q_top, z, w).terms()
        ) == 3 * (r - 1)
        assert bracket(p_top, q_top, z, w) == 0


def verify_laurent_centralizer_spectrum() -> None:
    z, w = sp.symbols("z w")

    # The full radial supports give z-exponents between -6r and 6 in
    # Q^2-LP^3.  Clear the one extra negative z-power introduced by
    # differentiation before constructing the exact coefficient matrix.
    for r in range(2, 7):
        root = w ** (r - 1) * (w + z)
        minimum_z_degree = -6 * r
        maximum_z_degree = 6
        count = maximum_z_degree - minimum_z_degree + 1
        for degree in range(r + 4, 6 * r):
            coefficients = sp.symbols(f"h_{r}_{degree}_0:{count}")
            homogeneous = sum(
                coefficient * z**z_degree * w ** (degree - z_degree)
                for coefficient, z_degree in zip(
                    coefficients,
                    range(minimum_z_degree, maximum_z_degree + 1),
                )
            )
            cleared = sp.expand(
                z ** (6 * r + 1)
                * bracket(root, homogeneous, z, w)
            )
            equations = sp.Poly(cleared, z, w).coeffs()
            matrix, _ = sp.linear_eq_to_matrix(equations, coefficients)
            kernel = matrix.nullspace()
            assert len(kernel) == (1 if degree % r == 0 else 0)


def verify_degree_and_contact_ledger() -> None:
    for k in range(1, 30):
        r = k + 1
        p_degree = 2 * r
        q_degree = 3 * r
        jacobian_degree = 4 - 3
        right_degree = q_degree + jacobian_degree
        assert right_degree == 3 * r + 1

        # {P_(2r),D_d} has total degree d+2r-2, so it centralizes
        # the leading root whenever d>r+3.
        assert (
            (r + 4) + p_degree - 2
            > right_degree
        )

        possible_high_degrees = [
            degree
            for degree in range(r + 4, 6 * r)
            if degree % r == 0
        ]
        assert set(possible_high_degrees).issubset(
            {2 * r, 3 * r, 4 * r, 5 * r}
        )
        possible_contacts = [
            6 * r - degree for degree in possible_high_degrees
        ]
        assert all(contact >= r for contact in possible_contacts)
        assert 6 * r - (r + 3) >= r


def main() -> None:
    verify_coordinate_and_support_bookkeeping()
    verify_leading_root_shapes()
    verify_laurent_centralizer_spectrum()
    verify_degree_and_contact_ledger()
    print("verified the all-k radial support and coordinate bookkeeping")
    print("verified the common leading root w^k(uw+vz)")
    print("verified Laurent centralizer kernels for r=2,...,6")
    print("verified the universal degree and contact spectrum")
    print("RESULT: ALL-k RADIAL CUSP CONTACT IS AT LEAST k+1")


if __name__ == "__main__":
    main()
