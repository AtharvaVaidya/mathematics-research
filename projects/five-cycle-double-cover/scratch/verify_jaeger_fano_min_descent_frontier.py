#!/usr/bin/env python3
"""Coverage and integrity verifier for the Fano-minimum descent census.

This independently regenerates the canonical graph streams, checks
3-edge-connectivity, recomputes vertex automorphism orbits, and compares
the exact rooted-instance list with the frozen census.  The C++ program is
the trusted whole-state enumerator; this verifier audits its input coverage,
output consistency, totals, and file integrity rather than re-enumerating
the 529 million states in a second language.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from collections import Counter
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "output" / "jaeger-fano-min-descent-through14" / "census.jsonl"
EXPECTED_SHA256 = "f1d720265cc58a732cf2b58920b8dacc12f36191cecc731949622f5c80f4f2e0"
EXPECTED_GRAPHS = {4: 1, 6: 2, 8: 4, 10: 14, 12: 57, 14: 341}
EXPECTED_ROOTED = {4: 1, 6: 2, 8: 8, 10: 44, 12: 329, 14: 3183}
EXPECTED_STATES = {
    4: 6,
    6: 84,
    8: 2304,
    10: 96720,
    12: 5994624,
    14: 523056384,
}


def three_edge_connected(graph: nx.Graph) -> bool:
    edges = tuple(graph.edges())
    for count in range(3):
        for deleted in itertools.combinations(range(len(edges)), count):
            changed = graph.copy()
            for edge in deleted:
                changed.remove_edge(*edges[edge])
            if not nx.is_connected(changed):
                return False
    return True


def vertex_orbit_representatives(graph: nx.Graph) -> tuple[int, ...]:
    parent = list(range(len(graph)))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def union(first: int, second: int) -> None:
        first, second = find(first), find(second)
        if first != second:
            parent[second] = first

    matcher = nx.algorithms.isomorphism.GraphMatcher(graph, graph)
    for mapping in matcher.isomorphisms_iter():
        for first, second in mapping.items():
            union(first, second)
    return tuple(sorted({find(vertex) for vertex in graph}))


def main() -> None:
    assert hashlib.sha256(CENSUS.read_bytes()).hexdigest() == EXPECTED_SHA256
    rows = [json.loads(line) for line in CENSUS.read_text().splitlines()]
    actual_keys = [
        (
            int(row["order"]),
            int(row["canonical_graph_index"]),
            str(row["graph6"]),
            int(row["root"]),
        )
        for row in rows
    ]
    expected_keys = []
    graph_counts = Counter()
    geng = Path("/opt/homebrew/bin/geng")
    for order in range(4, 15, 2):
        completed = subprocess.run(
            [str(geng), "-Cq", "-d3", "-D3", str(order)],
            check=True,
            capture_output=True,
            text=True,
        )
        for graph_index, graph6 in enumerate(completed.stdout.splitlines()):
            if not graph6:
                continue
            graph = nx.from_graph6_bytes(graph6.encode())
            assert len(graph) == order
            assert all(degree == 3 for _, degree in graph.degree())
            if not three_edge_connected(graph):
                continue
            graph_counts[order] += 1
            for root in vertex_orbit_representatives(graph):
                expected_keys.append((order, graph_index, graph6, root))
    assert actual_keys == expected_keys
    assert dict(graph_counts) == EXPECTED_GRAPHS

    rooted = Counter(int(row["order"]) for row in rows)
    states = Counter()
    for row in rows:
        order = int(row["order"])
        states[order] += int(row["states"])
        assert row["objective"] == "min-seven-fano-planes"
        assert not row["failure"]
        assert int(row["states"]) > 0
        assert int(row["max_score"]) in (0, 2, 4)
    assert dict(rooted) == EXPECTED_ROOTED
    assert dict(states) == EXPECTED_STATES
    assert len(rows) == 3567
    assert sum(states.values()) == 529150122
    print(
        json.dumps(
            {
                "census_sha256": EXPECTED_SHA256,
                "graphs": EXPECTED_GRAPHS,
                "rooted_orbit_instances": EXPECTED_ROOTED,
                "states": EXPECTED_STATES,
                "total_states": sum(states.values()),
                "failures": 0,
                "coverage_verified": True,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
