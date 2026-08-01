#!/usr/bin/env python3
"""Exhaust gauge-normalized connected 2-lifts of one hard local state."""

from __future__ import annotations

import sys
from collections import Counter
from itertools import combinations
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
    BASE_GRAPH6,
    construct_lift,
    validate_flow,
)
from stress_d5_local_boundary_degree import boundary_size  # noqa: E402
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402


def cotree_edges() -> tuple[int, ...]:
    base = graph_from_graph6(BASE_GRAPH6)
    graph = nx.Graph()
    graph.add_nodes_from(range(base.vertices))
    graph.add_edges_from(base.edges)
    tree = nx.minimum_spanning_tree(graph)
    tree_edges = {tuple(sorted(edge)) for edge in tree.edges}
    answer = tuple(
        edge
        for edge, endpoints in enumerate(base.edges)
        if tuple(sorted(endpoints)) not in tree_edges
    )
    assert len(answer) == len(base.edges) - base.vertices + 1 == 8
    return answer


def audit_state(graph, state):
    incidence = [[] for _ in range(graph.vertices)]
    for edge, (left, right) in enumerate(graph.edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    old_chi = euler_characteristic(graph, state)
    through = {}
    for pair in PAIRS:
        for component in component_edge_masks(
            graph, active_mask(state, *pair)
        ):
            other = tuple(
                transpose_label(label, *pair)
                if (component >> edge) & 1
                else label
                for edge, label in enumerate(state)
            )
            delta = euler_characteristic(graph, other) - old_chi
            size = boundary_size(graph, state, pair, component)
            for edge in range(graph.edge_count):
                if (component >> edge) & 1:
                    through[(edge, pair)] = (component, size, delta)
    patterns = Counter()
    first_zero_free = None
    first_max_negative = None
    for vertex, row in enumerate(incidence):
        for first, second in combinations(row, 2):
            candidates = []
            for pair in PAIRS:
                item = through.get((first, pair))
                if item and ((item[0] >> second) & 1):
                    candidates.append((pair, item[1], item[2]))
            assert len(candidates) == 3
            pattern = tuple(sorted(delta for _, _, delta in candidates))
            patterns[pattern] += 1
            if 0 not in pattern and first_zero_free is None:
                first_zero_free = {
                    "vertex": vertex,
                    "edge_pair": [first, second],
                    "candidates": candidates,
                }
            if max(pattern) < 0 and first_max_negative is None:
                first_max_negative = {
                    "vertex": vertex,
                    "edge_pair": [first, second],
                    "candidates": candidates,
                }
    return patterns, first_zero_free, first_max_negative


def main() -> int:
    cotree = cotree_edges()
    pattern_totals = Counter()
    lifts = 0
    triples = 0
    maximum_minimum_boundary = 0
    first_large_boundary = None
    zero_free_triples = 0
    for word in range(1, 1 << len(cotree)):
        voltages = {
            cotree[index]
            for index in range(len(cotree))
            if (word >> index) & 1
        }
        graph6, graph, state, _ = construct_lift(voltages)
        validate_flow(graph, state)
        patterns, zero_free, max_negative = audit_state(graph, state)
        lifts += 1
        triples += sum(patterns.values())
        pattern_totals.update(patterns)
        zero_free_triples += sum(
            count for pattern, count in patterns.items() if 0 not in pattern
        )
        if max_negative is not None:
            print({
                "status": "FAIL",
                "cotree_edges": cotree,
                "voltage_word": word,
                "voltage_one_edges": sorted(voltages),
                "graph6": graph6,
                "state_labels_hex": [
                    f"{label:02x}" for label in state
                ],
                **max_negative,
            })
            return 1

        # Track how far the already-refuted boundary-size bound can fail.
        incidence = [[] for _ in range(graph.vertices)]
        for edge, (left, right) in enumerate(graph.edges):
            incidence[left].append(edge)
            incidence[right].append(edge)
        through = {}
        for pair in PAIRS:
            for component in component_edge_masks(
                graph, active_mask(state, *pair)
            ):
                size = boundary_size(graph, state, pair, component)
                for edge in range(graph.edge_count):
                    if (component >> edge) & 1:
                        through[(edge, pair)] = (component, size)
        for vertex, row in enumerate(incidence):
            for first, second in combinations(row, 2):
                candidates = [
                    (pair, item[1])
                    for pair in PAIRS
                    if (item := through.get((first, pair)))
                    and ((item[0] >> second) & 1)
                ]
                minimum = min(size for _, size in candidates)
                if minimum > maximum_minimum_boundary:
                    maximum_minimum_boundary = minimum
                    first_large_boundary = {
                        "voltage_word": word,
                        "vertex": vertex,
                        "edge_pair": [first, second],
                        "boundary_sizes": sorted(
                            size for _, size in candidates
                        ),
                    }

    print("PASS")
    print(f"cotree edges: {cotree}")
    print(f"connected gauge-normalized 2-lifts: {lifts}")
    print(f"local triples: {triples}")
    print(f"zero-free local triples: {zero_free_triples}")
    print("max-delta-negative failures: 0")
    print(f"delta patterns: {dict(sorted(pattern_totals.items()))}")
    print(
        "maximum of the three-boundary minimum: "
        f"{maximum_minimum_boundary}"
    )
    print(f"first maximum witness: {first_large_boundary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
