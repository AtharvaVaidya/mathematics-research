#!/usr/bin/env python3
"""Exact b*=2 witness on the Tait flag graph of a triangular torus.

The graph is constructed from the flags of the 3-by-3 periodic triangular
map.  Its three flag involutions give a Tait colouring, embedded as the
D5 labels 01, 02, 12.  The checker reconstructs every factor component,
every shortest first component pair for the fixed ordered roots, and the
cyclic foreign-block statistic.  It uses only the Python standard library.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations


WIDTH = 3
HEIGHT = 3
PAIRS = tuple(combinations(range(5), 2))
ROOTS = (1, 156)


def vertex(x: int, y: int) -> int:
    return (x % WIDTH) * HEIGHT + (y % HEIGHT)


def triangular_faces() -> tuple[tuple[int, int, int], ...]:
    answer = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            answer.append(
                (vertex(x, y), vertex(x + 1, y), vertex(x + 1, y + 1))
            )
            answer.append(
                (vertex(x, y), vertex(x + 1, y + 1), vertex(x, y + 1))
            )
    return tuple(answer)


FACES = triangular_faces()
FLAGS = tuple(
    (face, side, endpoint)
    for face in range(len(FACES))
    for side in range(3)
    for endpoint in range(2)
)
FLAG_ID = {flag: index for index, flag in enumerate(FLAGS)}


def involution_zero(flag):
    face, side, endpoint = flag
    return face, side, 1 - endpoint


def involution_one(flag):
    face, side, endpoint = flag
    if endpoint == 0:
        return face, (side - 1) % 3, 1
    return face, (side + 1) % 3, 0


SIDE_OWNERS: dict[tuple[int, int], list[tuple[int, int, int, int]]] = {}
for face, row in enumerate(FACES):
    for side in range(3):
        left, right = row[side], row[(side + 1) % 3]
        SIDE_OWNERS.setdefault(
            tuple(sorted((left, right))), []
        ).append((face, side, left, right))
assert all(len(owners) == 2 for owners in SIDE_OWNERS.values())


def involution_two(flag):
    face, side, endpoint = flag
    row = FACES[face]
    actual_vertex = row[side] if endpoint == 0 else row[(side + 1) % 3]
    owners = SIDE_OWNERS[tuple(sorted((row[side], row[(side + 1) % 3])))]
    other = owners[0] if owners[1][0] == face else owners[1]
    other_face, other_side, left, right = other
    other_endpoint = 0 if left == actual_vertex else 1
    return other_face, other_side, other_endpoint


MATCHINGS = tuple(
    frozenset(
        tuple(sorted((FLAG_ID[flag], FLAG_ID[involution(flag)])))
        for flag in FLAGS
    )
    for involution in (involution_zero, involution_one, involution_two)
)
assert all(len(matching) == len(FLAGS) // 2 for matching in MATCHINGS)
assert not (MATCHINGS[0] & MATCHINGS[1])
assert not (MATCHINGS[0] & MATCHINGS[2])
assert not (MATCHINGS[1] & MATCHINGS[2])

EDGES = tuple(sorted(set().union(*MATCHINGS)))
EDGE_ID = {edge: index for index, edge in enumerate(EDGES)}
INCIDENCE = [[] for _ in FLAGS]
for edge, (left, right) in enumerate(EDGES):
    INCIDENCE[left].append(edge)
    INCIDENCE[right].append(edge)

EDGE_LABEL = {}
for matching, label in zip(MATCHINGS, (0x03, 0x05, 0x06), strict=True):
    for edge in matching:
        EDGE_LABEL[edge] = label
STATE = tuple(EDGE_LABEL[edge] for edge in EDGES)


def edge_components(mask: int) -> tuple[int, ...]:
    answer = []
    unseen = mask
    while unseen:
        seed_bit = unseen & -unseen
        unseen ^= seed_bit
        component = seed_bit
        queue = deque([seed_bit.bit_length() - 1])
        while queue:
            edge = queue.popleft()
            for endpoint in EDGES[edge]:
                for other in INCIDENCE[endpoint]:
                    bit = 1 << other
                    if unseen & bit:
                        unseen ^= bit
                        component |= bit
                        queue.append(other)
        answer.append(component)
    return tuple(answer)


def factors() -> tuple[tuple[tuple[int, int], int], ...]:
    answer = []
    for pair in PAIRS:
        pair_mask = (1 << pair[0]) | (1 << pair[1])
        active = sum(
            1 << edge
            for edge, label in enumerate(STATE)
            if (label & pair_mask).bit_count() == 1
        )
        for component in edge_components(active):
            answer.append((pair, component))
    return tuple(answer)


ROWS = factors()
ROW_ADJACENCY = [[] for _ in ROWS]
for left in range(len(ROWS)):
    for right in range(left + 1, len(ROWS)):
        if ROWS[left][1] & ROWS[right][1]:
            ROW_ADJACENCY[left].append(right)
            ROW_ADJACENCY[right].append(left)


def circuit_order(component: int, root: int) -> tuple[int, ...]:
    selected = {
        edge for edge in range(len(EDGES)) if (component >> edge) & 1
    }

    def adjacent(edge):
        return sorted(
            other
            for endpoint in EDGES[edge]
            for other in INCIDENCE[endpoint]
            if other != edge and other in selected
        )

    assert all(len(adjacent(edge)) == 2 for edge in selected)
    answer = [root]
    previous = root
    current = adjacent(root)[0]
    while current != root:
        answer.append(current)
        choices = adjacent(current)
        following = choices[0] if choices[0] != previous else choices[1]
        previous, current = current, following
    assert len(answer) == len(selected)
    return tuple(answer)


def distances_to_target(target: int) -> list[int]:
    distance = [10**9] * len(ROWS)
    queue = deque()
    for index, (_, component) in enumerate(ROWS):
        if (component >> target) & 1:
            distance[index] = 1
            queue.append(index)
    while queue:
        current = queue.popleft()
        for other in ROW_ADJACENCY[current]:
            if distance[other] == 10**9:
                distance[other] = distance[current] + 1
                queue.append(other)
    return distance


def profile(
    roots: tuple[int, int],
    first: int,
    second: int,
):
    pair_p, circuit = ROWS[first]
    pair_q, target_component = ROWS[second]
    if len(set(pair_p) & set(pair_q)) != 1:
        return None

    q_rows = [
        (index, component)
        for index, (pair, component) in enumerate(ROWS)
        if pair == pair_q
    ]
    root_rows = [
        (index, component)
        for index, component in q_rows
        if (component >> roots[0]) & 1
    ]
    assert len(root_rows) <= 1
    if not root_rows or root_rows[0][0] == second:
        return None
    root_index, root_component = root_rows[0]

    owner = {}
    for index, component in q_rows:
        common = circuit & component
        while common:
            bit = common & -common
            common ^= bit
            edge = bit.bit_length() - 1
            assert edge not in owner
            owner[edge] = index

    order = circuit_order(circuit, roots[0])
    size = len(order)
    scans = []
    for step in (1, -1):
        cursor = step
        while owner.get(order[cursor % size]) == root_index:
            cursor += step
            assert abs(cursor) <= size
        blockers = []
        previous = object()
        while abs(cursor) <= size:
            edge = order[cursor % size]
            current = owner.get(edge)
            if current != previous:
                if current == second:
                    scans.append((tuple(blockers), edge))
                    break
                if current is not None and current != root_index:
                    blockers.append(current)
            previous = current
            cursor += step
        else:
            raise AssertionError("target component absent from first circuit")
    return {
        "P": pair_p,
        "Q": pair_q,
        "C": circuit,
        "H": root_component,
        "D": target_component,
        "order": order,
        "scans": tuple(scans),
        "blockers": min(len(scan[0]) for scan in scans),
    }


def metric(roots: tuple[int, int]):
    target_distance = distances_to_target(roots[1])
    source_rows = [
        index
        for index, (_, component) in enumerate(ROWS)
        if (component >> roots[0]) & 1
    ]
    distance = min(target_distance[index] for index in source_rows)
    profiles = []
    if distance > 1:
        for first in source_rows:
            for second in ROW_ADJACENCY[first]:
                if 1 + target_distance[second] != distance:
                    continue
                candidate = profile(roots, first, second)
                if candidate is not None:
                    profiles.append(candidate)
    blocker = min(
        (candidate["blockers"] for candidate in profiles),
        default=None,
    )
    return distance, blocker, tuple(profiles)


def connected_without_edge(omitted: int) -> bool:
    seen = {0}
    queue = deque([0])
    while queue:
        current = queue.popleft()
        for edge in INCIDENCE[current]:
            if edge == omitted:
                continue
            left, right = EDGES[edge]
            other = left ^ right ^ current
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return len(seen) == len(FLAGS)


def surface_chi(state: tuple[int, ...]) -> int:
    coordinate_circuits = 0
    for coordinate in range(5):
        mask = sum(
            1 << edge
            for edge, label in enumerate(state)
            if (label >> coordinate) & 1
        )
        coordinate_circuits += len(edge_components(mask))
    return coordinate_circuits - len(EDGES) + len(FLAGS)


def switched(pair: tuple[int, int], component: int) -> tuple[int, ...]:
    pair_mask = (1 << pair[0]) | (1 << pair[1])
    return tuple(
        label ^ pair_mask if (component >> edge) & 1 else label
        for edge, label in enumerate(STATE)
    )


def main() -> None:
    assert len(FACES) == 18
    assert len(FLAGS) == 108
    assert len(EDGES) == 162
    assert len(set(EDGES)) == len(EDGES)
    assert all(left != right for left, right in EDGES)
    assert all(len(row) == 3 for row in INCIDENCE)
    assert connected_without_edge(-1)
    assert all(connected_without_edge(edge) for edge in range(len(EDGES)))
    assert all(label.bit_count() == 2 for label in STATE)
    assert all(
        STATE[row[0]] ^ STATE[row[1]] ^ STATE[row[2]] == 0
        for row in INCIDENCE
    )
    level = surface_chi(STATE)
    delta_histogram: dict[int, int] = {}
    for pair, component in ROWS:
        delta = surface_chi(switched(pair, component)) - level
        delta_histogram[delta] = delta_histogram.get(delta, 0) + 1
    assert level == 0
    assert delta_histogram == {0: 108, -2: 27, -4: 18, -10: 9}

    roots = ROOTS

    distance, blocker, profiles = metric(roots)
    assert (distance, blocker) == (2, 2)
    assert len(profiles) == 7
    assert all(candidate["blockers"] == 2 for candidate in profiles)
    minimizing = [
        candidate
        for candidate in profiles
        if candidate["blockers"] == blocker
    ]
    assert minimizing
    assert all(
        len(scan[0]) >= 2
        for candidate in profiles
        for scan in candidate["scans"]
    )
    print("PASS")
    print(
        f"triangular torus {WIDTH}x{HEIGHT}: "
        f"vertices={len(FLAGS)} edges={len(EDGES)} roots={roots}"
    )
    print(
        f"distance={distance} b*={blocker} "
        f"eligible_shortest_profiles={len(profiles)}"
    )
    print(f"chi={level} one_switch_deltas={delta_histogram}")
    for candidate in minimizing:
        print(
            "profile",
            f"P={candidate['P']}",
            f"Q={candidate['Q']}",
            f"C={tuple(i for i in range(len(EDGES)) if candidate['C'] >> i & 1)}",
            f"H={tuple(i for i in range(len(EDGES)) if candidate['H'] >> i & 1)}",
            f"D={tuple(i for i in range(len(EDGES)) if candidate['D'] >> i & 1)}",
            f"order={candidate['order']}",
            f"scans={candidate['scans']}",
        )


if __name__ == "__main__":
    main()
