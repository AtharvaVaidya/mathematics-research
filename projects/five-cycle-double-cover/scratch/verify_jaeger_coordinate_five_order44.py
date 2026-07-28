#!/usr/bin/env python3
"""Independent verifier for canonical-five-set Jaeger star witnesses.

This checker uses only the Python standard library.  It does not import the
SAT producer.  For every emitted witness it independently decodes graph6,
checks the graph and star fibre, reconstructs the three fundamental
completions from the three spanning trees, and checks the literal pair
labelling supported on {0,4,5,6,7}.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Iterable


SUPPORT = frozenset((0, 4, 5, 6, 7))


def decode_graph6(record: str) -> tuple[int, list[tuple[int, int]]]:
    record = record.strip()
    if record.startswith(">>graph6<<"):
        record = record[len(">>graph6<<") :]
    if not record or record[0] == "~":
        raise ValueError("checker accepts short graph6 records only")
    order = ord(record[0]) - 63
    if not 1 <= order <= 62:
        raise ValueError(f"bad short graph6 order {order}")
    bits: list[int] = []
    for character in record[1:]:
        chunk = ord(character) - 63
        if not 0 <= chunk < 64:
            raise ValueError("bad graph6 byte")
        bits.extend((chunk >> shift) & 1 for shift in range(5, -1, -1))
    required = order * (order - 1) // 2
    if len(bits) < required:
        raise ValueError("truncated graph6 record")
    edges: list[tuple[int, int]] = []
    cursor = 0
    for second in range(1, order):
        for first in range(second):
            if bits[cursor]:
                edges.append((first, second))
            cursor += 1
    return order, edges


def incidence(
    order: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    result = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        if first == second:
            raise AssertionError("loop")
        result[first].append(edge)
        result[second].append(edge)
    return result


def reached_vertices(
    order: int,
    edges: list[tuple[int, int]],
    incident: list[list[int]],
    omitted_edge: int | None = None,
) -> set[int]:
    reached = {0}
    queue = deque((0,))
    while queue:
        vertex = queue.popleft()
        for edge in incident[vertex]:
            if edge == omitted_edge:
                continue
            first, second = edges[edge]
            other = second if first == vertex else first
            if other not in reached:
                reached.add(other)
                queue.append(other)
    return reached


def check_graph(record: str) -> tuple[int, list[tuple[int, int]], list[list[int]]]:
    order, edges = decode_graph6(record)
    assert order == 44
    assert len(edges) == 3 * order // 2
    assert len(set(edges)) == len(edges)
    incident = incidence(order, edges)
    assert all(len(row) == 3 for row in incident)
    assert len(reached_vertices(order, edges, incident)) == order
    for edge in range(len(edges)):
        assert len(reached_vertices(order, edges, incident, edge)) == order
    return order, edges, incident


def check_spanning_tree(
    order: int,
    edges: list[tuple[int, int]],
    selected: Iterable[int],
) -> set[int]:
    tree = set(selected)
    assert len(tree) == order - 1
    assert all(0 <= edge < len(edges) for edge in tree)
    parent = list(range(order))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in tree:
        first, second = edges[edge]
        root_first, root_second = find(first), find(second)
        assert root_first != root_second
        parent[root_first] = root_second
    root = find(0)
    assert all(find(vertex) == root for vertex in range(order))
    return tree


def fundamental_completion(
    order: int,
    edges: list[tuple[int, int]],
    incident: list[list[int]],
    tree: set[int],
) -> set[int]:
    """Return the unique Eulerian set containing every cotree edge."""
    cotree = set(range(len(edges))) - tree
    tree_adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(order)
    ]
    for edge in tree:
        first, second = edges[edge]
        tree_adjacency[first].append((second, edge))
        tree_adjacency[second].append((first, edge))

    parent = [-1] * order
    parent_edge = [-1] * order
    traversal = [0]
    for vertex in traversal:
        for other, edge in tree_adjacency[vertex]:
            if other == parent[vertex]:
                continue
            assert parent[other] == -1 and other != 0
            parent[other] = vertex
            parent_edge[other] = edge
            traversal.append(other)
    assert len(traversal) == order

    selected_tree_edges: set[int] = set()
    tree_edge_bit: dict[int, int] = {}
    cotree_parity = [
        sum(edge in cotree for edge in incident[vertex]) & 1
        for vertex in range(order)
    ]
    for vertex in reversed(traversal[1:]):
        child_xor = 0
        for other, edge in tree_adjacency[vertex]:
            if parent[other] == vertex:
                child_xor ^= tree_edge_bit[edge]
        bit = cotree_parity[vertex] ^ child_xor
        tree_edge_bit[parent_edge[vertex]] = bit
        if bit:
            selected_tree_edges.add(parent_edge[vertex])
    root_xor = cotree_parity[0]
    for other, edge in tree_adjacency[0]:
        assert parent[other] == 0
        root_xor ^= tree_edge_bit[edge]
    assert root_xor == 0

    completion = cotree | selected_tree_edges
    for vertex in range(order):
        assert sum(edge in completion for edge in incident[vertex]) % 2 == 0
    assert cotree <= completion
    return completion


def verify_witness(
    row: dict,
    graph_data: tuple[int, list[tuple[int, int]], list[list[int]]],
) -> tuple[int, dict]:
    order, edges, incident = graph_data
    assert row["status"] == "SUPPORTED_SPECIAL_FIBRE"
    assert row["kind"] == "A_STAR"
    assert row["vertices"] == order

    defect = frozenset(row["defect_edges"])
    roots = [
        vertex
        for vertex in range(order)
        if frozenset(incident[vertex]) == defect
    ]
    assert len(roots) == 1
    root = roots[0]

    trees = [
        check_spanning_tree(order, edges, selected)
        for selected in row["model_trees"]
    ]
    assert len(trees) == 3
    for edge in range(len(edges)):
        expected = 1 if edge in defect else 2
        assert sum(edge in tree for tree in trees) == expected

    completions = [
        fundamental_completion(order, edges, incident, tree)
        for tree in trees
    ]
    flow_values = [
        sum((edge in completions[coordinate]) << coordinate
            for coordinate in range(3))
        for edge in range(len(edges))
    ]
    assert all(flow_values)
    assert flow_values == row["flow_values"]

    labels = row["pair_labels"]
    assert len(labels) == len(edges)
    for edge, pair in enumerate(labels):
        assert len(pair) == 2
        first, second = pair
        assert first < second
        assert first in SUPPORT and second in SUPPORT
        assert first ^ second == flow_values[edge]
    for vertex in range(order):
        for point in range(8):
            parity = 0
            for edge in incident[vertex]:
                parity ^= point in labels[edge]
            assert parity == 0

    normalized = {
        "graph6": row["graph6"],
        "root": root,
        "defect_edges": sorted(defect),
        "trees": [sorted(tree) for tree in trees],
        "completions": [sorted(completion) for completion in completions],
        "flow_values": flow_values,
        "pair_labels": labels,
    }
    return root, normalized


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--witnesses", required=True, type=Path)
    arguments = parser.parse_args()

    source_records = [
        line.strip()
        for line in arguments.input.read_text().splitlines()
        if line.strip()
    ]
    assert len(source_records) == 31
    assert len(set(source_records)) == 31
    graph_data = {record: check_graph(record) for record in source_records}

    supported: dict[tuple[str, int], dict] = {}
    summaries: dict[str, dict] = {}
    with arguments.witnesses.open() as stream:
        for line in stream:
            row = json.loads(line)
            record = row["graph6"]
            assert record in graph_data
            if row["status"] == "GRAPH_DONE":
                assert record not in summaries
                assert row["vertices"] == 44
                assert row["special_fibres_tested"] == 44
                assert row["feasible_special_fibres"] == 44
                assert row["all_bad_special_fibres"] == 0
                summaries[record] = row
                continue
            root, normalized = verify_witness(row, graph_data[record])
            key = (record, root)
            assert key not in supported
            supported[key] = normalized

    assert set(summaries) == set(source_records)
    assert len(supported) == 31 * 44
    for record in source_records:
        assert {
            root for candidate, root in supported if candidate == record
        } == set(range(44))

    semantic_hash = hashlib.sha256()
    for key in sorted(supported):
        encoded = json.dumps(
            supported[key], sort_keys=True, separators=(",", ":")
        ).encode()
        semantic_hash.update(encoded + b"\n")
    result = {
        "status": "PASS",
        "graphs": len(source_records),
        "vertex_star_witnesses": len(supported),
        "support": sorted(SUPPORT),
        "semantic_witness_sha256": semantic_hash.hexdigest(),
        "input_sha256": hashlib.sha256(arguments.input.read_bytes()).hexdigest(),
        "witness_file_sha256": hashlib.sha256(
            arguments.witnesses.read_bytes()
        ).hexdigest(),
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
