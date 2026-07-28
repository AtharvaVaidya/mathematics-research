#!/usr/bin/env python3
"""Audit a cyclic foreign-Q-block potential in a fixed D5 plateau.

For a shortest component chain whose first component C has pair P and
second component D has pair Q, let H be the Q-component containing the
source root.  On each orientation of the C circuit, ignore later
H-returns and count foreign Q-component blocks before the first D
block.  The minimum of the two counts is the triple's blocker number.

This script tests whether switching H or either first foreign blocker
has a neutral move that decreases (factor distance, minimum blocker
number).  It is exploratory and deliberately prints literal failures.
"""

from __future__ import annotations

import argparse
import itertools
import sys
from collections import Counter, deque
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "scratch") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scratch"))

from audit_d5_root_euler_potential import euler_characteristic
from audit_d5_root_kempe_orbits import (
    PAIRS,
    active_mask,
    canonical,
    component_edge_masks,
    transpose_label,
)
from tools.fixed_fano_merge_frontier import graph_from_graph6


DEFAULT_GRAPH6 = "K??FEagT@WB_"
DEFAULT_STATE = (
    "03 05 06 05 03 06 06 0a 0c "
    "06 0a 0c 0c 0a 06 0c 06 0a"
)


def factors(graph, state):
    answer = []
    for pair in PAIRS:
        for mask in component_edge_masks(graph, active_mask(state, *pair)):
            if mask:
                answer.append((pair, mask))
    return tuple(answer)


def switched(state, pair, mask):
    return tuple(
        transpose_label(label, *pair) if (mask >> edge) & 1 else label
        for edge, label in enumerate(state)
    )


def mask_edges(graph, mask):
    return tuple(
        edge for edge in range(graph.edge_count) if (mask >> edge) & 1
    )


def circuit_order(graph, mask, root):
    selected = set(mask_edges(graph, mask))

    def neighbours(edge):
        return sorted(
            other
            for other in selected
            if other != edge
            and set(graph.edges[edge]) & set(graph.edges[other])
        )

    assert root in selected
    assert all(len(neighbours(edge)) == 2 for edge in selected)
    answer = [root]
    previous = root
    current = neighbours(root)[0]
    while current != root:
        answer.append(current)
        adjacent = neighbours(current)
        following = adjacent[0] if adjacent[0] != previous else adjacent[1]
        previous, current = current, following
    assert len(answer) == len(selected)
    return tuple(answer)


def component_distances(factor_rows, initial):
    distance = {index: 1 for index in initial}
    queue = deque(initial)
    while queue:
        index = queue.popleft()
        for other in range(len(factor_rows)):
            if (
                other not in distance
                and factor_rows[index][1] & factor_rows[other][1]
            ):
                distance[other] = distance[index] + 1
                queue.append(other)
    return distance


def distance_and_shortest_first_pairs(graph, state, roots):
    rows = factors(graph, state)
    source_nodes = [
        index for index, (_, mask) in enumerate(rows)
        if (mask >> roots[0]) & 1
    ]
    target_nodes = [
        index for index, (_, mask) in enumerate(rows)
        if (mask >> roots[1]) & 1
    ]
    from_source = component_distances(rows, source_nodes)
    to_target = component_distances(rows, target_nodes)
    distance = min(from_source[index] for index in target_nodes)
    first_pairs = []
    for first in source_nodes:
        for second in range(len(rows)):
            if first == second or not (rows[first][1] & rows[second][1]):
                continue
            if 1 + to_target[second] == distance:
                first_pairs.append((first, second))
    return distance, rows, tuple(first_pairs)


def blocker_profile(graph, state, roots, rows, first, second):
    pair_p, circuit = rows[first]
    pair_q, target_component = rows[second]
    if len(set(pair_p) & set(pair_q)) != 1:
        return None

    q_rows = [
        (index, mask)
        for index, (pair, mask) in enumerate(rows)
        if pair == pair_q
    ]
    root_rows = [
        (index, mask)
        for index, mask in q_rows
        if (mask >> roots[0]) & 1
    ]
    assert len(root_rows) <= 1
    if not root_rows:
        return None
    root_index, root_component = root_rows[0]
    if root_index == second:
        return None

    owner = {}
    for index, mask in q_rows:
        for edge in mask_edges(graph, circuit & mask):
            assert edge not in owner
            owner[edge] = index

    order = circuit_order(graph, circuit, roots[0])
    n = len(order)

    def scan(step):
        # Leave the contiguous root H-block in this orientation.
        cursor = step
        while owner.get(order[cursor % n]) == root_index:
            cursor += step
            assert abs(cursor) <= n

        blockers = []
        previous_owner = None
        while abs(cursor) <= n:
            edge = order[cursor % n]
            current_owner = owner.get(edge)
            if current_owner != previous_owner:
                if current_owner == second:
                    return {
                        "blockers": tuple(blockers),
                        "join_edge": edge,
                        "steps": abs(cursor),
                    }
                if (
                    current_owner is not None
                    and current_owner != root_index
                ):
                    blockers.append(current_owner)
            previous_owner = current_owner
            cursor += step
        raise AssertionError("target component not found on circuit")

    scans = (scan(1), scan(-1))
    return {
        "pair_p": pair_p,
        "pair_q": pair_q,
        "circuit": circuit,
        "target_component": target_component,
        "root_component": root_component,
        "scans": scans,
        "blocker_number": min(len(row["blockers"]) for row in scans),
    }


