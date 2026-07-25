#!/usr/bin/env python3
"""Explore normalized negative-tail Euler cokernels for r-order 3 and 4."""

from __future__ import annotations

import sympy as sp


def bracket(i, p, q_grade, q, h):
    return sp.expand(
        q_grade * sp.diff(p, h) * q
        - i * p * sp.diff(q, h)
    )


def solve_euler(order, forcing, h):
    resonance_output = 7 - order
    obstruction = sp.factor(sp.expand(forcing).coeff(h, resonance_output))
    solution = 0
    for term in sp.Add.make_args(sp.expand(forcing)):
        coefficient, output_exponent = term.as_coeff_exponent(h)
        input_exponent = output_exponent - 7
        multiplier = -8 * (order + input_exponent)
        if multiplier == 0:
            continue
        solution += -coefficient * h**input_exponent / multiplier
    return sp.expand(solution), obstruction


def chart(order: int):
    h, t = sp.symbols("h t", nonzero=True)
    r3, r4 = sp.symbols("r3 r4")
    s = sp.symbols("s0:4")
    w = sp.symbols("w0:3")
    u = sp.symbols("u0:3")
    a = sp.symbols("a0:6")
    b = sp.symbols("b0:5")
    c = sp.symbols("c0:4")
    d = sp.symbols("d0:3")
    if order == 3:
        r = r3 * h**3 + r4 * h**4
    else:
        r = r4 * h**4
    s_poly = sum(s[index] * h**index for index in range(4))
    w_poly = sum(w[index] * h**index for index in range(3))
    u_poly = sum(u[index] * h**index for index in range(3))
    p = {
        8: h**8,
        7: h**4 * r,
        6: sp.expand(r**2 / 4 + h**4 * s_poly),
        5: sp.expand(r * s_poly / 2 + h**4 * w_poly),
        4: sp.expand(s_poly**2 / 4 + r * w_poly / 2 + h**4 * u_poly),
        3: sum(a[index] * h**index for index in range(6)),
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
    results = []
    for m in range(11, 20):
        forcing = 0
        total_grade = 8 - m
        for i in range(-1, 8):
            prior_order = i - total_grade
            if prior_order in n:
                forcing += bracket(
                    i, p[i], -prior_order, n[prior_order], h
                )
        n[m], obstruction = solve_euler(m, forcing, h)
        results.append((m, obstruction, n[m]))
    return results


def main() -> None:
    for order in (3, 4):
        print("ORDER", order)
        for m, obstruction, solution in chart(order):
            print("m", m, "obstruction", obstruction)
            print("n terms", len(sp.Add.make_args(solution)))


if __name__ == "__main__":
    main()
