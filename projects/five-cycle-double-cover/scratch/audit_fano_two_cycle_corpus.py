#!/usr/bin/env python3
"""Audit the exact two-cycle Fano line-cleaning normal form on a corpus.

For every Fano line L, the script builds an ordinary CNF for two binary
cycles p,q such that

  * p or q contains every edge whose flow value is in L; and
  * on every component W of that line factor,
        XOR_{e in delta(W)} (p_e AND q_e) = 0.

CaDiCaL is used only to obtain a model.  The model is then checked directly
against these graph semantics, and the corresponding nowhere-zero
three-bit flow is reconstructed and checked.  The ordinary CNF form is
also suitable for a proof-producing UNSAT rerun if a negative instance is
ever found.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from collections import deque
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = (
    ROOT
    / "search"
    / "connected-one-switch-countermodel-40v-20260726"
    / "construction.json",
    ROOT
    / "search"
    / "fano-pure-merge-one-switch-countermodel-46v-20260726"
    / "construction.json",
)
LINES = tuple(
    sorted(
        {
            tuple(sorted((first, second, first ^ second)))
            for first, second in combinations(range(1, 8), 2)
        }
    )
)


@dataclass(frozen=True)
class Instance:
    name: str
    order: int
    edges: tuple[tuple[int, int], ...]
    flow: tuple[int, ...]


class CNF:
    def __init__(self, variables: int) -> None:
        self.variables = variables
        self.clauses: list[tuple[int, ...]] = []

    def fresh(self) -> int:
        self.variables += 1
        return self.variables

    def add(self, *literals: int) -> None:
        assert literals
        self.clauses.append(tuple(literals))

    def xor_gate(self, first: int, second: int) -> int:
        """Return a fresh variable equal to first XOR second."""

        output = self.fresh()
        self.add(first, second, -output)
        self.add(first, -second, output)
        self.add(-first, second, output)
        self.add(-first, -second, -output)
        return output

    def even(self, variables: list[int]) -> None:
        if not variables:
            return
        if len(variables) == 1:
            self.add(-variables[0])
            return
        parity = self.xor_gate(variables[0], variables[1])
        for variable in variables[2:]:
            parity = self.xor_gate(parity, variable)
        self.add(-parity)

    def render(self) -> str:
        lines = [f"p cnf {self.variables} {len(self.clauses)}"]
        lines.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return "\n".join(lines) + "\n"


def load_instance(path: Path) -> Instance:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "expanded_graph" in data:
        graph = data["expanded_graph"]
    else:
        graph = data
    edges = tuple(tuple(map(int, edge)) for edge in graph["edges"])
    flow = tuple(map(int, graph["flow_values_by_edge"]))
    order = int(graph["vertices"])
    assert len(edges) == len(flow)
    return Instance(path.parent.name, order, edges, flow)


def factor_components(
    instance: Instance, line_edges: set[int]
) -> tuple[frozenset[int], ...]:
    adjacency = [[] for _ in range(instance.order)]
    for edge in line_edges:
        first, second = instance.edges[edge]
        adjacency[first].append(second)
        adjacency[second].append(first)
    unseen = set(range(instance.order))
    output: list[frozenset[int]] = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        output.append(frozenset(component))
    return tuple(output)


def cut(instance: Instance, shore: frozenset[int]) -> list[int]:
    return [
        edge
        for edge, (first, second) in enumerate(instance.edges)
        if (first in shore) != (second in shore)
    ]


def graph_audit(instance: Instance) -> tuple[tuple[int, ...], ...]:
    incident: list[list[int]] = [[] for _ in range(instance.order)]
    assert all(
        0 <= first < second < instance.order
        for first, second in instance.edges
    )
    assert len(set(instance.edges)) == len(instance.edges)
    for edge, (first, second) in enumerate(instance.edges):
        incident[first].append(edge)
        incident[second].append(edge)
    assert all(len(row) == 3 for row in incident)
    assert all(1 <= value <= 7 for value in instance.flow)
    for row in incident:
        assert (
            instance.flow[row[0]]
            ^ instance.flow[row[1]]
            ^ instance.flow[row[2]]
        ) == 0
    return tuple(tuple(row) for row in incident)


def build_cnf(
    instance: Instance,
    incident: tuple[tuple[int, ...], ...],
    line: tuple[int, int, int],
    components: tuple[frozenset[int], ...],
) -> tuple[CNF, tuple[int, ...], tuple[int, ...]]:
    edge_count = len(instance.edges)
    p = tuple(edge + 1 for edge in range(edge_count))
    q = tuple(edge_count + edge + 1 for edge in range(edge_count))
    cnf = CNF(2 * edge_count)

    # A cubic vertex has even selected degree iff it has degree zero or two.
    for row in incident:
        for variables in (
            [p[edge] for edge in row],
            [q[edge] for edge in row],
        ):
            cnf.add(variables[0], variables[1], -variables[2])
            cnf.add(variables[0], -variables[1], variables[2])
            cnf.add(-variables[0], variables[1], variables[2])
            cnf.add(-variables[0], -variables[1], -variables[2])

    line_set = set(line)
    for edge, value in enumerate(instance.flow):
        if value in line_set:
            cnf.add(p[edge], q[edge])

    for component in components:
        products = []
        for edge in cut(instance, component):
            product = cnf.fresh()
            # product <-> p_e AND q_e.
            cnf.add(-product, p[edge])
            cnf.add(-product, q[edge])
            cnf.add(product, -p[edge], -q[edge])
            products.append(product)
        cnf.even(products)
    return cnf, p, q


def solve(cnf: CNF, solver: str) -> tuple[bool, set[int]]:
    with tempfile.TemporaryDirectory(prefix="fano-two-cycle-") as directory:
        cnf_path = Path(directory) / "instance.cnf"
        cnf_path.write_text(cnf.render(), encoding="ascii")
        process = subprocess.run(
            [solver, "--quiet", str(cnf_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
    output = process.stdout + "\n" + process.stderr
    if process.returncode == 20:
        return False, set()
    assert process.returncode == 10, output
    positive: set[int] = set()
    for line in output.splitlines():
        if line.startswith("v "):
            positive.update(
                literal
                for literal in map(int, line.split()[1:])
                if literal > 0
            )
    return True, positive


def check_model(
    instance: Instance,
    incident: tuple[tuple[int, ...], ...],
    line: tuple[int, int, int],
    components: tuple[frozenset[int], ...],
    p_variables: tuple[int, ...],
    q_variables: tuple[int, ...],
    positive: set[int],
) -> None:
    p = tuple(variable in positive for variable in p_variables)
    q = tuple(variable in positive for variable in q_variables)
    assert all(sum(p[edge] for edge in row) % 2 == 0 for row in incident)
    assert all(sum(q[edge] for edge in row) % 2 == 0 for row in incident)

    line_edges = {
        edge for edge, value in enumerate(instance.flow) if value in line
    }
    assert all(p[edge] or q[edge] for edge in line_edges)
    assert all(
        sum(p[edge] and q[edge] for edge in cut(instance, component)) % 2
        == 0
        for component in components
    )

    # Reconstruct f'=b(mu o f)+(p,q), using the first two sorted line
    # values as a basis of the kernel.
    assert line[0] ^ line[1] == line[2]
    coordinate_image = (0, line[0], line[1], line[2])
    affine_base = min(value for value in range(1, 8) if value not in line)
    candidate = tuple(
        coordinate_image[int(p[edge]) | (int(q[edge]) << 1)]
        if edge in line_edges
        else affine_base
        ^ coordinate_image[int(p[edge]) | (int(q[edge]) << 1)]
        for edge in range(len(instance.edges))
    )
    assert all(candidate)
    assert all(
        candidate[row[0]] ^ candidate[row[1]] ^ candidate[row[2]] == 0
        for row in incident
    )
    outside = set(range(1, 8)) - set(line)
    for component in components:
        parities = {
            sum(candidate[edge] == value for edge in cut(instance, component))
            % 2
            for value in outside
        }
        assert parities == {0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "instances",
        nargs="*",
        type=Path,
        default=list(DEFAULT_CORPUS),
    )
    parser.add_argument("--solver", default=shutil.which("cadical"))
    args = parser.parse_args()
    if not args.solver:
        raise SystemExit("CaDiCaL was not found; pass --solver PATH")

    rows = []
    for path in args.instances:
        instance = load_instance(path.resolve())
        incident = graph_audit(instance)
        for line in LINES:
            line_edges = {
                edge
                for edge, value in enumerate(instance.flow)
                if value in line
            }
            components = factor_components(instance, line_edges)
            cnf, p_variables, q_variables = build_cnf(
                instance, incident, line, components
            )
            satisfiable, positive = solve(cnf, args.solver)
            assert satisfiable, (
                f"UNSAT line-preserving instance requires a retained CNF "
                f"and independently checked proof: {instance.name} {line}"
            )
            check_model(
                instance,
                incident,
                line,
                components,
                p_variables,
                q_variables,
                positive,
            )
            rows.append(
                (
                    instance.name,
                    line,
                    len(components),
                    cnf.variables,
                    len(cnf.clauses),
                )
            )

    print("Fano two-cycle corpus audit: PASS")
    for name, line, component_count, variables, clauses in rows:
        print(
            f"{name}: line={line} components={component_count} "
            f"cnf={variables}v/{clauses}c SAT+semantic-check"
        )
    print(f"instances={len(args.instances)} lines={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
