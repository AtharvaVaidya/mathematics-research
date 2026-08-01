#!/usr/bin/env python3
"""Structural verifier for the terminal-chi/chain order-14 report."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


REPORT = Path(__file__).with_name(
    "d5-terminal-chi-chain-lex-order14.jsonl"
)
EXPECTED_SHA256 = (
    "752a1f591c5ac9f5d21bc34f0e7ed82786bbff28f61ab296b46675a92cd87d3c"
)


def main() -> int:
    raw = REPORT.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
    records = [
        row
        for row in subprocess.run(
            ["/opt/homebrew/bin/geng", "-Cq", "-d3", "-D3", "14"],
            check=True,
            stdout=subprocess.PIPE,
            text=True,
            encoding="ascii",
        ).stdout.splitlines()
        if row
    ]
    rows = [
        json.loads(line)
        for line in raw.decode("utf-8").splitlines()
        if line
    ]
    graph_rows = rows[:-1]
    summary = rows[-1]
    assert len(records) == len(graph_rows) == 480
    for index, (record, row) in enumerate(
        zip(records, graph_rows), start=1
    ):
        assert row["status"] == "GRAPH_DONE"
        assert row["index"] == index
        assert row["graph6"] == record
        assert row["vertices"] == 14
        assert row["maximum_distance"] <= 3
        assert row["lex_failures"] == 0
        assert row["first_failure"] is None
    assert summary == {
        "status": "SUMMARY",
        "graphs": 480,
        "flows_mod_s5": 537418,
        "terminal_chi_plateaus": 33598,
        "terminal_chi_distance_plateaus": 642167,
        "maximum_distance": 3,
        "lex_failures": 0,
    }
    assert summary["flows_mod_s5"] == sum(
        row["flows_mod_s5"] for row in graph_rows
    )
    assert summary["terminal_chi_plateaus"] == sum(
        row["terminal_chi_plateaus"] for row in graph_rows
    )
    assert summary["terminal_chi_distance_plateaus"] == sum(
        row["terminal_chi_distance_plateaus"] for row in graph_rows
    )
    print("PASS")
    print(f"report sha256: {EXPECTED_SHA256}")
    print("graphs: 480")
    print("terminal chi plateaus: 33598")
    print("fixed-distance subplateaus: 642167")
    print("lex failures: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
