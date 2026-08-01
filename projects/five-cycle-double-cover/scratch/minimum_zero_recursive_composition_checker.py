#!/usr/bin/env python3
"""Independent audit of recursive composition of the 130-vertex gap graph.

This checker reconstructs the 60-vertex marked core from graph6, builds
the 130-vertex graph, its once-recursed connector gluing, and the two
natural marked-halfedge gluings.  It directly checks frozen positive
flow/5-CDC witnesses and independently renders the three lower-bound
CNFs used by the accompanying LRAT certificates.

The optional --generate-json mode uses CaDiCaL only to discover positive
witnesses.  Ordinary verification checks those witnesses semantically and
does not trust the SAT solver.
"""

from __future__ import annotations

from collections import Counter
from functools import reduce
from itertools import combinations, product
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
ARTIFACT = HERE / "minimum-zero-recursive-composition.json"

CORE_GRAPH6 = (
    "{??????O@?B?D?EGGSAK?H_?HG?Ao@A_??????????????C?G?C???M???B_???"
    "[???????????????????O?C??C????B_????M?????[_???????????????????????"
    "C??_???O?????B_?????B_?????@q?????????????????????????????C???G???"
    "C???????M???????B_???????[_??????????????????????????????????O????"
    "G???C????????B_????????M?????????["
)
MARKS = ((22, 26), (30, 34), (38, 42), (46, 50), (54, 58))
LEFT_HALF_IDS = (41, 54, 66, 78, 90)
RIGHT_HALF_IDS = (45, 58, 70, 82, 94)
TRIANGLE_LABELS = frozenset(("23", "24", "34"))

CNF_PATHS = {
    "p1": HERE / "minimum-zero-p1-at-most-five.cnf",
    "left": HERE / "minimum-zero-left-reuse-at-most-five.cnf",
    "right": HERE / "minimum-zero-right-reuse-at-most-five.cnf",
}


def parse_graph6(record: str) -> tuple[int, list[tuple[int, int]]]:
    if not record or record[0] == "~":
        raise ValueError("this independent parser expects n <= 62")
    vertices = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for high in range(1, vertices):
        for low in range(high):
            if bits[cursor]:
                edges.append((low, high))
            cursor += 1
    return vertices, edges


