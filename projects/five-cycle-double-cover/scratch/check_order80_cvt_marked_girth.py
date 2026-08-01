#!/usr/bin/env python3
"""Filter the order-80 cubic vertex-transitive census by marked girth.

For a cubic graph H and an eight-edge matching S, subdividing every edge
of S once gives girth at least 10 exactly when

    |C| + |C intersect S| >= 10

for every circuit C of H.  It is enough to impose this on the simple
cycles of length below 10.  The resulting feasibility problem is a
small 0-1 linear program:

* choose exactly eight edges;
* choose at most one edge at each vertex;
* for every short cycle C, choose at least 10-|C| of its edges.

The input used in the project is the graph6/sparse6 conversion of the
Potočnik--Spiga--Verret cubic vertex-transitive census:

  https://github.com/kguo-sagecode/cubic-vertextransitive-graphs

The file has a ``g6`` suffix but contains sparse6 records.  NetworkX
autodetects the format from the leading colon.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Iterable

import networkx as nx
import numpy as np
import scipy
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


def canonical_edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def canonical_cycle(vertices: list[int]) -> tuple[int, ...]:
    """Return a rotation/reflection-independent vertex representation."""

    n = len(vertices)
    rotations: list[tuple[int, ...]] = []
    for direction in (vertices, list(reversed(vertices))):
        for offset in range(n):
            rotations.append(tuple(direction[offset:] + direction[:offset]))
    return min(rotations)


def simple_cycles_below(g: nx.Graph, cutoff: int) -> list[tuple[int, ...]]:
    """Enumerate each undirected simple cycle of length < cutoff once."""

    found: set[tuple[int, ...]] = set()
    for start in sorted(g.nodes()):
        # Requiring start to be the least vertex on the cycle reduces work.
        stack: list[tuple[int, list[int], set[int]]] = [(start, [start], {start})]
        while stack:
            vertex, path, used = stack.pop()
            if len(path) >= cutoff:
                continue
            for nxt in sorted(g.neighbors(vertex), reverse=True):
                if nxt == start:
                    if len(path) >= 3:
                        found.add(canonical_cycle(path))
                    continue
                if nxt < start or nxt in used:
                    continue
                stack.append((nxt, path + [nxt], used | {nxt}))
    return sorted(found, key=lambda cycle: (len(cycle), cycle))


def cycle_edges(cycle: tuple[int, ...]) -> Iterable[tuple[int, int]]:
    for index, u in enumerate(cycle):
        yield canonical_edge(u, cycle[(index + 1) % len(cycle)])


def marked_girth_milp(
    g: nx.Graph, cycles: list[tuple[int, ...]]
) -> tuple[bool, list[tuple[int, int]] | None, str]:
    edges = sorted(canonical_edge(u, v) for u, v in g.edges())
    edge_index = {edge: index for index, edge in enumerate(edges)}

    rows: list[tuple[dict[int, float], float, float]] = []
    rows.append(({index: 1.0 for index in range(len(edges))}, 8.0, 8.0))

    for vertex in sorted(g.nodes()):
        incident = {
            edge_index[canonical_edge(vertex, neighbor)]: 1.0
            for neighbor in g.neighbors(vertex)
        }
        rows.append((incident, -np.inf, 1.0))

    for cycle in cycles:
        coefficients = {edge_index[edge]: 1.0 for edge in cycle_edges(cycle)}
        rows.append((coefficients, float(10 - len(cycle)), np.inf))

    matrix = lil_matrix((len(rows), len(edges)), dtype=float)
    lower = np.empty(len(rows))
    upper = np.empty(len(rows))
    for row_index, (coefficients, lo, hi) in enumerate(rows):
        for column, coefficient in coefficients.items():
            matrix[row_index, column] = coefficient
        lower[row_index] = lo
        upper[row_index] = hi

    result = milp(
        c=np.zeros(len(edges)),
        integrality=np.ones(len(edges)),
        bounds=Bounds(np.zeros(len(edges)), np.ones(len(edges))),
        constraints=LinearConstraint(matrix.tocsr(), lower, upper),
        options={"presolve": True},
    )
    if result.success:
        chosen = [edge for edge, value in zip(edges, result.x) if value > 0.5]
        assert len(chosen) == 8
        return True, chosen, result.message
    return False, None, result.message


def decode_graph(line: str) -> nx.Graph:
    data = line.encode("ascii")
    if line.startswith(":"):
        graph = nx.from_sparse6_bytes(data)
    else:
        graph = nx.from_graph6_bytes(data)
    return nx.Graph(graph)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("census", type=Path)
    parser.add_argument("--order", type=int, default=80)
    parser.add_argument("--target-girth", type=int, default=10)
    args = parser.parse_args()

    if args.target_girth != 10:
        raise SystemExit("this certificate script currently fixes target girth at 10")

    raw = args.census.read_bytes()
    lines = [
        line.strip()
        for line in raw.decode("ascii").splitlines()
        if line.strip() and not line.startswith(">>")
    ]
    selected = []
    for census_line, line in enumerate(lines, start=1):
        graph = decode_graph(line)
        if graph.number_of_nodes() != args.order:
            continue
        if (
            not nx.is_connected(graph)
            or nx.number_of_selfloops(graph)
            or set(dict(graph.degree()).values()) != {3}
        ):
            raise AssertionError(f"invalid cubic census row {census_line}")
        selected.append((census_line, line, graph))

    records = []
    for order_index, (census_line, line, graph) in enumerate(selected, start=1):
        cycles = simple_cycles_below(graph, args.target_girth)
        length_counts = Counter(map(len, cycles))
        girth = nx.girth(graph)
        edge_cycle_incidence = Counter(
            edge for cycle in cycles for edge in cycle_edges(cycle)
        )
        best_eight_edge_capacity = sum(
            sorted(edge_cycle_incidence.values(), reverse=True)[:8]
        )
        summed_cycle_requirement = sum(10 - len(cycle) for cycle in cycles)

        # If the ordinary girth is at most six, one subdivision on each
        # edge of a matching cannot bring a shortest cycle to length ten.
        if girth <= 6:
            feasible = False
            witness = None
            solver_message = "infeasible by matching bound on a shortest cycle"
            method = "shortest-cycle matching bound"
            milp_feasible = None
        else:
            milp_feasible, witness, solver_message = marked_girth_milp(
                graph, cycles
            )
            counting_infeasible = (
                best_eight_edge_capacity < summed_cycle_requirement
            )
            if counting_infeasible:
                assert not milp_feasible
                feasible = False
                method = "summed short-cycle incidence bound; SciPy MILP cross-check"
            else:
                feasible = milp_feasible
                method = "SciPy MILP"

        records.append(
            {
                "order_index": order_index,
                "census_line": census_line,
                "encoding": line,
                "ordinary_girth": girth,
                "short_cycle_counts": {
                    str(length): length_counts[length]
                    for length in sorted(length_counts)
                },
                "summed_short_cycle_requirement": summed_cycle_requirement,
                "best_eight_edge_incidence_capacity": best_eight_edge_capacity,
                "marked_girth_feasible": feasible,
                "milp_feasible": milp_feasible,
                "witness_matching": witness,
                "method": method,
                "solver_message": solver_message,
            }
        )

    output = {
        "input": str(args.census),
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "order": args.order,
        "target_subdivided_girth": args.target_girth,
        "networkx_version": nx.__version__,
        "scipy_version": scipy.__version__,
        "graphs_of_order": len(records),
        "feasible_order_indices": [
            record["order_index"]
            for record in records
            if record["marked_girth_feasible"]
        ],
        "records": records,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
