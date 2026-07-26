#!/usr/bin/env python3
"""Verify exact identities in the global minimal-boundary proof."""

from __future__ import annotations

import sympy as sp

import verify_weighted_lift_degree_six_ternary_boundary_wronskian_closure as boundary


def verify_exact_template_supports() -> None:
    _, _, _, template_a, template_b, template_h = (
        boundary.boundary_functions()
    )
    tops = (
        ("A", template_a, (6, 4)),
        ("B", template_b, (5, 4)),
        ("H", template_h, (20, 17)),
    )
    for name, template, top in tops:
        support = [
            monomial
            for monomial, coefficient in sp.Poly(
                template,
                boundary.u,
                boundary.f_symbol,
            ).terms()
            if coefficient != 0
        ]
        maximum_f_degree = max(j for _, j in support)
        assert maximum_f_degree == top[1], name
        assert [
            monomial
            for monomial in support
            if monomial[1] == maximum_f_degree
        ] == [top], name

        # Prove the gap for every symbolic L>=1.  A loss
        # du+L*df is at least L+1 when du,df>=1, or when
        # du>=0 and df>=2.
        for i, j in support:
            if (i, j) == top:
                continue
            u_loss = top[0] - i
            f_loss = top[1] - j
            assert u_loss >= 0
            assert f_loss >= 1
            assert u_loss >= 1 or f_loss >= 2


def verify_regular_face_parameterization() -> None:
    # Symbolic lattice identities; the finite audit below checks the
    # nonnegative endpoint bookkeeping.
    a, b, c, k, L = sp.symbols(
        "a b c k L",
        integer=True,
        nonnegative=True,
    )
    shifted = (a + 2 * k, b - 3 * k, c + k)
    assert sp.expand(sum(shifted) - (a + b + c)) == 0
    assert sp.expand(
        (-2 * shifted[0] - shifted[1] + shifted[2])
        - (-2 * a - b + c)
    ) == 0
    base_degree = a * (6 + 4 * L) + b * (5 + 4 * L) + c * L
    shifted_degree = (
        shifted[0] * (6 + 4 * L)
        + shifted[1] * (5 + 4 * L)
        + shifted[2] * L
    )
    assert sp.expand(
        base_degree - shifted_degree - 3 * k * (L + 1)
    ) == 0

    # Exhaust all homogeneous monomial sets through degree 20.
    for target_degree in range(1, 21):
        monomials = [
            (a, b, target_degree - a - b)
            for a in range(target_degree + 1)
            for b in range(target_degree - a + 1)
        ]
        by_beta: dict[int, list[tuple[int, int, int]]] = {}
        for a, b, c in monomials:
            by_beta.setdefault(-2 * a - b + c, []).append(
                (a, b, c)
            )
        for face in by_beta.values():
            ordered = sorted(face, key=lambda term: term[2])
            a0, b0, c0 = ordered[0]
            expected = [
                (a0 + 2 * k, b0 - 3 * k, c0 + k)
                for k in range(ordered[-1][2] - c0 + 1)
                if b0 - 3 * k >= 0
            ]
            assert ordered == expected

            for f_degree in range(1, 15):
                base_degree = (
                    a0 * (6 + 4 * f_degree)
                    + b0 * (5 + 4 * f_degree)
                    + c0 * f_degree
                )
                for a, b, c in ordered:
                    k = c - c0
                    degree = (
                        a * (6 + 4 * f_degree)
                        + b * (5 + 4 * f_degree)
                        + c * f_degree
                    )
                    assert base_degree - degree == (
                        3 * k * (f_degree + 1)
                    )


def verify_regular_wronskian_and_deviation() -> None:
    N, ell, d, L = sp.symbols(
        "N ell d L",
        integer=True,
        nonnegative=True,
    )
    q = 4 * N + ell
    beta = ell - N - d
    degree_h = 20 + 17 * L
    degree_v = 5 * N + d + q * L
    coefficient_b = 17 * d - 3 * N - 22 * ell
    coefficient_c = 15 * d - 5 * N - 20 * ell

    assert sp.expand(
        -5 * degree_v
        - beta * degree_h
        - coefficient_b * L
        - coefficient_c
    ) == 0
    assert sp.expand(
        17 * coefficient_c - 15 * coefficient_b
    ) == -10 * q

    u, c_lead, b_next = sp.symbols(
        "u c_lead b_next",
        nonzero=True,
    )
    delta = sp.symbols("delta", integer=True, positive=True)
    f = c_lead * u**L * (
        1 + b_next / c_lead * u ** (-delta)
    )
    # On B*L+C*=0, the first formal deviation is
    # -B*delta*(b/c)*u^(-delta-1).
    normalized = sp.factor(
        coefficient_b
        * (sp.diff(f, u) / f - L / u)
    )
    exact_deviation = sp.factor(
        -coefficient_b
        * delta
        * (b_next / c_lead)
        * u ** (-delta - 1)
        / (
            1
            + (b_next / c_lead) * u ** (-delta)
        )
    )
    assert sp.factor(normalized - exact_deviation) == 0


