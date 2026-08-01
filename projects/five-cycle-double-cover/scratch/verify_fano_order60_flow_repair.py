#!/usr/bin/env python3
"""Solver-independent replay of the order-60 bad-to-good flow repair.

The graph and initial flow are reconstructed independently from the two
order-32 pole recipes.  FiveCDC edge labels induce the target flow by
labeling the five cycle slots 000,001,010,011,100.  One displayed
simple-cycle switch already reaches a flow satisfying the Hušek--Šámal
component-parity condition.  A separate thirteen-switch path preserves
nowhere-zeroness and reaches the cover-induced target exactly.
"""

from __future__ import annotations

import json
from collections import Counter


BASE_GRAPH6 = (
    "_??G@EOGG?GB_AO_g_?CP_??C??O????[O?CA?AG??CA??@???A?O??C???????"
    "G????g???@W???E????@c"
)
BASE_FLOW = (
    3, 6, 2, 7, 5, 7, 2, 7, 5, 2, 1, 7, 2, 4, 6, 5,
    6, 6, 5, 3, 6, 5, 5, 5, 6, 3, 6, 3, 6, 3, 5, 6,
    3, 2, 4, 4, 1, 1, 6, 7, 2, 3, 1, 2, 6, 6, 2, 4,
)
TRANSFORM_A = (0, 4, 3, 7, 1, 5, 2, 6)
TRANSFORM_B = (0, 7, 3, 4, 5, 2, 6, 1)
DELETED_EDGE_A = 2
DELETED_EDGE_B = 6
PORT_PAIRING = ((0, 2), (1, 0), (2, 3), (3, 1))
LABELED_GRAPH6 = (
    "{??K`C?O[@G@P??Go??G?A????w_?_O@C??GC??G??@????G??????C???@O???"
    "J???B????BG?G???????????C?G???????????????@???????????G_???????A??"
    "A@?????_G????@AG????AG??????DC????A???????@???????O????????F?????"
    "C?C?????A?G_??????@??????_?@????????G?????@???????@????????????_??"
    "??????I????????@W????????W?????????X"
)
FIVECDC_LABELS = (
    3, 20, 5, 20, 17, 9, 5, 12, 12, 9, 12, 5, 5, 6, 5,
    3, 24, 5, 10, 9, 17, 24, 12, 20, 9, 17, 24, 18, 9, 17,
    3, 18, 24, 10, 24, 24, 10, 18, 9, 17, 10, 18, 24, 9, 9,
    6, 6, 10, 9, 6, 3, 5, 12, 20, 18, 10, 24, 17, 3, 3,
    17, 18, 5, 5, 10, 17, 9, 24, 20, 12, 12, 20, 24, 18, 18,
    10, 24, 3, 3, 24, 17, 9, 18, 10, 24, 9, 17, 10, 18, 24,
)

ONE_SWITCH_REPAIR = (
    7,
    (1, 2, 8, 11, 18, 22, 24, 26, 27, 30, 31, 33, 35, 37, 39, 40,
     42, 43, 45, 62, 65, 67, 73, 74, 75),
)
ONE_SWITCH_PROFILE = (10, 6, 6, 8, 8, 6, 0)

# Two disjoint T-joins in G-M_7 for the initial value-7 matching M_7.
# They are aligned with ONE_SWITCH_REPAIR for functional 7.  If F is the
# original affine support and J0=F-M_7, then the repair cycle is J0 xor J1.
# After the switch the affine support is M_7 union J1, while J2 lies in its
# complement.  This also proves that the initial flow is not bad for the
# older "every value-class matching fails to pack" test.
VALUE7_T_JOINS = (
    (1, 2, 13, 16, 18, 20, 26, 32, 35, 44, 46, 49, 50, 53, 57, 60,
     61, 62, 63, 64, 69, 71, 72, 73, 75, 81, 83),
    (3, 6, 7, 10, 12, 14, 17, 19, 22, 24, 27, 29, 34, 37, 40, 41,
     43, 45, 47, 48, 55, 56, 74, 80, 82, 85, 86, 87, 88),
)

