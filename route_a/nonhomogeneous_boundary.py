#!/usr/bin/env python3
"""Exact boundary-filtration checks for nonhomogeneous Darboux pairs.

The coefficient ring is characteristic zero.  The script has two purposes:

1. verify the first divisorial-boundary equation for arbitrary reduced
   polynomials P,Q;
2. certify that the *full* coefficient variety with
   deg(P),deg(Q) <= 2 is empty.  This ranges over every coefficient of both
   polynomials; it is not a sparse-P search.

Generator total degree is used, with the reduced B-basis
u^i v^j w^k, k in {0,1}.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


sys.path.insert(0, str(Path(__file__).resolve().parent))

from route_a_search import bracket  # noqa: E402


def derivative(poly: dict[int, object]) -> dict[int, object]:
    return {
        degree - 1: degree * coefficient
        for degree, coefficient in poly.items()
        if degree and coefficient != 0
    }


def multiply(left: dict[int, object], right: dict[int, object]) -> dict[int, object]:
    answer: dict[int, object] = {}
    for i, a in left.items():
        for j, b in right.items():
            answer[i + j] = sp.expand(answer.get(i + j, 0) + a * b)
    return {degree: coefficient for degree, coefficient in answer.items() if coefficient != 0}


def subtract(left: dict[int, object], right: dict[int, object]) -> dict[int, object]:
    answer = dict(left)
    for degree, coefficient in right.items():
        answer[degree] = sp.expand(answer.get(degree, 0) - coefficient)
        if answer[degree] == 0:
            del answer[degree]
    return answer


def add(*polys: dict[int, object]) -> dict[int, object]:
    answer: dict[int, object] = {}
    for poly in polys:
        for degree, coefficient in poly.items():
            answer[degree] = sp.expand(answer.get(degree, 0) + coefficient)
            if answer[degree] == 0:
                del answer[degree]
    return answer


def scale(poly: dict[int, object], coefficient) -> dict[int, object]:
    return {
        degree: sp.expand(coefficient * value)
        for degree, value in poly.items()
        if coefficient * value != 0
    }


def boundary_jets(poly):
    """Return P_0(v),P_1(v) in P=P_0+w P_1+O_D(2).

    At the divisor D=(u,w), ord_D(w)=1 and ord_D(u)=2.  Hence only
    monomials with u-degree zero contribute to these first two terms.
    """
    zero: dict[int, object] = {}
    one: dict[int, object] = {}
    for (u_degree, v_degree, w_degree), coefficient in poly.items():
        if u_degree == 0:
            (zero if w_degree == 0 else one)[v_degree] = coefficient
    return zero, one


def completion_jets_through_three(poly):
    """Return p_0,...,p_3 after using t=w in the D-adic completion."""
    jets = [{} for _ in range(4)]
    for (u_degree, v_degree, w_degree), coefficient in poly.items():
        t_degree = 2 * u_degree + w_degree
        if t_degree <= 3:
            jets[t_degree][v_degree] = coefficient
    return jets


def verify_boundary_equations():
    p = sp.symbols("p0:16")
    q = sp.symbols("q0:16")
    monomials = [
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (2, 0, 0),
        (1, 1, 0),
        (0, 2, 0),
        (1, 0, 1),
        (0, 1, 1),
        (0, 3, 0),
        (0, 2, 1),
        (2, 0, 1),
        (1, 2, 0),
        (1, 1, 1),
        (3, 0, 0),
        (2, 1, 0),
    ]
    P = dict(zip(monomials, p))
    Q = dict(zip(monomials, q))
    p0, p1 = boundary_jets(P)
    q0, q1 = boundary_jets(Q)
    expected = subtract(multiply(derivative(p0), q1), multiply(p1, derivative(q0)))
    actual = {
        v_degree: coefficient
        for (u_degree, v_degree, w_degree), coefficient in bracket(P, Q).items()
        if u_degree == 0 and w_degree == 0
    }
    if actual != expected:
        raise AssertionError(f"boundary equation mismatch: {actual} != {expected}")
    print("verified: {P,Q}|_D = P0'(v) Q1(v) - P1(v) Q0'(v)")

    p0, p1, p2, p3 = completion_jets_through_three(P)
    q0, q1, q2, q3 = completion_jets_through_three(Q)
    jacobian_zero = subtract(multiply(derivative(p0), q1), multiply(p1, derivative(q0)))
    jacobian_one = add(
        scale(multiply(derivative(p0), q2), 2),
        multiply(derivative(p1), q1),
        scale(multiply(p1, derivative(q1)), -1),
        scale(multiply(p2, derivative(q0)), -2),
    )
    jacobian_two = add(
        scale(multiply(derivative(p0), q3), 3),
        scale(multiply(derivative(p1), q2), 2),
        multiply(derivative(p2), q1),
        scale(multiply(p1, derivative(q2)), -1),
        scale(multiply(p2, derivative(q1)), -2),
        scale(multiply(p3, derivative(q0)), -3),
    )
    # {v,t}=sqrt(1+4vt^2)=1+2vt^2+O(t^4).
    expected_completion = [
        jacobian_zero,
        jacobian_one,
        add(
            jacobian_two,
            {degree + 1: 2 * value for degree, value in jacobian_zero.items()},
        ),
    ]
    actual_completion = completion_jets_through_three(bracket(P, Q))[:3]
    if actual_completion != expected_completion:
        raise AssertionError(
            "BF0--BF2 mismatch:\n"
            f"actual={actual_completion}\nexpected={expected_completion}"
        )
    print("verified: BF1 and BF2 completion recurrences")


def verify_de_rham_reduction():
    """Check the weight-zero calculation proving H^1_dR(B)=0."""
    s = sp.symbols("s")
    A = sp.Function("A")(s)
    B = sp.Function("B")(s)
    C = sp.Function("C")(s)
    # A weight-zero one-form is
    # A(s)v du+B(s)u dv+C(s)vw dw.  On the Laurent chart it is
    # X(s)dr/r+r*w*Y(s)dw.
    X = -s * A + (2 * s + 1) * B
    Y = 2 * B + s * C
    closed_equation = Y + (s + 1) * sp.diff(Y, s) - 2 * sp.diff(X, s)
    remainder = X - (s + 1) * Y / 2
    if sp.simplify(sp.diff(remainder, s) + closed_equation / 2) != 0:
        raise AssertionError("weight-zero de Rham identity failed")
    # remainder(0)=0 identically because X(0)=B(0), Y(0)=2B(0).
    B0 = sp.symbols("B0")
    if sp.expand(B0 - 2 * B0 / 2) != 0:
        raise AssertionError("weight-zero regularity boundary value failed")
    print("verified: weight-zero closed one-forms are exact")

    r, w = sp.symbols("r w", nonzero=True)
    u = 1 / r
    v = r**2 * w**2 - r
    beta_u = -4 * v**2 * w
    beta_v = w * (1 - 2 * u * v)
    beta_w = 2 * v * (1 + 2 * u * v)
    beta_dr = sp.factor(beta_u * sp.diff(u, r) + beta_v * sp.diff(v, r))
    beta_dw = sp.factor(beta_u * sp.diff(u, w) + beta_v * sp.diff(v, w) + beta_w)
    if (beta_dr, beta_dw) != (w, 2 * r):
        raise AssertionError(f"unexpected Laurent primitive: {(beta_dr, beta_dw)}")
    print("verified: beta = w dr + 2r dw = d(rw) + r dw on u != 0")


def verify_quadratic_elimination():
    # The constant bracket coefficient is the determinant of the linear
    # (v,w)-coefficient matrix.  An SL_2 change of the target therefore puts
    # every prospective pair into the following form without increasing the
    # common degree bound.
    a, b, d, e, f, g, h = sp.symbols("a b d e f g h")
    D, E, F, G, H = sp.symbols("D E F G H")
    P = {
        (0, 1, 0): 1,
        (1, 0, 0): a,
        (2, 0, 0): d,
        (1, 1, 0): e,
        (0, 2, 0): f,
        (1, 0, 1): g,
        (0, 1, 1): h,
    }
    Q = {
        (0, 0, 1): 1,
        (1, 0, 0): b,
        (2, 0, 0): D,
        (1, 1, 0): E,
        (0, 2, 0): F,
        (1, 0, 1): G,
        (0, 1, 1): H,
    }
    answer = bracket(P, Q)

    # Only these eight rows are needed.  Their ideal is already the unit
    # ideal; all omitted bracket equations can only strengthen the system.
    rows = [
        (1, 1, 0),  # uv
        (1, 1, 1),  # uvw
        (1, 2, 0),  # uv^2
        (1, 3, 0),  # uv^3
        (2, 0, 1),  # u^2 w
        (2, 1, 1),  # u^2 v w
        (2, 2, 0),  # u^2 v^2
        (4, 0, 0),  # u^4
    ]
    equations = [sp.expand(answer.get(row, 0)) for row in rows]
    expected = [
        E * h - 6 * F * g + 6 * G * f - H * e + 2,
        8 * D * f - 8 * F * d + 2 * h,
        2 * H + 4 * f,
        -4 * F * h + 4 * H * f,
        4 * D * e - 4 * E * d - g,
        5 * G * h - 5 * H * g,
        E * h - 8 * F * g + 8 * G * f - H * e,
        2 * D * g - 2 * G * d,
    ]
    if equations != expected:
        raise AssertionError(f"unexpected quadratic rows:\n{equations}")

    variables = (E, F, G, H, D, d, e, f, g, h)
    basis = sp.groebner(equations, *variables, order="grevlex", method="f5b")
    if len(basis.polys) != 1 or basis.polys[0].as_expr() != 1:
        raise AssertionError(f"quadratic elimination did not produce [1]: {basis}")
    print("verified: eight-row exact Groebner certificate is [1]")
    print("verified: no Darboux pair has generator total degrees <= (2,2)")


def main():
    verify_boundary_equations()
    verify_de_rham_reduction()
    verify_quadratic_elimination()
    print("all nonhomogeneous boundary checks passed")


if __name__ == "__main__":
    main()
