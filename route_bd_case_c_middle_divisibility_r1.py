#!/usr/bin/env python3
"""Exact H1 divisibility on the case-c chart r0=0, r1!=0.

In normalized a=b=1 coordinates, assume

    p7 = h^4*r,          r=h*(r1+r2*h+r3*h^2+r4*h^3),
    p6 = r^2/4+h^4*s,    s=s0+s1*h+s2*h^2+s3*h^3.

Writing D5=p5-r*s/2, this verifier proves that D5 is divisible by h^4.
The resonance/defect equations occur in pairs: E14/E13 separate the raw
q10 resonance from [h]D5, E13/E12 separate q9 from [h^2]D5, and a final
E12 square together with E13 kills [h^3]D5.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_next_descent import DescendingRecurrence


def build_through_p5() -> tuple[
    DescendingRecurrence,
    sp.Symbol,
    tuple[sp.Expr, ...],
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
    sp.Expr,
    sp.Expr,
]:
    recurrence = DescendingRecurrence()
    h = recurrence.h
    t = sp.symbols("t", nonzero=True)
    recurrence.a = sp.Integer(1)
    recurrence.b = sp.Integer(1)
    # Keep the fixed base block p_{-1}=z=h+t in the recurrence.  It
    # first enters at E11; q_{-1}=z^2 first enters at E7, below every
    # identity used in this D5 descent.
    recurrence.p = {-1: h + t, 8: h**8}
    recurrence.q = {12: h**12}

    r1, r2, r3, r4 = sp.symbols("r1 r2 r3 r4")
    r = (sp.Integer(0), r1, r2, r3, r4)
    s = sp.symbols("s0:4")
    r_poly = sum(r[index] * h**index for index in range(5))
    s_poly = sum(s[index] * h**index for index in range(4))

    recurrence.introduce(19)
    p7 = sp.symbols("p7_0:9")
    p7_values = {index + 4: r[index] for index in range(5)}
    recurrence.substitute(
        {
            **{
                p7[index]: p7_values.get(index, 0)
                for index in range(9)
            },
            sp.symbols("q11_11"): 3 * r3 / 2,
        }
    )

    recurrence.introduce(18)
    p6 = sp.symbols("p6_0:9")
    p6_poly = sp.expand(r_poly**2 / 4 + h**4 * s_poly)
    recurrence.substitute(
        {
            p6[index]: p6_poly.coeff(h, index)
            for index in range(9)
        }
    )

    recurrence.introduce(17)
    p5 = sp.symbols("p5_0:9")
    return recurrence, h, r, s, p5, r_poly, s_poly


def first_resonance_pair() -> dict[str, sp.Expr]:
    """Use E14/E13 to force [h^0,h^1]D5=0 and solve q10."""
    recurrence, h, r, s, p5, r_poly, s_poly = build_through_p5()
    recurrence.introduce(16)
    recurrence.introduce(15)
    compatibility14 = dict(recurrence.introduce(14)[0])
    compatibility13 = dict(recurrence.introduce(13)[0])

    # Since r starts at h, [h^0]D5=p5_0.
    equation_w0 = sp.factor(compatibility14[3])
    assert equation_w0 == -30 * p5[0] ** 2

    base = sp.expand(r_poly * s_poly / 2)
    w1 = sp.symbols("w1")
    low = {
        p5[0]: 0,
        p5[1]: base.coeff(h, 1) + w1,
    }
    q10_raw = sp.symbols("q10_10")
    resonance = (
        -20 * q10_raw
        + 30 * r[2] * r[4]
        + 15 * r[3] ** 2
        + 30 * s[2]
    )
    equation14 = sp.factor(compatibility14[5].subs(low))
    equation13 = sp.factor(compatibility13[2].subs(low))
    assert sp.expand(
        equation14
        + (r[1] ** 4 * resonance + 3072 * w1**2) / 128
    ) == 0
    assert sp.expand(
        equation13
        + r[1]
        * (r[1] ** 4 * resonance + 384 * w1**2)
        / 256
    ) == 0

    # On r1!=0, divide the second row by r1.  Subtracting its bracket
    # from the first gives 2688*w1^2=0; then resonance=0.
    q10_value = (
        6 * r[2] * r[4]
        + 3 * r[3] ** 2
        + 6 * s[2]
    ) / 4
    assert sp.expand(resonance.subs(q10_raw, q10_value)) == 0
    return {
        "E14_h3": equation_w0,
        "E14_h5": equation14,
        "E13_h2": equation13,
        "difference_consequence": 2688 * w1**2,
    }


def second_resonance_and_last_defect() -> dict[str, sp.Expr]:
    """Use E13/E12 to force the h^2 and h^3 coefficients of D5."""
    recurrence, h, r, s, p5, r_poly, s_poly = build_through_p5()
    base = sp.expand(r_poly * s_poly / 2)
    w2, w3 = sp.symbols("w2 w3")
    q10_value = (
        6 * r[2] * r[4]
        + 3 * r[3] ** 2
        + 6 * s[2]
    ) / 4
    recurrence.substitute(
        {
            sp.symbols("q10_10"): q10_value,
            p5[0]: 0,
            p5[1]: base.coeff(h, 1),
            p5[2]: base.coeff(h, 2) + w2,
            p5[3]: base.coeff(h, 3) + w3,
        }
    )
    recurrence.introduce(16)
    recurrence.introduce(15)
    recurrence.introduce(14)
    compatibility13 = dict(recurrence.introduce(13)[0])
    compatibility12 = dict(recurrence.introduce(12)[0])

    q9_raw = sp.symbols("q9_9")
    q9_numerator = (
        12 * p5[5]
        + 3 * r[1] * r[4] ** 2
        + 6 * r[2] * r[3] * r[4]
        + 6 * r[2] * s[3]
        + r[3] ** 3
        + 6 * r[3] * s[2]
        + 6 * r[4] * s[1]
    )
    resonance = q9_numerator - 8 * q9_raw
    equation13 = sp.factor(compatibility13[4])
    equation12 = sp.factor(compatibility12[1])
    assert sp.expand(
        equation13
        + 3
        * r[1]
        * (15 * r[1] ** 3 * resonance - 16384 * w2**2)
        / 4096
    ) == 0
    assert sp.expand(
        equation12
        + 9
        * r[1] ** 2
        * (5 * r[1] ** 3 * resonance - 1024 * w2**2)
        / 8192
    ) == 0

    # After dividing by the nonzero r1 factors, the first bracket minus
    # three times the second is -13312*w2^2.  Hence w2=0 and the raw q9
    # resonance has its displayed forced value.
    q9_value = q9_numerator / 8
    p4_0 = sp.symbols("p4_0")
    square = sp.factor(
        compatibility12[3].subs(
            {w2: 0, q9_raw: q9_value}
        )
    )
    last = sp.factor(
        compatibility13[6].subs(
            {w2: 0, q9_raw: q9_value}
        )
    )
    assert sp.expand(
        square
        + sp.Rational(3, 2) * (-4 * p4_0 + s[0] ** 2) ** 2
    ) == 0
    assert sp.expand(
        last
        - 9
        * w3
        * (-4 * p4_0 + r[1] * w3 + s[0] ** 2)
    ) == 0

    # The square row gives 4*p4_0=s0^2.  The last row then becomes
    # 9*r1*w3^2, which forces w3=0 because r1 is a unit on this chart.
    final_square = sp.factor(
        last.subs(p4_0, s[0] ** 2 / 4)
    )
    assert final_square == 9 * r[1] * w3**2
    return {
        "E13_h4": equation13,
        "E12_h1": equation12,
        "w2_difference_consequence": -13312 * w2**2,
        "E12_h3": square,
        "E13_h6_after_square": final_square,
    }


def main() -> None:
    first = first_resonance_pair()
    second = second_resonance_and_last_defect()
    print("h-adic chart: r0=0, r1!=0")
    print("first paired-row consequence:", first["difference_consequence"], "= 0")
    print(
        "second paired-row consequence:",
        second["w2_difference_consequence"],
        "= 0",
    )
    print("final E13 square:", second["E13_h6_after_square"], "= 0")
    print("proved [h^0,...,h^3](p5-r*s/2)=0")
    print("therefore h^4 divides p5-r*s/2 on the r1-unit chart")
    print("RESULT: EXACT r1-UNIT-CHART [y]H DIVISIBILITY PASSES")


if __name__ == "__main__":
    main()
