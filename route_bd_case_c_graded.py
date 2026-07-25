#!/usr/bin/env python3
"""Exact grade compression and certificates for the GGHV case-c branch.

Use z=x*y and retain y as the second coordinate.  The 61- and 125-point
supports become

    P = y^-1*z + sum_(d=0)^8 y^d p_d(z),
    Q = y^-1*z^2 + sum_(e=0)^12 y^e q_e(z).

Because dx wedge dy = y^-1 dz wedge dy, the coefficient of y^k in
[P,Q]_(x,y) is

    E_k = sum_(d+e=k) (e*p_d'(z)*q_e(z)-d*p_d(z)*q_e'(z)).

The grade -2 identity is the target z^2*y^-2=x^2.  The forced top edge
p_8=a(z-t)^8, q_12=b(z-t)^12 makes E_20 identically zero.  Thus the
remaining system consists of exactly the 21 identities E_-1,...,E_19=0.

This script verifies the reconstruction term by term, records the exact
descending linear-operator ranks, proves two characteristic-zero divisibility
consequences at the first descents, and verifies a four-row obstruction on a
29-parameter forced-edge-compatible full-Newton-polygon family.  It does not claim that these
partial algebraic-closure constraints eliminate the full case-c variety.
"""

from __future__ import annotations

from collections import defaultdict
from math import comb
from typing import Iterable, Sequence

import sympy as sp

import route_bd_verify as base


P_SUPPORT = base.lattice_points(base.C_P_VERTICES)
Q_SUPPORT = base.lattice_points(base.C_Q_VERTICES)


def grade_support(
    support: Iterable[tuple[int, int]],
) -> dict[int, tuple[int, ...]]:
    result: dict[int, list[int]] = defaultdict(list)
    for x_degree, y_degree in support:
        result[y_degree - x_degree].append(x_degree)
    return {
        grade: tuple(sorted(degrees))
        for grade, degrees in sorted(result.items())
    }


P_GRADES = grade_support(P_SUPPORT)
Q_GRADES = grade_support(Q_SUPPORT)


def p_degree_bound(grade: int) -> int:
    if grade == -1:
        return 1
    return grade + 2 if grade <= 5 else 8


def q_degree_bound(grade: int) -> int:
    if grade == -1:
        return 2
    return grade + 3 if grade <= 8 else 12


def verify_support_and_grade_reconstruction() -> dict[int, tuple[int, ...]]:
    assert len(P_SUPPORT) == 61
    assert len(Q_SUPPORT) == 125
    assert P_GRADES[-1] == (1,)
    assert Q_GRADES[-1] == (2,)
    assert all(
        P_GRADES[grade] == tuple(range(p_degree_bound(grade) + 1))
        for grade in range(9)
    )
    assert all(
        Q_GRADES[grade] == tuple(range(q_degree_bound(grade) + 1))
        for grade in range(13)
    )

    original_rows: set[tuple[int, int]] = set()
    rows_by_grade: dict[int, set[int]] = defaultdict(set)
    term_count = 0
    for u, v in P_SUPPORT:
        d = v - u
        for i, j in Q_SUPPORT:
            e = j - i
            original_determinant = u * j - v * i
            grade_determinant = e * u - d * i
            assert original_determinant == grade_determinant
            if not original_determinant:
                continue
            x_degree = u + i - 1
            y_degree = v + j - 1
            grade = d + e
            assert y_degree == x_degree + grade
            original_rows.add((x_degree, y_degree))
            rows_by_grade[grade].add(x_degree)
            term_count += 1

    assert len(original_rows) == 302
    assert term_count == 7141
    assert rows_by_grade[-2] == {2}
    assert sorted(rows_by_grade) == list(range(-2, 21))
    return {
        grade: tuple(sorted(degrees))
        for grade, degrees in sorted(rows_by_grade.items())
    }


ROWS_BY_GRADE = verify_support_and_grade_reconstruction()


