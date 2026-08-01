#!/usr/bin/env python3
"""Independent positive-witness audit for the two-edge-sum preprint.

This script deliberately does not import the construction verifier.  It
reads only the canonical base edge list and retained positive witnesses,
then checks their semantics and glues two copies through every possible
root edge.  The negative base claims are checked separately by the LRAT
replay command documented in README.md.
"""

from __future__ import annotations

from collections import deque
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "search/minimum-zero-exchange-countermodel-130v-20260727"


def incidence(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    rows = [[] for _ in range(n)]
    for edge_id, (u, v) in enumerate(edges):
        assert 0 <= u < v < n
        rows[u].append(edge_id)
        rows[v].append(edge_id)
    return rows


def check_graph(n: int, edges: list[tuple[int, int]]) -> None:
    assert len(edges) == len(set(edges))
    rows = incidence(n, edges)
    assert all(len(row) == 3 for row in rows)
    seen = {0}
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for edge_id in rows[u]:
            a, b = edges[edge_id]
            v = b if a == u else a
            if v not in seen:
                seen.add(v)
                queue.append(v)
    assert len(seen) == n

    # An edge is a bridge iff deleting it makes its endpoints disconnected.
    adjacency = [[] for _ in range(n)]
    for edge_id, (u, v) in enumerate(edges):
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))
    for skipped, (source, target) in enumerate(edges):
        reached = {source}
        queue = deque([source])
        while queue and target not in reached:
            u = queue.popleft()
            for v, edge_id in adjacency[u]:
                if edge_id != skipped and v not in reached:
                    reached.add(v)
                    queue.append(v)
        assert target in reached


def check_matching(
    n: int, edges: list[tuple[int, int]], selected: set[int]
) -> None:
    degrees = [0] * n
    for edge_id in selected:
        u, v = edges[edge_id]
        degrees[u] += 1
        degrees[v] += 1
    assert max(degrees, default=0) <= 1


def check_cycle(
    n: int, edges: list[tuple[int, int]], selected: set[int]
) -> None:
    degrees = [0] * n
    for edge_id in selected:
        u, v = edges[edge_id]
        degrees[u] += 1
        degrees[v] += 1
    assert all(degree % 2 == 0 for degree in degrees)


def check_flow(
    n: int, edges: list[tuple[int, int]], values: list[int]
) -> set[int]:
    assert len(values) == len(edges)
    balance = [0] * n
    zeros = set()
    for edge_id, ((u, v), value) in enumerate(zip(edges, values)):
        assert value in (0, 1, 2, 3)
        balance[u] ^= value
        balance[v] ^= value
        if value == 0:
            zeros.add(edge_id)
    assert balance == [0] * n
    return zeros


def check_labels(
    n: int, edges: list[tuple[int, int]], labels: list[str]
) -> list[int]:
    assert len(labels) == len(edges)
    parity = [[0] * 5 for _ in range(n)]
    sizes = [0] * 5
    for (u, v), label in zip(edges, labels):
        coordinates = tuple(map(int, label))
        assert len(coordinates) == 2
        assert 0 <= coordinates[0] < coordinates[1] < 5
        for coordinate in coordinates:
            parity[u][coordinate] ^= 1
            parity[v][coordinate] ^= 1
            sizes[coordinate] += 1
    assert all(bit == 0 for row in parity for bit in row)
    return sizes


def two_sum(
    n: int, edges: list[tuple[int, int]], root: int
) -> tuple[
    list[tuple[int, int]],
    list[dict[int, int]],
    tuple[int, int],
]:
    u, v = edges[root]
    result: list[tuple[int, int]] = []
    maps: list[dict[int, int]] = []
    for side in range(2):
        mapping: dict[int, int] = {}
        offset = side * n
        for edge_id, (a, b) in enumerate(edges):
            if edge_id == root:
                continue
            mapping[edge_id] = len(result)
            result.append((a + offset, b + offset))
        maps.append(mapping)
    cut = (len(result), len(result) + 1)
    result.append((u, u + n))
    result.append((v, v + n))
    return result, maps, cut


