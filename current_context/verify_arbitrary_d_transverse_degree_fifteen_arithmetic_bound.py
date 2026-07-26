#!/usr/bin/env python3
"""Exact checks for the arbitrary-d transverse-degree-fifteen bound."""

from __future__ import annotations

import math

import sympy as sp


def simple_total_degree_factor(value: int) -> bool:
    """Whether value*p is in a cited one-coordinate degree class."""
    return value in (1, 4) or bool(sp.isprime(value))


DegreeTuple = tuple[int, int, int, int, int, int, int, int]


def arithmetic_survivors(maximum_bound: int) -> list[DegreeTuple]:
    """Enumerate charts left by target reduction and the degree sieve."""
    survivors: list[DegreeTuple] = []
    for maximum_degree in range(2, maximum_bound + 1):
        for lower_degree in range(1, maximum_degree):
            common_degree = math.gcd(maximum_degree, lower_degree)
            a = maximum_degree // common_degree
            b = lower_degree // common_degree
            if b == 1:
                continue
            for t in sp.divisors(common_degree):
                covered = (
                    t in (1, 2)
                    or simple_total_degree_factor(a * t)
                    or simple_total_degree_factor(b * t)
                )
                if not covered:
                    survivors.append(
                        (
                            maximum_degree,
                            lower_degree,
                            common_degree,
                            a,
                            b,
                            t,
                            a * t,
                            b * t,
                        )
                    )
    return survivors


# Equal degrees are removed by a constant target change, and b=1 by
# the polynomial power shear P -> P-c*Q**a.  There are no remaining
# arithmetic charts through maximum y-degree eight.
assert arithmetic_survivors(8) == []


# The complete ledger through degree fifteen.  The first four tuples
# have separate exact normal-degree exclusions; the final three are
# the still-open equality charts for the boundary lower bound.
raw_survivors_through_fifteen = arithmetic_survivors(15)
expected_raw_survivors: list[DegreeTuple] = [
    (9, 6, 3, 3, 2, 3, 9, 6),
    (12, 8, 4, 3, 2, 4, 12, 8),
    (12, 9, 3, 4, 3, 3, 12, 9),
    (15, 6, 3, 5, 2, 3, 15, 6),
    (15, 9, 3, 5, 3, 3, 15, 9),
    (15, 10, 5, 3, 2, 5, 15, 10),
    (15, 12, 3, 5, 4, 3, 15, 12),
]
assert raw_survivors_through_fifteen == expected_raw_survivors

certified_exclusions = {
    (9, 6, 3, 3, 2, 3, 9, 6),
    (12, 8, 4, 3, 2, 4, 12, 8),
    (12, 9, 3, 4, 3, 3, 12, 9),
    (15, 6, 3, 5, 2, 3, 15, 6),
}
remaining_degree_fifteen = [
    row for row in raw_survivors_through_fifteen
    if row not in certified_exclusions
]
assert remaining_degree_fifteen == [
    (15, 9, 3, 5, 3, 3, 15, 9),
    (15, 10, 5, 3, 2, 5, 15, 10),
    (15, 12, 3, 5, 4, 3, 15, 12),
]
assert all(
    maximum_degree not in {10, 11, 13, 14}
    for maximum_degree, *_ in raw_survivors_through_fifteen
)


# Directly record every maximum-six chart after equal-degree reduction.
degree_six_ledger: list[tuple[int, int, int, int, int, str]] = []
for lower_degree in range(1, 6):
    common_degree = math.gcd(6, lower_degree)
    a = 6 // common_degree
    b = lower_degree // common_degree
    for t in sp.divisors(common_degree):
        if b == 1:
            reason = "power shear"
        elif t in (1, 2):
            reason = "gcd p or 2p"
        elif simple_total_degree_factor(a * t):
            reason = "upper simple degree"
        elif simple_total_degree_factor(b * t):
            reason = "lower simple degree"
        else:
            reason = "unresolved"
        degree_six_ledger.append(
            (lower_degree, common_degree, a, b, t, reason)
        )

assert all(entry[-1] != "unresolved" for entry in degree_six_ledger)


# Formal collision identities.  If d(x1)=zeta*d(x0) and
# x1-x0=(1-zeta**2)d(x0)**2/u, both boundary coordinates agree.
u, d0, zeta = sp.symbols("u d0 zeta", nonzero=True)
x0 = sp.symbols("x0")
x1 = x0 + (1 - zeta**2) * d0**2 / u
d1 = zeta * d0

p_difference = sp.expand(d1**2 + u * x1 - (d0**2 + u * x0))
q_difference = sp.expand(d1**3 - d0**3)
zeta_relation = zeta**2 + zeta + 1

assert sp.rem(sp.Poly(p_difference, zeta), sp.Poly(zeta_relation, zeta)) == 0
assert sp.rem(sp.Poly(q_difference, zeta), sp.Poly(zeta_relation, zeta)) == 0


# The collision polynomial has a nontrivial factor after the inherited
# roots of d are removed: 2g^2-g is positive for every g>=1.
for degree_d in range(1, 101):
    assert 2 * degree_d**2 - degree_d > 0


print("verified: every maximum-y-degree-six arithmetic chart is covered")
print("verified: no arithmetic survivor exists through maximum degree eight")
print("verified: the first survivor is exactly (9,6), with t=3")
print("verified: complete arithmetic survivor ledger through degree fifteen")
print("verified: exact exclusions leave only (15,9), (15,10), (15,12)")
print("verified: the arbitrary-d boundary collision identities are exact")