def grade_identity_text(grade: int) -> str:
    return (
        f"E_{grade}(z)=sum_(d+e={grade}) "
        "(e*p_d'(z)*q_e(z)-d*p_d(z)*q_e'(z))=0"
    )


def descending_operator_inventory() -> list[dict[str, object]]:
    """Return exact ranks and compatibility rows in h=z-t coordinates.

    At grade k=12,...,19 the new unknowns are p_(k-12),q_(k-8).
    At k=8,...,11 only q_(k-8) is new.  With
    p_8=a*h^8,q_12=b*h^12, a monomial h^n in the new p contributes
    at h^(n+11) with multiplier 12*b*(n-r), while h^m in the new q
    contributes at h^(m+7) with multiplier 8*a*(s-m).

    Hence, in characteristic zero with a*b nonzero, the image is the
    coordinate span of the listed reachable h-degrees.  Its complement
    is an exact set of recursive compatibility conditions.
    """
    inventory = []
    for grade in range(19, 7, -1):
        p_grade = grade - 12
        q_grade = grade - 8
        variable_count = q_degree_bound(q_grade) + 1
        reachable = {
            degree + 7
            for degree in range(q_degree_bound(q_grade) + 1)
            if degree != q_grade
        }
        if p_grade >= 0:
            variable_count += p_degree_bound(p_grade) + 1
            reachable.update(
                degree + 11
                for degree in range(p_degree_bound(p_grade) + 1)
                if degree != p_grade
            )
        row_degrees = set(ROWS_BY_GRADE[grade])
        reachable.intersection_update(row_degrees)
        rank = len(reachable)
        inventory.append(
            {
                "grade": grade,
                "new_p_grade": p_grade if p_grade >= 0 else None,
                "new_q_grade": q_grade,
                "rows": len(row_degrees),
                "variables": variable_count,
                "rank": rank,
                "kernel_dimension": variable_count - rank,
                "compatibility_h_degrees": tuple(
                    sorted(row_degrees - reachable)
                ),
            }
        )
    expected = {
        19: (12, 10, 8),
        18: (12, 10, 8),
        17: (12, 9, 8),
        16: (11, 8, 9),
        15: (10, 7, 9),
        14: (9, 6, 10),
        13: (8, 5, 10),
        12: (7, 4, 10),
        11: (6, 1, 10),
        10: (5, 1, 10),
        9: (4, 1, 10),
        8: (3, 1, 10),
    }
    assert {
        item["grade"]: (
            item["rank"],
            item["kernel_dimension"],
            len(item["compatibility_h_degrees"]),
        )
        for item in inventory
    } == expected
    return inventory


