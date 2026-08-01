#!/usr/bin/env python3
"""Exact replay of a counterexample to the proposed avoiding-circuit lemma.

The graph is an 18-vertex Blanusa snark in graph6 format.  Edge IDs are the
indices in the lexicographically sorted edge list.  Flow values are the
integers 1,...,7, regarded as the nonzero vectors of F_2^3; addition is XOR.

The script uses only the Python standard library.  It checks:

* the graph6 record and the displayed edge list agree;
* simplicity, connectedness, cubicity, bridgelessness, girth five, cyclic
  edge-connectivity four, and absence of a proper 3-edge-colouring;
* the displayed values form a nowhere-zero F_2^3-flow;
* H = G - E_4 is connected;
* the cycle space of H has dimension five; and
* all 32 even edge-subsets of H are enumerated.  Exactly four contain the
  three prescribed value-3 edges, and each of the four is disconnected.

Thus there is no circuit (connected Eulerian edge-subgraph, equivalently a
closed trail without repeated edges) containing S and avoiding E_4.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations


GRAPH6 = "Q???C@?GCoOoDO[?CcAO_?k?J??"

# The canonical edge order used throughout this certificate.
EDGES = (
    (0, 7),
    (0, 10),
    (0, 11),
    (1, 8),
    (1, 13),
    (1, 15),
    (2, 9),
    (2, 13),
    (2, 14),
    (3, 10),
    (3, 12),
    (3, 13),
    (4, 10),
    (4, 15),
    (4, 17),
    (5, 11),
    (5, 12),
    (5, 14),
    (6, 11),
    (6, 16),
    (6, 17),
    (7, 12),
    (7, 17),
    (8, 14),
    (8, 16),
    (9, 15),
    (9, 16),
)

# A nowhere-zero F_2^3-flow, in EDGES order.
FLOW = (
    2,
    6,
    4,
    2,
    1,
    3,
    3,
    4,
    7,
    4,
    1,
    5,
    2,
    1,
    3,
    2,
    4,
    6,
    6,
    2,
    4,
    5,
    7,
    1,
    3,
    2,
    1,
)

T_VALUE = 4
S_VALUE = 3
PRESCRIBED = frozenset((5, 6, 14))
EXPECTED_T_CLASS = frozenset((2, 7, 9, 16, 20))

# A human-readable cycle-space basis for H = G - E_4.
HUMAN_BASIS = (
    frozenset((0, 1, 4, 5, 10, 11, 12, 13, 21)),
    frozenset((3, 5, 6, 8, 23, 25)),
    frozenset((0, 1, 12, 14, 22)),
    frozenset((3, 5, 15, 17, 18, 19, 23, 25, 26)),
    frozenset((3, 5, 24, 25, 26)),
)

EXPECTED_COVERS = {
    frozenset((0, 1, 3, 5, 6, 8, 12, 14, 22, 23, 25)): (
        frozenset((0, 4, 7, 10, 17)),
        frozenset((1, 2, 8, 9, 14, 15)),
    ),
    frozenset(
        (4, 5, 6, 8, 10, 11, 13, 14, 15, 17, 18, 19, 21, 22, 26)
    ): (
        frozenset((1, 3, 4, 7, 12, 13, 15, 17)),
        frozenset((2, 5, 6, 9, 11, 14, 16)),
    ),
    frozenset((4, 5, 6, 8, 10, 11, 13, 14, 21, 22, 23, 24, 26)): (
        frozenset((1, 3, 4, 7, 12, 13, 15, 17)),
        frozenset((2, 8, 9, 14, 16)),
    ),
    frozenset(
        (0, 1, 3, 5, 6, 8, 12, 14, 15, 17, 18, 19, 22, 24, 25)
    ): (
        frozenset((0, 4, 7, 10, 17)),
        frozenset((1, 2, 5, 6, 8, 9, 11, 14, 15, 16)),
    ),
}


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    """Decode the small-order (n <= 62) part of graph6."""
    assert record and record[0] != "~"
    vertices = ord(record[0]) - 63
    assert 0 <= vertices <= 62
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = vertices * (vertices - 1) // 2
    assert len(bits) >= needed
    decoded = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                decoded.append((left, right))
            cursor += 1
    return vertices, tuple(sorted(decoded))


def incidence(vertices: int, edges=EDGES) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(vertices)]
    for edge_id, (left, right) in enumerate(edges):
        rows[left].append(edge_id)
        rows[right].append(edge_id)
    return tuple(tuple(row) for row in rows)


def vertex_components(
    vertices: int,
    selected: frozenset[int],
    *,
    include_isolates: bool,
) -> tuple[frozenset[int], ...]:
    rows: list[list[int]] = [[] for _ in range(vertices)]
    active = set(range(vertices)) if include_isolates else set()
    for edge_id in selected:
        left, right = EDGES[edge_id]
        rows[left].append(right)
        rows[right].append(left)
        active.add(left)
        active.add(right)
    answer = []
    while active:
        root = min(active)
        active.remove(root)
        reached = {root}
        queue = [root]
        while queue:
            vertex = queue.pop()
            for other in rows[vertex]:
                if other in active:
                    active.remove(other)
                    reached.add(other)
                    queue.append(other)
        answer.append(frozenset(reached))
    return tuple(answer)


def connected_graph(vertices: int, selected: frozenset[int]) -> bool:
    return len(vertex_components(vertices, selected, include_isolates=True)) == 1


def is_even(vertices: int, selected: frozenset[int]) -> bool:
    degree = [0] * vertices
    for edge_id in selected:
        left, right = EDGES[edge_id]
        degree[left] ^= 1
        degree[right] ^= 1
    return not any(degree)


def connected_eulerian(vertices: int, selected: frozenset[int]) -> bool:
    return (
        bool(selected)
        and is_even(vertices, selected)
        and len(vertex_components(vertices, selected, include_isolates=False)) == 1
    )


def has_cycle_on_shore(shore: frozenset[int]) -> bool:
    """Check whether the subgraph induced by shore contains a cycle."""
    parent = {vertex: vertex for vertex in shore}

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in EDGES:
        if left not in shore or right not in shore:
            continue
        root_left, root_right = find(left), find(right)
        if root_left == root_right:
            return True
        parent[root_left] = root_right
    return False


def cyclic_edge_connectivity(vertices: int) -> tuple[int, frozenset[int]]:
    """Exhaust all shores (normalised to contain vertex 0)."""
    all_vertices = frozenset(range(vertices))
    best = len(EDGES) + 1
    witness = frozenset()
    for remaining_mask in range(1 << (vertices - 1)):
        shore = frozenset(
            (0,)
            + tuple(
                vertex
                for vertex in range(1, vertices)
                if (remaining_mask >> (vertex - 1)) & 1
            )
        )
        if shore == all_vertices:
            continue
        other = all_vertices - shore
        boundary = frozenset(
            edge_id
            for edge_id, (left, right) in enumerate(EDGES)
            if (left in shore) != (right in shore)
        )
        if len(boundary) >= best:
            continue
        if has_cycle_on_shore(shore) and has_cycle_on_shore(other):
            best, witness = len(boundary), boundary
    return best, witness


def girth(vertices: int) -> int:
    rows = [[] for _ in range(vertices)]
    for left, right in EDGES:
        rows[left].append(right)
        rows[right].append(left)
    answer = vertices + 1
    for root in range(vertices):
        distance = [-1] * vertices
        parent = [-1] * vertices
        distance[root] = 0
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for other in rows[vertex]:
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    answer = min(
                        answer, distance[vertex] + distance[other] + 1
                    )
    return answer


def has_three_edge_colouring(vertices: int) -> bool:
    """Exact backtracking for a proper three-colouring of the edges."""
    used = [0] * vertices
    colours = [-1] * len(EDGES)

    def search() -> bool:
        best_edge = -1
        best_options = 0
        best_count = 4
        for edge_id, (left, right) in enumerate(EDGES):
            if colours[edge_id] >= 0:
                continue
            options = 0b111 & ~used[left] & ~used[right]
            count = options.bit_count()
            if count == 0:
                return False
            if count < best_count:
                best_edge, best_options, best_count = edge_id, options, count
        if best_edge < 0:
            return True
        left, right = EDGES[best_edge]
        while best_options:
            colour = best_options & -best_options
            best_options ^= colour
            colours[best_edge] = colour.bit_length() - 1
            used[left] |= colour
            used[right] |= colour
            if search():
                return True
            used[left] ^= colour
            used[right] ^= colour
            colours[best_edge] = -1
        return False

    # Break the global S_3 symmetry of the three colours.
    colours[0] = 0
    first_left, first_right = EDGES[0]
    used[first_left] = used[first_right] = 1
    return search()


def independent_even_basis(
    vertices: int, basis: tuple[frozenset[int], ...]
) -> bool:
    """Check evenness and F_2-linear independence by row reduction."""
    vectors = []
    for edge_set in basis:
        assert is_even(vertices, edge_set)
        value = sum(1 << edge_id for edge_id in edge_set)
        for pivot in vectors:
            value = min(value, value ^ pivot)
        if value == 0:
            return False
        vectors.append(value)
        vectors.sort(reverse=True)
    return True


def enumerate_cycle_space(
    basis: tuple[frozenset[int], ...],
) -> tuple[frozenset[int], ...]:
    words = [frozenset()]
    for vector in basis:
        words += [word ^ vector for word in words]
    return tuple(words)


def main() -> None:
    vertices, decoded = decode_graph6(GRAPH6)
    assert vertices == 18
    assert decoded == EDGES
    assert len(EDGES) == len(set(EDGES)) == 27
    assert all(left < right for left, right in EDGES)

    rows = incidence(vertices)
    assert all(len(row) == 3 for row in rows)
    all_edges = frozenset(range(len(EDGES)))
    assert connected_graph(vertices, all_edges)
    for edge_id in range(len(EDGES)):
        assert connected_graph(vertices, all_edges - {edge_id})
    assert girth(vertices) == 5
    cyclic_connectivity, cyclic_cut = cyclic_edge_connectivity(vertices)
    assert cyclic_connectivity == 4
    assert cyclic_cut
    assert not has_three_edge_colouring(vertices)

    assert len(FLOW) == len(EDGES)
    assert all(1 <= value <= 7 for value in FLOW)
    for vertex, incident_edges in enumerate(rows):
        total = 0
        for edge_id in incident_edges:
            total ^= FLOW[edge_id]
        assert total == 0, (vertex, incident_edges)

    t_class = frozenset(
        edge_id for edge_id, value in enumerate(FLOW) if value == T_VALUE
    )
    assert t_class == EXPECTED_T_CLASS
    assert all(FLOW[edge_id] == S_VALUE for edge_id in PRESCRIBED)
    h_edges = all_edges - t_class
    assert connected_graph(vertices, h_edges)
    assert len(h_edges) == 22

    # Since H is connected, its binary cycle-space dimension is
    # |E(H)|-|V(H)|+1 = 5.  Five independent even sets are therefore a basis.
    assert len(HUMAN_BASIS) == len(h_edges) - vertices + 1 == 5
    assert all(vector <= h_edges for vector in HUMAN_BASIS)
    assert independent_even_basis(vertices, HUMAN_BASIS)
    even_subgraphs = enumerate_cycle_space(HUMAN_BASIS)
    assert len(even_subgraphs) == 32
    assert len(set(even_subgraphs)) == 32
    assert all(is_even(vertices, word) for word in even_subgraphs)

    covers = tuple(word for word in even_subgraphs if PRESCRIBED <= word)
    assert frozenset(covers) == frozenset(EXPECTED_COVERS)
    assert len(covers) == 4
    for word in covers:
        actual_components = frozenset(
            vertex_components(vertices, word, include_isolates=False)
        )
        assert actual_components == frozenset(EXPECTED_COVERS[word])
        assert not connected_eulerian(vertices, word)

    # This is the exact negation of the proposed local switch:
    assert not any(
        PRESCRIBED <= word and connected_eulerian(vertices, word)
        for word in even_subgraphs
    )

    print("PASS")
    print(f"graph6: {GRAPH6}")
    print(
        "graph: simple connected bridgeless cubic; "
        f"girth={girth(vertices)}; cyclic_edge_connectivity={cyclic_connectivity}; "
        "not 3-edge-colourable"
    )
    print(f"t={T_VALUE}; E_t={sorted(t_class)}; H connected")
    print(f"s={S_VALUE}; prescribed edges={sorted(PRESCRIBED)}")
    print(
        "cycle-space audit: 32/32 even subgraphs enumerated; "
        f"{len(covers)} contain S; 0 are connected"
    )


if __name__ == "__main__":
    main()
