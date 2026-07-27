#!/usr/bin/env python3
"""Exact profile-level global gluing SAT model at order 100.

For one of the three surviving aligned excess profiles, every incidence
cell chooses one option

    (A-position subset, B-position subset, bijection, orientations).

The option domains include the empty off-diagonal choice and every
nonempty choice whose exact weighted two-circuit kernel has girth at least
ten.  Exact position-cover constraints induce the incidence matrix rather
than fixing one in advance.  Kempe support bounds are encoded separately.

The selected options reconstruct all 46 labelled c-edges and every B-edge
of G-M.  Lazy no-goods exclude concrete short circuits.  A core of girth
at least ten triggers an exact check of all 105 terminal pairings.

Thus SAT produces a concrete order-100 rotation realization.  UNSAT covers
all incidence matrices and rotations in the selected profile alignment.
The final CNF can be frozen for certificate production.
"""

from __future__ import annotations

import argparse
import functools
import itertools
import json
import subprocess
import sys
from pathlib import Path

import solve_order100_global_word_gluing as geometry


PROFILES = geometry.ORDER100_PROFILES if hasattr(geometry, "ORDER100_PROFILES") else (
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
def local_options(x_value: int, y_value: int, diagonal: bool):
    """Enumerate every exact cell geometry for one excess pair."""
    half_a = 5 + x_value
    half_b = 5 + y_value
    cap = (
        DIAGONAL_CAP if diagonal else OFF_DIAGONAL_CAP
    )[x_value][y_value]
    result = []
    minimum = 1 if diagonal else 0
    for multiplicity in range(minimum, cap + 1):
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
                if diagonal:
                    mappings = (
                        (0,) + tail
                        for tail in itertools.permutations(
                            range(1, multiplicity)
                        )
                    )
                else:
                    mappings = itertools.permutations(range(multiplicity))
                for mapping in mappings:
                    for orientation in range(1 << multiplicity):
                        # Reversing the undirected B-circuit gives the same
                        # graph with all traversal bits complemented.  Fix its
                        # marked connection's bit to zero.
                        if diagonal and orientation & 1:
                            continue
                        if not geometry.pair_option_is_good(
                            x_value,
                            y_value,
                            diagonal,
                            positions_a,
                            positions_b,
                            mapping,
                            orientation,
                        ):
                            continue
                        result.append(
                            (
                                tuple(positions_a),
                                tuple(positions_b),
                                tuple(mapping),
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
    """Linear-size Sinz encoding plus the at-least-one clause."""
    variables = tuple(variables)
    assert variables
    clauses = [variables]
    if len(variables) == 1:
        return clauses
    auxiliaries = allocator.variables(len(variables) - 1)
    clauses.append((-variables[0], auxiliaries[0]))
    for index in range(1, len(variables) - 1):
        clauses.extend(
            (
                (-variables[index], auxiliaries[index]),
                (-auxiliaries[index - 1], auxiliaries[index]),
                (-variables[index], -auxiliaries[index - 1]),
            )
        )
    clauses.append((-variables[-1], -auxiliaries[-1]))
    return clauses


class IncrementalCadical:
    def __init__(self, executable):
        self.process = subprocess.Popen(
            [str(executable)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        assert self.process.stdin is not None
        assert self.process.stdout is not None

    def add_all(self, clauses):
        for clause in clauses:
            self.process.stdin.write(
                "add " + " ".join(map(str, clause)) + " 0\n"
            )
        self.process.stdin.write("sync\n")
        self.process.stdin.flush()
        assert self.process.stdout.readline().strip() == "ok"

    def solve(self):
        self.process.stdin.write("solve\n")
        self.process.stdin.flush()
        return self.process.stdout.readline().strip()

    def values(self, variables):
        self.process.stdin.write(
            "values " + " ".join(map(str, variables)) + " 0\n"
        )
        self.process.stdin.flush()
        result = tuple(
            int(value) for value in self.process.stdout.readline().split()
        )
        assert len(result) == len(variables)
        return result

    def close(self):
        if self.process.poll() is None:
            self.process.stdin.write("quit\n")
            self.process.stdin.flush()
            self.process.stdout.readline()
            self.process.wait()


def graph_from_options(x, y, cell_domains, selected, pairing_index=None):
    offsets = []
    total = 0
    for value in x:
        offsets.append(total)
        total += 5 + value
    token_count = total
    core_order = 2 * token_count
    ambient_order = core_order + len(x)
    assert token_count == 46
    assert core_order == 92
    assert ambient_order == 100
    marked_tokens = tuple(offsets[row] for row in range(8))
    terminal_of = {
        token: core_order + index
        for index, token in enumerate(marked_tokens)
    }
    graph_edges = []

    for token in range(token_count):
        if token in terminal_of:
            terminal = terminal_of[token]
            graph_edges.append((2 * token, terminal, frozenset()))
            graph_edges.append((terminal, 2 * token + 1, frozenset()))
        else:
            graph_edges.append((2 * token, 2 * token + 1, frozenset()))

    for row, x_value in enumerate(x):
        length = 5 + x_value
        for position in range(length):
            token = offsets[row] + position
            following = offsets[row] + (position + 1) % length
            graph_edges.append(
                (2 * token + 1, 2 * following, frozenset())
            )

    rotations = [[None] * (5 + value) for value in y]
    twists = {}
    sources = {}
    for row in range(8):
        for column in range(8):
            variable = f"C{row}_{column}"
            option = cell_domains[row, column][selected[row, column]]
            positions_a, positions_b, mapping, orientation = option
            for local_b, b_position in enumerate(positions_b):
                local_a = mapping[local_b]
                token = offsets[row] + positions_a[local_a]
                assert rotations[column][b_position] is None
                rotations[column][b_position] = token
                twists[token] = orientation >> local_a & 1
                sources[token] = variable
    assert all(
        all(token is not None for token in rotation)
        for rotation in rotations
    )
    assert len(twists) == 46 and len(sources) == 46

    for rotation in rotations:
        for position, token in enumerate(rotation):
            following = rotation[(position + 1) % len(rotation)]
            provenance = frozenset((sources[token], sources[following]))
            graph_edges.append(
                (
                    2 * token + (1 - twists[token]),
                    2 * following + twists[following],
                    provenance,
                )
            )

    if pairing_index is not None:
        for left, right in geometry.PAIRINGS[pairing_index]:
            graph_edges.append(
                (
                    core_order + left,
                    core_order + right,
                    frozenset(("P",)),
                )
            )
        assert len(graph_edges) == 3 * ambient_order // 2
    else:
        assert len(graph_edges) == 3 * ambient_order // 2 - len(x) // 2
    return graph_edges


def write_dimacs(path, variable_count, clauses):
    with path.open("w", encoding="utf-8") as output:
        output.write(f"p cnf {variable_count} {len(clauses)}\n")
        for clause in clauses:
            output.write(" ".join(map(str, clause)) + " 0\n")


def solve(profile_index, max_models, server, output, cnf):
    x, y = PROFILES[profile_index]
    cell_domains = {
        (row, column): local_options(
            x[row], y[column], row == column
        )
        for row in range(8)
        for column in range(8)
    }
    assert all(cell_domains.values())

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

    # Every A and B c-position occurs in exactly one selected cell option.
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

    # Link support bits to the unique selected empty/nonempty cell option.
    for cell, domain in cell_domains.items():
        support = support_variables[cell]
        for option_index, option in enumerate(domain):
            option_variable = option_variables[cell][option_index]
            nonempty = bool(option[0])
            clauses.append(
                (-option_variable, support if nonempty else -support)
            )

    # Kempe support caps.  Eight cells make the direct combination encoding
    # smaller and easier to audit than introducing another counter.
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

    variable_count = allocator.count
    sat = IncrementalCadical(server)
    sat.add_all(clauses)
    queried_variables = tuple(
        variable
        for cell in sorted(option_variables)
        for variable in option_variables[cell]
    )
    seen_nogoods = set()
    core_pairing_failures = 0

    try:
        for model_number in range(1, max_models + 1):
            status = sat.solve()
            if status == "unsat":
                if cnf:
                    write_dimacs(cnf, variable_count, clauses)
                result = {
                    "status": "UNSAT",
                    "profile_index": profile_index,
                    "variables": variable_count,
                    "clauses": len(clauses),
                    "models_checked": model_number - 1,
                    "core_pairing_failures": core_pairing_failures,
                    "graph_dimensions": {
                        "c_edge_tokens": sum(5 + value for value in x),
                        "core_order": 2 * sum(5 + value for value in x),
                        "ambient_order": (
                            2 * sum(5 + value for value in x) + len(x)
                        ),
                    },
                    "cell_option_counts": {
                        f"{row},{column}": len(domain)
                        for (row, column), domain in cell_domains.items()
                    },
                    "certificate_warning": (
                        "Final CNF is replayable, but no proof object was "
                        "requested from the incremental discovery run."
                    ),
                }
                print(json.dumps(result, indent=2))
                return 20
            if status != "sat":
                raise RuntimeError(f"unexpected solver status: {status}")

            truth = sat.values(queried_variables)
            true_variables = {
                variable
                for variable, value in zip(queried_variables, truth)
                if value
            }
            selected = {}
            selected_option_variables = {}
            for cell, variables in option_variables.items():
                chosen = [
                    index
                    for index, variable in enumerate(variables)
                    if variable in true_variables
                ]
                assert len(chosen) == 1
                selected[cell] = chosen[0]
                selected_option_variables[
                    f"C{cell[0]}_{cell[1]}"
                ] = variables[chosen[0]]

            graph_edges = graph_from_options(
                x, y, cell_domains, selected
            )
            bad = geometry.defects_fast(graph_edges)
            if not bad:
                for pairing_index in range(len(geometry.PAIRINGS)):
                    full_edges = graph_from_options(
                        x,
                        y,
                        cell_domains,
                        selected,
                        pairing_index,
                    )
                    if geometry.defects_fast(full_edges):
                        continue
                    record = {
                        "schema": "order100-global-profile-realization-v1",
                        "scope_warning": (
                            "Concrete girth-ten rotation realization in one "
                            "profile; universal separation and five-CDC are "
                            "not asserted."
                        ),
                        "profile_index": profile_index,
                        "x": x,
                        "y": y,
                        "selected_cell_options": selected,
                        "pairing_index": pairing_index,
                        "terminal_pairing": geometry.PAIRINGS[pairing_index],
                        "graph_order": (
                            2 * sum(5 + value for value in x) + len(x)
                        ),
                        "graph_edges": [
                            {"u": left, "v": right}
                            for left, right, _source in full_edges
                        ],
                    }
                    rendered = json.dumps(record, indent=2)
                    if output:
                        output.write_text(rendered + "\n", encoding="utf-8")
                    print(rendered)
                    return 0
                core_pairing_failures += 1
                bad = {frozenset(selected_option_variables)}

            new_clauses = []
            for provenance in sorted(
                bad, key=lambda item: (len(item), sorted(item))
            ):
                clause = tuple(
                    sorted(
                        -selected_option_variables[variable]
                        for variable in provenance
                    )
                )
                if clause in seen_nogoods:
                    continue
                seen_nogoods.add(clause)
                new_clauses.append(clause)
            if not new_clauses:
                raise RuntimeError("defective model produced no new clause")
            clauses.extend(new_clauses)
            sat.add_all(new_clauses)
            if model_number == 1 or model_number % 100 == 0:
                print(
                    f"models={model_number} new_clauses={len(new_clauses)} "
                    f"clauses={len(clauses)} core_pairing_failures="
                    f"{core_pairing_failures}",
                    file=sys.stderr,
                    flush=True,
                )
    finally:
        sat.close()

    if cnf:
        write_dimacs(cnf, variable_count, clauses)
    print(
        f"UNKNOWN iteration limit models={max_models} clauses={len(clauses)}",
        file=sys.stderr,
    )
    return 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=int, choices=range(3), required=True)
    parser.add_argument("--max-models", type=int, default=10_000_000)
    parser.add_argument(
        "--server",
        type=Path,
        default=Path("/tmp/cadical_incremental_server"),
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--cnf", type=Path)
    args = parser.parse_args()
    raise SystemExit(
        solve(
            args.profile,
            args.max_models,
            args.server,
            args.output,
            args.cnf,
        )
    )


if __name__ == "__main__":
    main()
