#!/usr/bin/env python3
"""Independent graph6 reconstruction of the triangle-state no-go."""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path


GRAPH6 = "KQh?k`CGGQ?R"
STATE_WORDS = (
    "012", "012", "013", "014", "023", "025",
    "045", "124", "125", "135", "234", "345",
)


def decode_graph6(text: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    codes = [ord(character) - 63 for character in text]
    order = codes[0]
    assert order < 63
    bits = [
        (code >> shift) & 1
        for code in codes[1:]
        for shift in range(5, -1, -1)
    ]
    needed = order * (order - 1) // 2
    assert all(bit == 0 for bit in bits[needed:])
    position = 0
    edges = []
    for right in range(1, order):
        for left in range(right):
            if bits[position]:
                edges.append((left, right))
            position += 1
    return order, tuple(edges)


def incidence(order: int, edges: tuple[tuple[int, int], ...]) -> list[list[tuple[int, int]]]:
    rows: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append((right, edge))
        rows[right].append((left, edge))
    return rows


def bridges(order: int, edges: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    rows = incidence(order, edges)
    entered = [-1] * order
    low = [-1] * order
    time = 0
    answer: list[int] = []

    def visit(vertex: int, parent_edge: int) -> None:
        nonlocal time
        entered[vertex] = low[vertex] = time
        time += 1
        for other, edge in rows[vertex]:
            if edge == parent_edge:
                continue
            if entered[other] < 0:
                visit(other, edge)
                low[vertex] = min(low[vertex], low[other])
                if low[other] > entered[vertex]:
                    answer.append(edge)
            else:
                low[vertex] = min(low[vertex], entered[other])

    visit(0, -1)
    assert all(item >= 0 for item in entered)
    return tuple(sorted(answer))


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def join(self, left: int, right: int) -> None:
        left, right = self.find(left), self.find(right)
        if left != right:
            self.parent[right] = left


def find_tait(order: int, edges: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    rows = incidence(order, edges)
    colour = [-1] * len(edges)

    def search() -> bool:
        if min(colour) >= 0:
            return True
        candidates = []
        for edge, (left, right) in enumerate(edges):
            if colour[edge] >= 0:
                continue
            forbidden = {
                colour[item]
                for vertex in (left, right)
                for _, item in rows[vertex]
                if colour[item] >= 0
            }
            candidates.append((len(forbidden), edge, forbidden))
        _, edge, forbidden = max(candidates)
        for candidate in range(3):
            if candidate in forbidden:
                continue
            colour[edge] = candidate
            if search():
                return True
            colour[edge] = -1
        return False

    assert search()
    assert all({colour[edge] for _, edge in row} == {0, 1, 2} for row in rows)
    return tuple(colour)


def main() -> None:
    order, edges = decode_graph6(GRAPH6)
    assert order == 12 and len(edges) == 18 and bridges(order, edges) == ()
    rows = incidence(order, edges)
    assert all(len(row) == 3 for row in rows)

    states = tuple(frozenset(map(int, word)) for word in STATE_WORDS)
    edge_labels = tuple(
        tuple(sorted(states[left] & states[right])) for left, right in edges
    )
    assert all(len(label) == 2 for label in edge_labels)
    pair_order = tuple(reversed(tuple(combinations(range(6), 2))))
    assert set(edge_labels) == set(pair_order)
    for vertex, row in enumerate(rows):
        assert {edge_labels[edge] for _, edge in row} == set(combinations(sorted(states[vertex]), 2))

    distinct_states = tuple(sorted(set(states), key=lambda state: tuple(sorted(state))))
    ports = tuple(
        (state, pair)
        for state in distinct_states
        for pair in combinations(sorted(state), 2)
    )
    port_index = {port: index for index, port in enumerate(ports)}
    union = UnionFind(len(ports))
    for edge, (left, right) in enumerate(edges):
        pair = edge_labels[edge]
        union.join(port_index[states[left], pair], port_index[states[right], pair])

    # State transport must leave exactly one equality class for each of
    # the fifteen old pair types.
    roots_by_pair: dict[tuple[int, int], set[int]] = {}
    for index, (_, pair) in enumerate(ports):
        roots_by_pair.setdefault(pair, set()).add(union.find(index))
    assert set(roots_by_pair) == set(pair_order)
    assert all(len(roots) == 1 for roots in roots_by_pair.values())
    equality_classes = {next(iter(roots)) for roots in roots_by_pair.values()}
    assert len(equality_classes) == 15

    pair_index = {pair: index for index, pair in enumerate(pair_order)}
    triangle_equations = tuple(
        sum(1 << pair_index[pair] for pair in combinations(sorted(state), 2))
        for state in distinct_states
    )
    scalar_rules = {
        rule
        for rule in range(1 << 15)
        if all((rule & equation).bit_count() % 2 == 0 for equation in triangle_equations)
    }
    assert len(scalar_rules) == 32

    cuts = set()
    for assignment in range(1 << 5):
        values = (0,) + tuple((assignment >> (vertex - 1)) & 1 for vertex in range(1, 6))
        cut = 0
        for bit, (left, right) in enumerate(pair_order):
            if values[left] ^ values[right]:
                cut |= 1 << bit
        cuts.add(cut)
    assert scalar_rules == cuts and len(cuts) == 32

    six_cliques = 0
    for six_words in combinations(range(32), 6):
        if all((left ^ right).bit_count() == 2 for left, right in combinations(six_words, 2)):
            six_cliques += 1
    assert six_cliques == 0
    five_clique = (0, 3, 5, 9, 17)
    assert all((left ^ right).bit_count() == 2 for left, right in combinations(five_clique, 2))

    tait = find_tait(order, edges)
    target = (0b00011, 0b00101, 0b00110)
    assert all(
        target[tait[row[0][1]]] ^ target[tait[row[1][1]]] ^ target[tait[row[2][1]]] == 0
        for row in rows
    )
    repeated_profiles = []
    for vertex in (0, 1):
        repeated_profiles.append({
            f"{edge_labels[edge][0]}{edge_labels[edge][1]}": tait[edge]
            for _, edge in rows[vertex]
        })
    assert states[0] == states[1] and repeated_profiles[0] != repeated_profiles[1]

    report = {
        "schema": "fivecdc-eight-to-five-triangle-state-independent-v1",
        "date": "2026-07-31",
        "graph6_order": order,
        "graph6_edges": len(edges),
        "tarjan_bridges": 0,
        "distinct_states": len(distinct_states),
        "state_ports": len(ports),
        "transport_equality_classes": len(equality_classes),
        "all_pair_state_graphs_connected": True,
        "scalar_state_rules_after_transport": len(scalar_rules),
        "scalar_cut_rules": len(cuts),
        "state_rules_equal_cuts": True,
        "r5_six_subsets_checked": 906192,
        "r5_six_cliques": six_cliques,
        "r5_five_clique": list(five_clique),
        "tait_colouring_graph6_edge_order": list(tait),
        "repeated_state_profiles_graph6_edge_order": repeated_profiles,
        "profiles_differ": True,
        "positive_fivecdc_control": True,
        "scope": "triangle-state rule only; not FiveCDC",
        "status": "PASS",
    }
    expected_path = Path(__file__).with_name("independent-output.json")
    if expected_path.exists():
        assert report == json.loads(expected_path.read_text(encoding="utf-8"))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