# Each row is (nonzero value added, graph6 edge ids of a simple cycle).
SWITCHES = (
    (1, (13, 15, 17, 22, 23, 28, 31, 32, 34, 36, 37, 45, 49, 51,
         52, 54, 56, 57, 60, 61, 62, 64, 70, 71, 73, 74, 75)),
    (6, (0, 17, 19, 20, 24, 25)),
    (7, (3, 6, 7, 10, 12, 14, 15, 43, 45, 52, 53, 54, 55, 57, 58,
         59, 60, 63, 68, 69)),
    (2, (2, 3, 4, 28, 32, 35, 36, 44, 45, 46, 63, 64, 68, 69, 73,
         76, 78, 80, 81)),
    (5, (3, 5, 6, 10, 43, 45, 46, 62, 63, 65, 66, 68, 70, 72)),
    (3, (64, 65, 67, 70, 71)),
    (6, (35, 36, 39, 41, 42)),
    (7, (18, 22, 24, 26, 27, 28, 29)),
    (5, (1, 2, 16, 22, 25, 26)),
    (5, (1, 4, 6, 7, 8, 9)),
    (4, (47, 77, 78, 86, 87, 89)),
    (7, (82, 83, 86, 88, 89)),
    (1, (82, 83, 86, 88, 89)),
)

