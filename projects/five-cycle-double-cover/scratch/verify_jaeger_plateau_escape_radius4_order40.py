#!/usr/bin/env python3
"""Independent replay of a Jaeger state whose first descent is at radius four.

This standard-library checker does not import or invoke the C++ discovery
program.  It reconstructs the graph, the literal star state, every reciprocal
exchange examined by deterministic breadth-first search, and the exact seven
Fano-plane component defects.  The witness refutes only a bounded-radius
strengthening of the still-open full plateau-component claim.  It is not a
Five-Cycle Double Cover counterexample.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
import hashlib
import json


GRAPH6 = (
    "ghe?GC@@G??@?@??_@I??A?C_?G??G@?CA?@?C?G_??_@?@???@?@??_?C?"
    "G??C@?O??C?A??G????G????C????@??O??G?????_????H????_@?????G_"
    "????@G??_?C@"
)
ROOT = 0
SPOKES = (3, 0, 5)
START = (
    95184251351218348,
    47576007214007363,
    1354929510630160,
)
EXPECTED_START_PROFILE = (8, 2, 8, 8, 6, 10, 10)
EXPECTED_PATH = (
    START,
    (
        95183701612181676,
        47576556953044035,
        1354929510630160,
    ),
    (
        95183701612705836,
        47576556953044035,
        1354929510106000,
    ),
    (
        95183727382509612,
        47576556953044035,
        1354903740302224,
    ),
    (
        77169328873060396,
        65590955462493251,
        1354903740302224,
    ),
)
EXPECTED_PATH_PROFILES = (
    (8, 2, 8, 8, 6, 10, 10),
    (8, 2, 8, 8, 6, 10, 10),
    (6, 2, 8, 6, 10, 6, 6),
    (2, 4, 8, 8, 6, 6, 8),
    (4, 6, 6, 8, 8, 10, 0),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    require(record and record[0] != "~", "only short graph6 is supported")
    order = ord(record[0]) - 63
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, "invalid graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            require(cursor < len(bits), "truncated graph6")
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def incidence(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


def connected_after_deleting(
    order: int,
    edges: tuple[tuple[int, int], ...],
    inc: tuple[tuple[int, ...], ...],
    deleted: frozenset[int],
) -> bool:
    seen = {0}
    queue = [0]
    for vertex in queue:
        for edge in inc[vertex]:
            if edge in deleted:
                continue
            left, right = edges[edge]
            other = left ^ right ^ vertex
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return len(seen) == order


def is_tree(
    order: int,
    edges: tuple[tuple[int, int], ...],
    inc: tuple[tuple[int, ...], ...],
    chosen: frozenset[int],
) -> bool:
    return len(chosen) == order - 1 and connected_after_deleting(
        order,
        edges,
        inc,
        frozenset(range(len(edges))) - chosen,
    )


def odd_kernel(
    order: int,
    edges: tuple[tuple[int, int], ...],
    inc: tuple[tuple[int, ...], ...],
    tree: frozenset[int],
) -> frozenset[int]:
    parent = [-1] * order
    parent_edge = [-1] * order
    parent[0] = 0
    traversal = [0]
    for vertex in traversal:
        for edge in inc[vertex]:
            if edge not in tree:
                continue
            left, right = edges[edge]
            other = left ^ right ^ vertex
            if parent[other] < 0:
                parent[other] = vertex
                parent_edge[other] = edge
                traversal.append(other)
    require(len(traversal) == order, "kernel input is disconnected")
    subtree_size = [1] * order
    answer: set[int] = set()
    for vertex in reversed(traversal[1:]):
        if subtree_size[vertex] & 1:
            answer.add(parent_edge[vertex])
        subtree_size[parent[vertex]] += subtree_size[vertex]
    degrees = [0] * order
    for edge in answer:
        left, right = edges[edge]
        degrees[left] += 1
        degrees[right] += 1
    require(answer <= tree, "odd kernel leaves its tree")
    require(all(degree & 1 for degree in degrees), "kernel degree is even")
    return frozenset(answer)


def dot(left: int, right: int) -> int:
    return (left & right).bit_count() & 1


def exact_profile(
    order: int,
    edges: tuple[tuple[int, int], ...],
    inc: tuple[tuple[int, ...], ...],
    kernels: tuple[frozenset[int], ...],
) -> tuple[int, ...]:
    flow = tuple(
        sum(
            1 << coordinate
            for coordinate in range(3)
            if edge not in kernels[coordinate]
        )
        for edge in range(len(edges))
    )
    require(all(flow), "derived flow has a zero edge")
    for vertex in range(order):
        total = 0
        for edge in inc[vertex]:
            total ^= flow[edge]
        require(total == 0, "derived labels violate flow conservation")

    normals: list[int] = []
    for vertex in range(order):
        candidates = [
            functional
            for functional in range(1, 8)
            if all(dot(functional, flow[edge]) == 0 for edge in inc[vertex])
        ]
        require(len(candidates) == 1, "incident plane has no unique normal")
        normals.append(candidates[0])

    profile: list[int] = []
    for functional in range(1, 8):
        adjacency: list[list[int]] = [[] for _ in range(order)]
        for edge, (left, right) in enumerate(edges):
            if dot(functional, flow[edge]) == 0:
                adjacency[left].append(right)
                adjacency[right].append(left)
        require(
            all(len(row) in (1, 3) for row in adjacency),
            "zero-plane degree is not one or three",
        )
        transverse = functional & -functional
        unseen = set(range(order))
        defects = 0
        while unseen:
            start = unseen.pop()
            queue = [start]
            component_xor = 0
            for vertex in queue:
                if len(adjacency[vertex]) == 1:
                    component_xor ^= dot(
                        normals[vertex] ^ functional, transverse
                    )
                for other in adjacency[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        queue.append(other)
            defects += component_xor
        profile.append(defects)
    return tuple(profile)


def main() -> None:
    order, edges = decode_graph6(GRAPH6)
    inc = incidence(order, edges)
    require(order == 40 and len(edges) == 60, "wrong graph dimensions")
    require(len(set(edges)) == len(edges), "parallel edge")
    require(all(left < right for left, right in edges), "loop")
    require(all(len(row) == 3 for row in inc), "graph is not cubic")
    require(set(SPOKES) == set(inc[ROOT]), "wrong root spokes")
    for deleted_count in range(3):
        for deleted in combinations(range(len(edges)), deleted_count):
            require(
                connected_after_deleting(
                    order, edges, inc, frozenset(deleted)
                ),
                "graph is not three-edge-connected",
            )

    internal = tuple(edge for edge in range(len(edges)) if edge not in SPOKES)
    require(len(internal) == 57, "wrong internal-edge count")
    all_internal = (1 << len(internal)) - 1
    profile_cache: dict[tuple[int, int, int], tuple[int, ...]] = {}

    def reconstruct(
        omitted: tuple[int, int, int],
    ) -> tuple[frozenset[int], ...] | None:
        if (
            omitted[0] ^ omitted[1] ^ omitted[2] != all_internal
            or omitted[0] & omitted[1]
            or omitted[0] & omitted[2]
            or omitted[1] & omitted[2]
            or tuple(mask.bit_count() for mask in omitted) != (19, 19, 19)
        ):
            return None
        kernels: list[frozenset[int]] = []
        for coordinate in range(3):
            tree = frozenset(
                [SPOKES[coordinate]]
                + [
                    edge
                    for local, edge in enumerate(internal)
                    if not ((omitted[coordinate] >> local) & 1)
                ]
            )
            if not is_tree(order, edges, inc, tree):
                return None
            kernels.append(odd_kernel(order, edges, inc, tree))
        return tuple(kernels)

    def profile_of(omitted: tuple[int, int, int]) -> tuple[int, ...]:
        if omitted not in profile_cache:
            kernels = reconstruct(omitted)
            require(kernels is not None, "requested state is illegal")
            profile_cache[omitted] = exact_profile(
                order, edges, inc, kernels
            )
        return profile_cache[omitted]

    def neighbours(
        omitted: tuple[int, int, int],
    ) -> list[tuple[int, int, int]]:
        answer: list[tuple[int, int, int]] = []
        for first in range(3):
            for second in range(first + 1, 3):
                first_bits = omitted[first]
                while first_bits:
                    first_bit = first_bits & -first_bits
                    first_bits ^= first_bit
                    second_bits = omitted[second]
                    while second_bits:
                        second_bit = second_bits & -second_bits
                        second_bits ^= second_bit
                        changed = list(omitted)
                        toggle = first_bit | second_bit
                        changed[first] ^= toggle
                        changed[second] ^= toggle
                        candidate = tuple(changed)
                        if reconstruct(candidate) is not None:
                            answer.append(candidate)
        require(len(answer) == len(set(answer)), "duplicate neighbour")
        return answer

    start_profile = profile_of(START)
    require(
        start_profile == EXPECTED_START_PROFILE,
        "wrong initial exact profile",
    )
    level = min(start_profile)
    require(level == 2, "wrong positive level")

    parent: dict[
        tuple[int, int, int],
        tuple[int, int, int] | None,
    ] = {START: None}
    distance = {START: 0}
    queue = deque([START])
    popped_distance_histogram: Counter[int] = Counter()
    boundary_score_histogram: Counter[int] = Counter()
    candidate_exchanges = 0
    legal_exchange_arcs = 0
    neutral_arcs = 0
    lower_boundary_arcs = 0
    higher_boundary_arcs = 0
    escape: tuple[int, int, int] | None = None
    escape_parent: tuple[int, int, int] | None = None
    boundary_by_source_distance: Counter[tuple[int, int]] = Counter()
    examined_legal_arcs: list[
        tuple[
            tuple[int, int, int],
            tuple[int, int, int],
            int,
        ]
    ] = []
    maximum_plateau_radius = 3

    while queue:
        current = queue.popleft()
        current_distance = distance[current]
        popped_distance_histogram[current_distance] += 1
        candidate_exchanges += 3 * 19 * 19
        adjacent = neighbours(current)
        legal_exchange_arcs += len(adjacent)
        for candidate in adjacent:
            candidate_score = min(profile_of(candidate))
            examined_legal_arcs.append((current, candidate, candidate_score))
            if candidate_score == level:
                neutral_arcs += 1
                if (
                    current_distance < maximum_plateau_radius
                    and candidate not in distance
                ):
                    distance[candidate] = current_distance + 1
                    parent[candidate] = current
                    queue.append(candidate)
            else:
                boundary_score_histogram[candidate_score] += 1
                boundary_by_source_distance[
                    (current_distance, candidate_score)
                ] += 1
                if candidate_score < level:
                    lower_boundary_arcs += 1
                    if escape is None:
                        escape = candidate
                        escape_parent = current
                else:
                    higher_boundary_arcs += 1

    require(escape is not None and escape_parent is not None, "no escape")
    escape_distance = distance[escape_parent] + 1
    require(escape_distance == 4, "first descent is not at distance four")
    require(
        all(
            source_distance == 3
            for (source_distance, score), count
            in boundary_by_source_distance.items()
            if score < level and count
        ),
        "a descent exists within plateau radius three",
    )
    require(len(distance) == sum(popped_distance_histogram.values()), "BFS")
    require(
        popped_distance_histogram
        == Counter({3: 836, 2: 108, 1: 13, 0: 1}),
        "wrong complete plateau-layer histogram",
    )
    require(len(distance) == 958, "wrong radius-three plateau-ball size")
    require(candidate_exchanges == 1_037_514, "wrong candidate count")
    require(legal_exchange_arcs == 67_392, "wrong legal-arc count")
    require(neutral_arcs == 19_334, "wrong neutral-arc count")
    require(lower_boundary_arcs == 32, "wrong descending-boundary count")
    require(higher_boundary_arcs == 48_026, "wrong higher-boundary count")
    require(
        boundary_score_histogram
        == Counter({4: 37_413, 6: 10_502, 8: 111, 0: 32}),
        "wrong boundary score histogram",
    )
    require(
        boundary_by_source_distance
        == Counter(
            {
                (0, 4): 38,
                (0, 6): 14,
                (1, 4): 508,
                (1, 6): 174,
                (2, 4): 4_276,
                (2, 6): 1_317,
                (2, 8): 8,
                (3, 0): 32,
                (3, 4): 32_591,
                (3, 6): 8_997,
                (3, 8): 103,
            }
        ),
        "wrong boundary-by-layer histogram",
    )

    path = [escape]
    cursor: tuple[int, int, int] | None = escape_parent
    while cursor is not None:
        path.append(cursor)
        cursor = parent[cursor]
    path.reverse()
    require(tuple(path) == EXPECTED_PATH, "wrong shortest escape path")
    path_profiles = tuple(profile_of(state) for state in path)
    require(path_profiles == EXPECTED_PATH_PROFILES, "wrong path profiles")
    layer_payload = sorted(
        (state_distance, *state)
        for state, state_distance in distance.items()
    )
    layer_sha256 = hashlib.sha256(
        json.dumps(layer_payload, separators=(",", ":")).encode()
    ).hexdigest()
    arc_sha256 = hashlib.sha256(
        json.dumps(
            sorted(examined_legal_arcs),
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    require(
        layer_sha256
        == "51aa4f3ff1efa9bebcffe0f2869919c7bd25d60c2047f8b5383b8be90d435c58",
        "wrong canonical plateau-ball digest",
    )
    require(
        arc_sha256
        == "d2ad5a4bb090e43efffba60e51dec5c66037cf10465b7c43f86a2c5b3407c4ce",
        "wrong canonical legal-arc digest",
    )

    literal = {
        "graph6": GRAPH6,
        "root": ROOT,
        "spokes": SPOKES,
        "start": START,
        "path": EXPECTED_PATH,
    }
    report = {
        "claim_refuted": (
            "every positive Jaeger star state has a lower-d_min state "
            "within three reciprocal exchanges while staying at the "
            "initial d_min before the last exchange"
        ),
        "not_refuted": [
            "escape through the complete same-d_min component",
            "the Five-Cycle Double Cover Conjecture",
        ],
        "literal_sha256": hashlib.sha256(
            json.dumps(literal, sort_keys=True).encode()
        ).hexdigest(),
        "complete_radius_three_ball_sha256": layer_sha256,
        "examined_legal_arcs_sha256": arc_sha256,
        "graph6": GRAPH6,
        "order": order,
        "root": ROOT,
        "spokes_in_coordinate_order": list(SPOKES),
        "start_omitted_internal_masks": list(START),
        "start_profile_h1_through_h7": list(start_profile),
        "d_min": level,
        "minimum_escape_distance": escape_distance,
        "complete_plateau_ball_radius": maximum_plateau_radius,
        "popped_distance_histogram": dict(popped_distance_histogram),
        "plateau_states_in_complete_radius_three_ball": len(distance),
        "candidate_exchanges_checked": candidate_exchanges,
        "legal_exchange_arcs_checked": legal_exchange_arcs,
        "neutral_arcs_checked": neutral_arcs,
        "boundary_score_histogram": dict(boundary_score_histogram),
        "boundary_by_source_distance_and_score": {
            f"{source_distance}->{score}": count
            for (source_distance, score), count
            in sorted(boundary_by_source_distance.items())
        },
        "escape_path": [
            {
                "omitted_internal_masks": list(state),
                "profile_h1_through_h7": list(profile_of(state)),
            }
            for state in path
        ],
        "verified_simple_cubic": True,
        "verified_three_edge_connected": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
