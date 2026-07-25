#!/usr/bin/env python3
"""Exact H1 divisibility on the chart r0=r1=0, r2!=0.

The normalized square-root data are

    r=h^2*(r2+r3*h+r4*h^2),    p6=r^2/4+h^4*s.

For D5=p5-r*s/2, the rows through E11 prove that its h^0,h^1,h^2
coefficients vanish.  The high-endpoint proof of the raw q10 resonance
uses r4!=0.  This is not an extra chart restriction in the full case-c
stratum: the required p6 vertex and

    [h^8]p6 = r4^2/4

force r4!=0 before the h-adic chart split.  The endpoint identity below is
kept denominator-free so that this dependence is explicit.  If the
required vertex is discarded, the artificial r4=0 endpoint subsystem does
leave q10 free.
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

    r2, r3, r4 = sp.symbols("r2 r3 r4")
    r = (sp.Integer(0), sp.Integer(0), r2, r3, r4)
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


def eliminate_through_h2() -> dict[str, sp.Expr]:
    """Prove [h^0,h^1,h^2]D5=0 by exact square/radical rows."""
    recurrence, h, r, s, p5, r_poly, s_poly = build_through_p5()
    recurrence.introduce(16)
    recurrence.introduce(15)
    compatibility14 = dict(recurrence.introduce(14)[0])

    assert compatibility14[3] == -30 * p5[0] ** 2
    assert sp.factor(
        compatibility14[5].subs(p5[0], 0)
    ) == -24 * p5[1] ** 2

    base = sp.expand(r_poly * s_poly / 2)
    w2 = sp.symbols("w2")
    recurrence.substitute(
        {
            p5[0]: 0,
            p5[1]: 0,
            p5[2]: base.coeff(h, 2) + w2,
        }
    )
    compatibility13 = dict(recurrence.introduce(13)[0])
    compatibility12 = dict(recurrence.introduce(12)[0])
    compatibility11 = dict(recurrence.introduce(11)[0])

    p4_0 = sp.symbols("p4_0")
    L = s[0] ** 2 - 4 * p4_0
    equation13 = sp.factor(compatibility13[5])
    equation12 = sp.factor(compatibility12[3])
    equation11 = sp.factor(compatibility11[1])
    assert sp.expand(
        equation13
        - sp.Rational(21, 2) * w2 * (L + r[2] * w2)
    ) == 0
    expected12 = (
        -2 * L**2
        + 3 * L * r[2] * w2
        + 3 * r[2] ** 2 * w2**2
        + 16 * s[0] * w2**2
    )
    assert sp.expand(
        equation12 - sp.Rational(3, 4) * expected12
    ) == 0
    expected11 = (
        L**2 * r[2]
        + 2 * L * s[0] * w2
        - 6 * r[2] * s[0] * w2**2
        - 12 * w2**3
    )
    assert sp.expand(
        equation11 + sp.Rational(3, 8) * expected11
    ) == 0

    # Work over Q(r2), legitimate on the r2-unit chart.  The radical
    # consequence w2^3 belongs to the ideal of the three displayed rows.
    ell = sp.symbols("ell")
    ideal12 = (
        -2 * ell**2
        + 3 * ell * r[2] * w2
        + 3 * r[2] ** 2 * w2**2
        + 16 * s[0] * w2**2
    )
    ideal11 = (
        ell**2 * r[2]
        + 2 * ell * s[0] * w2
        - 6 * r[2] * s[0] * w2**2
        - 12 * w2**3
    )
    basis = sp.groebner(
        (
            w2 * (ell + r[2] * w2),
            ideal12,
            ideal11,
        ),
        ell,
        s[0],
        w2,
        order="grevlex",
        domain=sp.QQ.frac_field(r[2]),
    )
    assert basis.reduce(w2**3)[1] == 0
    return {
        "E13_h5": equation13,
        "E12_h3": equation12,
        "E11_h1": equation11,
        "ideal_consequence": w2**3,
    }


def q10_endpoint_forcing() -> dict[str, sp.Expr]:
    """Verify the denominator-free endpoint forcing and its exact scope."""
    recurrence, h, r, s, p5, r_poly, s_poly = build_through_p5()
    recurrence.introduce(16)
    recurrence.introduce(15)
    compatibility14 = dict(recurrence.introduce(14)[0])
    compatibility13 = dict(recurrence.introduce(13)[0])

    q10_raw = sp.symbols("q10_10")
    q10_value = (
        6 * r[2] * r[4]
        + 3 * r[3] ** 2
        + 6 * s[2]
    ) / 4
    endpoint14 = sp.factor(compatibility14[17])
    endpoint13 = sp.factor(compatibility13[17])
    p5_7 = p5[7]

    # The full case-c support requires the h^8 vertex of p6 to be
    # nonzero.  Since deg(s)<=3, this coefficient is exactly r4^2/4.
    p6_poly = sp.expand(r_poly**2 / 4 + h**4 * s_poly)
    required_vertex = p6_poly.coeff(h, 8)
    assert required_vertex == r[4] ** 2 / 4

    # Do not divide either compatibility row by r4.  Their polynomial
    # combination is r4 times a square.  On the required-vertex stratum
    # r4 is a unit, so the square vanishes.
    denominator_free_square = sp.factor(
        256 * r[4] * endpoint14 - 512 * endpoint13
    )
    assert sp.expand(
        denominator_free_square
        - 2688
        * r[4]
        * (p5_7 - r[4] * s[3] / 2) ** 2
    ) == 0

    # Retain the old localized expression as a consistency check, but
    # it is no longer the proof certificate used by this function.
    square = sp.factor(
        256 * endpoint14 - 512 * endpoint13 / r[4]
    )
    assert sp.expand(
        square - 2688 * (p5_7 - r[4] * s[3] / 2) ** 2
    ) == 0
    resonance = sp.factor(
        endpoint14.subs(p5_7, r[4] * s[3] / 2)
    )
    assert sp.expand(
        resonance
        + sp.Rational(5, 64)
        * r[4] ** 4
        * (q10_raw - q10_value)
    ) == 0

    # Exact boundary of the claim: without the required p6 vertex,
    # r4=0 makes E13[h^17] identically zero and E14[h^17]=12*p5_7^2.
    # Thus p5_7=0 solves both rows for every value of q10_raw.
    endpoint14_r4_zero = sp.factor(endpoint14.subs(r[4], 0))
    endpoint13_r4_zero = sp.factor(endpoint13.subs(r[4], 0))
    assert endpoint14_r4_zero == 12 * p5_7**2
    assert endpoint13_r4_zero == 0
    assert endpoint14_r4_zero.subs(p5_7, 0) == 0
    assert endpoint13_r4_zero.subs(p5_7, 0) == 0
    return {
        "required_p6_vertex": required_vertex,
        "denominator_free_square": denominator_free_square,
        "endpoint_square": square,
        "q10_relation": resonance,
        "r4_zero_E14": endpoint14_r4_zero,
        "r4_zero_E13": endpoint13_r4_zero,
    }


def eliminate_h3() -> dict[str, sp.Expr]:
    """Eliminate w3=[h^3]D5, including the complementary s0=0 chart."""
    recurrence, h, r, s, p5, r_poly, s_poly = build_through_p5()
    base = sp.expand(r_poly * s_poly / 2)
    w3, x = sp.symbols("w3 x")
    q10_base = (
        6 * r[2] * r[4]
        + 3 * r[3] ** 2
        + 6 * s[2]
    ) / 4
    recurrence.substitute(
        {
            sp.symbols("q10_10"): q10_base,
            p5[0]: 0,
            p5[1]: 0,
            p5[2]: base.coeff(h, 2),
            p5[3]: base.coeff(h, 3) + w3,
        }
    )
    recurrence.introduce(16)
    recurrence.substitute(
        {
            sp.symbols("p4_0"): s[0] ** 2 / 4,
            sp.symbols("p4_1"): (x + s[0] * s[1]) / 2,
        }
    )
    for grade in (15, 14, 13, 12):
        recurrence.introduce(grade)
    compatibility11 = dict(recurrence.introduce(11)[0])
    compatibility10 = dict(recurrence.introduce(10)[0])
    compatibility9 = dict(recurrence.introduce(9)[0])

    bracket11 = (
        2560 * r[2] ** 3 * w3**2
        - 5120 * r[2] ** 2 * w3 * x
        + 9216 * r[2] * s[0] * w3**2
        + 2560 * r[2] * x**2
        - 28672 * s[0] * w3 * x
    )
    bracket10 = (
        -2560 * r[2] ** 2 * w3**2
        + 5120 * r[2] * w3 * x
        - 2048 * s[0] * w3**2
        + 1024 * x**2
    )
    equation11 = sp.factor(compatibility11[3])
    equation10 = sp.factor(compatibility10[1])
    assert sp.expand(
        equation11 + sp.Rational(3, 8192) * bracket11
    ) == 0
    assert sp.expand(
        equation10
        - sp.Rational(3, 8192) * s[0] * bracket10
    ) == 0

    # On s0!=0, both brackets vanish.  Over Q(r2,s0), their exact ideal
    # contains w3^3.
    basis = sp.groebner(
        (bracket11, bracket10),
        x,
        w3,
        order="grevlex",
        domain=sp.QQ.frac_field(r[2], s[0]),
    )
    assert basis.reduce(w3**3)[1] == 0

    # On s0=0 the E10 row vanishes identically.  E11 is a square giving
    # x=r2*w3.  The next row E9[h^0] then becomes a nonzero unit times
    # r2^2*w3^3.
    equation11_zero = sp.factor(equation11.subs(s[0], 0))
    assert sp.expand(
        equation11_zero
        + sp.Rational(15, 16)
        * r[2]
        * (x - r[2] * w3) ** 2
    ) == 0
    equation9_zero = sp.factor(
        compatibility9[0].subs(s[0], 0)
    )
    assert sp.expand(
        equation9_zero
        - sp.Rational(15, 32)
        * w3
        * x
        * (2 * x - r[2] * w3)
    ) == 0
    final_zero = sp.factor(equation9_zero.subs(x, r[2] * w3))
    assert final_zero == sp.Rational(15, 32) * r[2] ** 2 * w3**3
    return {
        "E11_h3": equation11,
        "E10_h1": equation10,
        "s0_unit_consequence": w3**3,
        "E11_h3_on_s0_zero": equation11_zero,
        "E9_h0_on_s0_zero": final_zero,
    }


def main() -> None:
    q10_endpoint_forcing()
    low = eliminate_through_h2()
    final = eliminate_h3()
    print("h-adic chart: r0=r1=0, r2!=0")
    print("required p6 vertex forces r4!=0")
    print("denominator-free endpoint rows force the raw q10 resonance")
    print("middle ideal consequence:", low["ideal_consequence"], "= 0")
    print("s0-unit consequence:", final["s0_unit_consequence"], "= 0")
    print("s0=0 endpoint:", final["E9_h0_on_s0_zero"], "= 0")
    print("proved [h^0,...,h^3](p5-r*s/2)=0")
    print("therefore h^4 divides p5-r*s/2 on the r2-unit chart")
    print("RESULT: EXACT FULL-STRATUM r2-CHART [y]H DIVISIBILITY PASSES")


if __name__ == "__main__":
    main()
