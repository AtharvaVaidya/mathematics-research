#!/usr/bin/env python3
"""Independent finite-algebra audit for the rooted vertex/edge split state.

This checker uses only the Python standard library.  It does not import the
SAT census code.  It verifies the local facts used in
``vertex-edge-universal-split-state-frontier.md``:

* cubic D5 states are exactly the triangles of K5;
* 01,01,23,24,34 is a parity-valid five-boundary word;
* quotienting with colours 0 and 1 sent to zero has exact D5 zero fibre
  {01};
* the 23,24,34 star avoids coordinates 0 and 1 and uses each other
  coordinate twice; and
* if an 01 semiedge and one of 23,24,34 terminate at the same cubic
  vertex, no D5 label can complete that vertex.

Optional ``--census-output`` arguments parse the tiny PASS summaries emitted
by ``five-pole-universal-split-state-census.cpp`` and aggregate their record
and target-check counts.  They do not independently replay the SAT work.
"""

from __future__ import annotations

import argparse
from itertools import permutations, product
import json
from pathlib import Path


COLOURS = tuple(range(5))
D5 = tuple(
    (1 << left) | (1 << right)
    for left in COLOURS
    for right in range(left + 1, 5)
)
A = (1 << 0) | (1 << 1)
COMPLEMENT_TRIANGLE = (
    (1 << 2) | (1 << 3),
    (1 << 2) | (1 << 4),
    (1 << 3) | (1 << 4),
)


def pair_name(mask: int) -> str:
    points = [str(point) for point in COLOURS if mask >> point & 1]
    if len(points) != 2:
        raise AssertionError(f"{mask} is not a D5 pair")
    return "".join(points)


def quotient(mask: int) -> int:
    """The linear map pi_A:E5 -> F_2^2 used in the memo.

    Colours 0 and 1 have value 0.  Colours 2,3,4 have values 1,2,3.
    The value of a pair is the xor of the values of its endpoints.
    """

    point_values = (0, 0, 1, 2, 3)
    value = 0
    for point in COLOURS:
        if mask >> point & 1:
            value ^= point_values[point]
    return value


def parse_census_output(path: Path) -> tuple[int, int]:
    fields = path.read_text(encoding="utf-8").strip().split("\t")
    if (
        len(fields) != 5
        or fields[0] != "PASS"
        or fields[1] != "records"
        or fields[3] != "target_checks"
    ):
        raise AssertionError(f"unexpected census summary in {path}")
    records = int(fields[2])
    checks = int(fields[4])
    if records < 0 or checks != 10 * records:
        raise AssertionError(f"inconsistent census totals in {path}")
    return records, checks


def audit() -> dict[str, object]:
    if len(D5) != 10 or len(set(D5)) != 10:
        raise AssertionError("D5 does not have ten distinct pair labels")
    if any(mask.bit_count() != 2 for mask in D5):
        raise AssertionError("D5 contains a non-weight-two mask")

    ordered_states = [
        triple
        for triple in product(D5, repeat=3)
        if triple[0] ^ triple[1] ^ triple[2] == 0
    ]
    if len(ordered_states) != 60:
        raise AssertionError("wrong number of ordered cubic states")
    for triple in ordered_states:
        if len(set(triple)) != 3:
            raise AssertionError("a cubic D5 state repeats a label")
        degrees = [0] * 5
        for mask in triple:
            for point in COLOURS:
                degrees[point] += (mask >> point) & 1
        if sorted(degrees) != [0, 0, 2, 2, 2]:
            raise AssertionError("a cubic state is not a K5 triangle")

    split_words = {
        (A, A, *word) for word in permutations(COMPLEMENT_TRIANGLE)
    }
    if len(split_words) != 6:
        raise AssertionError("triangle ordering orbit has wrong size")
    if any(word[0] ^ word[1] ^ word[2] ^ word[3] ^ word[4]
           for word in split_words):
        raise AssertionError("split boundary word violates cut parity")

    zero_fibre = tuple(mask for mask in D5 if quotient(mask) == 0)
    if zero_fibre != (A,):
        raise AssertionError("quotient zero fibre is not exactly {01}")
    quotient_table = {pair_name(mask): quotient(mask) for mask in D5}
    if set(quotient_table.values()) != {0, 1, 2, 3}:
        raise AssertionError("quotient does not use all F_2^2 values")
    triangle_values = tuple(quotient(mask) for mask in COMPLEMENT_TRIANGLE)
    if set(triangle_values) != {1, 2, 3}:
        raise AssertionError("complement triangle does not map bijectively")

    coordinate_degrees = [
        sum((mask >> point) & 1 for mask in COMPLEMENT_TRIANGLE)
        for point in COLOURS
    ]
    if coordinate_degrees != [0, 0, 2, 2, 2]:
        raise AssertionError("wrong coordinate degrees at the split star")

    repeated_terminal_completions = {
        pair_name(boundary): [
            pair_name(label)
            for label in D5
            if A ^ boundary ^ label == 0
        ]
        for boundary in COMPLEMENT_TRIANGLE
    }
    if any(repeated_terminal_completions.values()):
        raise AssertionError("a forbidden repeated terminal has a completion")
    if any((A ^ boundary).bit_count() != 4
           for boundary in COMPLEMENT_TRIANGLE):
        raise AssertionError("adjacent obstruction is not weight four")

    return {
        "schema": "vertex-edge-split-state-algebra-audit-v1",
        "status": "PASS",
        "d5_labels": [pair_name(mask) for mask in D5],
        "ordered_cubic_states": len(ordered_states),
        "unordered_cubic_triangles": len(ordered_states) // 6,
        "normalized_split_word": ["01", "01", "23", "24", "34"],
        "triangle_orderings": len(split_words),
        "boundary_xor": 0,
        "quotient_table": quotient_table,
        "quotient_zero_fibre": [pair_name(mask) for mask in zero_fibre],
        "split_star_coordinate_degrees": coordinate_degrees,
        "repeated_terminal_completions": repeated_terminal_completions,
        "repeated_terminal_obstruction": (
            "01 xor each of 23,24,34 has weight four, not weight two"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--census-output",
        action="append",
        default=[],
        type=Path,
        help="optional PASS summary from the C++ census (repeatable)",
    )
    arguments = parser.parse_args()
    report = audit()
    if arguments.census_output:
        rows = []
        total_records = 0
        total_checks = 0
        for path in arguments.census_output:
            records, checks = parse_census_output(path)
            rows.append(
                {
                    "path": str(path),
                    "records": records,
                    "target_checks": checks,
                }
            )
            total_records += records
            total_checks += checks
        report["census_summaries"] = rows
        report["census_summary_totals"] = {
            "records": total_records,
            "target_checks": total_checks,
            "scope_warning": (
                "summary parsing only; this does not replay or independently "
                "verify the SAT decisions"
            ),
        }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
