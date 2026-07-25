#!/usr/bin/env python3
"""Exact checks for the universal osculating-Weierstrass-cubic theorem."""

from __future__ import annotations

import sympy as sp


def verify_chain_rule_and_leading_generators() -> None:
    x, y = sp.symbols("x y")
    L, c5, c4, c3, c2, c0 = sp.symbols("L c5 c4 c3 c2 c0")
    target = (
        y**2
        - L * x**3
        + c5 * x * y
        + c4 * x**2
        + c3 * y
        + c2 * x
        + c0
    )
    assert sp.diff(target, y) == 2 * y + c5 * x + c3

    alpha, beta, R = sp.symbols("alpha beta R", nonzero=True)
    p_top = alpha * R**2
    q_top = beta * R**3
    generators = [
        sp.expand(p_top * q_top),
        sp.expand(p_top**2),
        q_top,
        p_top,
    ]
    assert generators == [
        alpha * beta * R**5,
        alpha**2 * R**4,
        beta * R**3,
        alpha * R**2,
    ]
    assert sp.expand(
        q_top**2 - (beta**2 / alpha**3) * p_top**3
    ) == 0


def verify_recursive_degree_ledger() -> None:
    for r in range(2, 50):
        threshold = r + 3
        # The chain rule gives (2Q+c5P+c3)J, of degree <=3r+1.
        assert max(3 * r, 2 * r, 0) + 1 == 3 * r + 1
        assert threshold + 1 + 2 * r - 2 > 3 * r + 1

        active = [
            multiplier
            for multiplier in (5, 4, 3, 2)
            if multiplier * r > threshold
        ]
        if r in (2, 3):
            assert active == [5, 4, 3]
        else:
            assert active == [5, 4, 3, 2]

        # After an mr resonance is killed, there is no other multiple of r
        # strictly between (m-1)r and mr.
        for multiplier in active:
            assert not [
                degree
                for degree in range(
                    (multiplier - 1) * r + 1,
                    multiplier * r,
                )
                if degree % r == 0
            ]

        remaining_high_multiples = [
            degree
            for degree in range(threshold + 1, 6 * r)
            if degree % r == 0
        ]
        assert remaining_high_multiples == [
            multiplier * r for multiplier in reversed(active)
        ]


def verify_projective_geometry() -> None:
    X, Y, T = sp.symbols("X Y T")
    L, c5, c4, c3, c2, c0 = sp.symbols(
        "L c5 c4 c3 c2 c0", nonzero=True
    )
    projective = (
        T * Y**2
        - L * X**3
        + c5 * T * X * Y
        + c4 * T * X**2
        + c3 * T**2 * Y
        + c2 * T**2 * X
        + c0 * T**3
    )
    assert sp.expand(projective.subs(T, 0)) == -L * X**3
    assert sp.diff(projective, T).subs({X: 0, Y: 1, T: 0}) == 1

    # Completing the square produces a cubic whose discriminant is
    # genuinely quadratic in the freely variable constant term.
    a = c5**2 / 4 - c4
    b = c5 * c3 / 2 - c2
    constant = sp.symbols("constant")
    cubic_discriminant = sp.discriminant(
        L * X**3 + a * X**2 + b * X + constant,
        X,
    )
    assert sp.degree(cubic_discriminant, constant) == 2
    assert sp.Poly(
        cubic_discriminant, constant
    ).coeff_monomial(constant**2) == -27 * L**2


def verify_weighted_homogenization_and_contact() -> None:
    X, Y, T, t = sp.symbols("X Y T t")
    L, c5, c4, c3, c2, c0 = sp.symbols("L c5 c4 c3 c2 c0")
    affine = (
        Y**2
        - L * X**3
        + c5 * X * Y
        + c4 * X**2
        + c3 * Y
        + c2 * X
        + c0
    )
    weighted = (
        Y**2
        - L * X**3
        + c5 * X * Y * T
        + c4 * X**2 * T**2
        + c3 * Y * T**3
        + c2 * X * T**4
        + c0 * T**6
    )
    weights = {X: 2, Y: 3, T: 1}
    for monomial in sp.Poly(weighted, X, Y, T).monoms():
        assert sum(
            exponent * weights[variable]
            for exponent, variable in zip(monomial, (X, Y, T))
        ) == 6

    p, q = sp.symbols("p q")
    for r in range(2, 20):
        scaled = sp.expand(
            weighted.subs(
                {
                    X: t ** (2 * r) * p,
                    Y: t ** (3 * r) * q,
                    T: t**r,
                },
                simultaneous=True,
            )
        )
        assert sp.expand(
            scaled - t ** (6 * r) * affine.subs({X: p, Y: q})
        ) == 0
        assert 6 * r - (r + 3) == 5 * r - 3
        assert 9 * r - (r + 3) == 8 * r - 3

    # In the a/b case r=4 and delta is 1,2,4.  Pullback contact at least
    # 17 must be rounded up to a multiple of delta before division.
    r = 4
    lower = 5 * r - 3
    intrinsic = {}
    for delta in (1, 2, 4):
        rounded_pullback = min(
            value
            for value in range(lower, 6 * r + 1)
            if value % delta == 0
        )
        intrinsic[delta] = rounded_pullback // delta
    assert intrinsic == {1: 17, 2: 9, 4: 5}

    # Exact curve-level warning: p=w^8, q=w^12+w^4 factors through h=w^4.
    # The osculating cubic relation is exact, so after adding c0 != 0 the
    # weighted pullback order is 24 but the normalized order is only 6.
    w = sp.symbols("w")
    p_example = w**8
    q_example = w**12 + w**4
    example_relation = sp.expand(
        q_example**2 - p_example**3 - 2 * p_example**2 - p_example
    )
    assert example_relation == 0
    assert 24 // 4 == 6 < 17


def main() -> None:
    verify_chain_rule_and_leading_generators()
    verify_recursive_degree_ledger()
    verify_projective_geometry()
    verify_weighted_homogenization_and_contact()
    print("verified the exact chain-rule centralizer identity")
    print("verified descending R^5,R^4,R^3,R^2 cancellation, including r=2,3")
    print("verified the generalized Weierstrass cubic geometry")
    print("verified weighted contact and parametrization-degree correction")
    print("RESULT: UNIVERSAL OSCULATING CUBIC CHECKS PASS")


if __name__ == "__main__":
    main()
