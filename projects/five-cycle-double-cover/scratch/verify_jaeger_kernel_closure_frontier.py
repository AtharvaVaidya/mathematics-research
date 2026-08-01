#!/usr/bin/env python3
"""Independent semantic replay of the kernel-closure witness frontier."""

from __future__ import annotations

import json
import math
import shutil
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WITNESSES = (
    ROOT
    / "output/jaeger-kernel-closure-frontier"
    / "type-ab-witnesses-through10.jsonl"
)


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    if record.startswith(">>graph6<<"):
        record = record[10:]
    if not record or record[0] == "~":
        raise ValueError("only short graph6 is supported")
    order = ord(record[0]) - 63
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    cursor = 0
    edges = []
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def incidence(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


def is_tree(
    order: int, edges: tuple[tuple[int, int], ...], selected: frozenset[int]
) -> bool:
    if len(selected) != order - 1:
        return False
    parent = list(range(order))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in selected:
        left, right = edges[edge]
        a, b = find(left), find(right)
        if a == b:
            return False
        parent[a] = b
    return True


def odd_kernel(
    order: int,
    edges: tuple[tuple[int, int], ...],
    tree: frozenset[int],
) -> frozenset[int]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge in tree:
        left, right = edges[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    parent = [-2] * order
    parent_edge = [-1] * order
    parent[0] = -1
    traversal = [0]
    for vertex in traversal:
        for other, edge in adjacency[vertex]:
            if parent[other] == -2:
                parent[other] = vertex
                parent_edge[other] = edge
                traversal.append(other)
    assert len(traversal) == order
    size = [1] * order
    answer = set()
    for vertex in reversed(traversal[1:]):
        if size[vertex] & 1:
            answer.add(parent_edge[vertex])
        size[parent[vertex]] += size[vertex]
    return frozenset(answer)


def closure_good(
    order: int,
    edges: tuple[tuple[int, int], ...],
    kernels: tuple[frozenset[int], ...],
) -> bool:
    parent = list(range(order))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in kernels[2]:
        left, right = edges[edge]
        a, b = find(left), find(right)
        assert a != b
        parent[a] = b
    for edge in kernels[0] & kernels[1]:
        left, right = edges[edge]
        if find(left) != find(right):
            return False
    return True


def canonical_graphs_through10() -> set[str] | None:
    generator = shutil.which("geng")
    if generator is None:
        return None
    records: set[str] = set()
    for order in (4, 6, 8, 10):
        completed = subprocess.run(
            [generator, "-cqd3D3", str(order)],
            check=True,
            capture_output=True,
            text=True,
        )
        records.update(completed.stdout.split())
    return records


def main() -> None:
    rows = [
        json.loads(line)
        for line in WITNESSES.read_text().splitlines()
        if line.strip()
    ]
    witnesses = [row for row in rows if row.get("status") == "CLOSURE_WITNESS"]
    summaries = [row for row in rows if "patterns" in row]
    assert len(witnesses) == 12695
    assert len(summaries) == 27
    assert not [
        row for row in rows
        if row.get("status") == "CLOSURE_FAILURE"
    ]

    graph_records = {row["graph6"] for row in summaries}
    assert Counter(parse_graph6(record)[0] for record in graph_records) == {
        4: 1,
        6: 2,
        8: 5,
        10: 19,
    }
    canonical = canonical_graphs_through10()
    if canonical is not None:
        assert graph_records == canonical

    summary_by_graph = {row["graph6"]: row for row in summaries}
    assert len(summary_by_graph) == len(summaries)
    witnesses_per_graph = Counter(row["graph6"] for row in witnesses)
    keys = set()
    semantic_digest = 1469598103934665603

    for row in witnesses:
        record = row["graph6"]
        order, edges = parse_graph6(record)
        assert len(edges) == 3 * order // 2
        rows_incidence = incidence(order, edges)
        assert all(len(incident) == 3 for incident in rows_incidence)
        assert len({frozenset(edge) for edge in edges}) == len(edges)

        kind = row["kind"]
        defect = tuple(row["defect_edges"])
        key = (record, kind, defect)
        assert key not in keys
        keys.add(key)
        multiplicity = [2] * len(edges)
        if kind == "type_a":
            assert len(defect) == 3 and len(set(defect)) == 3
            for edge in defect:
                multiplicity[edge] = 1
        elif kind == "type_b":
            assert len(defect) == 2 and defect[0] != defect[1]
            multiplicity[defect[0]] = 0
            multiplicity[defect[1]] = 1
        else:
            raise AssertionError(f"unexpected kind {kind}")

        trees = tuple(frozenset(tree) for tree in row["trees"])
        assert len(trees) == 3
        assert all(is_tree(order, edges, tree) for tree in trees)
        for edge, expected in enumerate(multiplicity):
            assert sum(edge in tree for tree in trees) == expected
        kernels = tuple(odd_kernel(order, edges, tree) for tree in trees)
        for kernel, tree in zip(kernels, trees):
            assert kernel <= tree
            assert all(
                sum(edge in kernel for edge in incident) % 2 == 1
                for incident in rows_incidence
            )
        assert closure_good(order, edges, kernels)

        for tree in trees:
            for edge in sorted(tree):
                semantic_digest ^= 1000 + 3 * edge
                semantic_digest *= 1099511628211
                semantic_digest &= (1 << 64) - 1

    for record, summary in summary_by_graph.items():
        order, edges = parse_graph6(record)
        expected_patterns = (
            math.comb(len(edges), 3)
            + len(edges) * (len(edges) - 1)
        )
        assert summary["patterns"] == expected_patterns
        assert summary["failures"] == 0
        assert summary["closure_patterns"] == summary["feasible_patterns"]
        assert witnesses_per_graph[record] == summary["closure_patterns"]

    assert sum(row["patterns"] for row in summaries) == 14757
    assert sum(row["feasible_patterns"] for row in summaries) == 12695
    assert sum(row["closure_patterns"] for row in summaries) == 12695

    print("PASS")
    print("canonical_connected_simple_cubic_graphs_through_order10=27")
    print("type_a_b_patterns=14757 feasible=12695 closure_witnesses=12695")
    print(f"semantic_witness_digest_fnv1a64={semantic_digest}")


if __name__ == "__main__":
    main()
