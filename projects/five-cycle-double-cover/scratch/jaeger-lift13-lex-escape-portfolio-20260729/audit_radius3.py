#!/usr/bin/env python3
"""Audit augmented-trap rows from stdin for escape radius at most three."""

from __future__ import annotations

from collections import deque
from itertools import combinations
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "base",
    HERE.parent
    / "jaeger-lift13-girth10-augmented-trap-20260729"
    / "independent_verify.py",
)
assert SPEC and SPEC.loader
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

model = None
state_cache = {}
neighbour_cache = {}


def initialize(record):
    global model
    order, edges = base.graph6(record["graph6"])
    root = record["root"]
    spokes = tuple(
        edge for edge, endpoints in enumerate(edges) if root in endpoints
    )
    internal = tuple(
        edge for edge, endpoints in enumerate(edges)
        if root not in endpoints
    )
    assert order == 130 and len(spokes) == 3 and len(internal) == 192
    model = order, edges, spokes, internal


def state_data(labels):
    labels = tuple(labels)
    known = state_cache.get(labels)
    if known is not None:
        return known
    order, edges, spokes, internal = model
    trees = base.build_trees(order, edges, internal, spokes, labels)
    kernels, profile, flags = base.evaluate(order, edges, trees)
    value = profile, flags, (min(profile), sum(map(len, kernels)))
    state_cache[labels] = value
    return value


def legal_neighbours(labels):
    labels = tuple(labels)
    known = neighbour_cache.get(labels)
    if known is not None:
        return known
    order, edges, spokes, internal = model
    answer = []
    for first_coordinate, second_coordinate in combinations(range(3), 2):
        for first in range(192):
            if labels[first] != first_coordinate:
                continue
            for second in range(192):
                if labels[second] != second_coordinate:
                    continue
                changed = list(labels)
                changed[first], changed[second] = (
                    changed[second],
                    changed[first],
                )
                candidate = tuple(changed)
                try:
                    data = state_data(candidate)
                except AssertionError:
                    continue
                answer.append((candidate, (first, second), data))
    neighbour_cache[labels] = answer
    return answer


def audit(row):
    # Bound memory by one trap.  Cross-trap reuse is not needed for the
    # finite radius-three claim.
    state_cache.clear()
    neighbour_cache.clear()
    seed = tuple(row["state_labels"])
    seed_profile, seed_flags, seed_psi = state_data(seed)
    assert seed_profile == tuple(row["profile"])
    assert seed_flags == 0
    assert seed_psi == (row["d_min"], row["kernel_sum"])
    assert not any(
        tuple(neighbour["psi"]) < seed_psi
        or neighbour["parallel_successful_flags"] > 0
        for neighbour in row["full_neighbourhood"]
    )
    reconstructed_seed_neighbours = legal_neighbours(seed)
    reconstructed_rows = [
        {
            "local_positions": list(exchange),
            "coordinates": [
                seed[exchange[0]],
                seed[exchange[1]],
            ],
            "psi": list(data[2]),
            "parallel_successful_flags": data[1],
        }
        for _, exchange, data in reconstructed_seed_neighbours
    ]
    assert reconstructed_rows == row["full_neighbourhood"]

    # The raw row already exhausts distance one.  Reconstruct its safe
    # equal-Psi neighbours and independently evaluate every later state.
    queue = deque()
    predecessor = {seed: None}
    exchange_from_parent = {}
    for candidate, exchange, (_, flags, psi) in reconstructed_seed_neighbours:
        if psi != seed_psi or flags != 0:
            continue
        if candidate not in predecessor:
            predecessor[candidate] = seed
            exchange_from_parent[candidate] = exchange
            queue.append((candidate, 1))

    layers = {0: 1, 1: len(queue), 2: 0}
    examined_sources = 0
    legal_arcs = 0
    while queue:
        current, distance = queue.popleft()
        if distance > 2:
            continue
        examined_sources += 1
        for candidate, exchange, (profile, flags, psi) in (
            legal_neighbours(current)
        ):
            legal_arcs += 1
            if psi < seed_psi or flags > 0:
                path = []
                cursor = current
                while cursor != seed:
                    path.append(exchange_from_parent[cursor])
                    cursor = predecessor[cursor]
                path.reverse()
                path.append(exchange)
                return {
                    "status": "ESCAPES",
                    "step": row["step"],
                    "seed_psi": seed_psi,
                    "distance": distance + 1,
                    "escape_exchanges_local_positions": path,
                    "endpoint_psi": psi,
                    "endpoint_flags": flags,
                    "safe_layer_sizes_before_escape": layers,
                    "safe_sources_examined": examined_sources,
                    "legal_arcs_examined": legal_arcs,
                }
            if (
                distance < 2
                and psi == seed_psi
                and flags == 0
                and candidate not in predecessor
            ):
                predecessor[candidate] = current
                exchange_from_parent[candidate] = exchange
                queue.append((candidate, distance + 1))
                layers[distance + 1] += 1

    return {
        "status": "RADIUS_THREE_COUNTEREXAMPLE",
        "step": row["step"],
        "seed_psi": seed_psi,
        "safe_layer_sizes": layers,
        "safe_sources_examined": examined_sources,
        "legal_arcs_examined": legal_arcs,
    }


for line in sys.stdin:
    row = json.loads(line)
    if row["status"] == "ROOT_DONE":
        print(json.dumps(row, sort_keys=True), flush=True)
        continue
    if row["status"] != "EXACT_AUGMENTED_TRAP":
        continue
    if model is None:
        initialize(row)
    result = audit(row)
    print(json.dumps(result, sort_keys=True), flush=True)
    if result["status"] == "RADIUS_THREE_COUNTEREXAMPLE":
        raise SystemExit(1)
