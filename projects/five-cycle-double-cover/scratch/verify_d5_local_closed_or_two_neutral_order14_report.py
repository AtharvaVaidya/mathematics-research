#!/usr/bin/env python3
"""Verify the frozen order-14 boundary-size feature census."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path


REPORT = Path(__file__).with_name(
    "d5-local-closed-or-two-neutral-order14.jsonl"
)
EXPECTED_SHA256 = (
    "f9ceb777a4d99a46b035aeda6167ee6fc1e57467feb96f9606154a9962a64899"
)


def geng_path() -> str | None:
    for candidate in (
        shutil.which("geng"),
        "/opt/homebrew/bin/geng",
        "/usr/local/bin/geng",
    ):
        if candidate and Path(candidate).is_file():
            return candidate
    return None


def minimum_boundary_size(key: str) -> int:
    prefix = "boundary_sizes="
    assert key.startswith(prefix)
    first = key[len(prefix):].split(",", 1)[0]
    return int(first)


def main() -> int:
    raw = REPORT.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == EXPECTED_SHA256, (EXPECTED_SHA256, digest)
    rows = [
        json.loads(line)
        for line in raw.decode("utf-8").splitlines()
        if line
    ]
    graph_rows, summary = rows[:-1], rows[-1]
    assert len(graph_rows) == 480
    graph6_records = []
    for index, row in enumerate(graph_rows, 1):
        assert row["status"] == "GRAPH_DONE"
        assert row["index"] == index
        assert row["vertices"] == 14
        assert row["local_edge_pair_triples"] == 42 * row["flows_mod_s5"]
        assert row["no_closed_fewer_than_two_neutral_failures"] == 0
        assert row["boundary_two_nonzero_failures"] == 0
        assert row["first_failure"] is None
        graph6_records.append(row["graph6"])

    assert summary["status"] == "SUMMARY"
    assert summary["graphs"] == 480
    assert summary["flows_mod_s5"] == 537418
    assert summary["local_edge_pair_triples"] == 22571556
    assert summary["no_closed_candidate"] == 182446
    assert summary["no_closed_fewer_than_two_neutral_failures"] == 0
    assert summary["boundary_two_nonzero_failures"] == 0
    for field in (
        "flows_mod_s5",
        "local_edge_pair_triples",
        "no_closed_candidate",
        "no_closed_fewer_than_two_neutral_failures",
        "boundary_two_nonzero_failures",
    ):
        assert summary[field] == sum(row[field] for row in graph_rows)

    triple_histogram = summary["feature_histogram"]
    assert sum(triple_histogram.values()) == 22571556
    assert all(
        minimum_boundary_size(key) <= 2 for key in triple_histogram
    )
    no_closed_from_histogram = sum(
        count
        for key, count in triple_histogram.items()
        if minimum_boundary_size(key) != 0
    )
    assert no_closed_from_histogram == 182446

    switch_histogram = summary["switch_feature_histogram"]
    assert sum(switch_histogram.values()) == 3 * 22571556
    boundary_two_rows = {
        key: count
        for key, count in switch_histogram.items()
        if key.startswith("boundary_size=2;")
    }
    assert boundary_two_rows == {
        "boundary_size=2;delta=0": 13368874
    }

    geng = geng_path()
    if geng is not None:
        generated = subprocess.run(
            [geng, "-Cq", "-d3", "-D3", "14"],
            check=True,
            stdout=subprocess.PIPE,
            text=True,
            encoding="ascii",
        ).stdout.splitlines()
        assert graph6_records == generated
        graph_sequence = "regenerated and matched"
    else:
        graph_sequence = "not regenerated (geng unavailable)"

    print("PASS")
    print(f"report sha256: {EXPECTED_SHA256}")
    print("local triples: 22571556")
    print("triples with no closed candidate: 182446")
    print("boundary-size-two switches: 13368874; nonneutral: 0")
    print("minimum local boundary size greater than two: 0")
    print(f"canonical graph sequence: {graph_sequence}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
