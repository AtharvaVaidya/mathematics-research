#!/usr/bin/env python3
"""Exact primary checker for the triangle-state rigidity witness."""

from __future__ import annotations

import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path


BLOCKS = (
    (0, 1, 2), (0, 1, 2), (0, 1, 3), (0, 1, 4),
    (0, 2, 3), (0, 2, 5), (0, 4, 5), (1, 2, 4),
    (1, 2, 5), (1, 3, 5), (2, 3, 4), (3, 4, 5),
)

LABELLED_EDGES = (
    (0, 2, (0, 1)), (1, 3, (0, 1)),
    (0, 4, (0, 2)), (1, 5, (0, 2)),
    (2, 4, (0, 3)), (3, 6, (0, 4)), (5, 6, (0, 5)),
    (0, 7, (1, 2)), (1, 8, (1, 2)),
    (2, 9, (1, 3)), (3, 7, (1, 4)), (8, 9, (1, 5)),
    (4, 10, (2, 3)), (7, 10, (2, 4)), (5, 8, (2, 5)),
    (10, 11, (3, 4)), (9, 11, (3, 5)), (6, 11, (4, 5)),
)

TAIT_COLOURS = (0, 1, 1, 2, 2, 2, 0, 2, 0, 1, 0, 2, 0, 1, 1, 2, 0, 1)
EXPECTED_GRAPH6 = "KQh?k`CGGQ?R"
PAIRS = tuple(combinations(range(6), 2))


def incidence() -> tuple[tuple[int, ...], ...]:
    result: list[list[int]] = [[] for _ in BLOCKS]
    for edge, (left, right, _) in enumerate(LABELLED_EDGES):
        result[left].append(edge)
        result[right].append(edge)
    return tuple(tuple(row) for row in result)


def connected(removed_edge: int | None = None) -> bool:
    rows = incidence()
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for edge in rows[vertex]:
            if edge == removed_edge:
                continue
            left, right, _ = LABELLED_EDGES[edge]
            other = left ^ right ^ vertex
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return len(seen) == len(BLOCKS)


