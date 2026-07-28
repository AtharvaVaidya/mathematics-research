#!/usr/bin/env python3
"""Coverage/integrity verifier for 13 exact triangle-expansion rows.

This independently regenerates the 13 labelled expansions and checks their
graph premises, row coverage, totals, and hashes.  It does not duplicate the
17,297,280-state C++ enumeration.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_GRAPH6 = "M?AA@BORDGEOEOAo?"
CENSUS = (
    ROOT
    / "output"
    / "jaeger-fano-min-descent-triangle-expansions-16v"
    / "census.jsonl"
)
SOURCE = ROOT / "scratch" / "search_jaeger_star_parity_descent.cpp"
RUNNER = ROOT / "scratch" / "run_jaeger_triangle_expanded_fixedtrap_descent.py"
EXPECTED = {
    CENSUS: "501cc9db6987bc2b458abbf5f82bbcd37ccda74aff9817e91c36a9f6c49d80d3",
    SOURCE: "c087d9de1e8193680f7293543a5d6bd3a3fe95515ca74df6aedc26a852dbe7a5",
    RUNNER: "8d35f1c1b8639b9fcfd8cbdba4913877a2e6cb3506a6934fa0d182070c935833",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    order = ord(record[0]) - 63
    assert 0 < order <= 62
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    cursor = 0
    edges: list[tuple[int, int]] = []
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def encode_graph6(
    order: int, edges: tuple[tuple[int, int], ...]
) -> str:
    edge_set = {tuple(sorted(edge)) for edge in edges}
    bits = [
        int((left, right) in edge_set)
        for right in range(1, order)
        for left in range(right)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = 2 * value + bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def expansion(vertex: int) -> tuple[int, tuple[tuple[int, int], ...]]:
    order, base_edges = parse_graph6(BASE_GRAPH6)
    assert order == 14
    neighbours = [
        right if left == vertex else left
        for left, right in base_edges
        if vertex in (left, right)
    ]
    expanded = [edge for edge in base_edges if vertex not in edge]
    expanded.extend(((14, 15), (15, 16), (16, 14)))
    expanded.extend(zip((14, 15, 16), neighbours))
    labels = sorted({endpoint for edge in expanded for endpoint in edge})
    relabel = {old: new for new, old in enumerate(labels)}
    edges = tuple(
        sorted(
            tuple(sorted((relabel[left], relabel[right])))
            for left, right in expanded
        )
    )
    return 16, edges


def connected(
    order: int,
    edges: tuple[tuple[int, int], ...],
    deleted: frozenset[int] = frozenset(),
) -> bool:
    adjacency = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        if edge in deleted:
            continue
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other in adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                stack.append(other)
    return len(seen) == order


def three_edge_connected(
    order: int, edges: tuple[tuple[int, int], ...]
) -> bool:
    for count in range(3):
        for deleted in itertools.combinations(range(len(edges)), count):
            if not connected(order, edges, frozenset(deleted)):
                return False
    return True


def main() -> None:
    for path, expected in EXPECTED.items():
        assert digest(path) == expected
    rows = [json.loads(line) for line in CENSUS.read_text().splitlines()]
    assert len(rows) == 13
    for vertex, row in zip(range(1, 14), rows):
        order, edges = expansion(vertex)
        graph6 = encode_graph6(order, edges)
        assert row["expanded_vertex"] == vertex
        assert row["graph6"] == graph6
        assert order == 16 and len(edges) == 24
        assert all(left != right for left, right in edges)
        assert len(edges) == len(set(edges))
        degrees = [0] * order
        for left, right in edges:
            degrees[left] += 1
            degrees[right] += 1
        assert degrees == [3] * order
        assert three_edge_connected(order, edges)
        assert row["root"] == 0
        assert row["objective"] == "min-seven-fano-planes"
        assert row["states"] == 1_330_560
        assert row["max_score"] == 4
        assert not row["failure"]
    assert sum(int(row["states"]) for row in rows) == 17_297_280
    print(
        json.dumps(
            {
                "census_sha256": EXPECTED[CENSUS],
                "rows": len(rows),
                "states": 17_297_280,
                "failures": 0,
                "coverage_and_graph_premises_verified": True,
                "trust_boundary": (
                    "C++ exhausts states; this checker independently "
                    "audits inputs, graph premises, rows, totals, and hashes"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
