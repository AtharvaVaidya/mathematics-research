#!/usr/bin/env python3
"""Search the exact unavoidable first-block reentry implication.

For every D5 flow on connected simple cubic graphs of selected orders, find
distance-two rooted factor chains C,D for which the Q-factor component H
through the first root re-enters C before the first C-D join in both cyclic
directions.  Test whether switching Q on H puts the roots on one factor
component.

This is an exploratory producer.  Any emitted literal witness must be copied
to a small independent checker before it is used as a mathematical result.
"""

from __future__ import annotations

import argparse
import itertools
import subprocess
import sys
from collections import Counter, deque
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for item in (PROJECT_ROOT, PROJECT_ROOT / "scratch"):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from audit_d5_root_kempe_orbits import (  # noqa: E402
    PAIRS,
    active_mask,
    canonical,
    component_edge_masks,
    enumerate_flows,
    neighbours,
    transpose_label,
)
from audit_d5_surface_chi_plateaus_order12 import surface_chi  # noqa: E402
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402
from tools.flow_switch_audit import is_bridgeless  # noqa: E402


def graph_records(order: int) -> tuple[str, ...]:
    completed = subprocess.run(
        ["/opt/homebrew/bin/geng", "-cq", "-d3", "-D3", str(order)],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
        encoding="ascii",
    )
    return tuple(row for row in completed.stdout.splitlines() if row)


def factor_components(graph, state):
    return {
        pair: tuple(component_edge_masks(graph, active_mask(state, *pair)))
        for pair in PAIRS
    }


def contains(mask: int, edge: int) -> bool:
    return bool(mask & (1 << edge))


def edges_of(mask: int, edge_count: int) -> tuple[int, ...]:
    return tuple(edge for edge in range(edge_count) if contains(mask, edge))


def cycle_order(graph, component: int, root: int) -> tuple[int, ...]:
    """Return either cyclic orientation of a nonempty factor circuit."""
    selected = set(edges_of(component, graph.edge_count))
    adjacent = {}
    for edge in selected:
        endpoints = graph.edges[edge]
        neighbours = {
            other
            for other in selected - {edge}
            if set(endpoints) & set(graph.edges[other])
        }
        assert len(neighbours) == 2
        adjacent[edge] = tuple(sorted(neighbours))
    answer = [root]
    previous = None
    current = root
    while len(answer) < len(selected):
        choices = [edge for edge in adjacent[current] if edge != previous]
        assert choices
        following = choices[0]
        if following == root:
            following = choices[1]
        assert following not in answer
        answer.append(following)
        previous, current = current, following
    assert root in adjacent[current]
    return tuple(answer)


def reenters_before_join(order, h_mask: int, d_mask: int) -> bool:
    """Starting on order[0] in H, leave its root block then hit H before D."""
    assert contains(h_mask, order[0])
    position = 1
    while position < len(order) and contains(h_mask, order[position]):
        position += 1
    assert position < len(order)  # D is disjoint from H and meets the cycle.
    for edge in order[position:]:
        if contains(d_mask, edge):
            return False
        if contains(h_mask, edge):
            return True
    raise AssertionError("the D component must meet C")


def unavoidable(graph, c_mask: int, d_mask: int, h_mask: int, root: int):
    order = cycle_order(graph, c_mask, root)
    reverse = order[:1] + tuple(reversed(order[1:]))
    result = (
        reenters_before_join(order, h_mask, d_mask)
        and reenters_before_join(reverse, h_mask, d_mask)
    )
    return result, order


def switched(state, pair, component):
    return canonical(
        tuple(
            transpose_label(label, *pair)
            if contains(component, edge)
            else label
            for edge, label in enumerate(state)
        )
    )


def rescued(components, root, target):
    return any(
        contains(component, root) and contains(component, target)
        for rows in components.values()
        for component in rows
    )


