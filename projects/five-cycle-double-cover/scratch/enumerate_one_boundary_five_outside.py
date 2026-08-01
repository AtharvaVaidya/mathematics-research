#!/usr/bin/env python3
"""Enumerate small outside incidence patterns in the one-boundary-five branch.

The outside has W=A union U, |A|=s and |U|=4, singleton D-vertices
Z of size s+1, two fixed root edges 01 and 23 inside W, and all remaining
proper edges between Z and W.  Each z has degree three.  The unused degree
at W is the multiplicity b(w) of five boundary edges to the factor-critical
core Q.

Z vertices are quotiented by representing their three-neighbour sets as a
sorted multiset.  U and A remain labelled.  The program checks:

* the strict Hall condition on A versus the D-components Z plus Q;
* the local bridgelessness conditions forced by gluing to connected Q;
* the local cyclic-four condition: every cyclic connected X in the outside
  has at least four incident proper-or-boundary edges; and
* exact attainability of a boundary incidence with either prescribed root.

This is a finite structural census, not a Five-CDC solver.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, combinations_with_replacement
import json


def connected(adjacency: list[int], vertices: int) -> bool:
    if not vertices:
        return True
    start = vertices & -vertices
    reached = start
    frontier = start
    while frontier:
        bit = frontier & -frontier
        frontier ^= bit
        vertex = bit.bit_length() - 1
        fresh = adjacency[vertex] & vertices & ~reached
        reached |= fresh
        frontier |= fresh
    return reached == vertices


def graph_data(
    s: int, rows: tuple[tuple[int, int, int], ...]
) -> tuple[list[int], tuple[int, ...]]:
    w_count = s + 4
    z_count = s + 1
    order = w_count + z_count
    adjacency = [0] * order

    def add(left: int, right: int) -> None:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left

    add(0, 1)
    add(2, 3)
    for z, neighbours in enumerate(rows):
        vertex = w_count + z
        for w in neighbours:
            add(vertex, w)
    capacities = (2, 2, 2, 2, *(3 for _ in range(s)))
    boundary = tuple(
        capacities[w] - sum(w in neighbours for neighbours in rows)
        for w in range(w_count)
    )
    return adjacency, boundary


def strict_hall(s: int, rows: tuple[tuple[int, int, int], ...],
                boundary: tuple[int, ...]) -> bool:
    """Check |N(X)| >= |X|+1 for every nonempty X subset A."""
    for subset in range(1, 1 << s):
        components = set()
        for a_local in range(s):
            if not (subset >> a_local & 1):
                continue
            a = 4 + a_local
            for z, neighbours in enumerate(rows):
                if a in neighbours:
                    components.add(z)
            if boundary[a]:
                components.add(s + 1)  # the nontrivial component Q
        if len(components) < subset.bit_count() + 1:
            return False
    return True


def component_boundary_condition(
    adjacency: list[int], boundary: tuple[int, ...]
) -> bool:
    """Every outside component has >=2 Q incidences; both bridge sides have one."""
    order = len(adjacency)
    full = (1 << order) - 1
    seen = 0
    for start in range(order):
        if seen >> start & 1:
            continue
        reached = 1 << start
        frontier = reached
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            vertex = bit.bit_length() - 1
            fresh = adjacency[vertex] & ~reached
            reached |= fresh
            frontier |= fresh
        seen |= reached
        if sum(boundary[w] for w in range(len(boundary))
               if reached >> w & 1) < 2:
            return False

    edges = [
        (left, right)
        for left, row in enumerate(adjacency)
        for right in range(left + 1, order)
        if row >> right & 1
    ]
    for left, right in edges:
        modified = adjacency[:]
        modified[left] &= ~(1 << right)
        modified[right] &= ~(1 << left)
        reached = 1 << left
        frontier = reached
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            vertex = bit.bit_length() - 1
            fresh = modified[vertex] & ~reached
            reached |= fresh
            frontier |= fresh
        if reached >> right & 1:
            continue
        other = full ^ reached
        for side in (reached, other):
            if not any(side >> w & 1 and boundary[w]
                       for w in range(len(boundary))):
                return False
    return True


def locally_cyclic_four(adjacency: list[int], boundary: tuple[int, ...]) -> bool:
    """Every connected cyclic outside shore has full boundary at least four."""
    order = len(adjacency)
    full = (1 << order) - 1
    for vertices in range(1, full + 1):
        if not connected(adjacency, vertices):
            continue
        vertex_count = vertices.bit_count()
        degree_sum = sum(
            (adjacency[vertex] & vertices).bit_count()
            for vertex in range(order)
            if vertices >> vertex & 1
        )
        internal_edges = degree_sum // 2
        if internal_edges < vertex_count:
            continue
        proper_cut = sum(
            (adjacency[vertex] & ~vertices).bit_count()
            for vertex in range(order)
            if vertices >> vertex & 1
        )
        q_cut = sum(
            boundary[w]
            for w in range(len(boundary))
            if vertices >> w & 1
        )
        if proper_cut + q_cut <= 3:
            return False
    return True


def bipartite_perfect(
    rows: tuple[tuple[int, int, int], ...], allowed_w: set[int]
) -> bool:
    """Does Z have a matching onto the equally sized set allowed_w?"""
    if len(rows) != len(allowed_w):
        return False
    ordered = sorted(
        (set(neighbours) & allowed_w for neighbours in rows),
        key=len,
    )

    def search(index: int, used: set[int]) -> bool:
        if index == len(ordered):
            return True
        for w in ordered[index] - used:
            used.add(w)
            if search(index + 1, used):
                return True
            used.remove(w)
        return False

    return search(0, set())


def attainable_profile(
    s: int, rows: tuple[tuple[int, int, int], ...],
    boundary: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    w_set = set(range(s + 4))
    roots = ((0, 1), (2, 3))
    attainable_by_root = []
    for root in roots:
        attainable = []
        for w, multiplicity in enumerate(boundary):
            if not multiplicity or w in root:
                continue
            allowed = w_set - set(root) - {w}
            if bipartite_perfect(rows, allowed):
                attainable.extend([w] * multiplicity)
        attainable_by_root.append(tuple(attainable))
    union = tuple(
        w
        for w, multiplicity in enumerate(boundary)
        if multiplicity
        and any(w in attainable for attainable in attainable_by_root)
        for _ in range(multiplicity)
    )
    return union, tuple(attainable_by_root)


def enumerate_order(s: int) -> dict[str, object]:
    w_count = s + 4
    z_count = s + 1
    neighbourhoods = tuple(combinations(range(w_count), 3))
    counts: Counter[str] = Counter()
    attainable_histogram: Counter[int] = Counter()
    minimum = None
    examples = []
    for rows in combinations_with_replacement(neighbourhoods, z_count):
        counts["raw"] += 1
        adjacency, boundary = graph_data(s, rows)
        if any(value < 0 for value in boundary):
            continue
        counts["capacity"] += 1
        if not strict_hall(s, rows, boundary):
            continue
        counts["strict_hall"] += 1
        if not component_boundary_condition(adjacency, boundary):
            continue
        counts["locally_bridgeless"] += 1
        if not locally_cyclic_four(adjacency, boundary):
            continue
        counts["locally_cyclic_four"] += 1
        union, by_root = attainable_profile(s, rows, boundary)
        if any(not values for values in by_root):
            counts["root_unattainable"] += 1
            continue
        counts["both_roots_attainable"] += 1
        attainable_histogram[len(union)] += 1
        if minimum is None or len(union) < minimum:
            minimum = len(union)
            examples = []
        if len(union) == minimum and len(examples) < 10:
            examples.append({
                "z_neighbourhoods": [list(row) for row in rows],
                "boundary_multiplicities": list(boundary),
                "attainable_boundary_endpoints_by_root": [
                    list(values) for values in by_root
                ],
                "distinct_attainable_boundary_incidences": len(union),
            })
    return {
        "s": s,
        "W": w_count,
        "Z": z_count,
        "counts": dict(counts),
        "attainable_boundary_incidence_histogram": {
            str(key): value for key, value in sorted(attainable_histogram.items())
        },
        "minimum_attainable_boundary_incidences": minimum,
        "minimum_examples": examples,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-s", type=int, default=3)
    args = parser.parse_args()
    if not 0 <= args.max_s <= 3:
        parser.error("the exact subset census currently supports 0 <= s <= 3")
    report = {
        "schema": "one-boundary-five-outside-census-v1",
        "classification": "EXACT FINITE STRUCTURAL CENSUS",
        "orders": [enumerate_order(s) for s in range(args.max_s + 1)],
        "warning": "Finite incidence census only; not a Five-CDC resolution.",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
