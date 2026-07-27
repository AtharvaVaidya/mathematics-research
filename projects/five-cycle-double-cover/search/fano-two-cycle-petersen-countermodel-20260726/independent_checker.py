#!/usr/bin/env python3
"""Independent semantic checker for the Petersen fixed-line countermodel.

This checker deliberately does not import the CNF producer or any project
module.  It verifies graph metadata, the flow, the explicit five-CDC, all
seven line statuses, the K5 contraction proof, and an exhaustive cycle-pair
table directly from the definitions.
"""

from __future__ import annotations

import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
LINES = tuple(
    sorted(
        {
            tuple(sorted((first, second, first ^ second)))
            for first, second in combinations(range(1, 8), 2)
        }
    )
)


def connected(
    order: int,
    edges: tuple[tuple[int, int], ...],
    omitted: int | None = None,
) -> bool:
    adjacency = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        if edge == omitted:
            continue
        adjacency[first].append(second)
        adjacency[second].append(first)
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == order


def has_cycle(
    vertices: set[int], edges: tuple[tuple[int, int], ...]
) -> bool:
    adjacency = {vertex: [] for vertex in vertices}
    for first, second in edges:
        if first in vertices and second in vertices:
            adjacency[first].append(second)
            adjacency[second].append(first)
    seen: set[int] = set()
    for root in vertices:
        if root in seen:
            continue
        stack = [(root, -1)]
        seen.add(root)
        while stack:
            vertex, parent = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor == parent:
                    continue
                if neighbor in seen:
                    return True
                seen.add(neighbor)
                stack.append((neighbor, vertex))
    return False


def girth(order: int, edges: tuple[tuple[int, int], ...]) -> int:
    answer = order + 1
    for omitted, (source, target) in enumerate(edges):
        adjacency = [[] for _ in range(order)]
        for edge, (first, second) in enumerate(edges):
            if edge != omitted:
                adjacency[first].append(second)
                adjacency[second].append(first)
        distance = [-1] * order
        distance[source] = 0
        queue = deque([source])
        while queue and distance[target] < 0:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if distance[neighbor] < 0:
                    distance[neighbor] = distance[vertex] + 1
                    queue.append(neighbor)
        answer = min(answer, distance[target] + 1)
    return answer


def cyclic_connectivity(
    order: int, edges: tuple[tuple[int, int], ...]
) -> int:
    vertices = set(range(order))
    answer = len(edges)
    # Fix vertex 0 in the shore to count every bipartition once.
    for mask in range(1 << (order - 1)):
        shore = {0} | {
            vertex
            for vertex in range(1, order)
            if (mask >> (vertex - 1)) & 1
        }
        other = vertices - shore
        if not other:
            continue
        if not has_cycle(shore, edges) or not has_cycle(other, edges):
            continue
        size = sum(
            (first in shore) != (second in shore)
            for first, second in edges
        )
        answer = min(answer, size)
    return answer


def components(
    order: int,
    edges: tuple[tuple[int, int], ...],
    selected: set[int],
) -> tuple[frozenset[int], ...]:
    adjacency = [[] for _ in range(order)]
    for edge in selected:
        first, second = edges[edge]
        adjacency[first].append(second)
        adjacency[second].append(first)
    unseen = set(range(order))
    output = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        output.append(frozenset(component))
    return tuple(output)


def cut(
    edges: tuple[tuple[int, int], ...], shore: frozenset[int]
) -> tuple[int, ...]:
    return tuple(
        edge
        for edge, (first, second) in enumerate(edges)
        if (first in shore) != (second in shore)
    )


def is_cycle(mask: int, incident: tuple[tuple[int, ...], ...]) -> bool:
    return all(
        sum((mask >> edge) & 1 for edge in row) % 2 == 0
        for row in incident
    )


