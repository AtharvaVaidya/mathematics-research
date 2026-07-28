#!/usr/bin/env python3
"""Verify the frozen order-26/28 cyclic-4 all-seven search reports."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CASES = (
    {
        "order": 26,
        "graphs": 1297,
        "cycles": 16384,
        "input": ROOT
        / "search/focused-theta-choice-through28-20260727/artifacts"
        / "cyclic4-nontait-order26.g6",
        "input_sha256": (
            "1d2b95b9d412f5f6b8ccb788779bd685df23b3239bda8c7e9557266375519760"
        ),
        "results": ROOT
        / "scratch/fano-all-seven-cyclic4-order26-results.jsonl",
        "results_sha256": (
            "8a9c291500f824dc9d2a9805ca1f74fb320abbffe273086ccddb4c301c7eaf84"
        ),
        "bad_sum": 100_753,
        "bad_min": 1,
        "bad_max": 207,
    },
    {
        "order": 28,
        "graphs": 12517,
        "cycles": 32768,
        "input": ROOT
        / "search/focused-theta-choice-through28-20260727/artifacts"
        / "cyclic4-nontait-order28.g6",
        "input_sha256": (
            "b4f6494c23793a40158a03ccd7c0943ae2e397c90a1467e27814bd007789be1f"
        ),
        "results": ROOT
        / "scratch/fano-all-seven-cyclic4-order28-results.jsonl",
        "results_sha256": (
            "54720ae9c2364d5fa0d4044f7469b068f25d81dea6306f4ef0e544f5889d0cfe"
        ),
        "bad_sum": 1_855_709,
        "bad_min": 1,
        "bad_max": 570,
    },
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    for case in CASES:
        assert digest(case["input"]) == case["input_sha256"]
        assert digest(case["results"]) == case["results_sha256"]
        input_rows = tuple(
            row
            for row in case["input"].read_text(encoding="ascii").splitlines()
            if row
        )
        assert len(input_rows) == case["graphs"]
        result_rows = tuple(
            json.loads(row)
            for row in case["results"].read_text(encoding="utf-8").splitlines()
            if row
        )
        assert len(result_rows) == case["graphs"]
        assert all(row["order"] == case["order"] for row in result_rows)
        assert all(row["cycles"] == case["cycles"] for row in result_rows)
        assert all(
            row["all_seven_obstruction"] is False for row in result_rows
        )
        bad_counts = tuple(row["bad"] for row in result_rows)
        assert sum(bad_counts) == case["bad_sum"]
        assert min(bad_counts) == case["bad_min"]
        assert max(bad_counts) == case["bad_max"]
        print(
            f"order {case['order']}: PASS; "
            f"{case['graphs']}/{case['graphs']} retained graphs; "
            "zero all-seven obstructions; "
            f"bad range {case['bad_min']}..{case['bad_max']}"
        )


if __name__ == "__main__":
    main()
