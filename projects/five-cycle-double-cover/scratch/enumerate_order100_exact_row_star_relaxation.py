#!/usr/bin/env python3
"""Exact weighted-kernel row-star strengthening at order 100.

For each incidence row, this program asks whether its c-edge positions can
be partitioned among the opposite factor circuits so that every individual
two-circuit union has weighted girth at least ten.  The same test is imposed
on every column.  Pair feasibility is decided by a complete enumeration of
the three-perfect-matching kernel, including the exact placement of the
private marked edge.

The join is solver-free and exhausts all 1002 simultaneous-S8 profile
orbits.  Surviving matrices are still only local row/column objects; the
chosen row stars need not glue to one global cubic rotation system.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import json
from pathlib import Path

import enumerate_order100_incidence_relaxation as baseline


def positive_compositions(total: int, parts: int):
    current = [0] * parts

    def visit(position: int, remaining: int):
        if position == parts - 1:
            if remaining >= 1:
                current[position] = remaining
                yield tuple(current)
            return
        for value in range(1, remaining - (parts - position - 1) + 1):
            current[position] = value
            yield from visit(position + 1, remaining - value)

    yield from visit(0, total)


def weighted_girth_at_least_ten(edges):
    """Test every weighted multigraph circuit by edge deletion."""
    vertices = 1 + max(max(left, right) for left, right, _weight in edges)
    adjacency = [[] for _ in range(vertices)]
    for edge_id, (left, right, weight) in enumerate(edges):
        adjacency[left].append((right, weight, edge_id))
        adjacency[right].append((left, weight, edge_id))

    for removed, (source, target, edge_weight) in enumerate(edges):
        distance = [10**9] * vertices
        distance[source] = 0
        unseen = set(range(vertices))
        while unseen:
            vertex = min(unseen, key=lambda item: distance[item])
            unseen.remove(vertex)
            if distance[vertex] >= 10:
                break
            for following, weight, edge_id in adjacency[vertex]:
                if edge_id == removed:
                    continue
                candidate = distance[vertex] + weight
                if candidate < distance[following]:
                    distance[following] = candidate
        if distance[target] + edge_weight < 10:
            return False
    return True


@functools.lru_cache(maxsize=None)
def opposite_path_matchings(half_length: int, multiplicity: int, diagonal: bool):
    """Enumerate every exact residual matching on labelled common ends."""
    m = multiplicity
    q_indices = tuple(range(m))
    orders = (
        (0,) + tail
        for tail in itertools.permutations(q_indices[1:])
    )
    if diagonal:
        weight_sequences = tuple(
            tuple(2 * part - 1 for part in composition)
            for composition in positive_compositions(half_length, m)
        )
    else:
        sequences = set()
        for composition in positive_compositions(half_length, m):
            for marked_gap in range(m):
                if composition[marked_gap] < 2:
                    continue
                sequences.add(
                    tuple(
                        2 * part if index == marked_gap else 2 * part - 1
                        for index, part in enumerate(composition)
                    )
                )
        weight_sequences = tuple(sorted(sequences))

    result = set()
    for order in orders:
        for orientations in itertools.product((0, 1), repeat=m):
            entry = {
                edge: 2 * edge + orientations[edge] for edge in q_indices
            }
            exit_end = {
                edge: 2 * edge + (1 - orientations[edge])
                for edge in q_indices
            }
            for weights in weight_sequences:
                matching = []
                for position, edge in enumerate(order):
                    following = order[(position + 1) % m]
                    matching.append(
                        tuple(
                            sorted((exit_end[edge], entry[following]))
                        )
                        + (weights[position],)
                    )
                result.add(tuple(sorted(matching)))
    return tuple(sorted(result))


@functools.lru_cache(maxsize=None)
def pair_subset_feasible(
    own_excess: int,
    opposite_excess: int,
    diagonal: bool,
    subset: tuple[int, ...],
):
    """Decide one fixed set of shared positions by complete kernel search."""
    a = 5 + own_excess
    b = 5 + opposite_excess
    shared = tuple(sorted(subset))
    m = len(shared)
    if m == 0:
        return False
    if diagonal != (0 in shared):
        return False

    q_edges = []
    for q_index, position in enumerate(shared):
        q_weight = 2 if diagonal and position == 0 else 1
        q_edges.append((2 * q_index, 2 * q_index + 1, q_weight))

    a_paths = []
    for q_index, position in enumerate(shared):
        next_index = (q_index + 1) % m
        following = shared[next_index]
        gap = (following - position) % a
        if gap == 0:
            gap = a
        weight = 2 * gap - 1
        if not diagonal:
            interior_positions = {
                (position + step) % a for step in range(1, gap)
            }
            if 0 in interior_positions:
                weight += 1
        a_paths.append(
            (2 * q_index + 1, 2 * next_index, weight)
        )

    for b_paths in opposite_path_matchings(b, m, diagonal):
        if weighted_girth_at_least_ten(q_edges + a_paths + list(b_paths)):
            return True
    return False


@functools.lru_cache(maxsize=None)
def allowed_subsets(
    own_excess: int,
    opposite_excess: int,
    diagonal: bool,
    multiplicity: int,
):
    """List all fixed-position subsets admitting the opposite circuit."""
    positions = range(5 + own_excess)
    result = []
    for subset in itertools.combinations(positions, multiplicity):
        if diagonal != (0 in subset):
            continue
        if pair_subset_feasible(
            own_excess, opposite_excess, diagonal, subset
        ):
            result.append(subset)
    return tuple(result)


@functools.lru_cache(maxsize=None)
def row_star_witness(
    own_excess: int,
    opposite_excesses: tuple[int, ...],
    own_index: int,
    counts: tuple[int, ...],
):
    """Partition every c-position into exact pair-feasible subsets."""
    if sum(counts) != 5 + own_excess or counts[own_index] < 1:
        return None
    cells = []
    for opposite, multiplicity in enumerate(counts):
        if multiplicity == 0:
            continue
        options = allowed_subsets(
            own_excess,
            opposite_excesses[opposite],
            opposite == own_index,
            multiplicity,
        )
        if not options:
            return None
        cells.append((len(options), opposite, options))
    cells.sort()

    full = (1 << (5 + own_excess)) - 1

    def visit(position, used, chosen):
        if position == len(cells):
            return chosen if used == full else None
        _size, opposite, options = cells[position]
        for subset in options:
            bits = sum(1 << value for value in subset)
            if bits & used:
                continue
            found = visit(
                position + 1,
                used | bits,
                chosen + ((opposite, subset),),
            )
            if found is not None:
                return found
        return None

    return visit(0, 0, ())


def filtered_domains(x, y):
    row_domains = []
    for row in range(8):
        row_domains.append(
            tuple(
                candidate
                for candidate in baseline.make_row_candidates(x, y, row)
                if row_star_witness(x[row], y, row, candidate) is not None
            )
        )
    column_domains = []
    for column in range(8):
        column_domains.append(
            tuple(
                candidate
                for candidate in baseline.make_row_candidates(y, x, column)
                if row_star_witness(
                    y[column], x, column, candidate
                ) is not None
            )
        )
    return tuple(row_domains), tuple(column_domains)


def first_matrix(x, y):
    """Join exact row and column star domains by bit-mask propagation."""
    row_domains, column_domains = filtered_domains(x, y)
    if any(not domain for domain in row_domains + column_domains):
        return None, 0

    match_masks = []
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
        match_masks.append(per_row)

    row_order = tuple(
        sorted(range(8), key=lambda row: (len(row_domains[row]), row))
    )
    initial = tuple((1 << len(domain)) - 1 for domain in column_domains)
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
            following = tuple(
                possible_columns[column]
                & match_masks[column][row].get(candidate[column], 0)
                for column in range(8)
            )
            if any(mask == 0 for mask in following):
                continue
            tail = visit(position + 1, following)
            if tail is not None:
                return ((row, candidate),) + tail
        memo.add(key)
        return None

    selected = visit(0, initial)
    if selected is None:
        return None, nodes
    matrix = [None] * 8
    for row, candidate in selected:
        matrix[row] = candidate
    return tuple(matrix), nodes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--baseline-json",
        type=Path,
        help=(
            "optional canonical baseline artifact; profiles already proved "
            "infeasible there are skipped"
        ),
    )
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()
    baseline_feasible = None
    if args.baseline_json:
        artifact = json.loads(args.baseline_json.read_text(encoding="utf-8"))
        assert artifact["schema"] == "order100-all-marked-incidence-relaxation-v1"
        assert len(artifact["records"]) == 1002
        baseline_feasible = {
            (tuple(record["x"]), tuple(record["y"]))
            for record in artifact["records"]
            if record["feasible"]
        }
        assert len(baseline_feasible) == 155

    records = []
    survivors = []
    total_nodes = 0
    for x, y in baseline.canonical_profile_pairs():
        if baseline_feasible is not None and (x, y) not in baseline_feasible:
            matrix, nodes = None, 0
        else:
            matrix, nodes = first_matrix(x, y)
        total_nodes += nodes
        records.append(
            {"x": x, "y": y, "feasible": matrix is not None, "nodes": nodes}
        )
        if matrix is not None:
            columns = tuple(
                tuple(matrix[row][column] for row in range(8))
                for column in range(8)
            )
            survivors.append(
                {
                    "x": x,
                    "y": y,
                    "matrix": matrix,
                    "row_stars": tuple(
                        row_star_witness(x[row], y, row, matrix[row])
                        for row in range(8)
                    ),
                    "column_stars": tuple(
                        row_star_witness(
                            y[column], x, column, columns[column]
                        )
                        for column in range(8)
                    ),
                }
            )

    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    witness_text = json.dumps(
        survivors, sort_keys=True, separators=(",", ":")
    )
    artifact = {
        "schema": "order100-exact-row-star-relaxation-v1",
        "scope_warning": (
            "Exact pair-kernel row and column stars only; their local "
            "position choices need not glue to one global cubic graph."
        ),
        "records": records,
        "survivors": survivors,
    }
    if args.output_json:
        args.output_json.write_text(
            json.dumps(artifact, indent=2) + "\n", encoding="utf-8"
        )
    print("order-100 exact row-star incidence relaxation: PASS")
    print(f"canonical_profile_pairs={len(records)}")
    print(f"surviving_profiles={len(survivors)}")
    print(f"total_search_nodes={total_nodes}")
    print(f"pair_subset_queries={pair_subset_feasible.cache_info().misses}")
    print(
        "census_sha256="
        f"{hashlib.sha256(canonical.encode()).hexdigest()}"
    )
    print(
        "survivor_sha256="
        f"{hashlib.sha256(witness_text.encode()).hexdigest()}"
    )
    print(
        "scope=exact pair-kernel row/column-star relaxation; first matrix "
        "per profile; no global graph realization"
    )
    if survivors:
        print("canonical_frontier_survivor=")
        print(json.dumps(survivors[0], indent=2))


if __name__ == "__main__":
    main()
