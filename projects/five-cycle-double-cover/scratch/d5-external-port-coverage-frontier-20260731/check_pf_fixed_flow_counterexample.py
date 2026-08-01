#!/usr/bin/env python3
"""Independent semantic replay of the marked-girth fixed-flow counterexample."""

from __future__ import annotations

import base64
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import zlib


PETERSEN = (
    (0, 1), (1, 2), (2, 3), (0, 4), (3, 4),
    (0, 5), (1, 6), (2, 7), (5, 7), (3, 8),
    (5, 8), (6, 8), (4, 9), (6, 9), (7, 9),
)
LCF = (17, -9, 37, -37, 9, -17) * 15
FOSTER_PORTS = (1, 17, 89)
PAIR_MASKS = tuple((1 << a) | (1 << b)
                   for a, b in combinations(range(5), 2))
HERE = Path(__file__).resolve().parent


def graph() -> tuple[int, tuple[tuple[int, int], ...]]:
    foster = set()
    for vertex in range(90):
        for other in ((vertex + 1) % 90, (vertex + LCF[vertex]) % 90):
            foster.add(tuple(sorted((vertex, other))))
    assert len(foster) == 135
    edges = []
    for copy in range(10):
        for left, right in foster:
            if 0 not in (left, right):
                edges.append((89 * copy + left - 1, 89 * copy + right - 1))
    used = [0] * 10
    for left, right in PETERSEN:
        a = 89 * left + FOSTER_PORTS[used[left]] - 1
        b = 89 * right + FOSTER_PORTS[used[right]] - 1
        used[left] += 1
        used[right] += 1
        edges.append(tuple(sorted((a, b))))
    assert used == [3] * 10
    return 890, tuple(sorted(edges))


def incidence(n: int, edges: tuple[tuple[int, int], ...]) -> list[list[int]]:
    rows = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return rows


def adjacency(n: int, edges: tuple[tuple[int, int], ...], *,
              omit: int = -1, skip: int = -1):
    rows = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        if edge == skip or omit in (left, right):
            continue
        rows[left].append((right, edge))
        rows[right].append((left, edge))
    return rows


def connected(n: int, edges: tuple[tuple[int, int], ...], *,
              omit: int = -1, skip: int = -1) -> bool:
    rows = adjacency(n, edges, omit=omit, skip=skip)
    start = next(vertex for vertex in range(n) if vertex != omit)
    seen, todo = {start}, [start]
    while todo:
        for other, _ in rows[todo.pop()]:
            if other not in seen:
                seen.add(other)
                todo.append(other)
    return len(seen) == n - int(omit >= 0)


def bridges(n: int, edges: tuple[tuple[int, int], ...], *,
            omit: int = -1, skip: int = -1) -> tuple[int, ...]:
    rows = adjacency(n, edges, omit=omit, skip=skip)
    start = next(vertex for vertex in range(n) if vertex != omit)
    tin, low, found = [-1] * n, [-1] * n, []
    timer = 0

    def visit(vertex: int, parent_edge: int) -> None:
        nonlocal timer
        tin[vertex] = low[vertex] = timer
        timer += 1
        for other, edge in rows[vertex]:
            if edge == parent_edge:
                continue
            if tin[other] >= 0:
                low[vertex] = min(low[vertex], tin[other])
            else:
                visit(other, edge)
                low[vertex] = min(low[vertex], low[other])
                if low[other] > tin[vertex]:
                    found.append(edge)

    visit(start, -1)
    assert sum(value >= 0 for value in tin) == n - int(omit >= 0)
    return tuple(sorted(found))


