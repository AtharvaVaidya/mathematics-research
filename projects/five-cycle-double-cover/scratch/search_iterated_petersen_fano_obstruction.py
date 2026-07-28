#!/usr/bin/env python3
"""Search Petersen 3-sums for a flow whose seven projections are uncleanable.

This is a targeted search for a counterexample to the *sufficient*
"some good Fano line" statement, not directly for a counterexample to
five-cycle double cover.  It starts from the frozen order-18 six-bad-line
flow and replaces one vertex by a rooted Petersen 3-pole in every
flow-compatible way.

For each functional projection h, cleanability is encoded exactly by the
two-cycle normal form:

  * p and q are binary cycles;
  * p OR q contains every edge outside h; and
  * p AND q crosses every component of E-h evenly.

CaDiCaL is used only as a search solver.  A retained UNSAT result still
requires a certificate-producing replay and an independent checker.
"""

from __future__ import annotations

import argparse
import itertools
import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import networkx as nx


NEAR_GRAPH6 = "Q???C@?K@O@aDAw?GW?J?_g?Y??"
NEAR_FLOW = (
    1, 5, 6, 5, 3, 4, 6, 5, 3, 3, 4, 7, 2, 7,
    5, 2, 5, 7, 1, 6, 7, 3, 1, 2, 6, 2, 4,
)
PETERSEN_EDGES = (
    (0, 2), (0, 4), (0, 6), (1, 4), (1, 7),
    (1, 8), (2, 3), (2, 7), (3, 5), (3, 8),
    (4, 5), (5, 9), (6, 8), (6, 9), (7, 9),
)
PETERSEN_FLOW = (6, 3, 5, 5, 1, 4, 2, 4, 5, 7, 6, 3, 3, 6, 5)
PETERSEN_ROOT = 0


@dataclass(frozen=True)
class FlowGraph:
    order: int
    edges: tuple[tuple[int, int], ...]
    values: tuple[int, ...]


def decode_graph6(row: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    graph = nx.from_graph6_bytes(row.encode("ascii"))
    order = graph.number_of_nodes()
    edges = tuple(
        (first, second)
        for second in range(1, order)
        for first in range(second)
        if graph.has_edge(first, second)
    )
    return order, edges


def graph6(graph: FlowGraph) -> str:
    value = nx.Graph()
    value.add_nodes_from(range(graph.order))
    value.add_edges_from(graph.edges)
    return nx.to_graph6_bytes(value, header=False).decode("ascii").strip()


def incidence(graph: FlowGraph) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(graph.order)]
    for edge, (first, second) in enumerate(graph.edges):
        rows[first].append(edge)
        rows[second].append(edge)
    return tuple(tuple(row) for row in rows)


def validate(graph: FlowGraph) -> None:
    assert len(graph.edges) == len(graph.values)
    assert len(graph.edges) * 2 == 3 * graph.order
    rows = incidence(graph)
    assert all(len(row) == 3 for row in rows)
    for row in rows:
        total = 0
        for edge in row:
            assert 1 <= graph.values[edge] <= 7
            total ^= graph.values[edge]
        assert total == 0


def linear_image(
    source_line_map: dict[int, int], source_out: int, target_out: int
) -> tuple[int, ...]:
    source_line = sorted(source_line_map)
    first, second = source_line[:2]
    assert first ^ second in source_line_map
    source_basis = (first, second, source_out)
    target_basis = (
        source_line_map[first],
        source_line_map[second],
        target_out,
    )
    result = [0] * 8
    for value in range(8):
        for coefficients in range(8):
            reconstructed = 0
            image = 0
            for index in range(3):
                if (coefficients >> index) & 1:
                    reconstructed ^= source_basis[index]
                    image ^= target_basis[index]
            if reconstructed == value:
                result[value] = image
                break
        else:
            raise AssertionError("source basis is singular")
    assert sorted(result) == list(range(8))
    return tuple(result)


def incident_ports(graph: FlowGraph, vertex: int) -> tuple[tuple[int, int], ...]:
    ports = []
    for edge, (first, second) in enumerate(graph.edges):
        if first == vertex:
            ports.append((second, graph.values[edge]))
        elif second == vertex:
            ports.append((first, graph.values[edge]))
    assert len(ports) == 3
    return tuple(sorted(ports))


def graft_petersen(
    base: FlowGraph,
    base_vertex: int,
    port_permutation: tuple[int, int, int],
    target_out: int,
) -> FlowGraph:
    target_ports = incident_ports(base, base_vertex)
    source = FlowGraph(10, PETERSEN_EDGES, PETERSEN_FLOW)
    source_ports = incident_ports(source, PETERSEN_ROOT)

    line_map = {
        source_ports[index][1]: target_ports[port_permutation[index]][1]
        for index in range(3)
    }
    source_line = set(line_map)
    target_line = set(line_map.values())
    assert len(source_line) == len(target_line) == 3
    source_out = next(value for value in range(1, 8) if value not in source_line)
    assert target_out not in target_line
    transform = linear_image(line_map, source_out, target_out)

    base_vertices = [vertex for vertex in range(base.order) if vertex != base_vertex]
    source_vertices = [
        vertex for vertex in range(source.order) if vertex != PETERSEN_ROOT
    ]
    compact = {
        old: new for new, old in enumerate(("b", vertex) for vertex in base_vertices)
    }
    compact.update({
        ("p", old): len(base_vertices) + index
        for index, old in enumerate(source_vertices)
    })

    edges: list[tuple[int, int]] = []
    values: list[int] = []
    for edge, (first, second) in enumerate(base.edges):
        if base_vertex in (first, second):
            continue
        edges.append(tuple(sorted((compact[("b", first)], compact[("b", second)]))))
        values.append(base.values[edge])
    for edge, (first, second) in enumerate(source.edges):
        if PETERSEN_ROOT in (first, second):
            continue
        edges.append(tuple(sorted((compact[("p", first)], compact[("p", second)]))))
        values.append(transform[source.values[edge]])

    for source_index, (source_neighbor, source_value) in enumerate(source_ports):
        target_index = port_permutation[source_index]
        target_neighbor, target_value = target_ports[target_index]
        assert transform[source_value] == target_value
        edges.append(tuple(sorted((
            compact[("p", source_neighbor)],
            compact[("b", target_neighbor)],
        ))))
        values.append(target_value)

    ordering = sorted(range(len(edges)), key=lambda edge: edges[edge])
    result = FlowGraph(
        base.order + source.order - 2,
        tuple(edges[edge] for edge in ordering),
        tuple(values[edge] for edge in ordering),
    )
    validate(result)
    return result


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


