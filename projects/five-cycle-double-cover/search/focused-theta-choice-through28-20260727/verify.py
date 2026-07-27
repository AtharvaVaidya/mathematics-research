#!/usr/bin/env python3
"""Audit the finite prescribed-root perfect-or-theta census through order 28."""

from __future__ import annotations

from math import comb
from pathlib import Path
import hashlib
import json
import re


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
ORDERS = tuple(range(10, 29, 2))
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
EXPECTED = {
    10: (1, "7aec0fba73c081d7eebc551fc46b2484e73e58b2d36718dee105dbb6226e76aa", 75, 60, 15, 15),
    12: (0, EMPTY_SHA256, 0, 0, 0, 0),
    14: (0, EMPTY_SHA256, 0, 0, 0, 0),
    16: (0, EMPTY_SHA256, 0, 0, 0, 0),
    18: (2, "2660e7d5c8a351b4ed3d69f8df316e748e264a630c01328ea4bed43f96f78dfd", 594, 569, 25, 50),
    20: (6, "a65153d9dc38bebffca52b2c2ec05f194807b10ca097f50a551d5aab871244f1", 2_250, 2_183, 67, 101),
    22: (31, "2c3d91e55cb264450cf321e2299355f6cf0f5c2c60a83c99372a1d73ed5a4223", 14_322, 14_047, 275, 613),
    24: (155, "37ef068ab597c6cc882eb2121d9743464b0717bc4beefab4348ef4221b6a7456", 86_490, 85_156, 1_334, 4_449),
    26: (1_297, "1d2b95b9d412f5f6b8ccb788779bd685df23b3239bda8c7e9557266375519760", 859_911, 848_725, 11_186, 43_157),
    28: (12_517, "b4f6494c23793a40158a03ccd7c0943ae2e397c90a1467e27814bd007789be1f", 9_725_709, 9_617_033, 108_676, 512_419),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_independent() -> dict[int, dict[str, object]]:
    results: dict[int, dict[str, object]] = {}
    for name in (
        "independent-replay-through26.json",
        "independent-replay-order28.json",
    ):
        payload = json.loads((ROOT / name).read_text(encoding="utf-8"))
        if payload["classification"] != "PASS":
            raise SystemExit(f"{name}: replay did not pass")
        for row in payload["results"]:
            order = int(row["order"])
            if order in results:
                raise SystemExit(f"{name}: duplicate order {order}")
            results[order] = row
    return results


def main() -> int:
    primary_lines = (
        ROOT / "primary-results.ndjson"
    ).read_text(encoding="utf-8").splitlines()
    if len(primary_lines) != len(ORDERS):
        raise SystemExit("primary result stream has the wrong length")
    primary = {
        int(row["order"]): row for row in map(json.loads, primary_lines)
    }
    if tuple(sorted(primary)) != ORDERS:
        raise SystemExit("primary result orders changed")
    independent = load_independent()
    if tuple(sorted(independent)) != ORDERS:
        raise SystemExit("independent result orders changed")

    totals = {
        "graphs": 0,
        "pairs": 0,
        "def0": 0,
        "def2_theta": 0,
        "def2_all_dumbbell": 0,
        "def2_boundary6": 0,
        "def2_boundary8": 0,
        "near_matchings_checked": 0,
    }
    for order in ORDERS:
        graphs, expected_sha, pairs, def0, theta, near = EXPECTED[order]
        source = ARTIFACTS / f"cyclic4-nontait-order{order}.g6"
        source_data = source.read_bytes()
        rows = source_data.splitlines()
        if len(rows) != graphs or len(set(rows)) != graphs:
            raise SystemExit(f"order {order}: wrong or duplicate source rows")
        if digest(source_data) != expected_sha:
            raise SystemExit(f"order {order}: source digest mismatch")

        # A simple cubic order-n graph has 3n/2 edges.  Every vertex
        # contributes three adjacent edge pairs, and simplicity makes
        # those 3n pairs distinct.
        pairs_per_graph = comb(3 * order // 2, 2) - 3 * order
        if graphs * pairs_per_graph != pairs:
            raise SystemExit(f"order {order}: root-pair arithmetic changed")

        log = (
            ARTIFACTS / f"snarkhunter-order{order}.log"
        ).read_text(encoding="utf-8")
        command = rf"snarkhunter {order} 4 S s C4 o g"
        count = rf"All done, {graphs} graphs generated with {order} vertices\."
        if not re.search(command, log) or not re.search(count, log):
            raise SystemExit(f"order {order}: malformed generator log")

        expected_row = {
            "order": order,
            "graphs": graphs,
            "pairs": pairs,
            "def0": def0,
            "def2_theta": theta,
            "def2_all_dumbbell": 0,
            "def2_boundary6": 0,
            "def2_boundary8": theta,
            "near_matchings_checked": near,
        }
        for implementation, row in (
            ("primary", primary[order]),
            ("independent", independent[order]),
        ):
            for key, value in expected_row.items():
                if row.get(key) != value:
                    raise SystemExit(
                        f"order {order}: {implementation} {key} changed"
                    )
            if implementation == "independent" and row.get(
                "corpus_sha256"
            ) != expected_sha:
                raise SystemExit(
                    f"order {order}: independent source digest changed"
                )

        for key, value in expected_row.items():
            if key in totals:
                totals[key] += value

    expected_totals = {
        "graphs": 14_009,
        "pairs": 10_689_351,
        "def0": 10_567_773,
        "def2_theta": 121_578,
        "def2_all_dumbbell": 0,
        "def2_boundary6": 0,
        "def2_boundary8": 121_578,
        "near_matchings_checked": 560_804,
    }
    if totals != expected_totals:
        raise SystemExit("aggregate counts changed")

    report = {
        "schema": "five-cdc-focused-theta-choice-through28-v1",
        "classification": "FINITE_TWO_IMPLEMENTATION_CENSUS_PASS",
        **expected_totals,
        "orders": list(ORDERS),
        "result": (
            "Every independent root pair either leaves a perfectly "
            "matchable endpoint-deleted graph or admits a maximum "
            "near-perfect matching with a theta complement."
        ),
        "warning": (
            "This is a finite theorem conditional on the documented "
            "Snarkhunter source completeness and option semantics. "
            "It is not a universal theta-choice theorem and not Five-CDC."
        ),
    }
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
