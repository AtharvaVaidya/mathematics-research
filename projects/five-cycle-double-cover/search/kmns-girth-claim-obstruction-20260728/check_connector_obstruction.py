#!/usr/bin/env python3
"""Check the local girth obstruction in the literal KMNS Figure 4 gluing.

This script uses only the Python standard library.  It independently checks
the corrected Petersen graph underlying Figure 2, all decycling
distance-two triples and distinguished-u choices, the three short terminal
paths that survive the F_g construction, and all 18 structural
identifications (36 ordered junctions before quotienting by the symmetry of
the two isolated edges) of the two size-three connectors with a Z multipole.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations, permutations
import json


# Figure 2: vertices 0,...,5 are v_0,...,v_5 on the displayed 6-cycle.
# Vertex 6 is the branch adjacent to v_0 and v_3, vertex 7 is the branch
# adjacent to v_1 and v_4, vertex 8 is the branch adjacent to v_2 and v_5,
# and vertex 9 is the central vertex of the complementary spanning tree.
PETERSEN_EDGES = (
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5),
    (0, 6), (3, 6), (6, 9),
    (1, 7), (4, 7), (7, 9),
    (2, 8), (5, 8), (8, 9),
)

# In the example in the proof of Theorem 5.1, u_1=v_0 and the two vertices
# substituted by 5-poles are v_2 and v_4.  Deleting u_1 leaves a connector
# with retained terminal endpoints v_1, v_5, and the branch vertex 6.
TERMINALS = (1, 5, 6)
SUBSTITUTED_VERTICES = frozenset((2, 4))

# Paths inside P_1-u_1 which avoid both substituted vertices.  Therefore
# these paths survive every choice of the 5-poles M_g and every permutation
# used to attach those poles.
SURVIVING_PATHS = (
    (1, 7, 9, 8, 5),  # terminal 0 to terminal 1: four edges
    (1, 7, 9, 6),     # terminal 0 to terminal 2: three edges
    (5, 8, 9, 6),     # terminal 1 to terminal 2: three edges
)


def adjacency(order: int, edges: tuple[tuple[int, int], ...]) -> list[list[int]]:
    rows = [[] for _ in range(order)]
    seen: set[tuple[int, int]] = set()
    for left, right in edges:
        assert 0 <= left < order and 0 <= right < order and left != right
        edge = (min(left, right), max(left, right))
        assert edge not in seen
        seen.add(edge)
        rows[left].append(right)
        rows[right].append(left)
    for row in rows:
        row.sort()
    return rows


def connected(rows: list[list[int]]) -> bool:
    reached = {0}
    queue = deque([0])
    while queue:
        for other in rows[queue.popleft()]:
            if other not in reached:
                reached.add(other)
                queue.append(other)
    return len(reached) == len(rows)


def girth(rows: list[list[int]]) -> int:
    best = len(rows) + 1
    for source in range(len(rows)):
        distance = [-1] * len(rows)
        parent = [-1] * len(rows)
        distance[source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for other in rows[vertex]:
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    best = min(
                        best, distance[vertex] + distance[other] + 1
                    )
    return best


def verify_path(rows: list[list[int]], path: tuple[int, ...]) -> int:
    assert path[0] in TERMINALS and path[-1] in TERMINALS
    assert not (set(path) & SUBSTITUTED_VERTICES)
    assert 0 not in path
    assert len(path) == len(set(path))
    for left, right in zip(path, path[1:]):
        assert right in rows[left]
    return len(path) - 1


def induced_acyclic(rows: list[list[int]], deleted: frozenset[int]) -> bool:
    """Check by a spanning-forest traversal that the surviving graph is acyclic."""
    seen: set[int] = set()
    for root in range(len(rows)):
        if root in deleted or root in seen:
            continue
        seen.add(root)
        stack = [(root, -1)]
        while stack:
            vertex, parent = stack.pop()
            for other in rows[vertex]:
                if other in deleted or other == parent:
                    continue
                if other in seen:
                    return False
                seen.add(other)
                stack.append((other, vertex))
    return True


def shortest_distance(
    rows: list[list[int]], source: int, target: int,
    deleted: frozenset[int],
) -> int:
    assert source not in deleted and target not in deleted
    distance = {source: 0}
    queue = deque([source])
    while queue:
        vertex = queue.popleft()
        if vertex == target:
            return distance[vertex]
        for other in rows[vertex]:
            if other in deleted or other in distance:
                continue
            distance[other] = distance[vertex] + 1
            queue.append(other)
    raise AssertionError("connector terminals became disconnected")


def audit_decycling_triples(rows: list[list[int]]) -> list[dict[str, object]]:
    """Enumerate all allowed triples and every distinguished deleted vertex."""
    allowed = []
    for triple_tuple in combinations(range(len(rows)), 3):
        triple = frozenset(triple_tuple)
        # Petersen diameter is two, so pairwise distance two is equivalent
        # here to independence.
        if any(right in rows[left]
               for left, right in combinations(triple_tuple, 2)):
            continue
        if not induced_acyclic(rows, triple):
            continue
        allowed.append(triple_tuple)
    assert len(allowed) == 20

    records: list[dict[str, object]] = []
    for triple_tuple in allowed:
        triple = frozenset(triple_tuple)
        for distinguished in triple_tuple:
            terminals = tuple(rows[distinguished])
            distances = sorted(
                shortest_distance(rows, left, right, triple)
                for left, right in combinations(terminals, 2)
            )
            assert distances == [3, 3, 4]
            records.append({
                "triple": list(triple_tuple),
                "distinguished_u": distinguished,
                "terminals": list(terminals),
                "terminal_distance_multiset": distances,
            })
    assert len(records) == 60
    return records


def distance_upper_bounds(rows: list[list[int]]) -> tuple[tuple[int, ...], ...]:
    result = [[0] * 3 for _ in range(3)]
    for path in SURVIVING_PATHS:
        distance = verify_path(rows, path)
        left = TERMINALS.index(path[0])
        right = TERMINALS.index(path[-1])
        result[left][right] = result[right][left] = distance
    assert all(result[i][j] > 0 for i in range(3) for j in range(3) if i != j)
    return tuple(tuple(row) for row in result)


def cycle_bounds(
    distances: tuple[tuple[int, ...], ...],
    left_center: int,
    right_center: int,
    pairing: tuple[int, int],
) -> tuple[int, int, int]:
    """Return the three local-cycle upper bounds for one Z identification."""
    left_other = [index for index in range(3) if index != left_center]
    right_other = [index for index in range(3) if index != right_center]
    assert sorted(pairing) == right_other
    match = dict(zip(left_other, pairing))

    # Use both isolated edges of Z and one surviving path in each F_g.
    first, second = left_other
    two_isolated = (
        distances[first][second]
        + distances[match[first]][match[second]]
        + 2
    )

    # Use the central vertex of Z, one isolated edge, and one path in each F_g.
    one_isolated = tuple(
        distances[left_center][endpoint]
        + distances[right_center][match[endpoint]]
        + 3
        for endpoint in left_other
    )
    return (two_isolated, *one_isolated)


def main() -> int:
    rows = adjacency(10, PETERSEN_EDGES)
    assert connected(rows)
    assert all(len(row) == 3 for row in rows)
    assert girth(rows) == 5
    triple_records = audit_decycling_triples(rows)
    distances = distance_upper_bounds(rows)
    assert distances == ((0, 4, 3), (4, 0, 3), (3, 3, 0))

    records = []
    for left_center in range(3):
        for right_center in range(3):
            right_other = [index for index in range(3)
                           if index != right_center]
            for pairing in permutations(right_other):
                cycles = cycle_bounds(
                    distances, left_center, right_center, pairing
                )
                records.append({
                    "left_center": left_center,
                    "right_center": right_center,
                    "pairing": list(pairing),
                    "cycle_upper_bounds": list(cycles),
                    "minimum_cycle_upper_bound": min(cycles),
                })

    assert len(records) == 18
    assert all(record["minimum_cycle_upper_bound"] <= 9
               for record in records)
    assert max(record["minimum_cycle_upper_bound"] for record in records) == 9

    result = {
        "schema": "kmns-figure4-local-girth-obstruction-v1",
        "petersen": {
            "vertices": 10,
            "edges": len(PETERSEN_EDGES),
            "simple": True,
            "cubic": True,
            "connected": True,
            "girth": girth(rows),
        },
        "connector_terminal_order": list(TERMINALS),
        "decycling_distance_two_triples": 20,
        "distinguished_triple_choices_checked": len(triple_records),
        "distinguished_triple_records": triple_records,
        "surviving_paths": [list(path) for path in SURVIVING_PATHS],
        "terminal_distance_upper_bounds": [list(row) for row in distances],
        "ordered_connector_junctions_represented": 36,
        "structural_identifications_checked": len(records),
        "largest_certified_per_identification_upper_bound": 9,
        "records": records,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
