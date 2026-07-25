#!/usr/bin/env python3
"""Next exact characteristic-zero descent lemmas for GGHV case c.

This continues ``route_bd_case_c_graded.py``.  No finite-field sampling is
used.  All calculations take place over

    Q(a,b)[h, coefficient parameters],  h=z-t,

with a,b,t and the required vertex coefficients nonzero.

The main new universal conclusions are:

* the vertical Newton-edge coefficients are powers of one linear form;
* if p_7=h^4*r, then

      p_6 - r^2/(4*a)

  is divisible by h^2 and has degree at most seven;
* the grade-19 resonant parameter in q_11 vanishes;
* the required q_9 leading coefficient is forced and nonzero.

The file also proves that the explicit p_-1/q_12 cross term at grade 11
lies wholly in the new-q_3 operator image, so that term alone cannot be
the desired contradiction.
"""

from __future__ import annotations

from math import comb

import sympy as sp

import route_bd_case_c_graded as previous


def vertical_edge_power_theorem() -> dict[str, sp.Expr]:
    """Solve the z-leading edge identity over an algebraic closure."""
    y = sp.symbols("y")
    a, b, c, u = sp.symbols("a b c u", nonzero=True)
    v, w, xi = sp.symbols("v w xi")
    R = u + c * y + a * y**2
    S = v + w * y + xi * y**2 + b * y**3
    edge_identity = sp.Poly(
        sp.expand(2 * R * sp.diff(S, y) - 3 * sp.diff(R, y) * S),
        y,
    )
    solution = {
        u: c**2 / (4 * a),
        xi: 3 * b * c / (2 * a),
        w: 3 * b * c**2 / (4 * a**2),
        v: b * c**3 / (8 * a**3),
    }
    assert sp.expand(edge_identity.as_expr().subs(solution)) == 0
    assert sp.expand(
        R.subs(solution) - a * (y + c / (2 * a)) ** 2
    ) == 0
    assert sp.expand(
        S.subs(solution) - b * (y + c / (2 * a)) ** 3
    ) == 0

    # Conversely, solve every coefficient equation.  Division by a is
    # legitimate because it is a required top vertex.  The resulting
    # u=c^2/(4a), together with the required nonzero p_6 vertex u, also
    # proves c is nonzero.
    equations = edge_identity.all_coeffs()
    solved = sp.solve(equations, (u, v, w, xi), dict=True)
    assert solved == [
        {
            u: solution[u],
            v: solution[v],
            w: solution[w],
            xi: solution[xi],
        }
    ]
    return {
        "p6_lead": solution[u],
        "q11_lead": solution[xi],
        "q10_lead": solution[w],
        "q9_lead": solution[v],
    }


