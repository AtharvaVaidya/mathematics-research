#!/usr/bin/env python3
"""Exploratory exact rows for constant descent on the r2-unit chart."""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_middle_divisibility_r2 import build_through_p5


def build():
    recurrence, h, r, s, p5, r_poly, s_poly = build_through_p5()
    w = sp.symbols("w0:3")
    e = sp.symbols("e0:4")
    base = sp.expand(r_poly * s_poly / 2)
    q10 = (
        6 * r[2] * r[4] + 3 * r[3] ** 2 + 6 * s[2]
    ) / 4
    recurrence.substitute(
        {
            sp.symbols("q10_10"): q10,
            **{
                p5[index]: base.coeff(h, index)
                for index in range(4)
            },
            **{
                p5[index + 4]: base.coeff(h, index + 4) + w[index]
                for index in range(3)
            },
            p5[7]: base.coeff(h, 7),
        }
    )
    recurrence.introduce(16)
    p4 = sp.symbols("p4_0:7")
    w_poly = sum(w[index] * h**index for index in range(3))
    p4_base = sp.expand(s_poly**2 / 4 + r_poly * w_poly / 2)
    recurrence.substitute(
        {
            p4[index]: p4_base.coeff(h, index) + e[index]
            for index in range(4)
        }
    )
    recurrence.p[-1] = h + sp.symbols("t")
    return recurrence, r, s, w, e


