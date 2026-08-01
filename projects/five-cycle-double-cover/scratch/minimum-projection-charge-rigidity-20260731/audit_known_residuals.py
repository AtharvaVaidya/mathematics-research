#!/usr/bin/env python3
"""Classify the charge kernel of every frozen size-14/15/16 residual row."""

from __future__ import annotations

import csv
import glob
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCRATCH = HERE.parent


def rank_k(vectors):
    have1 = have2 = 0
    for value in vectors:
        if not value:
            continue
        if value & 2:
            if have2:
                value ^= have2
            else:
                have2 = value
                continue
        if value & 1:
            if have1:
                value ^= have1
            else:
                have1 = value
    return bool(have1) + bool(have2)


def profile(word_text, partition_text):
    words = word_text.split("|")
    assert len(words) == 2
    partition = tuple(map(int, partition_text))
    assert sum(map(len, words)) == len(partition)
    block_count = max(partition) + 1
    matrix = [[0, 0] for _ in range(block_count)]
    offset = 0
    for circuit, word in enumerate(words):
        for position, colour in enumerate(word):
            derivative = int(word[position - 1]) ^ int(colour)
            assert derivative
            matrix[partition[offset + position]][circuit] ^= derivative
        offset += len(word)
    assert all(left == right for left, right in matrix)
    active = [left for left, _right in matrix if left]
    isolated = sum(left == 0 for left, _right in matrix)
    # For two columns (x,x), the scalar block-kernel dimension is
    # |active|-rank(active).  Subtract its unavoidable all-ones dependency.
    excess = len(active) - rank_k(active) - 1 if active else 0
    return len(active), 2 if active else 0, excess, isolated


def parse_counterstate_files(pattern):
    rows = []
    for filename in sorted(glob.glob(str(pattern))):
        for line in Path(filename).read_text().splitlines():
            if not line.startswith("COUNTERSTATE "):
                continue
            fields = dict(item.split("=", 1) for item in line.split()[1:])
            rows.append(profile(fields["word"], fields["partition"]))
    return rows


def main():
    size14 = parse_counterstate_files(
        SCRATCH / "minimum-projection-through14-cleanability-20260729"
        / "shape7p7-census.txt"
    )
    size15 = parse_counterstate_files(
        SCRATCH / "minimum-projection-size15-exact-frontier-20260729"
        / "7p8-shard16-*.txt"
    )

    fixed_word = "01010123|01012302"
    residual_file = (
        SCRATCH / "unrestricted-support16-interaction-frontier-20260729"
        / "residuals.tsv"
    )
    with residual_file.open() as source:
        size16 = [
            profile(fixed_word, row["partition"])
            for row in csv.DictReader(source, delimiter="\t")
        ]

    expected = (5, 2, 2, 0)
    assert (len(size14), len(size15), len(size16)) == (224, 6036, 8)
    assert all(row == expected for row in size14 + size15 + size16)
    print(f"size-14 direct residuals: {len(size14)} profile={expected}")
    print(f"size-15 direct residuals: {len(size15)} profile={expected}")
    print(f"fixed-word size-16 direct residuals: {len(size16)} profile={expected}")
    print("ALL 6,268 KNOWN DIRECT RESIDUAL ROWS HAVE THE PETERSEN CHARGE CORE")


if __name__ == "__main__":
    main()
