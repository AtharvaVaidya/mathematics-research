#!/usr/bin/env python3
"""Search retained four-mark rows for an exact Ozeki-P4 failure.

Input rows are the JSON-lines witnesses emitted by
``tait_all_coloring_mark_separation`` with the marked cyclic-cut filter.
Thus this is a candidate finder, not an independent checker of those two
producer-side hypotheses.

For every unmarked edge f such that L-f is bridgeless and for which some
Tait colouring gives all four marks one colour and f another, subdivide
the marks in L-f.  For each endpoint w of a marked edge, ask whether
deleting w leaves a simple path through all four subdivision terminals.
The singleton terminal is forced to be one endpoint of such a path.

Path existence is encoded independently as an ordered simple-vertex
sequence and decided by CaDiCaL.  An UNSAT result is an exact finite
P4 failure (though this search script does not request a proof trace).
"""

from __future__ import annotations

import argparse
from collections import deque
import json
import os
import subprocess
import sys
import tempfile

from analyze_rooted_four_mark_batch import incidence, parse_graph6
from search_rooted_subcubic_linkage_counterexample import (
    deletion_is_bridgeless,
    tait_colourings,
)


def subdivide_marks_after_root_deletion(
    order: int,
    edges: list[tuple[int, int]],
    marks: tuple[int, ...],
    root: int,
) -> tuple[int, list[tuple[int, int]], tuple[int, ...]]:
    mark_set = set(marks)
    new_edges = [
        edge
        for edge_id, edge in enumerate(edges)
        if edge_id != root and edge_id not in mark_set
    ]
    terminals = []
    for index, mark_id in enumerate(marks):
        terminal = order + index
        terminals.append(terminal)
        left, right = edges[mark_id]
        new_edges.extend(((left, terminal), (right, terminal)))
    return order + len(marks), new_edges, tuple(terminals)


def path_cnf(
    order: int,
    edges: list[tuple[int, int]],
    terminals: tuple[int, ...],
    deleted: int,
    start: int,
) -> tuple[int, list[list[int]]]:
    """Encode a simple path starting at ``start`` and visiting terminals."""

    vertices = tuple(vertex for vertex in range(order) if vertex != deleted)
    positions = len(vertices)
    neighbours = {vertex: [] for vertex in vertices}
    for left, right in edges:
        if deleted in (left, right):
            continue
        neighbours[left].append(right)
        neighbours[right].append(left)

    next_variable = 1
    at: dict[tuple[int, int], int] = {}
    for vertex in vertices:
        for position in range(positions):
            at[vertex, position] = next_variable
            next_variable += 1
    active = []
    for _ in range(positions):
        active.append(next_variable)
        next_variable += 1

    clauses: list[list[int]] = []
    clauses.append([active[0]])
    clauses.append([at[start, 0]])

    for position in range(positions):
        column = [at[vertex, position] for vertex in vertices]
        clauses.append([-active[position], *column])
        for variable in column:
            clauses.append([-variable, active[position]])
        for left_index, left in enumerate(column):
            for right in column[left_index + 1 :]:
                clauses.append([-left, -right])
        if position + 1 < positions:
            clauses.append([-active[position + 1], active[position]])

    for vertex in vertices:
        row = [at[vertex, position] for position in range(positions)]
        for left_index, left in enumerate(row):
            for right in row[left_index + 1 :]:
                clauses.append([-left, -right])

    for terminal in terminals:
        if terminal == deleted:
            clauses.append([])
        else:
            clauses.append(
                [at[terminal, position] for position in range(positions)]
            )

    for position in range(positions - 1):
        for vertex in vertices:
            clauses.append(
                [
                    -at[vertex, position],
                    -active[position + 1],
                    *[
                        at[neighbour, position + 1]
                        for neighbour in neighbours[vertex]
                    ],
                ]
            )

    return next_variable - 1, clauses


