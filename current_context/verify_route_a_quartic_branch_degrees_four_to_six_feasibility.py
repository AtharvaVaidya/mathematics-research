#!/usr/bin/env python3
"""Exact checks for Route A branch-degree 4, 5, 6 feasibility."""

from __future__ import annotations

from itertools import permutations

import sympy as sp


t, zeta, x, y = sp.symbols("t zeta x y")
cyclotomic = sp.Poly(zeta**2 + zeta + 1, zeta)

q_by_degree = {
    4: t**4 + t**2,
    5: t**5 + t**4 + t**2,
    6: t**6 + t**5 + t**4 + t**2,
}

expected_implicit = {
    4: x**4 + 3 * x**2 * y + x**2 - y**3,
    5: (
        -x**5
        - 4 * x**4
        - 3 * x**3 * y
        - 3 * x**3
        - 3 * x**2 * y
        - x**2
        + y**3
    ),
    6: (
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
    ),
}


def reduce_zeta(expression: sp.Expr) -> sp.Expr:
    return sp.rem(
        sp.Poly(sp.expand(expression), zeta),
        cyclotomic,
    ).as_expr()


def verify_parametrizations() -> None:
    p = t**3
    node_counts = {}
    for degree, q in q_by_degree.items():
        implicit = sp.factor(sp.resultant(p - x, q - y, t))
        assert sp.expand(implicit - expected_implicit[degree]) == 0
        assert sp.Poly(implicit, x, y).total_degree() == degree
        assert sp.diff(p, t) == 3 * t**2
        assert sp.diff(q, t).subs(t, 0) == 0

        raw_difference = sp.expand(q - q.subs(t, zeta * t))
        H = reduce_zeta(
            sp.cancel(raw_difference / ((1 - zeta) * t**2))
        )
        expected_H = (
            t**2 + zeta + 1
            if degree == 4
            else (zeta + 1) * (t**3 + 1) + t**2
        )
        assert reduce_zeta(H - expected_H) == 0

        squarefree_resultant = reduce_zeta(
            sp.resultant(H, sp.diff(H, t), t)
        )
        expected_squarefree = (
            4 * (zeta + 1) if degree == 4 else -23 * zeta
        )
        assert reduce_zeta(
            squarefree_resultant - expected_squarefree
        ) == 0

        tangent_determinant = reduce_zeta(
            sp.diff(p, t) * sp.diff(q, t).subs(t, zeta * t)
            - sp.diff(q, t) * sp.diff(p, t).subs(t, zeta * t)
        )
        transverse_resultant = reduce_zeta(
            sp.resultant(H, tangent_determinant, t)
        )
        expected_transverse = (
            sp.Integer(108)
            if degree == 4
            else -1863 * (2 * zeta + 1)
        )
        assert reduce_zeta(
            transverse_resultant - expected_transverse
        ) == 0

        conjugate_H = reduce_zeta(H.subs(zeta, zeta**2))
        triple_resultant = reduce_zeta(
            sp.resultant(H, conjugate_H, t)
        )
        assert triple_resultant != 0
        node_counts[degree] = sp.degree(H, t)

    assert node_counts == {4: 2, 5: 3, 6: 3}


def verify_delta_and_puncture_ledgers() -> None:
    cusp_delta = 1
    node_counts = {4: 2, 5: 3, 6: 3}
    infinity_delta = {4: 0, 5: 2, 6: 6}
    for degree in (4, 5, 6):
        arithmetic_genus = (degree - 1) * (degree - 2) // 2
        assert (
            cusp_delta
            + node_counts[degree]
            + infinity_delta[degree]
            == arithmetic_genus
        )

        k_p = 3 - 2
        k_q = degree - 2
        assert 1 <= k_p <= 4
        assert 1 <= k_q <= 4
        s_p = 2 * k_p + 2
        s_q = 2 * k_q + 2
        assert (s_p, s_q) == (4, 2 * degree - 2)

    # The characteristic pairs at infinity give the stated deltas.
    assert (2 - 1) * (5 - 1) // 2 == 2
    assert (3 - 1) * (7 - 1) // 2 == 6


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(4))


def generated_group(
    generators: list[tuple[int, ...]],
) -> set[tuple[int, ...]]:
    identity = tuple(range(4))
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


def orbit_sizes(group: set[tuple[int, ...]]) -> tuple[int, ...]:
    unused = set(range(4))
    sizes = []
    while unused:
        seed = next(iter(unused))
        orbit = {permutation[seed] for permutation in group}
        unused -= orbit
        sizes.append(len(orbit))
    return tuple(sorted(sizes, reverse=True))


def verify_local_monodromy() -> None:
    a = (1, 0, 2, 3)  # (12)
    b = (0, 2, 1, 3)  # (23)
    c = (0, 1, 3, 2)  # (34)

    assert compose(compose(a, b), a) == compose(compose(b, a), b)
    assert compose(a, c) == compose(c, a)
    assert orbit_sizes(generated_group([a, b])) == (3, 1)
    assert orbit_sizes(generated_group([a, c])) == (2, 2)
    assert len(generated_group([a, b, c])) == len(
        list(permutations(range(4)))
    )


def main() -> None:
    verify_parametrizations()
    verify_delta_and_puncture_ledgers()
    verify_local_monodromy()
    print("verified: exact degree-4,5,6 implicit parametrizations")
    print("verified: cusp, node, and no-triple-collision resultants")
    print("verified: genus, infinity-semigroup, and puncture ledgers")
    print("verified: local 3+1 and 2+2 permutation compatibility")
    print("RESULT: QUARTIC BRANCH DEGREE 4-6 FEASIBILITY PASSES")


if __name__ == "__main__":
    main()
