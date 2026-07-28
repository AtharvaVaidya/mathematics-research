#!/usr/bin/env python3
"""SAT falsification search for independent-root D5 factor feasibility.

For a cubic graph H and root edges r,s, the generated CNF asks for a
D5 flow in which r and s lie on one component of Y_01.  This loses no
generality: a global S5 permutation sends any successful coordinate pair
to 01.

The CNF uses coordinate variables x[e,i], exact-weight-two clauses,
four-clause cubic parity constraints, XOR definitions of Y_01, and a
layered reachability witness in the line graph.  A satisfying assignment
is checked directly against the graph and factor connectivity.

This script is a falsification/search tool.  An UNSAT result is not
accepted as a counterexample without a separately checked proof trace.
"""

from __future__ import annotations

import argparse
from collections import deque
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess
import tempfile

import networkx as nx


TUTTE_COXETER_LCF = (-13, -9, 7, -7, 9, 13)
GRAY_LCF = (-25, 7, -7, 13, -13, 25)


class CNF:
    def __init__(self) -> None:
        self.names: dict[tuple[object, ...], int] = {}
        self.clauses: list[tuple[int, ...]] = []

    def var(self, *name: object) -> int:
        key = tuple(name)
        if key not in self.names:
            self.names[key] = len(self.names) + 1
        return self.names[key]

    def add(self, *literals: int) -> None:
        assert literals
        self.clauses.append(tuple(literals))

    def dimacs(self) -> str:
        rows = [f"p cnf {len(self.names)} {len(self.clauses)}"]
        rows.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return "\n".join(rows) + "\n"


def tutte_coxeter_graph() -> nx.Graph:
    graph = nx.LCF_graph(30, TUTTE_COXETER_LCF, 5)
    graph = nx.Graph(graph)
    assert graph.number_of_nodes() == 30
    assert graph.number_of_edges() == 45
    assert set(dict(graph.degree()).values()) == {3}
    assert nx.node_connectivity(graph) >= 2
    return graph


def gray_graph() -> nx.Graph:
    graph = nx.LCF_graph(54, GRAY_LCF, 9)
    graph = nx.Graph(graph)
    assert graph.number_of_nodes() == 54
    assert graph.number_of_edges() == 81
    assert set(dict(graph.degree()).values()) == {3}
    assert nx.node_connectivity(graph) >= 2
    return graph


def json_graph(path: Path) -> nx.Graph:
    data = json.loads(path.read_text(encoding="utf-8"))
    graph = nx.Graph()
    vertices = data.get("vertices", ())
    graph.add_nodes_from(range(vertices) if isinstance(vertices, int) else vertices)
    graph.add_edges_from((row["u"], row["v"]) for row in data["edges"])
    assert graph.number_of_edges() == len(data["edges"])
    assert set(dict(graph.degree()).values()) == {3}
    assert nx.is_connected(graph)
    return nx.convert_node_labels_to_integers(graph, ordering="sorted")


def girth(graph: nx.Graph) -> int:
    best = graph.number_of_nodes() + 1
    for source in graph:
        distance = {source: 0}
        parent = {source: None}
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for other in graph[vertex]:
                if other not in distance:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    best = min(best, distance[vertex] + distance[other] + 1)
    return best


def indexed_edges(graph: nx.Graph) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(tuple(sorted(edge)) for edge in graph.edges()))


def eliminate_edge(
    graph: nx.Graph, edge_index: int
) -> tuple[nx.Graph, tuple[int, int], tuple[int, int]]:
    """Delete the ends of one edge and close the two remaining pairs.

    Returns the reduced graph, the two root indices in its canonical edge
    order, and the eliminated parent edge.  This is the inverse-insertion
    geometry used in the minimum-counterexample reduction.
    """

    parent_edges = indexed_edges(graph)
    assert 0 <= edge_index < len(parent_edges)
    u, v = parent_edges[edge_index]
    u_side = sorted(set(graph[u]) - {v})
    v_side = sorted(set(graph[v]) - {u})
    assert len(u_side) == len(v_side) == 2
    assert len(set(u_side + v_side)) == 4

    reduced = graph.copy()
    reduced.remove_nodes_from((u, v))
    reduced.add_edge(*u_side)
    reduced.add_edge(*v_side)
    assert reduced.number_of_edges() == graph.number_of_edges() - 3
    assert set(dict(reduced.degree()).values()) == {3}

    relabel = {old: new for new, old in enumerate(sorted(reduced))}
    first_root_edge = tuple(sorted(relabel[x] for x in u_side))
    second_root_edge = tuple(sorted(relabel[x] for x in v_side))
    reduced = nx.relabel_nodes(reduced, relabel, copy=True)
    reduced_edges = indexed_edges(reduced)
    roots = (
        reduced_edges.index(first_root_edge),
        reduced_edges.index(second_root_edge),
    )
    assert set(reduced_edges[roots[0]]).isdisjoint(reduced_edges[roots[1]])
    return reduced, roots, (u, v)


