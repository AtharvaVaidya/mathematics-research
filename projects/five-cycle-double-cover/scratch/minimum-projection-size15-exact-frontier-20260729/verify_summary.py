#!/usr/bin/env python3
"""Aggregate and check the frozen sixteen-way size-15 census."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SHAPES = (
    "4+4+7",
    "4+5+6",
    "5+5+5",
    "4+11",
    "5+10",
    "6+9",
    "7+8",
    "15",
)
SLUG = {shape: shape.replace("+", "p") for shape in SHAPES}
RESULT = re.compile(
    r"^RESULT shape=(?P<shape>\S+)"
    r" canonical_words=(?P<canonical_words>\d+)"
    r" shard=(?P<shard>\d+)/(?P<shards>\d+)"
    r" selected_words=(?P<selected_words>\d+)"
    r" charge_valid=(?P<charge_valid>\d+)"
    r" dirty=(?P<dirty>\d+)"
    r" direct_clean=(?P<direct_clean>\d+)"
    r" delete_branch=(?P<delete_branch>\d+)"
    r" dichotomy_failures=(?P<dichotomy_failures>\d+)$"
)
ANCHOR_RESULT = re.compile(
    r"^RESULT order=15"
    r" canonical_words=(?P<canonical_words>\d+)"
    r" shard=(?P<shard>\d+)/(?P<shards>\d+)"
    r" selected_words=(?P<selected_words>\d+)"
    r" charge_valid=(?P<charge_valid>\d+)"
    r" dirty=(?P<dirty>\d+)"
    r" direct_clean=(?P<direct_clean>\d+)"
    r" failures=(?P<dichotomy_failures>\d+)"
    r" anchor_systems=\d+"
    r" anchor_evaluations=\d+"
    r" generic_evaluations=\d+"
    r" seconds=[0-9.]+$"
)
COUNTERSTATE = re.compile(r"^COUNTERSTATE word=\S+ partition=\d+$")
FIELDS = (
    "selected_words",
    "charge_valid",
    "dirty",
    "direct_clean",
    "delete_branch",
    "dichotomy_failures",
)


def read_shape(shape: str) -> tuple[dict[str, int], list[str]]:
    totals = {field: 0 for field in FIELDS}
    canonical_words = None
    seen_shards: set[int] = set()
    counterstates: list[str] = []
    files = sorted(ROOT.glob(f"{SLUG[shape]}-shard16-*.txt"))
    assert len(files) == 16, (shape, len(files))
    for path in files:
        lines = path.read_text(encoding="utf-8").splitlines()
        pattern = ANCHOR_RESULT if shape == "15" else RESULT
        rows = [pattern.fullmatch(line) for line in lines]
        rows = [row for row in rows if row is not None]
        assert len(rows) == 1, path
        row = rows[0].groupdict()
        if shape != "15":
            assert row["shape"] == shape, (path, row["shape"])
        assert int(row["shards"]) == 16, path
        shard = int(row["shard"])
        assert shard not in seen_shards, (shape, shard)
        seen_shards.add(shard)
        current_words = int(row["canonical_words"])
        if canonical_words is None:
            canonical_words = current_words
        assert canonical_words == current_words, path
        for field in FIELDS:
            if field == "delete_branch" and shape == "15":
                continue
            totals[field] += int(row[field])
        for line in lines:
            if line.startswith("COUNTERSTATE"):
                assert COUNTERSTATE.fullmatch(line), (path, line)
                counterstates.append(line)
    assert seen_shards == set(range(16)), shape
    assert canonical_words is not None
    assert totals["selected_words"] == canonical_words, shape
    if shape == "15":
        assert totals["dichotomy_failures"] == 0, (
            "single-circuit anchor failures require a separate deletion search",
            totals,
        )
    assert totals["dirty"] == (
        totals["direct_clean"]
        + totals["delete_branch"]
        + totals["dichotomy_failures"]
    ), shape
    totals["canonical_words"] = canonical_words
    return totals, counterstates


def main() -> None:
    expected = json.loads((ROOT / "EXPECTED.json").read_text(encoding="utf-8"))
    rows: dict[str, dict[str, int]] = {}
    all_counterstates: list[str] = []
    for shape in SHAPES:
        row, counterstates = read_shape(shape)
        rows[shape] = row
        all_counterstates.extend(counterstates)
        print(
            "SHAPE"
            f" shape={shape}"
            + "".join(f" {field}={row[field]}" for field in (
                "canonical_words",
                "charge_valid",
                "dirty",
                "direct_clean",
                "delete_branch",
                "dichotomy_failures",
            ))
        )
    digest = hashlib.sha256(
        ("\n".join(sorted(all_counterstates)) + "\n").encode()
    ).hexdigest()
    total = {
        field: sum(row[field] for row in rows.values())
        for field in (
            "canonical_words",
            "charge_valid",
            "dirty",
            "direct_clean",
            "delete_branch",
            "dichotomy_failures",
        )
    }
    actual = {
        "shapes": rows,
        "total": total,
        "counterstate_rows": len(all_counterstates),
        "counterstate_sha256": digest,
    }
    assert actual == expected, (
        json.dumps(actual, indent=2, sort_keys=True),
        json.dumps(expected, indent=2, sort_keys=True),
    )
    print(
        "TOTAL"
        + "".join(f" {field}={total[field]}" for field in total)
        + f" counterstate_sha256={digest}"
    )
    print("PASS")


if __name__ == "__main__":
    main()
