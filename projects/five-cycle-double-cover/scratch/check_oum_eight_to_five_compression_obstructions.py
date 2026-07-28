#!/usr/bin/env python3
"""Exact checks for direct 8-CDC to 5-CDC compression obstructions.

Only the Python standard library is used.  The script checks:

1. a minimum-order Petersen supplied Oum cover with co-occurrence K6;
2. impossibility of an affine F_2^3 -> F_2^5 compression on its
   all-seven-valued flow;
3. omega(R_5)=5, excluding every binary coordinate-linear compression
   of the supplied K6 cover;
4. all compatible Oum potentials of the Petersen flow (one K6 and three
   K5 choices after translation gauge);
5. a 12-vertex fixed flow with one gauged compatible potential, whose
   co-occurrence graph is K6.

These are compression countermodels, not graph counterexamples to FiveCDC.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, product


PETERSEN_BLOCKS = (
    (0, 1, 2),
    (0, 1, 3),
    (0, 2, 4),
    (0, 3, 5),
    (0, 4, 5),
    (1, 2, 5),
    (1, 3, 4),
    (1, 4, 5),
    (2, 3, 4),
    (2, 3, 5),
)
PETERSEN_GRAPH6 = "IqMA?[aDG"

RIGID_EDGES = (
    (0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 9),
    (2, 6), (2, 10), (2, 11), (3, 7), (3, 10), (3, 11),
    (4, 8), (4, 9), (4, 10), (5, 8), (5, 9), (5, 11),
)
RIGID_FLOW = (
    1, 2, 3, 4, 7, 3, 5, 3, 6,
    5, 7, 2, 5, 1, 4, 6, 2, 4,
)
RIGID_GRAPH6 = "K??FEaKR@oE_"


def graph6_encode(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> str:
    assert vertices < 63
    edge_set = {tuple(sorted(edge)) for edge in edges}
    bits = [
        int((left, right) in edge_set)
        for right in range(1, vertices)
        for left in range(right)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    return chr(vertices + 63) + "".join(
        chr(
            63
            + sum(
                bits[offset + index] << (5 - index)
                for index in range(6)
            )
        )
        for offset in range(0, len(bits), 6)
    )


def incidence(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


def connected(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    removed_edge: int | None = None,
) -> bool:
    rows = incidence(vertices, edges)
    reached = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for edge in rows[vertex]:
            if edge == removed_edge:
                continue
            left, right = edges[edge]
            other = left ^ right ^ vertex
            if other not in reached:
                reached.add(other)
                queue.append(other)
    return len(reached) == vertices


def graph_girth(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> int:
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


def petersen_construction() -> tuple[
    tuple[tuple[int, int], ...],
    tuple[tuple[int, int], ...],
]:
    pair_occurrences = Counter(
        pair
        for block in PETERSEN_BLOCKS
        for pair in combinations(block, 2)
    )
    assert pair_occurrences == Counter({
        pair: 2 for pair in combinations(range(6), 2)
    })

    rows = []
    for left, right in combinations(range(len(PETERSEN_BLOCKS)), 2):
        common = tuple(sorted(
            set(PETERSEN_BLOCKS[left]) & set(PETERSEN_BLOCKS[right])
        ))
        if len(common) == 2:
            rows.append((left, right, common))
        else:
            assert len(common) <= 1
    edges = tuple((left, right) for left, right, _ in rows)
    labels = tuple(label for _, _, label in rows)
    return edges, labels


def flow_is_good(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
) -> bool:
    rows = incidence(vertices, edges)
    return (
        len(flow) == len(edges)
        and all(1 <= value <= 7 for value in flow)
        and all(
            flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0
            for row in rows
        )
    )


def compatible_potentials(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    """Enumerate every Oum potential with the translation gauge t_0=0."""
    rows = incidence(vertices, edges)
    offsets = []
    for edge, (left, right) in enumerate(edges):
        other_left = next(item for item in rows[left] if item != edge)
        other_right = next(item for item in rows[right] if item != edge)
        offsets.append(flow[other_left] ^ flow[other_right])

    reached = {0}
    queue = deque([0])
    tree = []
    while queue:
        vertex = queue.popleft()
        for edge in rows[vertex]:
            left, right = edges[edge]
            other = left ^ right ^ vertex
            if other in reached:
                continue
            reached.add(other)
            queue.append(other)
            tree.append((vertex, other, edge))
    assert len(tree) == vertices - 1

    answer = []
    for choices in product((0, 1), repeat=vertices - 1):
        potential: list[int | None] = [None] * vertices
        potential[0] = 0
        for choice, (parent, child, edge) in zip(choices, tree):
            assert potential[parent] is not None
            difference = offsets[edge]
            if choice:
                difference ^= flow[edge]
            potential[child] = potential[parent] ^ difference
        assert all(item is not None for item in potential)
        candidate = tuple(int(item) for item in potential)
        if all(
            (candidate[left] ^ candidate[right])
            in (offsets[edge], offsets[edge] ^ flow[edge])
            for edge, (left, right) in enumerate(edges)
        ):
            answer.append(candidate)
    return tuple(answer)


def oum_pair_labels(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
    potential: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    rows = incidence(vertices, edges)
    labels = []
    for edge, (left, right) in enumerate(edges):
        other_left = next(item for item in rows[left] if item != edge)
        base_left = potential[left] ^ flow[other_left]
        label_left = tuple(sorted(
            (base_left, base_left ^ flow[edge])
        ))

        other_right = next(item for item in rows[right] if item != edge)
        base_right = potential[right] ^ flow[other_right]
        label_right = tuple(sorted(
            (base_right, base_right ^ flow[edge])
        ))
        assert label_left == label_right
        labels.append(label_left)

    for vertex, row in enumerate(rows):
        local_labels = [labels[edge] for edge in row]
        coordinate_counts = Counter(
            coordinate
            for label in local_labels
            for coordinate in label
        )
        assert sorted(coordinate_counts.values()) == [2, 2, 2]
        assert len(coordinate_counts) == 3
    return tuple(labels)


def coordinate_graph(
    labels: tuple[tuple[int, int], ...]
) -> tuple[frozenset[int], ...]:
    rows = [set() for _ in range(8)]
    for left, right in labels:
        rows[left].add(right)
        rows[right].add(left)
    return tuple(frozenset(row) for row in rows)


def complete_support(
    graph: tuple[frozenset[int], ...], size: int
) -> tuple[int, ...] | None:
    for vertices in combinations(range(8), size):
        if all(
            right in graph[left]
            for left, right in combinations(vertices, 2)
        ):
            return vertices
    return None


def chromatic_number(graph: tuple[frozenset[int], ...]) -> int:
    order = sorted(range(8), key=lambda vertex: -len(graph[vertex]))
    for bound in range(1, 9):
        colours = [-1] * 8

        def search(index: int) -> bool:
            if index == len(order):
                return True
            vertex = order[index]
            forbidden = {
                colours[other]
                for other in graph[vertex]
                if colours[other] >= 0
            }
            for colour in range(bound):
                if colour in forbidden:
                    continue
                colours[vertex] = colour
                if search(index + 1):
                    return True
                colours[vertex] = -1
            return False

        if search(0):
            return bound
    raise AssertionError("coordinate graph is not 8-colourable")


def maximum_r5_clique() -> tuple[int, tuple[int, ...]]:
    neighbours = [
        {
            other
            for other in range(32)
            if (word ^ other).bit_count() == 2
        }
        for word in range(32)
    ]
    best: tuple[int, ...] = ()

    def search(clique: tuple[int, ...], candidates: set[int]) -> None:
        nonlocal best
        if len(clique) + len(candidates) <= len(best):
            return
        if not candidates:
            if len(clique) > len(best):
                best = clique
            return
        while candidates:
            if len(clique) + len(candidates) <= len(best):
                return
            vertex = min(candidates)
            candidates.remove(vertex)
            search(
                clique + (vertex,),
                candidates & neighbours[vertex],
            )
        if len(clique) > len(best):
            best = clique

    search((), set(range(32)))
    return len(best), best


def validate_affine_map_obstruction() -> None:
    """Exhaust all 5 by 3 binary matrices."""
    successes = 0
    for columns_word in range(1 << 15):
        images = []
        for value in range(1, 8):
            image = 0
            for output in range(5):
                row = (columns_word >> (3 * output)) & 0b111
                if (row & value).bit_count() & 1:
                    image |= 1 << output
            images.append(image)
        if all(image.bit_count() == 2 for image in images):
            successes += 1
    assert successes == 0


def validate_petersen() -> None:
    edges, supplied_labels = petersen_construction()
    assert graph6_encode(10, edges) == PETERSEN_GRAPH6
    rows = incidence(10, edges)
    assert len(edges) == 15
    assert all(len(row) == 3 for row in rows)
    assert connected(10, edges)
    assert all(connected(10, edges, edge) for edge in range(len(edges)))
    assert graph_girth(10, edges) == 5
    assert set(supplied_labels) == set(combinations(range(6), 2))

    flow = tuple(left ^ right for left, right in supplied_labels)
    assert flow_is_good(10, edges, flow)
    assert set(flow) == set(range(1, 8))

    raw_potential = tuple(
        block[0] ^ block[1] ^ block[2]
        for block in PETERSEN_BLOCKS
    )
    reconstructed = oum_pair_labels(
        10, edges, flow, raw_potential
    )
    assert reconstructed == supplied_labels

    potentials = compatible_potentials(10, edges, flow)
    assert len(potentials) == 4
    expected_selected = tuple(
        value ^ raw_potential[0] for value in raw_potential
    )
    assert expected_selected in potentials
    profiles = Counter()
    for potential in potentials:
        labels = oum_pair_labels(10, edges, flow, potential)
        graph = coordinate_graph(labels)
        profiles[(
            len(set(labels)),
            chromatic_number(graph),
            len(complete_support(graph, 6) or ()),
        )] += 1
    assert profiles == Counter({
        (15, 6, 6): 1,
        (10, 5, 0): 3,
    })

    supplied_graph = coordinate_graph(supplied_labels)
    assert complete_support(supplied_graph, 6) == tuple(range(6))
    assert chromatic_number(supplied_graph) == 6


def validate_rigid_fixed_flow() -> None:
    assert graph6_encode(12, RIGID_EDGES) == RIGID_GRAPH6
    rows = incidence(12, RIGID_EDGES)
    assert all(len(row) == 3 for row in rows)
    assert connected(12, RIGID_EDGES)
    assert all(
        connected(12, RIGID_EDGES, edge)
        for edge in range(len(RIGID_EDGES))
    )
    assert flow_is_good(12, RIGID_EDGES, RIGID_FLOW)
    assert set(RIGID_FLOW) == set(range(1, 8))

    potentials = compatible_potentials(
        12, RIGID_EDGES, RIGID_FLOW
    )
    assert potentials == (
        (0, 5, 5, 1, 5, 6, 7, 4, 7, 3, 7, 2),
    )
    labels = oum_pair_labels(
        12, RIGID_EDGES, RIGID_FLOW, potentials[0]
    )
    expected_coordinates = (0, 1, 2, 3, 4, 6)
    assert set(combinations(expected_coordinates, 2)) <= set(labels)
    graph = coordinate_graph(labels)
    assert complete_support(graph, 6) == expected_coordinates
    assert chromatic_number(graph) == 6


def main() -> None:
    validate_affine_map_obstruction()
    clique_size, clique = maximum_r5_clique()
    assert clique_size == 5
    assert all(
        (left ^ right).bit_count() == 2
        for left, right in combinations(clique, 2)
    )
    validate_petersen()
    validate_rigid_fixed_flow()
    print(
        "PASS: exact Oum compression system controls; no affine "
        "all-seven map; omega(R5)=5; minimum-order Petersen supplied "
        "K6 obstruction; unique-potential 12-vertex fixed-flow K6"
    )


if __name__ == "__main__":
    main()
