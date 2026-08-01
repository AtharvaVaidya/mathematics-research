#!/usr/bin/env python3
"""Exact SAT search for a D5 factor through two prescribed root edges.

The implementation uses only the Python standard library.  CaDiCaL supplies
SAT solving; every satisfying assignment is independently checked from the
graph semantics before it is reported.

An UNSAT solver answer is never called a counterexample here unless a proof
trace is retained and independently checked outside this driver.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import tempfile
import time


PETERSEN_EDGES = (
    (0, 1), (1, 2), (2, 3), (0, 4), (3, 4),
    (0, 5), (1, 6), (2, 7), (5, 7), (3, 8),
    (5, 8), (6, 8), (4, 9), (6, 9), (7, 9),
)
FOSTER_LCF = (17, -9, 37, -37, 9, -17) * 15
FOSTER_PORTS = (1, 17, 89)


@dataclass(frozen=True)
class Graph:
    n: int
    edges: tuple[tuple[int, int], ...]


def make_graph(n: int, edges: list[tuple[int, int]] | tuple[tuple[int, int], ...],
               *, sort_edges: bool = True) -> Graph:
    normalized = [(min(u, v), max(u, v)) for u, v in edges]
    assert n >= 1
    assert all(0 <= u < n and 0 <= v < n and u != v for u, v in normalized)
    if sort_edges:
        normalized.sort()
    graph = Graph(n, tuple(normalized))
    rows = incidence(graph)
    assert all(len(row) == 3 for row in rows), {
        vertex: len(row) for vertex, row in enumerate(rows) if len(row) != 3
    }
    assert connected(graph)
    return graph


def incidence(graph: Graph) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(graph.n)]
    for edge, (u, v) in enumerate(graph.edges):
        rows[u].append(edge)
        rows[v].append(edge)
    return tuple(tuple(sorted(row)) for row in rows)


def adjacency(graph: Graph) -> tuple[tuple[tuple[int, int], ...], ...]:
    rows: list[list[tuple[int, int]]] = [[] for _ in range(graph.n)]
    for edge, (u, v) in enumerate(graph.edges):
        rows[u].append((v, edge))
        rows[v].append((u, edge))
    return tuple(tuple(row) for row in rows)


def connected(graph: Graph) -> bool:
    adj = adjacency(graph)
    seen = {0}
    todo = [0]
    while todo:
        u = todo.pop()
        for v, _ in adj[u]:
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return len(seen) == graph.n


def bridges(graph: Graph) -> tuple[int, ...]:
    adj = adjacency(graph)
    tin = [-1] * graph.n
    low = [-1] * graph.n
    timer = 0
    answer: list[int] = []

    def dfs(u: int, parent_edge: int) -> None:
        nonlocal timer
        tin[u] = low[u] = timer
        timer += 1
        for v, edge in adj[u]:
            if edge == parent_edge:
                continue
            if tin[v] >= 0:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, edge)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    answer.append(edge)

    dfs(0, -1)
    assert all(value >= 0 for value in tin)
    return tuple(sorted(answer))


def girth(graph: Graph) -> int:
    adj = adjacency(graph)
    best = graph.n + 1
    for source in range(graph.n):
        distance = [-1] * graph.n
        parent_edge = [-1] * graph.n
        distance[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v, edge in adj[u]:
                if distance[v] < 0:
                    distance[v] = distance[u] + 1
                    parent_edge[v] = edge
                    queue.append(v)
                elif parent_edge[u] != edge:
                    best = min(best, distance[u] + distance[v] + 1)
    return best


def graph_digest(graph: Graph) -> str:
    data = str(graph.n) + "\n"
    data += "".join(f"{edge} {u} {v}\n"
                    for edge, (u, v) in enumerate(graph.edges))
    return hashlib.sha256(data.encode("ascii")).hexdigest()


def petersen_graph() -> Graph:
    return make_graph(10, PETERSEN_EDGES)


def foster_edges() -> tuple[tuple[int, int], ...]:
    answer: set[tuple[int, int]] = set()
    for u in range(90):
        v = (u + 1) % 90
        answer.add((min(u, v), max(u, v)))
        v = (u + FOSTER_LCF[u]) % 90
        answer.add((min(u, v), max(u, v)))
    assert len(answer) == 135
    return tuple(sorted(answer))


def petersen_foster_graph() -> Graph:
    base = foster_edges()
    answer: list[tuple[int, int]] = []
    for copy in range(10):
        for u, v in base:
            if 0 in (u, v):
                continue
            answer.append((89 * copy + (u - 1), 89 * copy + (v - 1)))

    used = [0] * 10
    for a, b in PETERSEN_EDGES:
        pa = FOSTER_PORTS[used[a]]
        pb = FOSTER_PORTS[used[b]]
        used[a] += 1
        used[b] += 1
        answer.append((89 * a + (pa - 1), 89 * b + (pb - 1)))
    assert used == [3] * 10
    graph = make_graph(890, answer)
    assert len(graph.edges) == 1335
    return graph


def parse_graph6_row(row: bytes) -> Graph:
    row = row.strip()
    if row.startswith(b">>graph6<<"):
        row = row[len(b">>graph6<<"):]
    values = [byte - 63 for byte in row]
    assert values and all(0 <= value < 64 for value in values)
    if values[0] < 63:
        n = values[0]
        offset = 1
    elif values[1] < 63:
        n = (values[1] << 12) | (values[2] << 6) | values[3]
        offset = 4
    else:
        n = 0
        for value in values[2:8]:
            n = (n << 6) | value
        offset = 8
    bits: list[int] = []
    for value in values[offset:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    need = n * (n - 1) // 2
    assert len(bits) >= need
    edges = []
    index = 0
    for v in range(1, n):
        for u in range(v):
            if bits[index]:
                edges.append((u, v))
            index += 1
    return make_graph(n, edges)


def graph6_file(path: Path, row_number: int) -> Graph:
    rows = [row for row in path.read_bytes().splitlines() if row.strip()]
    assert 0 <= row_number < len(rows)
    return parse_graph6_row(rows[row_number])


def json_graph(path: Path) -> Graph:
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data["vertices"], int)
    edges = []
    for row in data["edges"]:
        if isinstance(row, dict):
            edges.append((int(row["u"]), int(row["v"])))
        else:
            edges.append((int(row[0]), int(row[1])))
    return make_graph(data["vertices"], edges)


def eliminate_edge(graph: Graph, edge_index: int
                   ) -> tuple[Graph, tuple[int, int], tuple[int, int]]:
    assert 0 <= edge_index < len(graph.edges)
    rows = incidence(graph)
    u, v = graph.edges[edge_index]
    u_other = [edge for edge in rows[u] if edge != edge_index]
    v_other = [edge for edge in rows[v] if edge != edge_index]
    assert len(u_other) == len(v_other) == 2

    def other_end(edge: int, vertex: int) -> int:
        a, b = graph.edges[edge]
        return b if a == vertex else a

    u_side = tuple(other_end(edge, u) for edge in u_other)
    v_side = tuple(other_end(edge, v) for edge in v_other)
    assert len(set(u_side + v_side)) == 4

    retained = [edge for edge in graph.edges if u not in edge and v not in edge]
    old_vertices = [vertex for vertex in range(graph.n) if vertex not in (u, v)]
    relabel = {old: new for new, old in enumerate(old_vertices)}
    decorated: list[tuple[int, int, str]] = [
        (min(relabel[a], relabel[b]), max(relabel[a], relabel[b]), "old")
        for a, b in retained
    ]
    decorated.append((
        min(relabel[u_side[0]], relabel[u_side[1]]),
        max(relabel[u_side[0]], relabel[u_side[1]]),
        "root-u",
    ))
    decorated.append((
        min(relabel[v_side[0]], relabel[v_side[1]]),
        max(relabel[v_side[0]], relabel[v_side[1]]),
        "root-v",
    ))
    decorated.sort()
    roots = (
        next(i for i, row in enumerate(decorated) if row[2] == "root-u"),
        next(i for i, row in enumerate(decorated) if row[2] == "root-v"),
    )
    reduced = make_graph(graph.n - 2, [(a, b) for a, b, _ in decorated],
                         sort_edges=False)
    assert set(reduced.edges[roots[0]]).isdisjoint(reduced.edges[roots[1]])
    return reduced, roots, (u, v)


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

    def add_xor(self, variables: tuple[int, ...] | list[int], rhs: int) -> None:
        assert rhs in (0, 1)
        for assignment in product((0, 1), repeat=len(variables)):
            if sum(assignment) % 2 != rhs:
                self.add(*(variable if bit == 0 else -variable
                           for variable, bit in zip(variables, assignment)))

    def dimacs(self) -> str:
        rows = [f"p cnf {len(self.names)} {len(self.clauses)}"]
        rows.extend(" ".join(map(str, clause)) + " 0"
                    for clause in self.clauses)
        return "\n".join(rows) + "\n"


def build_cnf(graph: Graph, roots: tuple[int, int],
              root_symmetry_break: bool = False
              ) -> tuple[CNF, dict[tuple[int, int, int], int]]:
    rows = incidence(graph)
    m = len(graph.edges)
    assert roots[0] != roots[1]
    assert set(graph.edges[roots[0]]).isdisjoint(graph.edges[roots[1]])
    cnf = CNF()

    for edge in range(m):
        variables = [cnf.var("x", edge, coordinate) for coordinate in range(5)]
        for triple in combinations(variables, 3):
            cnf.add(*(-variable for variable in triple))
        for four in combinations(variables, 4):
            cnf.add(*four)

    # The stabilizer of the coordinate pair {0,1} is transitive on the six
    # possible crossing labels at a root.  Hence fixing L(r)={0,2} preserves
    # satisfiability and removes a factor-six coordinate symmetry.
    if root_symmetry_break:
        first_root = roots[0]
        fixed = (1, 0, 1, 0, 0)
        for coordinate, value in enumerate(fixed):
            variable = cnf.var("x", first_root, coordinate)
            cnf.add(variable if value else -variable)

    for row in rows:
        assert len(row) == 3
        for coordinate in range(5):
            cnf.add_xor([cnf.var("x", edge, coordinate) for edge in row], 0)

    for edge in range(m):
        cnf.add_xor([
            cnf.var("x", edge, 0),
            cnf.var("x", edge, 1),
            cnf.var("y", edge),
        ], 0)

    transition: dict[tuple[int, int, int], int] = {}
    touching: list[list[int]] = [[] for _ in range(m)]
    for vertex, row in enumerate(rows):
        for first, second in combinations(row, 2):
            z = cnf.var("z", vertex, first, second)
            transition[(vertex, first, second)] = z
            cnf.add(-z, cnf.var("y", first))
            cnf.add(-z, cnf.var("y", second))
            touching[first].append(z)
            touching[second].append(z)

    for edge, variables in enumerate(touching):
        assert len(variables) == 4
        cnf.add_xor(variables, int(edge in roots))

    expected_variables = 8 * m
    expected_clauses = 133 * m // 3 + (5 if root_symmetry_break else 0)
    assert len(cnf.names) == expected_variables
    assert len(cnf.clauses) == expected_clauses
    return cnf, transition


def parse_model(output: str) -> set[int] | None:
    if "s UNSATISFIABLE" in output:
        return None
    assert "s SATISFIABLE" in output, output[-4000:]
    positive: set[int] = set()
    for row in output.splitlines():
        if row.startswith("v "):
            for token in row.split()[1:]:
                literal = int(token)
                if literal > 0:
                    positive.add(literal)
    return positive


def component_contains(adjacency_rows: list[set[int]], roots: tuple[int, int]
                       ) -> tuple[bool, tuple[int, ...]]:
    parent = {roots[0]: -1}
    queue = deque([roots[0]])
    while queue and roots[1] not in parent:
        edge = queue.popleft()
        for other in adjacency_rows[edge]:
            if other not in parent:
                parent[other] = edge
                queue.append(other)
    if roots[1] not in parent:
        return False, ()
    path = []
    current = roots[1]
    while current >= 0:
        path.append(current)
        current = parent[current]
    path.reverse()
    return True, tuple(path)


def validate_model(graph: Graph, roots: tuple[int, int], cnf: CNF,
                   transition: dict[tuple[int, int, int], int],
                   positive: set[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    m = len(graph.edges)
    rows = incidence(graph)
    labels = tuple(
        sum(1 << coordinate for coordinate in range(5)
            if cnf.names[("x", edge, coordinate)] in positive)
        for edge in range(m)
    )
    assert all(label.bit_count() == 2 for label in labels)
    for row in rows:
        assert labels[row[0]] ^ labels[row[1]] ^ labels[row[2]] == 0

    y = tuple(cnf.names[("y", edge)] in positive for edge in range(m))
    assert all(y[edge] == bool(
        ((labels[edge] >> 0) & 1) ^ ((labels[edge] >> 1) & 1))
        for edge in range(m))

    selected = {
        key for key, variable in transition.items() if variable in positive
    }
    degree = [0] * m
    selected_adjacency = [set() for _ in range(m)]
    for _, first, second in selected:
        assert y[first] and y[second]
        degree[first] ^= 1
        degree[second] ^= 1
        selected_adjacency[first].add(second)
        selected_adjacency[second].add(first)
    assert tuple(i for i, bit in enumerate(degree) if bit) == tuple(sorted(roots))
    selected_ok, selected_path = component_contains(selected_adjacency, roots)
    assert selected_ok

    full_adjacency = [set() for _ in range(m)]
    for row in rows:
        active = [edge for edge in row if y[edge]]
        assert len(active) in (0, 2)
        if active:
            first, second = active
            full_adjacency[first].add(second)
            full_adjacency[second].add(first)
    full_ok, _ = component_contains(full_adjacency, roots)
    assert full_ok
    return labels, selected_path


def solve_instance(graph: Graph, roots: tuple[int, int], cadical: Path,
                   keep_cnf: Path | None = None,
                   proof_out: Path | None = None,
                   include_labels: bool = False,
                   root_symmetry_break: bool = False,
                   include_timing: bool = False) -> dict[str, object]:
    cnf, transition = build_cnf(graph, roots, root_symmetry_break)
    remove_cnf = keep_cnf is None
    if keep_cnf is None:
        handle = tempfile.NamedTemporaryFile(suffix=".cnf", delete=False)
        cnf_path = Path(handle.name)
        handle.close()
    else:
        cnf_path = keep_cnf
        cnf_path.parent.mkdir(parents=True, exist_ok=True)
    cnf_path.write_text(cnf.dimacs(), encoding="ascii")
    command = [str(cadical), "--quiet", "--checkproof=1"]
    if proof_out is not None:
        proof_out.parent.mkdir(parents=True, exist_ok=True)
        command.append("--no-binary")
    command.append(str(cnf_path))
    if proof_out is not None:
        command.append(str(proof_out))

    started = time.monotonic()
    try:
        process = subprocess.run(command, check=False, text=True,
                                 capture_output=True)
        elapsed = time.monotonic() - started
        assert process.returncode in (10, 20), process.stderr[-4000:]
        positive = parse_model(process.stdout)
        base: dict[str, object] = {
            "roots": list(roots),
            "root_edges": [list(graph.edges[root]) for root in roots],
            "variables": len(cnf.names),
            "clauses": len(cnf.clauses),
            "graph_sha256": graph_digest(graph),
            "cnf_sha256": hashlib.sha256(cnf_path.read_bytes()).hexdigest(),
        }
        if include_timing:
            base["seconds"] = round(elapsed, 6)
        if positive is None:
            base["status"] = (
                "UNSAT_TRACE_GENERATED_NOT_INDEPENDENTLY_CHECKED"
                if proof_out is not None else "UNSAT_UNCERTIFIED"
            )
            if proof_out is not None:
                base["proof_path"] = str(proof_out)
                base["proof_sha256"] = hashlib.sha256(
                    proof_out.read_bytes()).hexdigest()
            return base

        labels, path = validate_model(
            graph, roots, cnf, transition, positive)
        if proof_out is not None and proof_out.exists():
            proof_out.unlink()
        base.update({
            "status": "SAT_MODEL_CHECKED",
            "labels_sha256": hashlib.sha256(bytes(labels)).hexdigest(),
            "selected_transition_path": list(path),
        })
        if include_labels:
            base["labels"] = list(labels)
        return base
    finally:
        if remove_cnf:
            cnf_path.unlink(missing_ok=True)


def graph_metadata(graph: Graph) -> dict[str, object]:
    found_bridges = bridges(graph)
    return {
        "vertices": graph.n,
        "edges": len(graph.edges),
        "girth": girth(graph),
        "bridge_edge_indices": list(found_bridges),
        "bridgeless": not found_bridges,
        "parallel_edge_pairs": len(graph.edges) - len(set(graph.edges)),
        "loops": 0,
        "graph_sha256": graph_digest(graph),
    }


def render(payload: dict[str, object], output: Path | None) -> None:
    data = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if output is None:
        print(data, end="")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(data, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    sources = parser.add_mutually_exclusive_group()
    sources.add_argument("--petersen", action="store_true")
    sources.add_argument("--petersen-foster", action="store_true")
    sources.add_argument("--graph-json", type=Path)
    sources.add_argument("--graph6", type=Path)
    parser.add_argument("--graph6-row", type=int, default=0)

    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--roots", nargs=2, type=int)
    modes.add_argument("--eliminate-edge", type=int)
    modes.add_argument("--all-eliminations", action="store_true")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int)

    parser.add_argument("--cadical", type=Path,
                        default=Path("/opt/homebrew/bin/cadical"))
    parser.add_argument("--keep-cnf", type=Path)
    parser.add_argument("--proof-out", type=Path)
    parser.add_argument("--cnf-dir", type=Path)
    parser.add_argument("--proof-dir", type=Path)
    parser.add_argument("--include-labels", action="store_true")
    parser.add_argument("--include-timing", action="store_true")
    parser.add_argument("--root-symmetry-break", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.petersen_foster:
        graph = petersen_foster_graph()
        source = "Petersen graph with Foster three-pole substitutions"
    elif args.graph_json:
        graph = json_graph(args.graph_json)
        source = str(args.graph_json)
    elif args.graph6:
        graph = graph6_file(args.graph6, args.graph6_row)
        source = f"{args.graph6}, row {args.graph6_row}"
    else:
        graph = petersen_graph()
        source = "Petersen graph"

    assert args.cadical.exists(), args.cadical
    parent_metadata = graph_metadata(graph)

    if args.all_eliminations:
        assert args.keep_cnf is None and args.proof_out is None
        stop = len(graph.edges)
        if args.limit is not None:
            stop = min(stop, args.start + args.limit)
        assert 0 <= args.start < stop <= len(graph.edges)
        results = []
        for index in range(args.start, stop):
            reduced, roots, parent_edge = eliminate_edge(graph, index)
            cnf_path = (
                args.cnf_dir / f"elimination-{index:04d}.cnf"
                if args.cnf_dir is not None else None
            )
            proof_path = (
                args.proof_dir / f"elimination-{index:04d}.drat"
                if args.proof_dir is not None else None
            )
            result = solve_instance(
                reduced, roots, args.cadical, cnf_path, proof_path,
                args.include_labels, args.root_symmetry_break,
                args.include_timing)
            result.update({
                "eliminated_edge_index": index,
                "eliminated_parent_edge": list(parent_edge),
                "reduced_metadata": graph_metadata(reduced),
            })
            results.append(result)
        payload = {
            "status": (
                "ALL_SAT_MODELS_CHECKED"
                if all(row["status"] == "SAT_MODEL_CHECKED" for row in results)
                else "UNSAT_CANDIDATE_REQUIRES_INDEPENDENT_PROOF_CHECK"
            ),
            "source": source,
            "parent_metadata": parent_metadata,
            "elimination_range": [args.start, stop],
            "results": results,
        }
        render(payload, args.output)
        return

    eliminated = None
    if args.eliminate_edge is not None:
        graph, roots, parent_edge = eliminate_edge(graph, args.eliminate_edge)
        eliminated = {
            "edge_index": args.eliminate_edge,
            "edge": list(parent_edge),
            "parent_metadata": parent_metadata,
        }
    else:
        assert args.roots is not None
        roots = tuple(args.roots)
        assert len(roots) == 2
        assert 0 <= roots[0] < len(graph.edges)
        assert 0 <= roots[1] < len(graph.edges)
        assert set(graph.edges[roots[0]]).isdisjoint(graph.edges[roots[1]])

    result = solve_instance(
        graph, roots, args.cadical, args.keep_cnf, args.proof_out,
        args.include_labels, args.root_symmetry_break, args.include_timing)
    payload = {
        "status": result["status"],
        "source": source,
        "elimination": eliminated,
        "graph_metadata": graph_metadata(graph),
        "result": result,
    }
    render(payload, args.output)


if __name__ == "__main__":
    main()
