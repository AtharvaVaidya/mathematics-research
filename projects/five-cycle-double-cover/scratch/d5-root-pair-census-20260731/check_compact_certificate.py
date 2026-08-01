#!/usr/bin/env python3
"""Independent semantic checker for compact rooted-D5 certificates.

This file deliberately does not import the SAT generator or its graph code.
It checks source hashes, parses graph6, verifies every displayed D5 flow, and
then exhausts all independent edge pairs against all ten displayed factors.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_graph6(raw: bytes) -> tuple[int, tuple[tuple[int, int], ...]]:
    raw = raw.strip()
    if raw.startswith(b">>graph6<<"):
        raw = raw[len(b">>graph6<<"):]
    values = [byte - 63 for byte in raw]
    if not values or any(value < 0 or value >= 64 for value in values):
        raise ValueError("invalid graph6 alphabet")
    if values[0] < 63:
        n, offset = values[0], 1
    elif len(values) >= 4 and values[1] < 63:
        n = (values[1] << 12) | (values[2] << 6) | values[3]
        offset = 4
    else:
        if len(values) < 8:
            raise ValueError("truncated graph6 order")
        n = 0
        for value in values[2:8]:
            n = (n << 6) | value
        offset = 8
    bits = []
    for value in values[offset:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    need = n * (n - 1) // 2
    if len(bits) < need:
        raise ValueError("truncated graph6 adjacency")
    edges = []
    index = 0
    for v in range(1, n):
        for u in range(v):
            if bits[index]:
                edges.append((u, v))
            index += 1
    edges.sort()
    return n, tuple(edges)


def graph_digest(n: int, edges: tuple[tuple[int, int], ...]) -> str:
    data = str(n) + "\n"
    data += "".join(
        f"{index} {u} {v}\n" for index, (u, v) in enumerate(edges)
    )
    return digest(data.encode("ascii"))


def incidence(n: int, edges: tuple[tuple[int, int], ...]) -> list[list[int]]:
    rows = [[] for _ in range(n)]
    for edge, (u, v) in enumerate(edges):
        if u == v or not (0 <= u < n and 0 <= v < n):
            raise ValueError("certificate is not a simple loopless graph")
        rows[u].append(edge)
        rows[v].append(edge)
    if len(set(edges)) != len(edges) or any(len(row) != 3 for row in rows):
        raise ValueError("certificate is not a simple cubic graph")
    return rows


def resolve_source(name: str) -> Path:
    path = Path(name)
    return path.resolve() if path.is_absolute() else (PROJECT / path).resolve()


def load_certificate(path: Path) -> object:
    data = path.read_bytes()
    if path.suffix == ".gz":
        data = gzip.decompress(data)
    return json.loads(data.decode("utf-8"))


def verify_flow(rows: list[list[int]], labels: tuple[int, ...]) -> None:
    if any(label <= 0 or label >= 32 or label.bit_count() != 2
           for label in labels):
        raise ValueError("edge label is not a two-subset of [5]")
    for row in rows:
        if labels[row[0]] ^ labels[row[1]] ^ labels[row[2]]:
            raise ValueError("D5 xor law fails at a vertex")


def pair_coverage(
    edges: tuple[tuple[int, int], ...],
    rows: list[list[int]],
    labels: tuple[int, ...],
) -> set[tuple[int, int]]:
    answer = set()
    for a, b in combinations(range(5), 2):
        mask = (1 << a) | (1 << b)
        active = [(label & mask).bit_count() == 1 for label in labels]
        adjacency = [set() for _ in edges]
        for row in rows:
            selected = [edge for edge in row if active[edge]]
            if len(selected) not in (0, 2):
                raise ValueError("factor is not Eulerian")
            if selected:
                x, y = selected
                adjacency[x].add(y)
                adjacency[y].add(x)
        unseen = {edge for edge, enabled in enumerate(active) if enabled}
        while unseen:
            start = min(unseen)
            component = {start}
            todo = [start]
            unseen.remove(start)
            while todo:
                edge = todo.pop()
                for other in adjacency[edge]:
                    if other in unseen:
                        unseen.remove(other)
                        component.add(other)
                        todo.append(other)
            for first, second in combinations(sorted(component), 2):
                if set(edges[first]).isdisjoint(edges[second]):
                    answer.add((first, second))
    return answer


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    payload = load_certificate(args.certificate)
    if payload.get("schema") != "fivecdc-compact-root-universality-certificate-v1":
        raise SystemExit("wrong certificate schema")

    declared_sources = {
        str(resolve_source(row["path"])): row["sha256"]
        for row in payload["sources"]
    }
    source_cache: dict[str, list[bytes]] = {}
    for source_name, expected in declared_sources.items():
        source = Path(source_name)
        data = source.read_bytes()
        if digest(data) != expected:
            raise SystemExit(f"source hash mismatch: {source}")
        source_cache[source_name] = [
            row.strip() for row in data.splitlines()
            if row.strip() and not row.startswith(b">")
        ]

    total_pairs = 0
    total_flows = 0
    for graph_index, record in enumerate(payload["graphs"]):
        source_name = str(resolve_source(record["source"]))
        if source_name not in source_cache:
            raise SystemExit(f"graph {graph_index}: undeclared source")
        row = int(record["source_row"])
        source_rows = source_cache[source_name]
        if not 0 <= row < len(source_rows):
            raise SystemExit(f"graph {graph_index}: source row out of range")
        n, edges = parse_graph6(source_rows[row])
        rows = incidence(n, edges)
        if n != record["vertices"] or len(edges) != record["edges"]:
            raise SystemExit(f"graph {graph_index}: size changed")
        if graph_digest(n, edges) != record["graph_sha256"]:
            raise SystemExit(f"graph {graph_index}: digest changed")

        all_pairs = {
            pair for pair in combinations(range(len(edges)), 2)
            if set(edges[pair[0]]).isdisjoint(edges[pair[1]])
        }
        if len(all_pairs) != record["independent_root_pairs"]:
            raise SystemExit(f"graph {graph_index}: pair count changed")
        covered = set()
        for flow_index, flow in enumerate(record["flows"]):
            labels = tuple(int(value) for value in flow["labels"])
            if len(labels) != len(edges):
                raise SystemExit(
                    f"graph {graph_index} flow {flow_index}: wrong label count"
                )
            verify_flow(rows, labels)
            flow_pairs = pair_coverage(edges, rows, labels) & all_pairs
            seed = tuple(int(value) for value in flow["seed_roots"])
            if seed not in flow_pairs:
                raise SystemExit(
                    f"graph {graph_index} flow {flow_index}: seed not covered"
                )
            covered |= flow_pairs
        missing = all_pairs - covered
        if missing:
            raise SystemExit(
                f"graph {graph_index}: {len(missing)} root pairs uncovered"
            )
        total_pairs += len(all_pairs)
        total_flows += len(record["flows"])

    expected = (
        payload["graphs_certified"],
        payload["root_pairs_certified"],
        payload["flows_recorded"],
    )
    actual = (len(payload["graphs"]), total_pairs, total_flows)
    if actual != expected:
        raise SystemExit(f"aggregate mismatch: {actual} != {expected}")
    print(json.dumps({
        "status": "PASS",
        "graphs_certified": actual[0],
        "root_pairs_certified": actual[1],
        "flows_checked": actual[2],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
