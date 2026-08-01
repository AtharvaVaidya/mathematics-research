#!/usr/bin/env python3
"""Deterministic stress test of the local boundary-degree lemma.

The candidate says that, for the three factor components through any
adjacent graph-edge pair, at least one has at most two same-pair boundary
chords.  This script samples Tait-derived states and deterministic Kempe
walks on random connected cubic graphs.
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRATCH = PROJECT_ROOT / "scratch"
for item in (str(PROJECT_ROOT), str(SCRATCH)):
    if item not in sys.path:
        sys.path.insert(0, item)

from audit_d5_root_kempe_orbits import (  # noqa: E402
    PAIRS,
    active_mask,
    component_edge_masks,
    neighbours,
)
from search_d5_component_chain_tait_stress import sample_graph  # noqa: E402


def component_vertices(graph, component: int) -> set[int]:
    answer = set()
    for edge, (left, right) in enumerate(graph.edges):
        if (component >> edge) & 1:
            answer.add(left)
            answer.add(right)
    return answer


def boundary_size(graph, state, pair, component) -> int:
    vertices = component_vertices(graph, component)
    pair_label = (1 << pair[0]) | (1 << pair[1])
    return sum(
        state[edge] == pair_label
        and ((left in vertices) != (right in vertices))
        for edge, (left, right) in enumerate(graph.edges)
    )


def audit_state(graph, state):
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
            assert size % 2 == 0
            for edge in range(graph.edge_count):
                if (component >> edge) & 1:
                    through[(edge, pair)] = (component, size)
    triples = 0
    for vertex, row in enumerate(incidence):
        for left in range(3):
            for right in range(left + 1, 3):
                candidates = []
                for pair in PAIRS:
                    item = through.get((row[left], pair))
                    if item and ((item[0] >> row[right]) & 1):
                        candidates.append((pair, item[1]))
                assert len(candidates) == 3
                triples += 1
                if min(size for _, size in candidates) > 2:
                    return triples, {
                        "vertex": vertex,
                        "edge_pair": [row[left], row[right]],
                        "candidates": [
                            {"pair": list(pair), "boundary_size": size}
                            for pair, size in candidates
                        ],
                    }
    return triples, None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=20)
    parser.add_argument("--graphs", type=int, default=20)
    parser.add_argument("--states-per-graph", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260728)
    args = parser.parse_args()
    generator = random.Random(args.seed)
    graph_count = 0
    state_count = 0
    triple_count = 0
    while graph_count < args.graphs:
        sampled = sample_graph(args.order, generator)
        if sampled is None:
            continue
        graph6, graph, state = sampled
        graph_count += 1
        for _ in range(args.states_per_graph):
            tested, failure = audit_state(graph, state)
            state_count += 1
            triple_count += tested
            if failure is not None:
                print({
                    "status": "FAIL",
                    "graph6": graph6,
                    "state_labels_hex": [
                        f"{label:02x}" for label in state
                    ],
                    **failure,
                })
                return 1
            next_states = sorted(set(neighbours(graph, state)) - {state})
            if next_states:
                state = generator.choice(next_states)
    print(
        "PASS: "
        f"graphs={graph_count}, states={state_count}, "
        f"local_triples={triple_count}, failures=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