def terminal_plateau_info(graph, initial):
    level = surface_chi(graph, initial)
    start = canonical(initial)
    plateau = {start}
    queue = deque([start])
    deltas = Counter()
    while queue:
        state = queue.popleft()
        for other in set(neighbours(graph, state)) - {state}:
            delta = surface_chi(graph, other) - level
            deltas[delta] += 1
            if delta == 0 and other not in plateau:
                plateau.add(other)
                queue.append(other)
    return {
        "states_mod_s5": len(plateau),
        "delta_histogram": dict(sorted(deltas.items())),
        "terminal": not any(delta > 0 for delta in deltas),
    }


def inspect_state(record, graph, state):
    components = factor_components(graph, state)
    level = surface_chi(graph, state)
    all_switch_deltas = [
        surface_chi(graph, switched(state, pair, component)) - level
        for pair, rows in components.items()
        for component in rows
    ]
    witnesses = []
    for p_pair, q_pair in itertools.permutations(PAIRS, 2):
        relation = len(set(p_pair) & set(q_pair))
        if relation not in (0, 1):
            continue
        for c_mask in components[p_pair]:
            for d_mask in components[q_pair]:
                if not (c_mask & d_mask):
                    continue
                for h_mask in components[q_pair]:
                    if h_mask == d_mask:
                        continue
                    roots = edges_of(c_mask & h_mask, graph.edge_count)
                    if not roots:
                        continue
                    for root in roots:
                        unavoidable_flag, order = unavoidable(
                            graph, c_mask, d_mask, h_mask, root
                        )
                        if not unavoidable_flag:
                            continue
                        for target in edges_of(d_mask, graph.edge_count):
                            if rescued(components, root, target):
                                continue
                            after = switched(state, q_pair, h_mask)
                            after_components = factor_components(graph, after)
                            forces_one = rescued(after_components, root, target)
                            witnesses.append(
                                {
                                    "graph6": record,
                                    "state": tuple(f"{x:02x}" for x in state),
                                    "roots": (root, target),
                                    "P": p_pair,
                                    "Q": q_pair,
                                    "relation": "disjoint" if relation == 0 else "shared",
                                    "C": edges_of(c_mask, graph.edge_count),
                                    "D": edges_of(d_mask, graph.edge_count),
                                    "H": edges_of(h_mask, graph.edge_count),
                                    "C_order": order,
                                    "after": tuple(f"{x:02x}" for x in after),
                                    "forces_d1": forces_one,
                                    "chi_delta": (
                                        surface_chi(graph, after)
                                        - level
                                    ),
                                    "maximum_switch_delta": max(all_switch_deltas),
                                }
                            )
    return witnesses


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("orders", nargs="*", type=int, default=[4, 6, 8, 10, 12])
    parser.add_argument("--stop-on-counterexample", action="store_true")
    parser.add_argument("--counterexample-local-max", action="store_true")
    parser.add_argument("--counterexample-terminal-neutral", action="store_true")
    args = parser.parse_args()
    totals = Counter()
    first = {}
    for order in args.orders:
        for record in graph_records(order):
            graph = graph_from_graph6(record)
            if not is_bridgeless(graph):
                continue
            for state in sorted(enumerate_flows(graph)):
                rows = inspect_state(record, graph, state)
                for row in rows:
                    key = (row["relation"], row["forces_d1"], row["chi_delta"])
                    totals[key] += 1
                    if key not in first:
                        first[key] = row
                        print("FIRST", key, row, flush=True)
                    if (
                        args.stop_on_counterexample
                        and not row["forces_d1"]
                        and (
                            not args.counterexample_terminal_neutral
                            or row["chi_delta"] == 0
                        )
                        and (
                            not args.counterexample_local_max
                            or row["maximum_switch_delta"] <= 0
                        )
                    ):
                        row["plateau"] = terminal_plateau_info(graph, state)
                        if (
                            args.counterexample_terminal_neutral
                            and not row["plateau"]["terminal"]
                        ):
                            continue
                        print("COUNTEREXAMPLE", row, flush=True)
                        print("TOTALS", dict(totals))
                        return 1
        print(f"finished order {order}: {dict(totals)}", flush=True)
    print("TOTALS", dict(totals))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
