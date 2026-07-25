#!/usr/bin/env python3
"""Exploratory exact rows for the case-c constant descent, r3-unit chart."""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_middle_divisibility_r3 import build_through_p5


def build():
    recurrence, h, r, s, p5, r_poly, s_poly = build_through_p5()
    w = sp.symbols("w0:4")
    e = sp.symbols("e0:4")
    base = sp.expand(r_poly * s_poly / 2)
    recurrence.substitute(
        {
            sp.symbols("q10_10"): (3 * r[3] ** 2 + 6 * s[2]) / 4,
            **{
                p5[index]: base.coeff(h, index)
                for index in range(4)
            },
            **{
                p5[index + 4]: base.coeff(h, index + 4) + w[index]
                for index in range(4)
            },
        }
    )
    recurrence.introduce(16)
    p4 = sp.symbols("p4_0:7")
    defect = sum(e[index] * h**index for index in range(4))
    w_poly = sum(w[index] * h**index for index in range(4))
    p4_base = sp.expand(s_poly**2 / 4 + r_poly * w_poly / 2)
    recurrence.substitute(
        {
            p4[index]: p4_base.coeff(h, index) + e[index]
            for index in range(4)
        }
    )
    recurrence.p[-1] = h + sp.symbols("t")
    return recurrence, h, r, s, w, e


def main():
    recurrence, _h, r, s, w, e = build()
    for grade in (15, 14, 13, 12):
        recurrence.introduce(grade)
    recurrence.substitute(
        {e[0]: 0, e[1]: 0, e[2]: 0, s[0]: 0}
    )
    rows11 = dict(recurrence.introduce(11)[0])
    rows10 = dict(recurrence.introduce(10)[0])
    rows9 = dict(recurrence.introduce(9)[0])
    rows8 = dict(recurrence.introduce(8)[0])
    q9 = sp.symbols("q9_9")
    p30, p31 = sp.symbols("p3_0 p3_1")
    q9_value = (
        r[3] ** 3 + 12 * r[3] * s[2]
        + 12 * r[4] * s[1] + 12 * w[1]
    ) / 8
    substitutions = {
        p30: 0,
        p31: s[1] * w[0] / 2,
    }
    p20 = sp.symbols("p2_0")
    zero_substitutions = {
        p30: 0,
        p31: 0,
        s[1]: 0,
        p20: w[0] ** 2 / 4,
    }
    row9 = sp.factor(rows9[5].subs(zero_substitutions))
    row8 = sp.factor(rows8[4].subs(zero_substitutions))
    print("E9h5", row9)
    print("E8h4", row8)
    p32 = sp.symbols("p3_2")
    residual = sp.expand(row8 * sp.Rational(1024, 3))
    basis = sp.groebner(
        (e[3] ** 2 * w[0], residual),
        p32, q9, w[1], s[2], r[3], w[0], e[3],
        order="grevlex",
    )
    print("basis", len(basis.polys))
    for power in range(1, 10):
        if basis.reduce(e[3] ** power)[1] == 0:
            print("e3 power", power)
            break


if __name__ == "__main__":
    main()
