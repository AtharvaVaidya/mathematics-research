#!/usr/bin/env python3
"""Independently aggregate the sixteen order-15 anchor census shards."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


EXPECTED_SHARDS = 16
EXPECTED_WORDS = 20_004
EXPECTED_CHARGE_VALID = 26_634_745_428
EXPECTED_INITIALLY_CLEAN = 3_235_970_836
EXPECTED_DIRTY = 23_398_774_592
EXPECTED_ANCHOR_SYSTEMS = 199_816_760_346
EXPECTED_GENERIC_EVALUATIONS = 26_634_725_424
EXPECTED_ROW_DIGEST = (
    "0a227e97a93e36b3063261335755483f2"
    "e6f34cbf7d9a4226e0782917f479c51"
)

RESULT = re.compile(
    r"RESULT order=15"
    r" canonical_words=(?P<canonical_words>\d+)"
    r" shard=(?P<shard>\d+)/(?P<shards>\d+)"
    r" selected_words=(?P<selected_words>\d+)"
    r" charge_valid=(?P<charge_valid>\d+)"
    r" dirty=(?P<dirty>\d+)"
    r" direct_clean=(?P<direct_clean>\d+)"
    r" failures=(?P<failures>\d+)"
    r" anchor_systems=(?P<anchor_systems>\d+)"
    r" anchor_evaluations=(?P<anchor_evaluations>\d+)"
    r" generic_evaluations=(?P<generic_evaluations>\d+)"
    r" seconds=(?P<seconds>[0-9.]+)"
)

INTEGER_FIELDS = (
    "selected_words",
    "charge_valid",
    "dirty",
    "direct_clean",
    "failures",
    "anchor_systems",
    "anchor_evaluations",
    "generic_evaluations",
)


def parse_file(path: Path) -> dict[str, int | str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    matches = [
        match
        for line in lines
        if (match := RESULT.fullmatch(line)) is not None
    ]
    assert len(matches) == 1, (path, len(matches))
    assert not any(line.startswith("COUNTERSTATE ") for line in lines), path
    raw = matches[0].groupdict()
    row: dict[str, int | str] = {
        field: int(raw[field])
        for field in (
            "canonical_words",
            "shard",
            "shards",
            *INTEGER_FIELDS,
        )
    }
    row["seconds"] = raw["seconds"]
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("shards", type=Path, nargs="+")
    args = parser.parse_args()
    assert len(args.shards) == EXPECTED_SHARDS, len(args.shards)

    rows = [parse_file(path) for path in args.shards]
    assert {int(row["shard"]) for row in rows} == set(
        range(EXPECTED_SHARDS)
    )
    assert all(
        int(row["shards"]) == EXPECTED_SHARDS
        and int(row["canonical_words"]) == EXPECTED_WORDS
        for row in rows
    )

    totals = {
        field: sum(int(row[field]) for row in rows)
        for field in INTEGER_FIELDS
    }
    assert totals["selected_words"] == EXPECTED_WORDS
    assert totals["charge_valid"] == EXPECTED_CHARGE_VALID
    assert totals["dirty"] == EXPECTED_DIRTY
    assert (
        totals["charge_valid"] - totals["dirty"]
        == EXPECTED_INITIALLY_CLEAN
    )
    assert totals["failures"] == 0
    assert totals["direct_clean"] == totals["dirty"]
    assert totals["anchor_systems"] == EXPECTED_ANCHOR_SYSTEMS
    assert totals["anchor_evaluations"] == EXPECTED_ANCHOR_SYSTEMS
    assert (
        totals["generic_evaluations"]
        == EXPECTED_GENERIC_EVALUATIONS
    )

    canonical_rows = []
    for row in sorted(rows, key=lambda item: int(item["shard"])):
        canonical_rows.append(
            " ".join(
                f"{field}={row[field]}"
                for field in (
                    "shard",
                    "selected_words",
                    "charge_valid",
                    "dirty",
                    "direct_clean",
                    "failures",
                    "anchor_systems",
                    "anchor_evaluations",
                    "generic_evaluations",
                )
            )
        )
    digest = hashlib.sha256(
        ("\n".join(canonical_rows) + "\n").encode("ascii")
    ).hexdigest()
    assert digest == EXPECTED_ROW_DIGEST

    print(
        "SHARDS"
        f" count={EXPECTED_SHARDS}"
        f" canonical_words={EXPECTED_WORDS}"
        f" selected_words={totals['selected_words']}"
    )
    print(
        "ZSP_AGREEMENT"
        f" charge_valid={totals['charge_valid']}"
        f" initially_clean={totals['charge_valid'] - totals['dirty']}"
        f" dirty={totals['dirty']}"
    )
    print(
        "ANCHOR_CENSUS"
        f" direct_clean={totals['direct_clean']}"
        f" failures={totals['failures']}"
        f" anchor_systems={totals['anchor_systems']}"
        f" anchor_evaluations={totals['anchor_evaluations']}"
        f" generic_evaluations={totals['generic_evaluations']}"
    )
    print(f"SHARD_ROW_SHA256 {digest}")
    print("PASS")


if __name__ == "__main__":
    main()
