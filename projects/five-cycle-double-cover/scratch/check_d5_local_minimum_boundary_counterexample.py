#!/usr/bin/env python3
"""Standalone checker for the 2-lift counterexample to min |B| <= 2."""

from collections import deque
import json


BASE_GRAPH6 = "I?Bcu`gM?"
BASE_EDGES = (
    (0, 5), (0, 6), (0, 7),
    (1, 5), (1, 7), (1, 8),
    (2, 5), (2, 8), (2, 9),
    (3, 6), (3, 7), (3, 9),
    (4, 6), (4, 8), (4, 9),
)
BASE_LABELS = (
    0x03, 0x05, 0x06, 0x0A, 0x03,
    0x09, 0x09, 0x11, 0x18, 0x09,
    0x05, 0x0C, 0x0C, 0x18, 0x14,
)
VOLTAGE_ONE_EDGE = 3
BASE_ANCHOR_VERTEX = 1
BASE_ANCHOR_EDGES = (3, 5)
EXPECTED_BASE = {
    (0, 1): ((3, 5, 6, 7), (0, 4)),
    (2, 3): ((3, 5, 6, 8, 13, 14), (11, 12)),
    (3, 4): ((3, 5, 6, 7), (8, 13)),
}
EXPECTED_LIFT = {
    (0, 1): (
        (6, 7, 10, 11, 12, 13, 14, 15),
        (0, 1, 8, 9),
        0,
    ),
    (2, 3): (
        (6, 7, 10, 11, 12, 13, 16, 17, 26, 27, 28, 29),
        (22, 23, 24, 25),
        0,
    ),
    (3, 4): (
        (6, 7, 10, 11, 12, 13, 14, 15),
        (16, 17, 26, 27),
        0,
    ),
}


def decode_graph6(record):
    n = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return n, tuple(edges)


def rows(n, edges):
    answer = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        answer[left].append(edge)
        answer[right].append(edge)
    return answer


def reachable(n, edges, omitted=None):
    incidence = rows(n, edges)
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for edge in incidence[vertex]:
            if edge == omitted:
                continue
            left, right = edges[edge]
            other = right if left == vertex else left
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return seen


def active(label, pair):
    return bool(
        ((label >> pair[0]) & 1) ^ ((label >> pair[1]) & 1)
    )


def component(n, edges, selected, seed):
    incidence = rows(n, edges)
    answer = {seed}
    seen_vertices = set(edges[seed])
    queue = deque(edges[seed])
    while queue:
        vertex = queue.popleft()
        for edge in incidence[vertex]:
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


def check_graph_and_flow(n, edges, labels):
    assert len(edges) == len(labels) == 3 * n // 2
    assert len(edges) == len(set(edges))
    assert all(left != right for left, right in edges)
    incidence = rows(n, edges)
    assert all(len(row) == 3 for row in incidence)
    assert len(reachable(n, edges)) == n
    assert all(len(reachable(n, edges, edge)) == n for edge in range(len(edges)))
    assert all(label.bit_count() == 2 and label < 32 for label in labels)
    for row in incidence:
        value = 0
        for edge in row:
            value ^= labels[edge]
        assert value == 0


def profile(n, edges, labels):
    incidence = rows(n, edges)
    answer = []
    for coordinate in range(5):
        unseen = {
            edge
            for edge, label in enumerate(labels)
            if (label >> coordinate) & 1
        }
        count = 0
        while unseen:
            count += 1
            seed = unseen.pop()
            seen_vertices = set(edges[seed])
            queue = deque(edges[seed])
            while queue:
                vertex = queue.popleft()
                for edge in incidence[vertex]:
                    if edge not in unseen:
                        continue
                    unseen.remove(edge)
                    for endpoint in edges[edge]:
                        if endpoint not in seen_vertices:
                            seen_vertices.add(endpoint)
                            queue.append(endpoint)
        answer.append(count)
    return tuple(answer)


