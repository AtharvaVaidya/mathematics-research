#!/usr/bin/env python3
"""Exact primitive marked degree-(8,12) generalized Davenport pairs.

The coefficient field is

    Q[r,t] / (r^3-t, 512000000*t^2-13257900*t-177147).

For each of the two values of t and each cube root r, the displayed
polynomials give a primitive parametrization with a marked cusp and
Weierstrass remainder of degree seven.
"""

from __future__ import annotations

import sympy as sp


h, r, t = sp.symbols("h r t")
T_POLYNOMIAL = 512000000 * t**2 - 13257900 * t - 177147
QUOTIENT = sp.groebner((r**3 - t, T_POLYNOMIAL), r, t, order="lex")


def reduce_coefficient(expression: sp.Expr) -> sp.Expr:
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    remainder = QUOTIENT.reduce(sp.Poly(numerator, r, t).as_expr())[1]
    return sp.factor(remainder / denominator)


def reduce_polynomial(expression: sp.Expr) -> sp.Expr:
    polynomial = sp.Poly(sp.expand(expression), h)
    return sp.Add(
        *(
            reduce_coefficient(polynomial.coeff_monomial(h**degree)) * h**degree
            for degree in range(polynomial.degree() + 1)
        )
    )


def pair() -> tuple[sp.Expr, sp.Expr]:
    a3 = 5 * r**2 * (35840000 * t - 591093) / 403623
    a2 = (128000 * t - 3339) / 29898
    a0 = 4 * r**2 * (1600000 * t - 34263) / 44847
    A = h**8 + h**5 + r * h**4 + a3 * h**3 + a2 * h**2 + a0

    B = (
        h**12
        + sp.Rational(3, 2) * h**9
        + sp.Rational(3, 2) * r * h**8
        + 5 * r**2 * (35840000 * t - 591093) / 269082 * h**7
        + (256000 * t + 8271) / 39864 * h**6
        + sp.Rational(3, 4) * r * h**5
        + r**2 * (588800000 * t - 10441179) / 1076328 * h**4
        + (1264000 * t - 6189) / 199320 * h**3
        + r * (512000 * t - 6561) / 14496 * h**2
        - (1359632 * t - 19683) / 637824
    )
    return A, B


def verify_pair_and_remainder() -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    A, B = pair()
    assert sp.degree(A, h) == 8
    assert sp.degree(B, h) == 12
    assert sp.Poly(A, h).coeff_monomial(h**7) == 0

    D = reduce_polynomial(B**2 - A**3)
    assert sp.degree(D, h) == 8
    assert all(
        sp.Poly(D, h).coeff_monomial(h**degree) == 0
        for degree in (11, 10, 9, 1)
    )
    expected_d8 = -19 * r * (512000 * t - 6561) / 579840
    assert reduce_coefficient(sp.Poly(D, h).coeff_monomial(h**8) - expected_d8) == 0

    # H(X,Y)=Y^2-X^3+uX is a smooth cubic, and H(A,B) has exact degree 7.
    u = -sp.Poly(D, h).coeff_monomial(h**8)
    G = reduce_polynomial(D + u * A)
    expected_g7 = r**2 * (5120000 * t - 836163) / 1913472
    assert sp.degree(G, h) == 7
    assert reduce_coefficient(sp.Poly(G, h).coeff_monomial(h**7) - expected_g7) == 0
    assert sp.resultant(
        T_POLYNOMIAL,
        sp.together(expected_g7 / r**2).as_numer_denom()[0],
        t,
    ) != 0
    assert sp.resultant(
        T_POLYNOMIAL,
        sp.together(u / r).as_numer_denom()[0],
        t,
    ) != 0

    # The chosen source point is nonimmersive.
    assert sp.diff(A, h).subs(h, 0) == 0
    assert sp.diff(B, h).subs(h, 0) == 0
    return A, B, G


def verify_primitivity_and_cusp(A: sp.Expr, B: sp.Expr) -> None:
    derivative_A = sp.exquo(sp.Poly(sp.diff(A, h), h), sp.Poly(h, h)).as_expr()
    derivative_B = sp.exquo(sp.Poly(sp.diff(B, h), h), sp.Poly(h, h)).as_expr()
    resultant = reduce_coefficient(sp.resultant(derivative_A, derivative_B, h))
    expected = (
        -sp.Rational(2592, 648828125)
        * (33187589620394900 * t + 273822469190757)
    )
    assert reduce_coefficient(resultant - expected) == 0
    assert sp.resultant(
        T_POLYNOMIAL,
        33187589620394900 * t + 273822469190757,
        t,
    ) != 0

    # Hence gcd(A',B')=h.  A common inner polynomial would have degree
    # dividing gcd(8,12)=4, and its derivative would divide this gcd.
    # The only remaining possibility is a quadratic in h^2; the h^5
    # coefficient of A rules that out.
    assert sp.Poly(A, h).coeff_monomial(h**5) == 1

    # After subtracting the tangent, the marked singularity has type (2,3).
    polynomial_A = sp.Poly(A, h)
    polynomial_B = sp.Poly(B, h)
    a2 = polynomial_A.coeff_monomial(h**2)
    b2 = polynomial_B.coeff_monomial(h**2)
    assert sp.resultant(
        T_POLYNOMIAL, sp.together(a2).as_numer_denom()[0], t
    ) != 0
    tangent = reduce_coefficient(b2 / a2)
    transverse = reduce_polynomial(
        B
        - polynomial_B.coeff_monomial(1)
        - tangent * (A - polynomial_A.coeff_monomial(1))
    )
    assert sp.Poly(transverse, h).coeff_monomial(h**2) == 0
    cubic = sp.Poly(transverse, h).coeff_monomial(h**3)
    expected_cubic = -7 * (2048000 * t - 8577) / (
        64 * (128000 * t - 3339)
    )
    assert reduce_coefficient(cubic - expected_cubic) == 0
    assert sp.resultant(
        T_POLYNOMIAL,
        sp.together(expected_cubic).as_numer_denom()[0],
        t,
    ) != 0


def main() -> None:
    A, B, G = verify_pair_and_remainder()
    verify_primitivity_and_cusp(A, B)
    roots = sp.solve(T_POLYNOMIAL, t)
    assert roots == [
        sp.Rational(132579, 10240000) - sp.Rational(14949, 10240000) * sp.sqrt(241),
        sp.Rational(132579, 10240000) + sp.Rational(14949, 10240000) * sp.sqrt(241),
    ]
    print("verified six exact marked pairs (two t-values, three cube roots each)")
    print("verified H(A,B) has exact degree 7 for a smooth Weierstrass cubic")
    print("verified gcd(A',B')=h and ruled out polynomial composition")
    print("verified the marked branch has cusp type (2,3)")
    print("RESULT: PRIMITIVE GLOBAL MARKED PAIRS EXIST")


if __name__ == "__main__":
    main()
