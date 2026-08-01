#!/usr/bin/env python3
"""Focused semantic replay of the flexible one-switch order-18 report."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scratch.audit_fano_single_value_cleaning import (  # noqa: E402
    subgraph_cycle_basis,
)
from scratch.census_fano_flexible_one_switch_snarks import (  # noqa: E402
    all_cycles,
    good_line,
)
from tools.fixed_fano_cover_merge_audit import (  # noqa: E402
    direct_potential_merge_audit,
    graph_incidence,
)
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402
from tools.flow_switch_audit import is_flow  # noqa: E402


REPORT = ROOT / "scratch/fano-flexible-one-switch-strict-through18-20260728.json"
SOURCE = (
    ROOT / "search/order22-filter-census-20260725/strict-snarks-through18.g6"
)
EXPECTED_REPORT_SHA256 = (
    "353c0340139d00f353d5c87826a2c3edc162ff135c7c0215cc25b097e1ccff57"
)
EXPECTED_SOURCE_SHA256 = (
    "1ab58368ae481cba9dba0e79fe95a631b61bbeb48b266307e528a3022066b8b1"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assert digest(REPORT) == EXPECTED_REPORT_SHA256
    assert digest(SOURCE) == EXPECTED_SOURCE_SHA256
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["first_countermodel"] is None
    totals = report["totals"]
    assert totals["gl3_flow_orbit_representatives"] == 238_390
    assert totals["no_fixed_line_cleaning"] == 4_278
    assert totals["Oum_easy"] == 3_322
    assert totals["Oum_hard"] == 956
    assert totals["flexible_one_switch_success"] == 940
    assert totals["line_only_one_switch_countermodels"] == 16
    assert totals["post_switch_Oum_only_success"] == 16
    assert totals.get("disjunctive_one_switch_countermodels", 0) == 0

    retained = report["first_line_only_countermodel"]
    graph = graph_from_graph6(retained["graph6"])
    flow = tuple(retained["flow_values_by_edge"])
    incidence = graph_incidence(graph.vertices, graph.edges)
    assert is_flow(graph, flow)
    assert good_line(graph, flow) is None
    initial_Oum = direct_potential_merge_audit(
        graph.vertices,
        graph.edges,
        incidence,
        flow,
        exhaustive=True,
        criterion="five-color",
    )
    assert initial_Oum["five_color_merge_exists"] is False

    switches = 0
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
            switches += 1
            assert not (cycle & forbidden)
            switched = tuple(
                value ^ switch_value if (cycle >> edge) & 1 else value
                for edge, value in enumerate(flow)
            )
            assert good_line(graph, switched) is None
    assert switches == 537

    witness = retained["post_switch_Oum_witness"]
    switch_value = witness["switch_value"]
    cycle = witness["cycle_mask"]
    assert switch_value == 1 and cycle == 8_389_016
    assert not any(
        (cycle >> edge) & 1 and value == switch_value
        for edge, value in enumerate(flow)
    )
    switched = tuple(
        value ^ switch_value if (cycle >> edge) & 1 else value
        for edge, value in enumerate(flow)
    )
    assert list(switched) == witness["switched_flow"]
    assert good_line(graph, switched) is None
    repaired_Oum = direct_potential_merge_audit(
        graph.vertices,
        graph.edges,
        incidence,
        switched,
        exhaustive=True,
        criterion="five-color",
    )
    assert repaired_Oum["five_color_merge_exists"] is True

    print("PASS")
    print("238390 normalized flow orbits; 956 Oum-hard")
    print("940 clean-line switch successes")
    print("16 line-only exceptions; all 16 have a post-switch Oum merge")
    print("focused exception replay: 537/537 switches have no clean line")
    print("displayed Oum-only rescue verified")


if __name__ == "__main__":
    main()
