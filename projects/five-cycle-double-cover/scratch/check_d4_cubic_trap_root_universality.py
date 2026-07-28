#!/usr/bin/env python3
"""Finite algebra replay for the cubic D4-trap root-universality lemma."""

from __future__ import annotations

from itertools import combinations, product


COORDINATES = frozenset(range(4))
D4 = tuple(frozenset(pair) for pair in combinations(COORDINATES, 2))


def complement(label: frozenset[int]) -> frozenset[int]:
    return COORDINATES - label


TAIT_CLASSES = tuple(
    frozenset((label, complement(label)))
    for label in D4
)
TAIT_CLASSES = tuple(sorted(set(TAIT_CLASSES), key=lambda row: sorted(map(sorted, row))))
TAIT_INDEX = {
    label: index
    for index, colour_class in enumerate(TAIT_CLASSES)
    for label in colour_class
}


def transpose(
    label: frozenset[int], first: int, second: int
) -> frozenset[int]:
    permutation = {
        coordinate: (
            second if coordinate == first
            else first if coordinate == second
            else coordinate
        )
        for coordinate in COORDINATES
    }
    return frozenset(permutation[coordinate] for coordinate in label)


def active(label: frozenset[int], pair: frozenset[int]) -> bool:
    return len(label & pair) == 1


def main() -> None:
    assert len(TAIT_CLASSES) == 3

    # Every local cubic D4 XOR triple projects to the three distinct Tait
    # colours.
    local_triples = []
    for triple in product(D4, repeat=3):
        xor = set()
        for label in triple:
            xor ^= set(label)
        if xor:
            continue
        local_triples.append(triple)
        assert {TAIT_INDEX[label] for label in triple} == {0, 1, 2}
    assert len(local_triples) == 24

    disjoint_cases = 0
    repair_checks = 0
    for root, target in product(D4, repeat=2):
        if root & target:
            continue
        disjoint_cases += 1
        assert target == complement(root)
        root_colour = TAIT_INDEX[root]
        assert TAIT_INDEX[target] == root_colour
        for desired_colour in range(3):
            if desired_colour == root_colour:
                continue
            excluded_colour = next(
                colour
                for colour in range(3)
                if colour not in (root_colour, desired_colour)
            )
            # Either representative of the excluded complementary class
            # defines the same active bichromatic factor.
            for factor_pair in TAIT_CLASSES[excluded_colour]:
                first, second = sorted(factor_pair)
                assert active(root, factor_pair)
                assert active(target, factor_pair)
                moved = transpose(root, first, second)
                assert TAIT_INDEX[moved] == desired_colour
                assert moved & target
                repair_checks += 1

    assert disjoint_cases == 6
    assert repair_checks == 24
    print(f"Tait complementary classes: {TAIT_CLASSES}")
    print(f"local ordered D4 XOR triples: {len(local_triples)}")
    print(f"ordered disjoint root-label cases: {disjoint_cases}")
    print(f"one-component algebraic repair checks: {repair_checks}")
    print("PASS")


if __name__ == "__main__":
    main()
