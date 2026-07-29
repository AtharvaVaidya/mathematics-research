#!/usr/bin/env python3
"""Freeze the complete simple cubic parallel-odd selector census through 16."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE
SOURCE_NAMES = (
    "census_jaeger_two_tree_exchange_through14.cpp",
    "search_six_point_star_perpacking_parity.cpp",
    "search_six_point_star_perpacking_parity_sat.cpp",
)
SOURCES = tuple(PACKAGE / "source" / name for name in SOURCE_NAMES)
DEFAULT_OUTPUT = PACKAGE.parent / "six-point-parallel-selector-through16-replay"
EXPECTED = {4: 1, 6: 2, 8: 5, 10: 18, 12: 81, 14: 480, 16: 3874}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def generate_graphs() -> tuple[tuple[int, str], ...]:
    answer = []
    for order, expected in EXPECTED.items():
        process = subprocess.run(
            ["geng", "-q", "-C", "-d3", "-D3", str(order)],
            text=True,
            capture_output=True,
            check=True,
        )
        graphs = tuple(sorted(process.stdout.splitlines()))
        assert len(graphs) == expected
        answer.extend((order, graph) for graph in graphs)
    return tuple(answer)


def compile_producer(binary: Path) -> None:
    subprocess.run(
        [
            "/usr/bin/clang++",
            "-O3",
            "-std=c++20",
            "-I/opt/homebrew/include",
            str(SOURCES[-1]),
            "/opt/homebrew/lib/libcadical.a",
            "-o",
            str(binary),
        ],
        cwd=ROOT,
        check=True,
    )


def run_graph(binary: Path, item: tuple[int, str]) -> dict[str, object]:
    order, graph6 = item
    process = subprocess.run(
        [str(binary), graph6, "--parallel-odd"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if process.returncode not in (0, 2):
        raise RuntimeError(
            f"producer failed on {graph6!r}: {process.returncode}\n"
            f"{process.stderr}\n{process.stdout}"
        )
    row = json.loads(process.stdout)
    assert row["graph6"] == graph6 and int(row["vertices"]) == order
    assert row["selector"] == "parallel-odd"
    assert (process.returncode == 2) == (row["status"] == "COUNTERMODEL")
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()
    output = arguments.output.resolve()
    if output.exists():
        raise ValueError(f"refusing to overwrite {output}")
    output.mkdir(parents=True)
    source_dir = output / "source"
    source_dir.mkdir()
    for source in SOURCES:
        shutil.copy2(source, source_dir / source.name)

    graph_items = generate_graphs()
    graphs_path = output / "graphs.g6"
    graphs_path.write_text(
        "".join(f"{order}\t{graph}\n" for order, graph in graph_items),
        encoding="ascii",
    )

    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="six-point-parallel-through16-") as raw:
        binary = Path(raw) / "producer"
        compile_producer(binary)
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=arguments.workers
        ) as executor:
            rows = list(executor.map(
                lambda item: run_graph(binary, item), graph_items
            ))
    rows.sort(key=lambda row: (int(row["vertices"]), str(row["graph6"])))

    by_order = {}
    for order in EXPECTED:
        selected = [row for row in rows if int(row["vertices"]) == order]
        by_order[str(order)] = {
            "graphs": len(selected),
            "feasible_star_fibres": sum(
                sum(bool(root["feasible"]) for root in row["roots"])
                for row in selected
            ),
            "parallel_odd_witness_star_fibres": sum(
                sum(bool(root["has_odd_packing"]) for root in row["roots"])
                for row in selected
            ),
        }

    summary = {
        "schema": "six-point-parallel-selector-through16-v1",
        "status": (
            "COUNTERMODEL_FOUND"
            if any(row["status"] == "COUNTERMODEL" for row in rows)
            else "NO_COUNTERMODEL_THROUGH_BOUND"
        ),
        "classification": "EXACT FINITE PRODUCER CENSUS",
        "max_order": 16,
        "graphs": len(rows),
        "by_order": by_order,
        "feasible_star_fibres": sum(
            sum(bool(root["feasible"]) for root in row["roots"])
            for row in rows
        ),
        "parallel_odd_witness_star_fibres": sum(
            sum(bool(root["has_odd_packing"]) for root in row["roots"])
            for row in rows
        ),
        "evaluated_flow_gl_orbits": sum(
            int(row["evaluated_flow_gl_orbits"]) for row in rows
        ),
        "packing_models": sum(
            sum(int(root["packing_models"]) for root in row["roots"])
            for row in rows
        ),
        "connectivity_cuts": sum(
            sum(int(root["connectivity_cuts"]) for root in row["roots"])
            for row in rows
        ),
        "seconds": round(time.monotonic() - started, 3),
        "graph_generator": "geng -q -C -d3 -D3 ORDER",
        "graph_corpus_sha256": sha256(graphs_path),
        "source_sha256": {
            f"source/{source.name}": sha256(source_dir / source.name)
            for source in SOURCES
        },
        "cadical_version": "3.0.1",
        "claim": (
            "Every feasible vertex-star fibre in every biconnected simple "
            "cubic graph through 16 vertices has a packing for which an "
            "odd number of the 21 parallel translation-orbit six-point "
            "systems are soluble."
        ),
        "semantic_note": (
            "The lazy SAT producer enumerates omission colourings and "
            "checks every retained model as three literal spanning trees "
            "before constructing its fundamental-completion flow."
        ),
        "trust_boundary": (
            "The producer supplies exhaustive finite evidence. It is "
            "AI-authored and is not an independently formalized proof of "
            "exhaustion. The universal selector and FiveCDC remain open."
        ),
    }
    census_path = output / "census.jsonl"
    census_path.write_text(
        "".join(
            json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
            for row in [*rows, summary]
        ),
        encoding="utf-8",
    )
    result_path = output / "RESULT.json"
    result_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    checksums_path = output / "SHA256SUMS"
    hashed = [
        graphs_path,
        census_path,
        result_path,
        *(source_dir / name for name in SOURCE_NAMES),
    ]
    checksums_path.write_text(
        "".join(
            f"{sha256(path)}  {path.relative_to(output)}\n" for path in hashed
        ),
        encoding="ascii",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
