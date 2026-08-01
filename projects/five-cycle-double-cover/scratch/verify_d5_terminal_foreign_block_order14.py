#!/usr/bin/env python3
"""Independent structural verifier for the frozen order-14 b* transcripts.

This verifier deliberately uses only the Python standard library and does not
import any flow, graph, or Kempe-switch code from the C++ audit.  It checks the
cryptographic identity and internal summary arithmetic of the frozen outputs.
It does not independently reperform the mathematical enumeration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


EXPECTED = {
    False: {
        "filename": "order14-ordered.jsonl",
        "sha256": (
            "e928f7a91a2f4235455a93756ae3f6343e20ce051058760a5ba6a9a3ac5d73f5"
        ),
        "summary": {
            "status": "SUMMARY",
            "graphs": 480,
            "flows_mod_s5": 537_418,
            "terminal_plateaus": 33_598,
            "metric_subplateaus": 646_399,
            "failures": 0,
            "endpoint_reversal": 0,
        },
    },
    True: {
        "filename": "order14-symmetric.jsonl",
        "sha256": (
            "4db705e221a7fe08bb71bbbeaa824c7037cff021a62a6a2c7782a3bac5a903a1"
        ),
        "summary": {
            "status": "SUMMARY",
            "graphs": 480,
            "flows_mod_s5": 537_418,
            "terminal_plateaus": 33_598,
            "metric_subplateaus": 643_528,
            "failures": 0,
            "endpoint_reversal": 1,
        },
    },
}

GRAPH_KEYS = {
    "status",
    "index",
    "graph6",
    "flows_mod_s5",
    "terminal_plateaus",
    "metric_subplateaus",
    "failure",
    "first_failure",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json_lines(path: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8", newline="") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.endswith("\n"):
                raise AssertionError(f"{path}:{line_number}: missing final newline")
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise AssertionError(
                    f"{path}:{line_number}: invalid JSON: {error}"
                ) from error
            if not isinstance(record, dict):
                raise AssertionError(f"{path}:{line_number}: expected JSON object")
            records.append(record)
    return records


def verify_transcript(path: Path, endpoint_reversal: bool) -> dict[str, int]:
    expected = EXPECTED[endpoint_reversal]
    actual_hash = sha256(path)
    assert actual_hash == expected["sha256"], (
        f"{path}: SHA-256 mismatch: {actual_hash} != {expected['sha256']}"
    )

    records = load_json_lines(path)
    assert len(records) == 481, f"{path}: expected 481 lines, got {len(records)}"
    graph_records = records[:-1]
    summary = records[-1]
    assert summary == expected["summary"], (
        f"{path}: unexpected summary:\n{summary!r}\n!=\n{expected['summary']!r}"
    )

    graph6_seen: set[str] = set()
    totals = {
        "graphs": 0,
        "flows_mod_s5": 0,
        "terminal_plateaus": 0,
        "metric_subplateaus": 0,
        "failures": 0,
    }
    for expected_index, record in enumerate(graph_records, 1):
        assert set(record) == GRAPH_KEYS, (
            f"{path}:{expected_index}: unexpected keys {set(record) ^ GRAPH_KEYS}"
        )
        assert record["status"] == "GRAPH_DONE"
        assert record["index"] == expected_index
        graph6 = record["graph6"]
        assert isinstance(graph6, str) and graph6
        assert graph6 not in graph6_seen, (
            f"{path}:{expected_index}: duplicate graph6 {graph6!r}"
        )
        graph6_seen.add(graph6)

        for key in ("flows_mod_s5", "terminal_plateaus", "metric_subplateaus"):
            value = record[key]
            assert isinstance(value, int) and not isinstance(value, bool)
            assert value >= 0
            totals[key] += value
        failure = record["failure"]
        assert failure in (0, 1) and not isinstance(failure, bool)
        totals["failures"] += failure
        if failure:
            assert isinstance(record["first_failure"], dict)
        else:
            assert record["first_failure"] is None
        totals["graphs"] += 1

    for key, total in totals.items():
        assert summary[key] == total, (
            f"{path}: accumulated {key}={total}, summary has {summary[key]}"
        )
    assert totals["failures"] == 0
    return totals


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path("output/d5-terminal-foreign-block-potential"),
    )
    arguments = parser.parse_args()

    for endpoint_reversal in (False, True):
        expected = EXPECTED[endpoint_reversal]
        path = arguments.directory / str(expected["filename"])
        totals = verify_transcript(path, endpoint_reversal)
        mode = "symmetric" if endpoint_reversal else "ordered"
        print(
            "PASS",
            mode,
            f"sha256={expected['sha256']}",
            " ".join(f"{key}={value}" for key, value in totals.items()),
        )
    print("PASS all frozen order-14 transcript checks")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        raise SystemExit(1)
