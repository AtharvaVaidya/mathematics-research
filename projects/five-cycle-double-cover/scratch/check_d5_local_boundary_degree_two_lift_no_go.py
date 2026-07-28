#!/usr/bin/env python3
"""Construct and check a 2-lift no-go for the local boundary-size lemma."""

from __future__ import annotations

import sys
from pathlib import Path

import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRATCH = PROJECT_ROOT / "scratch"
for item in (str(PROJECT_ROOT), str(SCRATCH)):
    if item not in sys.path:
        sys.path.insert(0, item)

from audit_d5_root_euler_potential import euler_characteristic  # noqa: E402
from audit_d5_root_kempe_orbits import (  # noqa: E402
    PAIRS,
    active_mask,
    component_edge_masks,
    transpose_label,
)
from stress_d5_local_boundary_degree import (  # noqa: E402
    boundary_size,
    component_vertices,
)
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402


BASE_GRAPH6 = "M??CBAPUAc@oJ?h??"
BASE_STATE = tuple(
    int(label, 16)
    for label in (
        "03 09 0a 0c 14 18 14 12 06 11 18 "
        "09 0c 18 14 0a 06 0c 11 12 18"
    ).split()
)
# Edges 0 and 3 meet the two distinct selected factor circuits oddly.
VOLTAGE_ONE_EDGES = {0, 3}
BASE_VERTEX = 2
BASE_EDGE_PAIR = (6, 7)


def construct_lift(voltage_one_edges=VOLTAGE_ONE_EDGES):
    base = graph_from_graph6(BASE_GRAPH6)
    lifted = nx.Graph()
    lifted.add_nodes_from(range(2 * base.vertices))
    label_by_edge = {}
    base_copy_to_edge = {}
    for edge, (left, right) in enumerate(base.edges):
        voltage = int(edge in voltage_one_edges)
        for sheet in (0, 1):
            lifted_edge = tuple(sorted((
                2 * left + sheet,
                2 * right + (sheet ^ voltage),
            )))
            lifted.add_edge(*lifted_edge)
            label_by_edge[lifted_edge] = BASE_STATE[edge]
            base_copy_to_edge[(edge, sheet)] = lifted_edge
    assert nx.is_connected(lifted)
    assert nx.number_of_edges(lifted) == 3 * nx.number_of_nodes(lifted) // 2
    assert all(degree == 3 for _, degree in lifted.degree())
    assert not list(nx.bridges(lifted))
    graph6 = nx.to_graph6_bytes(lifted, header=False).decode("ascii").strip()
    graph = graph_from_graph6(graph6)
    state = tuple(
        label_by_edge[tuple(sorted(edge))] for edge in graph.edges
    )
    edge_index = {
        tuple(sorted(edge)): index for index, edge in enumerate(graph.edges)
    }
    local_edges = tuple(
        edge_index[base_copy_to_edge[(edge, 0)]]
        for edge in BASE_EDGE_PAIR
    )
    return graph6, graph, state, local_edges


def validate_flow(graph, state) -> None:
    incidence = [[] for _ in range(graph.vertices)]
    for edge, (left, right) in enumerate(graph.edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    assert all(len(row) == 3 for row in incidence)
    assert all(label.bit_count() == 2 for label in state)
    assert all(
        state[row[0]] ^ state[row[1]] ^ state[row[2]] == 0
        for row in incidence
    )


def main() -> int:
    graph6, graph, state, local_edges = construct_lift()
    validate_flow(graph, state)
    first_edge, second_edge = local_edges
    assert set(graph.edges[first_edge]) & set(graph.edges[second_edge]) == {
        2 * BASE_VERTEX
    }
    old_chi = euler_characteristic(graph, state)
    candidates = []
    for pair in PAIRS:
        for component in component_edge_masks(
            graph, active_mask(state, *pair)
        ):
            if not (
                ((component >> first_edge) & 1)
                and ((component >> second_edge) & 1)
            ):
                continue
            switched = tuple(
                transpose_label(label, *pair)
                if (component >> edge) & 1
                else label
                for edge, label in enumerate(state)
            )
            candidates.append({
                "pair": pair,
                "component": component,
                "vertices": component_vertices(graph, component),
                "boundary_size": boundary_size(
                    graph, state, pair, component
                ),
                "delta": euler_characteristic(graph, switched) - old_chi,
            })
    assert len(candidates) == 3
    assert sorted(item["boundary_size"] for item in candidates) == [4, 4, 8]
    assert [
        (item["pair"], item["boundary_size"], item["delta"])
        for item in candidates
    ] == [
        ((0, 4), 4, 0),
        ((1, 2), 4, 2),
        ((3, 4), 8, 2),
    ]

    print("PASS")
    print(f"graph6: {graph6}")
    print(
        "state labels hex: "
        + " ".join(f"{label:02x}" for label in state)
    )
    print(f"local edge pair: {list(local_edges)}")
    print(
        "candidate boundary sizes and deltas: "
        + repr([
            (item["pair"], item["boundary_size"], item["delta"])
            for item in candidates
        ])
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