def verify_forced_top_and_first_descents() -> dict[str, object]:
    """Prove h^4 divides p_7 from the first two compatibility steps."""
    h, a, b, lam = sp.symbols("h a b lambda", nonzero=True)
    coefficients = sp.symbols("c0:9")
    p7 = sum(coefficients[index] * h**index for index in range(9))
    p8 = a * h**8
    q12 = b * h**12
    assert sp.expand(
        12 * sp.diff(p8, h) * q12 - 8 * p8 * sp.diff(q12, h)
    ) == 0

    # The complete grade-19 solution.  The extra lambda*h^11 is the
    # resonant kernel monomial.
    q11 = sp.Rational(3, 2) * b / a * h**4 * p7 + lam * h**11
    grade19 = sp.expand(
        12 * sp.diff(p7, h) * q12
        - 7 * p7 * sp.diff(q12, h)
        + 11 * sp.diff(p8, h) * q11
        - 8 * p8 * sp.diff(q11, h)
    )
    assert grade19 == 0

    # At grade 18, new p_6,q_10 can reach only h-degrees >=7.
    # The forcing from p_7,q_11 therefore has to vanish at h^3,...,h^6.
    forcing18 = sp.expand(
        11 * sp.diff(p7, h) * q11
        - 7 * p7 * sp.diff(q11, h)
    )
    low18 = tuple(
        sp.factor(forcing18.coeff(h, degree))
        for degree in range(3, 7)
    )
    expected_low18 = (
        -42 * b / a * coefficients[0] ** 2,
        -78 * b / a * coefficients[0] * coefficients[1],
        -36
        * b
        / a
        * (2 * coefficients[0] * coefficients[2] + coefficients[1] ** 2),
        -66
        * b
        / a
        * (
            coefficients[0] * coefficients[3]
            + coefficients[1] * coefficients[2]
        ),
    )
    assert all(
        sp.simplify(actual - expected) == 0
        for actual, expected in zip(low18, expected_low18)
    )
    # Since a,b are nonzero in characteristic zero, degrees 3 and 5
    # successively force c0=c1=0: h^2 divides p_7.

    p7_h2 = sp.expand(
        p7.subs({coefficients[0]: 0, coefficients[1]: 0})
    )
    q11_h2 = sp.expand(
        q11.subs({coefficients[0]: 0, coefficients[1]: 0})
    )
    forcing18_h2 = sp.expand(
        11 * sp.diff(p7_h2, h) * q11_h2
        - 7 * p7_h2 * sp.diff(q11_h2, h)
    )

    # The h^7,...,h^10 part of grade 18 is controlled only by q_10;
    # p_6*q_12 starts at h^11.  Recover that low jet exactly.
    q10_low = 0
    for degree in range(4):
        q10_low += (
            -forcing18_h2.coeff(h, degree + 7)
            / (8 * a * (10 - degree))
            * h**degree
        )
    q10_low = sp.factor(q10_low)
    expected_q10_low = (
        sp.Rational(3, 8)
        * b
        / a**2
        * (
            coefficients[2] ** 2
            + 2 * coefficients[2] * coefficients[3] * h
            + (
                2 * coefficients[2] * coefficients[4]
                + coefficients[3] ** 2
            )
            * h**2
            + (
                2 * coefficients[2] * coefficients[5]
                + 2 * coefficients[3] * coefficients[4]
            )
            * h**3
        )
    )
    assert sp.simplify(q10_low - expected_q10_low) == 0

    # At grade 17, new p_5,q_9 again start at h^7.  Contributions from
    # p_6,q_11 start at h^5 before c2,c3 are eliminated, so coefficients
    # h^1 and then h^4 below are uncontaminated.  They force c2=c3=0.
    forcing17_low = sp.expand(
        10 * sp.diff(p7_h2, h) * q10_low
        - 7 * p7_h2 * sp.diff(q10_low, h)
    )
    h1 = sp.factor(forcing17_low.coeff(h, 1))
    h4_after_c2 = sp.factor(
        forcing17_low.subs({coefficients[2]: 0}).coeff(h, 4)
    )
    assert sp.simplify(
        h1
        - sp.Rational(15, 2)
        * b
        / a**2
        * coefficients[2] ** 3
    ) == 0
    assert sp.simplify(
        h4_after_c2
        - 6 * b / a**2 * coefficients[3] ** 3
    ) == 0
    # Hence h^4 divides p_7 over every characteristic-zero algebraic
    # extension.  This is not a finite-prime sampling statement.
    return {
        "grade19_q11": q11,
        "grade18_low_constraints": low18,
        "grade18_q10_low_jet": q10_low,
        "grade17_h1_constraint": h1,
        "grade17_h4_after_c2": h4_after_c2,
        "conclusion": "(z-t)^4 divides p_7(z)",
    }


