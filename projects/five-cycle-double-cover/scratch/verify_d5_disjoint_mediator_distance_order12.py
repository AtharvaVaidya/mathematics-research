#!/usr/bin/env python3
"""Focused independent verifier for the order-12 mediator-distance report.

The producer propagates bit sets backwards through complete Kempe orbits.
This verifier instead computes, from each selected state, the literal
radius-zero, radius-one, and radius-two neighbourhood and classifies
required root pairs directly.  It also regenerates all 81 graph6 rows
and checks every reported arithmetic total.
"""

from __future__ import annotations

import itertools
import json
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


ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "scratch/d5-disjoint-mediator-distance-order12.json"
GENG = Path("/opt/homebrew/bin/geng")


def generated_records() -> list[str]:
    completed = subprocess.run(
        [str(GENG), "-Cq", "-d3", "-D3", "12"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
        encoding="ascii",
    )
    return [line for line in completed.stdout.splitlines() if line]


def required_pairs(graph, state) -> set[tuple[int, int]]:
    circuits = []
    for factor_pair in PAIRS:
        for component in component_edge_masks(
            graph, active_mask(state, *factor_pair)
        ):
            if component:
                circuits.append((factor_pair, component))
    answer: set[tuple[int, int]] = set()
    for index, (first_pair, first) in enumerate(circuits):
        for second_pair, second in circuits[index + 1 :]:
            if set(first_pair) & set(second_pair) or not (first & second):
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
            answer.update(
                tuple(sorted((left, right)))
                for left in first_edges
                for right in second_edges
                if left != right
            )
    return answer


def replay_row(record: str) -> dict[str, object]:
    graph = graph_from_graph6(record)
    flows = enumerate_flows(graph)
    unseen = set(flows)
    orbit_count = 0
    maximum_orbit = 0
    histogram: Counter[int] = Counter()
    states_with_requirements = 0

    while unseen:
        initial = next(iter(unseen))
        orbit = {initial}
        queue = deque([initial])
        while queue:
            state = queue.popleft()
            for neighbour in neighbours(graph, state):
                assert neighbour in flows
                if neighbour not in orbit:
                    orbit.add(neighbour)
                    queue.append(neighbour)
        unseen -= orbit
        orbit_count += 1
        maximum_orbit = max(maximum_orbit, len(orbit))

    for state in flows:
        required = required_pairs(graph, state)
        if required:
            states_with_requirements += 1
        reached_zero = successful_root_pairs(graph, state)
        first_states = set(neighbours(graph, state))
        reached_one = set(reached_zero)
        for neighbour in first_states:
            reached_one.update(successful_root_pairs(graph, neighbour))
        second_states = {
            second
            for neighbour in first_states
            for second in neighbours(graph, neighbour)
        }
        reached_two = set(reached_one)
        for second in second_states:
            reached_two.update(successful_root_pairs(graph, second))

        assert required <= reached_two
        histogram[0] += len(required & reached_zero)
        histogram[1] += len((required - reached_zero) & reached_one)
        histogram[2] += len((required - reached_one) & reached_two)

    histogram = Counter(
        {distance: count for distance, count in histogram.items() if count}
    )
    return {
        "flows_mod_global_s5": len(flows),
        "kempe_orbits_mod_global_s5": orbit_count,
        "maximum_orbit": maximum_orbit,
        "states_with_disjoint_intersecting_circuit_requirements": (
            states_with_requirements
        ),
        "required_state_root_pairs": sum(histogram.values()),
        "minimum_switch_distance_histogram": {
            str(distance): count
            for distance, count in sorted(histogram.items())
        },
        "maximum_minimum_switch_distance": max(histogram, default=0),
    }


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["status"] == "PASS"
    rows = report["rows"]
    generated = generated_records()
    assert [row["graph6"] for row in rows] == generated
    assert len(rows) == 81
    assert all(row["vertices"] == 12 and row["edges"] == 18 for row in rows)

    summary = report["summary"]
    combined_histogram: Counter[int] = Counter()
    for row in rows:
        combined_histogram.update(
            {
                int(distance): int(count)
                for distance, count in row[
                    "minimum_switch_distance_histogram"
                ].items()
            }
        )
    replayed_summary = {
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
            for distance, count in sorted(combined_histogram.items())
        },
        "maximum_minimum_switch_distance": max(combined_histogram),
    }
    assert replayed_summary == summary
    assert summary == {
        "graphs": 81,
        "flows_mod_global_s5": 25_960,
        "kempe_orbits_mod_global_s5": 2_650,
        "states_with_requirements": 25_960,
        "required_state_root_pairs": 3_970_092,
        "minimum_switch_distance_histogram": {
            "0": 3_783_384,
            "1": 181_065,
            "2": 5_643,
        },
        "maximum_minimum_switch_distance": 2,
    }

    selected_indices = {
        0,
        len(rows) - 1,
        next(
            index
            for index, row in enumerate(rows)
            if row["maximum_minimum_switch_distance"] == 2
        ),
        max(
            range(len(rows)),
            key=lambda index: int(rows[index]["flows_mod_global_s5"]),
        ),
        max(
            range(len(rows)),
            key=lambda index: int(rows[index]["kempe_orbits_mod_global_s5"]),
        ),
    }
    semantic_rows = []
    ignored_keys = {"graph6", "vertices", "edges"}
    for index in sorted(selected_indices):
        row = rows[index]
        replay = replay_row(str(row["graph6"]))
        expected = {
            key: value
            for key, value in row.items()
            if key not in ignored_keys
        }
        assert replay == expected
        semantic_rows.append(
            {
                "index": index + 1,
                "graph6": row["graph6"],
                **replay,
            }
        )

    print(
        json.dumps(
            {
                "status": "PASS",
                "complete_rows_regenerated": len(rows),
                "complete_required_state_root_pairs": summary[
                    "required_state_root_pairs"
                ],
                "focused_direct_radius_two_replays": semantic_rows,
                "scope": (
                    "All census identities and arithmetic are checked; "
                    "five deterministic boundary/extremal rows are "
                    "semantically replayed by direct radius-two expansion."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
