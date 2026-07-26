#!/usr/bin/env python3
"""Exact ten-type algebra for a two-plus-two composition of cubic 4-poles.

The calculation is deliberately tiny.  A boundary label is a two-subset
of five colours, represented by a weight-two bit mask.  Four labels are
admissible at the boundary exactly when their xor is zero.  Quotienting by
the global S_5 action gives the ten types of
Macajova--Mazzuoccolo--Tabarelli.

Two ordered four-poles are composed by identifying boundary positions
3,4 of the first with positions 1,2 of the second.  The remaining
positions 1,2 of the first and 3,4 of the second are the new ordered
boundary.  Since every type orbit contains all of its S_5 translates,
the ten-by-ten table below is the exact support-level composition law.

The second calculation filters all nonempty subsets of the ten types by
the necessary conditions in Lemmas 3.4 and 3.5 of the cited paper, then
lists all ordered factorizations of either exceptional signature.

This is a finite algebra calculation, not a graph-realizability claim.
"""

from __future__ import annotations

import argparse
from itertools import combinations, permutations, product
import json
from pathlib import Path


TYPE_NAMES = (
    "AA",
    "AT2",
    "T2T2",
    "AT3",
    "AT4",
    "T2T3",
    "T2T4",
    "T3T3",
    "T3T4",
    "T4T4",
)

# The ten type names are the loops and ordinary edges of the looped K_4
# with vertices A,T2,T3,T4, in the same order as TYPE_NAMES.
TYPE_ENDS = (
    (0, 0),
    (0, 1),
    (1, 1),
    (0, 2),
    (0, 3),
    (1, 2),
    (1, 3),
    (2, 2),
    (2, 3),
    (3, 3),
)


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(
        1 << permutation[colour]
        for colour in range(5)
        if (mask >> colour) & 1
    )


def canonical_word(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(permute_mask(mask, permutation) for mask in word)
        for permutation in permutations(range(5))
    )


def boundary_orbits() -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[tuple[int, ...], ...], ...],
]:
    labels = tuple(
        (1 << left) | (1 << right)
        for left, right in combinations(range(5), 2)
    )
    representatives = tuple(
        sorted(
            {
                canonical_word(word)
                for word in product(labels, repeat=4)
                if word[0] ^ word[1] ^ word[2] ^ word[3] == 0
            }
        )
    )
    if len(representatives) != 10:
        raise AssertionError("the boundary must have ten S_5 orbits")
    index = {word: orbit for orbit, word in enumerate(representatives)}
    words: list[list[tuple[int, ...]]] = [[] for _ in representatives]
    for word in product(labels, repeat=4):
        if word[0] ^ word[1] ^ word[2] ^ word[3]:
            continue
        words[index[canonical_word(word)]].append(word)
    if tuple(map(len, words)) != (10, 60, 30, 60, 60, 120, 120, 30, 120, 30):
        raise AssertionError("unexpected orbit sizes")
    return representatives, tuple(tuple(row) for row in words)


def singleton_composition_table(
    words: tuple[tuple[tuple[int, ...], ...], ...],
) -> tuple[tuple[int, ...], ...]:
    representatives, _ = boundary_orbits()
    orbit_index = {
        representative: orbit
        for orbit, representative in enumerate(representatives)
    }
    table: list[list[int]] = [[0] * 10 for _ in range(10)]
    for left_type in range(10):
        for right_type in range(10):
            output = 0
            for left_word in words[left_type]:
                for right_word in words[right_type]:
                    if left_word[2:] != right_word[:2]:
                        continue
                    boundary = left_word[:2] + right_word[2:]
                    output |= 1 << orbit_index[canonical_word(boundary)]
            table[left_type][right_type] = output
    return tuple(tuple(row) for row in table)


def compose(left: int, right: int, table: tuple[tuple[int, ...], ...]) -> int:
    output = 0
    for left_type in range(10):
        if not ((left >> left_type) & 1):
            continue
        for right_type in range(10):
            if (right >> right_type) & 1:
                output |= table[left_type][right_type]
    return output


