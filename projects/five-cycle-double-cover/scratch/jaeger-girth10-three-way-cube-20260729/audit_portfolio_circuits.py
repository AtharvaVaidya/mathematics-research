#!/usr/bin/env python3
"""Audit circuit geometry of all 196 frozen lift-13 two-step escapes."""

from __future__ import annotations

from collections import Counter
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PORTFOLIO = HERE.parent / "jaeger-lift13-lex-escape-portfolio-20260729"
SEMANTICS_PATH = (
    HERE.parent
    / "jaeger-lift13-girth10-augmented-trap-20260729"
    / "independent_verify.py"
)
SPEC = importlib.util.spec_from_file_location("semantics", SEMANTICS_PATH)
assert SPEC and SPEC.loader
semantics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(semantics)


def load(path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def apply_exchange(labels, exchange):
    changed = list(labels)
    first, second = exchange
    changed[first], changed[second] = (
        changed[second], changed[first]
    )
    return tuple(changed)


records = []
for raw_path in sorted((PORTFOLIO / "raw").glob("*.jsonl")):
    raw = load(raw_path)
    traps = {
        int(row["step"]): row for row in raw
        if row["status"] == "EXACT_AUGMENTED_TRAP"
    }
    audit_path = (
        PORTFOLIO
        / "audits"
        / raw_path.name.replace(".jsonl", "-radius3.jsonl")
    )
    audits = [
        row for row in load(audit_path) if row["status"] == "ESCAPES"
    ]
    assert len(traps) == len(audits)
    for audit in audits:
        row = traps[int(audit["step"])]
        order, edges = semantics.graph6(str(row["graph6"]))
        root = int(row["root"])
        spokes = tuple(
            edge for edge, endpoints in enumerate(edges)
            if root in endpoints
        )
        internal = tuple(
            edge for edge, endpoints in enumerate(edges)
            if root not in endpoints
        )
        seed = tuple(map(int, row["state_labels"]))
        path = tuple(
            tuple(map(int, exchange))
            for exchange in audit["escape_exchanges_local_positions"]
        )
        assert len(path) == 2

        def tree_data(labels):
            trees = semantics.build_trees(
                order, edges, internal, spokes, labels
            )
            kernels, profile, flags = semantics.evaluate(
                order, edges, trees
            )
            return trees, kernels, profile, flags

        def exchange_data(labels, exchange):
            trees, kernels, _, _ = tree_data(labels)
            first, second = exchange
            first_coordinate = labels[first]
            second_coordinate = labels[second]
            assert first_coordinate != second_coordinate
            result = []
            for coordinate, inserted_local, removed_local in (
                (first_coordinate, first, second),
                (second_coordinate, second, first),
            ):
                inserted = internal[inserted_local]
                removed = internal[removed_local]
                circuit = semantics.fundamental_cycle(
                    order, edges, trees[coordinate], inserted
                )
                assert removed in circuit
                result.append(
                    (
                        len(circuit),
                        removed in kernels[coordinate],
                        circuit,
                    )
                )
            return tuple(result)

        _, _, seed_profile, seed_flags = tree_data(seed)
        seed_psi = (
            min(seed_profile),
            int(row["kernel_sum"]),
        )
        assert seed_profile == tuple(row["profile"])
        assert seed_flags == 0
        assert seed_psi == tuple(audit["seed_psi"])

        first_data = exchange_data(seed, path[0])
        parent = apply_exchange(seed, path[0])
        _, parent_kernels, parent_profile, parent_flags = tree_data(parent)
        parent_psi = (
            min(parent_profile), sum(map(len, parent_kernels))
        )
        assert parent_flags == 0 and parent_psi == seed_psi

        second_data = exchange_data(parent, path[1])
        endpoint = apply_exchange(parent, path[1])
        _, endpoint_kernels, endpoint_profile, endpoint_flags = tree_data(
            endpoint
        )
        endpoint_psi = (
            min(endpoint_profile), sum(map(len, endpoint_kernels))
        )
        assert endpoint_psi == tuple(audit["endpoint_psi"])
        assert endpoint_flags == int(audit["endpoint_flags"])
        assert endpoint_flags > 0 or endpoint_psi < seed_psi

        disjoint = not set(path[0]) & set(path[1])
        second_alone = None
        changed_second_circuit = None
        if disjoint:
            try:
                second_alone = exchange_data(seed, path[1])
                tree_data(apply_exchange(seed, path[1]))
            except AssertionError:
                second_alone = None
            if second_alone is not None:
                changed_second_circuit = any(
                    before[2] != after[2]
                    for before, after in zip(second_alone, second_data)
                )
        records.append(
            {
                "disjoint": disjoint,
                "first_lengths": tuple(row[0] for row in first_data),
                "first_active": tuple(row[1] for row in first_data),
                "second_lengths": tuple(row[0] for row in second_data),
                "second_active": tuple(row[1] for row in second_data),
                "second_alone_legal": second_alone is not None,
                "changed_second_circuit": changed_second_circuit,
                "terminal_by_lower": endpoint_psi < seed_psi,
                "terminal_by_flags": endpoint_flags > 0,
            }
        )


def histogram(values):
    return {
        str(key): value for key, value in sorted(
            Counter(values).items(), key=lambda item: str(item[0])
        )
    }


summary = {
    "status": "PASS",
    "scope": "196_frozen_sampled_augmented_traps_not_full_state_space",
    "records": len(records),
    "path_sides": 4 * len(records),
    "disjoint_paths": sum(row["disjoint"] for row in records),
    "shared_position_paths": sum(not row["disjoint"] for row in records),
    "first_both_inactive": sum(
        not any(row["first_active"]) for row in records
    ),
    "first_any_active": sum(
        any(row["first_active"]) for row in records
    ),
    "second_any_active": sum(
        any(row["second_active"]) for row in records
    ),
    "minimum_path_side_circuit_length": min(
        length for row in records
        for length in row["first_lengths"] + row["second_lengths"]
    ),
    "minimum_active_path_side_circuit_length": min(
        length for row in records
        for lengths, active in (
            (row["first_lengths"], row["first_active"]),
            (row["second_lengths"], row["second_active"]),
        )
        for length, is_active in zip(lengths, active) if is_active
    ),
    "first_activity_histogram": histogram(
        row["first_active"] for row in records
    ),
    "second_activity_histogram": histogram(
        row["second_active"] for row in records
    ),
    "disjoint_second_alone_legal": sum(
        row["disjoint"] and row["second_alone_legal"]
        for row in records
    ),
    "disjoint_legal_second_circuit_changed": sum(
        row["disjoint"]
        and row["second_alone_legal"]
        and row["changed_second_circuit"]
        for row in records
    ),
    "terminal_by_lower": sum(
        row["terminal_by_lower"] for row in records
    ),
    "terminal_by_flags": sum(
        row["terminal_by_flags"] for row in records
    ),
}
assert summary == {
    "status": "PASS",
    "scope": "196_frozen_sampled_augmented_traps_not_full_state_space",
    "records": 196,
    "path_sides": 784,
    "disjoint_paths": 194,
    "shared_position_paths": 2,
    "first_both_inactive": 181,
    "first_any_active": 15,
    "second_any_active": 196,
    "minimum_path_side_circuit_length": 10,
    "minimum_active_path_side_circuit_length": 10,
    "first_activity_histogram": {
        "(False, False)": 181,
        "(False, True)": 8,
        "(True, False)": 5,
        "(True, True)": 2,
    },
    "second_activity_histogram": {
        "(False, True)": 55,
        "(True, False)": 101,
        "(True, True)": 40,
    },
    "disjoint_second_alone_legal": 144,
    "disjoint_legal_second_circuit_changed": 133,
    "terminal_by_lower": 186,
    "terminal_by_flags": 39,
}
print(json.dumps(summary, indent=2, sort_keys=True))
