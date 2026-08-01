#!/usr/bin/env python3
"""Reproduce the exact symmetric Fano-minimum descent census.

For every vertex-orbit representative of every simple 3-edge-connected
cubic graph in the selected even orders, run the C++ whole-state checker
with the minimum defect over all seven Fano planes.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import itertools
import json
import subprocess
import tempfile
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scratch" / "search_jaeger_star_parity_descent.cpp"


def graph_records(geng: Path, order: int) -> list[str]:
    completed = subprocess.run(
        [str(geng), "-Cq", "-d3", "-D3", str(order)],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in completed.stdout.splitlines() if line]


def three_edge_connected(graph: nx.Graph) -> bool:
    edges = tuple(graph.edges())
    for count in range(3):
        for deleted in itertools.combinations(range(len(edges)), count):
            changed = graph.copy()
            for edge in deleted:
                changed.remove_edge(*edges[edge])
            if not nx.is_connected(changed):
                return False
    return True


def vertex_orbit_representatives(graph: nx.Graph) -> tuple[int, ...]:
    parent = list(range(len(graph)))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def union(first: int, second: int) -> None:
        first, second = find(first), find(second)
        if first != second:
            parent[second] = first

    matcher = nx.algorithms.isomorphism.GraphMatcher(graph, graph)
    for mapping in matcher.isomorphisms_iter():
        for first, second in mapping.items():
            union(first, second)
    return tuple(sorted({find(vertex) for vertex in graph}))


def compile_checker(compiler: Path, binary: Path) -> None:
    subprocess.run(
        [
            str(compiler),
            "-O3",
            "-std=c++20",
            "-Wall",
            "-Wextra",
            "-pedantic",
            str(SOURCE),
            "-o",
            str(binary),
        ],
        check=True,
    )


def run_job(
    binary: Path, order: int, graph_index: int, graph6: str, root: int
) -> dict[str, object]:
    completed = subprocess.run(
        [
            str(binary),
            "--root",
            str(root),
            "--objective",
            "seven",
        ],
        input=graph6 + "\n",
        capture_output=True,
        text=True,
    )
    if completed.returncode not in (0, 1):
        raise RuntimeError(completed.stderr)
    lines = [line for line in completed.stdout.splitlines() if line]
    if len(lines) != 1:
        raise RuntimeError(
            f"expected one checker row, got {len(lines)}: {completed.stdout}"
        )
    row = json.loads(lines[0])
    assert row["graph6"] == graph6 and row["root"] == root
    row["order"] = order
    row["canonical_graph_index"] = graph_index
    row.pop("graph_index", None)
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orders", nargs="+", type=int, default=[4, 6, 8, 10, 12, 14]
    )
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--geng", type=Path, default=Path("/opt/homebrew/bin/geng"))
    parser.add_argument("--compiler", type=Path, default=Path("/usr/bin/clang++"))
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT
        / "output"
        / "jaeger-fano-min-descent-through14"
        / "census.jsonl",
    )
    arguments = parser.parse_args()

    jobs: list[tuple[int, int, str, int]] = []
    graph_counts: dict[int, int] = {}
    for order in arguments.orders:
        accepted = 0
        for graph_index, graph6 in enumerate(graph_records(arguments.geng, order)):
            graph = nx.from_graph6_bytes(graph6.encode())
            if not three_edge_connected(graph):
                continue
            for root in vertex_orbit_representatives(graph):
                jobs.append((order, graph_index, graph6, root))
            accepted += 1
        graph_counts[order] = accepted

    with tempfile.TemporaryDirectory(prefix="jaeger-fano-descent-") as directory:
        binary = Path(directory) / "checker"
        compile_checker(arguments.compiler, binary)
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=arguments.workers
        ) as executor:
            rows = list(
                executor.map(
                    lambda job: run_job(binary, *job),
                    jobs,
                )
            )

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    with arguments.output.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, sort_keys=True, separators=(",", ":")))
            stream.write("\n")
    digest = hashlib.sha256(arguments.output.read_bytes()).hexdigest()
    summary = {
        "schema": "jaeger-fano-minimum-descent-frontier-v1",
        "orders": arguments.orders,
        "graphs": graph_counts,
        "rooted_orbit_instances": len(rows),
        "states": sum(int(row["states"]) for row in rows),
        "failures": sum(bool(row["failure"]) for row in rows),
        "maximum_positive_score": max(int(row["max_score"]) for row in rows),
        "census_sha256": digest,
        "source": str(SOURCE.relative_to(ROOT)),
        "objective": "minimum component-defect count over seven Fano planes",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