def verify_z_leading_square_cube() -> dict[str, object]:
    """Verify the exact square/cube form of the z-leading coefficients.

    Only p_6,p_7,p_8 can have z-degree 8, and only q_9,...,q_12 can
    have z-degree 12.  If their leading coefficients are A(y),B(y),
    the z^19 part of the nonnegative-grade Jacobian is

        4*y*(2*A*B'-3*A'*B).

    Thus B^2/A^3 is constant.  Unique factorization, together with the
    nonzero endpoint coefficients, gives the displayed square/cube form.
    """
    y, a, b, s = sp.symbols("y a b s", nonzero=True)
    A = a * y**6 * (y - s) ** 2
    B = b * y**9 * (y - s) ** 3
    leading_equation = sp.expand(
        4 * y * (2 * A * sp.diff(B, y) - 3 * sp.diff(A, y) * B)
    )
    assert leading_equation == 0
    assert sp.expand(B**2 / (A**3)) == b**2 / a**3

    a_coefficients = tuple(
        sp.expand(A).coeff(y, degree) for degree in range(6, 9)
    )
    b_coefficients = tuple(
        sp.expand(B).coeff(y, degree) for degree in range(9, 13)
    )
    assert a_coefficients == (a * s**2, -2 * a * s, a)
    assert b_coefficients == (-b * s**3, 3 * b * s**2, -3 * b * s, b)
    return {
        "A": A,
        "B": B,
        "A_coefficients_y6_to_y8": a_coefficients,
        "B_coefficients_y9_to_y12": b_coefficients,
        "conclusion": (
            "lc_z(A)=a*y^6*(y-s)^2 and "
            "lc_z(B)=b*y^9*(y-s)^3, with a*b*s nonzero"
        ),
    }


