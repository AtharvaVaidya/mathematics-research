#!/usr/bin/env python3
"""Find root-forcing edges in marked four-edge instances.

Input is the JSON-lines output of ``tait_all_coloring_mark_separation``.
Each row must contain ``graph6`` and ``mark_edges``.  For every row this
checker independently decodes the graph, enumerates the affine cycle-space
fibre containing all four marks, retains cycles whose every circuit
component has even marked parity, and intersects their edge sets.  An
unmarked edge in that intersection is a possible obstruction to a rooted
cap-avoidance theorem.

This is an exact finite diagnostic.  It neither trusts the producer's
universal-separation/cut tests nor rechecks those two properties.
"""

from __future__ import annotations

import argparse
from collections import deque
import json
import sys


def parse_graph6(row: str) -> tuple[int, list[tuple[int, int]]]:
    values = [ord(character) - 63 for character in row]
    assert values and all(0 <= value <= 63 for value in values)
    if values[0] <= 62:
        order = values[0]
        header = 1
    elif len(values) >= 4 and values[1] <= 62:
        order = (values[1] << 12) | (values[2] << 6) | values[3]
        header = 4
    else:
        raise AssertionError("unsupported graph6 header")
    edges: list[tuple[int, int]] = []
    bit = 0
    for right in range(1, order):
        for left in range(right):
            byte = header + bit // 6
            assert byte < len(values), "truncated graph6 record"
            if (values[byte] >> (5 - bit % 6)) & 1:
                edges.append((left, right))
            bit += 1
    return order, edges


def incidence(
    order: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    answer = [[] for _ in range(order)]
    for edge_id, (left, right) in enumerate(edges):
        answer[left].append(edge_id)
        answer[right].append(edge_id)
    return answer


def fundamental_cycle_basis(
    order: int,
    edges: list[tuple[int, int]],
    incident: list[list[int]],
) -> list[int]:
    parent = [-1] * order
    parent_edge = [-1] * order
    depth = [0] * order
    tree_edges: set[int] = set()
    parent[0] = 0
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for edge_id in incident[vertex]:
            left, right = edges[edge_id]
            neighbour = left ^ right ^ vertex
            if parent[neighbour] == -1:
                parent[neighbour] = vertex
                parent_edge[neighbour] = edge_id
                depth[neighbour] = depth[vertex] + 1
                tree_edges.add(edge_id)
                queue.append(neighbour)
    assert all(value != -1 for value in parent)

    basis: list[int] = []
    for edge_id, (left0, right0) in enumerate(edges):
        if edge_id in tree_edges:
            continue
        left, right = left0, right0
        mask = 1 << edge_id
        while depth[left] > depth[right]:
            mask ^= 1 << parent_edge[left]
            left = parent[left]
        while depth[right] > depth[left]:
            mask ^= 1 << parent_edge[right]
            right = parent[right]
        while left != right:
            mask ^= 1 << parent_edge[left]
            mask ^= 1 << parent_edge[right]
            left = parent[left]
            right = parent[right]
        basis.append(mask)
    assert len(basis) == len(edges) - order + 1
    return basis


def solve_affine_trace(
    basis: list[int], marks: list[int]
) -> tuple[int, list[int]]:
    """Return one all-mark cycle and a basis of the trace-zero kernel."""

    variables = len(basis)
    rows: list[list[int]] = []
    for mark in marks:
        coefficients = sum(
            ((cycle >> mark) & 1) << index
            for index, cycle in enumerate(basis)
        )
        rows.append([coefficients, 1])

    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(variables):
        found = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if (rows[row][0] >> column) & 1
            ),
            None,
        )
        if found is None:
            continue
        rows[pivot_row], rows[found] = rows[found], rows[pivot_row]
        for row in range(len(rows)):
            if row != pivot_row and ((rows[row][0] >> column) & 1):
                rows[row][0] ^= rows[pivot_row][0]
                rows[row][1] ^= rows[pivot_row][1]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break

    for coefficients, right in rows:
        if coefficients == 0 and right:
            raise AssertionError("all-mark trace is infeasible")

    particular_coefficients = 0
    for row, column in enumerate(pivot_columns):
        if rows[row][1]:
            particular_coefficients |= 1 << column

    free_columns = [
        column for column in range(variables) if column not in pivot_columns
    ]
    kernel_coefficients: list[int] = []
    for free in free_columns:
        vector = 1 << free
        for row, pivot in enumerate(pivot_columns):
            if (rows[row][0] >> free) & 1:
                vector |= 1 << pivot
        kernel_coefficients.append(vector)

    def expand(coefficients: int) -> int:
        answer = 0
        while coefficients:
            lowest = coefficients & -coefficients
            answer ^= basis[lowest.bit_length() - 1]
            coefficients ^= lowest
        return answer

    return expand(particular_coefficients), [
        expand(vector) for vector in kernel_coefficients
    ]