def has_type(signature: int, edge: tuple[int, int]) -> bool:
    edge = tuple(sorted(edge))
    return bool((signature >> TYPE_ENDS.index(edge)) & 1)


def satisfies_published_lemmas(signature: int) -> bool:
    """Check exactly the necessary conditions in MMT Lemmas 3.4--3.5."""

    for vertex in range(4):
        loop = has_type(signature, (vertex, vertex))
        neighbours = [
            other
            for other in range(4)
            if other != vertex and has_type(signature, (vertex, other))
        ]

        # Lemma 3.4: no degree-one vertex and no isolated loop.
        if len(neighbours) == 1 and not loop:
            return False
        if loop and not neighbours:
            return False

        if not loop:
            continue

        # Lemma 3.5, first alternative.
        first = any(
            has_type(signature, (vertex, other))
            and has_type(signature, (other, other))
            for other in range(4)
            if other != vertex
        )

        # Lemma 3.5, second alternative.
        second = any(
            has_type(signature, (vertex, left))
            and has_type(signature, (vertex, right))
            and has_type(signature, (left, right))
            for left, right in combinations(
                (other for other in range(4) if other != vertex),
                2,
            )
        )
        if not (first or second):
            return False
    return True


def exceptional_signatures() -> tuple[tuple[int, ...], tuple[int, ...]]:
    name_to_index = {name: index for index, name in enumerate(TYPE_NAMES)}
    four = set()
    five = set()
    for excluded, left, right in permutations((2, 3, 4)):
        four_names = (
            "AA",
            f"AT{left}",
            f"AT{right}",
            f"T{min(left, right)}T{max(left, right)}",
        )
        five_names = (
            f"T{excluded}T{excluded}",
            f"T{left}T{left}",
            f"T{right}T{right}",
            f"T{min(excluded, left)}T{max(excluded, left)}",
            f"T{min(excluded, right)}T{max(excluded, right)}",
        )
        four.add(sum(1 << name_to_index[name] for name in four_names))
        five.add(sum(1 << name_to_index[name] for name in five_names))
    return tuple(sorted(four)), tuple(sorted(five))


def names(signature: int) -> list[str]:
    return [
        name
        for index, name in enumerate(TYPE_NAMES)
        if (signature >> index) & 1
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    representatives, words = boundary_orbits()
    table = singleton_composition_table(words)
    allowed = tuple(
        signature
        for signature in range(1, 1 << 10)
        if satisfies_published_lemmas(signature)
    )
    four_targets, five_targets = exceptional_signatures()
    exceptional_family = set(four_targets) | set(five_targets)

    factorizations = {}
    for target in (*four_targets, *five_targets):
        rows = [
            (left, right)
            for left in allowed
            for right in allowed
            if compose(left, right, table) == target
        ]
        factorizations[hex(target)] = [
            {
                "left": hex(left),
                "left_types": names(left),
                "right": hex(right),
                "right_types": names(right),
                "has_exceptional_factor": (
                    left in exceptional_family or right in exceptional_family
                ),
            }
            for left, right in rows
        ]

    report = {
        "schema": "four-pole-two-plus-two-algebra-v1",
        "ordered_boundary_words": sum(map(len, words)),
        "orbit_representatives": [
            {
                "type": TYPE_NAMES[index],
                "word": list(representative),
                "orbit_size": len(words[index]),
            }
            for index, representative in enumerate(representatives)
        ],
        "singleton_composition_table": [
            [names(cell) for cell in row]
            for row in table
        ],
        "published_lemma_admissible_nonempty_signatures": len(allowed),
        "exceptional_four": [hex(mask) for mask in four_targets],
        "exceptional_five": [hex(mask) for mask in five_targets],
        "factorizations": factorizations,
        "scope": (
            "Exact boundary-orbit algebra plus MMT Lemmas 3.4--3.5 only; "
            "admissible masks are not asserted graph-realizable."
        ),
    }

    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
