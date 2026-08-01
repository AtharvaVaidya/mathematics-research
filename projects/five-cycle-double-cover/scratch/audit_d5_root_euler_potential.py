#!/usr/bin/env python3
"""Audit the surface Euler-characteristic potential in D5 Kempe orbits."""

from __future__ import annotations

import itertools
import json
import sys
from collections import deque

from audit_d5_root_kempe_orbits import (
    canonical,
    component_edge_masks,
    enumerate_flows,
    neighbours,
    successful_root_pairs,
)
from tools.fixed_fano_merge_frontier import graph_from_graph6


def coordinate_mask(state, coordinate: int) -> int:
    return sum(
        1 << edge
        for edge, label in enumerate(state)
        if (label >> coordinate) & 1
    )


def euler_characteristic(graph, state) -> int:
    primal_vertices = sum(
        sum(
            component != 0
            for component in component_edge_masks(
                graph,
                coordinate_mask(state, coordinate),
            )
        )
        for coordinate in range(5)
    )
    return primal_vertices - graph.edge_count + graph.vertices


def audit(record: str):
    graph = graph_from_graph6(record)
    states = sorted(enumerate_flows(graph))
    index = {state: position for position, state in enumerate(states)}
    adjacency = [
        sorted(
            {
                index[other]
                for other in neighbours(graph, state)
                if other != state
            }
        )
        for state in states
    ]
    chi = [euler_characteristic(graph, state) for state in states]
    root_pairs = set(itertools.combinations(range(graph.edge_count), 2))
    successes = [
        successful_root_pairs(graph, state)
        for state in states
    ]

    unseen = set(range(len(states)))
    orbit_count = 0
    maximum_components = 0
    union_failures = 0
    component_failures = 0
    first_failure = None
    while unseen:
        initial = next(iter(unseen))
        orbit = {initial}
        queue = deque([initial])
        while queue:
            current = queue.popleft()
            for other in adjacency[current]:
                if other not in orbit:
                    orbit.add(other)
                    queue.append(other)
        unseen.difference_update(orbit)
        orbit_count += 1
        maximum = max(chi[state] for state in orbit)
        maximizers = {state for state in orbit if chi[state] == maximum}
        rescued = set().union(*(successes[state] for state in maximizers))
        union_missing = root_pairs - rescued
        if union_missing:
            union_failures += 1
            if first_failure is None:
                first_failure = {
                    "kind": "chi_maximum_union",
                    "orbit_initial_state_index": initial,
                    "chi_maximum": maximum,
                    "chi_maximizers": len(maximizers),
                    "first_missing_roots": list(min(union_missing)),
                }

        remaining = set(maximizers)
        components = 0
        while remaining:
            start = next(iter(remaining))
            component = {start}
            queue = deque([start])
            while queue:
                current = queue.popleft()
                for other in adjacency[current]:
                    if other in maximizers and other not in component:
                        component.add(other)
                        queue.append(other)
            remaining.difference_update(component)
            components += 1
            component_rescued = set().union(
                *(successes[state] for state in component)
            )
            component_missing = root_pairs - component_rescued
            if component_missing:
                component_failures += 1
                if first_failure is None:
                    first_failure = {
                        "kind": "chi_maximum_component",
                        "orbit_initial_state_index": initial,
                        "chi_maximum": maximum,
                        "chi_maximum_component_size": len(component),
                        "first_missing_roots": list(min(component_missing)),
                    }
        maximum_components = max(maximum_components, components)

    return {
        "graph6": record,
        "vertices": graph.vertices,
        "states_mod_s5": len(states),
        "kempe_orbits_mod_s5": orbit_count,
        "chi_range": [min(chi), max(chi)],
        "maximum_chi_components_in_one_orbit": maximum_components,
        "orbits_whose_chi_maximum_union_misses_a_root_pair": union_failures,
        "chi_maximum_components_missing_a_root_pair": component_failures,
        "chi_maximum_union_rescues_every_root_pair": union_failures == 0,
        "every_chi_maximum_component_rescues_every_root_pair":
            component_failures == 0,
        "first_failure": first_failure,
    }


def main() -> None:
    records = sys.argv[1:] or [
        line.strip() for line in sys.stdin if line.strip()
    ]
    if not records:
        raise SystemExit("supply graph6 records as arguments or stdin")
    results = [audit(record) for record in records]
    print(json.dumps(results[0] if len(results) == 1 else results, indent=2))


if __name__ == "__main__":
    main()
