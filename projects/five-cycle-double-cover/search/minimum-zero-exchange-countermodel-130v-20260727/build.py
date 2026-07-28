#!/usr/bin/env python3
"""Build and certify the 130-vertex minimum-zero exchange countermodel."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from search.canonical.canonical_search import parse_graph6  # noqa: E402
from tools.five_cdc_matching_four_flow import (  # noqa: E402
    build_encoding as build_extension_encoding,
    check_model as check_extension_model,
    parse_model,
    variable as extension_variable,
)
from tools.minimum_extension_gap_scan import (  # noqa: E402
    bounded,
    render_cnf,
)
from verifier_a import Edge, Graph  # noqa: E402


CORE_GRAPH6 = (
    "{??????O@?B?D?EGGSAK?H_?HG?Ao@A_??????????????C?G?C???M???B_???"
    "[???????????????????O?C??C????B_????M?????[_???????????????????????"
    "C??_???O?????B_?????B_?????@q?????????????????????????????C???G???"
    "C???????M???????B_???????[_??????????????????????????????????O????"
    "G???C????????B_????????M?????????["
)
MARKS = ((22, 26), (30, 34), (38, 42), (46, 50), (54, 58))


def graph6(vertices: int, edges: list[tuple[int, int]]) -> str:
    bits = [
        int((low, high) in set(edges))
        for high in range(1, vertices)
        for low in range(high)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    if vertices >= 63:
        prefix = "~" + "".join(
            chr(63 + ((vertices >> shift) & 63))
            for shift in (12, 6, 0)
        )
    else:
        prefix = chr(vertices + 63)
    return prefix + "".join(
        chr(
            63
            + sum(
                bits[position + offset] << (5 - offset)
                for offset in range(6)
            )
        )
        for position in range(0, len(bits), 6)
    )


def build_graph() -> tuple[list[tuple[int, int]], list[int]]:
    core = parse_graph6(CORE_GRAPH6)
    assert core.vertices == 60 and len(core.edges) == 90
    marks = {edge: index for index, edge in enumerate(MARKS)}
    raw: list[tuple[int, int]] = []
    cut_raw: list[int] = []
    for side in range(2):
        offset = 65 * side
        for edge in core.edges:
            if edge in marks:
                terminal = offset + 60 + marks[edge]
                raw.append(tuple(sorted((offset + edge[0], terminal))))
                raw.append(tuple(sorted((offset + edge[1], terminal))))
            else:
                raw.append(
                    tuple(sorted((offset + edge[0], offset + edge[1])))
                )
    for index in range(5):
        cut_raw.append(len(raw))
        raw.append((60 + index, 125 + index))
    order = sorted(range(len(raw)), key=raw.__getitem__)
    inverse = {old: new for new, old in enumerate(order)}
    return [raw[old] for old in order], sorted(inverse[old] for old in cut_raw)


def parity_clauses(
    vertices: int, edges: list[tuple[int, int]]
) -> list[tuple[int, ...]]:
    incident: list[list[int]] = [[] for _ in range(vertices)]
    for edge_id, (left, right) in enumerate(edges):
        incident[left].append(edge_id)
        incident[right].append(edge_id)
    clauses: list[tuple[int, ...]] = []
    for row in incident:
        assert len(row) == 3
        for bit in range(2):
            first, second, third = (
                2 * edge_id + bit + 1 for edge_id in row
            )
            clauses.extend(
                (
                    (-first, -second, -third),
                    (-first, second, third),
                    (first, -second, third),
                    (first, second, -third),
                )
            )
    return clauses


def flow_at_most_four(
    vertices: int, edges: list[tuple[int, int]]
) -> tuple[int, tuple[tuple[int, ...], ...]]:
    edge_count = len(edges)
    clauses = parity_clauses(vertices, edges)
    zeros = []
    for edge_id in range(edge_count):
        first = 2 * edge_id + 1
        second = first + 1
        zero = 2 * edge_count + edge_id + 1
        zeros.append(zero)
        clauses.extend(
            ((-zero, -first), (-zero, -second), (zero, first, second))
        )
    return bounded(
        3 * edge_count,
        tuple(clauses),
        tuple(zeros),
        4,
    )


def solve_cnf(
    variables: int, clauses: tuple[tuple[int, ...], ...]
) -> tuple[int, str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".cnf", encoding="ascii"
    ) as handle:
        handle.write(render_cnf(variables, clauses, "temporary"))
        handle.flush()
        result = subprocess.run(
            ["cadical", "-q", "--seed=0", handle.name],
            capture_output=True,
            text=True,
            check=False,
        )
    assert result.returncode in (10, 20)
    return result.returncode, result.stdout


def distinguished_flow(
    vertices: int,
    edges: list[tuple[int, int]],
    cut: list[int],
) -> list[int]:
    clauses = parity_clauses(vertices, edges)
    cut_set = set(cut)
    for edge_id in range(len(edges)):
        first = 2 * edge_id + 1
        second = first + 1
        if edge_id in cut_set:
            clauses.extend(((-first,), (-second,)))
        else:
            clauses.append((first, second))
    code, output = solve_cnf(2 * len(edges), tuple(clauses))
    assert code == 10
    assignment = parse_model(output, 2 * len(edges))
    return [
        int(assignment[2 * edge_id + 1])
        | (int(assignment[2 * edge_id + 2]) << 1)
        for edge_id in range(len(edges))
    ]


def extension_witness(graph: Graph, bound: int) -> dict[str, object]:
    encoding = build_extension_encoding(graph)
    variables, clauses = bounded(
        encoding.variables,
        encoding.clauses,
        tuple(1 + edge_id for edge_id in range(len(graph.edges))),
        bound,
    )
    code, output = solve_cnf(variables, clauses)
    assert code == 10
    assignment = parse_model(output, variables)
    primary = {
        variable: assignment[variable]
        for variable in range(1, encoding.variables + 1)
    }
    checked = check_extension_model(graph, primary)
    assert checked["valid"] and checked["matching_size"] == bound
    edge_count = len(graph.edges)
    matching = [
        edge_id
        for edge_id in range(edge_count)
        if primary[extension_variable(0, edge_id, edge_count)]
    ]
    first_cycle = [
        edge_id
        for edge_id in range(edge_count)
        if primary[extension_variable(1, edge_id, edge_count)]
    ]
    second_cycle = [
        edge_id
        for edge_id in range(edge_count)
        if primary[extension_variable(2, edge_id, edge_count)]
    ]
    flow = [
        int(primary[extension_variable(3, edge_id, edge_count)])
        | (
            int(primary[extension_variable(4, edge_id, edge_count)])
            << 1
        )
        for edge_id in range(edge_count)
    ]
    cover = reverse_lift(first_cycle, second_cycle, flow)
    return {
        "matching_edges": matching,
        "cycle_a": first_cycle,
        "cycle_b": second_cycle,
        "flow_values": flow,
        "five_cdc_labels": cover,
    }


def reverse_lift(
    first_cycle: list[int],
    second_cycle: list[int],
    flow: list[int],
) -> list[str]:
    first = set(first_cycle)
    second = set(second_cycle)
    section = {
        0: (0, 0, 0, 0),
        1: (1, 1, 0, 0),
        2: (1, 0, 1, 0),
        3: (0, 1, 1, 0),
    }
    labels = []
    for edge_id, value in enumerate(flow):
        if value == 0:
            assert edge_id in first and edge_id in second
            labels.append("01")
            continue
        d0 = int((edge_id in first) ^ (edge_id in second))
        selected = list(section[value])
        h = d0 ^ selected[0]
        if h:
            selected = [bit ^ 1 for bit in selected]
        assert selected[0] == d0 and sum(selected) == 2
        coordinates = []
        if edge_id in first:
            coordinates.append(0)
        if edge_id in second:
            coordinates.append(1)
        coordinates.extend(
            index + 1
            for index in range(1, 4)
            if selected[index]
        )
        assert len(coordinates) == 2
        labels.append("".join(map(str, coordinates)))
    return labels


def write_graph(
    path: Path, vertices: int, edges: list[tuple[int, int]]
) -> None:
    path.write_text(
        json.dumps(
            {
                "format": "five-cdc-multigraph-v1",
                "vertices": vertices,
                "edges": [
                    {"id": edge_id, "u": left, "v": right}
                    for edge_id, (left, right) in enumerate(edges)
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prove", action="store_true")
    arguments = parser.parse_args()
    edges, cut = build_graph()
    graph = Graph(
        130,
        tuple(
            Edge(edge_id, left, right)
            for edge_id, (left, right) in enumerate(edges)
        ),
    )
    write_graph(HERE / "graph.json", 130, edges)
    (HERE / "graph.g6").write_text(
        graph6(130, edges) + "\n", encoding="ascii"
    )

    flow_variables, flow_clauses = flow_at_most_four(130, edges)
    (HERE / "flow-at-most-four-zero.cnf").write_text(
        render_cnf(
            flow_variables,
            flow_clauses,
            "130v unrestricted F2^2 flow with at most four zero edges",
        ),
        encoding="ascii",
    )

    extension = build_extension_encoding(graph)
    extension_variables, extension_clauses = bounded(
        extension.variables,
        extension.clauses,
        tuple(1 + edge_id for edge_id in range(len(edges))),
        5,
    )
    (HERE / "extension-at-most-five.cnf").write_text(
        render_cnf(
            extension_variables,
            extension_clauses,
            "130v matching/four-flow extension with matching size at most five",
        ),
        encoding="ascii",
    )

    witness = {
        "vertices": 130,
        "edges": len(edges),
        "core_graph6": CORE_GRAPH6,
        "marked_core_edges": [list(edge) for edge in MARKS],
        "displayed_zero_cut": cut,
        "displayed_flow_values": distinguished_flow(130, edges, cut),
        "minimum_extending_witness": extension_witness(graph, 6),
        "claims": {
            "flow_resistance": 5,
            "minimum_exact_zero_matching_size": 5,
            "minimum_extending_matching_size": 6,
            "standard_five_cdc": True,
            "five_cdc_counterexample": False,
        },
    }
    (HERE / "witness.json").write_text(
        json.dumps(witness, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if arguments.prove:
        for stem in ("flow-at-most-four-zero", "extension-at-most-five"):
            cnf = HERE / f"{stem}.cnf"
            proof = HERE / f"{stem}.lrat"
            solved = subprocess.run(
                [
                    "cadical",
                    "-q",
                    "--seed=0",
                    "--lrat",
                    "--no-binary",
                    str(cnf),
                    str(proof),
                ],
                check=False,
            )
            assert solved.returncode == 20
            for checker in (
                ROOT / ".tools/cert-checkers/drat-trim/lrat-check",
                ROOT / ".tools/cert-checkers/cake_lpr/cake_lpr",
            ):
                subprocess.run(
                    [str(checker), str(cnf), str(proof)],
                    check=True,
                )

    paths = sorted(
        path
        for path in HERE.iterdir()
        if path.is_file()
        and path.name
        not in {"SHA256SUMS", "__pycache__"}
    )
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in paths),
        encoding="ascii",
    )
    print(
        json.dumps(
            {
                "cut": cut,
                "edges": len(edges),
                "extension_clauses": len(extension_clauses),
                "extension_variables": extension_variables,
                "flow_clauses": len(flow_clauses),
                "flow_variables": flow_variables,
                "vertices": 130,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