def cadical_sat(
    variables: int, clauses: list[list[int]], cadical: str
) -> bool:
    descriptor, path = tempfile.mkstemp(prefix="p4-path-", suffix=".cnf")
    try:
        with os.fdopen(descriptor, "w", encoding="ascii") as stream:
            stream.write(f"p cnf {variables} {len(clauses)}\n")
            for clause in clauses:
                stream.write(" ".join(map(str, clause)))
                stream.write(" 0\n")
        completed = subprocess.run(
            [cadical, "--quiet", path],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        if completed.returncode == 10:
            return True
        if completed.returncode == 20:
            return False
        raise RuntimeError(
            f"CaDiCaL returned {completed.returncode}: {completed.stderr}"
        )
    finally:
        os.unlink(path)


def fast_path_search(
    order: int,
    edges: list[tuple[int, int]],
    terminals: tuple[int, ...],
    deleted: int,
    start: int,
    state_limit: int = 100_000,
) -> bool | None:
    """Find a path quickly; return None when the exact fallback is needed."""

    adjacency = [[] for _ in range(order)]
    for left, right in edges:
        if deleted in (left, right):
            continue
        adjacency[left].append(right)
        adjacency[right].append(left)
    terminal_bits = {
        terminal: 1 << index for index, terminal in enumerate(terminals)
    }
    target = (1 << len(terminals)) - 1

    distances: dict[int, list[int]] = {}
    for terminal in terminals:
        distance = [order + 1] * order
        distance[terminal] = 0
        queue = deque([terminal])
        while queue:
            vertex = queue.popleft()
            for neighbour in adjacency[vertex]:
                if distance[neighbour] > distance[vertex] + 1:
                    distance[neighbour] = distance[vertex] + 1
                    queue.append(neighbour)
        distances[terminal] = distance

    states = 0
    stack = [(start, 1 << start, terminal_bits[start])]
    while stack:
        vertex, seen, trace = stack.pop()
        states += 1
        if trace == target:
            return True
        if states >= state_limit:
            return None
        missing = [
            terminal
            for index, terminal in enumerate(terminals)
            if not ((trace >> index) & 1)
        ]
        choices = [
            neighbour
            for neighbour in adjacency[vertex]
            if not ((seen >> neighbour) & 1)
        ]
        # Stack is LIFO: append farther choices first.
        choices.sort(
            key=lambda neighbour: min(
                distances[terminal][neighbour] for terminal in missing
            ),
            reverse=True,
        )
        for neighbour in choices:
            stack.append(
                (
                    neighbour,
                    seen | (1 << neighbour),
                    trace | terminal_bits.get(neighbour, 0),
                )
            )
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cadical", default="/opt/homebrew/bin/cadical")
    parser.add_argument("--maximum-rows", type=int)
    arguments = parser.parse_args()

    rows = roots = endpoint_tests = 0
    for line in sys.stdin:
        if arguments.maximum_rows is not None and rows >= arguments.maximum_rows:
            break
        record = json.loads(line)
        rows += 1
        order, edges = parse_graph6(record["graph6"])
        incident = incidence(order, edges)
        edge_to_id = {edge: edge_id for edge_id, edge in enumerate(edges)}
        mark_edges = tuple(
            tuple(sorted(edge)) for edge in record["mark_edges"]
        )
        marks = tuple(edge_to_id[edge] for edge in mark_edges)
        colours = tait_colourings(order, edges, incident)
        common_colourings = [
            colouring
            for colouring in colours
            if len({colouring[mark] for mark in marks}) == 1
        ]
        assert common_colourings

        for root in range(len(edges)):
            if root in marks:
                continue
            if not deletion_is_bridgeless(order, edges, incident, root):
                continue
            root_colouring = next(
                (
                    colouring
                    for colouring in common_colourings
                    if colouring[root] != colouring[marks[0]]
                ),
                None,
            )
            if root_colouring is None:
                continue
            roots += 1
            subdivided_order, subdivided_edges, terminals = (
                subdivide_marks_after_root_deletion(
                    order, edges, marks, root
                )
            )
            for mark_index, mark in enumerate(mark_edges):
                terminal = terminals[mark_index]
                for deleted in mark:
                    endpoint_tests += 1
                    quick = fast_path_search(
                        subdivided_order,
                        subdivided_edges,
                        terminals,
                        deleted,
                        terminal,
                    )
                    if quick is True:
                        continue
                    variables, clauses = path_cnf(
                        subdivided_order,
                        subdivided_edges,
                        terminals,
                        deleted,
                        terminal,
                    )
                    if quick is None and cadical_sat(
                        variables, clauses, arguments.cadical
                    ):
                        continue
                    print(
                        json.dumps(
                            {
                                "classification": (
                                    "FULL_PRODUCER_HYPOTHESES_P4_FAILURE"
                                ),
                                "source_row": record.get("row"),
                                "graph6": record["graph6"],
                                "order": order,
                                "marks": mark_edges,
                                "mark_edge_ids": marks,
                                "root": edges[root],
                                "root_edge_id": root,
                                "deleted_vertex": deleted,
                                "singleton_terminal": terminal,
                                "tait_colouring": root_colouring,
                                "tait_colourings_mod_s3": len(colours),
                                "path_cnf_variables": variables,
                                "path_cnf_clauses": len(clauses),
                                "rows_scanned": rows,
                                "roots_scanned": roots,
                                "endpoint_tests": endpoint_tests,
                            },
                            sort_keys=True,
                        )
                    )
                    return 0
        print(
            json.dumps(
                {
                    "rows": rows,
                    "roots": roots,
                    "endpoint_tests": endpoint_tests,
                },
                sort_keys=True,
            ),
            file=sys.stderr,
            flush=True,
        )

    print(
        json.dumps(
            {
                "classification": "NO_P4_FAILURE_IN_SCANNED_ROWS",
                "rows": rows,
                "roots": roots,
                "endpoint_tests": endpoint_tests,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
