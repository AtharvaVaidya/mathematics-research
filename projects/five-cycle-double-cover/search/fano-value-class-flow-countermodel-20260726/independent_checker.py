#!/usr/bin/env python3
"""Direct checker for the frozen Fano-value-class countermodel.

This checker does not import the producer or the even-marked-circuit
criterion.  For each of the seven matchings it literally enumerates every
edge subset of the complement, retains the T-joins, and checks every pair
for a common edge.
"""

from __future__ import annotations

from collections import deque
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def boundary(mask: int, edges: list[tuple[int, int]]) -> int:
    result = 0
    for edge, (u, v) in enumerate(edges):
        if (mask >> edge) & 1:
            result ^= (1 << u) | (1 << v)
    return result


def graph6_encode(vertices: int, edges: list[tuple[int, int]]) -> str:
    if not 0 <= vertices <= 62:
        raise ValueError("checker implements only the one-byte graph6 order")
    edge_set = {tuple(sorted(edge)) for edge in edges}
    bits = [
        int((u, v) in edge_set)
        for v in range(1, vertices)
        for u in range(v)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload = "".join(
        chr(
            63
            + sum(
                bits[offset + bit] << (5 - bit)
                for bit in range(6)
            )
        )
        for offset in range(0, len(bits), 6)
    )
    return chr(vertices + 63) + payload


def connected(
    vertices: int,
    edges: list[tuple[int, int]],
    omitted: int | None = None,
) -> bool:
    adjacency = [[] for _ in range(vertices)]
    for edge, (u, v) in enumerate(edges):
        if edge == omitted:
            continue
        adjacency[u].append(v)
        adjacency[v].append(u)
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for other in adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return len(seen) == vertices


def main() -> None:
    data = json.loads((ROOT / "instance.json").read_text())
    vertices = int(data["vertices"])
    edges = [tuple(map(int, edge)) for edge in data["edges"]]
    values = [int(value) for value in data["flow_values_by_edge"]]
    assert len(edges) == len(values) == 15
    assert len(set(edges)) == len(edges)
    assert all(0 <= u < v < vertices for u, v in edges)
    degrees = [0] * vertices
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
    assert degrees == [3] * vertices
    assert connected(vertices, edges)
    assert all(
        connected(vertices, edges, omitted=edge)
        for edge in range(len(edges))
    )
    assert graph6_encode(vertices, edges) == data["graph6"]

    incident_values = [0] * vertices
    for value, (u, v) in zip(values, edges):
        assert 1 <= value <= 7
        incident_values[u] ^= value
        incident_values[v] ^= value
    assert incident_values == [0] * vertices

    expected_classes = {
        int(value): [int(edge) for edge in support]
        for value, support in data["value_class_edges"].items()
    }
    classes = {
        value: [
            edge
            for edge, edge_value in enumerate(values)
            if edge_value == value
        ]
        for value in range(1, 8)
    }
    assert classes == expected_classes

    audit: dict[str, object] = {}
    all_edges = range(len(edges))
    for value in range(1, 8):
        matching_edges = classes[value]
        occupied: set[int] = set()
        matching_mask = 0
        for edge in matching_edges:
            u, v = edges[edge]
            assert u not in occupied and v not in occupied
            occupied.update((u, v))
            matching_mask |= 1 << edge
        terminals = boundary(matching_mask, edges)
        complement = [
            edge for edge in all_edges if edge not in matching_edges
        ]
        t_joins: list[int] = []
        for choice in range(1 << len(complement)):
            mask = sum(
                1 << edge
                for bit, edge in enumerate(complement)
                if (choice >> bit) & 1
            )
            if boundary(mask, edges) == terminals:
                t_joins.append(mask)
        minimum_intersection = min(
            (left & right).bit_count()
            for left in t_joins
            for right in t_joins
        )
        assert len(t_joins) == int(data["t_join_counts"][str(value)])
        assert minimum_intersection == int(
            data["minimum_pairwise_t_join_intersection"][str(value)]
        )
        assert minimum_intersection > 0
        audit[str(value)] = {
            "matching_edges": matching_edges,
            "terminals": [
                vertex
                for vertex in range(vertices)
                if (terminals >> vertex) & 1
            ],
            "t_joins": len(t_joins),
            "minimum_pairwise_intersection": minimum_intersection,
        }

    coloring = [
        int(color) for color in data["three_edge_coloring_by_edge"]
    ]
    assert len(coloring) == len(edges)
    for vertex in range(vertices):
        incident = [
            coloring[edge]
            for edge, (u, v) in enumerate(edges)
            if vertex in (u, v)
        ]
        assert sorted(incident) == [0, 1, 2]

    covers = [
        {
            edge
            for edge, color in enumerate(coloring)
            if color != omitted_color
        }
        for omitted_color in range(3)
    ] + [set(), set()]
    for cover in covers:
        assert boundary(sum(1 << edge for edge in cover), edges) == 0
    assert all(
        sum(edge in cover for cover in covers) == 2
        for edge in range(len(edges))
    )

    print(
        json.dumps(
            {
                "status": "VERIFIED",
                "graph6": data["graph6"],
                "simple_cubic_connected_bridgeless": True,
                "nowhere_zero_f2_3_flow": True,
                "all_seven_value_classes_are_matchings": True,
                "all_seven_fail_two_t_join_packing": True,
                "explicit_standard_five_cdc": True,
                "audit": audit,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
