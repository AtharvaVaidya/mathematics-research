#!/usr/bin/env python3
"""Exact H1 divisibility on the chart r0=r1=r2=0, r3!=0.

In normalized a=b=1 coordinates,

    r=h^3*(r3+r4*h),       p6=r^2/4+h^4*s.

For D5=p5-r*s/2, the rows through E11 first kill its h^0,h^1,h^2
coefficients.  The displayed q10 resonance value is forced by the
denominator-free high-endpoint identity.  That identity only uses r4!=0,
which follows globally from the required p6 vertex
[h^8]p6=r4^2/4!=0; it does not use r2!=0.  The h^3 coefficient is then
eliminated by E11/E10 when s0 is nonzero and by one final E9[h^0] endpoint
on the complementary s0=0 chart.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_middle_divisibility_r2 import (
    q10_endpoint_forcing,
)
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

    r3, r4 = sp.symbols("r3 r4")
    r = (
        sp.Integer(0),
        sp.Integer(0),
        sp.Integer(0),
        r3,
        r4,
    )
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
    """Prove that the first three coefficients of D5 vanish."""
    recurrence, h, _r, s, p5, _r_poly, _s_poly = (
        build_through_p5()
    )
    recurrence.introduce(16)
    recurrence.introduce(15)
    compatibility14 = dict(recurrence.introduce(14)[0])
    assert compatibility14[3] == -30 * p5[0] ** 2
    assert sp.factor(
        compatibility14[5].subs(p5[0], 0)
    ) == -24 * p5[1] ** 2

    w2 = sp.symbols("w2")
    recurrence.substitute(
        {p5[0]: 0, p5[1]: 0, p5[2]: w2}
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
        equation13 - sp.Rational(21, 2) * w2 * L
    ) == 0
    assert sp.expand(
        equation12
        + sp.Rational(3, 2) * (L**2 - 8 * s[0] * w2**2)
    ) == 0
    assert sp.expand(
        equation11
        + sp.Rational(3, 4)
        * w2
        * (s[0] * L - 6 * w2**2)
    ) == 0

    ell = sp.symbols("ell")
    basis = sp.groebner(
        (
            w2 * ell,
            ell**2 - 8 * s[0] * w2**2,
            w2 * (s[0] * ell - 6 * w2**2),
        ),
        ell,
        s[0],
        w2,
        order="grevlex",
    )
    assert basis.reduce(w2**3)[1] == 0
    return {
        "E13_h5": equation13,
        "E12_h3": equation12,
        "E11_h1": equation11,
        "ideal_consequence": w2**3,
    }


def s0_unit_h3() -> dict[str, sp.Expr]:
    """Eliminate [h^3]D5 on the s0!=0 subchart."""
    recurrence, h, r, s, p5, r_poly, s_poly = build_through_p5()
    base = sp.expand(r_poly * s_poly / 2)
    w3, x = sp.symbols("w3 x")
    q10_value = (3 * r[3] ** 2 + 6 * s[2]) / 4
    recurrence.substitute(
        {
            sp.symbols("q10_10"): q10_value,
            p5[0]: 0,
            p5[1]: 0,
            p5[2]: 0,
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

    equation11 = sp.factor(compatibility11[3])
    equation10 = sp.factor(compatibility10[1])
    assert equation11 == sp.Rational(21, 2) * s[0] * w3 * x
    assert sp.expand(
        equation10
        - sp.Rational(3, 8)
        * s[0]
        * (x**2 - 2 * s[0] * w3**2)
    ) == 0

    basis = sp.groebner(
        (w3 * x, x**2 - 2 * s[0] * w3**2),
        x,
        w3,
        order="grevlex",
        domain=sp.QQ.frac_field(s[0]),
    )
    assert basis.reduce(w3**3)[1] == 0
    return {
        "E11_h3": equation11,
        "E10_h1": equation10,
        "ideal_consequence": w3**3,
    }


def s0_zero_endpoint() -> dict[str, sp.Expr]:
    """Eliminate w3 on s0=0 without dividing by any lower coefficient."""
    recurrence, h, r, _s, p5, r_poly, _s_poly = build_through_p5()
    s1, s2, s3 = sp.symbols("s1 s2 s3")
    w3, x = sp.symbols("w3 x")
    q10_value = (3 * r[3] ** 2 + 6 * s2) / 4
    s_poly = s1 * h + s2 * h**2 + s3 * h**3

    # Replace the generic s block by its s0=0 specialization.
    generic_s = sp.symbols("s0:4")
    recurrence.substitute(
        {
            generic_s[0]: 0,
            generic_s[1]: s1,
            generic_s[2]: s2,
            generic_s[3]: s3,
            sp.symbols("q10_10"): q10_value,
            p5[0]: 0,
            p5[1]: 0,
            p5[2]: 0,
            p5[3]: sp.expand(r_poly * s_poly / 2).coeff(h, 3)
            + w3,
        }
    )
    q9_deviation = sp.symbols("g")
    q9_value = (
        12 * p5[5]
        + r[3] ** 3
        + 6 * r[3] * s2
        + 6 * r[4] * s1
    ) / 8 + q9_deviation
    recurrence.substitute({sp.symbols("q9_9"): q9_value})

    recurrence.introduce(16)
    recurrence.substitute(
        {sp.symbols("p4_0"): 0, sp.symbols("p4_1"): x / 2}
    )
    for grade in (15, 14, 13, 12):
        recurrence.introduce(grade)
    compatibility11 = dict(recurrence.introduce(11)[0])
    recurrence.introduce(10)
    compatibility9 = dict(recurrence.introduce(9)[0])

    p3_0 = sp.symbols("p3_0")
    equation11 = sp.factor(compatibility11[4])
    bracket11 = (
        96 * p3_0 * x
        + 9 * r[3] * x**2
        - 48 * s1 * w3 * x
        - 16 * w3**3
    )
    assert sp.expand(
        equation11 + sp.Rational(3, 16) * bracket11
    ) == 0
    endpoint = sp.factor(compatibility9[0])
    assert endpoint == sp.Rational(15, 16) * w3 * x**2

    # These two rows are exhaustive even when s1=0.  Their exact ideal
    # contains w3^7: set-theoretically, if w3 were nonzero then the E9
    # row would give x=0, and E11 would reduce to 3*w3^3=0.
    basis = sp.groebner(
        (w3 * x**2, bracket11),
        p3_0,
        x,
        w3,
        r[3],
        s1,
        order="grevlex",
    )
    assert basis.reduce(w3**7)[1] == 0
    return {
        "E11_h4": equation11,
        "E9_h0": endpoint,
        "ideal_consequence": w3**7,
    }


def main() -> None:
    # This denominator-free endpoint check proves the q10 formula used
    # below because the required p6 vertex forces r4!=0.  No r2-unit
    # hypothesis enters that check.
    q10_endpoint_forcing()
    low = eliminate_through_h2()
    unit = s0_unit_h3()
    zero = s0_zero_endpoint()
    print("h-adic chart: r0=r1=r2=0, r3!=0")
    print("required p6 vertex forces r4!=0 and hence the q10 resonance")
    print("middle ideal consequence:", low["ideal_consequence"], "= 0")
    print("s0-unit consequence:", unit["ideal_consequence"], "= 0")
    print("s0=0 ideal consequence:", zero["ideal_consequence"], "= 0")
    print("proved [h^0,...,h^3](p5-r*s/2)=0")
    print("therefore h^4 divides p5-r*s/2 on the r3-unit chart")
    print("RESULT: EXACT FULL-STRATUM r3-CHART [y]H DIVISIBILITY PASSES")


if __name__ == "__main__":
    main()
