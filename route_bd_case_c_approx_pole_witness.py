#!/usr/bin/env python3
"""Exact pole witnesses for the next case-c approximate-root coefficients.

The upper case-c identities E_12,...,E_20 do *not* force the remaining
coefficients of H=(P**(1/2))_+ to be polynomial in h=z-t.

Two explicit characteristic-zero pairs are checked directly:

1. A full-vertex upper-grade solution with [y]H=1/(2*h**2).
2. A full-vertex upper-grade solution with [y]H=0 but [1]H=1/(2*h**2).

Thus neither proposed h^4 divisibility follows from grades 12,...,20,
including the grade-13 and grade-12 compatibility equations.  Lower grades
could still eliminate these upper-grade fibers; this file makes no claim
about E_11,...,E_-1.
"""

from __future__ import annotations

from math import comb

import sympy as sp

import route_bd_case_c_graded as support_data


h, y = sp.symbols("h y")


def grade_identity(
    p: dict[int, sp.Expr],
    q: dict[int, sp.Expr],
    grade: int,
) -> sp.Expr:
    return sp.expand(
        sum(
            q_grade * sp.diff(p[p_grade], h) * q[q_grade]
            - p_grade
            * p[p_grade]
            * sp.diff(q[q_grade], h)
            for p_grade in p
            for q_grade in q
            if p_grade + q_grade == grade
        )
    )


def approximate_square_root(
    p: dict[int, sp.Expr],
) -> dict[int, sp.Expr]:
    """Return coefficients of H=h^4*y^4+... with P-H^2 of degree <=3."""
    coefficients: dict[int, sp.Expr] = {4: h**4}
    coefficients[3] = sp.cancel(p[7] / (2 * coefficients[4]))
    coefficients[2] = sp.cancel(
        (p[6] - coefficients[3] ** 2) / (2 * coefficients[4])
    )
    coefficients[1] = sp.cancel(
        (
            p[5]
            - 2 * coefficients[3] * coefficients[2]
        )
        / (2 * coefficients[4])
    )
    coefficients[0] = sp.cancel(
        (
            p[4]
            - coefficients[2] ** 2
            - 2 * coefficients[3] * coefficients[1]
        )
        / (2 * coefficients[4])
    )
    H = sum(
        coefficient * y**degree
        for degree, coefficient in coefficients.items()
    )
    P = sum(p[grade] * y**grade for grade in range(9))
    assert sp.Poly(sp.together(P - H**2), y).degree() <= 3
    return coefficients


def verify_support_bounds(
    p: dict[int, sp.Expr],
    q: dict[int, sp.Expr],
) -> None:
    for grade in range(9):
        assert sp.Poly(p[grade], h).degree() <= (
            grade + 2 if grade <= 5 else 8
        )
    for grade in range(13):
        assert sp.Poly(q[grade], h).degree() <= (
            grade + 3 if grade <= 8 else 12
        )

    # With h=z-1, these are exactly the five case-c vertices on each
    # required polygon.  Constants at z=0 are obtained by h=-1.
    assert p[0].subs(h, -1) != 0
    assert sp.LC(sp.Poly(p[6], h)) != 0
    assert sp.LC(sp.Poly(p[8], h)) != 0
    assert p[8].subs(h, -1) != 0
    assert q[0].subs(h, -1) != 0
    assert sp.LC(sp.Poly(q[9], h)) != 0
    assert sp.LC(sp.Poly(q[12], h)) != 0
    assert q[12].subs(h, -1) != 0


def common_p() -> dict[int, sp.Expr]:
    return {
        -1: h + 1,
        0: sp.Integer(1),
        1: sp.Integer(0),
        2: sp.Integer(0),
        3: sp.Integer(0),
        4: sp.Integer(0),
        5: sp.Integer(0),
        6: sp.Rational(1, 4) * h**8,
        7: h**8,
        8: h**8,
    }