def componentwise_even(
    cycle: int,
    mark_mask: int,
    edges: list[tuple[int, int]],
    incident: list[list[int]],
) -> bool:
    remaining = cycle
    while remaining:
        start_edge_bit = remaining & -remaining
        start_edge = start_edge_bit.bit_length() - 1
        component_edges = 0
        stack = [edges[start_edge][0]]
        seen_vertices = 0
        while stack:
            vertex = stack.pop()
            vertex_bit = 1 << vertex
            if seen_vertices & vertex_bit:
                continue
            seen_vertices |= vertex_bit
            for edge_id in incident[vertex]:
                edge_bit = 1 << edge_id
                if not (cycle & edge_bit):
                    continue
                component_edges |= edge_bit
                left, right = edges[edge_id]
                neighbour = left ^ right ^ vertex
                if not (seen_vertices >> neighbour) & 1:
                    stack.append(neighbour)
        if (component_edges & mark_mask).bit_count() & 1:
            return False
        remaining &= ~component_edges
    return True


def analyze(record: dict[str, object]) -> dict[str, object]:
    order, edges = parse_graph6(str(record["graph6"]))
    assert len(edges) == 3 * order // 2
    assert len(set(edges)) == len(edges)
    incident = incidence(order, edges)
    assert all(len(row) == 3 for row in incident)
    edge_to_id = {edge: edge_id for edge_id, edge in enumerate(edges)}
    mark_edges = [tuple(sorted(edge)) for edge in record["mark_edges"]]
    marks = [edge_to_id[edge] for edge in mark_edges]
    mark_mask = sum(1 << edge_id for edge_id in marks)

    basis = fundamental_cycle_basis(order, edges, incident)
    particular, kernel = solve_affine_trace(basis, marks)
    fibre_size = 1 << len(kernel)
    current = particular
    previous_gray = 0
    good_count = 0
    forced = (1 << len(edges)) - 1
    for index in range(fibre_size):
        if index:
            gray = index ^ (index >> 1)
            changed = gray ^ previous_gray
            current ^= kernel[changed.bit_length() - 1]
            previous_gray = gray
        if componentwise_even(current, mark_mask, edges, incident):
            good_count += 1
            forced &= current
    assert good_count, "producer claimed a standard four-mark instance"
    forced &= ~mark_mask
    return {
        "row": record.get("row"),
        "graph6": record["graph6"],
        "order": order,
        "marks": mark_edges,
        "cycle_space_dimension": len(basis),
        "all_mark_fibre_dimension": len(kernel),
        "all_mark_cycles": fibre_size,
        "componentwise_even_cycles": good_count,
        "forced_unmarked_edges": [
            edges[edge_id]
            for edge_id in range(len(edges))
            if (forced >> edge_id) & 1
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-all", action="store_true")
    arguments = parser.parse_args()
    rows = 0
    forced_rows: list[dict[str, object]] = []
    total_good = 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        result = analyze(json.loads(line))
        rows += 1
        total_good += int(result["componentwise_even_cycles"])
        if result["forced_unmarked_edges"]:
            forced_rows.append(result)
        if arguments.emit_all or result["forced_unmarked_edges"]:
            print(json.dumps(result, sort_keys=True))
    summary = {
        "status": "PASS",
        "rows": rows,
        "rows_with_forced_unmarked_edge": len(forced_rows),
        "total_componentwise_even_cycles": total_good,
    }
    print(json.dumps(summary, sort_keys=True), file=sys.stderr)


if __name__ == "__main__":
    main()
