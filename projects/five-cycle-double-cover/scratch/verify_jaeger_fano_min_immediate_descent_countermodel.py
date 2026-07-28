#!/usr/bin/env python3
"""Exact replay of two positive states obstructing naive descent claims.

The first refutes one-exchange strict descent for the symmetric seven-plane
score d_min.  The second refutes the stronger claim that motion preserving
all three odd kernels always exposes a descending exchange.  Neither is a
countermodel to descent through the full same-level component, and neither
is a counterexample to FiveCDC.
"""

from __future__ import annotations

from collections import Counter
import itertools
import json


GRAPH6 = "O??CA?_ceOGgH_F?AK@P?"
ROOT = 13
# Edge IDs are in the literal graph6 parser order below.  The SAT-produced
# vertex-star fibre assigns the three root spokes to coordinates in this order.
SPOKES = (16, 17, 15)
START = (857601, 1059160, 180390)
NEUTRAL = (792129, 1124632, 180390)
DESCENDED = (267969, 1124632, 704550)
START_PROFILE = (4, 4, 4, 2, 4, 6, 4)
DESCENDED_PROFILE = (2, 2, 2, 2, 4, 6, 0)
# A second state in the same fibre refutes the stronger proposal that
# kernel-inert motion alone always exposes a descending exchange.
EXPOSURE_START = (1722528, 307976, 66647)
EXPOSURE_MIDDLE = (1722504, 308000, 66647)
EXPOSURE_DESCENDED = (1595528, 434976, 66647)
EXPOSURE_PROFILE = (4, 4, 4, 4, 6, 2, 2)
EXPOSURE_MIDDLE_PROFILE = (4, 2, 2, 4, 6, 2, 2)
EXPOSURE_DESCENDED_PROFILE = (6, 4, 4, 4, 4, 4, 0)
EXPECTED_EDGES = (
    (0, 6), (1, 7), (2, 8), (0, 9), (3, 9), (6, 9),
    (0, 10), (1, 10), (4, 10), (1, 11), (5, 11), (7, 11),
    (2, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
    (3, 14), (7, 14), (8, 14), (2, 15), (4, 15), (8, 15),
)
EXPECTED_START_TREES = (
    (1, 2, 3, 4, 5, 6, 7, 8, 11, 13, 14, 16, 18, 20, 23),
    (0, 1, 2, 5, 7, 9, 10, 12, 14, 17, 18, 19, 20, 21, 22),
    (0, 3, 4, 6, 8, 9, 10, 11, 12, 13, 15, 19, 21, 22, 23),
)
EXPECTED_START_KERNELS = (
    (2, 3, 4, 5, 7, 11, 13, 16, 20, 23),
    (0, 1, 2, 5, 7, 9, 14, 17, 18, 22),
    (0, 3, 6, 9, 13, 15, 19, 21, 22, 23),
)
EXPECTED_NEIGHBOUR_PROFILE_HISTOGRAM = {
    (2, 4, 2, 2, 4, 6, 4): 1,
    (2, 4, 6, 2, 4, 4, 2): 2,
    (2, 6, 2, 2, 4, 6, 4): 1,
    (2, 6, 4, 4, 2, 4, 2): 1,
    (4, 2, 4, 2, 4, 4, 2): 1,
    (4, 2, 4, 4, 4, 4, 4): 2,
    (4, 4, 2, 2, 4, 6, 2): 1,
    (4, 4, 4, 2, 4, 4, 2): 1,
    (4, 4, 4, 2, 4, 6, 4): 4,
    (4, 4, 4, 6, 4, 4, 4): 2,
    (4, 6, 4, 4, 4, 4, 4): 1,
    (6, 4, 2, 2, 4, 4, 2): 1,
    (6, 4, 2, 4, 4, 2, 2): 2,
    (6, 4, 4, 2, 4, 4, 2): 1,
    (6, 4, 4, 4, 4, 6, 4): 2,
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
    """Return the unique subset of the tree having odd degree at every vertex."""
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
    subtree_size = [1] * order
    kernel: set[int] = set()
    for vertex in reversed(traversal[1:]):
        if subtree_size[vertex] % 2:
            kernel.add(parent_edge[vertex])
        subtree_size[parent[vertex]] += subtree_size[vertex]
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
    """Compute the exact component-parity defects for h=1,...,7."""
    flow = tuple(
        sum(
            1 << coordinate
            for coordinate in range(3)
            if edge not in kernels[coordinate]
        )
        for edge in range(len(edges))
    )
    assert all(flow)
    normals: list[int] = []
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

    profile: list[int] = []
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
        profile.append(bad)
    return tuple(profile)


def main() -> None:
    order, edges = parse_graph6(GRAPH6)
    assert order == 16
    assert edges == EXPECTED_EDGES
    assert len(edges) == len(set(edges))
    degrees = [0] * order
    incidence_lists: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        assert left < right
        degrees[left] += 1
        degrees[right] += 1
        incidence_lists[left].append(edge)
        incidence_lists[right].append(edge)
    incidence = tuple(tuple(row) for row in incidence_lists)
    assert degrees == [3] * order
    assert set(SPOKES) == set(incidence[ROOT])
    for deleted_count in range(3):
        for deleted in itertools.combinations(
            range(len(edges)), deleted_count
        ):
            assert connected(order, edges, frozenset(deleted))

    internal = tuple(
        edge for edge in range(len(edges)) if edge not in SPOKES
    )
    assert len(internal) == 21
    all_internal = (1 << len(internal)) - 1

    def reconstruct(
        classes: tuple[int, int, int],
    ) -> tuple[
        tuple[frozenset[int], frozenset[int], frozenset[int]],
        tuple[frozenset[int], frozenset[int], frozenset[int]],
    ] | None:
        if (
            classes[0] ^ classes[1] ^ classes[2] != all_internal
            or classes[0] & classes[1]
            or classes[0] & classes[2]
            or classes[1] & classes[2]
            or tuple(mask.bit_count() for mask in classes) != (7, 7, 7)
        ):
            return None
        trees: list[frozenset[int]] = []
        kernels: list[frozenset[int]] = []
        for coordinate in range(3):
            tree = frozenset(
                [SPOKES[coordinate]]
                + [
                    edge
                    for local, edge in enumerate(internal)
                    if not ((classes[coordinate] >> local) & 1)
                ]
            )
            if not is_tree(order, edges, tree):
                return None
            trees.append(tree)
            kernels.append(odd_kernel(order, edges, tree))
        return tuple(trees), tuple(kernels)  # type: ignore[return-value]

    start_data = reconstruct(START)
    assert start_data is not None
    start_trees, start_kernels = start_data
    assert tuple(tuple(sorted(tree)) for tree in start_trees) == (
        EXPECTED_START_TREES
    )
    assert tuple(tuple(sorted(kernel)) for kernel in start_kernels) == (
        EXPECTED_START_KERNELS
    )
    assert fano_profile(
        order, edges, incidence, start_kernels
    ) == START_PROFILE
    assert min(START_PROFILE) == 2

    candidates = 0
    neighbour_profiles: Counter[tuple[int, ...]] = Counter()
    minimum_histogram: Counter[int] = Counter()
    for first in range(3):
        for second in range(first + 1, 3):
            for first_local in range(len(internal)):
                if not ((START[first] >> first_local) & 1):
                    continue
                for second_local in range(len(internal)):
                    if not ((START[second] >> second_local) & 1):
                        continue
                    candidates += 1
                    toggle = (
                        (1 << first_local) | (1 << second_local)
                    )
                    changed = list(START)
                    changed[first] ^= toggle
                    changed[second] ^= toggle
                    changed_data = reconstruct(tuple(changed))
                    if changed_data is None:
                        continue
                    profile = fano_profile(
                        order, edges, incidence, changed_data[1]
                    )
                    neighbour_profiles[profile] += 1
                    minimum_histogram[min(profile)] += 1
    assert candidates == 147
    assert neighbour_profiles == Counter(
        EXPECTED_NEIGHBOUR_PROFILE_HISTOGRAM
    )
    assert minimum_histogram == Counter({2: 18, 4: 5})
    assert not any(
        score < min(START_PROFILE) for score in minimum_histogram
    )

    local_of_edge = {
        edge: local for local, edge in enumerate(internal)
    }

    def apply_exchange(
        classes: tuple[int, int, int],
        first: int,
        second: int,
        first_edge: int,
        second_edge: int,
    ) -> tuple[int, int, int]:
        assert (classes[first] >> local_of_edge[first_edge]) & 1
        assert (classes[second] >> local_of_edge[second_edge]) & 1
        toggle = (
            (1 << local_of_edge[first_edge])
            | (1 << local_of_edge[second_edge])
        )
        changed = list(classes)
        changed[first] ^= toggle
        changed[second] ^= toggle
        return tuple(changed)  # type: ignore[return-value]

    assert apply_exchange(START, 0, 1, 19, 6) == NEUTRAL
    neutral_data = reconstruct(NEUTRAL)
    assert neutral_data is not None
    neutral_profile = fano_profile(
        order, edges, incidence, neutral_data[1]
    )
    assert neutral_profile == START_PROFILE
    # This neutral move is kernel-inert in both changed coordinates, so it
    # changes the packing but leaves the entire flow and all seven defects.
    assert neutral_data[1] == start_kernels

    assert apply_exchange(NEUTRAL, 0, 2, 22, 7) == DESCENDED
    descended_data = reconstruct(DESCENDED)
    assert descended_data is not None
    descended_profile = fano_profile(
        order, edges, incidence, descended_data[1]
    )
    assert descended_profile == DESCENDED_PROFILE
    assert min(descended_profile) == 0

    exposure_data = reconstruct(EXPOSURE_START)
    assert exposure_data is not None
    exposure_profile = fano_profile(
        order, edges, incidence, exposure_data[1]
    )
    assert exposure_profile == EXPOSURE_PROFILE
    assert min(exposure_profile) == 2

    exposure_candidates = 0
    exposure_legal = 0
    exposure_minimum_histogram: Counter[int] = Counter()
    exposure_kernel_inert = 0
    for first in range(3):
        for second in range(first + 1, 3):
            for first_local in range(len(internal)):
                if not (
                    (EXPOSURE_START[first] >> first_local) & 1
                ):
                    continue
                for second_local in range(len(internal)):
                    if not (
                        (EXPOSURE_START[second] >> second_local) & 1
                    ):
                        continue
                    exposure_candidates += 1
                    toggle = (
                        (1 << first_local) | (1 << second_local)
                    )
                    changed = list(EXPOSURE_START)
                    changed[first] ^= toggle
                    changed[second] ^= toggle
                    changed_data = reconstruct(tuple(changed))
                    if changed_data is None:
                        continue
                    exposure_legal += 1
                    changed_profile = fano_profile(
                        order, edges, incidence, changed_data[1]
                    )
                    exposure_minimum_histogram[
                        min(changed_profile)
                    ] += 1
                    exposure_kernel_inert += (
                        changed_data[1] == exposure_data[1]
                    )
    assert exposure_candidates == 147
    assert exposure_legal == 23
    assert exposure_minimum_histogram == Counter({2: 23})
    assert exposure_kernel_inert == 0

    # An active same-level exchange, rather than a kernel-inert exchange,
    # is needed before the descending exchange in this state.
    assert (
        apply_exchange(EXPOSURE_START, 0, 1, 5, 3)
        == EXPOSURE_MIDDLE
    )
    exposure_middle_data = reconstruct(EXPOSURE_MIDDLE)
    assert exposure_middle_data is not None
    exposure_middle_profile = fano_profile(
        order, edges, incidence, exposure_middle_data[1]
    )
    assert exposure_middle_profile == EXPOSURE_MIDDLE_PROFILE
    assert exposure_middle_data[1] != exposure_data[1]
    assert (
        apply_exchange(EXPOSURE_MIDDLE, 0, 1, 20, 12)
        == EXPOSURE_DESCENDED
    )
    exposure_descended_data = reconstruct(EXPOSURE_DESCENDED)
    assert exposure_descended_data is not None
    exposure_descended_profile = fano_profile(
        order, edges, incidence, exposure_descended_data[1]
    )
    assert exposure_descended_profile == EXPOSURE_DESCENDED_PROFILE
    assert min(exposure_descended_profile) == 0

    report = {
        "claim_refuted": (
            "every state with positive symmetric d_min has an immediately "
            "descending reciprocal exchange"
        ),
        "not_refuted": [
            "descent after same-level reciprocal exchanges",
            "the Five-Cycle Double Cover Conjecture",
        ],
        "graph6": GRAPH6,
        "root": ROOT,
        "spoke_edge_ids_in_coordinate_order": list(SPOKES),
        "omitted_local_masks": list(START),
        "profile_h1_through_h7": list(START_PROFILE),
        "candidate_reciprocal_exchanges": candidates,
        "legal_reciprocal_exchanges": sum(
            neighbour_profiles.values()
        ),
        "neighbour_minimum_histogram": dict(minimum_histogram),
        "immediately_descending_neighbours": 0,
        "neutral_escape": {
            "exchange": {
                "coordinates": [0, 1],
                "edge_ids_from_respective_omitted_classes": [19, 6],
            },
            "omitted_local_masks": list(NEUTRAL),
            "profile_h1_through_h7": list(neutral_profile),
            "kernel_inert": True,
        },
        "descending_second_step": {
            "exchange": {
                "coordinates": [0, 2],
                "edge_ids_from_respective_omitted_classes": [22, 7],
            },
            "omitted_local_masks": list(DESCENDED),
            "profile_h1_through_h7": list(descended_profile),
        },
        "verified_simple_cubic": True,
        "verified_three_edge_connected": True,
        "verified_two_step_escape": True,
        "fixed_kernel_exposure_countermodel": {
            "claim_refuted": (
                "kernel-inert realization motion always exposes a "
                "descending exchange"
            ),
            "omitted_local_masks": list(EXPOSURE_START),
            "profile_h1_through_h7": list(exposure_profile),
            "candidate_reciprocal_exchanges": exposure_candidates,
            "legal_reciprocal_exchanges": exposure_legal,
            "neighbour_minimum_histogram": dict(
                exposure_minimum_histogram
            ),
            "kernel_inert_neighbours": exposure_kernel_inert,
            "active_same_level_then_descending_path": [
                {
                    "coordinates": [0, 1],
                    "edge_ids_from_respective_omitted_classes": [5, 3],
                    "omitted_local_masks": list(EXPOSURE_MIDDLE),
                    "profile_h1_through_h7": list(
                        exposure_middle_profile
                    ),
                },
                {
                    "coordinates": [0, 1],
                    "edge_ids_from_respective_omitted_classes": [20, 12],
                    "omitted_local_masks": list(EXPOSURE_DESCENDED),
                    "profile_h1_through_h7": list(
                        exposure_descended_profile
                    ),
                },
            ],
            "verified": True,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
