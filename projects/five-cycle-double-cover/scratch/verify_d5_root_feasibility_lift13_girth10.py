#!/usr/bin/env python3
"""Independent semantic verifier for the lift-13 root-feasibility report.

This checker does not parse a SAT solver assignment or import the producer.
It reconstructs every edge elimination from the frozen parent graph, checks
the reported D5 labels directly, and verifies root factor connectivity.
"""

from __future__ import annotations

from collections import deque
import hashlib
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "artifacts/structured/graphs/lift13_petersen_girth10.json"
REPORT_PATH = (
    ROOT / "output/d5-root-feasibility-lift13-girth10/all-eliminations.json"
)


def load_graph(path: Path) -> tuple[int, tuple[tuple[int, int], ...]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    vertex_count = data["vertices"]
    assert isinstance(vertex_count, int)
    edges = tuple(sorted(tuple(sorted((row["u"], row["v"]))) for row in data["edges"]))
    assert len(edges) == len(set(edges))
    return vertex_count, edges


def adjacency(
    vertex_count: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    rows = [[] for _ in range(vertex_count)]
    for edge, (u, v) in enumerate(edges):
        assert u != v
        rows[u].append(edge)
        rows[v].append(edge)
    return tuple(tuple(sorted(row)) for row in rows)


def other_end(edge: tuple[int, int], vertex: int) -> int:
    assert vertex in edge
    return edge[1] if edge[0] == vertex else edge[0]


def girth(vertex_count: int, edges: tuple[tuple[int, int], ...]) -> int:
    neighbors = [[] for _ in range(vertex_count)]
    for u, v in edges:
        neighbors[u].append(v)
        neighbors[v].append(u)
    best = vertex_count + 1
    for source in range(vertex_count):
        distance = [-1] * vertex_count
        parent = [-1] * vertex_count
        distance[source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for neighbor in neighbors[vertex]:
                if distance[neighbor] < 0:
                    distance[neighbor] = distance[vertex] + 1
                    parent[neighbor] = vertex
                    queue.append(neighbor)
                elif parent[vertex] != neighbor:
                    best = min(
                        best, distance[vertex] + distance[neighbor] + 1
                    )
    return best


def three_edge_cuts(
    vertex_count: int, edges: tuple[tuple[int, int], ...]
) -> set[tuple[int, int, int]]:
    """Enumerate 3-cuts as bridges left after deleting each edge pair."""

    incident = [[] for _ in range(vertex_count)]
    for edge, (u, v) in enumerate(edges):
        incident[u].append((v, edge))
        incident[v].append((u, edge))
    cuts: set[tuple[int, int, int]] = set()
    for first, second in combinations(range(len(edges)), 2):
        discovery = [-1] * vertex_count
        low = [0] * vertex_count
        timer = 0

        def visit(vertex: int, parent_edge: int) -> None:
            nonlocal timer
            discovery[vertex] = low[vertex] = timer
            timer += 1
            for neighbor, edge in incident[vertex]:
                if edge in (first, second) or edge == parent_edge:
                    continue
                if discovery[neighbor] >= 0:
                    low[vertex] = min(low[vertex], discovery[neighbor])
                else:
                    visit(neighbor, edge)
                    low[vertex] = min(low[vertex], low[neighbor])
                    if low[neighbor] > discovery[vertex]:
                        cuts.add(tuple(sorted((first, second, edge))))

        visit(0, -1)
        # This simultaneously rules out cuts of size at most two.
        assert all(value >= 0 for value in discovery)
    return cuts


def eliminate(
    vertex_count: int,
    parent_edges: tuple[tuple[int, int], ...],
    index: int,
) -> tuple[int, tuple[tuple[int, int], ...], tuple[int, int]]:
    u, v = parent_edges[index]
    parent_rows = adjacency(vertex_count, parent_edges)
    u_side = sorted(
        other_end(parent_edges[edge], u)
        for edge in parent_rows[u]
        if v not in parent_edges[edge]
    )
    v_side = sorted(
        other_end(parent_edges[edge], v)
        for edge in parent_rows[v]
        if u not in parent_edges[edge]
    )
    assert len(u_side) == len(v_side) == 2
    assert len(set(u_side + v_side)) == 4

    survivors = [vertex for vertex in range(vertex_count) if vertex not in (u, v)]
    renaming = {old: new for new, old in enumerate(survivors)}
    old_edges = [
        edge
        for edge in parent_edges
        if u not in edge and v not in edge
    ]
    old_edges.extend((tuple(u_side), tuple(v_side)))
    reduced_edges = tuple(
        sorted(
            tuple(sorted((renaming[a], renaming[b])))
            for a, b in old_edges
        )
    )
    assert len(reduced_edges) == len(set(reduced_edges))
    roots_as_edges = (
        tuple(sorted(renaming[x] for x in u_side)),
        tuple(sorted(renaming[x] for x in v_side)),
    )
    roots = tuple(reduced_edges.index(edge) for edge in roots_as_edges)
    return vertex_count - 2, reduced_edges, roots


def verify_labels(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    roots: tuple[int, int],
    labels: tuple[int, ...],
) -> None:
    assert len(labels) == len(edges)
    assert all(label.bit_count() == 2 and 0 < label < 32 for label in labels)
    rows = adjacency(vertex_count, edges)
    assert {len(row) for row in rows} == {3}
    for row in rows:
        assert labels[row[0]] ^ labels[row[1]] ^ labels[row[2]] == 0

    active = {
        edge
        for edge, label in enumerate(labels)
        if ((label >> 0) & 1) ^ ((label >> 1) & 1)
    }
    assert roots[0] in active and roots[1] in active
    reached = {roots[0]}
    queue = deque([roots[0]])
    while queue:
        edge = queue.popleft()
        for vertex in edges[edge]:
            for other in rows[vertex]:
                if other in active and other not in reached:
                    reached.add(other)
                    queue.append(other)
    assert roots[1] in reached


def main() -> None:
    vertex_count, parent_edges = load_graph(GRAPH_PATH)
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    assert report["status"] == "NO_COUNTEREXAMPLE"
    assert report["parent_vertices"] == vertex_count == 130
    assert report["parent_edges"] == len(parent_edges) == 195
    assert report["parent_girth"] == girth(vertex_count, parent_edges) == 10
    parent_rows = adjacency(vertex_count, parent_edges)
    assert three_edge_cuts(vertex_count, parent_edges) == {
        tuple(sorted(row)) for row in parent_rows
    }
    assert report["parent_graph_sha256"] == hashlib.sha256(
        GRAPH_PATH.read_bytes()
    ).hexdigest()
    assert report["eliminations"] == len(report["results"]) == len(parent_edges)

    reduced_girths = set()
    for expected_index, row in enumerate(report["results"]):
        assert row["eliminated_edge_index"] == expected_index
        assert tuple(row["eliminated_parent_edge"]) == parent_edges[expected_index]
        reduced_n, reduced_edges, roots = eliminate(
            vertex_count, parent_edges, expected_index
        )
        assert row["reduced_vertices"] == reduced_n == 128
        assert row["reduced_edges"] == len(reduced_edges) == 192
        assert tuple(row["roots"]) == roots
        assert tuple(tuple(edge) for edge in row["root_edges"]) == tuple(
            reduced_edges[root] for root in roots
        )
        assert row["status"] == "SAT"
        reduced_girth = girth(reduced_n, reduced_edges)
        assert row["reduced_girth"] == reduced_girth
        reduced_girths.add(reduced_girth)
        labels = tuple(int(value, 16) for value in row["labels_hex"])
        verify_labels(reduced_n, reduced_edges, roots, labels)

    assert reduced_girths == {9, 10}
    print(
        "PASS: 195/195 edge eliminations of the 130-vertex girth-10 "
        "cyclically-4 lift have independently verified root-good "
        "D5-flow witnesses; reduced girths are 9 or 10"
    )


if __name__ == "__main__":
    main()
