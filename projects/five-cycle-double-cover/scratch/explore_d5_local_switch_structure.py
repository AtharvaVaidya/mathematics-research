#!/usr/bin/env python3
"""Print structural data for the three local D5 switches at one edge pair.

This is an exploratory human-proof aid, not a verifier.  It exposes the
factor circuit, its graph vertices, and the pair-labelled third edges at
which the corresponding triangle recolouring changes a corner pairing.
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

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
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402


def edge_vertices(graph, edge_mask: int) -> set[int]:
    answer: set[int] = set()
    for edge, (left, right) in enumerate(graph.edges):
        if (edge_mask >> edge) & 1:
            answer.add(left)
            answer.add(right)
    return answer


def switched_state(state, pair, component):
    return tuple(
        transpose_label(label, *pair)
        if (component >> edge) & 1
        else label
        for edge, label in enumerate(state)
    )


def corner_circuit_count(graph, state, twisted_edges: set[int]) -> int:
    """Count vertex-link circuits after crossing selected side pairings."""
    palettes = [0] * graph.vertices
    for edge, (left, right) in enumerate(graph.edges):
        palettes[left] |= state[edge]
        palettes[right] |= state[edge]
    nodes = [
        (vertex, coordinate)
        for vertex, palette in enumerate(palettes)
        for coordinate in range(5)
        if (palette >> coordinate) & 1
    ]
    adjacency = {node: [] for node in nodes}
    for edge, (left, right) in enumerate(graph.edges):
        coordinates = [
            coordinate
            for coordinate in range(5)
            if (state[edge] >> coordinate) & 1
        ]
        assert len(coordinates) == 2
        if edge in twisted_edges:
            coordinates_at_right = list(reversed(coordinates))
        else:
            coordinates_at_right = coordinates
        for first, second in zip(coordinates, coordinates_at_right):
            adjacency[(left, first)].append((right, second))
            adjacency[(right, second)].append((left, first))
    assert all(len(row) == 2 for row in adjacency.values())
    unseen = set(nodes)
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            node = stack.pop()
            for other in adjacency[node]:
                if other in unseen:
                    unseen.remove(other)
                    stack.append(other)
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph6")
    parser.add_argument("labels", help="comma- or space-separated hex labels")
    parser.add_argument("first_edge", type=int)
    parser.add_argument("second_edge", type=int)
    args = parser.parse_args()

    graph = graph_from_graph6(args.graph6)
    state = tuple(
        int(token, 16)
        for token in args.labels.replace(",", " ").split()
    )
    if len(state) != graph.edge_count:
        raise SystemExit(
            f"expected {graph.edge_count} labels, received {len(state)}"
        )
    common_vertices = (
        set(graph.edges[args.first_edge])
        & set(graph.edges[args.second_edge])
    )
    if len(common_vertices) != 1:
        raise SystemExit("the two edges must have exactly one common vertex")
    vertex = next(iter(common_vertices))
    print(f"vertex={vertex} chi={euler_characteristic(graph, state)}")
    print(
        "incident=",
        [
            (edge, graph.edges[edge], f"{state[edge]:02x}")
            for edge in range(graph.edge_count)
            if vertex in graph.edges[edge]
        ],
    )

    old_chi = euler_characteristic(graph, state)
    boundary_sets = []
    for pair in PAIRS:
        active = active_mask(state, *pair)
        for component in component_edge_masks(graph, active):
            if not (
                ((component >> args.first_edge) & 1)
                and ((component >> args.second_edge) & 1)
            ):
                continue
            vertices = edge_vertices(graph, component)
            boundary_pair_edges = []
            for edge, (left, right) in enumerate(graph.edges):
                if state[edge] != (1 << pair[0]) | (1 << pair[1]):
                    continue
                if (left in vertices) != (right in vertices):
                    boundary_pair_edges.append(edge)
            other = switched_state(state, pair, component)
            print(
                {
                    "pair": pair,
                    "delta": euler_characteristic(graph, other) - old_chi,
                    "component_edges": [
                        edge
                        for edge in range(graph.edge_count)
                        if (component >> edge) & 1
                    ],
                    "component_vertices": sorted(vertices),
                    "boundary_pair_edges": boundary_pair_edges,
                }
            )
            boundary_sets.append((pair, set(boundary_pair_edges)))

    assert len(boundary_sets) == 3
    print("corner circuit counts for xor-combinations of boundary twists:")
    for bits in itertools.product((0, 1), repeat=3):
        twisted = set()
        for bit, (_, boundary) in zip(bits, boundary_sets):
            if bit:
                twisted.symmetric_difference_update(boundary)
        print(
            "".join(map(str, bits)),
            corner_circuit_count(graph, state, twisted),
        )


if __name__ == "__main__":
    main()
