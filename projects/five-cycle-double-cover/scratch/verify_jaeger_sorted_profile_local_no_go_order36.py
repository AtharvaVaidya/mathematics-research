#!/usr/bin/env python3
"""Independent exact replay of a sorted-profile local minimum.

The witness refutes the proposed one-step potential which orders a Jaeger
star state by the lexicographically sorted vector of its seven exact Fano
component defects.  It does not refute escape through the full d_min level
component and is not a Five-Cycle Double Cover counterexample.

Only the Python standard library is used.  The checker reconstructs the
graph, three trees, odd kernels, nowhere-zero F_2^3 flow, all seven exact
component defects, and every reciprocal two-tree exchange.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
import json


GRAPH6 = (
    "chc?GC@@G?_P?H??_?G?@??C??G?@G??C??P??@G?A?__?@_???C???g???"
    "GA??@?A??CG???G???GG????C_???@??A??G??A??_???OH"
)
ROOT = 0
SPOKES = (31, 3, 0)
OMITTED = (
    1273387172628768,
    107323987641370,
    871088653415109,
)
EXPECTED_PROFILE = (6, 6, 2, 4, 2, 2, 2)
EXPECTED_SORTED = (2, 2, 2, 2, 4, 6, 6)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    require(record and record[0] != "~", "only small graph6 is supported")
    order = ord(record[0]) - 63
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, "invalid graph6 character")
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
    return (
        len(chosen) == order - 1
        and connected_after_deleting(
            order,
            edges,
            inc,
            frozenset(range(len(edges))) - chosen,
        )
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
    require(len(traversal) == order, "tree kernel got disconnected input")
    subtree_size = [1] * order
    kernel: set[int] = set()
    for vertex in reversed(traversal[1:]):
        if subtree_size[vertex] & 1:
            kernel.add(parent_edge[vertex])
        subtree_size[parent[vertex]] += subtree_size[vertex]
    degrees = [0] * order
    for edge in kernel:
        left, right = edges[edge]
        degrees[left] += 1
        degrees[right] += 1
    require(kernel <= tree, "odd kernel is not in its tree")
    require(all(degree & 1 for degree in degrees), "kernel degree is even")
    return frozenset(kernel)


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
        require(len(candidates) == 1, "incident flow plane has no unique normal")
        normals.append(candidates[0])

    answer: list[int] = []
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
        bad_components = 0
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
            bad_components += component_xor
        answer.append(bad_components)
    return tuple(answer)


def main() -> None:
    order, edges = decode_graph6(GRAPH6)
    inc = incidence(order, edges)
    require(order == 36 and len(edges) == 54, "wrong graph dimensions")
    require(len(set(edges)) == len(edges), "parallel edge")
    require(all(left < right for left, right in edges), "loop or bad edge order")
    require(all(len(row) == 3 for row in inc), "graph is not cubic")
    require(set(SPOKES) == set(inc[ROOT]), "wrong root spokes")
    for deleted_count in range(3):
        for deleted in combinations(range(len(edges)), deleted_count):
            require(
                connected_after_deleting(
                    order, edges, inc, frozenset(deleted)
                ),
                "graph is not 3-edge-connected",
            )

    internal = tuple(
        edge for edge in range(len(edges)) if edge not in SPOKES
    )
    all_internal = (1 << len(internal)) - 1

    def reconstruct(
        omitted: tuple[int, int, int],
    ) -> tuple[
        tuple[frozenset[int], ...],
        tuple[frozenset[int], ...],
    ] | None:
        if (
            omitted[0] ^ omitted[1] ^ omitted[2] != all_internal
            or omitted[0] & omitted[1]
            or omitted[0] & omitted[2]
            or omitted[1] & omitted[2]
            or tuple(mask.bit_count() for mask in omitted)
            != (17, 17, 17)
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
                    if not ((omitted[coordinate] >> local) & 1)
                ]
            )
            if not is_tree(order, edges, inc, tree):
                return None
            trees.append(tree)
            kernels.append(odd_kernel(order, edges, inc, tree))
        return tuple(trees), tuple(kernels)

    profile_cache: dict[tuple[int, int, int], tuple[int, ...]] = {}

    def profile_of(omitted: tuple[int, int, int]) -> tuple[int, ...]:
        if omitted not in profile_cache:
            data = reconstruct(omitted)
            require(data is not None, "requested state is not legal")
            profile_cache[omitted] = exact_profile(
                order, edges, inc, data[1]
            )
        return profile_cache[omitted]

    def neighbours(
        omitted: tuple[int, int, int],
    ) -> list[tuple[int, int, int]]:
        answer: list[tuple[int, int, int]] = []
        for first in range(3):
            for second in range(first + 1, 3):
                for first_local in range(len(internal)):
                    if not ((omitted[first] >> first_local) & 1):
                        continue
                    for second_local in range(len(internal)):
                        if not ((omitted[second] >> second_local) & 1):
                            continue
                        toggle = (
                            (1 << first_local) | (1 << second_local)
                        )
                        changed = list(omitted)
                        changed[first] ^= toggle
                        changed[second] ^= toggle
                        candidate = tuple(changed)
                        if reconstruct(candidate) is not None:
                            answer.append(candidate)
        require(len(answer) == len(set(answer)), "duplicate exchange neighbour")
        return answer

    data = reconstruct(OMITTED)
    require(data is not None, "witness state is not legal")
    profile = profile_of(OMITTED)
    require(profile == EXPECTED_PROFILE, "wrong seven-plane profile")
    require(tuple(sorted(profile)) == EXPECTED_SORTED, "wrong sorted profile")

    adjacent = neighbours(OMITTED)
    require(len(adjacent) == 63, "wrong legal-neighbour count")
    comparison = Counter()
    ordered_histogram: Counter[tuple[int, ...]] = Counter()
    for candidate in adjacent:
        candidate_profile = profile_of(candidate)
        candidate_sorted = tuple(sorted(candidate_profile))
        relation = (
            "lower"
            if candidate_sorted < EXPECTED_SORTED
            else "equal"
            if candidate_sorted == EXPECTED_SORTED
            else "higher"
        )
        comparison[relation] += 1
        ordered_histogram[candidate_profile] += 1
    require(
        comparison == Counter({"equal": 13, "higher": 50}),
        "sorted-profile neighbourhood mismatch",
    )
    require(
        ordered_histogram[EXPECTED_PROFILE] == 13,
        "the thirteen neutral moves should preserve the ordered profile",
    )

    # Independently distinguish this local no-go from the open full-plateau
    # statement.  Breadth-first search only through states of d_min=2 and
    # stop at the first edge to d_min=0.
    minimum = min(profile)
    parent: dict[
        tuple[int, int, int],
        tuple[int, int, int] | None,
    ] = {OMITTED: None}
    queue = deque([(OMITTED, 0)])
    escaped: tuple[int, int, int] | None = None
    escape_parent: tuple[int, int, int] | None = None
    escape_distance = -1
    while queue and escaped is None:
        current, distance = queue.popleft()
        for candidate in neighbours(current):
            candidate_minimum = min(profile_of(candidate))
            if candidate_minimum < minimum:
                escaped = candidate
                escape_parent = current
                escape_distance = distance + 1
                break
            if candidate_minimum == minimum and candidate not in parent:
                parent[candidate] = current
                queue.append((candidate, distance + 1))
    require(escaped is not None, "d_min plateau did not escape")
    require(escape_distance == 2, "wrong d_min escape distance")
    require(len(parent) == 57, "wrong breadth-first frontier size")
    require(min(profile_of(escaped)) == 0, "escape did not reach zero")

    path = [escaped]
    cursor = escape_parent
    while cursor is not None:
        path.append(cursor)
        cursor = parent[cursor]
    path.reverse()
    require(len(path) == 3 and path[0] == OMITTED, "wrong escape path")

    report = {
        "claim_refuted": (
            "every positive Jaeger star state has a reciprocal exchange "
            "that lexicographically decreases its sorted seven-plane "
            "defect profile"
        ),
        "not_refuted": [
            "escape through the full same-d_min component",
            "the Five-Cycle Double Cover Conjecture",
        ],
        "graph6": GRAPH6,
        "order": order,
        "root": ROOT,
        "spokes_in_coordinate_order": list(SPOKES),
        "omitted_internal_masks": list(OMITTED),
        "profile_h1_through_h7": list(profile),
        "sorted_profile": list(EXPECTED_SORTED),
        "candidate_exchanges": 3 * 17 * 17,
        "legal_exchanges": len(adjacent),
        "sorted_profile_comparison": dict(comparison),
        "d_min_escape_distance": escape_distance,
        "d_min_bfs_states_seen": len(parent),
        "d_min_escape_path": [
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
