#!/usr/bin/env python3
"""Independent finite checker for the full-boundary Heawood four-pole.

The certificate consists of one internal labelling for each of the ten
global-S5 orbits of xor-zero ordered four-boundary words.  The checker does
not call SAT, NetworkX, or any project solver.
"""

from __future__ import annotations

from itertools import combinations, permutations, product
import hashlib
import json


GRAPH6 = "KhEGHC@AI?_P"
PORTS = (0, 3, 8, 11)
EDGES = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (0, 5),
    (4, 5),
    (5, 6),
    (2, 7),
    (6, 7),
    (7, 8),
    (4, 9),
    (8, 9),
    (1, 10),
    (9, 10),
    (6, 11),
    (10, 11),
)

# type name | labels on PORTS | labels on EDGES
ROWS = (
    ("AA", "02 02 02 02",
     "01 02 01 12 12 02 01 12 02 01 01 12 12 02 12 01"),
    ("AT2", "02 02 03 03",
     "01 02 03 23 12 02 01 23 03 02 03 23 12 02 13 01"),
    ("AT3", "02 03 02 03",
     "01 02 04 34 12 14 24 24 34 23 13 03 12 01 23 02"),
    ("AT4", "02 03 03 02",
     "01 02 01 13 12 01 02 12 01 02 03 23 12 02 12 01"),
    ("T2T2", "02 02 13 13",
     "01 02 01 12 12 02 01 12 02 01 01 03 12 13 12 23"),
    ("T2T3", "02 03 12 13",
     "01 02 01 13 12 01 02 12 01 02 03 01 12 13 12 23"),
    ("T2T4", "02 03 13 12",
     "01 02 04 34 12 13 23 24 12 14 14 34 12 13 13 23"),
    ("T3T3", "02 13 02 13",
     "01 02 01 03 12 02 01 12 02 01 23 12 12 13 12 23"),
    ("T3T4", "02 13 03 12",
     "01 02 03 01 12 02 01 23 03 02 12 23 12 13 13 23"),
    ("T4T4", "02 13 13 02",
     "01 02 01 03 12 01 02 12 24 14 13 34 12 14 04 24"),
)


def pair(text: str) -> int:
    if len(text) != 2 or not text.isdigit() or text[0] >= text[1]:
        raise AssertionError(f"bad pair token {text!r}")
    value = (1 << int(text[0])) | (1 << int(text[1]))
    if value.bit_count() != 2:
        raise AssertionError(f"bad pair token {text!r}")
    return value


def transform(mask: int, coordinate_permutation: tuple[int, ...]) -> int:
    return sum(
        1 << coordinate_permutation[coordinate]
        for coordinate in range(5)
        if mask & (1 << coordinate)
    )


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    values = [ord(character) - 63 for character in record]
    if not values or not 0 <= values[0] < 63:
        raise AssertionError("checker intentionally expects short graph6")
    order = values[0]
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    required = order * (order - 1) // 2
    if len(bits) < required or any(bits[required:]):
        raise AssertionError("malformed graph6")
    edges = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def graph_metadata() -> dict[str, int | bool]:
    order, parsed_edges = parse_graph6(GRAPH6)
    if order != 12 or parsed_edges != EDGES:
        raise AssertionError("graph6 and frozen edge table disagree")
    adjacency = [[] for _ in range(order)]
    for edge_id, (left, right) in enumerate(EDGES):
        if left == right:
            raise AssertionError("loop")
        adjacency[left].append((right, edge_id))
        adjacency[right].append((left, edge_id))
    if len(set(EDGES)) != len(EDGES):
        raise AssertionError("parallel edge")
    if tuple(vertex for vertex, row in enumerate(adjacency) if len(row) == 2) != PORTS:
        raise AssertionError("wrong ports")
    if any(len(row) not in (2, 3) for row in adjacency):
        raise AssertionError("wrong degree")

    def reached(skipped_edge: int) -> set[int]:
        seen = {0}
        stack = [0]
        while stack:
            vertex = stack.pop()
            for other, edge_id in adjacency[vertex]:
                if edge_id != skipped_edge and other not in seen:
                    seen.add(other)
                    stack.append(other)
        return seen

    if len(reached(-1)) != order:
        raise AssertionError("disconnected core")
    if any(len(reached(edge)) != order for edge in range(len(EDGES))):
        raise AssertionError("core bridge")

    girth = order + 1
    for start in range(order):
        distance = [-1] * order
        parent = [-1] * order
        distance[start] = 0
        queue = [start]
        for vertex in queue:
            for other, _ in adjacency[vertex]:
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    girth = min(girth, distance[vertex] + distance[other] + 1)
    if girth != 6:
        raise AssertionError("unexpected proper-core girth")
    return {
        "order": order,
        "proper_edges": len(EDGES),
        "ports": len(PORTS),
        "simple": True,
        "connected": True,
        "bridgeless": True,
        "girth": girth,
    }


