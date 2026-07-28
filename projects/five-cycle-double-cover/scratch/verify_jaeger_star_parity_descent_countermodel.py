#!/usr/bin/env python3
"""Independent exact checker for a trapped star-fibre parity state.

This verifies a counterexample to the proposed *monotone exchange-descent
lemma*, not a counterexample to FiveCDC.  The graph and state are hard-coded
so the checker only needs to inspect the at most 3 * 6 * 6 reciprocal
two-tree exchanges incident with the witness.
"""

from __future__ import annotations

import collections
import itertools
import json


GRAPH6 = "M?AA@BORDGEOEOAo?"
ROOT = 0
OMITTED_MASKS = (43146, 132692)
EXPECTED_GENG_INDEX_ZERO_BASED = 244


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    n = ord(record[0]) - 63
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    cursor = 0
    for v in range(1, n):
        for u in range(v):
            if bits[cursor]:
                edges.append((u, v))
            cursor += 1
    return n, tuple(edges)


def is_connected(
    n: int, edges: tuple[tuple[int, int], ...], deleted: frozenset[int]
) -> bool:
    adjacency = [[] for _ in range(n)]
    for edge, (u, v) in enumerate(edges):
        if edge in deleted:
            continue
        adjacency[u].append(v)
        adjacency[v].append(u)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other in adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                stack.append(other)
    return len(seen) == n


def is_tree(n: int, edges: tuple[tuple[int, int], ...], chosen: frozenset[int]) -> bool:
    return len(chosen) == n - 1 and is_connected(n, edges, frozenset(range(len(edges))) - chosen)


def odd_core(
    n: int, edges: tuple[tuple[int, int], ...], tree: frozenset[int]
) -> frozenset[int]:
    """Unique all-vertex-odd subgraph of the given spanning tree."""
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for edge in tree:
        u, v = edges[edge]
        adjacency[u].append((v, edge))
        adjacency[v].append((u, edge))
    parent = [-1] * n
    parent_edge = [-1] * n
    parent[0] = 0
    order = [0]
    for vertex in order:
        for other, edge in adjacency[vertex]:
            if parent[other] >= 0:
                continue
            parent[other] = vertex
            parent_edge[other] = edge
            order.append(other)
    assert len(order) == n
    subtree_size = [1] * n
    answer: set[int] = set()
    for vertex in reversed(order[1:]):
        if subtree_size[vertex] % 2:
            answer.add(parent_edge[vertex])
        subtree_size[parent[vertex]] += subtree_size[vertex]
    degrees = [0] * n
    for edge in answer:
        u, v = edges[edge]
        degrees[u] += 1
        degrees[v] += 1
    assert all(degree % 2 for degree in degrees)
    return frozenset(answer)


def score_and_bad_components(
    n: int,
    edges: tuple[tuple[int, int], ...],
    cores: tuple[frozenset[int], frozenset[int], frozenset[int]],
) -> tuple[int, tuple[tuple[int, ...], ...]]:
    adjacency = [[] for _ in range(n)]
    for edge in cores[2]:
        u, v = edges[edge]
        adjacency[u].append(v)
        adjacency[v].append(u)
    components: list[tuple[int, ...]] = []
    component_of = [-1] * n
    for start in range(n):
        if component_of[start] >= 0:
            continue
        identifier = len(components)
        seen = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            component_of[vertex] = identifier
            for other in adjacency[vertex]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        components.append(tuple(sorted(seen)))
    parity = [0] * len(components)
    for edge in cores[0] & cores[1]:
        u, v = edges[edge]
        first = component_of[u]
        second = component_of[v]
        if first != second:
            parity[first] ^= 1
            parity[second] ^= 1
    bad = tuple(components[index] for index, value in enumerate(parity) if value)
    return len(bad), bad


