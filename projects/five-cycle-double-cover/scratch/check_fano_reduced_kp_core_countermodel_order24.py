#!/usr/bin/env python3
"""Independent finite replay of the order-24 clean-core countermodel.

The checker uses only the Python standard library.  It literally enumerates
the affine space of T-joins for every Fano value class before and after the
displayed switch.  Its conclusion concerns the clean-suppressed-core
shortcut only, not the reduced one-switch lemma or FiveCDC.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "fano-reduced-kp-core-countermodel-order24.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(record: str) -> tuple[int, list[tuple[int, int]]]:
    require(record and record[0] != "~", "only small graph6 is supported")
    order = ord(record[0]) - 63
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            require(cursor < len(bits), "truncated graph6")
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, edges


def incidence(
    order: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    answer = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        answer[left].append(edge)
        answer[right].append(edge)
    return answer


def components(
    order: int,
    edges: list[tuple[int, int]],
    kept: set[int],
) -> list[set[int]]:
    adjacency = [[] for _ in range(order)]
    for edge in kept:
        left, right = edges[edge]
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen: set[int] = set()
    answer: list[set[int]] = []
    for start in range(order):
        if start in seen:
            continue
        piece = {start}
        seen.add(start)
        queue = [start]
        for vertex in queue:
            for other in adjacency[vertex]:
                if other not in seen:
                    seen.add(other)
                    piece.add(other)
                    queue.append(other)
        answer.append(piece)
    return answer


def has_cycle(
    piece: set[int],
    edges: list[tuple[int, int]],
    kept: set[int],
) -> bool:
    internal = sum(
        left in piece and right in piece
        for edge, (left, right) in enumerate(edges)
        if edge in kept
    )
    return internal >= len(piece)


def fundamental_cycle_basis(
    order: int,
    edges: list[tuple[int, int]],
    kept: set[int],
) -> tuple[int, list[int]]:
    inc = incidence(order, edges)
    parent = [-1] * order
    parent_edge = [-1] * order
    depth = [0] * order
    tree_edges: set[int] = set()
    components_count = 0
    for root in range(order):
        if parent[root] >= 0:
            continue
        components_count += 1
        parent[root] = root
        queue = [root]
        for vertex in queue:
            for edge in inc[vertex]:
                if edge not in kept:
                    continue
                left, right = edges[edge]
                other = left ^ right ^ vertex
                if parent[other] >= 0:
                    continue
                parent[other] = vertex
                parent_edge[other] = edge
                depth[other] = depth[vertex] + 1
                tree_edges.add(edge)
                queue.append(other)
    basis: list[int] = []
    for edge in sorted(kept - tree_edges):
        mask = 1 << edge
        left, right = edges[edge]
        while depth[left] > depth[right]:
            mask ^= 1 << parent_edge[left]
            left = parent[left]
        while depth[right] > depth[left]:
            mask ^= 1 << parent_edge[right]
            right = parent[right]
        while left != right:
            mask ^= 1 << parent_edge[left]
            left = parent[left]
            mask ^= 1 << parent_edge[right]
            right = parent[right]
        basis.append(mask)
    return components_count, basis


def one_t_join(
    order: int,
    edges: list[tuple[int, int]],
    kept: set[int],
    terminal: list[int],
) -> int:
    inc = incidence(order, edges)
    parent = [-1] * order
    parent_edge = [-1] * order
    children_order: list[int] = []
    roots: list[int] = []
    for root in range(order):
        if parent[root] >= 0:
            continue
        roots.append(root)
        parent[root] = root
        queue = [root]
        for vertex in queue:
            children_order.append(vertex)
            for edge in inc[vertex]:
                if edge not in kept:
                    continue
                left, right = edges[edge]
                other = left ^ right ^ vertex
                if parent[other] >= 0:
                    continue
                parent[other] = vertex
                parent_edge[other] = edge
                queue.append(other)
    parity = [0] * order
    answer = 0
    for vertex in reversed(children_order):
        if vertex in roots:
            require(
                parity[vertex] == terminal[vertex],
                "component has odd terminal parity",
            )
            continue
        if parity[vertex] != terminal[vertex]:
            edge = parent_edge[vertex]
            answer ^= 1 << edge
            parity[vertex] ^= 1
            parity[parent[vertex]] ^= 1
    return answer


def packs_two_t_joins(
    order: int,
    edges: list[tuple[int, int]],
    matching: set[int],
) -> bool:
    all_edges = set(range(len(edges)))
    kept = all_edges - matching
    terminal = [0] * order
    for edge in matching:
        left, right = edges[edge]
        terminal[left] ^= 1
        terminal[right] ^= 1
    base = one_t_join(order, edges, kept, terminal)
    _, basis = fundamental_cycle_basis(order, edges, kept)
    joins: list[int] = []
    for choice in range(1 << len(basis)):
        join = base
        for bit, cycle in enumerate(basis):
            if (choice >> bit) & 1:
                join ^= cycle
        joins.append(join)
    return any(
        left & right == 0
        for index, left in enumerate(joins)
        for right in joins[index:]
    )


def successful_values(
    order: int,
    edges: list[tuple[int, int]],
    flow: list[int],
) -> list[int]:
    return [
        value
        for value in range(1, 8)
        if packs_two_t_joins(
            order,
            edges,
            {edge for edge, item in enumerate(flow) if item == value},
        )
    ]


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    order, edges = decode_graph6(data["graph6"])
    require(order == 24, "wrong order")
    require(
        [list(edge) for edge in edges] == data["edge_order"],
        "graph6/edge-order mismatch",
    )
    flow = list(data["flow_values_by_edge"])
    require(len(edges) == len(flow) == 36, "wrong edge count")
    require(len(set(edges)) == len(edges), "parallel edge")
    require(all(left != right for left, right in edges), "loop")
    inc = incidence(order, edges)
    require(all(len(row) == 3 for row in inc), "not cubic")
    require(
        components(order, edges, set(range(len(edges))))
        == [set(range(order))],
        "not connected",
    )
    certificate = data["nonplanarity_certificate"]
    left_branch = set(certificate["left_branch_vertices"])
    right_branch = set(certificate["right_branch_vertices"])
    paths = [list(path) for path in certificate["paths"]]
    require(
        len(paths) == len(left_branch) * len(right_branch) == 9,
        "wrong K3,3 path count",
    )
    endpoint_pairs: set[tuple[int, int]] = set()
    internal_vertices: set[int] = set()
    graph_edge_set = {frozenset(edge) for edge in edges}
    for path in paths:
        require(
            (path[0] in left_branch and path[-1] in right_branch)
            or (path[-1] in left_branch and path[0] in right_branch),
            "K3,3 path has wrong branch endpoints",
        )
        left = path[0] if path[0] in left_branch else path[-1]
        right = path[-1] if path[-1] in right_branch else path[0]
        endpoint_pairs.add((left, right))
        for first, second in zip(path, path[1:]):
            require(
                frozenset((first, second)) in graph_edge_set,
                "K3,3 path uses a nonedge",
            )
        for vertex in path[1:-1]:
            require(
                vertex not in left_branch | right_branch,
                "K3,3 internal vertex is a branch vertex",
            )
            require(
                vertex not in internal_vertices,
                "K3,3 paths are not internally disjoint",
            )
            internal_vertices.add(vertex)
    require(
        endpoint_pairs
        == {(left, right) for left in left_branch for right in right_branch},
        "K3,3 branch pair missing",
    )
    require(
        all(
            flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0
            for row in inc
        ),
        "flow conservation failed",
    )
    require(all(1 <= value <= 7 for value in flow), "zero flow value")
    for value in range(1, 8):
        endpoints: set[int] = set()
        for edge, item in enumerate(flow):
            if item != value:
                continue
            left, right = edges[edge]
            require(left not in endpoints and right not in endpoints,
                    "value class is not a matching")
            endpoints.update((left, right))

    all_edges = set(range(len(edges)))
    for size in range(1, 4):
        for removed in combinations(range(len(edges)), size):
            kept = all_edges - set(removed)
            pieces = components(order, edges, kept)
            require(
                sum(has_cycle(piece, edges, kept) for piece in pieces) < 2,
                "cyclic edge cut below four",
            )
    displayed_four_cut = {1, 12, 17, 20}
    pieces = components(order, edges, all_edges - displayed_four_cut)
    require(
        sum(
            has_cycle(piece, edges, all_edges - displayed_four_cut)
            for piece in pieces
        )
        >= 2,
        "displayed cyclic four-cut failed",
    )

    for row in data["suppressed_core_obstructions"]:
        value = row["t"]
        matching = {edge for edge, item in enumerate(flow) if item == value}
        kept = all_edges - matching - set(row["bond_edge_ids"])
        pieces = components(order, edges, kept)
        require(len(pieces) == 2, f"t={value}: not a two-bond")
        degree_in_complement = [
            sum(edge not in matching for edge in inc[vertex])
            for vertex in range(order)
        ]
        require(
            all(any(degree_in_complement[v] == 3 for v in piece)
                for piece in pieces),
            f"t={value}: bond only isolates a suppressed path",
        )
        shore = set(row["small_shore"])
        require(shore in pieces, f"t={value}: wrong shore")
        cut = {
            edge
            for edge, (left, right) in enumerate(edges)
            if (left in shore) ^ (right in shore)
        }
        require(
            cut == set(row["G_cut_edge_ids"]),
            f"t={value}: wrong lifted G-cut",
        )
        require(
            set(row["bond_edge_ids"]) == cut - matching,
            f"t={value}: G-M_t boundary is not the displayed bond",
        )

    require(
        successful_values(order, edges, flow) == [],
        "initial flow is not bad",
    )
    repair = data["repair"]
    switch_value = repair["switch_value"]
    circuit = set(repair["circuit_edge_ids"])
    require(
        all(flow[edge] != switch_value for edge in circuit),
        "repair circuit meets forbidden value class",
    )
    circuit_degree = [0] * order
    for edge in circuit:
        left, right = edges[edge]
        circuit_degree[left] += 1
        circuit_degree[right] += 1
    active = {vertex for vertex, degree in enumerate(circuit_degree) if degree}
    require(
        all(circuit_degree[vertex] == 2 for vertex in active),
        "repair support is not Eulerian",
    )
    circuit_pieces = components(order, edges, circuit)
    require(
        sum(bool(piece & active) for piece in circuit_pieces) == 1,
        "repair support is not connected",
    )
    switched = [
        value ^ switch_value if edge in circuit else value
        for edge, value in enumerate(flow)
    ]
    require(
        switched == repair["resulting_flow_values_by_edge"],
        "wrong switched flow",
    )
    require(
        successful_values(order, edges, switched)
        == repair["resulting_successful_values"]
        == [3],
        "repair packing claim failed",
    )
    packing = repair["value_3_packing_certificate"]
    matching = {
        edge for edge, value in enumerate(switched) if value == 3
    }
    require(
        matching == set(packing["matching_edge_ids"]),
        "explicit packing has wrong matching",
    )
    first_join = set(packing["first_T_join_edge_ids"])
    second_join = set(packing["second_T_join_edge_ids"])
    require(not (first_join & second_join), "explicit joins intersect")
    require(not ((first_join | second_join) & matching),
            "explicit join uses a matching edge")
    matching_boundary = [0] * order
    for edge in matching:
        left, right = edges[edge]
        matching_boundary[left] ^= 1
        matching_boundary[right] ^= 1
    for name, join in (("first", first_join), ("second", second_join)):
        boundary = [0] * order
        for edge in join:
            left, right = edges[edge]
            boundary[left] ^= 1
            boundary[right] ^= 1
        require(
            boundary == matching_boundary,
            f"explicit {name} set is not a boundary T-join",
        )

    print("independent order-24 clean-core countermodel checker: PASS")
    print("initial successful values: []")
    print("all seven suppressed complements have a nontrivial two-bond")
    print("one legal value-1 circuit switch makes value 3 successful")
    print("scope: auxiliary shortcut refuted; reduced lemma and FiveCDC remain open")


if __name__ == "__main__":
    main()
