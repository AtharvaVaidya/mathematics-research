#!/usr/bin/env python3
"""Exact first-cokernel reduction for the case-c integral normal form.

After the c4 translation and the external c8 shear, put

    P = z/y + sum(p_m(z) y^m),
    Q = z(z-c8)/y + sum(q_m(z) y^m).

The grade n=m-1 equation has Euler part

    L_m(q_m) = z*q_m' + m*q_m.

This verifier proves three structural facts.

1.  The first genuinely nonzero internal row is n=2, but it merely
    determines q3 (and hence the last remainder coefficient S3).
2.  Newton degree caps create no Euler cokernel through n=8.  The first
    cokernel is one-dimensional at n=9, represented by [z^13].
3.  The resulting residue is the h^13 coefficient of the already-known
    outer-face Bezout equation.  It is a genuine scalar condition, not
    an identity and not a forced nonzero.  The c8 support-cost monomial
    has zero class in this and every Euler cokernel.
"""

from __future__ import annotations

import sympy as sp


z, h = sp.symbols("z h")


def euler(expression: sp.Expr, degree: int) -> sp.Expr:
    return sp.expand(z * sp.diff(expression, z) + degree * expression)


def verify_first_nonlinear_row() -> dict[str, sp.Expr]:
    """Derive I2 after the bottom three triangular solutions."""
    c8 = sp.symbols("c8")
    a = sp.symbols("a0:3")
    b = sp.symbols("b0:4")
    d = sp.symbols("d0:5")
    p0 = sum(a[index] * z**index for index in range(3))
    p1 = sum(b[index] * z**index for index in range(4))
    p2 = sum(d[index] * z**index for index in range(5))
    q0_prime = (z - c8) * sp.diff(p0, z)
    q1 = (z - c8) * p1
    q2 = sp.expand(
        sum(
            d[index]
            * (
                sp.Rational(index + 4, index + 3) * z ** (index + 1)
                - c8 * z**index
            )
            for index in range(5)
        )
    )
    internal_two = sp.expand(
        2 * sp.diff(p0, z) * q2
        + sp.diff(p1, z) * q1
        - p1 * sp.diff(q1, z)
        - 2 * p2 * q0_prime
    )
    inverse_d_plus_three = sum(
        d[index] * z**index / (index + 3)
        for index in range(5)
    )
    expected = sp.expand(
        2 * z * sp.diff(p0, z) * inverse_d_plus_three - p1**2
    )
    assert sp.expand(internal_two - expected) == 0
    assert not sp.Poly(internal_two, *a, *b, *d).is_zero
    return {
        "I2": internal_two,
        "I2_reduced": expected,
        "q2": q2,
    }


def verify_degree_cokernel_inventory() -> dict[int, tuple[int, int, int]]:
    """Return (source cap, q cap, cokernel dimension) for each m."""
    p_caps = {degree: min(degree + 2, 8) for degree in range(9)}
    q_caps = {degree: min(degree + 3, 12) for degree in range(13)}
    inventory: dict[int, tuple[int, int, int]] = {}
    for degree in range(13):
        source_caps = []
        if degree in p_caps:
            source_caps.append(p_caps[degree] + 1)
        for left_grade, left_cap in p_caps.items():
            right_grade = degree - 1 - left_grade
            if right_grade in q_caps:
                source_caps.append(
                    left_cap + q_caps[right_grade] - 1
                )
        source_cap = max(source_caps, default=q_caps[degree])
        cokernel_dimension = max(0, source_cap - q_caps[degree])
        inventory[degree] = (
            source_cap,
            q_caps[degree],
            cokernel_dimension,
        )
    assert all(
        inventory[degree][2] == 0 for degree in range(10)
    )
    assert inventory[10] == (13, 12, 1)
    assert inventory[11] == (14, 12, 2)
    assert inventory[12] == (15, 12, 3)
    return inventory


def verify_first_residue() -> dict[str, sp.Expr]:
    """Identify [z^13]J9 with the first outer-face compatibility."""
    alpha = sp.symbols("alpha0:7")
    beta = sp.symbols("beta0:10")
    p = {
        grade: alpha[grade] * z ** (grade + 2)
        for grade in range(7)
    }
    q = {
        grade: beta[grade] * z ** (grade + 3)
        for grade in range(10)
    }
    internal_nine = sp.expand(
        sum(
            right_grade * sp.diff(p[left_grade], z) * q[right_grade]
            - left_grade
            * p[left_grade]
            * sp.diff(q[right_grade], z)
            for left_grade in range(7)
            for right_grade in (9 - left_grade,)
        )
    )
    residue = sp.factor(internal_nine.coeff(z, 13))
    expected = sum(
        (18 - 5 * grade) * alpha[grade] * beta[9 - grade]
        for grade in range(7)
    )
    assert sp.expand(residue - expected) == 0

    # Put A=h*U and B=h^2*V on the outer face.  The face equation is
    # 2*A*B'-3*A'*B=h^2, equivalently
    # U*V+2*h*U*V'-3*h*U'*V=1.
    u = sp.symbols("u0:8")
    v = sp.symbols("v0:11")
    U = 1 + sum(u[index] * h ** (index + 1) for index in range(7))
    V = 1 + sum(v[index] * h ** (index + 1) for index in range(10))
    outer = sp.expand(
        U * V
        + 2 * h * U * sp.diff(V, h)
        - 3 * h * sp.diff(U, h) * V
        - 1
    )
    outer_residue = sp.factor(outer.coeff(h, 11))
    dictionary = {
        alpha[grade]: u[grade]
        for grade in range(7)
    }
    dictionary.update(
        {
            beta[grade]: v[grade]
            for grade in range(10)
        }
    )
    assert sp.expand(residue.subs(dictionary) - outer_residue) == 0
    return {
        "direct_residue": residue,
        "outer_residue": outer_residue,
        "outer_equation": outer,
    }


