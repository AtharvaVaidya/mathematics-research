#!/usr/bin/env python3
"""Independent local replay for the order-16 closure-no-go star fibre.

This script is deliberately independent of the C++ whole-state enumerator.
It checks the literal graph and one explicit state with seven-plane profile
(4,4,4,4,4,4,4), then exhausts every reciprocal exchange incident with that
state.  It does *not* independently re-enumerate all 953,856 fibre states.
"""

from __future__ import annotations

from collections import Counter
import itertools
import json


GRAPH6 = "O??CA?_ceOGgH_F?AK@P?"
ROOT = 13
OMITTED_LOCAL_MASKS = (8413, 1725442, 363296)
EXPECTED_EDGES = (
    (0, 6), (0, 9), (0, 10),
    (1, 7), (1, 10), (1, 11),
    (2, 8), (2, 12), (2, 15),
    (3, 9), (3, 13), (3, 14),
    (4, 10), (4, 13), (4, 15),
    (5, 11), (5, 12), (5, 13),
    (6, 9), (6, 12),
    (7, 11), (7, 14),
    (8, 14), (8, 15),
)
EXPECTED_PROFILE_H1_THROUGH_H7 = (4, 4, 4, 4, 4, 4, 4)
EXPECTED_NEIGHBOUR_MINIMUM_HISTOGRAM = {2: 22, 4: 3}
EXPECTED_NEIGHBOUR_PROFILE_HISTOGRAM = {
    (2, 2, 2, 4, 2, 4, 2): 1,
    (2, 2, 4, 4, 4, 4, 4): 1,
    (2, 4, 2, 2, 2, 4, 2): 1,
    (2, 4, 4, 2, 2, 4, 2): 2,
    (2, 4, 4, 4, 4, 4, 6): 1,
    (2, 4, 6, 2, 4, 4, 2): 1,
    (2, 6, 4, 4, 4, 4, 2): 1,
    (4, 2, 2, 4, 4, 2, 2): 1,
    (4, 2, 2, 4, 4, 4, 2): 2,
    (4, 2, 4, 4, 2, 2, 2): 1,
    (4, 4, 2, 2, 2, 2, 2): 1,
    (4, 4, 2, 4, 2, 4, 2): 2,
    (4, 4, 2, 4, 4, 4, 2): 1,
    (4, 4, 4, 4, 2, 4, 4): 1,
    (4, 4, 4, 4, 4, 2, 2): 1,
    (4, 4, 4, 4, 4, 2, 4): 2,
    (4, 4, 6, 4, 2, 2, 2): 1,
    (6, 4, 2, 4, 4, 4, 2): 1,
    (4, 4, 4, 4, 4, 4, 4): 3,
}


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    order = ord(record[0]) - 63
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    cursor = 0
    edges: list[tuple[int, int]] = []
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def connected(
    order: int,
    edges: tuple[tuple[int, int], ...],
    deleted: frozenset[int] = frozenset(),
) -> bool:
    adjacency: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        if edge in deleted:
            continue
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other in adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                stack.append(other)
    return len(seen) == order


def is_tree(
    order: int,
    edges: tuple[tuple[int, int], ...],
    chosen: frozenset[int],
) -> bool:
    return len(chosen) == order - 1 and connected(
        order, edges, frozenset(range(len(edges))) - chosen
    )


