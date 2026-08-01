#!/usr/bin/env python3
"""Independent semantic checker for the order-100 fixed-matrix CNFs.

This program does not import the discovery solver.  It independently:

* regenerates every cyclic word by direct multiset enumeration;
* checks fixed-position pair kernels by weighted shortest paths;
* reconstructs the exact Boolean variable allocation and base CNF; and
* proves every added negative no-good by finding a cycle below ten in the
  partial graph fixed by that no-good (or, for a full core assignment,
  checks all 105 terminal pairings).

An LRAT checker establishes that the frozen CNF is UNSAT.  This checker
establishes that the frozen CNF is a sound encoding of the stated
fixed-matrix rotation problem.
"""

from __future__ import annotations

import argparse
import functools
import itertools
import json
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORBITS = ROOT / "scratch/order100-row-star-matrix-orbits.json"
N_MARKS = 8


def multiset_words(counts):
    counts = list(counts)
    word = [0] * sum(counts)

    def visit(position):
        if position == len(word):
            yield tuple(word)
            return
        for label in range(len(counts)):
            if counts[label] == 0:
                continue
            counts[label] -= 1
            word[position] = label
            yield from visit(position + 1)
            counts[label] += 1

    yield from visit(0)


def residual_weights(half_length, positions, diagonal):
    positions = tuple(sorted(positions))
    assert positions
    assert (positions[0] == 0) == diagonal
    gaps = tuple(
        (
            positions[(index + 1) % len(positions)] - position
        )
        % half_length
        or half_length
        for index, position in enumerate(positions)
    )
    weights = [2 * gap - 1 for gap in gaps]
    if not diagonal:
        assert positions[0] > 0 and gaps[-1] >= 2
        weights[-1] += 1
    return tuple(weights)


def weighted_girth_at_least_ten(edges):
    vertex_count = 1 + max(max(u, v) for u, v, _weight in edges)
    adjacency = [[] for _ in range(vertex_count)]
    for edge_id, (u, v, weight) in enumerate(edges):
        adjacency[u].append((v, weight, edge_id))
        adjacency[v].append((u, weight, edge_id))
    for removed, (source, target, removed_weight) in enumerate(edges):
        distance = [10**9] * vertex_count
        distance[source] = 0
        queue = [(0, source)]
        while queue:
            queue.sort(reverse=True)
            value, vertex = queue.pop()
            if value != distance[vertex] or value >= 10:
                continue
            for following, weight, edge_id in adjacency[vertex]:
                if edge_id == removed:
                    continue
                candidate = value + weight
                if candidate < distance[following]:
                    distance[following] = candidate
                    queue.append((candidate, following))
        if distance[target] + removed_weight < 10:
            return False
    return True


@functools.lru_cache(maxsize=None)
def pair_option_good(
    x_value,
    y_value,
    diagonal,
    positions_a,
    positions_b,
    mapping,
    orientation,
):
    positions_a = tuple(positions_a)
    positions_b = tuple(positions_b)
    m = len(positions_a)
    assert len(positions_b) == m and m > 0
    a_weights = residual_weights(5 + x_value, positions_a, diagonal)
    b_weights = residual_weights(5 + y_value, positions_b, diagonal)
    edges = [
        (2 * q, 2 * q + 1, 2 if diagonal and q == 0 else 1)
        for q in range(m)
    ]
    edges.extend(
        (
            2 * q + 1,
            2 * ((q + 1) % m),
            a_weights[q],
        )
        for q in range(m)
    )
    for b_index, current in enumerate(mapping):
        following = mapping[(b_index + 1) % m]
        current_reverse = orientation >> current & 1
        following_reverse = orientation >> following & 1
        edges.append(
            (
                2 * current + (0 if current_reverse else 1),
                2 * following + (1 if following_reverse else 0),
                b_weights[b_index],
            )
        )
    return weighted_girth_at_least_ten(edges)


