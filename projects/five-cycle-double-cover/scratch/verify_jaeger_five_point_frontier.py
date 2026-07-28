#!/usr/bin/env python3
"""Independent structural verifier for the five-point frontier report."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import math
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parent.parent
PRIOR = ROOT / "output" / "jaeger-two-tree-exchange-through14"
REPORT = (
    ROOT
    / "output"
    / "jaeger-five-point-fibres-through14"
    / "census.jsonl"
)
EXPECTED_REPORT_SHA256 = (
    "482e2ee028aa1663f2b91b71569422ab59c1033d51601ca52fac581b173872f1"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_rows(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def canonical_graphs() -> set[str]:
    answer: set[str] = set()
    paths = [PRIOR / "census.jsonl"] + [
        PRIOR / f"order14-shard-{index}.jsonl" for index in range(8)
    ]
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("status") == "GRAPH_DONE":
                answer.add(str(row["graph6"]))
    assert len(answer) == 587
    return answer


def checked_graph(code: str) -> nx.Graph:
    graph = nx.from_graph6_bytes(code.encode("ascii"))
    assert not graph.is_multigraph()
    assert nx.is_connected(graph)
    assert all(degree == 3 for _, degree in graph.degree())
    assert nx.edge_connectivity(graph) >= 2
    return graph


def main() -> None:
    assert digest(REPORT) == EXPECTED_REPORT_SHA256
    report = load_rows(REPORT)
    summary = report.pop()
    assert len(report) == 587
    assert {str(row["graph6"]) for row in report} == canonical_graphs()
    assert Counter(int(row["vertices"]) for row in report) == {
        4: 1,
        6: 2,
        8: 5,
        10: 18,
        12: 81,
        14: 480,
    }

    for row in report:
        assert row["status"] == "GRAPH_DONE"
        assert int(row["producer_exit_code"]) == 0
        assert int(row["failures"]) == 0
        assert int(row["feasible_fibres"]) == int(
            row["five_point_good_fibres"]
        )
        graph = checked_graph(str(row["graph6"]))
        edge_count = graph.number_of_edges()
        assert int(row["patterns"]) == (
            math.comb(edge_count, 3) + edge_count * (edge_count - 1)
        )
        if nx.edge_connectivity(graph) >= 3:
            assert int(row["feasible_fibres"]) == int(row["patterns"])

    assert summary["status"] == "SUMMARY"
    assert summary["classification"] == "VERIFIED FINITE CASE"
    assert int(summary["graphs"]) == 587
    assert int(summary["patterns"]) == 944_974
    assert int(summary["feasible_fibres"]) == 804_204
    assert int(summary["five_point_good_fibres"]) == 804_204
    assert int(summary["failures"]) == 0
    assert int(summary["patterns"]) == sum(
        int(row["patterns"]) for row in report
    )
    assert int(summary["feasible_fibres"]) == sum(
        int(row["feasible_fibres"]) for row in report
    )
    assert int(summary["five_point_good_fibres"]) == sum(
        int(row["five_point_good_fibres"]) for row in report
    )
    producer = ROOT / str(summary["producer_source"])
    assert digest(producer) == summary["producer_sha256"]
    for relative, expected in summary["included_source_sha256"].items():
        assert digest(ROOT / relative) == expected
    print(
        "PASS: 587 simple bridgeless cubic graphs; 944974 Type A/B "
        "patterns; all 804204 feasible fibres have a checked Oum "
        "representative supported on at most five points."
    )


if __name__ == "__main__":
    main()