class DescendingRecurrence:
    """Coefficientwise exact solver for one descending grade at a time."""

    def __init__(self) -> None:
        self.h = sp.symbols("h")
        self.a, self.b = sp.symbols("a b", nonzero=True)
        self.p: dict[int, sp.Expr] = {8: self.a * self.h**8}
        self.q: dict[int, sp.Expr] = {12: self.b * self.h**12}

    def substitute(self, substitutions: dict[sp.Symbol, sp.Expr]) -> None:
        self.p = {
            grade: sp.expand(poly.subs(substitutions))
            for grade, poly in self.p.items()
        }
        self.q = {
            grade: sp.expand(poly.subs(substitutions))
            for grade, poly in self.q.items()
        }

    def bracket_term(self, p_grade: int, q_grade: int) -> sp.Expr:
        h = self.h
        return sp.expand(
            q_grade * sp.diff(self.p[p_grade], h) * self.q[q_grade]
            - p_grade
            * self.p[p_grade]
            * sp.diff(self.q[q_grade], h)
        )

    def introduce(
        self, grade: int
    ) -> tuple[tuple[tuple[int, sp.Expr], ...], dict[sp.Symbol, sp.Expr]]:
        """Solve the reachable coefficients and return compatibility rows."""
        p_grade = grade - 12 if grade >= 12 else None
        q_grade = grade - 8
        p_coefficients: tuple[sp.Symbol, ...] = ()
        if p_grade is not None:
            p_coefficients = sp.symbols(
                f"p{p_grade}_0:{previous.p_degree_bound(p_grade) + 1}"
            )
            self.p[p_grade] = sum(
                coefficient * self.h**degree
                for degree, coefficient in enumerate(p_coefficients)
            )
        q_coefficients = sp.symbols(
            f"q{q_grade}_0:{previous.q_degree_bound(q_grade) + 1}"
        )
        self.q[q_grade] = sum(
            coefficient * self.h**degree
            for degree, coefficient in enumerate(q_coefficients)
        )

        forcing = 0
        for known_p_grade in tuple(self.p):
            known_q_grade = grade - known_p_grade
            if (
                known_q_grade in self.q
                and known_p_grade != p_grade
                and known_q_grade != q_grade
            ):
                forcing += self.bracket_term(
                    known_p_grade, known_q_grade
                )
        forcing = sp.expand(forcing)

        solved: dict[sp.Symbol, sp.Expr] = {}
        compatibility: list[tuple[int, sp.Expr]] = []
        for h_degree in range(25):
            p_index = h_degree - 11
            q_index = h_degree - 7
            p_multiplier = 0
            if (
                p_grade is not None
                and 0 <= p_index < len(p_coefficients)
            ):
                p_multiplier = (
                    12 * self.b * (p_index - p_grade)
                )
            q_multiplier = 0
            if 0 <= q_index < len(q_coefficients):
                q_multiplier = 8 * self.a * (q_grade - q_index)
            right_hand_side = sp.expand(
                -forcing.coeff(self.h, h_degree)
            ).subs(solved)
            if q_multiplier:
                p_term = (
                    p_multiplier * p_coefficients[p_index]
                    if p_multiplier
                    else 0
                )
                solved[q_coefficients[q_index]] = sp.cancel(
                    (right_hand_side - p_term) / q_multiplier
                )
            elif p_multiplier:
                solved[p_coefficients[p_index]] = sp.cancel(
                    right_hand_side / p_multiplier
                )
            elif right_hand_side != 0:
                compatibility.append(
                    (h_degree, sp.cancel(-right_hand_side))
                )
        self.substitute(solved)
        return tuple(compatibility), solved


def universal_next_descent() -> dict[str, object]:
    recurrence = DescendingRecurrence()
    h, a, b = recurrence.h, recurrence.a, recurrence.b

    compatibility19, _ = recurrence.introduce(19)
    assert not compatibility19
    p7_coefficients = sp.symbols("p7_0:9")
    q11_resonant_coefficient = sp.symbols("q11_11")
    resonance = sp.symbols("lambda")

    compatibility18, _ = recurrence.introduce(18)
    by_degree18 = dict(compatibility18)
    assert sp.factor(by_degree18[3]) == -42 * b / a * p7_coefficients[0] ** 2
    recurrence.substitute(
        {p7_coefficients[0]: 0, p7_coefficients[1]: 0}
    )

    compatibility17, _ = recurrence.introduce(17)
    by_degree17 = dict(compatibility17)
    assert sp.factor(by_degree17[1]) == (
        sp.Rational(15, 2)
        * b
        / a**2
        * p7_coefficients[2] ** 3
    )
    recurrence.substitute(
        {p7_coefficients[2]: 0, p7_coefficients[3]: 0}
    )

    compatibility16, _ = recurrence.introduce(16)
    by_degree16 = dict(compatibility16)
    r = p7_coefficients[4:]
    p6_coefficients = sp.symbols("p6_0:9")
    assert sp.simplify(
        by_degree16[3]
        - (
            -sp.Rational(9, 4)
            * b
            / a**3
            * (-4 * a * p6_coefficients[0] + r[0] ** 2) ** 2
        )
    ) == 0
    substitutions16 = {
        p6_coefficients[0]: r[0] ** 2 / (4 * a),
        p6_coefficients[1]: r[0] * r[1] / (2 * a),
        p6_coefficients[8]: r[4] ** 2 / (4 * a),
        q11_resonant_coefficient: (
            3 * b * r[3] / (2 * a) + resonance
        ),
    }
    assert sp.simplify(
        by_degree16[6].subs(substitutions16)
        - (
            -sp.Rational(693, 128)
            * resonance
            * r[0] ** 3
            / a**2
        )
    ) == 0
    recurrence.substitute(substitutions16)

    # Grade 15 supplies the other endpoint of the resonance obstruction.
    compatibility15, _ = recurrence.introduce(15)
    by_degree15 = dict(compatibility15)
    assert sp.simplify(
        by_degree15[18]
        - (
            -sp.Rational(77, 1024)
            * resonance
            * r[4] ** 4
            / a**3
        )
    ) == 0

    # The p_6 vertex is nonzero.  From p6_8=r4^2/(4a), r4 is nonzero;
    # hence the grade-15 equation forces the resonance to vanish.
    defect = sp.expand(
        recurrence.p[6]
        - sum(r[index] * h**index for index in range(5)) ** 2
        / (4 * a)
    )
    # recurrence.p[6] has already received the substitutions above.
    assert defect.coeff(h, 0) == 0
    assert defect.coeff(h, 1) == 0
    assert defect.coeff(h, 8) == 0

    # q9_12 was solved at grade 17.  Substitute the forced p6 leading
    # coefficient and simplify the exact expression.
    q9_leading = sp.factor(
        recurrence.q[9].coeff(h, 12).subs(
            {
                p6_coefficients[8]: r[4] ** 2 / (4 * a),
                resonance: 0,
            }
        )
    )
    assert q9_leading == b * r[4] ** 3 / (8 * a**3)
    return {
        "p7_form": "p7=h^4*r, deg(r)=4 and lead(r)!=0",
        "p6_defect": "h^2 divides p6-r^2/(4a), and its degree is <=7",
        "q11_resonance": "lambda=0",
        "q9_leading": q9_leading,
        "grade16_compatibility": compatibility16,
        "grade15_compatibility": compatibility15,
    }


