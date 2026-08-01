#!/usr/bin/env python3
"""Audit the proposed forest-complement lemma for factor-critical five-poles.

Input is a stream of graph6 records.  Retain connected simple graphs with
exactly five degree-two vertices and all remaining vertices of degree three.
For each retained factor-critical graph Q and each degree-two vertex q, test
whether some perfect matching of Q-q has acyclic complement in Q.

The program deliberately uses only the Python standard library.  It prints
one JSON row per factor-critical graph for which at least one boundary
vertex q fails the forest-complement test.  A final summary is written to
stderr.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import json
from pathlib import Path
import sys


def decode_graph6(record: str) -> list[int]:
    """Return adjacency bit masks for a short graph6 record."""
    record = record.strip()
    if not record or record[0] == "~":
        raise ValueError("only nonempty short graph6 records are supported")
    n = ord(record[0]) - 63
    payload: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        payload.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [0] * n
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if payload[cursor]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1
    return adjacency


def connected(adjacency: list[int], allowed: int | None = None) -> bool:
    n = len(adjacency)
    if allowed is None:
        allowed = (1 << n) - 1
    if not allowed:
        return True
    start = allowed & -allowed
    reached = start
    frontier = start
    while frontier:
        bit = frontier & -frontier
        frontier ^= bit
        vertex = bit.bit_length() - 1
        fresh = adjacency[vertex] & allowed & ~reached
        reached |= fresh
        frontier |= fresh
    return reached == allowed


def has_bridge(adjacency: list[int]) -> bool:
    """Brute-force bridge test, adequate for the small exact census."""
    n = len(adjacency)
    for left in range(n):
        row = adjacency[left]
        while row:
            bit = row & -row
            row ^= bit
            right = bit.bit_length() - 1
            if left >= right:
                continue
            modified = adjacency[:]
            modified[left] &= ~(1 << right)
            modified[right] &= ~(1 << left)
            if not connected(modified):
                return True
    return False


def matching_witness(adjacency: list[int], allowed: int) -> tuple[int, ...] | None:
    """Find one perfect matching of the induced allowed set, if it exists."""

    @lru_cache(maxsize=None)
    def solve(mask: int) -> tuple[int, ...] | None:
        if not mask:
            return ()
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & mask & ~first_bit
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            tail = solve(mask ^ first_bit ^ second_bit)
            if tail is not None:
                return (first, second, *tail)
        return None

    return solve(allowed)


def factor_critical(adjacency: list[int]) -> bool:
    full = (1 << len(adjacency)) - 1
    return all(matching_witness(adjacency, full ^ (1 << vertex)) is not None
               for vertex in range(len(adjacency)))


def complement_components(
    adjacency: list[int], matching: tuple[int, ...]
) -> list[tuple[int, int, tuple[int, ...]]]:
    """Return (vertices, edges, vertex tuple) for complement components."""
    n = len(adjacency)
    matched_edges = {
        (min(matching[index], matching[index + 1]),
         max(matching[index], matching[index + 1]))
        for index in range(0, len(matching), 2)
    }
    complement = adjacency[:]
    for left, right in matched_edges:
        complement[left] &= ~(1 << right)
        complement[right] &= ~(1 << left)

    result: list[tuple[int, int, tuple[int, ...]]] = []
    seen = 0
    for start in range(n):
        if seen >> start & 1:
            continue
        reached = 1 << start
        frontier = reached
        degree_sum = 0
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            vertex = bit.bit_length() - 1
            degree_sum += complement[vertex].bit_count()
            fresh = complement[vertex] & ~reached
            reached |= fresh
            frontier |= fresh
        seen |= reached
        vertices = reached.bit_count()
        edges = degree_sum // 2
        result.append((
            vertices,
            edges,
            tuple(vertex for vertex in range(n) if reached >> vertex & 1),
        ))
    return result


def complement_is_forest(adjacency: list[int], matching: tuple[int, ...]) -> bool:
    return all(edges < vertices
               for vertices, edges, _ in complement_components(adjacency, matching))


def odd_circuit_count(adjacency: list[int], matching: tuple[int, ...]) -> int:
    """Count odd circuit components of the maximum-degree-two complement."""
    return sum(
        1
        for vertices, edges, _ in complement_components(adjacency, matching)
        if edges == vertices and vertices % 2 == 1
    )


def minimum_completed_cyclic_cut(
    adjacency: list[int],
) -> tuple[int | None, tuple[int, ...] | None]:
    """Minimize 3|X|-2|E(X)| over proper vertex sets containing a circuit.

    The expression is the cut size after one semiedge is attached at each
    degree-two terminal.  This is a deliberately direct subset audit for
    small explicit poles, independent of any low-cut routine.
    """
    order = len(adjacency)
    full = (1 << order) - 1
    best: int | None = None
    witness: tuple[int, ...] | None = None
    for allowed in range(1, full):
        internal_twice = sum(
            (adjacency[vertex] & allowed).bit_count()
            for vertex in range(order)
            if allowed >> vertex & 1
        )
        internal_edges = internal_twice // 2
        completed_cut = 3 * allowed.bit_count() - 2 * internal_edges
        if best is not None and completed_cut >= best:
            continue
        components = 0
        unseen = allowed
        while unseen:
            components += 1
            start = unseen & -unseen
            reached = start
            frontier = start
            while frontier:
                bit = frontier & -frontier
                frontier ^= bit
                vertex = bit.bit_length() - 1
                fresh = adjacency[vertex] & allowed & ~reached
                reached |= fresh
                frontier |= fresh
            unseen &= ~reached
        if internal_edges >= allowed.bit_count() - components + 1:
            best = completed_cut
            witness = tuple(
                vertex for vertex in range(order) if allowed >> vertex & 1
            )
    return best, witness


def forest_matching_witness(
    adjacency: list[int], exposed: int
) -> tuple[int, ...] | None:
    """Enumerate perfect matchings of Q-exposed until a forest complement appears."""
    allowed = ((1 << len(adjacency)) - 1) ^ (1 << exposed)

    def search(mask: int, pairs: list[int]) -> tuple[int, ...] | None:
        if not mask:
            matching = tuple(pairs)
            return matching if complement_is_forest(adjacency, matching) else None
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & mask & ~first_bit
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            pairs.extend((first, second))
            witness = search(mask ^ first_bit ^ second_bit, pairs)
            del pairs[-2:]
            if witness is not None:
                return witness
        return None

    return search(allowed, [])


def best_odd_circuit_matching(
    adjacency: list[int], exposed: int
) -> tuple[int, tuple[int, ...]]:
    """Return the minimum odd internal-circuit count and a witness matching."""
    allowed = ((1 << len(adjacency)) - 1) ^ (1 << exposed)
    best: tuple[int, tuple[int, ...]] | None = None

    def search(mask: int, pairs: list[int]) -> None:
        nonlocal best
        if not mask:
            matching = tuple(pairs)
            value = odd_circuit_count(adjacency, matching)
            if best is None or value < best[0]:
                best = (value, matching)
            return
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & mask & ~first_bit
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            pairs.extend((first, second))
            search(mask ^ first_bit ^ second_bit, pairs)
            del pairs[-2:]

    search(allowed, [])
    if best is None:
        raise AssertionError("factor-critical graph has no near-perfect matching")
    return best


def all_near_perfect_statistics(
    adjacency: list[int], exposed: int
) -> tuple[int, Counter[int]]:
    """Count all near-perfect matchings by odd complement-circuit count."""
    allowed = ((1 << len(adjacency)) - 1) ^ (1 << exposed)
    distribution: Counter[int] = Counter()

    def search(mask: int, pairs: list[int]) -> None:
        if not mask:
            distribution[odd_circuit_count(adjacency, tuple(pairs))] += 1
            return
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & mask & ~first_bit
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            pairs.extend((first, second))
            search(mask ^ first_bit ^ second_bit, pairs)
            del pairs[-2:]

    search(allowed, [])
    return sum(distribution.values()), distribution


def all_perfect_statistics(adjacency: list[int]) -> tuple[int, Counter[int]]:
    """Count all perfect matchings by odd complementary-circuit count."""
    distribution: Counter[int] = Counter()

    def search(mask: int, pairs: list[int]) -> None:
        if not mask:
            distribution[odd_circuit_count(adjacency, tuple(pairs))] += 1
            return
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & mask & ~first_bit
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            pairs.extend((first, second))
            search(mask ^ first_bit ^ second_bit, pairs)
            del pairs[-2:]

    search((1 << len(adjacency)) - 1, [])
    return sum(distribution.values()), distribution


def edge_list(adjacency: list[int]) -> list[list[int]]:
    return [
        [left, right]
        for left, row in enumerate(adjacency)
        for right in range(left + 1, len(adjacency))
        if row >> right & 1
    ]


def embedded_counterexample_report() -> dict[str, object]:
    cases = (
        ("forest", "H?b@bQS", 6, {1: 1}),
        ("one_odd_circuit", "N??CA?oI?gX?AoP_Og?", 2, {2: 2}),
    )
    reports = []
    for name, record, exposed, expected in cases:
        adjacency = decode_graph6(record)
        degrees = [row.bit_count() for row in adjacency]
        total, distribution = all_near_perfect_statistics(adjacency, exposed)
        minimum_cyclic_cut, cyclic_cut_witness = (
            minimum_completed_cyclic_cut(adjacency)
        )
        report = {
            "name": name,
            "graph6": record,
            "order": len(adjacency),
            "edges": edge_list(adjacency),
            "boundary_vertices": [
                vertex for vertex, degree in enumerate(degrees) if degree == 2
            ],
            "connected": connected(adjacency),
            "internally_bridgeless": not has_bridge(adjacency),
            "factor_critical": factor_critical(adjacency),
            "exposed_boundary_vertex": exposed,
            "near_perfect_matchings": total,
            "odd_internal_circuit_distribution": dict(sorted(distribution.items())),
            "minimum_completed_cut_of_cyclic_subset": minimum_cyclic_cut,
            "minimum_completed_cyclic_cut_witness": cyclic_cut_witness,
        }
        if (
            report["boundary_vertices"].__len__() != 5
            or any(degree not in (2, 3) for degree in degrees)
            or not report["connected"]
            or not report["internally_bridgeless"]
            or not report["factor_critical"]
            or dict(distribution) != expected
        ):
            raise AssertionError(f"embedded {name} counterexample audit failed")
        reports.append(report)
    return {
        "schema": "factor-critical-five-pole-counterexamples-v1",
        "classification": "EXACT EXPLICIT COUNTEREXAMPLE CHECK",
        "cases": reports,
    }


def r2_path_counterexample_report(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text())
    order = data["vertices"]
    base = [0] * order
    for edge in data["edges"]:
        left, right = edge["u"], edge["v"]
        base[left] |= 1 << right
        base[right] |= 1 << left
    if any(row.bit_count() != 3 for row in base):
        raise AssertionError("R2 source is not cubic")
    base_total, base_distribution = all_perfect_statistics(base)
    if base_total != 192 or dict(base_distribution) != {6: 192}:
        raise AssertionError("R2 exact oddness-six replay failed")

    deleted_path = (8, 6, 9)
    if not (base[8] >> 6 & 1 and base[6] >> 9 & 1):
        raise AssertionError("declared vertices do not form a path")
    if base[8] >> 9 & 1:
        raise AssertionError("declared path is not induced")
    retained = [vertex for vertex in range(order) if vertex not in deleted_path]
    new_index = {vertex: index for index, vertex in enumerate(retained)}
    core = []
    for vertex in retained:
        row = 0
        for other in retained:
            if base[vertex] >> other & 1:
                row |= 1 << new_index[other]
        core.append(row)
    boundary_old = [1, 3, 4, 5, 7]
    boundary_new = [new_index[vertex] for vertex in boundary_old]
    if [retained[index] for index, row in enumerate(core) if row.bit_count() == 2] != boundary_old:
        raise AssertionError("unexpected boundary after path deletion")
    if not connected(core) or has_bridge(core) or not factor_critical(core):
        raise AssertionError("path-deletion core failed structural audit")
    profiles = {}
    for old_vertex, new_vertex in zip(boundary_old, boundary_new):
        total, distribution = all_near_perfect_statistics(core, new_vertex)
        if dict(distribution) != {4: total}:
            raise AssertionError("R2 core did not force four odd internal circuits")
        profiles[str(old_vertex)] = {
            "near_perfect_matchings": total,
            "odd_internal_circuit_distribution": dict(sorted(distribution.items())),
        }
    return {
        "schema": "factor-critical-r2-path-counterexample-v1",
        "classification": "EXACT EXPLICIT COUNTEREXAMPLE CHECK",
        "source": str(path),
        "source_order": order,
        "source_perfect_matchings": base_total,
        "source_odd_cycle_distribution": dict(sorted(base_distribution.items())),
        "deleted_induced_path": list(deleted_path),
        "core_order": len(core),
        "core_boundary_vertices_in_source_numbering": boundary_old,
        "core_connected": connected(core),
        "core_internally_bridgeless": not has_bridge(core),
        "core_factor_critical": factor_critical(core),
        "boundary_profiles": profiles,
    }


def census() -> int:
    input_graphs = 0
    degree_profile = 0
    bridgeless_profile = 0
    factor_critical_graphs = 0
    forest_failures = 0
    odd_bound_failures = 0
    locally_cyclic_four_bad_graphs = 0
    corrected_bad_graphs = 0
    locally_cyclic_four_corrected_bad_graphs = 0
    for raw in sys.stdin:
        record = raw.strip()
        if not record or record.startswith(">"):
            continue
        input_graphs += 1
        adjacency = decode_graph6(record)
        degrees = [row.bit_count() for row in adjacency]
        boundary = [vertex for vertex, degree in enumerate(degrees) if degree == 2]
        if len(boundary) != 5 or any(degree not in (2, 3) for degree in degrees):
            continue
        degree_profile += 1
        if not connected(adjacency) or has_bridge(adjacency):
            continue
        bridgeless_profile += 1
        if not factor_critical(adjacency):
            continue
        factor_critical_graphs += 1
        bad_forest_roots = [
            vertex
            for vertex in boundary
            if forest_matching_witness(adjacency, vertex) is None
        ]
        bad_odd_roots = []
        corrected_bad_roots = []
        odd_profile = {}
        for vertex in boundary:
            best_odd, witness = best_odd_circuit_matching(adjacency, vertex)
            odd_profile[str(vertex)] = {
                "minimum_odd_internal_circuits": best_odd,
                "witness_matching": list(witness),
            }
            if best_odd > 1:
                bad_odd_roots.append(vertex)
            if best_odd > 2:
                corrected_bad_roots.append(vertex)
        if bad_forest_roots:
            forest_failures += 1
        if bad_odd_roots:
            odd_bound_failures += 1
        if corrected_bad_roots:
            corrected_bad_graphs += 1
        minimum_cyclic_cut = None
        cyclic_cut_witness = None
        if bad_forest_roots or bad_odd_roots:
            minimum_cyclic_cut, cyclic_cut_witness = (
                minimum_completed_cyclic_cut(adjacency)
            )
        if bad_odd_roots and (
            minimum_cyclic_cut is None or minimum_cyclic_cut >= 4
        ):
            locally_cyclic_four_bad_graphs += 1
        if corrected_bad_roots and (
            minimum_cyclic_cut is None or minimum_cyclic_cut >= 4
        ):
            locally_cyclic_four_corrected_bad_graphs += 1
        if bad_forest_roots or bad_odd_roots:
            print(json.dumps({
                "graph6": record,
                "order": len(adjacency),
                "edges": edge_list(adjacency),
                "boundary_vertices": boundary,
                "bad_forest_exposed_boundary_vertices": bad_forest_roots,
                "bad_odd_bound_exposed_boundary_vertices": bad_odd_roots,
                "corrected_bad_exposed_boundary_vertices": corrected_bad_roots,
                "minimum_completed_cut_of_cyclic_subset": minimum_cyclic_cut,
                "minimum_completed_cyclic_cut_witness": cyclic_cut_witness,
                "odd_profile": odd_profile,
            }, sort_keys=True))
    print(json.dumps({
        "input_graphs": input_graphs,
        "degree_profile": degree_profile,
        "internally_bridgeless": bridgeless_profile,
        "factor_critical": factor_critical_graphs,
        "forest_counterexamples": forest_failures,
        "odd_bound_counterexamples": odd_bound_failures,
        "corrected_bad_counterexamples": corrected_bad_graphs,
        "locally_cyclic_four_odd_bound_counterexamples": (
            locally_cyclic_four_bad_graphs
        ),
        "locally_cyclic_four_corrected_bad_counterexamples": (
            locally_cyclic_four_corrected_bad_graphs
        ),
    }, sort_keys=True), file=sys.stderr)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="audit the embedded order-9 and order-15 counterexamples",
    )
    parser.add_argument(
        "--r2-json",
        type=Path,
        help="audit the all-terminal path-deletion counterexample in R2",
    )
    args = parser.parse_args()
    if args.self_check:
        print(json.dumps(embedded_counterexample_report(), indent=2, sort_keys=True))
        return 0
    if args.r2_json is not None:
        print(json.dumps(r2_path_counterexample_report(args.r2_json),
                         indent=2, sort_keys=True))
        return 0
    return census()


if __name__ == "__main__":
    raise SystemExit(main())
