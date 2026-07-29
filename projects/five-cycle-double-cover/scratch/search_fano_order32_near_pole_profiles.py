#!/usr/bin/env python3
"""Classify deleted-edge poles of the exact cyclic-4 order-32 near-flow.

The retained flow has exactly five uncleanable functional projections.
For each of its 48 adjacent-vertex-deletion four-poles, this discovery
script solves the completion-sound local two-cycle formula for all seven
functionals.  It also checks whether the pole contains a cyclic internal
shore behind at most three proper/semiedge boundary incidences.

CaDiCaL is a discovery solver here.  Any positive theorem extracted from
this scan requires a solver-independent checker or proof certificate.
The target is an auxiliary fixed-flow obstruction, not FiveCDC itself.
"""

from __future__ import annotations

import argparse
import itertools
import json
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path


GRAPH6 = (
    "_??G@EOGG?GB_AO_g_?CP_??C??O????[O?CA?AG??CA??@???A?O??C???????"
    "G????g???@W???E????@c"
)
SOURCE = (
    "search/known_snarks/source/"
    "Generated_graphs.32.05.sn.cyc4-circ_flownr_5.g6"
)
SOURCE_ROW = 3
FLOW = (
    3, 6, 2, 7, 5, 7, 2, 7, 5, 2, 1, 7, 2, 4, 6, 5,
    6, 6, 5, 3, 6, 5, 5, 5, 6, 3, 6, 3, 6, 3, 5, 6,
    3, 2, 4, 4, 1, 1, 6, 7, 2, 3, 1, 2, 6, 6, 2, 4,
)
GLOBAL_BAD = (2, 3, 4, 5, 7)


class Cnf:
    def __init__(self) -> None:
        self.variables = 0
        self.clauses: list[tuple[int, ...]] = []

    def variable(self) -> int:
        self.variables += 1
        return self.variables

    def add(self, *literals: int) -> None:
        self.clauses.append(tuple(literals))

    def even3(self, first: int, second: int, third: int) -> None:
        self.add(first, second, -third)
        self.add(first, -second, third)
        self.add(-first, second, third)
        self.add(-first, -second, -third)

    def and_equivalence(self, output: int, first: int, second: int) -> None:
        self.add(-first, -second, output)
        self.add(first, -output)
        self.add(second, -output)

    def xor_equivalence(self, output: int, first: int, second: int) -> None:
        self.add(first, second, -output)
        self.add(first, -second, output)
        self.add(-first, second, output)
        self.add(-first, -second, -output)

    def even(self, variables: list[int]) -> None:
        if not variables:
            return
        if len(variables) == 1:
            self.add(-variables[0])
            return
        accumulator = variables[0]
        for variable in variables[1:]:
            output = self.variable()
            self.xor_equivalence(output, accumulator, variable)
            accumulator = output
        self.add(-accumulator)


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    values = [ord(character) - 63 for character in record.strip()]
    assert values and values[0] <= 62
    vertices = values[0]
    edges = []
    position = 0
    for right in range(1, vertices):
        for left in range(right):
            byte = 1 + position // 6
            assert byte < len(values)
            if values[byte] >> (5 - position % 6) & 1:
                edges.append((left, right))
            position += 1
    return vertices, tuple(edges)


def dot(first: int, second: int) -> int:
    return (first & second).bit_count() & 1


def read_source(source_root: Path) -> str:
    rows = (
        source_root.joinpath(SOURCE)
        .read_text(encoding="ascii")
        .splitlines()
    )
    assert SOURCE_ROW < len(rows)
    record = rows[SOURCE_ROW]
    assert record and record[0] == chr(32 + 63)
    assert record == GRAPH6
    return record


