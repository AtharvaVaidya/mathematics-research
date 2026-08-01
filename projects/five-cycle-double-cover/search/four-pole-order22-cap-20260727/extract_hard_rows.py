#!/usr/bin/env python3
"""Extract and identity-check the complete order-22 non-Tait hard corpus.

This program deliberately does not decide cyclic edge connectivity.  It
checks that every hard row retained by the frozen Tait filter occurs at its
claimed one-based position in the complete canonical graph6 stream, then
writes those rows in canonical-stream order for an independent cut checker.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_CANONICAL_ROWS = 7_319_447
EXPECTED_CANONICAL_SHA256 = (
    "6d90b02cab31dcd40bbf1de18e36bdc7b4b8515e626bfcb5f2d721b90bf2a41b"
)
EXPECTED_HARD_ROWS = 12_892
EXPECTED_FILTER_SHA256 = (
    "bceb0145309b9b0237231a271e74804db2197628ccccf70ac1f51ee8b6c9beb6"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical_stream", type=Path)
    parser.add_argument("filter_report", type=Path)
    parser.add_argument("hard_output", type=Path)
    parser.add_argument("report_output", type=Path)
    arguments = parser.parse_args()

    canonical_sha = sha256_file(arguments.canonical_stream)
    if canonical_sha != EXPECTED_CANONICAL_SHA256:
        raise SystemExit(
            "canonical stream SHA-256 mismatch: "
            f"{canonical_sha} != {EXPECTED_CANONICAL_SHA256}"
        )
    filter_sha = sha256_file(arguments.filter_report)
    if filter_sha != EXPECTED_FILTER_SHA256:
        raise SystemExit(
            f"filter report SHA-256 mismatch: {filter_sha} "
            f"!= {EXPECTED_FILTER_SHA256}"
        )

    source = json.loads(arguments.filter_report.read_text(encoding="utf-8"))
    if source.get("schema") != "order22-prelaunch-kernel-batch-v1":
        raise SystemExit("unexpected filter-report schema")
    if source.get("mode") != "FILTER_ONLY":
        raise SystemExit("filter report is not a filter-only run")
    if source.get("generated") != EXPECTED_CANONICAL_ROWS:
        raise SystemExit("filter-report canonical count mismatch")
    if source.get("hard_noncolourable") != EXPECTED_HARD_ROWS:
        raise SystemExit("filter-report hard count mismatch")

    hard_rows = source.get("hard_rows")
    if not isinstance(hard_rows, list) or len(hard_rows) != EXPECTED_HARD_ROWS:
        raise SystemExit("malformed hard-row list")
    hard_by_index: dict[int, bytes] = {}
    for position, row in enumerate(hard_rows, start=1):
        if not isinstance(row, dict):
            raise SystemExit(f"hard row {position} is not an object")
        index = row.get("index")
        graph6 = row.get("graph6")
        if not isinstance(index, int) or not isinstance(graph6, str):
            raise SystemExit(f"hard row {position} has malformed fields")
        if index in hard_by_index:
            raise SystemExit(f"duplicate hard-row index {index}")
        try:
            encoded = graph6.encode("ascii")
        except UnicodeEncodeError as error:
            raise SystemExit(f"hard row {position} is not ASCII") from error
        hard_by_index[index] = encoded

    if list(hard_by_index) != sorted(hard_by_index):
        raise SystemExit("hard rows are not in increasing canonical order")

    arguments.hard_output.parent.mkdir(parents=True, exist_ok=True)
    temporary = arguments.hard_output.with_suffix(
        arguments.hard_output.suffix + ".tmp"
    )
    full_rows = 0
    matched_rows = 0
    hard_digest = hashlib.sha256()
    with (
        arguments.canonical_stream.open("rb") as canonical,
        temporary.open("wb") as retained,
    ):
        for full_rows, raw in enumerate(canonical, start=1):
            if len(raw) != 41 or not raw.endswith(b"\n"):
                raise SystemExit(
                    f"canonical row {full_rows} is not a 41-byte record"
                )
            expected = hard_by_index.get(full_rows)
            if expected is None:
                continue
            if raw[:-1] != expected:
                raise SystemExit(
                    f"hard identity mismatch at canonical row {full_rows}"
                )
            retained.write(raw)
            hard_digest.update(raw)
            matched_rows += 1
    if full_rows != EXPECTED_CANONICAL_ROWS:
        raise SystemExit(
            f"canonical row count {full_rows} != {EXPECTED_CANONICAL_ROWS}"
        )
    if matched_rows != EXPECTED_HARD_ROWS:
        raise SystemExit(
            f"matched hard rows {matched_rows} != {EXPECTED_HARD_ROWS}"
        )
    temporary.replace(arguments.hard_output)

    report = {
        "schema": "order22-hard-corpus-identity-audit-v1",
        "canonical_stream": {
            "rows": full_rows,
            "sha256": canonical_sha,
        },
        "filter_report": {
            "sha256": filter_sha,
            "hard_rows": len(hard_rows),
        },
        "hard_corpus": {
            "path": str(arguments.hard_output),
            "rows": matched_rows,
            "sha256": hard_digest.hexdigest(),
        },
        "identity_failures": 0,
    }
    arguments.report_output.parent.mkdir(parents=True, exist_ok=True)
    arguments.report_output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
