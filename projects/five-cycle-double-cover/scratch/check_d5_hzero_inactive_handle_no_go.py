#!/usr/bin/env python3
"""Check the order-12 H=0 no-go for a newly inactive second handle."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for item in (str(PROJECT_ROOT), str(PROJECT_ROOT / "scratch")):
    if item not in sys.path:
        sys.path.insert(0, item)

from audit_d5_root_kempe_orbits import (  # noqa: E402
    PAIRS,
    active_mask,
    component_edge_masks,
)
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402


GRAPH6 = "K?`@EQgLAcAo"
STATE = (3, 5, 6, 9, 12, 5, 5, 12, 9, 17, 9, 24, 9, 10, 24, 17, 12, 9)
ROOTS = (2, 11)
LINE = ((0, 1), (1, 2), (0, 2))


def components(graph, state, pair):
    return tuple(
        component
        for component in component_edge_masks(
            graph, active_mask(state, *pair)
        )
        if component
    )


def switch(state, pair, component):
    toggle = (1 << pair[0]) | (1 << pair[1])
    return tuple(
        label ^ toggle if (component >> edge) & 1 else label
        for edge, label in enumerate(state)
    )


def listed(component, edge_count):
    return tuple(
        edge for edge in range(edge_count) if (component >> edge) & 1
    )


def root_good(graph, state):
    for pair in PAIRS:
        for component in components(graph, state, pair):
            if all((component >> root) & 1 for root in ROOTS):
                return pair, component
    return None


def root_moves(graph, state):
    for root in ROOTS:
        label = state[root]
        for pair in PAIRS:
            pair_mask = (1 << pair[0]) | (1 << pair[1])
            if (label & pair_mask).bit_count() != 1:
                continue
            component = next(
                component
                for component in components(graph, state, pair)
                if (component >> root) & 1
            )
            yield root, pair, component, switch(state, pair, component)


def main() -> None:
    graph = graph_from_graph6(GRAPH6)
    assert graph.edges == (
        (0, 4), (0, 7), (0, 8), (1, 5), (1, 7), (1, 10),
        (2, 6), (2, 8), (2, 9), (3, 9), (3, 10), (3, 11),
        (4, 7), (4, 8), (5, 9), (5, 11), (6, 10), (6, 11),
    )

    incidence = [[] for _ in range(graph.vertices)]
    for edge, (left, right) in enumerate(graph.edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    assert all(
        STATE[row[0]] ^ STATE[row[1]] ^ STATE[row[2]] == 0
        for row in incidence
    )
    assert STATE[ROOTS[0]] == 0b00110
    assert STATE[ROOTS[1]] == 0b11000
    assert root_good(graph, STATE) is None

    line_state = STATE
    line_circuits = []
    for pair in LINE:
        component = next(
            component
            for component in components(graph, line_state, pair)
            if (component >> ROOTS[0]) & 1
        )
        assert not ((component >> ROOTS[1]) & 1)
        line_circuits.append(component)
        line_state = switch(line_state, pair, component)
        assert root_good(graph, line_state) is None

    assert listed(line_circuits[0], graph.edge_count) == (1, 2, 12, 13)
    assert listed(line_circuits[1], graph.edge_count) == (
        0, 2, 4, 5, 6, 7, 12, 16
    )
    assert line_circuits[0] == line_circuits[2]
    assert listed(
        line_circuits[0] ^ line_circuits[1], graph.edge_count
    ) == (0, 1, 4, 5, 6, 7, 13, 16)

    # Exhaust the proposed hierarchy at both line endpoints.
    for endpoint in (STATE, line_state):
        moves = tuple(root_moves(graph, endpoint))
        assert len(moves) == 12
        for _, _, _, after_first in moves:
            assert root_good(graph, after_first) is None
            for pair in PAIRS:
                pair_mask = (1 << pair[0]) | (1 << pair[1])
                if any(
                    (after_first[root] & pair_mask).bit_count() == 1
                    for root in ROOTS
                ):
                    continue
                for component in components(graph, after_first, pair):
                    assert (
                        root_good(
                            graph, switch(after_first, pair, component)
                        )
                        is None
                    )

    # A genuine two-root-transition rescue still exists.
    first_component = next(
        component
        for component in components(graph, STATE, (0, 1))
        if (component >> ROOTS[0]) & 1
    )
    assert listed(first_component, graph.edge_count) == (1, 2, 12, 13)
    after_first = switch(STATE, (0, 1), first_component)
    assert root_good(graph, after_first) is None
    second_component = next(
        component
        for component in components(graph, after_first, (1, 3))
        if (component >> ROOTS[1]) & 1
    )
    assert listed(second_component, graph.edge_count) == (10, 11, 16, 17)
    final = switch(after_first, (1, 3), second_component)
    certificate = root_good(graph, final)
    assert certificate is not None
    assert certificate[0] == (1, 2)
    assert listed(certificate[1], graph.edge_count) == (
        0, 2, 4, 5, 6, 7, 10, 11, 12, 17
    )

    print(
        "PASS: H=0 line loop; no immediate root rescue and no "
        "root-transition-plus-inactive-handle rescue from either endpoint; "
        "two root transitions 01@r then 13@s rescue"
    )


if __name__ == "__main__":
    main()
