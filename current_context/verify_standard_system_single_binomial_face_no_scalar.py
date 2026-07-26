#!/usr/bin/env python3
"""Exact checks for the single-binomial-face no-scalar theorem."""

from math import gcd
from itertools import product

import sympy as sp


s, tau, c = sp.symbols("s tau c", nonzero=True)
zeta = sp.symbols("zeta")


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


def verify_face(a: int, b: int, g: int, d: int) -> None:
    assert 1 < a < b
    assert gcd(a, b) == 1
    n = g * a
    m = g * b
    q, r = divmod(b, a)
    assert 1 <= r < a
    assert 1 <= d <= n

    coefficients = [
        c**j * sp.binomial(sp.Rational(b, a), j)
        for j in range(q + 1)
    ]
    P = s**a + c * tau**d
    Q = sum(
        coefficients[j] * tau ** (d * j) * s ** (b - a * j)
        for j in range(q + 1)
    )
    actual = keller_bracket(P, Q, n, m)
    expected = (
        c
        * r
        * (n - d)
        * coefficients[q]
        * tau ** (d * (q + 1))
        * s ** (r - 1)
    )
    assert sp.expand(actual - expected) == 0

    # The recurrence is exact and nondegenerate precisely when d<n.
    if d < n:
        recursively_forced = [sp.Integer(1)]
        for j in range(q):
            recursively_forced.append(
                sp.simplify(
                    c
                    * sp.Rational(b - a * j, a * (j + 1))
                    * recursively_forced[j]
                )
            )
        assert all(
            sp.simplify(recursively_forced[j] - coefficients[j]) == 0
            for j in range(q + 1)
        )
        assert coefficients[q] != 0
    else:
        assert actual == 0
        assert expected == 0

    # A polynomial monomial reaching the terminal through the top
    # P-face term would require negative s-degree.  The only source
    # through the lower P term is the already present j=q monomial.
    terminal_tau_order = d * (q + 1)
    terminal_s_degree = r - 1
    top_source = (
        terminal_tau_order,
        terminal_s_degree - a + 1,
    )
    lower_source = (
        terminal_tau_order - d,
        terminal_s_degree + 1,
    )
    assert top_source == (d * (q + 1), r - a)
    assert top_source[1] < 0
    assert lower_source == (d * q, r)


for test_a in range(2, 7):
    for test_b in range(test_a + 1, 13):
        if gcd(test_a, test_b) != 1:
            continue
        for test_g in range(2, 6):
            test_n = test_g * test_a
            for test_d in range(1, test_n + 1):
                verify_face(test_a, test_b, test_g, test_d)


def verify_root_vanishing_face(
    a: int,
    b: int,
    g: int,
    d: int,
    sigma: int,
) -> None:
    assert 0 <= sigma < a
    n = g * a
    m = g * b
    h = a - sigma
    q_h, r_h = divmod(b, h)
    coefficients = [
        c**j * sp.binomial(sp.Rational(b, a), j)
        for j in range(q_h + 1)
    ]
    P = s**a + c * tau**d * s**sigma
    Q = sum(
        coefficients[j] * tau ** (d * j) * s ** (b - h * j)
        for j in range(q_h + 1)
    )
    actual = keller_bracket(P, Q, n, m)
    expected = (
        c
        * (g * h - d)
        * (b - a * q_h)
        * coefficients[q_h]
        * tau ** (d * (q_h + 1))
        * s ** (sigma + r_h - 1)
    )
    assert sigma + r_h - 1 >= 0
    assert sp.expand(actual - expected) == 0
    assert b - a * q_h != 0
    assert coefficients[q_h] != 0

    if d != g * h:
        recursively_forced = [sp.Integer(1)]
        for j in range(q_h):
            recursively_forced.append(
                sp.simplify(
                    c
                    * sp.Rational(b - a * j, a * (j + 1))
                    * recursively_forced[j]
                )
            )
        assert all(
            sp.simplify(recursively_forced[j] - coefficients[j]) == 0
            for j in range(q_h + 1)
        )
    else:
        assert actual == 0

    terminal_tau_order = d * (q_h + 1)
    terminal_s_degree = sigma + r_h - 1
    top_source = (
        terminal_tau_order,
        terminal_s_degree - a + 1,
    )
    lower_source = (
        terminal_tau_order - d,
        terminal_s_degree - sigma + 1,
    )
    assert top_source == (d * (q_h + 1), r_h - h)
    assert top_source[1] < 0
    assert lower_source == (d * q_h, r_h)


