#!/usr/bin/env python3
"""Exact small-order census for the minimum-support exchange route.

For every canonical connected simple cubic graph of a requested order, this
program enumerates all F_2^2 flows as ordered pairs of binary cycle words.
It retains exact-zero sets that are matchings and tests two properties:

* whether the zero matching extends to two edge-disjoint T-joins; and
* if it does not, whether some matching-admissible constant-value circuit
  switch strictly decreases the number of zero edges.

The second test uses the exact switch identity

    Z(phi + c 1_X) = (M - X) union (X intersect E_c).

Flow signatures are quotiented only by the six automorphisms of F_2^2:
the unordered partition of nonzero edges into its three colour classes is
retained.  Graph isomorphism is handled by nauty ``geng``.

This is a finite diagnostic.  Absence of a row is not a universal proof.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from search.canonical.canonical_search import (  # noqa: E402
    exact_three_edge_coloring,
    validate_simple_cubic,
)
from tools.cycle_space_switch_audit import (  # noqa: E402
    canonical_cubic_graphs,
    fundamental_cycle_space,
)
from tools.flow_switch_audit import Graph  # noqa: E402


def is_matching(mask: int, graph: Graph) -> bool:
    occupied = 0
    for edge, (u, v) in enumerate(graph.edges):
        if not ((mask >> edge) & 1):
            continue
        endpoints = (1 << u) | (1 << v)
        if occupied & endpoints:
            return False
        occupied |= endpoints
    return True


def terminal_vertices(mask: int, graph: Graph) -> int:
    terminals = 0
    for edge, (u, v) in enumerate(graph.edges):
        if (mask >> edge) & 1:
            terminals |= (1 << u) | (1 << v)
    return terminals


def terminal_incident_edges(
    matching: int, terminals: int, graph: Graph
) -> int:
    required = 0
    for edge, (u, v) in enumerate(graph.edges):
        if (matching >> edge) & 1:
            continue
        if ((terminals >> u) & 1) or ((terminals >> v) & 1):
            required |= 1 << edge
    return required


def circuit_terminal_parity_even(
    cycle: int, terminals: int, graph: Graph
) -> bool:
    """Check that every nontrivial component has even terminal count."""
    adjacency: list[list[int]] = [[] for _ in range(graph.vertices)]
    active = 0
    for edge, (u, v) in enumerate(graph.edges):
        if not ((cycle >> edge) & 1):
            continue
        adjacency[u].append(v)
        adjacency[v].append(u)
        active |= (1 << u) | (1 << v)

    unseen = active
    while unseen:
        start_bit = unseen & -unseen
        start = start_bit.bit_length() - 1
        stack = [start]
        component = 0
        unseen ^= start_bit
        while stack:
            vertex = stack.pop()
            component |= 1 << vertex
            for neighbour in adjacency[vertex]:
                bit = 1 << neighbour
                if unseen & bit:
                    unseen ^= bit
                    stack.append(neighbour)
        if (component & terminals).bit_count() % 2:
            return False
    return True


def packs_two_t_joins(
    matching: int, cycles: tuple[int, ...], graph: Graph
) -> tuple[bool, int | None]:
    """Apply the exact even-marked circuit criterion."""
    terminals = terminal_vertices(matching, graph)
    required = terminal_incident_edges(matching, terminals, graph)
    for cycle in cycles:
        if cycle & matching:
            continue
        if required & ~cycle:
            continue
        if circuit_terminal_parity_even(cycle, terminals, graph):
            return True, cycle
    return False, None


def switched_zero_set(matching: int, cycle: int, colour: int) -> int:
    return (matching & ~cycle) | (cycle & colour)


def negative_admissible_switch(
    matching: int,
    colours: tuple[int, int, int],
    cycles: tuple[int, ...],
    graph: Graph,
) -> tuple[int, int, int] | None:
    """Return (colour index, cycle, new support), if one strictly descends."""
    old_size = matching.bit_count()
    for colour_index, colour in enumerate(colours, start=1):
        for cycle in cycles:
            if not cycle:
                continue
            new = switched_zero_set(matching, cycle, colour)
            if new.bit_count() >= old_size:
                continue
            if is_matching(new, graph):
                return colour_index, cycle, new
    return None


def mask_edges(mask: int) -> list[int]:
    return [edge for edge in range(mask.bit_length()) if (mask >> edge) & 1]


def graph_profile(
    index: int, graph6: str, graph: Graph
) -> dict[str, object]:
    cycles = fundamental_cycle_space(graph)
    all_edges = (1 << graph.edge_count) - 1
    signatures: dict[tuple[int, tuple[int, int, int]], tuple[int, int]] = {}

    for first in cycles:
        for second in cycles:
            zero = all_edges ^ (first | second)
            if not is_matching(zero, graph):
                continue
            colour_one = first & ~second
            colour_two = second & ~first
            colour_three = first & second
            colours = tuple(sorted((colour_one, colour_two, colour_three)))
            signatures.setdefault((zero, colours), (first, second))

    support_packing: dict[int, tuple[bool, int | None]] = {}
    support_sizes: Counter[int] = Counter()
    for zero, _ in signatures:
        support_sizes[zero.bit_count()] += 1
        support_packing.setdefault(
            zero, packs_two_t_joins(zero, cycles, graph)
        )

    minimum = min(zero.bit_count() for zero, _ in signatures)
    minimum_supports = {
        zero for zero, _ in signatures if zero.bit_count() == minimum
    }
    nonpacking_supports = {
        zero for zero, (packs, _) in support_packing.items() if not packs
    }

    local_nonpacking = 0
    negative_nonpacking = 0
    first_local: dict[str, object] | None = None
    first_negative: dict[str, object] | None = None
    for (zero, colours), (first, second) in signatures.items():
        if zero not in nonpacking_supports:
            continue
        descent = negative_admissible_switch(
            zero, colours, cycles, graph
        )
        if descent is None:
            local_nonpacking += 1
            if first_local is None:
                first_local = {
                    "support": mask_edges(zero),
                    "support_size": zero.bit_count(),
                    "flow_bits": [first, second],
                    "colour_masks": list(colours),
                }
        else:
            negative_nonpacking += 1
            if first_negative is None:
                colour_index, cycle, new = descent
                first_negative = {
                    "support": mask_edges(zero),
                    "support_size": zero.bit_count(),
                    "flow_bits": [first, second],
                    "switch_colour_class": colour_index,
                    "switch_cycle": mask_edges(cycle),
                    "new_support": mask_edges(new),
                }

    return {
        "index": index,
        "graph6": graph6,
        "cycle_space_size": len(cycles),
        "flow_signatures_mod_gl22": len(signatures),
        "support_size_profile_over_signatures": {
            str(size): count for size, count in sorted(support_sizes.items())
        },
        "distinct_supports": len(support_packing),
        "minimum_support_size": minimum,
        "minimum_supports": len(minimum_supports),
        "minimum_nonpacking_supports": len(
            minimum_supports & nonpacking_supports
        ),
        "nonpacking_supports": len(nonpacking_supports),
        "nonpacking_flow_signatures_with_negative_switch": negative_nonpacking,
        "nonpacking_flow_signatures_switch_local_minimum": local_nonpacking,
        "first_negative_nonpacking": first_negative,
        "first_local_nonpacking": first_local,
    }


def census(order: int, geng: str) -> dict[str, object]:
    totals: Counter[str] = Counter()
    minimum_profile: Counter[int] = Counter()
    rows: list[dict[str, object]] = []
    first_local: dict[str, object] | None = None
    first_global: dict[str, object] | None = None

    for index, graph6, simple in canonical_cubic_graphs(
        geng, order, PROJECT_ROOT
    ):
        totals["generated"] += 1
        premise = validate_simple_cubic(simple)
        if not premise["bridgeless"]:
            totals["nonbridgeless"] += 1
            continue
        totals["bridgeless"] += 1
        if exact_three_edge_coloring(simple).colorable:
            totals["three_edge_colourable"] += 1
            continue
        totals["hard"] += 1
        graph = Graph(simple.vertices, simple.edges)
        row = graph_profile(index, graph6, graph)
        rows.append(row)
        minimum_profile[int(row["minimum_support_size"])] += 1
        totals["flow_signatures_mod_gl22"] += int(
            row["flow_signatures_mod_gl22"]
        )
        totals["distinct_supports"] += int(row["distinct_supports"])
        totals["nonpacking_supports"] += int(row["nonpacking_supports"])
        totals["minimum_nonpacking_supports"] += int(
            row["minimum_nonpacking_supports"]
        )
        totals["nonpacking_negative_signatures"] += int(
            row["nonpacking_flow_signatures_with_negative_switch"]
        )
        totals["nonpacking_local_minimum_signatures"] += int(
            row["nonpacking_flow_signatures_switch_local_minimum"]
        )
        if first_local is None and row["first_local_nonpacking"] is not None:
            first_local = {
                "graph6": graph6,
                **dict(row["first_local_nonpacking"]),
            }
        if (
            first_global is None
            and int(row["minimum_nonpacking_supports"]) > 0
        ):
            first_global = {
                "graph6": graph6,
                "minimum_support_size": row["minimum_support_size"],
            }

    return {
        "schema": "minimum-exchange-local-census-v1",
        "status": "EXACT_FINITE_CENSUS",
        "order": order,
        "scope": "canonical connected simple cubic graphs",
        "universal_claim": False,
        "totals": dict(sorted(totals.items())),
        "minimum_support_size_profile": {
            str(size): count for size, count in sorted(minimum_profile.items())
        },
        "first_switch_local_nonpacking_flow": first_local,
        "first_minimum_nonpacking_support": first_global,
        "hard_rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--geng", default="geng")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = census(args.order, args.geng)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")
        print(
            json.dumps(
                {
                    "status": report["status"],
                    "order": report["order"],
                    "totals": report["totals"],
                    "first_switch_local_nonpacking_flow": report[
                        "first_switch_local_nonpacking_flow"
                    ],
                },
                indent=2,
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
