#!/usr/bin/env python3
"""Standalone exact checker for the order-16 two-neutral counterexample.

No project module is imported.  The graph is decoded from graph6, and every
graph, flow, factor-component, boundary, switch, and component-count claim
is recomputed from the literal witness.
"""

from collections import deque
import json


GRAPH6 = "O????B_sDOM?D_BO@W?M?"
STATE_HEX = "0305060a030909030a0605030a1218120a18180911181109"
LABELS = tuple(
    int(STATE_HEX[index:index + 2], 16)
    for index in range(0, len(STATE_HEX), 2)
)
ANCHOR_VERTEX = 4
ANCHOR_EDGES = (8, 15)
EXPECTED = {
    (0, 1): ((3, 5, 6, 8, 12, 13, 15, 16), (0, 4, 7, 11), 2),
    (1, 2): ((7, 8, 10, 11, 12, 13, 15, 16), (2, 9), 0),
    (3, 4): (
        (3, 5, 6, 8, 12, 13, 15, 16),
        (14, 17, 18, 21),
        -2,
    ),
}


def decode_graph6(record):
    assert record and record[0] != "~"
    vertices = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, tuple(edges)


def incidence(vertices, edges):
    rows = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return rows


def reachable(vertices, edges, omitted=None):
    rows = incidence(vertices, edges)
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


def is_active(label, pair):
    return bool(
        ((label >> pair[0]) & 1) ^ ((label >> pair[1]) & 1)
    )


def factor_component(vertices, edges, selected, seed):
    rows = incidence(vertices, edges)
    answer = {seed}
    seen_vertices = set(edges[seed])
    queue = deque(edges[seed])
    while queue:
        vertex = queue.popleft()
        for edge in rows[vertex]:
            if edge not in selected or edge in answer:
                continue
            answer.add(edge)
            for endpoint in edges[edge]:
                if endpoint not in seen_vertices:
                    seen_vertices.add(endpoint)
                    queue.append(endpoint)
    return answer


def transpose(label, pair):
    first = (label >> pair[0]) & 1
    second = (label >> pair[1]) & 1
    return (
        label
        if first == second
        else label ^ (1 << pair[0]) ^ (1 << pair[1])
    )


def check_flow(vertices, edges, labels):
    assert len(edges) == len(labels)
    rows = incidence(vertices, edges)
    assert all(label < 32 and label.bit_count() == 2 for label in labels)
    for row in rows:
        xor_sum = 0
        for edge in row:
            xor_sum ^= labels[edge]
        assert xor_sum == 0
        for coordinate in range(5):
            assert sum(
                (labels[edge] >> coordinate) & 1 for edge in row
            ) % 2 == 0


def subgraph_component_count(vertices, edges, selected):
    rows = incidence(vertices, edges)
    unseen = set(selected)
    count = 0
    while unseen:
        count += 1
        seed = unseen.pop()
        seen_vertices = set(edges[seed])
        queue = deque(edges[seed])
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


def profile(vertices, edges, labels):
    return tuple(
        subgraph_component_count(
            vertices,
            edges,
            {
                edge
                for edge, label in enumerate(labels)
                if (label >> coordinate) & 1
            },
        )
        for coordinate in range(5)
    )


def main():
    vertices, edges = decode_graph6(GRAPH6)
    assert vertices == 16 and len(edges) == 24
    assert len(edges) == len(set(edges))
    assert all(left != right for left, right in edges)
    rows = incidence(vertices, edges)
    assert all(len(row) == 3 for row in rows)
    assert len(reachable(vertices, edges)) == vertices
    assert all(
        len(reachable(vertices, edges, edge)) == vertices
        for edge in range(len(edges))
    )
    check_flow(vertices, edges, LABELS)
    assert ANCHOR_EDGES[0] in rows[ANCHOR_VERTEX]
    assert ANCHOR_EDGES[1] in rows[ANCHOR_VERTEX]

    candidates = tuple(
        pair
        for first in range(5)
        for second in range(first + 1, 5)
        for pair in ((first, second),)
        if is_active(LABELS[ANCHOR_EDGES[0]], pair)
        and is_active(LABELS[ANCHOR_EDGES[1]], pair)
    )
    assert candidates == tuple(EXPECTED)

    old_profile = profile(vertices, edges, LABELS)
    assert old_profile == (2, 1, 1, 2, 2)
    results = {}
    for pair in candidates:
        active_edges = {
            edge
            for edge, label in enumerate(LABELS)
            if is_active(label, pair)
        }
        component = factor_component(
            vertices, edges, active_edges, ANCHOR_EDGES[0]
        )
        assert ANCHOR_EDGES[1] in component
        support = {
            endpoint for edge in component for endpoint in edges[edge]
        }
        pair_label = (1 << pair[0]) | (1 << pair[1])
        boundary = {
            edge
            for edge, (left, right) in enumerate(edges)
            if LABELS[edge] == pair_label
            and ((left in support) != (right in support))
        }
        switched = tuple(
            transpose(label, pair) if edge in component else label
            for edge, label in enumerate(LABELS)
        )
        check_flow(vertices, edges, switched)
        new_profile = profile(vertices, edges, switched)
        delta = sum(new_profile) - sum(old_profile)
        expected_component, expected_boundary, expected_delta = EXPECTED[pair]
        assert tuple(sorted(component)) == expected_component
        assert tuple(sorted(boundary)) == expected_boundary
        assert boundary
        assert delta == expected_delta
        results[str(pair)] = {
            "component_edges": sorted(component),
            "boundary_edges": sorted(boundary),
            "coordinate_components_before": old_profile,
            "coordinate_components_after": new_profile,
            "delta_chi": delta,
        }

    deltas = sorted(item["delta_chi"] for item in results.values())
    assert deltas == [-2, 0, 2]
    print(json.dumps({
        "status": "PASS",
        "graph6": GRAPH6,
        "vertices": vertices,
        "edges": len(edges),
        "simple_cubic_connected_bridgeless": True,
        "anchor_vertex": ANCHOR_VERTEX,
        "anchor_edges": ANCHOR_EDGES,
        "results": results,
        "conclusion": (
            "all three B(P,K) are nonempty, but only one switch is neutral"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
