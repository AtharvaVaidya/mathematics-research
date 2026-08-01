#!/usr/bin/env python3
"""Check the paired cyclic-cut inequality on the retained eight-mark core.

This is a finite diagnostic for
``docs/connected-eight-mark-paired-cut-condition.md``.  It enumerates all
core cuts of size at most three once, then tests all 105 perfect pairings
of the eight marks.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import networkx as nx

from stable8_pairing_five_cdc_search import (
    DEFAULT_GRAPH6,
    DEFAULT_MARKS,
    perfect_pairings,
)


def canonical_shore(vertices: frozenset[int], order: int) -> frozenset[int]:
    complement = frozenset(set(range(order)) - set(vertices))
    left = tuple(sorted(vertices))
    right = tuple(sorted(complement))
    return vertices if left <= right else complement


def has_cycle(graph: nx.Graph, vertices: frozenset[int]) -> bool:
    subgraph = graph.subgraph(vertices)
    return any(
        subgraph.subgraph(component).number_of_edges() >= len(component)
        for component in nx.connected_components(subgraph)
    )


def cut_edges(graph: nx.Graph, shore: frozenset[int]) -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted(
            tuple(sorted((u, v)))
            for u, v in graph.edges()
            if (u in shore) != (v in shore)
        )
    )


def enumerate_small_cyclic_cuts(
    graph: nx.Graph,
) -> list[dict[str, object]]:
    edges = tuple(tuple(sorted(edge)) for edge in graph.edges())
    order = graph.number_of_nodes()
    shores: dict[frozenset[int], tuple[tuple[int, int], ...]] = {}

    for size in range(1, 4):
        for removed in itertools.combinations(edges, size):
            reduced = graph.copy()
            reduced.remove_edges_from(removed)
            components = [
                frozenset(component) for component in nx.connected_components(reduced)
            ]
            if len(components) == 1:
                continue
            # Every cut of size at most three appears as a union of components
            # after deleting a superset of its boundary.  Quotient by complements.
            for mask in range(1, 1 << (len(components) - 1)):
                shore = frozenset(
                    vertex
                    for index, component in enumerate(components)
                    if (mask >> index) & 1
                    for vertex in component
                )
                shore = canonical_shore(shore, order)
                boundary = cut_edges(graph, shore)
                if len(boundary) <= 3:
                    shores[shore] = boundary

    all_vertices = frozenset(graph.nodes())
    rows: list[dict[str, object]] = []
    for shore, boundary in shores.items():
        opposite = all_vertices - shore
        if not has_cycle(graph, shore) or not has_cycle(graph, opposite):
            continue
        rows.append(
            {
                "shore": sorted(shore),
                "boundary": [list(edge) for edge in boundary],
                "boundary_size": len(boundary),
            }
        )
    rows.sort(
        key=lambda row: (
            int(row["boundary_size"]),
            tuple(row["shore"]),  # type: ignore[arg-type]
        )
    )
    return rows


def mark_partition(
    shore: frozenset[int],
) -> tuple[frozenset[int], frozenset[int], frozenset[int]]:
    internal = frozenset(
        index for index, (u, v) in enumerate(DEFAULT_MARKS) if u in shore and v in shore
    )
    boundary = frozenset(
        index for index, (u, v) in enumerate(DEFAULT_MARKS) if (u in shore) != (v in shore)
    )
    external = frozenset(range(len(DEFAULT_MARKS))) - internal - boundary
    return internal, boundary, external


def strict_pair_crossings(
    pairing: tuple[tuple[int, int], ...],
    internal: frozenset[int],
    external: frozenset[int],
) -> int:
    return sum(
        ((first in internal and second in external)
         or (second in internal and first in external))
        for first, second in pairing
    )


def main() -> int:
    graph = nx.from_graph6_bytes(DEFAULT_GRAPH6.encode("ascii"))
    cuts = enumerate_small_cyclic_cuts(graph)
    rows = []
    survivors = 0
    minimum_scores: dict[int, int] = {}

    for index, pairing in enumerate(
        perfect_pairings(tuple(range(len(DEFAULT_MARKS)))), 1
    ):
        violations = []
        minimum_score = 99
        for cut in cuts:
            shore = frozenset(int(vertex) for vertex in cut["shore"])  # type: ignore[arg-type]
            internal, boundary, external = mark_partition(shore)
            crossing_pairs = strict_pair_crossings(pairing, internal, external)
            score = int(cut["boundary_size"]) + crossing_pairs
            minimum_score = min(minimum_score, score)
            if score < 4:
                violations.append(
                    {
                        "shore": cut["shore"],
                        "boundary": cut["boundary"],
                        "boundary_size": cut["boundary_size"],
                        "internal_marks": sorted(internal),
                        "boundary_marks": sorted(boundary),
                        "external_marks": sorted(external),
                        "strict_pair_crossings": crossing_pairs,
                        "score": score,
                    }
                )
        if not violations:
            survivors += 1
        minimum_scores[minimum_score] = minimum_scores.get(minimum_score, 0) + 1
        rows.append(
            {
                "index": index,
                "pairing": [list(pair) for pair in pairing],
                "minimum_score": minimum_score,
                "paired_cut_condition": not violations,
                "violations": violations,
            }
        )

    report = {
        "schema": "stable8-paired-cyclic-cut-check-v1",
        "graph6": DEFAULT_GRAPH6,
        "marks": [list(mark) for mark in DEFAULT_MARKS],
        "vertices": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "small_cyclic_cuts": cuts,
        "small_cyclic_cut_count": len(cuts),
        "pairing_count": len(rows),
        "surviving_pairings": survivors,
        "minimum_score_histogram": {
            str(score): count for score, count in sorted(minimum_scores.items())
        },
        "rows": rows,
    }
    output = Path("scratch/stable8-paired-cut-result.json")
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "small_cyclic_cuts": len(cuts),
                "pairings": len(rows),
                "survivors": survivors,
                "minimum_score_histogram": report["minimum_score_histogram"],
                "output": str(output),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
