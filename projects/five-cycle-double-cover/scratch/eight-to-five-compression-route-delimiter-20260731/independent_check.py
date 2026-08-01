#!/usr/bin/env python3
"""Independent reconstruction of the local-rule rigidity witness.

This checker does not import verify.py, does not store its labelled edge
list, uses graph6 decoding rather than encoding, enumerates every scalar
triangle rule, and excludes a six-clique in R5 by direct combination
enumeration.  It is independently structured code, but is still AI-written.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path


G6 = "K`o_kP_COK?F"
BLOCK_WORDS = (
    "012", "013", "014", "015", "023", "024",
    "025", "123", "134", "135", "245", "345",
)


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    values = [ord(char) - 63 for char in record]
    assert 0 <= values[0] < 63
    order = values[0]
    bits: list[int] = []
    for value in values[1:]:
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    assert len(bits) >= needed and all(bit == 0 for bit in bits[needed:])
    edges = []
    position = 0
    for right in range(1, order):
        for left in range(right):
            if bits[position]:
                edges.append((left, right))
            position += 1
    return order, tuple(edges)


def adjacency(order: int, edges: tuple[tuple[int, int], ...]) -> list[list[tuple[int, int]]]:
    rows: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for index, (left, right) in enumerate(edges):
        rows[left].append((right, index))
        rows[right].append((left, index))
    return rows


def tarjan_bridges(order: int, edges: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    rows = adjacency(order, edges)
    discovery = [-1] * order
    low = [-1] * order
    clock = 0
    bridges: list[int] = []

    def dfs(vertex: int, parent_edge: int) -> None:
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        for other, edge in rows[vertex]:
            if edge == parent_edge:
                continue
            if discovery[other] < 0:
                dfs(other, edge)
                low[vertex] = min(low[vertex], low[other])
                if low[other] > discovery[vertex]:
                    bridges.append(edge)
            else:
                low[vertex] = min(low[vertex], discovery[other])

    dfs(0, -1)
    assert all(value >= 0 for value in discovery)
    return tuple(sorted(bridges))


def row_reduce(words: tuple[int, ...], width: int) -> tuple[int, tuple[int, ...]]:
    rows = list(words)
    pivot_row = 0
    pivots: list[int] = []
    # Deliberately use low-to-high pivot order, unlike verify.py.
    for column in range(width):
        selected = next(
            (row for row in range(pivot_row, len(rows)) if (rows[row] >> column) & 1),
            None,
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        for row in range(len(rows)):
            if row != pivot_row and ((rows[row] >> column) & 1):
                rows[row] ^= rows[pivot_row]
        pivots.append(column)
        pivot_row += 1
    assert all(word == 0 for word in rows[pivot_row:])
    return pivot_row, tuple(pivots)


def find_tait_colouring(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[int, ...]:
    rows = adjacency(order, edges)
    colours = [-1] * len(edges)

    def search() -> bool:
        if all(colour >= 0 for colour in colours):
            return True
        best_edge = -1
        best_score = -1
        for edge, (left, right) in enumerate(edges):
            if colours[edge] >= 0:
                continue
            used = {
                colours[item]
                for vertex in (left, right)
                for _, item in rows[vertex]
                if colours[item] >= 0
            }
            if len(used) > best_score:
                best_edge, best_score = edge, len(used)
        left, right = edges[best_edge]
        forbidden = {
            colours[item]
            for vertex in (left, right)
            for _, item in rows[vertex]
            if colours[item] >= 0
        }
        for colour in range(3):
            if colour in forbidden:
                continue
            colours[best_edge] = colour
            if search():
                return True
            colours[best_edge] = -1
        return False

    assert search()
    for row in rows:
        assert {colours[edge] for _, edge in row} == {0, 1, 2}
    return tuple(colours)


def main() -> None:
    order, edges = decode_graph6(G6)
    assert order == 12 and len(edges) == 18 and len(set(edges)) == 18
    rows = adjacency(order, edges)
    assert all(len(row) == 3 for row in rows)
    assert tarjan_bridges(order, edges) == ()

    blocks = tuple(frozenset(map(int, word)) for word in BLOCK_WORDS)
    labels = []
    for left, right in edges:
        label = tuple(sorted(blocks[left] & blocks[right]))
        assert len(label) == 2
        labels.append(label)
    assert set(labels) == set(combinations(range(6), 2))

    for vertex, row in enumerate(rows):
        assert {
            labels[edge] for _, edge in row
        } == set(combinations(sorted(blocks[vertex]), 2))

    flow = tuple(left ^ right for left, right in labels)
    # Reconstruct t as the xor of the three block points without sharing
    # the primary checker's stored potential vector.
    potential = tuple(
        value[0] ^ value[1] ^ value[2]
        for value in (tuple(sorted(block)) for block in blocks)
    )
    for vertex, row in enumerate(rows):
        assert flow[row[0][1]] ^ flow[row[1][1]] ^ flow[row[2][1]] == 0
        for _, edge in row:
            other_edge = next(item for _, item in row if item != edge)
            base = potential[vertex] ^ flow[other_edge]
            assert tuple(sorted((base, base ^ flow[edge]))) == labels[edge]

    # Use reverse lexicographic pair columns, independently of verify.py.
    pair_order = tuple(reversed(tuple(combinations(range(6), 2))))
    pair_index = {pair: index for index, pair in enumerate(pair_order)}
    equations = tuple(
        sum(1 << pair_index[pair] for pair in combinations(sorted(block), 2))
        for block in blocks
    )
    rank, pivots = row_reduce(equations, 15)
    aggregate = 0
    for equation in equations:
        aggregate ^= equation
    assert rank == 10 and aggregate == 0

    # Enumerate all 2^15 scalar pair tables satisfying the twelve local
    # parity equations.
    triangle_rules = {
        table
        for table in range(1 << 15)
        if all((table & equation).bit_count() % 2 == 0 for equation in equations)
    }
    assert len(triangle_rules) == 32

    # Independently enumerate the gauged vertex-potential cuts of K6.
    cut_rules = set()
    for assignment_on_1_through_5 in range(1 << 5):
        bits = (0,) + tuple(
            (assignment_on_1_through_5 >> (vertex - 1)) & 1
            for vertex in range(1, 6)
        )
        table = 0
        for index, (left, right) in enumerate(pair_order):
            if bits[left] ^ bits[right]:
                table |= 1 << index
        cut_rules.add(table)
    assert len(cut_rules) == 32 and triangle_rules == cut_rules

    # Exhaust every 6-subset of the 32 vertices of R5.  There is no
    # six-clique; a displayed five-clique proves the exact maximum.
    r5_six_cliques = 0
    for candidate in combinations(range(32), 6):
        if all((left ^ right).bit_count() == 2 for left, right in combinations(candidate, 2)):
            r5_six_cliques += 1
    assert r5_six_cliques == 0
    five_clique = (0, 3, 5, 9, 17)
    assert all(
        (left ^ right).bit_count() == 2
        for left, right in combinations(five_clique, 2)
    )

    tait = find_tait_colouring(order, edges)
    # Map its three colours to 01, 02, 12 and check FiveCDC semantics.
    target_masks = (0b00011, 0b00101, 0b00110)
    for row in rows:
        assert target_masks[tait[row[0][1]]] ^ target_masks[tait[row[1][1]]] ^ target_masks[tait[row[2][1]]] == 0
    assert all(mask.bit_count() == 2 for mask in target_masks)

    report = {
        "schema": "fivecdc-eight-to-five-local-rule-independent-v1",
        "date": "2026-07-31",
        "graph6_decoded_order": order,
        "graph6_decoded_edges": len(edges),
        "tarjan_bridge_count": 0,
        "inferred_old_pair_types": len(set(labels)),
        "triangle_rank_reverse_columns": rank,
        "triangle_pivots_reverse_columns": list(pivots),
        "triangle_equation_xor": aggregate,
        "scalar_triangle_rules": len(triangle_rules),
        "scalar_cut_rules": len(cut_rules),
        "triangle_rules_equal_cut_rules": True,
        "r5_six_subsets_checked": 906192,
        "r5_six_cliques": r5_six_cliques,
        "r5_five_clique_witness": list(five_clique),
        "independently_found_tait_colouring_graph6_edge_order": list(tait),
        "positive_fivecdc_control": True,
        "scope": "context-free pair rule only; not FiveCDC",
        "status": "PASS",
    }
    expected_path = Path(__file__).with_name("independent-output.json")
    if expected_path.exists():
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        assert report == expected
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
