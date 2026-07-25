#!/usr/bin/env python3
"""Exact middle-grade approximate-root divisibility in one h-adic chart.

This verifier treats the maximal-order chart of the case-c descent.  After
normalizing the nonzero top coefficients, the already-proved upper descent
has

    p8 = h^8,
    p7 = h^8,
    p6 = h^8/4 + h^4*(s0+s1*h+s2*h^2+s3*h^3).

Thus r=h^4 and the numerator of the y coefficient of the canonical
approximate square root is

    D5 = p5 - h^4*(s0+s1*h+s2*h^2+s3*h^3)/2.

The exact compatibility rows through E11 prove that the four low
coefficients p5_0,...,p5_3 vanish.  Equivalently, h^4 divides D5 in this
chart, so [y]H has no pole here.

No numerical sampling or floating-point calculation is used.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_next_descent import DescendingRecurrence


def normalized_recurrence() -> tuple[
    DescendingRecurrence,
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
]:
    """Build the normalized maximal-order chart through the p5 block."""
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

    s = sp.symbols("s0:4")
    p5 = sp.symbols("p5_0:9")

    recurrence.introduce(19)
    p7 = sp.symbols("p7_0:9")
    recurrence.substitute(
        {
            **{
                p7[index]: int(index == 8)
                for index in range(9)
            },
            # The universal endpoint obstruction kills this raw
            # q11 resonance because r3=0 in the present chart.
            sp.symbols("q11_11"): 0,
        }
    )

    recurrence.introduce(18)
    p6 = sp.symbols("p6_0:9")
    p6_values = {
        4: s[0],
        5: s[1],
        6: s[2],
        7: s[3],
        8: sp.Rational(1, 4),
    }
    recurrence.substitute(
        {
            p6[index]: p6_values.get(index, 0)
            for index in range(9)
        }
    )

    recurrence.introduce(17)
    return recurrence, s, p5, p6


def upper_forcing() -> dict[str, sp.Expr]:
    """Verify the upper rows needed by the middle-grade argument."""
    recurrence, s, p5, _p6 = normalized_recurrence()

    recurrence.introduce(16)
    recurrence.introduce(15)
    compatibility14 = dict(recurrence.introduce(14)[0])
    compatibility13 = dict(recurrence.introduce(13)[0])

    # These two square equations successively give p5_0=p5_1=0 over
    # characteristic zero.
    assert sp.factor(compatibility14[3]) == -30 * p5[0] ** 2
    assert sp.factor(
        compatibility14[5].subs(p5[0], 0)
    ) == -24 * p5[1] ** 2

    q10_raw = sp.symbols("q10_10")
    edge14 = sp.factor(compatibility14[17])
    edge13 = sp.factor(compatibility13[17])
    expected14 = (
        1536 * p5[7] ** 2
        - 1536 * p5[7] * s[3]
        - 10 * q10_raw
        + 15 * s[2]
        + 384 * s[3] ** 2
    ) / 128
    expected13 = (
        192 * p5[7] ** 2
        - 192 * p5[7] * s[3]
        - 10 * q10_raw
        + 15 * s[2]
        + 48 * s[3] ** 2
    ) / 256
    assert sp.expand(edge14 - expected14) == 0
    assert sp.expand(edge13 - expected13) == 0

    # The difference of the two zero rows is a nonzero scalar times
    # (p5_7-s3/2)^2.  Substitution into either row then gives the raw
    # resonance q10_10=3*s2/2.
    square = sp.factor(128 * edge14 - 256 * edge13)
    assert sp.expand(
        square - 336 * (2 * p5[7] - s[3]) ** 2
    ) == 0
    raw_resonance = sp.factor(
        edge13.subs(p5[7], s[3] / 2)
    )
    assert sp.expand(
        raw_resonance
        - 5 * (3 * s[2] - 2 * q10_raw) / 256
    ) == 0
    return {
        "p5_0_square": compatibility14[3],
        "p5_1_square": compatibility14[5].subs(p5[0], 0),
        "p5_7_square": square,
        "q10_raw_relation": raw_resonance,
    }


def middle_rows() -> tuple[
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
    dict[int, sp.Expr],
    dict[int, sp.Expr],
    dict[int, sp.Expr],
]:
    """Build E13,E12,E11 after the forced upper substitutions."""
    recurrence, s, p5, _p6 = normalized_recurrence()
    recurrence.substitute(
        {
            p5[0]: 0,
            p5[1]: 0,
            p5[7]: s[3] / 2,
            sp.symbols("q10_10"): 3 * s[2] / 2,
        }
    )
    recurrence.introduce(16)
    recurrence.introduce(15)
    recurrence.introduce(14)
    compatibility13 = dict(recurrence.introduce(13)[0])
    compatibility12 = dict(recurrence.introduce(12)[0])
    compatibility11 = dict(recurrence.introduce(11)[0])
    return s, p5, compatibility13, compatibility12, compatibility11


def eliminate_p5_2() -> dict[str, sp.Expr]:
    """Show that the first possible h^2 pole coefficient is zero."""
    s, p5, compatibility13, compatibility12, compatibility11 = (
        middle_rows()
    )
    p4_0 = sp.symbols("p4_0")
    u = p5[2]

    equation13 = sp.factor(compatibility13[5])
    equation12 = sp.factor(compatibility12[3])
    equation11 = sp.factor(compatibility11[1])
    assert sp.expand(
        equation13
        - sp.Rational(21, 2) * u * (
            s[0] ** 2 - 4 * p4_0
        )
    ) == 0
    assert sp.expand(
        equation12
        + sp.Rational(3, 2) * (
            16 * p4_0**2
            - 8 * p4_0 * s[0] ** 2
            - 8 * u**2 * s[0]
            + s[0] ** 4
        )
    ) == 0
    assert sp.expand(
        equation11
        + sp.Rational(3, 4) * u * (
            -4 * p4_0 * s[0] - 6 * u**2 + s[0] ** 3
        )
    ) == 0

    # Strip the nonzero rational row factors.  The exact Groebner basis
    # contains u^3, proving u=0 at every common zero over characteristic
    # zero (with no case lost by division).
    generators = (
        u * (s[0] ** 2 - 4 * p4_0),
        16 * p4_0**2
        - 8 * p4_0 * s[0] ** 2
        - 8 * u**2 * s[0]
        + s[0] ** 4,
        u * (-4 * p4_0 * s[0] - 6 * u**2 + s[0] ** 3),
    )
    basis = sp.groebner(
        generators,
        p4_0,
        s[0],
        u,
        order="grevlex",
    )
    assert basis.reduce(u**3)[1] == 0
    return {
        "E13_h5": equation13,
        "E12_h3": equation12,
        "E11_h1": equation11,
        "ideal_consequence": u**3,
    }


def eliminate_p5_3() -> dict[str, sp.Expr]:
    """Show that the remaining possible h^3 pole coefficient is zero."""
    s, p5, _compatibility13, compatibility12, compatibility11 = (
        middle_rows()
    )
    p4_0, p4_1 = sp.symbols("p4_0 p4_1")
    u, v = p5[2], p5[3]

    # Having proved u=0, E12[h^3] is a square and hence forces
    # p4_0=s0^2/4.
    square_row = sp.factor(compatibility12[3].subs(u, 0))
    assert sp.expand(
        square_row
        + sp.Rational(3, 2) * (
            -4 * p4_0 + s[0] ** 2
        ) ** 2
    ) == 0
    p4_0_value = s[0] ** 2 / 4
    x = 2 * p4_1 - s[0] * s[1]

    equation12 = sp.factor(
        compatibility12[5].subs(
            {u: 0, p4_0: p4_0_value}
        )
    )
    equation11 = sp.factor(
        compatibility11[3].subs(
            {u: 0, p4_0: p4_0_value}
        )
    )
    assert sp.expand(
        equation12
        + sp.Rational(9, 2) * (
            x**2 - 2 * s[0] * v**2
        )
    ) == 0
    assert sp.expand(
        equation11 - sp.Rational(21, 2) * s[0] * v * x
    ) == 0

    # If s0 is nonzero and v were nonzero, E11 gives x=0 while E12
    # gives s0*v^2=0, a contradiction.  On the complementary chart
    # s0=0, E12 gives p4_1=0; the next E11 row is then exactly 3*v^3.
    zero_s0_row = sp.factor(
        compatibility11[4].subs(
            {
                u: 0,
                s[0]: 0,
                p4_0: 0,
                p4_1: 0,
            }
        )
    )
    assert zero_s0_row == 3 * v**3
    return {
        "E12_h3_square": square_row,
        "E12_h5": equation12,
        "E11_h3": equation11,
        "E11_h4_on_s0_zero": zero_s0_row,
    }


def main() -> None:
    upper_forcing()
    low2 = eliminate_p5_2()
    low3 = eliminate_p5_3()
    print("normalized maximal h-adic chart: r=h^4, p6-r^2/4=h^4*s")
    print("upper rows force p5_0=p5_1=0 and the two edge resonances")
    print("middle ideal consequence:", low2["ideal_consequence"], "= 0")
    print("complementary s0=0 row:", low3["E11_h4_on_s0_zero"], "= 0")
    print("proved p5_0=p5_1=p5_2=p5_3=0")
    print("therefore h^4 divides p5-r*s/2 in this chart")
    print("RESULT: EXACT MAXIMAL-CHART [y]H DIVISIBILITY PASSES")


if __name__ == "__main__":
    main()
