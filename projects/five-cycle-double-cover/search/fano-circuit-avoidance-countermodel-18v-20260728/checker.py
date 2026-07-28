#!/usr/bin/env python3
"""Independent finite checker for the 18-vertex avoidance countermodel.

Only the Python standard library is used.  Values 0,...,7 represent
F_2^3 and addition is bitwise XOR.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from itertools import combinations, product
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
GRAPH6 = "QCGY?c?W???F_GAAo@?D@P??`?G"
FLOW = (
    6, 3, 5, 3, 4, 7, 5, 3, 6,
    3, 5, 6, 3, 5, 1, 2, 4, 4,
    5, 1, 7, 3, 5, 6, 6, 3, 2,
)
SWITCH_VALUE = 6
MARK_VALUE = 3
MARKS = (1, 3, 9)
SEPARATOR = (1, 6)
REPAIR_MASK = 34_367_022
ALTERNATIVE_SWITCH_VALUE = 1
ALTERNATIVE_CIRCUIT_MASK = 16_783_875

MINIMALITY_SOURCES = {
    10: (
        "7aec0fba73c081d7eebc551fc46b2484e73e58b2d36718dee105dbb6226e76aa",
        1,
    ),
    12: (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        0,
    ),
    14: (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        0,
    ),
    16: (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        0,
    ),
    18: (
        "2660e7d5c8a351b4ed3d69f8df316e748e264a630c01328ea4bed43f96f78dfd",
        2,
    ),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parse_graph6(text: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    data = text.strip().encode("ascii")
    require(data and data[0] != ord("~"), "only short graph6 is supported")
    vertices = data[0] - 63
    bits = []
    for byte in data[1:]:
        value = byte - 63
        require(0 <= value < 64, "invalid graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    index = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[index]:
                edges.append((left, right))
            index += 1
    return vertices, tuple(sorted(edges))


VERTICES, EDGES = parse_graph6(GRAPH6)
EDGE_COUNT = len(EDGES)


def incidence() -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(VERTICES)]
    for edge, (left, right) in enumerate(EDGES):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(sorted(row)) for row in rows)


INCIDENT = incidence()


def components(
    edge_ids: Iterable[int],
    removed_vertices: frozenset[int] = frozenset(),
) -> tuple[frozenset[int], ...]:
    adjacency = {
        vertex: set()
        for vertex in range(VERTICES)
        if vertex not in removed_vertices
    }
    for edge in edge_ids:
        left, right = EDGES[edge]
        if left in adjacency and right in adjacency:
            adjacency[left].add(right)
            adjacency[right].add(left)
    unseen = set(adjacency)
    result = []
    while unseen:
        start = min(unseen)
        reached = {start}
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for other in adjacency[vertex] & unseen:
                reached.add(other)
                unseen.remove(other)
                queue.append(other)
        unseen.discard(start)
        result.append(frozenset(reached))
    return tuple(result)


def induced_has_cycle(vertices: frozenset[int]) -> bool:
    parent = {vertex: vertex for vertex in vertices}

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in EDGES:
        if left not in vertices or right not in vertices:
            continue
        root_left, root_right = find(left), find(right)
        if root_left == root_right:
            return True
        parent[root_left] = root_right
    return False


def graph_properties() -> dict[str, object]:
    require(VERTICES == 18 and EDGE_COUNT == 27, "wrong graph order or size")
    require(len({tuple(sorted(edge)) for edge in EDGES}) == EDGE_COUNT, "not simple")
    require(all(left != right for left, right in EDGES), "loop found")
    require(all(len(row) == 3 for row in INCIDENT), "not cubic")
    require(len(components(range(EDGE_COUNT))) == 1, "not connected")

    adjacency = [[] for _ in range(VERTICES)]
    for left, right in EDGES:
        adjacency[left].append(right)
        adjacency[right].append(left)
    girth = VERTICES + 1
    for root in range(VERTICES):
        distance = [-1] * VERTICES
        parent = [-1] * VERTICES
        distance[root] = 0
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for other in adjacency[vertex]:
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    girth = min(girth, distance[vertex] + distance[other] + 1)
    require(girth == 5, "wrong girth")

    small_cyclic_cuts = []
    for size in range(1, 4):
        for cut in combinations(range(EDGE_COUNT), size):
            remaining = [edge for edge in range(EDGE_COUNT) if edge not in cut]
            pieces = components(remaining)
            if sum(induced_has_cycle(piece) for piece in pieces) >= 2:
                small_cyclic_cuts.append(cut)
    require(not small_cyclic_cuts, "cyclic edge cut below four")

    # Exhaustive proper three-edge-colouring search.
    colors = [-1] * EDGE_COUNT
    used = [set() for _ in range(VERTICES)]

    def tait_search(colored: int) -> bool:
        if colored == EDGE_COUNT:
            return True
        edge = max(
            (item for item in range(EDGE_COUNT) if colors[item] < 0),
            key=lambda item: (
                len(used[EDGES[item][0]] | used[EDGES[item][1]]),
                -item,
            ),
        )
        left, right = EDGES[edge]
        for color in range(3):
            if color in used[left] or color in used[right]:
                continue
            colors[edge] = color
            used[left].add(color)
            used[right].add(color)
            if tait_search(colored + 1):
                return True
            used[left].remove(color)
            used[right].remove(color)
            colors[edge] = -1
        return False

    require(not tait_search(0), "graph is Tait-colourable")
    return {
        "vertices": VERTICES,
        "edges": EDGE_COUNT,
        "simple": True,
        "cubic": True,
        "connected": True,
        "girth": girth,
        "cyclically_4_edge_connected": True,
        "tait_colourable": False,
    }


def selected_degrees(mask: int) -> tuple[int, ...]:
    degrees = [0] * VERTICES
    for edge, (left, right) in enumerate(EDGES):
        if (mask >> edge) & 1:
            degrees[left] += 1
            degrees[right] += 1
    return tuple(degrees)


def is_flow(flow: tuple[int, ...]) -> bool:
    if len(flow) != EDGE_COUNT or any(value not in range(1, 8) for value in flow):
        return False
    boundary = [0] * VERTICES
    for value, (left, right) in zip(flow, EDGES):
        boundary[left] ^= value
        boundary[right] ^= value
    return not any(boundary)


def fundamental_cycle_space(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> tuple[int, ...]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    for row in adjacency:
        row.sort()
    parent = [-1] * vertices
    parent_edge = [-1] * vertices
    depth = [0] * vertices
    parent[0] = 0
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other, edge in adjacency[vertex]:
            if parent[other] >= 0:
                continue
            parent[other] = vertex
            parent_edge[other] = edge
            depth[other] = depth[vertex] + 1
            stack.append(other)
    require(all(value >= 0 for value in parent), "cycle-space graph disconnected")
    tree_edges = frozenset(parent_edge[1:])
    basis = []
    for edge, (first, second) in enumerate(edges):
        if edge in tree_edges:
            continue
        cycle = 1 << edge
        left, right = first, second
        while depth[left] > depth[right]:
            cycle ^= 1 << parent_edge[left]
            left = parent[left]
        while depth[right] > depth[left]:
            cycle ^= 1 << parent_edge[right]
            right = parent[right]
        while left != right:
            cycle ^= 1 << parent_edge[left]
            left = parent[left]
            cycle ^= 1 << parent_edge[right]
            right = parent[right]
        basis.append(cycle)
    cycles = [0]
    for basis_cycle in basis:
        cycles.extend(cycle ^ basis_cycle for cycle in tuple(cycles))
    return tuple(sorted(cycles))


def elementary_circuits(cycles: Iterable[int]) -> tuple[int, ...]:
    result = []
    for mask in cycles:
        if not mask:
            continue
        degrees = selected_degrees(mask)
        if any(degree not in (0, 2) for degree in degrees):
            continue
        selected = [edge for edge in range(EDGE_COUNT) if (mask >> edge) & 1]
        active = {vertex for vertex, degree in enumerate(degrees) if degree}
        nonempty = [
            piece & active for piece in components(selected) if piece & active
        ]
        if len(nonempty) == 1 and nonempty[0] == active:
            result.append(mask)
    return tuple(result)


Pair = tuple[int, int]
PAIR_INDEX = {pair: index for index, pair in enumerate(combinations(range(8), 2))}


def normalized_pair(left: int, right: int) -> Pair:
    return (left, right) if left < right else (right, left)


def compatibility_rows(
    flow: tuple[int, ...],
) -> list[tuple[int, int]]:
    rows: list[tuple[int, int]] = []
    for edge, (left, right) in enumerate(EDGES):
        left_other = next(item for item in INCIDENT[left] if item != edge)
        right_other = next(item for item in INCIDENT[right] if item != edge)
        difference = flow[left_other] ^ flow[right_other]
        value = flow[edge]
        orthogonal = [
            vector
            for vector in range(1, 8)
            if ((vector & value).bit_count() & 1) == 0
        ]
        require(len(orthogonal) == 3, "wrong orthogonal plane")
        for functional in orthogonal[:2]:
            mask = 0
            for vertex in (left, right):
                for bit in range(3):
                    if (functional >> bit) & 1:
                        mask ^= 1 << (3 * vertex + bit)
            rows.append((mask, (functional & difference).bit_count() & 1))
    rows.extend((1 << bit, 0) for bit in range(3))
    return rows


def rref(rows: Iterable[tuple[int, int]]) -> dict[int, tuple[int, int]]:
    pivots: dict[int, tuple[int, int]] = {}
    for original_mask, original_rhs in rows:
        mask, rhs = original_mask, original_rhs
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (mask, rhs)
                break
            old_mask, old_rhs = pivots[pivot]
            mask ^= old_mask
            rhs ^= old_rhs
        require(mask != 0 or rhs == 0, "inconsistent potential system")
    return pivots


def assignment(
    pivots: dict[int, tuple[int, int]],
    free: tuple[int, ...],
    free_bits: int,
) -> int:
    value = sum(
        1 << variable
        for index, variable in enumerate(free)
        if (free_bits >> index) & 1
    )
    for pivot in sorted(pivots):
        mask, rhs = pivots[pivot]
        bit = ((mask & ((1 << pivot) - 1) & value).bit_count() & 1) ^ rhs
        if bit:
            value |= 1 << pivot
    return value


def labels_from_potential(
    flow: tuple[int, ...], potential_word: int
) -> tuple[Pair, ...]:
    potentials = tuple(
        sum(
            ((potential_word >> (3 * vertex + bit)) & 1) << bit
            for bit in range(3)
        )
        for vertex in range(VERTICES)
    )
    labels = []
    for edge, (left, right) in enumerate(EDGES):
        left_other = next(item for item in INCIDENT[left] if item != edge)
        base = potentials[left] ^ flow[left_other]
        pair = normalized_pair(base, base ^ flow[edge])
        right_other = next(item for item in INCIDENT[right] if item != edge)
        base_right = potentials[right] ^ flow[right_other]
        pair_right = normalized_pair(base_right, base_right ^ flow[edge])
        require(pair == pair_right, "potential gives inconsistent edge label")
        labels.append(pair)
    for vertex in range(VERTICES):
        counts = Counter(
            coordinate
            for edge in INCIDENT[vertex]
            for coordinate in labels[edge]
        )
        require(all(count % 2 == 0 for count in counts.values()), "cover parity failure")
    return tuple(labels)


def five_coloring(used_pairs: frozenset[Pair]) -> tuple[int, ...] | None:
    adjacency = [set() for _ in range(8)]
    for left, right in used_pairs:
        adjacency[left].add(right)
        adjacency[right].add(left)
    colors = [-1] * 8

    def search(colored: int, used_colors: int) -> bool:
        if colored == 8:
            return True
        vertex = max(
            (item for item in range(8) if colors[item] < 0),
            key=lambda item: (
                len({colors[n] for n in adjacency[item] if colors[n] >= 0}),
                len(adjacency[item]),
                -item,
            ),
        )
        forbidden = {colors[n] for n in adjacency[vertex] if colors[n] >= 0}
        for color in range(min(used_colors + 1, 5)):
            if color in forbidden:
                continue
            colors[vertex] = color
            if search(colored + 1, max(used_colors, color + 1)):
                return True
            colors[vertex] = -1
        return False

    return tuple(colors) if search(0, 0) else None


def potential_audit(flow: tuple[int, ...]) -> dict[str, object]:
    rows = compatibility_rows(flow)
    pivots = rref(rows)
    free = tuple(variable for variable in range(3 * VERTICES) if variable not in pivots)
    covers = []
    for free_bits in range(1 << len(free)):
        word = assignment(pivots, free, free_bits)
        labels = labels_from_potential(flow, word)
        used = frozenset(labels)
        coloring = five_coloring(used)
        six_cliques = [
            six
            for six in combinations(range(8), 6)
            if frozenset(combinations(six, 2)) <= used
        ]
        maximum_clique = max(
            size
            for size in range(1, 9)
            if any(
                frozenset(combinations(vertices, 2)) <= used
                for vertices in combinations(range(8), size)
            )
        )
        covers.append(
            {
                "free_assignment_index": free_bits,
                "potential_word": word,
                "used_pair_types": len(used),
                "maximum_clique_size": maximum_clique,
                "six_cliques": [list(row) for row in six_cliques],
                "five_coloring": list(coloring) if coloring is not None else None,
                "labels": [list(pair) for pair in labels],
            }
        )
    return {
        "rows": len(rows),
        "rank": len(pivots),
        "free_dimension": len(free),
        "gauged_potential_solutions": len(covers),
        "covers": covers,
    }


def odd_cut_audit() -> int:
    allowed = [edge for edge, value in enumerate(FLOW) if value != SWITCH_VALUE]
    marks = frozenset(MARKS)
    violations = 0
    # Fix vertex 0 outside the shore to count each cut once.
    for shore_bits in range(1 << (VERTICES - 1)):
        shore = {
            vertex + 1
            for vertex in range(VERTICES - 1)
            if (shore_bits >> vertex) & 1
        }
        cut = frozenset(
            edge
            for edge in allowed
            if (EDGES[edge][0] in shore) != (EDGES[edge][1] in shore)
        )
        if cut and len(cut) % 2 and cut <= marks:
            violations += 1
    return violations


def petersen_minimality_audit(graph6: str) -> dict[str, int]:
    vertices, edges = parse_graph6(graph6)
    require(vertices == 10 and len(edges) == 15, "wrong Petersen source")
    global VERTICES, EDGES, EDGE_COUNT, INCIDENT
    saved = (VERTICES, EDGES, EDGE_COUNT, INCIDENT)
    VERTICES, EDGES, EDGE_COUNT = vertices, edges, len(edges)
    INCIDENT = incidence()
    try:
        cycles = fundamental_cycle_space(VERTICES, EDGES)
        circuits = elementary_circuits(cycles)
        cache: dict[tuple[int, int], bool] = {}
        nowhere_zero = 0
        for first, second, third in product(cycles, repeat=3):
            flow = tuple(
                ((first >> edge) & 1)
                | (((second >> edge) & 1) << 1)
                | (((third >> edge) & 1) << 2)
                for edge in range(EDGE_COUNT)
            )
            if 0 in flow:
                continue
            nowhere_zero += 1
            value_masks = {
                value: sum(
                    1 << edge
                    for edge, edge_value in enumerate(flow)
                    if edge_value == value
                )
                for value in range(1, 8)
            }
            for switch_value in range(1, 8):
                allowed = tuple(
                    circuit
                    for circuit in circuits
                    if not (circuit & value_masks[switch_value])
                )
                for mark_value in range(1, 8):
                    if mark_value == switch_value:
                        continue
                    key = (value_masks[switch_value], value_masks[mark_value])
                    if key in cache:
                        require(cache[key], "cached Petersen failure")
                        continue
                    marked_edges = [
                        edge
                        for edge in range(EDGE_COUNT)
                        if (value_masks[mark_value] >> edge) & 1
                    ]
                    good = all(
                        any(all((circuit >> edge) & 1 for edge in marks) for circuit in allowed)
                        for size in range(1, min(3, len(marked_edges)) + 1)
                        for marks in combinations(marked_edges, size)
                    )
                    cache[key] = good
                    require(good, "Petersen has a smaller avoidance failure")
        require(nowhere_zero == 28_560, "wrong Petersen flow count")
        return {
            "binary_cycles": len(cycles),
            "elementary_circuits": len(circuits),
            "nowhere_zero_F2_3_flows": nowhere_zero,
            "distinct_value_mask_pairs_checked": len(cache),
            "avoidance_failures": 0,
        }
    finally:
        VERTICES, EDGES, EDGE_COUNT, INCIDENT = saved


def minimality_audit() -> dict[str, object]:
    source_root = (
        ROOT
        / "search/focused-theta-choice-through28-20260727/artifacts"
    )
    rows_by_order = {}
    for order, (expected_hash, expected_rows) in MINIMALITY_SOURCES.items():
        path = source_root / f"cyclic4-nontait-order{order}.g6"
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected_hash, f"source hash changed at order {order}")
        rows = tuple(row for row in path.read_text(encoding="ascii").splitlines() if row)
        require(len(rows) == expected_rows, f"source row count changed at order {order}")
        rows_by_order[order] = rows
    require(rows_by_order[18][0] == GRAPH6, "countermodel is not first canonical order-18 row")
    petersen = petersen_minimality_audit(rows_by_order[10][0])
    return {
        "scope": (
            "Relative to the frozen canonical Snarkhunter cyclically-4 "
            "non-Tait simple cubic lists; source completeness is inherited "
            "from that package."
        ),
        "source_rows_by_order": {
            str(order): len(rows) for order, rows in rows_by_order.items()
        },
        "source_sha256_by_order": {
            str(order): MINIMALITY_SOURCES[order][0]
            for order in sorted(MINIMALITY_SOURCES)
        },
        "petersen_exhaustion": petersen,
        "smallest_failure_order": 18,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "report.json")
    parser.add_argument("--skip-minimality", action="store_true")
    arguments = parser.parse_args()

    require((HERE / "canonical.g6").read_text(encoding="ascii").strip() == GRAPH6,
            "canonical.g6 differs from checker")
    properties = graph_properties()
    require(is_flow(FLOW), "displayed assignment is not a nowhere-zero flow")
    for value in range(1, 8):
        value_edges = [edge for edge, item in enumerate(FLOW) if item == value]
        endpoints = [vertex for edge in value_edges for vertex in EDGES[edge]]
        require(len(endpoints) == len(set(endpoints)), "value class is not a matching")

    h_edges = [edge for edge, value in enumerate(FLOW) if value != SWITCH_VALUE]
    h_components = components(h_edges)
    require(len(h_components) == 1, "G-M_6 is not connected")
    require(
        all(len(components([item for item in h_edges if item != edge])) == 1 for edge in h_edges),
        "G-M_6 has a bridge",
    )
    require(all(FLOW[edge] == MARK_VALUE for edge in MARKS), "marked values differ")
    separated = components(h_edges, frozenset(SEPARATOR))
    expected_separated = (
        frozenset((0, 2, 4, 8, 9, 10, 11, 12, 13, 14, 15)),
        frozenset((3, 5, 7, 16, 17)),
    )
    require(separated == expected_separated, "wrong two-vertex separation")
    require(set(EDGES[MARKS[0]]) <= separated[0], "first mark on wrong shore")
    require(set(EDGES[MARKS[2]]) <= separated[1], "third mark on wrong shore")
    require(set(EDGES[MARKS[1]]) == set(SEPARATOR), "middle mark is not separator edge")

    cycles = fundamental_cycle_space(VERTICES, EDGES)
    circuits = elementary_circuits(cycles)
    forbidden_mask = sum(
        1 << edge for edge, value in enumerate(FLOW) if value == SWITCH_VALUE
    )
    allowed_circuits = tuple(circuit for circuit in circuits if not (circuit & forbidden_mask))
    mark_pattern_profile = Counter(
        tuple(edge for edge in MARKS if (circuit >> edge) & 1)
        for circuit in allowed_circuits
    )
    require(
        not any(all((circuit >> edge) & 1 for edge in MARKS) for circuit in allowed_circuits),
        "a legal connected circuit contains all marks",
    )
    require(odd_cut_audit() == 0, "an odd H-cut is contained in the marks")

    require(not (REPAIR_MASK & forbidden_mask), "repair uses a switch-value edge")
    require(all((REPAIR_MASK >> edge) & 1 for edge in MARKS), "repair misses a mark")
    require(all(degree in (0, 2) for degree in selected_degrees(REPAIR_MASK)),
            "repair is not a binary cycle")
    repair_edges = [edge for edge in range(EDGE_COUNT) if (REPAIR_MASK >> edge) & 1]
    active = {
        vertex
        for edge in repair_edges
        for vertex in EDGES[edge]
    }
    repair_components = tuple(
        piece & active
        for piece in components(repair_edges)
        if piece & active
    )
    require(sorted(map(len, repair_components)) == [5, 6], "wrong repair components")
    switched = tuple(
        value ^ SWITCH_VALUE if (REPAIR_MASK >> edge) & 1 else value
        for edge, value in enumerate(FLOW)
    )
    require(is_flow(switched), "repair switch is not a nowhere-zero flow")

    initial_potentials = potential_audit(FLOW)
    require(initial_potentials["gauged_potential_solutions"] == 4,
            "wrong initial potential count")
    for cover in initial_potentials["covers"]:
        require(cover["used_pair_types"] == 15, "initial cover does not use 15 pairs")
        require(cover["maximum_clique_size"] == 6, "initial clique number is not six")
        require(len(cover["six_cliques"]) == 1, "initial cover does not force K6")
        require(cover["five_coloring"] is None, "initial cover is five-colourable")

    repaired_potentials = potential_audit(switched)
    require(repaired_potentials["gauged_potential_solutions"] == 4,
            "wrong repaired potential count")
    require(
        all(cover["five_coloring"] is not None for cover in repaired_potentials["covers"]),
        "a repaired compatible cover is not five-colourable",
    )
    require(
        all(cover["maximum_clique_size"] == 5 for cover in repaired_potentials["covers"]),
        "a repaired compatible cover does not have clique number five",
    )

    alternative_degrees = selected_degrees(ALTERNATIVE_CIRCUIT_MASK)
    require(
        all(degree in (0, 2) for degree in alternative_degrees),
        "alternative support is not a binary cycle",
    )
    alternative_edges = [
        edge
        for edge in range(EDGE_COUNT)
        if (ALTERNATIVE_CIRCUIT_MASK >> edge) & 1
    ]
    alternative_active = {
        vertex
        for edge in alternative_edges
        for vertex in EDGES[edge]
    }
    alternative_components = [
        piece & alternative_active
        for piece in components(alternative_edges)
        if piece & alternative_active
    ]
    require(
        len(alternative_components) == 1
        and len(alternative_active) == len(alternative_edges) == 6,
        "alternative support is not one six-circuit",
    )
    require(
        all(FLOW[edge] != ALTERNATIVE_SWITCH_VALUE for edge in alternative_edges),
        "alternative circuit contains a switch-value edge",
    )
    alternative_flow = tuple(
        value ^ ALTERNATIVE_SWITCH_VALUE
        if (ALTERNATIVE_CIRCUIT_MASK >> edge) & 1
        else value
        for edge, value in enumerate(FLOW)
    )
    require(is_flow(alternative_flow), "alternative switch is not a flow")
    alternative_potentials = potential_audit(alternative_flow)
    require(
        any(
            cover["five_coloring"] is not None
            for cover in alternative_potentials["covers"]
        ),
        "alternative connected switch does not repair pure merging",
    )

    report = {
        "schema": "fano-circuit-avoidance-countermodel-18v-v1",
        "status": "PASS",
        "scope_warning": (
            "This refutes a prescribed connected-circuit avoidance lemma "
            "inside the Oum pure-merge strategy. The same flow has another "
            "one-circuit repair, so this is not a countermodel to the "
            "unrestricted one-circuit repair conjecture and not a FiveCDC "
            "counterexample."
        ),
        "canonical_graph6": GRAPH6,
        "graph": properties,
        "flow_values_by_edge": list(FLOW),
        "switch_value": SWITCH_VALUE,
        "mark_value": MARK_VALUE,
        "marked_edge_ids": list(MARKS),
        "marked_edges": [list(EDGES[edge]) for edge in MARKS],
        "value_classes_are_matchings": True,
        "G_minus_M_t": {
            "connected": True,
            "bridgeless": True,
            "separator_vertices": list(SEPARATOR),
            "separated_components": [sorted(piece) for piece in separated],
            "odd_cuts_contained_in_marks": 0,
        },
        "circuit_audit": {
            "binary_cycle_space_size": len(cycles),
            "elementary_circuits": len(circuits),
            "circuits_avoiding_M_t": len(allowed_circuits),
            "mark_pattern_profile": {
                ",".join(map(str, pattern)): count
                for pattern, count in sorted(mark_pattern_profile.items())
            },
            "circuits_through_all_three_marks": 0,
        },
        "initial_Oum_potential_audit": initial_potentials,
        "disconnected_repair": {
            "binary_cycle_mask": REPAIR_MASK,
            "edge_ids": repair_edges,
            "edges": [list(EDGES[edge]) for edge in repair_edges],
            "component_vertices": [sorted(piece) for piece in repair_components],
            "component_lengths": sorted(map(len, repair_components)),
            "switched_flow_values_by_edge": list(switched),
            "repaired_Oum_potential_audit": repaired_potentials,
        },
        "separate_connected_repair": {
            "scope": (
                "This proves that the displayed prescribed-triple failure "
                "does not refute unrestricted one-circuit repair."
            ),
            "switch_value": ALTERNATIVE_SWITCH_VALUE,
            "circuit_mask": ALTERNATIVE_CIRCUIT_MASK,
            "edge_ids": alternative_edges,
            "edges": [list(EDGES[edge]) for edge in alternative_edges],
            "switched_flow_values_by_edge": list(alternative_flow),
            "repaired_Oum_potential_audit": alternative_potentials,
        },
        "minimality_audit": (
            {"skipped": True}
            if arguments.skip_minimality
            else minimality_audit()
        ),
    }
    arguments.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": report["status"],
        "vertices": VERTICES,
        "binary_cycles": len(cycles),
        "elementary_circuits": len(circuits),
        "allowed_circuits": len(allowed_circuits),
        "initial_potentials": initial_potentials["gauged_potential_solutions"],
        "repaired_potentials": repaired_potentials["gauged_potential_solutions"],
        "minimality_skipped": arguments.skip_minimality,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