def local_data(n, edges, labels, anchor_edges):
    candidates = []
    for first in range(5):
        for second in range(first + 1, 5):
            pair = (first, second)
            if active(labels[anchor_edges[0]], pair) and active(
                labels[anchor_edges[1]], pair
            ):
                selected = {
                    edge
                    for edge, label in enumerate(labels)
                    if active(label, pair)
                }
                factor = component(n, edges, selected, anchor_edges[0])
                assert anchor_edges[1] in factor
                support = {
                    endpoint for edge in factor for endpoint in edges[edge]
                }
                pair_label = (1 << first) | (1 << second)
                boundary = {
                    edge
                    for edge, (left, right) in enumerate(edges)
                    if labels[edge] == pair_label
                    and ((left in support) != (right in support))
                }
                candidates.append((pair, factor, boundary))
    assert len(candidates) == 3
    return candidates


def main():
    base_n, decoded = decode_graph6(BASE_GRAPH6)
    assert base_n == 10 and set(decoded) == set(BASE_EDGES)
    check_graph_and_flow(base_n, BASE_EDGES, BASE_LABELS)
    for pair, factor, boundary in local_data(
        base_n, BASE_EDGES, BASE_LABELS, BASE_ANCHOR_EDGES
    ):
        expected_factor, expected_boundary = EXPECTED_BASE[pair]
        assert tuple(sorted(factor)) == expected_factor
        assert tuple(sorted(boundary)) == expected_boundary
        assert sum(edge == VOLTAGE_ONE_EDGE for edge in factor) % 2 == 1

    # The 2-lift uses vertices 2*v+s.  Every base edge gets its sheet-0
    # lift first and its sheet-1 lift second.
    lift_edges = []
    lift_labels = []
    lifted_edge = {}
    for edge, (left, right) in enumerate(BASE_EDGES):
        voltage = int(edge == VOLTAGE_ONE_EDGE)
        ids = []
        for sheet in (0, 1):
            ids.append(len(lift_edges))
            lift_edges.append(
                (2 * left + sheet, 2 * right + (sheet ^ voltage))
            )
            lift_labels.append(BASE_LABELS[edge])
        lifted_edge[edge] = tuple(ids)
    lift_edges = tuple(lift_edges)
    lift_labels = tuple(lift_labels)
    lift_n = 2 * base_n
    check_graph_and_flow(lift_n, lift_edges, lift_labels)

    anchor_vertex = 2 * BASE_ANCHOR_VERTEX
    anchor_edges = (
        lifted_edge[BASE_ANCHOR_EDGES[0]][0],
        lifted_edge[BASE_ANCHOR_EDGES[1]][0],
    )
    assert all(edge in rows(lift_n, lift_edges)[anchor_vertex] for edge in anchor_edges)
    old_profile = profile(lift_n, lift_edges, lift_labels)
    assert old_profile == (2, 1, 2, 1, 2)
    results = {}
    for pair, factor, boundary in local_data(
        lift_n, lift_edges, lift_labels, anchor_edges
    ):
        switched = tuple(
            transpose(label, pair) if edge in factor else label
            for edge, label in enumerate(lift_labels)
        )
        check_graph_and_flow(lift_n, lift_edges, switched)
        new_profile = profile(lift_n, lift_edges, switched)
        delta = sum(new_profile) - sum(old_profile)
        expected_factor, expected_boundary, expected_delta = EXPECTED_LIFT[pair]
        assert tuple(sorted(factor)) == expected_factor
        assert tuple(sorted(boundary)) == expected_boundary
        assert len(boundary) == 4
        assert delta == expected_delta
        results[str(pair)] = {
            "component_edges": sorted(factor),
            "boundary_edges": sorted(boundary),
            "delta_chi": delta,
        }

    print(json.dumps({
        "status": "PASS",
        "base_graph6": BASE_GRAPH6,
        "lift_vertices": lift_n,
        "lift_edges": len(lift_edges),
        "voltage_one_base_edge": VOLTAGE_ONE_EDGE,
        "simple_cubic_connected_bridgeless": True,
        "anchor_vertex": anchor_vertex,
        "anchor_edges": anchor_edges,
        "results": results,
        "conclusion": "all three local boundary sets have size four",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
