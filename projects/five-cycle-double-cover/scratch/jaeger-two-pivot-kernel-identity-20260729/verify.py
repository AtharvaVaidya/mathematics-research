#!/usr/bin/env python3
"""Independent check of the neutral-memory two-pivot counterstate."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PORTFOLIO = HERE.parent / "jaeger-lift13-lex-escape-portfolio-20260729"
SEMANTICS = (
    HERE.parent
    / "jaeger-lift13-girth10-augmented-trap-20260729"
    / "independent_verify.py"
)
RAW = PORTFOLIO / "raw/lift13-r65-s211.jsonl"

spec = importlib.util.spec_from_file_location("semantics", SEMANTICS)
assert spec and spec.loader
semantics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(semantics)


def main() -> None:
    rows = [
        json.loads(line)
        for line in RAW.read_text(encoding="utf-8").splitlines()
    ]
    trap = next(
        row for row in rows
        if row["status"] == "EXACT_AUGMENTED_TRAP"
        and row["step"] == 81
    )
    order, edges = semantics.graph6(trap["graph6"])
    root = 65
    spokes = tuple(
        edge for edge, endpoints in enumerate(edges) if root in endpoints
    )
    internal = tuple(
        edge for edge, endpoints in enumerate(edges)
        if root not in endpoints
    )
    assert order == 130 and len(edges) == 195
    assert spokes == (65, 116, 145) and len(internal) == 192
    start = tuple(map(int, trap["state_labels"]))
    first_exchange = (65, 96)
    second_exchange = (64, 63)
    assert not (set(first_exchange) & set(second_exchange))
    assert tuple(start[index] for index in first_exchange) == (0, 1)
    assert tuple(start[index] for index in second_exchange) == (0, 1)
    assert tuple(internal[index] for index in first_exchange) == (66, 97)
    assert tuple(internal[index] for index in second_exchange) == (64, 63)

    def exchange(labels, pair):
        changed = list(labels)
        first, second = pair
        changed[first], changed[second] = (
            changed[second], changed[first]
        )
        return tuple(changed)

    def state_data(labels):
        trees = semantics.build_trees(
            order, edges, internal, spokes, labels
        )
        kernels, profile, flags = semantics.evaluate(
            order, edges, trees
        )
        return {
            "trees": trees,
            "kernels": kernels,
            "kernel_sizes": tuple(map(len, kernels)),
            "profile": profile,
            "flags": flags,
            "psi": (min(profile), sum(map(len, kernels))),
        }

    labels = {
        "start": start,
        "first_only": exchange(start, first_exchange),
        "second_only": exchange(start, second_exchange),
        "both": exchange(
            exchange(start, first_exchange), second_exchange
        ),
    }
    states = {name: state_data(value) for name, value in labels.items()}
    expected = {
        "start": {
            "kernel_sizes": (70, 70, 66),
            "profile": (22, 20, 18, 26, 12, 16, 2),
            "flags": 0,
            "psi": (2, 206),
        },
        "first_only": {
            "kernel_sizes": (70, 70, 66),
            "profile": (22, 20, 18, 26, 12, 16, 2),
            "flags": 0,
            "psi": (2, 206),
        },
        "second_only": {
            "kernel_sizes": (67, 70, 66),
            "profile": (24, 18, 12, 20, 14, 12, 4),
            "flags": 0,
            "psi": (4, 203),
        },
        "both": {
            "kernel_sizes": (69, 70, 66),
            "profile": (24, 20, 16, 22, 12, 14, 2),
            "flags": 0,
            "psi": (2, 205),
        },
    }
    for name, values in expected.items():
        for key, value in values.items():
            assert states[name][key] == value
    assert states["first_only"]["kernels"] == states["start"]["kernels"]
    assert states["first_only"]["psi"] == states["start"]["psi"]
    assert states["second_only"]["psi"] > states["start"]["psi"]
    assert states["both"]["psi"] < states["start"]["psi"]

    pivot_identities = []
    for coordinate, first_insert_local, first_remove_local, (
        second_insert_local,
        second_remove_local,
    ) in (
        (0, first_exchange[0], first_exchange[1], second_exchange),
        (
            1,
            first_exchange[1],
            first_exchange[0],
            (second_exchange[1], second_exchange[0]),
        ),
    ):
        first_insert = internal[first_insert_local]
        first_remove = internal[first_remove_local]
        second_insert = internal[second_insert_local]
        second_remove = internal[second_remove_local]
        tree = states["start"]["trees"][coordinate]
        first_tree = states["first_only"]["trees"][coordinate]
        kernel = states["start"]["kernels"][coordinate]
        first_kernel = states["first_only"]["kernels"][coordinate]
        endpoint_kernel = states["both"]["kernels"][coordinate]
        first_cycle = semantics.fundamental_cycle(
            order, edges, tree, first_insert
        )
        old_second_cycle = semantics.fundamental_cycle(
            order, edges, tree, second_insert
        )
        new_second_cycle = semantics.fundamental_cycle(
            order, edges, first_tree, second_insert
        )
        alpha = int(first_remove in old_second_cycle)
        assert new_second_cycle == (
            old_second_cycle ^ first_cycle
            if alpha else old_second_cycle
        )
        active_first = int(first_remove in kernel)
        active_second = int(second_remove in first_kernel)
        assert first_kernel == (
            kernel ^ first_cycle if active_first else kernel
        )
        predicted_endpoint = (
            kernel
            ^ (old_second_cycle if active_second else frozenset())
            ^ (
                first_cycle
                if active_first ^ (alpha & active_second)
                else frozenset()
            )
        )
        assert endpoint_kernel == predicted_endpoint
        pivot_identities.append(
            {
                "coordinate": coordinate,
                "alpha": alpha,
                "first_active": active_first,
                "second_active_after_first": active_second,
                "first_cycle_length": len(first_cycle),
                "old_second_cycle_length": len(old_second_cycle),
                "new_second_cycle_length": len(new_second_cycle),
            }
        )

    def active_cycle(state_name):
        data = states[state_name]
        inserted = internal[second_exchange[0]]
        removed = internal[second_exchange[1]]
        cycle = semantics.fundamental_cycle(
            order, edges, data["trees"][0], inserted
        )
        kernel = data["kernels"][0]
        assert removed in cycle and removed in kernel
        return cycle, len(cycle & kernel)

    start_cycle, start_intersection = active_cycle("start")
    parent_cycle, parent_intersection = active_cycle("first_only")
    assert (len(start_cycle), start_intersection) == (35, 19)
    assert (len(parent_cycle), parent_intersection) == (25, 13)
    assert len(start_cycle) - 2 * start_intersection == -3
    assert len(parent_cycle) - 2 * parent_intersection == -1

    for state_name in ("start", "first_only"):
        data = states[state_name]
        inserted = internal[second_exchange[1]]
        removed = internal[second_exchange[0]]
        cycle = semantics.fundamental_cycle(
            order, edges, data["trees"][1], inserted
        )
        assert removed in cycle
        assert removed not in data["kernels"][1]

    output = {
        "status": "PASS",
        "root": root,
        "seed": 211,
        "step": 81,
        "disjoint_exchanges": [first_exchange, second_exchange],
        "full_edges": [
            tuple(internal[index] for index in first_exchange),
            tuple(internal[index] for index in second_exchange),
        ],
        "states": {
            name: {
                key: value for key, value in data.items()
                if key not in ("trees", "kernels")
            }
            for name, data in states.items()
        },
        "second_active_cycle_at_start": {
            "length": len(start_cycle),
            "kernel_intersection": start_intersection,
            "kernel_size_change": -3,
        },
        "second_active_cycle_after_first": {
            "length": len(parent_cycle),
            "kernel_intersection": parent_intersection,
            "kernel_size_change": -1,
        },
        "first_exchange_kernel_neutral": True,
        "second_alone_legal_but_lex_higher": True,
        "both_lex_lower": True,
        "two_pivot_identities": pivot_identities,
    }
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