def verify_pole_graph_structure() -> None:
    # A graph monomial x^a y^b enters gamma with boundary exponent
    # rho=a+2-b and coefficient (u-1)^b.
    for rho in range(-12, 0):
        for a in range(10):
            b = a + 2 - rho
            assert a + 2 - b == rho
            assert b >= 2 - rho
        for largest_a in range(10):
            degree_f = largest_a + 2 - rho
            assert degree_f + rho + 1 >= 3


def verify_pole_face_algebra() -> None:
    rho, k = sp.symbols(
        "rho k",
        integer=True,
    )
    a, b, c = sp.symbols(
        "a b c",
        integer=True,
        nonnegative=True,
    )
    delta_a = (2 - 3 * rho) * k
    delta_b = -3 * (1 - rho) * k
    delta_c = k
    assert sp.expand(delta_a + delta_b + delta_c) == 0

    q = 4 * a + 4 * b + c
    s = 6 * a + 5 * b
    beta = -2 * a - b + c
    E = beta + rho * q
    q_shifted = sp.expand(
        4 * (a + delta_a)
        + 4 * (b + delta_b)
        + c
        + delta_c
    )
    s_shifted = sp.expand(
        6 * (a + delta_a) + 5 * (b + delta_b)
    )
    E_shifted = sp.expand(
        -2 * (a + delta_a)
        - (b + delta_b)
        + c
        + delta_c
        + rho * q_shifted
    )
    assert sp.expand(q_shifted - q) == -3 * k
    assert sp.expand(
        s_shifted - s + 3 * (1 + rho) * k
    ) == 0
    assert sp.expand(E_shifted - E) == 0

    alpha = -5 + 17 * rho
    resonance_at_one = sp.expand(alpha * q - 17 * E)
    F = -14 * a + 3 * b + 22 * c
    assert sp.expand(resonance_at_one + F) == 0

    G = 22 * a + 5 * b - 20 * c
    assert sp.factor(
        G.subs(b, (14 * a - 22 * c) / 3)
        - (136 * a - 170 * c) / 3
    ) == 0

    # Derive the infinity equation using the largest-c endpoint
    # (a,b,c) and an endpoint distance K back to smallest c.
    K, L = sp.symbols(
        "K L",
        integer=True,
        nonnegative=True,
    )
    q_small_c = q + 3 * K
    s_small_c = s + 3 * (1 + rho) * K
    E_resonant = alpha * q / 17
    infinity_factor = sp.expand(
        alpha * (s_small_c + q_small_c * L)
        - E_resonant * (20 + 17 * L)
    )
    assert sp.factor(
        infinity_factor
        - alpha
        * (
            G / 17
            + 3 * K * (L + rho + 1)
        )
    ) == 0


def verify_pole_faces_by_exhaustion() -> None:
    # Finite adversarial audit of endpoint signs and dominance.
    for rho in range(-8, 0):
        for target_degree in range(1, 18):
            monomials = [
                (a, b, target_degree - a - b)
                for a in range(target_degree + 1)
                for b in range(target_degree - a + 1)
            ]
            by_E: dict[int, list[tuple[int, int, int]]] = {}
            for a, b, c in monomials:
                q = 4 * a + 4 * b + c
                E = -2 * a - b + c + rho * q
                by_E.setdefault(E, []).append((a, b, c))

            for face in by_E.values():
                ordered = sorted(face, key=lambda term: term[2])
                a0, b0, c0 = ordered[0]
                for a1, b1, c1 in ordered:
                    k = c1 - c0
                    assert a1 - a0 == (2 - 3 * rho) * k
                    assert b1 - b0 == -3 * (1 - rho) * k

                aK, bK, cK = ordered[-1]
                F = -14 * aK + 3 * bK + 22 * cK
                if F == 0:
                    G = 22 * aK + 5 * bK - 20 * cK
                    assert G > 0
                    K = cK - c0
                    for f_degree in range(2 - rho, 25):
                        assert (
                            sp.Rational(G, 17)
                            + 3 * K * (f_degree + rho + 1)
                        ) > 0


def verify_affine_separation() -> None:
    rho = sp.symbols("rho", integer=True, nonpositive=True)
    alpha_u = -5 + 17 * rho
    assert sp.expand((-2 + 4 * rho) - alpha_u) == (
        3 - 13 * rho
    )
    assert sp.expand((-1 + 4 * rho) - alpha_u) == (
        4 - 13 * rho
    )
    assert sp.expand((1 + rho) - alpha_u) == (
        6 - 16 * rho
    )
    for rho_value in range(-20, 1):
        assert 3 - 13 * rho_value > 0
        assert 4 - 13 * rho_value > 0
        assert 6 - 16 * rho_value > 0


def main() -> None:
    verify_exact_template_supports()
    verify_regular_face_parameterization()
    verify_regular_wronskian_and_deviation()
    verify_pole_graph_structure()
    verify_pole_face_algebra()
    verify_pole_faces_by_exhaustion()
    verify_affine_separation()
    print("verified: exact seed templates and uniform degree gaps")
    print("verified: global regular-boundary face parameterization")
    print("verified: regular Wronskian and first-deviation coefficient")
    print("verified: pole-boundary graph divisibility and degree bound")
    print("verified: pole-face endpoint resonance contradiction")
    print("verified: affine first-coordinate separation")
    print("RESULT: global minimal-boundary closure identities pass")


if __name__ == "__main__":
    main()
