#!/usr/bin/env python3
"""Independent Python audit of the terminal-chi/chain lexicographic target."""

from __future__ import annotations

import json
import subprocess
import sys
from collections import deque
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for item in (PROJECT_ROOT, PROJECT_ROOT / "scratch"):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from audit_d5_root_component_chain_potential import (  # noqa: E402
    all_root_distances,
    component_masks,
)
from audit_d5_root_kempe_orbits import (  # noqa: E402
    enumerate_flows,
    neighbours,
)
from audit_d5_surface_chi_plateaus_order12 import surface_chi  # noqa: E402
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402


def graph_records(order: int) -> tuple[str, ...]:
    completed = subprocess.run(
        [
            "/opt/homebrew/bin/geng",
            "-Cq",
            "-d3",
            "-D3",
            str(order),
        ],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
        encoding="ascii",
    )
    return tuple(row for row in completed.stdout.splitlines() if row)


def audit_graph(record: str) -> dict[str, object]:
    graph = graph_from_graph6(record)
    states = enumerate_flows(graph)
    adjacency = {
        state: set(neighbours(graph, state)) - {state}
        for state in states
    }
    chis = {state: surface_chi(graph, state) for state in states}
    distances = {
        state: all_root_distances(
            graph.edge_count, component_masks(graph, state)
        )
        for state in states
    }
    maximum_distance = max(
        distance
        for matrix in distances.values()
        for row in matrix
        for distance in row
    )
    unseen_chi = set(states)
    terminal_chi_plateaus = 0
    distance_plateaus = 0
    failure = None
    while unseen_chi:
        seed = next(iter(unseen_chi))
        level = chis[seed]
        plateau = {seed}
        queue = deque([seed])
        terminal = True
        while queue:
            state = queue.popleft()
            for other in adjacency[state]:
                if chis[other] > level:
                    terminal = False
                if chis[other] == level and other not in plateau:
                    plateau.add(other)
                    queue.append(other)
        unseen_chi -= plateau
        if not terminal:
            continue
        terminal_chi_plateaus += 1
        for root in range(graph.edge_count):
            for target in range(root + 1, graph.edge_count):
                unseen_distance = set(plateau)
                while unseen_distance:
                    start = next(iter(unseen_distance))
                    distance_level = distances[start][root][target]
                    distance_plateau = {start}
                    queue = deque([start])
                    descent = False
                    while queue:
                        state = queue.popleft()
                        for other in adjacency[state]:
                            if other not in plateau:
                                continue
                            other_distance = distances[other][root][target]
                            if other_distance < distance_level:
                                descent = True
                            if (
                                other_distance == distance_level
                                and other not in distance_plateau
                            ):
                                distance_plateau.add(other)
                                queue.append(other)
                    unseen_distance -= distance_plateau
                    if distance_level <= 1:
                        continue
                    distance_plateaus += 1
                    if not descent and failure is None:
                        failure = {
                            "state_hex": "".join(
                                f"{label:02x}" for label in start
                            ),
                            "roots": [root, target],
                            "chi": level,
                            "distance": distance_level,
                            "chi_plateau_size": len(plateau),
                            "distance_plateau_size": len(distance_plateau),
                        }
    return {
        "graph6": record,
        "flows_mod_s5": len(states),
        "terminal_chi_plateaus": terminal_chi_plateaus,
        "terminal_chi_distance_plateaus": distance_plateaus,
        "maximum_distance": maximum_distance,
        "lex_failures": int(failure is not None),
        "first_failure": failure,
    }


def main() -> int:
    rows = [audit_graph(record) for record in graph_records(12)]
    summary = {
        "status": "PASS"
        if all(row["lex_failures"] == 0 for row in rows)
        else "FAIL",
        "graphs": len(rows),
        "flows_mod_s5": sum(row["flows_mod_s5"] for row in rows),
        "terminal_chi_plateaus": sum(
            row["terminal_chi_plateaus"] for row in rows
        ),
        "terminal_chi_distance_plateaus": sum(
            row["terminal_chi_distance_plateaus"] for row in rows
        ),
        "maximum_distance": max(
            row["maximum_distance"] for row in rows
        ),
        "lex_failures": sum(row["lex_failures"] for row in rows),
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
