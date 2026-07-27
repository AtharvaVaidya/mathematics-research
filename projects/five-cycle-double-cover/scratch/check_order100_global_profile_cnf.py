#!/usr/bin/env python3
"""Independent semantic checker for the three order-100 profile CNFs.

The producer is not imported.  Cell domains, sequential counters, position
cover clauses, support clauses, and Kempe support caps are regenerated
here.  Every appended lazy clause is decoded as a set of selected cell
options and checked against the partial order-100 graph that those options
force.  The clause is accepted only if that partial graph already contains
a parallel pair or a circuit shorter than ten; the fallback for a complete
core assignment checks all 105 terminal pairings.

The LRAT proves the checked CNF UNSAT.  This program proves that the CNF's
base encoding and all its dynamically learned graph clauses are sound.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import json
from collections import deque
from pathlib import Path

import check_order100_global_orbit_cnf as independent


ROOT = Path(__file__).resolve().parents[1]
ROW_STAR = ROOT / "scratch/order100-exact-row-star-survivors.json"
PROFILES = (
    (
        (2, 2, 1, 1, 0, 0, 0, 0),
        (0, 0, 0, 0, 2, 2, 1, 1),
    ),
    (
        (2, 2, 1, 1, 0, 0, 0, 0),
        (0, 0, 1, 0, 2, 2, 1, 0),
    ),
    (
        (2, 2, 1, 1, 0, 0, 0, 0),
        (0, 0, 1, 1, 2, 2, 0, 0),
    ),
)
OFF_DIAGONAL_CAP = (
    (1, 2, 2),
    (2, 2, 2),
    (2, 2, 3),
)
DIAGONAL_CAP = (
    (1, 1, 2),
    (1, 2, 2),
    (2, 2, 2),
)


@functools.lru_cache(maxsize=None)
def local_options(x_value, y_value, diagonal):
    """Independent exhaustive position/bijection/orientation enumeration."""
    half_a = 5 + x_value
    half_b = 5 + y_value
    cap = (
        DIAGONAL_CAP if diagonal else OFF_DIAGONAL_CAP
    )[x_value][y_value]
    result = []
    for multiplicity in range(1 if diagonal else 0, cap + 1):
        if multiplicity == 0:
            result.append(((), (), (), 0))
            continue
        if diagonal:
            a_subsets = (
                (0,) + tail
                for tail in itertools.combinations(
                    range(1, half_a), multiplicity - 1
                )
            )
            b_subsets = tuple(
                (0,) + tail
                for tail in itertools.combinations(
                    range(1, half_b), multiplicity - 1
                )
            )
        else:
            a_subsets = itertools.combinations(
                range(1, half_a), multiplicity
            )
            b_subsets = tuple(
                itertools.combinations(range(1, half_b), multiplicity)
            )
        for positions_a in a_subsets:
            for positions_b in b_subsets:
                for mapping in independent.mappings(
                    multiplicity, diagonal
                ):
                    mapping = tuple(mapping)
                    for orientation in range(1 << multiplicity):
                        if diagonal and orientation & 1:
                            continue
                        if independent.pair_option_good(
                            x_value,
                            y_value,
                            diagonal,
                            tuple(positions_a),
                            tuple(positions_b),
                            mapping,
                            orientation,
                        ):
                            result.append(
                                (
                                    tuple(positions_a),
                                    tuple(positions_b),
                                    mapping,
                                    orientation,
                                )
                            )
    return tuple(result)


class Allocator:
    def __init__(self):
        self.next = 1

    def variables(self, count):
        result = tuple(range(self.next, self.next + count))
        self.next += count
        return result

    @property
    def count(self):
        return self.next - 1


def exactly_one_sequential(variables, allocator):
    variables = tuple(variables)
    assert variables
    yield variables
    if len(variables) == 1:
        return
    auxiliaries = allocator.variables(len(variables) - 1)
    yield (-variables[0], auxiliaries[0])
    for index in range(1, len(variables) - 1):
        yield (-variables[index], auxiliaries[index])
        yield (-auxiliaries[index - 1], auxiliaries[index])
        yield (-variables[index], -auxiliaries[index - 1])
    yield (-variables[-1], -auxiliaries[-1])


def encoding(profile_index):
    x, y = PROFILES[profile_index]
    cell_domains = {
        (row, column): local_options(
            x[row], y[column], row == column
        )
        for row in range(8)
        for column in range(8)
    }
    allocator = Allocator()
    option_variables = {
        cell: allocator.variables(len(domain))
        for cell, domain in cell_domains.items()
    }
    support_variables = {
        cell: allocator.variables(1)[0] for cell in cell_domains
    }
    clauses = []
    for variables in option_variables.values():
        clauses.extend(exactly_one_sequential(variables, allocator))
    for row, x_value in enumerate(x):
        for position in range(5 + x_value):
            covering = []
            for column in range(8):
                for option_index, option in enumerate(
                    cell_domains[row, column]
                ):
                    if position in option[0]:
                        covering.append(
                            option_variables[row, column][option_index]
                        )
            clauses.extend(exactly_one_sequential(covering, allocator))
    for column, y_value in enumerate(y):
        for position in range(5 + y_value):
            covering = []
            for row in range(8):
                for option_index, option in enumerate(
                    cell_domains[row, column]
                ):
                    if position in option[1]:
                        covering.append(
                            option_variables[row, column][option_index]
                        )
            clauses.extend(exactly_one_sequential(covering, allocator))
    for cell, domain in cell_domains.items():
        support = support_variables[cell]
        for option_index, option in enumerate(domain):
            variable = option_variables[cell][option_index]
            clauses.append(
                (-variable, support if option[0] else -support)
            )
    for row, x_value in enumerate(x):
        cap = (7 + x_value) // 2
        supports = [support_variables[row, column] for column in range(8)]
        clauses.extend(
            tuple(-variable for variable in forbidden)
            for forbidden in itertools.combinations(supports, cap + 1)
        )
    for column, y_value in enumerate(y):
        cap = (7 + y_value) // 2
        supports = [support_variables[row, column] for row in range(8)]
        clauses.extend(
            tuple(-variable for variable in forbidden)
            for forbidden in itertools.combinations(supports, cap + 1)
        )
    reverse = {
        variable: (cell, option_index)
        for cell, variables in option_variables.items()
        for option_index, variable in enumerate(variables)
    }
    return (
        x,
        y,
        cell_domains,
        allocator.count,
        option_variables,
        reverse,
        tuple(clauses),
    )


def fixed_graph(x):
    offsets = []
    total = 0
    for value in x:
        offsets.append(total)
        total += 5 + value
    token_count = total
    core_order = 2 * token_count
    ambient_order = core_order + len(x)
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
    for row, value in enumerate(x):
        length = 5 + value
        for position in range(length):
            token = offsets[row] + position
            following = offsets[row] + (position + 1) % length
            edges.append((2 * token + 1, 2 * following))
    return tuple(offsets), ambient_order, tuple(edges)


def forced_b_edges(x, y, cell_domains, selected):
    offsets, _ambient_order, _fixed = fixed_graph(x)
    rotations = [[None] * (5 + value) for value in y]
    twists = [[None] * (5 + value) for value in y]
    used_a_positions = set()
    for (row, column), option_index in selected.items():
        positions_a, positions_b, mapping, orientation = (
            cell_domains[row, column][option_index]
        )
        for a_position in positions_a:
            a_key = (row, a_position)
            assert a_key not in used_a_positions
            used_a_positions.add(a_key)
        for local_b, b_position in enumerate(positions_b):
            assert rotations[column][b_position] is None
            local_a = mapping[local_b]
            rotations[column][b_position] = (
                offsets[row] + positions_a[local_a]
            )
            twists[column][b_position] = orientation >> local_a & 1
    result = []
    for column, rotation in enumerate(rotations):
        for position, token in enumerate(rotation):
            following_position = (position + 1) % len(rotation)
            following = rotation[following_position]
            if token is None or following is None:
                continue
            result.append(
                (
                    2 * token + (1 - twists[column][position]),
                    2 * following + twists[column][following_position],
                )
            )
    return tuple(result)


def has_short_cycle_forced(vertex_count, fixed_edges, added_edges):
    """A short cycle must use an added edge; test only those deletions."""
    all_edges = tuple(fixed_edges) + tuple(added_edges)
    pairs = {}
    adjacency = [[] for _ in range(vertex_count)]
    for edge_id, (u, v) in enumerate(all_edges):
        pair = tuple(sorted((u, v)))
        pairs.setdefault(pair, 0)
        pairs[pair] += 1
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))
    if any(count > 1 for count in pairs.values()):
        return True
    first_added = len(fixed_edges)
    for removed in range(first_added, len(all_edges)):
        source, target = all_edges[removed]
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


def cnf_stream(path):
    stream = path.open("r", encoding="utf-8")
    header = stream.readline().split()
    assert header[:2] == ["p", "cnf"] and len(header) == 4
    variable_count, clause_count = map(int, header[2:])

    def clauses():
        observed = 0
        for line in stream:
            if not line.strip() or line.startswith("c"):
                continue
            values = tuple(map(int, line.split()))
            assert values[-1] == 0
            observed += 1
            yield values[:-1]
        assert observed == clause_count
        stream.close()

    return variable_count, clause_count, clauses()


def check_profile(profile_index, cnf_path):
    (
        x,
        y,
        cell_domains,
        expected_variables,
        option_variables,
        reverse,
        base_clauses,
    ) = encoding(profile_index)
    variable_count, clause_count, clauses = cnf_stream(cnf_path)
    assert variable_count == expected_variables
    for clause_index, expected in enumerate(base_clauses):
        observed = next(clauses)
        assert observed == expected, (clause_index, observed, expected)

    offsets, ambient_order, fixed_edges = fixed_graph(x)
    assert offsets == (0, 7, 14, 20, 26, 31, 36, 41)
    lazy_count = 0
    terminal_clauses = 0
    clause_digest = hashlib.sha256()
    for clause in clauses:
        assert clause and len(clause) == len(set(clause))
        assert all(literal < 0 and -literal in reverse for literal in clause)
        selected = {}
        for literal in clause:
            cell, option_index = reverse[-literal]
            assert cell not in selected
            selected[cell] = option_index
        added_edges = forced_b_edges(x, y, cell_domains, selected)
        if not has_short_cycle_forced(
            ambient_order, fixed_edges, added_edges
        ):
            assert set(selected) == set(cell_domains)
            core_edges = fixed_edges + added_edges
            core_order = ambient_order - len(x)
            for pairing in independent.PAIRINGS:
                terminal_edges = tuple(
                    (core_order + left, core_order + right)
                    for left, right in pairing
                )
                assert has_short_cycle_forced(
                    ambient_order, core_edges, terminal_edges
                )
            terminal_clauses += 1
        clause_digest.update(" ".join(map(str, clause)).encode())
        clause_digest.update(b"\n")
        lazy_count += 1

    assert len(base_clauses) + lazy_count == clause_count
    source = json.loads(ROW_STAR.read_text(encoding="utf-8"))
    observed_profiles = tuple(
        (tuple(record["x"]), tuple(record["y"]))
        for record in source["survivors"]
    )
    assert observed_profiles == PROFILES
    return {
        "profile": profile_index,
        "variables": variable_count,
        "clauses": clause_count,
        "base_clauses": len(base_clauses),
        "semantic_lazy_clauses": lazy_count,
        "terminal_pairing_clauses": terminal_clauses,
        "lazy_clause_sha256": clause_digest.hexdigest(),
        "cell_option_counts": {
            f"{row},{column}": len(domain)
            for (row, column), domain in cell_domains.items()
        },
        "profile_coverage": {
            "row_star_survivor_profiles": len(observed_profiles),
            "profiles_match_exactly": True,
        },
        "derived_dimensions": {
            "c_edge_tokens": sum(5 + value for value in x),
            "core_order": 2 * sum(5 + value for value in x),
            "ambient_order": ambient_order,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=int, choices=range(3), required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = check_profile(args.profile, args.cnf)
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print("order-100 global profile CNF semantic check: PASS")
    print(rendered)


if __name__ == "__main__":
    main()