def factor_components(graph: FlowGraph, factor_edges: set[int]) -> list[set[int]]:
    adjacency: list[list[int]] = [[] for _ in range(graph.order)]
    for edge, (first, second) in enumerate(graph.edges):
        if edge in factor_edges:
            adjacency[first].append(second)
            adjacency[second].append(first)
    unseen = set(range(graph.order))
    components = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        stack = [root]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    stack.append(neighbor)
        components.append(component)
    return components


def cleanability_cnf(graph: FlowGraph, functional: int) -> Cnf:
    cnf = Cnf()
    p = [cnf.variable() for _ in graph.edges]
    q = [cnf.variable() for _ in graph.edges]
    rows = incidence(graph)
    for row in rows:
        cnf.even3(*(p[edge] for edge in row))
        cnf.even3(*(q[edge] for edge in row))

    projection = {
        edge
        for edge, value in enumerate(graph.values)
        if (value & functional).bit_count() & 1
    }
    factor = set(range(len(graph.edges))) - projection
    for edge in factor:
        cnf.add(p[edge], q[edge])

    components = factor_components(graph, factor)
    boundary_edges: set[int] = set()
    cuts: list[list[int]] = []
    for component in components:
        cut = [
            edge
            for edge, (first, second) in enumerate(graph.edges)
            if (first in component) != (second in component)
        ]
        cuts.append(cut)
        boundary_edges.update(cut)
    product = {edge: cnf.variable() for edge in boundary_edges}
    for edge, variable in product.items():
        cnf.and_equivalence(variable, p[edge], q[edge])
    for cut in cuts:
        cnf.even([product[edge] for edge in cut])
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
    if result.returncode == 10:
        return True
    if result.returncode == 20:
        return False
    raise RuntimeError(f"CaDiCaL returned {result.returncode}")


def profile(graph: FlowGraph, cadical: str) -> tuple[int, ...]:
    return tuple(
        functional
        for functional in range(1, 8)
        if not solve(cleanability_cnf(graph, functional), cadical)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cadical", default=shutil.which("cadical"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--stop-on-hit", action="store_true")
    arguments = parser.parse_args()
    if not arguments.cadical:
        raise SystemExit("cadical not found")

    order, edges = decode_graph6(NEAR_GRAPH6)
    base = FlowGraph(order, edges, NEAR_FLOW)
    validate(base)
    base_profile = profile(base, arguments.cadical)
    print(json.dumps({"base_order": order, "base_bad": base_profile}))
    assert len(base_profile) == 6

    seen: set[tuple[tuple[tuple[int, int], ...], tuple[int, ...]]] = set()
    rows = []
    histogram: dict[int, int] = {}
    for vertex in range(base.order):
        target_line = {value for _, value in incident_ports(base, vertex)}
        target_outs = [value for value in range(1, 8) if value not in target_line]
        for permutation in itertools.permutations(range(3)):
            for target_out in target_outs:
                candidate = graft_petersen(base, vertex, permutation, target_out)
                identity = (candidate.edges, candidate.values)
                if identity in seen:
                    continue
                seen.add(identity)
                bad = profile(candidate, arguments.cadical)
                histogram[len(bad)] = histogram.get(len(bad), 0) + 1
                row = {
                    "order": candidate.order,
                    "vertex": vertex,
                    "port_permutation": permutation,
                    "target_out": target_out,
                    "graph6": graph6(candidate),
                    "edges": candidate.edges,
                    "flow_values": candidate.values,
                    "bad_functionals": bad,
                }
                if len(bad) >= 6:
                    print(json.dumps({
                        key: value
                        for key, value in row.items()
                        if key not in {"edges", "flow_values"}
                    }))
                rows.append(row)
                if len(bad) == 7 and arguments.stop_on_hit:
                    break
            else:
                continue
            break
        else:
            continue
        break

    report = {
        "schema": "iterated-petersen-fano-search-v1",
        "base_graph6": NEAR_GRAPH6,
        "tested": len(rows),
        "bad_count_histogram": histogram,
        "hits": [row for row in rows if len(row["bad_functionals"]) == 7],
        "near_hits": [row for row in rows if len(row["bad_functionals"]) == 6],
    }
    print(json.dumps({
        "tested": report["tested"],
        "histogram": report["bad_count_histogram"],
        "hits": len(report["hits"]),
        "near_hits": len(report["near_hits"]),
    }))
    if arguments.output:
        arguments.output.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
