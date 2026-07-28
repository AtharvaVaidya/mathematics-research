#!/usr/bin/env python3
"""Verify the complete order-16 root-component-distance summary.

This verifier reads the four frozen JSONL shards, checks their hashes and
summary arithmetic, and independently recomputes the cyclically
4-edge-connected/girth stratification from each graph6 record.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from pathlib import Path


EXPECTED_TOTALS = {
    "graphs": 3874,
    "flows_mod_s5": 15187695,
    "initially_bad_state_root_pairs": 223926065,
}
EXPECTED_MAXIMUM_HISTOGRAM = {0: 145, 1: 966, 2: 2418, 3: 325, 4: 19, 5: 1}
EXPECTED_REDUCED_HISTOGRAM = {1: 23, 2: 478, 3: 100, 4: 6}
EXPECTED_GIRTH_DISTANCE = {
    (4, 1): 15,
    (4, 2): 438,
    (4, 3): 99,
    (4, 4): 6,
    (5, 1): 8,
    (5, 2): 39,
    (5, 3): 1,
    (6, 2): 1,
}


def decode_graph6(row: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    if not row or row[0] == "~":
        raise ValueError("only short graph6 records are expected")
    vertices = ord(row[0]) - 63
    bits: list[int] = []
    for character in row[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, tuple(edges)


def adjacency_masks(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[int, ...]:
    masks = [0] * vertices
    degrees = [0] * vertices
    for left, right in edges:
        masks[left] |= 1 << right
        masks[right] |= 1 << left
        degrees[left] += 1
        degrees[right] += 1
    assert degrees == [3] * vertices
    seen = 1
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        unseen = masks[vertex] & ~seen
        while unseen:
            bit = unseen & -unseen
            unseen ^= bit
            seen |= bit
            queue.append(bit.bit_length() - 1)
    assert seen == (1 << vertices) - 1
    return tuple(masks)


def is_cyclically_four(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    adjacency: tuple[int, ...],
) -> bool:
    """Return whether no cut of size at most three has two cyclic shores."""

    # Quotient complementary shores by requiring vertex zero on the shore.
    # Build internal edge counts incrementally over the other n-1 vertices.
    count = 1 << (vertices - 1)
    internal = [0] * count
    total_edges = len(edges)
    for reduced in range(count):
        if reduced:
            bit = reduced & -reduced
            previous = reduced ^ bit
            vertex = bit.bit_length()
            shore_previous = (previous << 1) | 1
            internal[reduced] = (
                internal[previous]
                + (adjacency[vertex] & shore_previous).bit_count()
            )
        shore = (reduced << 1) | 1
        shore_vertices = shore.bit_count()
        if shore_vertices == vertices:
            continue
        shore_edges = internal[reduced]
        cut = 3 * shore_vertices - 2 * shore_edges
        if cut > 3:
            continue
        other_vertices = vertices - shore_vertices
        other_edges = total_edges - shore_edges - cut
        if shore_edges >= shore_vertices and other_edges >= other_vertices:
            return False
    return True


def girth(vertices: int, adjacency: tuple[int, ...]) -> int:
    best = vertices + 1
    for source in range(vertices):
        distance = [-1] * vertices
        parent = [-1] * vertices
        distance[source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            neighbors = adjacency[vertex]
            while neighbors:
                bit = neighbors & -neighbors
                neighbors ^= bit
                other = bit.bit_length() - 1
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    best = min(best, distance[vertex] + distance[other] + 1)
    assert best <= vertices
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--directory",
        type=Path,
        default=Path(__file__).resolve().parent,
    )
    args = parser.parse_args()
    summary_path = args.directory / "d5-root-component-distance-order16-summary.json"
    summary = json.loads(summary_path.read_text())

    rows = []
    for shard in summary["shards"]:
        path = args.directory / shard["file"]
        data = path.read_bytes()
        assert len(data) == shard["bytes"]
        assert hashlib.sha256(data).hexdigest() == shard["sha256"]
        parsed = [json.loads(line) for line in data.splitlines()]
        assert parsed[-1] == {"status": "PASS", "graphs": shard["graph_count"]}
        graph_rows = [row for row in parsed if row["status"] == "GRAPH_DONE"]
        assert len(graph_rows) == shard["graph_count"]
        rows.extend(graph_rows)

    totals = {
        "graphs": len(rows),
        "flows_mod_s5": sum(row["flows_mod_s5"] for row in rows),
        "initially_bad_state_root_pairs": sum(
            row["initially_bad_state_root_pairs"] for row in rows
        ),
    }
    assert totals == EXPECTED_TOTALS
    assert Counter(
        row["maximum_root_switch_distance"] for row in rows
    ) == EXPECTED_MAXIMUM_HISTOGRAM

    maximum_rows = [
        row for row in rows if row["maximum_root_switch_distance"] == 5
    ]
    assert len(maximum_rows) == 1
    maximum = maximum_rows[0]
    frozen = summary["unique_distance_five_graph"]
    assert maximum["graph6"] == frozen["graph6"]
    assert maximum["flows_mod_s5"] == frozen["normalized_d5_flows_mod_s5"]
    assert (
        maximum["initially_bad_state_root_pairs"]
        == frozen["initially_root_bad_state_root_pairs"]
    )
    assert maximum["maximum_witness"]["state_hex"] == frozen["witness_state_hex"]
    assert maximum["maximum_witness"]["roots"] == frozen["root_edge_indices"]

    reduced_histogram: Counter[int] = Counter()
    girth_distance: Counter[tuple[int, int]] = Counter()
    for row in rows:
        vertices, edges = decode_graph6(row["graph6"])
        assert vertices == 16
        assert len(edges) == 24
        adjacency = adjacency_masks(vertices, edges)
        if not is_cyclically_four(vertices, edges, adjacency):
            continue
        distance = row["maximum_root_switch_distance"]
        reduced_histogram[distance] += 1
        girth_distance[(girth(vertices, adjacency), distance)] += 1

    assert sum(reduced_histogram.values()) == 607
    assert reduced_histogram == EXPECTED_REDUCED_HISTOGRAM
    assert girth_distance == EXPECTED_GIRTH_DISTANCE
    print(
        "PASS: 3,874 order-16 graphs, 15,187,695 normalized flows, "
        "223,926,065 initially bad pairs, maximum distance five; "
        "607 cyclically-4 graphs match the frozen true-girth stratification"
    )


if __name__ == "__main__":
    main()
