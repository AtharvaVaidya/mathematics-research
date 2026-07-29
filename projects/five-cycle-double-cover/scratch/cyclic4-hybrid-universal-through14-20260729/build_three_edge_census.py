#!/usr/bin/env python3
"""Diagnostic census of all 3-edge-connected cubic macros through order 14."""

from __future__ import annotations

import json
from pathlib import Path

from build_census import (
    ORDERS,
    automorphisms,
    connected,
    decode_graph6,
    graph_girth,
    incidence,
    junction_orbits,
)


HERE = Path(__file__).resolve().parent


def three_edge_connected(vertices, masks):
    full = (1 << vertices) - 1
    for shore in range(1, full):
        if not (shore & 1) or shore == full:
            continue
        cut = sum(
            (masks[vertex] & (full ^ shore)).bit_count()
            for vertex in range(vertices)
            if shore & (1 << vertex)
        )
        if cut < 3:
            return False
    return True


def main() -> int:
    by_order = {}
    total_graphs = 0
    total_orbits = 0
    for order in ORDERS:
        records = [
            line
            for line in (HERE / f"order{order}-connected-cubic.g6")
            .read_text(encoding="ascii")
            .splitlines()
            if line
        ]
        graphs = []
        raw_order = 0
        orbits_order = 0
        for graph_index, graph6 in enumerate(records):
            vertices, edges = decode_graph6(graph6)
            _, masks = incidence(vertices, edges)
            if (
                not connected(vertices, masks)
                or not three_edge_connected(vertices, masks)
            ):
                continue
            actions = automorphisms(vertices, edges)
            representatives, raw = junction_orbits(
                vertices, edges, actions
            )
            graphs.append({
                "graph_index": graph_index,
                "graph6": graph6,
                "girth": graph_girth(vertices, masks),
                "automorphisms": len(actions),
                "raw_independent_positive_even_junction_sets": raw,
                "canonical_junction_orbits": len(representatives),
                "junction_representatives": [
                    list(row) for row in representatives.values()
                ],
            })
            raw_order += raw
            orbits_order += len(representatives)
        by_order[str(order)] = {
            "connected_cubic_graphs": len(records),
            "three_edge_connected_graphs": len(graphs),
            "raw_independent_positive_even_junction_sets": raw_order,
            "canonical_junction_orbits": orbits_order,
            "graphs": graphs,
        }
        total_graphs += len(graphs)
        total_orbits += orbits_order
    report = {
        "schema": "three-edge-connected-cubic-hybrid-macro-through14-v1",
        "scope": (
            "simple connected cubic graphs with no edge cut smaller than 3"
        ),
        "orders": by_order,
        "totals": {
            "three_edge_connected_graphs": total_graphs,
            "canonical_junction_orbits": total_orbits,
        },
    }
    (HERE / "three-edge-census-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(json.dumps(report["totals"], sort_keys=True))
    for order in ORDERS:
        row = by_order[str(order)]
        print(
            f"n={order} graphs={row['three_edge_connected_graphs']} "
            f"junction_orbits={row['canonical_junction_orbits']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
