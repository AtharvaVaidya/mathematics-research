#!/usr/bin/env python3
"""Exact no-go for a universal two-switch disjoint-factor mediator.

The displayed 40-vertex bipartite cubic graph has a Tait-derived D5
flow, disjoint factor pairs P,Q, intersecting P- and Q-circuits A,B,
and roots e in A, g in B.  No state at Kempe distance at most two has
any factor circuit through both roots.  A displayed three-switch path
does rescue them, fixing the exact scope of the counterexample.
"""

from __future__ import annotations

import itertools
import json
from collections import deque

import networkx as nx


EDGES = (
    (0, 28), (0, 31), (0, 35), (1, 21), (1, 25), (1, 39),
    (2, 35), (2, 36), (2, 37), (3, 22), (3, 23), (3, 24),
    (4, 20), (4, 24), (4, 33), (5, 26), (5, 27), (5, 37),
    (6, 25), (6, 28), (6, 34), (7, 22), (7, 36), (7, 38),
    (8, 28), (8, 33), (8, 36), (9, 24), (9, 30), (9, 35),
    (10, 20), (10, 23), (10, 27), (11, 32), (11, 37), (11, 39),
    (12, 29), (12, 32), (12, 34), (13, 29), (13, 30), (13, 38),
    (14, 22), (14, 32), (14, 38), (15, 23), (15, 25), (15, 27),
    (16, 20), (16, 21), (16, 31), (17, 21), (17, 26), (17, 30),
    (18, 29), (18, 31), (18, 39), (19, 26), (19, 33), (19, 34),
)

# Tait colours embedded as 01=03, 02=05, 12=06.
INITIAL = (
    0x05, 0x03, 0x06, 0x03, 0x06, 0x05,
    0x05, 0x06, 0x03, 0x05, 0x03, 0x06,
    0x06, 0x03, 0x05, 0x03, 0x05, 0x06,
    0x05, 0x06, 0x03, 0x06, 0x03, 0x05,
    0x03, 0x06, 0x05, 0x05, 0x06, 0x03,
    0x05, 0x06, 0x03, 0x06, 0x05, 0x03,
    0x05, 0x03, 0x06, 0x06, 0x05, 0x03,
    0x03, 0x05, 0x06, 0x05, 0x03, 0x06,
    0x03, 0x05, 0x06, 0x06, 0x05, 0x03,
    0x03, 0x05, 0x06, 0x06, 0x03, 0x05,
)

P = (1, 4)
Q = (2, 3)
A_EDGES = (
    1, 2, 3, 4, 10, 11, 12, 13, 28,
    29, 31, 32, 46, 47, 48, 50, 51, 53,
)
B_EDGES = (
    0, 2, 4, 5, 6, 7, 9, 11, 12, 14, 16, 17, 18, 19, 21,
    23, 25, 26, 27, 28, 30, 31, 33, 34, 36, 38, 39, 40, 43,
    44, 45, 47, 49, 50, 51, 52, 55, 56, 57, 59,
)
ROOTS = (29, 33)

THREE_SWITCH_PATH = (
    (
        (0, 2),
        (
            1, 2, 3, 4, 10, 11, 12, 13, 28,
            29, 31, 32, 46, 47, 48, 50, 51, 53,
        ),
    ),
    (
        (0, 1),
        (
            0, 1, 3, 5, 9, 10, 16, 17, 18, 19, 21, 23,
            30, 32, 33, 34, 43, 44, 45, 46, 48, 49, 55, 56,
        ),
    ),
    (
        (0, 3),
        (
            1, 2, 3, 4, 6, 8, 10, 11, 12, 14, 15, 17, 19,
            20, 21, 22, 24, 26, 27, 28, 31, 32, 40, 41, 42,
            44, 46, 47, 48, 50, 51, 52, 58, 59,
        ),
    ),
)
FINAL_WITNESS_PAIR = (0, 1)
FINAL_WITNESS_EDGES = (
    0, 2, 4, 5, 7, 8, 9, 11, 12, 13, 15, 16, 18, 20, 22,
    23, 24, 25, 28, 29, 30, 31, 33, 34, 36, 38, 39, 41, 42,
    43, 45, 47, 49, 50, 51, 53, 55, 56, 57, 58,
)

