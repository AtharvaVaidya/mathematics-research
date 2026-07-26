#!/usr/bin/env python3
"""Canonical census of the all-marked order-100 incidence relaxation.

The program is a solver-free integer backtracker.  It enumerates one
representative of every pair of excess profiles under simultaneous
permutation of the eight marked indices and decides whether at least one
8-by-8 nonnegative integer incidence matrix satisfies the currently proved
pairwise girth, Kempe-support, and short-C10 spacing constraints.

This is a frontier census, not a graph-realization search.  It intentionally
stops at the first matrix for each feasible profile.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from dataclasses import dataclass
from pathlib import Path


ORDER = 8
SURPLUS = 6

OFF_DIAGONAL_CAP = (
    (1, 2, 2, 2, 2),
    (2, 2, 2, 3, 3),
    (2, 2, 3, 3, 4),
    (2, 3, 3, 3, 4),
    (2, 3, 4, 4, 4),
)

DIAGONAL_CAP = (
    (1, 1, 2, 2, 2),
    (1, 2, 2, 2, 3),
    (2, 2, 2, 3, 3),
    (2, 2, 3, 3, 4),
    (2, 3, 3, 4, 4),
)


def weak_compositions(total: int, parts: int):
    """Yield all ordered weak compositions of total into ``parts`` entries."""
    current = [0] * parts

    def visit(position: int, remaining: int):
        if position == parts - 1:
            current[position] = remaining
            yield tuple(current)
            return
        for value in range(remaining + 1):
            current[position] = value
            yield from visit(position + 1, remaining - value)

    yield from visit(0, total)


def partitions_padded(total: int, parts: int):
    """Return padded partitions in reverse lexicographic order."""
    return tuple(
        sorted(
            (
                values
                for values in weak_compositions(total, parts)
                if all(
                    values[index] >= values[index + 1]
                    for index in range(parts - 1)
                )
            ),
            reverse=True,
        )
    )


def canonical_profile_pairs():
    """Represent every orbit of ``(x,y)`` under simultaneous ``S_8``."""
    for x in partitions_padded(SURPLUS, ORDER):
        for y in weak_compositions(SURPLUS, ORDER):
            # With x sorted, its stabilizer acts inside its equal-value blocks.
            if not all(
                x[index] != x[index + 1] or y[index] >= y[index + 1]
                for index in range(ORDER - 1)
            ):
                continue
            yield x, y


def entry_cap(x_value: int, y_value: int, diagonal: bool):
    """Return exactly the proved local cap used by this relaxation."""
    if x_value <= 4 and y_value <= 4:
        table = DIAGONAL_CAP if diagonal else OFF_DIAGONAL_CAP
        return table[x_value][y_value]

    # The finite table was proved only through excess four.  Beyond it we
    # retain the general marked-overlap bound and the elementary fact that
    # two differently marked circuits each have a private marked c-edge.
    if diagonal:
        return min(1 + x_value + y_value, 5 + min(x_value, y_value))
    return min(1 + x_value + y_value, 4 + min(x_value, y_value))


def positive_assignments(caps: tuple[int, ...], total: int):
    """Yield positive bounded vectors having the requested total."""
    current = [0] * len(caps)

    def visit(position: int, remaining: int):
        if position == len(caps):
            if remaining == 0:
                yield tuple(current)
            return
        later_minimum = len(caps) - position - 1
        upper = min(caps[position], remaining - later_minimum)
        for value in range(1, upper + 1):
            current[position] = value
            yield from visit(position + 1, remaining - value)

    yield from visit(0, total)


def make_row_candidates(x, y, row: int):
    """Enumerate every admissible row before cross-row constraints."""
    degree = 5 + x[row]
    support_bound = (7 + x[row]) // 2
    caps = tuple(
        entry_cap(x[row], y[column], row == column)
        for column in range(ORDER)
    )
    candidates = []
    for support_size in range(1, min(ORDER, support_bound) + 1):
        for support in itertools.combinations(range(ORDER), support_size):
            if row not in support:
                continue
            support_caps = tuple(caps[column] for column in support)
            if sum(support_caps) < degree:
                continue
            for positive in positive_assignments(support_caps, degree):
                values = [0] * ORDER
                for column, value in zip(support, positive):
                    values[column] = value
                # A marked core C10 can double-overlap with at most one
                # differently marked opposite core C12.
                if x[row] == 0:
                    doubled_c12 = sum(
                        column != row
                        and y[column] == 1
                        and values[column] == 2
                        for column in range(ORDER)
                    )
                    if doubled_c12 > 1:
                        continue
                candidates.append(tuple(values))
    return tuple(candidates)


@dataclass
class SearchStats:
    nodes: int = 0
    memo_hits: int = 0


def first_matrix(x, y):
    """Return the first feasible matrix and exact DFS statistics."""
    row_domains = tuple(
        make_row_candidates(x, y, row) for row in range(ORDER)
    )
    if any(not domain for domain in row_domains):
        return None, row_domains, SearchStats()
    row_domain_sets = tuple(set(domain) for domain in row_domains)
    row_order = tuple(
        sorted(range(ORDER), key=lambda row: (len(row_domains[row]), row))
    )
    column_targets = tuple(5 + value for value in y)
    column_support_caps = tuple((7 + value) // 2 for value in y)
    column_minimum = tuple(
        tuple(min(candidate[column] for candidate in row_domains[row])
              for column in range(ORDER))
        for row in range(ORDER)
    )
    column_maximum = tuple(
        tuple(max(candidate[column] for candidate in row_domains[row])
              for column in range(ORDER))
        for row in range(ORDER)
    )
    stats = SearchStats()
    memo = set()

    def visit(unassigned, remaining, support, doubled):
        stats.nodes += 1
        if not unassigned:
            return () if all(value == 0 for value in remaining) else None
        key = (unassigned, remaining, support, doubled)
        if key in memo:
            stats.memo_hits += 1
            return None

        row = unassigned[0]
        if len(unassigned) == 1:
            forced = remaining
            candidates = [forced] if forced in row_domain_sets[row] else []
        else:
            candidates = [
                candidate
                for candidate in row_domains[row]
                if all(
                    candidate[column] <= remaining[column]
                    and support[column] + (candidate[column] > 0)
                    <= column_support_caps[column]
                    for column in range(ORDER)
                )
            ]

        next_unassigned = unassigned[1:]
        for candidate in candidates:
            if any(
                y[column] == 0
                and x[row] == 1
                and row != column
                and candidate[column] == 2
                and doubled[column] >= 1
                for column in range(ORDER)
            ):
                continue

            next_remaining = tuple(
                remaining[column] - candidate[column]
                for column in range(ORDER)
            )
            next_support = tuple(
                support[column] + (candidate[column] > 0)
                for column in range(ORDER)
            )
            next_doubled = list(doubled)
            for column in range(ORDER):
                if (
                    y[column] == 0
                    and x[row] == 1
                    and row != column
                    and candidate[column] == 2
                ):
                    next_doubled[column] += 1

            # Independent per-column capacity bounds are necessary conditions.
            feasible = True
            for column in range(ORDER):
                slots = column_support_caps[column] - next_support[column]
                forced_rows = [
                    other
                    for other in next_unassigned
                    if column_minimum[other][column] > 0
                ]
                if len(forced_rows) > slots:
                    feasible = False
                    break
                minimum = sum(
                    column_minimum[other][column]
                    for other in next_unassigned
                )
                forced_maximum = sum(
                    column_maximum[other][column] for other in forced_rows
                )
                optional_maxima = sorted(
                    (
                        column_maximum[other][column]
                        for other in next_unassigned
                        if other not in forced_rows
                    ),
                    reverse=True,
                )
                maximum = forced_maximum + sum(
                    optional_maxima[: slots - len(forced_rows)]
                )
                if not minimum <= next_remaining[column] <= maximum:
                    feasible = False
                    break
            if not feasible:
                continue

            tail = visit(
                next_unassigned,
                next_remaining,
                next_support,
                tuple(next_doubled),
            )
            if tail is not None:
                return ((row, candidate),) + tail

        memo.add(key)
        return None

    selected = visit(
        row_order,
        column_targets,
        (0,) * ORDER,
        (0,) * ORDER,
    )
    if selected is None:
        return None, row_domains, stats
    rows = [None] * ORDER
    for row, candidate in selected:
        rows[row] = candidate
    return tuple(rows), row_domains, stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-json",
        type=Path,
        help="write all canonical feasibility records and first witnesses",
    )
    args = parser.parse_args()
    records = []
    survivors = []
    total_nodes = 0
    for x, y in canonical_profile_pairs():
        matrix, domains, stats = first_matrix(x, y)
        total_nodes += stats.nodes
        record = {
            "x": x,
            "y": y,
            "feasible": matrix is not None,
            "row_domain_sizes": tuple(len(domain) for domain in domains),
            "nodes": stats.nodes,
        }
        records.append(record)
        if matrix is not None:
            survivors.append({"x": x, "y": y, "matrix": matrix})

    assert len(records) == 1002
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    witness_text = json.dumps(
        survivors, sort_keys=True, separators=(",", ":")
    )
    artifact = {
        "schema": "order100-all-marked-incidence-relaxation-v1",
        "scope_warning": (
            "Abstract incidence relaxation only; one matrix per feasible "
            "profile; no cyclic rotation or graph realization is asserted."
        ),
        "records": records,
        "survivors": survivors,
    }
    if args.output_json:
        args.output_json.write_text(
            json.dumps(artifact, indent=2) + "\n", encoding="utf-8"
        )
    print("order-100 all-marked incidence relaxation: PASS")
    print(f"canonical_profile_pairs={len(records)}")
    print(f"surviving_profiles={len(survivors)}")
    print(f"total_search_nodes={total_nodes}")
    print(
        "census_sha256="
        f"{hashlib.sha256(canonical.encode()).hexdigest()}"
    )
    print(
        "survivor_sha256="
        f"{hashlib.sha256(witness_text.encode()).hexdigest()}"
    )
    print(
        "scope=abstract all-marked incidence relaxation; first matrix per "
        "profile; no graph realization"
    )
    if survivors:
        print("canonical_frontier_survivor=")
        print(json.dumps(survivors[0], indent=2))


if __name__ == "__main__":
    main()
