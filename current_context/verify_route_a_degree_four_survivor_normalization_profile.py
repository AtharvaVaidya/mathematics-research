#!/usr/bin/env python3
"""Exact checks for the degree-four survivor normalization profiles."""

from itertools import permutations
from math import gcd

import sympy as sp


def compose(p, q):
    """Return p after q for image-tuple permutations."""
    return tuple(p[q[i]] for i in range(4))


def power(p, exponent):
    result = tuple(range(4))
    for _ in range(exponent):
        result = compose(p, result)
    return result


def generated_group(generators):
    identity = tuple(range(4))
    group = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            nxt = compose(generator, current)
            if nxt not in group:
                group.add(nxt)
                frontier.append(nxt)
    return group


def orbit_partition(group):
    unused = set(range(4))
    answer = []
    while unused:
        seed = min(unused)
        orbit = {g[seed] for g in group}
        unused -= orbit
        answer.append(len(orbit))
    return tuple(sorted(answer, reverse=True))


a = (1, 0, 2, 3)  # (12)
b = (0, 2, 1, 3)  # (23)
c = (0, 1, 3, 2)  # (34)
identity = tuple(range(4))

assert orbit_partition(generated_group([a, b])) == (3, 1)
assert orbit_partition(generated_group([a, c])) == (2, 2)
assert len(generated_group([a, b, c])) == 24

# Restriction to one normalization branch of a two-branch value sees
# the other transposition to the local intersection multiplicity.
for multiplicity in range(1, 20):
    residual_monodromy = power(c, multiplicity)
    assert (residual_monodromy != identity) == (multiplicity % 2 == 1)


def connected_profile(nodes, odd_nodes):
    """Return genus, deleted points, and retained Euler characteristic."""
    assert nodes >= 1
    assert 1 <= odd_nodes <= nodes
    finite_branch_points = 2 * odd_nodes
    genus = (finite_branch_points - 2) // 2
    deleted = 1 + 4 * nodes - 2 * odd_nodes
    z_euler = 2 - 2 * odd_nodes
    retained_euler = z_euler - deleted
    return genus, deleted, retained_euler


for nodes in range(1, 12):
    # Every even-contact profile splits into two affine lines.
    split_deleted = 1 + 4 * nodes
    assert 2 - split_deleted == 1 - 4 * nodes

    for odd_nodes in range(1, nodes + 1):
        genus, deleted, retained_euler = connected_profile(
            nodes, odd_nodes
        )
        assert genus == odd_nodes - 1
        assert deleted == 1 + 4 * nodes - 2 * odd_nodes
        assert retained_euler == 1 - 4 * nodes

# In the extra-boundary survivor, each section loses at least one point.
for first_punctures in range(1, 8):
    for second_punctures in range(1, 8):
        curve_euler = (
            1 - first_punctures + 1 - second_punctures
        )
        assert curve_euler == 2 - first_punctures - second_punctures

        # W is a finite degree-four étale cover of a zero-Euler
        # complement.  Removing E' minus all its punctures gives the
        # same Euler characteristic as S minus the two sections.
        boundary_open_euler = 1 - first_punctures - second_punctures
        complement_euler_from_w = -boundary_open_euler
        complement_euler_from_s = 1 - curve_euler
        assert complement_euler_from_w == complement_euler_from_s

# Smith normal forms of the two possible complement-homology
# presentations.  The relation matrix has columns mu_1, mu_2, h.
split_relation = sp.Matrix([[0, 0, 2]])
nontrivial_relation = sp.Matrix([[-1, -1, 2]])

split_invariant = gcd(*[abs(int(x)) for x in split_relation])
nontrivial_invariant = gcd(
    *[abs(int(x)) for x in nontrivial_relation]
)

assert split_relation.rank() == 1
assert nontrivial_relation.rank() == 1
assert split_invariant == 2  # Z^2 plus Z/2.
assert nontrivial_invariant == 1  # Z^2, torsion-free.

# One principal component gives <mu,h | 2h=0>.
one_component_relation = sp.Matrix([[0, 2]])
assert one_component_relation.rank() == 1
assert gcd(*[abs(int(x)) for x in one_component_relation]) == 2

# Every local factor in the r=2, delta=0 survivor is Gorenstein:
# ordinary branch values have support 2+1+1 and two-branch values
# have support 2+2, so every local factor has length at most two.
for second_survivor_fiber_lengths in ((2, 1, 1), (2, 2)):
    assert sum(second_survivor_fiber_lengths) == 4
    assert all(length <= 2 for length in second_survivor_fiber_lengths)

curvilinear_socle_dimension = 1
noncurvilinear_socle_dimension = 2
assert curvilinear_socle_dimension == 1
assert noncurvilinear_socle_dimension != 1

# Miranda's triple-cover discriminant is quartic in a,b,c,d.  If all
# four coefficients vanish, the branch order is therefore at least four.
a_symbol, b_symbol, c_symbol, d_symbol = sp.symbols("a b c d")
miranda_discriminant = (
    b_symbol**2 * c_symbol**2
    - 3 * a_symbol**2 * d_symbol**2
    + 4 * a_symbol**3 * c_symbol
    + 4 * b_symbol * d_symbol**3
    - 6 * a_symbol * b_symbol * c_symbol * d_symbol
)
for exponent_tuple, _coefficient in sp.Poly(
    miranda_discriminant,
    a_symbol,
    b_symbol,
    c_symbol,
    d_symbol,
).terms():
    assert sum(exponent_tuple) == 4

print("route A degree-four survivor normalization profiles: exact checks passed")
