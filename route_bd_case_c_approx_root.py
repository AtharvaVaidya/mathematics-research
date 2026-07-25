#!/usr/bin/env python3
"""Exact approximate-root normal form for the full GGHV case-c branch.

This is an all-parameter calculation over the differential field C(h).  It
does not specialize the coefficients of P and does not sample finite fields.

For a degree-eight polynomial P in y, with leading coefficient l**8, let

    L = P**(1/8) = l*y + O(1)
    A_j = polynomial_part_at_y_infinity(L**j).

The script verifies symbolically that J(P,A_j) has y-degree at most six for
j=0,...,12.  Since A_j has leading term l**j*y**j, these polynomials are a
triangular basis.  It follows that

    deg_y J(P,Q) <= 10

is equivalent to

    Q = sum(j=4,...,12) c_j*A_j + S_3,

where the c_j are constants of the derivation and deg_y(S_3)<=3.

The final checks identify A_4 with the canonical approximate square root,
identify the old q_11 resonance with c_11, and reproduce the exact endpoint
identity which forces c_11=0 when the required p_6/q_9 edge is present.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_next_descent import universal_next_descent


y = sp.symbols("y")
ell, dell = sp.symbols("ell dell", nonzero=True)
p = sp.symbols("p0:8")
dp = sp.symbols("dp0:8")


def truncated_multiply(
    left: list[sp.Expr], right: list[sp.Expr], bound: int
) -> list[sp.Expr]:
    result = [sp.Integer(0) for _ in range(bound + 1)]
    for i, left_coefficient in enumerate(left):
        for j, right_coefficient in enumerate(right):
            if i + j <= bound:
                result[i + j] += left_coefficient * right_coefficient
    return [sp.expand(coefficient) for coefficient in result]


def polynomial_part_power(power: int) -> sp.Expr:
    """Return (P**(power/8))_+ by the finite binomial expansion."""
    defect = [sp.Integer(0) for _ in range(power + 1)]
    for order in range(1, min(8, power) + 1):
        defect[order] = p[8 - order] / ell**8

    defect_power = [sp.Integer(0) for _ in range(power + 1)]
    defect_power[0] = 1
    coefficients = [sp.Integer(0) for _ in range(power + 1)]
    exponent = sp.Rational(power, 8)
    for multiplicity in range(power + 1):
        binomial = sp.binomial(exponent, multiplicity)
        for order, coefficient in enumerate(defect_power):
            coefficients[order] += binomial * coefficient
        defect_power = truncated_multiply(
            defect_power, defect, power
        )

    return sp.expand(
        sum(
            ell**power * coefficients[order] * y ** (power - order)
            for order in range(power + 1)
        )
    )


P = sp.expand(
    ell**8 * y**8 + sum(p[degree] * y**degree for degree in range(8))
)
A = tuple(polynomial_part_power(power) for power in range(13))


def coefficient_derivative(expression: sp.Expr) -> sp.Expr:
    variables = (ell,) + p
    derivatives = (dell,) + dp
    return sp.expand(
        sum(
            sp.diff(expression, variable) * derivative
            for variable, derivative in zip(variables, derivatives)
        )
    )


def jacobian(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    return sp.expand(
        coefficient_derivative(left) * sp.diff(right, y)
        - sp.diff(left, y) * coefficient_derivative(right)
    )


def verify_all_parameter_normal_form() -> None:
    # The finite binomial construction is triangular, with exact diagonal
    # ell**j.  Thus A_0,...,A_12 is a basis of K[y]_(degree <= 12).
    for power, approximate_power in enumerate(A):
        polynomial = sp.Poly(approximate_power, y)
        assert polynomial.degree() == power
        assert polynomial.coeff_monomial(y**power) == ell**power

        # L**power-A_power starts with y**(-1).  The following direct
        # symbolic calculation verifies the resulting degree-six bound
        # without assigning values to any coefficient or derivative.
        bracket = sp.Poly(jacobian(P, approximate_power), y)
        assert all(
            degree[0] <= 6 for degree, _ in bracket.terms()
        )

        # If a basis coefficient d_j(h) is allowed to vary, the only
        # high-degree contribution is -d_j' P_y A_j.  Its diagonal term
        # is nonzero, making the equations for d_12',...,d_4'
        # descending triangular.
        diagonal = sp.Poly(
            -sp.diff(P, y) * approximate_power, y
        ).coeff_monomial(y ** (power + 7))
        assert sp.expand(diagonal + 8 * ell ** (power + 8)) == 0

    # Consequently the nine equations in y-degrees 19,...,11 say,
    # successively and without a genericity assumption, that the
    # derivatives of the A_12,...,A_4 coefficients vanish.


def verify_square_cube_interpretation() -> None:
    H = A[4]
    remainder = sp.expand(P - H**2)
    assert sp.Poly(remainder, y).degree() <= 3
    assert sp.expand(A[8] - P) == 0

    # The degree >=3 portion of the approximate cube has the familiar
    # square-root form.  The omitted correction has degree at most two
    # and is absorbed by S_3 in the normal form.
    cube_difference = sp.expand(
        A[12] - H**3 - sp.Rational(3, 2) * H * remainder
    )
    assert sp.Poly(cube_difference, y).degree() <= 2

    h, alpha = sp.symbols("h alpha", nonzero=True)
    r = sp.symbols("r0:5")
    r_poly = sum(r[index] * h**index for index in range(5))
    p6 = sp.symbols("p6")
    substitutions = {
        ell: alpha * h,
        p[7]: h**4 * r_poly,
        p[6]: p6,
    }
    H_specialized = sp.Poly(sp.expand(H.subs(substitutions)), y)
    assert sp.expand(
        H_specialized.coeff_monomial(y**4) - alpha**4 * h**4
    ) == 0
    assert sp.expand(
        H_specialized.coeff_monomial(y**3)
        - r_poly / (2 * alpha**4)
    ) == 0
    expected_y2 = (
        p6 - r_poly**2 / (4 * alpha**8)
    ) / (2 * alpha**4 * h**4)
    assert sp.simplify(
        H_specialized.coeff_monomial(y**2) - expected_y2
    ) == 0


def verify_resonance_and_required_vertices() -> None:
    h, alpha, b = sp.symbols("h alpha b", nonzero=True)
    c11 = sp.symbols("c11")
    r = sp.symbols("r0:5")
    r_poly = sum(r[index] * h**index for index in range(5))
    p6_coefficients = sp.symbols("u0:9")
    p5_coefficients = sp.symbols("v0:8")
    p6_poly = sum(
        p6_coefficients[index] * h**index for index in range(9)
    )
    p5_poly = sum(
        p5_coefficients[index] * h**index for index in range(8)
    )
    edge_substitutions = {
        ell: alpha * h,
        p[7]: h**4 * r_poly,
        p[6]: p6_poly,
        p[5]: p5_poly,
    }

    # c_12 is fixed by q_12=b*h**12.  The y^11 coefficient separates
    # into the forced approximate-cube term and the old resonance.
    c12 = b / alpha**12
    A12_polynomial = sp.Poly(A[12], y)
    A11_polynomial = sp.Poly(A[11], y)
    q11 = sp.expand(
        c12
        * A12_polynomial.coeff_monomial(y**11).subs(
            edge_substitutions
        )
        + c11
        * A11_polynomial.coeff_monomial(y**11).subs(
            edge_substitutions
        )
    )
    assert sp.expand(
        q11
        - (
            sp.Rational(3, 2)
            * b
            / alpha**8
            * h**8
            * r_poly
            + c11 * alpha**11 * h**11
        )
    ) == 0

    # The required p_6 vertex and the vertical-edge square theorem give
    # [h^8]p_6=r_4^2/(4*alpha^8).  Only c_12*A_12 can contribute to
    # [h^12]q_9.  This recovers the required nonzero cube coefficient.
    q9_from_cube = sp.expand(
        c12
        * A12_polynomial.coeff_monomial(y**9).subs(
            edge_substitutions
        )
    ).subs(
        {p6_coefficients[8]: r[4] ** 2 / (4 * alpha**8)}
    )
    q9_leading = sp.Poly(sp.expand(q9_from_cube), h).coeff_monomial(
        h**12
    )
    assert sp.simplify(
        q9_leading - b * r[4] ** 3 / (8 * alpha**24)
    ) == 0

    # In the previous coefficient notation lambda=c_11*alpha^11.  The
    # exact grade-15 endpoint compatibility is the displayed nonzero
    # multiple.  Since alpha,b,r_4 are nonzero, it forces c_11=0.
    descent = universal_next_descent()
    endpoint_raw = dict(descent["grade15_compatibility"])[18]
    raw_symbols = {str(symbol): symbol for symbol in endpoint_raw.free_symbols}
    raw_lambda = raw_symbols["lambda"]
    raw_r4 = raw_symbols["p7_8"]
    raw_a = raw_symbols["a"]
    assert sp.simplify(
        endpoint_raw
        + sp.Rational(77, 1024)
        * raw_lambda
        * raw_r4**4
        / raw_a**3
    ) == 0

    resonance = c11 * alpha**11
    endpoint = (
        -sp.Rational(77, 1024)
        * resonance
        * r[4] ** 4
        / alpha**24
    )
    assert sp.factor(
        endpoint
        / (
            -sp.Rational(77, 1024)
            * c11
            * r[4] ** 4
            / alpha**13
        )
    ) == 1


def main() -> None:
    verify_all_parameter_normal_form()
    verify_square_cube_interpretation()
    verify_resonance_and_required_vertices()
    print("case-c approximate-root basis: A_j=(P^(j/8))_+, j=0,...,12")
    print("verified symbolically for arbitrary P coefficients and derivatives")
    print(
        "E_12,...,E_20 iff Q=sum_(j=4)^12 c_j*A_j+S_3, "
        "with c_j constant and deg_y S_3<=3"
    )
    print("A_4=H, deg_y(P-H^2)<=3, A_8=P")
    print("the old q_11 resonance is c_11*(alpha*h)^11")
    print("required endpoint compatibility forces c_11=0")
    print("required q_9 leading coefficient is b*r_4^3/(8*alpha^24)")
    print("RESULT: EXACT ALL-PARAMETER APPROXIMATE-ROOT CHECKS PASS")


if __name__ == "__main__":
    main()
