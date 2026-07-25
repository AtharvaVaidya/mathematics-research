#!/usr/bin/env python3
"""Identify the paired e3 rows after the r2 negative-tail constraint."""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_constant_descent_r2 import build_d4_recurrence


def main() -> None:
    recurrence, r, s, w, e = build_d4_recurrence()
    for grade in (15, 14, 13):
        recurrence.introduce(grade)
    recurrence.introduce(12)
    recurrence.substitute({e[0]: 0, e[1]: 0, e[2]: 0})
    rows = {}
    for grade in (11, 10, 9, 8):
        rows[grade] = dict(recurrence.introduce(grade)[0])
    q9, q7 = sp.symbols("q9_9 q7_7")
    p30, p31 = sp.symbols("p3_0 p3_1")
    x = sp.symbols("x")
    q9_value = (
        6 * r[2] * r[3] * r[4]
        + r[3] ** 3
        + 12 * r[2] * s[3]
        + 12 * r[3] * s[2]
        + 12 * r[4] * s[1]
        + 12 * w[1]
    ) / 8
    values = {
        q9: q9_value,
        s[0]: r[2] ** 2 / 16,
        p30: r[2] ** 2 * w[0] / 32,
        p31: (
            x + r[2] ** 2 * w[1] / 16 + s[1] * w[0]
        )
        / 2,
    }
    resonance = sp.factor(rows[11][6].subs(values))
    print("RESONANCE q7 coefficient", sp.factor(sp.expand(resonance).coeff(q7)))
    values[q7] = sp.solve(resonance, q7)[0]
    for grade, degree in (
        (10, 5),
        (9, 3),
        (8, 1),
        (8, 2),
    ):
        row = sp.factor(rows[grade][degree].subs(values).subs(values))
        print(f"E{grade}[h{degree}]", row)


if __name__ == "__main__":
    main()
