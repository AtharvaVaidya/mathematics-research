#!/usr/bin/env python3
"""Enumerate the support-18 interaction multiplicity profiles exactly."""

from __future__ import annotations

import itertools


PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EXPECTED = (
    (0, 0, 4, 4, 0, 1),
    (0, 0, 4, 5, 0, 0),
    (0, 1, 3, 3, 1, 1),
    (0, 1, 3, 3, 2, 0),
    (0, 1, 3, 4, 1, 0),
    (0, 2, 2, 2, 2, 1),
    (0, 2, 2, 2, 3, 0),
    (1, 1, 2, 2, 1, 2),
    (1, 1, 2, 3, 1, 1),
)


def degrees(profile: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0, 0, 0, 0]
    for multiplicity, (u, v) in zip(profile, PAIRS):
        answer[u] += multiplicity
        answer[v] += multiplicity
    return tuple(answer)


def relabel(profile: tuple[int, ...], permutation: tuple[int, ...]):
    values = {pair: value for pair, value in zip(PAIRS, profile)}
    changed = {}
    for (u, v), value in values.items():
        pair = tuple(sorted((permutation[u], permutation[v])))
        changed[pair] = value
    return tuple(changed[pair] for pair in PAIRS)


def connected(profile: tuple[int, ...]) -> bool:
    adjacency = [set() for _ in range(4)]
    for multiplicity, (u, v) in zip(profile, PAIRS):
        if multiplicity:
            adjacency[u].add(v)
            adjacency[v].add(u)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbour in adjacency[vertex] - seen:
            seen.add(neighbour)
            stack.append(neighbour)
    return len(seen) == 4


def has_bridge(profile: tuple[int, ...]) -> bool:
    for index, multiplicity in enumerate(profile):
        if multiplicity != 1:
            continue
        reduced = list(profile)
        reduced[index] = 0
        if not connected(tuple(reduced)):
            return True
    return False


def main() -> None:
    labelled = []
    for profile in itertools.product(range(10), repeat=6):
        if sum(profile) != 9:
            continue
        if sorted(degrees(profile)) == [4, 4, 5, 5]:
            labelled.append(profile)

    permutations = tuple(itertools.permutations(range(4)))
    canonical = {
        min(relabel(profile, permutation) for permutation in permutations)
        for profile in labelled
    }
    assert len(labelled) == 90
    assert tuple(sorted(canonical)) == EXPECTED
    assert sum(not connected(profile) for profile in canonical) == 1
    assert sum(
        connected(profile) and has_bridge(profile) for profile in canonical
    ) == 1

    print(f"labelled_profiles={len(labelled)} orbit_profiles={len(canonical)}")
    for profile in sorted(canonical):
        print(
            f"profile={profile} degrees={degrees(profile)}"
            f" connected={int(connected(profile))}"
            f" bridge={int(has_bridge(profile))}"
        )
    print("PASS exact four-vertex profile classification")


if __name__ == "__main__":
    main()
