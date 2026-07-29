#!/usr/bin/env python3
"""Independent semantic and LRAT verifier for the n=130 projection result."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    answer = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def check_hashes() -> None:
    for row in (HERE / "SHA256SUMS").read_text().splitlines():
        expected, name = row.split("  ", 1)
        assert digest(HERE / name) == expected, name


def rows_at_vertices(graph: dict) -> list[tuple[int, int, int]]:
    incident = [[] for _ in range(graph["vertices"])]
    for position, edge in enumerate(graph["edges"]):
        assert edge["id"] == position
        assert edge["u"] != edge["v"]
        incident[edge["u"]].append(position)
        incident[edge["v"]].append(position)
    assert all(len(row) == 3 for row in incident)
    return [tuple(row) for row in incident]


def validate_graph(graph: dict) -> None:
    edges = graph["edges"]
    pairs = [(min(edge["u"], edge["v"]), max(edge["u"], edge["v"])) for edge in edges]
    assert all(0 <= left < right < graph["vertices"] for left, right in pairs)
    assert len(set(pairs)) == len(pairs)
    rows_at_vertices(graph)

    def reached_without(omitted: int | None) -> set[int]:
        adjacency = [[] for _ in range(graph["vertices"])]
        for edge in edges:
            if edge["id"] == omitted:
                continue
            adjacency[edge["u"]].append(edge["v"])
            adjacency[edge["v"]].append(edge["u"])
        reached = {0}
        stack = [0]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if other not in reached:
                    reached.add(other)
                    stack.append(other)
        return reached

    all_vertices = set(range(graph["vertices"]))
    assert reached_without(None) == all_vertices
    assert all(reached_without(edge["id"]) == all_vertices for edge in edges)


def factors(graph: dict, omitted: int) -> list[set[int]]:
    adjacency = [[] for _ in range(graph["vertices"])]
    for edge in graph["edges"]:
        if not (omitted >> edge["id"] & 1):
            adjacency[edge["u"]].append(edge["v"])
            adjacency[edge["v"]].append(edge["u"])
    unseen = set(range(graph["vertices"]))
    answer = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        reached = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if other in unseen:
                    unseen.remove(other)
                    reached.add(other)
                    stack.append(other)
        answer.append(reached)
    return answer


def validate_witnesses(graph: dict) -> tuple[list[int], str]:
    payload = json.loads((HERE / "minimum-clean-witnesses.json").read_text())
    assert payload["minimum_projection_size"] == 42
    records = payload["records"]
    assert len(records) == 11264
    assert records == sorted(records)
    m = len(graph["edges"])
    all_mask = (1 << m) - 1
    vertex_rows = rows_at_vertices(graph)
    projections = []
    for h_text, p_text, q_text in records:
        h, p, q = map(lambda text: int(text, 16), (h_text, p_text, q_text))
        assert not (h | p | q) & ~all_mask
        assert h.bit_count() == 42
        assert all(((h >> e) & 1) + ((p >> e) & 1) + ((q >> e) & 1) for e in range(m))
        for row in vertex_rows:
            row_mask = sum(1 << e for e in row)
            assert (h & row_mask).bit_count() % 2 == 0
            assert (p & row_mask).bit_count() % 2 == 0
            assert (q & row_mask).bit_count() % 2 == 0
        product = p & q
        for component in factors(graph, h):
            cut = 0
            for edge in graph["edges"]:
                if (edge["u"] in component) != (edge["v"] in component):
                    cut |= 1 << edge["id"]
            assert (product & cut).bit_count() % 2 == 0
        projections.append(h)
    assert len(set(projections)) == len(projections)
    canonical = hashlib.sha256(
        "".join(f"{projection:049x}\n" for projection in projections).encode("ascii")
    ).hexdigest()
    return projections, canonical


def validate_rho3_witness(graph: dict) -> None:
    payload = json.loads((HERE / "rho3-five-witness.json").read_text())
    values = payload["flow_values"]
    assert payload["designated_value"] == 1
    assert len(values) == len(graph["edges"])
    assert all(1 <= value <= 7 for value in values)
    for row in rows_at_vertices(graph):
        total = 0
        for edge in row:
            total ^= values[edge]
        assert total == 0
    selected = [edge for edge, value in enumerate(values) if value == 1]
    assert selected == payload["class_edges"] == [48, 95, 97, 98, 148]
    # Quotient by the designated first-coordinate line: low two bits vanish
    # exactly on the designated value class.
    assert selected == [edge for edge, value in enumerate(values) if value >> 1 == 0]
    selected_set = set(selected)
    assert all(
        sum(edge in selected_set for edge in row) <= 1
        for row in rows_at_vertices(graph)
    )


def sinz(
    inputs: tuple[int, ...], limit: int, first_free: int
) -> tuple[int, list[tuple[int, ...]]]:
    """A separate implementation of the forward sequential counter."""
    state = {}
    fresh = first_free
    for prefix in range(len(inputs)):
        for count in range(1, min(limit, prefix + 1) + 1):
            state[prefix, count] = fresh
            fresh += 1
    clauses = []
    for prefix, literal in enumerate(inputs):
        clauses.append((-literal, state[prefix, 1]))
        if prefix:
            for count in range(1, min(limit, prefix) + 1):
                clauses.append((-state[prefix - 1, count], state[prefix, count]))
            for count in range(2, min(limit, prefix + 1) + 1):
                clauses.append(
                    (-literal, -state[prefix - 1, count - 1], state[prefix, count])
                )
            if prefix >= limit:
                clauses.append((-literal, -state[prefix - 1, limit]))
    return fresh - 1, clauses


def expected_formula(
    graph: dict, limit: int, blocks: list[int]
) -> tuple[int, list[tuple[int, ...]]]:
    m = len(graph["edges"])
    clauses = []
    for row in rows_at_vertices(graph):
        for coordinate in range(3):
            a, b, c = (1 + coordinate * m + edge for edge in row)
            clauses.extend(
                [
                    (-a, -b, -c),
                    (-a, b, c),
                    (a, -b, c),
                    (a, b, -c),
                ]
            )
    for edge in range(m):
        clauses.append((1 + edge, 1 + m + edge, 1 + 2 * m + edge))
    variables, counter = sinz(
        tuple(range(1, m + 1)), limit, 3 * m + 1
    )
    clauses.extend(counter)
    for projection in blocks:
        clauses.append(tuple(-(1 + edge) for edge in range(m) if projection >> edge & 1))
    return variables, clauses


def read_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables = None
    clauses = []
    for row in path.read_text().splitlines():
        if not row or row.startswith("c"):
            continue
        if row.startswith("p "):
            _, kind, variables_text, clause_text = row.split()
            assert kind == "cnf"
            variables = int(variables_text)
            expected = int(clause_text)
            continue
        values = tuple(map(int, row.split()))
        assert values[-1] == 0
        clauses.append(values[:-1])
    assert variables is not None and len(clauses) == expected
    return variables, clauses


def check_cnf(graph: dict, projections: list[int]) -> None:
    for stem, limit, blocks in (
        ("projection-at-most-41", 41, []),
        ("minimum-projections-exhausted", 42, projections),
    ):
        found = read_dimacs(HERE / f"{stem}.cnf")
        expected = expected_formula(graph, limit, blocks)
        assert found == expected, stem


def locate_tools() -> Path:
    roots = []
    configured = os.environ.get("FIVECDC_TOOLS")
    if configured:
        roots.append(Path(configured).expanduser().resolve())
    if len(HERE.parents) >= 4:
        roots.extend([HERE.parents[3] / ".tools", HERE.parents[1] / ".tools"])
        result = subprocess.run(
            ["git", "rev-parse", "--git-common-dir"],
            cwd=HERE.parents[3],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            common = Path(result.stdout.strip())
            if not common.is_absolute():
                common = (HERE.parents[3] / common).resolve()
            roots.append(common.parent / ".tools")
    relative = Path("cert-checkers/drat-trim/lrat-check")
    for root in roots:
        if (root / relative).is_file():
            return root
    raise FileNotFoundError(
        "proof checkers not found; set FIVECDC_TOOLS to the directory "
        "containing cert-checkers/"
    )


def check_lrat() -> None:
    tools = locate_tools()
    checkers = [
        tools / "cert-checkers/drat-trim/lrat-check",
        tools / "cert-checkers/cake_lpr/cake_lpr",
    ]
    for stem in ("projection-at-most-41", "minimum-projections-exhausted"):
        for checker in checkers:
            subprocess.run(
                [
                    str(checker),
                    str(HERE / f"{stem}.cnf"),
                    str(HERE / f"{stem}.lrat"),
                ],
                check=True,
            )


def main() -> int:
    check_hashes()
    graph = json.loads((HERE / "graph.json").read_text())
    assert graph["vertices"] == 130 and len(graph["edges"]) == 195
    validate_graph(graph)
    validate_rho3_witness(graph)
    projections, canonical = validate_witnesses(graph)
    check_cnf(graph, projections)
    check_lrat()
    print("VERIFIED")
    print("minimum_projection_size=42")
    print("minimum_projection_count=11264")
    print("all_minimum_projections_cleanable=true")
    print("rho3=5 (using this witness and the separately retained r_f>=5 LRAT)")
    print(f"projection_set_sha256={canonical}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
