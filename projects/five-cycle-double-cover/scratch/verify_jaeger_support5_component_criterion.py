#!/usr/bin/env python3
"""Exhaustive audit of the five-point support component criterion.

The finite audit fixes, without loss under affine translation and GL(3,2),

    U0 = {0,1,2,3},  S = {0,4,5,6,7},  z = 4.

It enumerates every nowhere-zero F_2^3 flow on every connected simple
cubic graph through order eight.  For each flow it compares:

  (a) direct CSP existence of compatible local pair triangles in S;
  (b) even xor of the forced leaf port bits in every component of E0.

It also checks all local plane cases and the explicit 34-vertex support-5
witness independently.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter, deque


U0 = frozenset((0, 1, 2, 3))
S = frozenset((0, 4, 5, 6, 7))
Z = 4

GRAPH6_THROUGH_8 = (
    "C~",
    "EFz_",
    "EUxo",
    "G?zTb_",
    "GCrb`o",
    "GCZJd_",
    "GCXmd_",
    "GCY^B_",
)

GRAPH34 = (
    "as???SK????A?A?C_@_?B?@_??G??_I?GA_AA????_??@?????B??@_?"
    "o??????_C??CGO??B@????a????__??C@O??A?_"
)

FLOW34 = (
    6, 3, 5, 2, 4, 4, 3, 3, 3, 1, 6, 1, 5, 7, 4, 6, 5,
    3, 3, 7, 6, 1, 3, 7, 4, 6, 2, 2, 5, 1, 2, 7, 4, 7,
    1, 4, 7, 3, 1, 4, 5, 5, 3, 7, 2, 6, 3, 5, 1, 7, 6,
)

# The displayed support in the witness is {3,4,5,6,7}; translate every
# point by the affine-plane missing point 3 to obtain canonical S.
LABELS34_TRANSLATED = (
    (0, 6), (5, 6), (0, 5), (4, 6), (0, 4), (0, 4), (4, 7),
    (5, 6), (5, 6), (6, 7), (0, 6), (4, 5), (0, 5), (0, 7),
    (0, 4), (0, 6), (0, 5), (5, 6), (4, 7), (0, 7), (0, 6),
    (6, 7), (4, 7), (0, 7), (0, 4), (0, 6), (5, 7), (4, 6),
    (0, 5), (4, 5), (5, 7), (0, 7), (0, 4), (0, 7), (6, 7),
    (0, 4), (0, 7), (4, 7), (4, 5), (0, 4), (0, 5), (0, 5),
    (5, 6), (0, 7), (5, 7), (0, 6), (5, 6), (0, 5), (6, 7),
    (0, 7), (0, 6),
)


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    order = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        chunk = ord(character) - 63
        bits.extend((chunk >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def incidence_rows(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    rows = tuple(
        tuple(edge for edge, ends in enumerate(edges) if vertex in ends)
        for vertex in range(order)
    )
    assert all(len(row) == 3 for row in rows)
    return rows


def local_choices(
    incident_edges: tuple[int, ...], flow: tuple[int, ...]
) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Enumerate supported local triangles, indexed by incident-edge slot."""
    directions = tuple(flow[edge] for edge in incident_edges)
    assert directions[0] ^ directions[1] ^ directions[2] == 0
    assert len(set(directions)) == 3 and all(directions)
    answer = set()
    for triangle in itertools.combinations(sorted(S), 3):
        by_direction = {}
        for first, second in itertools.combinations(triangle, 2):
            by_direction[first ^ second] = (first, second)
        if set(by_direction) != set(directions):
            continue
        answer.add(tuple(by_direction[value] for value in directions))
    return tuple(sorted(answer))


def direct_supported_labeling(
    order: int,
    edges: tuple[tuple[int, int], ...],
    rows: tuple[tuple[int, ...], ...],
    flow: tuple[int, ...],
) -> tuple[tuple[int, int], ...] | None:
    choices = tuple(local_choices(rows[v], flow) for v in range(order))
    edge_pair: list[tuple[int, int] | None] = [None] * len(edges)
    assigned = [False] * order

    def recurse(remaining: int) -> bool:
        if remaining == 0:
            return True
        candidates = [v for v in range(order) if not assigned[v]]
        vertex = max(
            candidates,
            key=lambda v: sum(edge_pair[e] is not None for e in rows[v]),
        )
        assigned[vertex] = True
        for option in choices[vertex]:
            if any(
                edge_pair[edge] is not None and edge_pair[edge] != option[slot]
                for slot, edge in enumerate(rows[vertex])
            ):
                continue
            new_edges = []
            for slot, edge in enumerate(rows[vertex]):
                if edge_pair[edge] is None:
                    edge_pair[edge] = option[slot]
                    new_edges.append(edge)
            if recurse(remaining - 1):
                return True
            for edge in new_edges:
                edge_pair[edge] = None
        assigned[vertex] = False
        return False

    if not recurse(order):
        return None
    answer = tuple(pair for pair in edge_pair if pair is not None)
    assert len(answer) == len(edges)
    return answer


