#!/usr/bin/env python3
"""Independent literal checker for the local-maximum sign counterexample.

This implementation imports only Python's standard library and shares no
code with the producing 2-lift search.
"""

from collections import Counter, deque
import json


GRAPH6 = (
    "[???????????_?O?D??g?__H@?PB??c_?aA?COO?@S??Ag?AE??@H??P?_?AGO??"
)
STATE_HEX = (
    "03 09 0a 03 09 0a 0c 14 18 0c 14 18 14 12 06 14 12 06 "
    "11 18 09 11 18 09 0c 18 14 0c 18 14 0a 06 0c 0a 06 0c "
    "11 12 11 12 18 18"
)
LABELS = tuple(int(token, 16) for token in STATE_HEX.split())
LOCAL_EDGES = (7, 8)
EXPECTED_LOCAL = {
    (0, 4): (4, -2),
    (1, 4): (4, -2),
    (2, 3): (4, -2),
}


def decode_graph6(record):
    assert record and record[0] != "~"
    n = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    decoded = []
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                decoded.append((left, right))
            cursor += 1
    # The witness labels use the producer's deterministic endpoint order.
    return n, tuple(sorted(decoded))


def incidence(n, edges):
    answer = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        answer[left].append(edge)
        answer[right].append(edge)
    return answer


def reachable(n, edges, omitted=None):
    rows = incidence(n, edges)
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for edge in rows[vertex]:
            if edge == omitted:
                continue
            left, right = edges[edge]
            other = right if left == vertex else left
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return seen


def check_flow(n, edges, labels):
    assert len(edges) == len(labels)
    assert all(label.bit_count() == 2 and label < 32 for label in labels)
    for row in incidence(n, edges):
        assert len(row) == 3
        assert labels[row[0]] ^ labels[row[1]] ^ labels[row[2]] == 0
        for coordinate in range(5):
            assert sum(
                (labels[edge] >> coordinate) & 1 for edge in row
            ) % 2 == 0


def active(label, pair):
    return bool(
        ((label >> pair[0]) & 1) ^ ((label >> pair[1]) & 1)
    )


def edge_components(n, edges, selected):
    rows = incidence(n, edges)
    unseen = set(selected)
    answer = []
    while unseen:
        seed = unseen.pop()
        component = {seed}
        seen_vertices = set(edges[seed])
        queue = deque(edges[seed])
        while queue:
            vertex = queue.popleft()
            for edge in rows[vertex]:
                if edge not in unseen:
                    continue
                unseen.remove(edge)
                component.add(edge)
                for endpoint in edges[edge]:
                    if endpoint not in seen_vertices:
                        seen_vertices.add(endpoint)
                        queue.append(endpoint)
        answer.append(frozenset(component))
    return tuple(answer)


def transpose(label, pair):
    first = (label >> pair[0]) & 1
    second = (label >> pair[1]) & 1
    return (
        label
        if first == second
        else label ^ (1 << pair[0]) ^ (1 << pair[1])
    )


def profile(n, edges, labels):
    return tuple(
        len(edge_components(
            n,
            edges,
            {
                edge
                for edge, label in enumerate(labels)
                if (label >> coordinate) & 1
            },
        ))
        for coordinate in range(5)
    )


def chi(n, edges, labels):
    return sum(profile(n, edges, labels)) - len(edges) + n


def neutral_distances(edge_count, components, source):
    through = [[] for _ in range(edge_count)]
    for index, component in enumerate(components):
        for edge in component:
            through[edge].append(index)
    distance = [None] * edge_count
    distance[source] = 0
    queue = deque([source])
    used_components = set()
    while queue:
        edge = queue.popleft()
        for index in through[edge]:
            if index in used_components:
                continue
            used_components.add(index)
            for other in components[index]:
                candidate = distance[edge] + 1
                if distance[other] is None or candidate < distance[other]:
                    distance[other] = candidate
                    queue.append(other)
    return distance


def main():
    n, edges = decode_graph6(GRAPH6)
    assert n == 28 and len(edges) == 42
    assert len(edges) == len(set(edges))
    assert all(left != right for left, right in edges)
    assert all(len(row) == 3 for row in incidence(n, edges))
    assert len(reachable(n, edges)) == n
    assert all(
        len(reachable(n, edges, omitted=edge)) == n
        for edge in range(len(edges))
    )
    check_flow(n, edges, LABELS)
    assert set(edges[LOCAL_EDGES[0]]) & set(edges[LOCAL_EDGES[1]]) == {2}

    old_profile = profile(n, edges, LABELS)
    old_chi = chi(n, edges, LABELS)
    assert old_chi == -4
    moves = []
    local = {}
    for first in range(5):
        for second in range(first + 1, 5):
            pair = (first, second)
            selected = {
                edge
                for edge, label in enumerate(LABELS)
                if active(label, pair)
            }
            for component in edge_components(n, edges, selected):
                switched = tuple(
                    transpose(label, pair) if edge in component else label
                    for edge, label in enumerate(LABELS)
                )
                check_flow(n, edges, switched)
                delta = chi(n, edges, switched) - old_chi
                moves.append((pair, component, delta))
                if all(edge in component for edge in LOCAL_EDGES):
                    support = {
                        endpoint
                        for edge in component
                        for endpoint in edges[edge]
                    }
                    pair_label = (1 << first) | (1 << second)
                    boundary = {
                        edge
                        for edge, (left, right) in enumerate(edges)
                        if LABELS[edge] == pair_label
                        and ((left in support) != (right in support))
                    }
                    local[pair] = {
                        "component_edges": sorted(component),
                        "boundary_edges": sorted(boundary),
                        "boundary_size": len(boundary),
                        "delta_chi": delta,
                    }

    histogram = Counter(delta for _, _, delta in moves)
    # Only nonempty factor components are moves.  Isolated graph vertices
    # of a factor are not components of its edge subgraph.
    assert len(moves) == 24
    assert histogram == Counter({0: 12, -2: 12})
    assert max(histogram) == 0
    assert set(local) == set(EXPECTED_LOCAL)
    for pair, (boundary_size, delta) in EXPECTED_LOCAL.items():
        assert local[pair]["boundary_size"] == boundary_size
        assert local[pair]["delta_chi"] == delta

    neutral_components = [
        component for _, component, delta in moves if delta == 0
    ]
    distances = [
        neutral_distances(len(edges), neutral_components, source)
        for source in range(len(edges))
    ]
    assert all(
        distance is not None for row in distances for distance in row
    )
    assert distances[LOCAL_EDGES[0]][LOCAL_EDGES[1]] == 2
    assert max(distance for row in distances for distance in row) == 3

    print(json.dumps({
        "status": "PASS",
        "graph6": GRAPH6,
        "vertices": n,
        "edges": len(edges),
        "simple_cubic_connected_bridgeless": True,
        "coordinate_components": old_profile,
        "surface_chi": old_chi,
        "all_switch_delta_histogram": dict(sorted(histogram.items())),
        "one_move_local_maximum": True,
        "local_edge_pair": LOCAL_EDGES,
        "local_candidates": {
            str(pair): data for pair, data in local.items()
        },
        "neutral_hypergraph_connected": True,
        "local_neutral_distance": 2,
        "maximum_neutral_distance": 3,
        "conclusion": (
            "all three local switch deltas are -2 at a local chi maximum"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
