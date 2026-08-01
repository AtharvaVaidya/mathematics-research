#!/usr/bin/env python3
"""Solver-independent checker for all Petersen--Foster root witnesses."""

from __future__ import annotations

import argparse
from collections import deque
import gzip
import hashlib
import json
from pathlib import Path


PETERSEN = (
    (0, 1), (1, 2), (2, 3), (0, 4), (3, 4),
    (0, 5), (1, 6), (2, 7), (5, 7), (3, 8),
    (5, 8), (6, 8), (4, 9), (6, 9), (7, 9),
)
FOSTER_LCF = (17, -9, 37, -37, 9, -17) * 15
FOSTER_PORTS = (1, 17, 89)
PARENT_SHA256 = "3fe0630cb52d5a0b29a473faff02389195c7e119ea8f7a6f95f3ba9c38272282"


def petersen_foster() -> tuple[int, tuple[tuple[int, int], ...]]:
    foster: set[tuple[int, int]] = set()
    for u in range(90):
        for v in ((u + 1) % 90, (u + FOSTER_LCF[u]) % 90):
            foster.add((min(u, v), max(u, v)))
    assert len(foster) == 135

    edges: list[tuple[int, int]] = []
    for copy in range(10):
        for u, v in foster:
            if 0 not in (u, v):
                edges.append((89 * copy + u - 1, 89 * copy + v - 1))

    used = [0] * 10
    for u, v in PETERSEN:
        a = 89 * u + FOSTER_PORTS[used[u]] - 1
        b = 89 * v + FOSTER_PORTS[used[v]] - 1
        used[u] += 1
        used[v] += 1
        edges.append((min(a, b), max(a, b)))
    assert used == [3] * 10
    return 890, tuple(sorted(edges))


def incidence(n: int, edges: tuple[tuple[int, int], ...]) -> list[list[int]]:
    rows = [[] for _ in range(n)]
    for index, (u, v) in enumerate(edges):
        assert 0 <= u < v < n
        rows[u].append(index)
        rows[v].append(index)
    return rows


def graph_digest(n: int, edges: tuple[tuple[int, int], ...]) -> str:
    data = str(n) + "\n"
    data += "".join(f"{index} {u} {v}\n"
                    for index, (u, v) in enumerate(edges))
    return hashlib.sha256(data.encode("ascii")).hexdigest()


def connected(n: int, edges: tuple[tuple[int, int], ...]) -> bool:
    rows = [[] for _ in range(n)]
    for u, v in edges:
        rows[u].append(v)
        rows[v].append(u)
    seen, todo = {0}, [0]
    while todo:
        for v in rows[todo.pop()]:
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return len(seen) == n


def bridges(n: int, edges: tuple[tuple[int, int], ...]) -> list[int]:
    rows = [[] for _ in range(n)]
    for index, (u, v) in enumerate(edges):
        rows[u].append((v, index))
        rows[v].append((u, index))
    tin, low, found = [-1] * n, [-1] * n, []
    clock = 0

    def visit(u: int, parent_edge: int) -> None:
        nonlocal clock
        tin[u] = low[u] = clock
        clock += 1
        for v, edge in rows[u]:
            if edge == parent_edge:
                continue
            if tin[v] >= 0:
                low[u] = min(low[u], tin[v])
            else:
                visit(v, edge)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    found.append(edge)

    visit(0, -1)
    assert all(value >= 0 for value in tin)
    return sorted(found)


