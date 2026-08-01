#!/usr/bin/env python3
"""Finite frontier for the fixed-flow three-pair merge criterion.

For each graph6 row in a retained graph report, enumerate one representative
of every nowhere-zero F_2^3-flow orbit under GL(3,2), following the same
normalization used by ``fano_flow_repair_audit.py``.  For every representative
solve the joint local-triangle/three-pair-merge SAT instance from
``fixed_fano_cover_merge_audit.py`` and check the decoded five-cover
semantically.

The result is a finite census only.  Even a complete PASS cannot replace a
universal proof of the fixed-flow merge statement.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.cycle_space_switch_audit import fundamental_cycle_space
from tools.fano_value_class_tjoin_audit import flow_values
from tools.fixed_fano_cover_merge_audit import (
    build_joint_merge_cnf,
    decode_and_check,
    decode_joint_matching,
    direct_potential_merge_audit,
    graph_incidence,
    local_states,
    solve,
)
from tools.flow_switch_audit import Graph, good_lines, is_flow


def graph_from_graph6(row: str) -> Graph:
    graph = nx.from_graph6_bytes(row.encode("ascii"))
    vertices = graph.number_of_nodes()
    if sorted(graph.nodes()) != list(range(vertices)):
        graph = nx.convert_node_labels_to_integers(
            graph, ordering="sorted"
        )
    edges = tuple(
        sorted((min(int(u), int(v)), max(int(u), int(v))) for u, v in graph.edges())
    )
    result = Graph(vertices, edges)
    if len(edges) != 3 * vertices // 2:
        raise ValueError("graph6 row is not cubic")
    degree = Counter(point for edge in edges for point in edge)
    if set(degree.values()) != {3}:
        raise ValueError("graph6 row is not cubic")
    if not nx.is_connected(graph):
        raise ValueError("graph6 row is not connected")
    return result


def cycle_pattern(
    cycle: int, incident: tuple[int, int, int]
) -> tuple[int, int, int]:
    return tuple((cycle >> edge) & 1 for edge in incident)


def matching_rank(matching: tuple[tuple[int, int], ...]) -> int:
    basis: list[int] = []
    for value in (first ^ second for first, second in matching):
        for pivot in basis:
            value = min(value, value ^ pivot)
        if value:
            basis.append(value)
            basis.sort(reverse=True)
    return len(basis)


def audit_graph(
    graph6: str,
    graph: Graph,
    cadical: str,
    stop_on_failure: bool,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    cycles = fundamental_cycle_space(graph)
    all_edges = (1 << graph.edge_count) - 1
    incidence = graph_incidence(graph.vertices, graph.edges)
    incident = tuple(
        edge for edge, endpoints in enumerate(graph.edges) if 0 in endpoints
    )
    if len(incident) != 3:
        raise AssertionError("normalizing vertex is not cubic")
    first_cycles = tuple(
        cycle
        for cycle in cycles
        if cycle_pattern(cycle, incident) == (1, 0, 1)
    )
    second_cycles = tuple(
        cycle
        for cycle in cycles
        if cycle_pattern(cycle, incident) == (0, 1, 1)
    )
    third_cycles = tuple(
        cycle
        for cycle in cycles
        if cycle_pattern(cycle, incident) == (0, 0, 0)
    )

    totals: Counter[str] = Counter()
    merge_rank_profile: Counter[int] = Counter()
    first_failure: dict[str, Any] | None = None
    for first in first_cycles:
        for second in second_cycles:
            union = first | second
            for third in third_cycles:
                totals["coordinate_triples"] += 1
                if union | third != all_edges:
                    continue
                totals["normalized_nowhere_zero_flows"] += 1
                values = flow_values(
                    graph.edge_count, first, second, third
                )
                if not is_flow(graph, values):
                    raise AssertionError("coordinate cycles did not form a flow")
                first_outside = next(
                    (
                        value
                        for value in values
                        if value not in (1, 2, 3)
                    ),
                    None,
                )
                if first_outside is None:
                    # Values 1,2,3 give the explicit local triangle
                    # {0,1},{0,2},{1,2}; hence a merge exists without SAT.
                    totals["line_valued_automatic"] += 1
                    continue
                if first_outside != 4:
                    totals["stabilizer_noncanonical_flows"] += 1
                    continue
                totals["gl3_flow_orbit_representatives"] += 1

                # A good quotient line supplies a D5-flow q lifting this
                # fixed phi.  Write the quotient map as
                # L:E_5 -> F_2^3 and set a_5=0,
                # a_i=L(e_i+e_5).  Its weight-four kernel contains no
                # weight-two vector, so a_1,...,a_5 are distinct.  Label
                # each q-edge ij by {a_i,a_j}; assign the three unused
                # Fano points as second preimages of any three colors.
                # This is precisely a three-pair merge witness.
                quotient_lines = good_lines(graph, values)
                if quotient_lines:
                    totals["quotient_lift_automatic"] += 1
                    continue

                totals["all_quotient_lines_bad"] += 1
                direct = direct_potential_merge_audit(
                    graph.vertices,
                    graph.edges,
                    incidence,
                    values,
                    exhaustive=False,
                )
                totals["potential_solutions_examined"] += int(
                    direct["potential_solutions_examined"]
                )
                if direct["merge_exists"]:
                    totals["fixed_flow_merge_sat"] += 1
                    matching = tuple(
                        tuple(pair)
                        for pair in direct["first_witness"][
                            "forbidden_merge_pairs"
                        ]
                    )
                    merge_rank_profile[matching_rank(matching)] += 1
                    continue

                if not direct["exhaustive"]:
                    raise AssertionError(
                        "negative direct audit did not exhaust potentials"
                    )
                states = local_states(incidence, values)
                variables, clauses = build_joint_merge_cnf(
                    graph.vertices, graph.edges, incidence, states
                )
                satisfiable, model, _ = solve(cadical, variables, clauses)
                if not satisfiable:
                    totals["fixed_flow_merge_unsat"] += 1
                    first_failure = {
                        "graph6": graph6,
                        "vertices": graph.vertices,
                        "edges": [list(edge) for edge in graph.edges],
                        "coordinate_cycle_masks": [first, second, third],
                        "flow_values_by_edge": list(values),
                        "variables": variables,
                        "clauses": len(clauses),
                        "direct_potential_audit": direct,
                    }
                    if stop_on_failure:
                        return (
                            {
                                "graph6": graph6,
                                "vertices": graph.vertices,
                                "edges": graph.edge_count,
                                "cycle_space_size": len(cycles),
                                "totals": dict(totals),
                                "merge_difference_rank_profile": dict(
                                    merge_rank_profile
                                ),
                            },
                            first_failure,
                        )
                    continue

                raise AssertionError(
                    "direct exhaustive audit says UNSAT but joint SAT says SAT"
                )

    return (
        {
            "graph6": graph6,
            "vertices": graph.vertices,
            "edges": graph.edge_count,
            "cycle_space_size": len(cycles),
            "totals": dict(totals),
            "merge_difference_rank_profile": dict(merge_rank_profile),
        },
        first_failure,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph_report", type=Path)
    parser.add_argument("--cadical", default="cadical")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--maximum-order", type=int)
    parser.add_argument(
        "--no-stop-on-failure",
        action="store_true",
        help="continue after the first fixed-flow UNSAT instance",
    )
    arguments = parser.parse_args()

    source = json.loads(arguments.graph_report.read_text(encoding="utf-8"))
    graph6_rows = sorted(
        {
            str(row["graph6"])
            for row in source["graph_rows"]
            if arguments.maximum_order is None
            or int(row["order"]) <= arguments.maximum_order
        },
        key=lambda row: (graph_from_graph6(row).vertices, row),
    )
    started = time.monotonic()
    rows = []
    aggregate: Counter[str] = Counter()
    rank_profile: Counter[int] = Counter()
    first_failure = None
    for index, graph6 in enumerate(graph6_rows, 1):
        graph = graph_from_graph6(graph6)
        row, failure = audit_graph(
            graph6,
            graph,
            arguments.cadical,
            not arguments.no_stop_on_failure,
        )
        rows.append(row)
        aggregate.update(row["totals"])
        rank_profile.update(
            {
                int(rank): int(count)
                for rank, count in row[
                    "merge_difference_rank_profile"
                ].items()
            }
        )
        print(
            json.dumps(
                {
                    "graph": index,
                    "graphs": len(graph6_rows),
                    "order": graph.vertices,
                    "graph6": graph6,
                    "flow_orbits": row["totals"].get(
                        "gl3_flow_orbit_representatives", 0
                    ),
                    "sat": row["totals"].get("fixed_flow_merge_sat", 0),
                    "unsat": row["totals"].get("fixed_flow_merge_unsat", 0),
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if failure is not None and first_failure is None:
            first_failure = failure
            if not arguments.no_stop_on_failure:
                break

    report = {
        "schema": "fixed-fano-three-pair-merge-frontier-v1",
        "status": (
            "FIXED-FLOW COUNTERMODEL"
            if first_failure is not None
            else "FINITE PASS"
        ),
        "scope": {
            "graph_source": str(arguments.graph_report),
            "connected_simple_cubic_bridgeless": True,
            "flow_scope": "one representative per GL(3,2) orbit",
            "maximum_order": arguments.maximum_order,
            "claim": (
                "Every audited fixed flow has some Oum-compatible 8-CDC "
                "avoiding three disjoint coordinate pairs."
            ),
            "warning": "A finite PASS is not a universal proof or a 5-CDC resolution.",
        },
        "elapsed_seconds": time.monotonic() - started,
        "graph_rows": rows,
        "totals": dict(aggregate),
        "merge_difference_rank_profile": dict(rank_profile),
        "first_failure": first_failure,
    }
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(
        json.dumps(
            {
                "status": report["status"],
                "graphs": len(rows),
                "flow_orbits": aggregate[
                    "gl3_flow_orbit_representatives"
                ],
                "sat": aggregate["fixed_flow_merge_sat"],
                "unsat": aggregate["fixed_flow_merge_unsat"],
                "elapsed_seconds": report["elapsed_seconds"],
            },
            sort_keys=True,
        )
    )
    return 1 if first_failure is not None else 0


if __name__ == "__main__":
    raise SystemExit(main())
