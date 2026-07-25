#!/usr/bin/env python3
"""First exact descent steps for the constant coefficient of case-c H.

Work in the normalized maximal h-adic chart

    p8=h^8,  p7=h^8,
    p6=h^8/4+h^4*S,
    p5=h^4*(S/2+W),

where the previously proved endpoint and middle descents give
deg(S)<=3 and deg(W)<=2.  If H=(P^(1/2))_+, then

    [y^0]H = D4/(2*h^4),
    D4=p4-S^2/4-h^4*W/2.

Writing D4=sum(e_i*h^i), this verifier proves e0=e1=e2=e3=0
universally on the maximal chart.  Thus the constant coefficient of H
is polynomial throughout this chart.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_middle_divisibility import normalized_recurrence


def build_d4_recurrence() -> tuple[
    object,
    sp.Symbol,
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
]:
    """Build the normalized recurrence through the p4 block."""
    recurrence, s, p5, _p6 = normalized_recurrence()
    h = recurrence.h
    w = sp.symbols("w0:3")
    e = sp.symbols("e0:7")
    s_poly = sum(s[index] * h**index for index in range(4))
    w_poly = sum(w[index] * h**index for index in range(3))
    p5_poly = sp.expand(h**4 * (s_poly / 2 + w_poly))

    recurrence.substitute(
        {
            **{
                p5[index]: p5_poly.coeff(h, index)
                for index in range(8)
            },
            # Forced by the two high endpoint rows on this chart.
            sp.symbols("q10_10"): 3 * s[2] / 2,
        }
    )
    recurrence.introduce(16)
    p4 = sp.symbols("p4_0:7")
    defect = sum(e[index] * h**index for index in range(7))
    p4_poly = sp.expand(
        s_poly**2 / 4 + h**4 * w_poly / 2 + defect
    )
    recurrence.substitute(
        {
            p4[index]: p4_poly.coeff(h, index)
            for index in range(7)
        }
    )
    return recurrence, h, s, w, e


def universal_first_two_coefficients() -> dict[str, sp.Expr]:
    """Prove e0=e1=0 from the four low grade-12 rows."""
    recurrence, _h, _s, _w, e = build_d4_recurrence()
    for grade in (15, 14, 13):
        recurrence.introduce(grade)
    compatibility12 = dict(recurrence.introduce(12)[0])

    expected = {
        3: -24 * e[0] ** 2,
        4: -42 * e[0] * e[1],
        5: -18 * (2 * e[0] * e[2] + e[1] ** 2),
        6: -30 * (e[0] * e[3] + e[1] * e[2]),
    }
    for degree, equation in expected.items():
        assert sp.expand(compatibility12[degree] - equation) == 0
    assert sp.factor(
        compatibility12[5].subs(e[0], 0)
    ) == -18 * e[1] ** 2
    return {
        "E12_h3": compatibility12[3],
        "E12_h5_after_e0": compatibility12[5].subs(e[0], 0),
    }


def s0_unit_third_coefficient() -> dict[str, sp.Expr]:
    """Prove e2=0 on s0!=0 by an exact two-row radical consequence."""
    recurrence, _h, s, w, e = build_d4_recurrence()
    for grade in (15, 14, 13, 12):
        recurrence.introduce(grade)
    recurrence.substitute({e[0]: 0, e[1]: 0})
    compatibility11 = dict(recurrence.introduce(11)[0])
    compatibility10 = dict(recurrence.introduce(10)[0])

    q9 = sp.symbols("q9_9")
    p3_0 = sp.symbols("p3_0")
    x = sp.symbols("x")
    endpoint = sp.factor(compatibility11[4])
    assert sp.expand(
        endpoint
        - sp.Rational(45, 128)
        * s[0] ** 3
        * (-2 * q9 + 3 * s[1] + 3 * w[1])
    ) == 0
    q9_value = 3 * (s[1] + w[1]) / 2

    equation11 = sp.factor(
        compatibility11[5].subs(q9, q9_value)
    )
    assert sp.expand(
        equation11
        + 15 * e[2] * (2 * p3_0 - s[0] * w[0])
    ) == 0
    equation10 = sp.factor(compatibility10[3])
    assert sp.expand(
        equation10
        + sp.Rational(9, 2)
        * (
            (2 * p3_0 - s[0] * w[0]) ** 2
            - 2 * s[0] * e[2] ** 2
        )
    ) == 0

    # On s0!=0, the endpoint first fixes q9.  Replacing
    # 2*p3_0-s0*w0 by x, the two remaining brackets generate an ideal
    # containing e2^3 over Q(s0).
    basis = sp.groebner(
        (
            e[2] * x,
            x**2 - 2 * s[0] * e[2] ** 2,
        ),
        x,
        e[2],
        order="grevlex",
        domain=sp.QQ.frac_field(s[0]),
    )
    assert basis.reduce(e[2] ** 3)[1] == 0
    return {
        "E11_h4": endpoint,
        "E11_h5": equation11,
        "E10_h3": equation10,
        "ideal_consequence": e[2] ** 3,
    }


def s0_zero_third_coefficient() -> dict[str, sp.Expr]:
    """Prove e2=0 on s0=0 by a division-free four-row ideal."""
    recurrence, h, s, w, e = build_d4_recurrence()

    # Include the fixed p_-1=z=h+t block before the grades at which it
    # enters.  It changes solved image coordinates but not the four low
    # compatibility rows used below.
    t = sp.symbols("t")
    recurrence.p[-1] = h + t
    for grade in (15, 14, 13, 12):
        recurrence.introduce(grade)
    recurrence.substitute({e[0]: 0, e[1]: 0, s[0]: 0})
    compatibility11 = dict(recurrence.introduce(11)[0])
    compatibility10 = dict(recurrence.introduce(10)[0])
    recurrence.introduce(9)
    compatibility8 = dict(recurrence.introduce(8)[0])

    p3_0, p3_1 = sp.symbols("p3_0 p3_1")
    row11_5 = sp.factor(compatibility11[5])
    row11_6 = sp.factor(compatibility11[6])
    row10_4 = sp.factor(compatibility10[4])
    row8_1 = sp.factor(compatibility8[1])
    f1 = e[2] * p3_0
    f2 = (
        -2 * e[2] * p3_1
        + e[2] * s[1] * w[0]
        - 2 * e[3] * p3_0
    )
    f3 = (
        e[2] ** 2 * s[1]
        - 4 * p3_0 * p3_1
        + 2 * p3_0 * s[1] * w[0]
    )
    f4 = (
        4 * e[2] ** 3
        + e[2] ** 2 * s[1] ** 2
        + 2 * e[2] * p3_0 * w[0]
        - 6 * p3_0**2 * s[2]
        - 4 * p3_0 * p3_1 * s[1]
        + 2 * p3_0 * s[1] ** 2 * w[0]
    )
    assert sp.expand(row11_5 + 30 * f1) == 0
    assert sp.expand(row11_6 - 12 * f2) == 0
    assert sp.expand(row10_4 - sp.Rational(15, 2) * f3) == 0
    assert sp.expand(row8_1 - sp.Rational(3, 4) * f4) == 0

    # No coefficient is inverted.  The ideal itself, over the full
    # polynomial parameter ring, contains e2^4.
    basis = sp.groebner(
        (f1, f2, f3, f4),
        e[3],
        p3_0,
        p3_1,
        s[2],
        w[0],
        s[1],
        e[2],
        order="grevlex",
    )
    assert len(basis.polys) == 9
    assert basis.reduce(e[2] ** 4)[1] == 0
    return {
        "E11_h5": row11_5,
        "E11_h6": row11_6,
        "E10_h4": row10_4,
        "E8_h1": row8_1,
        "ideal_consequence": e[2] ** 4,
    }


def s0_unit_fourth_coefficient() -> dict[str, sp.Expr]:
    """Prove e3=0 on s0!=0 by the next paired-row obstruction."""
    recurrence, h, s, w, e = build_d4_recurrence()
    recurrence.p[-1] = h + sp.symbols("t")
    for grade in (15, 14, 13, 12):
        recurrence.introduce(grade)
    recurrence.substitute({e[0]: 0, e[1]: 0, e[2]: 0})
    compatibility11 = dict(recurrence.introduce(11)[0])
    compatibility10 = dict(recurrence.introduce(10)[0])
    compatibility9 = dict(recurrence.introduce(9)[0])
    compatibility8 = dict(recurrence.introduce(8)[0])

    q9, p3_0, p3_1, p3_3, q7 = sp.symbols(
        "q9_9 p3_0 p3_1 p3_3 q7_7"
    )
    q9_value = 3 * (s[1] + w[1]) / 2
    endpoint = sp.factor(compatibility11[4])
    assert sp.expand(
        endpoint
        - sp.Rational(45, 128)
        * s[0] ** 3
        * (-2 * q9 + 3 * s[1] + 3 * w[1])
    ) == 0
    p3_square = sp.factor(
        compatibility10[3].subs(q9, q9_value)
    )
    assert sp.expand(
        p3_square
        + sp.Rational(9, 2) * (2 * p3_0 - s[0] * w[0]) ** 2
    ) == 0
    p3_0_value = s[0] * w[0] / 2

    edge_sum = (
        s[0] * s[3]
        + s[1] * s[2]
        + s[1] * w[2]
        + s[2] * w[1]
        + s[3] * w[0]
    )
    resonance = (
        3 * e[3] + 6 * p3_3 - 4 * q7 + 3 * edge_sum
    )
    substitutions = {q9: q9_value, p3_0: p3_0_value}
    equation11 = sp.factor(compatibility11[6].subs(substitutions))
    assert sp.expand(
        equation11
        - sp.Rational(21, 16) * s[0] ** 2 * resonance
    ) == 0
    q7_value = (3 * e[3] + 6 * p3_3 + 3 * edge_sum) / 4
    substitutions[q7] = q7_value

    x = 2 * p3_1 - s[0] * w[1] - s[1] * w[0]
    equation9 = sp.factor(compatibility9[3].subs(substitutions))
    assert sp.expand(
        equation9 - sp.Rational(15, 2) * s[0] * e[3] * x
    ) == 0
    square_combination = sp.factor(
        compatibility10[5].subs(substitutions)
        - 2 * compatibility8[1].subs(substitutions) / s[0]
    )
    assert sp.expand(
        square_combination
        + sp.Rational(15, 4) * (x**2 - 2 * s[0] * e[3] ** 2)
    ) == 0

    x_symbol = sp.symbols("x")
    basis = sp.groebner(
        (
            e[3] * x_symbol,
            x_symbol**2 - 2 * s[0] * e[3] ** 2,
        ),
        x_symbol,
        e[3],
        order="grevlex",
        domain=sp.QQ.frac_field(s[0]),
    )
    assert basis.reduce(e[3] ** 3)[1] == 0
    return {
        "E9_h3": equation9,
        "square_combination": square_combination,
        "ideal_consequence": e[3] ** 3,
    }


def s0_zero_fourth_coefficient() -> dict[str, sp.Expr]:
    """Prove e3=0 on s0=0, including both s1 subcharts."""
    recurrence, h, s, w, e = build_d4_recurrence()
    recurrence.p[-1] = h + sp.symbols("t")
    for grade in (15, 14, 13, 12):
        recurrence.introduce(grade)
    recurrence.substitute(
        {e[0]: 0, e[1]: 0, e[2]: 0, s[0]: 0}
    )
    recurrence.introduce(11)
    compatibility10 = dict(recurrence.introduce(10)[0])
    compatibility9 = dict(recurrence.introduce(9)[0])
    compatibility8 = dict(recurrence.introduce(8)[0])

    q9, p3_0, p3_1, p2_0 = sp.symbols(
        "q9_9 p3_0 p3_1 p2_0"
    )
    row_p30 = sp.factor(compatibility10[3])
    assert row_p30 == -18 * p3_0**2
    row_p31 = sp.factor(compatibility10[5].subs(p3_0, 0))
    x = -2 * p3_1 + s[1] * w[0]
    assert sp.expand(row_p31 + 3 * x**2) == 0
    p3_substitutions = {
        p3_0: 0,
        p3_1: s[1] * w[0] / 2,
    }

    # First take s1!=0.  An endpoint fixes q9, after which two rows
    # generate an ideal containing e3^3.
    endpoint = sp.factor(
        compatibility9[4].subs(p3_substitutions)
    )
    assert sp.expand(
        endpoint
        + sp.Rational(45, 2048)
        * s[1] ** 4
        * (-2 * q9 + 3 * s[1] + 3 * w[1])
    ) == 0
    q9_value = 3 * (s[1] + w[1]) / 2
    s1_substitutions = {
        **p3_substitutions,
        q9: q9_value,
    }
    y = 4 * p2_0 - w[0] ** 2
    square = sp.factor(compatibility8[3].subs(s1_substitutions))
    assert sp.expand(square + sp.Rational(3, 4) * y**2) == 0
    product = sp.factor(compatibility10[6].subs(s1_substitutions))
    assert sp.expand(
        product
        - sp.Rational(9, 2) * e[3] * (e[3] * s[1] - y)
    ) == 0
    y_symbol = sp.symbols("y")
    unit_basis = sp.groebner(
        (
            y_symbol**2,
            e[3] * (e[3] * s[1] - y_symbol),
        ),
        y_symbol,
        e[3],
        order="grevlex",
        domain=sp.QQ.frac_field(s[1]),
    )
    assert unit_basis.reduce(e[3] ** 3)[1] == 0

    # On s1=0, the same square gives 4*p2_0=w0^2.  The next two
    # division-free rows have an ideal containing e3^5.
    zero_substitutions = {
        p3_0: 0,
        p3_1: 0,
        s[1]: 0,
        p2_0: w[0] ** 2 / 4,
    }
    row9 = sp.factor(compatibility9[5].subs(zero_substitutions))
    assert row9 == sp.Rational(9, 2) * e[3] ** 2 * w[0]
    row8 = sp.factor(compatibility8[4].subs(zero_substitutions))
    p3_2 = sp.symbols("p3_2")
    residual = (
        -128 * e[3] ** 3
        - 768 * e[3] * p3_2 * w[0]
        + 384 * e[3] * s[2] * w[0] ** 2
        + 30 * q9 * w[0] ** 3
        - 45 * w[0] ** 3 * w[1]
    )
    assert sp.expand(row8 + sp.Rational(3, 256) * residual) == 0
    zero_basis = sp.groebner(
        (e[3] ** 2 * w[0], residual),
        p3_2,
        q9,
        w[1],
        s[2],
        w[0],
        e[3],
        order="grevlex",
    )
    assert zero_basis.reduce(e[3] ** 5)[1] == 0
    return {
        "s1_unit_consequence": e[3] ** 3,
        "s1_zero_consequence": e[3] ** 5,
    }


def main() -> None:
    universal_first_two_coefficients()
    unit = s0_unit_third_coefficient()
    zero = s0_zero_third_coefficient()
    fourth_unit = s0_unit_fourth_coefficient()
    fourth_zero = s0_zero_fourth_coefficient()
    print("normalized maximal chart: D4=p4-S^2/4-h^4*W/2")
    print("grade 12 proves [h^0]D4=[h^1]D4=0 universally")
    print("s0-unit ideal consequence:", unit["ideal_consequence"], "= 0")
    print("s0=0 ideal consequence:", zero["ideal_consequence"], "= 0")
    print(
        "fourth coefficient consequences:",
        fourth_unit["ideal_consequence"],
        fourth_zero["s1_unit_consequence"],
        fourth_zero["s1_zero_consequence"],
        "= 0",
    )
    print("therefore h^4 divides D4 on the maximal chart")
    print("RESULT: EXACT MAXIMAL-CHART CONSTANT-COEFFICIENT DESCENT PASSES")


if __name__ == "__main__":
    main()