def port_bit(direction: int, pair: tuple[int, int]) -> int:
    assert direction in U0 and direction
    base = tuple(sorted((Z, Z ^ direction)))
    assert pair == base or set(pair).isdisjoint(base)
    return int(pair == base)


def component_criterion(
    order: int,
    edges: tuple[tuple[int, int], ...],
    rows: tuple[tuple[int, ...], ...],
    flow: tuple[int, ...],
) -> tuple[bool, tuple[dict[str, object], ...]]:
    e0 = {edge for edge, value in enumerate(flow) if value in U0}
    e0_rows = tuple(tuple(edge for edge in rows[v] if edge in e0)
                    for v in range(order))
    assert all(len(row) in (1, 3) for row in e0_rows)

    leaf_bit = {}
    for vertex in range(order):
        if len(e0_rows[vertex]) != 1:
            continue
        choices = local_choices(rows[vertex], flow)
        assert len(choices) == 1
        edge = e0_rows[vertex][0]
        slot = rows[vertex].index(edge)
        leaf_bit[vertex] = port_bit(flow[edge], choices[0][slot])

    adjacency = [[] for _ in range(order)]
    for edge in e0:
        left, right = edges[edge]
        adjacency[left].append(right)
        adjacency[right].append(left)
    unseen = set(range(order))
    reports = []
    passed = True
    while unseen:
        root = next(iter(unseen))
        queue = [root]
        unseen.remove(root)
        vertices = []
        while queue:
            vertex = queue.pop()
            vertices.append(vertex)
            for other in adjacency[vertex]:
                if other in unseen:
                    unseen.remove(other)
                    queue.append(other)
        leaves = [v for v in vertices if len(e0_rows[v]) == 1]
        special = [v for v in vertices if len(e0_rows[v]) == 3]
        leaf_xor = 0
        for vertex in leaves:
            leaf_xor ^= leaf_bit[vertex]
        edge_count = sum(len(e0_rows[v]) for v in vertices) // 2
        reports.append(
            {
                "vertices": len(vertices),
                "edges": edge_count,
                "leaves": len(leaves),
                "special": len(special),
                "cycle_rank": edge_count - len(vertices) + 1,
                "leaf_xor": leaf_xor,
            }
        )
        passed &= leaf_xor == 0
    return passed, tuple(reports)


