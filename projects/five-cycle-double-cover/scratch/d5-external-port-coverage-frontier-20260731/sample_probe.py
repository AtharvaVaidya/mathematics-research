#!/usr/bin/env python3
"""Replay the deterministic order-40 and Petersen--Foster samples."""

from __future__ import annotations

import argparse
from pathlib import Path
import random

from probe import RT, solve_external


PROJECT = Path(__file__).resolve().parents[2]
ORDER40 = (PROJECT / "search" / "strong_snarks" / "source" /
           "strongsnarks_40_5_cyc4.g6")
SEED = 20260731
EXPECTED_ROWS = (
    131, 192, 203, 498, 732, 915, 1105, 1263, 1440, 1463,
    1866, 1948, 1992, 2013, 2070, 2138, 2190, 2199, 2295, 2629,
    2901, 3109, 3424, 3638, 3860, 4319, 4357, 4425, 4617, 4660,
    4746, 4886, 4957, 5315, 5420, 5477, 5639, 5666, 5811, 6094,
    6350, 6601, 6634, 7207, 7333, 7448, 7540, 7543, 7567, 7649,
)
EXPECTED_PF = (
    (26, 74, 49), (294, 772, 453), (727, 135, 1100),
    (250, 34, 383), (592, 777, 901), (258, 478, 345),
    (117, 643, 158), (495, 495, 754), (162, 197, 252),
    (372, 430, 568),
)


def eligible(graph):
    incident = RT.incidence(graph)
    answer = []
    for z in range(graph.n):
        for root, root_ends in enumerate(graph.edges):
            if z in root_ends:
                continue
            for port in incident[z]:
                if set(root_ends).isdisjoint(graph.edges[port]):
                    answer.append((z, root, port))
    return answer


def order40(cadical: Path) -> None:
    rows = [row for row in ORDER40.read_bytes().splitlines() if row.strip()]
    rng = random.Random(SEED)
    chosen_rows = tuple(sorted(rng.sample(range(len(rows)), 50)))
    assert chosen_rows == EXPECTED_ROWS
    queries = 0
    for graph_index in chosen_rows:
        graph = RT.graph6_file(ORDER40, graph_index)
        for z, root, port in rng.sample(eligible(graph), 20):
            status, _ = solve_external(graph, z, root, port, cadical)
            assert status == "SAT_MODEL_CHECKED_EXTERNAL"
            queries += 1
    assert queries == 1000
    print("ORDER40 sampled_graphs=50 independent_sat=1000 PASS")


def petersen_foster(cadical: Path) -> None:
    graph = RT.petersen_foster_graph()
    assert RT.graph_digest(graph) == (
        "3fe0630cb52d5a0b29a473faff02389195c7e119ea8f7a6f95f3ba9c38272282")
    chosen = tuple(random.Random(SEED).sample(eligible(graph), 10))
    assert chosen == EXPECTED_PF
    for z, root, port in chosen:
        status, _ = solve_external(graph, z, root, port, cadical)
        assert status == "SAT_MODEL_CHECKED_EXTERNAL"
    print("PETERSEN_FOSTER sampled_interfaces=10 independent_sat=10 PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order40", action="store_true")
    parser.add_argument("--petersen-foster", action="store_true")
    parser.add_argument("--cadical", type=Path,
                        default=Path("/opt/homebrew/bin/cadical"))
    args = parser.parse_args()
    assert args.order40 or args.petersen_foster
    if args.order40:
        order40(args.cadical)
    if args.petersen_foster:
        petersen_foster(args.cadical)
    print("PASS")


if __name__ == "__main__":
    main()
