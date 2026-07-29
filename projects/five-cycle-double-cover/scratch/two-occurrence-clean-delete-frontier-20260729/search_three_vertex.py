#!/usr/bin/env python3
"""Exact three-vertex search at the first odd-degree profile (5,5,4)."""

from __future__ import annotations

import argparse
import itertools

from search_two_vertex import K, NZ, bilinear


def make_graph(multiplicities):
    edges = tuple(
        [(0, 1)] * multiplicities[0]
        + [(0, 2)] * multiplicities[1]
        + [(1, 2)] * multiplicities[2]
    )
    incident = tuple(
        tuple(e for e, ends in enumerate(edges) if v in ends)
        for v in range(3)
    )
    return edges, incident


def canonical_cycle(order: tuple[int, ...]) -> tuple[int, ...]:
    images = []
    n = len(order)
    for reverse in (False, True):
        current = order if not reverse else tuple(reversed(order))
        images.extend(current[i:] + current[:i] for i in range(n))
    return min(images)


def cyclic_representatives(items: tuple[int, ...]):
    first = min(items)
    rest = tuple(item for item in items if item != first)
    for tail in itertools.permutations(rest):
        order = (first,) + tail
        if order == canonical_cycle(order):
            yield order


def xor(values) -> int:
    result = 0
    for value in values:
        result ^= value
    return result


def feasible_flows(edges, incident):
    for flow in itertools.product(NZ, repeat=len(edges)):
        if all(xor(flow[e] for e in incident[v]) == 0 for v in range(3)):
            yield flow


def prefixes(order: tuple[int, ...], flow: tuple[int, ...]):
    value = 0
    result = {}
    used = set()
    for edge in order:
        result[edge] = value
        used.add(value)
        value ^= flow[edge]
    assert value == 0
    return result, frozenset(used)


def classify(edges, orders, flow):
    endpoint_prefix = []
    used = []
    for order in orders:
        prefix, colours = prefixes(order, flow)
        endpoint_prefix.append(prefix)
        used.append(colours)

    rhs = []
    for edge, (u, v) in enumerate(edges):
        rhs.append(
            bilinear(
                endpoint_prefix[u][edge] ^ endpoint_prefix[v][edge],
                flow[edge],
            )
        )

    clean = False
    for x1, x2 in itertools.product(K, repeat=2):
        translations = (0, x1, x2)
        if all(
            bilinear(translations[u] ^ translations[v], flow[edge])
            == rhs[edge]
            for edge, (u, v) in enumerate(edges)
        ):
            clean = True
            break
    deletes = any(len(colours) < 4 for colours in used)
    return clean, deletes, tuple(rhs), tuple(used)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--multiplicities",
        default="3,2,2",
        help="numbers of parallel edges on 01,02,12",
    )
    args = parser.parse_args()
    multiplicities = tuple(map(int, args.multiplicities.split(",")))
    assert len(multiplicities) == 3 and all(x >= 1 for x in multiplicities)
    edges, incident = make_graph(multiplicities)

    flows = tuple(feasible_flows(edges, incident))
    rotations = tuple(
        tuple(cyclic_representatives(incident[v])) for v in range(3)
    )
    print(
        f"GRAPH multiplicities={multiplicities} edges={len(edges)}"
        f" degrees={tuple(map(len, incident))} feasible_flows={len(flows)}"
        f" rotations_per_vertex={tuple(map(len, rotations))}"
    )

    states = 0
    fixed_bad = None
    universal_bad = []
    goal_histogram = {}
    state_goal_types = {"clean": 0, "delete_only": 0, "none": 0}
    for orders in itertools.product(*rotations):
        states += 1
        goals = 0
        clean_goals = 0
        delete_goals = 0
        first_row = None
        for flow in flows:
            row = classify(edges, orders, flow)
            if first_row is None:
                first_row = (flow, row)
            if row[0] or row[1]:
                goals += 1
            if row[0]:
                clean_goals += 1
            if row[1]:
                delete_goals += 1
            elif not row[0] and fixed_bad is None:
                fixed_bad = (orders, flow, row)
                print(
                    "FIXED_FLOW_COUNTEREXAMPLE"
                    f" orders={orders} flow={flow} rhs={row[2]}"
                    f" used={tuple(sorted(x) for x in row[3])}"
                )
        goal_histogram[goals] = goal_histogram.get(goals, 0) + 1
        if clean_goals:
            state_goal_types["clean"] += 1
        elif delete_goals:
            state_goal_types["delete_only"] += 1
        else:
            state_goal_types["none"] += 1
        if goals == 0:
            universal_bad.append((orders, first_row))
            print(f"UNIVERSAL_COUNTEREXAMPLE orders={orders}")
            break

    assert fixed_bad is not None
    print(
        f"RESULT states={states} universal_counterexamples="
        f"{len(universal_bad)} state_goal_types={state_goal_types}"
        f" goal_histogram={sorted(goal_histogram.items())}"
    )
    if universal_bad:
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    main()