def common_q() -> dict[int, sp.Expr]:
    return {
        -1: (h + 1) ** 2,
        0: sp.Integer(1),
        1: sp.Integer(0),
        2: sp.Integer(0),
        3: sp.Integer(0),
        4: sp.Integer(0),
        5: sp.Integer(0),
        6: sp.Integer(0),
        7: sp.Integer(0),
        8: sp.Integer(0),
        9: sp.Rational(1, 8) * h**12,
        10: sp.Rational(3, 4) * h**12,
        11: sp.Rational(3, 2) * h**12,
        12: h**12,
    }


def y_coefficient_pole_witness() -> tuple[
    dict[int, sp.Expr], dict[int, sp.Expr], dict[int, sp.Expr]
]:
    p = common_p()
    p[5] = h**2
    q = common_q()
    q.update(
        {
            4: sp.Rational(3, 32),
            5: -sp.Rational(3, 16),
            6: sp.Rational(3, 8),
            8: sp.Rational(3, 4) * h**6,
            9: sp.Rational(1, 8) * h**12
            + sp.Rational(3, 2) * h**6,
        }
    )
    verify_support_bounds(p, q)
    assert all(
        grade_identity(p, q, grade) == 0
        for grade in range(12, 21)
    )
    H = approximate_square_root(p)
    assert H[3] == h**4 / 2
    assert H[2] == 0
    assert H[1] == 1 / (2 * h**2)
    # The proposed numerator is p5-2*H3*H2=h^2, not h^4-divisible.
    assert p[5] - 2 * H[3] * H[2] == h**2
    return p, q, H


def constant_coefficient_pole_witness() -> tuple[
    dict[int, sp.Expr], dict[int, sp.Expr], dict[int, sp.Expr]
]:
    p = common_p()
    p[4] = h**2
    q = common_q()
    q.update(
        {
            4: sp.Rational(3, 8),
            7: sp.Rational(3, 4) * h**6,
            8: sp.Rational(3, 2) * h**6,
        }
    )
    verify_support_bounds(p, q)
    assert all(
        grade_identity(p, q, grade) == 0
        for grade in range(12, 21)
    )
    H = approximate_square_root(p)
    assert H[3] == h**4 / 2
    assert H[2] == 0
    assert H[1] == 0
    assert H[0] == 1 / (2 * h**2)
    # Even after the y coefficient is polynomial, the next numerator is
    # p4-H2^2-2*H3*H1=h^2, again not h^4-divisible.
    assert p[4] - H[2] ** 2 - 2 * H[3] * H[1] == h**2
    return p, q, H


def fixed_p_partner_ranks(p: dict[int, sp.Expr]) -> tuple[int, int]:
    """Return exact full-system ranks for the P underlying a witness."""
    z = sp.symbols("z")
    coefficients: dict[tuple[int, int], sp.Expr] = {(1, 0): 1}
    for grade in range(9):
        polynomial = sp.Poly(sp.expand(p[grade].subs(h, z - 1)), z)
        for (z_degree,), coefficient in polynomial.terms():
            point = (z_degree, z_degree + grade)
            coefficients[point] = (
                coefficients.get(point, 0) + coefficient
            )
    rows, matrix = support_data.coefficient_matrix_for_fixed_p(coefficients)
    target = sp.Matrix([int(row == (2, 0)) for row in rows])
    return (
        matrix.to_DM().rank(),
        matrix.row_join(target).to_DM().rank(),
    )


