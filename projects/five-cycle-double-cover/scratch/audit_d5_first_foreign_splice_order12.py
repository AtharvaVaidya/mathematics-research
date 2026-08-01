#!/usr/bin/env python3
"""Complete terminal order-12 audit of the first-foreign splice lemma."""

from __future__ import annotations

import json
import sys
from collections import Counter, deque
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for item in (PROJECT_ROOT, PROJECT_ROOT / "scratch"):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from audit_d5_root_component_chain_potential import (  # noqa: E402
    all_root_distances,
)
from audit_d5_root_euler_potential import euler_characteristic  # noqa: E402
from audit_d5_root_kempe_orbits import (  # noqa: E402
    PAIRS,
    active_mask,
    component_edge_masks,
    enumerate_flows,
    neighbours,
    transpose_label,
)
from audit_d5_terminal_chi_chain_lex_order12 import graph_records  # noqa: E402
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402


def factor_family(graph, state):
    return tuple(
        (pair, component)
        for pair in PAIRS
        for component in component_edge_masks(
            graph, active_mask(state, *pair)
        )
        if component
    )


def switched(state, pair, component):
    return tuple(
        transpose_label(label, *pair)
        if (component >> edge) & 1
        else label
        for edge, label in enumerate(state)
    )


def cycle_order(graph, component, root):
    incidence = [[] for _ in range(graph.vertices)]
    for edge, (left, right) in enumerate(graph.edges):
        if (component >> edge) & 1:
            incidence[left].append(edge)
            incidence[right].append(edge)
    assert all(len(row) in (0, 2) for row in incidence)
    vertex = graph.edges[root][1]
    previous = root
    answer = [root]
    while True:
        edge = (
            incidence[vertex][0]
            if incidence[vertex][0] != previous
            else incidence[vertex][1]
        )
        if edge == root:
            return tuple(answer)
        answer.append(edge)
        left, right = graph.edges[edge]
        vertex = left ^ right ^ vertex
        previous = edge


def transformed_pair(pair, switch_pair):
    answer = []
    for coordinate in pair:
        if coordinate == switch_pair[0]:
            coordinate = switch_pair[1]
        elif coordinate == switch_pair[1]:
            coordinate = switch_pair[0]
        answer.append(coordinate)
    return tuple(sorted(answer))


def terminal_states(graph, states):
    index = {state: position for position, state in enumerate(states)}
    adjacency = [
        {
            index[other]
            for other in neighbours(graph, state)
            if other != state
        }
        for state in states
    ]
    chis = [euler_characteristic(graph, state) for state in states]
    answer = [False] * len(states)
    unseen = set(range(len(states)))
    plateaus = 0
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
        if terminal:
            plateaus += 1
            for state in plateau:
                answer[state] = True
    return answer, chis, plateaus


def audit_graph(record):
    graph = graph_from_graph6(record)
    states = sorted(enumerate_flows(graph))
    terminal, chis, plateau_count = terminal_states(graph, states)
    configurations = 0
    rooted_distance_two = 0
    delta_histogram = Counter()
    orientation_histogram = Counter()
    first_failure = None

    for state_index, state in enumerate(states):
        if not terminal[state_index]:
            continue
        family = factor_family(graph, state)
        by_pair = {
            pair: tuple(
                component
                for candidate, component in family
                if candidate == pair
            )
            for pair in PAIRS
        }
        distances = all_root_distances(
            graph.edge_count,
            [component for _, component in family],
        )
        switch_cache = {}

        for pair_p, components_p in by_pair.items():
            for pair_q, components_q in by_pair.items():
                if len(set(pair_p) & set(pair_q)) != 1:
                    continue
                foreign_by_edge = {}
                for component in components_q:
                    mask = component
                    while mask:
                        bit = mask & -mask
                        foreign_by_edge[bit.bit_length() - 1] = component
                        mask ^= bit

                for component_c in components_p:
                    for component_h in components_q:
                        roots = component_c & component_h
                        while roots:
                            bit = roots & -roots
                            root = bit.bit_length() - 1
                            roots ^= bit
                            order = cycle_order(
                                graph, component_c, root
                            )

                            first_foreign = []
                            for oriented in (order[1:], order[:0:-1]):
                                found = None
                                for edge in oriented:
                                    candidate = foreign_by_edge.get(edge)
                                    if (
                                        candidate is not None
                                        and candidate != component_h
                                    ):
                                        found = candidate
                                        break
                                first_foreign.append(found)

                            candidates_d = {
                                component
                                for component in first_foreign
                                if component is not None
                            }
                            for component_d in candidates_d:
                                configurations += 1
                                orientation_histogram[
                                    sum(
                                        item == component_d
                                        for item in first_foreign
                                    )
                                ] += 1
                                key = (pair_q, component_h)
                                if key not in switch_cache:
                                    other = switched(
                                        state, pair_q, component_h
                                    )
                                    switch_cache[key] = (
                                        other,
                                        factor_family(graph, other),
                                        euler_characteristic(graph, other)
                                        - chis[state_index],
                                    )
                                other, other_family, delta = switch_cache[key]
                                delta_histogram[delta] += 1
                                pair_prime = transformed_pair(
                                    pair_p, pair_q
                                )
                                roots_prime = [
                                    component
                                    for candidate, component in other_family
                                    if candidate == pair_prime
                                    and ((component >> root) & 1)
                                ]
                                valid = (
                                    len(roots_prime) == 1
                                    and bool(roots_prime[0] & component_d)
                                )
                                if not valid and first_failure is None:
                                    first_failure = {
                                        "state_labels_hex": [
                                            f"{label:02x}"
                                            for label in state
                                        ],
                                        "root": root,
                                        "pair_p": pair_p,
                                        "pair_q": pair_q,
                                        "component_c": component_c,
                                        "component_h": component_h,
                                        "component_d": component_d,
                                        "cycle_order": order,
                                        "first_foreign": first_foreign,
                                    }

                                targets = component_d
                                while targets:
                                    target_bit = targets & -targets
                                    target = target_bit.bit_length() - 1
                                    targets ^= target_bit
                                    if distances[root][target] == 2:
                                        rooted_distance_two += 1

    return {
        "graph6": record,
        "flows_mod_s5": len(states),
        "terminal_states_mod_s5": sum(terminal),
        "terminal_plateaus": plateau_count,
        "configurations": configurations,
        "rooted_distance_two_cases": rooted_distance_two,
        "orientation_histogram": dict(orientation_histogram),
        "delta_histogram": dict(delta_histogram),
        "failure": first_failure,
    }


def main():
    totals = Counter()
    first_failure = None
    rows = []
    for index, record in enumerate(graph_records(12), 1):
        row = audit_graph(record)
        rows.append(row)
        for key in (
            "flows_mod_s5",
            "terminal_states_mod_s5",
            "terminal_plateaus",
            "configurations",
            "rooted_distance_two_cases",
        ):
            totals[key] += row[key]
        if row["failure"] is not None and first_failure is None:
            first_failure = {
                "graph6": record,
                **row["failure"],
            }
        print(
            f"{index}: {record} configs={row['configurations']} "
            f"failure={row['failure'] is not None}",
            file=sys.stderr,
            flush=True,
        )
        if first_failure is not None:
            break
    report = {
        "status": "PASS" if first_failure is None else "FAIL",
        "graphs": len(rows),
        **dict(totals),
        "first_failure": first_failure,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if first_failure is None else 1


if __name__ == "__main__":
    raise SystemExit(main())
