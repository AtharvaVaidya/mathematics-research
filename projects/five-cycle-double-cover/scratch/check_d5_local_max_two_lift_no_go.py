#!/usr/bin/env python3
"""Literal local-maximum 2-lift no-go for the max-delta inequality.

At one adjacent edge pair all three candidate switches have delta -2.
The state is a local chi maximum: every component switch has delta 0 or -2.
The neutral-component hypergraph nevertheless remains connected.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRATCH = PROJECT_ROOT / "scratch"
for item in (str(PROJECT_ROOT), str(SCRATCH)):
    if item not in sys.path:
        sys.path.insert(0, item)

from audit_d5_root_component_chain_potential import (  # noqa: E402
    all_root_distances,
)
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


VOLTAGE_ONE_EDGES = {10, 14, 17}
EXPECTED_GRAPH6 = (
    "[???????????_?O?D??g?__H@?PB??c_?aA?COO?@S??Ag?AE??@H??P?_?AGO??"
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

    old_chi = euler_characteristic(graph, state)
    moves = []
    local_candidates = []
    for pair in PAIRS:
        for component in component_edge_masks(
            graph, active_mask(state, *pair)
        ):
            if not component:
                continue
            other = tuple(
                transpose_label(label, *pair)
                if (component >> edge) & 1
                else label
                for edge, label in enumerate(state)
            )
            validate_flow(graph, other)
            delta = euler_characteristic(graph, other) - old_chi
            moves.append((pair, component, delta))
            if all(
                (component >> edge) & 1 for edge in LOCAL_EDGE_PAIR
            ):
                local_candidates.append((
                    pair,
                    boundary_size(graph, state, pair, component),
                    delta,
                ))

    assert old_chi == -4
    assert len(moves) == 24
    assert Counter(delta for _, _, delta in moves) == {0: 12, -2: 12}
    assert max(delta for _, _, delta in moves) == 0
    assert local_candidates == [
        ((0, 4), 4, -2),
        ((1, 4), 4, -2),
        ((2, 3), 4, -2),
    ]

    neutral = [
        component for _, component, delta in moves if delta == 0
    ]
    distances = all_root_distances(graph.edge_count, neutral)
    finite_distances = [
        distances[first][second]
        for first in range(graph.edge_count)
        for second in range(first + 1, graph.edge_count)
    ]
    assert max(finite_distances) == 3
    assert distances[LOCAL_EDGE_PAIR[0]][LOCAL_EDGE_PAIR[1]] == 2

    print("PASS")
    print(f"graph6: {graph6}")
    print(
        "state labels hex: "
        + " ".join(f"{label:02x}" for label in state)
    )
    print("surface chi: -4")
    print("all nonempty-switch delta histogram: {-2: 12, 0: 12}")
    print(
        "local candidate (pair, boundary size, delta): "
        "[(04,4,-2),(14,4,-2),(23,4,-2)]"
    )
    print(
        "neutral hypergraph: connected; local edge distance 2; "
        "maximum distance 3"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