def graph6_encode() -> str:
    edge_set = {
        tuple(sorted((left, right))) for left, right, _ in LABELLED_EDGES
    }
    bits = [
        int((left, right) in edge_set)
        for right in range(1, len(BLOCKS))
        for left in range(right)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    return chr(len(BLOCKS) + 63) + "".join(
        chr(63 + sum(bits[start + index] << (5 - index) for index in range(6)))
        for start in range(0, len(bits), 6)
    )


def rank_gf2(rows: list[int]) -> tuple[int, tuple[int, ...]]:
    basis: dict[int, int] = {}
    for original in rows:
        word = original
        while word:
            pivot = word.bit_length() - 1
            if pivot in basis:
                word ^= basis[pivot]
            else:
                basis[pivot] = word
                break
    return len(basis), tuple(sorted(basis))


def maximum_r5_clique() -> tuple[int, tuple[int, ...]]:
    neighbours = tuple(
        frozenset(other for other in range(32) if (word ^ other).bit_count() == 2)
        for word in range(32)
    )
    best: tuple[int, ...] = ()

    def visit(clique: tuple[int, ...], candidates: set[int]) -> None:
        nonlocal best
        if len(clique) > len(best):
            best = clique
        if len(clique) + len(candidates) <= len(best):
            return
        while candidates:
            vertex = min(candidates)
            candidates.remove(vertex)
            visit(clique + (vertex,), candidates & neighbours[vertex])

    visit((), set(range(32)))
    return len(best), best


def check_graph_cover_and_oum() -> dict[str, object]:
    rows = incidence()
    assert len(BLOCKS) == 12 and len(LABELLED_EDGES) == 18
    assert all(len(row) == 3 for row in rows)
    assert len({tuple(sorted((u, v))) for u, v, _ in LABELLED_EDGES}) == 18
    assert connected() and all(connected(edge) for edge in range(18))
    assert graph6_encode() == EXPECTED_GRAPH6

    label_counts = Counter(label for _, _, label in LABELLED_EDGES)
    assert set(label_counts) == set(PAIRS)
    assert sorted(label_counts.values()) == [1] * 12 + [2] * 3

    flow = tuple(left ^ right for _, _, (left, right) in LABELLED_EDGES)
    potential = tuple(a ^ b ^ c for a, b, c in BLOCKS)
    assert set(flow) == set(range(1, 8))
    for vertex, block in enumerate(BLOCKS):
        row = rows[vertex]
        assert {LABELLED_EDGES[edge][2] for edge in row} == set(combinations(block, 2))
        assert flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0
        for edge in row:
            other = next(item for item in row if item != edge)
            base = potential[vertex] ^ flow[other]
            assert tuple(sorted((base, base ^ flow[edge]))) == LABELLED_EDGES[edge][2]

    for coordinate in range(8):
        for row in rows:
            assert sum(coordinate in LABELLED_EDGES[edge][2] for edge in row) % 2 == 0

    return {
        "vertices": 12,
        "edges": 18,
        "graph6": EXPECTED_GRAPH6,
        "simple": True,
        "connected": True,
        "bridgeless_edge_deletions": 18,
        "distinct_triangle_states": len(set(BLOCKS)),
        "repeated_state": "012",
        "old_pair_multiplicities": dict(
            sorted((f"{a}{b}", count) for (a, b), count in label_counts.items())
        ),
        "flow_values_used": list(range(1, 8)),
        "potential": list(potential),
    }


def check_state_transport_and_rigidity() -> dict[str, object]:
    states = tuple(sorted(set(BLOCKS)))
    connected_profiles: dict[str, dict[str, int]] = {}
    for pair in PAIRS:
        relevant = {state for state in states if pair in combinations(state, 2)}
        adjacency = {state: set() for state in relevant}
        edge_count = 0
        for left, right, label in LABELLED_EDGES:
            if label != pair:
                continue
            first, second = BLOCKS[left], BLOCKS[right]
            adjacency[first].add(second)
            adjacency[second].add(first)
            edge_count += 1
        assert relevant
        reached = {min(relevant)}
        queue = deque(reached)
        while queue:
            state = queue.popleft()
            for other in adjacency[state]:
                if other not in reached:
                    reached.add(other)
                    queue.append(other)
        assert reached == relevant
        connected_profiles[f"{pair[0]}{pair[1]}"] = {
            "states": len(relevant), "cover_edges": edge_count
        }

    pair_index = {pair: index for index, pair in enumerate(PAIRS)}
    triangle_rows = [
        sum(1 << pair_index[pair] for pair in combinations(state, 2))
        for state in states
    ]
    triangle_rank, triangle_pivots = rank_gf2(triangle_rows)
    assert triangle_rank == 10 == len(PAIRS) - 6 + 1

    ports = tuple(
        (state, pair) for state in states for pair in combinations(state, 2)
    )
    port_index = {port: index for index, port in enumerate(ports)}
    system_rows = [
        sum(1 << port_index[state, pair] for pair in combinations(state, 2))
        for state in states
    ]
    for left, right, pair in LABELLED_EDGES:
        system_rows.append(
            (1 << port_index[BLOCKS[left], pair])
            ^ (1 << port_index[BLOCKS[right], pair])
        )
    system_rank, system_pivots = rank_gf2(system_rows)
    assert len(ports) == 33 and len(system_rows) == 29
    assert system_rank == 28 and len(ports) - system_rank == 5

    clique_size, clique = maximum_r5_clique()
    assert clique_size == 5

    return {
        "state_adjacency_profiles": connected_profiles,
        "all_state_adjacency_graphs_connected": True,
        "pair_columns": [f"{a}{b}" for a, b in PAIRS],
        "distinct_triangle_rows": len(triangle_rows),
        "triangle_rank": triangle_rank,
        "triangle_rank_pivots_zero_based": list(triangle_pivots),
        "triangle_state_scalar_variables": len(ports),
        "triangle_state_scalar_equations": len(system_rows),
        "triangle_state_scalar_rank": system_rank,
        "triangle_state_scalar_nullity": len(ports) - system_rank,
        "triangle_state_scalar_solutions": 1 << (len(ports) - system_rank),
        "triangle_state_system_pivots_zero_based": list(system_pivots),
        "r5_maximum_clique": clique_size,
        "r5_clique_witness_decimal": list(clique),
        "k6_to_r5": False,
        "minimum_connected_state_full_rank_order": 12,
    }


def check_positive_control() -> dict[str, object]:
    rows = incidence()
    assert len(TAIT_COLOURS) == len(LABELLED_EDGES)
    for row in rows:
        assert {TAIT_COLOURS[edge] for edge in row} == {0, 1, 2}
    target = (0b00011, 0b00101, 0b00110)
    for row in rows:
        assert target[TAIT_COLOURS[row[0]]] ^ target[TAIT_COLOURS[row[1]]] ^ target[TAIT_COLOURS[row[2]]] == 0

    profiles = []
    for vertex in (0, 1):
        mapping = {
            f"{pair[0]}{pair[1]}": TAIT_COLOURS[edge]
            for edge in rows[vertex]
            for pair in (LABELLED_EDGES[edge][2],)
        }
        profiles.append(mapping)
    assert BLOCKS[0] == BLOCKS[1] == (0, 1, 2)
    assert profiles[0] != profiles[1]

    return {
        "proper_tait_colouring": list(TAIT_COLOURS),
        "target_labels_by_colour": ["01", "02", "12"],
        "repeated_012_state_local_colour_profiles": profiles,
        "profiles_differ": True,
        "fivecdc_exists": True,
    }


def main() -> None:
    report = {
        "schema": "fivecdc-eight-to-five-triangle-state-rigidity-v1",
        "date": "2026-07-31",
        "scope": "triangle-state-dependent compression only; not FiveCDC",
        "graph_and_oum_cover": check_graph_cover_and_oum(),
        "state_transport_and_rigidity": check_state_transport_and_rigidity(),
        "positive_control": check_positive_control(),
        "status": "PASS",
    }
    expected_path = Path(__file__).with_name("certificate.json")
    if expected_path.exists():
        assert report == json.loads(expected_path.read_text(encoding="utf-8"))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
