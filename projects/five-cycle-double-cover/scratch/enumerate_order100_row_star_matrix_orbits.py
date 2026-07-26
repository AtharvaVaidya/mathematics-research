#!/usr/bin/env python3
"""Enumerate matrix orbits inside the three order-100 row-star profiles.

The simultaneous stabilizer of an aligned profile pair permutes indices
having the same ordered pair ``(x_i,y_i)``.  This solver-free program
enumerates every labelled row/column-star matrix and retains the
lexicographically least matrix under that stabilizer.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import enumerate_order100_exact_row_star_relaxation as row_star


INPUT = Path("scratch/order100-exact-row-star-survivors.json")
OUTPUT = Path("scratch/order100-row-star-matrix-orbits.json")


def stabilizer_permutations(x, y):
    groups = {}
    for index, pair in enumerate(zip(x, y)):
        groups.setdefault(pair, []).append(index)
    result = []
    for choices in itertools.product(
        *(itertools.permutations(group) for group in groups.values())
    ):
        permutation = list(range(8))
        for old_group, new_group in zip(groups.values(), choices):
            for old, new in zip(old_group, new_group):
                permutation[old] = new
        result.append(tuple(permutation))
    return tuple(result)


def transform(matrix, permutation):
    inverse = [0] * 8
    for old, new in enumerate(permutation):
        inverse[new] = old
    return tuple(
        tuple(
            matrix[inverse[row]][inverse[column]]
            for column in range(8)
        )
        for row in range(8)
    )


def canonical_matrix(matrix, permutations):
    return min(transform(matrix, permutation) for permutation in permutations)


def enumerate_matrices(x, y):
    row_domains, column_domains = row_star.filtered_domains(x, y)
    masks = []
    for column, domain in enumerate(column_domains):
        per_row = []
        for row in range(8):
            per_value = {}
            for candidate_index, candidate in enumerate(domain):
                value = candidate[row]
                per_value[value] = per_value.get(value, 0) | (
                    1 << candidate_index
                )
            per_row.append(per_value)
        masks.append(per_row)
    order = tuple(
        sorted(range(8), key=lambda row: (len(row_domains[row]), row))
    )
    initial = tuple((1 << len(domain)) - 1 for domain in column_domains)
    rows = [None] * 8
    result = []
    nodes = 0

    def visit(position, possible_columns):
        nonlocal nodes
        nodes += 1
        if position == 8:
            result.append(tuple(rows))
            return
        row = order[position]
        for candidate in row_domains[row]:
            following = tuple(
                possible_columns[column]
                & masks[column][row].get(candidate[column], 0)
                for column in range(8)
            )
            if any(mask == 0 for mask in following):
                continue
            rows[row] = candidate
            visit(position + 1, following)
        rows[row] = None

    visit(0, initial)
    return tuple(result), nodes


def main():
    source = json.loads(INPUT.read_text(encoding="utf-8"))
    assert source["schema"] == "order100-exact-row-star-relaxation-v1"
    records = []
    for profile_index, survivor in enumerate(source["survivors"]):
        x = tuple(survivor["x"])
        y = tuple(survivor["y"])
        labelled, nodes = enumerate_matrices(x, y)
        permutations = stabilizer_permutations(x, y)
        canonical = tuple(
            sorted(
                {
                    canonical_matrix(matrix, permutations)
                    for matrix in labelled
                }
            )
        )
        records.append(
            {
                "profile_index": profile_index,
                "x": x,
                "y": y,
                "stabilizer_order": len(permutations),
                "labelled_matrices": len(labelled),
                "matrix_orbits": len(canonical),
                "search_nodes": nodes,
                "matrices": canonical,
            }
        )

    artifact = {
        "schema": "order100-row-star-matrix-orbits-v1",
        "scope_warning": (
            "Canonical incidence matrices satisfying exact row and column "
            "stars; no global rotation realization is asserted."
        ),
        "profiles": records,
    }
    canonical_text = json.dumps(
        records, sort_keys=True, separators=(",", ":")
    )
    OUTPUT.write_text(
        json.dumps(artifact, indent=2) + "\n", encoding="utf-8"
    )
    print("order-100 row-star matrix orbit census: PASS")
    print(f"profiles={len(records)}")
    print(
        "labelled_matrices="
        + ",".join(str(record["labelled_matrices"]) for record in records)
    )
    print(
        "matrix_orbits="
        + ",".join(str(record["matrix_orbits"]) for record in records)
    )
    print(
        "stabilizer_orders="
        + ",".join(str(record["stabilizer_order"]) for record in records)
    )
    print(
        "artifact_sha256="
        f"{hashlib.sha256(canonical_text.encode()).hexdigest()}"
    )
    print(
        "scope=exact simultaneous-profile-stabilizer quotient; "
        "no global rotation realization"
    )


if __name__ == "__main__":
    main()