def make_pole(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    deleted_edge: int,
) -> tuple[
    tuple[int, ...],
    tuple[tuple[int, int], ...],
    tuple[int, ...],
    tuple[tuple[int, int], ...],
]:
    deleted_vertices = set(edges[deleted_edge])
    retained = tuple(
        vertex for vertex in range(vertices) if vertex not in deleted_vertices
    )
    proper_edges = []
    proper_values = []
    ports = []
    for edge, (first, second) in enumerate(edges):
        if first in deleted_vertices and second in deleted_vertices:
            continue
        if first in deleted_vertices:
            ports.append((second, FLOW[edge]))
        elif second in deleted_vertices:
            ports.append((first, FLOW[edge]))
        else:
            proper_edges.append((first, second))
            proper_values.append(FLOW[edge])
    assert len(retained) == 30
    assert len(proper_edges) == 43
    assert len(ports) == 4
    return retained, tuple(proper_edges), tuple(proper_values), tuple(sorted(ports))


def local_cnf(
    retained: tuple[int, ...],
    proper_edges: tuple[tuple[int, int], ...],
    proper_values: tuple[int, ...],
    ports: tuple[tuple[int, int], ...],
    functional: int,
) -> Cnf:
    cnf = Cnf()
    edge_count = len(proper_edges) + len(ports)
    first = [cnf.variable() for _ in range(edge_count)]
    second = [cnf.variable() for _ in range(edge_count)]
    vertex_index = {vertex: index for index, vertex in enumerate(retained)}
    rows: list[list[int]] = [[] for _ in retained]
    for edge, (left, right) in enumerate(proper_edges):
        rows[vertex_index[left]].append(edge)
        rows[vertex_index[right]].append(edge)
    offset = len(proper_edges)
    for port, (vertex, _) in enumerate(ports):
        rows[vertex_index[vertex]].append(offset + port)
    assert all(len(row) == 3 for row in rows)
    for row in rows:
        cnf.even3(*(first[edge] for edge in row))
        cnf.even3(*(second[edge] for edge in row))

    values = proper_values + tuple(value for _, value in ports)
    factor = {
        edge for edge, value in enumerate(values)
        if dot(functional, value) == 0
    }
    for edge in factor:
        cnf.add(first[edge], second[edge])

    adjacency: list[list[int]] = [[] for _ in retained]
    for edge, (left, right) in enumerate(proper_edges):
        if edge in factor:
            a = vertex_index[left]
            b = vertex_index[right]
            adjacency[a].append(b)
            adjacency[b].append(a)
    unseen = set(range(len(retained)))
    components = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        queue = [root]
        while queue:
            vertex = queue.pop()
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        components.append(component)

    cuts = []
    product_edges: set[int] = set()
    for component in components:
        if any(
            offset + port in factor and vertex_index[vertex] in component
            for port, (vertex, _) in enumerate(ports)
        ):
            continue
        cut = [
            edge
            for edge, (left, right) in enumerate(proper_edges)
            if (
                (vertex_index[left] in component)
                != (vertex_index[right] in component)
            )
        ]
        cut.extend(
            offset + port
            for port, (vertex, _) in enumerate(ports)
            if vertex_index[vertex] in component
        )
        cuts.append(cut)
        product_edges.update(cut)
    products = {edge: cnf.variable() for edge in product_edges}
    for edge, output in products.items():
        cnf.and_equivalence(output, first[edge], second[edge])
    for cut in cuts:
        cnf.even([products[edge] for edge in cut])
    return cnf