def mappings(m, diagonal):
    if diagonal:
        yield from (
            (0,) + tail for tail in itertools.permutations(range(1, m))
        )
    else:
        yield from itertools.permutations(range(m))


@functools.lru_cache(maxsize=None)
def fixed_positions_extend(x_value, y_value, diagonal, positions_a):
    half_b = 5 + y_value
    m = len(positions_a)
    position_choices = (
        (
            (0,) + tail
            for tail in itertools.combinations(range(1, half_b), m - 1)
        )
        if diagonal
        else itertools.combinations(range(1, half_b), m)
    )
    for positions_b in position_choices:
        for mapping in mappings(m, diagonal):
            for orientation in range(1 << m):
                if diagonal and orientation & 1:
                    continue
                if pair_option_good(
                    x_value,
                    y_value,
                    diagonal,
                    tuple(positions_a),
                    tuple(positions_b),
                    tuple(mapping),
                    orientation,
                ):
                    return True
    return False


@functools.lru_cache(maxsize=None)
def all_words(own_excess, opposite_excesses, own_index, counts):
    counts = tuple(counts)
    remaining = list(counts)
    assert remaining[own_index] >= 1
    remaining[own_index] -= 1
    result = []
    for tail in multiset_words(remaining):
        word = (own_index,) + tail
        for opposite, multiplicity in enumerate(counts):
            if multiplicity <= 1:
                continue
            positions = tuple(
                position
                for position, label in enumerate(word)
                if label == opposite
            )
            if not fixed_positions_extend(
                own_excess,
                opposite_excesses[opposite],
                opposite == own_index,
                positions,
            ):
                break
        else:
            result.append(word)
    return tuple(result)


def domains(record):
    x = tuple(record["x"])
    y = tuple(record["y"])
    matrix = tuple(tuple(row) for row in record["matrix"])
    columns = tuple(
        tuple(matrix[row][column] for row in range(8))
        for column in range(8)
    )
    a_words = tuple(
        all_words(x[row], y, row, matrix[row]) for row in range(8)
    )
    b_words = tuple(
        all_words(y[column], x, column, columns[column])
        for column in range(8)
    )
    cell_domains = {}
    for row in range(8):
        for column in range(8):
            multiplicity = matrix[row][column]
            if multiplicity == 0:
                continue
            options = []
            for a_index, a_word in enumerate(a_words[row]):
                positions_a = tuple(
                    position
                    for position, label in enumerate(a_word)
                    if label == column
                )
                for b_index, b_word in enumerate(b_words[column]):
                    positions_b = tuple(
                        position
                        for position, label in enumerate(b_word)
                        if label == row
                    )
                    for mapping in mappings(multiplicity, row == column):
                        for orientation in range(1 << multiplicity):
                            if row == column and orientation & 1:
                                continue
                            mapping = tuple(mapping)
                            if pair_option_good(
                                x[row],
                                y[column],
                                row == column,
                                positions_a,
                                positions_b,
                                mapping,
                                orientation,
                            ):
                                options.append(
                                    (
                                        a_index,
                                        b_index,
                                        mapping,
                                        orientation,
                                    )
                                )
            assert options
            cell_domains[row, column] = tuple(options)
    return x, y, matrix, a_words, b_words, cell_domains


def exactly_one(variables):
    yield tuple(variables)
    for left_index, left in enumerate(variables):
        for right in variables[left_index + 1 :]:
            yield (-left, -right)


def allocation(a_words, b_words, cell_domains):
    next_variable = 1
    a_variables = []
    for words in a_words:
        group = tuple(range(next_variable, next_variable + len(words)))
        next_variable += len(words)
        a_variables.append(group)
    b_variables = []
    for words in b_words:
        group = tuple(range(next_variable, next_variable + len(words)))
        next_variable += len(words)
        b_variables.append(group)
    cell_variables = {}
    reverse = {}
    for cell, domain in sorted(cell_domains.items()):
        group = tuple(range(next_variable, next_variable + len(domain)))
        next_variable += len(domain)
        cell_variables[cell] = group
        for option_index, variable in enumerate(group):
            reverse[variable] = (cell, option_index)
    return (
        next_variable - 1,
        tuple(a_variables),
        tuple(b_variables),
        cell_variables,
        reverse,
    )


