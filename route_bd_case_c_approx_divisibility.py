#!/usr/bin/env python3
"""Exact chart proof that the third approximate-root coefficient is polynomial.

Assume the universal case-c conclusions already proved by the preceding
descending blocks:

    p_7 = h^4*r,  deg(r)=4,
    h^2 divides p_6-r^2/(4*a),
    the q_11 resonance is zero.

This file constructs the grade-15 and grade-14 compatibility equations with
all parameters still symbolic.  Three exhaustive h-adic charts prove

    h^4 divides p_6-r^2/(4*a).

Equivalently, the y^2 coefficient of H=(P**(1/2))_+ is a polynomial in h.
No coefficient is numerically specialized.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_next_descent import DescendingRecurrence


def numerator(expression: sp.Expr) -> sp.Expr:
    return sp.factor(sp.fraction(sp.together(expression))[0])


def build_compatibilities() -> tuple[
    sp.Symbol,
    sp.Symbol,
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
    dict[int, sp.Expr],
    dict[int, sp.Expr],
]:
    recurrence = DescendingRecurrence()
    for grade in (19, 18, 17, 16):
        recurrence.introduce(grade)

    a, b = recurrence.a, recurrence.b
    p7 = sp.symbols("p7_0:9")
    p6 = sp.symbols("p6_0:9")
    p5 = sp.symbols("p5_0:9")
    q11_resonance_slot = sp.symbols("q11_11")

    # The first four p7 coefficients vanish, p6 has its two low square
    # coefficients and required high square coefficient, and the exact
    # endpoint obstruction has killed the q11 resonance.
    recurrence.substitute(
        {
            p7[0]: 0,
            p7[1]: 0,
            p7[2]: 0,
            p7[3]: 0,
            p6[0]: p7[4] ** 2 / (4 * a),
            p6[1]: p7[4] * p7[5] / (2 * a),
            p6[8]: p7[8] ** 2 / (4 * a),
            q11_resonance_slot: 3 * b * p7[7] / (2 * a),
        }
    )
    compatibility15 = dict(recurrence.introduce(15)[0])
    compatibility14 = dict(recurrence.introduce(14)[0])
    return (
        a,
        b,
        p7,
        p6,
        p5,
        compatibility15,
        compatibility14,
    )


def verify_three_charts() -> None:
    (
        a,
        b,
        p7,
        p6,
        p5,
        compatibility15,
        compatibility14,
    ) = build_compatibilities()

    r0, r1, r2, r3, _r4 = p7[4:9]
    defect2 = 4 * a * p6[2] - 2 * r0 * r2 - r1**2
    defect3 = 2 * a * p6[3] - r0 * r3 - r1 * r2

    # Chart 1: r0 != 0.  Grade 15 first forces defect2=0.
    assert sp.simplify(
        compatibility15[3]
        - 33 * b * r0 * defect2**2 / (32 * a**4)
    ) == 0
    square2_chart0 = {p6[2]: (2 * r0 * r2 + r1**2) / (4 * a)}

    # The next two equations are linear in the raw q10 resonance.  Their
    # exact resultant is a nonzero unit times r0^5*defect3^2.
    q10_slot = sp.symbols("q10_10")
    equation15_chart0 = numerator(
        compatibility15[5].subs(square2_chart0)
    )
    equation14_chart0 = numerator(
        compatibility14[1].subs(square2_chart0)
    )
    resultant_chart0 = sp.factor(
        sp.resultant(
            equation15_chart0, equation14_chart0, q10_slot
        )
    )
    assert resultant_chart0 == (
        181440 * a**2 * b * r0**5 * defect3**2
    )
    # Since a,b,r0 are nonzero on this chart, defect3=0.

    # Chart 2: r0=0 and r1!=0.  The next coefficient of grade 15 forces
    # defect2=0.
    chart1 = {r0: 0}
    defect2_chart1 = sp.expand(defect2.subs(chart1))
    assert sp.simplify(
        compatibility15[4].subs(chart1)
        - 15
        * b
        * r1
        * defect2_chart1**2
        / (16 * a**4)
    ) == 0
    square2_chart1 = {
        r0: 0,
        p6[2]: r1**2 / (4 * a),
    }
    defect3_chart1 = sp.expand(defect3.subs(square2_chart1))
    equation15_chart1 = sp.factor(
        compatibility15[6].subs(square2_chart1)
    )
    equation14_chart1 = sp.factor(
        compatibility14[3].subs(square2_chart1)
    )
    assert sp.factor(equation15_chart1) == (
        -3
        * b
        * defect3_chart1
        * (
            8 * a**2 * p5[0]
            - 2 * a * p6[3] * r1
            + r1**2 * r2
        )
        / a**4
    )

    # If defect3 were nonzero, the second factor above would vanish.
    # Its resultant with the grade-14 equation is again a nonzero unit
    # times defect3^2.
    reduced_factor = sp.factor(
        equation15_chart1 / defect3_chart1
    )
    resultant_chart1 = sp.factor(
        sp.resultant(
            numerator(reduced_factor),
            numerator(equation14_chart1),
            p5[0],
        )
    )
    assert resultant_chart1 == (
        -8640
        * a**4
        * b**3
        * r1**2
        * defect3_chart1**2
    )
    # Since a,b,r1 are nonzero, defect3=0.

    # Chart 3: r0=r1=0 (including both the double-zero and higher-zero
    # cases).  Grade 14 directly forces p6_2, then p5_0, then p6_3.
    chart2 = {r0: 0, r1: 0}
    equation1 = sp.factor(compatibility14[1].subs(chart2))
    assert equation1 == 6 * b * p6[2] ** 3 / a**2

    chart2_p6 = {**chart2, p6[2]: 0}
    equation3 = sp.factor(compatibility14[3].subs(chart2_p6))
    assert equation3 == -30 * b * p5[0] ** 2 / a

    chart2_p5 = {**chart2_p6, p5[0]: 0}
    equation4 = sp.factor(compatibility14[4].subs(chart2_p5))
    assert equation4 == 9 * b * p6[3] ** 3 / (2 * a**2)
    # Thus p6_2=p6_3=0, which is defect2=defect3=0 on this chart.


def main() -> None:
    verify_three_charts()
    print("case-c approximate-root h-adic charts: r0!=0, r0=0/r1!=0, r0=r1=0")
    print("all grade-15/14 identities checked over Q(a,b) with symbolic parameters")
    print("proved h^4 divides p6-r^2/(4*a)")
    print("therefore [y^2](P^(1/2))_+ is polynomial in h")
    print("RESULT: EXACT UNIVERSAL APPROXIMATE-ROOT DIVISIBILITY PASSES")


if __name__ == "__main__":
    main()
