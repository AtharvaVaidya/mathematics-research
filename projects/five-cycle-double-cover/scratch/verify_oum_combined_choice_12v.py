#!/usr/bin/env python3
"""Independent verifier for the all-flow Oum audit on K??FEaKR@oE_.

Potential spaces are regenerated without Gaussian elimination: after
fixing t_0=0, all 2^11 binary choices on a fixed spanning tree are
propagated and the remaining edge equations are checked directly.
"""

from __future__ import annotations

from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path


EXPECTED_SHA256 = "41c50f3413262cfb6a382424674edc2e226325f8b444af0f079ad89f5bc8924a"
VERTICES = 12
EDGES = (
    (0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 9),
    (2, 6), (2, 10), (2, 11), (3, 7), (3, 10), (3, 11),
    (4, 8), (4, 9), (4, 10), (5, 8), (5, 9), (5, 11),
)
ALL_EDGES = (1 << len(EDGES)) - 1
ALL_PAIRS = tuple(combinations(range(8), 2))


def graph_incidence() -> tuple[tuple[int, ...], ...]:
    result: list[list[int]] = [[] for _ in range(VERTICES)]
    for edge, (left, right) in enumerate(EDGES):
        result[left].append(edge)
        result[right].append(edge)
    assert all(len(row) == 3 for row in result)
    return tuple(tuple(row) for row in result)


INCIDENCE = graph_incidence()


def is_binary_cycle(mask: int) -> bool:
    return all(
        sum((mask >> edge) & 1 for edge in INCIDENCE[vertex]) % 2 == 0
        for vertex in range(VERTICES)
    )


def independent_flow_orbits() -> tuple[tuple[int, ...], ...]:
    cycles = tuple(mask for mask in range(1 << len(EDGES)) if is_binary_cycle(mask))
    assert len(cycles) == 128
    buckets: dict[tuple[int, int, int], list[int]] = {}
    for pattern in ((1, 0, 1), (0, 1, 1), (0, 0, 0)):
        buckets[pattern] = [
            mask
            for mask in cycles
            if tuple((mask >> edge) & 1 for edge in (0, 1, 2)) == pattern
        ]
        assert len(buckets[pattern]) == 32

    representatives = set()
    normalized = 0
    for first in buckets[(1, 0, 1)]:
        for second in buckets[(0, 1, 1)]:
            for third in buckets[(0, 0, 0)]:
                if first | second | third != ALL_EDGES:
                    continue
                normalized += 1
                flow = tuple(
                    ((first >> edge) & 1)
                    | (((second >> edge) & 1) << 1)
                    | (((third >> edge) & 1) << 2)
                    for edge in range(len(EDGES))
                )
                residual_orbit = tuple(
                    tuple(
                        (value & 3) ^ ((4 ^ shift) if value & 4 else 0)
                        for value in flow
                    )
                    for shift in range(4)
                )
                representatives.add(min(residual_orbit))
    assert normalized == 3_576 and len(representatives) == 900
    return tuple(sorted(representatives))


def spanning_tree_orientation() -> tuple[tuple[int, int, int], ...]:
    seen = {0}
    queue = [0]
    result = []
    for parent in queue:
        for edge in INCIDENCE[parent]:
            left, right = EDGES[edge]
            child = right if left == parent else left
            if child not in seen:
                seen.add(child)
                queue.append(child)
                result.append((parent, child, edge))
    assert len(seen) == VERTICES and len(result) == VERTICES - 1
    return tuple(result)


TREE_ORIENTATION = spanning_tree_orientation()


def edge_offset(flow: tuple[int, ...], edge: int) -> int:
    left, right = EDGES[edge]
    left_other = next(item for item in INCIDENCE[left] if item != edge)
    right_other = next(item for item in INCIDENCE[right] if item != edge)
    return flow[left_other] ^ flow[right_other]