def fano_profile(
    n: int,
    edges: tuple[tuple[int, int], ...],
    cores: tuple[frozenset[int], frozenset[int], frozenset[int]],
) -> tuple[int, ...]:
    """Seven component-defect counts, in functional order 1,...,7."""

    def dot(first: int, second: int) -> int:
        return (first & second).bit_count() % 2

    flow = tuple(
        sum(1 << coordinate for coordinate in range(3) if edge not in cores[coordinate])
        for edge in range(len(edges))
    )
    assert all(flow)
    rows = tuple(
        tuple(edge for edge, endpoints in enumerate(edges) if vertex in endpoints)
        for vertex in range(n)
    )
    normals = tuple(
        next(
            functional
            for functional in range(1, 8)
            if all(dot(functional, flow[edge]) == 0 for edge in rows[vertex])
        )
        for vertex in range(n)
    )
    answer = []
    for functional in range(1, 8):
        zero_edges = {
            edge for edge, value in enumerate(flow) if dot(functional, value) == 0
        }
        adjacency = [[] for _ in range(n)]
        for edge in zero_edges:
            u, v = edges[edge]
            adjacency[u].append(v)
            adjacency[v].append(u)
        assert all(len(row) in (1, 3) for row in adjacency)
        transverse_point = functional & -functional
        unseen = set(range(n))
        bad = 0
        while unseen:
            start = next(iter(unseen))
            unseen.remove(start)
            stack = [start]
            leaf_xor = 0
            while stack:
                vertex = stack.pop()
                if len(adjacency[vertex]) == 1:
                    leaf_xor ^= dot(
                        normals[vertex] ^ functional, transverse_point
                    )
                for other in adjacency[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        stack.append(other)
            bad += leaf_xor
        answer.append(bad)
    return tuple(answer)


def main() -> None:
    n, edges = parse_graph6(GRAPH6)
    degrees = [0] * n
    for u, v in edges:
        assert u != v
        degrees[u] += 1
        degrees[v] += 1
    assert n == 14 and len(edges) == 21 and degrees == [3] * n
    assert len(set(edges)) == len(edges)

    # Independent exhaustive check that deleting zero, one, or two edges
    # preserves connectivity.
    for count in range(3):
        for deleted in itertools.combinations(range(len(edges)), count):
            assert is_connected(n, edges, frozenset(deleted))

    spokes = tuple(edge for edge, endpoints in enumerate(edges) if ROOT in endpoints)
    internal = tuple(edge for edge in range(len(edges)) if edge not in spokes)
    assert len(spokes) == 3 and len(internal) == 18
    all_internal = (1 << len(internal)) - 1
    omitted = (
        OMITTED_MASKS[0],
        OMITTED_MASKS[1],
        all_internal ^ OMITTED_MASKS[0] ^ OMITTED_MASKS[1],
    )
    assert all(mask.bit_count() == 6 for mask in omitted)
    assert omitted[0] & omitted[1] == omitted[0] & omitted[2] == omitted[1] & omitted[2] == 0

    def trees_and_cores(
        classes: tuple[int, int, int],
    ) -> tuple[
        tuple[frozenset[int], frozenset[int], frozenset[int]],
        tuple[frozenset[int], frozenset[int], frozenset[int]],
    ]:
        trees = []
        cores = []
        for coordinate in range(3):
            tree = frozenset(
                [spokes[coordinate]]
                + [
                    edge
                    for local, edge in enumerate(internal)
                    if not ((classes[coordinate] >> local) & 1)
                ]
            )
            assert is_tree(n, edges, tree)
            trees.append(tree)
            cores.append(odd_core(n, edges, tree))
        return tuple(trees), tuple(cores)  # type: ignore[return-value]

    trees, cores = trees_and_cores(omitted)
    witness_score, bad_components = score_and_bad_components(n, edges, cores)
    assert witness_score == 2
    witness_fano_profile = fano_profile(n, edges, cores)
    assert witness_fano_profile == (2, 4, 2, 2, 0, 6, 2)

    neighbour_scores: collections.Counter[int] = collections.Counter()
    valid_neighbours = 0
    for first in range(3):
        for second in range(first + 1, 3):
            for first_edge in range(len(internal)):
                if not ((omitted[first] >> first_edge) & 1):
                    continue
                for second_edge in range(len(internal)):
                    if not ((omitted[second] >> second_edge) & 1):
                        continue
                    changed = list(omitted)
                    toggle = (1 << first_edge) | (1 << second_edge)
                    changed[first] ^= toggle
                    changed[second] ^= toggle
                    try:
                        _, changed_cores = trees_and_cores(tuple(changed))
                    except AssertionError:
                        continue
                    changed_score, _ = score_and_bad_components(n, edges, changed_cores)
                    valid_neighbours += 1
                    neighbour_scores[changed_score] += 1

    # No incident exchange is neutral or descending.  Therefore this witness
    # is a singleton component of the positive level set score=2 and that
    # component has no exchange edge to a lower level.
    assert valid_neighbours > 0
    assert all(score > witness_score for score in neighbour_scores)

    # This particular fixed-coordinate countermodel is not an obstruction
    # to either symmetric minimum.  The legal (1,2)-exchange of graph edge
    # IDs 4 and 1 makes coordinate functional 1 good immediately.
    local_of_edge = {edge: local for local, edge in enumerate(internal)}
    symmetric_rescue = list(omitted)
    rescue_toggle = (1 << local_of_edge[4]) | (1 << local_of_edge[1])
    symmetric_rescue[1] ^= rescue_toggle
    symmetric_rescue[2] ^= rescue_toggle
    _, rescued_cores = trees_and_cores(tuple(symmetric_rescue))
    rescued_fano_profile = fano_profile(n, edges, rescued_cores)
    assert rescued_fano_profile == (0, 2, 4, 4, 2, 2, 2)

    def edge_rows(indices: frozenset[int] | tuple[int, ...]) -> list[list[int]]:
        return [[edge, *edges[edge]] for edge in sorted(indices)]

    report = {
        "claim_refuted": (
            "every positive fixed-defect component under reciprocal two-tree "
            "exchanges has an edge to a lower defect level"
        ),
        "not_claimed": "this is not a counterexample to FiveCDC",
        "graph6": GRAPH6,
        "geng_Cq_d3_D3_14_zero_based_index": EXPECTED_GENG_INDEX_ZERO_BASED,
        "root": ROOT,
        "edges": edge_rows(tuple(range(len(edges)))),
        "spoke_edge_ids_in_coordinate_order": list(spokes),
        "internal_edge_ids_in_local_bit_order": list(internal),
        "omitted_local_masks": list(omitted),
        "omitted_edge_ids": [
            [internal[local] for local in range(len(internal)) if (mask >> local) & 1]
            for mask in omitted
        ],
        "tree_edge_ids": [sorted(tree) for tree in trees],
        "odd_core_edge_ids": [sorted(core) for core in cores],
        "bad_K2_components": [list(component) for component in bad_components],
        "witness_score": witness_score,
        "witness_fano_profile_functionals_1_through_7": list(
            witness_fano_profile
        ),
        "valid_exchange_neighbours": valid_neighbours,
        "neighbour_score_histogram": dict(sorted(neighbour_scores.items())),
        "symmetric_rescue_exchange": {
            "coordinates": [1, 2],
            "graph_edge_ids": [4, 1],
            "result_fano_profile": list(rescued_fano_profile),
        },
        "verified_simple_cubic": True,
        "verified_three_edge_connected": True,
        "verified_trapped_singleton": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
