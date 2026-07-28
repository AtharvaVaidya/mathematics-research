#!/usr/bin/env python3
"""Deterministic stress search for the D5 component-chain potential.

Generate simple connected cubic graphs as unions of three disjoint perfect
matchings.  Their matching colors give a Tait-derived D5 state.  For every
root pair, test whether some single Kempe move lowers the current factor-
component chain distance.  A hit is only a strict local minimum; a separate
equal-level plateau traversal is needed to refute the proposed plateau lemma.
"""

from __future__ import annotations

import argparse
import random
import sys
from collections import Counter, deque
from pathlib import Path

import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRATCH = PROJECT_ROOT / "scratch"
for item in (str(PROJECT_ROOT), str(SCRATCH)):
    if item not in sys.path:
        sys.path.insert(0, item)

from audit_d5_root_component_chain_potential import (  # noqa: E402
    all_root_distances,
    component_masks,
)
from audit_d5_root_kempe_orbits import canonical, neighbours  # noqa: E402
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402


def random_matching(vertices: list[int], generator: random.Random):
    shuffled = vertices[:]
    generator.shuffle(shuffled)
    return {
        tuple(sorted((shuffled[index], shuffled[index + 1])))
        for index in range(0, len(shuffled), 2)
    }


def sample_graph(order: int, generator: random.Random):
    vertices = list(range(order))
    first = {(index, index + 1) for index in range(0, order, 2)}
    while True:
        second = random_matching(vertices, generator)
        if first.isdisjoint(second):
            break
    while True:
        third = random_matching(vertices, generator)
        if first.isdisjoint(third) and second.isdisjoint(third):
            break
    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(first | second | third)
    if not nx.is_connected(graph):
        return None
    graph6 = nx.to_graph6_bytes(graph, header=False).decode("ascii").strip()
    decoded = graph_from_graph6(graph6)
    color = {
        **{edge: 3 for edge in first},
        **{edge: 5 for edge in second},
        **{edge: 6 for edge in third},
    }
    state = canonical(tuple(color[edge] for edge in decoded.edges))
    return graph6, decoded, state


def plateau_escape(graph, initial, roots, level: int, cap: int):
    queue = deque([(initial, 0)])
    seen = {initial}
    while queue:
        state, depth = queue.popleft()
        for other in set(neighbours(graph, state)) - {state}:
            distance = all_root_distances(
                graph.edge_count,
                component_masks(graph, other),
            )[roots[0]][roots[1]]
            if distance < level:
                return {
                    "status": "ESCAPED",
                    "equal_states_seen": len(seen),
                    "equal_moves_before_descent": depth,
                    "new_distance": distance,
                }
            if distance == level and other not in seen:
                seen.add(other)
                if len(seen) > cap:
                    return {
                        "status": "CAP_REACHED",
                        "equal_states_seen": len(seen),
                    }
                queue.append((other, depth + 1))
    return {
        "status": "PLATEAU_FAILURE",
        "equal_states_seen": len(seen),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=20)
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260728)
    parser.add_argument("--plateau-cap", type=int, default=100_000)
    parser.add_argument("--audit-all-local-minima", action="store_true")
    arguments = parser.parse_args()
    generator = random.Random(arguments.seed)
    generated = 0
    maximum = 0
    root_tests = 0
    strict_local_minima = Counter()
    plateau_escape_depths = Counter()
    plateau_failures = []
    first = None
    while generated < arguments.samples:
        sampled = sample_graph(arguments.order, generator)
        if sampled is None:
            continue
        generated += 1
        graph6, graph, state = sampled
        distances = all_root_distances(
            graph.edge_count,
            component_masks(graph, state),
        )
        next_states = set(neighbours(graph, state)) - {state}
        next_distances = [
            all_root_distances(
                graph.edge_count,
                component_masks(graph, other),
            )
            for other in next_states
        ]
        for root in range(graph.edge_count):
            for target in range(root + 1, graph.edge_count):
                level = distances[root][target]
                maximum = max(maximum, level)
                root_tests += 1
                if level > 1 and all(
                    row[root][target] >= level for row in next_distances
                ):
                    strict_local_minima[level] += 1
                    plateau_audit = None
                    if arguments.audit_all_local_minima:
                        plateau_audit = plateau_escape(
                            graph,
                            state,
                            (root, target),
                            level,
                            arguments.plateau_cap,
                        )
                        if plateau_audit["status"] == "ESCAPED":
                            plateau_escape_depths[
                                plateau_audit["equal_moves_before_descent"]
                            ] += 1
                        else:
                            plateau_failures.append(
                                {
                                    "graph6": graph6,
                                    "roots": [root, target],
                                    "distance": level,
                                    "audit": plateau_audit,
                                }
                            )
                    if first is None:
                        first = {
                            "graph6": graph6,
                            "labels_hex": [hex(value) for value in state],
                            "roots": [root, target],
                            "distance": level,
                            "neighbour_distance_histogram": dict(
                                Counter(
                                    row[root][target]
                                    for row in next_distances
                                )
                            ),
                        }
                        first["plateau_audit"] = plateau_audit or plateau_escape(
                                graph,
                                state,
                                (root, target),
                                level,
                                arguments.plateau_cap,
                            )
        if generated % 10 == 0:
            print(
                f"PROGRESS graphs={generated} root_tests={root_tests} "
                f"maximum_distance={maximum} "
                f"strict_local_minima={dict(strict_local_minima)}",
                flush=True,
            )
    print(
        {
            "graphs": generated,
            "order": arguments.order,
            "root_tests": root_tests,
            "maximum_distance": maximum,
            "strict_local_minima_by_level": dict(strict_local_minima),
            "plateau_escape_depths": dict(plateau_escape_depths),
            "plateau_failures": plateau_failures,
            "first_strict_local_minimum": first,
        }
    )


if __name__ == "__main__":
    main()
