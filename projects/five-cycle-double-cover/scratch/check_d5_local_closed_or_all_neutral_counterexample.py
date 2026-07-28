#!/usr/bin/env python3
"""Standalone checker for a counterexample to a local D5 switch dichotomy.

The checker deliberately imports no project code.  It verifies the graph6
record, cubicity, simplicity, connectedness, bridgelessness, the D5 flow
equations, the three local factor components, their nonempty P-boundaries,
and the exact Euler-characteristic changes after the three switches.
"""

from collections import deque
import json


GRAPH6 = "M???FBObB_DOD_B_?"

# graph6's standard upper-triangle (right endpoint first) edge order.
EDGES = (
    (0, 7), (1, 7), (2, 7),
    (0, 8), (1, 8), (3, 8),
    (0, 9), (4, 9), (5, 9),
    (1, 10), (2, 10), (3, 10),
    (2, 11), (4, 11), (6, 11),
    (3, 12), (5, 12), (6, 12),
    (4, 13), (5, 13), (6, 13),
)

# A label is a bit mask for a two-subset of {0,1,2,3,4}.
LABELS = (
    0x03, 0x05, 0x06,
    0x0A, 0x0C, 0x06,
    0x09, 0x18, 0x11,
    0x09, 0x05, 0x0C,
    0x03, 0x09, 0x0A,
    0x0A, 0x09, 0x03,
    0x11, 0x18, 0x09,
)

ANCHOR_VERTEX = 2
ANCHOR_EDGES = (10, 12)
EXPECTED = {
    (0, 3): {
        "component": (10, 11, 12, 14, 15, 17),
        "boundary": (9, 13, 16, 20),
        "delta_chi": 2,
    },
    (0, 4): {
        "component": (0, 1, 6, 7, 9, 10, 12, 13),
        "boundary": (8, 18),
        "delta_chi": 0,
    },
    (1, 2): {
        "component": (10, 11, 12, 14, 15, 17),
        "boundary": (2, 5),
        "delta_chi": 0,
    },
}


def decode_short_graph6(record):
    assert record and record[0] != "~"
    n = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    answer = []
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                answer.append((left, right))
            cursor += 1
    return n, tuple(answer)


def incidence(n, edges):
    rows = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return rows


def reachable_vertices(n, edges, omitted_edge=None):
    rows = incidence(n, edges)
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for edge in rows[vertex]:
            if edge == omitted_edge:
                continue
            left, right = edges[edge]
            other = right if left == vertex else left
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return seen


def active(label, pair):
    return ((label >> pair[0]) & 1) ^ ((label >> pair[1]) & 1)


def edge_component(n, edges, selected, seed):
    rows = incidence(n, edges)
    answer = {seed}
    vertices = deque(edges[seed])
    seen_vertices = set(edges[seed])
    while vertices:
        vertex = vertices.popleft()
        for edge in rows[vertex]:
            if edge not in selected or edge in answer:
                continue
            answer.add(edge)
            for endpoint in edges[edge]:
                if endpoint not in seen_vertices:
                    seen_vertices.add(endpoint)
                    vertices.append(endpoint)
    return answer


def transpose_label(label, pair):
    first = (label >> pair[0]) & 1
    second = (label >> pair[1]) & 1
    if first == second:
        return label
    return label ^ (1 << pair[0]) ^ (1 << pair[1])


def edge_subgraph_components(n, edges, selected):
    """Count nonempty connected components of an edge subset."""
    unseen = set(selected)
    count = 0
    rows = incidence(n, edges)
    while unseen:
        count += 1
        seed = unseen.pop()
        queue = deque(edges[seed])
        seen_vertices = set(edges[seed])
        while queue:
            vertex = queue.popleft()
            for edge in rows[vertex]:
                if edge not in unseen:
                    continue
                unseen.remove(edge)
                for endpoint in edges[edge]:
                    if endpoint not in seen_vertices:
                        seen_vertices.add(endpoint)
                        queue.append(endpoint)
    return count


