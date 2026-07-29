#!/usr/bin/env python3
"""Construct the 366-vertex girth-ten non-full six-pole.

The skeleton is the first order-18 Blanusa row in the retained strict-snark
source.  Delete vertices 13 and 16.  Replace five skeleton edges by the
two-pole obtained by deleting edge (0,1) from the Harries (3,10)-cage.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations
import argparse
import json
from pathlib import Path


BLANUSA_GRAPH6 = "Q???C@?GCoOoDO[?CcAO_?k?J??"
DELETED_VERTICES = (13, 16)
REPLACED_EDGE_INDICES = (0, 1, 3, 10, 18)
HARRIES_LCF_BLOCK = (
    -29, -19, -13, 13, 21, -27, 27,
    33, -13, 13, 19, -21, -33, 29,
)


def decode_graph6(record: str) -> tuple[int, list[tuple[int, int]]]:
    if record.startswith(">>graph6<<"):
        record = record[10:]
    if not record or ord(record[0]) - 63 >= 63:
        raise AssertionError("this source must use the short graph6 header")
    vertices = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise AssertionError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, edges


def lcf_graph(block: tuple[int, ...], repeats: int):
    shifts = block * repeats
    vertices = len(shifts)
    edges = {
        tuple(sorted((vertex, (vertex + 1) % vertices)))
        for vertex in range(vertices)
    }
    for vertex, shift in enumerate(shifts):
        edges.add(tuple(sorted((vertex, (vertex + shift) % vertices))))
    return vertices, sorted(edges)


def adjacency(
    vertices: int, edges: list[tuple[int, int]]
) -> list[list[tuple[int, int]]]:
    rows = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append((right, edge))
        rows[right].append((left, edge))
    return rows


def connected_bridgeless(
    vertices: int, edges: list[tuple[int, int]]
) -> tuple[bool, bool]:
    rows = adjacency(vertices, edges)
    discovery = [-1] * vertices
    low = [-1] * vertices
    clock = 0
    bridges = 0

    def visit(vertex: int, parent_edge: int) -> None:
        nonlocal clock, bridges
        discovery[vertex] = low[vertex] = clock
        clock += 1
        for other, edge in rows[vertex]:
            if edge == parent_edge:
                continue
            if discovery[other] < 0:
                visit(other, edge)
                low[vertex] = min(low[vertex], low[other])
                if low[other] > discovery[vertex]:
                    bridges += 1
            else:
                low[vertex] = min(low[vertex], discovery[other])

    visit(0, -1)
    connected = all(value >= 0 for value in discovery)
    return connected, connected and bridges == 0


def girth(vertices: int, edges: list[tuple[int, int]]) -> int | None:
    rows = adjacency(vertices, edges)
    best = vertices + 1
    for source in range(vertices):
        distance = [-1] * vertices
        parent = [-1] * vertices
        distance[source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for other, _ in rows[vertex]:
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    best = min(
                        best,
                        distance[vertex] + distance[other] + 1,
                    )
    return None if best == vertices + 1 else best


def source_skeleton():
    vertices, edges = decode_graph6(BLANUSA_GRAPH6)
    if (vertices, len(edges)) != (18, 27):
        raise AssertionError("wrong Blanusa source dimensions")
    rows = adjacency(vertices, edges)
    if any(len(row) != 3 for row in rows):
        raise AssertionError("Blanusa source is not cubic")
    if connected_bridgeless(vertices, edges) != (True, True):
        raise AssertionError("Blanusa source premise failure")
    if girth(vertices, edges) != 5:
        raise AssertionError("Blanusa source has wrong girth")

    deleted = set(DELETED_VERTICES)
    retained = [v for v in range(vertices) if v not in deleted]
    mapping = {old: new for new, old in enumerate(retained)}
    internal = [
        (mapping[left], mapping[right])
        for left, right in edges
        if left not in deleted and right not in deleted
    ]
    ports = [
        mapping[other]
        for deleted_vertex in DELETED_VERTICES
        for other, _ in sorted(rows[deleted_vertex])
    ]
    if len(ports) != 6 or len(set(ports)) != 6:
        raise AssertionError("deleted vertices do not give six distinct ports")
    if len(internal) != 21:
        raise AssertionError("wrong skeleton edge count")
    return internal, ports


def minimum_short_cycle_hitting_set(
    vertices: int, edges: list[tuple[int, int]]
) -> tuple[int, ...]:
    for size in range(len(edges) + 1):
        for removed in combinations(range(len(edges)), size):
            retained = [
                edge for index, edge in enumerate(edges)
                if index not in removed
            ]
            value = girth(vertices, retained)
            if value is None or value >= 10:
                return removed
    raise AssertionError("no short-cycle hitting set found")


def build_atom():
    skeleton_edges, ports = source_skeleton()
    minimum = minimum_short_cycle_hitting_set(16, skeleton_edges)
    if minimum != REPLACED_EDGE_INDICES:
        raise AssertionError(
            f"unexpected lexicographically first minimum set {minimum}"
        )
    residual = [
        edge for index, edge in enumerate(skeleton_edges)
        if index not in REPLACED_EDGE_INDICES
    ]
    residual_girth = girth(16, residual)
    if residual_girth is not None and residual_girth < 10:
        raise AssertionError("residual skeleton still has a short cycle")

    cage_vertices, cage_edges = lcf_graph(HARRIES_LCF_BLOCK, 5)
    if (cage_vertices, len(cage_edges), girth(cage_vertices, cage_edges)) != (
        70, 105, 10
    ):
        raise AssertionError("Harries cage premise failure")
    cut_edge = (0, 1)
    if cut_edge not in cage_edges:
        raise AssertionError("selected Harries edge is absent")
    cage_internal = [edge for edge in cage_edges if edge != cut_edge]

    atom_edges = list(residual)
    replacements = []
    next_vertex = 16
    for skeleton_edge_index in REPLACED_EDGE_INDICES:
        left, right = skeleton_edges[skeleton_edge_index]
        offset = next_vertex
        next_vertex += cage_vertices
        atom_edges.extend(
            (offset + first, offset + second)
            for first, second in cage_internal
        )
        atom_edges.append(tuple(sorted((left, offset))))
        atom_edges.append(tuple(sorted((right, offset + 1))))
        replacements.append({
            "skeleton_edge_index": skeleton_edge_index,
            "skeleton_edge": [left, right],
            "vertex_offset": offset,
            "cage_cut_edge": [0, 1],
        })
    atom_edges.sort()
    if (next_vertex, len(atom_edges)) != (366, 546):
        raise AssertionError("wrong expanded atom dimensions")
    if len(atom_edges) != len(set(atom_edges)):
        raise AssertionError("expanded atom has a duplicate edge")
    rows = adjacency(next_vertex, atom_edges)
    for vertex, row in enumerate(rows):
        expected = 2 if vertex in ports else 3
        if len(row) != expected:
            raise AssertionError(
                f"wrong degree {len(row)} at atom vertex {vertex}"
            )
    if girth(next_vertex, atom_edges) != 10:
        raise AssertionError("expanded atom does not have girth ten")
    return skeleton_edges, ports, atom_edges, replacements


def write_pole(
    path: Path,
    vertices: int,
    edges: list[tuple[int, int]],
    ports: list[int],
) -> None:
    rows = [
        f"{vertices} {len(edges)} 6",
        " ".join(map(str, ports)),
        *(f"{left} {right}" for left, right in edges),
    ]
    path.write_text("\n".join(rows) + "\n", encoding="ascii")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("small_pole", type=Path)
    parser.add_argument("expanded_atom", type=Path)
    parser.add_argument("report", type=Path)
    arguments = parser.parse_args()
    skeleton, ports, expanded, replacements = build_atom()
    write_pole(arguments.small_pole, 16, skeleton, ports)
    write_pole(arguments.expanded_atom, 366, expanded, ports)
    report = {
        "schema": "blanusa-harries-nonfull-atom-v1",
        "source": {
            "blanusa_graph6": BLANUSA_GRAPH6,
            "retained_source_row": 2,
            "deleted_vertices": list(DELETED_VERTICES),
            "harries_lcf_block": list(HARRIES_LCF_BLOCK),
            "harries_lcf_repeats": 5,
            "harries_cut_edge": [0, 1],
        },
        "skeleton": {
            "vertices": 16,
            "internal_edges": len(skeleton),
            "ports": ports,
            "ports_distinct": len(set(ports)) == 6,
            "minimum_short_cycle_hitting_set_size": 5,
            "replaced_edge_indices": list(REPLACED_EDGE_INDICES),
            "residual_girth": girth(
                16,
                [
                    edge for index, edge in enumerate(skeleton)
                    if index not in REPLACED_EDGE_INDICES
                ],
            ),
        },
        "atom": {
            "vertices": 366,
            "internal_edges": len(expanded),
            "ports": ports,
            "simple": len(set(expanded)) == len(expanded),
            "internal_girth": girth(366, expanded),
            "degree_two_ports": 6,
            "degree_three_internal_vertices": 360,
        },
        "replacements": replacements,
    }
    arguments.report.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(json.dumps(
        {
            "atom_vertices": 366,
            "atom_edges": len(expanded),
            "girth": report["atom"]["internal_girth"],
            "ports": ports,
            "replaced_edges": list(REPLACED_EDGE_INDICES),
        },
        sort_keys=True,
        separators=(",", ":"),
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
