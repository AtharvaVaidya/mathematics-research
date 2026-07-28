#!/usr/bin/env python3
"""Audit terminal surface-chi plateaus in selected large Kempe orbits."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, deque
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRATCH = PROJECT_ROOT / "scratch"
for item in (str(PROJECT_ROOT), str(SCRATCH)):
    if item not in sys.path:
        sys.path.insert(0, item)

from audit_d5_disjoint_two_switch_no_go import (  # noqa: E402
    INITIAL as ORDER40_INITIAL,
)
from audit_d5_root_kempe_orbits import (  # noqa: E402
    PAIRS,
    active_mask,
    canonical,
    component_edge_masks,
    neighbours,
)
from audit_d5_surface_chi_plateaus_order12 import surface_chi  # noqa: E402
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402
from verify_d5_root_component_chain_order20 import (  # noqa: E402
    GRAPH6 as ORDER20_GRAPH6,
    LABEL_NAMES as ORDER20_LABEL_NAMES,
)


ORDER40_GRAPH6 = (
    "g????????????????????????????????GGGO?B?a@?A@A?EC??O_C??_?g?"
    "GO_?_g????BA???aG?C??S???E_??AG?O??CCA??SA????GW????H@?????"
    "GK???A?GC???"
)


def label_mask(name: str) -> int:
    return sum(1 << int(coordinate) for coordinate in name)


CASES = {
    "order20": (
        ORDER20_GRAPH6,
        tuple(label_mask(name) for name in ORDER20_LABEL_NAMES),
    ),
    "order40": (ORDER40_GRAPH6, ORDER40_INITIAL),
}


def component_pair_bits(component: int, edge_count: int) -> int:
    edges = []
    while component:
        edge = (component & -component).bit_length() - 1
        component &= component - 1
        edges.append(edge)
    answer = 0
    for first, second in itertools.combinations(edges, 2):
        before = first * (2 * edge_count - first - 1) // 2
        pair_index = before + second - first - 1
        answer |= 1 << pair_index
    return answer


def success_bits(graph, state) -> int:
    answer = 0
    for first, second in PAIRS:
        for component in component_edge_masks(
            graph,
            active_mask(state, first, second),
        ):
            answer |= component_pair_bits(component, graph.edge_count)
    return answer


def audit(case_name: str, maximum_states: int | None) -> dict[str, object]:
    graph6, supplied = CASES[case_name]
    graph = graph_from_graph6(graph6)
    initial = canonical(supplied)
    states = [initial]
    index = {initial: 0}
    adjacency: list[list[int]] = []
    for cursor, state in enumerate(states):
        row = []
        for other in sorted(set(neighbours(graph, state)) - {state}):
            position = index.get(other)
            if position is None:
                position = len(states)
                index[other] = position
                states.append(other)
                if maximum_states is not None and len(states) > maximum_states:
                    raise RuntimeError(
                        f"{case_name} exceeded state cap {maximum_states}"
                    )
            row.append(position)
        adjacency.append(row)
        if (cursor + 1) % 10_000 == 0:
            print(
                f"{case_name}: processed {cursor + 1}, "
                f"discovered {len(states)}",
                file=sys.stderr,
                flush=True,
            )

    chis = [surface_chi(graph, state) for state in states]
    unseen = set(range(len(states)))
    plateau_count = 0
    terminal_count = 0
    terminal_histogram: Counter[tuple[int, int]] = Counter()
    terminal_support_histogram: Counter[tuple[int, int]] = Counter()
    failures = []
    pair_count = graph.edge_count * (graph.edge_count - 1) // 2
    all_pairs = (1 << pair_count) - 1
    while unseen:
        start = next(iter(unseen))
        level = chis[start]
        plateau = {start}
        queue = deque([start])
        terminal = True
        while queue:
            current = queue.popleft()
            for other in adjacency[current]:
                if chis[other] > level:
                    terminal = False
                elif chis[other] == level and other not in plateau:
                    plateau.add(other)
                    queue.append(other)
        unseen.difference_update(plateau)
        plateau_count += 1
        if not terminal:
            continue
        terminal_count += 1
        terminal_histogram[(level, len(plateau))] += 1
        support_sizes = [
            len({
                coordinate
                for label in states[state]
                for coordinate in range(5)
                if (label >> coordinate) & 1
            })
            for state in plateau
        ]
        terminal_support_histogram[
            (min(support_sizes), max(support_sizes))
        ] += 1
        rescued = 0
        for state in plateau:
            rescued |= success_bits(graph, states[state])
            if rescued == all_pairs:
                break
        if rescued != all_pairs:
            missing = ((all_pairs ^ rescued) & -(all_pairs ^ rescued)).bit_length() - 1
            failures.append({
                "surface_chi": level,
                "plateau_size": len(plateau),
                "first_missing_pair_index": missing,
                "representative_state_labels_hex": [
                    f"{label:02x}" for label in states[start]
                ],
            })

    return {
        "schema": "d5-surface-chi-target-orbit-v1",
        "case": case_name,
        "graph6": graph6,
        "vertices": graph.vertices,
        "edges": graph.edge_count,
        "states_mod_global_s5": len(states),
        "surface_chi_range": [min(chis), max(chis)],
        "equal_surface_chi_plateaus": plateau_count,
        "terminal_surface_chi_plateaus": terminal_count,
        "terminal_plateau_histogram": [
            {"surface_chi": chi, "size": size, "count": count}
            for (chi, size), count in sorted(terminal_histogram.items())
        ],
        "terminal_plateau_coordinate_support_ranges": [
            {
                "minimum_used_coordinates": minimum,
                "maximum_used_coordinates": maximum,
                "count": count,
            }
            for (minimum, maximum), count
            in sorted(terminal_support_histogram.items())
        ],
        "terminal_plateau_failures": len(failures),
        "all_terminal_plateaus_root_universal": not failures,
        "first_failure": failures[0] if failures else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("case", choices=sorted(CASES))
    parser.add_argument("--maximum-states", type=int)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    report = audit(arguments.case, arguments.maximum_states)
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
