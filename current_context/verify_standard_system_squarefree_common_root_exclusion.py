#!/usr/bin/env python3
"""Exact checks for the squarefree common-root exclusion theorem.

These calculations verify the displayed algebra, the reciprocal degree
bookkeeping, and the finite integer argument behind the least-residual
induction.  They are not a replacement for the Newton-face proof.
"""

from __future__ import annotations

import math
from itertools import product

import sympy as sp


X, s, tau, z = sp.symbols("X s tau z")


def keller_bracket(
    first: sp.Expr,
    second: sp.Expr,
    variable: sp.Symbol,
    n: int,
    m: int,
) -> sp.Expr:
    return sp.expand(
        tau
        * (
            sp.diff(first, variable) * sp.diff(second, tau)
            - sp.diff(first, tau) * sp.diff(second, variable)
        )
        + n * first * sp.diff(second, variable)
        - m * second * sp.diff(first, variable)
    )


def verify_strict_face_identity_and_gap() -> None:
    samples = (
        (2, 3, 2, 2, 2),
        (2, 5, 3, 2, 4),
        (3, 4, 2, 3, 3),
        (3, 5, 3, 2, 2),
        (4, 7, 3, 4, 8),
    )
    for a, b, g, horizontal_drop, vertical_drop in samples:
        edge_length = math.gcd(horizontal_drop, vertical_drop)
        h_prime = horizontal_drop // edge_length
        d_prime = vertical_drop // edge_length
        if d_prime >= g * h_prime:
            continue

        A = 1 + sum(
            (index + 1) * z**index
            for index in range(1, edge_length + 1)
        )
        B = 1 + sum(
            (2 * index + 1) * z**index
            for index in range(1, b // h_prime + 1)
        )
        face_coordinate = tau**d_prime / s**h_prime
        P_face = sp.cancel(s**a * A.subs(z, face_coordinate))
        Q_face = sp.cancel(s**b * B.subs(z, face_coordinate))
        assert sp.denom(P_face) == 1
        assert sp.denom(Q_face) == 1

        actual = keller_bracket(
            sp.expand(P_face),
            sp.expand(Q_face),
            s,
            g * a,
            g * b,
        )
        expected = sp.cancel(
            (d_prime - g * h_prime)
            * s ** (a + b - 1)
            * face_coordinate
            * (
                a * A * sp.diff(B, z)
                - b * sp.diff(A, z) * B
            ).subs(z, face_coordinate)
        )
        assert sp.expand(actual - expected) == 0

        face_weight = (a + b - 1) * d_prime
        forcing_weight = h_prime * (g * (a + b) - 2)
        gap = (
            (a + b - 1) * (g * h_prime - d_prime)
            + h_prime * (g - 2)
        )
        assert forcing_weight - face_weight == gap
        assert gap > 0

    # If one face polynomial is constant, the kernel equation forces
    # the other to be constant as well.
    b0, b1, b2, a = sp.symbols("b0 b1 b2 a")
    trial_B = b0 + b1 * z + b2 * z**2
    matching_defect = sp.Poly(a * sp.diff(trial_B, z), z)
    equations = matching_defect.all_coeffs()
    solution = sp.solve(equations, (b1, b2), dict=True)
    assert solution == [{b1: 0, b2: 0}]


def verify_existing_g_sector_is_strictly_higher() -> None:
    for exponent in range(2, 10):
        for g in range(2, 8):
            for h_prime in range(1, exponent + 1):
                for d_prime in range(1, g * h_prime):
                    leading_weight = exponent * d_prime
                    for q in range(1, exponent + 1):
                        sector_weight = (
                            g * q * h_prime
                            + (exponent - q) * d_prime
                        )
                        assert (
                            sector_weight - leading_weight
                            == q * (g * h_prime - d_prime)
                        )
                        assert sector_weight > leading_weight


def reciprocal_degree_bound(
    polynomial: sp.Expr,
    total_degree: int,
) -> None:
    for (tau_order,), coefficient in sp.Poly(
        sp.expand(polynomial),
        tau,
    ).terms():
        assert sp.degree(coefficient, X) <= total_degree - tau_order


def verify_bridge_and_absorption_coefficients() -> None:
    samples = (
        (2, 2, 3),
        (3, 2, 5),
        (3, 3, 4),
        (4, 3, 5),
    )
    for g, a, b in samples:
        R = X**g + X + 1
        S_previous = R
        for e in range(1, g):
            L = X ** (g - e) + e
            S_updated = sp.expand(S_previous + tau**e * L)
            assert sp.expand(
                sp.expand(S_updated**a - S_previous**a).coeff(tau, e)
                - a * R ** (a - 1) * L
            ) == 0
            assert sp.expand(
                sp.expand(S_updated**b - S_previous**b).coeff(tau, e)
                - b * R ** (b - 1) * L
            ) == 0
            reciprocal_degree_bound(S_updated, g)
            S_previous = S_updated

        S = S_previous
        for q in range(a + 1):
            sector = sp.expand(tau ** (g * q) * S ** (a - q))
            assert sp.expand(
                sector.coeff(tau, g * q) - R ** (a - q)
            ) == 0
            reciprocal_degree_bound(sector, g * a)
        for q in range(b + 1):
            sector = sp.expand(tau ** (g * q) * S ** (b - q))
            assert sp.expand(
                sector.coeff(tau, g * q) - R ** (b - q)
            ) == 0
            reciprocal_degree_bound(sector, g * b)


def verify_truncated_degree_average() -> None:
    # h=a-min(ord(T),a) is the correct nonnegative variable.
    # Exhaustively check:
    #   j <= sum(h_alpha),  g*h_alpha <= j for every alpha
    # imply j=gq and every h_alpha=q.
    for g in range(2, 6):
        for exponent in range(2, 7):
            for h_values in product(range(exponent + 1), repeat=g):
                total_h = sum(h_values)
                for j in range(1, g * exponent + 1):
                    if j > total_h:
                        continue
                    if not all(g * h <= j for h in h_values):
                        continue
                    assert total_h == j
                    assert j % g == 0
                    q = j // g
                    assert all(h == q for h in h_values)
                    assert 1 <= q <= exponent

    # The same enumeration serves the Q-only case after replacing a by b.
    # Explicitly include raw vanishing orders above the exponent to check
    # that truncation maps all of them to h=0.
    for exponent in range(2, 8):
        for raw_order in range(exponent, exponent + 5):
            sigma = min(raw_order, exponent)
            assert sigma == exponent
            assert exponent - sigma == 0


def verify_coordinate_covariance() -> None:
    u = sp.symbols("u")
    g = 3
    n = 6
    m = 9
    S = X**g + X + 1 + tau * (X**2 + 2) + tau**2 * (X + 3)
    f = (
        u**2
        + 2 * tau * u
        + 3 * tau**2
        + tau**3 * u**2
    )
    k = (
        u**3
        - tau * u**2
        + 5 * tau**2 * u
        + 7 * tau**4
    )
    P = sp.expand(f.subs(u, S))
    Q = sp.expand(k.subs(u, S))
    bracket_in_X = keller_bracket(P, Q, X, n, m)
    bracket_in_u = keller_bracket(f, k, u, n, m)
    expected = sp.expand(sp.diff(S, X) * bracket_in_u.subs(u, S))
    assert sp.expand(bracket_in_X - expected) == 0


def verify_resonant_normal_form_has_zero_bracket() -> None:
    samples = (
        (2, 2, 3),
        (3, 2, 5),
        (4, 3, 4),
    )
    for g, a, b in samples:
        R = X**g + X + 1
        S = R + tau * (X ** (g - 1) + 2)
        if g > 2:
            S += tau**2 * (X ** (g - 2) + 3)

        A_coefficients = [sp.Integer(1)] + [
            sp.Integer(2 * q + 1) for q in range(1, a + 1)
        ]
        B_coefficients = [sp.Integer(1)] + [
            sp.Integer(3 * q + 2) for q in range(1, b + 1)
        ]
        P = sp.expand(
            sum(
                A_coefficients[q]
                * tau ** (g * q)
                * S ** (a - q)
                for q in range(a + 1)
            )
        )
        Q = sp.expand(
            sum(
                B_coefficients[q]
                * tau ** (g * q)
                * S ** (b - q)
                for q in range(b + 1)
            )
        )
        reciprocal_degree_bound(P, g * a)
        reciprocal_degree_bound(Q, g * b)
        assert keller_bracket(P, Q, X, g * a, g * b) == 0


def main() -> None:
    verify_strict_face_identity_and_gap()
    verify_existing_g_sector_is_strictly_higher()
    verify_bridge_and_absorption_coefficients()
    verify_truncated_degree_average()
    verify_coordinate_covariance()
    verify_resonant_normal_form_has_zero_bracket()
    print("verified: strict compact-face bracket identity and forcing gap")
    print("verified: existing g-sectors lie above every strict face")
    print("verified: bridge shifts and scalar absorptions preserve degree bounds")
    print("verified: truncated multiplicity averaging forces uniform g-sectors")
    print("verified: the bracket is covariant under tau-dependent root changes")
    print("verified: every exact resonant normal form has zero bracket")


if __name__ == "__main__":
    main()
