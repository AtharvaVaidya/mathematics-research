#!/usr/bin/env python3
"""Reproduce the five-point fixed-fibre SAT census through order 14."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path

import run_jaeger_six_point_frontier as common


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "scratch" / "search_jaeger_five_point_fibre_sat.cpp"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    binary = Path("/tmp") / "jaeger-five-point-frontier"
    common.compile_binary(SOURCE, binary)
    graphs = common.graph_rows()
    with ThreadPoolExecutor(max_workers=arguments.workers) as executor:
        rows = list(
            executor.map(lambda row: common.run_one(binary, row), graphs)
        )
    rows.sort(key=lambda row: (int(row["vertices"]), str(row["graph6"])))
    failures = [row for row in rows if row["status"] != "GRAPH_DONE"]
    summary = {
        "status": "SUMMARY",
        "schema": "jaeger-five-point-fixed-fibre-frontier-v1",
        "classification": "VERIFIED FINITE CASE",
        "scope": (
            "Every feasible Type A or Type B multiplicity fibre in every "
            "connected simple bridgeless cubic graph through order 14."
        ),
        "claim": (
            "Every tested feasible fibre has an Oum pair labelling "
            "supported on at most five of the eight coordinate points."
        ),
        "graphs": len(rows),
        "patterns": sum(int(row["patterns"]) for row in rows),
        "feasible_fibres": sum(
            int(row["feasible_fibres"]) for row in rows
        ),
        "five_point_good_fibres": sum(
            int(row.get("five_point_good_fibres", 0)) for row in rows
        ),
        "failures": len(failures),
        "producer_source": str(SOURCE.relative_to(ROOT)),
        "producer_sha256": digest(SOURCE),
        "included_source_sha256": {
            "scratch/search_jaeger_fixed_fibre_sat.cpp": digest(
                ROOT / "scratch" / "search_jaeger_fixed_fibre_sat.cpp"
            ),
            "scratch/census_jaeger_two_tree_exchange_through14.cpp": digest(
                ROOT
                / "scratch"
                / "census_jaeger_two_tree_exchange_through14.cpp"
            ),
        },
        "cadical_version": "3.0.1",
        "non_resolution_warning": (
            "This finite census is not a proof for arbitrary graphs."
        ),
    }
    text = "\n".join(
        json.dumps(row, sort_keys=True, separators=(",", ":"))
        for row in [*rows, summary]
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(text + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
