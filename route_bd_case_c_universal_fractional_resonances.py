#!/usr/bin/env python3
"""Universal lower fractional-resonance descent for case c.

The previously proved chart package gives:

* c11=c10=0;
* the canonical square root H is polynomial on every surviving
  r0=r1=0 chart;
* P=H^2+R with deg_y(R)<=3.

This verifier works with r=h^2*(r2+r3*h+r4*h^2), without assuming r2 is
nonzero.  The required p6 vertex gives r4!=0, so the same identities cover
the r2-, r3-, and r4-leading charts.

An unused grade-13 endpoint first forces the raw q9 slot to equal its
approximate-cube value, hence c9=0.  Four subsequent endpoint rows form a
short square cascade that forces c7,c6,c5=0.  No coefficient other than
the globally required r4 is inverted.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_approx_root import A, ell, p, y
from route_bd_case_c_constant_descent_r2 import build_d4_recurrence


def build_closed_tail_rows():
    """Build the r0=r1=0 recurrence after h^4|D4, keeping c9 raw."""
    recurrence, r, s, w, e = build_d4_recurrence()
    h = recurrence.h
    q9 = sp.symbols("q9_9")
    g = sp.symbols("g")
    q9_base = (
        6 * r[2] * r[3] * r[4]
        + r[3] ** 3
        + 12 * r[2] * s[3]
        + 12 * r[3] * s[2]
        + 12 * r[4] * s[1]
        + 12 * w[1]
    ) / 8
    recurrence.substitute(
        {
            q9: q9_base + g,
            **{coefficient: 0 for coefficient in e},
        }
    )
    rows = {}
    for grade in (15, 14, 13, 12, 11, 10, 9, 8):
        rows[grade] = dict(recurrence.introduce(grade)[0])
    return recurrence, r, s, w, g, q9_base, rows


def approximate_root_slots(recurrence, r, s, w):
    """Return the exact c8,c7,c6,c5 triangular raw-slot substitutions."""
    h = recurrence.h
    r_poly = sum(r[index] * h**index for index in range(2, 5))
    s_poly = sum(s[index] * h**index for index in range(4))
    w_poly = sum(w[index] * h**index for index in range(3))
    p4 = recurrence.p[4]
    u_poly = sp.cancel(
        (p4 - s_poly**2 / 4 - r_poly * w_poly / 2) / h**4
    )
    H = sp.expand(
        h**4 * y**4
        + r_poly * y**3 / 2
        + s_poly * y**2 / 2
        + w_poly * y / 2
        + u_poly / 2
    )
    P = sp.expand(
        sum(recurrence.p[degree] * y**degree for degree in range(9))
    )
    R = sp.expand(P - H**2)
    assert sp.Poly(R, y).degree() <= 3

    # Since deg_y(R)<=3,
    #
    #   (P^(3/2))_+ - H^3 - (3/2)H*R
    #
    # has y-degree at most two.  Thus the displayed polynomial gives
    # every A12 slot of y-degree 5,6,7,8 used here.
    a12_high = sp.Poly(
        sp.expand(H**3 + sp.Rational(3, 2) * H * R),
        y,
    )

    def slot(degree: int) -> sp.Expr:
        return sp.expand(
            a12_high.coeff_monomial(y**degree)
        ).coeff(h, degree)

    q8, q7, q6, q5 = sp.symbols("q8_8 q7_7 q6_6 q5_5")
    c8 = sp.factor(q8 - slot(8))
    c7, c6, c5 = sp.symbols("c7 c6 c5")

    # Keep the lower-triangular contributions of A7 to q6,q5 and of A6
    # to q5.  They vanish after the preceding mode is killed, but
    # retaining them here makes the coordinate change itself exact.
    approximate_substitutions = {
        ell: h,
        **{p[degree]: recurrence.p[degree] for degree in range(8)},
    }

    def lower_slot(power: int, y_degree: int, h_degree: int) -> sp.Expr:
        coefficient = sp.Poly(A[power], y).coeff_monomial(y**y_degree)
        return sp.expand(
            coefficient.subs(approximate_substitutions)
        ).coeff(h, h_degree)

    a7_to_q6 = lower_slot(7, 6, 6)
    a7_to_q5 = lower_slot(7, 5, 5)
    a6_to_q5 = lower_slot(6, 5, 5)
    assert a7_to_q6 == sp.Rational(7, 8) * r[3]
    assert a7_to_q5 == (
        sp.Rational(7, 128)
        * (6 * r[2] * r[4] + 3 * r[3] ** 2 + 16 * s[2])
    )
    assert a6_to_q5 == sp.Rational(3, 4) * r[3]

    substitutions = {
        q7: slot(7) + c8 * recurrence.p[7].coeff(h, 7) + c7,
        q6: (
            slot(6)
            + c8 * recurrence.p[6].coeff(h, 6)
            + a7_to_q6 * c7
            + c6
        ),
        q5: (
            slot(5)
            + c8 * recurrence.p[5].coeff(h, 5)
            + a7_to_q5 * c7
            + a6_to_q5 * c6
            + c5
        ),
    }
    return c7, c6, c5, substitutions


def verify_fractional_square_cascade() -> dict[str, sp.Expr]:
    recurrence, r, s, w, g, _q9_base, rows = build_closed_tail_rows()
    c7, c6, c5, slot_substitutions = approximate_root_slots(
        recurrence, r, s, w
    )
    r3, r4 = r[3], r[4]
    s2, s3 = s[2], s[3]
    w1, w2 = w[1], w[2]
    p4_5, p4_6, p3_5 = sp.symbols("p4_5 p4_6 p3_5")

    # The raw q9 deviation is the c9 triangular coordinate because c10
    # is already zero.  The required r4 vertex makes this a unit row.
    c9_row = sp.factor(rows[13][16])
    assert c9_row == -sp.Rational(45, 1024) * r4**4 * g

    # After c9=0, the next endpoint is a pure square.  Put U equal to
    # the square's linear factor.
    U = -4 * p4_6 + 2 * r4 * w2 + s3**2
    u_row = sp.factor(rows[12][15].subs(g, 0))
    assert u_row == sp.Rational(3, 4) * U**2
    u_zero = {g: 0, p4_6: (2 * r4 * w2 + s3**2) / 4}

    # The next raw slot is c7 with a nonzero r4^4 coefficient.
    c7_row = sp.factor(
        rows[11][14].subs(slot_substitutions).subs(u_zero)
    )
    assert c7_row == sp.Rational(35, 1024) * r4**4 * c7

    # The c6 slot is paired with one new square X^2.  The two rows have
    # different square coefficients, so their difference first kills X
    # and either row then kills c6.
    B = (
        r3 * r4 * w2
        + r4**2 * w1
        + r4 * s2 * s3
        - 2 * s3 * w2
    )
    X = 2 * p3_5 - p4_5 * r4 + B / 2
    through_c7 = {**u_zero, c7: 0}
    c6_row_10 = sp.factor(
        rows[10][13].subs(slot_substitutions).subs(through_c7)
    )
    c6_row_9 = sp.factor(
        rows[9][13].subs(slot_substitutions).subs(through_c7)
    )
    assert sp.expand(
        c6_row_10
        - sp.Rational(3, 64) * (c6 * r4**4 + 64 * X**2)
    ) == 0
    assert sp.expand(
        c6_row_9
        - sp.Rational(3, 128)
        * r4
        * (c6 * r4**4 + 24 * X**2)
    ) == 0
    square_difference = sp.factor(
        sp.Rational(64, 3) * c6_row_10
        - sp.Rational(128, 3) * c6_row_9 / r4
    )
    assert sp.expand(square_difference - 40 * X**2) == 0

    # With X=c6=0, one final endpoint is a unit times c5.
    x_zero = {
        **through_c7,
        c6: 0,
        p3_5: p4_5 * r4 / 2 - B / 4,
    }
    c5_row = sp.factor(
        rows[9][12].subs(slot_substitutions).subs(x_zero)
    )
    assert c5_row == sp.Rational(35, 1024) * r4**4 * c5

    return {
        "c9_row": c9_row,
        "u_square": u_row,
        "c7_row": c7_row,
        "c6_square_difference": square_difference,
        "c5_row": c5_row,
    }


def main() -> None:
    rows = verify_fractional_square_cascade()
    print("required full-stratum vertex: r4 != 0")
    print("c9 endpoint:", rows["c9_row"], "= 0")
    print("next endpoint square:", rows["u_square"], "= 0")
    print("c7 endpoint:", rows["c7_row"], "= 0")
    print("c6 paired-row square:", rows["c6_square_difference"], "= 0")
    print("c5 endpoint:", rows["c5_row"], "= 0")
    print("therefore c9=c7=c6=c5=0 on all r0=r1=0 tail charts")
    print(
        "with the existing r0 elimination and r1 tail obstruction, "
        "all fractional case-c modes vanish universally"
    )
    print("RESULT: EXACT UNIVERSAL CASE-C FRACTIONAL DESCENT PASSES")


if __name__ == "__main__":
    main()
