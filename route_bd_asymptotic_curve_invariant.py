#!/usr/bin/env python3
"""Exact checks for the five-block asymptotic-curve invariant.

The script verifies:

* an exact five-block solution over Q(theta)/(27 theta^2-9 theta+1)
  whose asymptotic curve is not contained in a (2,3)-cusp;
* the coefficient formula and pole bound used in conditional cusp
  rigidity;
* examples of degrees 1, 2, and 4 for polynomial parametrizations of
  degree pair (8,12).
"""

from __future__ import annotations

import sympy as sp


def reduce_theta(expression: sp.Expr, theta: sp.Symbol) -> sp.Expr:
    """Reduce a rational-coefficient polynomial modulo theta's quadratic."""

    numerator, denominator = sp.cancel(expression).as_numer_denom()
    assert not denominator.has(theta)
    modulus = 27 * theta**2 - 9 * theta + 1
    numerator_remainder = sp.rem(numerator, modulus, theta)
    return sp.cancel(numerator_remainder / denominator)


def verify_non_cusp_five_block_solution() -> None:
    z, w, theta = sp.symbols("z w theta")
    d = (9 * theta + 1) / 7
    e = 3 * theta * d / 5

    a0 = theta * w**3
    a1 = w
    a2 = sp.Integer(0)
    b0 = e * w**5
    b1 = d * w**3
    b2 = w
    b3 = sp.Integer(0)

    equations = [
        a1 * sp.diff(b0, w) - sp.diff(a0, w) * b1,
        w**2
        * (
            2 * a2 * sp.diff(b0, w)
            + a1 * sp.diff(b1, w)
            - sp.diff(a1, w) * b1
            - 2 * sp.diff(a0, w) * b2
        )
        + 2 * w * sp.diff(b0, w),
        w**2
        * (
            2 * a2 * sp.diff(b1, w)
            + a1 * sp.diff(b2, w)
            - 2 * sp.diff(a1, w) * b2
            - sp.diff(a2, w) * b1
            - 3 * sp.diff(a0, w) * b3
        )
        + b1
        + 2 * w * sp.diff(b1, w)
        - 3 * w * sp.diff(a0, w),
        w**2
        * (
            2 * a2 * sp.diff(b2, w)
            + a1 * sp.diff(b3, w)
            - 3 * sp.diff(a1, w) * b3
            - 2 * sp.diff(a2, w) * b2
        )
        + 2 * b2
        + 2 * w * sp.diff(b2, w)
        - a1
        - 3 * w * sp.diff(a1, w),
        w**2
        * (2 * a2 * sp.diff(b3, w) - 3 * sp.diff(a2, w) * b3)
        + 3 * b3
        + 2 * w * sp.diff(b3, w)
        - 2 * a2
        - 3 * w * sp.diff(a2, w),
    ]
    assert all(reduce_theta(equation, theta) == 0 for equation in equations)

    P = z**2 / w + a0 + z * a1 + z**2 * a2
    Q = z**3 / w + b0 + z * b1 + z**2 * b2 + z**3 * b3
    jacobian = sp.diff(P, z) * sp.diff(Q, w) - sp.diff(P, w) * sp.diff(Q, z)
    assert reduce_theta(sp.cancel((jacobian - z**4 / w**3) * w**3), theta) == 0

    cusp_ratio = sp.cancel(b0**2 / a0**3)
    assert sp.diff(cusp_ratio, w) != 0
    assert sp.degree(a0, w) == 3
    assert sp.degree(b0, w) == 5


