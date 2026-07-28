#!/usr/bin/env python3
"""Independent semantic checker for the direct FiveCDC lift portfolio.

This program does not import the generator, the C++ solver, Verifier A, or
networkx.  It decodes graph6, recomputes cubicity/connectivity/bridges, checks
every returned edge label against exact-two and vertex parity, and, when
source metadata is supplied, reconstructs each voltage 2-lift literally.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def decode_order(record: str) -> tuple[int, int]:
    values = [ord(char) - 63 for char in record]
    if not values or any(value < 0 or value > 63 for value in values):
        raise ValueError("bad graph6 bytes")
    if values[0] != 63:
        return values[0], 1
    if len(values) < 4:
        raise ValueError("truncated graph6 order")
    if values[1] != 63:
        n = (values[1] << 12) | (values[2] << 6) | values[3]
        if n < 63:
            raise ValueError("noncanonical medium order")
        return n, 4
    if len(values) < 8:
        raise ValueError("truncated graph6 order")
    n = 0
    for value in values[2:8]:
        n = (n << 6) | value
    if n < 258048:
        raise ValueError("noncanonical large order")
    return n, 8


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    if record.startswith(">>graph6<<"):
        record = record[10:]
    n, offset = decode_order(record)
    count = n * (n - 1) // 2
    chunks = (count + 5) // 6
    if len(record) != offset + chunks:
        raise ValueError("bad graph6 length")
    bits = [
        (ord(char) - 63) >> shift & 1
        for char in record[offset:]
        for shift in range(5, -1, -1)
    ]
    if any(bits[count:]):
        raise ValueError("nonzero graph6 padding")
    edges: list[tuple[int, int]] = []
    at = 0
    for v in range(1, n):
        for u in range(v):
            if bits[at]:
                edges.append((u, v))
            at += 1
    return n, tuple(edges)


def premise_check(
    n: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if len(set(edges)) != len(edges) or any(not (0 <= u < v < n) for u, v in edges):
        raise AssertionError("graph is not simple")
    incident: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for edge, (u, v) in enumerate(edges):
        incident[u].append((v, edge))
        incident[v].append((u, edge))
    if any(len(row) != 3 for row in incident):
        raise AssertionError("graph is not cubic")

    discovered = [-1] * n
    low = [-1] * n
    tick = 0
    bridges: list[int] = []

    def visit(vertex: int, parent_edge: int) -> None:
        nonlocal tick
        discovered[vertex] = low[vertex] = tick
        tick += 1
        for other, edge in incident[vertex]:
            if edge == parent_edge:
                continue
            if discovered[other] < 0:
                visit(other, edge)
                low[vertex] = min(low[vertex], low[other])
                if low[other] > discovered[vertex]:
                    bridges.append(edge)
            else:
                low[vertex] = min(low[vertex], discovered[other])

    if not n:
        raise AssertionError("empty graph")
    visit(0, -1)
    if -1 in discovered:
        raise AssertionError("graph is disconnected")
    if bridges:
        raise AssertionError("graph has bridges")
    return tuple(tuple(row) for row in incident)


def check_cover(
    edges: tuple[tuple[int, int], ...],
    incident: tuple[tuple[tuple[int, int], ...], ...],
    labels: object,
) -> None:
    if not isinstance(labels, list) or len(labels) != len(edges):
        raise AssertionError("wrong label count")
    for mask in labels:
        if not isinstance(mask, int) or not (0 <= mask < 32):
            raise AssertionError("bad label mask")
        if mask.bit_count() != 2:
            raise AssertionError("edge label does not have weight two")
    for row in incident:
        for coordinate in range(5):
            parity = 0
            for _, edge in row:
                parity ^= labels[edge] >> coordinate & 1
            if parity:
                raise AssertionError("vertex parity failure")


def load_json_lines(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for number, text in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        value = json.loads(text)
        if not isinstance(value, dict):
            raise AssertionError(f"{path}:{number}: row is not an object")
        rows.append(value)
    return rows


def reconstruct_lift(source: dict[str, object]) -> tuple[int, tuple[tuple[int, int], ...]]:
    base = source.get("base_graph6")
    voltage_hex = source.get("voltage_hex")
    if not isinstance(base, str) or not isinstance(voltage_hex, str):
        raise AssertionError("bad source metadata")
    n, decoded_base_edges = decode_graph6(base)
    # The generator uses the existing parser's lexicographic edge order.
    base_edges = tuple(sorted(decoded_base_edges))
    voltage = int(voltage_hex, 16)
    edges: list[tuple[int, int]] = []
    for edge, (u, v) in enumerate(base_edges):
        bit = voltage >> edge & 1
        for sheet in range(2):
            ends = (2 * u + sheet, 2 * v + (sheet ^ bit))
            edges.append(tuple(sorted(ends)))
    return 2 * n, tuple(sorted(edges))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--base-results", type=Path)
    arguments = parser.parse_args()

    results = load_json_lines(arguments.results)
    sources = load_json_lines(arguments.source) if arguments.source else None
    base_results = (
        load_json_lines(arguments.base_results) if arguments.base_results else None
    )
    if base_results is not None and sources is None:
        raise AssertionError("--base-results requires --source")
    if sources is not None and len(sources) != len(results):
        raise AssertionError("source/result row count differs")

    orders: dict[int, int] = {}
    for at, result in enumerate(results):
        if result.get("index") != at + 1:
            raise AssertionError("nonsequential result index")
        if result.get("status") != "SAT_SEMANTIC_CHECK":
            raise AssertionError(f"row {at + 1} is not checked SAT")
        record = result.get("graph6")
        if not isinstance(record, str):
            raise AssertionError("missing graph6")
        n, edges = decode_graph6(record)
        incident = premise_check(n, edges)
        check_cover(edges, incident, result.get("labels"))
        if result.get("vertices") != n or result.get("edges") != len(edges):
            raise AssertionError("declared graph size differs")
        orders[n] = orders.get(n, 0) + 1
        if sources is not None:
            source = sources[at]
            if source.get("lift_graph6") != record:
                raise AssertionError("source/result graph6 differs")
            lifted_n, lifted_edges = reconstruct_lift(source)
            if lifted_n != n or lifted_edges != tuple(sorted(edges)):
                raise AssertionError("literal voltage lift reconstruction differs")
            if base_results is not None:
                base_index = source.get("base_index")
                if not isinstance(base_index, int) or not (1 <= base_index <= len(base_results)):
                    raise AssertionError("bad base index")
                base_result = base_results[base_index - 1]
                if base_result.get("graph6") != source.get("base_graph6"):
                    raise AssertionError("base result/source graph6 differs")
                base_n, base_edges = decode_graph6(str(source["base_graph6"]))
                if n != 2 * base_n:
                    raise AssertionError("lift order is not twice base order")
                base_labels = base_result.get("labels")
                if not isinstance(base_labels, list) or len(base_labels) != len(base_edges):
                    raise AssertionError("bad base cover")
                label_by_edge = dict(zip(base_edges, base_labels, strict=True))
                pulled_labels = [
                    label_by_edge[tuple(sorted((u // 2, v // 2)))]
                    for u, v in edges
                ]
                check_cover(edges, incident, pulled_labels)

    report = {
        "classification": "FINITE POSITIVE EVIDENCE ONLY",
        "results": str(arguments.results),
        "results_sha256": hashlib.sha256(arguments.results.read_bytes()).hexdigest(),
        "rows": len(results),
        "orders": orders,
        "all_graph_premises_checked": True,
        "all_fivecdc_witnesses_checked": True,
        "all_declared_two_lifts_reconstructed": sources is not None,
        "all_pullback_covers_checked": base_results is not None,
    }
    if arguments.source:
        report["source"] = str(arguments.source)
        report["source_sha256"] = hashlib.sha256(arguments.source.read_bytes()).hexdigest()
    if arguments.base_results:
        report["base_results"] = str(arguments.base_results)
        report["base_results_sha256"] = hashlib.sha256(
            arguments.base_results.read_bytes()
        ).hexdigest()
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
