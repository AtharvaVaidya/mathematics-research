#!/usr/bin/env python3
"""Solver-independent audit of a packable H--S radius-one obstruction.

This checker uses only the Python standard library.  It verifies an explicit
nowhere-zero F_2^3-flow on a strict 26-vertex snark with all of the following
properties:

* value class 4 has two edge-disjoint boundary joins in its complement;
* the initial flow fails the Hušek--Šámal component criterion;
* none of the 1,485 legal simple-cycle/value switches repairs that criterion;
* the packing-to-switch construction gives two legal simple-cycle switches
  that do repair it; and
* an explicit five-cycle-double-cover labeling exists.

Thus the certificate refutes only the auxiliary assertion that a packable
H--S-bad flow is always one legal circuit switch from an H--S-good flow.  It
is not a counterexample to the Five-Cycle Double Cover Conjecture.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json


GRAPH6 = "Y??G@cOOGC??P??Ap???`_A??CIC???IC_C?@??HO??A??B_G????D?_"
CANONICAL_GRAPH6 = (
    "Ys?GO?@?GC?Q@O?O?@O?a?@??_GGO?O??O?BC?DA??AC?G@O?A?G?G?_"
)
FLOW = (
    5, 1, 5, 4, 4, 4, 7, 1, 6, 7, 3, 1, 6, 4, 3, 2, 3, 2, 6,
    1, 2, 5, 5, 2, 7, 6, 3, 2, 5, 7, 1, 1, 7, 6, 5, 3, 1, 7, 6,
)
PROFILE_BEFORE = (6, 6, 4, 6, 2, 4, 4)
PACKING_VALUE = 4
PACKING_RED = (
    1, 14, 15, 18, 20, 21, 26, 28, 29, 30, 31, 32, 35, 37, 38,
)
PACKING_BLUE = (0, 2, 6, 7, 8, 9, 12, 16, 17)
PACKING_SWITCH_CYCLES = (
    (0, 1, 2, 8, 9, 20, 22, 24, 25, 26, 30, 31, 33),
    (6, 12, 14, 15, 34, 35),
)
PACKING_SWITCH_PROFILES = (
    (4, 6, 4, 2, 4, 4, 4),
    (4, 6, 4, 0, 6, 4, 4),
)
FIVE_CDC_LABELS = (
    3, 20, 5, 17, 3, 5, 6, 3, 3, 5, 10, 6, 3, 5, 3, 6, 5, 9,
    10, 12, 6, 18, 24, 12, 20, 6, 18, 6, 20, 18, 6, 6, 18, 20,
    6, 5, 5, 6, 3,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    require(record and record[0] != "~", "only small graph6 is supported")
    order = ord(record[0]) - 63
    require(0 <= order <= 62, "invalid graph6 order")
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, "invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            require(cursor < len(bits), "truncated graph6 record")
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    require(not any(bits[cursor:]), "nonzero graph6 padding")
    return order, tuple(edges)


def incidence(
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        require(0 <= left < right < order, "unnormalized edge")
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


def check_graph_and_flow(
    order: int,
    edges: tuple[tuple[int, int], ...],
    values: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    require(len(edges) == 3 * order // 2, "wrong cubic edge count")
    require(len(set(edges)) == len(edges), "parallel edge")
    rows = incidence(order, edges)
    require(all(len(row) == 3 for row in rows), "graph is not cubic")
    require(len(values) == len(edges), "flow length differs")
    require(all(1 <= value <= 7 for value in values), "zero flow value")
    require(
        all(values[row[0]] ^ values[row[1]] ^ values[row[2]] == 0
            for row in rows),
        "flow conservation fails",
    )
    reached = {0}
    queue = [0]
    for vertex in queue:
        for edge in rows[vertex]:
            left, right = edges[edge]
            other = left ^ right ^ vertex
            if other not in reached:
                reached.add(other)
                queue.append(other)
    require(len(reached) == order, "graph is disconnected")
    return rows


def defect_profile(
    order: int,
    edges: tuple[tuple[int, int], ...],
    values: tuple[int, ...],
) -> tuple[int, ...]:
    defects = []
    for functional in range(1, 8):
        adjacency = [[] for _ in range(order)]
        for edge, (left, right) in enumerate(edges):
            if ((functional & values[edge]).bit_count() & 1) == 0:
                adjacency[left].append(right)
                adjacency[right].append(left)
        component = [-1] * order
        count = 0
        for root in range(order):
            if component[root] >= 0:
                continue
            component[root] = count
            queue = [root]
            for vertex in queue:
                for other in adjacency[vertex]:
                    if component[other] < 0:
                        component[other] = count
                        queue.append(other)
            count += 1
        affine_value = next(
            value for value in range(1, 8)
            if (functional & value).bit_count() & 1
        )
        odd = [0] * count
        for edge, (left, right) in enumerate(edges):
            if values[edge] == affine_value:
                odd[component[left]] ^= 1
                odd[component[right]] ^= 1
        defects.append(sum(odd))
    return tuple(defects)


def boundary(
    order: int,
    edges: tuple[tuple[int, int], ...],
    selected: frozenset[int],
) -> frozenset[int]:
    parity = [0] * order
    for edge in selected:
        left, right = edges[edge]
        parity[left] ^= 1
        parity[right] ^= 1
    return frozenset(
        vertex for vertex, bit in enumerate(parity) if bit
    )


def is_simple_cycle(
    order: int,
    edges: tuple[tuple[int, int], ...],
    selected: tuple[int, ...],
) -> bool:
    require(len(selected) == len(set(selected)), "cycle repeats an edge")
    degree: Counter[int] = Counter()
    adjacency = [[] for _ in range(order)]
    for edge in selected:
        require(0 <= edge < len(edges), "cycle edge is out of range")
        left, right = edges[edge]
        degree[left] += 1
        degree[right] += 1
        adjacency[left].append(right)
        adjacency[right].append(left)
    if not degree or set(degree.values()) != {2}:
        return False
    reached = {min(degree)}
    queue = list(reached)
    for vertex in queue:
        for other in adjacency[vertex]:
            if other not in reached:
                reached.add(other)
                queue.append(other)
    return reached == set(degree)


def switched(
    values: tuple[int, ...],
    switch_value: int,
    cycle: tuple[int, ...],
) -> tuple[int, ...]:
    require(
        all(values[edge] != switch_value for edge in cycle),
        "switch creates a zero edge",
    )
    selected = frozenset(cycle)
    return tuple(
        value ^ switch_value if edge in selected else value
        for edge, value in enumerate(values)
    )


def all_simple_cycles(
    order: int,
    edges: tuple[tuple[int, int], ...],
    rows: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    """Enumerate undirected simple cycles by their edge bit masks."""

    result: list[int] = []
    used = [False] * order
    path: list[int] = []

    def extend(start: int, vertex: int, mask: int) -> None:
        for edge in rows[vertex]:
            left, right = edges[edge]
            other = left ^ right ^ vertex
            if other == start:
                if len(path) >= 3 and path[1] < vertex:
                    result.append(mask | (1 << edge))
                continue
            if other < start or used[other]:
                continue
            used[other] = True
            path.append(other)
            extend(start, other, mask | (1 << edge))
            path.pop()
            used[other] = False

    for start in range(order):
        used[start] = True
        path[:] = [start]
        extend(start, start, 0)
        used[start] = False
    require(len(result) == len(set(result)), "duplicate simple cycle")
    return tuple(result)


def components_after_deletion(
    order: int,
    edges: tuple[tuple[int, int], ...],
    rows: tuple[tuple[int, ...], ...],
    deleted: frozenset[int],
) -> tuple[frozenset[int], ...]:
    unseen = set(range(order))
    pieces = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        piece = {root}
        queue = [root]
        for vertex in queue:
            for edge in rows[vertex]:
                if edge in deleted:
                    continue
                left, right = edges[edge]
                other = left ^ right ^ vertex
                if other in unseen:
                    unseen.remove(other)
                    piece.add(other)
                    queue.append(other)
        pieces.append(frozenset(piece))
    return tuple(pieces)


def cyclic_cut_count(
    order: int,
    edges: tuple[tuple[int, int], ...],
    rows: tuple[tuple[int, ...], ...],
    size: int,
) -> int:
    answer = 0
    for deleted_tuple in combinations(range(len(edges)), size):
        deleted = frozenset(deleted_tuple)
        pieces = components_after_deletion(
            order, edges, rows, deleted
        )
        cyclic = 0
        for piece in pieces:
            internal = sum(
                edge not in deleted and left in piece and right in piece
                for edge, (left, right) in enumerate(edges)
            )
            cyclic += internal >= len(piece)
        answer += cyclic >= 2
    return answer


def girth(
    order: int,
    edges: tuple[tuple[int, int], ...],
    rows: tuple[tuple[int, ...], ...],
) -> int:
    best = order + 1
    for omitted, (source, target) in enumerate(edges):
        distance = [-1] * order
        distance[source] = 0
        queue = [source]
        for vertex in queue:
            for edge in rows[vertex]:
                if edge == omitted:
                    continue
                left, right = edges[edge]
                other = left ^ right ^ vertex
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    queue.append(other)
        if distance[target] >= 0:
            best = min(best, distance[target] + 1)
    return best


def has_tait_coloring(
    edges: tuple[tuple[int, int], ...],
) -> bool:
    colors = [-1] * len(edges)
    used = [0] * (max(max(edge) for edge in edges) + 1)

    def search(colored: int) -> bool:
        if colored == len(edges):
            return True
        choice = None
        for edge, (left, right) in enumerate(edges):
            if colors[edge] >= 0:
                continue
            available = 0b111 & ~(used[left] | used[right])
            if not available:
                return False
            key = (available.bit_count(), edge, available)
            if choice is None or key < choice:
                choice = key
        require(choice is not None, "Tait search lost an edge")
        _, edge, available = choice
        left, right = edges[edge]
        while available:
            color = available & -available
            available ^= color
            colors[edge] = color
            used[left] |= color
            used[right] |= color
            if search(colored + 1):
                return True
            used[left] ^= color
            used[right] ^= color
            colors[edge] = -1
        return False

    return search(0)


def main() -> None:
    order, edges = decode_graph6(GRAPH6)
    rows = check_graph_and_flow(order, edges, FLOW)
    profile = defect_profile(order, edges, FLOW)
    require(profile == PROFILE_BEFORE, "initial H-S profile differs")
    require(0 not in profile, "initial flow is H-S-good")

    matching = frozenset(
        edge for edge, value in enumerate(FLOW)
        if value == PACKING_VALUE
    )
    red = frozenset(PACKING_RED)
    blue = frozenset(PACKING_BLUE)
    terminals = boundary(order, edges, matching)
    require(red.isdisjoint(blue), "packing joins overlap")
    require(red.isdisjoint(matching), "red join meets matching")
    require(blue.isdisjoint(matching), "blue join meets matching")
    require(
        boundary(order, edges, red) == terminals,
        "red boundary differs from matching boundary",
    )
    require(
        boundary(order, edges, blue) == terminals,
        "blue boundary differs from matching boundary",
    )

    functional = PACKING_VALUE
    affine_support = frozenset(
        edge for edge, value in enumerate(FLOW)
        if (functional & value).bit_count() & 1
    )
    initial_join = affine_support - matching
    packing_cycle = initial_join ^ red
    require(
        packing_cycle == frozenset(
            edge
            for cycle in PACKING_SWITCH_CYCLES
            for edge in cycle
        ),
        "packing-to-switch support differs",
    )

    current = FLOW
    path_profiles = []
    for cycle, expected_profile in zip(
        PACKING_SWITCH_CYCLES, PACKING_SWITCH_PROFILES
    ):
        require(
            is_simple_cycle(order, edges, cycle),
            "packing switch is not a simple cycle",
        )
        current = switched(current, PACKING_VALUE, cycle)
        check_graph_and_flow(order, edges, current)
        current_profile = defect_profile(order, edges, current)
        require(
            current_profile == expected_profile,
            "packing switch profile differs",
        )
        path_profiles.append(current_profile)
    require(
        0 not in path_profiles[0] and 0 in path_profiles[1],
        "packing path is not a two-switch repair",
    )

    cycles = all_simple_cycles(order, edges, rows)
    legal = 0
    repairs = 0
    minimum_defect = min(profile)
    minimum_profile = profile
    for mask in cycles:
        selected = tuple(
            edge for edge in range(len(edges)) if mask >> edge & 1
        )
        present = {FLOW[edge] for edge in selected}
        for value in range(1, 8):
            if value in present:
                continue
            legal += 1
            candidate_profile = defect_profile(
                order, edges, switched(FLOW, value, selected)
            )
            if min(candidate_profile) < minimum_defect:
                minimum_defect = min(candidate_profile)
                minimum_profile = candidate_profile
            repairs += 0 in candidate_profile
    require(len(cycles) == 9213, "simple-cycle count differs")
    require(legal == 1485, "legal-switch count differs")
    require(repairs == 0, "a one-switch H-S repair exists")

    require(
        len(FIVE_CDC_LABELS) == len(edges)
        and all(label.bit_count() == 2 for label in FIVE_CDC_LABELS),
        "FiveCDC labels do not select exactly two coordinates",
    )
    require(
        all(
            all(
                sum(
                    (FIVE_CDC_LABELS[edge] >> coordinate) & 1
                    for edge in row
                ) % 2 == 0
                for coordinate in range(5)
            )
            for row in rows
        ),
        "FiveCDC label parity fails",
    )

    cyclic_cuts = {
        str(size): cyclic_cut_count(order, edges, rows, size)
        for size in range(1, 4)
    }
    require(
        all(count == 0 for count in cyclic_cuts.values()),
        "graph is not cyclically 4-edge-connected",
    )
    graph_girth = girth(order, edges, rows)
    require(graph_girth == 5, "graph girth differs")
    require(not has_tait_coloring(edges), "graph is Tait colorable")

    print(json.dumps({
        "schema": "husek-samal-packable-one-switch-countermodel-v1",
        "scope": (
            "counterexample only to the packable-state one-switch "
            "auxiliary assertion; not to FiveCDC"
        ),
        "graph6": GRAPH6,
        "canonical_graph6_external_labelg": CANONICAL_GRAPH6,
        "order": order,
        "edges": len(edges),
        "girth": graph_girth,
        "cyclic_cut_counts_sizes_1_to_3": cyclic_cuts,
        "cyclically_4_edge_connected": True,
        "three_edge_colorable": False,
        "strict_snark": True,
        "initial_husek_samal_profile": profile,
        "packing_value": PACKING_VALUE,
        "matching_edges": sorted(matching),
        "packing_red_join": PACKING_RED,
        "packing_blue_join": PACKING_BLUE,
        "simple_cycles_exhausted": len(cycles),
        "legal_cycle_value_switches_exhausted": legal,
        "husek_samal_good_one_switches": repairs,
        "minimum_defect_after_at_most_one_switch": minimum_defect,
        "one_minimum_profile": minimum_profile,
        "exact_husek_samal_distance": 2,
        "packing_two_switch_path": PACKING_SWITCH_CYCLES,
        "packing_two_switch_profiles": path_profiles,
        "explicit_five_cdc_labels": FIVE_CDC_LABELS,
        "explicit_five_cdc_control": True,
        "solver_independent": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
