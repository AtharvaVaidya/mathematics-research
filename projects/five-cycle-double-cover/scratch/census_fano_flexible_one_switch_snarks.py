#!/usr/bin/env python3
"""Exact strict-snark census for flexible one-switch Fano cleaning.

For each normalized nowhere-zero F_2^3-flow, the script first applies the
already certified fixed-line cleaning test.  Only flows failing that test
need the Oum potential audit.  For every Oum-hard remainder, it exhausts
all nonzero t and every binary cycle in G-M_t, switches by t, and asks
whether any Fano line of the resulting flow has zero rainbow defect.

A zero-defect line lifts directly to a D_5-flow and hence a standard
five-cycle double cover.  Binary cycles may be disconnected; their circuit
components can be switched successively because the t-class stays fixed.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scratch.audit_fano_single_value_cleaning import (  # noqa: E402
    cleaning_pair_exists_fast,
    dot,
    kernel_line,
    subgraph_cycle_basis,
)
from tools.fano_value_class_tjoin_audit import flow_values  # noqa: E402
from tools.fixed_fano_cover_merge_audit import (  # noqa: E402
    direct_potential_merge_audit,
    graph_incidence,
)
from tools.fixed_fano_merge_frontier import (  # noqa: E402
    cycle_pattern,
    graph_from_graph6,
)
from tools.flow_switch_audit import connected_components  # noqa: E402
from tools.cycle_space_switch_audit import fundamental_cycle_space  # noqa: E402


def good_line(
    graph: Any, flow: tuple[int, ...]
) -> int | None:
    """Return a functional whose line factor has zero rainbow defect."""
    for mu in range(1, 8):
        line = kernel_line(mu)
        factor_edges = tuple(
            edge for edge, value in enumerate(flow) if value in line
        )
        components = connected_components(graph, factor_edges)
        owner = [0] * graph.vertices
        for index, component in enumerate(components):
            for vertex in component:
                owner[vertex] = index
        affine = tuple(value for value in range(1, 8) if dot(mu, value))
        base = min(affine)
        defect = 0
        for edge, (left, right) in enumerate(graph.edges):
            first, second = owner[left], owner[right]
            if first != second and flow[edge] == base:
                defect ^= (1 << first) ^ (1 << second)
        if defect == 0:
            return mu
    return None


def all_cycles(basis: tuple[int, ...]) -> tuple[int, ...]:
    cycles = [0]
    for vector in basis:
        cycles += [cycle ^ vector for cycle in cycles]
    return tuple(cycles)


def flexible_switch_witness(
    graph: Any, flow: tuple[int, ...]
) -> dict[str, Any] | None:
    assert good_line(graph, flow) is None
    for switch_value in range(1, 8):
        basis = subgraph_cycle_basis(
            graph,
            (
                edge
                for edge, value in enumerate(flow)
                if value != switch_value
            ),
        )
        forbidden = sum(
            1 << edge
            for edge, value in enumerate(flow)
            if value == switch_value
        )
        for cycle in all_cycles(basis):
            if cycle == 0:
                continue
            assert not (cycle & forbidden)
            switched = tuple(
                value ^ switch_value if (cycle >> edge) & 1 else value
                for edge, value in enumerate(flow)
            )
            assert all(switched)
            mu = good_line(graph, switched)
            if mu is not None:
                return {
                    "switch_value": switch_value,
                    "cycle_mask": cycle,
                    "clean_functional": mu,
                    "switched_flow": list(switched),
                }
    return None


def post_switch_Oum_witness(
    graph: Any,
    incidence: Any,
    flow: tuple[int, ...],
) -> dict[str, Any] | None:
    """Find a switch whose Oum coordinate graph is five-colourable."""
    for switch_value in range(1, 8):
        basis = subgraph_cycle_basis(
            graph,
            (
                edge
                for edge, value in enumerate(flow)
                if value != switch_value
            ),
        )
        for cycle in all_cycles(basis):
            if cycle == 0:
                continue
            switched = tuple(
                value ^ switch_value if (cycle >> edge) & 1 else value
                for edge, value in enumerate(flow)
            )
            oum = direct_potential_merge_audit(
                graph.vertices,
                graph.edges,
                incidence,
                switched,
                exhaustive=True,
                criterion="five-color",
            )
            if oum["five_color_merge_exists"]:
                return {
                    "switch_value": switch_value,
                    "cycle_mask": cycle,
                    "switched_flow": list(switched),
                    "Oum_potential_audit": oum,
                }
    return None


def audit_graph(graph6: str) -> tuple[dict[str, Any], dict[str, Any] | None]:
    graph = graph_from_graph6(graph6)
    cycles = fundamental_cycle_space(graph)
    all_edges = (1 << graph.edge_count) - 1
    incidence = graph_incidence(graph.vertices, graph.edges)
    incident = tuple(
        edge for edge, endpoints in enumerate(graph.edges) if 0 in endpoints
    )
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
    first_countermodel = None
    first_line_only_countermodel = None
    for first in first_cycles:
        for second in second_cycles:
            union = first | second
            for third in third_cycles:
                totals["coordinate_triples"] += 1
                if union | third != all_edges:
                    continue
                totals["normalized_nowhere_zero_flows"] += 1
                flow = flow_values(graph.edge_count, first, second, third)
                first_outside = next(
                    (value for value in flow if value not in (1, 2, 3)),
                    None,
                )
                if first_outside is None:
                    totals["line_valued_automatic_clean"] += 1
                    continue
                if first_outside != 4:
                    totals["stabilizer_noncanonical_flows"] += 1
                    continue
                totals["gl3_flow_orbit_representatives"] += 1

                # This test includes an already clean line and every
                # fixed-line switch by a value inside that line.
                if cleaning_pair_exists_fast(graph, flow):
                    totals["fixed_line_cleaning_success"] += 1
                    continue
                totals["no_fixed_line_cleaning"] += 1

                oum = direct_potential_merge_audit(
                    graph.vertices,
                    graph.edges,
                    incidence,
                    flow,
                    exhaustive=True,
                    criterion="five-color",
                )
                if oum["five_color_merge_exists"]:
                    totals["Oum_easy"] += 1
                    continue
                totals["Oum_hard"] += 1
                witness = flexible_switch_witness(graph, flow)
                if witness is not None:
                    totals["flexible_one_switch_success"] += 1
                    continue

                totals["line_only_one_switch_countermodels"] += 1
                Oum_witness = post_switch_Oum_witness(
                    graph, incidence, flow
                )
                if first_line_only_countermodel is None:
                    first_line_only_countermodel = {
                        "graph6": graph6,
                        "coordinate_cycle_masks": [first, second, third],
                        "flow_values_by_edge": list(flow),
                        "initial_Oum_potential_audit": oum,
                        "post_switch_Oum_witness": Oum_witness,
                    }
                if Oum_witness is not None:
                    totals["post_switch_Oum_only_success"] += 1
                    continue

                totals["disjunctive_one_switch_countermodels"] += 1
                if first_countermodel is None:
                    first_countermodel = {
                        "graph6": graph6,
                        "coordinate_cycle_masks": [first, second, third],
                        "flow_values_by_edge": list(flow),
                        "Oum_potential_audit": oum,
                    }

    return (
        {
            "graph6": graph6,
            "vertices": graph.vertices,
            "edges": graph.edge_count,
            "cycle_space_size": len(cycles),
            "totals": dict(totals),
            "first_line_only_countermodel": first_line_only_countermodel,
        },
        first_countermodel,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph6_file", type=Path)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    records = tuple(
        row.strip()
        for row in arguments.graph6_file.read_text(encoding="ascii").splitlines()
        if row.strip()
    )
    started = time.monotonic()
    rows = []
    totals: Counter[str] = Counter()
    first_countermodel = None
    for index, record in enumerate(records):
        row, countermodel = audit_graph(record)
        rows.append(row)
        totals.update(row["totals"])
        print(
            json.dumps(
                {"row": index, "rows": len(records), **row["totals"]},
                sort_keys=True,
            ),
            flush=True,
        )
        if first_countermodel is None and countermodel is not None:
            first_countermodel = countermodel
    report = {
        "schema": "fano-flexible-one-switch-strict-snark-census-v1",
        "scope": {
            "graph6_source": str(arguments.graph6_file),
            "flow_scope": "one representative per GL(3,2) orbit",
            "switch_scope": (
                "every nonzero t and every nonempty binary cycle in G-M_t"
            ),
            "claim_tested": (
                "every Oum-hard flow has a flexible one-switch good Fano line"
            ),
        },
        "elapsed_seconds": time.monotonic() - started,
        "graph_rows": rows,
        "totals": dict(totals),
        "first_countermodel": first_countermodel,
        "first_line_only_countermodel": next(
            (
                row["first_line_only_countermodel"]
                for row in rows
                if row["first_line_only_countermodel"] is not None
            ),
            None,
        ),
    }
    if arguments.output:
        arguments.output.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(report["totals"], sort_keys=True))
    return 1 if first_countermodel is not None else 0


if __name__ == "__main__":
    raise SystemExit(main())