def base_clauses(a_variables, b_variables, cell_variables, cell_domains):
    for group in a_variables + b_variables:
        yield from exactly_one(group)
    for group in cell_variables.values():
        yield from exactly_one(group)
    for cell, domain in sorted(cell_domains.items()):
        row, column = cell
        for option_index, (a_index, b_index, _mapping, _orientation) in enumerate(
            domain
        ):
            variable = cell_variables[cell][option_index]
            yield (-variable, a_variables[row][a_index])
            yield (-variable, b_variables[column][b_index])


def all_pairings(items):
    if not items:
        yield ()
        return
    first = items[0]
    for position in range(1, len(items)):
        second = items[position]
        rest = items[1:position] + items[position + 1 :]
        for tail in all_pairings(rest):
            yield ((first, second),) + tail


PAIRINGS = tuple(all_pairings(tuple(range(N_MARKS))))
assert len(PAIRINGS) == 105


def partial_graph(
    x,
    matrix,
    a_words,
    b_words,
    cell_domains,
    selected,
    pairing=None,
):
    chosen_a = {}
    chosen_b = {}
    chosen_cells = {}
    for (row, column), option_index in selected.items():
        option = cell_domains[row, column][option_index]
        a_index, b_index, _mapping, _orientation = option
        assert chosen_a.setdefault(row, a_index) == a_index
        assert chosen_b.setdefault(column, b_index) == b_index
        chosen_cells[row, column] = option

    lengths = tuple(5 + value for value in x)
    offsets = []
    total = 0
    for length in lengths:
        offsets.append(total)
        total += length
    token_count = total
    core_order = 2 * token_count
    ambient_order = core_order + N_MARKS
    assert (token_count, core_order, ambient_order) == (46, 92, 100)

    marked = tuple(offsets)
    terminal_of = {
        token: core_order + index for index, token in enumerate(marked)
    }
    edges = []
    for token in range(token_count):
        if token in terminal_of:
            terminal = terminal_of[token]
            edges.append((2 * token, terminal))
            edges.append((terminal, 2 * token + 1))
        else:
            edges.append((2 * token, 2 * token + 1))
    for row, length in enumerate(lengths):
        for position in range(length):
            token = offsets[row] + position
            following = offsets[row] + (position + 1) % length
            edges.append((2 * token + 1, 2 * following))

    for column in range(8):
        if column not in chosen_b:
            continue
        b_word = b_words[column][chosen_b[column]]
        rotation = [None] * len(b_word)
        twists = [None] * len(b_word)
        for row in range(8):
            option = chosen_cells.get((row, column))
            if option is None:
                continue
            a_index, b_index, mapping, orientation = option
            assert b_index == chosen_b[column]
            a_word = a_words[row][a_index]
            positions_a = tuple(
                position
                for position, label in enumerate(a_word)
                if label == column
            )
            positions_b = tuple(
                position
                for position, label in enumerate(b_word)
                if label == row
            )
            for local_b, b_position in enumerate(positions_b):
                local_a = mapping[local_b]
                rotation[b_position] = offsets[row] + positions_a[local_a]
                twists[b_position] = orientation >> local_a & 1
        for position, token in enumerate(rotation):
            following_position = (position + 1) % len(rotation)
            following = rotation[following_position]
            if token is None or following is None:
                continue
            edges.append(
                (
                    2 * token + (1 - twists[position]),
                    2 * following + twists[following_position],
                )
            )
    if pairing is not None:
        for left, right in pairing:
            edges.append((core_order + left, core_order + right))
    return ambient_order, edges


