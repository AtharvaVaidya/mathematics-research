#!/usr/bin/env python3
"""Second checker: reconstruct CNFs and verify the retained DRAT proofs."""

from __future__ import annotations

import json
import shutil
import subprocess
from collections import deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def graph6(order: int, edges: tuple[tuple[int, int], ...]) -> str:
    assert order < 63
    edge_set = set(edges)
    bits = [
        int((first, second) in edge_set)
        for second in range(1, order)
        for first in range(second)
    ]
    while len(bits) % 6:
        bits.append(0)
    return chr(order + 63) + "".join(
        chr(
            63
            + sum(
                bits[offset + position] << (5 - position)
                for position in range(6)
            )
        )
        for offset in range(0, len(bits), 6)
    )


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
    answer = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        block = {root}
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    block.add(neighbor)
                    queue.append(neighbor)
        answer.append(frozenset(block))
    return tuple(answer)


def independently_render_cnf(
    order: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
    line: tuple[int, int, int],
) -> str:
    clauses: list[tuple[int, ...]] = []
    next_variable = 2 * len(edges)
    p = {edge: edge + 1 for edge in range(len(edges))}
    q = {edge: len(edges) + edge + 1 for edge in range(len(edges))}

    incidence = [[] for _ in range(order)]
    for edge, endpoints in enumerate(edges):
        for vertex in endpoints:
            incidence[vertex].append(edge)

    def add_even_three(first: int, second: int, third: int) -> None:
        clauses.extend(
            (
                (first, second, -third),
                (first, -second, third),
                (-first, second, third),
                (-first, -second, -third),
            )
        )

    def new_xor(first: int, second: int) -> int:
        nonlocal next_variable
        next_variable += 1
        output = next_variable
        clauses.extend(
            (
                (first, second, -output),
                (first, -second, output),
                (-first, second, output),
                (-first, -second, -output),
            )
        )
        return output

    for row in incidence:
        add_even_three(*(p[edge] for edge in row))
        add_even_three(*(q[edge] for edge in row))

    factor = {edge for edge, value in enumerate(flow) if value in line}
    clauses.extend((p[edge], q[edge]) for edge in sorted(factor))

    for component in factor_components(order, edges, factor):
        products = []
        for edge, (first, second) in enumerate(edges):
            if (first in component) == (second in component):
                continue
            next_variable += 1
            product = next_variable
            clauses.extend(
                (
                    (-product, p[edge]),
                    (-product, q[edge]),
                    (product, -p[edge], -q[edge]),
                )
            )
            products.append(product)
        parity = new_xor(products[0], products[1])
        parity = new_xor(parity, products[2])
        parity = new_xor(parity, products[3])
        clauses.append((-parity,))

    assert next_variable == 65
    assert len(clauses) == 210
    return (
        f"p cnf {next_variable} {len(clauses)}\n"
        + "".join(
            " ".join(map(str, clause)) + " 0\n" for clause in clauses
        )
    )


def main() -> int:
    data = json.loads(
        (HERE / "construction.json").read_text(encoding="utf-8")
    )
    order = data["order"]
    edges = tuple(tuple(edge) for edge in data["edges"])
    flow = tuple(data["flow_values_by_edge"])

    raw = graph6(order, edges)
    labelg = shutil.which("labelg")
    if labelg is None:
        raise SystemExit("nauty labelg not found")
    canonical = subprocess.run(
        [labelg, "-q"],
        input=raw + "\n",
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert canonical == data["canonical_graph6"]
    assert (HERE / "canonical.g6").read_text(encoding="ascii").strip() == canonical

    drat_trim = ROOT / "berge-fulkerson" / "certificate" / "bin" / "drat-trim"
    assert drat_trim.is_file()
    logs = []
    for line, stem in (
        ((1, 2, 3), "line-123"),
        ((1, 6, 7), "line-167"),
    ):
        expected = independently_render_cnf(order, edges, flow, line)
        cnf_path = HERE / f"{stem}.cnf"
        proof_path = HERE / f"{stem}.drat"
        assert cnf_path.read_text(encoding="ascii") == expected
        process = subprocess.run(
            [str(drat_trim), str(cnf_path), str(proof_path)],
            check=False,
            capture_output=True,
            text=True,
        )
        output = process.stdout + process.stderr
        assert process.returncode == 0 and "s VERIFIED" in output, output
        logs.append(f"{stem}: 65 variables, 210 clauses, DRAT VERIFIED")

    print("Petersen two-cycle certificate package: PASS")
    print(f"canonical_graph6={canonical}")
    for log in logs:
        print(log)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
