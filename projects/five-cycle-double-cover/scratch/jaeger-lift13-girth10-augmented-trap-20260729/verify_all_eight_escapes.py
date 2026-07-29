#!/usr/bin/env python3
"""Exact radius-two replay for the eight sampled augmented traps.

This checker is exhaustive only over the full reciprocal-exchange
neighbourhoods of the eight states recorded in trap-directed-run.jsonl.
It makes no claim to enumerate the graph's complete star-state space.
"""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path

import independent_verify as base


HERE = Path(__file__).resolve().parent
RUN_PATH = HERE / "trap-directed-run.jsonl"

# The paths were found by breadth-first search after the trap run.  Each
# pair is a pair of local internal-edge positions to exchange.
ESCAPE_PATHS = {
    11: ((113, 136), (109, 169)),
    109: ((0, 33), (6, 157)),
    196: ((16, 50), (60, 59)),
    217: ((9, 49), (46, 138)),
    259: ((33, 76), (57, 65)),
    367: ((0, 12), (29, 18)),
    413: ((70, 156), (71, 26)),
    461: ((25, 19), (71, 18)),
}

EXPECTED_EQUAL_LAYER_ONE = {
    11: 107,
    109: 110,
    196: 82,
    217: 120,
    259: 109,
    367: 117,
    413: 101,
    461: 115,
}


def state_data(
    order: int,
    edges: tuple[tuple[int, int], ...],
    internal: tuple[int, ...],
    spokes: tuple[int, int, int],
    labels: tuple[int, ...],
):
    trees = base.build_trees(order, edges, internal, spokes, labels)
    kernels, profile, flags = base.evaluate(order, edges, trees)
    psi = (min(profile), sum(map(len, kernels)))
    return kernels, profile, flags, psi


def enumerate_neighbours(
    order: int,
    edges: tuple[tuple[int, int], ...],
    internal: tuple[int, ...],
    spokes: tuple[int, int, int],
    labels: tuple[int, ...],
):
    rows = []
    candidates = 0
    for first_coordinate, second_coordinate in combinations(range(3), 2):
        for first in range(len(internal)):
            if labels[first] != first_coordinate:
                continue
            for second in range(len(internal)):
                if labels[second] != second_coordinate:
                    continue
                candidates += 1
                changed = list(labels)
                changed[first], changed[second] = (
                    changed[second],
                    changed[first],
                )
                try:
                    kernels, profile, flags, psi = state_data(
                        order,
                        edges,
                        internal,
                        spokes,
                        tuple(changed),
                    )
                except AssertionError:
                    continue
                rows.append(
                    {
                        "local_positions": [first, second],
                        "coordinates": [
                            first_coordinate,
                            second_coordinate,
                        ],
                        "psi": list(psi),
                        "parallel_successful_flags": flags,
                    }
                )
    assert candidates == 3 * 64 * 64
    return rows


def apply_exchange(
    labels: tuple[int, ...], exchange: tuple[int, int]
) -> tuple[int, ...]:
    changed = list(labels)
    first, second = exchange
    assert changed[first] != changed[second]
    changed[first], changed[second] = changed[second], changed[first]
    return tuple(changed)


def main() -> None:
    run = [
        json.loads(line)
        for line in RUN_PATH.read_text(encoding="utf-8").splitlines()
    ]
    traps = [
        row for row in run if row["status"] == "EXACT_AUGMENTED_TRAP"
    ]
    old_traps = [
        row for row in run if row["status"] == "EXACT_OLD_TRAP"
    ]
    assert len(traps) == 8 and len(old_traps) == 2
    assert {row["step"] for row in traps} == set(ESCAPE_PATHS)
    assert all(row["graph6"] == traps[0]["graph6"] for row in traps)
    assert all(row["root"] == 0 for row in traps)

    order, edges = base.graph6(traps[0]["graph6"])
    root = 0
    spokes = tuple(
        edge for edge, endpoints in enumerate(edges) if root in endpoints
    )
    internal = tuple(
        edge for edge, endpoints in enumerate(edges)
        if root not in endpoints
    )
    assert order == 130 and len(internal) == 192 and len(spokes) == 3

    output_rows = []
    total_candidates = 0
    total_legal = 0
    for row in traps:
        step = row["step"]
        labels = tuple(row["state_labels"])
        kernels, profile, flags, psi = state_data(
            order, edges, internal, spokes, labels
        )
        assert profile == tuple(row["profile"])
        assert psi == (row["d_min"], row["kernel_sum"])
        assert flags == row["parallel_successful_flags"] == 0

        neighbourhood = enumerate_neighbours(
            order, edges, internal, spokes, labels
        )
        assert neighbourhood == row["full_neighbourhood"]
        assert len(neighbourhood) == row["legal_neighbours"]
        assert not any(tuple(item["psi"]) < psi
                       for item in neighbourhood)
        assert not any(item["parallel_successful_flags"] > 0
                       for item in neighbourhood)
        equal = sum(
            tuple(item["psi"]) == psi for item in neighbourhood
        )
        assert equal == EXPECTED_EQUAL_LAYER_ONE[step]
        higher = len(neighbourhood) - equal
        total_candidates += 3 * 64 * 64
        total_legal += len(neighbourhood)

        first_exchange, second_exchange = ESCAPE_PATHS[step]
        parent_labels = apply_exchange(labels, first_exchange)
        parent_kernels, parent_profile, parent_flags, parent_psi = (
            state_data(order, edges, internal, spokes, parent_labels)
        )
        assert parent_psi == psi and parent_flags == 0
        endpoint_labels = apply_exchange(
            parent_labels, second_exchange
        )
        endpoint_kernels, endpoint_profile, endpoint_flags, endpoint_psi = (
            state_data(order, edges, internal, spokes, endpoint_labels)
        )
        assert endpoint_psi < psi or endpoint_flags > 0

        output_rows.append(
            {
                "step": step,
                "seed_psi": psi,
                "legal_layer_one_neighbours": len(neighbourhood),
                "equal_psi_layer_one_neighbours": equal,
                "higher_psi_layer_one_neighbours": higher,
                "lower_psi_layer_one_neighbours": 0,
                "parallel_success_layer_one_neighbours": 0,
                "first_exchange_local_positions": first_exchange,
                "first_exchange_full_edges":
                    tuple(internal[index] for index in first_exchange),
                "intermediate_psi": parent_psi,
                "intermediate_flags": parent_flags,
                "second_exchange_local_positions": second_exchange,
                "second_exchange_full_edges":
                    tuple(internal[index] for index in second_exchange),
                "endpoint_psi": endpoint_psi,
                "endpoint_flags": endpoint_flags,
                "escape_is_lower": endpoint_psi < psi,
                "escape_is_parallel_success": endpoint_flags > 0,
                "exact_augmented_escape_distance": 2,
            }
        )

    print(
        json.dumps(
            {
                "status": "PASS",
                "scope":
                    "eight_sampled_traps_not_complete_state_space",
                "sampled_augmented_traps_checked": len(traps),
                "sampled_old_nonaugmented_traps_not_checked":
                    len(old_traps),
                "candidate_exchanges_checked": total_candidates,
                "legal_neighbours_checked": total_legal,
                "all_eight_escape_at_exact_distance_two": True,
                "traps": output_rows,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