def solve(cnf: Cnf, cadical: str) -> bool:
    with tempfile.NamedTemporaryFile("w", suffix=".cnf") as stream:
        stream.write(f"p cnf {cnf.variables} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")
        stream.flush()
        result = subprocess.run(
            [cadical, "-q", stream.name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    assert result.returncode in (10, 20)
    return result.returncode == 10


def has_small_cyclic_internal_shore(
    retained: tuple[int, ...],
    proper_edges: tuple[tuple[int, int], ...],
    ports: tuple[tuple[int, int], ...],
) -> tuple[int, ...] | None:
    """Find a cyclic pole shore with at most three boundary incidences."""
    index = {vertex: offset for offset, vertex in enumerate(retained)}
    outside = len(retained)
    augmented = [
        (index[first], index[second]) for first, second in proper_edges
    ]
    augmented.extend((index[vertex], outside) for vertex, _ in ports)
    vertex_count = outside + 1
    for size in range(1, 4):
        for omitted_tuple in itertools.combinations(range(len(augmented)), size):
            omitted = set(omitted_tuple)
            adjacency = [[] for _ in range(vertex_count)]
            for edge, (first, second) in enumerate(augmented):
                if edge not in omitted:
                    adjacency[first].append((second, edge))
                    adjacency[second].append((first, edge))
            seen = {outside}
            queue = [outside]
            for vertex in queue:
                for neighbor, _ in adjacency[vertex]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        queue.append(neighbor)
            for root in range(outside):
                if root in seen:
                    continue
                component = {root}
                seen.add(root)
                queue = [root]
                internal_edges = 0
                for vertex in queue:
                    internal_edges += len(adjacency[vertex])
                    for neighbor, _ in adjacency[vertex]:
                        if neighbor not in seen:
                            seen.add(neighbor)
                            component.add(neighbor)
                            queue.append(neighbor)
                internal_edges //= 2
                if internal_edges >= len(component):
                    return tuple(sorted(retained[vertex] for vertex in component))
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-root",
        type=Path,
        help="optional laboratory root used to verify the embedded source row",
    )
    parser.add_argument("--cadical", default=shutil.which("cadical"))
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    assert arguments.cadical
    record = (
        read_source(arguments.source_root)
        if arguments.source_root is not None
        else GRAPH6
    )
    vertices, edges = parse_graph6(record)
    assert vertices == 32
    assert len(edges) == len(FLOW) == 48
    rows = [[] for _ in range(vertices)]
    for edge, (first, second) in enumerate(edges):
        rows[first].append(edge)
        rows[second].append(edge)
    assert all(len(row) == 3 for row in rows)
    assert all(
        FLOW[row[0]] ^ FLOW[row[1]] ^ FLOW[row[2]] == 0
        for row in rows
    )

    pole_rows = []
    histogram: Counter[tuple[int, ...]] = Counter()
    for deleted_edge in range(len(edges)):
        pole = make_pole(vertices, edges, deleted_edge)
        profile = tuple(
            functional
            for functional in range(1, 8)
            if not solve(local_cnf(*pole, functional), arguments.cadical)
        )
        assert set(profile) <= set(GLOBAL_BAD)
        shore = has_small_cyclic_internal_shore(
            pole[0],
            pole[1],
            pole[3],
        )
        histogram[profile] += 1
        pole_rows.append({
            "deleted_edge": deleted_edge,
            "endpoints": edges[deleted_edge],
            "value": FLOW[deleted_edge],
            "local_bad_profile": profile,
            "contains_cyclic_internal_shore_of_boundary_at_most_three": (
                shore is not None
            ),
            "first_small_cyclic_shore": shore,
        })
        print(json.dumps(pole_rows[-1]))

    report = {
        "schema": "fano-order32-near-pole-profiles-v1",
        "claim_scope": "discovery scan; auxiliary fixed-flow route; not FiveCDC",
        "source": SOURCE,
        "source_row_zero_based": SOURCE_ROW,
        "graph6": record,
        "flow_values": FLOW,
        "global_bad_profile": GLOBAL_BAD,
        "profile_histogram": {
            ",".join(map(str, profile)): count
            for profile, count in sorted(histogram.items())
        },
        "poles": pole_rows,
    }
    print(json.dumps({
        "profile_histogram": report["profile_histogram"],
        "robust_nonempty_poles": sum(
            bool(row["local_bad_profile"])
            and not row[
                "contains_cyclic_internal_shore_of_boundary_at_most_three"
            ]
            for row in pole_rows
        ),
    }))
    if arguments.output:
        arguments.output.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
