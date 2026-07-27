#!/usr/bin/env python3
"""Streaming independent audit for rooted base-pair decision rows."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys


GRAPH6 = re.compile(rb"^[?-~]+$")
BASE_PAIRS = (0x0C, 0x12, 0x21)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--implementation", choices=("cadical", "csp"), required=True)
    parser.add_argument("--shard", type=int, required=True)
    args = parser.parse_args()
    if not 0 <= args.shard < 8:
        raise SystemExit("shard must lie in [0,7]")

    digest = hashlib.sha256()
    rows = 0
    empty = 0
    closed = 0
    violations = 0
    previous_record: bytes | None = None
    previous_root = -1
    for raw in sys.stdin.buffer:
        rows += 1
        digest.update(raw)
        if not raw.endswith(b"\n"):
            raise SystemExit(f"row {rows}: missing newline")
        fields = raw[:-1].split(b"\t")
        if len(fields) != 5:
            raise SystemExit(f"row {rows}: expected five tab-separated fields")
        record, root_text, category_text, queried_text, observed_text = fields
        if not GRAPH6.fullmatch(record):
            raise SystemExit(f"row {rows}: malformed graph6 record")
        try:
            root = int(root_text)
            category = int(category_text)
            queried = int(queried_text, 16)
            observed = int(observed_text, 16)
        except ValueError as error:
            raise SystemExit(f"row {rows}: malformed numeric field") from error
        if root < 0 or category not in {0, 1, 2}:
            raise SystemExit(f"row {rows}: invalid root or category")
        if queried >= 1 << 7 or observed >= 1 << 7:
            raise SystemExit(f"row {rows}: orbit mask outside seven-state universe")
        if observed & ~queried:
            raise SystemExit(f"row {rows}: observed orbit was not queried")
        if record == previous_record:
            if root <= previous_root:
                raise SystemExit(f"row {rows}: non-increasing root sequence")
        else:
            previous_record = record
            previous_root = -1
        previous_root = root

        contains_base = any(observed & base == base for base in BASE_PAIRS)
        if category == 0:
            if observed != 0 or queried != 0x7F:
                raise SystemExit(f"row {rows}: malformed empty decision")
            empty += 1
        elif category == 1:
            if not contains_base:
                raise SystemExit(f"row {rows}: closed decision lacks a base pair")
            closed += 1
        else:
            if observed == 0 or queried != 0x7F or contains_base:
                raise SystemExit(f"row {rows}: malformed violation decision")
            violations += 1
            raise SystemExit(f"row {rows}: base-pair violation present")

    result = {
        "schema": "five-cdc-rooted-base-pair-transcript-audit-v1",
        "implementation": args.implementation,
        "shard": args.shard,
        "rows": rows,
        "empty": empty,
        "closed": closed,
        "violations": violations,
        "sha256": digest.hexdigest(),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