def forced_edge_extension_ranks(
    p: dict[int, sp.Expr],
    threshold: int,
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
    """Test extension through all grades at least ``threshold``.

    The q_12 block is constrained to B*(z-1)^12, but B is initially
    free.  The three returned rank pairs concern the free-B system,
    its B=0 slice, and its B=1 slice.  Thus equality only on B=0 proves
    that the middle-grade equations kill the required nonzero edge.
    """
    z = sp.symbols("z")
    coefficients: dict[tuple[int, int], sp.Expr] = {(1, 0): 1}
    for grade in range(9):
        polynomial = sp.Poly(sp.expand(p[grade].subs(h, z - 1)), z)
        for (z_degree,), coefficient in polynomial.terms():
            point = (z_degree, z_degree + grade)
            coefficients[point] = (
                coefficients.get(point, 0) + coefficient
            )
    rows, matrix = support_data.coefficient_matrix_for_fixed_p(coefficients)
    q_support = list(support_data.Q_SUPPORT)
    selected_rows = [
        index
        for index, (x_degree, y_degree) in enumerate(rows)
        if y_degree - x_degree >= threshold
    ]
    equations = matrix[selected_rows, :]
    right_hand_side = sp.zeros(len(selected_rows), 1)

    # The target row fixes the base coefficient [x^2*y]Q=1.
    base_row = sp.zeros(1, len(q_support))
    base_row[0, q_support.index((2, 1))] = 1
    equations = equations.col_join(base_row)
    right_hand_side = right_hand_side.col_join(sp.Matrix([1]))

    # Eliminate the scalar B by expressing the other twelve edge
    # coefficients through the leading z^12 coefficient.
    leading_column = q_support.index((12, 24))
    for z_degree in range(12):
        edge_row = sp.zeros(1, len(q_support))
        edge_row[0, q_support.index((z_degree, z_degree + 12))] = 1
        edge_row[0, leading_column] = (
            -comb(12, z_degree) * (-1) ** (12 - z_degree)
        )
        equations = equations.col_join(edge_row)
        right_hand_side = right_hand_side.col_join(sp.Matrix([0]))

    def ranks(
        extra_value: int | None,
    ) -> tuple[int, int]:
        sliced_equations = equations
        sliced_right_hand_side = right_hand_side
        if extra_value is not None:
            scalar_row = sp.zeros(1, len(q_support))
            scalar_row[0, leading_column] = 1
            sliced_equations = sliced_equations.col_join(scalar_row)
            sliced_right_hand_side = sliced_right_hand_side.col_join(
                sp.Matrix([extra_value])
            )
        return (
            sliced_equations.to_DM().rank(),
            sliced_equations.row_join(
                sliced_right_hand_side
            ).to_DM().rank(),
        )

    return ranks(None), ranks(0), ranks(1)


def main() -> None:
    # Importing the prior verifier also checks that these dictionaries use
    # precisely the reconstructed 61+125 support bounds.
    assert len(support_data.P_SUPPORT) == 61
    assert len(support_data.Q_SUPPORT) == 125
    p1, q1, H1 = y_coefficient_pole_witness()
    p2, q2, H2 = constant_coefficient_pole_witness()
    ranks1 = fixed_p_partner_ranks(p1)
    ranks2 = fixed_p_partner_ranks(p2)
    assert ranks1 == (124, 125)
    assert ranks2 == (124, 125)
    # Witness 1 extends through E_12 but E_11 forces its top-edge scalar
    # B to vanish.  Witness 2 extends through E_9, while E_8 forces B=0.
    middle1 = forced_edge_extension_ranks(p1, 11)
    middle2 = forced_edge_extension_ranks(p2, 8)
    assert middle1 == ((105, 105), (105, 105), (105, 106))
    assert middle2 == ((120, 120), (120, 120), (120, 121))
    print("exact full-vertex upper-grade witness 1: E_12,...,E_20=0")
    print("[y]H =", H1[1])
    print(
        "witness-1 q4,...,q12 =",
        tuple(q1[grade] for grade in range(4, 13)),
    )
    print("exact full-vertex upper-grade witness 2: E_12,...,E_20=0")
    print("[y]H =", H2[1], "; [1]H =", H2[0])
    print(
        "witness-2 q4,...,q12 =",
        tuple(q2[grade] for grade in range(4, 13)),
    )
    print(
        "full fixed-P Q ranks (matrix, augmented):",
        ranks1,
        ranks2,
    )
    print(
        "middle-grade forced-edge ranks "
        "(free B, B=0, B=1):",
        middle1,
        middle2,
    )
    print("RESULT: BOTH PROPOSED UPPER-GRADE DIVISIBILITIES ARE FALSE")
    print(
        "SCOPE: lower identities E_11,...,E_-1 may still eliminate "
        "these exact high-grade fibers"
    )


if __name__ == "__main__":
    main()
