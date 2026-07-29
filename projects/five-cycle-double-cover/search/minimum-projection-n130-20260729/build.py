#!/usr/bin/env python3
"""Build exact certificates for the 130-vertex minimum Fano projection."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

from pycryptosat import Solver

HERE = Path(__file__).resolve().parent


def at_most_k(
    inputs: tuple[int, ...], bound: int, first: int
) -> tuple[int, list[tuple[int, ...]]]:
    if bound < 0:
        return first - 1, [()]
    if bound >= len(inputs):
        return first - 1, []
    if bound == 0:
        return first - 1, [(-item,) for item in inputs]
    next_variable = first
    counter = {}
    for index in range(len(inputs)):
        for threshold in range(1, min(bound, index + 1) + 1):
            counter[index, threshold] = next_variable
            next_variable += 1
    clauses = []
    for index, item in enumerate(inputs):
        clauses.append((-item, counter[index, 1]))
        if index == 0:
            continue
        for threshold in range(1, min(bound, index) + 1):
            clauses.append(
                (-counter[index - 1, threshold], counter[index, threshold])
            )
        for threshold in range(2, min(bound, index + 1) + 1):
            clauses.append(
                (
                    -item,
                    -counter[index - 1, threshold - 1],
                    counter[index, threshold],
                )
            )
        if index >= bound:
            clauses.append((-item, -counter[index - 1, bound]))
    return next_variable - 1, clauses


def parity3(a: int, b: int, c: int) -> list[tuple[int, ...]]:
    return [
        (-a, -b, -c),
        (-a, b, c),
        (a, -b, c),
        (a, b, -c),
    ]


def incidence(graph: dict) -> list[list[int]]:
    rows = [[] for _ in range(graph["vertices"])]
    for edge in graph["edges"]:
        rows[edge["u"]].append(edge["id"])
        rows[edge["v"]].append(edge["id"])
    assert all(len(row) == 3 for row in rows)
    return rows


def projection_cnf(
    graph: dict, bound: int
) -> tuple[int, list[tuple[int, ...]]]:
    m = len(graph["edges"])
    clauses = []
    for row in incidence(graph):
        for coordinate in range(3):
            clauses.extend(parity3(*(1 + coordinate * m + e for e in row)))
    for e in range(m):
        clauses.append(tuple(1 + coordinate * m + e for coordinate in range(3)))
    variables = 3 * m
    variables, cardinality = at_most_k(
        tuple(1 + e for e in range(m)), bound, variables + 1
    )
    clauses.extend(cardinality)
    return variables, clauses


def components_without_h(graph: dict, h: set[int]) -> list[set[int]]:
    adjacent = [[] for _ in range(graph["vertices"])]
    for edge in graph["edges"]:
        if edge["id"] not in h:
            adjacent[edge["u"]].append(edge["v"])
            adjacent[edge["v"]].append(edge["u"])
    unseen = set(range(graph["vertices"]))
    answer = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        stack = [root]
        while stack:
            vertex = stack.pop()
            for other in adjacent[vertex]:
                if other in unseen:
                    unseen.remove(other)
                    component.add(other)
                    stack.append(other)
        answer.append(component)
    return answer


def clean_lift_cnf(
    graph: dict, h: set[int]
) -> tuple[int, list[tuple[int, ...]]]:
    """Variables 1..m are p, m+1..2m are q; later variables are products/xors."""
    m = len(graph["edges"])
    clauses = []
    for row in incidence(graph):
        clauses.extend(parity3(*(1 + e for e in row)))
        clauses.extend(parity3(*(1 + m + e for e in row)))
    for e in range(m):
        if e not in h:
            clauses.append((1 + e, 1 + m + e))
    variables = 2 * m
    products = []
    for e in range(m):
        p, q = 1 + e, 1 + m + e
        variables += 1
        r = variables
        products.append(r)
        clauses.extend(((-r, p), (-r, q), (r, -p, -q)))
    for component in components_without_h(graph, h):
        cut = [
            edge["id"]
            for edge in graph["edges"]
            if (edge["u"] in component) != (edge["v"] in component)
        ]
        if not cut:
            continue
        accumulator = products[cut[0]]
        for e in cut[1:]:
            right = products[e]
            variables += 1
            out = variables
            clauses.extend(
                (
                    (-accumulator, -right, -out),
                    (-accumulator, right, out),
                    (accumulator, -right, out),
                    (accumulator, right, -out),
                )
            )
            accumulator = out
        clauses.append((-accumulator,))
    return variables, clauses


def solver(clauses: list[tuple[int, ...]]) -> Solver:
    answer = Solver()
    for clause in clauses:
        answer.add_clause(list(clause))
    return answer


def mask_hex(edges: set[int], m: int) -> str:
    value = sum(1 << e for e in edges)
    return f"{value:0{(m + 3) // 4}x}"


def validate_flow(
    graph: dict, h: set[int], p: set[int], q: set[int], clean: bool
) -> None:
    assert len(h) == 42
    for row in incidence(graph):
        assert len(h.intersection(row)) % 2 == 0
        assert len(p.intersection(row)) % 2 == 0
        assert len(q.intersection(row)) % 2 == 0
    all_edges = set(range(len(graph["edges"])))
    assert all_edges - h <= p | q
    if clean:
        for component in components_without_h(graph, h):
            cut = {
                edge["id"]
                for edge in graph["edges"]
                if (edge["u"] in component) != (edge["v"] in component)
            }
            assert len(cut & p & q) % 2 == 0


def enumerate_minima(graph: dict) -> list[tuple[str, str, str]]:
    variables, clauses = projection_cnf(graph, 42)
    outer = solver(clauses)
    m = len(graph["edges"])
    records = []
    while True:
        sat, model = outer.solve()
        if not sat:
            break
        h = {e for e in range(m) if model[1 + e]}
        assert len(h) == 42
        clean_variables, clean_clauses = clean_lift_cnf(graph, h)
        clean_sat, clean_model = solver(clean_clauses).solve()
        assert clean_sat
        p = {e for e in range(m) if clean_model[1 + e]}
        q = {e for e in range(m) if clean_model[1 + m + e]}
        validate_flow(graph, h, p, q, True)
        records.append((mask_hex(h, m), mask_hex(p, m), mask_hex(q, m)))
        outer.add_clause([-(1 + e) for e in h])
    records.sort()
    assert len(records) == 11264
    assert len({row[0] for row in records}) == len(records)
    return records


def render_cnf(
    path: Path, variables: int, clauses: list[tuple[int, ...]], label: str
) -> None:
    with path.open("w", encoding="ascii") as out:
        out.write(f"c {label}\n")
        out.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            out.write(" ".join(map(str, clause)) + " 0\n")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prove", action="store_true")
    args = parser.parse_args()
    graph = json.loads((HERE / "graph.json").read_text())
    records = enumerate_minima(graph)
    witness_path = HERE / "minimum-clean-witnesses.json"
    witness_path.write_text(
        json.dumps(
            {
                "encoding": "195-bit edge masks, hexadecimal, least-significant bit is edge 0",
                "minimum_projection_size": 42,
                "records": records,
            },
            separators=(",", ":"),
        )
        + "\n"
    )
    lower_variables, lower_clauses = projection_cnf(graph, 41)
    render_cnf(
        HERE / "projection-at-most-41.cnf",
        lower_variables,
        lower_clauses,
        "no extendable projection has at most 41 edges",
    )
    complete_variables, complete_clauses = projection_cnf(graph, 42)
    for h_hex, _, _ in records:
        h = int(h_hex, 16)
        complete_clauses.append(
            tuple(-(1 + e) for e in range(len(graph["edges"])) if h >> e & 1)
        )
    render_cnf(
        HERE / "minimum-projections-exhausted.cnf",
        complete_variables,
        complete_clauses,
        "all 11264 minimum projections are blocked",
    )
    if args.prove:
        for stem in ("projection-at-most-41", "minimum-projections-exhausted"):
            result = subprocess.run(
                [
                    shutil.which("cadical") or "cadical",
                    "-q",
                    "--seed=0",
                    "--lrat",
                    "--no-binary",
                    str(HERE / f"{stem}.cnf"),
                    str(HERE / f"{stem}.lrat"),
                ]
            )
            assert result.returncode == 20
    paths = sorted(
        path
        for path in HERE.iterdir()
        if path.is_file() and path.name not in {"SHA256SUMS"}
    )
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in paths)
    )
    print(f"minimum_projections={len(records)}")
    print(f"witness_sha256={sha256(witness_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