def coordinate_profile(n, edges, labels):
    profile = []
    for coordinate in range(5):
        selected = {
            edge
            for edge, label in enumerate(labels)
            if (label >> coordinate) & 1
        }
        profile.append(edge_subgraph_components(n, edges, selected))
    return tuple(profile)


def check_flow(n, edges, labels):
    rows = incidence(n, edges)
    assert all(label.bit_count() == 2 and label < 32 for label in labels)
    for row in rows:
        xor_sum = 0
        for edge in row:
            xor_sum ^= labels[edge]
        assert xor_sum == 0
        assert all(
            sum((labels[edge] >> coordinate) & 1 for edge in row) % 2 == 0
            for coordinate in range(5)
        )


def main():
    n, decoded_edges = decode_short_graph6(GRAPH6)
    assert n == 14
    assert decoded_edges == EDGES
    assert len(EDGES) == len(set(EDGES)) == 21
    assert all(left != right for left, right in EDGES)
    rows = incidence(n, EDGES)
    assert all(len(row) == 3 for row in rows)
    assert len(reachable_vertices(n, EDGES)) == n
    assert all(
        len(reachable_vertices(n, EDGES, omitted_edge=edge)) == n
        for edge in range(len(EDGES))
    )
    check_flow(n, EDGES, LABELS)

    first_edge, second_edge = ANCHOR_EDGES
    assert first_edge in rows[ANCHOR_VERTEX]
    assert second_edge in rows[ANCHOR_VERTEX]
    assert LABELS[first_edge] == 0x05  # {0,2}
    assert LABELS[second_edge] == 0x03  # {0,1}

    common_pairs = []
    for first in range(5):
        for second in range(first + 1, 5):
            pair = (first, second)
            if active(LABELS[first_edge], pair) and active(
                LABELS[second_edge], pair
            ):
                common_pairs.append(pair)
    assert tuple(common_pairs) == tuple(EXPECTED)

    old_profile = coordinate_profile(n, EDGES, LABELS)
    old_chi = sum(old_profile) - n // 2
    assert old_profile == (1, 1, 1, 1, 1)
    assert old_chi == -2

    results = {}
    for pair in common_pairs:
        selected = {
            edge
            for edge, label in enumerate(LABELS)
            if active(label, pair)
        }
        component = edge_component(n, EDGES, selected, first_edge)
        assert second_edge in component
        vertices = {
            endpoint for edge in component for endpoint in EDGES[edge]
        }
        pair_label = (1 << pair[0]) | (1 << pair[1])
        boundary = {
            edge
            for edge, (left, right) in enumerate(EDGES)
            if LABELS[edge] == pair_label
            and ((left in vertices) != (right in vertices))
        }

        switched = tuple(
            transpose_label(label, pair) if edge in component else label
            for edge, label in enumerate(LABELS)
        )
        check_flow(n, EDGES, switched)
        new_profile = coordinate_profile(n, EDGES, switched)
        delta = sum(new_profile) - sum(old_profile)

        expected = EXPECTED[pair]
        assert tuple(sorted(component)) == expected["component"]
        assert tuple(sorted(boundary)) == expected["boundary"]
        assert boundary
        assert delta == expected["delta_chi"]
        results[str(pair)] = {
            "component_edges": sorted(component),
            "boundary_edges": sorted(boundary),
            "coordinate_components_before": old_profile,
            "coordinate_components_after": new_profile,
            "delta_chi": delta,
        }

    assert sorted(item["delta_chi"] for item in results.values()) == [0, 0, 2]
    print(json.dumps({
        "status": "PASS",
        "graph6": GRAPH6,
        "vertices": n,
        "edges": len(EDGES),
        "simple_cubic_connected_bridgeless": True,
        "anchor_vertex": ANCHOR_VERTEX,
        "anchor_edges": ANCHOR_EDGES,
        "results": results,
        "conclusion": (
            "all three B(P,K) are nonempty, but the three delta-chi "
            "values are not all zero"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
