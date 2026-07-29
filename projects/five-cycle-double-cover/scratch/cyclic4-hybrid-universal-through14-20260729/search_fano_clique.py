#!/usr/bin/env python3
"""Test a seven-state sufficient subrelation for universal witnesses.

The seven unordered connector triples below form a looped clique in the
common robust compatibility graph.  Hence a macro labelling in which every
connector has one of these triples is automatically matching-universal.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product
from multiprocessing import get_context
import argparse
import json
from pathlib import Path

from search_universal import (
    COMMON_UNSAFE,
    DUADS,
    common_robust,
    decode_graph6,
    incidence,
    parity_forbidding_clauses,
)


HERE = Path(__file__).resolve().parent
FANO_CLIQUE = (
    (3, 5, 24),
    (3, 9, 20),
    (3, 12, 17),
    (5, 9, 18),
    (5, 10, 17),
    (6, 9, 17),
    (6, 10, 18),
)
PATH_CORE = FANO_CLIQUE[:6]
ORDERED_ALLOWED = frozenset(
    tuple(row[index] for index in action)
    for row in FANO_CLIQUE
    for action in permutations(range(3))
)
ORDERED_FORBIDDEN = tuple(
    row
    for row in product(sorted(DUADS), repeat=3)
    if row not in ORDERED_ALLOWED
)


def solve_graph(task):
    import pycryptosat

    order, graph = task
    graph6 = graph["graph6"]
    vertices, edges = decode_graph6(graph6)
    rows = incidence(vertices, edges)
    edge_variable_count = 5 * len(edges)

    def edge_variable(edge, coordinate):
        return 5 * edge + coordinate + 1

    def junction_variable(vertex):
        return edge_variable_count + vertex + 1

    solver = pycryptosat.Solver()
    for edge in range(len(edges)):
        variables = [edge_variable(edge, c) for c in range(5)]
        for triple in combinations(variables, 3):
            solver.add_clause([-entry for entry in triple])
        for four in combinations(variables, 4):
            solver.add_clause(list(four))
    for coordinate in range(5):
        solver.add_clause([
            edge_variable(0, coordinate)
            if coordinate < 2
            else -edge_variable(0, coordinate)
        ])

    for vertex in range(vertices):
        junction = junction_variable(vertex)
        for coordinate in range(5):
            variables = [
                edge_variable(edge, coordinate)
                for edge in rows[vertex]
            ]
            for clause in parity_forbidding_clauses(variables):
                solver.add_clause([-junction, *clause])
        for word in ORDERED_FORBIDDEN:
            clause = [junction]
            for edge, label in zip(rows[vertex], word, strict=True):
                clause.extend(
                    -edge_variable(edge, coordinate)
                    for coordinate in range(5)
                    if label & (1 << coordinate)
                )
            solver.add_clause(clause)

    witnesses = []
    failures = []
    for junctions_list in graph["junction_representatives"]:
        junctions = tuple(junctions_list)
        junction_set = set(junctions)
        assumptions = [
            junction_variable(vertex)
            if vertex in junction_set
            else -junction_variable(vertex)
            for vertex in range(vertices)
        ]
        sat, model = solver.solve(assumptions)
        base = {
            "order": order,
            "graph_index": graph["graph_index"],
            "graph6": graph6,
            "girth": graph["girth"],
            "junctions": list(junctions),
        }
        if not sat:
            failures.append(base)
            continue
        labels = tuple(
            sum(
                1 << coordinate
                for coordinate in range(5)
                if model[edge_variable(edge, coordinate)]
            )
            for edge in range(len(edges))
        )
        for vertex in range(vertices):
            word = tuple(labels[edge] for edge in rows[vertex])
            if vertex in junction_set:
                if word[0] ^ word[1] ^ word[2]:
                    raise AssertionError("junction parity failure")
            elif word not in ORDERED_ALLOWED:
                raise AssertionError("connector left seven-state clique")
        base["edge_labels"] = list(labels)
        witnesses.append(base)
    return witnesses, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--path-core-only", action="store_true")
    parser.add_argument(
        "--census",
        type=Path,
        default=HERE / "census-report.json",
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    global ORDERED_ALLOWED, ORDERED_FORBIDDEN
    selected = PATH_CORE if arguments.path_core_only else FANO_CLIQUE
    ORDERED_ALLOWED = frozenset(
        tuple(row[index] for index in action)
        for row in selected
        for action in permutations(range(3))
    )
    ORDERED_FORBIDDEN = tuple(
        row
        for row in product(sorted(DUADS), repeat=3)
        if row not in ORDERED_ALLOWED
    )
    if (
        len(COMMON_UNSAFE) != 10540
        or len(ORDERED_ALLOWED) != 6 * len(selected)
        or len(ORDERED_FORBIDDEN) != 1000 - 6 * len(selected)
        or not all(
            common_robust(left + right)
            for left in selected
            for right in selected
        )
    ):
        raise AssertionError("seven-state common-robust clique changed")
    census = json.loads(arguments.census.read_text(encoding="ascii"))
    tasks = [
        (int(order), graph)
        for order, row in census["orders"].items()
        for graph in row["graphs"]
    ]
    if arguments.workers == 1:
        results = list(map(solve_graph, tasks))
    else:
        with get_context("fork").Pool(arguments.workers) as pool:
            results = list(pool.imap_unordered(
                solve_graph, tasks, chunksize=1
            ))
    witnesses = [row for left, _ in results for row in left]
    failures = [row for _, right in results for row in right]
    witnesses.sort(
        key=lambda row: (
            row["order"],
            row["graph_index"],
            row["junctions"],
        )
    )
    failures.sort(
        key=lambda row: (
            row["order"],
            row["graph_index"],
            row["junctions"],
        )
    )
    label = "path_core" if arguments.path_core_only else "seven_state"
    statuses = Counter(
        [f"{label}_safe_sat"] * len(witnesses)
        + [f"{label}_ansatz_unsat"] * len(failures)
    )
    report = {
        "schema": f"cubic-hybrid-{label}-through14-v1",
        "scope": (
            "sufficient subrelation for matching-universal common-robust "
            "witnesses; subrelation UNSAT is not macro UNSAT"
        ),
        "selected_connector_states": [list(row) for row in selected],
        "statuses": dict(statuses),
        "witnesses": witnesses,
        "failures": failures,
    }
    output = arguments.output or HERE / (
        "path-core-report.json"
        if arguments.path_core_only
        else "fano-clique-report.json"
    )
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(json.dumps({
        "statuses": dict(statuses),
        "failure_orders": dict(Counter(
            row["order"] for row in failures
        )),
        "girth5_failures": sum(row["girth"] >= 5 for row in failures),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
