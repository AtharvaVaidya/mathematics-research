#!/usr/bin/env python3
"""Check the 13-row certificate for the Petersen four-pole extension lemma."""

from __future__ import annotations

from itertools import combinations, permutations
import json


PORTS = (6, 9, 7, 8)
INTERNAL_EDGES = (
    (1, 4),
    (1, 6),
    (1, 8),
    (2, 5),
    (2, 6),
    (2, 7),
    (4, 7),
    (4, 9),
    (5, 8),
    (5, 9),
)

# boundary labels at PORTS | labels on INTERNAL_EDGES
ROWS = (
    ("01 01 01 01", "01 02 12 01 12 02 12 02 02 12"),
    ("01 01 02 02", "01 02 12 02 12 01 12 02 01 12"),
    ("01 02 01 02", "02 03 23 34 13 14 04 24 03 04"),
    ("01 02 02 01", "34 03 04 01 13 03 23 24 14 04"),
    ("02 01 01 02", "34 03 04 02 23 03 13 14 24 04"),
    ("02 01 02 01", "01 03 13 34 23 24 04 14 03 04"),
    ("02 02 01 01", "02 01 12 01 12 02 12 01 02 12"),
    ("01 01 23 23", "01 02 12 01 12 02 03 13 13 03"),
    ("01 23 01 23", "01 02 12 01 12 02 12 02 13 03"),
    ("01 23 23 01", "01 02 12 01 12 02 03 13 02 12"),
    ("23 01 01 23", "01 02 12 01 03 13 03 13 13 03"),
    ("23 01 23 01", "01 02 12 01 03 13 12 02 02 12"),
    ("23 23 01 01", "01 02 12 01 03 13 03 13 02 12"),
)


def mask(name: str) -> int:
    if len(name) != 2 or name[0] >= name[1]:
        raise AssertionError("noncanonical pair label")
    value = (1 << int(name[0])) | (1 << int(name[1]))
    if value.bit_count() != 2:
        raise AssertionError("bad pair label")
    return value


def transform(value: int, coordinate_permutation: tuple[int, ...]) -> int:
    result = 0
    for coordinate in range(5):
        if value >> coordinate & 1:
            result |= 1 << coordinate_permutation[coordinate]
    return result


def check_assignment(boundary: tuple[int, ...], internal: tuple[int, ...]) -> None:
    if len(boundary) != 4 or len(internal) != len(INTERNAL_EDGES):
        raise AssertionError("wrong assignment length")
    if any(value.bit_count() != 2 for value in boundary + internal):
        raise AssertionError("non-weight-two label")
    at_vertex: dict[int, list[int]] = {vertex: [] for vertex in range(1, 10)}
    at_vertex.pop(3)
    for value, (u, v) in zip(internal, INTERNAL_EDGES, strict=True):
        at_vertex[u].append(value)
        at_vertex[v].append(value)
    for value, vertex in zip(boundary, PORTS, strict=True):
        at_vertex[vertex].append(value)
    if any(len(row) != 3 for row in at_vertex.values()):
        raise AssertionError("internal degree is not three")
    for row in at_vertex.values():
        xor = row[0] ^ row[1] ^ row[2]
        if xor:
            raise AssertionError("internal vertex parity failure")


def main() -> int:
    certificates = tuple(
        (
            tuple(mask(item) for item in boundary.split()),
            tuple(mask(item) for item in internal.split()),
        )
        for boundary, internal in ROWS
    )
    for boundary, internal in certificates:
        check_assignment(boundary, internal)

    labels = tuple(
        (1 << first) | (1 << second)
        for first, second in combinations(range(5), 2)
    )
    coordinate_permutations = tuple(permutations(range(5)))
    targets = 0
    for first in labels:
        for second in labels:
            for boundary in set(permutations((first, first, second, second))):
                targets += 1
                found = False
                for source_boundary, source_internal in certificates:
                    for coordinate_permutation in coordinate_permutations:
                        transformed_boundary = tuple(
                            transform(value, coordinate_permutation)
                            for value in source_boundary
                        )
                        if transformed_boundary != boundary:
                            continue
                        transformed_internal = tuple(
                            transform(value, coordinate_permutation)
                            for value in source_internal
                        )
                        check_assignment(boundary, transformed_internal)
                        found = True
                        break
                    if found:
                        break
                if not found:
                    raise AssertionError(
                        f"uncovered boundary assignment {boundary}"
                    )

    print(
        json.dumps(
            {
                "classification": "EXACT FINITE LOCAL THEOREM",
                "certificate_rows": len(certificates),
                "coordinate_permutations": len(coordinate_permutations),
                "ordered_label_pairs": len(labels) ** 2,
                "boundary_assignments_checked": targets,
                "all_internal_parities_checked": True,
                "all_boundary_assignments_extend": True,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
