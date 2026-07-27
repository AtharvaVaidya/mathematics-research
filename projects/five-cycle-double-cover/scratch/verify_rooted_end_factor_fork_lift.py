#!/usr/bin/env python3
"""Literal finite checks for rooted-cap-end-factor-fork-lift.md.

The endpoint lift itself is the human gluing argument in the note.  This
standard-library replay checks the two finite pieces used there: ordered
triangle normalization and the complete cross-relation table of forks.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations
import json


EDGES = tuple(frozenset(edge) for edge in combinations(range(5), 2))
TAU = (
    frozenset((0, 1)),
    frozenset((0, 2)),
    frozenset((1, 2)),
)


def apply(permutation: tuple[int, ...], edge: frozenset[int]) -> frozenset[int]:
    return frozenset(permutation[coordinate] for coordinate in edge)


def ordered_triangles() -> set[tuple[frozenset[int], ...]]:
    result: set[tuple[frozenset[int], ...]] = set()
    for coordinates in combinations(range(5), 3):
        triangle = tuple(
            frozenset(edge) for edge in combinations(coordinates, 2)
        )
        result.update(permutations(triangle))
    return result


def forks() -> set[frozenset[frozenset[int]]]:
    result: set[frozenset[frozenset[int]]] = set()
    for p, q, r, s, t in permutations(range(5)):
        result.add(
            frozenset(
                (
                    frozenset((q, r)),
                    frozenset((p, s)),
                    frozenset((p, t)),
                )
            )
        )
    return result


def relation(
    left: frozenset[frozenset[int]],
    right: frozenset[frozenset[int]],
) -> str:
    kinds = set()
    for first in left:
        for second in right:
            if first == second:
                kinds.add("E")
            elif first & second:
                kinds.add("I")
            else:
                kinds.add("D")
    return "".join(kind for kind in "EID" if kind in kinds)


def main() -> int:
    triangles = ordered_triangles()
    assert len(triangles) == 60
    normalization_profile = Counter()
    for triangle in triangles:
        count = sum(
            tuple(apply(permutation, edge) for edge in triangle) == TAU
            for permutation in permutations(range(5))
        )
        normalization_profile[count] += 1
    assert normalization_profile == {2: 60}

    all_forks = forks()
    assert len(all_forks) == 30
    relation_profile = Counter(
        relation(left, right) for left in all_forks for right in all_forks
    )
    assert relation_profile == {"ID": 330, "EID": 570}

    for fork in all_forks:
        assert len(fork) == 3
        assert set().union(*fork) == set(range(5))
        common_intersectors = {
            edge for edge in EDGES if all(edge & member for member in fork)
        }
        assert len(common_intersectors) == 2

    result = {
        "schema": "rooted-end-factor-fork-lift-replay-v1",
        "ordered_triangles": len(triangles),
        "normalizations_per_ordered_triangle": 2,
        "forks": len(all_forks),
        "ordered_fork_pair_relations": {
            "intersection_disjointness": relation_profile["ID"],
            "equality_intersection_disjointness": relation_profile["EID"],
        },
        "status": "PASS",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
