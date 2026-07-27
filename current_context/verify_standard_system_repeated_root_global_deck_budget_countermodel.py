#!/usr/bin/env python3
"""Checks for the global repeated-root deck-budget countermodel."""

from __future__ import annotations

from itertools import product
from math import gcd

import sympy as sp


X, tau, beta = sp.symbols("X tau beta")


def homogenized_bracket(
    p: sp.Expr, q: sp.Expr, n: int, m: int
) -> sp.Expr:
    return sp.expand(
        tau
        * (
            sp.diff(p, X) * sp.diff(q, tau)
            - sp.diff(p, tau) * sp.diff(q, X)
        )
        + n * p * sp.diff(q, X)
        - m * q * sp.diff(p, X)
    )


def order_at(poly: sp.Expr, point: int) -> int:
    """Return the exact vanishing order at a rational point."""
    value = sp.expand(poly)
    order = 0
    while sp.expand(value.subs(X, point)) == 0:
        value = sp.diff(value, X)
        order += 1
    return order


def coefficient_in_tau(poly: sp.Expr, exponent: int) -> sp.Expr:
    return sp.Poly(sp.expand(poly), tau).coeff_monomial(tau**exponent)


def check_reciprocal_caps(poly: sp.Expr, total_degree: int) -> None:
    tau_poly = sp.Poly(sp.expand(poly), tau)
    for exponent in range(tau_poly.degree() + 1):
        coefficient = tau_poly.coeff_monomial(tau**exponent)
        if coefficient == 0:
            continue
        assert sp.degree(coefficient, X) <= total_degree - exponent


# The concrete saturated example.
a, b = 2, 3
g = 5
n, m = a * g, b * g
N = n + m - 2
R = X**2 * (X - 1) ** 3
L = X * (X - 1) ** 2 * (X - 2)
D = sp.expand(R + tau * L)

assert sp.degree(R, X) == g
assert sp.degree(L, X) == g - 1
assert gcd(g, gcd(2, 3)) == 1

local_data = (
    (0, 2, 1, 1, 1, 3),
    (1, 3, 1, 1, 2, 2),
)
for alpha, e, d, h, f, G in local_data:
    assert order_at(R, alpha) == e
    assert order_at(L, alpha) == e - 1
    assert e == h + f
    assert G == h * g - e * d
    assert d * e < h * g
    assert a * G > h
    assert b * G > h
    assert (a * G - h + d, b * G - h) == (a * G, b * G - 1)
    assert a * G > 0 and b * G - 1 > 0

# The global first P-layer is exactly the common-root deformation and
# saturates its reciprocal degree cap.
common_p = sp.expand(D**a)
common_q = sp.expand(D**b)
first_p = coefficient_in_tau(common_p, 1)
assert sp.expand(first_p - a * R ** (a - 1) * L) == 0
assert sp.degree(first_p, X) == n - 1
for alpha, e, *_ in local_data:
    assert order_at(first_p, alpha) == a * e - 1

check_reciprocal_caps(common_p, n)
check_reciprocal_caps(common_q, m)
assert homogenized_bracket(common_p, common_q, n, m) == 0

# Add the affine defect-one endpoint.  Its zero beta is arbitrary.
p = sp.expand(common_p + tau ** (n - 1) * (X - beta))
q = sp.expand(common_q + tau ** (m - 1))
check_reciprocal_caps(p, n)
check_reciprocal_caps(q, m)
assert sp.expand(p.subs(tau, 0) - R**a) == 0
assert sp.expand(q.subs(tau, 0) - R**b) == 0

endpoint_only = homogenized_bracket(
    tau ** (n - 1) * (X - beta),
    tau ** (m - 1),
    n,
    m,
)
assert endpoint_only == -(tau**N)

full_bracket = homogenized_bracket(p, q, n, m)
assert coefficient_in_tau(full_bracket, N) == -1
assert sp.expand(full_bracket + tau**N) != 0
assert sp.diff(X - beta, X) == 1

# The family proof is non-enumerative.  This small sanity check only
# confirms its arithmetic for repeated-root partitions of bounded g.
def repeated_partitions(total: int, minimum: int = 2) -> list[tuple[int, ...]]:
    output: list[tuple[int, ...]] = []

    def visit(remaining: int, floor: int, prefix: tuple[int, ...]) -> None:
        if remaining == 0:
            if len(prefix) >= 2:
                output.append(prefix)
            return
        for value in range(floor, remaining + 1):
            if value < minimum:
                continue
            visit(remaining - value, value, prefix + (value,))

    visit(total, minimum, ())
    return output


families_checked = 0
for g0 in range(4, 17):
    for multiplicities in repeated_partitions(g0):
        r = len(multiplicities)
        assert sum(multiplicities) == g0
        assert g0 - r <= g0 - 2
        for e0, a0 in product(multiplicities, range(2, 7)):
            d0 = h0 = 1
            k0 = 1
            f0 = e0 - 1
            G0 = g0 - e0
            assert e0 == k0 * h0 + f0
            assert d0 * e0 < h0 * g0
            assert G0 >= 2
            assert a0 * G0 > h0
        families_checked += 1

assert families_checked > 0

print("verified: saturated (2,3) repeated-root first-layer example")
print("verified: every reciprocal coefficient cap")
print("verified: both roots lie in the deep band aG > h")
print("verified: affine endpoint coefficient is exactly -tau^(n+m-2)")
print("verified: endpoint zero beta is unrestricted by the common polynomial")
print(f"verified: {families_checked} bounded family instances")
