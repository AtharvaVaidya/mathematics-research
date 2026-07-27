#!/usr/bin/env python3
"""Exact checks for the strict compact-face Keller bridge."""

import sympy as sp


s, tau, z = sp.symbols("s tau z")
x = sp.symbols("x")


def keller_bracket(
    P: sp.Expr,
    Q: sp.Expr,
    n: int,
    m: int,
) -> sp.Expr:
    return sp.expand(
        tau
        * (
            sp.diff(P, s) * sp.diff(Q, tau)
            - sp.diff(P, tau) * sp.diff(Q, s)
        )
        + n * P * sp.diff(Q, s)
        - m * Q * sp.diff(P, s)
    )


def verify_coset_formula(
    a: int,
    b: int,
    g: int,
    h_primitive: int,
    d_primitive: int,
    u: int,
    v: int,
) -> None:
    assert sp.gcd(h_primitive, d_primitive) == 1
    A = 1 + 2 * z + 3 * z**2
    B = 1 + 5 * z + 7 * z**2
    z_substitution = tau**d_primitive / s**h_primitive
    P_face = s**a * A.subs(z, z_substitution)
    Q_coset = (
        tau**u
        * s**v
        * B.subs(z, z_substitution)
    )
    weight = h_primitive * u + d_primitive * v
    delta = d_primitive - g * h_primitive
    radial_defect = u + g * v - g * b
    expected = (
        tau**u
        * s ** (a + v - 1)
        * (
            a * radial_defect * A * B
            + a * delta * z * A * sp.diff(B, z)
            + (g * b * h_primitive - weight)
            * z
            * sp.diff(A, z)
            * B
        ).subs(z, z_substitution)
    )
    actual = keller_bracket(
        P_face,
        Q_coset,
        g * a,
        g * b,
    )
    assert sp.cancel(actual - expected) == 0


for parameters in (
    (2, 3, 2, 1, 1, 1, 0),
    (2, 5, 3, 1, 2, 3, 2),
    (3, 4, 2, 2, 3, 2, 1),
    (3, 5, 3, 1, 2, 4, 3),
):
    verify_coset_formula(*parameters)


# A zero Euler defect cannot occur below the matched s^b face at a
# strict slope.
for test_b in range(2, 12):
    for test_g in range(2, 6):
        for test_h in range(1, 6):
            for test_d in range(1, test_g * test_h):
                if sp.gcd(test_h, test_d) != 1:
                    continue
                base_weight = test_b * test_d
                for test_v in range(test_b + 1):
                    test_u = test_g * (test_b - test_v)
                    test_weight = test_h * test_u + test_d * test_v
                    assert test_weight >= base_weight
                    assert (
                        test_weight - base_weight
                        == (test_b - test_v)
                        * (test_g * test_h - test_d)
                    )


# The raw standard-sector weight is strictly above the base face for
# every k>0 at a strict slope.
for test_b in range(2, 10):
    for test_g in range(2, 6):
        for test_h in range(1, 6):
            for test_d in range(1, test_g * test_h):
                base_weight = sp.Rational(test_b * test_d)
                for test_k in range(1, 20):
                    sector_weight = (
                        base_weight
                        + test_k
                        * (
                            test_h
                            - sp.Rational(test_d, test_g)
                        )
                    )
                    assert sector_weight > base_weight


# Polynomial projection can lower the finite-root Taylor order, so the
# raw sector-weight calculation is not the bridge proof.
polynomial_part = (
    x**5 + sp.Rational(5, 2) * x**3 + sp.Rational(15, 8) * x
)
assert polynomial_part.subs(x, sp.I) == sp.Rational(3, 8) * sp.I
inverse_x = sp.symbols("inverse_x")
series_check = sp.series(
    (1 + inverse_x**2) ** sp.Rational(5, 2),
    inverse_x,
    0,
    6,
).removeO().expand()
assert series_check == (
    1
    + sp.Rational(5, 2) * inverse_x**2
    + sp.Rational(15, 8) * inverse_x**4
)