PAIRS = tuple(itertools.combinations(range(5), 2))
LABELS = frozenset(
    (1 << first) | (1 << second) for first, second in PAIRS
)


def mask(edges: tuple[int, ...]) -> int:
    return sum(1 << edge for edge in edges)


def incidence() -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(40)]
    for edge, (left, right) in enumerate(EDGES):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


INCIDENCE = incidence()


def connected_after(
    removed_vertices: frozenset[int] = frozenset(),
    removed_edges: frozenset[int] = frozenset(),
) -> bool:
    remaining = set(range(40)) - set(removed_vertices)
    if not remaining:
        return True
    seen = {min(remaining)}
    queue = list(seen)
    while queue:
        vertex = queue.pop()
        for edge in INCIDENCE[vertex]:
            if edge in removed_edges:
                continue
            left, right = EDGES[edge]
            other = right if left == vertex else left
            if other in remaining and other not in seen:
                seen.add(other)
                queue.append(other)
    return seen == remaining


def validate_graph() -> None:
    assert len(EDGES) == len(set(EDGES)) == 60
    assert all(left != right for left, right in EDGES)
    assert all(len(row) == 3 for row in INCIDENCE)
    assert connected_after()
    assert all(
        connected_after(removed_edges=frozenset((edge,)))
        for edge in range(60)
    )
    assert all(
        connected_after(removed_edges=frozenset((first, second)))
        for first, second in itertools.combinations(range(60), 2)
    )
    assert all(
        connected_after(removed_vertices=frozenset((vertex,)))
        for vertex in range(40)
    )
    assert all(
        connected_after(removed_vertices=frozenset((first, second)))
        for first, second in itertools.combinations(range(40), 2)
    )
    assert all(
        (left < 20) != (right < 20)
        for left, right in EDGES
    )
    graph = nx.Graph()
    graph.add_nodes_from(range(40))
    graph.add_edges_from(EDGES)
    assert not nx.check_planarity(graph)[0]
    assert nx.to_graph6_bytes(graph, header=False).decode("ascii").strip() == (
        "g????????????????????????????????GGGO?B?a@?A@A?"
        "EC??O_C??_?g?GO_?_g????BA???aG?C??S???E_??AG?"
        "O??CCA??SA????GW????H@?????GK???A?GC???"
    )


def validate_state(state: tuple[int, ...]) -> None:
    assert len(state) == len(EDGES)
    assert all(label in LABELS for label in state)
    assert all(len(row) == 3 for row in INCIDENCE)
    assert all(
        state[row[0]] ^ state[row[1]] ^ state[row[2]] == 0
        for row in INCIDENCE
    )


def active_mask(state: tuple[int, ...], pair: tuple[int, int]) -> int:
    first, second = pair
    return sum(
        1 << edge
        for edge, label in enumerate(state)
        if ((label >> first) & 1) ^ ((label >> second) & 1)
    )


def components(selected: int) -> tuple[int, ...]:
    unseen = {
        edge for edge in range(len(EDGES)) if (selected >> edge) & 1
    }
    answer = []
    while unseen:
        queue = [min(unseen)]
        component: set[int] = set()
        while queue:
            edge = queue.pop()
            if edge in component:
                continue
            component.add(edge)
            for vertex in EDGES[edge]:
                queue.extend(
                    other
                    for other in INCIDENCE[vertex]
                    if (selected >> other) & 1 and other not in component
                )
        unseen -= component
        answer.append(sum(1 << edge for edge in component))
    return tuple(sorted(answer))


def factor_circuits(
    state: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], int], ...]:
    return tuple(
        (pair, component)
        for pair in PAIRS
        for component in components(active_mask(state, pair))
    )


def transpose_label(label: int, pair: tuple[int, int]) -> int:
    first, second = pair
    if ((label >> first) & 1) == ((label >> second) & 1):
        return label
    return label ^ (1 << first) ^ (1 << second)


