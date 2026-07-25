#!/usr/bin/env python3
"""Exact formal-tail and weighted-face obstructions for case c.

This is the lightweight verifier for the global approximate-root tail.
It checks:

* the arbitrary Euler resonance and forced target coefficient;
* the r0 next-cokernel obstruction;
* the r1 hyperelliptic de Rham obstruction;
* the full r2 square-face residue; and
* the first common transverse condition on the still-open r3/r4 charts.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_lower_remainder_identity import (
    verify_negative_tail_obstruction,
    verify_r1_hyperelliptic_obstruction,
    verify_terminal_euler_lemma,
    verify_weighted_residue_obstruction,
)


def bracket(
    p_grade: int,
    p: sp.Expr,
    q_grade: int,
    q: sp.Expr,
    h: sp.Symbol,
) -> sp.Expr:
    return sp.expand(
        q_grade * sp.diff(p, h) * q
        - p_grade * p * sp.diff(q, h)
    )


def solve_euler(
    order: int,
    forcing: sp.Expr,
    h: sp.Symbol,
) -> tuple[sp.Expr, sp.Expr]:
    """Solve L_order(n)+forcing=0 off the unique Euler cokernel."""
    resonance_output = 7 - order
    obstruction = sp.factor(
        sp.expand(forcing).coeff(h, resonance_output)
    )
    solution = 0
    for term in sp.Add.make_args(sp.expand(forcing)):
        coefficient, output_exponent = term.as_coeff_exponent(h)
        input_exponent = output_exponent - 7
        multiplier = -8 * (order + input_exponent)
        if multiplier == 0:
            continue
        solution += -coefficient * h**input_exponent / multiplier
    return sp.expand(solution), obstruction


def verify_r3_r4_first_transverse_condition(
    order: int,
) -> dict[str, sp.Expr]:
    """Normalize through m=14 on ord_h(r)=3 or 4."""
    if order not in (3, 4):
        raise ValueError("order must be 3 or 4")

    h, t = sp.symbols("h t", nonzero=True)
    r3, r4 = sp.symbols("r3 r4")
    s = sp.symbols("s0:4")
    w = sp.symbols("w0:3")
    u = sp.symbols("u0:3")
    r = r3 * h**3 + r4 * h**4 if order == 3 else r4 * h**4
    s_poly = sum(s[index] * h**index for index in range(4))
    w_poly = sum(w[index] * h**index for index in range(3))
    u_poly = sum(u[index] * h**index for index in range(3))
    p = {
        8: h**8,
        7: h**4 * r,
        6: sp.expand(r**2 / 4 + h**4 * s_poly),
        5: sp.expand(r * s_poly / 2 + h**4 * w_poly),
        4: sp.expand(
            s_poly**2 / 4 + r * w_poly / 2 + h**4 * u_poly
        ),
    }
    n = {
        10: (
            -sp.Rational(1, 40) * h**-5
            - t * h**-6 / 16
            - t**2 * h**-7 / 24
        )
    }
    obstructions: dict[int, sp.Expr] = {}
    for current_order in range(11, 15):
        total_grade = 8 - current_order
        forcing = 0
        for p_grade in range(4, 8):
            prior_order = p_grade - total_grade
            if prior_order in n:
                forcing += bracket(
                    p_grade,
                    p[p_grade],
                    -prior_order,
                    n[prior_order],
                    h,
                )
        n[current_order], obstructions[current_order] = solve_euler(
            current_order, forcing, h
        )

    assert all(obstructions[index] == 0 for index in (11, 12, 13))
    expected = -sp.Rational(3, 16) * s[0] * t * (
        s[0] + s[1] * t
    )
    assert sp.expand(obstructions[14] - expected) == 0
    return {
        "m11": obstructions[11],
        "m12": obstructions[12],
        "m13": obstructions[13],
        "m14": obstructions[14],
    }


def verify_r3_r4_deep_transverse_condition(
    order: int,
) -> dict[str, sp.Expr]:
    """Continue the s0=s1=0 branch until the fixed base enters."""
    if order not in (3, 4):
        raise ValueError("order must be 3 or 4")

    h, t = sp.symbols("h t", nonzero=True)
    r3, r4 = sp.symbols("r3 r4")
    s2, s3 = sp.symbols("s2 s3")
    w0, w1, w2 = sp.symbols("w0 w1 w2")
    u = sp.symbols("u0:3")
    a = sp.symbols("a1:6")
    b = sp.symbols("b0:5")
    c = sp.symbols("c0:4")
    d = sp.symbols("d0:3")
    r = r3 * h**3 + r4 * h**4 if order == 3 else r4 * h**4
    s_poly = s2 * h**2 + s3 * h**3
    w_poly = w0 + w1 * h + w2 * h**2
    u_poly = sum(u[index] * h**index for index in range(3))
    p = {
        8: h**8,
        7: h**4 * r,
        6: sp.expand(r**2 / 4 + h**4 * s_poly),
        5: sp.expand(r * s_poly / 2 + h**4 * w_poly),
        4: sp.expand(
            s_poly**2 / 4 + r * w_poly / 2 + h**4 * u_poly
        ),
        # m=15 already gives [h^0]p3=0 on s0=0.
        3: sum(a[index - 1] * h**index for index in range(1, 6)),
        2: sum(b[index] * h**index for index in range(5)),
        1: sum(c[index] * h**index for index in range(4)),
        0: sum(d[index] * h**index for index in range(3)),
        -1: h + t,
    }
    n = {
        10: (
            -sp.Rational(1, 40) * h**-5
            - t * h**-6 / 16
            - t**2 * h**-7 / 24
        )
    }
    obstructions: dict[int, sp.Expr] = {}
    for current_order in range(11, 20):
        total_grade = 8 - current_order
        forcing = 0
        for p_grade in range(-1, 8):
            prior_order = p_grade - total_grade
            if prior_order in n:
                forcing += bracket(
                    p_grade,
                    p[p_grade],
                    -prior_order,
                    n[prior_order],
                    h,
                )
        n[current_order], obstructions[current_order] = solve_euler(
            current_order, forcing, h
        )

    assert all(
        obstructions[index] == 0
        for index in (11, 12, 13, 14, 15, 16, 17)
    )
    expected18 = -sp.Rational(5, 16) * a[0] * t**2 * w0
    assert sp.expand(obstructions[18] - expected18) == 0
    r3_term = 46 * a[0] * r3 if order == 3 else 0
    expected19 = (
        sp.Rational(11, 1024)
        * t**2
        * w0
        * (r3_term - 48 * b[0] + 5 * w0**2)
    )
    assert sp.expand(obstructions[19] - expected19) == 0
    return {
        "m18": obstructions[18],
        "m19": obstructions[19],
    }


def main() -> None:
    terminal = verify_terminal_euler_lemma()
    r0 = verify_negative_tail_obstruction()
    weighted = verify_weighted_residue_obstruction()
    r1 = verify_r1_hyperelliptic_obstruction()
    r3 = verify_r3_r4_first_transverse_condition(3)
    r4 = verify_r3_r4_first_transverse_condition(4)
    r3_deep = verify_r3_r4_deep_transverse_condition(3)
    r4_deep = verify_r3_r4_deep_transverse_condition(4)
    print("target coefficient:", terminal["target_particular"])
    print("r0 cokernel:", r0["cokernel_obstruction"])
    print("r1 Hermite remainder:", r1["hermite_remainder"])
    print("r2 square-face cokernel:", weighted["r2_obstruction"])
    print("r3 first transverse condition:", r3["m14"])
    print("r4 first transverse condition:", r4["m14"])
    print("r3 deep transverse condition:", r3_deep["m19"])
    print("r4 deep transverse condition:", r4_deep["m19"])
    print("RESULT: EXACT CASE-C FORMAL-TAIL OBSTRUCTIONS PASS")


if __name__ == "__main__":
    main()
