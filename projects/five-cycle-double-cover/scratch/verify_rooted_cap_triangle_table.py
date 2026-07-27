#!/usr/bin/env python3
"""Exhaustively replay the local tables in rooted-cap-triangle-induction.md."""

from __future__ import annotations

from itertools import combinations, permutations
import json


EDGES = tuple(frozenset(edge) for edge in combinations(range(5), 2))
EDGE_NAME = {edge: "".join(map(str, sorted(edge))) for edge in EDGES}
TAU = (
    frozenset((0, 1)),
    frozenset((0, 2)),
    frozenset((1, 2)),
)
BASE_PAIRS = (
    frozenset((frozenset((1, 2)), frozenset((0, 3)), frozenset((0, 4)))),
    frozenset((frozenset((0, 2)), frozenset((1, 3)), frozenset((1, 4)))),
    frozenset((frozenset((0, 1)), frozenset((2, 3)), frozenset((2, 4)))),
)


def apply(permutation: tuple[int, ...], edge: frozenset[int]) -> frozenset[int]:
    return frozenset(permutation[vertex] for vertex in edge)


def fork_triples() -> set[frozenset[frozenset[int]]]:
    forks: set[frozenset[frozenset[int]]] = set()
    for p, q, r, s, t in permutations(range(5)):
        forks.add(
            frozenset(
                (
                    frozenset((q, r)),
                    frozenset((p, s)),
                    frozenset((p, t)),
                )
            )
        )
    return forks


def main() -> int:
    first, second, third = TAU
    valid = []
    for internal in EDGES:
        effective = (first ^ internal, second ^ internal, third)
        if any(len(edge) != 2 for edge in effective):
            continue
        normalizations = tuple(
            permutation
            for permutation in permutations(range(5))
            if tuple(apply(permutation, edge) for edge in effective) == TAU
        )
        assert len(normalizations) == 2
        valid.append((internal, effective, normalizations))
    assert {row[0] for row in valid} == BASE_PAIRS[0]

    rows = []
    expected_retained = (0, 2, 1)
    for base_index, base_pair in enumerate(BASE_PAIRS):
        forced: set[frozenset[int]] = set()
        for _, _, normalizations in valid:
            for normalization in normalizations:
                inverse = [0] * 5
                for source, target in enumerate(normalization):
                    inverse[target] = source
                forced.update(
                    frozenset(inverse[vertex] for vertex in edge)
                    for edge in base_pair
                )
        retained = tuple(
            index for index, candidate in enumerate(BASE_PAIRS) if candidate <= forced
        )
        assert expected_retained[base_index] in retained
        rows.append(
            {
                "contracted_base_pair": base_index,
                "forced_expanded_labels": sorted(EDGE_NAME[edge] for edge in forced),
                "retained_base_pairs": retained,
            }
        )

    root_triangle_values = sorted(EDGE_NAME[row[0]] for row in valid)
    assert root_triangle_values == ["03", "04", "12"]

    forks = fork_triples()
    assert len(forks) == 30
    common_intersectors = []
    for fork in forks:
        common = frozenset(
            edge for edge in EDGES if all(edge & fork_edge for fork_edge in fork)
        )
        assert len(common) == 2
        common_intersectors.append(
            {
                "fork": sorted(EDGE_NAME[edge] for edge in fork),
                "common_intersectors": sorted(EDGE_NAME[edge] for edge in common),
            }
        )

    for permutation in permutations(range(5)):
        for fork in forks:
            assert frozenset(apply(permutation, edge) for edge in fork) in forks

    result = {
        "schema": "rooted-cap-triangle-table-v2",
        "valid_internal_root_values": root_triangle_values,
        "connector_expansion_rows": rows,
        "fork_triple_count": len(forks),
        "fork_common_intersectors": sorted(
            common_intersectors, key=lambda row: row["fork"]
        ),
        "status": "PASS",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