def switch(
    state: tuple[int, ...], pair: tuple[int, int], component: int
) -> tuple[int, ...]:
    answer = tuple(
        transpose_label(label, pair) if (component >> edge) & 1 else label
        for edge, label in enumerate(state)
    )
    validate_state(answer)
    return answer


def root_witness(
    state: tuple[int, ...],
) -> tuple[tuple[int, int], int] | None:
    for pair, component in factor_circuits(state):
        if all((component >> root) & 1 for root in ROOTS):
            return pair, component
    return None


def radius_two() -> tuple[dict[int, set[tuple[int, ...]]], set[tuple[int, ...]]]:
    levels = {0: {INITIAL}}
    seen = {INITIAL}
    for distance in (1, 2):
        next_level = {
            switch(state, pair, component)
            for state in levels[distance - 1]
            for pair, component in factor_circuits(state)
        }
        levels[distance] = next_level - seen
        seen |= next_level
    return levels, seen


def main() -> None:
    validate_graph()
    validate_state(INITIAL)
    assert set(label for label in INITIAL) == {0x03, 0x05, 0x06}
    assert set(P).isdisjoint(Q)
    assert mask(A_EDGES) in components(active_mask(INITIAL, P))
    assert mask(B_EDGES) in components(active_mask(INITIAL, Q))
    assert mask(A_EDGES) & mask(B_EDGES)
    assert ROOTS[0] in A_EDGES
    assert ROOTS[1] in B_EDGES
    assert root_witness(INITIAL) is None

    levels, radius_states = radius_two()
    assert all(root_witness(state) is None for state in radius_states)

    state = INITIAL
    replayed_path = []
    for pair, edge_tuple in THREE_SWITCH_PATH:
        component = mask(edge_tuple)
        assert component in components(active_mask(state, pair))
        state = switch(state, pair, component)
        replayed_path.append(
            {"pair": list(pair), "component_edges": list(edge_tuple)}
        )
    witness = root_witness(state)
    assert witness == (
        FINAL_WITNESS_PAIR,
        mask(FINAL_WITNESS_EDGES),
    )

    print(
        json.dumps(
            {
                "schema": "d5-disjoint-two-switch-no-go-v1",
                "status": "PASS",
                "graph": {
                    "vertices": 40,
                    "edges": 60,
                    "graph6": (
                        "g????????????????????????????????GGGO?B?a@?A@A?"
                        "EC??O_C??_?g?GO_?_g????BA???aG?C??S???E_??AG?"
                        "O??CCA??SA????GW????H@?????GK???A?GC???"
                    ),
                    "simple_connected_cubic_bipartite": True,
                    "edge_connectivity": 3,
                    "vertex_connectivity": 3,
                    "nonplanar": True,
                },
                "initial_labels_hex": [
                    f"{label:02x}" for label in INITIAL
                ],
                "disjoint_factor_witness": {
                    "P": list(P),
                    "Q": list(Q),
                    "A_edges": list(A_EDGES),
                    "B_edges": list(B_EDGES),
                    "intersection_edges": sorted(
                        set(A_EDGES) & set(B_EDGES)
                    ),
                    "roots": list(ROOTS),
                    "root_graph_edges": [
                        list(EDGES[root]) for root in ROOTS
                    ],
                },
                "exhaustive_radius": {
                    "distance_0_states": len(levels[0]),
                    "distance_1_new_states": len(levels[1]),
                    "distance_2_new_states": len(levels[2]),
                    "all_states_through_distance_2": len(radius_states),
                    "root_good_states": 0,
                },
                "three_switch_rescue": {
                    "moves": replayed_path,
                    "witness_pair": list(witness[0]),
                    "witness_edges": list(FINAL_WITNESS_EDGES),
                },
                "conclusion": (
                    "The minimum Kempe distance to a rooted factor "
                    "circuit is exactly three."
                ),
                "scope": (
                    "Refutes only a universal at-most-two-switch "
                    "disjoint-factor mediator lemma, not orbit-rooted "
                    "transitivity or FiveCDC."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
