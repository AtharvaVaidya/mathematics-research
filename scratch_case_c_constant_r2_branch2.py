#!/usr/bin/env python3
"""Exact structural probes for the second r2/e3 resonance."""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_constant_descent_r2 import build_d4_recurrence


def show(name: str, expression: sp.Expr) -> None:
    expression = sp.factor(sp.cancel(expression))
    print(
        name,
        "terms",
        len(sp.Add.make_args(sp.expand(expression))),
        "factor",
        expression,
        flush=True,
    )


def main() -> None:
    recurrence, r, s, w, e = build_d4_recurrence()
    for grade in (15, 14, 13):
        recurrence.introduce(grade)
    recurrence.introduce(12)
    recurrence.substitute({e[0]: 0, e[1]: 0, e[2]: 0})
    rows = {}
    for grade in (11, 10, 9, 8):
        rows[grade] = dict(recurrence.introduce(grade)[0])
    recurrence.q[-1] = (recurrence.h + sp.symbols("t")) ** 2
    identity7 = sp.expand(
        sum(
            recurrence.bracket_term(p_grade, q_grade)
            for p_grade in recurrence.p
            for q_grade in recurrence.q
            if p_grade + q_grade == 7
        )
    )

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
        s[0]: r[2] ** 2 / 8,
        p30: r[2] ** 2 * w[0] / 16,
        p31: (
            r[2] * e[3] / 4
            + r[2] ** 2 * w[1] / 16
            + s[1] * w[0] / 2
        ),
    }
    branch[q7] = sp.solve(rows[11][6].subs(branch), q7)[0]
    branch[q5] = sp.solve(rows[10][6].subs(branch), q5)[0]
    show("SPLIT", rows[8][1].subs(branch).subs(branch))

    for label, delta in (
        ("IIA", sp.Integer(0)),
        ("IIB", 32 * e[3] / r[2]),
    ):
        values = {**branch, w[1]: w[0] + delta}
        print(label, flush=True)
        for grade in (11, 10, 9, 8):
            for degree, source in rows[grade].items():
                candidate = sp.cancel(source.subs(values).subs(values))
                count = len(sp.Add.make_args(sp.expand(candidate)))
                if candidate != 0 and count <= 25:
                    show(f"{label} SIMPLE E{grade}[h{degree}]", candidate)
        row82 = sp.factor(
            rows[8][2].subs(values).subs(values)
        )
        show(f"{label} E8[h2]", row82)
        p20 = sp.symbols("p2_0")
        p20_value = sp.solve(row82, p20)[0]
        next_values = {**values, p20: p20_value}
        common = sp.cancel(
            rows[10][5].subs(next_values).subs(next_values)
        )
        row94 = sp.cancel(
            rows[9][4].subs(next_values).subs(next_values)
        )
        print(label, "COMMONZERO", common == 0, "ROW94ZERO", row94 == 0, flush=True)
        p22 = sp.symbols("p2_2")
        common_multiplier = sp.cancel(
            sp.expand(row94).coeff(p22)
            / sp.expand(common).coeff(p22)
        )
        common_difference = sp.factor(
            row94 - common_multiplier * common
        )
        print(
            label,
            "COMMONMULT",
            sp.factor(common_multiplier),
            flush=True,
        )
        show(f"{label} COMMONPAIR", common_difference)
        row95 = sp.cancel(
            rows[9][5].subs(next_values).subs(next_values)
        )
        row83 = sp.cancel(
            rows[8][3].subs(next_values).subs(next_values)
        )
        multiplier = sp.cancel(
            sp.expand(row83).coeff(p22)
            / sp.expand(row95).coeff(p22)
        )
        difference = sp.factor(row83 - multiplier * row95)
        print(label, "MULT", sp.factor(multiplier), flush=True)
        show(f"{label} PAIR", difference)
        resonance_values = {
            s[1]: r[2] * r[3] / 4,
            w[0]: r[2]
            * (8 * s[2] - 2 * r[2] * r[4] - r[3] ** 2)
            / 32,
            sp.symbols("p4_6"): (
                2 * r[4] * w[2] + s[3] ** 2
            )
            / 4,
        }
        merged = {**next_values, **resonance_values}
        q66 = sp.symbols("q6_6")
        common_merged = sp.cancel(
            rows[10][5].subs(merged).subs(merged).subs(merged)
        )
        if sp.expand(common_merged).coeff(q66) != 0:
            merged[q66] = sp.solve(common_merged, q66)[0]
        row95_merged = sp.cancel(
            rows[9][5].subs(merged).subs(merged).subs(merged)
        )
        p21 = sp.symbols("p2_1")
        merged[p21] = sp.solve(row95_merged, p21)[0]
        for degree in range(4):
            fixed = sp.cancel(
                identity7.coeff(recurrence.h, degree)
                .subs(merged)
                .subs(merged)
                .subs(merged)
            )
            count = len(sp.Add.make_args(sp.expand(fixed)))
            if fixed != 0 and count <= 100:
                show(f"{label} FIXED E7[h{degree}]", fixed)
            else:
                print(
                    label,
                    "FIXED",
                    degree,
                    "terms",
                    count,
                    flush=True,
                )
        print(label, "MERGED SIMPLE", flush=True)
        for grade in (11, 10, 9, 8):
            for degree, source in rows[grade].items():
                candidate = sp.cancel(
                    source.subs(merged).subs(merged).subs(merged)
                )
                count = len(sp.Add.make_args(sp.expand(candidate)))
                if candidate != 0 and count <= 30:
                    show(
                        f"{label} MERGED E{grade}[h{degree}]",
                        candidate,
                    )


if __name__ == "__main__":
    main()
