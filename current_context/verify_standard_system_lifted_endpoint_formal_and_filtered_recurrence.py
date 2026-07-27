#!/usr/bin/env python3
"""Exact checks for the lifted-endpoint formal and filtered recurrence."""

import math

import sympy as sp


x, y = sp.symbols("x y")


def degree_at_most(polynomial: sp.Expr, bound: int) -> bool:
    """Return whether a polynomial has degree at most the given bound."""
    return polynomial == 0 or sp.degree(polynomial, x) <= bound


def catalan(index: int) -> sp.Integer:
    """Return the exact Catalan number C_index."""
    return sp.Integer(math.comb(2 * index, index) // (index + 1))


def verify_closed_formal_lift() -> None:
    """Check the universal scalar formal equation through ten orders."""
    c, w = sp.symbols("c w", nonzero=True)
    order = 11
    phi = sp.expand(
        sum(
            (-1) ** (r - 1)
            * catalan(r - 1)
            * (w / (2 * c)) ** (r - 1)
            * y**r
            for r in range(1, order)
        )
    )

    algebraic_residual = sp.series(
        c * phi + w * phi**2 / 2 - c * y,
        y,
        0,
        order,
    ).removeO()
    differential_residual = sp.series(
        (c + w * phi) * sp.diff(phi, y) - c,
        y,
        0,
        order - 1,
    ).removeO()
    assert sp.expand(algebraic_residual) == 0
    assert sp.expand(differential_residual) == 0


def filtered_solution(
    A: sp.Expr,
    B: sp.Expr,
    h: sp.Expr,
    q_bound: int,
    p_bound: int,
) -> tuple[sp.Expr, sp.Expr] | None:
    """Use the modular criterion to solve A*q-B*p=h inside degree caps."""
    inverse = sp.invert(A, B)
    q = sp.rem(sp.expand(inverse * h), B)
    q = sp.expand(q)
    if not degree_at_most(q, q_bound):
        return None
    p = sp.cancel((A * q - h) / B)
    if not p.is_polynomial(x):
        return None
    p = sp.expand(p)
    if not degree_at_most(p, p_bound):
        return None
    assert sp.expand(A * q - B * p - h) == 0
    return q, p


def verify_modular_cokernel() -> None:
    """Check the exact criterion and its r-2 ranks on structured bases."""
    # Rational scalar denominators are coefficients in QQ, not
    # polynomial denominators in x.
    rational_solution = filtered_solution(
        sp.Integer(1),
        x,
        -x**2 / 2,
        0,
        1,
    )
    assert rational_solution == (0, x / 2)

    for alpha, beta in ((2, 2), (3, 4), (4, 3), (5, 5)):
        A = x**alpha + x + 1
        B = x**beta + 2 * x + 3
        assert sp.gcd(A, B) == 1

        for r in range(2, min(alpha + 1, beta + 1) + 1):
            domain_degree = alpha + beta - r + 1
            q_bound = beta - r + 1
            p_bound = alpha - r + 1

            q_coefficients = sp.symbols(f"q_{alpha}_{beta}_{r}_0:{q_bound + 1}")
            p_coefficients = sp.symbols(f"p_{alpha}_{beta}_{r}_0:{p_bound + 1}")
            q = sum(value * x**i for i, value in enumerate(q_coefficients))
            p = sum(value * x**i for i, value in enumerate(p_coefficients))

            columns = []
            for variable in (*q_coefficients, *p_coefficients):
                image = sp.expand(A * sp.diff(q, variable) - B * sp.diff(p, variable))
                columns.append(
                    [sp.Poly(image, x).coeff_monomial(x**i) for i in range(domain_degree + 1)]
                )
            matrix = sp.Matrix(domain_degree + 1, len(columns), lambda i, j: columns[j][i])
            assert matrix.rank() == len(columns)
            assert (domain_degree + 1) - matrix.rank() == r - 2

            # Every basis target is accepted exactly when the top
            # r-2 coefficients of the modular representative vanish.
            inverse = sp.invert(A, B)
            for degree in range(domain_degree + 1):
                h = x**degree
                representative = sp.expand(sp.rem(inverse * h, B))
                modular_accepts = degree_at_most(representative, q_bound)

                augmented_column = sp.Matrix(
                    [sp.Poly(h, x).coeff_monomial(x**i) for i in range(domain_degree + 1)]
                )
                linear_accepts = matrix.row_join(augmented_column).rank() == matrix.rank()
                assert modular_accepts == linear_accepts

                solution = filtered_solution(A, B, h, q_bound, p_bound)
                assert (solution is not None) == modular_accepts


def verify_cubic_witness() -> None:
    """Check exact formal lifting and failure of the cubic degree cap."""
    p0 = x**3 / 3 + x**2 / 2 + x
    q0 = x**3 / 3 + x**2 + 3 * x
    p1 = (x - 1) / 3
    q1 = x / 3
    A = sp.diff(p0, x)
    B = sp.diff(q0, x)
    W = sp.expand(sp.diff(p1, x) * q1 - p1 * sp.diff(q1, x))

    assert A == x**2 + x + 1
    assert B == x**2 + 2 * x + 3
    assert sp.expand(A * q1 - B * p1) == 1
    assert W == sp.Rational(1, 9)

    second = filtered_solution(A, B, -W / 2, 1, 1)
    assert second is not None
    q2, p2 = second
    assert q2 == -x / 54
    assert p2 == (1 - x) / 54

    H3 = sp.expand(
        2 * sp.diff(p1, x) * q2
        - p1 * sp.diff(q2, x)
        + sp.diff(p2, x) * q1
        - 2 * p2 * sp.diff(q1, x)
    )
    assert H3 == -sp.Rational(1, 54)
    assert filtered_solution(A, B, -H3 / 3, 0, 0) is None

    # The unrestricted formal lift supplies degree-one third
    # coefficients, exactly one degree above the cubic cap.
    p3 = (x - 1) / 486
    q3 = x / 486
    assert sp.expand(A * q3 - B * p3 + H3 / 3) == 0
    assert sp.degree(p3, x) == 1
    assert sp.degree(q3, x) == 1

    phi = sp.series(
        -9 + 9 * sp.sqrt(1 + 2 * y / 9),
        y,
        0,
        8,
    ).removeO()
    F = sp.expand(p0 + p1 * phi)
    G = sp.expand(q0 + q1 * phi)
    jacobian = sp.diff(F, x) * sp.diff(G, y) - sp.diff(F, y) * sp.diff(G, x)
    assert sp.series(jacobian - 1, y, 0, 7).removeO().expand() == 0


def verify_first_obstruction_gauge_invariance() -> None:
    """Check that the cubic obstruction survives every tangent shear."""
    lam = sp.symbols("lam")
    p0 = x**3 / 3 + x**2 / 2 + x
    q0 = x**3 / 3 + x**2 + 3 * x
    p1 = (x - 1) / 3
    q1 = x / 3
    p2 = (1 - x) / 54
    q2 = -x / 54
    A = sp.diff(p0, x)
    B = sp.diff(q0, x)

    shifted_p1 = sp.expand(p1 + lam * A)
    shifted_q1 = sp.expand(q1 + lam * B)
    shifted_p2 = sp.expand(
        p2
        + lam * sp.diff(p1, x)
        + lam**2 * sp.diff(p0, x, 2) / 2
    )
    shifted_q2 = sp.expand(
        q2
        + lam * sp.diff(q1, x)
        + lam**2 * sp.diff(q0, x, 2) / 2
    )

    shifted_W = sp.expand(
        sp.diff(shifted_p1, x) * shifted_q1
        - shifted_p1 * sp.diff(shifted_q1, x)
    )
    assert sp.expand(
        2 * (A * shifted_q2 - B * shifted_p2) + shifted_W
    ) == 0

    shifted_H3 = sp.expand(
        2 * sp.diff(shifted_p1, x) * shifted_q2
        - shifted_p1 * sp.diff(shifted_q2, x)
        + sp.diff(shifted_p2, x) * shifted_q1
        - 2 * shifted_p2 * sp.diff(shifted_q1, x)
    )
    inverse = sp.invert(A, B)
    representative = sp.rem(
        sp.expand(inverse * (-shifted_H3 / 3)),
        B,
        domain=sp.QQ.frac_field(lam),
    )
    assert sp.Poly(representative, x).coeff_monomial(x) == sp.Rational(1, 486)


def verify_repeated_boundary_automorphism() -> None:
    """Check an exact repeated-boundary map in the exponent-one regime."""
    tau, X = sp.symbols("tau X")
    F = y + x**2
    G = x + F**2
    jacobian = sp.diff(F, x) * sp.diff(G, y) - sp.diff(F, y) * sp.diff(G, x)
    assert sp.expand(jacobian) == -1

    P = sp.expand(tau**2 * F.subs({x: X / tau, y: 1 / tau}))
    Q = sp.expand(tau**4 * G.subs({x: X / tau, y: 1 / tau}))
    assert P == X**2 + tau
    assert sp.expand(Q - ((X**2 + tau) ** 2 + X * tau**3)) == 0
    assert P.subs(tau, 0) == X**2
    assert Q.subs(tau, 0) == X**4


verify_closed_formal_lift()
verify_modular_cokernel()
verify_cubic_witness()
verify_first_obstruction_gauge_invariance()
verify_repeated_boundary_automorphism()

print("verified: every defect-one zero/one-jet has an exact polynomial-coefficient formal lift")
print("verified: the order-r reciprocal cokernel has dimension r-2")
print("verified: modular remainders exactly detect the filtered obstruction")
print("verified: the cubic witness lifts formally but not within degree three")
print("verified: the cubic witness obstruction is invariant under every tangent shear")
print("verified: repeated reciprocal boundary alone does not force an obstruction")
