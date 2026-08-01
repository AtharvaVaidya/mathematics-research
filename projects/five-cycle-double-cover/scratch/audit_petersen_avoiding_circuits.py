#!/usr/bin/env python3
"""Complete Petersen audit for the equal-value avoiding-circuit question.

This is a small-order companion to verify_avoiding_circuit_counterexample.py.
It enumerates all 64^3 triples of binary flows on the Petersen graph, retains
all 28,560 triples whose coordinate-wise union is nowhere zero, and tests
every choice of distinct nonzero s,t and every three-edge subset of E_s.

For all 28,560 labelled F_2^3-flows, G-E_t is connected for every t, and
every tested same-value triple is contained in a circuit of G-E_t.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations

from verify_avoiding_circuit_counterexample import decode_graph6


GRAPH6 = "ICOf@pSb?"
VERTICES, EDGES = decode_graph6(GRAPH6)
EDGE_COUNT = len(EDGES)
ALL_EDGES = (1 << EDGE_COUNT) - 1


def active_component_count(edge_mask: int) -> int:
    rows = [[] for _ in range(VERTICES)]
    active: set[int] = set()
    for edge_id, (left, right) in enumerate(EDGES):
        if (edge_mask >> edge_id) & 1:
            rows[left].append(right)
            rows[right].append(left)
            active.add(left)
            active.add(right)
    answer = 0
    while active:
        answer += 1
        root = active.pop()
        queue = [root]
        while queue:
            vertex = queue.pop()
            for other in rows[vertex]:
                if other in active:
                    active.remove(other)
                    queue.append(other)
    return answer


def cycle_basis(edge_mask: int) -> tuple[int, ...]:
    """Return a fundamental binary cycle basis in the original edge IDs."""
    parent = list(range(VERTICES))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    tree_edges = []
    chords = []
    for edge_id, (left, right) in enumerate(EDGES):
        if not ((edge_mask >> edge_id) & 1):
            continue
        root_left, root_right = find(left), find(right)
        if root_left != root_right:
            parent[root_left] = root_right
            tree_edges.append(edge_id)
        else:
            chords.append(edge_id)

    tree = [[] for _ in range(VERTICES)]
    for edge_id in tree_edges:
        left, right = EDGES[edge_id]
        tree[left].append((right, edge_id))
        tree[right].append((left, edge_id))

    basis = []
    for chord in chords:
        start, target = EDGES[chord]
        queue = deque([start])
        predecessor = {start: (-1, -1)}
        while target not in predecessor:
            vertex = queue.popleft()
            for other, edge_id in tree[vertex]:
                if other not in predecessor:
                    predecessor[other] = (vertex, edge_id)
                    queue.append(other)
        word = 1 << chord
        vertex = target
        while vertex != start:
            vertex, edge_id = predecessor[vertex]
            word |= 1 << edge_id
        basis.append(word)
    return tuple(basis)


def cycle_space(edge_mask: int) -> tuple[int, ...]:
    words = [0]
    for vector in cycle_basis(edge_mask):
        words += [word ^ vector for word in words]
    return tuple(words)


def main() -> None:
    assert VERTICES == 10 and EDGE_COUNT == 15
    assert all(
        sum(vertex in edge for edge in EDGES) == 3
        for vertex in range(VERTICES)
    )
    binary_flows = cycle_space(ALL_EDGES)
    assert len(binary_flows) == 64

    # Cache the circuit triples for each t-class deletion.
    circuit_triples: dict[int, frozenset[tuple[int, int, int]]] = {}
    labelled_flows = 0
    tested_triples = 0

    for coordinate_0 in binary_flows:
        for coordinate_1 in binary_flows:
            for coordinate_2 in binary_flows:
                if coordinate_0 | coordinate_1 | coordinate_2 != ALL_EDGES:
                    continue
                labelled_flows += 1
                values = tuple(
                    ((coordinate_0 >> edge_id) & 1)
                    | (((coordinate_1 >> edge_id) & 1) << 1)
                    | (((coordinate_2 >> edge_id) & 1) << 2)
                    for edge_id in range(EDGE_COUNT)
                )
                assert all(1 <= value <= 7 for value in values)

                for t_value in range(1, 8):
                    removed = sum(
                        (values[edge_id] == t_value) << edge_id
                        for edge_id in range(EDGE_COUNT)
                    )
                    remaining = ALL_EDGES ^ removed
                    # Every t-deletion in the complete flow census is connected.
                    assert active_component_count(remaining) == 1

                    if removed not in circuit_triples:
                        covered: set[tuple[int, int, int]] = set()
                        for even_word in cycle_space(remaining)[1:]:
                            if active_component_count(even_word) != 1:
                                continue
                            word_edges = tuple(
                                edge_id
                                for edge_id in range(EDGE_COUNT)
                                if (even_word >> edge_id) & 1
                            )
                            covered.update(combinations(word_edges, 3))
                        circuit_triples[removed] = frozenset(covered)

                    covered = circuit_triples[removed]
                    for s_value in range(1, 8):
                        if s_value == t_value:
                            continue
                        same_value_edges = tuple(
                            edge_id
                            for edge_id, value in enumerate(values)
                            if value == s_value
                        )
                        for prescribed in combinations(same_value_edges, 3):
                            tested_triples += 1
                            assert prescribed in covered

    assert labelled_flows == 28_560
    assert tested_triples == 655_200
    assert len(circuit_triples) == 295
    print("PASS")
    print(f"Petersen graph6: {GRAPH6}")
    print("labelled nowhere-zero F_2^3-flows: 28560/28560")
    print("connected t-deletions: all")
    print("same-value three-edge cases: 655200/655200 have a circuit")


if __name__ == "__main__":
    main()
