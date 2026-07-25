#!/usr/bin/env python3
"""Deep normalized-tail probes on the s0=s1=0 branches."""

from __future__ import annotations

import sympy as sp

from scratch_negative_tail_j34 import bracket, solve_euler


def run(order: int, w0_unit: bool):
    h, t = sp.symbols("h t", nonzero=True)
    r3, r4 = sp.symbols("r3 r4")
    s2, s3 = sp.symbols("s2 s3")
    w0, w1, w2 = sp.symbols("w0 w1 w2")
    u = sp.symbols("u0:3")
    a = sp.symbols("a0:6")
    b = sp.symbols("b0:5")
    c = sp.symbols("c0:4")
    d = sp.symbols("d0:3")
    r = r3 * h**3 + r4 * h**4 if order == 3 else r4 * h**4
    s = s2 * h**2 + s3 * h**3
    w = w0 + w1 * h + w2 * h**2
    p3 = sum(a[index] * h**index for index in range(6))
    p2 = sum(b[index] * h**index for index in range(5))
    substitutions = {a[0]: 0}
    if w0_unit:
        substitutions.update(
            {
                a[1]: 0,
                b[0]: sp.Rational(5, 48) * w0**2,
            }
        )
    else:
        substitutions[w0] = 0
    p = {
        8: h**8,
        7: h**4 * r,
        6: sp.expand(r**2 / 4 + h**4 * s),
        5: sp.expand(r * s / 2 + h**4 * w),
        4: sp.expand(
            s**2 / 4
            + r * w / 2
            + h**4 * sum(u[index] * h**index for index in range(3))
        ),
        3: p3,
        2: p2,
        1: sum(c[index] * h**index for index in range(4)),
        0: sum(d[index] * h**index for index in range(3)),
        -1: h + t,
    }
    p = {grade: value.subs(substitutions) for grade, value in p.items()}
    n = {
        10: (
            -sp.Rational(1, 40) * h**-5
            - t * h**-6 / 16
            - t**2 * h**-7 / 24
        )
    }
    output = []
    for m in range(11, 23):
        forcing = 0
        total_grade = 8 - m
        for i in range(-1, 8):
            prior_order = i - total_grade
            if prior_order in n:
                forcing += bracket(
                    i, p[i], -prior_order, n[prior_order], h
                )
        n[m], obstruction = solve_euler(m, forcing, h)
        output.append((m, sp.factor(obstruction)))
    return output


def main() -> None:
    for order in (3, 4):
        for unit in (False, True):
            print("CHART", order, "W0UNIT", unit, flush=True)
            for m, obstruction in run(order, unit):
                if m >= 18:
                    print(
                        m,
                        "terms",
                        len(sp.Add.make_args(sp.expand(obstruction))),
                        "factor",
                        obstruction,
                        flush=True,
                    )


if __name__ == "__main__":
    main()