def potential(graph, state, roots):
    distance, rows, first_pairs = distance_and_shortest_first_pairs(
        graph, state, roots
    )
    profiles = []
    for first, second in first_pairs:
        row = blocker_profile(graph, state, roots, rows, first, second)
        if row is not None:
            profiles.append(row)
    minimum = min(
        (row["blocker_number"] for row in profiles),
        default=None,
    )
    return distance, minimum, tuple(profiles)


def equal_chi_plateau(graph, initial):
    level = euler_characteristic(graph, initial)
    start = canonical(initial)
    states = {start}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        for pair, mask in factors(graph, state):
            other = switched(state, pair, mask)
            if euler_characteristic(graph, other) == level:
                other = canonical(other)
                if other not in states:
                    states.add(other)
                    queue.append(other)
    return states


def audit_state(graph, state, roots):
    level = euler_characteristic(graph, state)
    before_d, before_mu, profiles = potential(graph, state, roots)
    if before_d <= 1 or before_mu is None:
        return None

    minimizing = [
        profile
        for profile in profiles
        if profile["blocker_number"] == before_mu
    ]
    candidates = set()
    for profile in minimizing:
        pair_q = profile["pair_q"]
        candidates.add((pair_q, profile["root_component"]))
        q_masks = {
            mask
            for pair, mask in factors(graph, state)
            if pair == pair_q
        }
        for scan in profile["scans"]:
            if scan["blockers"]:
                blocker_index = scan["blockers"][0]
                # Indices refer to the same deterministic factor row list.
                rows = factors(graph, state)
                blocker_pair, blocker_mask = rows[blocker_index]
                assert blocker_pair == pair_q
                assert blocker_mask in q_masks
                candidates.add((pair_q, blocker_mask))

    outcomes = []
    for pair, mask in sorted(candidates):
        other = switched(state, pair, mask)
        delta = euler_characteristic(graph, other) - level
        after_d, after_mu, _ = potential(graph, other, roots)
        outcomes.append((pair, mask, delta, after_d, after_mu))

    def key(distance, blocker):
        return (distance, float("inf") if blocker is None else blocker)

    improving_neutral = [
        row
        for row in outcomes
        if row[2] == 0 and key(row[3], row[4]) < key(before_d, before_mu)
    ]
    return {
        "distance": before_d,
        "potential": before_mu,
        "profiles": minimizing,
        "outcomes": outcomes,
        "improving_neutral": improving_neutral,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph6", default=DEFAULT_GRAPH6)
    parser.add_argument("--state", default=DEFAULT_STATE)
    parser.add_argument("--roots", default="0,17")
    parser.add_argument("--plateau", action="store_true")
    args = parser.parse_args()

    graph = graph_from_graph6(args.graph6)
    state = tuple(int(label, 16) for label in args.state.split())
    roots = tuple(int(item) for item in args.roots.split(","))
    assert len(roots) == 2

    states = equal_chi_plateau(graph, state) if args.plateau else {state}
    histogram = Counter()
    first_failure = None
    for current in sorted(states):
        row = audit_state(graph, current, roots)
        if row is None:
            histogram["not_applicable"] += 1
            continue
        histogram[(row["distance"], row["potential"])] += 1
        if not row["improving_neutral"] and first_failure is None:
            first_failure = (current, row)

    print("states", len(states))
    print("histogram", dict(histogram))
    if first_failure is None:
        print("NO FAILURE")
        return

    current, row = first_failure
    print("FIRST FAILURE")
    print("labels", " ".join(f"{label:02x}" for label in current))
    print("roots", roots)
    print("distance", row["distance"], "potential", row["potential"])
    for profile in row["profiles"]:
        print(
            "profile",
            profile["pair_p"],
            profile["pair_q"],
            hex(profile["circuit"]),
            hex(profile["root_component"]),
            hex(profile["target_component"]),
            profile["scans"],
        )
    for outcome in row["outcomes"]:
        print(
            "outcome",
            outcome[0],
            hex(outcome[1]),
            "delta",
            outcome[2],
            "after",
            outcome[3:],
        )


if __name__ == "__main__":
    main()
