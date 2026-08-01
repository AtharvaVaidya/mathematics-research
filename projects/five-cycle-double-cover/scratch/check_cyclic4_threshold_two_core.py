#!/usr/bin/env python3
"""Check sharpness of the two-odd-circuit threshold for a cyclic-four core.

The 44-vertex source graph is reconstructed from `sn44_2.fig` in the arXiv
source of Goedgebeur--Máčajová--Škoviera, "The smallest nontrivial snarks
of oddness 4", arXiv:1901.10911.  Vertex numbers are the order in which
the 44 vertex circles occur in that XFig file.  Two degree-two-looking
circles lie on diagonal edge segments; those two segments are split at
the circles, yielding the cubic edge table below.

Delete the induced path 10-11-43.  The checker proves by exhaustive,
standard-library calculations that:

* the source is simple cubic and cyclically four-edge-connected;
* it has 501 perfect matchings and every complementary 2-factor has four
  odd circuits;
* the remaining 41-vertex core is factor-critical and has exactly five
  degree-two terminals, 9,12,14,25,37 in the source numbering;
* it satisfies the local cyclic-four five-pole cut condition; and
* every near-perfect matching exposing any terminal leaves at least two
  odd internal circuit components, while each terminal admits one leaving
  exactly two.

This shows that the sufficient local threshold ``at most two`` is sharp:
neither forestness nor ``at most one`` is universally available even under
the local cyclic-four condition.  It is not a counterexample to the
Five-Cycle Double Cover Conjecture; the source has oddness four and therefore
has a standard five-cycle double cover by known theorems.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations
import json


SOURCE_EDGES = (
    (0, 1), (0, 4), (0, 7), (1, 2), (1, 35), (2, 3), (2, 6),
    (3, 4), (3, 9), (4, 5), (5, 6), (5, 41), (6, 7), (7, 42),
    (8, 9), (8, 12), (8, 15), (9, 10), (10, 11), (10, 14),
    (11, 12), (11, 43), (12, 13), (13, 14), (13, 42), (14, 15),
    (15, 29), (16, 17), (16, 23), (16, 32), (17, 18), (17, 21),
    (18, 19), (18, 42), (19, 20), (19, 23), (20, 21), (20, 31),
    (21, 22), (22, 23), (22, 41), (24, 25), (24, 28), (24, 31),
    (25, 26), (25, 43), (26, 27), (26, 30), (27, 28), (27, 32),
    (28, 29), (29, 30), (30, 31), (32, 33), (33, 34), (33, 40),
    (34, 35), (34, 38), (35, 36), (36, 37), (36, 40), (37, 38),
    (37, 43), (38, 39), (39, 40), (39, 41),
)
SOURCE_ORDER = 44
DELETED_PATH = (10, 11, 43)
EXPECTED_BOUNDARY_OLD = (9, 12, 14, 25, 37)
EXPECTED_PROFILES = {
    9: {2: 60, 3: 4, 4: 1},
    12: {2: 104, 3: 8, 4: 1},
    14: {2: 72, 3: 24, 4: 2},
    25: {2: 64, 3: 24, 4: 2},
    37: {2: 56, 3: 30},
}


def adjacency(order: int, edges: tuple[tuple[int, int], ...]) -> list[int]:
    rows = [0] * order
    seen = set()
    for left, right in edges:
        if not (0 <= left < right < order) or (left, right) in seen:
            raise AssertionError("edge table is not simple and normalized")
        seen.add((left, right))
        rows[left] |= 1 << right
        rows[right] |= 1 << left
    return rows


def components(rows: list[int], allowed: int) -> list[int]:
    result = []
    while allowed:
        reached = allowed & -allowed
        frontier = reached
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            vertex = bit.bit_length() - 1
            fresh = rows[vertex] & allowed & ~reached
            reached |= fresh
            frontier |= fresh
        result.append(reached)
        allowed &= ~reached
    return result


def component_has_circuit(rows: list[int], vertices: int) -> bool:
    degree_sum = sum(
        (rows[vertex] & vertices).bit_count()
        for vertex in range(len(rows))
        if vertices >> vertex & 1
    )
    return degree_sum // 2 >= vertices.bit_count()


def cyclically_four(rows: list[int],
                    edges: tuple[tuple[int, int], ...]) -> bool:
    full = (1 << len(rows)) - 1
    for size in (1, 2, 3):
        for cut in combinations(edges, size):
            modified = rows[:]
            for left, right in cut:
                modified[left] &= ~(1 << right)
                modified[right] &= ~(1 << left)
            parts = components(modified, full)
            if len(parts) > 1 and sum(
                component_has_circuit(modified, part) for part in parts
            ) >= 2:
                return False
    return True


def complement_odd_circuits(
    rows: list[int], matching: tuple[tuple[int, int], ...]
) -> int:
    complement = rows[:]
    for left, right in matching:
        complement[left] &= ~(1 << right)
        complement[right] &= ~(1 << left)
    result = 0
    full = (1 << len(rows)) - 1
    for part in components(complement, full):
        vertices = part.bit_count()
        degree_sum = sum(
            (complement[vertex] & part).bit_count()
            for vertex in range(len(rows))
            if part >> vertex & 1
        )
        edges = degree_sum // 2
        if edges == vertices and vertices % 2:
            result += 1
    return result


def matching_distribution(rows: list[int], exposed: int | None) -> Counter[int]:
    allowed = (1 << len(rows)) - 1
    if exposed is not None:
        allowed ^= 1 << exposed
    distribution: Counter[int] = Counter()

    def search(vertices: int, chosen: list[tuple[int, int]]) -> None:
        if not vertices:
            distribution[complement_odd_circuits(rows, tuple(chosen))] += 1
            return
        first_bit = vertices & -vertices
        first = first_bit.bit_length() - 1
        candidates = rows[first] & vertices & ~first_bit
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            chosen.append((first, second))
            search(vertices ^ first_bit ^ second_bit, chosen)
            chosen.pop()

    search(allowed, [])
    return distribution


def has_perfect_matching(rows: list[int], allowed: int) -> bool:
    @lru_cache(maxsize=None)
    def solve(vertices: int) -> bool:
        if not vertices:
            return True
        if vertices.bit_count() % 2:
            return False
        first_bit = vertices & -vertices
        first = first_bit.bit_length() - 1
        candidates = rows[first] & vertices & ~first_bit
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            if solve(vertices ^ first_bit ^ second_bit):
                return True
        return False

    return solve(allowed)


def delete_source_vertices(
    source: list[int], deleted: tuple[int, ...]
) -> tuple[list[int], list[int], dict[int, int]]:
    retained = [vertex for vertex in range(len(source)) if vertex not in deleted]
    new_index = {vertex: index for index, vertex in enumerate(retained)}
    rows = []
    for vertex in retained:
        row = 0
        for other in retained:
            if source[vertex] >> other & 1:
                row |= 1 << new_index[other]
        rows.append(row)
    return rows, retained, new_index


def locally_cyclic_four(rows: list[int], terminals: tuple[int, ...]) -> bool:
    """Direct semiedge-cut check using a common outside marker.

    Add a marker adjacent to each terminal semiedge.  A cyclic pole shore
    with boundary at most three becomes a cyclic component not containing
    the marker after removal of those boundary edges.
    """
    order = len(rows)
    marker = order
    augmented = rows[:] + [0]
    proper_edges = [
        (left, right)
        for left, row in enumerate(rows)
        for right in range(left + 1, order)
        if row >> right & 1
    ]
    semiedges = []
    for terminal in terminals:
        augmented[terminal] |= 1 << marker
        augmented[marker] |= 1 << terminal
        semiedges.append((terminal, marker))
    all_edges = tuple(proper_edges + semiedges)
    full = (1 << (order + 1)) - 1
    for size in (1, 2, 3):
        for cut in combinations(all_edges, size):
            modified = augmented[:]
            for left, right in cut:
                modified[left] &= ~(1 << right)
                modified[right] &= ~(1 << left)
            for part in components(modified, full):
                if part >> marker & 1:
                    continue
                q_part = part & ((1 << order) - 1)
                if component_has_circuit(rows, q_part):
                    return False
    return True


def main() -> int:
    source = adjacency(SOURCE_ORDER, SOURCE_EDGES)
    if any(row.bit_count() != 3 for row in source):
        raise AssertionError("source is not cubic")
    if len(components(source, (1 << SOURCE_ORDER) - 1)) != 1:
        raise AssertionError("source is disconnected")
    if not cyclically_four(source, SOURCE_EDGES):
        raise AssertionError("source has a cyclic edge-cut of size at most three")
    source_distribution = matching_distribution(source, None)
    if source_distribution != Counter({4: 501}):
        raise AssertionError("source perfect-matching/oddness profile changed")

    if not (
        source[10] >> 11 & 1
        and source[11] >> 43 & 1
        and not (source[10] >> 43 & 1)
    ):
        raise AssertionError("declared deletion is not an induced path")
    core, retained, new_index = delete_source_vertices(source, DELETED_PATH)
    boundary_new = tuple(
        vertex for vertex, row in enumerate(core) if row.bit_count() == 2
    )
    boundary_old = tuple(retained[vertex] for vertex in boundary_new)
    if boundary_old != EXPECTED_BOUNDARY_OLD:
        raise AssertionError("unexpected five-pole boundary")
    if any(row.bit_count() not in (2, 3) for row in core):
        raise AssertionError("core has the wrong degree profile")
    full_core = (1 << len(core)) - 1
    if len(components(core, full_core)) != 1:
        raise AssertionError("core is disconnected")
    if not all(
        has_perfect_matching(core, full_core ^ (1 << vertex))
        for vertex in range(len(core))
    ):
        raise AssertionError("core is not factor-critical")
    if not locally_cyclic_four(core, boundary_new):
        raise AssertionError("core violates the local cyclic-four condition")

    profiles = {}
    for old_terminal in EXPECTED_BOUNDARY_OLD:
        distribution = matching_distribution(core, new_index[old_terminal])
        if dict(distribution) != EXPECTED_PROFILES[old_terminal]:
            raise AssertionError(f"terminal {old_terminal} profile changed")
        profiles[str(old_terminal)] = {
            "near_perfect_matchings": sum(distribution.values()),
            "odd_internal_circuit_distribution": dict(sorted(distribution.items())),
            "minimum_odd_internal_circuits": min(distribution),
        }

    report = {
        "schema": "cyclic4-threshold-two-factor-critical-core-v1",
        "classification": "EXACT EXPLICIT SHARPNESS CHECK",
        "source": {
            "order": SOURCE_ORDER,
            "edges": len(SOURCE_EDGES),
            "cyclically_four_edge_connected": True,
            "perfect_matchings": sum(source_distribution.values()),
            "complementary_odd_circuit_distribution": dict(source_distribution),
            "provenance": (
                "sn44_2.fig in arXiv:1901.10911 source; vertices are XFig "
                "circle order"
            ),
        },
        "deleted_induced_path": list(DELETED_PATH),
        "core": {
            "order": len(core),
            "factor_critical": True,
            "locally_cyclic_four": True,
            "boundary_vertices_in_source_numbering": list(boundary_old),
            "boundary_vertices_forcing_two_odd_circuits": list(boundary_old),
            "profiles": profiles,
        },
        "logical_scope": (
            "Shows sharpness of the sufficient at-most-two threshold; does "
            "not refute Five-CDC."
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
