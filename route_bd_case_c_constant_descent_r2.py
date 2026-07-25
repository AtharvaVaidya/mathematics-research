#!/usr/bin/env python3
"""Exact constant descent on the full case-c r2-unit chart.

This verifier includes the fixed base p_-1=h+t and proves that all four
coefficients e0,e1,e2,e3 of

    D4=p4-s^2/4-r*w/2

vanish when r=h^2*(r2+r3*h+r4*h^2).  The required p6 vertex gives
[h^8]p6=r4^2/4!=0, so the uses of r4^{-1} below impose no additional
subchart restriction.  The final step uses the normalized negative formal tail: its
L13 Euler cokernel forces s0=r2^2/16, where two low compatibility rows kill
e3.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_middle_divisibility_r2 import build_through_p5


def build_d4_recurrence():
    recurrence, h, r, s, p5, r_poly, s_poly = build_through_p5()
    w = sp.symbols("w0:3")
    e = sp.symbols("e0:4")
    base = sp.expand(r_poly * s_poly / 2)
    recurrence.substitute(
        {
            sp.symbols("q10_10"): (
                6 * r[2] * r[4] + 3 * r[3] ** 2 + 6 * s[2]
            )
            / 4,
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


def rows_through_e8():
    recurrence, r, s, w, e = build_d4_recurrence()
    for grade in (15, 14, 13):
        recurrence.introduce(grade)
    rows12 = dict(recurrence.introduce(12)[0])
    expected = {
        3: -24 * e[0] ** 2,
        4: -42 * e[0] * e[1],
        5: -18 * (2 * e[0] * e[2] + e[1] ** 2),
    }
    for degree, expression in expected.items():
        difference = sp.expand(rows12[degree] - expression)
        assert difference == 0, (degree, sp.factor(difference))
    recurrence.substitute({e[0]: 0, e[1]: 0})
    rows11 = dict(recurrence.introduce(11)[0])
    rows10 = dict(recurrence.introduce(10)[0])
    rows9 = dict(recurrence.introduce(9)[0])
    rows8 = dict(recurrence.introduce(8)[0])
    return r, s, w, e, rows11, rows10, rows9, rows8


def eliminate_e2():
    r, s, w, e, rows11, rows10, rows9, rows8 = rows_through_e8()
    q9 = sp.symbols("q9_9")
    q9_value = (
        6 * r[2] * r[3] * r[4]
        + r[3] ** 3
        + 12 * r[2] * s[3]
        + 12 * r[3] * s[2]
        + 12 * r[4] * s[1]
        + 12 * w[1]
    ) / 8
    g = sp.symbols("g")
    A = (
        7 * r[2] ** 6
        - 164 * r[2] ** 4 * s[0]
        + 1408 * r[2] ** 2 * s[0] ** 2
        + 1024 * s[0] ** 3
    )
    D = (
        119 * r[2] ** 4
        - 544 * r[2] ** 2 * s[0]
        + 256 * s[0] ** 2
    )
    pure11 = sp.cancel(rows11[4].subs(q9, q9_value + g))
    pure9 = sp.cancel(rows9[8].subs(q9, q9_value + g))
    assert sp.expand(pure11 + sp.Rational(45, 65536) * g * A) == 0
    assert sp.expand(
        pure9
        - sp.Rational(5265, 33554432) * r[4] ** 4 * g * D
    ) == 0

    # A/r2^6 and D/r2^4 are coprime in u=s0/r2^2.  The r2 chart and the
    # required p6 vertex give r2*r4!=0, so the two pure endpoint rows
    # force g=0.
    u = sp.symbols("u")
    A0 = 7 - 164 * u + 1408 * u**2 + 1024 * u**3
    D0 = 119 - 544 * u + 256 * u**2
    bezout_a, bezout_d, gcd = sp.gcdex(A0, D0, u)
    assert gcd == 1
    assert sp.expand(bezout_a * A0 + bezout_d * D0) == 1

    p30, p31 = sp.symbols("p3_0 p3_1")
    x = sp.symbols("x")
    row11 = sp.factor(rows11[5].subs(q9, q9_value))
    row10 = sp.factor(rows10[3].subs(q9, q9_value))
    x_expression = 2 * p30 - s[0] * w[0]
    f11 = e[2] * (r[2] * e[2] - 2 * x_expression)
    f10 = (
        e[2] ** 2 * (r[2] ** 2 + 6 * s[0])
        - 2 * r[2] * e[2] * x_expression
        - 3 * x_expression**2
    )
    assert sp.expand(row11 - sp.Rational(15, 2) * f11) == 0
    assert sp.expand(row10 - sp.Rational(3, 2) * f10) == 0
    first_basis = sp.groebner(
        (
            e[2] * (r[2] * e[2] - 2 * x),
            e[2] ** 2 * (r[2] ** 2 + 6 * s[0])
            - 2 * r[2] * e[2] * x
            - 3 * x**2,
        ),
        x,
        s[0],
        e[2],
        order="grevlex",
        domain=sp.QQ.frac_field(r[2]),
    )
    assert first_basis.reduce(
        e[2] ** 3 * (8 * s[0] - r[2] ** 2)
    )[1] == 0
    assert first_basis.reduce(
        e[2] * (2 * x - r[2] * e[2])
    )[1] == 0

    # On a hypothetical e2!=0 component, the preceding consequences
    # force the following substitutions.
    branch = {
        q9: q9_value,
        s[0]: r[2] ** 2 / 8,
        p30: r[2] ** 2 * w[0] / 16 + r[2] * e[2] / 4,
    }
    resonance11 = sp.cancel(rows11[6].subs(branch))
    combination10 = sp.factor(
        rows10[4].subs(branch) - 3 * r[2] * resonance11 / 4
    )
    combination9 = sp.factor(
        rows9[2].subs(branch) - 3 * r[2] ** 2 * resonance11 / 16
    )
    B10 = (
        76 * e[2] * r[2] * r[3]
        - 160 * e[2] * s[1]
        + 36 * e[3] * r[2] ** 2
        - 144 * p31 * r[2]
        + 9 * r[2] ** 3 * w[1]
        + 72 * r[2] * s[1] * w[0]
    )
    B9 = (
        6 * e[2] * r[2] * r[3]
        - 8 * e[2] * s[1]
        + 4 * e[3] * r[2] ** 2
        - 16 * p31 * r[2]
        + r[2] ** 3 * w[1]
        + 8 * r[2] * s[1] * w[0]
    )
    assert sp.expand(
        combination10 + sp.Rational(3, 64) * e[2] * B10
    ) == 0
    assert sp.expand(
        combination9
        + sp.Rational(27, 128) * e[2] * r[2] * B9
    ) == 0
    assert sp.expand(
        B10
        - 9 * B9
        - 22 * e[2] * (r[2] * r[3] - 4 * s[1])
    ) == 0
    branch[s[1]] = r[2] * r[3] / 4
    branch[p31] = (
        e[2] * r[3] / 4
        + e[3] * r[2] / 4
        + r[2] ** 2 * w[1] / 16
        + r[2] * r[3] * w[0] / 8
    )

    q7 = sp.symbols("q7_7")
    resonance11 = sp.cancel(rows11[6].subs(branch))
    q7_coefficient = sp.factor(sp.expand(resonance11).coeff(q7))
    assert q7_coefficient != 0
    branch[q7] = sp.solve(resonance11, q7)[0]
    row10_5 = sp.factor(rows10[5].subs(branch))
    row9_3 = sp.factor(rows9[3].subs(branch))
    bracket10 = sp.cancel(row10_5 * 16 / (3 * e[2]))
    bracket9 = sp.cancel(row9_3 * 64 / (3 * e[2]))
    forced_w = sp.factor(bracket9 - 2 * r[2] * bracket10)
    expected_w = 5 * e[2] * (
        2 * r[2] ** 2 * r[4]
        + r[2] * r[3] ** 2
        - 8 * r[2] * s[2]
        + 32 * w[0]
    )
    assert sp.expand(forced_w - expected_w) == 0
    branch[w[0]] = (
        r[2] * (8 * s[2] - 2 * r[2] * r[4] - r[3] ** 2)
        / 32
    )
    p20 = sp.symbols("p2_0")
    equation10 = sp.cancel(rows10[5].subs(branch))
    branch[p20] = sp.solve(equation10, p20)[0]
    final = sp.factor(rows8[1].subs(branch))
    assert final == 3 * e[2] ** 3
    return {
        "q9_deviation": g,
        "e2_final_row": final,
    }


def negative_tail_constraint():
    """Verify the normalized L13 cokernel on the full r2 chart."""
    h, t = sp.symbols("h t", nonzero=True)
    r2, r3, r4 = sp.symbols("r2 r3 r4")
    s0, s1, s2, s3 = sp.symbols("s0 s1 s2 s3")
    w0, w1, w2 = sp.symbols("w0 w1 w2")
    r_poly = r2 * h**2 + r3 * h**3 + r4 * h**4
    s_poly = s0 + s1 * h + s2 * h**2 + s3 * h**3
    w_poly = w0 + w1 * h + w2 * h**2
    p = {
        8: h**8,
        7: h**4 * r_poly,
        6: sp.expand(r_poly**2 / 4 + h**4 * s_poly),
        5: sp.expand(r_poly * s_poly / 2 + h**4 * w_poly),
    }

    def bracket(p_grade, p_value, q_grade, q_value):
        return sp.expand(
            q_grade * sp.diff(p_value, h) * q_value
            - p_grade * p_value * sp.diff(q_value, h)
        )

    def solve_euler(order, forcing):
        solution = 0
        for term in sp.Add.make_args(sp.expand(forcing)):
            coefficient, output_exponent = term.as_coeff_exponent(h)
            input_exponent = output_exponent - 7
            multiplier = -8 * (order + input_exponent)
            # The zero multiplier is the h^-order centralizer
            # resonance, removed by the normalized-tail convention.
            assert multiplier != 0
            solution += (
                -coefficient * h**input_exponent / multiplier
            )
        return sp.expand(solution)

    n10 = (
        -sp.Rational(1, 40) * h**-5
        - t * h**-6 / 16
        - t**2 * h**-7 / 24
    )
    assert sp.expand(
        bracket(8, p[8], -10, n10) - (h + t) ** 2
    ) == 0
    forcing11 = bracket(7, p[7], -10, n10)
    n11 = solve_euler(11, forcing11)
    assert sp.expand(
        bracket(8, p[8], -11, n11) + forcing11
    ) == 0
    forcing12 = sp.expand(
        bracket(7, p[7], -11, n11)
        + bracket(6, p[6], -10, n10)
    )
    n12 = solve_euler(12, forcing12)
    assert sp.expand(
        bracket(8, p[8], -12, n12) + forcing12
    ) == 0
    forcing13 = sp.expand(
        bracket(7, p[7], -12, n12)
        + bracket(6, p[6], -11, n11)
        + bracket(5, p[5], -10, n10)
    )
    obstruction = sp.factor(forcing13.coeff(h, -6))
    expected = (
        sp.Rational(5, 1024)
        * r2
        * t**2
        * (r2**2 - 16 * s0)
    )
    assert sp.expand(obstruction - expected) == 0
    return {
        "obstruction": obstruction,
        "forced_s0": r2**2 / 16,
    }


def eliminate_e3():
    """Kill e3 at the s0 value forced by the normalized tail."""
    r, s, w, e, rows11, rows10, rows9, rows8 = rows_through_e8()
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
        e[2]: 0,
        q9: q9_value,
        s[0]: r[2] ** 2 / 16,
        p30: r[2] ** 2 * w[0] / 32,
        p31: (
            x + r[2] ** 2 * w[1] / 16 + s[1] * w[0]
        )
        / 2,
    }

    # E10[h3] first supplies the displayed p30 value as a square.
    square0 = sp.factor(
        rows10[3].subs(
            {
                e[2]: 0,
                q9: q9_value,
                s[0]: r[2] ** 2 / 16,
            }
        )
    )
    assert sp.expand(
        square0
        + sp.Rational(9, 2)
        * (2 * p30 - r[2] ** 2 * w[0] / 16) ** 2
    ) == 0

    resonance = sp.cancel(rows11[6].subs(values))
    assert sp.factor(sp.expand(resonance).coeff(q7)) == (
        -sp.Rational(7, 512) * r[2] ** 4
    )
    values[q7] = sp.solve(resonance, q7)[0]

    row10 = sp.cancel(rows10[5].subs(values).subs(values))
    row9 = sp.cancel(rows9[3].subs(values).subs(values))
    row8 = sp.cancel(rows8[1].subs(values).subs(values))
    normalized10 = sp.cancel(-sp.Rational(131072, 3) * row10)
    normalized9 = sp.cancel(
        -sp.Rational(262144, 3) * row9 / r[2]
    )
    normalized8 = sp.cancel(
        sp.Rational(4194304, 3) * row8 / r[2] ** 2
    )
    f9 = (
        r[2] * x**2
        - sp.Rational(3, 2) * r[2] ** 2 * e[3] * x
        + sp.Rational(5, 8) * r[2] ** 3 * e[3] ** 2
    )
    f8 = (
        2 * x**2
        - 2 * r[2] * e[3] * x
        + sp.Rational(3, 4) * r[2] ** 2 * e[3] ** 2
    )
    assert sp.expand(
        normalized10 - normalized9 - 81920 * f9 / r[2]
    ) == 0
    assert sp.expand(
        normalized10 + normalized8 - 81920 * f8
    ) == 0
    basis = sp.groebner(
        (f9 / r[2], f8),
        x,
        e[3],
        order="grevlex",
        domain=sp.QQ.frac_field(r[2]),
    )
    assert basis.reduce(e[3] ** 3)[1] == 0
    return {
        "tail_value": r[2] ** 2 / 16,
        "e3_consequence": e[3] ** 3,
    }


def main() -> None:
    result = eliminate_e2()
    tail = negative_tail_constraint()
    final = eliminate_e3()
    print("h-adic chart: r0=r1=0, r2!=0")
    print("required p6 vertex supplies r4!=0")
    print("coprime endpoint factors force", result["q9_deviation"], "= 0")
    print("exceptional component E8[h1]:", result["e2_final_row"], "= 0")
    print("negative-tail L13 cokernel:", tail["obstruction"], "= 0")
    print("paired-row consequence:", final["e3_consequence"], "= 0")
    print("therefore h^4 divides D4=p4-s^2/4-r*w/2")
    print("RESULT: EXACT FULL-STRATUM r2-CHART CONSTANT DESCENT PASSES")


if __name__ == "__main__":
    main()
