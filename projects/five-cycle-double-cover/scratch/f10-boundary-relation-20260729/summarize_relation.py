#!/usr/bin/env python3
"""Summarize the full F10 relation and its emergent S6 port symmetry."""

from __future__ import annotations

from itertools import combinations, combinations_with_replacement, permutations
import argparse
import json
from pathlib import Path


DUADS = tuple(
    sum(1 << coordinate for coordinate in pair)
    for pair in combinations(range(5), 2)
)
COORDINATE_PERMUTATIONS = tuple(permutations(range(5)))


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(
        1 << permutation[coordinate]
        for coordinate in range(5)
        if mask >> coordinate & 1
    )


def canonical_multiset(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(sorted(permute_mask(mask, permutation) for mask in word))
        for permutation in COORDINATE_PERMUTATIONS
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("representatives", type=Path)
    parser.add_argument("results", type=Path)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()
    source = json.loads(arguments.representatives.read_text(encoding="ascii"))
    rows = [
        json.loads(line)
        for line in arguments.results.read_text(encoding="ascii").splitlines()
    ]
    assert len(source["representatives"]) == len(rows) == 571
    assert all(row["status"] == "SAT_SEMANTIC_CHECK" for row in rows)

    multisets = []
    quotient = set()
    for word in combinations_with_replacement(DUADS, 6):
        total = 0
        for mask in word:
            total ^= mask
        if total:
            continue
        multisets.append(word)
        quotient.add(canonical_multiset(word))
    assert len(multisets) == 385
    assert len(quotient) == 11
    result = {
        "schema": "f10-full-six-port-d5-relation-summary-v1",
        "relation": {
            "ordered_duad_words": 10**6,
            "ordered_xor_zero_words": 62560,
            "s5_coordinate_orbits": 571,
            "positive_s5_orbits": len(rows),
            "negative_s5_orbits": 0,
            "description": (
                "exactly the ordered six-duad words with total xor zero"
            ),
        },
        "emergent_port_symmetry": {
            "group": "full S6 on the six ordered ports",
            "note": (
                "This is symmetry of the proved boundary relation; it is "
                "stronger than, and does not assert, graph automorphisms."
            ),
            "xor_zero_multisets": len(multisets),
            "s5_times_s6_orbits": len(quotient),
            "representatives": [list(word) for word in sorted(quotient)],
        },
        "network_consequence": (
            "Every finite network formed from copies of the F10 six-pole "
            "by attaching every port to a trivalent junction has a FiveCDC."
        ),
    }
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(json.dumps(
        {
            "positive_s5_orbits": len(rows),
            "s5_times_s6_orbits": len(quotient),
            "xor_zero_multisets": len(multisets),
        },
        sort_keys=True,
        separators=(",", ":"),
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
