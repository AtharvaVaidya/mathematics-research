#!/usr/bin/env python3
"""Build a compact positive certificate for rooted D5 universality.

For each input graph, repeatedly ask the published SAT driver for a D5 flow
covering the lexicographically first root pair not yet covered.  One flow can
certify many pairs: the checker tests all ten coordinate pairs.  The output is
only a positive witness list; no UNSAT answer is accepted by this program.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
from itertools import combinations
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
DRIVER = PROJECT / "scratch" / "d5-root-transition-sat-20260731" / "search.py"


def load_driver():
    spec = importlib.util.spec_from_file_location("compact_root_driver", DRIVER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def portable(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(PROJECT))
    except ValueError:
        return str(resolved)


def write_payload(path: Path, payload: object) -> None:
    data = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix != ".gz":
        path.write_bytes(data)
        return
    # Empty filename and zero mtime make the gzip stream reproducible.
    with path.open("wb") as raw:
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0
        ) as compressed:
            compressed.write(data)


def source_rows(path: Path) -> list[tuple[int, bytes]]:
    answer = []
    for index, raw in enumerate(path.read_bytes().splitlines()):
        row = raw.strip()
        if row and not row.startswith(b">>"):
            answer.append((index, row))
    return answer


def independent_pairs(graph) -> set[tuple[int, int]]:
    answer = set()
    for first, second in combinations(range(len(graph.edges)), 2):
        if set(graph.edges[first]).isdisjoint(graph.edges[second]):
            answer.add((first, second))
    return answer


def covered_pairs(graph, labels: tuple[int, ...]) -> set[tuple[int, int]]:
    rows = [[] for _ in range(graph.n)]
    for edge, (u, v) in enumerate(graph.edges):
        rows[u].append(edge)
        rows[v].append(edge)

    covered: set[tuple[int, int]] = set()
    for a, b in combinations(range(5), 2):
        coordinate_pair = (1 << a) | (1 << b)
        active = [
            (label & coordinate_pair).bit_count() == 1 for label in labels
        ]
        adjacency = [set() for _ in graph.edges]
        for row in rows:
            selected = [edge for edge in row if active[edge]]
            assert len(selected) in (0, 2)
            if selected:
                x, y = selected
                adjacency[x].add(y)
                adjacency[y].add(x)

        seen: set[int] = set()
        for start, enabled in enumerate(active):
            if not enabled or start in seen:
                continue
            component = {start}
            todo = [start]
            seen.add(start)
            while todo:
                edge = todo.pop()
                for other in adjacency[edge]:
                    if other not in seen:
                        seen.add(other)
                        component.add(other)
                        todo.append(other)
            for first, second in combinations(sorted(component), 2):
                if set(graph.edges[first]).isdisjoint(graph.edges[second]):
                    covered.add((first, second))
    return covered


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--cadical", type=Path,
                        default=Path("/opt/homebrew/bin/cadical"))
    parser.add_argument("--progress-every", type=int, default=1)
    args = parser.parse_args()

    driver = load_driver()
    graph_records = []
    total_pairs = 0
    total_flows = 0

    for source_arg in args.inputs:
        source = source_arg.resolve()
        for source_row, _ in source_rows(source):
            graph = driver.graph6_file(source, source_row)
            all_pairs = independent_pairs(graph)
            uncovered = set(all_pairs)
            flow_records = []
            while uncovered:
                roots = min(uncovered)
                result = driver.solve_instance(
                    graph, roots, args.cadical,
                    include_labels=True,
                    root_symmetry_break=True,
                )
                if result["status"] != "SAT_MODEL_CHECKED":
                    raise SystemExit(
                        f"refusing non-positive result at {source}:{source_row} "
                        f"roots={roots}: {result['status']}"
                    )
                labels = tuple(int(value) for value in result["labels"])
                coverage = covered_pairs(graph, labels) & all_pairs
                if roots not in coverage:
                    raise SystemExit("driver witness did not cover its seed pair")
                newly_covered = coverage & uncovered
                flow_records.append({
                    "seed_roots": list(roots),
                    "labels": list(labels),
                    "new_pairs": len(newly_covered),
                })
                uncovered -= coverage

            graph_records.append({
                "source": portable(source),
                "source_row": source_row,
                "graph_sha256": driver.graph_digest(graph),
                "vertices": graph.n,
                "edges": len(graph.edges),
                "independent_root_pairs": len(all_pairs),
                "flows": flow_records,
            })
            total_pairs += len(all_pairs)
            total_flows += len(flow_records)
            if args.progress_every and len(graph_records) % args.progress_every == 0:
                print(
                    f"graph={len(graph_records)} vertices={graph.n} "
                    f"pairs={total_pairs} flows={total_flows}",
                    file=sys.stderr,
                    flush=True,
                )

    payload = {
        "schema": "fivecdc-compact-root-universality-certificate-v1",
        "status": "POSITIVE_WITNESSES_RECORDED",
        "driver": portable(DRIVER),
        "driver_sha256": sha256(DRIVER),
        "sources": [
            {"path": portable(path), "sha256": sha256(path.resolve())}
            for path in args.inputs
        ],
        "graphs": graph_records,
        "graphs_certified": len(graph_records),
        "root_pairs_certified": total_pairs,
        "flows_recorded": total_flows,
    }
    write_payload(args.output, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
