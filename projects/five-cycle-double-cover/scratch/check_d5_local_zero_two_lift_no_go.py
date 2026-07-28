#!/usr/bin/env python3
"""Literal 28-vertex no-go for universal exact local zero-neutrality.

The three local switches have deltas -2,-2,+2.  Hence none is neutral,
although their maximum is positive.  This refutes exact zero-existence
without refuting the weaker terminal-sufficient max-delta inequality.
"""

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
from check_d5_local_boundary_degree_two_lift_no_go import (  # noqa: E402
    construct_lift,
    validate_flow,
)
from stress_d5_local_boundary_degree import boundary_size  # noqa: E402


VOLTAGE_ONE_EDGES = {10, 14}
EXPECTED_GRAPH6 = (
    "[???????????_?O?D??g?__H@?PB??c_?aA?COO?@S??Ag?AE??@H??P@??AGG??"
)
LOCAL_EDGE_PAIR = (7, 8)


def main() -> int:
    graph6, graph, state, _ = construct_lift(VOLTAGE_ONE_EDGES)
    assert graph6 == EXPECTED_GRAPH6
    validate_flow(graph, state)

    host = nx.Graph()
    host.add_nodes_from(range(graph.vertices))
    host.add_edges_from(graph.edges)
    assert nx.is_connected(host)
    assert nx.number_of_nodes(host) == 28
    assert nx.number_of_edges(host) == 42
    assert all(degree == 3 for _, degree in host.degree())
    assert not list(nx.bridges(host))

    first_edge, second_edge = LOCAL_EDGE_PAIR
    common_vertex = (
        set(graph.edges[first_edge]) & set(graph.edges[second_edge])
    )
    assert common_vertex == {2}
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
            other = tuple(
                transpose_label(label, *pair)
                if (component >> edge) & 1
                else label
                for edge, label in enumerate(state)
            )
            validate_flow(graph, other)
            candidates.append((
                pair,
                boundary_size(graph, state, pair, component),
                euler_characteristic(graph, other) - old_chi,
            ))
    assert candidates == [
        ((0, 4), 4, -2),
        ((1, 4), 4, -2),
        ((2, 3), 4, 2),
    ]
    assert all(delta != 0 for _, _, delta in candidates)
    assert max(delta for _, _, delta in candidates) == 2

    print("PASS")
    print(f"graph6: {graph6}")
    print(
        "state labels hex: "
        + " ".join(f"{label:02x}" for label in state)
    )
    print("local vertex and edge pair: 2, [7, 8]")
    print(
        "candidate (pair, boundary size, delta): "
        "[(04,4,-2),(14,4,-2),(23,4,+2)]"
    )
    print("exact-zero candidates: 0; maximum delta: +2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
