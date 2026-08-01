#!/usr/bin/env python3
"""Run the external-port SAT probe on every eligible rooted interface."""

from __future__ import annotations

import argparse
from pathlib import Path

from probe import RT, solve_external


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph6", type=Path)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--cadical", type=Path,
                        default=Path("/opt/homebrew/bin/cadical"))
    args = parser.parse_args()

    rows = [row for row in args.graph6.read_bytes().splitlines() if row.strip()]
    stop = len(rows) if args.limit is None else min(len(rows), args.start + args.limit)
    assert 0 <= args.start < stop <= len(rows)
    total_independent = 0
    total_adjacent = 0
    for graph_index in range(args.start, stop):
        graph = RT.graph6_file(args.graph6, graph_index)
        incident = RT.incidence(graph)
        independent = 0
        adjacent = 0
        for z in range(graph.n):
            for root, root_ends in enumerate(graph.edges):
                if z in root_ends:
                    continue
                for port in incident[z]:
                    if not set(root_ends).isdisjoint(graph.edges[port]):
                        adjacent += 1
                        continue
                    status, _ = solve_external(
                        graph, z, root, port, args.cadical)
                    assert status == "SAT_MODEL_CHECKED_EXTERNAL", (
                        graph_index, z, root, port, status)
                    independent += 1
        print(
            f"graph={graph_index} order={graph.n} "
            f"independent_sat={independent} adjacent_by_lemma={adjacent}",
            flush=True,
        )
        total_independent += independent
        total_adjacent += adjacent
    print(
        f"PASS graphs={stop - args.start} independent_sat={total_independent} "
        f"adjacent_by_lemma={total_adjacent}"
    )


if __name__ == "__main__":
    main()
