#!/usr/bin/env python3
"""Linear-time native-XOR encoder for the exact five-CDC formula.

This is a production encoder for large indexed graphs.  It deliberately
streams the instance instead of building a quadratic vertex-by-edge scan or
holding every clause in memory.  The emitted variable convention is the same
as Verifier A: variable ``5*edge + coordinate + 1`` represents x[edge,coordinate].
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def load_graph(path: Path) -> tuple[int, list[tuple[int, int]]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("format") != "five-cdc-multigraph-v1":
        raise ValueError("wrong graph format")
    vertices = value.get("vertices")
    records = value.get("edges")
    if not isinstance(vertices, int) or vertices < 0 or not isinstance(records, list):
        raise ValueError("invalid graph dimensions")
    edges: list[tuple[int, int]] = []
    for expected, record in enumerate(records):
        if not isinstance(record, dict) or record.get("id") != expected:
            raise ValueError("edge IDs must be consecutive and ordered")
        u, v = record.get("u"), record.get("v")
        if (
            not isinstance(u, int)
            or not isinstance(v, int)
            or not (0 <= u < vertices)
            or not (0 <= v < vertices)
        ):
            raise ValueError("invalid edge endpoint")
        edges.append((u, v))
    return vertices, edges


def variable(edge: int, coordinate: int) -> int:
    return 5 * edge + coordinate + 1


def encode(graph_path: Path, output: Path) -> dict[str, object]:
    if output.exists():
        raise ValueError(f"refusing to overwrite {output}")
    vertices, edges = load_graph(graph_path)
    incident: list[list[int]] = [[] for _ in range(vertices)]
    for edge, (u, v) in enumerate(edges):
        if u == v:
            continue  # two loop incidences cancel in GF(2)
        incident[u].append(edge)
        incident[v].append(edge)

    ordinary_clauses = 15 * len(edges)
    xor_rows = 5 * sum(bool(row) for row in incident)
    digest = sha256()

    def emit(stream, line: str) -> None:
        data = (line + "\n").encode("ascii")
        stream.write(data)
        digest.update(data)

    with output.open("xb") as stream:
        emit(stream, "c five-cdc-xor-dimacs-v1-linear-stream")
        emit(stream, f"c source {graph_path}")
        emit(
            stream,
            f"p cnf {5 * len(edges)} {ordinary_clauses + xor_rows}",
        )
        for edge in range(len(edges)):
            variables = tuple(variable(edge, coordinate) for coordinate in range(5))
            # At most two true.
            for triple in combinations(variables, 3):
                emit(stream, " ".join(str(-literal) for literal in triple) + " 0")
            # At least two true.
            for quadruple in combinations(variables, 4):
                emit(stream, " ".join(map(str, quadruple)) + " 0")
        for row in incident:
            if not row:
                continue
            for coordinate in range(5):
                variables = [variable(edge, coordinate) for edge in row]
                # CryptoMiniSat reads each x-row as XOR(literals)=true.
                variables[0] = -variables[0]
                emit(stream, "x " + " ".join(map(str, variables)) + " 0")

    return {
        "schema": "five-cdc-xor-fast-summary-v1",
        "vertices": vertices,
        "edges": len(edges),
        "variables": 5 * len(edges),
        "ordinary_clauses": ordinary_clauses,
        "xor_rows": xor_rows,
        "rows": ordinary_clauses + xor_rows,
        "instance_sha256": digest.hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    print(
        json.dumps(
            encode(arguments.graph, arguments.output),
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
