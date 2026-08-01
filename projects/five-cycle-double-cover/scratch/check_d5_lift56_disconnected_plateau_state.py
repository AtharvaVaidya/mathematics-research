#!/usr/bin/env python3
"""Independent literal check of the disconnected state in the 56v plateau.

This standard-library-only script does not attempt the 55,652-state plateau
BFS.  It independently checks the graph, flow, local-maximum property,
complete switch histogram, and exact neutral-component partition of the
frozen state emitted by the exhaustive C++ auditor.
"""

from collections import Counter, deque
import json


BASE_GRAPH6 = (
    "[???????????_?O?D??g?__H@?PB??c_?aA?COO?@S??Ag?AE??@H??P?_?AGO??"
)
VOLTAGE_ONE_EDGES = {18, 36}
STATE_HEX = (
    "03 03 05 05 06 06 03 03 05 05 06 06 18 18 0a 0c 12 14 11 18 "
    "03 0c 12 14 0c 0c 06 06 0a 0a 05 0c 06 06 03 0a 11 11 12 14 "
    "03 05 11 11 12 14 03 05 18 18 14 14 0c 0c 11 18 14 14 05 0c "
    "06 06 03 0a 05 0c 06 06 0a 0a 0c 0c 11 11 12 12 11 11 12 12 "
    "14 14 14 14"
)
LABELS = tuple(int(token, 16) for token in STATE_HEX.split())


def decode_graph6(record):
    n = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return n, tuple(sorted(edges))


def construct_lift():
    base_n, base_edges = decode_graph6(BASE_GRAPH6)
    assert base_n == 28 and len(base_edges) == 42
    edges = []
    for edge, (left, right) in enumerate(base_edges):
        voltage = int(edge in VOLTAGE_ONE_EDGES)
        for sheet in (0, 1):
            edges.append((
                2 * left + sheet,
                2 * right + (sheet ^ voltage),
            ))
    return 2 * base_n, tuple(edges)


def incidence(n, edges):
    rows = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return rows


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


def check_graph_and_flow(n, edges, labels):
    assert len(edges) == len(labels) == 3 * n // 2
    assert len(edges) == len(set(edges))
    assert all(left != right for left, right in edges)
    rows = incidence(n, edges)
    assert all(len(row) == 3 for row in rows)
    assert len(reachable(n, edges)) == n
    assert all(
        len(reachable(n, edges, edge)) == n
        for edge in range(len(edges))
    )
    assert all(label.bit_count() == 2 and label < 32 for label in labels)
    for row in rows:
        assert labels[row[0]] ^ labels[row[1]] ^ labels[row[2]] == 0


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


class Dsu:
    def __init__(self, size):
        self.parent = list(range(size))

    def find(self, value):
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def join(self, left, right):
        left = self.find(left)
        right = self.find(right)
        if left != right:
            self.parent[right] = left


def main():
    n, edges = construct_lift()
    check_graph_and_flow(n, edges, LABELS)
    old_chi = chi(n, edges, LABELS)
    assert old_chi == -8
    histogram = Counter()
    neutral = []
    moves = 0
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
                check_graph_and_flow(n, edges, switched)
                delta = chi(n, edges, switched) - old_chi
                histogram[delta] += 1
                moves += 1
                if delta == 0:
                    neutral.append(component)

    assert moves == 34
    assert histogram == Counter({0: 18, -2: 13, -3: 2, -1: 1})
    assert max(histogram) == 0
    dsu = Dsu(len(edges))
    for component in neutral:
        first = next(iter(component))
        for edge in component:
            dsu.join(first, edge)
    classes = {}
    for edge in range(len(edges)):
        classes.setdefault(dsu.find(edge), []).append(edge)
    class_rows = sorted(sorted(row) for row in classes.values())
    assert class_rows == [
        [edge for edge in range(84) if edge != 75],
        [75],
    ]

    print(json.dumps({
        "status": "PASS",
        "vertices": n,
        "edges": len(edges),
        "simple_cubic_connected_bridgeless": True,
        "surface_chi": old_chi,
        "nonempty_switches": moves,
        "delta_histogram": dict(sorted(histogram.items())),
        "one_move_local_maximum": True,
        "neutral_components": len(neutral),
        "neutral_classes": class_rows,
        "conclusion": (
            "the frozen state in the terminal plateau has a "
            "disconnected neutral-component hypergraph"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
