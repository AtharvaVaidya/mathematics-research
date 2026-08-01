#!/usr/bin/env python3
"""Independent replay of the reported lift-13 Jaeger augmented trap."""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROW_PATH = HERE / "trap-directed-first-row.json"
GRAPH_PATH = (
    HERE / "../../artifacts/structured/graphs/"
    "lift13_petersen_girth10.json"
).resolve()


def graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    values = [ord(character) - 63 for character in record]
    if values[0] < 63:
        order, start = values[0], 1
    else:
        assert values[0] == 63 and values[1] < 63
        order = (values[1] << 12) | (values[2] << 6) | values[3]
        start = 4
    bits = [
        (value >> shift) & 1
        for value in values[start:]
        for shift in range(5, -1, -1)
    ]
    required = order * (order - 1) // 2
    assert len(bits) >= required and not any(bits[required:])
    edges = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


class DSU:
    def __init__(self, order: int) -> None:
        self.parent = list(range(order))

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, first: int, second: int) -> None:
        first, second = self.find(first), self.find(second)
        if first != second:
            self.parent[first] = second


def connected(
    order: int,
    edges: tuple[tuple[int, int], ...],
    deleted: frozenset[int] = frozenset(),
) -> bool:
    adjacency = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        if edge not in deleted:
            adjacency[left].append(right)
            adjacency[right].append(left)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other in adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                stack.append(other)
    return len(seen) == order


