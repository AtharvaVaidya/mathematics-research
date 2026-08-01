#!/usr/bin/env python3
"""Dependency-free verifier for the reconstructed packing certificate.

The program checks only finite/combinatorial assertions.  Global minimality
for every n is imported from MNP Lemma 3.5 and Theorem 3.6, as recorded in
certificate.json; this program does not pretend to reprove that infinite
lower bound.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROLES = ("alpha", "gamma", "beta", "delta", "epsilon")


def fail(message: str) -> None:
    raise AssertionError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def check_manifest() -> None:
    ledger = {}
    for line in (HERE / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        digest, name = line.split("  ", 1)
        ledger[name] = digest
    require(
        set(ledger)
        == {
            "README.md",
            "THEOREM.md",
            "certificate.json",
            "verification.json",
            "verify.py",
        },
        "unexpected manifest contents",
    )
    for name, expected in ledger.items():
        actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        require(actual == expected, f"manifest mismatch: {name}")


def decode_graph6(text: str) -> tuple[int, list[tuple[int, int]]]:
    """Decode graph6 without networkx; return lexicographically sorted edges."""
    text = text.strip()
    if text.startswith(">>graph6<<"):
        text = text[len(">>graph6<<") :]
    data = [ord(char) - 63 for char in text]
    require(data and all(0 <= item <= 63 for item in data), "bad graph6 byte")
    if data[0] != 63:
        order, position = data[0], 1
    elif data[1] != 63:
        order = (data[1] << 12) | (data[2] << 6) | data[3]
        position = 4
    else:
        order = 0
        for item in data[2:8]:
            order = (order << 6) | item
        position = 8
    bits: list[int] = []
    for item in data[position:]:
        bits.extend((item >> shift) & 1 for shift in range(5, -1, -1))
    need = order * (order - 1) // 2
    require(len(bits) >= need, "truncated graph6")
    edges: list[tuple[int, int]] = []
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                edges.append((low, high))
            cursor += 1
    return order, sorted(edges)


def stable_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def boundary(edges: set[tuple[int, int]]) -> set[int]:
    odd: set[int] = set()
    for u, v in edges:
        odd.symmetric_difference_update((u, v))
    return odd


def validate_graph(vertices: set[int], labels: dict[tuple[int, int], str]) -> dict:
    require(labels, "empty graph")
    adjacency = {vertex: set() for vertex in vertices}
    for edge in labels:
        u, v = edge
        require(u < v, f"non-normalized edge {edge}")
        require(u in vertices and v in vertices, f"unknown endpoint in {edge}")
        require(v not in adjacency[u], f"duplicate edge {edge}")
        adjacency[u].add(v)
        adjacency[v].add(u)
    require(all(len(adjacency[v]) == 3 for v in vertices), "graph is not cubic")

    seen = {min(vertices)}
    queue = deque(seen)
    while queue:
        vertex = queue.popleft()
        for other in adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                queue.append(other)
    require(seen == vertices, "graph is disconnected")

    # Iterative Tarjan low-link bridge test.  Keeping this iterative lets the
    # checker handle arbitrarily long requested prefixes without depending
    # on Python's recursion limit.
    root = min(vertices)
    entered = {root: 0}
    low = {root: 0}
    parent: dict[int, int | None] = {root: None}
    timer = 1
    bridges: list[tuple[int, int]] = []
    stack: list[tuple[int, object]] = [(root, iter(adjacency[root]))]
    while stack:
        vertex, iterator = stack[-1]
        try:
            other = next(iterator)
        except StopIteration:
            stack.pop()
            previous = parent[vertex]
            if previous is not None:
                low[previous] = min(low[previous], low[vertex])
                if low[vertex] > entered[previous]:
                    bridges.append(tuple(sorted((previous, vertex))))
            continue
        if other == parent[vertex]:
            continue
        if other in entered:
            low[vertex] = min(low[vertex], entered[other])
            continue
        parent[other] = vertex
        entered[other] = timer
        low[other] = timer
        timer += 1
        stack.append((other, iter(adjacency[other])))
    require(not bridges, f"bridges found: {bridges[:3]}")

    # Shortest cycle length by deleting each edge and finding a shortest
    # path between its ends.  Used only as a scope check, never as a theorem
    # about girth at least ten.
    girth = len(vertices) + 1
    for source, target in labels:
        distances = {source: 0}
        bfs = deque((source,))
        while bfs:
            vertex = bfs.popleft()
            if distances[vertex] + 1 >= girth:
                continue
            for other in adjacency[vertex]:
                if (vertex == source and other == target) or (
                    vertex == target and other == source
                ):
                    continue
                if other not in distances:
                    distances[other] = distances[vertex] + 1
                    bfs.append(other)
        if target in distances:
            girth = min(girth, distances[target] + 1)
    require(girth <= len(vertices), "acyclic cubic graph")
    return {"connected": True, "cubic": True, "bridgeless": True, "girth": girth}


def label_bits(name: str, data: dict) -> tuple[int, int]:
    bits = data["labels"][name]
    require(bits in ([0, 0], [1, 0], [0, 1], [1, 1]), "bad label")
    return bits[0], bits[1]


def check_tile(data: dict) -> tuple[list[tuple[int, int]], dict[tuple[int, int], str]]:
    tile = data["tile"]
    order, edges = decode_graph6(tile["closed_J_graph6"])
    require(order == 42 and len(edges) == 63, "wrong closed J dimensions")
    require(
        stable_digest(edges) == tile["closed_J_edge_list_sha256"],
        "closed J digest mismatch",
    )
    omit = set(tile["omitted_edge_ids"])
    require(omit == {4, 12, 39, 56, 57, 59, 61, 62}, "wrong omitted IDs")
    internal_ids = set(range(63)) - omit
    first_ids = set(tile["internal_J1_edge_ids"])
    second_ids = set(tile["internal_J2_edge_ids"])
    require(first_ids <= internal_ids and second_ids <= internal_ids, "join outside tile")
    require(first_ids.isdisjoint(second_ids), "tile joins overlap")
    internal_labels: dict[tuple[int, int], str] = {}
    for edge_id in internal_ids:
        edge = edges[edge_id]
        internal_labels[edge] = (
            "J1" if edge_id in first_ids else "J2" if edge_id in second_ids else "R"
        )

    input_ends = tile["input_attachment_by_role"]
    output_ends = tile["output_attachment_by_role"]
    require(set(input_ends) == set(ROLES), "missing input role")
    require(set(output_ends) == set(ROLES), "missing output role")
    require(len(set(input_ends.values())) == 5, "repeated input attachment")
    require(len(set(output_ends.values())) == 5, "repeated output attachment")
    state = tile["state_by_role"]
    internal_vertices = set(range(42)) - {38, 39}
    incidence_rows = []
    for vertex in sorted(internal_vertices):
        objects: list[tuple[str, str]] = []
        parity = [0, 0]
        for edge_id in sorted(internal_ids):
            if vertex in edges[edge_id]:
                category = (
                    "J1"
                    if edge_id in first_ids
                    else "J2"
                    if edge_id in second_ids
                    else "R"
                )
                objects.append((f"e{edge_id}", category))
                bits = label_bits(category, data)
                parity[0] ^= bits[0]
                parity[1] ^= bits[1]
        for side, attachments in (("in", input_ends), ("out", output_ends)):
            for role in ROLES:
                if attachments[role] == vertex:
                    category = state[role]
                    objects.append((f"{side}:{role}", category))
                    bits = label_bits(category, data)
                    parity[0] ^= bits[0]
                    parity[1] ^= bits[1]
        require(len(objects) == 3, f"tile vertex {vertex} has {len(objects)} objects")
        require(parity == [0, 0], f"tile parity failure at vertex {vertex}")
        incidence_rows.append({"vertex": vertex, "objects": objects})

    require(len(internal_labels) == 55, "wrong internal edge count")
    return edges, internal_labels


def check_packing(
    n: int,
    vertices: set[int],
    labels: dict[tuple[int, int], str],
    closure: dict,
    data: dict,
) -> dict:
    graph = validate_graph(vertices, labels)
    allowed = {"R", "J1", "J2", "M"}
    require(set(labels.values()) <= allowed, "unknown category")
    classes = {
        category: {edge for edge, label in labels.items() if label == category}
        for category in ("R", "J1", "J2", "M")
    }
    require(sum(map(len, classes.values())) == len(labels), "classes do not partition")
    require(classes["J1"].isdisjoint(classes["J2"]), "joins overlap")
    require(classes["M"].isdisjoint(classes["J1"] | classes["J2"]), "join meets M")
    m_vertices = [vertex for edge in classes["M"] for vertex in edge]
    require(len(m_vertices) == len(set(m_vertices)), "M is not a matching")
    terminals = boundary(classes["M"])
    require(boundary(classes["J1"]) == terminals, "J1 is not a boundary(M)-join")
    require(boundary(classes["J2"]) == terminals, "J2 is not a boundary(M)-join")

    expected = {
        "vertices": 40 * n + 2,
        "edges": 60 * n + 3,
        "M": n,
        "J1": 12 * n + 3,
        "J2": 11 * n + 26,
        "R": 36 * n - 26,
    }
    actual = {
        "vertices": len(vertices),
        "edges": len(labels),
        **{category: len(edges) for category, edges in classes.items()},
    }
    require(actual == expected, f"count formula mismatch at n={n}: {actual}")

    terminal = closure["terminal_by_role"]
    x = closure["x"]
    state = closure["state_by_role"]
    pair = tuple(sorted((terminal["alpha"], terminal["gamma"])))
    require(labels.get(pair) == state["alpha"] == state["gamma"], "bad alpha-gamma")
    for role in ("beta", "delta", "epsilon"):
        edge = tuple(sorted((x, terminal[role])))
        require(labels.get(edge) == state[role], f"bad closure state at {role}")
    require(graph["girth"] == 5, f"unexpected girth at n={n}")
    return {
        "n": n,
        "graph": {
            "vertices": len(vertices),
            "edges": len(labels),
            **graph,
            "edge_list_sha256": stable_digest(sorted(labels)),
        },
        "class_sizes": {category: len(classes[category]) for category in classes},
        "terminals": len(terminals),
        "stable_closure": True,
        "two_disjoint_boundary_joins": True,
    }


def extend(
    vertices: set[int],
    labels: dict[tuple[int, int], str],
    closure: dict,
    tile_edges: list[tuple[int, int]],
    tile_internal_labels: dict[tuple[int, int], str],
    data: dict,
) -> tuple[set[int], dict[tuple[int, int], str], dict]:
    """Perform one literal recurring substitution and propagate categories."""
    old_x = closure["x"]
    terminal = closure["terminal_by_role"]
    old_closure_edges = {
        tuple(sorted((terminal["alpha"], terminal["gamma"]))),
        *(tuple(sorted((old_x, terminal[role]))) for role in ("beta", "delta", "epsilon")),
    }
    require(len(old_closure_edges) == 4, "degenerate old closure")
    require(all(edge in labels for edge in old_closure_edges), "old closure edge missing")
    require(
        {labels[edge] for edge in old_closure_edges} == {"R", "J1", "J2", "M"},
        "old closure categories wrong",
    )

    survivors = sorted(vertices - {old_x})
    old_to_new = {vertex: index for index, vertex in enumerate(survivors)}
    new_labels: dict[tuple[int, int], str] = {}
    for edge, category in labels.items():
        if edge in old_closure_edges:
            continue
        require(old_x not in edge, "unrecorded edge at old closure vertex")
        mapped = tuple(sorted((old_to_new[edge[0]], old_to_new[edge[1]])))
        require(mapped not in new_labels, "old-edge collision")
        new_labels[mapped] = category

    # The open tile removes local 38 and 39, after which a fresh output
    # closure vertex is inserted.  It is harmless and convenient to give
    # that fresh vertex the old local name 39.
    local_order = list(range(38)) + [39, 40, 41]
    offset = len(survivors)
    local_to_new = {local: offset + index for index, local in enumerate(local_order)}
    for (u, v), category in tile_internal_labels.items():
        mapped = tuple(sorted((local_to_new[u], local_to_new[v])))
        require(mapped not in new_labels, "tile-edge collision")
        new_labels[mapped] = category

    tile = data["tile"]
    state = tile["state_by_role"]
    old_terminal_new = {role: old_to_new[terminal[role]] for role in ROLES}
    for role in ROLES:
        edge = tuple(
            sorted(
                (
                    old_terminal_new[role],
                    local_to_new[tile["input_attachment_by_role"][role]],
                )
            )
        )
        require(edge not in new_labels, "connector collision")
        new_labels[edge] = state[role]

    output = {
        role: local_to_new[tile["output_attachment_by_role"][role]] for role in ROLES
    }
    new_x = local_to_new[39]
    pair = tuple(sorted((output["alpha"], output["gamma"])))
    require(pair not in new_labels, "new pair-closure collision")
    new_labels[pair] = state["alpha"]
    for role in ("beta", "delta", "epsilon"):
        edge = tuple(sorted((new_x, output[role])))
        require(edge not in new_labels, "new spoke collision")
        new_labels[edge] = state[role]

    new_vertices = set(range(len(survivors) + len(local_order)))
    new_closure = {
        "x": new_x,
        "terminal_by_role": output,
        "state_by_role": state,
    }
    return new_vertices, new_labels, new_closure


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=20)
    args = parser.parse_args()
    require(args.max_n >= 5, "--max-n must be at least 5")
    check_manifest()
    data = json.loads((HERE / "certificate.json").read_text(encoding="utf-8"))

    tile_edges, tile_internal_labels = check_tile(data)
    base = data["h2_base"]
    order, base_edges = decode_graph6(base["graph6"])
    require(order == 82 and len(base_edges) == 123, "wrong H2 dimensions")
    require(stable_digest(base_edges) == base["edge_list_sha256"], "H2 digest mismatch")
    base_sets = {
        "M": set(base["minimum_zero_matching_edge_ids"]),
        "J1": set(base["J1_edge_ids"]),
        "J2": set(base["J2_edge_ids"]),
    }
    require(all(ids <= set(range(123)) for ids in base_sets.values()), "bad H2 edge ID")
    require(base_sets["J1"].isdisjoint(base_sets["J2"]), "base joins overlap")
    require(base_sets["M"].isdisjoint(base_sets["J1"] | base_sets["J2"]), "base M overlap")
    base_labels = {}
    for edge_id, edge in enumerate(base_edges):
        base_labels[edge] = (
            "M"
            if edge_id in base_sets["M"]
            else "J1"
            if edge_id in base_sets["J1"]
            else "J2"
            if edge_id in base_sets["J2"]
            else "R"
        )
    closure = base["closure"]
    vertices = set(range(order))
    labels = base_labels
    reports = []
    frozen = data["frozen_regression"]
    for n in range(2, args.max_n + 1):
        report = check_packing(n, vertices, labels, closure, data)
        if str(n) in frozen:
            expected = frozen[str(n)]
            require(
                report["graph"]["vertices"] == expected["vertices"]
                and report["graph"]["edges"] == expected["edges"]
                and report["graph"]["edge_list_sha256"] == expected["edge_list_sha256"],
                f"frozen H{n} regression mismatch",
            )
            report["frozen_regression"] = "PASS"
        reports.append(report)
        if n < args.max_n:
            vertices, labels, closure = extend(
                vertices,
                labels,
                closure,
                tile_edges,
                tile_internal_labels,
                data,
            )

    output = {
        "schema": "mnp-reconstructed-minimum-support-packing-verification-v1",
        "status": "PASS",
        "checked_n": [2, args.max_n],
        "finite_checks": {
            "literal_H2_base": True,
            "literal_open_tile_all_40_vertex_parities": True,
            "recursive_graph_and_packing_through_max_n": True,
            "frozen_H2_H5_edge_exact_regression": True,
            "simple_connected_cubic_bridgeless_girth5_through_max_n": True,
            "matching_and_two_edge_disjoint_boundary_joins_through_max_n": True,
            "closed_form_counts_through_max_n": True,
        },
        "imported_not_machine_reproved": {
            "MNP_flow_resistance_theorem": "r_f(H_n)=n",
            "MNP_exact_zero_support": "{epsilon_1,...,epsilon_n}",
            "reconstruction_identity": "conditional on audited figure transcription",
        },
        "sample_reports": [reports[0], *reports[1:4], reports[-1]],
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