def glue_scalar(
    old: list[int] | list[str],
    root: int,
    maps: list[dict[int, int]],
    cut: tuple[int, int],
) -> list[int] | list[str]:
    new = [old[root]] * (2 * (len(old) - 1) + 2)
    for mapping in maps:
        for old_id, new_id in mapping.items():
            new[new_id] = old[old_id]
    new[cut[0]] = old[root]
    new[cut[1]] = old[root]
    return new


def glue_set(
    old: set[int],
    root: int,
    maps: list[dict[int, int]],
    cut: tuple[int, int],
) -> set[int]:
    new = {
        mapping[old_id]
        for mapping in maps
        for old_id in old
        if old_id != root
    }
    if root in old:
        new.update(cut)
    return new


def main() -> None:
    graph = json.loads((BASE / "graph.json").read_text(encoding="utf-8"))
    witness = json.loads((BASE / "witness.json").read_text(encoding="utf-8"))
    n = int(graph["vertices"])
    edges = [(int(e["u"]), int(e["v"])) for e in graph["edges"]]
    assert (n, len(edges)) == (130, 195)
    check_graph(n, edges)

    minimum_flow = list(map(int, witness["displayed_flow_values"]))
    minimum_zeros = check_flow(n, edges, minimum_flow)
    assert len(minimum_zeros) == 5
    assert minimum_zeros == set(map(int, witness["displayed_zero_cut"]))
    check_matching(n, edges, minimum_zeros)

    extension = witness["minimum_extending_witness"]
    flow = list(map(int, extension["flow_values"]))
    cycle_a = set(map(int, extension["cycle_a"]))
    cycle_b = set(map(int, extension["cycle_b"]))
    matching = set(map(int, extension["matching_edges"]))
    labels = list(map(str, extension["five_cdc_labels"]))
    assert len(matching) == 6
    assert matching == cycle_a & cycle_b == check_flow(n, edges, flow)
    check_matching(n, edges, matching)
    check_cycle(n, edges, cycle_a)
    check_cycle(n, edges, cycle_b)
    assert check_labels(n, edges, labels) == [57, 66, 84, 92, 91]

    roots_checked = 0
    for root in range(len(edges)):
        joined, maps, cut = two_sum(n, edges, root)
        check_graph(2 * n, joined)

        joined_minimum_flow = list(
            map(int, glue_scalar(minimum_flow, root, maps, cut))
        )
        joined_minimum_zeros = check_flow(
            2 * n, joined, joined_minimum_flow
        )
        assert len(joined_minimum_zeros) == 10
        check_matching(2 * n, joined, joined_minimum_zeros)

        joined_flow = list(map(int, glue_scalar(flow, root, maps, cut)))
        joined_a = glue_set(cycle_a, root, maps, cut)
        joined_b = glue_set(cycle_b, root, maps, cut)
        joined_matching = check_flow(2 * n, joined, joined_flow)
        assert len(joined_matching) == 12
        assert joined_matching == joined_a & joined_b
        check_matching(2 * n, joined, joined_matching)
        check_cycle(2 * n, joined, joined_a)
        check_cycle(2 * n, joined, joined_b)

        joined_labels = list(
            map(str, glue_scalar(labels, root, maps, cut))
        )
        joined_sizes = check_labels(2 * n, joined, joined_labels)
        assert joined_sizes == [2 * x for x in [57, 66, 84, 92, 91]]
        roots_checked += 1

    print(
        json.dumps(
            {
                "base_graph": "PASS",
                "base_minimum_flow_positive_witness": "PASS",
                "base_size_six_certificate": "PASS",
                "base_five_cdc": "PASS",
                "two_copy_roots_checked": roots_checked,
                "two_copy_order": 260,
                "glued_zero_matching_size": 10,
                "glued_certificate_matching_size": 12,
                "glued_five_cdc": "PASS",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
