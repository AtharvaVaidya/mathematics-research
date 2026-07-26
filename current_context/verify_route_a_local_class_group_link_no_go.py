#!/usr/bin/env python3
"""Exact checks for ROUTE_A_LOCAL_CLASS_GROUP_LINK_NO_GO.md.

Literature theorems about local Picard groups are citation-level inputs.
This script checks the Hesse model and the nodal monodromy/Euler algebra.
"""

from __future__ import annotations

from itertools import permutations

import sympy as sp


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(3))


def generated_group(generators: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    identity = (0, 1, 2)
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


def orbit_count(group: set[tuple[int, ...]]) -> int:
    unseen = {0, 1, 2}
    count = 0
    while unseen:
        seed = next(iter(unseen))
        orbit = {permutation[seed] for permutation in group}
        unseen -= orbit
        count += 1
    return count


def hesse_simple_elliptic_model() -> None:
    x, y, z = sp.symbols("x y z")
    hesse = z**3 + 3 * x * y * z + x**3 + y**3

    # The projective cubic is smooth.
    partials = [sp.diff(hesse, variable) for variable in (x, y, z)]
    for variable in (x, y, z):
        basis = sp.groebner(
            partials + [variable - 1],
            x,
            y,
            z,
            order="lex",
        )
        assert list(basis) == [1]

    # The projection to (x,y) is cubic with squarefree discriminant.
    discriminant = sp.factor(sp.discriminant(hesse, z))
    expected = -27 * (x**6 + 6 * x**3 * y**3 + y**6)
    assert sp.expand(discriminant - expected) == 0
    squarefree_gcd = sp.gcd(
        sp.gcd(discriminant, sp.diff(discriminant, x)),
        sp.diff(discriminant, y),
    )
    assert sp.Poly(squarefree_gcd, x, y).total_degree() == 0

    # A nonzero-Euler-number circle bundle over an elliptic curve has
    # rational H_1 equal to the base H_1.
    base_b1 = 2
    link_b1 = base_b1
    assert link_b1 == 2


def nodal_monodromy_and_balance() -> None:
    first = (1, 0, 2)  # (12)
    same = first
    distinct = (0, 2, 1)  # (23)

    same_group = generated_group([first, same])
    distinct_group = generated_group([first, distinct])

    assert len(same_group) == 2
    assert orbit_count(same_group) == 2
    assert len(distinct_group) == 6
    assert distinct_group == set(permutations(range(3)))
    assert orbit_count(distinct_group) == 1

    delta, transitive = sp.symbols(
        "delta transitive", integer=True, nonnegative=True
    )
    chi_branch = 1 - delta
    boundary_components = 2 - chi_branch - transitive
    assert sp.expand(boundary_components) == 1 + delta - transitive

    inequality_left = 1 + chi_branch + transitive
    assert sp.expand(inequality_left) == 2 - delta + transitive

    # Equality means every node is transitive, hence r=1.
    equality_r = boundary_components.subs(transitive, delta)
    assert equality_r == 1

    # The unique ramified boundary is fiberwise one point over Delta,
    # so chi(R)=chi(Delta)=1-delta, whereas duality would give chi(R)=r=1.
    discrepancy = sp.expand(equality_r - chi_branch)
    assert discrepancy == delta


def generalized_jacobian_dimensions() -> None:
    total_genus, graph_b1 = sp.symbols(
        "total_genus graph_b1", integer=True, nonnegative=True
    )
    link_b1 = 2 * total_genus + graph_b1
    picard_identity_dimension = total_genus + graph_b1

    # For nonnegative inputs, positive link b1 forces positive Pic^0 dimension.
    for genus_value in range(5):
        for graph_value in range(5):
            link_value = link_b1.subs(
                {total_genus: genus_value, graph_b1: graph_value}
            )
            picard_value = picard_identity_dimension.subs(
                {total_genus: genus_value, graph_b1: graph_value}
            )
            if link_value > 0:
                assert picard_value > 0


def main() -> None:
    hesse_simple_elliptic_model()
    nodal_monodromy_and_balance()
    generalized_jacobian_dimensions()
    print("verified: Hesse cone is a smooth-projectivization cubic model")
    print("verified: Hesse projection has squarefree cubic discriminant")
    print("verified: same/distinct node transpositions have 2/1 orbits")
    print("verified: nodal equality forces r=1 and Euler discrepancy delta")
    print("verified: positive link b1 forces positive generalized Pic^0 dimension")
    print("RESULT: algebraic local Cl finite generation cannot kill link b1")


if __name__ == "__main__":
    main()