def all_gauged_potentials(flow: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    offsets = tuple(edge_offset(flow, edge) for edge in range(len(EDGES)))
    solutions = []
    for choices in range(1 << (VERTICES - 1)):
        potential = [-1] * VERTICES
        potential[0] = 0
        for index, (parent, child, edge) in enumerate(TREE_ORIENTATION):
            potential[child] = (
                potential[parent]
                ^ offsets[edge]
                ^ (flow[edge] if (choices >> index) & 1 else 0)
            )
        assert all(value >= 0 for value in potential)
        if all(
            (potential[left] ^ potential[right] ^ offsets[edge])
            in (0, flow[edge])
            for edge, (left, right) in enumerate(EDGES)
        ):
            solutions.append(tuple(potential))
    assert solutions
    return tuple(solutions)


def labels(
    flow: tuple[int, ...], potential: tuple[int, ...]
) -> tuple[tuple[int, int], ...]:
    result = []
    for edge, (left, right) in enumerate(EDGES):
        left_other = next(item for item in INCIDENCE[left] if item != edge)
        right_other = next(item for item in INCIDENCE[right] if item != edge)
        left_point = potential[left] ^ flow[left_other]
        right_point = potential[right] ^ flow[right_other]
        left_pair = tuple(sorted((left_point, left_point ^ flow[edge])))
        right_pair = tuple(sorted((right_point, right_point ^ flow[edge])))
        assert left_pair == right_pair
        result.append(left_pair)
    return tuple(result)


def five_colorable(used: frozenset[tuple[int, int]]) -> bool:
    adjacency = [0] * 8
    for left, right in used:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    colors = [-1] * 8

    def recurse(remaining: int) -> bool:
        if not remaining:
            return True
        choices = [vertex for vertex in range(8) if (remaining >> vertex) & 1]
        vertex = max(
            choices,
            key=lambda item: (
                (adjacency[item] & remaining).bit_count(),
                -item,
            ),
        )
        forbidden = {
            colors[other]
            for other in range(8)
            if colors[other] >= 0 and ((adjacency[vertex] >> other) & 1)
        }
        for color in range(5):
            if color not in forbidden:
                colors[vertex] = color
                if recurse(remaining ^ (1 << vertex)):
                    return True
                colors[vertex] = -1
        return False

    return recurse((1 << 8) - 1)


def is_forest(indices: list[int] | tuple[int, ...]) -> bool:
    parent = list(range(VERTICES))

    def find(vertex: int) -> int:
        if parent[vertex] != vertex:
            parent[vertex] = find(parent[vertex])
        return parent[vertex]

    for edge in indices:
        left, right = EDGES[edge]
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            return False
        parent[left_root] = right_root
    return True


def rank(values: list[int]) -> int:
    pivots: dict[int, int] = {}
    for original in values:
        value = original
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    return len(pivots)


def verify_tree_construction(
    construction: dict[str, object], flow: tuple[int, ...]
) -> None:
    rows = construction["coordinate_constructions"]
    trees = []
    for row in rows:
        functional = int(
            row.get("coordinate_functional", row.get("coordinate_bit"))
        )
        tree = tuple(map(int, row["spanning_tree_edge_indices"]))
        trees.append(set(tree))
        assert len(tree) == VERTICES - 1 and is_forest(tree)
        zero = tuple(
            edge
            for edge, value in enumerate(flow)
            if (value & functional).bit_count() % 2 == 0
        )
        assert list(zero) == row["zero_edge_indices"]
        assert set(zero).issubset(tree)
        support = sum(
            1 << edge
            for edge, value in enumerate(flow)
            if (value & functional).bit_count() % 2 == 1
        )
        assert support == row["fundamental_completion_mask"]
        assert is_binary_cycle(support)
        assert all((support >> edge) & 1 for edge in range(len(EDGES)) if edge not in tree)
    assert not set.intersection(*trees)


def verify_literal_certificate(
    flow: tuple[int, ...], certificate: dict[str, object], success: bool
) -> None:
    potential = tuple(map(int, certificate["potential"]))
    assert potential in all_gauged_potentials(flow)
    rebuilt = labels(flow, potential)
    assert [list(pair) for pair in rebuilt] == certificate["labels"]
    colorable = five_colorable(frozenset(rebuilt))
    assert colorable == success
    if not success:
        clique = tuple(map(int, certificate["k6"]))
        used = frozenset(rebuilt)
        assert all(tuple(sorted(pair)) in used for pair in combinations(clique, 2))


def main() -> None:
    path = Path("output/oum-combined-choice-12v/all-flow-orbits.json")
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == EXPECTED_SHA256, (digest, EXPECTED_SHA256)
    report = json.loads(raw)
    assert tuple(map(tuple, report["scope"]["edges"])) == EDGES
    rows = report["flow_orbits"]
    expected_flows = independent_flow_orbits()
    assert tuple(tuple(row["flow"]) for row in rows) == expected_flows

    orbit_profile = Counter()
    free_profile = Counter()
    forest_profile = Counter()
    forest_status_profile = Counter()
    totals = Counter()
    for row, flow in zip(rows, expected_flows, strict=True):
        solutions = all_gauged_potentials(flow)
        outcomes = [
            five_colorable(frozenset(labels(flow, potential)))
            for potential in solutions
        ]
        assert len(solutions) == row["gauged_potentials"]
        assert sum(outcomes) == row["successful_potentials"]
        assert len(outcomes) - sum(outcomes) == row["obstructed_potentials"]
        assert len(solutions) == 1 << int(row["potential_free_dimension_after_gauge"])
        free_profile[int(row["potential_free_dimension_after_gauge"])] += 1

        functionals = [
            functional
            for functional in range(1, 8)
            if is_forest(
                [
                    edge
                    for edge, value in enumerate(flow)
                    if (functional & value).bit_count() % 2 == 0
                ]
            )
        ]
        assert functionals == row["forest_zero_functionals"]
        assert rank(functionals) == row["forest_zero_functional_rank"]
        forest_profile[(len(functionals), rank(functionals))] += 1

        orbit_size = int(row["gl3_orbit_size"])
        orbit_profile["successful_orbits" if any(outcomes) else "obstructed_orbits"] += 1
        forest_status_profile[
            (
                "successful" if any(outcomes) else "obstructed",
                len(functionals),
                rank(functionals),
            )
        ] += 1
        totals["gl3_flow_orbits"] += 1
        totals["labeled_nowhere_zero_flows"] += orbit_size
        totals["gauged_flow_potential_pairs"] += orbit_size * len(outcomes)
        totals["successful_gauged_flow_potential_pairs"] += orbit_size * sum(outcomes)
        totals["obstructed_gauged_flow_potential_pairs"] += orbit_size * (
            len(outcomes) - sum(outcomes)
        )
        totals[
            "successful_labeled_flows" if any(outcomes) else "obstructed_labeled_flows"
        ] += orbit_size
        if row["first_success"] is not None:
            verify_literal_certificate(flow, row["first_success"], True)
        if row["first_obstruction"] is not None:
            verify_literal_certificate(flow, row["first_obstruction"], False)

    assert dict(totals) == report["totals"]
    assert dict(orbit_profile) == report["flow_status_profile"]
    assert {str(key): value for key, value in sorted(free_profile.items())} == report[
        "free_dimension_profile_on_flow_orbits"
    ]
    assert {
        f"{count}_functionals_rank_{dimension}": value
        for (count, dimension), value in sorted(forest_profile.items())
    } == report["forest_zero_functional_profile_on_flow_orbits"]
    assert {
        f"{status}_{count}_functionals_rank_{dimension}": value
        for (status, count, dimension), value in sorted(
            forest_status_profile.items()
        )
    } == report["forest_zero_profile_by_flow_status"]

    bad = report["jaeger_tree_type_fixed_flow_countermodel"]
    bad_flow = tuple(bad["flow"])
    verify_tree_construction(bad, bad_flow)
    verify_literal_certificate(
        bad_flow, bad["unique_gauged_potential_obstruction"], False
    )
    good = report["explicit_successful_jaeger_tree_choice"]
    good_flow = tuple(good["flow"])
    verify_tree_construction(good, good_flow)
    verify_literal_certificate(good_flow, good["certificate"], True)

    print(
        json.dumps(
            {
                "status": "VERIFIED",
                "sha256": digest,
                "flow_orbits": len(rows),
                **report["totals"],
                **report["flow_status_profile"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