def incidence(
    vertices: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    rows = [[] for _ in range(vertices)]
    for edge_id, (left, right) in enumerate(edges):
        rows[left].append(edge_id)
        rows[right].append(edge_id)
    return rows


def build_g1() -> tuple[int, list[tuple[int, int]], list[int]]:
    core_vertices, core_edges = parse_graph6(CORE_GRAPH6)
    assert core_vertices == 60 and len(core_edges) == 90
    mark_index = {edge: index for index, edge in enumerate(MARKS)}
    raw = []
    for side in range(2):
        offset = 65 * side
        for edge in core_edges:
            if edge in mark_index:
                terminal = offset + 60 + mark_index[edge]
                raw.append(tuple(sorted((offset + edge[0], terminal))))
                raw.append(tuple(sorted((offset + edge[1], terminal))))
            else:
                raw.append(
                    tuple(sorted((offset + edge[0], offset + edge[1])))
                )
    raw.extend((60 + index, 125 + index) for index in range(5))
    edges = sorted(raw)
    connectors = [edges.index((60 + index, 125 + index)) for index in range(5)]
    assert connectors == [95, 96, 97, 98, 99]
    return 130, edges, connectors


def split_marked(
    vertices: int,
    edges: list[tuple[int, int]],
    marked_ids: list[int] | tuple[int, ...],
) -> tuple[int, list[tuple[int, int]], list[int]]:
    marked = {edges[edge_id]: index for index, edge_id in enumerate(marked_ids)}
    raw = []
    for edge in edges:
        if edge in marked:
            terminal = vertices + marked[edge]
            raw.append(tuple(sorted((edge[0], terminal))))
            raw.append(tuple(sorted((edge[1], terminal))))
        else:
            raw.append(edge)
    return vertices + 5, sorted(raw), list(range(vertices, vertices + 5))


def self_glue(
    vertices: int,
    edges: list[tuple[int, int]],
    marked_ids: list[int] | tuple[int, ...],
) -> tuple[int, list[tuple[int, int]], list[int]]:
    marked_edges = [edges[edge_id] for edge_id in marked_ids]
    mark_index = {edge: index for index, edge in enumerate(marked_edges)}
    stride = vertices + 5
    raw = []
    for side in range(2):
        offset = side * stride
        for edge in edges:
            if edge in mark_index:
                terminal = offset + vertices + mark_index[edge]
                raw.append(tuple(sorted((offset + edge[0], terminal))))
                raw.append(tuple(sorted((offset + edge[1], terminal))))
            else:
                raw.append(
                    tuple(sorted((offset + edge[0], offset + edge[1])))
                )
    connector_edges = [
        (vertices + index, stride + vertices + index)
        for index in range(5)
    ]
    raw.extend(connector_edges)
    answer = sorted(raw)
    connector_ids = [answer.index(edge) for edge in connector_edges]
    return 2 * stride, answer, connector_ids


def graph_checks(
    vertices: int,
    edges: list[tuple[int, int]],
    boundary: set[int] | frozenset[int] = frozenset(),
) -> None:
    assert len(set(edges)) == len(edges)
    assert all(left < right for left, right in edges)
    rows = incidence(vertices, edges)
    assert all(
        len(row) == (2 if vertex in boundary else 3)
        for vertex, row in enumerate(rows)
    )
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for edge_id in rows[vertex]:
            left, right = edges[edge_id]
            other = right if left == vertex else left
            if other not in seen:
                seen.add(other)
                stack.append(other)
    assert len(seen) == vertices


def zero_variable(edge: int) -> int:
    return 1 + edge


def bit_variable(bit: int, edge: int, edge_count: int) -> int:
    return 1 + (bit + 1) * edge_count + edge


def parity_three(first: int, second: int, third: int) -> list[tuple[int, ...]]:
    return [
        (-first, -second, -third),
        (-first, second, third),
        (first, -second, third),
        (first, second, -third),
    ]


def at_most(
    variables: tuple[int, ...], bound: int, first_auxiliary: int
) -> tuple[int, list[tuple[int, ...]]]:
    if bound == 0:
        return first_auxiliary - 1, [(-item,) for item in variables]
    counter = {}
    next_variable = first_auxiliary
    for index in range(len(variables)):
        for threshold in range(1, min(bound, index + 1) + 1):
            counter[index, threshold] = next_variable
            next_variable += 1
    clauses = []
    for index, item in enumerate(variables):
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


def flow_matching_cnf(
    vertices: int,
    edges: list[tuple[int, int]],
    boundary: set[int] | frozenset[int],
    bound: int,
    signature: tuple[int, ...] | None = None,
) -> tuple[int, list[tuple[int, ...]]]:
    edge_count = len(edges)
    rows = incidence(vertices, edges)
    clauses = []
    for edge in range(edge_count):
        zero = zero_variable(edge)
        first = bit_variable(0, edge, edge_count)
        second = bit_variable(1, edge, edge_count)
        clauses.extend(
            (
                (-zero, -first),
                (-zero, -second),
                (zero, first, second),
            )
        )
    for vertex, row in enumerate(rows):
        for left, right in combinations(row, 2):
            clauses.append(
                (-zero_variable(left), -zero_variable(right))
            )
        if vertex not in boundary:
            assert len(row) == 3
            for bit in range(2):
                clauses.extend(
                    parity_three(
                        *(
                            bit_variable(bit, edge, edge_count)
                            for edge in row
                        )
                    )
                )
    if signature is not None:
        assert len(signature) == len(boundary)
        for value, vertex in zip(signature, sorted(boundary)):
            left, right = rows[vertex]
            for bit in range(2):
                first = bit_variable(bit, left, edge_count)
                second = bit_variable(bit, right, edge_count)
                if (value >> bit) & 1:
                    clauses.extend(((first, second), (-first, -second)))
                else:
                    clauses.extend(((-first, second), (first, -second)))
    last, cardinality = at_most(
        tuple(zero_variable(edge) for edge in range(edge_count)),
        bound,
        3 * edge_count + 1,
    )
    clauses.extend(cardinality)
    return max(3 * edge_count, last), clauses


def render_cnf(
    variables: int, clauses: list[tuple[int, ...]], description: str
) -> str:
    lines = [
        "c minimum-zero-recursive-composition-v1",
        f"c {description}",
        f"p cnf {variables} {len(clauses)}",
    ]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return "\n".join(lines) + "\n"


def parse_model(output: str, variables: int) -> dict[int, bool]:
    assignment = {}
    for line in output.splitlines():
        if not line.startswith("v"):
            continue
        for token in line[1:].split():
            literal = int(token)
            if literal:
                assignment[abs(literal)] = literal > 0
    assert len(assignment) >= variables
    return assignment


def solve_cnf(
    variables: int, clauses: list[tuple[int, ...]]
) -> tuple[int, dict[int, bool] | None]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".cnf", encoding="ascii"
    ) as stream:
        stream.write(render_cnf(variables, clauses, "temporary"))
        stream.flush()
        result = subprocess.run(
            ["cadical", "-q", "--seed=0", stream.name],
            capture_output=True,
            text=True,
            check=False,
        )
    assert result.returncode in (10, 20)
    if result.returncode == 20:
        return 20, None
    return 10, parse_model(result.stdout, variables)


