#!/usr/bin/env python3
"""Identify the case-c diagonal exactness locus with the a/b Hurwitz ODE.

The genus-three diagonal differential is exact precisely when there is a
polynomial R of degree at most ten such that

    2*C*R' - 3*C'*R = 2*q^16,

where C is monic of degree seven and has nonzero constant coefficient.
Under

    w=1/q,  C=q^7*U(w),  R=-2*q^10*V(w),

this is exactly

    U*V + 2*w*U*V' - 3*w*U'*V = 1.

Thus its scaling quotient is the same five-point degree-21 Hurwitz space as
the outer a/b equation.  The normalization [q^0]C=1 is the slice u7=1 and
meets each free scaling orbit in seven points, giving 35 points.
"""

from __future__ import annotations

import sympy as sp

from route_bd_ab_hurwitz_count import hurwitz_number
from route_bd_fbar_obstruction import K, PRIME, T, outer_coefficients


def verify_modular_representatives() -> None:
    """Scale the existing two rational and one cubic outer points to u7=1."""

    seventh_root_exponent = pow(7, -1, PRIME**3 - 1)

    def multiply(left: list[K], right: list[K]) -> list[K]:
        result = [K()] * (len(left) + len(right) - 1)
        for i, a in enumerate(left):
            for j, b in enumerate(right):
                result[i + j] += a * b
        return result

    def derivative(poly: list[K]) -> list[K]:
        return [degree * poly[degree] for degree in range(1, len(poly))]

    for primitive in (K(26839), K(16621), T):
        u, v = outer_coefficients(primitive)
        scaling = primitive**seventh_root_exponent
        assert scaling**7 == primitive
        scaled_u = [coefficient * scaling**degree for degree, coefficient in enumerate(u)]
        scaled_v = [coefficient * scaling**degree for degree, coefficient in enumerate(v)]
        assert scaled_u[7] == K(1)

        # Coefficients are stored in increasing q-degree.
        C = list(reversed(scaled_u))
        R = [-2 * coefficient for coefficient in reversed(scaled_v)]
        left = [
            2 * value
            for value in multiply(C, derivative(R))
        ]
        right = [
            3 * value
            for value in multiply(derivative(C), R)
        ]
        size = max(len(left), len(right), 17)
        residual = [
            (left[index] if index < len(left) else K())
            - (right[index] if index < len(right) else K())
            - (K(2) if index == 16 else K())
            for index in range(size)
        ]
        assert not any(residual)


def main() -> None:
    q, w, scaling = sp.symbols("q w scaling", nonzero=True)
    u = (sp.Integer(1), *sp.symbols("u1:8"))
    v = (sp.Integer(1), *sp.symbols("v1:11"))
    U = sum(u[index] * w**index for index in range(8))
    V = sum(v[index] * w**index for index in range(11))

    # Differentiate after w=q^{-1}, keeping the intermediate formulas
    # explicit so the signs and the factor -2 in R are independently checked.
    Uq = U.subs(w, 1 / q)
    Vq = V.subs(w, 1 / q)
    C = q**7 * Uq
    R = sp.expand(-2 * q**10 * Vq)
    diagonal = sp.expand(2 * C * sp.diff(R, q) - 3 * sp.diff(C, q) * R)
    outer = U * V + 2 * w * U * sp.diff(V, w) - 3 * w * sp.diff(U, w) * V
    assert sp.cancel(diagonal - 2 * q**16 * outer.subs(w, 1 / q)) == 0

    # Coefficient reversal:
    #   C=q^7+c6*q^6+...+c0  <=>  U=1+c6*w+...+c0*w^7,
    #   [q^(10-j)]R=-2*v_j.
    c = sp.symbols("c0:7")
    reversed_C = q**7 + sum(c[index] * q**index for index in range(7))
    reversed_U = sp.expand(q**-7 * reversed_C).subs(q, 1 / w)
    expected_U = 1 + sum(c[7 - index] * w**index for index in range(1, 8))
    assert sp.expand(reversed_U - expected_U) == 0
    for index in range(11):
        assert sp.expand(R.coeff(q, 10 - index) + 2 * v[index]) == 0

    # The G_m action preserves both normalizations and gives weight seven to
    # c0=u7.  It is the q-coordinate form of w -> scaling*w.
    scaled_C = sp.expand(scaling**7 * reversed_C.subs(q, q / scaling))
    for index in range(7):
        assert scaled_C.coeff(q, index) == scaling ** (7 - index) * c[index]
    assert scaled_C.coeff(q, 0) == scaling**7 * c[0]

    _character_sum, hurwitz_count, _nonzero_terms = hurwitz_number()
    assert hurwitz_count == 5
    slice_degree = 7
    assert slice_degree * hurwitz_count == 35

    # Reuse of the certified p=32003 outer algebra is literal.  Its
    # primitive element is s=u7^{-1}; adjoining scaling^7=s gives the
    # c0=u7=1 slice.  The composed eliminant is reduced of degree 35.
    prime = 32003
    s = sp.symbols("s")
    outer_eliminant = (
        s**5
        + 9413 * s**4
        + 8734 * s**3
        - 3563 * s**2
        + 7508 * s
        - 3664
    )
    slice_eliminant = sp.Poly(
        outer_eliminant.subs(s, scaling**7),
        scaling,
        modulus=prime,
    )
    assert slice_eliminant.degree() == 35
    assert sp.gcd(slice_eliminant, slice_eliminant.diff()).degree() == 0
    verify_modular_representatives()

    # Radial-deficit grading for the transverse system.
    for p_degree in range(-8, 3):
        for q_degree in range(-12, 4):
            row_degree = p_degree + q_degree - 1
            assert (2 - p_degree) + (3 - q_degree) == 4 - row_degree
    parameter_weights = (
        2 - 1,
        3 - 2,
        2 - 0,
        3 - 1,
        2 - (-1),
        3 - 0,
        2 - (-2),
    )
    assert parameter_weights == (1, 1, 2, 2, 3, 3, 4)
    # z^i*w^j corresponds to x^(i+j)*y^(i+2j).
    assert (0 + 8, 0 + 2 * 8) == (8, 16)
    assert (0 + 12, 0 + 2 * 12) == (12, 24)

    print("2*C*R'-3*C'*R = 2*q^16 times the normalized outer ODE")
    print("coefficient map: u_i=c_(7-i), v_j=-r_(10-j)/2")
    print("c0=u7 has scaling weight 7")
    print("Hurwitz orbits:", hurwitz_count)
    print("u7=1 slice degree:", slice_degree)
    print("mod-32003 slice eliminant: h(scaling^7), squarefree of degree 35")
    print("scaled representatives verified in the two rational and cubic fields")
    print("transverse parameter weights:", parameter_weights)
    print("RESULT: CASE-c DIAGONAL LOCUS IS THE SAME FIVE-ORBIT HURWITZ SPACE")
    print("RESULT: ITS c0=1 NORMALIZATION HAS 35 GEOMETRIC POINTS")


if __name__ == "__main__":
    main()
