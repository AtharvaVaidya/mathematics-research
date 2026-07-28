#!/usr/bin/env python3
"""Audit the retained root-insertion reports without rerunning the census.

This checker compares the C++ producer's NDJSON with the separately written
Python replay reports, verifies the four order-28 shard hashes recorded in
the combined report, and recomputes all displayed aggregate totals.  It is a
publication-consistency checker, not a substitute for the two classifiers.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRATCH = ROOT / "scratch"
FIELDS = (
    "graphs",
    "pairs",
    "deficient",
    "local_witness",
    "local_failure",
    "singleton",
    "singleton_local_witness",
    "singleton_local_failure",
)


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text())


def read_primary() -> dict[int, dict[str, object]]:
    rows = [
        json.loads(line)
        for line in (
            SCRATCH / "focused-local-insertion-result.ndjson"
        ).read_text().splitlines()
        if line
    ]
    by_order = {int(row["order"]): row for row in rows}
    assert sorted(by_order) == list(range(10, 30, 2))
    return by_order


def compare_replay_rows(
    primary: dict[int, dict[str, object]],
    path: Path,
) -> None:
    report = read_json(path)
    assert report["implementation"] == "clean-room-python-bitmask-v1"
    for row in report["results"]:
        order = int(row["order"])
        expected = primary[order]
        for field in FIELDS:
            assert row[field] == expected[field], (
                path.name,
                order,
                field,
                row[field],
                expected[field],
            )
        assert row["first_failure"] == expected["first_failure"]
        assert (
            row["first_singleton_failure"]
            == expected["first_singleton_failure"]
        )


def main() -> None:
    primary = read_primary()
    compare_replay_rows(
        primary, SCRATCH / "root-insertion-independent-through22.json"
    )
    compare_replay_rows(
        primary, SCRATCH / "root-insertion-independent-through26.json"
    )

    combined = read_json(
        SCRATCH / "root-insertion-independent-order28-combined.json"
    )
    assert combined["status"] == "independent-clean-room-replay-pass"
    assert combined["scope"]["order"] == 28
    assert combined["scope"]["shard_count"] == 4

    shard_rows: list[dict[str, object]] = []
    for recorded in combined["shards"]:
        path = ROOT / recorded["file"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == recorded["sha256"]
        report = read_json(path)
        assert report["implementation"] == "clean-room-python-bitmask-v1"
        assert len(report["results"]) == 1
        row = report["results"][0]
        assert row["order"] == 28
        assert row["shard"] == recorded["shard"]
        assert row["shard_count"] == 4
        shard_rows.append(row)

    totals = {
        field: sum(int(row[field]) for row in shard_rows)
        for field in FIELDS
    }
    assert totals == combined["totals"]
    for field in FIELDS:
        assert totals[field] == primary[28][field]
    failures = [
        row["first_failure"]
        for row in shard_rows
        if row["first_failure"]
    ]
    assert min(failures, key=lambda value: int(value.split(":", 1)[0])) == (
        primary[28]["first_failure"]
    )
    assert all(not row["first_singleton_failure"] for row in shard_rows)
    assert combined["comparison"] == {
        "all_totals_match": True,
        "first_failure_matches": True,
        "no_singleton_failure_in_either_implementation": True,
    }

    singleton_total = sum(int(row["singleton"]) for row in primary.values())
    overall = {
        field: sum(int(row[field]) for row in primary.values())
        for field in FIELDS
    }
    assert overall["deficient"] == 121_578
    assert overall["local_witness"] == 119_652
    assert overall["local_failure"] == 1_926
    assert singleton_total == 807
    assert all(
        int(row["singleton_local_failure"]) == 0
        for row in primary.values()
    )

    print(
        json.dumps(
            {
                "status": "PASS",
                "orders": sorted(primary),
                "independently_replayed_orders": sorted(primary),
                "singleton_instances": singleton_total,
                "singleton_local_failures": 0,
                "all_orders": overall,
                "order28": totals,
                "claim_boundary": (
                    "exact finite publication audit only; "
                    "Five-CDC remains unresolved"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