def recursively_solved_outer_residue(
    U: sp.Expr,
) -> tuple[sp.Expr, sp.Expr]:
    """Solve V through degree ten and return its first residue."""
    coefficients = [sp.Integer(1)]
    for degree in range(1, 11):
        new_coefficient = sp.symbols(f"temporary_v_{degree}")
        partial_v = (
            sum(
                coefficients[index] * h**index
                for index in range(degree)
            )
            + new_coefficient * h**degree
        )
        row = sp.expand(
            U * partial_v
            + 2 * h * U * sp.diff(partial_v, h)
            - 3 * h * sp.diff(U, h) * partial_v
            - 1
        ).coeff(h, degree)
        solution = sp.solve(row, new_coefficient)
        assert len(solution) == 1
        coefficients.append(sp.factor(solution[0]))
    V = sum(
        coefficients[index] * h**index
        for index in range(11)
    )
    residue = sp.factor(
        sp.expand(
            U * V
            + 2 * h * U * sp.diff(V, h)
            - 3 * h * sp.diff(U, h) * V
            - 1
        ).coeff(h, 11)
    )
    return sp.expand(V), residue


def verify_residue_is_genuine() -> dict[str, sp.Expr]:
    """Exhibit both zero and nonzero values with the required top term."""
    a, b = sp.symbols("a b", nonzero=True)
    sparse_u = 1 + b * h**7
    _sparse_v, sparse_residue = recursively_solved_outer_residue(
        sparse_u
    )
    assert sparse_residue == 0

    mixed_u = 1 + a * h**4 + b * h**7
    mixed_v, mixed_residue = recursively_solved_outer_residue(mixed_u)
    assert mixed_residue == -sp.Rational(32, 3) * a * b
    return {
        "zero_example_U": sparse_u,
        "zero_example_residue": sparse_residue,
        "nonzero_example_U": mixed_u,
        "nonzero_example_V": mixed_v,
        "nonzero_example_residue": mixed_residue,
    }


def verify_c8_has_zero_cokernel_class() -> dict[str, sp.Expr]:
    """Show the support-cost mode is Euler-exact at every grade."""
    c8 = sp.symbols("c8")
    degree = sp.symbols("m", integer=True, positive=True)
    p = sp.Function("p")(z)
    difference = sp.expand(
        (
            -z * (z - c8) * sp.diff(p, z)
            - degree * (2 * z - c8) * p
        )
        - (
            -z**2 * sp.diff(p, z)
            - 2 * degree * z * p
        )
    )
    expected = c8 * (
        z * sp.diff(p, z) + degree * p
    )
    assert sp.expand(difference - expected) == 0

    # Equivalent next-face calculation.  The missing monomial is h,
    # but A-h is allowed in the normalized positive support, and
    # L_A(h)=-L_A(A-h).
    A = sp.Function("A")(h)
    face_operator_h = sp.expand(
        2 * (A * sp.diff(h, h) - sp.diff(A, h) * h)
    )
    face_operator_allowed = sp.expand(
        2
        * (
            A * sp.diff(A - h, h)
            - sp.diff(A, h) * (A - h)
        )
    )
    assert sp.expand(face_operator_h + face_operator_allowed) == 0
    return {
        "grade_difference": difference,
        "euler_exact": expected,
        "face_missing_monomial": face_operator_h,
        "face_allowed_compensator": face_operator_allowed,
    }


def main() -> None:
    nonlinear = verify_first_nonlinear_row()
    inventory = verify_degree_cokernel_inventory()
    first = verify_first_residue()
    genuine = verify_residue_is_genuine()
    c8_exact = verify_c8_has_zero_cokernel_class()
    print("first nonzero internal row: n=2")
    print("I2 =", nonlinear["I2_reduced"])
    print("first degree-cap cokernel: n=9, representative [z^13]")
    print("cokernel dimensions at n=9,10,11:", tuple(
        inventory[degree][2] for degree in (10, 11, 12)
    ))
    print("first residue =", first["direct_residue"])
    print("nonzero test value =", genuine["nonzero_example_residue"])
    print("c8 grade contribution is Euler-exact:", c8_exact["euler_exact"])
    print("RESULT: EXACT CASE-C FIRST INTEGRAL COKERNEL PASSES")


if __name__ == "__main__":
    main()