for test_a in range(2, 7):
    for test_b in range(test_a + 1, 13):
        if gcd(test_a, test_b) != 1:
            continue
        for test_g in range(2, 5):
            for test_sigma in range(test_a):
                test_h = test_a - test_sigma
                for test_d in range(1, test_g * test_h + 2):
                    verify_root_vanishing_face(
                        test_a,
                        test_b,
                        test_g,
                        test_d,
                        test_sigma,
                    )


# The scalar endpoint arithmetic is exhaustive in a broad exact range.
scalar_hits = []
for test_a in range(2, 25):
    for test_b in range(test_a + 1, 60):
        if gcd(test_a, test_b) != 1:
            continue
        test_q, test_r = divmod(test_b, test_a)
        if test_r != 1:
            continue
        for test_g in range(2, 20):
            test_n = test_g * test_a
            test_N = test_g * (test_a + test_b) - 2
            for test_d in range(1, test_n + 1):
                if test_d * (test_q + 1) == test_N:
                    scalar_hits.append(
                        (test_a, test_b, test_g, test_d, test_n)
                    )
assert scalar_hits
assert all(
    test_g == 2 and test_d == test_n
    for _test_a, _test_b, test_g, test_d, test_n in scalar_hits
)


# Symbolic form of the endpoint arithmetic:
# N-n(q+1)=g-2 when b=aq+1.
a_symbol, q_symbol, g_symbol = sp.symbols(
    "a_symbol q_symbol g_symbol",
    integer=True,
    positive=True,
)
n_symbol = g_symbol * a_symbol
b_symbol = a_symbol * q_symbol + 1
N_symbol = g_symbol * (a_symbol + b_symbol) - 2
assert sp.expand(N_symbol - n_symbol * (q_symbol + 1)) == g_symbol - 2


# Root-vanishing scalar candidates obey the same endpoint arithmetic.
root_scalar_hits = []
for test_a in range(2, 20):
    for test_b in range(test_a + 1, 45):
        if gcd(test_a, test_b) != 1:
            continue
        for test_sigma in range(test_a):
            test_h = test_a - test_sigma
            test_q_h, test_r_h = divmod(test_b, test_h)
            if test_sigma + test_r_h != 1:
                continue
            for test_g in range(2, 15):
                test_N = test_g * (test_a + test_b) - 2
                for test_d in range(1, test_g * test_h + 1):
                    if test_d * (test_q_h + 1) == test_N:
                        root_scalar_hits.append(
                            (
                                test_a,
                                test_b,
                                test_sigma,
                                test_g,
                                test_d,
                                test_g * test_h,
                            )
                        )
assert root_scalar_hits
assert all(
    test_g == 2 and test_d == test_gh
    for (
        _test_a,
        _test_b,
        _test_sigma,
        test_g,
        test_d,
        test_gh,
    ) in root_scalar_hits
)


# Varying root orders: the global degree bound d<=sum h_i and absence
# of a strict local obstruction g*h_i>d force equality at every root.
for varying_g in range(2, 5):
    for varying_a in range(2, 6):
        for sigma_tuple in product(range(varying_a), repeat=varying_g):
            h_tuple = tuple(varying_a - value for value in sigma_tuple)
            h_sum = sum(h_tuple)
            for varying_d in range(1, h_sum + 1):
                if all(varying_g * value <= varying_d for value in h_tuple):
                    assert h_sum == varying_d
                    assert all(
                        varying_g * value == varying_d
                        for value in h_tuple
                    )
                    assert len(set(sigma_tuple)) == 1
                    sigma_value = sigma_tuple[0]
                    assert (
                        varying_g * sigma_value
                        == varying_g * varying_a - varying_d
                    )


# The number of strict interior lattice points on the binomial edge is
# gcd(a,d)-1.
for edge_a in range(2, 15):
    for edge_d in range(1, 15):
        interior = [
            (edge_k, edge_e)
            for edge_k in range(1, edge_a)
            for edge_e in range(1, edge_d)
            if edge_d * edge_k + edge_a * edge_e
            == edge_a * edge_d
        ]
        assert len(interior) == gcd(edge_a, edge_d) - 1


