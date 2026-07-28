#!/usr/bin/env python3
"""Independent structural and semantic checks for the chi-max reports."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRATCH = PROJECT_ROOT / "scratch"
for item in (str(PROJECT_ROOT), str(SCRATCH)):
    if item not in sys.path:
        sys.path.insert(0, item)

from audit_d5_root_euler_potential import audit  # noqa: E402


GENG = "/opt/homebrew/bin/geng"
CASES = {
    12: {
        "graphs": 81,
        "flows_mod_s5": 25_960,
        "kempe_orbits_mod_s5": 2_650,
        "maximum_chi_components_in_one_orbit": 2,
        "replays": (0, 6, 40, 79, 80),
    },
    14: {
        "graphs": 480,
        "flows_mod_s5": 537_418,
        "kempe_orbits_mod_s5": 33_102,
        "maximum_chi_components_in_one_orbit": 12,
        "replays": (0, 17, 252, 477, 479),
    },
}


def check(order: int) -> None:
    report = (
        SCRATCH
        / f"d5-root-euler-chi-max-all-biconnected-cubic-order{order}.jsonl"
    )
    rows = [
        json.loads(line)
        for line in report.read_text(encoding="utf-8").splitlines()
        if line
    ]
    graph_rows = rows[:-1]
    summary = rows[-1]
    expected = CASES[order]
    generated = subprocess.run(
        [GENG, "-Cq", "-d3", "-D3", str(order)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()

    assert len(graph_rows) == len(generated) == expected["graphs"]
    assert [row["graph6"] for row in graph_rows] == generated
    assert all(
        row["index"] == index
        for index, row in enumerate(graph_rows, 1)
    )
    assert all(
        row["vertices"] == order and row["edges"] == 3 * order // 2
        for row in graph_rows
    )
    assert all(
        row["chi_maximum_union_failures"] == 0
        and row["chi_maximum_component_failures"] == 0
        and row["first_failure"] is None
        for row in graph_rows
    )

    assert summary == {
        "status": "SUMMARY",
        "graphs": expected["graphs"],
        "flows_mod_s5": expected["flows_mod_s5"],
        "kempe_orbits_mod_s5": expected["kempe_orbits_mod_s5"],
        "maximum_chi_components_in_one_orbit":
            expected["maximum_chi_components_in_one_orbit"],
        "chi_maximum_union_failures": 0,
        "chi_maximum_component_failures": 0,
    }
    assert (
        sum(row["flows_mod_s5"] for row in graph_rows)
        == summary["flows_mod_s5"]
    )
    assert (
        sum(row["kempe_orbits_mod_s5"] for row in graph_rows)
        == summary["kempe_orbits_mod_s5"]
    )
    assert (
        max(
            row["maximum_chi_components_in_one_orbit"]
            for row in graph_rows
        )
        == summary["maximum_chi_components_in_one_orbit"]
    )

    for index in expected["replays"]:
        row = graph_rows[index]
        replay = audit(row["graph6"])
        assert replay["states_mod_s5"] == row["flows_mod_s5"]
        assert (
            replay["kempe_orbits_mod_s5"]
            == row["kempe_orbits_mod_s5"]
        )
        assert replay["chi_range"] == row["chi_range"]
        assert (
            replay["maximum_chi_components_in_one_orbit"]
            == row["maximum_chi_components_in_one_orbit"]
        )
        assert (
            replay[
                "orbits_whose_chi_maximum_union_misses_a_root_pair"
            ]
            == row["chi_maximum_union_failures"]
            == 0
        )
        assert (
            replay["chi_maximum_components_missing_a_root_pair"]
            == row["chi_maximum_component_failures"]
            == 0
        )
        assert replay["first_failure"] is None


def main() -> None:
    for order in CASES:
        check(order)
    print(
        "PASS: generator identities, arithmetic totals, zero-failure "
        "fields, and ten independent Python semantic replays for the "
        "complete order-12 and order-14 reports"
    )


if __name__ == "__main__":
    main()
