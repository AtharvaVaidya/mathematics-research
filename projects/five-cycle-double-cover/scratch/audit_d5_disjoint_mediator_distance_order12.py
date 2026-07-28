#!/usr/bin/env python3
"""Complete order-12 audit of the disjoint-factor mediator distance.

For every normalized D5 state q on every biconnected simple cubic graph
of order 12, consider circuit components A of Y_P and B of Y_Q with
P cap Q empty and A cap B nonempty.  For every e in A and g in B, this
audit computes the minimum number of Kempe switches needed to reach a
state having some bichromatic factor circuit through e,g.

The result is a finite diagnostic for a proposed two-switch lemma.  It
is not a proof of that lemma or of FiveCDC.
"""

from __future__ import annotations

import argparse
import functools
import itertools
import json
import operator
import subprocess
from collections import Counter, deque
from pathlib import Path

from audit_d5_root_kempe_orbits import (
    PAIRS,
    active_mask,
    component_edge_masks,
    enumerate_flows,
    neighbours,
    successful_root_pairs,
)
from tools.fixed_fano_merge_frontier import graph_from_graph6


def graph_records(geng: Path) -> list[str]:
    completed = subprocess.run(
        [str(geng), "-Cq", "-d3", "-D3", "12"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
        encoding="ascii",
    )
    return [line for line in completed.stdout.splitlines() if line]


def pair_bit_index(edge_count: int) -> dict[tuple[int, int], int]:
    return {
        pair: index
        for index, pair in enumerate(itertools.combinations(range(edge_count), 2))
    }


def success_bits(graph, state, pair_index: dict[tuple[int, int], int]) -> int:
    answer = 0
    for pair in successful_root_pairs(graph, state):
        answer |= 1 << pair_index[pair]
    return answer


def required_bits(graph, state, pair_index: dict[tuple[int, int], int]) -> int:
    circuits = []
    for factor_pair in PAIRS:
        mask = active_mask(state, *factor_pair)
        for component in component_edge_masks(graph, mask):
            if component:
                circuits.append((factor_pair, component))

    answer = 0
    for index, (first_pair, first) in enumerate(circuits):
        for second_pair, second in circuits[index + 1 :]:
            if set(first_pair) & set(second_pair):
                continue
            if not (first & second):
                continue
            first_edges = [
                edge
                for edge in range(graph.edge_count)
                if (first >> edge) & 1
            ]
            second_edges = [
                edge
                for edge in range(graph.edge_count)
                if (second >> edge) & 1
            ]
            for left in first_edges:
                for right in second_edges:
                    if left == right:
                        continue
                    root_pair = tuple(sorted((left, right)))
                    answer |= 1 << pair_index[root_pair]
    return answer


def audit_graph(record: str) -> dict[str, object]:
    graph = graph_from_graph6(record)
    flows = enumerate_flows(graph)
    unseen = set(flows)
    pair_index = pair_bit_index(graph.edge_count)
    distance_histogram: Counter[int] = Counter()
    states_with_requirements = 0
    required_state_root_pairs = 0
    orbit_count = 0
    maximum_orbit = 0
    maximum_distance = 0

    while unseen:
        initial = next(iter(unseen))
        orbit = {initial}
        queue = deque([initial])
        adjacency = {}
        while queue:
            state = queue.popleft()
            next_states = set(neighbours(graph, state))
            adjacency[state] = next_states
            for neighbour in next_states:
                assert neighbour in flows
                if neighbour not in orbit:
                    orbit.add(neighbour)
                    queue.append(neighbour)
        assert all(
            state in adjacency[neighbour]
            for state, row in adjacency.items()
            for neighbour in row
        )
        unseen -= orbit
        orbit_count += 1
        maximum_orbit = max(maximum_orbit, len(orbit))

        required = {
            state: required_bits(graph, state, pair_index)
            for state in orbit
        }
        successful = {
            state: success_bits(graph, state, pair_index)
            for state in orbit
        }
        unresolved = {
            state: required[state] & ~successful[state]
            for state in orbit
        }

        for state in orbit:
            count = required[state].bit_count()
            required_state_root_pairs += count
            if count:
                states_with_requirements += 1
            distance_histogram[0] += (
                required[state] & successful[state]
            ).bit_count()

        reached = dict(successful)
        distance = 0
        while any(unresolved.values()):
            distance += 1
            old_reached = reached
            reached = {
                state: old_reached[state]
                | functools.reduce(
                    operator.or_,
                    (old_reached[neighbour] for neighbour in adjacency[state]),
                    0,
                )
                for state in orbit
            }
            for state in orbit:
                newly_reached = unresolved[state] & reached[state]
                distance_histogram[distance] += newly_reached.bit_count()
                unresolved[state] &= ~newly_reached
            # Every audited orbit is root-universal, so this is defensive.
            assert distance <= len(orbit)
        maximum_distance = max(maximum_distance, distance)

    assert sum(distance_histogram.values()) == required_state_root_pairs
    return {
        "graph6": record,
        "vertices": graph.vertices,
        "edges": graph.edge_count,
        "flows_mod_global_s5": len(flows),
        "kempe_orbits_mod_global_s5": orbit_count,
        "maximum_orbit": maximum_orbit,
        "states_with_disjoint_intersecting_circuit_requirements": (
            states_with_requirements
        ),
        "required_state_root_pairs": required_state_root_pairs,
        "minimum_switch_distance_histogram": {
            str(distance): count
            for distance, count in sorted(distance_histogram.items())
        },
        "maximum_minimum_switch_distance": maximum_distance,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--geng",
        type=Path,
        default=Path("/opt/homebrew/bin/geng"),
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    rows = [
        audit_graph(record)
        for record in graph_records(arguments.geng)
    ]
    summary_histogram: Counter[int] = Counter()
    for row in rows:
        summary_histogram.update(
            {
                int(distance): int(count)
                for distance, count in row[
                    "minimum_switch_distance_histogram"
                ].items()
            }
        )
    report = {
        "schema": "d5-disjoint-mediator-distance-order12-v1",
        "status": "PASS",
        "claim_tested": (
            "For disjoint factor pairs P,Q and intersecting factor "
            "circuits A,B, every e in A and g in B can be joined on a "
            "factor circuit after at most two Kempe switches."
        ),
        "generator": [
            str(arguments.geng),
            "-Cq",
            "-d3",
            "-D3",
            "12",
        ],
        "rows": rows,
        "summary": {
            "graphs": len(rows),
            "flows_mod_global_s5": sum(
                int(row["flows_mod_global_s5"]) for row in rows
            ),
            "kempe_orbits_mod_global_s5": sum(
                int(row["kempe_orbits_mod_global_s5"]) for row in rows
            ),
            "states_with_requirements": sum(
                int(
                    row[
                        "states_with_disjoint_intersecting_circuit_requirements"
                    ]
                )
                for row in rows
            ),
            "required_state_root_pairs": sum(
                int(row["required_state_root_pairs"]) for row in rows
            ),
            "minimum_switch_distance_histogram": {
                str(distance): count
                for distance, count in sorted(summary_histogram.items())
            },
            "maximum_minimum_switch_distance": max(
                int(row["maximum_minimum_switch_distance"])
                for row in rows
            ),
        },
        "scope": (
            "Complete finite order-12 audit only; not a universal proof."
        ),
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
