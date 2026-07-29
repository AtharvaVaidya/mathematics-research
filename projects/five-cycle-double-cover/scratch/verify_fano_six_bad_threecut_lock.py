#!/usr/bin/env python3
"""Independently verify the order-18 six-bad-flow three-cut lock.

No SAT solver or graph library is used.  Binary pole cycles are enumerated
from a row-reduced incidence matrix, and the local two-cycle formula is
checked directly.

This concerns an auxiliary fixed-flow clean-projection statement.  It is not
a Five-Cycle Double Cover counterexample or proof.
"""

from __future__ import annotations

import json
from collections import Counter


GRAPH6 = "Q???C@?K@O@aDAw?GW?J?_g?Y??"
FLOW = (
    1, 5, 6, 5, 3, 4, 6, 5, 3, 3, 4, 7, 2, 7,
    5, 2, 5, 7, 1, 6, 7, 3, 1, 2, 6, 2, 4,
)
SHORE_A = frozenset({2, 3, 4, 5, 9, 10, 11, 12, 17})
SHORE_B = frozenset(set(range(18)) - SHORE_A)
CUT_EDGES = frozenset({14, 18, 26})
EXPECTED_PROFILES = {
    **{
        edge: (4, 5, 6)
        for edge in (0, 1, 12, 13, 15, 16, 17, 19, 20, 21, 22, 23)
    },
    **{
        edge: (1, 3, 7)
        for edge in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 24, 25)
    },
    14: (),
    18: (),
    26: (),
}


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    values = [ord(character) - 63 for character in record]
    assert values and all(0 <= value <= 63 for value in values)
    assert values[0] <= 62
    vertices = values[0]
    edges = []
    bit = 0
    for right in range(1, vertices):
        for left in range(right):
            byte = 1 + bit // 6
            assert byte < len(values)
            if (values[byte] >> (5 - bit % 6)) & 1:
                edges.append((left, right))
            bit += 1
    return vertices, tuple(edges)


def dot(first: int, second: int) -> int:
    return (first & second).bit_count() & 1


def incidence(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], ...]:
    rows = [[] for _ in range(vertices)]
    for edge, (first, second) in enumerate(edges):
        rows[first].append(edge)
        rows[second].append(edge)
    return tuple(tuple(row) for row in rows)


def connected(
    vertices: frozenset[int],
    edges: tuple[tuple[int, int], ...],
) -> bool:
    root = min(vertices)
    seen = {root}
    stack = [root]
    while stack:
        vertex = stack.pop()
        for first, second in edges:
            if first == vertex and second in vertices and second not in seen:
                seen.add(second)
                stack.append(second)
            elif second == vertex and first in vertices and first not in seen:
                seen.add(first)
                stack.append(first)
    return seen == set(vertices)


def nullspace(rows: list[int], columns: int) -> tuple[int, ...]:
    """Enumerate the nullspace of a binary matrix represented by row masks."""
    reduced = list(rows)
    pivots = []
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(reduced)) if reduced[row] >> column & 1),
            None,
        )
        if pivot is None:
            continue
        reduced[rank], reduced[pivot] = reduced[pivot], reduced[rank]
        for row in range(len(reduced)):
            if row != rank and reduced[row] >> column & 1:
                reduced[row] ^= reduced[rank]
        pivots.append(column)
        rank += 1
    reduced = reduced[:rank]
    free = [column for column in range(columns) if column not in set(pivots)]
    basis = []
    for column in free:
        vector = 1 << column
        for row, pivot in zip(reduced, pivots, strict=True):
            if row >> column & 1:
                vector |= 1 << pivot
        basis.append(vector)
    answers = [0]
    for vector in basis:
        answers.extend(value ^ vector for value in tuple(answers))
    assert len(answers) == 1 << (columns - rank)
    assert all(
        all((value & row).bit_count() % 2 == 0 for row in rows)
        for value in answers
    )
    return tuple(answers)


