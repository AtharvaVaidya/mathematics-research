#!/usr/bin/env python3
"""Verify a completed two-implementation rooted order-17 screen."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


EXPECTED_GRAPHS = 654_676
SUMMARY = re.compile(
    r"^SUMMARY implementation=(cadical|csp) graphs=(\d+) "
    r"nonbridge_roots=(\d+) empty=(\d+) closed=(\d+) "
    r"violations=(\d+) calls=(\d+)$"
)


def read_summary(path: Path, implementation: str) -> dict[str, int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if any("ERROR" in line for line in lines):
        raise SystemExit(f"{path}: classifier error present")
    matches = [match for line in lines if (match := SUMMARY.fullmatch(line))]
    if len(matches) != 1 or matches[0].group(1) != implementation:
        raise SystemExit(f"{path}: malformed summary")
    match = matches[0]
    return {
        "graphs": int(match.group(2)),
        "nonbridge_roots": int(match.group(3)),
        "empty": int(match.group(4)),
        "closed": int(match.group(5)),
        "violations": int(match.group(6)),
        "calls": int(match.group(7)),
    }


def read_audit(path: Path, implementation: str, shard: int) -> dict:
    result = json.loads(path.read_text(encoding="utf-8"))
    for key, expected in {
        "schema": "five-cdc-rooted-base-pair-transcript-audit-v1",
        "implementation": implementation,
        "shard": shard,
        "violations": 0,
    }.items():
        if result.get(key) != expected:
            raise SystemExit(f"{path}: expected {key}={expected!r}")
    digest = result.get("sha256")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise SystemExit(f"{path}: malformed digest")
    for key in ("rows", "empty", "closed"):
        if not isinstance(result.get(key), int) or result[key] < 0:
            raise SystemExit(f"{path}: invalid {key}")
    if result["empty"] + result["closed"] != result["rows"]:
        raise SystemExit(f"{path}: audit accounting mismatch")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_directory", type=Path)
    args = parser.parse_args()
    root = args.run_directory

    totals = {
        "graphs": 0,
        "nonbridge_roots": 0,
        "empty": 0,
        "closed": 0,
        "violations": 0,
        "calls": 0,
    }
    shards = []
    for shard in range(8):
        audits = {}
        summaries = {}
        for implementation in ("cadical", "csp"):
            prefix = root / f"{implementation}-shard{shard}"
            audit = read_audit(
                prefix.with_suffix(".transcript.audit.json"),
                implementation,
                shard,
            )
            summary = read_summary(
                prefix.with_suffix(".classifier.log"),
                implementation,
            )
            status = prefix.with_suffix(".status").read_text(encoding="utf-8")
            if status != f"PASS implementation={implementation} shard={shard}\n":
                raise SystemExit(f"{prefix}: malformed PASS marker")
            if prefix.with_suffix(".geng.log").read_bytes():
                raise SystemExit(f"{prefix}: unexpected generator output")
            if {
                "rows": summary["nonbridge_roots"],
                "empty": summary["empty"],
                "closed": summary["closed"],
                "violations": summary["violations"],
            } != {
                key: audit[key]
                for key in ("rows", "empty", "closed", "violations")
            }:
                raise SystemExit(f"shard {shard}: summary/audit mismatch")
            audits[implementation] = audit
            summaries[implementation] = summary
        if audits["cadical"]["sha256"] != audits["csp"]["sha256"]:
            raise SystemExit(f"shard {shard}: transcript digest mismatch")
        if summaries["cadical"] != summaries["csp"]:
            raise SystemExit(f"shard {shard}: implementation summary mismatch")
        summary = summaries["cadical"]
        for key in totals:
            totals[key] += summary[key]
        shards.append(
            {
                "shard": shard,
                **summary,
                "transcript_sha256": audits["cadical"]["sha256"],
            }
        )
    if totals["graphs"] != EXPECTED_GRAPHS:
        raise SystemExit(
            f"expected {EXPECTED_GRAPHS} graphs, observed {totals['graphs']}"
        )
    if totals["violations"] != 0:
        raise SystemExit("aggregate base-pair violation present")

    result = {
        "schema": "five-cdc-rooted-base-pair-order17-v1",
        "classification": "FINITE INDEPENDENT EXACT ENUMERATION",
        "order": 17,
        **totals,
        "shards": shards,
        "theorem": (
            "Every nonempty nonbridge rooted signature of a connected "
            "simple cubic three-pole through order 17 contains one of "
            "the three base pairs."
        ),
        "warning": (
            "This finite theorem is not universal base-pair closure and "
            "does not resolve the exceptional-signature or Five-Cycle "
            "Double Cover conjectures."
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