def grade11_cross_term_test() -> dict[str, sp.Expr]:
    """Show the p_-1/q_12 cross term is reachable, not contradictory."""
    h, a, b, t = sp.symbols("h a b t", nonzero=True)
    p_minus_one = h + t
    q12 = b * h**12
    cross_term = sp.expand(
        12 * sp.diff(p_minus_one, h) * q12
        + p_minus_one * sp.diff(q12, h)
    )
    assert cross_term == 12 * b * t * h**11 + 24 * b * h**12

    # At grade 11 the new q_3 block is
    # 8*a*h^7*(3*q_3-h*q_3').  Its h^4,h^5 coefficients cancel the
    # two cross-term monomials exactly.
    q3_piece = (
        sp.Rational(3, 2) * b * t / a * h**4
        + sp.Rational(3, 2) * b / a * h**5
    )
    operator = sp.expand(
        8 * a * h**7 * (3 * q3_piece - h * sp.diff(q3_piece, h))
    )
    assert sp.expand(operator + cross_term) == 0
    reachable = next(
        item
        for item in previous.descending_operator_inventory()
        if item["grade"] == 11
    )
    assert 11 not in reachable["compatibility_h_degrees"]
    assert 12 not in reachable["compatibility_h_degrees"]
    return {
        "cross_term": cross_term,
        "canceling_q3_piece": q3_piece,
        "conclusion": (
            "the base/top grade-11 cross term lies in the q3 image; "
            "it cannot by itself force a contradiction"
        ),
    }


