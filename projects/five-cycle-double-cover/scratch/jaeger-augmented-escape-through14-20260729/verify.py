#!/usr/bin/env python3
"""Verify the frozen through-order-14 augmented-escape certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "jaeger-high-girth-local-trap-frontier-20260729"
EXPECTED_EXTERNAL_HASHES = {
    "trap-structures-through14.jsonl":
        "487d32d60f54f119930460e65a53a1f499ce5ed5501601b280d0604a67beb831",
    "verify_blanusa_a_trap.py":
        "aebcf436a32a61fb42e91cce7f24658bf178ab566207b4ab18c4ce22597f2d07",
    "CENSUS-SUMMARY.json":
        "94d30b699974a0acdebfaa540103a7f4db8f6de905691e9cb1b7f624e3ad62cb",
    "AUGMENTED-TRAP-SUMMARY.json":
        "45ffbc85e050105f9a52cc7bfea0ee0105f8c07107f24d11378cdbf41ce6c13f",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def load_final(path: Path):
    final_lines = [
        line for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("FINAL ")
    ]
    assert len(final_lines) == 1
    return json.loads(final_lines[0][len("FINAL "):])


def verify_frozen_output():
    final = load_final(HERE / "audit-output.jsonl")
    expected = {
        "status": "PASS",
        "scope": "complete_canonical_cubic_census_through_order_14",
        "source_rows": 1287,
        "old_objective_traps": 14643,
        "augmented_trap_rows": 187,
        "augmented_traps": 557,
        "distance_histogram": {"2": 557},
        "safe_sources_examined": 659,
        "legal_arcs_examined": 4210,
        "maximum_sources_examined": 4,
    }
    for key, value in expected.items():
        assert final[key] == value, (key, final[key], value)

    results = final["results"]
    assert len(results) == 557
    assert len({
        (result["row"], result["trap_index"]) for result in results
    }) == 557
    assert len({result["row"] for result in results}) == 187
    for result in results:
        assert result["distance"] == 2
        assert result["equal_layer_one"] >= result["sources_examined"] >= 1
        assert result["legal_arcs_examined"] >= 1
        endpoint = result["escape"]
        assert endpoint is not None
        assert (
            tuple(endpoint["endpoint_psi"]) < tuple(result["psi"])
            or endpoint["endpoint_flags"] > 0
        )


def verify_source():
    for name, expected in EXPECTED_EXTERNAL_HASHES.items():
        path = SOURCE / name
        assert path.is_file(), path
        actual = digest(path)
        assert actual == expected, (name, actual, expected)

    rows = [
        json.loads(line)
        for line in (SOURCE / "trap-structures-through14.jsonl")
        .read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(rows) == 1287
    assert sum(len(row["local_traps"]) for row in rows) == 14643

    census = json.loads(
        (SOURCE / "CENSUS-SUMMARY.json").read_text(encoding="utf-8")
    )
    aggregate = census["aggregate"]
    assert aggregate["graphs"] == 419
    assert aggregate["rows"] == 3567
    assert aggregate["states"] == 529150122
    assert aggregate["trap_states"] == 14643


def replay():
    with tempfile.TemporaryDirectory(prefix="fivecdc-through14-") as name:
        replay_path = Path(name) / "audit-output.jsonl"
        with replay_path.open("wb") as handle:
            subprocess.run(
                [sys.executable, str(HERE / "audit.py")],
                check=True,
                stdout=handle,
            )
        expected = (HERE / "audit-output.jsonl").read_bytes()
        actual = replay_path.read_bytes()
        assert actual == expected, (
            f"replay differs: expected sha256={digest(HERE / 'audit-output.jsonl')}, "
            f"actual sha256={digest(replay_path)}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--replay",
        action="store_true",
        help="recompute every neighbourhood and compare output byte-for-byte",
    )
    args = parser.parse_args()
    verify_source()
    verify_frozen_output()
    if args.replay:
        replay()
    print("PASS: frozen through-order-14 augmented-escape certificate")
    print("  source rows: 1,287; old traps: 14,643")
    print("  augmented traps: 557 in 187 rows")
    print("  exact distance histogram: {2: 557}")
    print("  external source hashes: PASS")
    print(f"  full replay: {'PASS' if args.replay else 'not requested'}")


if __name__ == "__main__":
    main()
