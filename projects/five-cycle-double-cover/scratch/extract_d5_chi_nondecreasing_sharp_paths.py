#!/usr/bin/env python3
"""Extract shortest nondecreasing-chi rescues for two sharp D5 states."""

from __future__ import annotations

import json
import sys
from collections import deque
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRATCH = PROJECT_ROOT / "scratch"
for item in (str(PROJECT_ROOT), str(SCRATCH)):
    if item not in sys.path:
        sys.path.insert(0, item)

from audit_d5_root_euler_potential import euler_characteristic  # noqa: E402
from audit_d5_root_kempe_orbits import (  # noqa: E402
    PAIRS,
    active_mask,
    canonical,
    component_edge_masks,
    transpose_label,
)
from extract_d5_component_chain_depth2_witness import (  # noqa: E402
    GRAPH6 as DEPTH2_GRAPH6,
    INITIAL as DEPTH2_INITIAL,
    ROOTS as DEPTH2_ROOTS,
)
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402
from verify_d5_root_plateau_counterexample import (  # noqa: E402
    INITIAL as ONE_SWITCH_INITIAL,
    ROOT as ONE_SWITCH_ROOT,
    TARGET as ONE_SWITCH_TARGET,
)


CASES = (
    {
        "name": "one-switch chain-distance no-go",
        "graph6": "M??CBAPsAWBOH_J??",
        "roots": (ONE_SWITCH_ROOT, ONE_SWITCH_TARGET),
        "initial": ONE_SWITCH_INITIAL,
    },
    {
        "name": "two-neutral-chain-move witness",
        "graph6": DEPTH2_GRAPH6,
        "roots": DEPTH2_ROOTS,
        "initial": DEPTH2_INITIAL,
    },
)


def coordinate_component_count(graph, state, coordinate: int) -> int:
    mask = sum(
        1 << edge
        for edge, label in enumerate(state)
        if (label >> coordinate) & 1
    )
    return sum(
        component != 0
        for component in component_edge_masks(graph, mask)
    )


def is_root_good(graph, state, roots) -> bool:
    root, target = roots
    for first, second in PAIRS:
        for component in component_edge_masks(
            graph,
            active_mask(state, first, second),
        ):
            if (component >> root) & 1 and (component >> target) & 1:
                return True
    return False


def moves(graph, state):
    old_chi = euler_characteristic(graph, state)
    for first, second in PAIRS:
        for component in component_edge_masks(
            graph,
            active_mask(state, first, second),
        ):
            raw = tuple(
                transpose_label(label, first, second)
                if (component >> edge) & 1
                else label
                for edge, label in enumerate(state)
            )
            other = canonical(raw)
            if other == state:
                continue
            new_chi = euler_characteristic(graph, raw)
            yield other, {
                "pair": [first, second],
                "component_edges": [
                    edge
                    for edge in range(graph.edge_count)
                    if (component >> edge) & 1
                ],
                "chi_before": old_chi,
                "chi_after": new_chi,
                "delta_chi": new_chi - old_chi,
                "coordinate_component_counts_before": [
                    coordinate_component_count(graph, state, first),
                    coordinate_component_count(graph, state, second),
                ],
                "coordinate_component_counts_after": [
                    coordinate_component_count(graph, raw, first),
                    coordinate_component_count(graph, raw, second),
                ],
            }


def shortest_nondecreasing_rescue(graph, initial, roots):
    initial = canonical(initial)
    queue = deque([initial])
    parent = {initial: None}
    parent_move = {}
    rescued = initial if is_root_good(graph, initial, roots) else None
    while queue and rescued is None:
        state = queue.popleft()
        old_chi = euler_characteristic(graph, state)
        for other, move in moves(graph, state):
            if move["chi_after"] < old_chi or other in parent:
                continue
            parent[other] = state
            parent_move[other] = move
            if is_root_good(graph, other, roots):
                rescued = other
                break
            queue.append(other)
    assert rescued is not None
    path = []
    cursor = rescued
    while parent[cursor] is not None:
        path.append((cursor, parent_move[cursor]))
        cursor = parent[cursor]
    path.reverse()
    states = [initial] + [state for state, _ in path]
    return {
        "path_length": len(path),
        "chi_sequence": [
            euler_characteristic(graph, state)
            for state in states
        ],
        "states_labels_hex": [
            [f"{label:02x}" for label in state]
            for state in states
        ],
        "moves": [move for _, move in path],
        "states_examined": len(parent),
    }


def main() -> None:
    reports = []
    for case in CASES:
        graph = graph_from_graph6(case["graph6"])
        result = shortest_nondecreasing_rescue(
            graph,
            case["initial"],
            case["roots"],
        )
        reports.append({
            "name": case["name"],
            "graph6": case["graph6"],
            "roots": list(case["roots"]),
            **result,
        })
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    main()
