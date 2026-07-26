#!/usr/bin/env python3
"""Exact algebra and finite-group checks for the trigonal cusp obstruction."""

from __future__ import annotations

import itertools

import sympy as sp


x, y, t = sp.symbols("x y t")

q4 = t**4 + t**2
q5 = t**5 + t**4 + t**2
q6 = t**6 + t**5 + t**4 + t**2

F4 = x**4 + 3 * x**2 * y + x**2 - y**3
F5 = (
    -x**5
    - 4 * x**4
    - 3 * x**3 * y
    - 3 * x**3
    - 3 * x**2 * y
    - x**2
    + y**3
)
F6 = (
    x**6
    - 2 * x**5
    - 3 * x**4 * y
    + x**4
    + 3 * x**3 * y
    + 3 * x**3
    + 3 * x**2 * y**2
    + 3 * x**2 * y
    + x**2
    - y**3
)


# Exact parametrizations, trigonal degree, and critical-value polynomials.
for implicit, q_polynomial in ((F4, q4), (F5, q5), (F6, q6)):
    assert sp.expand(implicit.subs({x: t**3, y: q_polynomial})) == 0
    assert sp.degree(implicit, y) == 3
    assert sp.Poly(q_polynomial, t).terms()[-1] == ((2,), 1)

assert sp.factor(sp.discriminant(F4, y)) == (
    -27 * x**4 * (x - 1) ** 2 * (x + 1) ** 2
)
node_polynomial = x**3 + 2 * x**2 + 3 * x + 1
for implicit in (F5, F6):
    assert sp.factor(sp.discriminant(implicit, y)) == (
        -27 * x**4 * node_polynomial**2
    )


# Degree six is polynomially equivalent to degree five.
assert sp.expand(q6 - q5 - t**6) == 0
assert sp.expand(F6.subs(y, y + x**2) + F5) == 0


Permutation = tuple[int, int, int, int]


def compose(first: Permutation, second: Permutation) -> Permutation:
    """Return first after second."""
    return tuple(first[second[index]] for index in range(4))


def generated_group(generators: tuple[Permutation, ...]) -> set[Permutation]:
    identity: Permutation = (0, 1, 2, 3)
    group = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            product = compose(current, generator)
            if product not in group:
                group.add(product)
                frontier.append(product)
    return group


identity: Permutation = (0, 1, 2, 3)
transpositions: list[Permutation] = []
for first in range(4):
    for second in range(first + 1, 4):
        permutation = list(identity)
        permutation[first], permutation[second] = (
            permutation[second],
            permutation[first],
        )
        transpositions.append(tuple(permutation))


def has_transitive_action(group: set[Permutation]) -> bool:
    return {
        permutation[0]
        for permutation in group
    } == {0, 1, 2, 3}


# Exhaust all transposition-valued images of the two cusp meridians.
# The braid relation leaves only a common C2 or an S3 fixing one letter.
braid_pairs: list[tuple[Permutation, Permutation]] = []
for first, second in itertools.product(transpositions, repeat=2):
    left = compose(compose(first, second), first)
    right = compose(compose(second, first), second)
    if left == right:
        braid_pairs.append((first, second))

assert len(braid_pairs) == 30
for first, second in braid_pairs:
    group = generated_group((first, second))
    assert len(group) == (2 if first == second else 6)
    assert not has_transitive_action(group)


print("verified: exact trigonal equations and vertical discriminants")
print("verified: each parametrization has local orders (3,2) at the origin")
print("verified: degree six is polynomially equivalent to degree five")
print("verified: no transposition-valued A2 cusp image is transitive in S4")
print("RESULT: THE FULL-DEGREE CUSP OBSTRUCTS CONNECTED QUARTIC MONODROMY")
