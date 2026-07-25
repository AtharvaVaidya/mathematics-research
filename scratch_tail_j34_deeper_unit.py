#!/usr/bin/env python3
"""Continue the normalized tail on the ``w0 != 0`` deepest charts.

The substitutions imposed here are precisely the cokernel equations through
order 22 from ``scratch_tail_j34_deep.py``.  Keeping them in the input avoids
carrying already-vanishing factors through the later recurrence.
"""

from __future__ import annotations

import argparse

import sympy as sp

from scratch_negative_tail_j34 import bracket, solve_euler


def run(order: int, maximum: int) -> None:
    h, t = sp.symbols("h t", nonzero=True)
    r3, r4 = sp.symbols("r3 r4")
    s2, s3 = sp.symbols("s2 s3")
    w0, w1, w2 = sp.symbols("w0 w1 w2", nonzero=True)
    u = sp.symbols("u0:3")
    a = sp.symbols("a0:7")
    b = sp.symbols("b0:6")
    c = sp.symbols("c0:5")
    d = sp.symbols("d0:4")

    if order == 3:
        r = r3 * h**3 + r4 * h**4
        a2_value = sp.Rational(3, 256) * w0 * (48 * s2 - r3**2)
        b1_value = (
            w0 * (63 * r3**3 - 528 * r3 * s2 + 3840 * w1) / 3072
            + sp.Rational(25, 48) * w0**2 / t
        )
    else:
        r = r4 * h**4
        a2_value = sp.Rational(9, 16) * s2 * w0
        b1_value = (
            sp.Rational(5, 4) * w0 * w1
            + sp.Rational(25, 48) * w0**2 / t
        )

    s = s2 * h**2 + s3 * h**3
    w = w0 + w1 * h + w2 * h**2
    substitutions = {
        a[0]: 0,
        a[1]: 0,
        a[2]: a2_value,
        b[0]: sp.Rational(5, 48) * w0**2,
        b[1]: b1_value,
    }
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
        3: sum(a[index] * h**index for index in range(7)),
        2: sum(b[index] * h**index for index in range(6)),
        1: sum(c[index] * h**index for index in range(5)),
        0: sum(d[index] * h**index for index in range(4)),
        -1: h + t,
    }
    p = {
        grade: sp.expand(value.subs(substitutions))
        for grade, value in p.items()
    }
    n = {
        10: (
            -sp.Rational(1, 40) * h**-5
            - t * h**-6 / 16
            - t**2 * h**-7 / 24
        )
    }
    for m in range(11, maximum + 1):
        forcing = 0
        total_grade = 8 - m
        for i in range(-1, 8):
            prior_order = i - total_grade
            if prior_order in n:
                forcing += bracket(
                    i, p[i], -prior_order, n[prior_order], h
                )
        n[m], obstruction = solve_euler(m, forcing, h)
        if m >= 21:
            obstruction = sp.factor(obstruction)
            print(
                m,
                "terms",
                len(sp.Add.make_args(sp.expand(obstruction))),
                "factor",
                obstruction,
                flush=True,
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("order", type=int, choices=(3, 4))
    parser.add_argument("--maximum", type=int, default=25)
    arguments = parser.parse_args()
    run(arguments.order, arguments.maximum)


if __name__ == "__main__":
    main()