def girth(n: int, edges: tuple[tuple[int, int], ...]) -> int:
    rows = [[] for _ in range(n)]
    for index, (u, v) in enumerate(edges):
        rows[u].append((v, index))
        rows[v].append((u, index))
    best = n + 1
    for source in range(n):
        distance, parent_edge = [-1] * n, [-1] * n
        distance[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v, edge in rows[u]:
                if distance[v] < 0:
                    distance[v] = distance[u] + 1
                    parent_edge[v] = edge
                    queue.append(v)
                elif parent_edge[u] != edge:
                    best = min(best, distance[u] + distance[v] + 1)
    return best


def shortest_cycle_through_edge(
    n: int, edges: tuple[tuple[int, int], ...], target: int
) -> int:
    """Return the length of the shortest cycle containing ``target``."""
    rows = [[] for _ in range(n)]
    for index, (u, v) in enumerate(edges):
        rows[u].append((v, index))
        rows[v].append((u, index))
    source, sink = edges[target]
    distance = [-1] * n
    distance[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v, edge in rows[u]:
            if edge == target or distance[v] >= 0:
                continue
            distance[v] = distance[u] + 1
            if v == sink:
                return distance[v] + 1
            queue.append(v)
    raise AssertionError("target edge is a bridge")


def eliminate(n: int, edges: tuple[tuple[int, int], ...], index: int
              ) -> tuple[int, tuple[tuple[int, int], ...], tuple[int, int]]:
    rows = incidence(n, edges)
    u, v = edges[index]
    u_other = [edge for edge in rows[u] if edge != index]
    v_other = [edge for edge in rows[v] if edge != index]
    assert len(u_other) == len(v_other) == 2

    def other_end(edge: int, vertex: int) -> int:
        a, b = edges[edge]
        return b if a == vertex else a

    u_side = [other_end(edge, u) for edge in u_other]
    v_side = [other_end(edge, v) for edge in v_other]
    assert len(set(u_side + v_side)) == 4

    retained = [edge for edge in edges if u not in edge and v not in edge]
    old_vertices = [vertex for vertex in range(n) if vertex not in (u, v)]
    relabel = {old: new for new, old in enumerate(old_vertices)}
    decorated = [
        (min(relabel[a], relabel[b]), max(relabel[a], relabel[b]), "old")
        for a, b in retained
    ]
    decorated.append((
        min(relabel[u_side[0]], relabel[u_side[1]]),
        max(relabel[u_side[0]], relabel[u_side[1]]),
        "root-u",
    ))
    decorated.append((
        min(relabel[v_side[0]], relabel[v_side[1]]),
        max(relabel[v_side[0]], relabel[v_side[1]]),
        "root-v",
    ))
    decorated.sort()
    roots = (
        next(i for i, row in enumerate(decorated) if row[2] == "root-u"),
        next(i for i, row in enumerate(decorated) if row[2] == "root-v"),
    )
    reduced = tuple((a, b) for a, b, _ in decorated)
    return n - 2, reduced, roots


def check_labels(n: int, edges: tuple[tuple[int, int], ...],
                 roots: tuple[int, int], labels: list[int]) -> None:
    assert len(labels) == len(edges)
    assert all(isinstance(label, int) and label.bit_count() == 2
               and 0 < label < 32 for label in labels)
    rows = incidence(n, edges)
    assert all(len(row) == 3 for row in rows)
    assert all(labels[a] ^ labels[b] ^ labels[c] == 0
               for a, b, c in rows)

    # The SAT job fixed the target factor to Y_01.  Verify connectivity
    # directly from the displayed D5 labels, without transition variables.
    active = [bool((label & 1) ^ ((label & 2) >> 1)) for label in labels]
    assert active[roots[0]] and active[roots[1]]
    seen, todo = {roots[0]}, [roots[0]]
    while todo:
        edge = todo.pop()
        for vertex in edges[edge]:
            local = [other for other in rows[vertex] if active[other]]
            assert len(local) in (0, 2)
            for other in local:
                if other not in seen:
                    seen.add(other)
                    todo.append(other)
    assert roots[1] in seen


def load(path: Path) -> dict[str, object]:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            return json.load(handle)
    return json.loads(path.read_text(encoding="utf-8"))


def check_payload(path: Path, start: int, stop: int,
                  parent_n: int, parent_edges: tuple[tuple[int, int], ...]
                  ) -> tuple[int, str]:
    payload = load(path)
    assert payload["status"] == "ALL_SAT_MODELS_CHECKED"
    assert payload["source"] == "Petersen graph with Foster three-pole substitutions"
    assert payload["elimination_range"] == [start, stop]
    metadata = payload["parent_metadata"]
    assert metadata == {
        "bridge_edge_indices": [],
        "bridgeless": True,
        "edges": 1335,
        "girth": 10,
        "graph_sha256": PARENT_SHA256,
        "loops": 0,
        "parallel_edge_pairs": 0,
        "vertices": 890,
    }
    results = payload["results"]
    assert len(results) == stop - start
    for expected, result in zip(range(start, stop), results):
        assert result["status"] == "SAT_MODEL_CHECKED"
        assert result["eliminated_edge_index"] == expected
        assert result["eliminated_parent_edge"] == list(parent_edges[expected])
        assert result["variables"] == 10656
        assert result["clauses"] == 59052
        assert "seconds" not in result
        reduced_n, reduced_edges, roots = eliminate(parent_n, parent_edges, expected)
        assert len(reduced_edges) == len(set(reduced_edges)) == 1332
        assert all(0 <= u < v < reduced_n for u, v in reduced_edges)
        assert connected(reduced_n, reduced_edges)
        assert not bridges(reduced_n, reduced_edges)
        assert result["roots"] == list(roots)
        assert result["root_edges"] == [list(reduced_edges[root]) for root in roots]
        digest = graph_digest(reduced_n, reduced_edges)
        assert result["graph_sha256"] == digest
        reduced_metadata = result["reduced_metadata"]
        assert reduced_metadata["vertices"] == 888
        assert reduced_metadata["edges"] == 1332
        assert reduced_metadata["loops"] == 0
        assert reduced_metadata["parallel_edge_pairs"] == 0
        assert reduced_metadata["bridgeless"] is True
        assert reduced_metadata["girth"] == 9
        assert reduced_metadata["graph_sha256"] == digest
        # Every cycle avoiding the two artificial roots is a parent cycle and
        # hence has length at least ten.  It is therefore enough to find the
        # shortest cycle through each root; this independently verifies the
        # asserted reduced girth without an all-vertices BFS for every row.
        root_girth = min(shortest_cycle_through_edge(
            reduced_n, reduced_edges, root) for root in roots)
        assert root_girth == 9
        labels = result["labels"]
        assert hashlib.sha256(bytes(labels)).hexdigest() == result["labels_sha256"]
        check_labels(reduced_n, reduced_edges, roots, labels)

        path_edges = result["selected_transition_path"]
        assert isinstance(path_edges, list) and path_edges
        assert all(type(edge) is int and 0 <= edge < len(reduced_edges)
                   for edge in path_edges)
        assert path_edges[0] == roots[0] and path_edges[-1] == roots[1]
        assert len(path_edges) == len(set(path_edges))
        assert all(bool((labels[edge] & 1) ^ ((labels[edge] & 2) >> 1))
                   for edge in path_edges)
        assert all(set(reduced_edges[a]) & set(reduced_edges[b])
                   for a, b in zip(path_edges, path_edges[1:]))
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"SHARD range={start}:{stop} rows={len(results)} sha256={digest} PASS")
    return len(results), digest


def main() -> None:
    if not __debug__:
        raise RuntimeError("refusing to run with Python assertions disabled")
    parser = argparse.ArgumentParser()
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    args = parser.parse_args()

    n, edges = petersen_foster()
    assert len(edges) == len(set(edges)) == 1335
    rows = incidence(n, edges)
    assert all(len(row) == 3 for row in rows)
    assert connected(n, edges) and not bridges(n, edges)
    assert girth(n, edges) == 10
    assert graph_digest(n, edges) == PARENT_SHA256
    print("PARENT vertices=890 edges=1335 simple=1 cubic=1 bridgeless=1 girth=10 PASS")

    first, _ = check_payload(args.first, 0, 668, n, edges)
    second, _ = check_payload(args.second, 668, 1335, n, edges)
    assert first + second == 1335
    print("ALL_ELIMINATIONS rows=1335 literal_models_checked=1335 PASS")


if __name__ == "__main__":
    main()