def verify_grade16_compatibility() -> dict[str, object]:
    """Verify the next exact radical consequences of the descent.

    The top scalars are normalized to one; this is harmless for the
    high-grade subsystem because every term is bilinear in a p-block and
    a q-block.  After h^4|p_7, solve grades 18 and 17 diagonally for q_10
    and q_9.  The grade-16 cokernel rows then have the square factors
    asserted below.
    """
    h = sp.symbols("h")
    r = sp.symbols("r0:5")
    d = sp.symbols("d0:9")
    f = sp.symbols("f0:8")
    lambda11, lambda10, lambda9 = sp.symbols(
        "lambda11 lambda10 lambda9"
    )
    p7 = sum(r[index] * h ** (index + 4) for index in range(5))
    p6 = sum(d[index] * h**index for index in range(9))
    p5 = sum(f[index] * h**index for index in range(8))
    q12 = h**12
    q11 = sp.Rational(3, 2) * h**4 * p7 + lambda11 * h**11

    # The actual operator is diagonal in the h-monomial basis.  Given a
    # source, choose the resonant h^q_grade coefficient freely and solve
    # all other q coefficients; the p-block is kept as a kernel parameter.
    def solve_q(
        source: sp.Expr,
        p_grade: int,
        p_block: sp.Expr,
        q_grade: int,
        q_degree: int,
        resonant: sp.Symbol,
    ) -> sp.Expr:
        result = resonant * h**q_grade
        source = sp.expand(source)
        p_block = sp.expand(p_block)
        for m in range(q_degree + 1):
            if m == q_grade:
                continue
            output_degree = m + 7
            n = output_degree - 11
            p_term = 0
            if 0 <= n <= sp.degree(p_block, h):
                p_term = (
                    12
                    * (n - p_grade)
                    * p_block.coeff(h, n)
                )
            result += (
                -source.coeff(h, output_degree) - p_term
            ) / (8 * (q_grade - m)) * h**m
        return sp.expand(result)

    source18 = sp.expand(
        11 * sp.diff(p7, h) * q11
        - 7 * p7 * sp.diff(q11, h)
    )
    q10 = solve_q(source18, 6, p6, 10, 12, lambda10)
    equation18 = sp.expand(
        source18
        + 12 * h**12 * sp.diff(p6, h)
        - 72 * h**11 * p6
        + 80 * h**7 * q10
        - 8 * h**8 * sp.diff(q10, h)
    )
    assert equation18 == 0

    source17 = sp.expand(
        10 * sp.diff(p7, h) * q10
        - 7 * p7 * sp.diff(q10, h)
        + 11 * sp.diff(p6, h) * q11
        - 6 * p6 * sp.diff(q11, h)
    )
    q9 = solve_q(source17, 5, p5, 9, 12, lambda9)
    equation17 = sp.expand(
        source17
        + 12 * h**12 * sp.diff(p5, h)
        - 60 * h**11 * p5
        + 72 * h**7 * q9
        - 8 * h**8 * sp.diff(q9, h)
    )
    assert equation17 == 0

    source16 = sp.expand(
        9 * sp.diff(p7, h) * q9
        - 7 * p7 * sp.diff(q9, h)
        + 10 * sp.diff(p6, h) * q10
        - 6 * p6 * sp.diff(q10, h)
        + 11 * sp.diff(p5, h) * q11
        - 5 * p5 * sp.diff(q11, h)
    )
    c3 = sp.factor(source16.coeff(h, 3))
    c4 = sp.factor(source16.coeff(h, 4))
    c5 = sp.factor(source16.coeff(h, 5))
    c6 = sp.factor(source16.coeff(h, 6))
    c19 = sp.factor(source16.coeff(h, 19))

    first_relation = {d[0]: r[0] ** 2 / 4}
    second_relation = {
        **first_relation,
        d[1]: r[0] * r[1] / 2,
    }
    assert sp.simplify(
        c3 + sp.Rational(9, 4) * (4 * d[0] - r[0] ** 2) ** 2
    ) == 0
    assert sp.simplify(
        c4
        + sp.Rational(33, 4)
        * (4 * d[0] - r[0] ** 2)
        * (2 * d[1] - r[0] * r[1])
    ) == 0
    assert sp.simplify(
        c5.subs(first_relation)
        + sp.Rational(15, 2)
        * (2 * d[1] - r[0] * r[1]) ** 2
    ) == 0
    c6_after_relations = sp.factor(c6.subs(second_relation))
    assert c6_after_relations == (
        -sp.Rational(693, 128) * lambda11 * r[0] ** 3
    )
    assert sp.simplify(
        c19 - sp.Rational(3, 4) * (4 * d[8] - r[4] ** 2) ** 2
    ) == 0
    return {
        "relations": (
            "d0=r0^2/4, d1=r0*r1/2, d8=r4^2/4, "
            "r0^3*lambda11=0"
        ),
        "compatibility_coefficients": {
            3: c3,
            4: c4,
            5: c5,
            6: c6,
            19: c19,
        },
    }


def verify_square_cube_endgame() -> dict[str, object]:
    """Record the exact PDE for a possible global square/cube closure.

    If the descent eventually proves P=x+H^2 and Q=x^2*y+H^3, the
    remaining Jacobian equation is the PDE recorded here.  Comparing
    y-degrees shows a polynomial solution has y-degree at most one.
    Writing H=a(x)y+b(x), the two coefficient equations then have only
    H constant or H=2*x*y/3 as polynomial solutions.  Neither can have
    the required case-c Newton vertices.  The recursive descent has not
    yet proved the square/cube hypothesis, so this is an endgame lemma,
    not an elimination of case c.
    """
    x, y = sp.symbols("x y")
    H = sp.Function("H")(x, y)
    P = x + H**2
    Q = x**2 * y + H**3
    jacobian = sp.expand(
        sp.diff(P, x) * sp.diff(Q, y)
        - sp.diff(P, y) * sp.diff(Q, x)
    )
    pde = (
        2 * x**2 * sp.diff(H, x)
        + (3 * H - 4 * x * y) * sp.diff(H, y)
    )
    assert sp.simplify(jacobian - x**2 - H * pde) == 0

    a = sp.Function("a")(x)
    b = sp.Function("b")(x)
    linear_H = a * y + b
    linear_pde = sp.Poly(
        sp.expand(
            2 * x**2 * sp.diff(linear_H, x)
            + (3 * linear_H - 4 * x * y) * sp.diff(linear_H, y)
        ),
        y,
    )
    y_equation = sp.factor(linear_pde.coeff_monomial(y))
    constant_equation = sp.factor(linear_pde.coeff_monomial(1))
    assert y_equation == 3 * a**2 - 4 * x * a + 2 * x**2 * sp.diff(a, x)
    assert constant_equation == 3 * a * b + 2 * x**2 * sp.diff(b, x)

    for polynomial_H in (sp.Integer(1), sp.Rational(2, 3) * x * y):
        assert sp.expand(
            2 * x**2 * sp.diff(polynomial_H, x)
            + (3 * polynomial_H - 4 * x * y)
            * sp.diff(polynomial_H, y)
        ) == 0
    return {
        "pde": "2*x^2*H_x+(3*H-4*x*y)*H_y=0",
        "polynomial_solutions": "H=constant or H=2*x*y/3",
        "scope": "conditional on a global P=x+H^2, Q=x^2*y+H^3 closure",
    }


