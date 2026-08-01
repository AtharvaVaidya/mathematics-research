#!/usr/bin/env python3
"""Independent structural and semantic checks for the order-14 report."""

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

from audit_d5_root_component_chain_potential import audit  # noqa: E402


REPORT = SCRATCH / "d5-root-component-chain-all-biconnected-cubic-order14.jsonl"
GENG = "/opt/homebrew/bin/geng"


def main() -> None:
    rows = [
        json.loads(line)
        for line in REPORT.read_text(encoding="utf-8").splitlines()
        if line
    ]
    graph_rows = rows[:-1]
    summary = rows[-1]
    generated = subprocess.run(
        [GENG, "-Cq", "-d3", "-D3", "14"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    assert len(graph_rows) == len(generated) == 480
    assert [row["graph6"] for row in graph_rows] == generated
    assert all(row["index"] == index for index, row in enumerate(graph_rows, 1))
    assert all(row["vertices"] == 14 and row["edges"] == 21 for row in graph_rows)
    assert all(not row["failure"] and row["first_failure"] is None for row in graph_rows)

    assert summary == {
        "status": "SUMMARY",
        "graphs": 480,
        "flows_mod_s5": 537_418,
        "state_root_pair_tests": 112_857_780,
        "plateaus_checked": 951_298,
        "maximum_distance": 3,
        "failures": 0,
    }
    assert sum(row["flows_mod_s5"] for row in graph_rows) == summary["flows_mod_s5"]
    assert (
        sum(row["state_root_pair_tests"] for row in graph_rows)
        == summary["state_root_pair_tests"]
    )
    assert (
        sum(row["plateaus_checked"] for row in graph_rows)
        == summary["plateaus_checked"]
    )
    assert max(row["maximum_distance"] for row in graph_rows) == 3

    # The Python audit treats (r,s) and (s,r) as distinct; the C++ report
    # uses unordered root pairs.  These independently implemented counts
    # must therefore differ by exactly a factor of two.
    for index in (0, 5, 239, 477, 479):
        replay = audit(graph_rows[index]["graph6"])
        assert replay["states_mod_s5"] == graph_rows[index]["flows_mod_s5"]
        assert replay["plateaus_checked"] == 2 * graph_rows[index]["plateaus_checked"]
        assert replay["nonincreasing_chain_distance"]
        assert replay["first_failure"] is None

    print(
        "PASS: 480 identities, arithmetic totals, zero-failure fields, "
        "and five independent Python semantic replays"
    )


if __name__ == "__main__":
    main()