def girth(n: int, edges: tuple[tuple[int, int], ...], *,
          omit: int = -1, skip: int = -1) -> int:
    rows = adjacency(n, edges, omit=omit, skip=skip)
    best = n + 1
    for source in range(n):
        if source == omit:
            continue
        distance, parent_edge = [-1] * n, [-1] * n
        distance[source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for other, edge in rows[vertex]:
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent_edge[other] = edge
                    queue.append(other)
                elif parent_edge[vertex] != edge:
                    best = min(best, distance[vertex] + distance[other] + 1)
    return best


def petersen_not_tait() -> bool:
    rows = incidence(10, tuple(PETERSEN))
    colors = [-1] * len(PETERSEN)

    def search() -> bool:
        try:
            edge = colors.index(-1)
        except ValueError:
            return True
        for color in range(3):
            if all(colors[other] != color for vertex in PETERSEN[edge]
                   for other in rows[vertex] if other != edge):
                colors[edge] = color
                if search():
                    return True
                colors[edge] = -1
        return False

    return not search()


def component(edges, rows, labels: bytes, pair: int, root: int) -> set[int]:
    active = [((label & pair).bit_count() == 1) for label in labels]
    assert active[root]
    found, todo = {root}, [root]
    while todo:
        edge = todo.pop()
        for vertex in edges[edge]:
            local = [other for other in rows[vertex] if active[other]]
            assert len(local) in (0, 2)
            for other in local:
                if other not in found:
                    found.add(other)
                    todo.append(other)
    return found


def main() -> None:
    n, edges = graph()
    rows = incidence(n, edges)
    canonical = str(n) + "\n" + "".join(
        f"{edge} {left} {right}\n"
        for edge, (left, right) in enumerate(edges))
    assert sha256(canonical.encode()).hexdigest() == (
        "3fe0630cb52d5a0b29a473faff02389195c7e119ea8f7a6f95f3ba9c38272282")
    assert len(edges) == len(set(edges)) == 1335
    assert all(left != right for left, right in edges)
    assert all(len(row) == 3 for row in rows)
    assert connected(n, edges) and not bridges(n, edges)
    for removed in range(len(edges)):
        assert connected(n, edges, skip=removed)
        assert not bridges(n, edges, skip=removed)
    assert girth(n, edges) == 10
    assert petersen_not_tait()
    print("PF_GRAPH vertices=890 edges=1335 simple=1 cubic=1 edge_connectivity=3 girth=10 non_tait=1 PASS")

    z, root = 0, 552
    ports = tuple(rows[z])
    assert ports == (0, 1, 2) and edges[root] == (363, 400)
    assert connected(n, edges, omit=z)
    assert not bridges(n, edges, omit=z)
    assert girth(n, edges, omit=z) == 10
    assert connected(n, edges, omit=z, skip=root)
    assert girth(n, edges, omit=z, skip=root) >= 10
    print("PF_CORE vertices=889 degree2=3 degree3=886 connected=1 bridgeless=1 girth=10 root_deleted_connected=1 root_deleted_girth=10 PASS")

    encoded = (HERE / "pf-fixed-flow-labels.b85").read_bytes().strip()
    labels = zlib.decompress(base64.b85decode(encoded))
    assert len(labels) == 1335
    assert sha256(labels).hexdigest() == (
        "6390ba1039116351e8e4343264f9881e4d1541dc028a661db848be9c695fdc9a")
    assert all(0 < label < 32 and label.bit_count() == 2 for label in labels)
    assert all(labels[a] ^ labels[b] ^ labels[c] == 0 for a, b, c in rows)
    assert tuple(labels[edge] for edge in ports) == (18, 6, 20)
    assert labels[root] == 18
    print("PF_FLOW labels=1335 weight_two=1 vertex_xor=1 sha256=6390ba1039116351e8e4343264f9881e4d1541dc028a661db848be9c695fdc9a PASS")

    expected = {
        3: (449, (0, 1), "out"),
        17: (273, (), "none"),
        6: (523, (0, 2), "in"),
        10: (463, (), "none"),
        20: (46, (), "none"),
        24: (48, (), "none"),
    }
    typed_mask = 0
    external_ports = set()
    components = {}
    active_pairs = []
    for pair in PAIR_MASKS:
        if (labels[root] & pair).bit_count() != 1:
            continue
        active_pairs.append(pair)
        found = component(edges, rows, labels, pair, root)
        components[pair] = found
        slots = tuple(slot for slot, edge in enumerate(ports) if edge in found)
        if len(slots) == 2:
            inactive_slot = next(slot for slot in range(3) if slot not in slots)
            inactive = labels[ports[inactive_slot]]
            if inactive == pair:
                mode = "in"
                mode_bit = 0
            else:
                assert inactive & pair == 0
                mode = "out"
                mode_bit = 1
                external_ports.update(slots)
            physical = {(0, 1): 0, (0, 2): 1, (1, 2): 2}[slots]
            typed_mask |= 1 << (2 * physical + mode_bit)
        else:
            assert slots == ()
            mode = "none"
        assert (len(found), slots, mode) == expected[pair]
    assert tuple(active_pairs) == (3, 17, 6, 10, 20, 24)
    assert typed_mask == 6 and external_ports == {0, 1}
    print("PF_ROOT_FACTORS active_pairs=6 fixed_typed_mask=6 external_physical_pair=01 missing_external_port=2 PASS")

    internal = components[6]

    def trace(start_vertex: int) -> list[int]:
        sequence, previous, vertex = [root], root, start_vertex
        while vertex != z:
            following = next(edge for edge in rows[vertex]
                             if edge in internal and edge != previous)
            sequence.append(following)
            left, right = edges[following]
            vertex = right if vertex == left else left
            previous = following
            assert len(sequence) <= len(internal)
        return sequence

    arcs = [trace(vertex) for vertex in edges[root]]
    assert tuple(len(arc) for arc in arcs) == (355, 169)
    assert tuple(arc[-1] for arc in arcs) == (0, 2)
    counts = []
    for arc in arcs:
        values = []
        for edge in arc:
            outside = labels[edge] & ~6
            assert outside.bit_count() == 1
            values.append(outside.bit_length() - 1)
        counts.append(Counter(values))
    assert counts == [Counter({0: 109, 3: 115, 4: 131}),
                      Counter({0: 50, 3: 64, 4: 55})]
    print("PF_BLOCKERS arc_lengths=355,169 arc0_outside=0:109,3:115,4:131 arc1_outside=0:50,3:64,4:55 PASS")
    print("PASS")


if __name__ == "__main__":
    main()