def incidence(
    graph: nx.Graph, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    edge_index = {edge: index for index, edge in enumerate(edges)}
    rows = []
    for vertex in sorted(graph):
        row = tuple(
            sorted(edge_index[tuple(sorted((vertex, other)))] for other in graph[vertex])
        )
        assert len(row) == 3
        rows.append(row)
    return tuple(rows)


def line_graph_adjacency(
    rows: tuple[tuple[int, ...], ...], edge_count: int
) -> tuple[tuple[int, ...], ...]:
    answer = [set() for _ in range(edge_count)]
    for row in rows:
        for first, second in combinations(row, 2):
            answer[first].add(second)
            answer[second].add(first)
    return tuple(tuple(sorted(row)) for row in answer)


def build_good_flow_cnf(
    graph: nx.Graph, roots: tuple[int, int]
) -> tuple[CNF, tuple[tuple[int, int], ...]]:
    edges = indexed_edges(graph)
    rows = incidence(graph, edges)
    adjacent = line_graph_adjacency(rows, len(edges))
    first_root, second_root = roots
    assert first_root != second_root

    cnf = CNF()
    # Every edge label has exactly two of the five coordinates.
    for edge in range(len(edges)):
        variables = [cnf.var("x", edge, coordinate) for coordinate in range(5)]
        # At most two true: forbid every true triple.
        for triple in combinations(variables, 3):
            cnf.add(*(-variable for variable in triple))
        # At least two true: every four coordinates contain a true one.
        for four in combinations(variables, 4):
            cnf.add(*four)

    # Cubic xor parity: forbid 100, 010, 001, and 111.
    for row in rows:
        for coordinate in range(5):
            a, b, c = (cnf.var("x", edge, coordinate) for edge in row)
            cnf.add(-a, b, c)
            cnf.add(a, -b, c)
            cnf.add(a, b, -c)
            cnf.add(-a, -b, -c)

    # y[e] iff x[e,0] xor x[e,1].
    for edge in range(len(edges)):
        x0 = cnf.var("x", edge, 0)
        x1 = cnf.var("x", edge, 1)
        y = cnf.var("y", edge)
        cnf.add(-x0, -x1, -y)
        cnf.add(x0, x1, -y)
        cnf.add(x0, -x1, y)
        cnf.add(-x0, x1, y)

    cnf.add(cnf.var("y", first_root))
    cnf.add(cnf.var("y", second_root))

    # Layered line-graph reachability.  A true R[e,k] is supported by an
    # active path of at most k transitions from the first root.
    depth = len(edges) - 1
    for edge in range(len(edges)):
        initial = cnf.var("reach", edge, 0)
        cnf.add(initial if edge == first_root else -initial)
    for layer in range(depth + 1):
        for edge in range(len(edges)):
            cnf.add(-cnf.var("reach", edge, layer), cnf.var("y", edge))
    for layer in range(depth):
        for edge in range(len(edges)):
            old = cnf.var("reach", edge, layer)
            new = cnf.var("reach", edge, layer + 1)
            cnf.add(-old, new)
            cnf.add(
                -new,
                old,
                *(cnf.var("reach", other, layer) for other in adjacent[edge]),
            )
    cnf.add(cnf.var("reach", second_root, depth))
    return cnf, edges


def parse_model(output: str) -> set[int] | None:
    if "s UNSATISFIABLE" in output:
        return None
    assert "s SATISFIABLE" in output, output[-2000:]
    positive: set[int] = set()
    for row in output.splitlines():
        if not row.startswith("v "):
            continue
        for token in row.split()[1:]:
            literal = int(token)
            if literal > 0:
                positive.add(literal)
    return positive


def factor_components(
    graph: nx.Graph,
    edges: tuple[tuple[int, int], ...],
    labels: tuple[int, ...],
    pair: tuple[int, int] = (0, 1),
) -> tuple[tuple[int, ...], ...]:
    selected = {
        edge
        for edge, label in enumerate(labels)
        if ((label >> pair[0]) & 1) ^ ((label >> pair[1]) & 1)
    }
    rows = incidence(graph, edges)
    unseen = set(selected)
    answer = []
    while unseen:
        stack = [min(unseen)]
        component: set[int] = set()
        while stack:
            edge = stack.pop()
            if edge in component:
                continue
            component.add(edge)
            for vertex in edges[edge]:
                stack.extend(
                    other
                    for other in rows[vertex]
                    if other in selected and other not in component
                )
        unseen -= component
        answer.append(tuple(sorted(component)))
    return tuple(answer)


def validate_model(
    graph: nx.Graph,
    cnf: CNF,
    edges: tuple[tuple[int, int], ...],
    roots: tuple[int, int],
    positive: set[int],
) -> tuple[int, ...]:
    labels = tuple(
        sum(
            1 << coordinate
            for coordinate in range(5)
            if cnf.var("x", edge, coordinate) in positive
        )
        for edge in range(len(edges))
    )
    assert all(label.bit_count() == 2 for label in labels)
    for row in incidence(graph, edges):
        assert labels[row[0]] ^ labels[row[1]] ^ labels[row[2]] == 0
    root_mask = (1 << roots[0]) | (1 << roots[1])
    assert any(
        sum(1 << edge for edge in component) & root_mask == root_mask
        for component in factor_components(graph, edges, labels)
    )
    return labels


def edge_pair_orbits(
    graph: nx.Graph, edges: tuple[tuple[int, int], ...], independent_only: bool
) -> tuple[tuple[int, int], ...]:
    edge_index = {edge: index for index, edge in enumerate(edges)}
    pairs = {
        pair
        for pair in combinations(range(len(edges)), 2)
        if not independent_only
        or set(edges[pair[0]]).isdisjoint(edges[pair[1]])
    }
    unseen = set(pairs)
    representatives = []
    automorphisms = tuple(
        nx.algorithms.isomorphism.GraphMatcher(graph, graph).isomorphisms_iter()
    )
    while unseen:
        representative = min(unseen)
        orbit = set()
        for mapping in automorphisms:
            mapped = tuple(
                sorted(
                    edge_index[
                        tuple(sorted(mapping[vertex] for vertex in edges[edge]))
                    ]
                    for edge in representative
                )
            )
            orbit.add(mapped)
        unseen -= orbit
        representatives.append(representative)
    return tuple(representatives)


def solve_instance(
    graph: nx.Graph,
    roots: tuple[int, int],
    cadical: Path,
    keep_cnf: Path | None,
) -> dict[str, object]:
    cnf, edges = build_good_flow_cnf(graph, roots)
    if keep_cnf is None:
        temporary = tempfile.NamedTemporaryFile(suffix=".cnf", delete=False)
        cnf_path = Path(temporary.name)
        temporary.close()
        remove = True
    else:
        cnf_path = keep_cnf
        remove = False
    cnf_path.write_text(cnf.dimacs(), encoding="ascii")
    try:
        process = subprocess.run(
            [str(cadical), "-q", str(cnf_path)],
            check=False,
            text=True,
            capture_output=True,
        )
        assert process.returncode in (10, 20), process.stderr
        positive = parse_model(process.stdout)
        if positive is None:
            return {
                "roots": list(roots),
                "root_edges": [list(edges[root]) for root in roots],
                "status": "UNSAT_UNCERTIFIED",
                "variables": len(cnf.names),
                "clauses": len(cnf.clauses),
            }
        labels = validate_model(graph, cnf, edges, roots, positive)
        return {
            "roots": list(roots),
            "root_edges": [list(edges[root]) for root in roots],
            "status": "SAT",
            "variables": len(cnf.names),
            "clauses": len(cnf.clauses),
            "labels_hex": [f"{label:02x}" for label in labels],
        }
    finally:
        if remove:
            cnf_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph",
        choices=("tutte-coxeter", "gray"),
        default="tutte-coxeter",
    )
    parser.add_argument("--graph-json", type=Path)
    parser.add_argument(
        "--eliminate-edge",
        type=int,
        help="replace the selected parent edge by its two reduction roots",
    )
    parser.add_argument(
        "--all-eliminations",
        action="store_true",
        help="solve the root instance obtained from every parent edge",
    )
    parser.add_argument(
        "--cadical", type=Path, default=Path("/opt/homebrew/bin/cadical")
    )
    parser.add_argument("--roots", nargs=2, type=int)
    parser.add_argument("--all-independent-orbits", action="store_true")
    parser.add_argument("--keep-cnf", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    graph_name = args.graph
    if args.graph_json is not None:
        graph = json_graph(args.graph_json)
        graph_name = str(args.graph_json)
    else:
        graph = {
            "tutte-coxeter": tutte_coxeter_graph,
            "gray": gray_graph,
        }[args.graph]()

    if args.all_eliminations:
        assert args.eliminate_edge is None
        assert args.roots is None and not args.all_independent_orbits
        assert args.keep_cnf is None
        parent_edges = indexed_edges(graph)
        elimination_results = []
        for index in range(len(parent_edges)):
            reduced, roots, parent_edge = eliminate_edge(graph, index)
            result = solve_instance(
                reduced,
                roots,
                args.cadical,
                None,
            )
            result.update(
                {
                    "eliminated_edge_index": index,
                    "eliminated_parent_edge": list(parent_edge),
                    "reduced_vertices": reduced.number_of_nodes(),
                    "reduced_edges": reduced.number_of_edges(),
                    "reduced_girth": girth(reduced),
                }
            )
            elimination_results.append(result)
        payload = {
            "status": (
                "NO_COUNTEREXAMPLE"
                if all(row["status"] == "SAT" for row in elimination_results)
                else "UNSAT_CANDIDATE_REQUIRES_PROOF"
            ),
            "scope": f"every edge elimination of {graph_name}",
            "parent_vertices": graph.number_of_nodes(),
            "parent_edges": graph.number_of_edges(),
            "parent_girth": girth(graph),
            "parent_graph_sha256": (
                hashlib.sha256(args.graph_json.read_bytes()).hexdigest()
                if args.graph_json is not None
                else None
            ),
            "eliminations": len(elimination_results),
            "results": elimination_results,
        }
        rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if args.output is None:
            print(rendered, end="")
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        return

    eliminated_parent_edge = None
    forced_roots = None
    if args.eliminate_edge is not None:
        graph, forced_roots, eliminated_parent_edge = eliminate_edge(
            graph, args.eliminate_edge
        )

    edges = indexed_edges(graph)
    if forced_roots is not None:
        assert args.roots is None and not args.all_independent_orbits
        root_rows = (forced_roots,)
    elif args.roots:
        roots = (args.roots[0], args.roots[1])
        assert set(edges[roots[0]]).isdisjoint(edges[roots[1]])
        root_rows = (roots,)
    elif args.all_independent_orbits:
        root_rows = edge_pair_orbits(graph, edges, True)
    else:
        parser.error("supply --roots E F or --all-independent-orbits")

    results = [
        solve_instance(
            graph,
            roots,
            args.cadical,
            args.keep_cnf if len(root_rows) == 1 else None,
        )
        for roots in root_rows
    ]
    payload = {
                "status": (
                    "NO_COUNTEREXAMPLE"
                    if all(row["status"] == "SAT" for row in results)
                    else "UNSAT_CANDIDATE_REQUIRES_PROOF"
                ),
                "scope": (
                    f"{graph_name} graph"
                    + (
                        f", reduction of parent edge {args.eliminate_edge}"
                        if args.eliminate_edge is not None
                        else (
                            ", one pair per automorphism orbit"
                            if args.all_independent_orbits
                            else ", prescribed root pair"
                        )
                    )
                ),
                "eliminated_parent_edge": (
                    list(eliminated_parent_edge)
                    if eliminated_parent_edge is not None
                    else None
                ),
                "vertices": graph.number_of_nodes(),
                "edges": graph.number_of_edges(),
                "girth": girth(graph),
                "independent_root_pair_orbits": len(root_rows),
                "results": results,
            }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
