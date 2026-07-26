#!/usr/bin/env python3
"""Repair the rooted 28-vertex witness's two-cut by one cross-shore switch.

For every eligible internal edge on each side of the displayed 3+1
marked two-cut, delete the two edges and reconnect their four ends
cross-shore in both possible ways.  The original two cut edges remain,
so the old two-cut becomes a four-edge cut.  All vertices and the four
marked/root edge endpoint labels are retained.

The output is a graph6 stream for exact downstream screening.  This is a
structured candidate generator, not a completeness claim.
"""

from __future__ import annotations

import argparse
from itertools import product
import json

import networkx as nx

from verify_rooted_four_mark_countermodel import (
    GRAPH6,
    MARK_EDGES,
    ROOT_EDGE,
    parse_graph6,
)


LEFT = frozenset(range(20))
RIGHT = frozenset(range(20, 28))
SECOND_CUT_EDGE = (8, 24)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit analyzer-ready JSON rows instead of plain graph6",
    )
    arguments = parser.parse_args()
    order, parsed_edges = parse_graph6(GRAPH6)
    assert order == 28
    base = nx.Graph()
    base.add_nodes_from(range(order))
    base.add_edges_from(parsed_edges)
    marks = {tuple(sorted(edge)) for edge in MARK_EDGES}
    protected = marks | {tuple(sorted(ROOT_EDGE)), SECOND_CUT_EDGE}
    left_edges = [
        edge
        for edge in base.edges()
        if edge[0] in LEFT
        and edge[1] in LEFT
        and tuple(sorted(edge)) not in protected
    ]
    right_edges = [
        edge
        for edge in base.edges()
        if edge[0] in RIGHT
        and edge[1] in RIGHT
        and tuple(sorted(edge)) not in protected
    ]

    emitted: set[bytes] = set()
    for left_edge, right_edge in product(left_edges, right_edges):
        a, b = left_edge
        c, d = right_edge
        for cross_edges in (((a, c), (b, d)), ((a, d), (b, c))):
            graph = base.copy()
            graph.remove_edge(a, b)
            graph.remove_edge(c, d)
            if any(graph.has_edge(*edge) for edge in cross_edges):
                continue
            graph.add_edges_from(cross_edges)
            if (
                not nx.is_connected(graph)
                or set(dict(graph.degree()).values()) != {3}
                or any(not graph.has_edge(*edge) for edge in protected)
            ):
                continue
            record = nx.to_graph6_bytes(graph, header=False).strip()
            if record in emitted:
                continue
            emitted.add(record)
            decoded = record.decode("ascii")
            if arguments.json:
                print(
                    json.dumps(
                        {
                            "graph6": decoded,
                            "mark_edges": MARK_EDGES,
                        },
                        sort_keys=True,
                    )
                )
            else:
                print(decoded)

    print(f"generated={len(emitted)}", file=__import__("sys").stderr)


if __name__ == "__main__":
    main()