def coefficient_matrix_for_fixed_p(
    p_coefficients: dict[tuple[int, int], sp.Expr],
) -> tuple[list[tuple[int, int]], sp.Matrix]:
    rows = sorted(base.equation_inventory(P_SUPPORT, Q_SUPPORT))
    matrix = sp.zeros(len(rows), len(Q_SUPPORT))
    for row_index, row in enumerate(rows):
        for column, (i, j) in enumerate(Q_SUPPORT):
            matrix[row_index, column] = sp.expand(
                sum(
                    (u * j - v * i) * coefficient
                    for (u, v), coefficient in p_coefficients.items()
                    if (u + i - 1, v + j - 1) == row
                )
            )
    return rows, matrix


def verify_four_row_full_polygon_family() -> dict[str, object]:
    """Verify a rational certificate on a 29-parameter full-P family."""
    a, c, t = sp.symbols("a c t", nonzero=True)
    p_coefficients: dict[tuple[int, int], sp.Expr] = {
        (0, 0): 1,
        (1, 0): 1,
        (8, 14): c,
    }
    for degree in range(9):
        p_coefficients[(degree, degree + 8)] = (
            p_coefficients.get((degree, degree + 8), 0)
            + a * comb(8, degree) * (-t) ** (8 - degree)
        )
    required_vertices = ((0, 0), (1, 0), (8, 14), (8, 16), (0, 8))
    assert all(sp.simplify(p_coefficients[vertex]) != 0 for vertex in required_vertices)

    covector = {
        (2, 0): sp.Integer(1),
        (0, 7): sp.Rational(9, 16) / (a * t**9),
        (1, 8): sp.Rational(1, 16) / (a * t**8),
        (0, 16): sp.Rational(9, 128) / (a**2 * t**16),
    }
    pairings = []
    for i, j in Q_SUPPORT:
        pairing = 0
        for (u, v), coefficient in p_coefficients.items():
            row = (u + i - 1, v + j - 1)
            pairing += (
                covector.get(row, 0)
                * (u * j - v * i)
                * coefficient
            )
        pairings.append(sp.factor(pairing))
    assert not any(pairings)
    assert covector[(2, 0)] == 1

    # Determine every individual P perturbation that this same covector
    # annihilates when a=t=1.  There are 36; their span, together with the
    # base x+y^8(z-1)^8 direction, gives a 37-dimensional kernel.
    numeric_covector = {
        row: sp.simplify(value.subs({a: 1, t: 1}))
        for row, value in covector.items()
    }
    residual = sp.Matrix(
        [
            [
                numeric_covector.get((u + i - 1, v + j - 1), 0)
                * (u * j - v * i)
                for u, v in P_SUPPORT
            ]
            for i, j in Q_SUPPORT
        ]
    )
    residual_rank = residual.rank()
    assert residual_rank == 24
    assert len(P_SUPPORT) - residual_rank == 37
    individually_free = tuple(
        P_SUPPORT[column]
        for column in range(len(P_SUPPORT))
        if not any(residual[:, column])
    )
    assert len(individually_free) == 36
    assert (8, 14) in individually_free
    assert (0, 0) in individually_free
    forced_edge_compatible_free = tuple(
        point
        for point in individually_free
        if point[1] - point[0] != 8
    )
    # Seven individually-free grade-8 monomials would deform
    # a*(z-t)^8 and therefore are excluded from the forced-edge family.
    assert len(forced_edge_compatible_free) == 29

    # Exact characteristic-zero fixed-P rank check at a=c=t=1.
    numeric_p = {
        point: sp.expand(sp.sympify(value).subs({a: 1, c: 1, t: 1}))
        for point, value in p_coefficients.items()
    }
    rows, matrix = coefficient_matrix_for_fixed_p(numeric_p)
    target = sp.Matrix([int(row == (2, 0)) for row in rows])
    rank = matrix.rank()
    augmented_rank = matrix.row_join(target).rank()
    assert (rank, augmented_rank) == (124, 125)
    return {
        "family": (
            "P=x+a*y^8*(xy-t)^8 plus arbitrary linear combinations "
            "of the 29 forced-edge-compatible free monomials"
        ),
        "covector": covector,
        "individual_free_monomials": individually_free,
        "forced_edge_compatible_free_monomials": (
            forced_edge_compatible_free
        ),
        "forced_edge_family_parameter_count": 29,
        "certificate_kernel_dimension_at_a_t_1": 37,
        "fixed_p_rank": rank,
        "fixed_p_augmented_rank": augmented_rank,
    }


