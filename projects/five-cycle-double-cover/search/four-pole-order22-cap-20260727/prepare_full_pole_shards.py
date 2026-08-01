#!/usr/bin/env python3
"""Verify and deterministically shard the complete order-22 cap-pole stream."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_ROWS = 5_956_104
EXPECTED_SHA256 = (
    "cf7a19244912c746c1ef1247a4b45e6ad1df647feaa4251e59db381351b5db46"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output_directory", type=Path)
    arguments = parser.parse_args()

    arguments.output_directory.mkdir(parents=True, exist_ok=True)
    paths = [
        arguments.output_directory / f"input-shard{index}.g6"
        for index in range(8)
    ]
    temporary = [path.with_suffix(".g6.tmp") for path in paths]
    handles = [path.open("wb") for path in temporary]
    full_digest = hashlib.sha256()
    shard_digests = [hashlib.sha256() for _ in range(8)]
    shard_rows = [0] * 8
    rows = 0
    try:
        with arguments.input.open("rb") as source:
            for raw in source:
                rows += 1
                if not raw.endswith(b"\n") or b"\t" in raw or len(raw) <= 1:
                    raise SystemExit(f"malformed graph6 input row {rows}")
                full_digest.update(raw)
                shard = (rows - 1) % 8
                handles[shard].write(raw)
                shard_digests[shard].update(raw)
                shard_rows[shard] += 1
    finally:
        for handle in handles:
            handle.close()

    observed_sha = full_digest.hexdigest()
    if rows != EXPECTED_ROWS:
        raise SystemExit(f"expected {EXPECTED_ROWS} rows, observed {rows}")
    if observed_sha != EXPECTED_SHA256:
        raise SystemExit(
            f"expected input SHA-256 {EXPECTED_SHA256}, observed {observed_sha}"
        )
    for source, destination in zip(temporary, paths, strict=True):
        source.replace(destination)

    report = {
        "schema": "five-cdc-order22-cap-input-shards-v1",
        "input": {
            "rows": rows,
            "sha256": observed_sha,
        },
        "shards": [
            {
                "shard": index,
                "rows": shard_rows[index],
                "sha256": shard_digests[index].hexdigest(),
                "file": paths[index].name,
            }
            for index in range(8)
        ],
    }
    manifest = arguments.output_directory / "input-manifest.json"
    manifest.write_text(
        json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
