#!/usr/bin/env python3
"""Verify a completed two-implementation order-22 full cap screen."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


EXPECTED_ROWS = 5_956_104
EXPECTED_INPUT_SHA256 = (
    "cf7a19244912c746c1ef1247a4b45e6ad1df647feaa4251e59db381351b5db46"
)
SUMMARY = re.compile(
    r"^SUMMARY implementation=(cadical|csp) mode=exceptional "
    r"rows=(\d+) queries=(\d+) sat=(\d+) hits=(\d+)$"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_summary(path: Path, implementation: str) -> dict[str, int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if any("ERROR" in line for line in lines):
        raise SystemExit(f"{path}: classifier error present")
    matches = [match for line in lines if (match := SUMMARY.fullmatch(line))]
    if len(matches) != 1 or matches[0].group(1) != implementation:
        raise SystemExit(f"{path}: malformed summary")
    match = matches[0]
    return {
        "rows": int(match.group(2)),
        "queries": int(match.group(3)),
        "sat": int(match.group(4)),
        "hits": int(match.group(5)),
    }


def read_audit(path: Path, implementation: str, shard: int) -> dict:
    result = json.loads(path.read_text(encoding="utf-8"))
    for key, expected in {
        "schema": "five-cdc-exceptional-transcript-audit-v1",
        "implementation": implementation,
        "shard": shard,
        "exceptional_rows": 0,
    }.items():
        if result.get(key) != expected:
            raise SystemExit(f"{path}: expected {key}={expected!r}")
    digest = result.get("sha256")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise SystemExit(f"{path}: malformed transcript digest")
    if not isinstance(result.get("rows"), int) or result["rows"] < 0:
        raise SystemExit(f"{path}: malformed row count")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_directory", type=Path)
    arguments = parser.parse_args()
    root = arguments.run_directory

    manifest = json.loads(
        (root / "input-manifest.json").read_text(encoding="utf-8")
    )
    if manifest.get("schema") != "five-cdc-order22-cap-input-shards-v1":
        raise SystemExit("unexpected input-manifest schema")
    if manifest.get("input") != {
        "rows": EXPECTED_ROWS,
        "sha256": EXPECTED_INPUT_SHA256,
    }:
        raise SystemExit("input-manifest aggregate mismatch")
    if len(manifest.get("shards", [])) != 8:
        raise SystemExit("input-manifest shard count mismatch")

    total_rows = 0
    total_queries = 0
    total_sat = 0
    shards = []
    for shard in range(8):
        expected_shard = manifest["shards"][shard]
        if expected_shard.get("shard") != shard:
            raise SystemExit(f"input manifest: wrong shard {shard}")
        input_path = root / expected_shard["file"]
        if sha256_file(input_path) != expected_shard["sha256"]:
            raise SystemExit(f"shard {shard}: input digest mismatch")
        if sum(1 for _ in input_path.open("rb")) != expected_shard["rows"]:
            raise SystemExit(f"shard {shard}: input row-count mismatch")

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
                prefix.with_suffix(".classifier.log"), implementation
            )
            expected_status = (
                f"PASS implementation={implementation} shard={shard}\n"
            )
            if prefix.with_suffix(".status").read_text(
                encoding="utf-8"
            ) != expected_status:
                raise SystemExit(f"{prefix}: malformed PASS marker")
            if audit["rows"] != summary["rows"] or summary["hits"] != 0:
                raise SystemExit(f"shard {shard}: audit/summary mismatch")
            audits[implementation] = audit
            summaries[implementation] = summary
        if audits["cadical"]["sha256"] != audits["csp"]["sha256"]:
            raise SystemExit(f"shard {shard}: transcript digest mismatch")
        if summaries["cadical"] != summaries["csp"]:
            raise SystemExit(f"shard {shard}: implementation summary mismatch")
        summary = summaries["cadical"]
        if summary["rows"] != expected_shard["rows"]:
            raise SystemExit(f"shard {shard}: decision/input row mismatch")
        total_rows += summary["rows"]
        total_queries += summary["queries"]
        total_sat += summary["sat"]
        shards.append(
            {
                "shard": shard,
                **summary,
                "transcript_sha256": audits["cadical"]["sha256"],
                "input_sha256": expected_shard["sha256"],
            }
        )

    if total_rows != EXPECTED_ROWS:
        raise SystemExit("aggregate row count mismatch")
    result = {
        "schema": "five-cdc-order22-full-cap-screen-v1",
        "classification": "FINITE INDEPENDENT EXACT ENUMERATION",
        "rows": total_rows,
        "queries_per_implementation": total_queries,
        "sat_per_implementation": total_sat,
        "exceptional_hits": 0,
        "input_sha256": EXPECTED_INPUT_SHA256,
        "shards": shards,
        "theorem": (
            "No independent-edge deletion of any bridgeless non-Tait "
            "connected simple cubic graph of order 22 has either exceptional "
            "exact boundary signature in the fixed five-colour D5 model."
        ),
        "warning": (
            "This finite theorem is restricted to bridge-free connected "
            "simple terminal-distinct order-22 four-poles via the separately "
            "proved cap reduction. It is not a universal exceptional-pole "
            "theorem and does not resolve Five-CDC."
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
