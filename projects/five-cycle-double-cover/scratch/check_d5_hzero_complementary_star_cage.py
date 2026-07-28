#!/usr/bin/env python3
"""Literal order-12 cage at the H=0 triangle-monodromy endpoint."""

from __future__ import annotations

import itertools
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


GRAPH6 = "K?ABApoMCWOo"
NAMES = (
    "01", "02", "12", "23", "34", "24",
    "34", "23", "24", "24", "34", "23",
    "23", "34", "24", "04", "14", "24",
)
ROOTS = (0, 10)
LINE = ((1, 2), (0, 1), (0, 2))
LINE_CIRCUITS = (
    (0, 1, 3, 5, 7, 8, 9, 11, 12, 14, 16, 17),
    (0, 2, 3, 5, 7, 8, 9, 11, 12, 14, 15, 17),
    (0, 1, 3, 5, 7, 8, 9, 11, 12, 14, 16, 17),
)
STARS = (
    ((0, 3), (0, 1), (1, 3)),
    ((1, 3), (0, 1), (0, 3)),
    ((0, 4), (0, 1), (1, 4)),
    ((1, 4), (0, 1), (0, 4)),
)


def mask(name: str) -> int:
    return sum(1 << int(coordinate) for coordinate in name)


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


def root_good(graph, state):
    first, second = ROOTS
    for pair in PAIRS:
        for component in components(graph, state, pair):
            if ((component >> first) & 1) and ((component >> second) & 1):
                return pair, component
    return None


def lift(graph, state, moving_root, other_root, sequence):
    circuits = []
    for pair in sequence:
        component = next(
            component
            for component in components(graph, state, pair)
            if (component >> moving_root) & 1
        )
        assert not ((component >> other_root) & 1)
        state = switch(state, pair, component)
        circuits.append(component)
        assert root_good(graph, state) is None
    return state, tuple(circuits)


def edge_mask(edge_tuple):
    return sum(1 << edge for edge in edge_tuple)


def listed(value: int, edge_count: int) -> tuple[int, ...]:
    return tuple(edge for edge in range(edge_count) if (value >> edge) & 1)


def main() -> None:
    graph = graph_from_graph6(GRAPH6)
    assert graph.edges == (
        (0, 5), (0, 10), (0, 11),
        (1, 6), (1, 7), (1, 8),
        (2, 6), (2, 8), (2, 9),
        (3, 7), (3, 8), (3, 9),
        (4, 7), (4, 9), (4, 10),
        (5, 10), (5, 11), (6, 11),
    )
    initial = tuple(mask(name) for name in NAMES)
    incidence = [[] for _ in range(graph.vertices)]
    for edge, (left, right) in enumerate(graph.edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    for row in incidence:
        assert initial[row[0]] ^ initial[row[1]] ^ initial[row[2]] == 0
    assert initial[ROOTS[0]] == mask("01")
    assert initial[ROOTS[1]] == mask("34")
    assert root_good(graph, initial) is None

    line_state = initial
    actual_line_circuits = []
    for pair, listed_circuit in zip(LINE, LINE_CIRCUITS):
        circuit = edge_mask(listed_circuit)
        assert circuit in components(graph, line_state, pair)
        line_state = switch(line_state, pair, circuit)
        actual_line_circuits.append(circuit)
        assert root_good(graph, line_state) is None
    first, middle, third = actual_line_circuits
    assert first == third
    assert listed(first ^ middle, graph.edge_count) == (1, 2, 15, 16)
    assert first ^ third == 0

    for star in STARS:
        star_state, star_circuits = lift(
            graph, initial, ROOTS[1], ROOTS[0], star
        )
        assert star_state == initial
        assert star_circuits[0] == star_circuits[1] == star_circuits[2]

        after_line_star, after_line_circuits = lift(
            graph, line_state, ROOTS[1], ROOTS[0], star
        )
        assert after_line_star == line_state
        assert (
            after_line_circuits[0]
            == after_line_circuits[1]
            == after_line_circuits[2]
        )

        star_first, _ = lift(
            graph, initial, ROOTS[1], ROOTS[0], star
        )
        transported_line, transported_circuits = lift(
            graph, star_first, ROOTS[0], ROOTS[1], LINE
        )
        assert transported_line == line_state
        assert transported_circuits[0] == transported_circuits[2]
        assert listed(
            transported_circuits[0] ^ transported_circuits[1],
            graph.edge_count,
        ) == (1, 2, 15, 16)

    # The cage is not a full-orbit obstruction.  A cross-root pivot followed
    # by a root-inactive handle rescues in two switches.
    first_escape = edge_mask((0, 1, 6, 8, 13, 14, 16, 17))
    assert first_escape in components(graph, initial, (0, 4))
    middle_state = switch(initial, (0, 4), first_escape)
    assert root_good(graph, middle_state) is None
    second_escape = edge_mask((3, 5, 6, 7))
    assert second_escape in components(graph, middle_state, (0, 2))
    final = switch(middle_state, (0, 2), second_escape)
    certificate = root_good(graph, final)
    assert certificate is not None
    assert certificate[0] == (0, 4)
    assert listed(certificate[1], graph.edge_count) == (
        0, 1, 3, 4, 7, 8, 9, 10, 13, 14, 16, 17
    )

    print(
        "PASS: order-12 H=0 cage has Z={1,2,15,16}; all four "
        "complementary stars are literal identity loops in either order; "
        "cross pivot 04 then inactive handle 02 rescues"
    )


if __name__ == "__main__":
    main()
