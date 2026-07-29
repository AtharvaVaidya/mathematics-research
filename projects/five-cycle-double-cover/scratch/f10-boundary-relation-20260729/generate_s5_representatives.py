#!/usr/bin/env python3
"""Generate the S5 orbits of xor-zero ordered six-duad boundary words."""

from __future__ import annotations

from itertools import combinations, permutations, product
import argparse
import json
from pathlib import Path


DUADS = tuple(
    sum(1 << coordinate for coordinate in pair)
    for pair in combinations(range(5), 2)
)
PERMUTATIONS = tuple(permutations(range(5)))


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(
        1 << permutation[coordinate]
        for coordinate in range(5)
        if mask >> coordinate & 1
    )


def canonical(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(permute_mask(mask, permutation) for mask in word)
        for permutation in PERMUTATIONS
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()

    words = []
    representatives = set()
    for word in product(DUADS, repeat=6):
        total = 0
        for mask in word:
            total ^= mask
        if total:
            continue
        words.append(word)
        representatives.add(canonical(word))

    result = {
        "schema": "ordered-six-duad-xor-zero-s5-orbits-v1",
        "duads": list(DUADS),
        "ordered_xor_zero_words": len(words),
        "s5_orbits": len(representatives),
        "representatives": [list(word) for word in sorted(representatives)],
    }
    assert len(words) == 62560
    assert len(representatives) == 571
    arguments.output.write_text(
        json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="ascii",
    )
    print(
        f"ordered_xor_zero_words={len(words)} "
        f"s5_orbits={len(representatives)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