def values_from_model(
    model: dict[int, bool], edge_count: int
) -> list[int]:
    return [
        int(model[bit_variable(0, edge, edge_count)])
        | (int(model[bit_variable(1, edge, edge_count)]) << 1)
        for edge in range(edge_count)
    ]


def flow_state_check(
    vertices: int,
    edges: list[tuple[int, int]],
    boundary: set[int] | frozenset[int],
    expected_signature: tuple[int, ...],
    values: list[int],
    expected_zeros: int,
) -> None:
    assert len(values) == len(edges)
    assert all(value in range(4) for value in values)
    rows = incidence(vertices, edges)
    for vertex, row in enumerate(rows):
        if vertex not in boundary:
            assert reduce(int.__xor__, (values[edge] for edge in row), 0) == 0
        assert sum(values[edge] == 0 for edge in row) <= 1
    signature = tuple(
        reduce(int.__xor__, (values[edge] for edge in rows[vertex]), 0)
        for vertex in sorted(boundary)
    )
    assert signature == expected_signature
    assert sum(value == 0 for value in values) == expected_zeros


def label_mask(label: str) -> int:
    assert len(label) == 2 and label[0] < label[1]
    first, second = map(int, label)
    assert 0 <= first < second < 5
    return (1 << first) | (1 << second)


def cover_check(
    vertices: int,
    edges: list[tuple[int, int]],
    labels: list[str],
    expected_zeros: int,
    boundary: set[int] | frozenset[int] = frozenset(),
    boundary_labels: list[str] | None = None,
) -> None:
    assert len(labels) == len(edges)
    masks = [label_mask(label) for label in labels]
    columns = (0, 0, 1, 2, 3)
    induced_flow = [
        columns[int(label[0])] ^ columns[int(label[1])]
        for label in labels
    ]
    rows = incidence(vertices, edges)
    expected_boundary = {}
    if boundary_labels is not None:
        assert len(boundary_labels) == len(boundary)
        expected_boundary = dict(zip(sorted(boundary), boundary_labels))
    for vertex, row in enumerate(rows):
        parity = reduce(int.__xor__, (masks[edge] for edge in row), 0)
        if vertex in boundary:
            assert parity == label_mask(expected_boundary[vertex])
            expected = expected_boundary[vertex]
            assert reduce(
                int.__xor__, (induced_flow[edge] for edge in row), 0
            ) == columns[int(expected[0])] ^ columns[int(expected[1])]
        else:
            assert parity == 0
            assert reduce(
                int.__xor__, (induced_flow[edge] for edge in row), 0
            ) == 0
    zero_edges = {
        edge for edge, label in enumerate(labels) if label == "01"
    }
    assert zero_edges == {
        edge for edge, value in enumerate(induced_flow) if value == 0
    }
    assert len(zero_edges) == expected_zeros
    for row in rows:
        assert sum(edge in zero_edges for edge in row) <= 1


