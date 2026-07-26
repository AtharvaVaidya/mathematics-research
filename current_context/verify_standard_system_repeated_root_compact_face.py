#!/usr/bin/env python3
"""Exact checks for strict compact faces at a repeated common root."""

import math

import sympy as sp


s, tau, z = sp.symbols("s tau z")


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


def verify_general_coset(
    a: int,
    b: int,
    g: int,
    multiplicity: int,
    h_primitive: int,
    d_primitive: int,
    u: int,
    v: int,
) -> None:
    p = a * multiplicity
    q = b * multiplicity
    n = g * a
    m = g * b
    A = 1 + 2 * z + 3 * z**2
    B = 1 + 5 * z + 7 * z**2
    z_substitution = tau**d_primitive / s**h_primitive
    P_face = s**p * A.subs(z, z_substitution)
    Q_coset = (
        tau**u
        * s**v
        * B.subs(z, z_substitution)
    )
    weight = h_primitive * u + d_primitive * v
    gamma = sp.Rational(g, multiplicity)
    delta = d_primitive - gamma * h_primitive
    radial_defect = u + gamma * v - m
    expected = (
        tau**u
        * s ** (p + v - 1)
        * (
            p * radial_defect * A * B
            + p * delta * z * A * sp.diff(B, z)
            + (m * h_primitive - weight)
            * z
            * sp.diff(A, z)
            * B
        ).subs(z, z_substitution)
    )
    actual = keller_bracket(P_face, Q_coset, n, m)
    assert sp.cancel(actual - expected) == 0

    matched_Q = s**q * B.subs(z, z_substitution)
    matched_expected = (
        delta
        * s ** (p + q - 1)
        * z
        * (
            p * A * sp.diff(B, z)
            - q * sp.diff(A, z) * B
        )
    ).subs(z, z_substitution)
    matched_actual = keller_bracket(
        P_face,
        matched_Q,
        n,
        m,
    )
    assert sp.cancel(matched_actual - matched_expected) == 0


for parameters in (
    (2, 3, 5, 2, 1, 2, 1, 0),
    (3, 4, 5, 4, 9, 11, 2, 1),
    (2, 5, 7, 3, 2, 3, 4, 2),
    (3, 5, 8, 5, 3, 4, 5, 4),
):
    verify_general_coset(*parameters)


# Every zero-Euler-defect Q coset at a strict slope has weight at
# least that of the matched s^q face.
for test_g in range(2, 15):
    for test_e in range(2, test_g + 1):
        gamma = sp.Rational(test_g, test_e)
        for test_b in range(2, 10):
            test_q = test_b * test_e
            for test_h in range(1, 8):
                for test_d in range(1, 20):
                    if math.gcd(test_d, test_h) != 1:
                        continue
                    if not sp.Rational(test_d, test_h) < gamma:
                        continue
                    matched_weight = test_q * test_d
                    for test_v in range(test_q + 1):
                        candidate_u = gamma * (test_q - test_v)
                        if candidate_u.q != 1:
                            continue
                        candidate_weight = (
                            test_h * int(candidate_u)
                            + test_d * test_v
                        )
                        assert candidate_weight >= matched_weight


# In every strict forcing-weight coincidence, local polynomiality
# leaves the Wronskian at least one degree short of the scalar.
coincidences = []
for test_g in range(2, 80):
    for test_e in range(2, test_g + 1):
        for test_a in range(2, 16):
            for test_b in range(test_a + 1, 24):
                if math.gcd(test_a, test_b) != 1:
                    continue
                total = test_a + test_b
                forcing_order = test_g * total - 2
                local_exponent = test_e * total - 1
                common_divisor = math.gcd(
                    forcing_order,
                    local_exponent,
                )
                d_primitive = forcing_order // common_divisor
                h_primitive = local_exponent // common_divisor
                strict = (
                    sp.Rational(d_primitive, h_primitive)
                    < sp.Rational(test_g, test_e)
                )
                assert strict == (2 * test_e > test_g)
                if not strict:
                    continue
                assert (2 * test_e - test_g) % common_divisor == 0
                assert math.gcd(common_divisor, test_e) == 1
                assert math.gcd(h_primitive, test_e) == 1
                assert common_divisor < test_e
                assert h_primitive > total
                p = test_a * test_e
                q = test_b * test_e
                max_A_degree = p // h_primitive
                max_B_degree = q // h_primitive
                assert (
                    max_A_degree + max_B_degree
                    == common_divisor - 1
                )
                assert (
                    max_A_degree + max_B_degree - 1
                    <= common_divisor - 2
                )
                coincidences.append(
                    (
                        test_g,
                        test_e,
                        test_a,
                        test_b,
                        common_divisor,
                        d_primitive,
                        h_primitive,
                        max_A_degree,
                        max_B_degree,
                    )
                )


# The first locally nonconstant coincidence is the exact near-miss
# (g,e,a,b)=(5,4,3,4).
locally_nonconstant = [
    data
    for data in coincidences
    if data[-2] >= 1
]
assert locally_nonconstant[0] == (5, 4, 3, 4, 3, 11, 9, 1, 1)

coefficient_A, coefficient_B = sp.symbols(
    "coefficient_A coefficient_B"
)
A_near_miss = 1 + coefficient_A * z
B_near_miss = 1 + coefficient_B * z
near_miss_wronskian = sp.expand(
    12 * A_near_miss * sp.diff(B_near_miss, z)
    - 16 * sp.diff(A_near_miss, z) * B_near_miss
)
assert sp.degree(z * near_miss_wronskian, z) <= 2
assert sp.expand(z * near_miss_wronskian).coeff(z, 3) == 0


# Common local-factor deformations make the strict face bracket
# vanish identically.
factor_C = 1 + 2 * z + 3 * z**2
A_common = factor_C**2
B_common = factor_C**3
common_wronskian = sp.expand(
    4 * A_common * sp.diff(B_common, z)
    - 6 * sp.diff(A_common, z) * B_common
)
assert common_wronskian == 0


print("verified: the repeated-root general Q-coset bracket")
print("verified: the matched compact Wronskian formula")
print("verified: zero-defect lower Q faces are impossible")
print("verified: every strict scalar coincidence is one degree short")
print("verified: the first local coincidence is (5,4,3,4)")
print("verified: common local-factor powers kill the strict face")
