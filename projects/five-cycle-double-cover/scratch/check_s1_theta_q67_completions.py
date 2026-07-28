#!/usr/bin/env python3
"""Exact census of the 120 s=1 theta completions of the Q67 five-pole.

This is a structural/oddness experiment, not a Five-CDC counterexample
search.  The 67-vertex factor-critical five-pole Q is obtained by deleting
the induced path 4-0-5 from the 70-vertex N2-N2-N1 graph constructed in
``check_cyclic4_all_bad_threshold_three_core.py``.

The outside shore has W = {w0,...,w4}, roots w0w1 and w2w3, and singleton
vertices z0,z1 with neighbourhoods

    N(z0) = {w0,w2,w4},   N(z1) = {w1,w3,w4}.

Every w has one boundary stub.  The program checks every one of the 5!
bijections from the five Q terminals to these stubs.  It independently:

* validates simplicity, cubicity, connectedness and bridgelessness;
* exhaustively detects edge cuts of size at most three;
* enumerates every perfect matching and the odd circuits in its complement
  once per canonical isomorphism class (or once per labelled graph when
  ``--no-canonical`` is used);
* checks the advertised Gallai--Edmonds decomposition after deleting the
  four root endpoints; and
* optionally canonicalizes graph6 strings with Brendan McKay's ``labelg``.

The perfect-matching census uses no SAT solver and is exact.  The imported
module is used only to reproduce the previously audited primary-source Q67
edge table; all completion and census routines below are separate.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import subprocess

from check_cyclic4_all_bad_threshold_three_core import (
    DELETED_PATH,
    EXPECTED_BOUNDARY_OLD,
    adjacency as source_adjacency,
    build_source,
    delete_source_vertices,
)


Q_ORDER = 67
W = tuple(range(Q_ORDER, Q_ORDER + 5))
Z = (Q_ORDER + 5, Q_ORDER + 6)
ORDER = Q_ORDER + 7
ROOTS = ((W[0], W[1]), (W[2], W[3]))
OUTSIDE_EDGES = (
    ROOTS[0],
    ROOTS[1],
    (Z[0], W[0]),
    (Z[0], W[2]),
    (Z[0], W[4]),
    (Z[1], W[1]),
    (Z[1], W[3]),
    (Z[1], W[4]),
)


def normalized_edges(rows: list[int]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (left, right)
        for left, row in enumerate(rows)
        for right in range(left + 1, len(rows))
        if row >> right & 1
    )


def rows_from_edges(
    order: int, edges: tuple[tuple[int, int], ...]
) -> list[int]:
    rows = [0] * order
    seen: set[tuple[int, int]] = set()
    for edge in edges:
        left, right = sorted(edge)
        if left == right or not (0 <= left < right < order):
            raise AssertionError(f"invalid edge {edge}")
        if (left, right) in seen:
            raise AssertionError(f"duplicate edge {(left, right)}")
        seen.add((left, right))
        rows[left] |= 1 << right
        rows[right] |= 1 << left
    return rows


def components(rows: list[int], allowed: int) -> list[int]:
    answer: list[int] = []
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
        answer.append(reached)
        allowed &= ~reached
    return answer


def q67() -> tuple[
    list[int], tuple[int, ...], tuple[int, ...], tuple[tuple[int, int], ...]
]:
    source_order, source_edges = build_source()
    if source_order != 70:
        raise AssertionError("unexpected source order")
    source = source_adjacency(source_order, source_edges)
    core, retained, old_to_new = delete_source_vertices(source, DELETED_PATH)
    terminals_new = tuple(old_to_new[old] for old in EXPECTED_BOUNDARY_OLD)
    degree_two = tuple(
        vertex for vertex, row in enumerate(core) if row.bit_count() == 2
    )
    if set(terminals_new) != set(degree_two) or len(core) != Q_ORDER:
        raise AssertionError("unexpected Q67 terminal set")
    return core, terminals_new, tuple(retained), normalized_edges(core)


def completion(
    q_edges: tuple[tuple[int, int], ...],
    terminals_new: tuple[int, ...],
    terminal_at_w: tuple[int, ...],
) -> tuple[list[int], tuple[tuple[int, int], ...]]:
    if set(terminal_at_w) != set(terminals_new):
        raise AssertionError("not a terminal bijection")
    boundary = tuple((terminal_at_w[index], W[index]) for index in range(5))
    edges = tuple(sorted(q_edges + OUTSIDE_EDGES + boundary))
    rows = rows_from_edges(ORDER, edges)
    return rows, edges


def bridge_indices(
    incidence: list[list[tuple[int, int]]], banned: frozenset[int]
) -> list[int]:
    """Tarjan bridge search in a graph with selected edge indices removed."""
    order = len(incidence)
    discovery = [-1] * order
    low = [0] * order
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

    for vertex in range(order):
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
    """Return bridgelessness and exact nontrivial cuts of sizes <= 3.

    In a connected cubic graph a shore of a k-edge cut has cycle rank
    ``(n-k+2)/2``.  Thus every 1- or 2-cut is cyclic on both shores, while a
    3-cut is non-cyclic on a shore exactly when that shore is one vertex.
    """
    incidence: list[list[tuple[int, int]]] = [[] for _ in range(ORDER)]
    for index, (left, right) in enumerate(edges):
        incidence[left].append((right, index))
        incidence[right].append((left, index))
    full = (1 << ORDER) - 1
    cut_counts: Counter[int] = Counter()
    first_bad: tuple[int, ...] | None = None

    bridges = bridge_indices(incidence, frozenset())
    if bridges:
        return False, False, Counter({1: len(bridges)}), (bridges[0],)

    # Every 2-cut {e,f} appears as a bridge f after e is removed.
    cuts_two: set[tuple[int, int]] = set()
    for first in range(len(edges)):
        for second in bridge_indices(incidence, frozenset((first,))):
            if second != first:
                cuts_two.add(tuple(sorted((first, second))))
    if cuts_two:
        cut_counts[2] = len(cuts_two)
        first_bad = next(iter(cuts_two))
        return True, False, cut_counts, first_bad

    # With no smaller cut, test each unordered first pair.  A bridge in the
    # twice-deleted graph completes a 3-cut.  Count each cut only once.
    cuts_three: set[tuple[int, int, int]] = set()
    nontrivial_three: set[tuple[int, int, int]] = set()
    edge_count = len(edges)
    for first in range(edge_count):
        for second in range(first + 1, edge_count):
            banned_two = frozenset((first, second))
            for third in bridge_indices(incidence, banned_two):
                if third == first or third == second:
                    continue
                cut = tuple(sorted((first, second, third)))
                if cut in cuts_three:
                    continue
                cuts_three.add(cut)
                banned_three = frozenset(cut)
                shore = component_after_deleting(
                    incidence, banned_three, edges[cut[0]][0]
                )
                if shore != full:
                    size = shore.bit_count()
                    if size != 1 and size != ORDER - 1:
                        nontrivial_three.add(cut)
    cut_counts[3] = len(cuts_three)
    if nontrivial_three:
        first_bad = next(iter(nontrivial_three))
    return True, not nontrivial_three, cut_counts, first_bad


def complement_odd_circuits(
    rows: list[int], matching: tuple[tuple[int, int], ...]
) -> int:
    complement = rows[:]
    for left, right in matching:
        complement[left] &= ~(1 << right)
        complement[right] &= ~(1 << left)
    full = (1 << len(rows)) - 1
    odd = 0
    for part in components(complement, full):
        # The complement of a perfect matching in a cubic graph is 2-regular.
        if part.bit_count() % 2:
            odd += 1
    return odd


def matching_profile(
    rows: list[int],
) -> tuple[Counter[int], Counter[tuple[int, int, int]]]:
    """Enumerate every perfect matching and its complementary odd circuits.

    The secondary key is (number of roots, number of Q--W boundary edges,
    odd circuits), making the Gallai--Edmonds matching equation checkable.
    """
    full = (1 << len(rows)) - 1
    distribution: Counter[int] = Counter()
    typed: Counter[tuple[int, int, int]] = Counter()
    root_set = {tuple(sorted(edge)) for edge in ROOTS}
    boundary_mask = (1 << Q_ORDER) - 1

    def search(vertices: int, chosen: list[tuple[int, int]]) -> None:
        if not vertices:
            matching = tuple(chosen)
            odd = complement_odd_circuits(rows, matching)
            root_count = sum(tuple(sorted(edge)) in root_set for edge in matching)
            boundary_count = sum(
                ((1 << left) & boundary_mask) != 0
                and Q_ORDER <= right < Q_ORDER + 5
                or ((1 << right) & boundary_mask) != 0
                and Q_ORDER <= left < Q_ORDER + 5
                for left, right in matching
            )
            distribution[odd] += 1
            typed[(root_count, boundary_count, odd)] += 1
            return

        # Branch on the unmatched vertex with fewest currently available
        # neighbours.  This is exact and substantially faster than label order.
        remaining = vertices
        first = -1
        candidates = 0
        best = ORDER + 1
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            vertex = bit.bit_length() - 1
            available = rows[vertex] & vertices & ~bit
            count = available.bit_count()
            if count < best:
                first = vertex
                candidates = available
                best = count
                if count <= 1:
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

    search(full, [])
    return distribution, typed


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
        candidates = rows[first] & vertices
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            if matchable(vertices ^ first_bit ^ second_bit):
                return True
        return False

    return all(matchable(full ^ (1 << vertex)) for vertex in range(len(rows)))


def ge_structure(rows: list[int], q_rows: list[int]) -> bool:
    """Check D-components after deleting U and the one A-vertex w4.

    In H=G-U, the canonical Gallai--Edmonds separator is A={w4}; deleting
    A from H therefore leaves Q,z0,z1.
    """
    deleted_w = sum(1 << vertex for vertex in W)
    allowed = ((1 << ORDER) - 1) ^ deleted_w
    parts = components(rows, allowed)
    q_mask = (1 << Q_ORDER) - 1
    singleton_masks = {1 << Z[0], 1 << Z[1]}
    return (
        set(parts) == {q_mask, *singleton_masks}
        and factor_critical(q_rows)
    )


def graph6(rows: list[int]) -> str:
    n = len(rows)
    if n <= 62:
        data = [n]
    elif n <= 258047:
        data = [63, (n >> 12) & 63, (n >> 6) & 63, n & 63]
    else:
        raise ValueError("order too large for this encoder")
    bits = [
        1 if rows[left] >> right & 1 else 0
        for right in range(1, n)
        for left in range(right)
    ]
    while len(bits) % 6:
        bits.append(0)
    data.extend(
        sum(bits[offset + index] << (5 - index) for index in range(6))
        for offset in range(0, len(bits), 6)
    )
    return "".join(chr(value + 63) for value in data)


def canonical_graph6(g6: str) -> str | None:
    try:
        completed = subprocess.run(
            ["labelg", "-q"],
            input=(g6 + "\n").encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return completed.stdout.decode().strip()


def edge_sha256(edges: tuple[tuple[int, int], ...]) -> str:
    payload = "\n".join(f"{left} {right}" for left, right in edges) + "\n"
    return sha256(payload.encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit", type=int, default=120,
        help="debugging prefix of the lexicographic 120 bijections",
    )
    parser.add_argument(
        "--output", type=Path,
        help="write the JSON report here as well as stdout",
    )
    parser.add_argument(
        "--no-canonical", action="store_true",
        help="do not call optional nauty labelg",
    )
    args = parser.parse_args()
    if not 1 <= args.limit <= 120:
        parser.error("--limit must be between 1 and 120")

    q_rows, terminals_new, retained, q_edges = q67()
    if not factor_critical(q_rows):
        raise AssertionError("Q67 factor-criticality changed")

    records: list[dict[str, object]] = []
    census: Counter[tuple[bool, int]] = Counter()
    canonical_classes: Counter[str] = Counter()
    matching_cache: dict[
        str, tuple[Counter[int], Counter[tuple[int, int, int]]]
    ] = {}
    for index, assignment in enumerate(permutations(terminals_new)):
        if index >= args.limit:
            break
        rows, edges = completion(q_edges, terminals_new, assignment)
        if len(edges) != 111:
            raise AssertionError("wrong completion size")
        if any(row.bit_count() != 3 for row in rows):
            raise AssertionError("completion is not cubic")
        if len(components(rows, (1 << ORDER) - 1)) != 1:
            raise AssertionError("completion is disconnected")
        bridgeless, cyclic4, cut_profile, first_bad_cut = cyclic_cut_profile(edges)
        g6 = graph6(rows)
        canonical = None if args.no_canonical else canonical_graph6(g6)
        cache_key = canonical if canonical is not None else f"labelled:{index}"
        if cache_key in matching_cache:
            cached_distribution, cached_typed = matching_cache[cache_key]
            distribution = Counter(cached_distribution)
            typed = Counter(cached_typed)
        else:
            distribution, typed = matching_profile(rows)
            matching_cache[cache_key] = (
                Counter(distribution), Counter(typed)
            )
        if not distribution:
            raise AssertionError("completion has no perfect matching")
        if any(root_count * 2 + boundary_count != 3
               for root_count, boundary_count, _odd in typed):
            raise AssertionError("matching type violates k+2r=3")
        if not ge_structure(rows, q_rows):
            raise AssertionError("claimed GE deletion structure failed")
        oddness = min(distribution)
        census[(cyclic4, oddness)] += 1
        if canonical is not None:
            canonical_classes[canonical] += 1
        record = {
            "bijection_index": index,
            "terminal_at_w_source_labels": [
                retained[terminal] for terminal in assignment
            ],
            "terminal_at_w_q_labels": list(assignment),
            "bridgeless": bridgeless,
            "cyclically_four": cyclic4,
            "small_cut_counts": {
                str(key): value for key, value in sorted(cut_profile.items())
            },
            "first_nontrivial_small_cut_edges": (
                [list(edges[edge_index]) for edge_index in first_bad_cut]
                if first_bad_cut is not None else None
            ),
            "perfect_matchings": sum(distribution.values()),
            "oddness": oddness,
            "complementary_odd_circuit_distribution": {
                str(key): value for key, value in sorted(distribution.items())
            },
            "matching_type_distribution": {
                f"r={root_count},k={boundary_count},odd={odd}": count
                for (root_count, boundary_count, odd), count
                in sorted(typed.items())
            },
            "graph6_labelled": g6,
            "graph6_canonical": canonical,
            "edge_table_sha256": edge_sha256(edges),
        }
        records.append(record)
        print(
            f"{index + 1}/{args.limit}: "
            f"cyclic4={cyclic4} oddness={oddness} "
            f"PM={sum(distribution.values())}",
            flush=True,
        )

    # Store the complete normalized edge table for the lexicographically first
    # cyclic-four completion of maximum observed oddness.
    cyclic_records = [record for record in records if record["cyclically_four"]]
    witness_record = None
    witness_edges = None
    if cyclic_records:
        witness_record = max(
            cyclic_records,
            key=lambda record: (
                int(record["oddness"]),
                -int(record["bijection_index"]),
            ),
        )
        witness_assignment = tuple(
            terminals_new[EXPECTED_BOUNDARY_OLD.index(old)]
            for old in witness_record["terminal_at_w_source_labels"]
        )
        _rows, witness_edges_tuple = completion(
            q_edges, terminals_new, witness_assignment
        )
        witness_edges = [list(edge) for edge in witness_edges_tuple]

    report = {
        "schema": "s1-theta-q67-completion-census-v1",
        "classification": "EXACT FINITE STRUCTURAL AND ODDNESS CENSUS",
        "scope_warning": (
            "Oddness is not a Five-CDC obstruction. This census neither "
            "proves nor disproves the Five-Cycle Double Cover Conjecture."
        ),
        "q67": {
            "order": Q_ORDER,
            "deleted_source_path": list(DELETED_PATH),
            "terminal_source_labels": list(EXPECTED_BOUNDARY_OLD),
            "terminal_q_labels": list(terminals_new),
        },
        "outside": {
            "W": list(W),
            "Z": list(Z),
            "roots": [list(edge) for edge in ROOTS],
            "z_neighbourhoods_in_W_indices": [[0, 2, 4], [1, 3, 4]],
            "one_boundary_stub_at_every_W": True,
        },
        "bijections_checked": len(records),
        "census_by_cyclic4_and_oddness": {
            f"cyclic4={cyclic4},oddness={oddness}": count
            for (cyclic4, oddness), count in sorted(census.items())
        },
        "canonical_isomorphism_classes": len(canonical_classes),
        "canonical_class_multiplicities": dict(sorted(canonical_classes.items())),
        "maximum_cyclic4_oddness": (
            max(int(record["oddness"]) for record in cyclic_records)
            if cyclic_records else None
        ),
        "selected_witness": witness_record,
        "selected_witness_normalized_edges": witness_edges,
        "records": records,
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