def spanning_tree_and_cotree(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[set[int], tuple[int, ...]]:
    parent = list(range(order))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    tree = set()
    for edge, (left, right) in enumerate(edges):
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            continue
        parent[left_root] = right_root
        tree.add(edge)
    assert len(tree) == order - 1
    cotree = tuple(edge for edge in range(len(edges)) if edge not in tree)
    return tree, cotree


def nowhere_zero_flows(
    order: int,
    edges: tuple[tuple[int, int], ...],
    rows: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    tree, cotree = spanning_tree_and_cotree(order, edges)
    tree_neighbours: list[list[tuple[int, int]]] = [
        [] for _ in range(order)
    ]
    for edge in tree:
        left, right = edges[edge]
        tree_neighbours[left].append((right, edge))
        tree_neighbours[right].append((left, edge))
    answer = []
    for values in itertools.product(range(1, 8), repeat=len(cotree)):
        flow = [0] * len(edges)
        demand = [0] * order
        for edge, value in zip(cotree, values):
            flow[edge] = value
            left, right = edges[edge]
            demand[left] ^= value
            demand[right] ^= value
        degree = [len(row) for row in tree_neighbours]
        removed = [False] * order
        queue = deque(v for v in range(order) if degree[v] == 1)
        while queue:
            leaf = queue.popleft()
            if removed[leaf] or degree[leaf] != 1:
                continue
            removed[leaf] = True
            for other, edge in tree_neighbours[leaf]:
                if removed[other]:
                    continue
                flow[edge] = demand[leaf]
                demand[other] ^= demand[leaf]
                degree[other] -= 1
                if degree[other] == 1:
                    queue.append(other)
                break
        root = next(vertex for vertex in range(order) if not removed[vertex])
        assert demand[root] == 0
        if all(flow):
            literal = tuple(flow)
            assert all(
                literal[row[0]] ^ literal[row[1]] ^ literal[row[2]] == 0
                for row in rows
            )
            answer.append(literal)
    return tuple(answer)


def check_local_theorem() -> dict[str, int]:
    planes = []
    for first, second in itertools.combinations(range(1, 8), 2):
        plane = frozenset((0, first, second, first ^ second))
        if len(plane) == 4 and plane not in planes:
            planes.append(plane)
    assert len(planes) == 7 and U0 in planes
    special_cases = nonspecial_cases = 0
    for plane in planes:
        directions = tuple(sorted(plane - {0}))
        fake_flow = directions
        choices = local_choices((0, 1, 2), fake_flow)
        if plane == U0:
            assert len(choices) == 4
            for option in choices:
                bits = [
                    port_bit(direction, pair)
                    for direction, pair in zip(directions, option)
                ]
                assert bits[0] ^ bits[1] ^ bits[2] == 0
            special_cases += 1
        else:
            assert len(choices) == 1
            in_u0 = [i for i, value in enumerate(directions) if value in U0]
            assert len(in_u0) == 1
            for slot, value in enumerate(directions):
                pair = choices[0][slot]
                if value not in U0:
                    assert pair == tuple(sorted((0, value)))
            nonspecial_cases += 1
    return {"special_planes": special_cases, "nonspecial_planes": nonspecial_cases}


def plane_normalizations() -> dict[frozenset[int], tuple[int, ...]]:
    planes = []
    for first, second in itertools.combinations(range(1, 8), 2):
        plane = frozenset((0, first, second, first ^ second))
        if len(plane) == 4 and plane not in planes:
            planes.append(plane)
    tables = []
    for first, second, third in itertools.permutations(range(1, 8), 3):
        table = tuple(
            (first if value & 1 else 0)
            ^ (second if value & 2 else 0)
            ^ (third if value & 4 else 0)
            for value in range(8)
        )
        if len(set(table)) == 8 and table not in tables:
            tables.append(table)
    assert len(planes) == 7 and len(tables) == 168
    return {
        plane: next(
            table
            for table in tables
            if frozenset(table[value] for value in plane) == U0
        )
        for plane in planes
    }


def check_small_flows() -> dict[str, object]:
    rows_out = []
    total_flows = total_supported = 0
    component_profiles = Counter()
    plane_histogram = Counter()
    digest = 1469598103934665603
    normalizations = plane_normalizations()
    for graph6 in GRAPH6_THROUGH_8:
        order, edges = parse_graph6(graph6)
        rows = incidence_rows(order, edges)
        flows = nowhere_zero_flows(order, edges, rows)
        supported = 0
        for flow in flows:
            direct = direct_supported_labeling(order, edges, rows, flow)
            criterion, reports = component_criterion(
                order, edges, rows, flow
            )
            assert (direct is not None) == criterion
            supported_planes = 0
            for table in normalizations.values():
                transformed = tuple(table[value] for value in flow)
                supported_planes += component_criterion(
                    order, edges, rows, transformed
                )[0]
            plane_histogram[supported_planes] += 1
            supported += criterion
            for report in reports:
                component_profiles[
                    (
                        report["vertices"],
                        report["leaves"],
                        report["special"],
                        report["cycle_rank"],
                        report["leaf_xor"],
                    )
                ] += 1
            for value in flow:
                digest ^= value
                digest = (digest * 1099511628211) & ((1 << 64) - 1)
            digest ^= int(criterion)
            digest = (digest * 1099511628211) & ((1 << 64) - 1)
        rows_out.append(
            {
                "graph6": graph6,
                "vertices": order,
                "flows": len(flows),
                "supported": supported,
            }
        )
        total_flows += len(flows)
        total_supported += supported
    return {
        "graphs": rows_out,
        "total_flows": total_flows,
        "total_supported": total_supported,
        "supported_plane_count_histogram": dict(
            sorted(plane_histogram.items())
        ),
        "component_profiles": len(component_profiles),
        "digest_fnv1a64": f"{digest:016x}",
    }


def check_34v_witness() -> dict[str, object]:
    order, edges = parse_graph6(GRAPH34)
    rows = incidence_rows(order, edges)
    assert len(edges) == len(FLOW34) == len(LABELS34_TRANSLATED)
    for edge, pair in enumerate(LABELS34_TRANSLATED):
        assert pair[0] in S and pair[1] in S
        assert pair[0] ^ pair[1] == FLOW34[edge]
    for vertex in range(order):
        for point in range(8):
            assert (
                sum(point in LABELS34_TRANSLATED[edge]
                    for edge in rows[vertex])
                % 2
                == 0
            )
    criterion, reports = component_criterion(order, edges, rows, FLOW34)
    direct = direct_supported_labeling(order, edges, rows, FLOW34)
    assert criterion and direct is not None
    plane_reports = []
    for plane, table in plane_normalizations().items():
        transformed = tuple(table[value] for value in FLOW34)
        passed, transformed_reports = component_criterion(
            order, edges, rows, transformed
        )
        plane_reports.append(
            {
                "plane": sorted(plane),
                "criterion": passed,
                "components": len(transformed_reports),
                "failed_components": sum(
                    report["leaf_xor"] for report in transformed_reports
                ),
            }
        )
    return {
        "vertices": order,
        "edges": len(edges),
        "e0_components": reports,
        "plane_reports": sorted(plane_reports, key=lambda row: row["plane"]),
        "criterion": criterion,
    }


def main() -> None:
    report = {
        "status": "PASS",
        "local": check_local_theorem(),
        "small_flows": check_small_flows(),
        "witness_34v": check_34v_witness(),
    }
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
