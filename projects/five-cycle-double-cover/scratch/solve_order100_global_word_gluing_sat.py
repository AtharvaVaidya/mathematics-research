#!/usr/bin/env python3
"""Incremental propositional version of the order-100 global gluing search.

This uses one-hot Boolean variables for row words, column words, and exact
cell bijection/orientation options.  A tiny local CaDiCaL bridge retains
learned clauses across lazy short-cycle refinements.  The mathematical
finite domain and concrete graph reconstruction are shared with
``solve_order100_global_word_gluing.py``.

SAT returns a concrete graph record.  If the accumulated formula becomes
UNSAT, ``--cnf`` freezes the exact final DIMACS instance for independent
replay.  This remains a fixed-matrix result, not an exclusion of all
matrices in the profile orbit.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import solve_order100_global_word_gluing as model


def exactly_one(variables):
    yield tuple(variables)
    for left_index, left in enumerate(variables):
        for right in variables[left_index + 1 :]:
            yield (-left, -right)


class IncrementalCadical:
    def __init__(self, executable: Path):
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
        response = self.process.stdout.readline().strip()
        if response != "ok":
            raise RuntimeError(f"incremental solver sync failed: {response}")

    def solve(self):
        self.process.stdin.write("solve\n")
        self.process.stdin.flush()
        return self.process.stdout.readline().strip()

    def values(self, variables):
        self.process.stdin.write(
            "values " + " ".join(map(str, variables)) + " 0\n"
        )
        self.process.stdin.flush()
        values = tuple(
            int(value) for value in self.process.stdout.readline().split()
        )
        if len(values) != len(variables):
            raise RuntimeError("incremental solver returned wrong value count")
        return values

    def close(self):
        if self.process.poll() is None:
            self.process.stdin.write("quit\n")
            self.process.stdin.flush()
            self.process.stdout.readline()
            self.process.wait()


def write_dimacs(path, variable_count, clauses):
    with path.open("w", encoding="utf-8") as output:
        output.write(f"p cnf {variable_count} {len(clauses)}\n")
        for clause in clauses:
            output.write(" ".join(map(str, clause)) + " 0\n")


def solve(profile_index, orbit_index, max_models, server, output, cnf):
    if orbit_index is None:
        artifact = json.loads(model.ARTIFACT.read_text(encoding="utf-8"))
        assert artifact["schema"] == "order100-exact-row-star-relaxation-v1"
        record = artifact["survivors"][profile_index]
    else:
        artifact = json.loads(
            Path("scratch/order100-row-star-matrix-orbits.json").read_text(
                encoding="utf-8"
            )
        )
        assert artifact["schema"] == "order100-row-star-matrix-orbits-v1"
        profile = artifact["profiles"][profile_index]
        record = {
            "x": profile["x"],
            "y": profile["y"],
            "matrix": profile["matrices"][orbit_index],
        }
    x, y, matrix, a_words, b_words = model.word_domains(record)
    cell_domains = model.build_cell_domains(
        x, y, matrix, a_words, b_words
    )

    next_variable = 1
    a_variables = []
    for words in a_words:
        variables = tuple(range(next_variable, next_variable + len(words)))
        next_variable += len(words)
        a_variables.append(variables)
    b_variables = []
    for words in b_words:
        variables = tuple(range(next_variable, next_variable + len(words)))
        next_variable += len(words)
        b_variables.append(variables)
    cell_variables = {}
    for cell, domain in sorted(cell_domains.items()):
        variables = tuple(range(next_variable, next_variable + len(domain)))
        next_variable += len(domain)
        cell_variables[cell] = variables
    variable_count = next_variable - 1

    clauses = []
    for variables in a_variables + b_variables:
        clauses.extend(exactly_one(variables))
    for variables in cell_variables.values():
        clauses.extend(exactly_one(variables))
    for (row, column), domain in sorted(cell_domains.items()):
        for option_index, (a_index, b_index, _mapping, _orientation) in enumerate(
            domain
        ):
            option_variable = cell_variables[row, column][option_index]
            clauses.append((-option_variable, a_variables[row][a_index]))
            clauses.append((-option_variable, b_variables[column][b_index]))

    sat = IncrementalCadical(server)
    sat.add_all(clauses)
    all_variables = tuple(range(1, variable_count + 1))
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
                    "matrix_orbit_index": orbit_index,
                    "variables": variable_count,
                    "clauses": len(clauses),
                    "models_checked": model_number - 1,
                    "core_pairing_failures": core_pairing_failures,
                    "certificate_warning": (
                        "Final CNF is replayable, but no proof object was "
                        "requested from the incremental discovery run."
                    ),
                    "word_domain_sizes": {
                        **{
                            f"A{row}": len(a_words[row])
                            for row in range(8)
                        },
                        **{
                            f"B{column}": len(b_words[column])
                            for column in range(8)
                        },
                    },
                    "cell_domain_sizes": {
                        f"{row},{column}": len(domain)
                        for (row, column), domain in cell_domains.items()
                    },
                }
                print(json.dumps(result, indent=2))
                return 20
            if status != "sat":
                raise RuntimeError(f"unexpected solver status: {status}")

            truth = sat.values(all_variables)
            true_variables = {
                variable
                for variable, value in zip(all_variables, truth)
                if value
            }
            values = {}
            for row, variables in enumerate(a_variables):
                chosen = [
                    index
                    for index, variable in enumerate(variables)
                    if variable in true_variables
                ]
                assert len(chosen) == 1
                values[f"A{row}"] = chosen[0]
            for column, variables in enumerate(b_variables):
                chosen = [
                    index
                    for index, variable in enumerate(variables)
                    if variable in true_variables
                ]
                assert len(chosen) == 1
                values[f"B{column}"] = chosen[0]
            chosen_option_variables = {}
            for (row, column), variables in cell_variables.items():
                chosen = [
                    index
                    for index, variable in enumerate(variables)
                    if variable in true_variables
                ]
                assert len(chosen) == 1
                values[f"C{row}_{column}"] = chosen[0]
                chosen_option_variables[f"C{row}_{column}"] = variables[
                    chosen[0]
                ]

            graph_edges, _rotations, _twists, _marked = model.chosen_graph(
                matrix, a_words, b_words, cell_domains, values
            )
            bad = model.defects_fast(graph_edges)
            if not bad:
                for pairing_index in range(len(model.PAIRINGS)):
                    full_edges, _r, _t, _m = model.chosen_graph(
                        matrix,
                        a_words,
                        b_words,
                        cell_domains,
                        values,
                        pairing_index,
                    )
                    if model.defects_fast(full_edges):
                        continue
                    result = model.realization_record(
                        profile_index,
                        record,
                        a_words,
                        b_words,
                        cell_domains,
                        values,
                        pairing_index,
                    )
                    rendered = json.dumps(result, indent=2)
                    if output:
                        output.write_text(rendered + "\n", encoding="utf-8")
                    print(rendered)
                    return 0
                core_pairing_failures += 1
                bad = {
                    frozenset(chosen_option_variables)
                }

            new_clauses = []
            for provenance in sorted(
                bad, key=lambda item: (len(item), sorted(item))
            ):
                clause = tuple(
                    sorted(
                        -chosen_option_variables[variable]
                        for variable in provenance
                    )
                )
                if clause in seen_nogoods:
                    continue
                seen_nogoods.add(clause)
                new_clauses.append(clause)
            if not new_clauses:
                raise RuntimeError("model had defects but produced no new clause")
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
    parser.add_argument("--orbit-index", type=int)
    parser.add_argument("--max-models", type=int, default=1_000_000)
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
            args.orbit_index,
            args.max_models,
            args.server,
            args.output,
            args.cnf,
        )
    )


if __name__ == "__main__":
    main()