def make_pole(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    values: tuple[int, ...],
    deleted_edge: int,
) -> tuple[
    tuple[int, ...],
    tuple[tuple[int, int], ...],
    tuple[int, ...],
    tuple[tuple[int, int], ...],
]:
    deleted_vertices = set(edges[deleted_edge])
    retained_vertices = tuple(
        vertex for vertex in range(vertices) if vertex not in deleted_vertices
    )
    proper_edges = []
    proper_values = []
    ports = []
    for edge, (first, second) in enumerate(edges):
        if first in deleted_vertices and second in deleted_vertices:
            continue
        if first in deleted_vertices:
            ports.append((second, values[edge]))
        elif second in deleted_vertices:
            ports.append((first, values[edge]))
        else:
            proper_edges.append((first, second))
            proper_values.append(values[edge])
    assert len(retained_vertices) == 16
    assert len(proper_edges) == 22
    assert len(ports) == 4
    return (
        retained_vertices,
        tuple(proper_edges),
        tuple(proper_values),
        tuple(sorted(ports)),
    )


def pole_cycles(
    retained_vertices: tuple[int, ...],
    proper_edges: tuple[tuple[int, int], ...],
    ports: tuple[tuple[int, int], ...],
) -> tuple[int, ...]:
    vertex_index = {
        vertex: index for index, vertex in enumerate(retained_vertices)
    }
    rows = [0 for _ in retained_vertices]
    for edge, (first, second) in enumerate(proper_edges):
        rows[vertex_index[first]] |= 1 << edge
        rows[vertex_index[second]] |= 1 << edge
    offset = len(proper_edges)
    for port, (vertex, _) in enumerate(ports):
        rows[vertex_index[vertex]] |= 1 << (offset + port)
    assert all(row.bit_count() == 3 for row in rows)
    cycles = nullspace(rows, len(proper_edges) + len(ports))
    assert len(cycles) == 1024
    return cycles


def factor_cut_masks(
    retained_vertices: tuple[int, ...],
    proper_edges: tuple[tuple[int, int], ...],
    ports: tuple[tuple[int, int], ...],
    factor: int,
) -> tuple[int, ...]:
    vertex_index = {
        vertex: index for index, vertex in enumerate(retained_vertices)
    }
    parent = list(range(len(retained_vertices)))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def union(first: int, second: int) -> None:
        first = find(first)
        second = find(second)
        if first != second:
            parent[second] = first

    for edge, (first, second) in enumerate(proper_edges):
        if factor >> edge & 1:
            union(vertex_index[first], vertex_index[second])

    components: dict[int, set[int]] = {}
    for vertex in range(len(retained_vertices)):
        components.setdefault(find(vertex), set()).add(vertex)

    offset = len(proper_edges)
    cuts = []
    for component in components.values():
        open_component = any(
            factor >> (offset + port) & 1
            and vertex_index[vertex] in component
            for port, (vertex, _) in enumerate(ports)
        )
        if open_component:
            continue
        cut = 0
        for edge, (first, second) in enumerate(proper_edges):
            if (
                (vertex_index[first] in component)
                != (vertex_index[second] in component)
            ):
                cut |= 1 << edge
        for port, (vertex, _) in enumerate(ports):
            if vertex_index[vertex] in component:
                cut |= 1 << (offset + port)
        cuts.append(cut)
    return tuple(cuts)


def local_cleanable(
    retained_vertices: tuple[int, ...],
    proper_edges: tuple[tuple[int, int], ...],
    proper_values: tuple[int, ...],
    ports: tuple[tuple[int, int], ...],
    cycles: tuple[int, ...],
    functional: int,
) -> tuple[int, int] | None:
    values = proper_values + tuple(value for _, value in ports)
    factor = sum(
        1 << edge
        for edge, value in enumerate(values)
        if dot(functional, value) == 0
    )
    cuts = factor_cut_masks(
        retained_vertices,
        proper_edges,
        ports,
        factor,
    )
    for first in cycles:
        missing = factor & ~first
        for second in cycles:
            if second & missing != missing:
                continue
            product = first & second
            if all((product & cut).bit_count() % 2 == 0 for cut in cuts):
                return first, second
    return None


