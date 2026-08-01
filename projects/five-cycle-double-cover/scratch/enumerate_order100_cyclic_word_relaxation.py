#!/usr/bin/env python3
"""Exact solver-free cyclic-word strengthening at order 100.

This imports only the baseline row-domain generator from the transparent
order-100 incidence census.  It then imposes, on every marked core C10 on
both shores, the existence of a cyclic word on its five c-edge positions
that satisfies:

* position zero is its private marked edge (the diagonal incidence);
* a doubled off-diagonal C12 neighbour occupies positions 1 and 4; and
* a doubled off-diagonal C14 neighbour does not occupy consecutive
  positions.

The program exhausts all 1002 simultaneous-S8 profile orbits and stops at
the first matrix per feasible profile.  The result is still a relaxation:
compatible words on distinct circuits need not extend to one global cubic
rotation system.
"""

from __future__ import annotations

import hashlib
import itertools
import json

import enumerate_order100_incidence_relaxation as baseline


def cyclic_word_witness(
    own_excess: int,
    opposite_excesses: tuple[int, ...],
    own_index: int,
    counts: tuple[int, ...],
):
    """Return the first valid C10 incidence word, or ``None``.

    Non-C10 circuits have no word constraint in this strengthening.
    """
    if own_excess != 0:
        return ()
    if sum(counts) != 5 or counts[own_index] < 1:
        return None

    remaining = list(counts)
    remaining[own_index] -= 1
    multiset = tuple(
        column
        for column, multiplicity in enumerate(remaining)
        for _ in range(multiplicity)
    )
    if len(multiset) != 4:
        return None

    for tail in sorted(set(itertools.permutations(multiset))):
        word = (own_index,) + tail
        positions = {
            column: {
                position
                for position, value in enumerate(word)
                if value == column
            }
            for column in set(word)
        }
        valid = True
        for column, used in positions.items():
            if column == own_index or len(used) != 2:
                continue
            if opposite_excesses[column] == 1 and used != {1, 4}:
                valid = False
                break
            if opposite_excesses[column] == 2:
                left, right = sorted(used)
                if (right - left) % 5 in {1, 4}:
                    valid = False
                    break
        if valid:
            return word
    return None


def filtered_domains(x, y):
    """Return exact row and column domains after cyclic-word filtering."""
    row_domains = []
    for row in range(8):
        domain = tuple(
            candidate
            for candidate in baseline.make_row_candidates(x, y, row)
            if cyclic_word_witness(x[row], y, row, candidate) is not None
        )
        row_domains.append(domain)

    column_domains = []
    for column in range(8):
        domain = tuple(
            candidate
            for candidate in baseline.make_row_candidates(y, x, column)
            if cyclic_word_witness(
                y[column], x, column, candidate
            ) is not None
        )
        column_domains.append(domain)
    return tuple(row_domains), tuple(column_domains)


def first_matrix(x, y):
    """Join exact row and column domains with a bit-mask backtracker."""
    row_domains, column_domains = filtered_domains(x, y)
    if any(not domain for domain in row_domains + column_domains):
        return None, 0

    # For every column candidate, pre-index the candidates having a specified
    # entry in each row.  Intersecting these masks after a row choice enforces
    # the complete column domain without an unsafe aggregate-state memo.
    masks = []
    for column, domain in enumerate(column_domains):
        by_row = []
        for row in range(8):
            by_value = {}
            for candidate_index, candidate in enumerate(domain):
                value = candidate[row]
                by_value[value] = by_value.get(value, 0) | (
                    1 << candidate_index
                )
            by_row.append(by_value)
        masks.append(by_row)

    row_order = tuple(
        sorted(range(8), key=lambda row: (len(row_domains[row]), row))
    )
    initial_column_masks = tuple(
        (1 << len(domain)) - 1 for domain in column_domains
    )
    memo = set()
    nodes = 0

    def visit(position, possible_columns):
        nonlocal nodes
        nodes += 1
        if position == 8:
            return ()
        key = (position, possible_columns)
        if key in memo:
            return None
        row = row_order[position]
        for candidate in row_domains[row]:
            next_columns = tuple(
                possible_columns[column]
                & masks[column][row].get(candidate[column], 0)
                for column in range(8)
            )
            if any(mask == 0 for mask in next_columns):
                continue
            tail = visit(position + 1, next_columns)
            if tail is not None:
                return ((row, candidate),) + tail
        memo.add(key)
        return None

    selected = visit(0, initial_column_masks)
    if selected is None:
        return None, nodes
    matrix = [None] * 8
    for row, candidate in selected:
        matrix[row] = candidate
    return tuple(matrix), nodes


def main():
    records = []
    survivors = []
    total_nodes = 0
    for x, y in baseline.canonical_profile_pairs():
        matrix, nodes = first_matrix(x, y)
        total_nodes += nodes
        records.append(
            {"x": x, "y": y, "feasible": matrix is not None, "nodes": nodes}
        )
        if matrix is not None:
            row_words = tuple(
                cyclic_word_witness(x[row], y, row, matrix[row])
                for row in range(8)
            )
            columns = tuple(
                tuple(matrix[row][column] for row in range(8))
                for column in range(8)
            )
            column_words = tuple(
                cyclic_word_witness(y[column], x, column, columns[column])
                for column in range(8)
            )
            assert all(word is not None for word in row_words + column_words)
            survivors.append(
                {
                    "x": x,
                    "y": y,
                    "matrix": matrix,
                    "row_words": row_words,
                    "column_words": column_words,
                }
            )

    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    witness_text = json.dumps(
        survivors, sort_keys=True, separators=(",", ":")
    )
    print("order-100 cyclic-word incidence relaxation: PASS")
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
        "scope=abstract row/column cyclic-word relaxation; first matrix per "
        "profile; no global graph realization"
    )
    if survivors:
        print("canonical_frontier_survivor=")
        print(json.dumps(survivors[0], indent=2))


if __name__ == "__main__":
    main()
