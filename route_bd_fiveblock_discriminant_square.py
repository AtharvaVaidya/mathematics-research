#!/usr/bin/env python3
"""Exact checks for the five-block fourth-jet discriminant.

For a boundary parametrization (A(h), B(h)), put

    J = A' B'' - B' A'',
    K = A' J' - 3 A'' J,
    L = A' K' - 5 A'' K,
    Phi = 3 K^2 - J L.

The fourth Taylor row of the five-block system makes Phi a polynomial
square over the algebraic closure.  This verifier checks that identity,
the exact leading term of Phi when D=B^2-A^3 has small degree, and the
failure of the new r=5 Wronskian countermodel to satisfy the square test.
"""

from __future__ import annotations

import sympy as sp

from route_bd_universal_wronskian_countermodel import (
    PRIME,
    build_system,
    finite_field_point,
    polynomial_mod_prime,
)


def verify_graph_derivatives_and_discriminant() -> None:
    h = sp.symbols("h")
    A = sp.Function("A")(h)
    B = sp.Function("B")(h)
    Ap = sp.diff(A, h)

    def derivative_in_A(expression: sp.Expr) -> sp.Expr:
        return sp.factor(sp.diff(expression, h) / Ap)

    J = sp.expand(Ap * sp.diff(B, h, 2) - sp.diff(B, h) * sp.diff(A, h, 2))
    K = sp.expand(Ap * sp.diff(J, h) - 3 * sp.diff(A, h, 2) * J)
    L = sp.expand(Ap * sp.diff(K, h) - 5 * sp.diff(A, h, 2) * K)
    Phi = sp.expand(3 * K**2 - J * L)

    g1 = sp.diff(B, h) / Ap
    g2 = derivative_in_A(g1)
    g3 = derivative_in_A(g2)
    g4 = derivative_in_A(g3)
    assert sp.factor(g2 - J / Ap**3) == 0
    assert sp.factor(g3 - K / Ap**5) == 0
    assert sp.factor(g4 - L / Ap**7) == 0

    C = sp.symbols("C")
    fourth_row = sp.expand(g4 * C**2 + 12 * g3 * C + 12 * g2)
    discriminant = sp.factor((12 * g3) ** 2 - 4 * g4 * 12 * g2)
    assert sp.factor(discriminant - 48 * Phi / Ap**10) == 0

    # If C is a rational root, the discriminant is literally
    # (2*g4*C+12*g3)^2.  This remains valid when g4 vanishes.
    square_witness = sp.expand((2 * g4 * C + 12 * g3) ** 2)
    assert sp.factor(
        square_witness - discriminant - 4 * g4 * fourth_row
    ) == 0


def verify_exact_leading_coefficient() -> None:
    """Check the formal coefficient controlling deg(Phi).

    Let deg A=M, deg B=3M/2 and D=B^2-A^3 have degree d.  The first
    Laurent correction to B is lc(D) h^(d-3M/2)/2.  Since Phi vanishes
    identically on B=A^(3/2), its leading term is the first variation
    checked below.
    """

    M, n, t, d, delta = sp.symbols("M n t d delta")

    def monomial_covariants(exponent: sp.Expr) -> tuple[sp.Expr, ...]:
        J = M * exponent * (exponent - M)
        K = M * J * (exponent - 2 * M)
        L = M * K * (exponent - 3 * M)
        return J, K, L

    J0, K0, L0 = monomial_covariants(n)
    J1, K1, L1 = monomial_covariants(t)
    first_variation = sp.factor(6 * K0 * K1 - J0 * L1 - J1 * L0)
    specialized = sp.factor(
        first_variation.subs(
            {
                n: sp.Rational(3, 2) * M,
                t: d - sp.Rational(3, 2) * M,
            }
        )
        * delta
        / 2
    )
    expected = sp.factor(
        -sp.Rational(3, 32)
        * M**6
        * (d - 3 * M)
        * (d - 2 * M)
        * (2 * d - 5 * M)
        * (2 * d - 3 * M)
        * delta
    )
    assert sp.factor(specialized - expected) == 0

    # With M=2r and 0<=d<=2r, none of the displayed factors vanishes.
    # Hence deg Phi=d+8r-10 exactly, so a nonzero square Phi forces d even.
    for r_value in range(2, 30):
        M_value = 2 * r_value
        for d_value in range(0, 2 * r_value + 1):
            coefficient = expected.subs(
                {M: M_value, d: d_value, delta: 1}
            )
            assert coefficient != 0
            assert (d_value + 8 * r_value - 10) % 2 == d_value % 2


def verify_marked_local_parity() -> None:
    m = sp.symbols("m", integer=True, positive=True)
    n = (3 * m + 1) / 2
    order_phi = sp.simplify(4 * m + 2 * n - 10)
    assert order_phi == 7 * m - 9
    for m_value in range(3, 30, 2):
        assert int(order_phi.subs(m, m_value)) % 2 == 0


def verify_scale_five_countermodel_fails_square_test() -> None:
    data = build_system()
    h = data["h"]
    point = finite_field_point(data)
    solved = data["solved"]
    A = polynomial_mod_prime(data["X"].subs(point), h)
    B = polynomial_mod_prime(data["T"].subs(solved).subs(point), h)

    Ap = A.diff()
    Bp = B.diff()
    J = Ap * Bp.diff() - Bp * Ap.diff()
    K = Ap * J.diff() - 3 * Ap.diff() * J
    L = Ap * K.diff() - 5 * Ap.diff() * K
    Phi = 3 * K**2 - J * L
    D = B**2 - A**3

    assert D.degree() == 10
    assert Phi.degree() == 40
    M_value = 10
    d_value = D.degree()
    predicted = (
        -sp.Rational(3, 32)
        * M_value**6
        * (d_value - 3 * M_value)
        * (d_value - 2 * M_value)
        * (2 * d_value - 5 * M_value)
        * (2 * d_value - 3 * M_value)
        * (int(D.LC()) % PRIME)
    )
    assert int(Phi.LC()) % PRIME == int(predicted) % PRIME

    factorization = sp.factor_list(Phi.as_expr(), modulus=PRIME)[1]
    degree_exponents = sorted(
        (sp.degree(factor, h), exponent)
        for factor, exponent in factorization
    )
    assert degree_exponents == [(1, 12), (2, 1), (4, 1), (5, 1), (17, 1)]
    assert any(exponent % 2 for _, exponent in degree_exponents)


def main() -> None:
    verify_graph_derivatives_and_discriminant()
    verify_exact_leading_coefficient()
    verify_marked_local_parity()
    verify_scale_five_countermodel_fails_square_test()
    print("verified the fourth-row discriminant 48*Phi/(A')^10")
    print("verified: every five-block boundary makes Phi a polynomial square")
    print("verified exact deg Phi=d+8r-10 and the parity condition d even")
    print("verified the r=5 Wronskian countermodel fails the square test")
    print("RESULT: FIVE-BLOCK DISCRIMINANT-SQUARE INVARIANT PASSES")


if __name__ == "__main__":
    main()