def defect_distribution(
    cycles: tuple[int, ...],
    factor_edges: set[int],
    factor_components: tuple[frozenset[int], ...],
    edges: tuple[tuple[int, int], ...],
) -> Counter[int]:
    distribution: Counter[int] = Counter()
    for p in cycles:
        for q in cycles:
            if any(
                not (((p >> edge) & 1) or ((q >> edge) & 1))
                for edge in factor_edges
            ):
                continue
            defect = 0
            for position, component in enumerate(factor_components):
                parity = (
                    sum(
                        ((p >> edge) & 1) & ((q >> edge) & 1)
                        for edge in cut(edges, component)
                    )
                    & 1
                )
                defect |= parity << position
            distribution[defect] += 1
    return distribution


def verify_witness(
    p_edges: list[int],
    q_edges: list[int],
    factor_edges: set[int],
    factor_components: tuple[frozenset[int], ...],
    edges: tuple[tuple[int, int], ...],
    incident: tuple[tuple[int, ...], ...],
) -> None:
    p = sum(1 << edge for edge in p_edges)
    q = sum(1 << edge for edge in q_edges)
    assert is_cycle(p, incident)
    assert is_cycle(q, incident)
    assert all(((p >> edge) & 1) or ((q >> edge) & 1) for edge in factor_edges)
    assert all(
        sum(
            ((p >> edge) & 1) & ((q >> edge) & 1)
            for edge in cut(edges, component)
        )
        % 2
        == 0
        for component in factor_components
    )


def binary_rank(vectors: list[int]) -> int:
    pivots: dict[int, int] = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = vector
                break
            vector ^= pivots[pivot]
    return len(pivots)


