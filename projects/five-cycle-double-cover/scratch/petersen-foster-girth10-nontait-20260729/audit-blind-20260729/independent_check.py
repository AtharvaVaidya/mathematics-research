#!/usr/bin/env python3
"""Blind audit of the Petersen--Foster reconfiguration certificate.

This deliberately imports none of the candidate checker code.  In particular,
the short-path audit obtains all preimages of each edge difference by direct
enumeration, rather than using the candidate's chosen right inverse.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import product
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent
CERTIFICATE = SOURCE / "reconfiguration-certificate.json"
LABELS = SOURCE / "fivecdc-labels.txt"

FOSTER_LCF = (17, -9, 37, -37, 9, -17) * 15
PETERSEN_EDGES = (
    (0, 1), (1, 2), (2, 3), (0, 4), (3, 4),
    (0, 5), (1, 6), (2, 7), (5, 7), (3, 8),
    (5, 8), (6, 8), (4, 9), (6, 9), (7, 9),
)
PORTS = (1, 17, 89)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph_edges() -> tuple[tuple[int, int], ...]:
    foster: set[tuple[int, int]] = set()
    for vertex, jump in enumerate(FOSTER_LCF):
        for neighbour in ((vertex + 1) % 90, (vertex + jump) % 90):
            foster.add(tuple(sorted((vertex, neighbour))))
    assert len(foster) == 135

    answer: set[tuple[int, int]] = set()
    for copy in range(10):
        for left, right in foster:
            if 0 not in (left, right):
                answer.add(tuple(sorted((
                    89 * copy + left - 1,
                    89 * copy + right - 1,
                ))))
    used = [0] * 10
    for left_copy, right_copy in PETERSEN_EDGES:
        left_port = PORTS[used[left_copy]]
        right_port = PORTS[used[right_copy]]
        used[left_copy] += 1
        used[right_copy] += 1
        answer.add(tuple(sorted((
            89 * left_copy + left_port - 1,
            89 * right_copy + right_port - 1,
        ))))
    assert used == [3] * 10
    assert len(answer) == 1335
    return tuple(
        (left, right)
        for right in range(1, 890)
        for left in range(right)
        if (left, right) in answer
    )


def graph6(order: int, edges: tuple[tuple[int, int], ...]) -> str:
    edge_set = set(edges)
    header = [
        126,
        63 + ((order >> 12) & 63),
        63 + ((order >> 6) & 63),
        63 + (order & 63),
    ]
    bits = [
        int((left, right) in edge_set)
        for right in range(1, order)
        for left in range(right)
    ]
    bits += [0] * (-len(bits) % 6)
    body = [
        63 + sum(bits[offset + bit] << (5 - bit) for bit in range(6))
        for offset in range(0, len(bits), 6)
    ]
    return "".join(map(chr, header + body))


def rows_for(
    order: int, edges: tuple[tuple[int, int], ...]
) -> list[list[int]]:
    rows = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return rows


def rank(values: tuple[int, ...] | set[int]) -> int:
    pivots: dict[int, int] = {}
    for original in values:
        value = original
        while value:
            bit = value.bit_length() - 1
            if bit not in pivots:
                pivots[bit] = value
                break
            value ^= pivots[bit]
    return len(pivots)


def image(constants: tuple[int, ...], mask: int) -> int:
    answer = 0
    for position, constant in enumerate(constants):
        if (mask >> position) & 1:
            answer ^= constant
    return answer


def legal_word(start: int, constants: tuple[int, ...], mask: int) -> bool:
    value = start
    for position, constant in enumerate(constants):
        if (mask >> position) & 1:
            value ^= constant
        if value == 0:
            return False
    return True


def flow_ok(flow: tuple[int, ...], rows: list[list[int]]) -> bool:
    return (
        len(flow) == 1335
        and all(value in range(1, 8) for value in flow)
        and all(
            flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0
            for row in rows
        )
    )


def tree_ok(
    edges: tuple[tuple[int, int], ...], chosen: set[int]
) -> bool:
    if len(chosen) != 889:
        return False
    parent = list(range(890))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in chosen:
        left, right = edges[edge]
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            return False
        parent[right_root] = left_root
    return True


def odd_kernel(
    edges: tuple[tuple[int, int], ...], tree: set[int]
) -> frozenset[int]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(890)]
    for edge in tree:
        left, right = edges[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    parent = [-1] * 890
    parent[0] = 0
    parent_edge = [-1] * 890
    order = [0]
    for vertex in order:
        for neighbour, edge in adjacency[vertex]:
            if parent[neighbour] == -1:
                parent[neighbour] = vertex
                parent_edge[neighbour] = edge
                order.append(neighbour)
    assert len(order) == 890
    subtree = [1] * 890
    answer: set[int] = set()
    for vertex in reversed(order[1:]):
        if subtree[vertex] & 1:
            answer.add(parent_edge[vertex])
        subtree[parent[vertex]] += subtree[vertex]
    return frozenset(answer)


def component_parity_feasible(
    edges: tuple[tuple[int, int], ...],
    demand: list[int],
    domains: list[int],
) -> bool:
    """Solve B*x=demand, with 1/2/3 denoting {0}/{1}/{0,1}."""
    residual = demand[:]
    adjacency = [[] for _ in range(890)]
    for edge, domain in enumerate(domains):
        left, right = edges[edge]
        if domain == 2:
            residual[left] ^= 1
            residual[right] ^= 1
        elif domain == 3:
            adjacency[left].append(right)
            adjacency[right].append(left)
        else:
            assert domain == 1
    unseen = set(range(890))
    while unseen:
        root = min(unseen)
        component = {root}
        queue = [root]
        while queue:
            vertex = queue.pop()
            for neighbour in adjacency[vertex]:
                if neighbour not in component:
                    component.add(neighbour)
                    queue.append(neighbour)
        if sum(residual[vertex] for vertex in component) & 1:
            return False
        unseen -= component
    return True


def short_paths(
    edges: tuple[tuple[int, int], ...],
    rows: list[list[int]],
    start: tuple[int, ...],
    target: tuple[int, ...],
) -> dict[str, int]:
    difference = tuple(a ^ b for a, b in zip(start, target))
    assert rank(set(difference)) == 3

    triples = legal_triples = 0
    for constants in product(range(1, 8), repeat=3):
        if rank(constants) != 3:
            continue
        triples += 1
        preimage = {
            value: next(mask for mask in range(8)
                        if image(constants, mask) == value)
            for value in range(8)
        }
        words = [preimage[value] for value in difference]
        assert all(
            sum((words[edge] >> move) & 1 for edge in row) % 2 == 0
            for row in rows for move in range(3)
        )
        legal_triples += all(
            legal_word(start[edge], constants, words[edge])
            for edge in range(len(edges))
        )

    quads = local_blocked = parity_blocked = legal_quads = 0
    for constants in product(range(1, 8), repeat=4):
        if rank(constants) != 3:
            continue
        quads += 1
        dependency = next(
            mask for mask in range(1, 16)
            if image(constants, mask) == 0
        )
        assert sum(
            image(constants, mask) == 0 for mask in range(1, 16)
        ) == 1

        bases: list[int] = []
        domains: list[int] = []
        impossible = False
        for edge, delta in enumerate(difference):
            preimages = [
                mask for mask in range(16)
                if image(constants, mask) == delta
            ]
            assert len(preimages) == 2
            base = min(preimages)
            assert set(preimages) == {base, base ^ dependency}
            bases.append(base)
            domain = 0
            if legal_word(start[edge], constants, base):
                domain |= 1
            if legal_word(start[edge], constants, base ^ dependency):
                domain |= 2
            if domain == 0:
                impossible = True
                break
            domains.append(domain)
        if impossible:
            local_blocked += 1
            continue

        demands = []
        for row in rows:
            parity_vector = 0
            for edge in row:
                parity_vector ^= bases[edge]
            assert parity_vector in (0, dependency)
            demands.append(int(parity_vector == dependency))
        if component_parity_feasible(edges, demands, domains):
            legal_quads += 1
        else:
            parity_blocked += 1

    return {
        "triples": triples,
        "legal_triples": legal_triples,
        "quads": quads,
        "local_blocked": local_blocked,
        "parity_blocked": parity_blocked,
        "legal_quads": legal_quads,
    }


def support_cycle_lengths(
    edges: tuple[tuple[int, int], ...], support: set[int]
) -> list[int]:
    adjacency: dict[int, list[tuple[int, int]]] = {}
    for edge in support:
        left, right = edges[edge]
        adjacency.setdefault(left, []).append((right, edge))
        adjacency.setdefault(right, []).append((left, edge))
    assert all(len(row) == 2 for row in adjacency.values())
    unseen = set(support)
    lengths = []
    while unseen:
        first = min(unseen)
        component_edges = {first}
        left, right = edges[first]
        queue = deque((left, right))
        vertices = {left, right}
        while queue:
            vertex = queue.popleft()
            for neighbour, edge in adjacency[vertex]:
                component_edges.add(edge)
                if neighbour not in vertices:
                    vertices.add(neighbour)
                    queue.append(neighbour)
        assert len(component_edges) == len(vertices)
        unseen -= component_edges
        lengths.append(len(component_edges))
    return sorted(lengths)


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text())
    edges = graph_edges()
    rows = rows_for(890, edges)
    assert len(edges) == 1335 and all(len(row) == 3 for row in rows)
    graph6_digest = hashlib.sha256(
        (graph6(890, edges) + "\n").encode()
    ).hexdigest()
    assert graph6_digest == (
        "c89a74ee736367cb6571600ee748f68e4eb4667787f57b1c05ccba6ee49cbd47"
    )
    assert digest(LABELS) == (
        "441f2c328ff9631c3a7c9fe48ef39c6b029297a66676d7214131671dfc72b863"
    )

    state = tuple(map(int, payload["jaeger_state_digits"]))
    internal = [
        edge for edge, endpoints in enumerate(edges)
        if 0 not in endpoints
    ]
    spokes = rows[0]
    assert len(state) == len(internal) == 1332
    assert Counter(state) == {0: 444, 1: 444, 2: 444}
    trees = [
        {spokes[coordinate]} | {
            internal[local] for local, label in enumerate(state)
            if label != coordinate
        }
        for coordinate in range(3)
    ]
    assert all(tree_ok(edges, tree) for tree in trees)
    kernels = [odd_kernel(edges, tree) for tree in trees]
    assert tuple(map(len, kernels)) == (506, 507, 526)
    start = tuple(
        sum(
            1 << coordinate for coordinate in range(3)
            if edge not in kernels[coordinate]
        )
        for edge in range(1335)
    )
    assert start == tuple(map(int, payload["bad_flow_digits"]))
    assert flow_ok(start, rows)

    masks = tuple(map(int, LABELS.read_text().split()))
    assert len(masks) == 1335
    assert all(mask.bit_count() == 2 and 0 < mask < 32 for mask in masks)
    vertex_parity = [0] * 890
    for edge, (left, right) in enumerate(edges):
        vertex_parity[left] ^= masks[edge]
        vertex_parity[right] ^= masks[edge]
    assert vertex_parity == [0] * 890

    points = payload["good_point_assignment"]
    assert len(points) == len(set(points)) == 5
    target_values = []
    for mask in masks:
        pair = [bit for bit in range(5) if (mask >> bit) & 1]
        target_values.append(points[pair[0]] ^ points[pair[1]])
    target = tuple(target_values)
    assert flow_ok(target, rows)

    paths = short_paths(edges, rows, start, target)
    assert paths == {
        "triples": 168,
        "legal_triples": 0,
        "quads": 1848,
        "local_blocked": 1176,
        "parity_blocked": 672,
        "legal_quads": 0,
    }

    constants = tuple(payload["legal_path_constants"])
    support_masks = [
        int(text, 16) for text in payload["legal_path_support_masks_hex"]
    ]
    current = list(start)
    cycle_lengths = []
    for constant, mask in zip(constants, support_masks):
        assert mask >> 1335 == 0
        support = {
            edge for edge in range(1335) if (mask >> edge) & 1
        }
        assert all(
            sum(edge in support for edge in row) % 2 == 0
            for row in rows
        )
        assert all(current[edge] != constant for edge in support)
        cycle_lengths.append(support_cycle_lengths(edges, support))
        for edge in support:
            current[edge] ^= constant
        assert flow_ok(tuple(current), rows)
    assert tuple(current) == target
    assert [sum(lengths) for lengths in cycle_lengths] == [
        566, 608, 565, 610, 604,
    ]
    assert [len(lengths) for lengths in cycle_lengths] == [14, 11, 10, 14, 14]

    print(json.dumps({
        "classification": "BLIND_AUDIT_PASS",
        "certificate_sha256": digest(CERTIFICATE),
        "labels_sha256": digest(LABELS),
        "graph6_sha256_with_newline": graph6_digest,
        "kernel_sizes": list(map(len, kernels)),
        "short_paths": paths,
        "five_path_constants": list(constants),
        "five_path_support_sizes": [
            sum(lengths) for lengths in cycle_lengths
        ],
        "five_path_component_counts": [
            len(lengths) for lengths in cycle_lengths
        ],
        "total_connected_cycle_moves": sum(map(len, cycle_lengths)),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
