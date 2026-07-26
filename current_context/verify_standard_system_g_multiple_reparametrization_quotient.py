#!/usr/bin/env python3
"""Exact checks for the g-multiple approximate-root quotient."""

from __future__ import annotations

import sympy as sp


def truncate(expression: sp.Expr, variable: sp.Symbol, order: int) -> sp.Expr:
    return sp.series(expression, variable, 0, order).removeO().expand()


def verify_group_invariant_and_slice() -> None:
    # These are units in an arbitrary truncated characteristic-zero
    # coefficient algebra.  The calculation is independent of the
    # truncation order and of the induced compositional change z -> z/phi.
    A, B, phi = sp.symbols("A B phi", nonzero=True)
    a, b = sp.symbols("a b", integer=True, positive=True)
    transformed_A = A / phi**a
    transformed_B = B / phi**b
    assert sp.cancel(
        transformed_B**a / transformed_A**b - B**a / A**b
    ) == 0

    # On the A=1 slice, phi=A^(1/a), and the surviving normal form is
    # B*A^(-b/a).  Test the exact rational-exponent identity.
    normal_phi = A ** (sp.Rational(1, 3))
    normal_A = sp.powdenest(A / normal_phi**3, force=True)
    normal_B = sp.powdenest(B / normal_phi**5, force=True)
    assert normal_A == 1
    assert sp.powdenest(normal_B - B * A ** (-sp.Rational(5, 3)), force=True) == 0

    # A tangent-to-the-identity composition preserves the order and
    # leading coefficient of the relative unit.
    z, kappa, c2 = sp.symbols("z kappa c2")
    relative = 1 + kappa * z**3 + c2 * z**4
    new_argument = z + sp.Symbol("d2") * z**2 + sp.Symbol("d3") * z**3
    composed = truncate(relative.subs(z, new_argument), z, 5)
    assert sp.expand(composed - 1).coeff(z, 1) == 0
    assert sp.expand(composed - 1).coeff(z, 2) == 0
    assert sp.expand(composed - 1).coeff(z, 3) == kappa


def verify_degree_bound_countermodel() -> None:
    X, tau, r1, r0, kappa = sp.symbols("X tau r1 r0 kappa")
    g, a, b = 3, 2, 5
    n, m = g * a, g * b
    R = X**g + r1 * X + r0

    for c in range(1, a + 1):
        P = sp.Poly(
            sp.expand(R**a + kappa * tau ** (g * c) * R ** (a - c)),
            X,
            tau,
        )
        coefficient = sp.Poly(P.as_expr(), tau).coeff_monomial(
            tau ** (g * c)
        )
        assert sp.Poly(coefficient, X).degree() == n - g * c

        z = sp.symbols("z")
        relative = truncate((1 + kappa * z**c) ** (-b), z, c + 2)
        assert relative.coeff(z, c) == -b * kappa

    Q = sp.Poly(R**b, X, tau)
    assert Q.degree(X) == m
    assert Q.degree(tau) == 0

    # If both pure powers after a simultaneous polynomial
    # reparametrization obey their reciprocal bounds, the polynomial
    # phi has degree at most one: deg(phi^a)=a*deg(phi)<=a.
    degree_phi = sp.symbols("degree_phi", integer=True, nonnegative=True)
    assert sp.solve_univariate_inequality(
        a * degree_phi <= a,
        degree_phi,
    ) == (degree_phi <= 1)


def triangular_zero_sector_normalizer(
    a: int,
    b: int,
    c: int,
    maximum: int,
) -> tuple[list[sp.Expr], sp.Expr]:
    """Construct the unique mu_q in the triangular identity."""

    z, kappa = sp.symbols("z kappa")
    coefficients: list[sp.Expr] = [sp.Integer(1)]
    partial = truncate((1 + kappa * z**c) ** sp.Rational(b, a), z, maximum + 1)
    for q in range(1, maximum + 1):
        current = sp.expand(partial).coeff(z, q)
        mu_q = -current
        coefficients.append(sp.factor(mu_q))
        partial = truncate(
            partial
            + mu_q
            * z**q
            * (1 + kappa * z**c) ** sp.Rational(b - q, a),
            z,
            maximum + 1,
        )
    return coefficients, sp.expand(partial)


def verify_triangular_parameter_presentation() -> None:
    for a, b, c in ((2, 3, 1), (2, 3, 2), (3, 5, 1), (3, 5, 3)):
        maximum = a + b - 1
        coefficients, normalized = triangular_zero_sector_normalizer(
            a,
            b,
            c,
            maximum,
        )
        assert coefficients[0] == 1
        assert normalized == 1


def verify_relative_log_transport() -> None:
    X, tau = sp.symbols("X tau")
    a, b, g = sp.symbols("a b g", integer=True, positive=True)
    P = sp.Function("P")(X, tau)
    Q = sp.Function("Q")(X, tau)
    ell = a * sp.log(Q) - b * sp.log(P)

    original_scaled = sp.expand(
        a
        * (
            tau
            * (
                sp.diff(P, X) * sp.diff(Q, tau)
                - sp.diff(P, tau) * sp.diff(Q, X)
            )
            + g * a * P * sp.diff(Q, X)
            - g * b * Q * sp.diff(P, X)
        )
        / (P * Q)
    )
    transport = sp.expand(
        tau
        * (
            sp.diff(P, X) / P * sp.diff(ell, tau)
            - sp.diff(P, tau) / P * sp.diff(ell, X)
        )
        + a * g * sp.diff(ell, X)
    )
    assert sp.simplify(original_scaled - transport) == 0

    # The first relative coefficient and the endpoint residue equation.
    R = sp.Function("R")(X)
    d, kappa = sp.symbols("d kappa")
    first = kappa * R ** (-d / g)
    assert sp.simplify(
        g * R * sp.diff(first, X) + d * sp.diff(R, X) * first
    ) == 0

    W = sp.Function("W")(X)
    N = g * (a + b) - 2
    endpoint_unknown = W / R ** (a + b)
    endpoint_left = sp.factor(
        g * R * sp.diff(endpoint_unknown, X)
        + N * sp.diff(R, X) * endpoint_unknown
    )
    endpoint_expected = (
        g * R * sp.diff(W, X) - 2 * sp.diff(R, X) * W
    ) / R ** (a + b)
    assert sp.simplify(endpoint_left - endpoint_expected) == 0


def main() -> None:
    verify_group_invariant_and_slice()
    verify_degree_bound_countermodel()
    verify_triangular_parameter_presentation()
    verify_relative_log_transport()
    print("verified: exact approximate-root action and relative-unit invariant")
    print("verified: canonical one-sided slice and degree-bound countermodel")
    print("verified: triangular zero-sector parameter presentation")
    print("verified: linear relative-log transport and endpoint ODE")


if __name__ == "__main__":
    main()
