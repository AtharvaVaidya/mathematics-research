#!/usr/bin/env python3
"""Exact H1 divisibility on the case-c h-adic chart r0 != 0.

Work in the normalized a=b=1 coordinates after the universal descent

    p7 = h^4*r,                 r=r0+...+r4*h^4,
    p6 = r^2/4 + h^4*s,         s=s0+...+s3*h^3.

For D5=p5-r*s/2, this verifier proves that the coefficients of
h^0,h^1,h^2,h^3 in D5 vanish whenever r0 is nonzero.  In fact the upper
identities E15,E14,E13 already suffice: E15 and E14 first solve the two
raw Q resonances, and four square rows then kill the four coefficients of
D5 successively.

All calculations are exact over Q in symbolic parameters.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_next_descent import DescendingRecurrence


def build_through_p5() -> tuple[
    DescendingRecurrence,
    sp.Symbol,
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
    sp.Expr,
    sp.Expr,
]:
    """Construct p7,p6,p5 in square-root normal form."""
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

    r = sp.symbols("r0:5")
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
            # The killed q11 resonance leaves its forced approximate-cube
            # coefficient 3*r3/2.
            sp.symbols("q11_11"): 3 * r[3] / 2,
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


def resonance_and_first_two_squares() -> dict[str, sp.Expr]:
    """Verify E15/E14's triangular resonance and defect chain."""
    recurrence, _h, r, s, p5, r_poly, s_poly = (
        build_through_p5()
    )
    recurrence.introduce(16)
    compatibility15 = dict(recurrence.introduce(15)[0])

    q10_raw = sp.symbols("q10_10")
    q10_value = (
        6 * r[2] * r[4]
        + 3 * r[3] ** 2
        + 6 * s[2]
    ) / 4
    equation15 = sp.factor(compatibility15[5])
    assert sp.expand(
        equation15
        - sp.Rational(45, 64)
        * r[0] ** 3
        * (
            -4 * q10_raw
            + 6 * r[2] * r[4]
            + 3 * r[3] ** 2
            + 6 * s[2]
        )
    ) == 0
    # Since r0!=0, E15[h^5]=0 gives q10_raw=q10_value.
    recurrence.substitute({q10_raw: q10_value})

    compatibility14 = dict(recurrence.introduce(14)[0])
    base = sp.expand(r_poly * s_poly / 2)
    w0, w1 = sp.symbols("w0 w1")
    low_substitutions = {
        p5[0]: base.coeff(recurrence.h, 0) + w0,
        p5[1]: base.coeff(recurrence.h, 1) + w1,
    }

    equation_w0 = sp.factor(
        compatibility14[3].subs(low_substitutions)
    )
    assert equation_w0 == -30 * w0**2

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
    q9_value = q9_numerator / 8
    equation_q9 = sp.factor(
        compatibility14[4].subs(low_substitutions).subs(w0, 0)
    )
    assert sp.expand(
        equation_q9
        - sp.Rational(135, 1024)
        * r[0] ** 3
        * (q9_numerator - 8 * q9_raw)
    ) == 0
    # E14[h^4]=0 gives q9_raw=q9_value on this chart.

    equation_w1 = sp.factor(
        compatibility14[5]
        .subs(low_substitutions)
        .subs({w0: 0, q9_raw: q9_value})
    )
    assert equation_w1 == -24 * w1**2
    return {
        "E15_h5": equation15,
        "E14_h3": equation_w0,
        "E14_h4": equation_q9,
        "E14_h5": equation_w1,
    }


def last_two_squares() -> dict[str, sp.Expr]:
    """Verify that E13 successively kills the h^2 and h^3 defects."""
    recurrence, h, r, s, p5, r_poly, s_poly = build_through_p5()
    q10_value = (
        6 * r[2] * r[4]
        + 3 * r[3] ** 2
        + 6 * s[2]
    ) / 4
    base = sp.expand(r_poly * s_poly / 2)
    w2, w3 = sp.symbols("w2 w3")
    q9_value = (
        12 * p5[5]
        + 3 * r[1] * r[4] ** 2
        + 6 * r[2] * r[3] * r[4]
        + 6 * r[2] * s[3]
        + r[3] ** 3
        + 6 * r[3] * s[2]
        + 6 * r[4] * s[1]
    ) / 8
    recurrence.substitute(
        {
            sp.symbols("q10_10"): q10_value,
            sp.symbols("q9_9"): q9_value,
            p5[0]: base.coeff(h, 0),
            p5[1]: base.coeff(h, 1),
            p5[2]: base.coeff(h, 2) + w2,
            p5[3]: base.coeff(h, 3) + w3,
        }
    )
    recurrence.introduce(16)
    recurrence.introduce(15)
    recurrence.introduce(14)
    compatibility13 = dict(recurrence.introduce(13)[0])

    equation_w2 = sp.factor(compatibility13[3])
    assert equation_w2 == sp.Rational(27, 2) * r[0] * w2**2

    equation_w3 = sp.factor(
        compatibility13[5].subs(w2, 0)
    )
    assert equation_w3 == sp.Rational(21, 2) * r[0] * w3**2
    return {
        "E13_h3": equation_w2,
        "E13_h5_after_w2": equation_w3,
    }


def main() -> None:
    resonance_and_first_two_squares()
    final = last_two_squares()
    print("h-adic chart: r0 != 0")
    print("E15/E14 solve q10_10,q9_9 and force [h^0,h^1]D5=0")
    print("E13 h^3 square:", final["E13_h3"])
    print("E13 h^5 square after [h^2]D5=0:", final["E13_h5_after_w2"])
    print("proved [h^0,...,h^3](p5-r*s/2)=0")
    print("therefore h^4 divides p5-r*s/2 on the r0!=0 chart")
    print("RESULT: EXACT r0-UNIT-CHART [y]H DIVISIBILITY PASSES")


if __name__ == "__main__":
    main()
