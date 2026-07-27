#!/usr/bin/env python3
"""Rebuild the two ordinary CNFs and their textual DRAT proofs."""

from __future__ import annotations

import json
import shutil
import subprocess
from collections import deque
from pathlib import Path


HERE = Path(__file__).resolve().parent


class CNF:
    def __init__(self, variables: int) -> None:
        self.variables = variables
        self.clauses: list[tuple[int, ...]] = []

    def fresh(self) -> int:
        self.variables += 1
        return self.variables

    def add(self, *literals: int) -> None:
        self.clauses.append(tuple(literals))

    def xor_gate(self, first: int, second: int) -> int:
        output = self.fresh()
        self.add(first, second, -output)
        self.add(first, -second, output)
        self.add(-first, second, output)
        self.add(-first, -second, -output)
        return output

    def even(self, variables: list[int]) -> None:
        parity = self.xor_gate(variables[0], variables[1])
        for variable in variables[2:]:
            parity = self.xor_gate(parity, variable)
        self.add(-parity)

    def render(self) -> str:
        lines = [f"p cnf {self.variables} {len(self.clauses)}"]
        lines.extend(" ".join(map(str, row)) + " 0" for row in self.clauses)
        return "\n".join(lines) + "\n"


def factor_components(
    order: int,
    edges: tuple[tuple[int, int], ...],
    selected: set[int],
) -> tuple[frozenset[int], ...]:
    adjacency = [[] for _ in range(order)]
    for edge in selected:
        first, second = edges[edge]
        adjacency[first].append(second)
        adjacency[second].append(first)
    unseen = set(range(order))
    output = []
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


def build(
    order: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
    line: tuple[int, int, int],
) -> str:
    edge_count = len(edges)
    p = tuple(edge + 1 for edge in range(edge_count))
    q = tuple(edge_count + edge + 1 for edge in range(edge_count))
    cnf = CNF(2 * edge_count)
    incident = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        incident[first].append(edge)
        incident[second].append(edge)

    for row in incident:
        for variables in (
            [p[edge] for edge in row],
            [q[edge] for edge in row],
        ):
            cnf.add(variables[0], variables[1], -variables[2])
            cnf.add(variables[0], -variables[1], variables[2])
            cnf.add(-variables[0], variables[1], variables[2])
            cnf.add(-variables[0], -variables[1], -variables[2])

    factor_edges = {
        edge for edge, value in enumerate(flow) if value in line
    }
    for edge in sorted(factor_edges):
        cnf.add(p[edge], q[edge])

    for component in factor_components(order, edges, factor_edges):
        products = []
        for edge, (first, second) in enumerate(edges):
            if (first in component) == (second in component):
                continue
            product = cnf.fresh()
            cnf.add(-product, p[edge])
            cnf.add(-product, q[edge])
            cnf.add(product, -p[edge], -q[edge])
            products.append(product)
        cnf.even(products)

    assert cnf.variables == 65
    assert len(cnf.clauses) == 210
    return cnf.render()


def main() -> int:
    data = json.loads(
        (HERE / "construction.json").read_text(encoding="utf-8")
    )
    order = data["order"]
    edges = tuple(tuple(edge) for edge in data["edges"])
    flow = tuple(data["flow_values_by_edge"])
    solver = shutil.which("cadical")
    if solver is None:
        raise SystemExit("CaDiCaL not found")

    for line, stem in (
        ((1, 2, 3), "line-123"),
        ((1, 6, 7), "line-167"),
    ):
        cnf_path = HERE / f"{stem}.cnf"
        proof_path = HERE / f"{stem}.drat"
        cnf_path.write_text(build(order, edges, flow, line), encoding="ascii")
        process = subprocess.run(
            [
                solver,
                "--quiet",
                "--no-binary",
                str(cnf_path),
                str(proof_path),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        assert process.returncode == 20, process.stdout + process.stderr
        assert proof_path.stat().st_size > 0
        print(f"{stem}: 65 variables, 210 clauses, UNSAT proof written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
