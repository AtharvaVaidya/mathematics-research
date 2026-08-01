#!/usr/bin/env python3
"""Independent semantic checker for the 34-vertex non-thin good witness."""

from __future__ import annotations


GRAPH6 = (
    "as???SK????A?A?C_@_?B?@_??G??_I?GA_AA????_??@?????B??@_?"
    "o??????_C??CGO??B@????a????__??C@O??A?_"
)

TREES = (
    (0, 3, 4, 5, 8, 10, 13, 14, 15, 16, 17, 19, 20, 22, 24, 25, 26,
     27, 28, 30, 31, 32, 35, 37, 39, 41, 43, 44, 45, 46, 47, 49, 50),
    (2, 4, 5, 6, 7, 9, 10, 11, 12, 14, 16, 18, 20, 21, 23, 24, 28, 29,
     31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 43, 47, 48, 49),
    (1, 3, 6, 7, 8, 9, 11, 12, 13, 15, 17, 18, 19, 21, 22, 23, 25, 26,
     27, 29, 30, 33, 34, 36, 37, 38, 40, 42, 44, 45, 46, 48, 50),
)

EXPECTED_FLOW = (
    6, 3, 5, 2, 4, 4, 3, 3, 3, 1, 6, 1, 5, 7, 4, 6, 5,
    3, 3, 7, 6, 1, 3, 7, 4, 6, 2, 2, 5, 1, 2, 7, 4, 7,
    1, 4, 7, 3, 1, 4, 5, 5, 3, 7, 2, 6, 3, 5, 1, 7, 6,
)

LABELS = (
    (3, 5), (5, 6), (3, 6), (5, 7), (3, 7), (3, 7), (4, 7),
    (5, 6), (5, 6), (4, 5), (3, 5), (6, 7), (3, 6), (3, 4),
    (3, 7), (3, 5), (3, 6), (5, 6), (4, 7), (3, 4), (3, 5),
    (4, 5), (4, 7), (3, 4), (3, 7), (3, 5), (4, 6), (5, 7),
    (3, 6), (6, 7), (4, 6), (3, 4), (3, 7), (3, 4), (4, 5),
    (3, 7), (3, 4), (4, 7), (6, 7), (3, 7), (3, 6), (3, 6),
    (5, 6), (3, 4), (4, 6), (3, 5), (5, 6), (3, 6), (4, 5),
    (3, 4), (3, 5),
)

COLOURS = (0, 1, 0, 4, 0, 1, 3, 2)


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


def check_tree(
    order: int, edges: tuple[tuple[int, int], ...], chosen: set[int]
) -> None:
    assert len(chosen) == order - 1
    parent = list(range(order))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in chosen:
        left, right = edges[edge]
        left, right = find(left), find(right)
        assert left != right
        parent[left] = right
    root = find(0)
    assert all(find(vertex) == root for vertex in range(order))


def completion(
    order: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    chosen: set[int],
) -> set[int]:
    answer = set(range(len(edges))) - chosen
    demand = [0] * order
    neighbours: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        if edge in chosen:
            neighbours[left].append((right, edge))
            neighbours[right].append((left, edge))
        else:
            demand[left] ^= 1
            demand[right] ^= 1
    degree = list(map(len, neighbours))
    removed = [False] * order
    stack = [vertex for vertex in range(order) if degree[vertex] == 1]
    while stack:
        leaf = stack.pop()
        if removed[leaf] or degree[leaf] != 1:
            continue
        removed[leaf] = True
        for other, edge in neighbours[leaf]:
            if removed[other]:
                continue
            if demand[leaf]:
                answer.add(edge)
                demand[other] ^= 1
            degree[other] -= 1
            if degree[other] == 1:
                stack.append(other)
            break
    root = next(vertex for vertex in range(order) if not removed[vertex])
    assert demand[root] == 0
    assert all(
        sum(edge in answer for edge in incidence[vertex]) % 2 == 0
        for vertex in range(order)
    )
    return answer


def main() -> None:
    order, edges = parse_graph6(GRAPH6)
    assert order == 34 and len(edges) == 51
    incidence = tuple(
        tuple(edge for edge, ends in enumerate(edges) if vertex in ends)
        for vertex in range(order)
    )
    assert all(len(row) == 3 for row in incidence)
    assert incidence[0] == (0, 1, 2)

    trees = tuple(set(row) for row in TREES)
    for tree in trees:
        check_tree(order, edges, tree)
    multiplicities = tuple(
        sum(edge in tree for tree in trees) for edge in range(len(edges))
    )
    assert multiplicities[:3] == (1, 1, 1)
    assert all(value == 2 for value in multiplicities[3:])

    completions = tuple(
        completion(order, edges, incidence, tree) for tree in trees
    )
    flow = tuple(
        sum((edge in completions[coordinate]) << coordinate
            for coordinate in range(3))
        for edge in range(len(edges))
    )
    assert flow == EXPECTED_FLOW
    assert min(flow.count(value) for value in range(1, 8)) == 5

    assert len(LABELS) == len(edges)
    assert all(left ^ right == flow[edge]
               for edge, (left, right) in enumerate(LABELS))
    for vertex in range(order):
        for point in range(8):
            degree = sum(
                point in LABELS[edge] for edge in incidence[vertex]
            )
            assert degree % 2 == 0
    assert all(COLOURS[left] != COLOURS[right] for left, right in LABELS)

    used_points = sorted({point for pair in LABELS for point in pair})
    used_pairs = set(LABELS)
    active_pairs = {
        (left, right)
        for left in used_points
        for right in used_points
        if left < right
    }
    assert used_points == [3, 4, 5, 6, 7]
    assert not active_pairs - used_pairs
    print(
        "PASS order=34 edges=51 star=(0,1,2) "
        "min_flow_count=5 cooccurrence=K5 support=5"
    )


if __name__ == "__main__":
    main()