def main():
    recurrence, r, s, w, e = build()
    for grade in (15, 14, 13, 12):
        recurrence.introduce(grade)
    recurrence.substitute({e[0]: 0, e[1]: 0, e[2]: 0})
    rows11 = dict(recurrence.introduce(11)[0])
    rows10 = dict(recurrence.introduce(10)[0])
    rows9 = dict(recurrence.introduce(9)[0])
    rows8 = dict(recurrence.introduce(8)[0])
    q9 = sp.symbols("q9_9")
    q9_value = (
        6 * r[2] * r[3] * r[4]
        + r[3] ** 3
        + 12 * r[2] * s[3]
        + 12 * r[3] * s[2]
        + 12 * r[4] * s[1]
        + 12 * w[1]
    ) / 8
    p30, p31 = sp.symbols("p3_0 p3_1")
    branch = {
        q9: q9_value,
        s[0]: 0,
        p30: 0,
        p31: (r[2] * e[3] + s[1] * w[0]) / 2,
    }
    q7 = sp.symbols("q7_7")
    branch[q7] = sp.solve(rows11[6].subs(branch), q7)[0]
    q5 = sp.symbols("q5_5")
    branch[q5] = sp.solve(rows10[6].subs(branch), q5)[0]
    row10_5 = sp.cancel(rows10[5].subs(branch).subs(branch))
    common = sp.cancel(
        -sp.Rational(2048, 3) * row10_5 / r[2] ** 4
    )
    row8_2 = sp.cancel(rows8[2].subs(branch).subs(branch))
    defect2 = sp.factor(
        row8_2 - sp.Rational(3, 4) * s[1] * row10_5
    )
    expected2 = (
        -sp.Rational(21, 32)
        * r[2] ** 2
        * e[3]
        * (4 * sp.symbols("p2_0") - w[0] ** 2 - e[3] * s[1])
    )
    print("DEFECT2", defect2)
    print("DEFECT2 CHECK", sp.expand(defect2 - expected2) == 0)

    branch2 = {
        **branch,
        sp.symbols("p2_0"): (w[0] ** 2 + e[3] * s[1]) / 4,
    }
    row9_4 = sp.cancel(rows9[4].subs(branch2).subs(branch2))
    p22 = sp.symbols("p2_2")
    common_coefficient = sp.expand(common).coeff(p22)
    row9_coefficient = sp.expand(row9_4).coeff(p22)
    multiplier9 = sp.cancel(row9_coefficient / common_coefficient)
    defect9 = sp.factor(row9_4 - multiplier9 * common)
    print("MULTIPLIER9", sp.factor(multiplier9))
    print(
        "DEFECT9 terms",
        len(sp.Add.make_args(sp.expand(defect9))),
        "factor",
        defect9,
    )

    recurrence.q[-1] = (recurrence.h + sp.symbols("t")) ** 2
    identity7 = sp.expand(
        sum(
            recurrence.bracket_term(p_grade, q_grade)
            for p_grade in recurrence.p
            for q_grade in recurrence.q
            if p_grade + q_grade == 7
        )
    )
    specialized = sp.expand(
        sp.cancel(identity7.subs(branch2).subs(branch2))
    )
    row1 = sp.factor(specialized.coeff(recurrence.h, 1))
    row1_coefficient = sp.expand(row1).coeff(p22)
    multiplier7 = sp.cancel(row1_coefficient / common_coefficient)
    defect7 = sp.factor(row1 - multiplier7 * common)
    print("MULTIPLIER7", sp.factor(multiplier7))
    print(
        "DEFECT7 terms",
        len(sp.Add.make_args(sp.expand(defect7))),
        "factor",
        defect7,
    )
    branch3 = {
        **branch2,
        w[0]: s[1] ** 2 / (4 * r[2]),
    }
    p46 = sp.symbols("p4_6")
    q66 = sp.symbols("q6_6")
    branch4 = {
        **branch3,
        p46: (2 * r[4] * w[2] + s[3] ** 2) / 4,
    }
    branch4[q66] = sp.solve(common.subs(branch4).subs(branch4), q66)[0]
    for grade, degree in ((9, 5), (8, 3)):
        candidate = sp.factor(
            {9: rows9, 8: rows8}[grade][degree]
            .subs(branch4)
            .subs(branch4)
        )
        print(
            "CHAIN",
            grade,
            degree,
            "terms",
            len(sp.Add.make_args(sp.expand(candidate))),
            "factor",
            candidate,
            flush=True,
        )
    p32 = sp.symbols("p3_2")
    p44 = sp.symbols("p4_4")
    square_defect = (
        -8 * e[3] * r[2] * r[3]
        + 8 * e[3] * s[1]
        + 16 * p32 * r[2]
        - 8 * p44 * r[2] ** 2
        + 4 * r[2] ** 3 * w[2]
        + 4 * r[2] ** 2 * r[3] * w[1]
        + 4 * r[2] ** 2 * s[1] * s[3]
        + 2 * r[2] ** 2 * s[2] ** 2
        + r[2] * r[4] * s[1] ** 2
        - 8 * r[2] * s[1] * w[1]
        - 2 * s[1] ** 2 * s[2]
    )
    branch5 = {
        **branch4,
        p32: sp.solve(square_defect, p32)[0],
    }
    base_defect = sp.factor(
        rows8[4].subs(branch5).subs(branch5)
        - r[2] * rows9[6].subs(branch5).subs(branch5) / 2
    )
    print(
        "BASEDEFECT terms",
        len(sp.Add.make_args(sp.expand(base_defect))),
        "factor",
        base_defect,
        flush=True,
    )
    row7_2 = sp.factor(
        identity7.coeff(recurrence.h, 2).subs(branch5).subs(branch5)
    )
    print(
        "FIXEDDEFECT terms",
        len(sp.Add.make_args(sp.expand(row7_2))),
        "factor",
        row7_2,
        flush=True,
    )
    for degree in range(7):
        row = sp.cancel(identity7.coeff(recurrence.h, degree).subs(branch3).subs(branch3))
        p10 = sp.symbols("p1_0")
        print(
            "E7SCAN",
            degree,
            "terms",
            len(sp.Add.make_args(sp.expand(row))),
            "p10deg",
            sp.degree(sp.together(row).as_numer_denom()[0], p10),
            flush=True,
        )


if __name__ == "__main__":
    main()