def explicit_high_grade_skeleton() -> dict[str, object]:
    """Exhibit a full-vertex solution of every identity E_8,...,E_20.

    This is a rigorous negative test for a hoped-for contradiction in the
    high descent: even after imposing both required Newton edges and all
    five P/Q vertices, the first thirteen descending identities are
    simultaneously consistent.
    """
    h = sp.symbols("h")
    p = {
        -1: h + 1,
        0: sp.Integer(1),
        1: sp.Integer(0),
        2: sp.Integer(0),
        3: sp.Integer(0),
        4: sp.Integer(0),
        5: sp.Integer(0),
        6: h**8,
        7: 2 * h**8,
        8: h**8,
    }
    q = {
        -1: (h + 1) ** 2,
        0: sp.Integer(1),
        1: sp.Integer(0),
        2: sp.Rational(3, 2) * h**4 * (h + 1),
        3: sp.Rational(3, 2) * h**4 * (h + 1),
        4: sp.Integer(0),
        5: sp.Integer(0),
        6: sp.Integer(0),
        7: sp.Integer(0),
        8: sp.Integer(0),
        9: h**12,
        10: 3 * h**12,
        11: 3 * h**12,
        12: h**12,
    }

    def identity(grade: int) -> sp.Expr:
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

    assert sp.expand(identity(-2) - (h + 1) ** 2) == 0
    assert all(identity(grade) == 0 for grade in range(8, 21))
    # Required case-c vertices:
    # p0(0 in z)=1; lead(p6)=lead(p8)=1; p8(0 in z)=1 since h=z-1.
    # q0=1; lead(q9)=lead(q12)=1; q12(0 in z)=1.
    assert p[0] == 1 and sp.LC(sp.Poly(p[6], h)) == 1
    assert sp.LC(sp.Poly(p[8], h)) == 1
    assert q[0] == 1 and sp.LC(sp.Poly(q[9], h)) == 1
    assert sp.LC(sp.Poly(q[12], h)) == 1
    residual = {
        grade: sp.factor(identity(grade))
        for grade in range(-1, 8)
        if identity(grade) != 0
    }

    # Keeping this P fixed does not permit the five residual grades to be
    # repaired by any choice of the 125 allowed Q coefficients.  This is
    # an exact rank test, not a numerical solve.
    p_coefficients: dict[tuple[int, int], sp.Expr] = {
        (0, 0): sp.Integer(1),
        (1, 0): sp.Integer(1),
    }
    for y_shift, multiplier in enumerate((1, 2, 1)):
        for z_degree in range(9):
            point = (z_degree, z_degree + 6 + y_shift)
            p_coefficients[point] = (
                p_coefficients.get(point, 0)
                + multiplier
                * comb(8, z_degree)
                * (-1) ** (8 - z_degree)
            )
    rows, matrix = previous.coefficient_matrix_for_fixed_p(p_coefficients)
    target = sp.Matrix([int(row == (2, 0)) for row in rows])
    fixed_p_rank = matrix.to_DM().rank()
    augmented_rank = matrix.row_join(target).to_DM().rank()
    assert (fixed_p_rank, augmented_rank) == (124, 125)
    return {
        "P": (
            "z/y + 1 + h^8*y^6*(y+1)^2, with h=z-1"
        ),
        "Q": (
            "z^2/y + 1 + h^12*y^9*(y+1)^3 "
            "+ (3/2)*(h+1)*h^4*(y^2+y^3)"
        ),
        "vanishing_grades": tuple(range(8, 21)),
        "remaining_residual": residual,
        "fixed_p_rank": fixed_p_rank,
        "fixed_p_augmented_rank": augmented_rank,
    }


def main() -> None:
    edge = vertical_edge_power_theorem()
    print("vertical-edge power theorem:", edge)
    descent = universal_next_descent()
    print("universal next descent:", descent["p7_form"])
    print("universal p6 defect:", descent["p6_defect"])
    print("grade-19 q11 resonance:", descent["q11_resonance"])
    print("forced q9 leading coefficient:", descent["q9_leading"])
    cross = grade11_cross_term_test()
    print("grade-11 test:", cross["conclusion"])
    print("canceling q3 contribution:", cross["canceling_q3_piece"])
    skeleton = explicit_high_grade_skeleton()
    print(
        "explicit full-vertex high skeleton vanishes on grades:",
        skeleton["vanishing_grades"],
    )
    print("remaining lower-grade residual:", skeleton["remaining_residual"])
    print(
        "full fixed-P Q system:",
        f"rank {skeleton['fixed_p_rank']}, "
        f"augmented rank {skeleton['fixed_p_augmented_rank']}",
    )
    print("RESULT: ALL NEXT-DESCENT EXACT CHECKS PASS")
    print(
        "SCOPE: these are universal characteristic-zero lemmas, but the "
        "remaining nonlinear compatibility branches at grades 15..8 "
        "have not been eliminated"
    )


if __name__ == "__main__":
    main()
