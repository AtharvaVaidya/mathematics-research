#!/usr/bin/env python3
"""Independent structural verifier for the six-point frontier report."""

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
    / "jaeger-six-point-fibres-through14"
    / "census.jsonl"
)
EXPECTED_REPORT_SHA256 = (
    "9bfa6ba83f22a6b2013699a817662ce3e6d57734f86d332c23463bfa8b02cfd6"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def prior_graphs() -> set[str]:
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


def graph(code: str) -> nx.Graph:
    result = nx.from_graph6_bytes(code.encode("ascii"))
    assert not result.is_multigraph()
    assert nx.is_connected(result)
    assert all(degree == 3 for _, degree in result.degree())
    assert nx.edge_connectivity(result) >= 2
    return result


def main() -> None:
    assert digest(REPORT) == EXPECTED_REPORT_SHA256
    report = rows(REPORT)
    summary = report.pop()
    prior = prior_graphs()
    assert len(report) == 587
    assert {str(row["graph6"]) for row in report} == prior
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
            row["six_point_good_fibres"]
        )
        g = graph(str(row["graph6"]))
        edge_count = g.number_of_edges()
        assert int(row["patterns"]) == (
            math.comb(edge_count, 3) + edge_count * (edge_count - 1)
        )
        if nx.edge_connectivity(g) >= 3:
            assert int(row["feasible_fibres"]) == int(row["patterns"])

    assert summary["status"] == "SUMMARY"
    assert summary["classification"] == "VERIFIED FINITE CASE"
    assert int(summary["graphs"]) == 587
    assert int(summary["patterns"]) == 944_974
    assert int(summary["feasible_fibres"]) == 804_204
    assert int(summary["six_point_good_fibres"]) == 804_204
    assert int(summary["failures"]) == 0
    assert int(summary["patterns"]) == sum(
        int(row["patterns"]) for row in report
    )
    assert int(summary["feasible_fibres"]) == sum(
        int(row["feasible_fibres"]) for row in report
    )
    assert int(summary["six_point_good_fibres"]) == sum(
        int(row["six_point_good_fibres"]) for row in report
    )
    assert summary["by_order"] == [
        {
            "vertices": 4,
            "graphs": 1,
            "patterns": 50,
            "feasible_fibres": 50,
            "six_point_good_fibres": 50,
        },
        {
            "vertices": 6,
            "graphs": 2,
            "patterns": 312,
            "feasible_fibres": 312,
            "six_point_good_fibres": 312,
        },
        {
            "vertices": 8,
            "graphs": 5,
            "patterns": 1_760,
            "feasible_fibres": 1_608,
            "six_point_good_fibres": 1_608,
        },
        {
            "vertices": 10,
            "graphs": 18,
            "patterns": 11_970,
            "feasible_fibres": 10_725,
            "six_point_good_fibres": 10_725,
        },
        {
            "vertices": 12,
            "graphs": 81,
            "patterns": 90_882,
            "feasible_fibres": 77_508,
            "six_point_good_fibres": 77_508,
        },
        {
            "vertices": 14,
            "graphs": 480,
            "patterns": 840_000,
            "feasible_fibres": 714_001,
            "six_point_good_fibres": 714_001,
        },
    ]
    source = ROOT / str(summary["producer_source"])
    assert digest(source) == summary["producer_sha256"]
    for relative, expected in summary["included_source_sha256"].items():
        assert digest(ROOT / relative) == expected
    print(
        "PASS: 587 simple bridgeless cubic graphs; 944974 Type A/B "
        "patterns; all 804204 feasible fibres have a checked good "
        "representative supported on at most six Oum points."
    )


if __name__ == "__main__":
    main()
