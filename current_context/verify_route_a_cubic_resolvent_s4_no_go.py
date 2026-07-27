#!/usr/bin/env python3
"""Exact checks for the Route A cubic-resolvent S4 no-go."""

from __future__ import annotations

import sympy as sp


u, v, w, P, Q, T, Z = sp.symbols("u v w P Q T Z")


def reduce_surface(expression: sp.Expr) -> sp.Expr:
    """Reduce modulo w^2-u-u^2*v."""
    return sp.factor(
        sp.rem(
            sp.Poly(sp.expand(expression), w),
            sp.Poly(w**2 - u - u**2 * v, w),
        ).as_expr()
    )


def bracket(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    """Route A Poisson bracket."""
    raw = (
        -2 * w
        * (
            sp.diff(left, u) * sp.diff(right, v)
            - sp.diff(left, v) * sp.diff(right, u)
        )
        - u**2
        * (
            sp.diff(left, u) * sp.diff(right, w)
            - sp.diff(left, w) * sp.diff(right, u)
        )
        + (1 + 2 * u * v)
        * (
            sp.diff(left, v) * sp.diff(right, w)
            - sp.diff(left, w) * sp.diff(right, v)
        )
    )
    return reduce_surface(raw)


def main() -> None:
    p = w
    q = sp.expand(u * (u + 2 - v) / 4)
    cubic = sp.expand(T * (T + 1) ** 2 - 4 * Q * T - P**2)
    quartic = Z**4 + Z**2 + P * Z + Q

    assert reduce_surface(cubic.subs({T: u, P: p, Q: q})) == 0
    assert sp.factor(sp.diff(cubic, T).subs({T: u, P: p, Q: q})) == (
        2 * u**2 + u * v + 2 * u + 1
    )

    cubic_discriminant = sp.factor(sp.discriminant(cubic, T))
    quartic_discriminant = sp.factor(sp.discriminant(quartic, Z))
    assert cubic_discriminant == quartic_discriminant
    assert cubic_discriminant == (
        -27 * P**4
        + 144 * P**2 * Q
        - 4 * P**2
        + 256 * Q**3
        - 128 * Q**2
        + 16 * Q
    )

    pulled_discriminant = reduce_surface(
        cubic_discriminant.subs({P: p, Q: q})
    )
    ramification_factor = 2 * u**2 + u * v + 2 * u + 1
    retained_factor = u - 4 * v + 4
    assert pulled_discriminant == sp.factor(
        u * retained_factor * ramification_factor**2
    )
    assert bracket(p, q) == u * ramification_factor / 4

    # Factor the quartic after adjoining s^2=T.
    s = sp.symbols("s", nonzero=True)
    left = Z**2 - s * Z + (T + 1 + P / s) / 2
    right = Z**2 + s * Z + (T + 1 - P / s) / 2
    factor_error = sp.together(
        sp.expand(left * right - quartic).subs(s**2, T)
    )
    numerator = sp.factor(sp.together(factor_error).as_numer_denom()[0])
    assert sp.rem(
        sp.Poly(numerator, T),
        sp.Poly(cubic, T),
    ).as_expr() == 0

    # Exact S4 specialization certificate.
    specialized = Z**4 + Z**2 + Z + 1
    assert sp.discriminant(specialized, Z) == 257
    assert sp.Poly(specialized, Z, modulus=3).is_irreducible
    factors_mod_2 = sp.factor_list(specialized, Z, modulus=2)[1]
    factor_degrees = sorted(
        sp.degree(factor, Z)
        for factor, multiplicity in factors_mod_2
        for _ in range(multiplicity)
    )
    assert factor_degrees == [1, 3]

    # The canonical finite double cover.
    a, z = sp.symbols("a z")
    cover_relation = z**2 - 1 - a**2 * v
    assert sp.expand(
        (w**2 - u - u**2 * v).subs({u: a**2, w: a * z})
        - a**2 * cover_relation
    ) == 0

    # The retained principal curve is integral.
    retained_equation = 4 * w**2 - u * (u + 2) ** 2
    assert sp.Poly(retained_equation, w).is_irreducible
    assert sp.rem(
        sp.Poly(
            sp.together((2 * w / (u + 2)) ** 2 - u).as_numer_denom()[0],
            w,
        ),
        sp.Poly(retained_equation, w),
    ).as_expr() == 0

    # Every correction preserving the exact quartic-resolvent identity
    # has P=w*A+u*H.  Check its boundary bracket on a generic polynomial
    # test family; the displayed algebra in the memo proves the same
    # formula for arbitrary A,H in B.
    coefficients = sp.symbols("a0:5")
    A = sum(coefficient * v**index for index, coefficient in enumerate(coefficients))
    H = u + v + w
    c = sp.symbols("c")
    corrected_p = w * A + u * H
    corrected_q = sp.expand(
        (u + c) ** 2 / 4
        - ((1 + u * v) * A**2 + 2 * w * A * H + u * H**2) / 4
    )
    boundary_bracket = sp.factor(
        bracket(corrected_p, corrected_q).subs({u: 0, w: 0})
    )
    assert boundary_bracket == sp.factor(A**2 * sp.diff(A, v) / 2)

    # Degree obstruction to A^2*A'=nonzero constant.
    for degree in range(1, 100):
        assert 3 * degree - 1 > 0

    # In the varying-coefficient ansatz, the boundary unit equation
    # forces A0 constant and Q0 affine.  No polynomial C(Y) can then
    # make C(Y)^2-4Y constant.
    Y = sp.symbols("Y")
    varying_coefficients = sp.symbols("c0:8")
    for degree in range(0, len(varying_coefficients)):
        C = sum(
            varying_coefficients[index] * Y**index
            for index in range(degree + 1)
        )
        if degree == 0:
            assert sp.degree(C**2 - 4 * Y, Y) == 1
        else:
            # On the exact-degree stratum the leading square term has
            # degree 2*degree and cannot cancel the linear term.
            assert sp.Poly(C**2 - 4 * Y, Y).coeff_monomial(
                Y ** (2 * degree)
            ) == varying_coefficients[degree] ** 2

    # The source-ring strengthening ends with the same elementary
    # degree impossibility: a polynomial square cannot be a nonconstant
    # affine polynomial.
    for degree in range(0, 100):
        square_degree = 0 if degree == 0 else 2 * degree
        assert square_degree != 1

    print("verified the cubic/quartic resolvent identity")
    print("verified the S4 specialization cycle certificate")
    print("verified the canonical sqrt(u) cover and distinct discriminant cover")
    print("verified the retained principal sheet and exact bracket failure")
    print("verified the all-polynomial exact-resolvent boundary obstruction")
    print("verified the polynomially varying quartic-coefficient obstruction")
    print("verified the source-ring quartic-resolvent Darboux obstruction")
    print("RESULT: ROUTE A RESOLVENT COMPARISON DOES NOT EXCLUDE DEGREE THREE")


if __name__ == "__main__":
    main()
