#!/usr/bin/env python3
"""Exact constant-coefficient descent on the case-c r3-unit chart.

In normalized coordinates

    r=h^3*(r3+r4*h),       p6=r^2/4+h^4*s,
    p5=r*s/2+h^4*w,

where the already-proved endpoint rows give deg(w)<=2.  For

    D4=p4-s^2/4-r*w/2,

this verifier proves h^4 | D4.  The q10 resonance value used in the input
recurrence is forced by the denominator-free endpoint calculation in
route_bd_case_c_middle_divisibility_r2.py: its only localization is
r4!=0, supplied globally by the required p6 vertex.  The fixed base term
p_-1=h+t is included before every row E11 and below.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_middle_divisibility_r3 import build_through_p5


def build_d4_recurrence():
    recurrence, h, r, s, p5, r_poly, s_poly = build_through_p5()
    w = sp.symbols("w0:3")
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


def universal_first_two():
    recurrence, _r, _s, _w, e = build_d4_recurrence()
    for grade in (15, 14, 13):
        recurrence.introduce(grade)
    rows12 = dict(recurrence.introduce(12)[0])
    expected = {
        3: -24 * e[0] ** 2,
        4: -42 * e[0] * e[1],
        5: -18 * (2 * e[0] * e[2] + e[1] ** 2),
        6: -30 * (e[0] * e[3] + e[1] * e[2]),
    }
    for degree, expression in expected.items():
        assert sp.expand(rows12[degree] - expression) == 0
    return {"e0": e[0] ** 2, "e1_after_e0": e[1] ** 2}


def third_coefficient():
    recurrence, r, s, w, e = build_d4_recurrence()
    for grade in (15, 14, 13, 12):
        recurrence.introduce(grade)
    recurrence.substitute({e[0]: 0, e[1]: 0})
    rows11 = dict(recurrence.introduce(11)[0])
    rows10 = dict(recurrence.introduce(10)[0])
    recurrence.introduce(9)
    rows8 = dict(recurrence.introduce(8)[0])

    q9 = sp.symbols("q9_9")
    p30, p31 = sp.symbols("p3_0 p3_1")
    q9_value = (
        r[3] ** 3
        + 12 * r[3] * s[2]
        + 12 * r[4] * s[1]
        + 12 * w[1]
    ) / 8
    endpoint = sp.factor(rows11[4])
    assert sp.expand(
        endpoint
        - sp.Rational(45, 512)
        * s[0] ** 3
        * (-8 * q9 + 8 * q9_value)
    ) == 0
    row11 = sp.factor(rows11[5].subs(q9, q9_value))
    row10 = sp.factor(rows10[3].subs(q9, q9_value))
    x = 2 * p30 - s[0] * w[0]
    assert sp.expand(row11 + 15 * e[2] * x) == 0
    assert sp.expand(
        row10 + sp.Rational(9, 2) * (x**2 - 2 * s[0] * e[2] ** 2)
    ) == 0
    x_symbol = sp.symbols("x")
    unit_basis = sp.groebner(
        (e[2] * x_symbol, x_symbol**2 - 2 * s[0] * e[2] ** 2),
        x_symbol,
        e[2],
        order="grevlex",
        domain=sp.QQ.frac_field(s[0]),
    )
    assert unit_basis.reduce(e[2] ** 3)[1] == 0

    zero = {s[0]: 0}
    row11_5 = sp.factor(rows11[5].subs(zero))
    row11_6 = sp.factor(rows11[6].subs(zero))
    row10_4 = sp.factor(rows10[4].subs(zero))
    row8_1 = sp.factor(rows8[1].subs(zero))
    f1 = e[2] * p30
    f2 = (
        e[2] ** 2 * r[3]
        - 4 * e[2] * p31
        + 2 * e[2] * s[1] * w[0]
        - 4 * e[3] * p30
    )
    f3 = (
        -2 * e[2] ** 2 * s[1]
        + 3 * e[2] * p30 * r[3]
        + 8 * p30 * p31
        - 4 * p30 * s[1] * w[0]
    )
    f4 = (
        4 * e[2] ** 3
        + e[2] ** 2 * s[1] ** 2
        + 2 * e[2] * p30 * w[0]
        - 6 * p30**2 * s[2]
        - 4 * p30 * p31 * s[1]
        + 2 * p30 * s[1] ** 2 * w[0]
    )
    assert sp.expand(row11_5 + 30 * f1) == 0
    assert sp.expand(row11_6 - 6 * f2) == 0
    assert sp.expand(row10_4 + sp.Rational(15, 4) * f3) == 0
    assert sp.expand(row8_1 - sp.Rational(3, 4) * f4) == 0
    zero_basis = sp.groebner(
        (f1, f2, f3, f4),
        e[3],
        p30,
        p31,
        s[2],
        w[0],
        s[1],
        e[2],
        order="grevlex",
        domain=sp.QQ.frac_field(r[3]),
    )
    assert zero_basis.reduce(e[2] ** 4)[1] == 0
    return {"s0_unit": e[2] ** 3, "s0_zero": e[2] ** 4}


def fourth_coefficient():
    recurrence, r, s, w, e = build_d4_recurrence()
    for grade in (15, 14, 13, 12):
        recurrence.introduce(grade)
    recurrence.substitute({e[0]: 0, e[1]: 0, e[2]: 0})
    rows11 = dict(recurrence.introduce(11)[0])
    rows10 = dict(recurrence.introduce(10)[0])
    rows9 = dict(recurrence.introduce(9)[0])
    rows8 = dict(recurrence.introduce(8)[0])

    q9, q7 = sp.symbols("q9_9 q7_7")
    p30, p31, p20 = sp.symbols("p3_0 p3_1 p2_0")
    q9_value = (
        r[3] ** 3
        + 12 * r[3] * s[2]
        + 12 * r[4] * s[1]
        + 12 * w[1]
    ) / 8
    first = {q9: q9_value, p30: s[0] * w[0] / 2}
    resonance = sp.factor(rows11[6].subs(first))
    assert sp.factor(sp.expand(resonance).coeff(q7)) == (
        -sp.Rational(21, 4) * s[0] ** 2
    )
    q7_value = sp.solve(resonance, q7)[0]
    second = {**first, q7: q7_value}
    x = 2 * p31 - s[0] * w[1] - s[1] * w[0]
    product = sp.factor(rows9[3].subs(second))
    square = sp.factor(
        rows10[5].subs(second) - 2 * rows8[1].subs(second) / s[0]
    )
    product_difference = sp.expand(
        product - sp.Rational(15, 2) * s[0] * e[3] * x
    )
    assert product_difference == 0, sp.factor(product_difference)
    assert sp.expand(
        square + sp.Rational(15, 4) * (x**2 - 2 * s[0] * e[3] ** 2)
    ) == 0
    x_symbol = sp.symbols("x")
    unit_basis = sp.groebner(
        (e[3] * x_symbol, x_symbol**2 - 2 * s[0] * e[3] ** 2),
        x_symbol,
        e[3],
        order="grevlex",
        domain=sp.QQ.frac_field(s[0]),
    )
    assert unit_basis.reduce(e[3] ** 3)[1] == 0

    zero = {s[0]: 0}
    assert sp.factor(rows10[3].subs(zero)) == -18 * p30**2
    assert sp.expand(
        rows10[5].subs({**zero, p30: 0})
        + 3 * (-2 * p31 + s[1] * w[0]) ** 2
    ) == 0
    p3_values = {s[0]: 0, p30: 0, p31: s[1] * w[0] / 2}
    endpoint = sp.factor(rows9[4].subs(p3_values))
    assert sp.expand(
        endpoint
        + sp.Rational(45, 8192)
        * s[1] ** 4
        * (-8 * q9 + 8 * q9_value)
    ) == 0
    unit_values = {**p3_values, q9: q9_value}
    y = 4 * p20 - w[0] ** 2
    row8 = sp.factor(rows8[3].subs(unit_values))
    row10 = sp.factor(rows10[6].subs(unit_values))
    assert sp.expand(row8 + sp.Rational(3, 4) * y**2) == 0
    assert sp.expand(
        row10 - sp.Rational(9, 2) * e[3] * (e[3] * s[1] - y)
    ) == 0
    y_symbol = sp.symbols("y")
    s1_basis = sp.groebner(
        (y_symbol**2, e[3] * (e[3] * s[1] - y_symbol)),
        y_symbol,
        e[3],
        order="grevlex",
        domain=sp.QQ.frac_field(s[1]),
    )
    assert s1_basis.reduce(e[3] ** 3)[1] == 0

    final_values = {
        s[0]: 0,
        s[1]: 0,
        p30: 0,
        p31: 0,
        p20: w[0] ** 2 / 4,
    }
    row9 = sp.factor(rows9[5].subs(final_values))
    row8 = sp.factor(rows8[4].subs(final_values))
    assert row9 == sp.Rational(9, 2) * e[3] ** 2 * w[0]
    residual = sp.expand(row8 * sp.Rational(1024, 3))
    p32 = sp.symbols("p3_2")
    zero_basis = sp.groebner(
        (e[3] ** 2 * w[0], residual),
        p32,
        q9,
        w[1],
        s[2],
        r[3],
        w[0],
        e[3],
        order="grevlex",
    )
    assert zero_basis.reduce(e[3] ** 5)[1] == 0
    return {
        "s0_unit": e[3] ** 3,
        "s0_zero_s1_unit": e[3] ** 3,
        "s0_s1_zero": e[3] ** 5,
    }


def main() -> None:
    universal_first_two()
    third = third_coefficient()
    fourth = fourth_coefficient()
    print("h-adic chart: r0=r1=r2=0, r3!=0")
    print("required p6 vertex supplies r4!=0 and the q10 resonance")
    print("third-coefficient consequences:", *third.values(), "= 0")
    print("fourth-coefficient consequences:", *fourth.values(), "= 0")
    print("therefore h^4 divides D4=p4-s^2/4-r*w/2")
    print("RESULT: EXACT FULL-STRATUM r3-CHART CONSTANT DESCENT PASSES")


if __name__ == "__main__":
    main()