def boundary_size(
    shore: frozenset[int],
    proper_edges: tuple[tuple[int, int], ...],
    ports: tuple[tuple[int, int], ...],
) -> int:
    return sum(
        (first in shore) != (second in shore)
        for first, second in proper_edges
    ) + sum(vertex in shore for vertex, _ in ports)


def main() -> int:
    vertices, edges = parse_graph6(GRAPH6)
    assert vertices == 18
    assert len(edges) == len(FLOW) == 27
    rows = incidence(vertices, edges)
    assert all(len(row) == 3 for row in rows)
    for row in rows:
        total = 0
        for edge in row:
            total ^= FLOW[edge]
        assert total == 0
    assert all(1 <= value <= 7 for value in FLOW)

    actual_cut = frozenset(
        edge
        for edge, (first, second) in enumerate(edges)
        if (first in SHORE_A) != (second in SHORE_A)
    )
    assert actual_cut == CUT_EDGES
    for shore in (SHORE_A, SHORE_B):
        induced = tuple(
            edge for edge in edges if edge[0] in shore and edge[1] in shore
        )
        assert len(shore) == 9
        assert len(induced) == 12
        assert connected(shore, induced)
        assert len(induced) >= len(shore)

    profiles = {}
    witnesses = {}
    locked_shores = {}
    for deleted_edge in range(len(edges)):
        pole = make_pole(vertices, edges, FLOW, deleted_edge)
        retained, proper_edges, proper_values, ports = pole
        cycles = pole_cycles(retained, proper_edges, ports)
        profile = []
        pole_witnesses = {}
        for functional in range(1, 8):
            witness = local_cleanable(
                retained,
                proper_edges,
                proper_values,
                ports,
                cycles,
                functional,
            )
            if witness is None:
                profile.append(functional)
            else:
                pole_witnesses[str(functional)] = [
                    hex(witness[0]),
                    hex(witness[1]),
                ]
        profiles[deleted_edge] = tuple(profile)
        witnesses[str(deleted_edge)] = pole_witnesses
        assert tuple(profile) == EXPECTED_PROFILES[deleted_edge]

        first, second = edges[deleted_edge]
        if deleted_edge in CUT_EDGES:
            assert (first in SHORE_A) != (second in SHORE_A)
            assert not profile
            continue
        deleted_shore = SHORE_A if first in SHORE_A else SHORE_B
        assert second in deleted_shore
        locked = SHORE_B if deleted_shore == SHORE_A else SHORE_A
        assert locked <= set(retained)
        assert boundary_size(locked, proper_edges, ports) == 3
        locked_induced = tuple(
            edge
            for edge in proper_edges
            if edge[0] in locked and edge[1] in locked
        )
        assert len(locked_induced) == 12
        assert connected(locked, locked_induced)
        locked_shores[str(deleted_edge)] = (
            "B" if locked == SHORE_B else "A"
        )

    histogram = Counter(profiles.values())
    assert histogram == Counter({(4, 5, 6): 12, (1, 3, 7): 12, (): 3})
    report = {
        "schema": "fano-six-bad-threecut-lock-v1",
        "claim_scope": (
            "auxiliary fixed-flow clean-projection composition route; "
            "not FiveCDC"
        ),
        "graph6": GRAPH6,
        "flow_values": FLOW,
        "cyclic_three_cut_edge_ids": sorted(CUT_EDGES),
        "cyclic_three_cut_edges": [edges[edge] for edge in sorted(CUT_EDGES)],
        "shore_A": sorted(SHORE_A),
        "shore_B": sorted(SHORE_B),
        "shore_induced_edge_counts": [12, 12],
        "local_profile_histogram": {
            ",".join(map(str, profile)): count
            for profile, count in sorted(histogram.items())
        },
        "local_profiles_by_deleted_edge": {
            str(edge): profiles[edge] for edge in range(len(edges))
        },
        "locked_cyclic_shore_by_obstructive_deleted_edge": locked_shores,
        "sat_witnesses_hex": witnesses,
        "binary_cycle_count_per_pole": 1024,
        "solver_independent": True,
    }
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
