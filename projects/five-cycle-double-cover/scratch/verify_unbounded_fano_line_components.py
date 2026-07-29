#!/usr/bin/env python3
"""Deterministic audit for the unbounded Fano-line-component construction.

Starting from Petersen, recursively choose a spanning tree which contains
all but one edge of a displayed binary circuit, replace every cotree edge
by a diamond K4-e, and lift both a standard FiveCDC and a nowhere-zero
F_2^3 flow.  At depth d the displayed flow has exactly d+1 components in
the fixed line {1,2,3}.

The universal lower bound for every flow is the human induction in the
accompanying note.  This checker audits the construction and sharpness
witnesses; it does not enumerate all flows on the large graphs.
"""

from __future__ import annotations

from collections import deque


LINE = frozenset((1, 2, 3))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


class DisjointSet:
    def __init__(self, order: int) -> None:
        self.parent = list(range(order))
        self.rank = [0] * order

    def find(self, vertex: int) -> int:
        while self.parent[vertex] != vertex:
            self.parent[vertex] = self.parent[self.parent[vertex]]
            vertex = self.parent[vertex]
        return vertex

    def unite(self, first: int, second: int) -> bool:
        first = self.find(first)
        second = self.find(second)
        if first == second:
            return False
        if self.rank[first] < self.rank[second]:
            first, second = second, first
        self.parent[second] = first
        if self.rank[first] == self.rank[second]:
            self.rank[first] += 1
        return True


def incidence(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    rows = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        rows[first].append(edge)
        rows[second].append(edge)
    return tuple(tuple(row) for row in rows)


def component_sizes(
    order: int,
    edges: tuple[tuple[int, int], ...],
    selected: set[int],
) -> tuple[int, ...]:
    adjacency = [[] for _ in range(order)]
    for edge in selected:
        first, second = edges[edge]
        adjacency[first].append(second)
        adjacency[second].append(first)
    unseen = set(range(order))
    sizes = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        queue = [root]
        size = 0
        while queue:
            vertex = queue.pop()
            size += 1
            for other in adjacency[vertex]:
                if other in unseen:
                    unseen.remove(other)
                    queue.append(other)
        sizes.append(size)
    return tuple(sorted(sizes))


def check_graph(
    order: int, edges: tuple[tuple[int, int], ...]
) -> None:
    require(
        all(0 <= first < second < order for first, second in edges),
        "edge endpoint convention failure",
    )
    require(len(set(edges)) == len(edges), "graph is not simple")
    rows = incidence(order, edges)
    require(all(len(row) == 3 for row in rows), "graph is not cubic")
    require(
        len(component_sizes(order, edges, set(range(len(edges))))) == 1,
        "graph is disconnected",
    )
    for omitted in range(len(edges)):
        require(
            len(
                component_sizes(
                    order,
                    edges,
                    set(range(len(edges))) - {omitted},
                )
            )
            == 1,
            "graph has a bridge",
        )


def check_flow(
    order: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
) -> None:
    require(len(flow) == len(edges), "flow has wrong length")
    require(all(1 <= value <= 7 for value in flow), "flow has a zero value")
    for row in incidence(order, edges):
        total = 0
        for edge in row:
            total ^= flow[edge]
        require(total == 0, "flow conservation failure")


def check_cover(
    order: int,
    edges: tuple[tuple[int, int], ...],
    labels: tuple[int, ...],
) -> None:
    require(len(labels) == len(edges), "cover has wrong length")
    require(all(label.bit_count() == 2 for label in labels), "bad duad")
    for row in incidence(order, edges):
        total = 0
        for edge in row:
            total ^= labels[edge]
        require(total == 0, "cover parity failure")


def check_cycle(
    order: int,
    edges: tuple[tuple[int, int], ...],
    selected: set[int],
) -> None:
    degrees = [0] * order
    for edge in selected:
        first, second = edges[edge]
        degrees[first] += 1
        degrees[second] += 1
    require(all(degree in (0, 2) for degree in degrees), "not 2-regular")
    active = {vertex for vertex, degree in enumerate(degrees) if degree}
    require(active, "cycle is empty")
    components = component_sizes(order, edges, selected)
    nontrivial = [size for size in components if size > 1]
    require(len(nontrivial) == 1, "cycle is not connected")
    require(nontrivial[0] == len(active), "cycle component mismatch")


def adapted_tree(
    order: int,
    edges: tuple[tuple[int, int], ...],
    cycle: set[int],
) -> set[int]:
    """Extend a cycle-minus-one-edge path to a spanning tree."""
    omitted = min(cycle)
    tree = set(cycle) - {omitted}
    disjoint = DisjointSet(order)
    for edge in sorted(tree):
        first, second = edges[edge]
        require(disjoint.unite(first, second), "cycle-minus-edge is not a forest")
    for edge, (first, second) in enumerate(edges):
        if edge in tree:
            continue
        if disjoint.unite(first, second):
            tree.add(edge)
        if len(tree) == order - 1:
            break
    require(len(tree) == order - 1, "failed to build spanning tree")
    require(len(cycle - tree) == 1, "tree does not omit exactly one cycle edge")
    return tree


def base_instance() -> tuple[
    int,
    tuple[tuple[int, int], ...],
    tuple[int, ...],
    tuple[int, ...],
]:
    edges = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (0, 4),
        (0, 5),
        (1, 6),
        (2, 7),
        (3, 8),
        (4, 9),
        (5, 7),
        (7, 9),
        (6, 9),
        (6, 8),
        (5, 8),
    )
    edges = tuple(tuple(sorted(edge)) for edge in edges)

    coordinate_sets = (
        (0, 1, 2, 5, 8, 14),
        (2, 3, 4, 5, 7, 10),
        (0, 4, 6, 9, 12),
        (1, 3, 6, 7, 8, 9, 11, 13),
        (10, 11, 12, 13, 14),
    )
    labels = [0] * len(edges)
    for coordinate, chosen in enumerate(coordinate_sets):
        for edge in chosen:
            labels[edge] |= 1 << coordinate

    flow = (5, 1, 3, 1, 2, 7, 4, 2, 2, 3, 3, 1, 2, 6, 4)
    return 10, edges, tuple(flow), tuple(labels)


