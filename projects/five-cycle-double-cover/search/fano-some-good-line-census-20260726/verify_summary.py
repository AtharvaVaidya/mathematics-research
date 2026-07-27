#!/usr/bin/env python3
"""Verify the frozen some-good-line census summary.

The default check independently replays the complete Python census through
order 12 and the retained strict-snark controls through order 18.  Pass
--full to regenerate the complete C++ census through order 18 and all
targeted rows through order 26.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CPP = ROOT / "scratch" / "fano_all_bad_projection_search.cpp"
PYTHON = ROOT / "scratch" / "search_fano_all_bad_projection_subspaces.py"


def compile_cpp(directory: Path) -> Path:
    compiler = shutil.which("c++")
    if compiler is None:
        raise SystemExit("C++ compiler not found")
    binary = directory / "fano-all-bad"
    subprocess.run(
        [compiler, "-O3", "-std=c++20", str(CPP), "-o", str(binary)],
        check=True,
    )
    return binary


def run_cpp_file(binary: Path, path: Path) -> list[dict[str, object]]:
    process = subprocess.run(
        [str(binary), str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return [json.loads(row) for row in process.stdout.splitlines() if row]


def run_cpp_geng(
    binary: Path, geng: str, order: int
) -> list[dict[str, object]]:
    generator = subprocess.Popen(
        [geng, "-cq", "-d3", "-D3", str(order)],
        stdout=subprocess.PIPE,
        text=True,
    )
    assert generator.stdout is not None
    classifier = subprocess.run(
        [str(binary), "/dev/stdin"],
        stdin=generator.stdout,
        check=True,
        capture_output=True,
        text=True,
    )
    generator.stdout.close()
    assert generator.wait() == 0
    return [
        json.loads(row)
        for row in classifier.stdout.splitlines()
        if row
    ]


def profile(rows: list[dict[str, object]]) -> tuple[int, int, list[dict[str, int]]]:
    bridgeless = [row for row in rows if not row.get("skipped")]
    counts = Counter(
        (
            int(row["bad"]),
            int(row["liftable_bad"]),
            int(row["liftable_bad_rank"]),
        )
        for row in bridgeless
    )
    result = [
        {
            "bad": bad,
            "graphs": graphs,
            "liftable_bad": liftable_bad,
            "liftable_bad_rank": rank,
        }
        for (bad, liftable_bad, rank), graphs in sorted(counts.items())
    ]
    assert not any(bool(row["all_seven_obstruction"]) for row in bridgeless)
    return len(rows), len(bridgeless), result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    arguments = parser.parse_args()
    summary = json.loads(
        (HERE / "SUMMARY.json").read_text(encoding="utf-8")
    )
    expected_by_order = {
        row["order"]: row
        for row in summary["complete_connected_simple_cubic_census"]
    }
    assert set(expected_by_order) == set(range(4, 19, 2))
    for row in expected_by_order.values():
        assert sum(item["graphs"] for item in row["profiles"]) == row["bridgeless_graphs"]
        assert row["all_seven_obstructions"] == 0

    # Independently written Python semantics on the complete small boundary.
    maximum = 16 if arguments.full else 12
    process = subprocess.run(
        [
            "python3",
            str(PYTHON),
            "--min-order",
            "4",
            "--max-order",
            str(maximum),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    python_rows = [
        json.loads(row) for row in process.stdout.splitlines() if row
    ]
    for observed in python_rows:
        expected = expected_by_order[observed["order"]]
        assert observed["connected_cubic_graphs"] == expected["connected_cubic_graphs"]
        assert observed["bridgeless_graphs"] == expected["bridgeless_graphs"]
        observed_pairs = {
            tuple(map(int, key.replace("_total", "").replace("_liftable", "").split("/"))): value
            for key, value in observed["bad_projection_count_histogram"].items()
        }
        expected_pairs = {
            (row["bad"], row["liftable_bad"]): row["graphs"]
            for row in expected["profiles"]
        }
        assert observed_pairs == expected_pairs

    geng = shutil.which("geng")
    if geng is None:
        raise SystemExit("nauty-geng not found")
    with tempfile.TemporaryDirectory(prefix="fano-census-") as directory:
        binary = compile_cpp(Path(directory))

        controls = run_cpp_file(
            binary,
            ROOT
            / "search"
            / "order22-filter-census-20260725"
            / "strict-snarks-through18.g6",
        )
        assert [
            (
                row["order"],
                row["bad"],
                row["liftable_bad"],
                row["liftable_bad_rank"],
                row["all_seven_obstruction"],
            )
            for row in controls
        ] == [
            (10, 7, 6, 5, False),
            (18, 5, 4, 3, False),
            (18, 9, 8, 5, False),
        ]

        if arguments.full:
            for order in range(4, 19, 2):
                rows = run_cpp_geng(binary, geng, order)
                generated, bridgeless, profiles = profile(rows)
                expected = expected_by_order[order]
                assert generated == expected["connected_cubic_graphs"]
                assert bridgeless == expected["bridgeless_graphs"]
                assert profiles == expected["profiles"]

            targets = (
                (
                    ROOT / "search" / "order22-filter-census-20260725"
                    / "strict-snarks-order20.g6",
                    6,
                ),
                (
                    ROOT / "search" / "order22-filter-census-20260725"
                    / "strict-snarks-order22.g6",
                    20,
                ),
                (
                    ROOT / "search" / "fano-flow-one-switch-frontier-20260726"
                    / "strict-snarks-order24.g6",
                    38,
                ),
                (
                    ROOT / "berge-fulkerson" / "search" / "snark_frontier"
                    / "data" / "n26-cyclic5.g6",
                    10,
                ),
            )
            for path, expected_count in targets:
                rows = run_cpp_file(binary, path)
                assert len(rows) == expected_count
                assert not any(row["all_seven_obstruction"] for row in rows)

    print("Fano some-good-line census summary: PASS")
    print(f"independent_python_complete_through={maximum}")
    print("strict_controls_through18=3")
    print(f"full_replay={arguments.full}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
