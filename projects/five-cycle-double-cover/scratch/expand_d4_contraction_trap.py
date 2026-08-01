#!/usr/bin/env python3
"""Try all cubic splittings of the exact four-coordinate contraction trap.

This is a focused bridge between the degree-four obstruction in
``d5-contraction-generalized-circuit-no-go.md`` and the cubic rooted
Kempe-orbit theorem.  It splits the exceptional degree-four vertex in
each of its three 2+2 ways, retains the displayed trapped flow whenever
the new edge receives an admissible weight-two xor, and then explores
the complete component-Kempe orbit.
"""

from __future__ import annotations

import json
from itertools import combinations

from check_d5_contraction_circuit_orbit_counterexample import (
    CONTRACTED_EDGE,
    GRAPH6,
    WITNESS_TEXT,
    contract,
    decode_graph6,
    parse_label,
)
from search_d4_trapped_root_orbit import (
    LABEL_SET,
    canonical4,
    connected_graph,
    orbit_audit,
    validate_flow,
)


def pairings(items: tuple[int, int, int, int]):
    first = items[0]
    for second in items[1:]:
        left = tuple(sorted((first, second)))
        right = tuple(item for item in items if item not in left)
        yield left, right


def split_graph(
    edges: tuple[tuple[int, int], ...],
    labels: tuple[int, ...],
    left_side: tuple[int, int],
    right_side: tuple[int, int],
):
    new_vertex = max(max(edge) for edge in edges) + 1
    right_set = set(right_side)
    expanded = []
    for edge_index, (u, v) in enumerate(edges):
        if edge_index in right_set:
            if u == 0:
                u = new_vertex
            if v == 0:
                v = new_vertex
        expanded.append(tuple(sorted((u, v))))
    new_label = labels[left_side[0]] ^ labels[left_side[1]]
    assert new_label == labels[right_side[0]] ^ labels[right_side[1]]
    expanded.append((0, new_vertex))
    augmented_labels = labels + (new_label,)
    ordered = sorted(zip(expanded, augmented_labels))
    return (
        tuple(edge for edge, _label in ordered),
        tuple(label for _edge, label in ordered),
        new_label,
    )


def main() -> None:
    vertices, parent_edges = decode_graph6(GRAPH6)
    (
        contracted_vertices,
        contracted_edges,
        _old_indices,
        u_side,
        v_side,
    ) = contract(vertices, parent_edges, CONTRACTED_EDGE)
    assert contracted_vertices == 13
    incident = tuple(sorted(u_side + v_side))
    labels = tuple(parse_label(text) for text in WITNESS_TEXT)

    rows = []
    for left_side, right_side in pairings(incident):
        expanded_edges, expanded_labels, new_label = split_graph(
            contracted_edges,
            labels,
            left_side,
            right_side,
        )
        row = {
            "split": [list(left_side), list(right_side)],
            "new_label_mask": new_label,
            "admissible_weight_two": new_label in LABEL_SET,
        }
        if new_label in LABEL_SET:
            assert connected_graph(14, expanded_edges)
            normalized = canonical4(expanded_labels)
            validate_flow(14, expanded_edges, normalized)
            audit = orbit_audit(14, expanded_edges, normalized)
            row.update({
                "edges": expanded_edges,
                "labels": normalized,
                "orbit_states_mod_s5": len(audit["states"]),
                "fully_d4_trapped": audit["trapped"],
                "failed_roots": audit["failed_roots"],
            })
        rows.append(row)

    print(json.dumps({
        "classification": (
            "CUBIC_ROOT_ORBIT_COUNTEREXAMPLE"
            if any(row.get("failed_roots") for row in rows)
            else "NO_CUBIC_ROOT_FAILURE_FROM_THE_THREE_SPLITS"
        ),
        "parent_graph6": GRAPH6,
        "contracted_edge": CONTRACTED_EDGE,
        "degree_four_incident_edges": incident,
        "splits": rows,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