def reverse_lift(
    first_cycle: set[int],
    second_cycle: set[int],
    flow: list[int],
) -> list[str]:
    section = {
        0: (0, 0, 0, 0),
        1: (1, 1, 0, 0),
        2: (1, 0, 1, 0),
        3: (0, 1, 1, 0),
    }
    labels = []
    for edge, value in enumerate(flow):
        if value == 0:
            assert edge in first_cycle and edge in second_cycle
            labels.append("01")
            continue
        d0 = int((edge in first_cycle) ^ (edge in second_cycle))
        selected = list(section[value])
        if d0 ^ selected[0]:
            selected = [bit ^ 1 for bit in selected]
        coordinates = []
        if edge in first_cycle:
            coordinates.append(0)
        if edge in second_cycle:
            coordinates.append(1)
        coordinates.extend(
            index + 1
            for index in range(1, 4)
            if selected[index]
        )
        assert len(coordinates) == 2
        labels.append("".join(map(str, coordinates)))
    return labels


def solve_extension_labels(
    vertices: int,
    edges: list[tuple[int, int]],
    bound: int,
    forbidden_zero_edges: tuple[int, ...] = (),
) -> list[str]:
    # Generation helper only.  Frozen labels are checked above without
    # relying on this imported encoding.
    from tools.five_cdc_matching_four_flow import (
        build_encoding,
        parse_model as parse_extension_model,
        variable,
    )
    from tools.minimum_extension_gap_scan import bounded
    from verifier_a import Edge, Graph

    graph = Graph(
        vertices,
        tuple(
            Edge(edge_id, left, right)
            for edge_id, (left, right) in enumerate(edges)
        ),
    )
    encoding = build_encoding(graph)
    variables, bounded_clauses = bounded(
        encoding.variables,
        encoding.clauses,
        tuple(1 + edge for edge in range(len(edges))),
        bound,
    )
    clauses = bounded_clauses + tuple(
        (-(1 + edge),) for edge in forbidden_zero_edges
    )
    with tempfile.NamedTemporaryFile(
        "w", suffix=".cnf", encoding="ascii"
    ) as stream:
        stream.write(render_cnf(variables, list(clauses), "extension"))
        stream.flush()
        result = subprocess.run(
            ["cadical", "-q", "--seed=0", stream.name],
            capture_output=True,
            text=True,
            check=False,
        )
    assert result.returncode == 10
    model = parse_extension_model(result.stdout, variables)
    edge_count = len(edges)
    first = {
        edge
        for edge in range(edge_count)
        if model[variable(1, edge, edge_count)]
    }
    second = {
        edge
        for edge in range(edge_count)
        if model[variable(2, edge, edge_count)]
    }
    flow = [
        int(model[variable(3, edge, edge_count)])
        | (int(model[variable(4, edge, edge_count)]) << 1)
        for edge in range(edge_count)
    ]
    return reverse_lift(first, second, flow)


def cnf_instances() -> dict[str, tuple[int, list[tuple[int, ...]], str]]:
    g1_vertices, g1_edges, connectors = build_g1()
    p1_vertices, p1_edges, boundary_vertices = split_marked(
        g1_vertices, g1_edges, connectors
    )
    instances = {}
    variables, clauses = flow_matching_cnf(
        p1_vertices, p1_edges, set(boundary_vertices), 5
    )
    instances["p1"] = (
        variables,
        clauses,
        "P1 compatible exact-zero matching flow with at most five zeros",
    )
    for name, marks in (
        ("left", LEFT_HALF_IDS),
        ("right", RIGHT_HALF_IDS),
    ):
        vertices, edges, _ = self_glue(g1_vertices, g1_edges, marks)
        variables, clauses = flow_matching_cnf(
            vertices, edges, frozenset(), 5
        )
        instances[name] = (
            variables,
            clauses,
            f"{name} marked-halfedge recursion with at most five zeros",
        )
    return instances


