#!/usr/bin/env python3
"""Exact checks for the delta=2 multisection obstruction."""

from __future__ import annotations

import sympy as sp


def verify_graph_jet_identities() -> None:
    z = sp.symbols("z")
    p0, p1, p2 = sp.symbols("p0 p1 p2")
    g0, g1, g2, g3, g4 = sp.symbols("g0 g1 g2 g3 g4")
    delta = p1 * z + p2 * z**2
    graph = (
        g0
        + g1 * delta
        + g2 * delta**2 / 2
        + g3 * delta**3 / 6
        + g4 * delta**4 / 24
    )
    assert sp.expand(graph).coeff(z, 1) == g1 * p1
    assert sp.expand(graph).coeff(z, 2) == g1 * p2 + g2 * p1**2 / 2
    assert sp.expand(graph).coeff(z, 3) == (
        g2 * p1 * p2 + g3 * p1**3 / 6
    )
    assert sp.expand(graph).coeff(z, 4) == (
        g2 * p2**2 / 2
        + g3 * p1**2 * p2 / 2
        + g4 * p1**4 / 24
    )

    # In the inverse graph P=f(Q), q1 and q2 are polynomial.  If f'=0
    # at w=0, the coefficient f'*q2+f''*q1^2/2 cannot have a pole.
    f1, f2, q1, q2 = sp.symbols("f1 f2 q1 q2")
    inverse_second = f1 * q2 + f2 * q1**2 / 2
    assert inverse_second.subs(f1, 0) == f2 * q1**2 / 2


def verify_davenport_normal_form() -> None:
    h, a, b, v = sp.symbols("h a b v", nonzero=True)
    A = h**4 + b * h**2 + a * h + b**2 / 4
    B = (
        h**6
        + sp.Rational(3, 2) * b * h**4
        + sp.Rational(3, 2) * a * h**3
        + sp.Rational(3, 4) * b**2 * h**2
        + sp.Rational(3, 4) * a * b * h
        + (b**3 + 3 * a**2) / 8
    )
    u = -sp.Rational(3, 8) * a**2 * b
    restriction = sp.factor(B**2 - A**3 + u * A + v)
    expected = (
        a**3 * h**3 / 8
        + 3 * a**3 * b * h / 16
        + 9 * a**4 / 64
        + v
    )
    assert sp.expand(restriction - expected) == 0
    assert sp.degree(restriction, h) == 3

    resultant = sp.factor(
        sp.resultant(sp.diff(A, h), sp.diff(B, h), h)
    )
    assert resultant == -1728 * a**5


def verify_triangular_cancellation() -> None:
    h = sp.symbols("h")
    a2, a1, a0 = sp.symbols("a2 a1 a0")
    b = sp.symbols("b0:6")
    A = h**4 + a2 * h**2 + a1 * h + a0
    B = h**6 + sum(b[index] * h**index for index in range(6))

    solved = {
        b[5]: 0,
        b[4]: 3 * a2 / 2,
        b[3]: 3 * a1 / 2,
        b[2]: 3 * a0 / 2 + 3 * a2**2 / 8,
        b[1]: 3 * a1 * a2 / 4,
        b[0]: 3 * a0 * a2 / 4 + 3 * a1**2 / 8 - a2**3 / 16,
    }
    difference = sp.expand((B**2 - A**3).subs(solved))
    assert all(difference.coeff(h, degree) == 0 for degree in range(6, 13))
    assert sp.factor(difference.coeff(h, 5)) == (
        -3 * a1 * (4 * a0 - a2**2) / 8
    )

    primitive_substitution = {a0: a2**2 / 4}
    degree_four = sp.factor(
        difference.subs(primitive_substitution).coeff(h, 4)
    )
    assert degree_four == 3 * a1**2 * a2 / 8
    u = -degree_four
    completed = sp.expand(
        difference.subs(primitive_substitution)
        + u * A.subs(primitive_substitution)
    )
    assert completed.coeff(h, 3) == a1**3 / 8
    assert completed.coeff(h, 2) == 0


def verify_curve_level_countermodel() -> None:
    h, w = sp.symbols("h w")
    A = h**4 + h
    B = h**6 + sp.Rational(3, 2) * h**3 + sp.Rational(3, 8)
    assert sp.expand(
        B**2 - A**3 - h**3 / 8 - sp.Rational(9, 64)
    ) == 0

    p = sp.expand(A.subs(h, w**2))
    q = sp.expand(B.subs(h, w**2))
    assert sp.degree(p, w) == 8
    assert sp.degree(q, w) == 12
    # h^3 is in C(A,B), and A=h(h^3+1), so the normalization parameter
    # is recovered rationally.
    recovered_h = sp.cancel(A / (8 * (B**2 - A**3) - sp.Rational(1, 8)))
    assert sp.simplify(recovered_h - h) == 0


def main() -> None:
    verify_graph_jet_identities()
    verify_davenport_normal_form()
    verify_triangular_cancellation()
    verify_curve_level_countermodel()
    print("verified the fixed-pole graph-jet identities")
    print("verified the complete generalized Davenport normal form")
    print("verified resultant -1728*a^5 and global immersion")
    print("verified an exact primitive curve-level degree-three model")
    print("RESULT: DELTA=2 MULTISECTION OBSTRUCTION PASSES")


if __name__ == "__main__":
    main()
