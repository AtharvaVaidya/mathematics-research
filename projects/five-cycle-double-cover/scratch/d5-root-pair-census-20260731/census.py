#!/usr/bin/env python3
"""Exhaust rooted D5 feasibility over graph6 corpora.

Every positive row is checked semantically by the published linear
root-transition driver.  A first negative answer is immediately rerun with
a frozen DIMACS instance and a CaDiCaL proof trace; it is still reported as
uncertified until an independent proof checker accepts that trace.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
DRIVER = PROJECT / "scratch" / "d5-root-transition-sat-20260731" / "search.py"


def load_driver():
    spec = importlib.util.spec_from_file_location("root_transition_driver", DRIVER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph_rows(path: Path) -> list[int]:
    rows = []
    for index, raw in enumerate(path.read_text(encoding="ascii").splitlines()):
        if raw and not raw.startswith(">>"):
            rows.append(index)
    return rows


def independent_pairs(graph) -> list[tuple[int, int]]:
    pairs = []
    for first in range(len(graph.edges)):
        endpoints = set(graph.edges[first])
        for second in range(first + 1, len(graph.edges)):
            if endpoints.isdisjoint(graph.edges[second]):
                pairs.append((first, second))
    return pairs


def canonical_bytes(payload: object) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--cadical", type=Path,
                        default=Path("/opt/homebrew/bin/cadical"))
    parser.add_argument("--failure-dir", type=Path,
                        default=HERE / "failure-certificates")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--stop-after-graphs", type=int)
    args = parser.parse_args()

    driver = load_driver()
    assert args.cadical.exists(), args.cadical
    graph_total = 0
    root_total = 0
    graph_results = []
    failures = []

    for source in args.inputs:
        source = source.resolve()
        for row in graph_rows(source):
            if args.stop_after_graphs is not None and graph_total >= args.stop_after_graphs:
                break
            graph = driver.graph6_file(source, row)
            pairs = independent_pairs(graph)
            aggregate = hashlib.sha256()
            graph_failures = []
            for roots in pairs:
                result = driver.solve_instance(graph, roots, args.cadical)
                root_total += 1
                witness_record = {
                    "cnf_sha256": result["cnf_sha256"],
                    "labels_sha256": result.get("labels_sha256"),
                    "roots": list(roots),
                    "selected_transition_path": result.get("selected_transition_path"),
                    "status": result["status"],
                }
                aggregate.update(canonical_bytes(witness_record))
                if result["status"] != "SAT_MODEL_CHECKED":
                    stem = f"g{graph_total:05d}-row{row:05d}-r{roots[0]}-{roots[1]}"
                    args.failure_dir.mkdir(parents=True, exist_ok=True)
                    cnf = args.failure_dir / f"{stem}.cnf"
                    proof = args.failure_dir / f"{stem}.drat"
                    retained = driver.solve_instance(
                        graph, roots, args.cadical, cnf, proof)
                    failure = {
                        "source": str(source),
                        "source_row": row,
                        "roots": list(roots),
                        "first_result": result,
                        "retained_result": retained,
                    }
                    failures.append(failure)
                    graph_failures.append(failure)
                    break

            metadata = driver.graph_metadata(graph)
            graph_results.append({
                "source": str(source),
                "source_row": row,
                "metadata": metadata,
                "independent_root_pairs": len(pairs),
                "checked_root_pairs": len(pairs) if not graph_failures else None,
                "witness_aggregate_sha256": aggregate.hexdigest(),
                "failures": graph_failures,
            })
            graph_total += 1
            print(
                f"graph={graph_total} vertices={graph.n} roots={root_total} "
                f"failures={len(failures)}",
                file=sys.stderr,
                flush=True,
            )
            if failures:
                break
        if failures or (
            args.stop_after_graphs is not None and graph_total >= args.stop_after_graphs
        ):
            break

    payload = {
        "status": (
            "ALL_SAT_MODELS_SEMANTICALLY_CHECKED"
            if not failures else
            "UNSAT_CANDIDATE_RETAINED_REQUIRES_INDEPENDENT_PROOF_CHECK"
        ),
        "driver": str(DRIVER),
        "driver_sha256": file_sha256(DRIVER),
        "sources": [
            {"path": str(path.resolve()), "sha256": file_sha256(path.resolve())}
            for path in args.inputs
        ],
        "graphs_checked": graph_total,
        "root_pairs_checked": root_total,
        "graphs": graph_results,
        "failures": failures,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
