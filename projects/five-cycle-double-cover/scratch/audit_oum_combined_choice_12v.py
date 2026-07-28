#!/usr/bin/env python3
"""Exact all-flow/all-potential Oum audit on the rigid 12-vertex graph.

The program is standard-library only.  It enumerates one representative
of every nowhere-zero F_2^3-flow orbit under GL(3,2), exhausts the
translation-gauged compatible-potential affine space for each flow, and
tests the exact five-colour/R5 criterion through the three equivalent
nonco-occurrence packings.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path


GRAPH6 = "K??FEaKR@oE_"
VERTICES = 12
EDGES = (
    (0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 9),
    (2, 6), (2, 10), (2, 11), (3, 7), (3, 10), (3, 11),
    (4, 8), (4, 9), (4, 10), (5, 8), (5, 9), (5, 11),
)
ROOT_EDGES = (0, 1, 2)
ALL_EDGES = (1 << len(EDGES)) - 1
PAIRS = tuple(combinations(range(8), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
RIGID_FLOW = (
    1, 2, 3, 4, 7, 3, 5, 3, 6, 5, 7, 2, 5, 1, 4, 6, 2, 4,
)
JAEGER_TREES = (
    (1, 2, 3, 4, 7, 8, 11, 14, 15, 16, 17),
    (0, 3, 4, 5, 6, 8, 9, 12, 13, 14, 17),
    (0, 1, 2, 5, 6, 7, 9, 11, 12, 13, 16),
)
TAIT_FLOW = (
    1, 2, 3, 3, 1, 2, 2, 1, 3, 3, 2, 1, 2, 1, 3, 1, 3, 2,
)
SUCCESS_JAEGER_FLOW = tuple(
    ((value & 1).bit_count() % 2)
    | (((value & 2).bit_count() % 2) << 1)
    | (((value & 7).bit_count() % 2) << 2)
    for value in TAIT_FLOW
)
SUCCESS_JAEGER_TREES = (
    (0, 1, 2, 3, 5, 6, 7, 8, 10, 12, 17),
    (0, 1, 4, 5, 6, 7, 9, 11, 12, 13, 15),
    (2, 3, 4, 8, 9, 10, 11, 13, 14, 15, 16),
)


def incidence() -> tuple[tuple[int, ...], ...]:
    answer: list[list[int]] = [[] for _ in range(VERTICES)]
    for edge, (left, right) in enumerate(EDGES):
        answer[left].append(edge)
        answer[right].append(edge)
    assert all(len(row) == 3 for row in answer)
    return tuple(tuple(row) for row in answer)


INCIDENCE = incidence()


def binary_cycles() -> tuple[int, ...]:
    """Enumerate the binary cycle space directly from vertex parity."""
    result = []
    for mask in range(1 << len(EDGES)):
        if all(
            sum((mask >> edge) & 1 for edge in INCIDENCE[vertex]) % 2 == 0
            for vertex in range(VERTICES)
        ):
            result.append(mask)
    assert len(result) == 128
    return tuple(result)


def root_pattern(mask: int) -> tuple[int, int, int]:
    return tuple((mask >> edge) & 1 for edge in ROOT_EDGES)


def flow_from_cycles(first: int, second: int, third: int) -> tuple[int, ...]:
    return tuple(
        ((first >> edge) & 1)
        | (((second >> edge) & 1) << 1)
        | (((third >> edge) & 1) << 2)
        for edge in range(len(EDGES))
    )


def residual_transform(value: int, translate_four_by: int) -> int:
    """A GL(3,2) map fixing 1,2,3 and sending 4 to 4+k."""
    return (value & 3) ^ ((4 ^ translate_four_by) if value & 4 else 0)


def normalized_flow_orbits() -> tuple[tuple[int, ...], ...]:
    """Return exactly one representative of every GL(3,2)-flow orbit."""
    cycles = binary_cycles()
    first_rows = tuple(mask for mask in cycles if root_pattern(mask) == (1, 0, 1))
    second_rows = tuple(mask for mask in cycles if root_pattern(mask) == (0, 1, 1))
    third_rows = tuple(mask for mask in cycles if root_pattern(mask) == (0, 0, 0))
    assert tuple(map(len, (first_rows, second_rows, third_rows))) == (32, 32, 32)

    normalized = []
    representatives: set[tuple[int, ...]] = set()
    for first in first_rows:
        for second in second_rows:
            union = first | second
            for third in third_rows:
                if union | third != ALL_EDGES:
                    continue
                flow = flow_from_cycles(first, second, third)
                assert all(flow)
                assert all(
                    flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0
                    for row in INCIDENCE
                )
                normalized.append(flow)
                orbit_rows = tuple(
                    tuple(residual_transform(value, shift) for value in flow)
                    for shift in range(4)
                )
                representatives.add(min(orbit_rows))
    assert len(normalized) == 3_576
    assert len(representatives) == 900
    return tuple(sorted(representatives))


def potential_rows(flow: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    """Build two scalar equations per edge and the t_0=0 gauge."""
    rows: list[tuple[int, int]] = []
    for edge, (left, right) in enumerate(EDGES):
        left_other = next(item for item in INCIDENCE[left] if item != edge)
        right_other = next(item for item in INCIDENCE[right] if item != edge)
        offset = flow[left_other] ^ flow[right_other]
        value = flow[edge]
        orthogonal = tuple(
            functional
            for functional in range(1, 8)
            if (functional & value).bit_count() % 2 == 0
        )
        assert len(orthogonal) == 3
        for functional in orthogonal[:2]:
            mask = 0
            for vertex in (left, right):
                for bit in range(3):
                    if (functional >> bit) & 1:
                        mask ^= 1 << (3 * vertex + bit)
            rhs = (functional & offset).bit_count() % 2
            rows.append((mask, rhs))
    rows.extend((1 << bit, 0) for bit in range(3))
    assert len(rows) == 39
    return tuple(rows)


def rref(rows: tuple[tuple[int, int], ...]) -> dict[int, tuple[int, int]]:
    pivots: dict[int, tuple[int, int]] = {}
    for original_mask, original_rhs in rows:
        mask, rhs = original_mask, original_rhs
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (mask, rhs)
                break
            old_mask, old_rhs = pivots[pivot]
            mask ^= old_mask
            rhs ^= old_rhs
        assert mask or rhs == 0
    return pivots


def assignment_from_free_bits(
    pivots: dict[int, tuple[int, int]],
    free: tuple[int, ...],
    free_bits: int,
) -> int:
    assignment = sum(
        1 << variable
        for index, variable in enumerate(free)
        if (free_bits >> index) & 1
    )
    for pivot in sorted(pivots):
        mask, rhs = pivots[pivot]
        value = ((mask & ((1 << pivot) - 1) & assignment).bit_count() % 2) ^ rhs
        assignment |= value << pivot
    return assignment


def potential_list(assignment: int) -> list[int]:
    return [
        sum(
            ((assignment >> (3 * vertex + bit)) & 1) << bit
            for bit in range(3)
        )
        for vertex in range(VERTICES)
    ]


def labels_from_assignment(
    flow: tuple[int, ...], assignment: int
) -> tuple[tuple[int, int], ...]:
    potentials = potential_list(assignment)
    labels = []
    for edge, (left, right) in enumerate(EDGES):
        left_other = next(item for item in INCIDENCE[left] if item != edge)
        right_other = next(item for item in INCIDENCE[right] if item != edge)
        left_point = potentials[left] ^ flow[left_other]
        right_point = potentials[right] ^ flow[right_other]
        left_pair = tuple(sorted((left_point, left_point ^ flow[edge])))
        right_pair = tuple(sorted((right_point, right_point ^ flow[edge])))
        assert left_pair == right_pair
        labels.append(left_pair)
    return tuple(labels)


def packing_witness(
    used: frozenset[tuple[int, int]],
) -> tuple[str, tuple[tuple[int, ...], ...]] | None:
    missing = tuple(pair for pair in PAIRS if pair not in used)
    for triple in combinations(missing, 3):
        if len(set().union(*map(set, triple))) == 6:
            return "3K2", tuple(tuple(pair) for pair in triple)
    missing_set = frozenset(missing)
    for triangle in combinations(range(8), 3):
        if not all(tuple(sorted(pair)) in missing_set for pair in combinations(triangle, 2)):
            continue
        for edge in missing:
            if set(triangle).isdisjoint(edge):
                return "K3_PLUS_K2", (tuple(triangle), tuple(edge))
    for clique in combinations(range(8), 4):
        if all(tuple(sorted(pair)) in missing_set for pair in combinations(clique, 2)):
            return "K4", (tuple(clique),)
    return None


def k6_witness(used: frozenset[tuple[int, int]]) -> tuple[int, ...] | None:
    for vertices in combinations(range(8), 6):
        if all(tuple(sorted(pair)) in used for pair in combinations(vertices, 2)):
            return vertices
    return None


def span_rank(flow: tuple[int, ...]) -> int:
    basis: list[int] = []
    for original in flow:
        value = original
        for pivot in basis:
            value = min(value, value ^ pivot)
        if value:
            basis.append(value)
            basis.sort(reverse=True)
    return len(basis)


def edge_set_is_forest(edge_indices: tuple[int, ...] | list[int]) -> bool:
    parent = list(range(VERTICES))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in edge_indices:
        left, right = EDGES[edge]
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            return False
        parent[left_root] = right_root
    return True


def forest_functionals(flow: tuple[int, ...]) -> tuple[int, ...]:
    answer = []
    for functional in range(1, 8):
        zero_edges = tuple(
            edge
            for edge, value in enumerate(flow)
            if (functional & value).bit_count() % 2 == 0
        )
        if edge_set_is_forest(zero_edges):
            answer.append(functional)
    return tuple(answer)


def fundamental_completion(tree: tuple[int, ...]) -> int:
    """Return the xor of the fundamental circuits of all cotree edges."""
    assert len(tree) == VERTICES - 1 and edge_set_is_forest(tree)
    tree_set = frozenset(tree)
    tree_incidence: list[list[tuple[int, int]]] = [
        [] for _ in range(VERTICES)
    ]
    for edge in tree:
        left, right = EDGES[edge]
        tree_incidence[left].append((right, edge))
        tree_incidence[right].append((left, edge))

    answer = 0
    for cotree_edge in range(len(EDGES)):
        if cotree_edge in tree_set:
            continue
        start, finish = EDGES[cotree_edge]
        queue = [start]
        predecessor: dict[int, tuple[int, int]] = {start: (-1, -1)}
        for vertex in queue:
            if vertex == finish:
                break
            for other, tree_edge in tree_incidence[vertex]:
                if other not in predecessor:
                    predecessor[other] = (vertex, tree_edge)
                    queue.append(other)
        assert finish in predecessor
        circuit = 1 << cotree_edge
        current = finish
        while current != start:
            previous, tree_edge = predecessor[current]
            circuit ^= 1 << tree_edge
            current = previous
        answer ^= circuit
    return answer


def audit_flow(flow: tuple[int, ...]) -> dict[str, object]:
    rows = potential_rows(flow)
    pivots = rref(rows)
    free = tuple(variable for variable in range(3 * VERTICES) if variable not in pivots)
    successes = 0
    failures = 0
    first_success: dict[str, object] | None = None
    first_failure: dict[str, object] | None = None
    packing_types: Counter[str] = Counter()
    used_pair_counts: Counter[int] = Counter()
    for free_bits in range(1 << len(free)):
        assignment = assignment_from_free_bits(pivots, free, free_bits)
        assert all(
            (mask & assignment).bit_count() % 2 == rhs for mask, rhs in rows
        )
        labels = labels_from_assignment(flow, assignment)
        used = frozenset(labels)
        used_pair_counts[len(used)] += 1
        witness = packing_witness(used)
        if witness is not None:
            successes += 1
            packing_type, packing = witness
            packing_types[packing_type] += 1
            if first_success is None:
                first_success = {
                    "free_bits": free_bits,
                    "potential": potential_list(assignment),
                    "labels": [list(pair) for pair in labels],
                    "packing_type": packing_type,
                    "packing": [list(item) for item in packing],
                }
        else:
            failures += 1
            clique = k6_witness(used)
            # With only 18 graph edges, J cannot contain the 23-edge
            # obstruction K3 join C5.  The order-eight dichotomy therefore
            # forces, and this line directly checks, a K6.
            assert clique is not None
            if first_failure is None:
                first_failure = {
                    "free_bits": free_bits,
                    "potential": potential_list(assignment),
                    "labels": [list(pair) for pair in labels],
                    "k6": list(clique),
                }
    rank = span_rank(flow)
    assert rank in (2, 3)
    forests = forest_functionals(flow)
    return {
        "flow": list(flow),
        "span_rank": rank,
        "forest_zero_functionals": list(forests),
        "forest_zero_functional_rank": span_rank(forests),
        "gl3_orbit_size": 42 if rank == 2 else 168,
        "potential_rank_after_gauge": len(pivots),
        "potential_free_dimension_after_gauge": len(free),
        "gauged_potentials": 1 << len(free),
        "successful_potentials": successes,
        "obstructed_potentials": failures,
        "packing_type_profile": dict(sorted(packing_types.items())),
        "used_pair_count_profile": {
            str(key): value for key, value in sorted(used_pair_counts.items())
        },
        "first_success": first_success,
        "first_obstruction": first_failure,
    }


def main() -> None:
    output = Path("output/oum-combined-choice-12v/all-flow-orbits.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    totals: Counter[str] = Counter()
    free_dimension_profile: Counter[int] = Counter()
    forest_functional_profile: Counter[tuple[int, int]] = Counter()
    forest_status_profile: Counter[tuple[str, int, int]] = Counter()
    flow_status_profile: Counter[str] = Counter()
    potential_status_profile: Counter[str] = Counter()
    for flow in normalized_flow_orbits():
        row = audit_flow(flow)
        rows.append(row)
        orbit_size = int(row["gl3_orbit_size"])
        free_dimension_profile[int(row["potential_free_dimension_after_gauge"])] += 1
        forest_functional_profile[
            (
                len(row["forest_zero_functionals"]),
                int(row["forest_zero_functional_rank"]),
            )
        ] += 1
        totals["gl3_flow_orbits"] += 1
        totals["labeled_nowhere_zero_flows"] += orbit_size
        totals["gauged_flow_potential_pairs"] += (
            orbit_size * int(row["gauged_potentials"])
        )
        totals["successful_gauged_flow_potential_pairs"] += (
            orbit_size * int(row["successful_potentials"])
        )
        totals["obstructed_gauged_flow_potential_pairs"] += (
            orbit_size * int(row["obstructed_potentials"])
        )
        if int(row["successful_potentials"]):
            flow_status_profile["successful_orbits"] += 1
            totals["successful_labeled_flows"] += orbit_size
            flow_status = "successful"
        else:
            flow_status_profile["obstructed_orbits"] += 1
            totals["obstructed_labeled_flows"] += orbit_size
            flow_status = "obstructed"
        forest_status_profile[
            (
                flow_status,
                len(row["forest_zero_functionals"]),
                int(row["forest_zero_functional_rank"]),
            )
        ] += 1
        for key, value in row["packing_type_profile"].items():
            potential_status_profile[key] += orbit_size * int(value)

    line_row = next(
        row
        for row in rows
        if row["span_rank"] == 2
        and row["flow"] == list(TAIT_FLOW)
    )
    rigid_row = next(row for row in rows if row["flow"] == list(RIGID_FLOW))
    assert not rigid_row["successful_potentials"]
    assert set(JAEGER_TREES[0]).intersection(*map(set, JAEGER_TREES[1:])) == set()
    jaeger_rows = []
    for bit, tree in zip((1, 2, 4), JAEGER_TREES, strict=True):
        zero_edges = tuple(
            edge for edge, value in enumerate(RIGID_FLOW) if not (value & bit)
        )
        assert set(zero_edges).issubset(tree)
        completion = fundamental_completion(tree)
        expected = sum(
            1 << edge
            for edge, value in enumerate(RIGID_FLOW)
            if value & bit
        )
        assert completion == expected
        jaeger_rows.append(
            {
                "coordinate_functional": bit,
                "zero_edge_indices": list(zero_edges),
                "spanning_tree_edge_indices": list(tree),
                "spanning_tree_edges": [list(EDGES[edge]) for edge in tree],
                "fundamental_completion_mask": completion,
            }
        )
    assert set(SUCCESS_JAEGER_TREES[0]).intersection(
        *map(set, SUCCESS_JAEGER_TREES[1:])
    ) == set()
    successful_jaeger_rows = []
    for bit, tree in zip((1, 2, 4), SUCCESS_JAEGER_TREES, strict=True):
        zero_edges = tuple(
            edge
            for edge, value in enumerate(SUCCESS_JAEGER_FLOW)
            if not (value & bit)
        )
        assert set(zero_edges).issubset(tree)
        completion = fundamental_completion(tree)
        expected = sum(
            1 << edge
            for edge, value in enumerate(SUCCESS_JAEGER_FLOW)
            if value & bit
        )
        assert completion == expected
        successful_jaeger_rows.append(
            {
                "coordinate_bit": bit,
                "zero_edge_indices": list(zero_edges),
                "spanning_tree_edge_indices": list(tree),
                "fundamental_completion_mask": completion,
            }
        )
    successful_jaeger_audit = audit_flow(SUCCESS_JAEGER_FLOW)
    assert successful_jaeger_audit["successful_potentials"]
    report = {
        "schema": "oum-combined-choice-12v-all-flow-orbits-v1",
        "scope": {
            "graph6": GRAPH6,
            "vertices": VERTICES,
            "edges": [list(edge) for edge in EDGES],
            "flow_quotient": "one representative per GL(3,2) orbit",
            "potential_quotient": "global coordinate translation fixed by t_0=0",
            "success_criterion": (
                "noncooccurrence graph contains 3K2, K3+K2, or K4"
            ),
        },
        "normalization": {
            "binary_cycle_space_size": 128,
            "normalized_flows_before_residual_stabilizer": 3576,
            "residual_stabilizer_size_for_full_span_flows": 4,
        },
        "totals": dict(totals),
        "flow_status_profile": dict(flow_status_profile),
        "potential_packing_profile_weighted_over_labeled_flows": dict(
            potential_status_profile
        ),
        "free_dimension_profile_on_flow_orbits": {
            str(key): value for key, value in sorted(free_dimension_profile.items())
        },
        "forest_zero_functional_profile_on_flow_orbits": {
            f"{count}_functionals_rank_{rank}": value
            for (count, rank), value in sorted(forest_functional_profile.items())
        },
        "forest_zero_profile_by_flow_status": {
            f"{status}_{count}_functionals_rank_{rank}": value
            for (status, count, rank), value in sorted(
                forest_status_profile.items()
            )
        },
        "jaeger_tree_type_fixed_flow_countermodel": {
            "claim_refuted": (
                "Every nowhere-zero flow obtained from three spanning-tree "
                "fundamental completions has a successful compatible potential."
            ),
            "flow": list(RIGID_FLOW),
            "three_spanning_trees_have_empty_common_intersection": True,
            "coordinate_constructions": jaeger_rows,
            "unique_gauged_potential_obstruction": rigid_row["first_obstruction"],
        },
        "explicit_combined_choice_witness": {
            "explanation": (
                "This line-valued flow is a Tait flow.  Its displayed "
                "compatible potential has a successful packing."
            ),
            "flow": line_row["flow"],
            "certificate": line_row["first_success"],
        },
        "explicit_successful_jaeger_tree_choice": {
            "explanation": (
                "An invertible coordinate change sends the Tait values "
                "1,2,3 to 5,6,3.  All three coordinate supports are "
                "fundamental completions of the displayed spanning trees, "
                "whose common intersection is empty."
            ),
            "flow": list(SUCCESS_JAEGER_FLOW),
            "three_spanning_trees_have_empty_common_intersection": True,
            "coordinate_constructions": successful_jaeger_rows,
            "certificate": successful_jaeger_audit["first_success"],
        },
        "flow_orbits": rows,
    }
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({**totals, **flow_status_profile}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
