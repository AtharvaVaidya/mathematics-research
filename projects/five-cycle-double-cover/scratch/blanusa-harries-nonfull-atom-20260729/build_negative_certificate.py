#!/usr/bin/env python3
"""Build one CNF/LRAT certificate for all 16 negative boundary orbits.

The CNF has one selector per negative S5-orbit representative.  At least one
selector is true, and selector j conditionally fixes the six boundary duads
to representative j.  Thus the CNF is satisfiable exactly when at least one
listed boundary word extends to the 16-vertex six-pole.
"""

from __future__ import annotations

from itertools import combinations, product
import argparse
import json
from pathlib import Path
import shutil
import subprocess


def read_pole(path: Path):
    tokens = [int(token) for token in path.read_text(encoding="ascii").split()]
    vertices, edge_count, port_count = tokens[:3]
    if (vertices, edge_count, port_count) != (16, 21, 6):
        raise AssertionError("unexpected pole dimensions")
    ports = tokens[3:9]
    edge_tokens = tokens[9:]
    if len(edge_tokens) != 2 * edge_count:
        raise AssertionError("wrong edge count")
    edges = [
        (edge_tokens[2 * edge], edge_tokens[2 * edge + 1])
        for edge in range(edge_count)
    ]
    return vertices, ports, edges


def variable(edge: int, coordinate: int) -> int:
    return 1 + 5 * edge + coordinate


def blocking_clause(
    variables: list[int],
    assignment: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(
        -entry if bit else entry
        for entry, bit in zip(variables, assignment, strict=True)
    )


def parity_clauses(
    variables: list[int],
    target: int,
) -> list[tuple[int, ...]]:
    return [
        blocking_clause(variables, assignment)
        for assignment in product((0, 1), repeat=len(variables))
        if sum(assignment) % 2 != target
    ]


def build_formula(pole: Path, relation: Path):
    vertices, ports, edges = read_pole(pole)
    rows = [
        json.loads(line)
        for line in relation.read_text(encoding="ascii").splitlines()
    ]
    negative = [
        {
            "orbit": row["orbit"],
            "boundary": row["boundary"],
        }
        for row in rows
        if row["status"] == "UNSAT_UNCERTIFIED"
    ]
    if len(negative) != 16:
        raise AssertionError("expected exactly 16 negative rows")

    incident = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        incident[left].append(edge)
        incident[right].append(edge)
    port_index = {vertex: index for index, vertex in enumerate(ports)}
    if len(port_index) != 6:
        raise AssertionError("ports are not distinct")
    if any(
        len(row) != (2 if vertex in port_index else 3)
        for vertex, row in enumerate(incident)
    ):
        raise AssertionError("wrong six-pole degrees")

    clauses = []
    for edge in range(len(edges)):
        variables = [variable(edge, coordinate) for coordinate in range(5)]
        # At most two true coordinates.
        clauses.extend(
            tuple(-variables[coordinate] for coordinate in triple)
            for triple in combinations(range(5), 3)
        )
        # At least two true coordinates.
        clauses.extend(
            tuple(variables[coordinate] for coordinate in four)
            for four in combinations(range(5), 4)
        )

    # The ten ordinary cubic vertices have unconditional even parity.
    for vertex, row in enumerate(incident):
        if vertex in port_index:
            continue
        for coordinate in range(5):
            clauses.extend(parity_clauses(
                [variable(edge, coordinate) for edge in row],
                0,
            ))

    selectors = [
        5 * len(edges) + 1 + index
        for index in range(len(negative))
    ]
    clauses.append(tuple(selectors))
    # At each port the xor of the two internal labels equals the fixed
    # dangling boundary label.  Each pair of parity clauses is conditional
    # on the corresponding boundary selector.
    for selector, record in zip(selectors, negative, strict=True):
        boundary = record["boundary"]
        for vertex in ports:
            port = port_index[vertex]
            row = incident[vertex]
            for coordinate in range(5):
                target = (boundary[port] >> coordinate) & 1
                for clause in parity_clauses(
                    [variable(edge, coordinate) for edge in row],
                    target,
                ):
                    clauses.append((-selector, *clause))

    return 5 * len(edges) + len(selectors), clauses, negative


def render_cnf(path: Path, variables: int, clauses, negative) -> None:
    with path.open("w", encoding="ascii") as output:
        output.write(
            "c disjunction of the 16 negative Blanusa six-pole "
            "boundary instances\n"
        )
        for index, record in enumerate(negative):
            output.write(
                f"c selector {106 + index} orbit {record['orbit']} "
                f"boundary {' '.join(map(str, record['boundary']))}\n"
            )
        output.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            output.write(" ".join(map(str, clause)) + " 0\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prove", action="store_true")
    parser.add_argument("--pole", type=Path, default=Path("small-pole.txt"))
    parser.add_argument(
        "--relation",
        type=Path,
        default=Path("boundary-relation.jsonl"),
    )
    parser.add_argument(
        "--cnf",
        type=Path,
        default=Path("negative-boundary-orbits.cnf"),
    )
    parser.add_argument(
        "--lrat",
        type=Path,
        default=Path("negative-boundary-orbits.lrat"),
    )
    parser.add_argument(
        "--negative",
        type=Path,
        default=Path("negative-boundary-orbits.json"),
    )
    arguments = parser.parse_args()
    variables, clauses, negative = build_formula(
        arguments.pole,
        arguments.relation,
    )
    render_cnf(arguments.cnf, variables, clauses, negative)
    arguments.negative.write_text(
        json.dumps(
            {
                "schema": "blanusa-sixpole-negative-s5-orbits-v1",
                "negative_s5_orbits": negative,
            },
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="ascii",
    )
    if arguments.prove:
        cadical = shutil.which("cadical")
        if cadical is None:
            raise AssertionError("cadical not found")
        completed = subprocess.run([
            cadical,
            "-q",
            "--seed=0",
            "--lrat",
            "--no-binary",
            str(arguments.cnf),
            str(arguments.lrat),
        ])
        if completed.returncode != 20:
            raise AssertionError(
                f"CaDiCaL returned {completed.returncode}, not UNSAT"
            )
    print(json.dumps({
        "clauses": len(clauses),
        "negative_orbits": len(negative),
        "variables": variables,
    }, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
