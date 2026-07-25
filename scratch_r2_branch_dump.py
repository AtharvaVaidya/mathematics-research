#!/usr/bin/env python3
"""Dump exact specialized rows on the two r2/e3 branches."""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_constant_descent_r2 import build_d4_recurrence


def brief(name: str, expression: sp.Expr) -> None:
    expression = sp.cancel(expression)
    if expression == 0:
        return
    expanded = sp.expand(expression)
    term_count = len(sp.Add.make_args(expanded))
    expression = (
        sp.factor(expression)
        if term_count <= 100
        else sp.factor_terms(expression)
    )
    print(
        name,
        "terms=",
        term_count,
        "factor=",
        expression,
        flush=True,
    )


def main() -> None:
    recurrence, r, s, w, e = build_d4_recurrence()
    for grade in (15, 14, 13):
        recurrence.introduce(grade)
    recurrence.introduce(12)
    recurrence.substitute({e[0]: 0, e[1]: 0, e[2]: 0})
    row_groups = {}
    for grade in (11, 10, 9, 8):
        row_groups[grade] = dict(recurrence.introduce(grade)[0])

    q9, q7, q5 = sp.symbols("q9_9 q7_7 q5_5")
    p30, p31 = sp.symbols("p3_0 p3_1")
    q9_value = (
        6 * r[2] * r[3] * r[4]
        + r[3] ** 3
        + 12 * r[2] * s[3]
        + 12 * r[3] * s[2]
        + 12 * r[4] * s[1]
        + 12 * w[1]
    ) / 8
    branch = {
        q9: q9_value,
        s[0]: 0,
        p30: 0,
        p31: (r[2] * e[3] + s[1] * w[0]) / 2,
    }
    branch[q7] = sp.solve(row_groups[11][6].subs(branch), q7)[0]
    branch[q5] = sp.solve(row_groups[10][6].subs(branch), q5)[0]
    branch.update(
        {
            r[3]: 0,
            r[4]: 1,
            s[1]: 0,
            s[2]: 0,
            s[3]: 0,
            w[0]: 0,
            w[1]: 0,
            w[2]: 0,
        }
    )

    for grade, rows in row_groups.items():
        for degree, row in rows.items():
            brief(f"E{grade}[h{degree}]", row.subs(branch).subs(branch))

    p20, p22 = sp.symbols("p2_0 p2_2")
    p32, p34 = sp.symbols("p3_2 p3_4")
    p44, p46 = sp.symbols("p4_4 p4_6")
    q66, q88 = sp.symbols("q6_6 q8_8")
    common = sp.cancel(row_groups[10][5].subs(branch).subs(branch))
    q66_value = sp.solve(
        common.subs({p20: 0, p32: p44 * r[2] / 2}), q66
    )[0]
    reduced = {
        **branch,
        p20: 0,
        p32: p44 * r[2] / 2,
        p46: 0,
        q66: q66_value,
    }
    print("STRUCTURAL REDUCTION", flush=True)
    for grade, degree in ((8, 3), (9, 6), (8, 4), (8, 5), (8, 6)):
        brief(
            f"RED E{grade}[h{degree}]",
            row_groups[grade][degree].subs(reduced).subs(reduced),
        )


if __name__ == "__main__":
    main()
