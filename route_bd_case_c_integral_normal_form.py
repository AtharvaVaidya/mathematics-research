#!/usr/bin/env python3
"""Exact integral normal form and reduced equation system for case c.

After universal fractional descent,

    P_+ = H^2 + R,
    Q_+ = H^3 + (3/2) H R + c8 P_+ + c4 H + S,
    deg_y(R), deg_y(S) <= 3.

This verifier checks the invariant bracket identity, removes c4 by a
slice-preserving target translation, records the support cost of removing
c8, and derives the resulting thirteen coefficient ODEs.  It also gives
the complete degree-capped solution of the bottom two ODEs, proving that
those rows alone cannot be the remaining obstruction.
"""

from __future__ import annotations

import sympy as sp

from route_bd_verify import (
    C_P_VERTICES,
    C_Q_VERTICES,
    lattice_points,
)


z, y = sp.symbols("z y")


def graded_bracket(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    """The case-c bracket after z=xy: y times the (z,y)-Jacobian."""
    return sp.expand(
        y
        * (
            sp.diff(left, z) * sp.diff(right, y)
            - sp.diff(left, y) * sp.diff(right, z)
        )
    )


def generic_polynomial(prefix: str, degree: int) -> sp.Expr:
    return sum(
        sp.Function(f"{prefix}{index}")(z) * y**index
        for index in range(degree + 1)
    )


def verify_integral_bracket_identity() -> dict[str, sp.Expr]:
    H = generic_polynomial("H", 4)
    R = generic_polynomial("R", 3)
    S = generic_polynomial("S", 3)
    c8, c4 = sp.symbols("c8 c4", constant=True)
    P = sp.expand(H**2 + R)
    Q = sp.expand(
        H**3
        + sp.Rational(3, 2) * H * R
        + c8 * P
        + c4 * H
        + S
    )
    reduced = sp.expand(
        graded_bracket(P, S)
        - (sp.Rational(3, 2) * R + c4)
        * graded_bracket(H, R)
    )
    assert sp.expand(graded_bracket(P, Q) - reduced) == 0
    return {
        "P": P,
        "Q": Q,
        "H": H,
        "R": R,
        "S": S,
        "reduced_bracket": reduced,
    }


def verify_integral_gauges() -> dict[str, sp.Expr]:
    H, R, S, P = sp.symbols("H R S P")
    c8, c4 = sp.symbols("c8 c4")
    lam = sp.Rational(2, 3) * c4
    original = H**3 + sp.Rational(3, 2) * H * R + c8 * P + c4 * H + S
    translated = (
        H**3
        + sp.Rational(3, 2) * H * (R + lam)
        + c8 * (P + lam)
        + (S - c8 * lam)
    )
    assert sp.expand(original - translated) == 0

    # P -> P+lambda changes only the already-allowed constant monomial.
    # By contrast, Q -> Q-c8*P introduces P's (1,0) monomial, which is
    # the unique P-support point absent from the normalized Q support.
    p_support = set(lattice_points(C_P_VERTICES))
    q_support = set(lattice_points(C_Q_VERTICES))
    support_difference = p_support - q_support
    assert support_difference == {(1, 0)}

    # After the external target shear, the fixed negative blocks become
    # z*y^-1 and z*(z-c8)*y^-1.  Their bracket remains exactly the target.
    negative_p = z / y
    negative_q = z * (z - c8) / y
    negative_bracket = sp.factor(graded_bracket(negative_p, negative_q))
    assert negative_bracket == z**2 / y**2
    return {
        "translation": lam,
        "translated_normal_form": translated,
        "support_difference": support_difference,
        "sheared_negative_q": negative_q,
        "negative_bracket": negative_bracket,
    }


def verify_thirteen_reduced_equations() -> dict[int, sp.Expr]:
    H = generic_polynomial("H", 4)
    R = generic_polynomial("R", 3)
    S = generic_polynomial("S", 3)
    c8 = sp.symbols("c8", constant=True)
    P_plus = sp.expand(H**2 + R)
    Q_plus = sp.expand(H**3 + sp.Rational(3, 2) * H * R + S)
    base_p = z / y
    base_q = z * (z - c8) / y
    P = sp.expand(base_p + P_plus)
    Q = sp.expand(base_q + Q_plus)

    internal = sp.expand(
        graded_bracket(P_plus, S)
        - sp.Rational(3, 2) * R * graded_bracket(H, R)
    )
    full_residual = sp.expand(
        graded_bracket(P, Q) - z**2 / y**2
    )

    equations: dict[int, sp.Expr] = {}
    for grade in range(-1, 12):
        p = sp.expand(P_plus).coeff(y, grade + 1)
        q = sp.expand(Q_plus).coeff(y, grade + 1)
        inside = internal.coeff(y, grade) if grade >= 0 else 0
        expected = sp.expand(
            z * sp.diff(q, z)
            + (grade + 1) * q
            - z * (z - c8) * sp.diff(p, z)
            - (grade + 1) * (2 * z - c8) * p
            + inside
        )
        actual = sp.expand(full_residual.coeff(y, grade))
        assert sp.expand(actual - expected) == 0
        equations[grade] = expected

    # There are no other rows after the fixed grade -2 target is removed.
    reconstructed = sum(
        equations[grade] * y**grade for grade in equations
    )
    assert sp.expand(full_residual - reconstructed) == 0
    return equations


def verify_bottom_rows_are_integrable() -> dict[str, sp.Expr]:
    c8 = sp.symbols("c8")
    a0, a1, a2, b0, b1, b2, b3, constant = sp.symbols(
        "a0 a1 a2 b0 b1 b2 b3 constant"
    )
    p0 = a0 + a1 * z + a2 * z**2
    q0 = (
        constant
        - a1 * c8 * z
        + (sp.Rational(1, 2) * a1 - a2 * c8) * z**2
        + sp.Rational(2, 3) * a2 * z**3
    )
    bottom_minus_one = sp.expand(
        z * sp.diff(q0, z)
        - z * (z - c8) * sp.diff(p0, z)
    )
    assert bottom_minus_one == 0

    p1 = b0 + b1 * z + b2 * z**2 + b3 * z**3
    q1 = sp.expand((z - c8) * p1)
    bottom_zero = sp.expand(
        z * sp.diff(q1, z)
        + q1
        - z * (z - c8) * sp.diff(p1, z)
        - (2 * z - c8) * p1
    )
    assert bottom_zero == 0
    assert sp.degree(p0, z) <= 2
    assert sp.degree(q0, z) <= 3
    assert sp.degree(p1, z) <= 3
    assert sp.degree(q1, z) <= 4
    return {
        "p0": p0,
        "q0": q0,
        "p1": p1,
        "q1": q1,
        "bottom_minus_one": bottom_minus_one,
        "bottom_zero": bottom_zero,
    }


def verify_first_internal_row_is_integrable() -> dict[str, sp.Expr]:
    """Show that the apparent first nonlinear row vanishes structurally.

    The coefficient of y in the positive-positive bracket is

        J_1 = p_0' q_1 - p_1 q_0'.

    The two bottom equations give q_0'=(z-c8)p_0' and
    q_1=(z-c8)p_1, so J_1=0.  The resulting grade-one equation is
    again an invertible Euler equation, with no degree-cap obstruction.
    """
    c8 = sp.symbols("c8")
    a0, a1, a2 = sp.symbols("a0 a1 a2")
    b0, b1, b2, b3, b4 = sp.symbols("b0 b1 b2 b3 b4")
    p0 = a0 + a1 * z + a2 * z**2
    p1 = sp.Function("p1")(z)
    q0_prime = (z - c8) * sp.diff(p0, z)
    q1 = (z - c8) * p1
    internal_one = sp.expand(
        sp.diff(p0, z) * q1 - p1 * q0_prime
    )
    assert internal_one == 0

    p2 = b0 + b1 * z + b2 * z**2 + b3 * z**3 + b4 * z**4
    q2 = sp.expand(
        sum(
            coefficient
            * (
                sp.Rational(index + 4, index + 3) * z ** (index + 1)
                - c8 * z**index
            )
            for index, coefficient in enumerate((b0, b1, b2, b3, b4))
        )
    )
    grade_one = sp.expand(
        z * sp.diff(q2, z)
        + 2 * q2
        - z * (z - c8) * sp.diff(p2, z)
        - 2 * (2 * z - c8) * p2
        + internal_one
    )
    assert grade_one == 0
    assert sp.degree(q2, z) <= 5
    return {
        "internal_one": internal_one,
        "p2": p2,
        "q2": q2,
        "grade_one": grade_one,
    }


def main() -> None:
    identity = verify_integral_bracket_identity()
    gauges = verify_integral_gauges()
    equations = verify_thirteen_reduced_equations()
    bottom = verify_bottom_rows_are_integrable()
    first_internal = verify_first_internal_row_is_integrable()
    assert identity["reduced_bracket"] is not None
    print("[P_+,Q_+]=[P_+,S]-(3R/2+c4)[H,R]: verified")
    print("slice-preserving translation kills c4:", gauges["translation"])
    print("c8 shear support cost:", gauges["support_difference"])
    print("reduced equation grades:", min(equations), "...", max(equations))
    print("bottom q0:", bottom["q0"])
    print("bottom q1:", bottom["q1"])
    print("first internal bracket row:", first_internal["internal_one"])
    print("grades -1,0,1 are exactly integrable within their degree caps")
    print("RESULT: EXACT CASE-C INTEGRAL NORMAL FORM PASSES")


if __name__ == "__main__":
    main()
