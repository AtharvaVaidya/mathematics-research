#!/usr/bin/env python3
"""Test monotonicity of the current-factor component-chain distance.

For a D5 state q, form a hypergraph on E(G) whose hyperedges are all
connected components of all ten bichromatic factors Y_ij(q).  The
root-chain distance d_q(r,s) is the least number of hyperedges in a chain
from r to s.  It is one exactly for a rooted-good state.

This audit asks whether every bad state can reach a smaller distance
without first increasing it (equal-distance Kempe moves are allowed).
Failure refutes only this proposed proof potential.
"""

from __future__ import annotations

import json
import sys
from collections import deque

from audit_d5_root_kempe_orbits import (
    PAIRS,
    active_mask,
    component_edge_masks,
    enumerate_flows,
    neighbours,
)
from tools.fixed_fano_merge_frontier import graph_from_graph6


def component_masks(graph, state: tuple[int, ...]) -> list[int]:
    return [
        component
        for i, j in PAIRS
        for component in component_edge_masks(graph, active_mask(state, i, j))
    ]


def all_root_distances(edge_count: int, components: list[int]) -> list[list[int]]:
    through: list[list[int]] = [[] for _ in range(edge_count)]
    for component in components:
        for edge in range(edge_count):
            if (component >> edge) & 1:
                through[edge].append(component)

    answer: list[list[int]] = []
    for root in range(edge_count):
        distance = [-1] * edge_count
        distance[root] = 0
        queue = deque([root])
        while queue:
            edge = queue.popleft()
            for component in through[edge]:
                mask = component
                while mask:
                    bit = mask & -mask
                    other = bit.bit_length() - 1
                    mask ^= bit
                    if distance[other] < 0:
                        distance[other] = distance[edge] + 1
                        queue.append(other)
        if any(value < 0 for value in distance):
            raise AssertionError("factor-component hypergraph is disconnected")
        answer.append(distance)
    return answer


def audit(record: str) -> dict[str, object]:
    graph = graph_from_graph6(record)
    states = sorted(enumerate_flows(graph))
    index = {state: i for i, state in enumerate(states)}
    adjacency = [
        {index[nxt] for nxt in neighbours(graph, state)} - {i}
        for i, state in enumerate(states)
    ]
    distances = [
        all_root_distances(graph.edge_count, component_masks(graph, state))
        for state in states
    ]

    first_failure = None
    plateau_count = 0
    seen: set[tuple[int, int, int, int]] = set()
    for root in range(graph.edge_count):
        for target in range(graph.edge_count):
            if root == target:
                continue
            for start in range(len(states)):
                level = distances[start][root][target]
                if level == 1 or (root, target, level, start) in seen:
                    continue
                plateau_count += 1
                plateau = {start}
                queue = deque([start])
                escaped = False
                while queue:
                    current = queue.popleft()
                    for nxt in adjacency[current]:
                        value = distances[nxt][root][target]
                        if value < level:
                            escaped = True
                        elif value == level and nxt not in plateau:
                            plateau.add(nxt)
                            queue.append(nxt)
                seen.update((root, target, level, state) for state in plateau)
                if not escaped and first_failure is None:
                    first_failure = {
                        "root_edge_indices": [root, target],
                        "distance": level,
                        "plateau_state_indices": sorted(plateau),
                        "plateau_size": len(plateau),
                        "neighbour_distances": sorted(
                            {
                                distances[nxt][root][target]
                                for state in plateau
                                for nxt in adjacency[state]
                                if nxt not in plateau
                            }
                        ),
                    }
    return {
        "graph6": record,
        "vertices": graph.vertices,
        "edges": graph.edge_count,
        "states_mod_s5": len(states),
        "plateaus_checked": plateau_count,
        "nonincreasing_chain_distance": first_failure is None,
        "first_failure": first_failure,
    }


if __name__ == "__main__":
    records = sys.argv[1:]
    if not records:
        records = [line.strip() for line in sys.stdin if line.strip()]
    if not records:
        raise SystemExit(f"usage: {sys.argv[0]} [GRAPH6 ...]")
    results = [audit(record) for record in records]
    print(json.dumps(results[0] if len(results) == 1 else results, indent=2))
