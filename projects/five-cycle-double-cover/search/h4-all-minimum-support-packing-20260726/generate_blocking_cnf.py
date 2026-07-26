#!/usr/bin/env python3
"""Reconstruct the H4 projected-support blocking CNF.

The formula has:
  * two F_2 flow bits per edge;
  * one indicator z_e equivalent to both flow bits being zero;
  * even parity for each bit at every cubic vertex;
  * clauses making the zero set a matching;
  * a Sinz sequential counter imposing at most four zero edges; and
  * one blocking clause for every support in the supplied corpus.

UNSAT therefore proves that the corpus contains every exact-zero matching
of cardinality at most four.  The separately retained at-most-three proof
establishes that cardinality four is the global minimum.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


Clause = tuple[int, ...]


def xor_even_three(a: int, b: int, c: int) -> tuple[Clause, ...]:
    return (
        (a, b, -c),
        (a, -b, c),
        (-a, b, c),
        (-a, -b, -c),
    )


def at_most(
    variables: list[int], bound: int, next_variable: int
) -> tuple[list[Clause], int]:
    count = len(variables)
    if not 0 < bound < count:
        raise AssertionError("unsupported sequential-counter dimensions")
    sequential = [
        [0] * (bound + 1) for _ in range(count - 1)
    ]
    for row in range(count - 1):
        for column in range(1, bound + 1):
            sequential[row][column] = next_variable
            next_variable += 1

    clauses: list[Clause] = [
        (-variables[0], sequential[0][1])
    ]
    for row in range(1, count - 1):
        clauses.append((-variables[row], sequential[row][1]))
        clauses.append(
            (-sequential[row - 1][1], sequential[row][1])
        )
        for column in range(2, bound + 1):
            clauses.append(
                (
                    -variables[row],
                    -sequential[row - 1][column - 1],
                    sequential[row][column],
                )
            )
            clauses.append(
                (
                    -sequential[row - 1][column],
                    sequential[row][column],
                )
            )
    for row in range(1, count):
        clauses.append(
            (-variables[row], -sequential[row - 1][bound])
        )
    return clauses, next_variable


def base_formula(
    graph_path: Path,
) -> tuple[list[Clause], list[int], int, int]:
    graph = json.loads(graph_path.read_text())
    raw_edges = graph["edges"]
    if [edge["id"] for edge in raw_edges] != list(range(len(raw_edges))):
        raise AssertionError("edge ids are not consecutive in file order")
    edges = [(int(edge["u"]), int(edge["v"])) for edge in raw_edges]
    vertices = 1 + max(max(edge) for edge in edges)
    incidence: list[list[int]] = [[] for _ in range(vertices)]
    for edge, (first, second) in enumerate(edges):
        if first == second:
            raise AssertionError("loop in H4 graph")
        incidence[first].append(edge)
        incidence[second].append(edge)
    if any(len(row) != 3 for row in incidence):
        raise AssertionError("H4 graph is not cubic")

    edge_count = len(edges)
    clauses: list[Clause] = []
    zero_variables: list[int] = []
    for edge in range(edge_count):
        first_bit = edge + 1
        second_bit = edge_count + edge + 1
        zero = 2 * edge_count + edge + 1
        zero_variables.append(zero)
        clauses.extend(
            (
                (-zero, -first_bit),
                (-zero, -second_bit),
                (zero, first_bit, second_bit),
            )
        )

    for row in incidence:
        for offset in (0, edge_count):
            clauses.extend(
                xor_even_three(
                    row[0] + offset + 1,
                    row[1] + offset + 1,
                    row[2] + offset + 1,
                )
            )
        for first in range(3):
            for second in range(first + 1, 3):
                clauses.append(
                    (-zero_variables[row[first]],
                     -zero_variables[row[second]])
                )

    counter, next_variable = at_most(
        zero_variables, 4, 3 * edge_count + 1
    )
    clauses.extend(counter)
    return clauses, zero_variables, next_variable - 1, edge_count


def support_rows(
    support_path: Path, zero_variables: list[int], edge_count: int
) -> Iterable[Clause]:
    with support_path.open() as source:
        for number, line in enumerate(source, 1):
            fields = line.split()
            if len(fields) != 4:
                raise AssertionError(
                    f"support row {number} has {len(fields)} fields"
                )
            edges = tuple(map(int, fields))
            if tuple(sorted(edges)) != edges or len(set(edges)) != 4:
                raise AssertionError(
                    f"support row {number} is not a sorted 4-set"
                )
            if not all(0 <= edge < edge_count for edge in edges):
                raise AssertionError(
                    f"support row {number} has out-of-range edge"
                )
            yield tuple(-zero_variables[edge] for edge in edges)


def count_rows(path: Path) -> int:
    with path.open("rb") as source:
        return sum(block.count(b"\n") for block in iter(
            lambda: source.read(8 * 1024 * 1024), b""
        ))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("supports", type=Path)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()

    base, zero_variables, maximum_variable, edge_count = base_formula(
        arguments.graph
    )
    rows = count_rows(arguments.supports)
    clause_count = len(base) + rows
    with arguments.output.open("w") as output:
        output.write(
            "c H4 F_2^2 exact-zero matching supports not in corpus\n"
        )
        output.write(
            "c UNSAT proves the corpus covers every support of size at most 4\n"
        )
        output.write(
            f"p cnf {maximum_variable} {clause_count}\n"
        )
        for clause in base:
            output.write(" ".join(map(str, clause)) + " 0\n")
        emitted = 0
        for clause in support_rows(
            arguments.supports, zero_variables, edge_count
        ):
            output.write(" ".join(map(str, clause)) + " 0\n")
            emitted += 1
    if emitted != rows:
        raise AssertionError(
            f"row count changed during generation: {rows} != {emitted}"
        )
    print(
        json.dumps(
            {
                "variables": maximum_variable,
                "base_clauses": len(base),
                "support_clauses": rows,
                "clauses": clause_count,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