def generate_json() -> dict[str, object]:
    g1_vertices, g1_edges, connectors = build_g1()
    p1_vertices, p1_edges, boundary_vertices = split_marked(
        g1_vertices, g1_edges, connectors
    )
    boundary = set(boundary_vertices)
    cut_free_labels = solve_extension_labels(
        g1_vertices,
        g1_edges,
        6,
        tuple(connectors),
    )
    cover_check(g1_vertices, g1_edges, cut_free_labels, 6)
    assert all(cut_free_labels[edge] != "01" for edge in connectors)

    state_table = []
    for signature in product(range(4), repeat=5):
        if reduce(int.__xor__, signature, 0) != 0:
            continue
        variables, clauses = flow_matching_cnf(
            p1_vertices, p1_edges, boundary, 6, signature
        )
        code, model = solve_cnf(variables, clauses)
        assert code == 10 and model is not None
        values = values_from_model(model, len(p1_edges))
        flow_state_check(
            p1_vertices,
            p1_edges,
            boundary,
            signature,
            values,
            6,
        )
        state_table.append({
            "signature": list(signature),
            "flow_values": values,
        })

    g2_vertices, g2_edges, g2_connectors = self_glue(
        g1_vertices, g1_edges, connectors
    )
    g2_labels = solve_extension_labels(g2_vertices, g2_edges, 12)
    g2_label_by_edge = dict(zip(g2_edges, g2_labels))
    p1_labels = [g2_label_by_edge[edge] for edge in p1_edges]
    boundary_labels = [g2_labels[edge] for edge in g2_connectors]
    assert set(boundary_labels) <= TRIANGLE_LABELS
    cover_check(
        p1_vertices,
        p1_edges,
        p1_labels,
        6,
        boundary,
        boundary_labels,
    )

    half_controls = {}
    for name, marks in (
        ("left", LEFT_HALF_IDS),
        ("right", RIGHT_HALF_IDS),
    ):
        vertices, edges, _ = self_glue(g1_vertices, g1_edges, marks)
        labels = solve_extension_labels(vertices, edges, 6)
        cover_check(vertices, edges, labels, 6)
        half_controls[name] = {
            "vertices": vertices,
            "edges": len(edges),
            "five_cdc_labels": labels,
            "support_01_size": 6,
        }

    return {
        "schema": "minimum-zero-recursive-composition-v1",
        "classification": (
            "PRECISE COMPOSITION NO-GO / NOT A FIVE-CDC COUNTEREXAMPLE"
        ),
        "base_graph": {
            "vertices": 130,
            "edges": 195,
            "connector_edge_ids": connectors,
            "cut_free_size_six_extension_labels": cut_free_labels,
        },
        "connector_recursion": {
            "p1_vertices": p1_vertices,
            "p1_edges": len(p1_edges),
            "feasible_signature_condition": (
                "xor of the five F2^2 boundary values is zero"
            ),
            "state_count": len(state_table),
            "minimum_internal_zero_matching": 6,
            "state_table": state_table,
            "five_cdc_induction_seed": {
                "edge_labels": p1_labels,
                "boundary_labels": boundary_labels,
                "support_01_size": 6,
            },
            "closed_level_2": {
                "vertices": g2_vertices,
                "edges": len(g2_edges),
                "minimum_matching_support": 12,
                "minimum_extending_support": 12,
            },
            "general_closed_level_k_for_k_at_least_2": {
                "vertices": "140*2^(k-1)-10",
                "minimum_matching_support": "6*2^(k-1)",
                "minimum_extending_support": "6*2^(k-1)",
            },
        },
        "marked_halfedge_controls": half_controls,
        "scope_warning": (
            "Every tested/naturally recursive composition has an explicit "
            "standard 5-CDC. No FiveCDC UNSAT claim is made."
        ),
    }


