#!/usr/bin/env python3
"""Audit actual equal-chi plateaus seeded by all hard-state 2-lifts.

Unlike a one-state local-maximum check, terminality here means that the
entire connected component under equal-chi Kempe moves has no positive-chi
exit.  For each terminal plateau reached from a gauge-normalized connected
2-lift, also test neutral-component support connectivity at every state.
"""

from __future__ import annotations

import sys
from collections import Counter, deque
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRATCH = PROJECT_ROOT / "scratch"
for item in (str(PROJECT_ROOT), str(SCRATCH)):
    if item not in sys.path:
        sys.path.insert(0, item)

from audit_d5_local_chi_max_neutral_connectivity_two_lifts import (  # noqa: E402
    audit_state,
    cotree_edges,
)
from audit_d5_root_euler_potential import euler_characteristic  # noqa: E402
from audit_d5_root_kempe_orbits import (  # noqa: E402
    PAIRS,
    active_mask,
    canonical,
    component_edge_masks,
    transpose_label,
)
from check_d5_local_boundary_degree_two_lift_no_go import (  # noqa: E402
    construct_lift,
    validate_flow,
)


def moves(graph, state, old_chi=None):
    if old_chi is None:
        old_chi = euler_characteristic(graph, state)
    for pair in PAIRS:
        for component in component_edge_masks(
            graph, active_mask(state, *pair)
        ):
            if not component:
                continue
            other = tuple(
                transpose_label(label, *pair)
                if (component >> edge) & 1
                else label
                for edge, label in enumerate(state)
            )
            yield pair, component, euler_characteristic(graph, other) - old_chi, other


def plateau_from_seed(graph, supplied):
    initial = canonical(supplied)
    level = euler_characteristic(graph, initial)
    states = [initial]
    seen = {initial}
    terminal = True
    positive_exit = None
    disconnected_states = []
    for cursor, state in enumerate(states):
        _, _, blocks = audit_state(graph, state)
        if len(blocks) != 1:
            disconnected_states.append({
                "state_index": cursor,
                "block_sizes": sorted(mask.bit_count() for mask in blocks),
                "labels_hex": [f"{label:02x}" for label in state],
            })
        for pair, component, delta, other in moves(graph, state, level):
            if delta > 0:
                terminal = False
                if positive_exit is None:
                    positive_exit = {
                        "state_index": cursor,
                        "pair": pair,
                        "component_edges": [
                            edge
                            for edge in range(graph.edge_count)
                            if (component >> edge) & 1
                        ],
                        "delta": delta,
                    }
            elif delta == 0:
                normalized = canonical(other)
                if normalized not in seen:
                    seen.add(normalized)
                    states.append(normalized)
    return {
        "level": level,
        "size_mod_s5": len(states),
        "terminal": terminal,
        "positive_exit": positive_exit,
        "disconnected_states": disconnected_states,
    }


def main() -> int:
    cotree = cotree_edges()
    local_maxima = 0
    actual_terminal = 0
    terminal_sizes = Counter()
    terminal_disconnected = []
    nonterminal_plateau_sizes = Counter()

    for word in range(1, 1 << len(cotree)):
        voltages = {
            cotree[index]
            for index in range(len(cotree))
            if (word >> index) & 1
        }
        graph6, graph, state, _ = construct_lift(voltages)
        validate_flow(graph, state)
        delta_histogram, _, _ = audit_state(graph, state)
        if max(delta_histogram) > 0:
            continue
        local_maxima += 1
        plateau = plateau_from_seed(graph, state)
        if plateau["terminal"]:
            actual_terminal += 1
            terminal_sizes[plateau["size_mod_s5"]] += 1
            if plateau["disconnected_states"]:
                terminal_disconnected.append({
                    "voltage_word": word,
                    "voltage_one_edges": sorted(voltages),
                    "graph6": graph6,
                    **plateau,
                })
        else:
            nonterminal_plateau_sizes[plateau["size_mod_s5"]] += 1
        print(
            f"word={word} local_max={local_maxima} "
            f"plateau={plateau['size_mod_s5']} "
            f"terminal={plateau['terminal']}",
            file=sys.stderr,
            flush=True,
        )

    print("PASS" if not terminal_disconnected else "FAIL")
    print(f"connected gauge-normalized 2-lifts: {(1 << len(cotree)) - 1}")
    print(f"seed states which are local chi maxima: {local_maxima}")
    print(f"seed plateaus which are actually terminal: {actual_terminal}")
    print(f"terminal plateau sizes: {dict(sorted(terminal_sizes.items()))}")
    print(
        "nonterminal seed plateau sizes: "
        f"{dict(sorted(nonterminal_plateau_sizes.items()))}"
    )
    print(
        "terminal plateaus containing disconnected neutral support: "
        f"{len(terminal_disconnected)}"
    )
    if terminal_disconnected:
        print(f"first witness: {terminal_disconnected[0]}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