def main() -> int:
    data = json.loads(
        (HERE / "construction.json").read_text(encoding="utf-8")
    )
    order = data["order"]
    edges = tuple(tuple(edge) for edge in data["edges"])
    flow = tuple(data["flow_values_by_edge"])
    assert order == 10 and len(edges) == 15
    assert all(
        0 <= first < second < order for first, second in edges
    )
    assert len(set(edges)) == len(edges)

    incident_lists = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        incident_lists[first].append(edge)
        incident_lists[second].append(edge)
    incident = tuple(tuple(row) for row in incident_lists)
    assert all(len(row) == 3 for row in incident)
    assert connected(order, edges)
    assert all(connected(order, edges, edge) for edge in range(len(edges)))
    assert girth(order, edges) == 5
    assert cyclic_connectivity(order, edges) == 5

    # Explicit isomorphism to the standard Petersen presentation.
    mapping = {0: 0, 2: 1, 3: 2, 5: 3, 4: 4, 6: 5, 7: 6, 8: 7, 9: 8, 1: 9}
    standard_petersen = {
        tuple(sorted(edge))
        for edge in (
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
            (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
            (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
        )
    }
    assert {
        tuple(sorted((mapping[first], mapping[second])))
        for first, second in edges
    } == standard_petersen

    assert all(1 <= value <= 7 for value in flow)
    assert all(
        flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0
        for row in incident
    )

    cycles = tuple(
        mask for mask in range(1 << len(edges)) if is_cycle(mask, incident)
    )
    assert len(cycles) == 64

    expected_failed_distribution = Counter(
        {
            int(mask, 2): multiplicity
            for masks, multiplicity in (
                (
                    (
                        "00011", "00101", "00110", "01001", "01010",
                        "01100", "10001", "10010", "10100", "11000",
                    ),
                    72,
                ),
                (
                    ("01111", "10111", "11011", "11101", "11110"),
                    48,
                ),
            )
            for mask in masks
        }
    )
    failed_lines = []
    result_rows = []
    for row in data["line_results"]:
        line = tuple(row["line"])
        factor_edges = {
            edge for edge, value in enumerate(flow) if value in line
        }
        factor_components = components(order, edges, factor_edges)
        assert len(factor_components) == row["factor_components"]
        distribution = defect_distribution(
            cycles, factor_edges, factor_components, edges
        )

        if row["status"] == "UNSAT":
            assert len(factor_edges) == 5
            assert all(len(component) == 2 for component in factor_components)
            assert distribution == expected_failed_distribution
            assert distribution[0] == 0
            failed_lines.append(line)

            # Contract the five matching edges and check that the remaining
            # ten edges give each pair of components exactly once: K5.
            owner = {
                vertex: position
                for position, component in enumerate(factor_components)
                for vertex in component
            }
            quotient_edges = [
                tuple(sorted((owner[first], owner[second])))
                for edge, (first, second) in enumerate(edges)
                if edge not in factor_edges
            ]
            assert len(set(quotient_edges)) == 10
            assert set(quotient_edges) == set(combinations(range(5), 2))
        else:
            verify_witness(
                row["p_edge_ids"],
                row["q_edge_ids"],
                factor_edges,
                factor_components,
                edges,
                incident,
            )
            assert distribution[0] > 0

        result_rows.append(
            {
                "covering_pairs": sum(distribution.values()),
                "factor_components": len(factor_components),
                "line": list(line),
                "status": row["status"],
                "zero_defect_pairs": distribution[0],
            }
        )
    assert tuple(failed_lines) == ((1, 2, 3), (1, 6, 7))

    # Self-contained Tait obstruction: enumerate all perfect matchings and
    # verify that every complement is two odd 5-cycles.
    perfect_matchings = []
    for matching in combinations(range(len(edges)), 5):
        endpoints = [
            vertex for edge in matching for vertex in edges[edge]
        ]
        if len(set(endpoints)) == order:
            perfect_matchings.append(matching)
            complement = set(range(len(edges))) - set(matching)
            complement_components = components(order, edges, complement)
            assert sorted(map(len, complement_components)) == [5, 5]
    assert len(perfect_matchings) == 6

    # Classify all possible binary functional projections h.  The factor
    # is the complement of h.  Exactly zero and the six 10-edge 2-factors
    # fail the two-cycle normal form.
    projection_failures = []
    for projection in cycles:
        factor_edges = {
            edge
            for edge in range(len(edges))
            if not ((projection >> edge) & 1)
        }
        factor_components = components(order, edges, factor_edges)
        distribution = defect_distribution(
            cycles, factor_edges, factor_components, edges
        )
        if distribution[0] == 0:
            projection_failures.append(projection)
    two_factors = [
        ((1 << len(edges)) - 1)
        ^ sum(1 << edge for edge in matching)
        for matching in perfect_matchings
    ]
    assert set(projection_failures) == {0, *two_factors}
    assert len(projection_failures) == 7

    # The six nonzero bad projections have rank five, with their XOR as
    # their only dependency.  Consequently a 3-dimensional projection
    # space contains at most three of them, so every Petersen Fano flow
    # has at least four cleanable lines.
    assert binary_rank(two_factors) == 5
    assert not any(
        binary_rank(list(rows)) < 4
        for rows in combinations(two_factors, 4)
    )
    total_xor = 0
    for row in two_factors:
        total_xor ^= row
    assert total_xor == 0

    # Verify the supplied positive five-cycle-double-cover directly.
    cover = data["explicit_five_cdc_edge_ids"]
    assert len(cover) == 5
    assert all(
        is_cycle(sum(1 << edge for edge in cycle), incident)
        for cycle in cover
    )
    assert all(
        sum(edge in cycle for cycle in cover) == 2
        for edge in range(len(edges))
    )

    result = {
        "binary_cycles": len(cycles),
        "bridgeless_edge_deletions": len(edges),
        "cyclic_edge_connectivity": 5,
        "failed_lines": [list(line) for line in failed_lines],
        "five_cdc_verified": True,
        "girth": 5,
        "line_results": result_rows,
        "possible_functional_projections": len(cycles),
        "projection_clean_count": len(cycles) - len(projection_failures),
        "projection_failure_count": len(projection_failures),
        "projection_nonzero_failure_rank": binary_rank(two_factors),
        "perfect_matchings": [list(row) for row in perfect_matchings],
        "schema": "fano-two-cycle-petersen-independent-check-v1",
        "status": "PASS",
    }
    expected = json.loads(
        (HERE / "independent-check.json").read_text(encoding="utf-8")
    )
    assert result == expected
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
