"""Exact graph checks and SAT encodings for verifier A.

This module intentionally uses only the Python standard library.  All graph
indices are zero-based; the five CDC coordinates printed in artifacts are
one-based.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union


FORMAT = "five-cdc-multigraph-v1"
COORDINATES = 5


class GraphFormatError(ValueError):
    """The graph JSON is not a witness in the specified format."""


class ModelFormatError(ValueError):
    """The solver model is malformed or not a SAT model."""


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


@dataclass(frozen=True, order=True)
class Edge:
    id: int
    u: int
    v: int

    @property
    def is_loop(self) -> bool:
        return self.u == self.v


@dataclass(frozen=True)
class Graph:
    vertices: int
    edges: Tuple[Edge, ...]

    def as_object(self) -> dict:
        return {
            "format": FORMAT,
            "vertices": self.vertices,
            "edges": [
                {"id": edge.id, "u": edge.u, "v": edge.v}
                for edge in self.edges
            ],
        }


@dataclass(frozen=True)
class PremiseResult:
    components: Tuple[Tuple[int, ...], ...]
    connected: bool
    bridge_ids: Tuple[int, ...]

    @property
    def bridgeless(self) -> bool:
        return not self.bridge_ids

    def as_object(self) -> dict:
        return {
            "bridgeless": self.bridgeless,
            "bridge_ids": list(self.bridge_ids),
            "components": [list(component) for component in self.components],
            "connected": self.connected,
        }


@dataclass(frozen=True)
class ModelResult:
    valid: bool
    exact_two_failures: Tuple[int, ...]
    parity_failures: Tuple[Tuple[int, int], ...]

    def as_object(self) -> dict:
        return {
            "valid": self.valid,
            "exact_two_failures": list(self.exact_two_failures),
            "parity_failures": [
                {"vertex": vertex, "coordinate": coordinate}
                for vertex, coordinate in self.parity_failures
            ],
        }


@dataclass(frozen=True)
class XorGate:
    output: int
    left: int
    right: int
    vertex: int
    coordinate: int
    step: int


@dataclass(frozen=True)
class CNFEncoding:
    variables: int
    base_variables: int
    clauses: Tuple[Tuple[int, ...], ...]
    gates: Tuple[XorGate, ...]
    forced_false: Tuple[int, ...]
    comments: Tuple[str, ...]


def _reject_duplicate_keys(pairs: Iterable[Tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise GraphFormatError("duplicate JSON object key: {!r}".format(key))
        result[key] = value
    return result


def parse_graph_text(text: str) -> Graph:
    """Parse and strictly validate a graph witness.

    Edge IDs must equal their positions and endpoints must be ordered.  This
    makes indexed representation deterministic without pretending to solve
    graph isomorphism.
    """

    try:
        obj = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except GraphFormatError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise GraphFormatError("invalid JSON: {}".format(exc)) from exc

    if not isinstance(obj, dict):
        raise GraphFormatError("top level must be a JSON object")
    expected_top = {"format", "vertices", "edges"}
    if set(obj) != expected_top:
        raise GraphFormatError(
            "top-level keys must be exactly {}".format(sorted(expected_top))
        )
    if obj["format"] != FORMAT:
        raise GraphFormatError("format must be {!r}".format(FORMAT))
    n = obj["vertices"]
    if not _is_int(n) or n < 0:
        raise GraphFormatError("vertices must be a nonnegative integer")
    raw_edges = obj["edges"]
    if not isinstance(raw_edges, list):
        raise GraphFormatError("edges must be an array")

    edges = []
    expected_edge = {"id", "u", "v"}
    for position, raw in enumerate(raw_edges):
        if not isinstance(raw, dict) or set(raw) != expected_edge:
            raise GraphFormatError(
                "edge {} keys must be exactly {}".format(
                    position, sorted(expected_edge)
                )
            )
        edge_id, u, v = raw["id"], raw["u"], raw["v"]
        if not all(_is_int(value) for value in (edge_id, u, v)):
            raise GraphFormatError("edge {} fields must be integers".format(position))
        if edge_id != position:
            raise GraphFormatError(
                "edge id {} must equal array position {}".format(edge_id, position)
            )
        if not (0 <= u < n and 0 <= v < n):
            raise GraphFormatError(
                "edge {} endpoint outside 0..{}".format(position, n - 1)
            )
        if u > v:
            raise GraphFormatError(
                "edge {} endpoints must be ordered with u <= v".format(position)
            )
        edges.append(Edge(edge_id, u, v))
    return Graph(n, tuple(edges))


def load_graph(path: Union[Path, str]) -> Graph:
    return parse_graph_text(Path(path).read_text(encoding="utf-8"))


def canonical_graph_bytes(graph: Graph) -> bytes:
    """Return the one canonical UTF-8 serialization for this indexed graph."""

    return (
        json.dumps(
            graph.as_object(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
        + "\n"
    ).encode("ascii")


def graph_sha256(graph: Graph) -> str:
    return sha256(canonical_graph_bytes(graph)).hexdigest()


def _adjacency_without_loops(graph: Graph) -> List[List[Tuple[int, int]]]:
    adjacency: List[List[Tuple[int, int]]] = [
        [] for _ in range(graph.vertices)
    ]
    for edge in graph.edges:
        if edge.is_loop:
            continue
        adjacency[edge.u].append((edge.v, edge.id))
        adjacency[edge.v].append((edge.u, edge.id))
    for entries in adjacency:
        entries.sort(key=lambda item: (item[1], item[0]))
    return adjacency


def check_premises(graph: Graph) -> PremiseResult:
    """Compute components and bridges in an undirected multigraph.

    The DFS skips only the parent *edge ID*, not the parent endpoint.  Thus a
    second parallel edge is a back edge, as required.  Loops are omitted from
    DFS: they connect no components and can never be bridges.
    """

    adjacency = _adjacency_without_loops(graph)
    n = graph.vertices
    discovery = [-1] * n
    low = [-1] * n
    tick = 0
    bridges: List[int] = []

    # Iterative Tarjan DFS avoids depending on Python's recursion limit.
    for root in range(n):
        if discovery[root] >= 0:
            continue
        discovery[root] = low[root] = tick
        tick += 1
        # Each mutable frame is [vertex, parent_vertex, parent_edge, next_index].
        stack = [[root, -1, -1, 0]]
        while stack:
            vertex, parent, parent_edge, next_index = stack[-1]
            if next_index < len(adjacency[vertex]):
                other, edge_id = adjacency[vertex][next_index]
                stack[-1][3] += 1
                if edge_id == parent_edge:
                    continue
                if discovery[other] < 0:
                    discovery[other] = low[other] = tick
                    tick += 1
                    stack.append([other, vertex, edge_id, 0])
                else:
                    low[vertex] = min(low[vertex], discovery[other])
                continue
            stack.pop()
            if parent >= 0:
                low[parent] = min(low[parent], low[vertex])
                if low[vertex] > discovery[parent]:
                    bridges.append(parent_edge)

    seen = [False] * n
    components: List[Tuple[int, ...]] = []
    for root in range(n):
        if seen[root]:
            continue
        stack = [root]
        seen[root] = True
        component = []
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for other, _edge_id in adjacency[vertex]:
                if not seen[other]:
                    seen[other] = True
                    stack.append(other)
        components.append(tuple(sorted(component)))
    components.sort()
    return PremiseResult(
        tuple(components),
        len(components) == 1,
        tuple(sorted(bridges)),
    )


def x_variable(edge_id: int, coordinate: int) -> int:
    """Map zero-based edge ID and one-based coordinate to DIMACS variable."""

    if edge_id < 0 or not (1 <= coordinate <= COORDINATES):
        raise ValueError("invalid edge or coordinate")
    return COORDINATES * edge_id + coordinate


def parity_variables(
    graph: Graph, vertex: int, coordinate: int
) -> Tuple[int, ...]:
    """Variables occurring with odd incidence multiplicity.

    A non-loop edge occurs once at each endpoint.  A loop occurs twice at its
    endpoint, so its two copies cancel over GF(2).
    """

    result = []
    for edge in graph.edges:
        if edge.is_loop:
            continue
        if edge.u == vertex or edge.v == vertex:
            result.append(x_variable(edge.id, coordinate))
    return tuple(result)


def _xor_gate_clauses(left: int, right: int, output: int) -> Tuple[Tuple[int, ...], ...]:
    """CNF for output iff (left XOR right)."""

    return (
        (left, right, -output),
        (-left, -right, -output),
        (left, -right, output),
        (-left, right, output),
    )


def build_cnf(graph: Graph) -> CNFEncoding:
    """Build a projection-equivalent CNF for the original x semantics."""

    base_variables = COORDINATES * len(graph.edges)
    next_variable = base_variables + 1
    clauses: List[Tuple[int, ...]] = []
    gates: List[XorGate] = []
    forced_false: List[int] = []
    comments = [
        "five-cdc-cnf-v1",
        "graph-sha256 {}".format(graph_sha256(graph)),
        "coordinates are 1..5; vertices and edge ids are 0-based",
    ]

    for edge in graph.edges:
        variables = tuple(
            x_variable(edge.id, coordinate)
            for coordinate in range(1, COORDINATES + 1)
        )
        for triple in combinations(variables, 3):
            clauses.append(tuple(-variable for variable in triple))
        for quadruple in combinations(variables, 4):
            clauses.append(tuple(quadruple))
        for coordinate, variable in enumerate(variables, 1):
            comments.append(
                "var {} x edge {} coordinate {}".format(
                    variable, edge.id, coordinate
                )
            )

    for vertex in range(graph.vertices):
        for coordinate in range(1, COORDINATES + 1):
            variables = parity_variables(graph, vertex, coordinate)
            if not variables:
                continue
            if len(variables) == 1:
                clauses.append((-variables[0],))
                forced_false.append(variables[0])
                continue
            accumulator = variables[0]
            for step, variable in enumerate(variables[1:], 1):
                output = next_variable
                next_variable += 1
                gate = XorGate(
                    output, accumulator, variable, vertex, coordinate, step
                )
                gates.append(gate)
                clauses.extend(_xor_gate_clauses(accumulator, variable, output))
                comments.append(
                    "var {} parity vertex {} coordinate {} step {}".format(
                        output, vertex, coordinate, step
                    )
                )
                accumulator = output
            clauses.append((-accumulator,))
            forced_false.append(accumulator)

    return CNFEncoding(
        variables=next_variable - 1,
        base_variables=base_variables,
        clauses=tuple(clauses),
        gates=tuple(gates),
        forced_false=tuple(forced_false),
        comments=tuple(comments),
    )


def render_cnf(graph: Graph) -> str:
    encoding = build_cnf(graph)
    lines = ["c " + comment for comment in encoding.comments]
    lines.append("p cnf {} {}".format(encoding.variables, len(encoding.clauses)))
    lines.extend(
        "{} 0".format(" ".join(str(literal) for literal in clause))
        if clause
        else "0"
        for clause in encoding.clauses
    )
    return "\n".join(lines) + "\n"


def _exact_two_clauses(graph: Graph) -> List[Tuple[int, ...]]:
    clauses: List[Tuple[int, ...]] = []
    for edge in graph.edges:
        variables = tuple(
            x_variable(edge.id, coordinate)
            for coordinate in range(1, COORDINATES + 1)
        )
        clauses.extend(
            tuple(-variable for variable in triple)
            for triple in combinations(variables, 3)
        )
        clauses.extend(tuple(group) for group in combinations(variables, 4))
    return clauses


def render_xor_dimacs(graph: Graph) -> str:
    """Render CryptoMiniSat extended DIMACS.

    CryptoMiniSat interprets an ``x`` row as XOR(literals) = true.  Negating
    the first literal therefore encodes XOR(positive variables) = false.
    Empty even-parity equations are tautologies and are omitted.
    """

    ordinary = _exact_two_clauses(graph)
    xor_rows: List[Tuple[int, ...]] = []
    for vertex in range(graph.vertices):
        for coordinate in range(1, COORDINATES + 1):
            variables = parity_variables(graph, vertex, coordinate)
            if variables:
                xor_rows.append((-variables[0],) + variables[1:])
    lines = [
        "c five-cdc-xor-dimacs-v1",
        "c graph-sha256 {}".format(graph_sha256(graph)),
        "c x rows use CryptoMiniSat convention XOR(literals)=true",
        "p cnf {} {}".format(
            COORDINATES * len(graph.edges), len(ordinary) + len(xor_rows)
        ),
    ]
    lines.extend(
        "{} 0".format(" ".join(str(literal) for literal in clause))
        for clause in ordinary
    )
    lines.extend(
        "x {} 0".format(" ".join(str(literal) for literal in row))
        for row in xor_rows
    )
    return "\n".join(lines) + "\n"


def parse_model_text(
    text: str,
    required_base_variables: int,
    maximum_variable: Optional[int] = None,
) -> Dict[int, bool]:
    """Parse a DIMACS competition model and require every base variable."""

    if required_base_variables < 0:
        raise ValueError("negative base variable count")
    if maximum_variable is None:
        maximum_variable = required_base_variables
    assignment: Dict[int, bool] = {}
    status = None
    saw_model_data = False
    for line_number, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("c"):
            continue
        tokens = line.split()
        if tokens[0] == "s":
            if len(tokens) != 2:
                raise ModelFormatError(
                    "line {}: malformed status line".format(line_number)
                )
            status = tokens[1].upper()
            continue
        if len(tokens) == 1 and tokens[0].upper() in {
            "SAT",
            "SATISFIABLE",
            "UNSAT",
            "UNSATISFIABLE",
            "UNKNOWN",
        }:
            status = tokens[0].upper()
            continue
        if tokens[0] == "v":
            tokens = tokens[1:]
        saw_model_data = True
        for token in tokens:
            try:
                literal = int(token, 10)
            except ValueError as exc:
                raise ModelFormatError(
                    "line {}: noninteger model token {!r}".format(
                        line_number, token
                    )
                ) from exc
            if literal == 0:
                continue
            variable = abs(literal)
            if variable > maximum_variable:
                raise ModelFormatError(
                    "line {}: variable {} exceeds encoding maximum {}".format(
                        line_number, variable, maximum_variable
                    )
                )
            value = literal > 0
            if variable in assignment and assignment[variable] != value:
                raise ModelFormatError(
                    "contradictory values for variable {}".format(variable)
                )
            assignment[variable] = value
    if status in {"UNSAT", "UNSATISFIABLE", "UNKNOWN"}:
        raise ModelFormatError("input does not claim SAT: {}".format(status))
    if not saw_model_data and required_base_variables:
        raise ModelFormatError("no model literals found")
    missing = [
        variable
        for variable in range(1, required_base_variables + 1)
        if variable not in assignment
    ]
    if missing:
        preview = ",".join(str(variable) for variable in missing[:8])
        suffix = "..." if len(missing) > 8 else ""
        raise ModelFormatError("missing base variables: {}{}".format(preview, suffix))
    return assignment


def check_assignment(
    graph: Graph, assignment: Mapping[int, bool]
) -> ModelResult:
    """Check a model directly against exact-two and degree parity semantics."""

    exact_two_failures = []
    for edge in graph.edges:
        count = sum(
            bool(assignment.get(x_variable(edge.id, coordinate), False))
            for coordinate in range(1, COORDINATES + 1)
        )
        if count != 2:
            exact_two_failures.append(edge.id)

    parity_failures = []
    for vertex in range(graph.vertices):
        for coordinate in range(1, COORDINATES + 1):
            parity = 0
            for edge in graph.edges:
                value = bool(
                    assignment.get(x_variable(edge.id, coordinate), False)
                )
                if edge.u == vertex:
                    parity ^= int(value)
                if edge.v == vertex:
                    parity ^= int(value)
            if parity:
                parity_failures.append((vertex, coordinate))
    return ModelResult(
        not exact_two_failures and not parity_failures,
        tuple(exact_two_failures),
        tuple(parity_failures),
    )


def clauses_satisfied(
    clauses: Sequence[Sequence[int]], assignment: Mapping[int, bool]
) -> bool:
    """Evaluate a total assignment on CNF clauses (used by unit tests/tools)."""

    for clause in clauses:
        if not any(
            assignment.get(abs(literal), False) == (literal > 0)
            for literal in clause
        ):
            return False
    return True


def extend_gate_assignment(
    encoding: CNFEncoding, base_assignment: Mapping[int, bool]
) -> Dict[int, bool]:
    """Deterministically extend base values through all parity XOR gates."""

    result = dict(base_assignment)
    for gate in encoding.gates:
        if gate.left not in result or gate.right not in result:
            raise ValueError("base assignment is incomplete for parity gates")
        result[gate.output] = result[gate.left] ^ result[gate.right]
    return result
