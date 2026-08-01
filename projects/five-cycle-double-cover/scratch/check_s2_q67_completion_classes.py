#!/usr/bin/env python3
"""Canonical census of the s=2 outside completions of the Q67 five-pole.

The outside convention is the one used in
``enumerate_one_boundary_five_outside.py``:

* W has six labelled vertices, with roots w0w1 and w2w3;
* Z has three independent degree-three vertices;
* the first four W vertices have residual capacity two and the two
  A-vertices w4,w5 have residual capacity three;
* the five unused W incidences are joined bijectively to the five terminals
  of the factor-critical Q67 five-pole.

The script regenerates all 128 sorted-Z incidence patterns satisfying strict
Hall, the outside bridgelessness condition, and local cyclic four-connectivity.
It then removes duplicate assignments caused by repeated boundary vertices,
constructs every resulting labelled full graph, and canonically quotients
them using nauty ``labelg``.  Full cyclic four-connectivity is checked once
per exact isomorphism class and weighted back to all labelled constructions.

Only one advertised completion is subjected to a full perfect-matching
census.  Exhaustively enumerating perfect matchings in every isomorphism
class would be unnecessary for the requested structural quotient.

This is an exact finite structural/oddness experiment, not a Five-CDC
counterexample search.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations
import json
from pathlib import Path
import subprocess

from check_s1_theta_q67_completions import (
    components,
    graph6,
    q67,
    rows_from_edges,
)
from enumerate_one_boundary_five_outside import (
    component_boundary_condition,
    graph_data,
    locally_cyclic_four,
    strict_hall,
)


Q_ORDER = 67
S = 2
W_COUNT = 6
Z_COUNT = 3
ORDER = Q_ORDER + W_COUNT + Z_COUNT
W = tuple(range(Q_ORDER, Q_ORDER + W_COUNT))
Z = tuple(range(Q_ORDER + W_COUNT, ORDER))
ROOTS = ((W[0], W[1]), (W[2], W[3]))

LEX_ROWS = ((0, 2, 4), (0, 2, 5), (1, 3, 4))
LEX_BOUNDARY_ASSIGNMENT = (1, 3, 4, 5, 5)
EXPECTED_LEX_DISTRIBUTION = {4: 40_562, 6: 24_346, 8: 400}


def outside_patterns() -> list[
    tuple[tuple[tuple[int, int, int], ...], tuple[int, ...]]
]:
    patterns = []
    neighbourhoods = tuple(combinations(range(W_COUNT), 3))
    for rows in combinations_with_replacement(neighbourhoods, Z_COUNT):
        outside_rows, boundary = graph_data(S, rows)
        if any(value < 0 for value in boundary):
            continue
        if not strict_hall(S, rows, boundary):
            continue
        if not component_boundary_condition(outside_rows, boundary):
            continue
        if not locally_cyclic_four(outside_rows, boundary):
            continue
        patterns.append((rows, boundary))
    return patterns


def outside_edges(
    z_neighbourhoods: tuple[tuple[int, int, int], ...],
) -> tuple[tuple[int, int], ...]:
    answer = list(ROOTS)
    for z_index, neighbours in enumerate(z_neighbourhoods):
        answer.extend((Z[z_index], W[w_index]) for w_index in neighbours)
    return tuple(answer)


def boundary_assignments(boundary: tuple[int, ...]) -> list[tuple[int, ...]]:
    """Maps the five fixed Q terminals, in source order, to W indices."""
    slots = tuple(
        w_index
        for w_index, multiplicity in enumerate(boundary)
        for _ in range(multiplicity)
    )
    if len(slots) != 5:
        raise AssertionError("outside does not have five boundary stubs")
    return sorted(set(permutations(slots)))


def completion_edges(
    q_edges: tuple[tuple[int, int], ...],
    terminals: tuple[int, ...],
    z_neighbourhoods: tuple[tuple[int, int, int], ...],
    assignment: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    boundary_edges = tuple(
        (terminals[index], W[assignment[index]]) for index in range(5)
    )
    return tuple(sorted(
        q_edges + outside_edges(z_neighbourhoods) + boundary_edges
    ))


def canonicalize_all(labelled_graph6: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["labelg", "-q"],
            input=("\n".join(labelled_graph6) + "\n").encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError("nauty labelg is required for the quotient") from error
    canonical = result.stdout.decode().splitlines()
    if len(canonical) != len(labelled_graph6):
        raise AssertionError("labelg changed the number of graphs")
    return canonical


def bridge_indices(
    incidence: list[list[tuple[int, int]]], banned: frozenset[int]
) -> list[int]:
    discovery = [-1] * len(incidence)
    low = [0] * len(incidence)
    clock = 0
    answer: list[int] = []

    def dfs(vertex: int, parent_edge: int) -> None:
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        for other, edge_index in incidence[vertex]:
            if edge_index in banned:
                continue
            if discovery[other] < 0:
                dfs(other, edge_index)
                low[vertex] = min(low[vertex], low[other])
                if low[other] > discovery[vertex]:
                    answer.append(edge_index)
            elif edge_index != parent_edge:
                low[vertex] = min(low[vertex], discovery[other])

    for vertex in range(len(incidence)):
        if discovery[vertex] < 0:
            dfs(vertex, -1)
    return answer


def component_after_deleting(
    incidence: list[list[tuple[int, int]]],
    banned: frozenset[int],
    start: int,
) -> int:
    reached = 1 << start
    frontier = reached
    while frontier:
        bit = frontier & -frontier
        frontier ^= bit
        vertex = bit.bit_length() - 1
        for other, edge_index in incidence[vertex]:
            if edge_index in banned or reached >> other & 1:
                continue
            reached |= 1 << other
            frontier |= 1 << other
    return reached


def cyclic_cut_profile(
    edges: tuple[tuple[int, int], ...]
) -> tuple[bool, bool, Counter[int], tuple[int, ...] | None]:
    """Exact cuts through size three in a connected cubic graph."""
    incidence: list[list[tuple[int, int]]] = [[] for _ in range(ORDER)]
    for index, (left, right) in enumerate(edges):
        incidence[left].append((right, index))
        incidence[right].append((left, index))
    full = (1 << ORDER) - 1
    profile: Counter[int] = Counter()

    bridges = bridge_indices(incidence, frozenset())
    if bridges:
        return False, False, Counter({1: len(bridges)}), (bridges[0],)

    cuts_two: set[tuple[int, int]] = set()
    for first in range(len(edges)):
        for second in bridge_indices(incidence, frozenset((first,))):
            if second != first:
                cuts_two.add(tuple(sorted((first, second))))
    if cuts_two:
        profile[2] = len(cuts_two)
        return True, False, profile, next(iter(cuts_two))

    cuts_three: set[tuple[int, int, int]] = set()
    nontrivial: set[tuple[int, int, int]] = set()
    for first in range(len(edges)):
        for second in range(first + 1, len(edges)):
            banned_two = frozenset((first, second))
            for third in bridge_indices(incidence, banned_two):
                if third in banned_two:
                    continue
                cut = tuple(sorted((first, second, third)))
                if cut in cuts_three:
                    continue
                cuts_three.add(cut)
                shore = component_after_deleting(
                    incidence, frozenset(cut), edges[cut[0]][0]
                )
                if shore != full and shore.bit_count() not in (1, ORDER - 1):
                    nontrivial.add(cut)
    profile[3] = len(cuts_three)
    first_bad = next(iter(nontrivial)) if nontrivial else None
    return True, not nontrivial, profile, first_bad


def complement_odd_circuits(
    rows: list[int], matching: tuple[tuple[int, int], ...]
) -> int:
    complement = rows[:]
    for left, right in matching:
        complement[left] &= ~(1 << right)
        complement[right] &= ~(1 << left)
    return sum(
        part.bit_count() % 2
        for part in components(complement, (1 << len(rows)) - 1)
    )


def matching_distribution(rows: list[int]) -> Counter[int]:
    result: Counter[int] = Counter()

    def search(vertices: int, chosen: list[tuple[int, int]]) -> None:
        if not vertices:
            result[complement_odd_circuits(rows, tuple(chosen))] += 1
            return
        remaining = vertices
        first = -1
        candidates = 0
        best = len(rows) + 1
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            vertex = bit.bit_length() - 1
            available = rows[vertex] & vertices & ~bit
            if available.bit_count() < best:
                first = vertex
                candidates = available
                best = available.bit_count()
                if best <= 1:
                    break
        if not candidates:
            return
        first_bit = 1 << first
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            chosen.append((first, second))
            search(vertices ^ first_bit ^ second_bit, chosen)
            chosen.pop()

    search((1 << len(rows)) - 1, [])
    return result


def edge_sha256(edges: tuple[tuple[int, int], ...]) -> str:
    encoded = "".join(f"{left} {right}\n" for left, right in edges)
    return sha256(encoded.encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--skip-class-cuts", action="store_true",
        help="only construct/canonicalize; skip full cyclic-cut classification",
    )
    args = parser.parse_args()

    q_rows, terminals, retained, q_edges = q67()
    patterns = outside_patterns()
    if len(patterns) != 128:
        raise AssertionError(f"expected 128 outside patterns, got {len(patterns)}")

    metadata: list[dict[str, object]] = []
    labelled_g6: list[str] = []
    for pattern_index, (z_rows, boundary) in enumerate(patterns):
        for assignment in boundary_assignments(boundary):
            edges = completion_edges(q_edges, terminals, z_rows, assignment)
            rows = rows_from_edges(ORDER, edges)
            if len(edges) != 114 or any(row.bit_count() != 3 for row in rows):
                raise AssertionError("completion is not a simple cubic 76-vertex graph")
            if len(components(rows, (1 << ORDER) - 1)) != 1:
                raise AssertionError("completion is disconnected")
            metadata.append({
                "pattern_index": pattern_index,
                "z_neighbourhoods": z_rows,
                "boundary_multiplicities": boundary,
                "terminal_to_w_assignment": assignment,
                "edges": edges,
                "rows": rows,
            })
            labelled_g6.append(graph6(rows))

    if len(metadata) != 9_600:
        raise AssertionError(f"expected 9600 unique labelled gluings, got {len(metadata)}")
    canonical = canonicalize_all(labelled_g6)
    classes: dict[str, list[int]] = {}
    for index, canonical_g6 in enumerate(canonical):
        classes.setdefault(canonical_g6, []).append(index)
    if len(classes) != 570:
        raise AssertionError(f"expected 570 isomorphism classes, got {len(classes)}")

    class_records: list[dict[str, object]] = []
    labelled_cyclic4 = 0
    labelled_bridgeless = 0
    for class_index, (canonical_g6, members) in enumerate(classes.items()):
        representative = metadata[members[0]]
        if args.skip_class_cuts:
            bridgeless = None
            cyclic4 = None
            cut_profile: Counter[int] = Counter()
            bad_edges = None
        else:
            bridgeless, cyclic4, cut_profile, bad_cut = cyclic_cut_profile(
                representative["edges"]
            )
            bad_edges = (
                [representative["edges"][edge_index] for edge_index in bad_cut]
                if bad_cut is not None else None
            )
            if bridgeless:
                labelled_bridgeless += len(members)
            if cyclic4:
                labelled_cyclic4 += len(members)
        class_records.append({
            "class_index": class_index,
            "canonical_graph6": canonical_g6,
            "multiplicity_among_labelled_gluings": len(members),
            "representative": {
                "labelled_index": members[0],
                "pattern_index": representative["pattern_index"],
                "z_neighbourhoods": [
                    list(row) for row in representative["z_neighbourhoods"]
                ],
                "boundary_multiplicities": list(
                    representative["boundary_multiplicities"]
                ),
                "terminal_source_labels": list(EXPECTED_TERMINALS),
                "terminal_to_w_assignment": list(
                    representative["terminal_to_w_assignment"]
                ),
                "edge_table_sha256": edge_sha256(representative["edges"]),
            },
            "bridgeless": bridgeless,
            "cyclically_four": cyclic4,
            "small_cut_counts": {
                str(key): value for key, value in sorted(cut_profile.items())
            },
            "first_nontrivial_small_cut_edges": (
                [list(edge) for edge in bad_edges] if bad_edges else None
            ),
        })

    lex_index = next(
        index for index, item in enumerate(metadata)
        if item["z_neighbourhoods"] == LEX_ROWS
        and item["terminal_to_w_assignment"] == LEX_BOUNDARY_ASSIGNMENT
    )
    lex = metadata[lex_index]
    lex_distribution = matching_distribution(lex["rows"])
    if dict(lex_distribution) != EXPECTED_LEX_DISTRIBUTION:
        raise AssertionError("lex-first perfect-matching distribution changed")
    (
        lex_bridgeless,
        lex_cyclic4,
        lex_cut_profile,
        lex_bad_cut,
    ) = cyclic_cut_profile(lex["edges"])
    if not lex_bridgeless or not lex_cyclic4 or lex_bad_cut is not None:
        raise AssertionError("advertised lex-first completion is not cyclically four")
    lex_class = class_records[
        next(index for index, key in enumerate(classes) if key == canonical[lex_index])
    ]
    if not args.skip_class_cuts and not lex_class["cyclically_four"]:
        raise AssertionError("advertised lex-first completion is not cyclically four")

    multiplicity_histogram = Counter(len(members) for members in classes.values())
    boundary_shape_histogram = Counter(
        tuple(sorted((value for value in boundary if value), reverse=True))
        for _rows, boundary in patterns
    )
    assignments_per_pattern_histogram = Counter(
        len(boundary_assignments(boundary)) for _rows, boundary in patterns
    )
    report = {
        "schema": "s2-q67-completion-class-census-v1",
        "classification": "EXACT FINITE STRUCTURAL CENSUS",
        "scope_warning": (
            "Perfect matchings were exhaustively enumerated only for the "
            "selected lex-first completion. Oddness is not a Five-CDC "
            "obstruction, and this report is not a Five-CDC resolution."
        ),
        "outside_patterns": len(patterns),
        "outside_boundary_shape_histogram": {
            "+".join(map(str, key)): value
            for key, value in sorted(boundary_shape_histogram.items())
        },
        "terminal_assignments_per_pattern_histogram": {
            str(key): value
            for key, value in sorted(assignments_per_pattern_histogram.items())
        },
        "unique_labelled_gluings": len(metadata),
        "isomorphism_classes": len(classes),
        "class_multiplicity_histogram": {
            str(key): value for key, value in sorted(multiplicity_histogram.items())
        },
        "class_cut_checks_skipped": args.skip_class_cuts,
        "labelled_bridgeless_completions": (
            None if args.skip_class_cuts else labelled_bridgeless
        ),
        "labelled_cyclically_four_completions": (
            None if args.skip_class_cuts else labelled_cyclic4
        ),
        "cyclically_four_isomorphism_classes": (
            None if args.skip_class_cuts else
            sum(record["cyclically_four"] for record in class_records)
        ),
        "selected_lex_completion": {
            "labelled_index": lex_index,
            "z_neighbourhoods": [list(row) for row in LEX_ROWS],
            "boundary_multiplicities": [0, 1, 0, 1, 1, 2],
            "terminal_source_labels": list(EXPECTED_TERMINALS),
            "terminal_to_w_assignment": list(LEX_BOUNDARY_ASSIGNMENT),
            "order": ORDER,
            "edges": len(lex["edges"]),
            "canonical_graph6": canonical[lex_index],
            "edge_table_sha256": edge_sha256(lex["edges"]),
            "bridgeless": lex_bridgeless,
            "cyclically_four": lex_cyclic4,
            "small_cut_counts": {
                str(key): value for key, value in sorted(lex_cut_profile.items())
            },
            "perfect_matchings": sum(lex_distribution.values()),
            "oddness": min(lex_distribution),
            "complementary_odd_circuit_distribution": {
                str(key): value for key, value in sorted(lex_distribution.items())
            },
            "normalized_edges": [list(edge) for edge in lex["edges"]],
        },
        "class_records": class_records,
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n")
    print(rendered)
    return 0


# Kept explicit to make the terminal order in reports visually auditable.
EXPECTED_TERMINALS = (3, 7, 8, 9, 12)


if __name__ == "__main__":
    raise SystemExit(main())
