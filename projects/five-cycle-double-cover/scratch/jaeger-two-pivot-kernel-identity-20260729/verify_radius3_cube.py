#!/usr/bin/env python3
"""Check the three-way interaction in the exact order-40 radius-3 path."""

from __future__ import annotations

from itertools import combinations
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = (
    HERE.parent
    / "jaeger-order40-augmented-radius-two-counterexample-20260729"
    / "verify.py"
)
spec = importlib.util.spec_from_file_location("source", SOURCE)
assert spec and spec.loader
source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)


def main() -> None:
    order, edges = source.semantics.graph6(source.GRAPH6)
    spokes = tuple(
        edge for edge, endpoints in enumerate(edges)
        if source.ROOT in endpoints
    )
    internal = tuple(
        edge for edge, endpoints in enumerate(edges)
        if source.ROOT not in endpoints
    )
    seed = source.labels_from_masks(len(internal))
    exchanges = source.ESCAPE_PATH
    assert not any(
        set(first) & set(second)
        for first, second in combinations(exchanges, 2)
    )

    def state_data(labels):
        trees = tuple(
            frozenset(
                [spokes[coordinate]]
                + [
                    internal[local]
                    for local, label in enumerate(labels)
                    if label != coordinate
                ]
            )
            for coordinate in range(3)
        )
        assert all(
            source.semantics.is_tree(order, edges, tree)
            for tree in trees
        )
        kernels, profile, flags = source.semantics.evaluate(
            order, edges, trees
        )
        return {
            "kernel_sizes": tuple(map(len, kernels)),
            "profile": profile,
            "flags": flags,
            "psi": (min(profile), sum(map(len, kernels))),
        }

    observed = {}
    for subset_mask in range(8):
        labels = list(seed)
        for exchange_index, (first, second) in enumerate(exchanges):
            if subset_mask >> exchange_index & 1:
                labels[first], labels[second] = (
                    labels[second], labels[first]
                )
        observed[subset_mask] = state_data(tuple(labels))

    expected = {
        0: ((20, 20, 20), (4, 6, 2, 6, 6, 6, 2), 0, (2, 60)),
        1: ((20, 20, 20), (4, 6, 2, 6, 6, 6, 2), 0, (2, 60)),
        2: ((22, 20, 20), (4, 6, 4, 6, 2, 6, 2), 0, (2, 62)),
        3: ((20, 20, 20), (4, 6, 4, 6, 2, 4, 2), 0, (2, 60)),
        4: ((20, 20, 21), (6, 6, 4, 8, 6, 4, 2), 0, (2, 61)),
        5: ((20, 20, 21), (6, 6, 4, 8, 6, 4, 2), 0, (2, 61)),
        6: ((22, 20, 21), (6, 10, 6, 6, 4, 6, 2), 0, (2, 63)),
        7: ((20, 20, 21), (6, 6, 6, 6, 4, 4, 0), 3, (0, 61)),
    }
    for subset_mask, row in expected.items():
        assert observed[subset_mask] == {
            "kernel_sizes": row[0],
            "profile": row[1],
            "flags": row[2],
            "psi": row[3],
        }
    assert all(
        observed[subset]["flags"] == 0
        and not (observed[subset]["psi"] < observed[0]["psi"])
        for subset in range(7)
    )
    assert (
        observed[7]["flags"] > 0
        or observed[7]["psi"] < observed[0]["psi"]
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "order": order,
                "root": source.ROOT,
                "disjoint_exchanges": exchanges,
                "full_edges": [
                    tuple(internal[index] for index in exchange)
                    for exchange in exchanges
                ],
                "coordinate_pairs_along_path": ((0, 1), (0, 1), (0, 2)),
                "proper_subsets_lower_or_successful": 0,
                "full_triple_successful_flags": observed[7]["flags"],
                "states": observed,
                "conclusion":
                    "three-way interaction_not_pairwise_uncrossing",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
