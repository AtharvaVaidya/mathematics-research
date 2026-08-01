#!/usr/bin/env python3
"""Independent checker for the direct Petersen-dot-product portfolio."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from verify_direct_fivecdc_lift_portfolio_20260728 import (
    check_cover,
    decode_graph6,
    premise_check,
)


PETERSEN_GRAPH6 = "ICOf@pSb?"


def json_lines(path: Path) -> list[dict[str, object]]:
    result = []
    for text in path.read_text(encoding="ascii").splitlines():
        value = json.loads(text)
        if not isinstance(value, dict):
            raise AssertionError("JSONL row is not an object")
        result.append(value)
    return result


def neighbours(edges: tuple[tuple[int, int], ...], vertex: int) -> tuple[int, ...]:
    return tuple(
        sorted(
            v if u == vertex else u
            for u, v in edges
            if u == vertex or v == vertex
        )
    )


def reconstruct(source: dict[str, object]) -> tuple[int, tuple[tuple[int, int], ...]]:
    base_record = source.get("base_graph6")
    removed_raw = source.get("removed_base_edges")
    permutation_raw = source.get("port_permutation")
    deleted_raw = source.get("deleted_petersen_edge")
    if not isinstance(base_record, str):
        raise AssertionError("missing base record")
    if (
        not isinstance(removed_raw, list)
        or len(removed_raw) != 2
        or any(not isinstance(edge, list) or len(edge) != 2 for edge in removed_raw)
    ):
        raise AssertionError("bad removed edge pair")
    if not isinstance(permutation_raw, list) or sorted(permutation_raw) != list(range(4)):
        raise AssertionError("bad port permutation")

    base_n, base_decoded = decode_graph6(base_record)
    base_edges = tuple(sorted(base_decoded))
    removed = tuple(tuple(int(v) for v in edge) for edge in removed_raw)
    if any(edge not in base_edges for edge in removed):
        raise AssertionError("removed base edge absent")
    if set(removed[0]) & set(removed[1]):
        raise AssertionError("removed base edges are not independent")

    petersen_n, petersen_decoded = decode_graph6(PETERSEN_GRAPH6)
    petersen_edges = tuple(sorted(petersen_decoded))
    deleted = min(petersen_edges)
    if list(deleted) != deleted_raw:
        raise AssertionError("declared Petersen deletion differs")
    deleted_vertices = set(deleted)
    ports = tuple(
        vertex
        for endpoint in deleted
        for vertex in neighbours(petersen_edges, endpoint)
        if vertex not in deleted_vertices
    )
    kept = [vertex for vertex in range(petersen_n) if vertex not in deleted_vertices]
    mapping = {old: base_n + new for new, old in enumerate(kept)}

    result = [edge for edge in base_edges if edge not in removed]
    result.extend(
        tuple(sorted((mapping[u], mapping[v])))
        for u, v in petersen_edges
        if u not in deleted_vertices and v not in deleted_vertices
    )
    base_ports = removed[0] + removed[1]
    permutation = tuple(int(value) for value in permutation_raw)
    result.extend(
        tuple(sorted((base_ports[position], mapping[ports[permutation[position]]])))
        for position in range(4)
    )
    return base_n + 8, tuple(sorted(result))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    arguments = parser.parse_args()
    results = json_lines(arguments.results)
    sources = json_lines(arguments.source)
    if len(results) != len(sources):
        raise AssertionError("result/source row count differs")

    for index, (result, source) in enumerate(zip(results, sources, strict=True), 1):
        if result.get("index") != index or source.get("base_index") != index:
            raise AssertionError("nonsequential row index")
        if result.get("status") != "SAT_SEMANTIC_CHECK":
            raise AssertionError("non-SAT result")
        record = result.get("graph6")
        if not isinstance(record, str) or source.get("dot_graph6") != record:
            raise AssertionError("result/source graph6 differs")
        n, decoded_edges = decode_graph6(record)
        reconstructed_n, reconstructed_edges = reconstruct(source)
        if n != reconstructed_n or tuple(sorted(decoded_edges)) != reconstructed_edges:
            raise AssertionError("literal dot-product reconstruction differs")
        incident = premise_check(n, decoded_edges)
        check_cover(decoded_edges, incident, result.get("labels"))

    report = {
        "classification": "FINITE POSITIVE EVIDENCE ONLY",
        "rows": len(results),
        "order": sorted({result["vertices"] for result in results}),
        "all_dot_products_reconstructed": True,
        "all_graph_premises_checked": True,
        "all_fivecdc_witnesses_checked": True,
        "results_sha256": hashlib.sha256(arguments.results.read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(arguments.source.read_bytes()).hexdigest(),
    }
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