def has_short_cycle(vertex_count, edges):
    pairs = {}
    adjacency = [[] for _ in range(vertex_count)]
    for edge_id, (u, v) in enumerate(edges):
        pair = tuple(sorted((u, v)))
        pairs.setdefault(pair, 0)
        pairs[pair] += 1
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))
    if any(count > 1 for count in pairs.values()):
        return True
    for removed, (source, target) in enumerate(edges):
        distance = [-1] * vertex_count
        distance[source] = 0
        queue = deque((source,))
        while queue:
            vertex = queue.popleft()
            if distance[vertex] >= 8:
                continue
            for following, edge_id in adjacency[vertex]:
                if edge_id == removed or distance[following] >= 0:
                    continue
                distance[following] = distance[vertex] + 1
                queue.append(following)
        if 0 <= distance[target] < 9:
            return True
    return False


def read_cnf(path):
    stream = path.open("r", encoding="utf-8")
    header = stream.readline().split()
    assert header[:2] == ["p", "cnf"] and len(header) == 4
    variables, clause_count = map(int, header[2:])

    def clauses():
        seen = 0
        for line in stream:
            if not line.strip() or line.startswith("c"):
                continue
            values = tuple(map(int, line.split()))
            assert values and values[-1] == 0
            seen += 1
            yield values[:-1]
        assert seen == clause_count
        stream.close()

    return variables, clause_count, clauses()


def check_one(profile_index, orbit_index, cnf_path):
    artifact = json.loads(ORBITS.read_text(encoding="utf-8"))
    profile = artifact["profiles"][profile_index]
    record = {
        "x": profile["x"],
        "y": profile["y"],
        "matrix": profile["matrices"][orbit_index],
    }
    x, _y, matrix, a_words, b_words, cell_domains = domains(record)
    (
        expected_variables,
        a_variables,
        b_variables,
        cell_variables,
        reverse,
    ) = allocation(a_words, b_words, cell_domains)
    variables, clause_count, clauses = read_cnf(cnf_path)
    assert variables == expected_variables

    base_count = 0
    for expected in base_clauses(
        a_variables, b_variables, cell_variables, cell_domains
    ):
        observed = next(clauses)
        assert observed == expected, (base_count, observed, expected)
        base_count += 1

    lazy_count = 0
    for clause in clauses:
        assert clause and all(literal < 0 for literal in clause)
        assert len(clause) == len(set(clause))
        selected = {}
        for literal in clause:
            variable = -literal
            assert variable in reverse
            cell, option_index = reverse[variable]
            assert cell not in selected
            selected[cell] = option_index
        order, edges = partial_graph(
            x,
            matrix,
            a_words,
            b_words,
            cell_domains,
            selected,
        )
        if not has_short_cycle(order, edges):
            assert set(selected) == set(cell_domains)
            assert all(
                has_short_cycle(
                    *partial_graph(
                        x,
                        matrix,
                        a_words,
                        b_words,
                        cell_domains,
                        selected,
                        pairing,
                    )
                )
                for pairing in PAIRINGS
            )
        lazy_count += 1
    assert base_count + lazy_count == clause_count
    return {
        "profile": profile_index,
        "orbit": orbit_index,
        "variables": variables,
        "clauses": clause_count,
        "base_clauses": base_count,
        "semantic_nogoods": lazy_count,
        "derived_dimensions": {
            "c_edge_tokens": sum(5 + value for value in x),
            "core_order": 2 * sum(5 + value for value in x),
            "ambient_order": 2 * sum(5 + value for value in x) + N_MARKS,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=int, choices=range(3), required=True)
    parser.add_argument("--orbit", type=int, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    args = parser.parse_args()
    result = check_one(args.profile, args.orbit, args.cnf)
    print("order-100 global orbit CNF semantic check: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
