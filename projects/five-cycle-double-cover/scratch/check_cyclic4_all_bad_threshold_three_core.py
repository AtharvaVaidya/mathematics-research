#!/usr/bin/env python3
"""Check a cyclic-four factor-critical five-pole with five truly bad terminals.

The source is the 70-vertex cyclic-connectivity-four construction described
by Lukot'ka, Máčajová, Mazák and Škoviera in "Small snarks with large
oddness", Electron. J. Combin. 22 (2015), P1.51, arXiv:1212.3641.
It is a cyclic junction of two copies of their 26-vertex 4-pole N2 and one
copy of their 18-vertex 4-pole N1.  The code constructs P4v and P4e directly
from the Petersen graph, constructs N1/N2, and performs the cyclic junction.

Deleting the induced path 4-0-5 leaves a 67-vertex factor-critical five-pole.
All five boundary terminals q have the property that every perfect matching
of Q-q leaves at least four odd internal circuit components.  In particular,
all five violate the local sufficient threshold "at most two".

The script is standard-library only and exhaustively checks all relevant
matchings and all cyclic cuts of size at most three.  This refutes a proposed
local five-pole lemma, not the Five-Cycle Double Cover Conjecture.  It does
not prove that this five-pole can occur with the special outside shore in the
one-boundary-five Gallai--Edmonds branch.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations
import json


DELETED_PATH = (4, 0, 5)
EXPECTED_BOUNDARY_OLD = (3, 7, 8, 9, 12)
EXPECTED_SOURCE_DISTRIBUTION = {6: 20_855, 8: 88}
EXPECTED_CORE_DISTRIBUTIONS = {
    3: {4: 3_592, 5: 196, 6: 56, 7: 4},
    7: {4: 3_592, 5: 196, 6: 56, 7: 4},
    8: {4: 2_772, 5: 196, 6: 56, 7: 4},
    9: {4: 3_592, 5: 196, 6: 56, 7: 4},
    12: {4: 5_347, 5: 392, 6: 112, 7: 8},
}


def petersen_edges() -> tuple[tuple[int, int], ...]:
    outer = [(index, (index + 1) % 5) for index in range(5)]
    spokes = [(index, index + 5) for index in range(5)]
    inner = [
        (5 + index, 5 + ((index + 2) % 5))
        for index in range(5)
    ]
    return tuple(sorted(tuple(sorted(edge)) for edge in outer + spokes + inner))


def p4v() -> tuple[
    int, list[tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]
]:
    """Petersen minus adjacent vertices 0,1, with their two connector pairs."""
    retained = [vertex for vertex in range(10) if vertex not in (0, 1)]
    new_index = {vertex: index for index, vertex in enumerate(retained)}
    edges = [
        (new_index[left], new_index[right])
        for left, right in petersen_edges()
        if left in new_index and right in new_index
    ]
    pairs = (
        (new_index[4], new_index[5]),
        (new_index[2], new_index[6]),
    )
    return len(retained), edges, pairs


def p4e() -> tuple[
    int, list[tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]
]:
    """Petersen with the distance-one edges 01 and 23 split off."""
    removed = {(0, 1), (2, 3)}
    edges = [edge for edge in petersen_edges() if edge not in removed]
    return 10, edges, ((0, 1), (2, 3))


def block(kind: str) -> tuple[
    int, list[tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]
]:
    """Build N1 or N2 with the two surviving connector pairs."""
    order, edges, p4e_pairs = p4e()
    free_pairs: list[tuple[int, int]] = []
    copies = 1 if kind == "N1" else 2
    if kind not in ("N1", "N2"):
        raise ValueError("unknown block")
    for copy in range(copies):
        piece_order, piece_edges, piece_pairs = p4v()
        offset = order
        order += piece_order
        edges.extend((left + offset, right + offset)
                     for left, right in piece_edges)
        edges.extend(
            (left, right + offset)
            for left, right in zip(p4e_pairs[copy], piece_pairs[0])
        )
        free_pairs.append(tuple(vertex + offset for vertex in piece_pairs[1]))
    if kind == "N1":
        free_pairs.append(p4e_pairs[1])
    return order, edges, (free_pairs[0], free_pairs[1])


def build_source() -> tuple[int, tuple[tuple[int, int], ...]]:
    pieces = (block("N2"), block("N2"), block("N1"))
    order = 0
    edges: list[tuple[int, int]] = []
    connectors = []
    for piece_order, piece_edges, piece_connectors in pieces:
        edges.extend(
            (left + order, right + order)
            for left, right in piece_edges
        )
        connectors.append(tuple(
            tuple(vertex + order for vertex in pair)
            for pair in piece_connectors
        ))
        order += piece_order
    for index in range(3):
        edges.extend(
            (left, right)
            for left, right in zip(
                connectors[index][1],
                connectors[(index + 1) % 3][0],
            )
        )
    normalized = tuple(sorted(tuple(sorted(edge)) for edge in edges))
    return order, normalized


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
        if degree_sum // 2 == vertices and vertices % 2:
            result += 1
    return result


def matching_distribution(rows: list[int], exposed: int | None) -> Counter[int]:
    allowed = (1 << len(rows)) - 1
    if exposed is not None:
        allowed ^= 1 << exposed
    result: Counter[int] = Counter()

    def search(vertices: int, chosen: list[tuple[int, int]]) -> None:
        if not vertices:
            result[complement_odd_circuits(rows, tuple(chosen))] += 1
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
    return result


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


def factor_critical(rows: list[int]) -> bool:
    full = (1 << len(rows)) - 1

    @lru_cache(maxsize=None)
    def matchable(vertices: int) -> bool:
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
            if matchable(vertices ^ first_bit ^ second_bit):
                return True
        return False

    return all(matchable(full ^ (1 << vertex))
               for vertex in range(len(rows)))


def locally_cyclic_four(rows: list[int], terminals: tuple[int, ...]) -> bool:
    """Directly search all proper/semiedge cuts of size at most three."""
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
                core_part = part & ((1 << order) - 1)
                if component_has_circuit(rows, core_part):
                    return False
    return True


def main() -> int:
    source_order, source_edges = build_source()
    if source_order != 70 or len(source_edges) != 105:
        raise AssertionError("source construction has the wrong size")
    source = adjacency(source_order, source_edges)
    if any(row.bit_count() != 3 for row in source):
        raise AssertionError("source is not cubic")
    if len(components(source, (1 << source_order) - 1)) != 1:
        raise AssertionError("source is disconnected")
    if not cyclically_four(source, source_edges):
        raise AssertionError("source has a cyclic cut of size at most three")
    source_distribution = matching_distribution(source, None)
    if dict(source_distribution) != EXPECTED_SOURCE_DISTRIBUTION:
        raise AssertionError("source oddness profile changed")

    left, middle, right = DELETED_PATH
    if not (
        source[left] >> middle & 1
        and source[middle] >> right & 1
        and not (source[left] >> right & 1)
    ):
        raise AssertionError("declared deletion is not an induced path")
    core, retained, new_index = delete_source_vertices(source, DELETED_PATH)
    boundary_new = tuple(
        vertex for vertex, row in enumerate(core) if row.bit_count() == 2
    )
    boundary_old = tuple(retained[vertex] for vertex in boundary_new)
    if boundary_old != EXPECTED_BOUNDARY_OLD:
        raise AssertionError("unexpected core boundary")
    if any(row.bit_count() not in (2, 3) for row in core):
        raise AssertionError("core has the wrong degree profile")
    if not factor_critical(core):
        raise AssertionError("core is not factor-critical")
    if not locally_cyclic_four(core, boundary_new):
        raise AssertionError("core violates the local cyclic-four condition")

    profiles = {}
    for old_terminal in EXPECTED_BOUNDARY_OLD:
        distribution = matching_distribution(core, new_index[old_terminal])
        if dict(distribution) != EXPECTED_CORE_DISTRIBUTIONS[old_terminal]:
            raise AssertionError(f"terminal {old_terminal} profile changed")
        profiles[str(old_terminal)] = {
            "near_perfect_matchings": sum(distribution.values()),
            "odd_internal_circuit_distribution": dict(sorted(distribution.items())),
            "minimum_odd_internal_circuits": min(distribution),
        }

    report = {
        "schema": "cyclic4-all-bad-threshold-three-core-v1",
        "classification": "EXACT EXPLICIT COUNTEREXAMPLE CHECK",
        "source": {
            "construction": "cyclic junction N2-N2-N1 from arXiv:1212.3641",
            "order": source_order,
            "edges": len(source_edges),
            "cyclically_four_edge_connected": True,
            "perfect_matchings": sum(source_distribution.values()),
            "complementary_odd_circuit_distribution": dict(
                sorted(source_distribution.items())
            ),
            "oddness": min(source_distribution),
        },
        "deleted_induced_path": list(DELETED_PATH),
        "core": {
            "order": len(core),
            "factor_critical": True,
            "locally_cyclic_four": True,
            "boundary_vertices_in_source_numbering": list(boundary_old),
            "bad_threshold": "minimum odd internal circuits >= 3",
            "bad_boundary_vertices": list(boundary_old),
            "profiles": profiles,
        },
        "logical_scope": (
            "Refutes the purely local cyclic-four at-most-one-bad-terminal "
            "lemma. Does not refute Five-CDC and does not establish GE "
            "outside-shore realizability."
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
