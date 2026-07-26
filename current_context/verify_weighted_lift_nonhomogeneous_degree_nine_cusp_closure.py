#!/usr/bin/env python3
"""Verify the one-step degree-nine cusp closure."""

from __future__ import annotations

import itertools

import sympy as sp

import verify_weighted_lift_first_nonlinear_cusp_subduction as cusp


def invariants(a: int, b: int, c: int) -> tuple[int, int, int]:
    beta = -2 * a - b + c
    h = 6 * a + 5 * b
    return beta, h, h + beta


def ordinary_support() -> list[tuple[int, int, int]]:
    return [
        (a, b, c)
        for total_degree in range(1, 10)
        for a in range(total_degree + 1)
        for b in range(total_degree - a + 1)
        for c in (total_degree - a - b,)
    ]


def verify_unique_degree_nine_collision() -> None:
    matrix = sp.Matrix(
        [
            [-2, -1, 1],
            [6, 5, 0],
        ]
    )
    primitive = sp.Matrix([5, -6, 4])
    assert matrix.rank() == 2
    assert matrix * primitive == sp.zeros(2, 1)
    assert primitive[0] > 0 and primitive[1] < 0
    assert sp.gcd_list(list(primitive)) == 1

    support = ordinary_support()
    collisions = []
    for left, right in itertools.combinations(support, 2):
        if invariants(*left)[:2] == invariants(*right)[:2]:
            collisions.append({left, right})
    assert collisions == [{(0, 6, 0), (5, 0, 4)}]


def verify_exact_t_atom() -> None:
    p, q = cusp.build_seed()
    first_numerator, _, lambda_zero, _ = (
        cusp.build_maximal_subductions(p, q)
    )
    assert lambda_zero != 0
    polynomial = sp.Poly(first_numerator, cusp.w, cusp.gamma)
    assert polynomial.coeff_monomial(cusp.w**25) == lambda_zero

    losses = []
    for (i, j), coefficient in polynomial.terms():
        if coefficient == 0 or (i, j) == (25, 0):
            continue
        explicit_loss = 25 - i
        gamma_loss = 25 - i - j
        assert explicit_loss >= 1
        assert gamma_loss >= 1
        losses.append((explicit_loss, gamma_loss))
    assert losses

    # No ordinary monomial has (beta,h,q)=(-6,25,19).
    assert [
        triple
        for triple in ordinary_support()
        if invariants(*triple) == (-6, 25, 19)
    ] == []


def verify_augmented_vertex_injectivity() -> None:
    # Eliminate A^5 C^4 using T.  The only old collision then vanishes.
    support = [
        triple
        for triple in ordinary_support()
        if triple != (5, 0, 4)
    ]
    regular_keys = [invariants(*triple)[:2] for triple in support]
    polar_keys = [
        (invariants(*triple)[0], invariants(*triple)[2])
        for triple in support
    ]
    assert len(regular_keys) == len(set(regular_keys))
    assert len(polar_keys) == len(set(polar_keys))
    assert (-6, 25) not in regular_keys
    assert (-6, 19) not in polar_keys


def verify_regular_t_wronskian() -> None:
    L = sp.symbols("L", integer=True, positive=True)
    degree_u = 20 + 17 * L
    degree_t = 25 + 19 * L
    coefficient = sp.expand(-5 * degree_t + 6 * degree_u)
    assert coefficient == 7 * L - 5
    # For integral L>=1 this is at least two.
    assert coefficient.subs(L, 1) == 2

    u = sp.symbols("u")
    f = sp.Function("f")(u)
    h_top = u**20 * f**17
    t_top = u**25 * f**19
    wronskian = sp.factor(
        -5 * h_top * sp.diff(t_top, u)
        + 6 * sp.diff(h_top, u) * t_top
    )
    assert wronskian == (
        u**44 * f**35 * (-5 * f + 7 * u * sp.diff(f, u))
    )


def verify_polar_t_atom() -> None:
    rho = sp.symbols("rho", integer=True, negative=True)
    beta_t, h_t, q_t = -6, 25, 19
    e_t = beta_t + rho * q_t
    recovered_h = sp.expand((1 + rho) * q_t - e_t)
    assert recovered_h == h_t

    # A same-(E,q) ordinary atom would have beta=-6 and h=25.
    for triple in ordinary_support():
        beta, h, q = invariants(*triple)
        if q == q_t:
            assert beta != beta_t
            assert h != h_t

    # The fixed first-coordinate perturbation scope remains later than U.
    alpha = -5 + 17 * rho
    for total_degree in range(1, 3):
        for a in range(total_degree + 1):
            for b in range(total_degree - a + 1):
                c = total_degree - a - b
                beta, _, q = invariants(a, b, c)
                difference = sp.expand(beta + rho * q - alpha)
                # beta>=-4, q<=8 and rho<0 make this positive.
                assert sp.expand(
                    difference
                    - ((beta + 5) + rho * (q - 17))
                ) == 0
                assert beta + 5 >= 1
                assert q - 17 <= -9


def main() -> None:
    verify_unique_degree_nine_collision()
    verify_exact_t_atom()
    verify_augmented_vertex_injectivity()
    verify_regular_t_wronskian()
    verify_polar_t_atom()
    print("verified: the sole Newton collision through degree nine")
    print("verified: exact T top, regular gap, and polar separation")
    print("verified: augmented support has singleton Newton vertices")
    print("verified: J(U,T) has nonzero regular characteristic")
    print("verified: first-coordinate perturbations of degree <=2 are later")
    print("RESULT: arbitrary nonhomogeneous target degree <=9 is obstructed")


if __name__ == "__main__":
    main()