def lift_duad(label: int) -> tuple[int, ...]:
    points = [point for point in range(5) if (label >> point) & 1]
    require(len(points) == 2, "lift received a non-duad")
    first, second = points
    third = min(point for point in range(5) if not (label >> point) & 1)
    left = (1 << first) | (1 << third)
    right = (1 << second) | (1 << third)
    return (label, left, right, right, left, label, label)


def lift_flow(value: int) -> tuple[int, ...]:
    if value in LINE:
        choices = [other for other in sorted(LINE) if other != value]
    else:
        choices = [
            other
            for other in (4, 5, 6, 7)
            if other != value
        ][:2]
    first, second = choices
    answer = (
        value,
        first,
        value ^ first,
        second,
        value ^ second,
        first ^ second,
        value,
    )
    require(all(answer), "diamond lift created a zero flow value")
    return answer


def expand(
    order: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
    labels: tuple[int, ...],
    tree: set[int],
) -> tuple[
    int,
    tuple[tuple[int, int], ...],
    tuple[int, ...],
    tuple[int, ...],
]:
    records = []
    next_vertex = order
    for edge, (u, v) in enumerate(edges):
        if edge in tree:
            records.append(((u, v), flow[edge], labels[edge]))
            continue
        a, b, c, d = range(next_vertex, next_vertex + 4)
        next_vertex += 4
        inserted_edges = (
            (u, a),
            (a, c),
            (a, d),
            (b, c),
            (b, d),
            (c, d),
            (b, v),
        )
        for pair, value, label in zip(
            inserted_edges,
            lift_flow(flow[edge]),
            lift_duad(labels[edge]),
        ):
            records.append((tuple(sorted(pair)), value, label))
    records.sort(key=lambda row: row[0])
    return (
        next_vertex,
        tuple(row[0] for row in records),
        tuple(row[1] for row in records),
        tuple(row[2] for row in records),
    )


def check_petersen_non_tait(
    order: int, edges: tuple[tuple[int, int], ...]
) -> None:
    require(order == 10 and len(edges) == 15, "wrong Petersen size")
    perfect_matchings = []
    for mask in range(1 << len(edges)):
        if mask.bit_count() != 5:
            continue
        degrees = [0] * order
        for edge, (first, second) in enumerate(edges):
            if (mask >> edge) & 1:
                degrees[first] += 1
                degrees[second] += 1
        if degrees == [1] * order:
            perfect_matchings.append(mask)
    require(len(perfect_matchings) == 6, "wrong perfect-matching count")
    for matching in perfect_matchings:
        complement = {
            edge
            for edge in range(len(edges))
            if not (matching >> edge) & 1
        }
        require(
            component_sizes(order, edges, complement) == (5, 5),
            "Petersen has an even complementary 2-factor",
        )


def main() -> None:
    order, edges, flow, labels = base_instance()
    check_petersen_non_tait(order, edges)

    expected_orders = (10, 34, 106, 322)
    for depth, expected_order in enumerate(expected_orders):
        check_graph(order, edges)
        check_flow(order, edges, flow)
        check_cover(order, edges, labels)
        require(order == expected_order, "order recurrence failure")
        require(len(edges) == 3 * order // 2, "cubic size identity failure")

        outside = {
            edge for edge, value in enumerate(flow) if value not in LINE
        }
        check_cycle(order, edges, outside)
        line_edges = set(range(len(edges))) - outside
        line_sizes = component_sizes(order, edges, line_edges)
        require(len(line_sizes) == depth + 1, "line-component count failure")
        require(
            all(size % 2 == 0 for size in line_sizes),
            "line component has odd order",
        )

        print(
            f"depth={depth} order={order} edges={len(edges)} "
            f"outside_cycle={len(outside)} line_components={line_sizes}"
        )

        if depth + 1 == len(expected_orders):
            break
        tree = adapted_tree(order, edges, outside)
        cotree = set(range(len(edges))) - tree
        require(
            len(cotree) == order // 2 + 1,
            "wrong cubic cotree size",
        )
        require(
            len(outside & cotree) == 1,
            "outside cycle does not meet cotree once",
        )
        order, edges, flow, labels = expand(
            order, edges, flow, labels, tree
        )

    print("unbounded Fano-line-component construction: PASS")


if __name__ == "__main__":
    main()