def verify_artifact(data: dict[str, object]) -> None:
    assert data["schema"] == "minimum-zero-recursive-composition-v1"
    g1_vertices, g1_edges, connectors = build_g1()
    graph_checks(g1_vertices, g1_edges)
    cut_free_labels = data["base_graph"][
        "cut_free_size_six_extension_labels"
    ]
    cover_check(g1_vertices, g1_edges, cut_free_labels, 6)
    assert all(cut_free_labels[edge] != "01" for edge in connectors)
    p1_vertices, p1_edges, boundary_vertices = split_marked(
        g1_vertices, g1_edges, connectors
    )
    boundary = set(boundary_vertices)
    graph_checks(p1_vertices, p1_edges, boundary)

    connector = data["connector_recursion"]
    table = connector["state_table"]
    assert len(table) == 256
    observed = set()
    for row in table:
        signature = tuple(row["signature"])
        assert signature not in observed
        observed.add(signature)
        assert reduce(int.__xor__, signature, 0) == 0
        flow_state_check(
            p1_vertices,
            p1_edges,
            boundary,
            signature,
            row["flow_values"],
            6,
        )
    assert observed == {
        signature
        for signature in product(range(4), repeat=5)
        if reduce(int.__xor__, signature, 0) == 0
    }

    seed = connector["five_cdc_induction_seed"]
    assert set(seed["boundary_labels"]) <= TRIANGLE_LABELS
    cover_check(
        p1_vertices,
        p1_edges,
        seed["edge_labels"],
        6,
        boundary,
        seed["boundary_labels"],
    )

    # Close two identical seed poles.  This is the level-2 270-vertex
    # positive certificate and the base of the recursive cover induction.
    g2_vertices, g2_edges, g2_connectors = self_glue(
        g1_vertices, g1_edges, connectors
    )
    seed_map = dict(zip(p1_edges, seed["edge_labels"]))
    stride = p1_vertices
    closed_map = {}
    for side in range(2):
        offset = side * stride
        for edge, label in seed_map.items():
            closed_map[
                tuple(sorted((edge[0] + offset, edge[1] + offset)))
            ] = label
    for edge_id, label in zip(g2_connectors, seed["boundary_labels"]):
        closed_map[g2_edges[edge_id]] = label
    assert len(closed_map) == len(g2_edges)
    cover_check(
        g2_vertices,
        g2_edges,
        [closed_map[edge] for edge in g2_edges],
        12,
    )

    for name, marks in (
        ("left", LEFT_HALF_IDS),
        ("right", RIGHT_HALF_IDS),
    ):
        vertices, edges, _ = self_glue(g1_vertices, g1_edges, marks)
        graph_checks(vertices, edges)
        control = data["marked_halfedge_controls"][name]
        cover_check(
            vertices,
            edges,
            control["five_cdc_labels"],
            6,
        )


def write_cnfs() -> None:
    for name, (variables, clauses, description) in cnf_instances().items():
        CNF_PATHS[name].write_text(
            render_cnf(variables, clauses, description), encoding="ascii"
        )


def check_proofs() -> None:
    expected = cnf_instances()
    for name, (variables, clauses, description) in expected.items():
        cnf = CNF_PATHS[name]
        proof = cnf.with_suffix(".lrat")
        assert cnf.read_text(encoding="ascii") == render_cnf(
            variables, clauses, description
        )
        for checker in (
            ROOT / ".tools/cert-checkers/drat-trim/lrat-check",
            ROOT / ".tools/cert-checkers/cake_lpr/cake_lpr",
        ):
            subprocess.run(
                [str(checker), str(cnf), str(proof)],
                check=True,
            )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate-json", action="store_true")
    parser.add_argument("--write-cnfs", action="store_true")
    parser.add_argument("--check-proofs", action="store_true")
    arguments = parser.parse_args()

    if arguments.generate_json:
        ARTIFACT.write_text(
            json.dumps(generate_json(), indent=2, sort_keys=True) + "\n",
            encoding="ascii",
        )
    if arguments.write_cnfs:
        write_cnfs()

    data = json.loads(ARTIFACT.read_text(encoding="ascii"))
    verify_artifact(data)
    if arguments.check_proofs:
        check_proofs()
    print(
        json.dumps(
            {
                "artifact_sha256": sha256(ARTIFACT),
                "classification": data["classification"],
                "connector_state_count": 256,
                "connector_recursion_level_2_minimum": 12,
                "left_reuse_minimum": 6,
                "right_reuse_minimum": 6,
                "verified": True,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
