#!/usr/bin/env python3
"""Literal seven-orbit check for the rooted three-pole factorization."""

from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path


D5 = tuple(sum(1 << coordinate for coordinate in pair)
           for pair in combinations(range(5), 2))
ORBITS = (
    frozenset({0b00011}),  # 01
    frozenset({0b00101}),  # 02
    frozenset({0b00110}),  # 12
    frozenset({0b01001, 0b10001}),  # 03,04
    frozenset({0b01010, 0b10010}),  # 13,14
    frozenset({0b01100, 0b10100}),  # 23,24
    frozenset({0b11000}),  # 34
)
EQUAL = 1
INTERSECT = 2
DISJOINT = 4


def labels(mask: int) -> frozenset[int]:
    result: set[int] = set()
    for orbit, values in enumerate(ORBITS):
        if (mask >> orbit) & 1:
            result.update(values)
    return frozenset(result)


def relation(left: int, right: int) -> int:
    result = 0
    for first in labels(left):
        for second in labels(right):
            if first == second:
                result |= EQUAL
            elif first & second:
                result |= INTERSECT
            else:
                result |= DISJOINT
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    profile: dict[str, int] = {}
    equality = []
    disjoint_ordered = []
    equal_intersect = []
    names = {
        EQUAL: "E",
        INTERSECT: "I",
        DISJOINT: "D",
        EQUAL | INTERSECT: "EI",
        EQUAL | DISJOINT: "ED",
        INTERSECT | DISJOINT: "ID",
        EQUAL | INTERSECT | DISJOINT: "EID",
    }
    for left in range(1, 1 << 7):
        for right in range(1, 1 << 7):
            value = relation(left, right)
            name = names[value]
            profile[name] = profile.get(name, 0) + 1
            if value == EQUAL:
                equality.append((left, right))
            elif value == DISJOINT:
                disjoint_ordered.append((left, right))
            elif value == EQUAL | INTERSECT:
                equal_intersect.append((left, right))

    expected_equality = {(1, 1), (2, 2), (4, 4), (64, 64)}
    assert set(equality) == expected_equality

    triangle_masks = range(1, 8)
    expected_disjoint = set()
    for triangle_mask in triangle_masks:
        common = set(D5)
        for edge in labels(triangle_mask):
            common = {other for other in common if not (edge & other)}
        for other_mask in range(1, 1 << 7):
            if labels(other_mask) and labels(other_mask) <= common:
                expected_disjoint.add((triangle_mask, other_mask))
                expected_disjoint.add((other_mask, triangle_mask))
    assert set(disjoint_ordered) == expected_disjoint

    disjoint_unordered = sorted(
        {tuple(sorted(pair)) for pair in disjoint_ordered}
    )
    assert len(disjoint_unordered) == 13
    assert len(equal_intersect) == 231
    assert sum(profile.values()) == 127 * 127

    result = {
        "status": "PASS",
        "orbit_labels": [sorted(values) for values in ORBITS],
        "relation_profile": dict(sorted(profile.items())),
        "equality_only_ordered_masks": [
            [hex(left), hex(right)] for left, right in sorted(equality)
        ],
        "disjoint_only_ordered_count": len(disjoint_ordered),
        "disjoint_only_unordered_count": len(disjoint_unordered),
        "disjoint_only_unordered_masks": [
            [hex(left), hex(right)] for left, right in disjoint_unordered
        ],
        "equal_intersect_ordered_count": len(equal_intersect),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
