#!/usr/bin/env python3
"""Independent parser/check of the frozen size-14/15/16 residual rows."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


AUDIT_DIR = Path(__file__).resolve().parent
SCRATCH = AUDIT_DIR.parent
COUNTERSTATE = re.compile(
    r"^COUNTERSTATE word=([0-3]+)\|([0-3]+) partition=([0-9]+)$"
)


def xor_sum(values):
    answer = 0
    for value in values:
        answer ^= value
    return answer


def subset_span(vectors):
    span = {0}
    for vector in vectors:
        span |= {old ^ vector for old in tuple(span)}
    return frozenset(span)


def classify(words, labels):
    assert len(words) == 2
    assert sum(map(len, words)) == len(labels)
    block_labels = sorted(set(labels))
    assert block_labels == list(range(len(block_labels)))

    charge = [[0, 0] for _ in block_labels]
    cursor = 0
    for circuit, word in enumerate(words):
        values = tuple(map(int, word))
        for position, value in enumerate(values):
            derivative = values[position - 1] ^ value
            assert derivative in (1, 2, 3)
            charge[labels[cursor + position]][circuit] ^= derivative
        cursor += len(values)

    assert all(xor_sum(row) == 0 for row in charge)
    assert all(xor_sum(row[j] for row in charge) == 0 for j in range(2))
    assert all(left == right != 0 for left, right in charge)

    vectors = tuple(left for left, _right in charge)
    span_size = len(subset_span(vectors))
    assert span_size in (1, 2, 4)
    rank = span_size.bit_length() - 1
    kernel_dimension = len(vectors) - rank
    excess_nullity = kernel_dimension - 1
    multiplicities = tuple(sorted(Counter(vectors).values()))
    return len(vectors), rank, excess_nullity, multiplicities


def read_counterstates(path):
    answer = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.startswith("COUNTERSTATE"):
            continue
        match = COUNTERSTATE.fullmatch(line)
        assert match is not None, (path, line_number, line)
        left, right, labels = match.groups()
        answer.append(classify((left, right), tuple(map(int, labels))))
    return answer


def read_size16_partitions(path):
    lines = path.read_text().splitlines()
    headings = lines[0].split("\t")
    partition_column = headings.index("partition")
    answer = []
    fixed_words = ("01010123", "01012302")
    for line in lines[1:]:
        fields = line.split("\t")
        assert len(fields) == len(headings)
        answer.append(
            classify(fixed_words, tuple(map(int, fields[partition_column])))
        )
    return answer


def main():
    size14_path = (
        SCRATCH / "minimum-projection-through14-cleanability-20260729"
        / "shape7p7-census.txt"
    )
    size15_paths = sorted(
        (SCRATCH / "minimum-projection-size15-exact-frontier-20260729").glob(
            "7p8-shard16-*.txt"
        )
    )
    size16_path = (
        SCRATCH / "unrestricted-support16-interaction-frontier-20260729"
        / "residuals.tsv"
    )
    assert len(size15_paths) == 16

    families = {
        "size14": read_counterstates(size14_path),
        "size15": [row for path in size15_paths for row in read_counterstates(path)],
        "size16": read_size16_partitions(size16_path),
    }
    expected_profile = (5, 2, 2, (1, 1, 3))
    assert tuple(map(len, families.values())) == (224, 6036, 8)
    for name, rows in families.items():
        assert all(row == expected_profile for row in rows), name
        print(f"{name}: rows={len(rows)} profile={expected_profile}")
    print("INDEPENDENT PARSE PASSED FOR ALL 6,268 FROZEN RESIDUAL ROWS")


if __name__ == "__main__":
    main()