EXPECTED_MISMATCHES = (74, 63, 59, 51, 44, 34, 29, 24, 19, 15, 9, 5, 5, 0)
EXPECTED_ODD_COMPONENTS = (
    (8, 8, 4, 6, 6, 8, 6),
    (8, 12, 10, 8, 4, 10, 2),
    (8, 12, 12, 6, 6, 12, 4),
    (12, 6, 12, 6, 12, 14, 8),
    (8, 6, 10, 12, 12, 10, 12),
    (12, 8, 6, 10, 12, 14, 12),
    (10, 10, 6, 8, 12, 14, 12),
    (8, 10, 6, 8, 12, 16, 12),
    (8, 10, 6, 6, 12, 14, 10),
    (8, 12, 6, 6, 10, 14, 12),
    (8, 10, 6, 6, 10, 14, 12),
    (8, 10, 4, 0, 10, 14, 16),
    (10, 12, 4, 2, 12, 16, 14),
    (10, 10, 4, 0, 10, 16, 14),
)


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    values = tuple(ord(character) - 63 for character in record)
    assert values and 0 <= values[0] <= 62
    vertices = values[0]
    edges = []
    position = 0
    for second in range(1, vertices):
        for first in range(second):
            byte = 1 + position // 6
            assert byte < len(values)
            if values[byte] >> (5 - position % 6) & 1:
                edges.append((first, second))
            position += 1
    assert all(
        not (values[1 + offset // 6] >> (5 - offset % 6) & 1)
        for offset in range(position, 6 * (len(values) - 1))
    )
    return vertices, tuple(edges)


def encode_graph6(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
) -> str:
    edge_set = set(edges)
    bits = [
        int((first, second) in edge_set)
        for second in range(1, vertices)
        for first in range(second)
    ]
    bits.extend([0] * (-len(bits) % 6))
    result = [chr(vertices + 63)]
    for start in range(0, len(bits), 6):
        value = sum(bits[start + index] << (5 - index) for index in range(6))
        result.append(chr(value + 63))
    return "".join(result)


def make_pole(
    edges: tuple[tuple[int, int], ...],
    deleted_edge: int,
) -> tuple[
    tuple[int, ...],
    dict[int, int],
    tuple[tuple[int, int, int], ...],
    tuple[tuple[int, int], ...],
]:
    deleted = set(edges[deleted_edge])
    retained = tuple(vertex for vertex in range(32) if vertex not in deleted)
    index = {vertex: position for position, vertex in enumerate(retained)}
    proper = []
    ports = []
    for edge, (first, second) in enumerate(edges):
        value = BASE_FLOW[edge]
        if first in deleted and second in deleted:
            continue
        if first in deleted:
            ports.append((second, value))
        elif second in deleted:
            ports.append((first, value))
        else:
            proper.append((first, second, value))
    assert (len(retained), len(proper), len(ports)) == (30, 43, 4)
    return retained, index, tuple(proper), tuple(sorted(ports))


def build_graph() -> tuple[tuple[tuple[int, int], ...], tuple[int, ...]]:
    vertices, base_edges = parse_graph6(BASE_GRAPH6)
    assert (vertices, len(base_edges)) == (32, 48)
    first = make_pole(base_edges, DELETED_EDGE_A)
    second = make_pole(base_edges, DELETED_EDGE_B)
    rows = []
    for pole, transform, offset in (
        (first, TRANSFORM_A, 0),
        (second, TRANSFORM_B, 30),
    ):
        _, index, proper, _ = pole
        for old_first, old_second, value in proper:
            edge = tuple(sorted((
                offset + index[old_first],
                offset + index[old_second],
            )))
            rows.append((edge, transform[value]))
    for first_port, second_port in PORT_PAIRING:
        first_vertex, first_value = first[3][first_port]
        second_vertex, second_value = second[3][second_port]
        value = TRANSFORM_A[first_value]
        assert value == TRANSFORM_B[second_value]
        edge = (
            first[1][first_vertex],
            30 + second[1][second_vertex],
        )
        rows.append((edge, value))
    rows.sort(key=lambda row: (row[0][1], row[0][0]))
    edges = tuple(edge for edge, _ in rows)
    values = tuple(value for _, value in rows)
    assert encode_graph6(60, edges) == LABELED_GRAPH6
    return edges, values


def incidence(
    edges: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], ...]:
    rows = [[] for _ in range(60)]
    for edge, (first, second) in enumerate(edges):
        rows[first].append(edge)
        rows[second].append(edge)
    return tuple(tuple(row) for row in rows)


def check_flow(
    values: tuple[int, ...],
    vertex_edges: tuple[tuple[int, ...], ...],
) -> None:
    assert len(values) == 90
    assert all(1 <= value <= 7 for value in values)
    assert all(len(row) == 3 for row in vertex_edges)
    assert all(
        values[row[0]] ^ values[row[1]] ^ values[row[2]] == 0
        for row in vertex_edges
    )


def target_flow() -> tuple[int, ...]:
    slot_labels = (0, 1, 2, 3, 4)
    result = []
    for label in FIVECDC_LABELS:
        coordinates = tuple(
            index for index in range(5) if label >> index & 1
        )
        assert len(coordinates) == 2
        result.append(
            slot_labels[coordinates[0]] ^ slot_labels[coordinates[1]]
        )
    return tuple(result)


def is_simple_cycle(
    selected: tuple[int, ...],
    edges: tuple[tuple[int, int], ...],
) -> bool:
    degree: Counter[int] = Counter()
    adjacency: dict[int, list[int]] = {}
    for edge in selected:
        first, second = edges[edge]
        degree[first] += 1
        degree[second] += 1
        adjacency.setdefault(first, []).append(second)
        adjacency.setdefault(second, []).append(first)
    if not degree or set(degree.values()) != {2}:
        return False
    reached = {next(iter(degree))}
    queue = list(reached)
    for vertex in queue:
        for neighbor in adjacency[vertex]:
            if neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    return reached == set(degree)


def component_defect_count(
    values: tuple[int, ...],
    functional: int,
    edges: tuple[tuple[int, int], ...],
) -> int:
    adjacency = [[] for _ in range(60)]
    for edge, (first, second) in enumerate(edges):
        if (values[edge] & functional).bit_count() % 2 == 0:
            adjacency[first].append(second)
            adjacency[second].append(first)
    components = []
    unseen = set(range(60))
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        queue = [root]
        for vertex in queue:
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        components.append(component)

    affine_value = next(
        value for value in range(1, 8)
        if (value & functional).bit_count() % 2
    )
    marked = {
        vertex
        for edge, (first, second) in enumerate(edges)
        if values[edge] == affine_value
        for vertex in (first, second)
    }
    result = tuple(len(marked & component) % 2 for component in components)

    # Flow conservation makes the same parity appear for all four affine
    # values; checking it catches both convention and implementation errors.
    for value in range(affine_value + 1, 8):
        if (value & functional).bit_count() % 2 == 0:
            continue
        other = {
            vertex
            for edge, (first, second) in enumerate(edges)
            if values[edge] == value
            for vertex in (first, second)
        }
        assert tuple(
            len(other & component) % 2 for component in components
        ) == result
    return sum(result)


def profile(
    values: tuple[int, ...],
    edges: tuple[tuple[int, int], ...],
) -> tuple[int, ...]:
    return tuple(
        component_defect_count(values, functional, edges)
        for functional in range(1, 8)
    )


def main() -> None:
    edges, initial = build_graph()
    vertex_edges = incidence(edges)
    check_flow(initial, vertex_edges)
    target = target_flow()
    check_flow(target, vertex_edges)

    one_value, one_cycle = ONE_SWITCH_REPAIR
    assert is_simple_cycle(one_cycle, edges)
    assert all(initial[edge] != one_value for edge in one_cycle)
    one_repaired = tuple(
        edge_value ^ one_value if edge in one_cycle else edge_value
        for edge, edge_value in enumerate(initial)
    )
    check_flow(one_repaired, vertex_edges)
    assert profile(one_repaired, edges) == ONE_SWITCH_PROFILE

    value7_matching = {
        edge for edge, value in enumerate(initial) if value == 7
    }
    terminals = {
        vertex
        for edge in value7_matching
        for vertex in edges[edge]
    }
    join_sets = tuple(set(row) for row in VALUE7_T_JOINS)
    assert not (join_sets[0] & join_sets[1])
    for join in join_sets:
        assert not (join & value7_matching)
        boundary = {
            vertex
            for vertex, row in enumerate(vertex_edges)
            if sum(edge in join for edge in row) % 2
        }
        assert boundary == terminals
    affine_support7 = {
        edge for edge, value in enumerate(initial)
        if (value & 7).bit_count() % 2
    }
    canonical_join7 = affine_support7 - value7_matching
    assert set(one_cycle) == canonical_join7 ^ join_sets[0]
    repaired_support7 = {
        edge for edge, value in enumerate(one_repaired)
        if (value & 7).bit_count() % 2
    }
    assert repaired_support7 == value7_matching | join_sets[0]
    assert not (repaired_support7 & join_sets[1])

    current = initial
    profiles = [profile(current, edges)]
    mismatches = [sum(first != second for first, second in zip(current, target))]
    clean_steps = []

    for step, (value, selected) in enumerate(SWITCHES, start=1):
        assert 1 <= value <= 7
        assert len(set(selected)) == len(selected)
        assert is_simple_cycle(selected, edges)
        assert all(current[edge] != value for edge in selected)
        current = tuple(
            edge_value ^ value if edge in selected else edge_value
            for edge, edge_value in enumerate(current)
        )
        check_flow(current, vertex_edges)
        current_profile = profile(current, edges)
        profiles.append(current_profile)
        mismatches.append(
            sum(first != second for first, second in zip(current, target))
        )
        if 0 in current_profile:
            clean_steps.append(step)

    assert tuple(mismatches) == EXPECTED_MISMATCHES
    assert tuple(profiles) == EXPECTED_ODD_COMPONENTS
    assert clean_steps == [11, 13]
    assert current == target

    print(json.dumps({
        "schema": "fano-order60-flow-repair-check-v1",
        "order": 60,
        "edges": 90,
        "switch_count": len(SWITCHES),
        "switch_lengths": [len(selected) for _, selected in SWITCHES],
        "one_switch_repair_value": one_value,
        "one_switch_repair_length": len(one_cycle),
        "one_switch_repair_functional": 7,
        "one_switch_repair_profile": ONE_SWITCH_PROFILE,
        "initial_value7_matching_edges": sorted(value7_matching),
        "initial_value7_two_disjoint_t_joins": VALUE7_T_JOINS,
        "initial_value7_matching_packs": True,
        "initial_flow_is_not_all_value_classes_nonpacking": True,
        "one_switch_cycle_is_canonical_join_xor_first_t_join": True,
        "repaired_support_is_matching_union_first_t_join": True,
        "second_t_join_avoids_repaired_support": True,
        "target_mismatches": mismatches,
        "odd_component_profiles": profiles,
        "first_clean_step": 11,
        "first_clean_functional": 4,
        "target_reached_step": 13,
        "all_intermediate_flows_nowhere_zero": True,
        "all_switch_supports_simple_cycles": True,
        "solver_independent": True,
    }, separators=(",", ":")))


if __name__ == "__main__":
    main()
