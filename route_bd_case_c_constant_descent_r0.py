#!/usr/bin/env python3
"""Exact constant-term descent on the case-c chart r0 != 0.

This is the r0-unit analogue of ``route_bd_case_c_constant_descent.py``.
It builds the already normalized coefficients

    p7 = h^4*r,
    p6 = r^2/4 + h^4*s,
    p5 = r*s/2 + h^4*W

and writes

    p4 = s^2/4 + r*W/2 + D4,   D4=sum(e_i*h^i).

The verifier proves e0=e1=e2=e3=0.  The final step uses the high
grade-14 endpoint to kill the top coefficient w3 of W, after which the
low grade-10 row becomes a nonzero multiple of r0^2*e3^2.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_middle_divisibility_r0 import build_through_p5


def build_d4_recurrence():
    """Build the r0-unit recurrence through the p4 block."""
    recurrence, h, r, s, p5, r_poly, s_poly = build_through_p5()
    w = sp.symbols("w0:4")
    e = sp.symbols("e0:7")
    w_poly = sum(w[index] * h**index for index in range(4))
    p5_poly = sp.expand(r_poly * s_poly / 2 + h**4 * w_poly)

    q10_value = (
        6 * r[2] * r[4] + 3 * r[3] ** 2 + 6 * s[2]
    ) / 4
    q9_value = (
        12 * p5_poly.coeff(h, 5)
        + 3 * r[1] * r[4] ** 2
        + 6 * r[2] * r[3] * r[4]
        + 6 * r[2] * s[3]
        + r[3] ** 3
        + 6 * r[3] * s[2]
        + 6 * r[4] * s[1]
    ) / 8
    recurrence.substitute(
        {
            **{
                p5[index]: p5_poly.coeff(h, index)
                for index in range(9)
            },
            sp.symbols("q10_10"): q10_value,
            sp.symbols("q9_9"): q9_value,
        }
    )

    recurrence.introduce(16)
    p4 = sp.symbols("p4_0:7")
    defect = sum(e[index] * h**index for index in range(7))
    p4_poly = sp.expand(
        s_poly**2 / 4 + r_poly * w_poly / 2 + defect
    )
    recurrence.substitute(
        {
            p4[index]: p4_poly.coeff(h, index)
            for index in range(7)
        }
    )
    return recurrence, h, r, s, w, e


def triangular_rows():
    """Return exact resonance substitutions and the first four defects."""
    recurrence, _h, r, _s, w, e = build_d4_recurrence()
    compatibility15 = dict(recurrence.introduce(15)[0])
    compatibility14 = dict(recurrence.introduce(14)[0])
    compatibility13 = dict(recurrence.introduce(13)[0])
    compatibility12 = dict(recurrence.introduce(12)[0])

    q7 = sp.symbols("q7_7")
    resonance13 = sp.factor(compatibility13[6])
    resonance12 = sp.factor(compatibility12[2])
    q7_value = sp.solve(resonance13, q7, dict=True)[0][q7]
    assert sp.factor(resonance12.subs(q7, q7_value)) == 0
    recurrence.substitute({q7: q7_value})

    # Re-read the stored rows under the exact q7 substitution.
    compatibility12 = {
        degree: sp.factor(row.subs(q7, q7_value))
        for degree, row in compatibility12.items()
    }
    assert compatibility12[3] == -24 * e[0] ** 2

    # Restore the fixed p_-1=z=h+t block before grade 11, the first
    # grade at which it contributes.  It then remains present in every
    # lower-grade forcing term.
    recurrence.p[-1] = recurrence.h + sp.symbols("t")
    recurrence.substitute({e[0]: 0})
    compatibility11 = dict(recurrence.introduce(11)[0])
    q6 = sp.symbols("q6_6")
    row12 = sp.factor(compatibility12[5].subs(e[0], 0))
    row11 = sp.factor(compatibility11[1])
    # The two rows share the same q6-linear nuisance.  Their stated
    # combination kills it and forces e1=0 on r0 != 0.
    combination = sp.factor(2 * row11 / r[0] - row12)
    assert combination == sp.Rational(45, 2) * e[1] ** 2
    q6_value = sp.solve(row12.subs(e[1], 0), q6, dict=True)[0][q6]
    recurrence.substitute({e[1]: 0, q6: q6_value})

    all_known = {q7: q7_value, e[0]: 0, e[1]: 0, q6: q6_value}
    compatibility15 = {
        degree: sp.cancel(row.subs(all_known))
        for degree, row in compatibility15.items()
    }
    compatibility14 = {
        degree: sp.cancel(row.subs(all_known))
        for degree, row in compatibility14.items()
    }
    compatibility13 = {
        degree: sp.cancel(row.subs(all_known))
        for degree, row in compatibility13.items()
    }
    compatibility11 = {
        degree: sp.factor(row.subs({e[1]: 0, q6: q6_value}))
        for degree, row in compatibility11.items()
    }
    row_e2 = compatibility11[3]
    assert row_e2 == sp.Rational(21, 2) * r[0] * e[2] ** 2
    recurrence.substitute({e[2]: 0})

    compatibility10 = dict(recurrence.introduce(10)[0])
    q5 = sp.symbols("q5_5")
    q5_value = sp.solve(compatibility10[0], q5, dict=True)[0][q5]
    row_e3 = sp.factor(compatibility10[1].subs(q5, q5_value))
    assert row_e3 == (
        -sp.Rational(9, 256)
        * r[0] ** 2
        * (32 * e[3] ** 2 + 223 * r[0] ** 2 * w[3] ** 2)
    )
    recurrence.substitute({q5: q5_value})
    compatibility10 = {
        degree: sp.cancel(row.subs(q5, q5_value))
        for degree, row in compatibility10.items()
    }
    compatibility15 = {
        degree: sp.cancel(row.subs(e[2], 0))
        for degree, row in compatibility15.items()
    }
    compatibility14 = {
        degree: sp.cancel(row.subs(e[2], 0))
        for degree, row in compatibility14.items()
    }
    compatibility13 = {
        degree: sp.cancel(row.subs(e[2], 0))
        for degree, row in compatibility13.items()
    }
    compatibility12 = {
        degree: sp.cancel(row.subs({e[1]: 0, q6: q6_value, e[2]: 0}))
        for degree, row in compatibility12.items()
    }
    compatibility11 = {
        degree: sp.cancel(row.subs(e[2], 0))
        for degree, row in compatibility11.items()
    }
    endpoint_w3 = sp.factor(compatibility14[17])
    assert endpoint_w3 == 12 * w[3] ** 2
    row_e3_after_endpoint = sp.factor(row_e3.subs(w[3], 0))
    assert row_e3_after_endpoint == (
        -sp.Rational(9, 8) * r[0] ** 2 * e[3] ** 2
    )
    return {
        "recurrence": recurrence,
        "r": r,
        "w": w,
        "e": e,
        "q7_value": q7_value,
        "q6_value": q6_value,
        "q5_value": q5_value,
        "compatibility15": compatibility15,
        "compatibility14": compatibility14,
        "compatibility13": compatibility13,
        "compatibility12": compatibility12,
        "compatibility11": compatibility11,
        "compatibility10": compatibility10,
        "E12_h3": compatibility12[3],
        "e1_combination": combination,
        "E11_h3": row_e2,
        "E14_h17": endpoint_w3,
        "E10_h1": row_e3,
        "E10_h1_after_w3": row_e3_after_endpoint,
    }


def main() -> None:
    data = triangular_rows()
    print("h-adic chart: r0 != 0")
    print("E12 h3:", data["E12_h3"])
    print("e1 resonance-free combination:", data["e1_combination"])
    print("E11 h3 after e0=e1=0:", data["E11_h3"])
    print("E14 h17 endpoint:", data["E14_h17"])
    print("E10 h1 after q5:", data["E10_h1"])
    print("E10 h1 after endpoint:", data["E10_h1_after_w3"])
    print("therefore h^4 divides D4 on the r0-unit chart")
    print("RESULT: EXACT r0-UNIT-CHART CONSTANT DESCENT PASSES")


if __name__ == "__main__":
    main()
