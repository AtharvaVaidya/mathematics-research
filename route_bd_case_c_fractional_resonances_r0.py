#!/usr/bin/env python3
"""Kill the c10,c9,c7,c6,c5 fractional resonances on the r0 chart.

After the square-root descents, write the upper approximate-root normal
form (with a=b=1)

    Q_+ = A12 + c10*A10 + c9*A9 + c8*A8 + ...,
    A_j=(P_+**(j/8))_+.

The previously eliminated c11 term is omitted.  This verifier first
identifies the raw recurrence slots q10_10 and q9_9 with their triangular
approximate-root contributions.  It then uses the exact q7,q6,q5 values
from the full-base constant descent and compares them with A12+c8*P.
The resulting identities force all five displayed fractional constants
to vanish; c8 is retained because A8=P is an integral power.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_approx_root import A, ell, p, y
from route_bd_case_c_middle_divisibility_r0 import (
    resonance_and_first_two_squares,
)
from route_bd_case_c_constant_descent_r0 import triangular_rows


def approximate_root_resonance_slots() -> dict[str, sp.Expr]:
    """Identify the two raw slots in the A_j basis exactly."""
    h = sp.symbols("h")
    r = sp.symbols("r0:5")
    s = sp.symbols("s0:4")
    w = sp.symbols("w0:4")
    r_poly = sum(r[index] * h**index for index in range(5))
    s_poly = sum(s[index] * h**index for index in range(4))
    w_poly = sum(w[index] * h**index for index in range(4))
    p5_poly = sp.expand(r_poly * s_poly / 2 + h**4 * w_poly)
    substitutions = {
        ell: h,
        p[7]: h**4 * r_poly,
        p[6]: r_poly**2 / 4 + h**4 * s_poly,
        p[5]: p5_poly,
    }

    # Extract before specialization.  Expanding the entire A12 after
    # substituting the h-polynomials creates many irrelevant lower
    # coefficients.
    a12_generic = sp.Poly(A[12], y)
    a10_generic = sp.Poly(A[10], y)
    a9_generic = sp.Poly(A[9], y)
    a12_y10 = sp.expand(
        a12_generic.coeff_monomial(y**10).subs(substitutions)
    )
    a12_y9 = sp.expand(
        a12_generic.coeff_monomial(y**9).subs(substitutions)
    )
    a10_y10 = sp.expand(
        a10_generic.coeff_monomial(y**10).subs(substitutions)
    )
    a10_y9 = sp.expand(
        a10_generic.coeff_monomial(y**9).subs(substitutions)
    )
    a9_y9 = sp.expand(
        a9_generic.coeff_monomial(y**9).subs(substitutions)
    )
    cube_q10 = (
        6 * r[2] * r[4] + 3 * r[3] ** 2 + 6 * s[2]
    ) / 4
    cube_q9 = (
        12 * p5_poly.coeff(h, 5)
        + 3 * r[1] * r[4] ** 2
        + 6 * r[2] * r[3] * r[4]
        + 6 * r[2] * s[3]
        + r[3] ** 3
        + 6 * r[3] * s[2]
        + 6 * r[4] * s[1]
    ) / 8

    a12_q10 = a12_y10.coeff(h, 10)
    a12_q9 = a12_y9.coeff(h, 9)
    assert sp.expand(a12_q10 - cube_q10) == 0
    assert sp.expand(a12_q9 - cube_q9) == 0

    # These are the triangular diagonal statements.  A10 contributes
    # one unit to q10_10 and a known lower-triangular term to q9_9;
    # after c10=0, A9 contributes one unit to q9_9.  Terms A8 and below
    # cannot reach y-degrees 10 or 9.
    assert a10_y10.coeff(h, 10) == 1
    a10_to_q9 = a10_y9.coeff(h, 9)
    assert a10_to_q9 == sp.Rational(5, 4) * r[3]
    assert a9_y9.coeff(h, 9) == 1
    return {
        "cube_q10": cube_q10,
        "cube_q9": cube_q9,
        "a10_to_q9": a10_to_q9,
        "p5_h5": p5_poly.coeff(h, 5),
    }


def exact_row_elimination() -> dict[str, sp.Expr]:
    """Substitute qj_j=(A12 slot)+cj into the exact r0 rows."""
    slots = approximate_root_resonance_slots()
    rows = resonance_and_first_two_squares()
    r0 = sp.symbols("r0")
    c10, c9 = sp.symbols("c10 c9")
    q10, q9 = sp.symbols("q10_10 q9_9")

    row10 = sp.factor(
        rows["E15_h5"].subs(q10, slots["cube_q10"] + c10)
    )
    row9_before_c10 = sp.factor(
        rows["E14_h4"].subs(
            {
                q9: (
                    slots["cube_q9"]
                    + slots["a10_to_q9"] * c10
                    + c9
                ),
                sp.symbols("p5_5"): slots["p5_h5"],
            }
        )
    )
    assert row10 == -sp.Rational(45, 16) * r0**3 * c10
    row9 = sp.factor(row9_before_c10.subs(c10, 0))
    assert row9 == -sp.Rational(135, 128) * r0**3 * c9
    return {
        "c10_row": row10,
        "c9_row_before_c10": row9_before_c10,
        "c9_row": row9,
    }


def lower_fractional_slots() -> dict[str, sp.Expr]:
    """Identify q7,q6,q5 with A12+c8*P after the D4 descent."""
    data = triangular_rows()
    recurrence = data["recurrence"]
    h = recurrence.h
    r = data["r"]
    w = data["w"]
    e = data["e"]
    s = sp.symbols("s0:4")
    r_poly = sum(r[index] * h**index for index in range(5))
    s_poly = sum(s[index] * h**index for index in range(4))
    w_poly = sum(w[index] * h**index for index in range(3))
    v_poly = sum(e[index + 4] * h**index for index in range(3))

    # The endpoint E14[h^17] and E10[h^1] have already proved
    # w3=e3=0.  The resulting canonical square root is polynomial.
    closed = {w[3]: 0, e[3]: 0}
    H = sp.expand(
        h**4 * y**4
        + r_poly * y**3 / 2
        + s_poly * y**2 / 2
        + w_poly * y / 2
        + v_poly / 2
    )
    P = sp.expand(
        sum(
            recurrence.p[grade].subs(closed) * y**grade
            for grade in range(9)
        )
    )
    remainder = sp.expand(P - H**2)
    assert sp.Poly(remainder, y).degree() <= 3

    # A12-H^3-(3/2)H(P-H^2) has y-degree at most two, so this expression
    # gives all slots used below without expanding the lower A12 terms.
    a12_high = sp.Poly(
        sp.expand(H**3 + sp.Rational(3, 2) * H * remainder),
        y,
    )

    def slot(y_degree: int, h_degree: int) -> sp.Expr:
        return sp.expand(
            a12_high.coeff_monomial(y**y_degree)
        ).coeff(h, h_degree)

    q8 = sp.symbols("q8_8")
    c8 = sp.expand(q8 - slot(8, 8))
    p7_h7 = sp.expand(recurrence.p[7]).coeff(h, 7)
    p6_h6 = sp.expand(recurrence.p[6]).coeff(h, 6)
    p5_h5 = sp.expand(recurrence.p[5].subs(closed)).coeff(h, 5)

    c7_residual = sp.factor(
        data["q7_value"].subs(closed) - slot(7, 7) - c8 * p7_h7
    )
    c6_residual = sp.factor(
        data["q6_value"].subs(closed) - slot(6, 6) - c8 * p6_h6
    )
    c5_residual = sp.factor(
        data["q5_value"].subs(closed) - slot(5, 5) - c8 * p5_h5
    )
    assert c7_residual == 0
    assert c6_residual == 0
    assert c5_residual == 0
    return {
        "c7_residual": c7_residual,
        "c6_residual": c6_residual,
        "c5_residual": c5_residual,
    }


def main() -> None:
    rows = exact_row_elimination()
    lower = lower_fractional_slots()
    print("closed h-adic chart: r0 != 0")
    print("c10 obstruction:", rows["c10_row"], "= 0")
    print("c9 obstruction:", rows["c9_row"], "= 0")
    print(
        "lower slot residuals:",
        lower["c7_residual"],
        lower["c6_residual"],
        lower["c5_residual"],
    )
    print("therefore c10=c9=c7=c6=c5=0 on the r0-unit chart")
    print("RESULT: EXACT r0 FRACTIONAL-RESONANCE ELIMINATION PASSES")


if __name__ == "__main__":
    main()