def graph_girth(
    order: int, edges: tuple[tuple[int, int], ...]
) -> int:
    adjacency = [[] for _ in range(order)]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    answer = order + 1
    for source in range(order):
        distance = [-1] * order
        parent = [-1] * order
        distance[source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for other in adjacency[vertex]:
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    answer = min(
                        answer,
                        distance[vertex] + distance[other] + 1,
                    )
    return answer


def is_tree(
    order: int,
    edges: tuple[tuple[int, int], ...],
    chosen: frozenset[int],
) -> bool:
    if len(chosen) != order - 1:
        return False
    dsu = DSU(order)
    for edge in chosen:
        left, right = edges[edge]
        if dsu.find(left) == dsu.find(right):
            return False
        dsu.union(left, right)
    return True


def build_trees(
    order: int,
    edges: tuple[tuple[int, int], ...],
    internal: tuple[int, ...],
    spokes: tuple[int, int, int],
    labels: tuple[int, ...],
) -> tuple[frozenset[int], frozenset[int], frozenset[int]]:
    assert len(labels) == len(internal)
    assert Counter(labels) == {0: 64, 1: 64, 2: 64}
    trees = []
    for coordinate in range(3):
        tree = frozenset(
            [spokes[coordinate]]
            + [
                internal[local]
                for local, label in enumerate(labels)
                if label != coordinate
            ]
        )
        assert is_tree(order, edges, tree)
        trees.append(tree)
    return tuple(trees)  # type: ignore[return-value]


def odd_kernel(
    order: int,
    edges: tuple[tuple[int, int], ...],
    tree: frozenset[int],
) -> frozenset[int]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge in tree:
        left, right = edges[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    parent = [-1] * order
    parent_edge = [-1] * order
    parent[0] = 0
    traversal = [0]
    for vertex in traversal:
        for other, edge in adjacency[vertex]:
            if parent[other] < 0:
                parent[other] = vertex
                parent_edge[other] = edge
                traversal.append(other)
    assert len(traversal) == order
    size = [1] * order
    answer = set()
    for vertex in reversed(traversal[1:]):
        if size[vertex] & 1:
            answer.add(parent_edge[vertex])
        size[parent[vertex]] += size[vertex]
    degree = [0] * order
    for edge in answer:
        left, right = edges[edge]
        degree[left] += 1
        degree[right] += 1
    assert all(value & 1 for value in degree)
    return frozenset(answer)


def scalar(first: int, second: int) -> int:
    return (first & second).bit_count() & 1


def span_contains(target: int, columns: list[int]) -> bool:
    pivots: dict[int, int] = {}
    for column in columns:
        while column:
            pivot = column.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = column
                break
            column ^= pivots[pivot]
    while target:
        pivot = target.bit_length() - 1
        if pivot not in pivots:
            return False
        target ^= pivots[pivot]
    return True


def evaluate(
    order: int,
    edges: tuple[tuple[int, int], ...],
    trees: tuple[frozenset[int], frozenset[int], frozenset[int]],
) -> tuple[
    tuple[frozenset[int], frozenset[int], frozenset[int]],
    tuple[int, ...],
    int,
]:
    kernels = tuple(odd_kernel(order, edges, tree) for tree in trees)
    incidence = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    flow = tuple(
        sum(
            1 << coordinate
            for coordinate in range(3)
            if edge not in kernels[coordinate]
        )
        for edge in range(len(edges))
    )
    assert all(flow)
    assert all(
        flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0
        for row in incidence
    )
    normals = []
    for row in incidence:
        choices = [
            functional
            for functional in range(1, 8)
            if all(not scalar(functional, flow[edge]) for edge in row)
        ]
        assert len(choices) == 1
        normals.append(choices[0])

    profile = []
    flags = 0
    for functional in range(1, 8):
        zero = DSU(order)
        zero_degree = [0] * order
        for edge, (left, right) in enumerate(edges):
            if scalar(functional, flow[edge]):
                continue
            zero.union(left, right)
            zero_degree[left] += 1
            zero_degree[right] += 1
        assert all(value in (1, 3) for value in zero_degree)
        roots = sorted({zero.find(vertex) for vertex in range(order)})
        root_index = {root: index for index, root in enumerate(roots)}
        transverse = functional & -functional
        beta = 0
        for vertex in range(order):
            if (
                zero_degree[vertex] == 1
                and scalar(normals[vertex] ^ functional, transverse)
            ):
                beta ^= 1 << root_index[zero.find(vertex)]
        profile.append(beta.bit_count())

        outside = DSU(order)
        for edge, (left, right) in enumerate(edges):
            if scalar(functional, flow[edge]):
                outside.union(left, right)
        inside_value = [0] * order
        for vertex in range(order):
            if zero_degree[vertex] == 1:
                values = [
                    flow[edge]
                    for edge in incidence[vertex]
                    if not scalar(functional, flow[edge])
                ]
                assert len(values) == 1
                inside_value[vertex] = values[0]
        for direction in range(1, 8):
            if scalar(functional, direction):
                continue
            columns: dict[int, int] = {}
            for vertex in range(order):
                if (
                    zero_degree[vertex] != 1
                    or inside_value[vertex] == direction
                ):
                    continue
                root = outside.find(vertex)
                columns[root] = columns.get(root, 0) ^ (
                    1 << root_index[zero.find(vertex)]
                )
            flags += span_contains(
                beta, [value for value in columns.values() if value]
            )
    return kernels, tuple(profile), flags  # type: ignore[return-value]


def fundamental_cycle(
    order: int,
    edges: tuple[tuple[int, int], ...],
    tree: frozenset[int],
    inserted: int,
) -> frozenset[int]:
    source, target = edges[inserted]
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge in tree:
        left, right = edges[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    parent = [-1] * order
    parent_edge = [-1] * order
    parent[source] = source
    stack = [source]
    while stack and parent[target] < 0:
        vertex = stack.pop()
        for other, edge in adjacency[vertex]:
            if parent[other] < 0:
                parent[other] = vertex
                parent_edge[other] = edge
                stack.append(other)
    cycle = {inserted}
    vertex = target
    while vertex != source:
        cycle.add(parent_edge[vertex])
        vertex = parent[vertex]
    return frozenset(cycle)


def main() -> None:
    row = json.loads(ROW_PATH.read_text(encoding="utf-8").splitlines()[0])
    order, edges = graph6(row["graph6"])
    assert order == 130 and len(edges) == 195
    assert len(set(edges)) == len(edges)
    degree = Counter(vertex for edge in edges for vertex in edge)
    assert set(degree.values()) == {3} and len(degree) == order
    assert connected(order, edges)
    for first in range(-1, len(edges)):
        for second in range(first + 1, len(edges)):
            deleted = frozenset(
                edge for edge in (first, second) if edge >= 0
            )
            assert connected(order, edges, deleted)
    assert graph_girth(order, edges) == 10
    source = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    source_edges = {
        tuple(sorted((int(edge["u"]), int(edge["v"]))))
        for edge in source["edges"]
    }
    assert source["vertices"] == order and source_edges == set(edges)

    root = row["root"]
    spokes = tuple(
        edge for edge, endpoints in enumerate(edges) if root in endpoints
    )
    internal = tuple(
        edge for edge, endpoints in enumerate(edges)
        if root not in endpoints
    )
    labels = tuple(map(int, row["state_labels"]))
    assert len(spokes) == 3 and len(internal) == 192
    trees = build_trees(order, edges, internal, spokes, labels)
    kernels, profile, flags = evaluate(order, edges, trees)
    psi = (min(profile), sum(map(len, kernels)))
    assert profile == tuple(row["profile"])
    assert flags == row["parallel_successful_flags"] == 0
    assert psi == (row["d_min"], row["kernel_sum"]) == (2, 202)

    observed = []
    ordinary_lengths = []
    active_lengths = []
    candidates = 0
    for first_coordinate, second_coordinate in combinations(range(3), 2):
        for first in range(len(internal)):
            if labels[first] != first_coordinate:
                continue
            for second in range(len(internal)):
                if labels[second] != second_coordinate:
                    continue
                candidates += 1
                changed = list(labels)
                changed[first], changed[second] = (
                    changed[second],
                    changed[first],
                )
                try:
                    changed_trees = build_trees(
                        order,
                        edges,
                        internal,
                        spokes,
                        tuple(changed),
                    )
                except AssertionError:
                    continue
                changed_kernels, changed_profile, changed_flags = evaluate(
                    order, edges, changed_trees
                )
                changed_psi = (
                    min(changed_profile),
                    sum(map(len, changed_kernels)),
                )
                observed.append(
                    {
                        "local_positions": [first, second],
                        "coordinates": [
                            first_coordinate,
                            second_coordinate,
                        ],
                        "psi": list(changed_psi),
                        "parallel_successful_flags": changed_flags,
                    }
                )

                first_cycle = fundamental_cycle(
                    order, edges, trees[first_coordinate], internal[first]
                )
                second_cycle = fundamental_cycle(
                    order, edges, trees[second_coordinate], internal[second]
                )
                assert internal[second] in first_cycle
                assert internal[first] in second_cycle
                ordinary_lengths.extend(
                    (len(first_cycle), len(second_cycle))
                )
                if internal[second] in kernels[first_coordinate]:
                    active_lengths.append(len(first_cycle))
                if internal[first] in kernels[second_coordinate]:
                    active_lengths.append(len(second_cycle))

    assert candidates == 3 * 64 * 64
    assert observed == row["full_neighbourhood"]
    assert len(observed) == row["legal_neighbours"] == 436
    assert not any(tuple(item["psi"]) < psi for item in observed)
    assert not any(
        item["parallel_successful_flags"] > 0 for item in observed
    )
    equal_psi_neighbours = sum(
        tuple(item["psi"]) == psi for item in observed
    )
    assert equal_psi_neighbours == 107
    assert len(observed) - equal_psi_neighbours == 329
    assert min(ordinary_lengths) >= 10
    assert active_lengths and min(active_lengths) >= 10

    # Check one literal active 10-cycle, independently of the minimum
    # extracted from the complete active-length list.
    literal_first, literal_second = 49, 73
    assert (labels[literal_first], labels[literal_second]) == (0, 1)
    assert (internal[literal_first], internal[literal_second]) == (51, 76)
    literal_cycle = fundamental_cycle(
        order, edges, trees[0], internal[literal_first]
    )
    assert internal[literal_second] in kernels[0]
    assert literal_cycle == frozenset(
        (7, 15, 26, 45, 46, 51, 52, 76, 138, 139)
    )

    # The complete layer-one audit proves that no augmented escape has
    # distance one.  Verify a literal two-exchange lower-Psi escape.
    escape_labels = list(labels)
    first_escape = (113, 136)
    second_escape = (109, 169)
    assert tuple(escape_labels[index] for index in first_escape) == (0, 1)
    assert tuple(internal[index] for index in first_escape) == (116, 139)
    escape_labels[first_escape[0]], escape_labels[first_escape[1]] = (
        escape_labels[first_escape[1]],
        escape_labels[first_escape[0]],
    )
    parent_trees = build_trees(
        order, edges, internal, spokes, tuple(escape_labels)
    )
    parent_kernels, parent_profile, parent_flags = evaluate(
        order, edges, parent_trees
    )
    parent_psi = (
        min(parent_profile),
        sum(map(len, parent_kernels)),
    )
    assert parent_profile == profile
    assert parent_flags == 0 and parent_psi == (2, 202)

    assert tuple(escape_labels[index] for index in second_escape) == (0, 1)
    assert tuple(internal[index] for index in second_escape) == (112, 172)
    escape_labels[second_escape[0]], escape_labels[second_escape[1]] = (
        escape_labels[second_escape[1]],
        escape_labels[second_escape[0]],
    )
    endpoint_trees = build_trees(
        order, edges, internal, spokes, tuple(escape_labels)
    )
    endpoint_kernels, endpoint_profile, endpoint_flags = evaluate(
        order, edges, endpoint_trees
    )
    endpoint_psi = (
        min(endpoint_profile),
        sum(map(len, endpoint_kernels)),
    )
    assert tuple(map(len, endpoint_kernels)) == (67, 67, 67)
    assert endpoint_profile == (14, 24, 8, 22, 6, 16, 2)
    assert endpoint_flags == 0 and endpoint_psi == (2, 201)

    print(
        json.dumps(
            {
                "status": "PASS",
                "order": order,
                "edges": len(edges),
                "simple_cubic": True,
                "three_edge_connected": True,
                "girth": graph_girth(order, edges),
                "root": root,
                "spokes": spokes,
                "internal_edges": len(internal),
                "omitted_class_sizes": tuple(Counter(labels)[i]
                                             for i in range(3)),
                "kernel_sizes": tuple(map(len, kernels)),
                "profile": profile,
                "psi": psi,
                "parallel_successful_flags": flags,
                "candidate_exchanges": candidates,
                "legal_exchanges": len(observed),
                "lower_neighbours": 0,
                "parallel_success_neighbours": 0,
                "equal_psi_neighbours": equal_psi_neighbours,
                "higher_psi_neighbours":
                    len(observed) - equal_psi_neighbours,
                "minimum_exchange_cycle_length": min(ordinary_lengths),
                "minimum_active_exchange_cycle_length":
                    min(active_lengths),
                "active_sides": len(active_lengths),
                "active_cycle_length_histogram": {
                    str(key): value
                    for key, value in sorted(Counter(active_lengths).items())
                },
                "neighbour_psi_histogram": {
                    str(key): value
                    for key, value in sorted(Counter(
                        tuple(item["psi"]) for item in observed
                    ).items())
                },
                "literal_active_ten_cycle": {
                    "coordinates": (0, 1),
                    "local_positions":
                        (literal_first, literal_second),
                    "inserted_full_edge": internal[literal_first],
                    "removed_active_full_edge": internal[literal_second],
                    "cycle_edges": tuple(sorted(literal_cycle)),
                },
                "shortest_augmented_escape": {
                    "distance": 2,
                    "first_exchange_local_positions": first_escape,
                    "first_exchange_full_edges":
                        tuple(internal[index] for index in first_escape),
                    "second_exchange_local_positions": second_escape,
                    "second_exchange_full_edges":
                        tuple(internal[index] for index in second_escape),
                    "parent_kernel_sizes":
                        tuple(map(len, parent_kernels)),
                    "parent_profile": parent_profile,
                    "parent_psi": parent_psi,
                    "parent_flags": parent_flags,
                    "endpoint_kernel_sizes":
                        tuple(map(len, endpoint_kernels)),
                    "endpoint_profile": endpoint_profile,
                    "endpoint_psi": endpoint_psi,
                    "endpoint_flags": endpoint_flags,
                    "escape_is_lower": True,
                    "escape_is_parallel_success": False,
                },
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