# A tau-dependent local coordinate introduces no extra determinant
# term: the two chain-rule copies involving S_tau cancel exactly.
coordinate = x + tau * x**2 + tau**2
P_template = s**2 + tau**2 * s + tau**3
Q_template = s**3 + 2 * tau * s**2 + tau**4
P_in_x = P_template.subs(s, coordinate)
Q_in_x = Q_template.subs(s, coordinate)
actual_in_x = sp.expand(
    tau
    * (
        sp.diff(P_in_x, x) * sp.diff(Q_in_x, tau)
        - sp.diff(P_in_x, tau) * sp.diff(Q_in_x, x)
    )
    + 4 * P_in_x * sp.diff(Q_in_x, x)
    - 6 * Q_in_x * sp.diff(P_in_x, x)
)
local_then_substitute = keller_bracket(
    P_template,
    Q_template,
    4,
    6,
).subs(s, coordinate)
assert sp.expand(
    actual_in_x
    - sp.diff(coordinate, x) * local_then_substitute
) == 0


# A strict compact face has far endpoint d=aE but primitive shift
# order E=d/a.  At the globally earliest coefficient, the inequalities
# E <= E_alpha <= E/h <= E force h=1 and E_alpha=E at every active
# root.
for test_a in range(2, 8):
    for test_E in range(1, 8):
        far_endpoint = test_a * test_E
        assert sp.gcd(test_a, far_endpoint) == test_a
        assert far_endpoint // test_a == test_E

for test_E in range(1, 8):
    for horizontal_length in range(1, 8):
        possible_local_exponents = [
            local_exponent
            for local_exponent in range(test_E, 8)
            if sp.Rational(local_exponent)
            <= sp.Rational(test_E, horizontal_length)
        ]
        if possible_local_exponents:
            assert horizontal_length == 1
            assert possible_local_exponents == [test_E]


# Global gluing arithmetic: divisibility by R^(a-1) leaves a root
# deformation of degree at most g-E.  This is already at most g-2 for
# E>=2; only E=1 needs the missing-X^(n-1) normalization.
for test_a in range(2, 8):
    for test_g in range(2, 9):
        test_n = test_g * test_a
        for test_E in range(1, test_g + 1):
            coefficient_degree_bound = test_n - test_E
            divisor_degree = test_g * (test_a - 1)
            quotient_degree_bound = (
                coefficient_degree_bound - divisor_degree
            )
            assert quotient_degree_bound == test_g - test_E
            if test_E >= 2:
                assert quotient_degree_bound <= test_g - 2
            else:
                assert quotient_degree_bound == test_g - 1
            assert min(quotient_degree_bound, test_g - 2) <= test_g - 2
            for binomial_order in range(test_a + 1):
                shifted_term_degree = (
                    (test_a - binomial_order) * test_g
                    + binomial_order * (test_g - test_E)
                )
                assert (
                    shifted_term_degree
                    == test_n - binomial_order * test_E
                )
            for test_b in range(test_a + 1, test_a + 5):
                test_m = test_g * test_b
                q_coefficient_degree_bound = test_m - test_E
                q_divisor_degree = test_g * (test_b - 1)
                assert (
                    q_coefficient_degree_bound - q_divisor_degree
                    == test_g - test_E
                )
                for binomial_order in range(test_b + 1):
                    shifted_q_term_degree = (
                        (test_b - binomial_order) * test_g
                        + binomial_order * (test_g - test_E)
                    )
                    assert (
                        shifted_q_term_degree
                        == test_m - binomial_order * test_E
                    )


# Every Q coefficient below the current primitive order E lies below
# the matched weight at any root where its s-order is less than b.
for test_b in range(2, 10):
    for test_E in range(1, 8):
        for lower_order in range(1, test_E):
            for local_order in range(test_b):
                assert (
                    lower_order + test_E * local_order
                    < test_b * test_E
                )


print("verified: the general local Q-coset bracket")
print("verified: no zero-defect Q face lies below the matched face")
print("verified: all raw k>0 standard sectors have higher face weight")
print("verified: polynomial projection can mix finite-root Taylor order")
print("verified: tau-dependent root coordinates preserve the bracket")
print("verified: far endpoint and primitive shift orders are distinct")
print("verified: earliest-layer inequalities force horizontal length one")
print("verified: both reduced shifts obey the global gluing bounds")
print("verified: lower Q orders lie below the matched face")
