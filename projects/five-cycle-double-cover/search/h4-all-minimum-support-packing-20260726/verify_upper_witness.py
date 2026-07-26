#!/usr/bin/env python3
"""Directly verify the retained size-four H4 exact-zero-flow witness."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def graph() -> tuple[int, tuple[tuple[int, int], ...]]:
    document = json.loads((HERE / "H4.graph.json").read_text())
    rows = document["edges"]
    if [row["id"] for row in rows] != list(range(len(rows))):
        raise AssertionError("nonconsecutive edge identifiers")
    edges = tuple((int(row["u"]), int(row["v"])) for row in rows)
    vertices = 1 + max(max(edge) for edge in edges)
    incidence = [[] for _ in range(vertices)]
    seen_edges: set[tuple[int, int]] = set()
    for edge, (first, second) in enumerate(edges):
        if first == second:
            raise AssertionError("loop")
        key = tuple(sorted((first, second)))
        if key in seen_edges:
            raise AssertionError("parallel edge")
        seen_edges.add(key)
        incidence[first].append(edge)
        incidence[second].append(edge)
    if vertices != 162 or len(edges) != 243:
        raise AssertionError("unexpected H4 dimensions")
    if any(len(row) != 3 for row in incidence):
        raise AssertionError("not cubic")

    def connected_without(deleted: int) -> bool:
        reached = {0}
        todo = [0]
        while todo:
            vertex = todo.pop()
            for edge in incidence[vertex]:
                if edge == deleted:
                    continue
                first, second = edges[edge]
                neighbour = second if first == vertex else first
                if neighbour not in reached:
                    reached.add(neighbour)
                    todo.append(neighbour)
        return len(reached) == vertices

    if not connected_without(-1):
        raise AssertionError("disconnected")
    if any(not connected_without(edge) for edge in range(len(edges))):
        raise AssertionError("bridge")
    return vertices, edges


def assignment() -> dict[int, bool]:
    values: dict[int, bool] = {}
    status = None
    for raw in (HERE / "H4-minimum.model").read_text().splitlines():
        line = raw.strip()
        if line.startswith("s "):
            status = line
        elif line.startswith("v "):
            for word in line.split()[1:]:
                literal = int(word)
                if literal == 0:
                    continue
                variable = abs(literal)
                if variable in values:
                    raise AssertionError("duplicate model variable")
                values[variable] = literal > 0
    if status != "s SATISFIABLE":
        raise AssertionError("model is not SAT")
    return values


def check_cnf(values: dict[int, bool]) -> tuple[int, int]:
    variables = expected_clauses = None
    clauses = 0
    for raw in (HERE / "H4-minimum.cnf").read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            _, kind, variable_text, clause_text = line.split()
            if kind != "cnf":
                raise AssertionError("not CNF")
            variables = int(variable_text)
            expected_clauses = int(clause_text)
            continue
        words = tuple(map(int, line.split()))
        if not words or words[-1] != 0:
            raise AssertionError("unterminated clause")
        clause = words[:-1]
        if not any(values[abs(literal)] == (literal > 0)
                   for literal in clause):
            raise AssertionError(f"falsified clause {clauses + 1}")
        clauses += 1
    if variables is None or clauses != expected_clauses:
        raise AssertionError("CNF header mismatch")
    if set(values) != set(range(1, variables + 1)):
        raise AssertionError("incomplete assignment")
    return variables, clauses


def main() -> None:
    vertices, edges = graph()
    values = assignment()
    variables, clauses = check_cnf(values)
    edge_count = len(edges)

    def selected(block: int) -> set[int]:
        return {
            edge for edge in range(edge_count)
            if values[block * edge_count + edge + 1]
        }

    matching = selected(0)
    first_cycle = selected(1)
    second_cycle = selected(2)
    flow_first = selected(3)
    flow_second = selected(4)
    if matching != first_cycle & second_cycle:
        raise AssertionError("matching is not cycle intersection")
    if matching != {58, 114, 139, 210}:
        raise AssertionError("unexpected matching")
    used: set[int] = set()
    for edge in matching:
        first, second = edges[edge]
        if first in used or second in used:
            raise AssertionError("matching edges meet")
        used.update((first, second))

    incidence = [[] for _ in range(vertices)]
    for edge, (first, second) in enumerate(edges):
        incidence[first].append(edge)
        incidence[second].append(edge)

    def even(edge_set: set[int]) -> bool:
        return all(
            sum(edge in edge_set for edge in row) % 2 == 0
            for row in incidence
        )

    for edge_set in (
        first_cycle, second_cycle, flow_first, flow_second
    ):
        if not even(edge_set):
            raise AssertionError("non-Eulerian witness coordinate")
    for edge in range(edge_count):
        zero = edge not in flow_first and edge not in flow_second
        if zero != (edge in matching):
            raise AssertionError("flow zero set mismatch")

    frozen = json.loads((HERE / "H4-minimum.result.json").read_text())
    if frozen["model_check"]["matching_edges"] != sorted(matching):
        raise AssertionError("result summary mismatch")
    print(json.dumps({
        "status": "PASS",
        "vertices": vertices,
        "edges": edge_count,
        "cnf_variables": variables,
        "cnf_clauses": clauses,
        "exact_zero_matching": sorted(matching),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
