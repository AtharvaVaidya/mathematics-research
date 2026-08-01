#!/usr/bin/env python3
"""Independently check the complete order-14 D5 Kempe-orbit report.

The report producer is a C++ implementation.  This verifier:

* regenerates the complete nauty ``geng -C -d3 -D3 14`` input and checks
  graph6 identity and order, byte for byte;
* replays all report-level arithmetic and the asserted zero-failure result;
* selects deterministic extremal/control rows and recomputes their D5 flows,
  Kempe orbits, and root-pair coverage with the separately written Python
  implementation in ``audit_d5_root_kempe_orbits.py``.

The focused semantic replay is intentionally not a second full 480-graph
census.  Its scope is printed in the PASS record.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from audit_d5_root_kempe_orbits import audit_graph


ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "scratch/d5-root-kempe-all-biconnected-cubic-order14.jsonl"
GENG = Path("/opt/homebrew/bin/geng")


def load_report() -> tuple[list[dict[str, object]], dict[str, object]]:
    records = [
        json.loads(line)
        for line in REPORT.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert records
    assert records[-1]["status"] == "SUMMARY"
    rows = records[:-1]
    assert all(row["status"] == "GRAPH_DONE" for row in rows)
    return rows, records[-1]


def generate_graphs() -> list[str]:
    completed = subprocess.run(
        [str(GENG), "-Cq", "-d3", "-D3", "14"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
        encoding="ascii",
    )
    return [line for line in completed.stdout.splitlines() if line]


def main() -> None:
    rows, summary = load_report()
    generated = generate_graphs()
    reported = [str(row["graph6"]) for row in rows]
    assert reported == generated
    assert len(rows) == 480
    assert [row["index"] for row in rows] == list(range(1, len(rows) + 1))
    assert all(row["vertices"] == 14 and row["edges"] == 21 for row in rows)
    assert all(row["failed_orbits"] == 0 for row in rows)
    assert all(row["first_failure"] is None for row in rows)

    sums = {
        "graphs": len(rows),
        "flows_mod_s5": sum(int(row["flows_mod_s5"]) for row in rows),
        "kempe_orbits_mod_s5": sum(
            int(row["kempe_orbits_mod_s5"]) for row in rows
        ),
        "orbit_root_pair_tests": sum(
            int(row["orbit_root_pair_tests"]) for row in rows
        ),
        "failed_orbits": sum(int(row["failed_orbits"]) for row in rows),
    }
    assert sums == {
        key: summary[key]
        for key in (
            "graphs",
            "flows_mod_s5",
            "kempe_orbits_mod_s5",
            "orbit_root_pair_tests",
            "failed_orbits",
        )
    }
    assert sums == {
        "graphs": 480,
        "flows_mod_s5": 537_418,
        "kempe_orbits_mod_s5": 33_102,
        "orbit_root_pair_tests": 6_951_420,
        "failed_orbits": 0,
    }
    assert all(
        int(row["orbit_root_pair_tests"])
        == 210 * int(row["kempe_orbits_mod_s5"])
        for row in rows
    )

    selected_indices = {
        0,
        len(rows) - 1,
        min(range(len(rows)), key=lambda i: int(rows[i]["flows_mod_s5"])),
        max(range(len(rows)), key=lambda i: int(rows[i]["flows_mod_s5"])),
        max(range(len(rows)), key=lambda i: int(rows[i]["kempe_orbits_mod_s5"])),
        max(range(len(rows)), key=lambda i: int(rows[i]["maximum_orbit"])),
    }
    semantic_rows = []
    for index in sorted(selected_indices):
        row = rows[index]
        replay = audit_graph(str(row["graph6"]))
        assert replay["graph6"] == row["graph6"]
        assert replay["vertices"] == row["vertices"]
        assert replay["edges"] == row["edges"]
        assert replay["d5_flows_mod_global_s5"] == row["flows_mod_s5"]
        assert replay["kempe_orbits_mod_global_s5"] == row["kempe_orbits_mod_s5"]
        assert replay["all_orbits_rescue_all_root_pairs"]
        assert replay["first_failure"] is None
        assert max(
            orbit["states_mod_global_s5"] for orbit in replay["orbit_summaries"]
        ) == row["maximum_orbit"]
        semantic_rows.append(
            {
                "index": index + 1,
                "graph6": row["graph6"],
                "flows_mod_s5": row["flows_mod_s5"],
                "kempe_orbits_mod_s5": row["kempe_orbits_mod_s5"],
                "maximum_orbit": row["maximum_orbit"],
            }
        )

    print(
        json.dumps(
            {
                "status": "PASS",
                "report": str(REPORT.relative_to(ROOT)),
                "complete_structural_rows": len(rows),
                "complete_orbit_root_pair_tests": sums[
                    "orbit_root_pair_tests"
                ],
                "focused_independent_semantic_replays": semantic_rows,
                "scope": (
                    "All 480 report rows are regenerated and arithmetically "
                    "checked; the separately written Python semantics are "
                    "replayed on deterministic boundary/extremal rows."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
