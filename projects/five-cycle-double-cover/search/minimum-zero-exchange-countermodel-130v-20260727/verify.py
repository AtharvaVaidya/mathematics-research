#!/usr/bin/env python3
"""Independent semantic and proof audit of the 130-vertex countermodel."""

from __future__ import annotations

from collections import deque
from itertools import combinations
import hashlib
import json
import os
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPOSITORY = HERE.parents[3]
CORE_GRAPH6 = (
    "{??????O@?B?D?EGGSAK?H_?HG?Ao@A_??????????????C?G?C???M???B_???"
    "[???????????????????O?C??C????B_????M?????[_???????????????????????"
    "C??_???O?????B_?????B_?????@q?????????????????????????????C???G???"
    "C???????M???????B_???????[_??????????????????????????????????O????"
    "G???C????????B_????????M?????????["
)
MARKS = ((22, 26), (30, 34), (38, 42), (46, 50), (54, 58))


def locate_checker(relative: Path) -> Path:
    roots = []
    configured = os.environ.get("FIVECDC_TOOLS")
    if configured:
        roots.append(Path(configured).expanduser().resolve())
    roots.extend([REPOSITORY / ".tools", ROOT / ".tools"])
    result = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=REPOSITORY,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        common = Path(result.stdout.strip())
        if not common.is_absolute():
            common = (REPOSITORY / common).resolve()
        roots.append(common.parent / ".tools")
    for tools_root in roots:
        candidate = tools_root / relative
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        f"proof checker {relative} not found under any of: "
        + ", ".join(map(str, roots))
    )


def parse_graph6(text: str) -> tuple[int, list[tuple[int, int]]]:
    text = text.strip()
    assert text and not text.startswith("~~")
    if text.startswith("~"):
        assert len(text) >= 4
        vertices = sum(
            (ord(text[index]) - 63) << shift
            for index, shift in zip((1, 2, 3), (12, 6, 0))
        )
        payload = text[4:]
    else:
        vertices = ord(text[0]) - 63
        payload = text[1:]
    bits = []
    for character in payload:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    position = 0
    for high in range(1, vertices):
        for low in range(high):
            if bits[position]:
                edges.append((low, high))
            position += 1
    return vertices, edges