def check_labelling(boundary: tuple[int, ...], internal: tuple[int, ...]) -> None:
    if len(boundary) != 4 or len(internal) != len(EDGES):
        raise AssertionError("wrong certificate row length")
    if any(label.bit_count() != 2 for label in boundary + internal):
        raise AssertionError("label outside D5")
    at_vertex: list[list[int]] = [[] for _ in range(12)]
    for label, (left, right) in zip(internal, EDGES, strict=True):
        at_vertex[left].append(label)
        at_vertex[right].append(label)
    for label, port in zip(boundary, PORTS, strict=True):
        at_vertex[port].append(label)
    if any(len(row) != 3 for row in at_vertex):
        raise AssertionError("completed vertex is not cubic")
    if any(row[0] ^ row[1] ^ row[2] for row in at_vertex):
        raise AssertionError("vertex xor failure")


def main() -> int:
    metadata = graph_metadata()
    certificates = tuple(
        (
            name,
            tuple(pair(token) for token in boundary.split()),
            tuple(pair(token) for token in internal.split()),
        )
        for name, boundary, internal in ROWS
    )
    if len({name for name, _, _ in certificates}) != 10:
        raise AssertionError("duplicate type name")
    for _, boundary, internal in certificates:
        if boundary[0] ^ boundary[1] ^ boundary[2] ^ boundary[3]:
            raise AssertionError("certificate boundary has nonzero xor")
        check_labelling(boundary, internal)

    labels = tuple(
        (1 << left) | (1 << right)
        for left, right in combinations(range(5), 2)
    )
    coordinate_permutations = tuple(permutations(range(5)))
    targets = tuple(
        word
        for word in product(labels, repeat=4)
        if word[0] ^ word[1] ^ word[2] ^ word[3] == 0
    )
    if len(targets) != 640:
        raise AssertionError("unexpected xor-zero boundary count")

    covered_by: dict[tuple[int, ...], str] = {}
    for name, source_boundary, source_internal in certificates:
        for coordinate_permutation in coordinate_permutations:
            boundary = tuple(
                transform(label, coordinate_permutation)
                for label in source_boundary
            )
            internal = tuple(
                transform(label, coordinate_permutation)
                for label in source_internal
            )
            check_labelling(boundary, internal)
            covered_by.setdefault(boundary, name)
    if set(covered_by) != set(targets):
        missing = set(targets) - set(covered_by)
        extra = set(covered_by) - set(targets)
        raise AssertionError(f"orbit coverage mismatch: {missing=} {extra=}")

    orbit_sizes = {
        name: len({
            tuple(transform(label, permutation) for label in boundary)
            for permutation in coordinate_permutations
        })
        for name, boundary, _ in certificates
    }
    if sum(orbit_sizes.values()) != 640:
        raise AssertionError("certificate rows are not ten disjoint orbits")

    certificate_text = "\n".join(
        f"{name}|{' '.join(boundary.split())}|{' '.join(internal.split())}"
        for name, boundary, internal in ROWS
    ).encode("ascii")
    print(
        json.dumps(
            {
                "classification": "EXACT_FINITE_BOUNDARY_THEOREM",
                "graph6": GRAPH6,
                "graph": metadata,
                "certificate_rows": len(certificates),
                "certificate_sha256": hashlib.sha256(certificate_text).hexdigest(),
                "coordinate_permutations": len(coordinate_permutations),
                "xor_zero_boundary_words": len(targets),
                "orbit_sizes": orbit_sizes,
                "all_boundary_words_extend": True,
                "all_internal_vertex_parities_checked": True,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
