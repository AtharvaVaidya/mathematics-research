#!/usr/bin/env python3
"""Complete order-12 audit of terminal surface-Euler plateaus.

For a normalized D5 state q on a cubic graph with n vertices, put

    chi(q) = sum_i kappa(C_i(q)) - n/2.

This is the Euler characteristic of the normalized properly 5-coloured
triangulated surface dual to the graph.  In each Kempe orbit, form the
connected components of moves preserving chi.  Such a component is
terminal if no state in it has a chi-increasing move.  The audit checks
whether every terminal plateau is root-universal.
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
from collections import Counter, deque
from pathlib import Path

from audit_d5_root_kempe_orbits import (
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


def surface_chi(graph, state: tuple[int, ...]) -> int:
    link_components = 0
    for coordinate in range(5):
        coordinate_mask = sum(
            1 << edge
            for edge, label in enumerate(state)
            if (label >> coordinate) & 1
        )
        link_components += len(
            [
                component
                for component in component_edge_masks(
                    graph, coordinate_mask
                )
                if component
            ]
        )
    return link_components - graph.vertices // 2


def audit_graph(record: str) -> dict[str, object]:
    graph = graph_from_graph6(record)
    flows = enumerate_flows(graph)
    all_root_pairs = set(
        itertools.combinations(range(graph.edge_count), 2)
    )
    unseen_orbit = set(flows)
    orbit_count = 0
    terminal_plateaus = 0
    plateau_histogram: Counter[tuple[int, int]] = Counter()
    support_range_histogram: Counter[tuple[int, int]] = Counter()
    all_five_plateau_size_histogram: Counter[tuple[int, int]] = Counter()
    all_five_plateaus_with_static_universal_state = 0
    terminal_plateaus_without_missing_coordinate = 0
    first_failure = None

    while unseen_orbit:
        initial = next(iter(unseen_orbit))
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
        unseen_orbit -= orbit
        orbit_count += 1
        chis = {state: surface_chi(graph, state) for state in orbit}

        unseen_plateau = set(orbit)
        while unseen_plateau:
            state = next(iter(unseen_plateau))
            chi = chis[state]
            plateau = {state}
            queue = deque([state])
            while queue:
                current = queue.popleft()
                for neighbour in adjacency[current]:
                    if (
                        chis[neighbour] == chi
                        and neighbour not in plateau
                    ):
                        plateau.add(neighbour)
                        queue.append(neighbour)
            unseen_plateau -= plateau
            if any(
                chis[neighbour] > chi
                for current in plateau
                for neighbour in adjacency[current]
            ):
                continue

            terminal_plateaus += 1
            plateau_histogram[(chi, len(plateau))] += 1
            support_sizes = [
                len({
                    coordinate
                    for label in current
                    for coordinate in range(5)
                    if (label >> coordinate) & 1
                })
                for current in plateau
            ]
            support_range_histogram[
                (min(support_sizes), max(support_sizes))
            ] += 1
            if min(support_sizes) == 5:
                terminal_plateaus_without_missing_coordinate += 1
                all_five_plateau_size_histogram[(chi, len(plateau))] += 1
                if any(
                    successful_root_pairs(graph, current)
                    == all_root_pairs
                    for current in plateau
                ):
                    all_five_plateaus_with_static_universal_state += 1
            successful = set().union(
                *(
                    successful_root_pairs(graph, current)
                    for current in plateau
                )
            )
            failed = sorted(all_root_pairs - successful)
            if failed and first_failure is None:
                first_failure = {
                    "surface_chi": chi,
                    "plateau_size": len(plateau),
                    "root_edge_indices": list(failed[0]),
                    "state_labels_hex": [
                        f"{label:02x}" for label in state
                    ],
                }

    return {
        "graph6": record,
        "vertices": graph.vertices,
        "edges": graph.edge_count,
        "flows_mod_global_s5": len(flows),
        "kempe_orbits_mod_global_s5": orbit_count,
        "terminal_surface_chi_plateaus": terminal_plateaus,
        "terminal_plateau_chi_size_histogram": [
            {"surface_chi": chi, "plateau_size": size, "count": count}
            for (chi, size), count in sorted(plateau_histogram.items())
        ],
        "terminal_plateau_coordinate_support_range_histogram": [
            {
                "minimum_used_coordinates": minimum,
                "maximum_used_coordinates": maximum,
                "count": count,
            }
            for (minimum, maximum), count
            in sorted(support_range_histogram.items())
        ],
        "terminal_plateaus_without_missing_coordinate":
            terminal_plateaus_without_missing_coordinate,
        "all_five_terminal_plateau_chi_size_histogram": [
            {"surface_chi": chi, "plateau_size": size, "count": count}
            for (chi, size), count
            in sorted(all_five_plateau_size_histogram.items())
        ],
        "all_five_terminal_plateaus_with_static_universal_state":
            all_five_plateaus_with_static_universal_state,
        "all_terminal_plateaus_root_universal": first_failure is None,
        "first_failure": first_failure,
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
    histogram: Counter[tuple[int, int]] = Counter()
    support_histogram: Counter[tuple[int, int]] = Counter()
    all_five_histogram: Counter[tuple[int, int]] = Counter()
    for row in rows:
        for item in row["terminal_plateau_chi_size_histogram"]:
            histogram[
                (int(item["surface_chi"]), int(item["plateau_size"]))
            ] += int(item["count"])
        for item in row[
            "terminal_plateau_coordinate_support_range_histogram"
        ]:
            support_histogram[
                (
                    int(item["minimum_used_coordinates"]),
                    int(item["maximum_used_coordinates"]),
                )
            ] += int(item["count"])
        for item in row["all_five_terminal_plateau_chi_size_histogram"]:
            all_five_histogram[
                (int(item["surface_chi"]), int(item["plateau_size"]))
            ] += int(item["count"])
    report = {
        "schema": "d5-surface-chi-terminal-plateau-order12-v1",
        "status": "PASS"
        if all(
            row["all_terminal_plateaus_root_universal"]
            for row in rows
        )
        else "FAIL",
        "claim_tested": (
            "Every terminal equal-surface-chi Kempe plateau is "
            "root-universal."
        ),
        "rows": rows,
        "summary": {
            "graphs": len(rows),
            "flows_mod_global_s5": sum(
                int(row["flows_mod_global_s5"]) for row in rows
            ),
            "kempe_orbits_mod_global_s5": sum(
                int(row["kempe_orbits_mod_global_s5"]) for row in rows
            ),
            "terminal_surface_chi_plateaus": sum(
                int(row["terminal_surface_chi_plateaus"])
                for row in rows
            ),
            "terminal_plateau_chi_size_histogram": [
                {
                    "surface_chi": chi,
                    "plateau_size": size,
                    "count": count,
                }
                for (chi, size), count in sorted(histogram.items())
            ],
            "terminal_plateau_coordinate_support_range_histogram": [
                {
                    "minimum_used_coordinates": minimum,
                    "maximum_used_coordinates": maximum,
                    "count": count,
                }
                for (minimum, maximum), count
                in sorted(support_histogram.items())
            ],
            "terminal_plateaus_without_missing_coordinate": sum(
                int(row["terminal_plateaus_without_missing_coordinate"])
                for row in rows
            ),
            "all_five_terminal_plateau_chi_size_histogram": [
                {
                    "surface_chi": chi,
                    "plateau_size": size,
                    "count": count,
                }
                for (chi, size), count
                in sorted(all_five_histogram.items())
            ],
            "all_five_terminal_plateaus_with_static_universal_state":
                sum(
                    int(row[
                        "all_five_terminal_plateaus_with_static_universal_state"
                    ])
                    for row in rows
                ),
            "surface_chi_min": min(chi for chi, _ in histogram),
            "surface_chi_max": max(chi for chi, _ in histogram),
            "maximum_plateau_size": max(size for _, size in histogram),
            "failed_terminal_plateaus": sum(
                not bool(row["all_terminal_plateaus_root_universal"])
                for row in rows
            ),
        },
        "implication": (
            "For every audited state and root pair, a root-good state "
            "is reachable along a surface-chi-nondecreasing Kempe path."
        ),
        "scope": (
            "Complete finite order-12 audit only; not a universal proof."
        ),
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
