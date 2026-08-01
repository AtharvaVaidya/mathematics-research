#!/usr/bin/env python3
"""Exhaustively verify the Petersen odd-side-forest obstruction."""

from __future__ import annotations

from itertools import combinations


GRAPH6 = "ICOf@pSb?"
EXPECTED_PER_STAR = {
    "cotrees": 240,
    "packings": 4416,
    "some_coordinate_good": 384,
    "fixed_coordinate_good": 128,
    "some_pair_disjoint": 0,
    "minimum_pair_intersection": 1,
}


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    order = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    cursor = 0
    edges = []
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def is_tree_on_vertices(
    vertices: tuple[int, ...],
    edges: tuple[tuple[int, int], ...],
    chosen: tuple[int, ...],
) -> bool:
    if len(chosen) != len(vertices) - 1:
        return False
    parent = {vertex: vertex for vertex in vertices}

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in chosen:
        left, right = map(find, edges[edge])
        if left == right:
            return False
        parent[left] = right
    return len({find(vertex) for vertex in vertices}) == 1


def odd_side_forest(
    order: int,
    edges: tuple[tuple[int, int], ...],
    chosen: tuple[int, ...],
) -> int:
    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(order)
    ]
    for edge in chosen:
        left, right = edges[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    parent = [-1] * order
    parent_edge = [-1] * order
    traversal = [0]
    parent[0] = 0
    for vertex in traversal:
        for other, edge in adjacency[vertex]:
            if parent[other] >= 0:
                continue
            parent[other] = vertex
            parent_edge[other] = edge
            traversal.append(other)
    assert len(traversal) == order
    subtree_size = [1] * order
    answer = 0
    for vertex in reversed(traversal[1:]):
        if subtree_size[vertex] % 2:
            answer |= 1 << parent_edge[vertex]
        subtree_size[parent[vertex]] += subtree_size[vertex]
    for vertex in range(order):
        degree = sum(
            bool(answer & (1 << edge))
            for edge, endpoints in enumerate(edges)
            if vertex in endpoints
        )
        assert degree % 2 == 1
    return answer


def contracted_eulerian(
    order: int,
    edges: tuple[tuple[int, int], ...],
    contraction: int,
    selected: int,
) -> bool:
    parent = list(range(order))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge, (left, right) in enumerate(edges):
        if not contraction & (1 << edge):
            continue
        left, right = find(left), find(right)
        if left != right:
            parent[left] = right
    parity = [0] * order
    for edge, (left, right) in enumerate(edges):
        if not selected & (1 << edge):
            continue
        left, right = find(left), find(right)
        if left != right:
            parity[left] ^= 1
            parity[right] ^= 1
    return not any(parity)


def main() -> None:
    order, edges = parse_graph6(GRAPH6)
    assert order == 10 and len(edges) == 15
    reports = []
    for star in range(order):
        spokes = tuple(
            edge
            for edge, endpoints in enumerate(edges)
            if star in endpoints
        )
        assert len(spokes) == 3
        internal = tuple(
            edge for edge in range(len(edges)) if edge not in spokes
        )
        remaining_vertices = tuple(
            vertex for vertex in range(order) if vertex != star
        )
        cotrees = []
        for omitted in combinations(internal, 4):
            omitted_mask = sum(1 << edge for edge in omitted)
            selected = tuple(
                edge
                for edge in internal
                if not omitted_mask & (1 << edge)
            )
            if is_tree_on_vertices(remaining_vertices, edges, selected):
                cotrees.append(omitted_mask)
        cotree_set = set(cotrees)
        internal_mask = sum(1 << edge for edge in internal)
        packings = 0
        some_coordinate_good = 0
        fixed_coordinate_good = 0
        some_pair_disjoint = 0
        minimum_pair_intersection = len(edges)
        for first in cotrees:
            for second in cotrees:
                if first & second:
                    continue
                third = internal_mask ^ first ^ second
                if third not in cotree_set:
                    continue
                packings += 1
                omitted = (first, second, third)
                forests = []
                for coordinate in range(3):
                    chosen = tuple(
                        edge
                        for edge in internal
                        if not omitted[coordinate] & (1 << edge)
                    ) + (spokes[coordinate],)
                    assert is_tree_on_vertices(
                        tuple(range(order)), edges, chosen
                    )
                    forests.append(
                        odd_side_forest(order, edges, chosen)
                    )
                good = []
                intersections = []
                for coordinate in range(3):
                    other_first = (coordinate + 1) % 3
                    other_second = (coordinate + 2) % 3
                    intersection = (
                        forests[other_first] & forests[other_second]
                    )
                    intersections.append(intersection)
                    good.append(
                        contracted_eulerian(
                            order,
                            edges,
                            forests[coordinate],
                            intersection,
                        )
                    )
                some_coordinate_good += any(good)
                fixed_coordinate_good += good[2]
                some_pair_disjoint += any(
                    intersection == 0 for intersection in intersections
                )
                minimum_pair_intersection = min(
                    minimum_pair_intersection,
                    *(intersection.bit_count()
                      for intersection in intersections),
                )
        report = {
            "cotrees": len(cotrees),
            "packings": packings,
            "some_coordinate_good": some_coordinate_good,
            "fixed_coordinate_good": fixed_coordinate_good,
            "some_pair_disjoint": some_pair_disjoint,
            "minimum_pair_intersection": minimum_pair_intersection,
        }
        assert report == EXPECTED_PER_STAR
        reports.append(report)
    assert all(report == reports[0] for report in reports)
    print(
        "PASS: each of 10 Petersen stars has 4416 ordered packings; "
        "none has a disjoint K-pair; minimum intersection one; "
        "384 packings satisfy contracted parity in some coordinate."
    )


if __name__ == "__main__":
    main()