def verify_cusp_coordinate_and_pole_formula() -> None:
    P, Q, alpha, beta, L, h = sp.symbols("P Q alpha beta L h", nonzero=True)
    t = alpha * Q / (beta * P)
    n = Q**2 - L * P**3
    target_jacobian = sp.simplify(
        sp.diff(t, P) * sp.diff(n, Q) - sp.diff(t, Q) * sp.diff(n, P)
    )
    boundary = target_jacobian.subs(
        {
            P: alpha * h**2,
            Q: beta * h**3,
            L: beta**2 / alpha**3,
        }
    )
    assert sp.simplify(boundary - beta * h**2 / alpha) == 0

    w = sp.symbols("w")
    a1, a2, b2, b3 = (
        sp.Function(name)(w) for name in ("a1", "a2", "b2", "b3")
    )
    p2 = a2 + 1 / w
    q3 = b3 + 1 / w
    n5 = 2 * b2 * q3 - 3 * L * a1 * p2**2
    # Multiplication by w^2 clears every possible pole at w=0.
    assert not sp.cancel(w**2 * n5).has(sp.zoo)
    assert sp.denom(sp.cancel(w**2 * n5)) == 1

    c = sp.symbols("c", nonzero=True)
    h_monomial = c * w**4
    forced_n5 = sp.simplify(
        -beta * h_monomial**2
        / (5 * alpha * w**3 * sp.diff(h_monomial, w))
    )
    assert forced_n5 == -beta * c * w**2 / (20 * alpha)


def verify_pure_cusp_square_contradiction() -> None:
    p0, p1, p2, q0 = sp.symbols("p0 p1 p2 q0", nonzero=True)
    L = q0**2 / p0**3
    q1 = 3 * q0 * p1 / (2 * p0)
    q2 = 3 * q0 * p2 / (2 * p0) + 3 * q0 * p1**2 / (8 * p0**2)
    q3 = (
        3 * q0 * p1 * p2 / (4 * p0**2)
        - q0 * p1**3 / (16 * p0**3)
    )

    # These are exactly the z^1,...,z^4 coefficients of Q^2-L*P^3.
    n1 = 2 * q0 * q1 - 3 * L * p0**2 * p1
    n2 = q1**2 + 2 * q0 * q2 - 3 * L * (
        p0**2 * p2 + p0 * p1**2
    )
    n3 = 2 * q0 * q3 + 2 * q1 * q2 - L * (
        6 * p0 * p1 * p2 + p1**3
    )
    n4 = q2**2 + 2 * q1 * q3 - 3 * L * (
        p0 * p2**2 + p1**2 * p2
    )
    assert sp.simplify(n1) == 0
    assert sp.simplify(n2) == 0
    assert sp.simplify(n3) == 0
    square_identity = (
        -3 * q0**2 * (4 * p0 * p2 - p1**2) ** 2 / (64 * p0**4)
    )
    assert sp.factor(n4 - square_identity) == 0

    # In the five-block map p0=A*w^8 and p2=a2+1/w.  Since a2 is
    # polynomial, 4*p0*p2 has exact w-order 7.  No polynomial p1 can
    # have a square of that order.
    possible_square_orders = {2 * order for order in range(8)}
    assert 7 not in possible_square_orders


def verify_parametrization_degrees() -> None:
    w, v = sp.symbols("w v")
    rational_function_field = sp.QQ.frac_field(w)
    for delta in (1, 2, 4):
        a = w**8
        b = w**12 + w**delta
        common_fiber = sp.gcd(
            sp.Poly(v**8 - a, v, domain=rational_function_field),
            sp.Poly(v**12 + v**delta - b, v, domain=rational_function_field),
        )
        assert common_fiber.degree() == delta
        assert sp.expand(common_fiber.monic().as_expr() - (v**delta - w**delta)) == 0
        assert sp.degree(b**2 - a**3, w) == 12 + delta


def main() -> None:
    verify_non_cusp_five_block_solution()
    verify_cusp_coordinate_and_pole_formula()
    verify_pure_cusp_square_contradiction()
    verify_parametrization_degrees()
    print("verified an exact non-cusp five-block solution")
    print("verified the conditional cusp target-coordinate and pole formulas")
    print("verified the pure-cusp z^4 square contradiction")
    print("verified parametrization degrees delta=1,2,4 for degree pair (8,12)")
    print("RESULT: ALL ASYMPTOTIC-CURVE CHECKS PASS")


if __name__ == "__main__":
    main()