def main() -> None:
    print(
        "case-c exact reconstruction: |S_P|=61, |S_Q|=125, "
        "Jacobian rows=302, nonzero terms=7141"
    )
    print(
        "grade -2 is the target; forced E_20=0; remaining identities: "
        "E_-1,...,E_19 (21 identities)"
    )
    print(
        "bottom identity E_-1: z*q_0'(z)-z^2*p_0'(z)=0, "
        "equivalently q_0'=z*p_0'"
    )
    inventory = descending_operator_inventory()
    for item in inventory:
        print(
            "recursive block "
            f"k={item['grade']}: new p={item['new_p_grade']}, "
            f"new q={item['new_q_grade']}, rank={item['rank']}, "
            f"kernel={item['kernel_dimension']}, "
            "compatibility h-degrees="
            f"{item['compatibility_h_degrees']}"
        )
    descent = verify_forced_top_and_first_descents()
    print("algebraic-closure descent:", descent["conclusion"])
    leading = verify_z_leading_square_cube()
    print("z-leading square/cube lemma:", leading["conclusion"])
    grade16 = verify_grade16_compatibility()
    print("grade-16 radical consequences:", grade16["relations"])
    endgame = verify_square_cube_endgame()
    print(
        "conditional square/cube endgame:",
        endgame["polynomial_solutions"],
    )
    family = verify_four_row_full_polygon_family()
    print("four-row family certificate:", family["covector"])
    print(
        "certificate-valid P kernel dimension at a=t=1:",
        family["certificate_kernel_dimension_at_a_t_1"],
    )
    print(
        "forced-edge-compatible free P monomials:",
        family["forced_edge_family_parameter_count"],
    )
    print(
        "exact Q-rank for P=1+x+x^8*y^14+y^8*(xy-1)^8: "
        f"{family['fixed_p_rank']}; augmented rank="
        f"{family['fixed_p_augmented_rank']}"
    )
    print("RESULT: ALL EXACT CASE-C GRADED CHECKS PASS")
    print(
        "SCOPE: recursive compression and a large full-polygon family "
        "obstruction only; the unrestricted 61+125 variety remains open"
    )


if __name__ == "__main__":
    main()
