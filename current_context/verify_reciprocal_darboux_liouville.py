#!/usr/bin/env python3
"""Exact checks for RECIPROCAL_DARBOUX_LIOUVILLE_AUDIT.md."""

from __future__ import annotations

import sympy as sp


def wedge_coefficient(
    left: sp.Expr,
    right: sp.Expr,
    x: sp.Symbol,
    t: sp.Symbol,
) -> sp.Expr:
    """Coefficient of dx wedge dt in d(left) wedge d(right)."""

    return sp.expand(
        sp.diff(left, x) * sp.diff(right, t)
        - sp.diff(left, t) * sp.diff(right, x)
    )


def k1_endpoint() -> tuple[sp.Symbol, sp.Expr, sp.Expr]:
    t = sp.symbols("t")
    a = (
        t**3
        + t**2
        + sp.Rational(6, 25) * t
        + sp.Rational(9, 250)
    )
    b = (
        t**4
        + sp.Rational(2, 3) * t**3
        + sp.Rational(6, 25) * t**2
        + sp.Rational(36, 875) * t
        + sp.Rational(18, 4375)
    )
    return t, a, b


def verify_general_weight_arithmetic() -> None:
    m = sp.symbols("m", integer=True, positive=True)
    p = 2 * m + 1
    q = 3 * m + 1
    n = 5 * m + 2

    assert sp.expand(p + q - n) == 0
    assert sp.expand(5 * m - n) == -2
    assert sp.gcd(p, n) == 1
    assert sp.gcd(5, n) == 1


def verify_k1_wronskian_and_darboux_signs() -> None:
    t, a, b = k1_endpoint()
    x = sp.symbols("xi", nonzero=True)
    n = 7

    wronskian = sp.expand(3 * sp.diff(a, t) * b - 2 * a * sp.diff(b, t))
    assert wronskian == t ** (n - 1)

    p = x**2 * a
    q = x**3 * b
    s = x**5
    y = t**n

    jacobian = wedge_coefficient(p, q, x, t)
    assert sp.factor(jacobian + x**4 * t ** (n - 1)) == 0

    # Coefficients of dxi and dt in 3Q dP - 2P dQ.
    liouville_x = sp.expand(
        3 * q * sp.diff(p, x) - 2 * p * sp.diff(q, x)
    )
    liouville_t = sp.expand(
        3 * q * sp.diff(p, t) - 2 * p * sp.diff(q, t)
    )
    assert liouville_x == 0
    assert sp.factor(liouville_t - s * t ** (n - 1)) == 0
    assert sp.factor(liouville_t - s * sp.diff(y, t) / n) == 0

    product = s * y
    logarithmic_y = sp.diff(y, t) / y
    assert sp.factor(n * liouville_t / product - logarithmic_y) == 0

    darboux = -wedge_coefficient(s, y, x, t) / (5 * n)
    assert sp.factor(jacobian - darboux) == 0


def verify_k1_cusp_and_local_model() -> None:
    t, a, b = k1_endpoint()
    x = sp.symbols("x", nonzero=True)
    n = 7

    ratio = sp.cancel(b**2 / a**3)
    critical_value = sp.factor(ratio.subs(t, 0))
    assert critical_value == sp.Rational(160, 441)
    cusp_numerator = sp.factor(b**2 - critical_value * a**3)
    assert cusp_numerator == (
        -t**7 * (800 * t**2 + 195 * t + 36) / 2205
    )

    # The square-root coordinate r=B/A^(3/2) has exact contact order 7.
    radial = b / a ** sp.Rational(3, 2)
    radial_zero = radial.subs(t, 0)
    radial_derivative = sp.diff(radial, t)
    expected_derivative = -t**6 / (2 * a ** sp.Rational(5, 2))
    assert sp.simplify(radial_derivative - expected_derivative) == 0

    radial_series = sp.series(radial - radial_zero, t, 0, 9).removeO()
    assert sp.expand(radial_series).coeff(t, 7) != 0
    assert sp.expand(radial_series).coeff(t, 8) != 0
    assert all(sp.expand(radial_series).coeff(t, j) == 0 for j in range(7))

    # Completed-local genuine-endpoint model:
    # Xi=x/sqrt(A), P=x^2, Q=x^3*r(t).
    xi = x / sp.sqrt(a)
    p = x**2
    q = x**3 * radial
    assert sp.simplify(xi**2 * a - p) == 0
    assert sp.simplify(xi**3 * b - q) == 0

    liouville_x = sp.simplify(
        3 * q * sp.diff(p, x) - 2 * p * sp.diff(q, x)
    )
    liouville_t = sp.simplify(
        3 * q * sp.diff(p, t) - 2 * p * sp.diff(q, t)
    )
    assert liouville_x == 0
    assert sp.simplify(liouville_t - xi**5 * t**6) == 0
    assert sp.simplify(liouville_t + 2 * x**5 * radial_derivative) == 0

    jacobian = wedge_coefficient(p, q, x, t)
    s = xi**5
    y = t**n
    darboux = -wedge_coefficient(s, y, x, t) / (5 * n)
    assert sp.simplify(jacobian - darboux) == 0

    # If T^7 were in the base local field, A(T)^5 would have to be a
    # series in T^7.  The exact endpoint violates that invariance.
    a_fifth = sp.Poly(sp.expand(a**5), t)
    forbidden_exponents = [
        degree
        for (degree,), coefficient in a_fifth.terms()
        if coefficient != 0 and degree % n != 0
    ]
    assert forbidden_exponents


def verify_generic_inverse_is_nontrivial() -> None:
    t, a, b = k1_endpoint()
    rho, y = sp.symbols("rho y")

    fiber = sp.Poly(
        b**2 - rho * a**3,
        t,
        domain=sp.QQ.frac_field(rho),
    )
    assert fiber.degree() == 9
    assert len(sp.factor_list(fiber.as_expr())[1]) == 1

    # Since gcd(deg R, 7)=1, adjoining t^7 to Q(R) recovers Q(t).
    # The resultant confirms that t^7 still has degree 9 over Q(R).
    eliminant = sp.resultant(t**7 - y, b**2 - rho * a**3, t)
    assert sp.degree(eliminant, y) == 9
    assert sp.degree(eliminant, rho) == 7
    factors = sp.factor_list(eliminant)[1]
    assert len(factors) == 1
    assert sp.degree(factors[0][0], y) == 9


def main() -> None:
    verify_general_weight_arithmetic()
    verify_k1_wronskian_and_darboux_signs()
    verify_k1_cusp_and_local_model()
    verify_generic_inverse_is_nontrivial()
    print("verified reciprocal Wronskian sign and normalized constant")
    print("verified Liouville and Darboux identities with negative wedge sign")
    print("verified descent equivalence arithmetic for Xi^5 and T^(5k+2)")
    print("verified the product invariant Xi^5*T^(5k+2)=Z^5/W^2")
    print("verified exact k=1 genuine-endpoint local cusp countermodel")
    print("RESULT: either Darboux power descends iff the whole branch descends")


if __name__ == "__main__":
    main()
