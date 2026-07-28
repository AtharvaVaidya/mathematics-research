#!/usr/bin/env python3
"""Independent coverage verifier for the order-16 closure census.

The verifier does not solve any closure instance.  It independently
regenerates the canonical connected cubic graph stream with geng, decodes
every graph6 record, checks graph premises and row arithmetic, and verifies
the unique failure pointer and frozen digest.  The SAT producer remains in
the trust boundary for the 45,247 positive classifications.
"""

from __future__ import annotations

from collections import deque
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent.parent
REPORT = (
    ROOT
    / "output"
    / "jaeger-kernel-closure-frontier"
    / "stars-order16.jsonl"
)
EXPECTED_SHA256 = (
    "889d0e5857b62e082f3fcad0a929e7c0d92032a8e675f4d2ff9f40272ea43d46"
)
FAILURE_GRAPH6 = "O??CA?_ceOGgH_F?AK@P?"
FAILURE_ROOT = 13


def parse_short_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    order = ord(record[0]) - 63
    assert order == 16
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    cursor = 0
    edges = []
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def check_graph(record: str) -> None:
    order, edges = parse_short_graph6(record)
    assert order == 16 and len(edges) == 24
    rows: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        assert left < right
        rows[left].append(edge)
        rows[right].append(edge)
    assert all(len(row) == 3 for row in rows)
    seen = {0}
    queue = deque(seen)
    while queue:
        vertex = queue.popleft()
        for edge in rows[vertex]:
            left, right = edges[edge]
            other = right if left == vertex else left
            if other not in seen:
                seen.add(other)
                queue.append(other)
    assert len(seen) == order


def main() -> None:
    assert hashlib.sha256(REPORT.read_bytes()).hexdigest() == EXPECTED_SHA256
    rows = [
        json.loads(line)
        for line in REPORT.read_text(encoding="ascii").splitlines()
        if line
    ]
    summaries = [row for row in rows if "mode" in row]
    failures = [
        row for row in rows if row.get("status") == "CLOSURE_FAILURE"
    ]
    assert len(rows) == 4061
    assert len(summaries) == 4060
    assert failures == [
        {
            "status": "CLOSURE_FAILURE",
            "graph6": FAILURE_GRAPH6,
            "kind": "star",
            "defect_edges": [FAILURE_ROOT],
        }
    ]

    graph_records = [row["graph6"] for row in summaries]
    assert len(set(graph_records)) == len(graph_records)
    for row in summaries:
        assert row["vertices"] == 16
        assert row["mode"] == "stars"
        assert row["patterns"] == 16
        assert 0 <= row["closure_patterns"] <= row["feasible_patterns"] <= 16
        assert row["failures"] == (
            row["feasible_patterns"] - row["closure_patterns"]
        )
        assert row["connected_third_kernel_models"] >= 0
        check_graph(row["graph6"])

    assert sum(row["patterns"] for row in summaries) == 64960
    assert sum(row["feasible_patterns"] for row in summaries) == 45248
    assert sum(row["closure_patterns"] for row in summaries) == 45247
    assert sum(row["failures"] for row in summaries) == 1
    bad_summaries = [row for row in summaries if row["failures"]]
    assert len(bad_summaries) == 1
    assert bad_summaries[0]["graph6"] == FAILURE_GRAPH6
    assert bad_summaries[0]["failures"] == 1

    geng = Path("/opt/homebrew/bin/geng")
    generated = subprocess.run(
        [str(geng), "-q", "-c", "-d3", "-D3", "16"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.splitlines()
    assert generated == graph_records

    print("PASS")
    print(
        "canonical connected simple cubic order16 graphs=4060; "
        "roots=64960"
    )
    print(
        "feasible=45248; closure_good=45247; failures=1; "
        "unique failure graph/root verified"
    )
    print(
        "trust boundary=coverage and arithmetic independently checked; "
        "positive SAT classifications are producer claims"
    )


if __name__ == "__main__":
    main()
