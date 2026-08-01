#!/usr/bin/env python3
"""Focused independent verifier for the order-12 chi-plateau report."""

from __future__ import annotations

import itertools
import json
import subprocess
from collections import Counter, deque
from pathlib import Path

from audit_d5_root_kempe_orbits import (
    enumerate_flows,
    neighbours,
    successful_root_pairs,
)
from tools.fixed_fano_merge_frontier import graph_from_graph6


ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "scratch/d5-surface-chi-terminal-plateaus-order12.json"
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


def independent_chi(graph, state: tuple[int, ...]) -> int:
    incidence = [[] for _ in range(graph.vertices)]
    for edge, (left, right) in enumerate(graph.edges):
        incidence[left].append(edge)
        incidence[right].append(edge)

    def edge_component_count(selected: set[int]) -> int:
        unseen = set(selected)
        count = 0
        while unseen:
            count += 1
            queue = [min(unseen)]
            component: set[int] = set()
            while queue:
                edge = queue.pop()
                if edge in component:
                    continue
                component.add(edge)
                for vertex in graph.edges[edge]:
                    queue.extend(
                        other
                        for other in incidence[vertex]
                        if other in selected and other not in component
                    )
            unseen -= component
        return count

    vertices = 0
    for coordinate in range(5):
        selected = {
            edge
            for edge, label in enumerate(state)
            if (label >> coordinate) & 1
        }
        vertices += edge_component_count(selected)
    return vertices - graph.vertices // 2


def replay_graph(record: str) -> dict[str, object]:
    graph = graph_from_graph6(record)
    flows = enumerate_flows(graph)
    all_roots = set(itertools.combinations(range(graph.edge_count), 2))
    unseen = set(flows)
    orbit_count = 0
    terminal_count = 0
    histogram: Counter[tuple[int, int]] = Counter()

    while unseen:
        initial = next(iter(unseen))
        orbit = {initial}
        queue = deque([initial])
        adjacency = {}
        while queue:
            state = queue.popleft()
            row = set(neighbours(graph, state))
            adjacency[state] = row
            for neighbour in row:
                if neighbour not in orbit:
                    orbit.add(neighbour)
                    queue.append(neighbour)
        unseen -= orbit
        orbit_count += 1
        chi = {state: independent_chi(graph, state) for state in orbit}

        remaining = set(orbit)
        while remaining:
            initial_state = next(iter(remaining))
            value = chi[initial_state]
            plateau = {initial_state}
            queue = deque([initial_state])
            while queue:
                state = queue.popleft()
                for neighbour in adjacency[state]:
                    if chi[neighbour] == value and neighbour not in plateau:
                        plateau.add(neighbour)
                        queue.append(neighbour)
            remaining -= plateau
            has_ascent = any(
                chi[neighbour] > value
                for state in plateau
                for neighbour in adjacency[state]
            )
            if has_ascent:
                continue

            terminal_count += 1
            histogram[(value, len(plateau))] += 1
            covered = set()
            for state in plateau:
                covered.update(successful_root_pairs(graph, state))
            assert covered == all_roots

    return {
        "flows_mod_global_s5": len(flows),
        "kempe_orbits_mod_global_s5": orbit_count,
        "terminal_surface_chi_plateaus": terminal_count,
        "terminal_plateau_chi_size_histogram": [
            {"surface_chi": chi, "plateau_size": size, "count": count}
            for (chi, size), count in sorted(histogram.items())
        ],
        "all_terminal_plateaus_root_universal": True,
        "first_failure": None,
    }


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["status"] == "PASS"
    rows = report["rows"]
    generated = generated_records()
    assert [row["graph6"] for row in rows] == generated
    assert len(rows) == 81
    assert all(row["vertices"] == 12 and row["edges"] == 18 for row in rows)
    assert all(
        row["all_terminal_plateaus_root_universal"]
        and row["first_failure"] is None
        for row in rows
    )

    histogram: Counter[tuple[int, int]] = Counter()
    for row in rows:
        for item in row["terminal_plateau_chi_size_histogram"]:
            histogram[
                (int(item["surface_chi"]), int(item["plateau_size"]))
            ] += int(item["count"])
    summary = report["summary"]
    assert summary["graphs"] == 81
    assert summary["flows_mod_global_s5"] == 25_960
    assert summary["kempe_orbits_mod_global_s5"] == 2_650
    assert summary["terminal_surface_chi_plateaus"] == 2_659
    assert summary["failed_terminal_plateaus"] == 0
    assert summary["surface_chi_min"] == -3
    assert summary["surface_chi_max"] == 2
    assert summary["maximum_plateau_size"] == 432
    assert sum(histogram.values()) == 2_659
    assert summary["terminal_plateau_chi_size_histogram"] == [
        {"surface_chi": chi, "plateau_size": size, "count": count}
        for (chi, size), count in sorted(histogram.items())
    ]

    selected_indices = {
        0,
        len(rows) - 1,
        max(
            range(len(rows)),
            key=lambda index: int(rows[index]["flows_mod_global_s5"]),
        ),
        next(
            index
            for index, row in enumerate(rows)
            if any(
                item["surface_chi"] == -3
                for item in row["terminal_plateau_chi_size_histogram"]
            )
        ),
        next(
            index
            for index, row in enumerate(rows)
            if any(
                item["plateau_size"] == 432
                for item in row["terminal_plateau_chi_size_histogram"]
            )
        ),
    }
    semantic_rows = []
    # The producer may append exploratory coordinate-support diagnostics.
    # The independent replay below certifies the frozen root-universality
    # fields; those additive diagnostics have their own direct census and
    # are deliberately outside this verifier's claim.
    ignored = {
        "graph6",
        "vertices",
        "edges",
        "terminal_plateau_coordinate_support_range_histogram",
        "terminal_plateaus_without_missing_coordinate",
        "all_five_terminal_plateau_chi_size_histogram",
        "all_five_terminal_plateaus_with_static_universal_state",
    }
    for index in sorted(selected_indices):
        row = rows[index]
        replay = replay_graph(str(row["graph6"]))
        expected = {
            key: value for key, value in row.items() if key not in ignored
        }
        assert replay == expected
        semantic_rows.append(
            {"index": index + 1, "graph6": row["graph6"], **replay}
        )

    print(
        json.dumps(
            {
                "status": "PASS",
                "complete_rows_regenerated": len(rows),
                "complete_terminal_plateaus": 2_659,
                "focused_independent_semantic_replays": semantic_rows,
                "scope": (
                    "All graph identities and report arithmetic are "
                    "checked; deterministic boundary/extremal rows are "
                    "recomputed with an independently structured "
                    "plateau traversal and coordinate-link counter."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