def encode_graph6(vertices: int, edges: list[tuple[int, int]]) -> str:
    edge_set = set(edges)
    bits = [
        int((low, high) in edge_set)
        for high in range(1, vertices)
        for low in range(high)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    if vertices < 63:
        prefix = chr(vertices + 63)
    else:
        prefix = "~" + "".join(
            chr(63 + ((vertices >> shift) & 63))
            for shift in (12, 6, 0)
        )
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


def reconstruct() -> tuple[list[tuple[int, int]], list[int]]:
    vertices, core = parse_graph6(CORE_GRAPH6)
    assert vertices == 60 and len(core) == 90
    marks = {edge: index for index, edge in enumerate(MARKS)}
    raw = []
    cut_raw = []
    for side in range(2):
        offset = 65 * side
        for edge in core:
            if edge in marks:
                terminal = offset + 60 + marks[edge]
                raw.extend(
                    (
                        tuple(sorted((offset + edge[0], terminal))),
                        tuple(sorted((offset + edge[1], terminal))),
                    )
                )
            else:
                raw.append(
                    tuple(sorted((offset + edge[0], offset + edge[1])))
                )
    for index in range(5):
        cut_raw.append(len(raw))
        raw.append((60 + index, 125 + index))
    order = sorted(range(len(raw)), key=raw.__getitem__)
    inverse = {old: new for new, old in enumerate(order)}
    return [raw[old] for old in order], sorted(inverse[x] for x in cut_raw)


def incident(
    vertices: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    rows = [[] for _ in range(vertices)]
    for edge_id, (left, right) in enumerate(edges):
        rows[left].append(edge_id)
        rows[right].append(edge_id)
    return rows


def components(
    vertices: int,
    edges: list[tuple[int, int]],
    retained: set[int],
) -> list[set[int]]:
    adjacency = [[] for _ in range(vertices)]
    for edge_id in retained:
        left, right = edges[edge_id]
        adjacency[left].append(right)
        adjacency[right].append(left)
    unseen = set(range(vertices))
    result = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        part = {root}
        queue = [root]
        while queue:
            for other in adjacency[queue.pop()]:
                if other in unseen:
                    unseen.remove(other)
                    part.add(other)
                    queue.append(other)
        result.append(part)
    return result


def bridges(
    vertices: int,
    edges: list[tuple[int, int]],
    skipped: int | None = None,
) -> list[int]:
    rows = incident(vertices, edges)
    discovery = [-1] * vertices
    low = [-1] * vertices
    parent_edge = [-1] * vertices
    result = []
    clock = 0

    def visit(vertex: int) -> None:
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        for edge_id in rows[vertex]:
            if edge_id == skipped:
                continue
            left, right = edges[edge_id]
            other = right if left == vertex else left
            if discovery[other] < 0:
                parent_edge[other] = edge_id
                visit(other)
                low[vertex] = min(low[vertex], low[other])
                if low[other] > discovery[vertex]:
                    result.append(edge_id)
            elif edge_id != parent_edge[vertex]:
                low[vertex] = min(low[vertex], discovery[other])

    for vertex in range(vertices):
        if discovery[vertex] < 0:
            visit(vertex)
    return sorted(result)


def girth(vertices: int, edges: list[tuple[int, int]]) -> int:
    adjacency = [[] for _ in range(vertices)]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    answer = vertices + 1
    for root in range(vertices):
        distance = [-1] * vertices
        parent = [-1] * vertices
        distance[root] = 0
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for other in adjacency[vertex]:
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    answer = min(
                        answer, distance[vertex] + distance[other] + 1
                    )
    return answer


def first_cyclic_two_cut(
    vertices: int, edges: list[tuple[int, int]]
) -> tuple[int, int] | None:
    all_edges = set(range(len(edges)))
    for first in range(len(edges)):
        for second in bridges(vertices, edges, skipped=first):
            if first >= second:
                continue
            parts = components(
                vertices, edges, all_edges - {first, second}
            )
            if len(parts) != 2:
                continue
            cyclic = []
            for part in parts:
                internal = sum(
                    left in part and right in part for left, right in edges
                )
                cyclic.append(internal >= len(part))
            if all(cyclic):
                return first, second
    return None


def parity_clauses(variables: tuple[int, ...]) -> list[tuple[int, ...]]:
    clauses = []
    for word in range(1 << len(variables)):
        if word.bit_count() & 1:
            clauses.append(
                tuple(
                    -variable if (word >> index) & 1 else variable
                    for index, variable in enumerate(variables)
                )
            )
    return clauses


def at_most(
    inputs: tuple[int, ...],
    bound: int,
    first_auxiliary: int,
) -> tuple[int, list[tuple[int, ...]]]:
    counter = {}
    next_variable = first_auxiliary
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


def independent_flow_cnf(
    vertices: int, edges: list[tuple[int, int]]
) -> tuple[int, list[tuple[int, ...]]]:
    rows = incident(vertices, edges)
    clauses = []
    for row in rows:
        for bit in range(2):
            clauses.extend(
                parity_clauses(
                    tuple(2 * edge_id + bit + 1 for edge_id in row)
                )
            )
    edge_count = len(edges)
    zeros = []
    for edge_id in range(edge_count):
        first = 2 * edge_id + 1
        second = first + 1
        zero = 2 * edge_count + edge_id + 1
        zeros.append(zero)
        clauses.extend(
            ((-zero, -first), (-zero, -second), (zero, first, second))
        )
    variables, cardinality = at_most(
        tuple(zeros), 4, 3 * edge_count + 1
    )
    return variables, clauses + cardinality


def block(kind: int, edge_id: int, edge_count: int) -> int:
    return 1 + kind * edge_count + edge_id


def independent_extension_cnf(
    vertices: int, edges: list[tuple[int, int]]
) -> tuple[int, list[tuple[int, ...]]]:
    edge_count = len(edges)
    clauses = []
    for edge_id in range(edge_count):
        match = block(0, edge_id, edge_count)
        first = block(1, edge_id, edge_count)
        second = block(2, edge_id, edge_count)
        flow_zero = block(3, edge_id, edge_count)
        flow_one = block(4, edge_id, edge_count)
        clauses.extend(
            (
                (-match, first),
                (-match, second),
                (match, -first, -second),
                (-match, -flow_zero),
                (-match, -flow_one),
                (match, flow_zero, flow_one),
            )
        )
    rows = incident(vertices, edges)
    for row in rows:
        for first, second in combinations(row, 2):
            clauses.append(
                (
                    -block(0, first, edge_count),
                    -block(0, second, edge_count),
                )
            )
    for row in rows:
        for kind in (1, 2, 3, 4):
            clauses.extend(
                parity_clauses(
                    tuple(
                        block(kind, edge_id, edge_count)
                        for edge_id in row
                    )
                )
            )
    variables, cardinality = at_most(
        tuple(block(0, edge_id, edge_count) for edge_id in range(edge_count)),
        5,
        5 * edge_count + 1,
    )
    return variables, clauses + cardinality


def parse_cnf(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables = None
    declared = None
    clauses = []
    for raw in path.read_text(encoding="ascii").splitlines():
        if not raw or raw.startswith("c"):
            continue
        if raw.startswith("p "):
            _, kind, variable_text, clause_text = raw.split()
            assert kind == "cnf" and variables is None
            variables = int(variable_text)
            declared = int(clause_text)
            continue
        literals = tuple(map(int, raw.split()))
        assert literals[-1] == 0
        clauses.append(literals[:-1])
    assert variables is not None and declared == len(clauses)
    return variables, clauses


def verify_flow(
    vertices: int,
    edges: list[tuple[int, int]],
    values: list[int],
) -> list[int]:
    assert len(values) == len(edges)
    balance = [0] * vertices
    for (left, right), value in zip(edges, values):
        assert 0 <= value <= 3
        balance[left] ^= value
        balance[right] ^= value
    assert not any(balance)
    return [
        edge_id for edge_id, value in enumerate(values) if value == 0
    ]


def verify_cycle(
    vertices: int,
    edges: list[tuple[int, int]],
    selected: set[int],
) -> None:
    degrees = [0] * vertices
    for edge_id in selected:
        left, right = edges[edge_id]
        degrees[left] += 1
        degrees[right] += 1
    assert all(degree % 2 == 0 for degree in degrees)


def verify_extension(
    vertices: int,
    edges: list[tuple[int, int]],
    record: dict[str, object],
) -> dict[str, object]:
    matching = set(map(int, record["matching_edges"]))
    first = set(map(int, record["cycle_a"]))
    second = set(map(int, record["cycle_b"]))
    flow = list(map(int, record["flow_values"]))
    assert len(matching) == 6
    assert first & second == matching
    rows = incident(vertices, edges)
    assert all(sum(edge in matching for edge in row) <= 1 for row in rows)
    verify_cycle(vertices, edges, first)
    verify_cycle(vertices, edges, second)
    assert set(verify_flow(vertices, edges, flow)) == matching

    labels = list(map(str, record["five_cdc_labels"]))
    assert len(labels) == len(edges)
    parity = [[0] * 5 for _ in range(vertices)]
    counts = [0] * 5
    for (left, right), label in zip(edges, labels):
        coordinates = tuple(map(int, label))
        assert (
            len(coordinates) == 2
            and coordinates[0] < coordinates[1]
            and all(0 <= coordinate < 5 for coordinate in coordinates)
        )
        for coordinate in coordinates:
            counts[coordinate] += 1
            parity[left][coordinate] ^= 1
            parity[right][coordinate] ^= 1
    assert not any(value for row in parity for value in row)
    return {
        "matching_edges": sorted(matching),
        "coordinate_sizes": counts,
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    edges, cut = reconstruct()
    assert len(edges) == 195 and len(set(edges)) == 195
    rows = incident(130, edges)
    assert all(len(row) == 3 for row in rows)
    stored_graph = json.loads((HERE / "graph.json").read_text())
    assert stored_graph["vertices"] == 130
    assert [
        (edge["u"], edge["v"]) for edge in stored_graph["edges"]
    ] == edges
    assert (HERE / "graph.g6").read_text().strip() == encode_graph6(
        130, edges
    )

    graph_bridges = bridges(130, edges)
    assert not graph_bridges
    assert len(components(130, edges, set(range(len(edges))))) == 1
    graph_girth = girth(130, edges)
    assert graph_girth == 4
    cyclic_two_cut = first_cyclic_two_cut(130, edges)
    assert cyclic_two_cut is None
    cyclic_three_cut = (0, 32, 97)
    three_cut_components = components(
        130,
        edges,
        set(range(len(edges))) - set(cyclic_three_cut),
    )
    assert len(three_cut_components) == 2
    for component in three_cut_components:
        internal_edges = sum(
            left in component and right in component
            for left, right in edges
        )
        assert internal_edges >= len(component)

    witness = json.loads((HERE / "witness.json").read_text())
    assert witness["displayed_zero_cut"] == cut
    displayed_zeros = verify_flow(
        130, edges, list(map(int, witness["displayed_flow_values"]))
    )
    assert displayed_zeros == cut
    assert all(sum(edge in set(cut) for edge in row) <= 1 for row in rows)
    cut_components = components(
        130, edges, set(range(len(edges))) - set(cut)
    )
    assert sorted(map(len, cut_components)) == [65, 65]
    terminal_counts = sorted(
        sum(
            int(left in component) + int(right in component)
            for edge_id, (left, right) in enumerate(edges)
            if edge_id in set(cut)
        )
        for component in cut_components
    )
    assert terminal_counts == [5, 5]

    expected_flow = independent_flow_cnf(130, edges)
    actual_flow = parse_cnf(HERE / "flow-at-most-four-zero.cnf")
    assert actual_flow[0] == expected_flow[0]
    assert sorted(actual_flow[1]) == sorted(expected_flow[1])
    expected_extension = independent_extension_cnf(130, edges)
    actual_extension = parse_cnf(HERE / "extension-at-most-five.cnf")
    assert actual_extension[0] == expected_extension[0]
    assert sorted(actual_extension[1]) == sorted(expected_extension[1])

    checkers = (
        (
            "lrat-check",
            locate_checker(Path("cert-checkers/drat-trim/lrat-check")),
        ),
        (
            "cake_lpr",
            locate_checker(Path("cert-checkers/cake_lpr/cake_lpr")),
        ),
    )
    proof_results = {}
    for stem in ("flow-at-most-four-zero", "extension-at-most-five"):
        cnf = HERE / f"{stem}.cnf"
        proof = HERE / f"{stem}.lrat"
        assert proof.is_file() and proof.stat().st_size > 0
        proof_results[stem] = {}
        for name, checker in checkers:
            result = subprocess.run(
                [str(checker), str(cnf), str(proof)],
                capture_output=True,
                text=True,
                check=False,
            )
            assert result.returncode == 0, result.stdout + result.stderr
            proof_results[stem][name] = "PASS"

    extension_result = verify_extension(
        130, edges, witness["minimum_extending_witness"]
    )
    claims = witness["claims"]
    assert claims == {
        "five_cdc_counterexample": False,
        "flow_resistance": 5,
        "minimum_exact_zero_matching_size": 5,
        "minimum_extending_matching_size": 6,
        "standard_five_cdc": True,
    }

    ledger = {}
    for line in (HERE / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        ledger[name] = digest
    for name, digest in ledger.items():
        assert sha256(HERE / name) == digest
    assert set(ledger) == {
        path.name
        for path in HERE.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    }

    print(
        json.dumps(
            {
                "classification": (
                    "EXACT MINIMUM-ZERO EXCHANGE COUNTERMODEL; "
                    "STANDARD FIVE-CDC POSITIVE"
                ),
                "vertices": 130,
                "edges": 195,
                "simple": True,
                "cubic": True,
                "connected": True,
                "bridgeless": True,
                "girth": graph_girth,
                "cyclic_edge_connectivity": 3,
                "cyclic_three_edge_cut": list(cyclic_three_cut),
                "displayed_minimum_zero_cut": cut,
                "displayed_complement_terminal_profile": terminal_counts,
                "flow_resistance": 5,
                "minimum_exact_zero_matching_size": 5,
                "minimum_extending_matching_size": 6,
                "positive_extension": extension_result,
                "proof_checks": proof_results,
                "standard_five_cdc": "PASS",
                "five_cdc_counterexample": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