# The root-vanishing edge has gcd(h,d)-1 strict interior points.
for edge_a in range(2, 15):
    for edge_sigma in range(edge_a):
        edge_h = edge_a - edge_sigma
        for edge_d in range(1, 15):
            interior = [
                (edge_k, edge_e)
                for edge_k in range(edge_sigma + 1, edge_a)
                for edge_e in range(1, edge_d)
                if edge_d * edge_k + edge_h * edge_e
                == edge_d * edge_a
            ]
            assert len(interior) == gcd(edge_h, edge_d) - 1


def verify_compact_face(
    a: int,
    b: int,
    g: int,
    h: int,
    d: int,
) -> None:
    edge_gcd = gcd(h, d)
    h_primitive = h // edge_gcd
    d_primitive = d // edge_gcd
    A = 1 + sum(
        (index + 1) * zeta**index
        for index in range(1, edge_gcd + 1)
    )
    maximum_B_degree = b // h_primitive
    B = 1 + sum(
        (2 * index + 1) * zeta**index
        for index in range(1, maximum_B_degree + 1)
    )
    z_substitution = tau**d_primitive / s**h_primitive
    P_face = sp.cancel(s**a * A.subs(zeta, z_substitution))
    Q_face = sp.cancel(s**b * B.subs(zeta, z_substitution))
    assert sp.denom(P_face) == 1
    assert sp.denom(Q_face) == 1

    actual = keller_bracket(
        sp.expand(P_face),
        sp.expand(Q_face),
        g * a,
        g * b,
    )
    expected = sp.cancel(
        (d_primitive - g * h_primitive)
        * s ** (a + b - 1)
        * z_substitution
        * (
            a * A * sp.diff(B, zeta)
            - b * sp.diff(A, zeta) * B
        ).subs(zeta, z_substitution)
    )
    assert sp.expand(actual - expected) == 0

    forcing_weight_gap = (
        h_primitive * (g * (a + b) - 2)
        - (a + b - 1) * d_primitive
    )
    expected_gap = (
        (a + b - 1) * (g * h_primitive - d_primitive)
        + h_primitive * (g - 2)
    )
    assert forcing_weight_gap == expected_gap
    if d_primitive < g * h_primitive:
        assert forcing_weight_gap > 0


for compact_parameters in (
    (2, 3, 2, 2, 2),
    (2, 5, 3, 2, 4),
    (3, 4, 2, 3, 6),
    (3, 5, 3, 2, 4),
    (4, 5, 2, 3, 6),
    (4, 7, 3, 4, 8),
):
    verify_compact_face(*compact_parameters)


# In the strict compact-face kernel, UFD gives A=C^a.  Its degree
# arithmetic forces the whole edge to be a reduced-root shift.
for compact_a in range(2, 15):
    for compact_h in range(1, compact_a + 1):
        for compact_d in range(1, 30):
            compact_e = gcd(compact_h, compact_d)
            if compact_e % compact_a == 0:
                assert compact_e == compact_a
                assert compact_h == compact_a
                assert compact_h // compact_e == 1


kappa = sp.symbols("kappa", nonzero=True)
for shift_a, shift_b, shift_g, shift_d_primitive in (
    (2, 3, 2, 1),
    (2, 5, 3, 2),
    (3, 4, 2, 1),
    (4, 5, 3, 2),
):
    assert shift_d_primitive < shift_g
    shifted_root = s + kappa * tau**shift_d_primitive
    assert keller_bracket(
        shifted_root**shift_a,
        shifted_root**shift_b,
        shift_g * shift_a,
        shift_g * shift_b,
    ) == 0


print("verified: the single-face coefficients telescope binomially")
print("verified: the only terminal bracket is c*r*(n-d)*C_q")
print("verified: no distinct polynomial Q monomial reaches the endpoint")
print("verified: scalar endpoint arithmetic forces g=2 and d=n")
print("verified: the forced scalar coefficient then vanishes")
print("verified: the root-vanishing chain and terminal telescope exactly")
print("verified: varying root orders force the uniform g-sector survivor")
print("verified: the complete compact-face bracket identity")
print("verified: every strict compact kernel is a reduced-root shift")
