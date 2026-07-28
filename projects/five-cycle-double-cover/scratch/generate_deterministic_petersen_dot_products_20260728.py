#!/usr/bin/env python3
"""Generate one deterministic Petersen dot product per graph6 input.

For each input graph, delete two independent edges.  In a fresh Petersen
factor delete the endpoints of one edge, and join the resulting four ports
by a SHA-256-selected permutation.  Unlike a graph lift, this construction
has no assumed FiveCDC preservation rule; every output is solved directly.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from search.canonical.canonical_search import parse_graph6, validate_simple_cubic
from scratch.generate_deterministic_connected_two_lifts_20260728 import encode_graph6


PETERSEN_GRAPH6 = "ICOf@pSb?"


def neighbours(edges: tuple[tuple[int, int], ...], vertex: int) -> tuple[int, ...]:
    return tuple(
        sorted(
            v if u == vertex else u
            for u, v in edges
            if u == vertex or v == vertex
        )
    )


def build_dot_product(
    base_vertices: int,
    base_edges: tuple[tuple[int, int], ...],
    removed: tuple[tuple[int, int], tuple[int, int]],
    permutation: tuple[int, int, int, int],
) -> tuple[int, tuple[tuple[int, int], ...], tuple[int, int]]:
    petersen = parse_graph6(PETERSEN_GRAPH6)
    deleted_edge = min(petersen.edges)
    deleted_vertices = set(deleted_edge)
    petersen_ports = tuple(
        vertex
        for endpoint in deleted_edge
        for vertex in neighbours(petersen.edges, endpoint)
        if vertex not in deleted_vertices
    )
    if len(petersen_ports) != 4:
        raise AssertionError("Petersen boundary has wrong size")
    kept_vertices = [
        vertex for vertex in range(petersen.vertices) if vertex not in deleted_vertices
    ]
    petersen_map = {
        old: base_vertices + new for new, old in enumerate(kept_vertices)
    }
    result = [
        edge for edge in base_edges if edge not in set(removed)
    ]
    result.extend(
        tuple(sorted((petersen_map[u], petersen_map[v])))
        for u, v in petersen.edges
        if u not in deleted_vertices and v not in deleted_vertices
    )
    base_ports = removed[0] + removed[1]
    for position, base_vertex in enumerate(base_ports):
        petersen_vertex = petersen_ports[permutation[position]]
        result.append(tuple(sorted((base_vertex, petersen_map[petersen_vertex]))))
    return (
        base_vertices + 8,
        tuple(sorted(result)),
        deleted_edge,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--g6-output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--seed", default="direct-fivecdc-dot-20260728")
    arguments = parser.parse_args()

    bases = [
        line.strip()
        for line in arguments.input.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    permutations = tuple(itertools.permutations(range(4)))
    output: list[str] = []
    metadata: list[dict[str, object]] = []
    for index, record in enumerate(bases, 1):
        graph = parse_graph6(record)
        checks = validate_simple_cubic(graph)
        if not all(checks[key] for key in ("simple", "cubic", "connected", "bridgeless")):
            raise ValueError(f"base row {index} fails premises: {checks}")
        pairs = tuple(
            (first, second)
            for at, first in enumerate(graph.edges)
            for second in graph.edges[at + 1 :]
            if not set(first) & set(second)
        )
        digest = hashlib.sha256(
            f"{arguments.seed}\0{record}".encode("ascii")
        ).digest()
        selector = int.from_bytes(digest, "big")
        removed = pairs[selector % len(pairs)]
        permutation = permutations[(selector // len(pairs)) % len(permutations)]
        n, edges, petersen_edge = build_dot_product(
            graph.vertices, graph.edges, removed, permutation
        )
        lifted_record = encode_graph6(n, list(edges))
        decoded = parse_graph6(lifted_record)
        if decoded.vertices != n or decoded.edges != edges:
            raise AssertionError("dot-product graph6 round trip failed")
        output.append(lifted_record)
        metadata.append(
            {
                "base_index": index,
                "base_graph6": record,
                "removed_base_edges": removed,
                "deleted_petersen_edge": petersen_edge,
                "port_permutation": permutation,
                "dot_graph6": lifted_record,
            }
        )
    arguments.g6_output.write_text("\n".join(output) + "\n", encoding="ascii")
    arguments.metadata.write_text(
        "\n".join(json.dumps(row, sort_keys=True) for row in metadata) + "\n",
        encoding="ascii",
    )
    print(json.dumps({"bases": len(bases), "outputs": len(output)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