def odd_kernel(
    order: int,
    edges: tuple[tuple[int, int], ...],
    tree: frozenset[int],
) -> frozenset[int]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge in tree:
        left, right = edges[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    parent = [-2] * order
    parent_edge = [-1] * order
    parent[0] = -1
    traversal = [0]
    for vertex in traversal:
        for other, edge in adjacency[vertex]:
            if parent[other] == -2:
                parent[other] = vertex
                parent_edge[other] = edge
                traversal.append(other)
    assert len(traversal) == order
    size = [1] * order
    kernel: set[int] = set()
    for vertex in reversed(traversal[1:]):
        if size[vertex] % 2:
            kernel.add(parent_edge[vertex])
        size[parent[vertex]] += size[vertex]
    degrees = [0] * order
    for edge in kernel:
        left, right = edges[edge]
        degrees[left] += 1
        degrees[right] += 1
    assert kernel <= tree
    assert all(degree % 2 == 1 for degree in degrees)
    return frozenset(kernel)


def dot(first: int, second: int) -> int:
    return (first & second).bit_count() % 2


def fano_profile(
    order: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    kernels: tuple[frozenset[int], frozenset[int], frozenset[int]],
) -> tuple[int, ...]:
    flow = tuple(
        sum(
            1 << coordinate
            for coordinate in range(3)
            if edge not in kernels[coordinate]
        )
        for edge in range(len(edges))
    )
    assert all(flow)
    normals = []
    for vertex in range(order):
        candidates = [
            functional
            for functional in range(1, 8)
            if all(
                dot(functional, flow[edge]) == 0
                for edge in incidence[vertex]
            )
        ]
        assert len(candidates) == 1
        normals.append(candidates[0])

    answer = []
    for functional in range(1, 8):
        adjacency: list[list[int]] = [[] for _ in range(order)]
        for edge, (left, right) in enumerate(edges):
            if dot(functional, flow[edge]) == 0:
                adjacency[left].append(right)
                adjacency[right].append(left)
        assert all(len(row) in (1, 3) for row in adjacency)
        transverse = functional & -functional
        unseen = set(range(order))
        bad = 0
        while unseen:
            start = unseen.pop()
            stack = [start]
            component_xor = 0
            while stack:
                vertex = stack.pop()
                if len(adjacency[vertex]) == 1:
                    component_xor ^= dot(
                        normals[vertex] ^ functional, transverse
                    )
                for other in adjacency[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        stack.append(other)
            bad += component_xor
        answer.append(bad)
    return tuple(answer)


def main() -> None:
    order, graph6_edges = parse_graph6(GRAPH6)
    assert order == 16
    assert frozenset(graph6_edges) == frozenset(EXPECTED_EDGES)
    # The explicit masks below use the independently frozen edge order from
    # the kernel-closure package, not graph6 column order.
    edges = EXPECTED_EDGES
    assert len(edges) == 24
    assert len(set(edges)) == len(edges)
    degrees = [0] * order
    incidence_lists: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        assert left != right
        degrees[left] += 1
        degrees[right] += 1
        incidence_lists[left].append(edge)
        incidence_lists[right].append(edge)
    assert degrees == [3] * order
    incidence = tuple(tuple(row) for row in incidence_lists)
    for count in range(3):
        for deleted in itertools.combinations(range(len(edges)), count):
            assert connected(order, edges, frozenset(deleted))

    spokes = tuple(incidence[ROOT])
    internal = tuple(
        edge for edge in range(len(edges)) if edge not in spokes
    )
    assert spokes == (10, 13, 17)
    assert len(internal) == 21
    all_internal = (1 << len(internal)) - 1
    omitted = OMITTED_LOCAL_MASKS
    assert omitted[0] ^ omitted[1] ^ omitted[2] == all_internal
    assert not (
        omitted[0] & omitted[1]
        or omitted[0] & omitted[2]
        or omitted[1] & omitted[2]
    )
    assert tuple(mask.bit_count() for mask in omitted) == (7, 7, 7)

    def reconstruct(
        classes: tuple[int, int, int],
    ) -> tuple[
        tuple[frozenset[int], frozenset[int], frozenset[int]],
        tuple[frozenset[int], frozenset[int], frozenset[int]],
    ]:
        trees = []
        kernels = []
        for coordinate in range(3):
            tree = frozenset(
                [spokes[coordinate]]
                + [
                    edge
                    for local, edge in enumerate(internal)
                    if not ((classes[coordinate] >> local) & 1)
                ]
            )
            assert is_tree(order, edges, tree)
            trees.append(tree)
            kernels.append(odd_kernel(order, edges, tree))
        return tuple(trees), tuple(kernels)  # type: ignore[return-value]

    trees, kernels = reconstruct(omitted)
    profile = fano_profile(order, edges, incidence, kernels)
    assert profile == EXPECTED_PROFILE_H1_THROUGH_H7

    neighbour_profiles: Counter[tuple[int, ...]] = Counter()
    candidate_exchanges = 0
    for first in range(3):
        for second in range(first + 1, 3):
            first_locals = [
                local
                for local in range(len(internal))
                if (omitted[first] >> local) & 1
            ]
            second_locals = [
                local
                for local in range(len(internal))
                if (omitted[second] >> local) & 1
            ]
            for first_local in first_locals:
                for second_local in second_locals:
                    candidate_exchanges += 1
                    toggle = (1 << first_local) | (1 << second_local)
                    changed = list(omitted)
                    changed[first] ^= toggle
                    changed[second] ^= toggle
                    try:
                        _, changed_kernels = reconstruct(tuple(changed))
                    except AssertionError:
                        continue
                    neighbour_profiles[
                        fano_profile(
                            order, edges, incidence, changed_kernels
                        )
                    ] += 1

    assert candidate_exchanges == 147
    assert neighbour_profiles == Counter(
        EXPECTED_NEIGHBOUR_PROFILE_HISTOGRAM
    )
    minimum_histogram = Counter(
        {minimum: 0 for minimum in EXPECTED_NEIGHBOUR_MINIMUM_HISTOGRAM}
    )
    for neighbour_profile, multiplicity in neighbour_profiles.items():
        minimum_histogram[min(neighbour_profile)] += multiplicity
    assert dict(minimum_histogram) == EXPECTED_NEIGHBOUR_MINIMUM_HISTOGRAM

    report = {
        "graph6": GRAPH6,
        "root": ROOT,
        "omitted_local_masks": list(omitted),
        "tree_edge_ids": [sorted(tree) for tree in trees],
        "odd_kernel_edge_ids": [sorted(kernel) for kernel in kernels],
        "fano_profile_functionals_1_through_7": list(profile),
        "candidate_reciprocal_exchanges": candidate_exchanges,
        "legal_reciprocal_exchanges": sum(neighbour_profiles.values()),
        "neighbour_minimum_histogram": dict(minimum_histogram),
        "descending_neighbours": minimum_histogram[2],
        "verified_simple_cubic": True,
        "verified_three_edge_connected": True,
        "scope": (
            "independent local replay only; the full 953856-state "
            "plateau theorem is checked by the separate C++ enumerator"
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
