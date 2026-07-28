#!/usr/bin/env python3
"""Compact integrity and aggregate verifier for the order-30 package.

This checker does not redo the expensive matching census.  It checks the
retained corpus, every recorded hash, the primary result, all sixteen
independent shard reports, and their exact aggregate agreement.  Use
independent_verifier.py as described in REPRODUCING.md for a clean-room
semantic replay.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
REPORT = json.loads((ROOT / "report.json").read_text())


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes())


def decode_graph6(record: bytes) -> list[int]:
    if not record or record[0] >= 126:
        raise AssertionError("only nonempty short graph6 is retained")
    order = record[0] - 63
    bits: list[int] = []
    for byte in record[1:]:
        value = byte - 63
        if not 0 <= value < 64:
            raise AssertionError("invalid graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [0] * order
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1
    return adjacency


def main() -> None:
    corpus_path = ARTIFACTS / "Generated_graphs.30.04.sn.cyc4.g6.gz"
    compressed = corpus_path.read_bytes()
    if sha256(compressed) != REPORT["corpus"]["gzip_sha256"]:
        raise AssertionError("compressed corpus hash mismatch")
    decompressed = gzip.decompress(compressed)
    if sha256(decompressed) != REPORT["corpus"]["decompressed_sha256"]:
        raise AssertionError("decompressed corpus hash mismatch")
    records = decompressed.splitlines()
    if len(records) != REPORT["corpus"]["graphs"]:
        raise AssertionError("corpus row count mismatch")
    if len(set(records)) != len(records):
        raise AssertionError("duplicate graph6 records")
    for record in records:
        adjacency = decode_graph6(record)
        if len(adjacency) != 30:
            raise AssertionError("wrong graph order")
        if any(row.bit_count() != 3 for row in adjacency):
            raise AssertionError("corpus row is not simple cubic")
        if sum(row.bit_count() for row in adjacency) != 90:
            raise AssertionError("wrong edge count")

    primary_spec = REPORT["primary"]
    for key in ("source", "result", "log"):
        if file_sha256(ROOT / primary_spec[key]) != primary_spec[f"{key}_sha256"]:
            raise AssertionError(f"primary {key} hash mismatch")
    independent_spec = REPORT["independent_replay"]
    if (
        file_sha256(ROOT / independent_spec["source"])
        != independent_spec["source_sha256"]
    ):
        raise AssertionError("independent source hash mismatch")

    agreed = REPORT["agreed_totals"]
    expected = {
        "graphs": agreed["graphs"],
        "pairs": agreed["independent_root_pairs"],
        "def0": agreed["deficiency_zero"],
        "def2_theta": agreed["deficiency_two_theta"],
        "def2_all_dumbbell": agreed["deficiency_two_all_dumbbell"],
        "def2_boundary6": agreed["deficiency_two_boundary_six"],
        "def2_boundary8": agreed["deficiency_two_boundary_eight"],
        "near_matchings_checked": (
            agreed["near_perfect_matchings_checked_until_first_theta"]
        ),
    }
    primary = json.loads((ROOT / primary_spec["result"]).read_text())
    for key, value in expected.items():
        if primary[key] != value:
            raise AssertionError(f"primary total mismatch: {key}")
    if primary["first_witness"]:
        raise AssertionError("primary unexpectedly retained an all-dumbbell witness")

    totals = {key: 0 for key in expected}
    seen_indices = set()
    for shard_index in range(independent_spec["shard_count"]):
        path = ARTIFACTS / "independent" / f"shard-{shard_index}.json"
        recorded_hash = independent_spec["result_sha256_by_shard"][
            str(shard_index)
        ]
        if file_sha256(path) != recorded_hash:
            raise AssertionError(f"independent shard {shard_index} hash mismatch")
        report = json.loads(path.read_text())
        if report["classification"] != "PASS" or len(report["results"]) != 1:
            raise AssertionError(f"independent shard {shard_index} did not pass")
        result = report["results"][0]
        if result["shard_index"] != shard_index or result["shard_count"] != 16:
            raise AssertionError("bad shard metadata")
        if result["corpus_sha256"] != REPORT["corpus"]["decompressed_sha256"]:
            raise AssertionError("shard corpus hash mismatch")
        if result["source_graphs"] != REPORT["corpus"]["graphs"]:
            raise AssertionError("shard source graph count mismatch")
        seen_indices.add(shard_index)
        for key in totals:
            totals[key] += result[key]
    if seen_indices != set(range(16)):
        raise AssertionError("missing shard")
    if totals != expected:
        raise AssertionError(f"independent aggregate mismatch: {totals!r}")

    print(json.dumps({
        "schema": "focused-theta-choice-order30-package-verifier-v1",
        "status": "PASS",
        "corpus_records": len(records),
        "shards": len(seen_indices),
        "agreed_totals": expected,
        "warning": REPORT["warning"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
