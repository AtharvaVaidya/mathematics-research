#!/usr/bin/env python3
"""Verify the minimum-order full-boundary cube four-pole certificate."""

from itertools import permutations, product


PORTS = (2, 3, 4, 7)
EDGES = (
    (2, 3),
    (2, 6),
    (3, 5),
    (4, 5),
    (4, 7),
    (5, 6),
    (6, 7),
)
ROWS = (
    ("AA", "02 02 02 02", "12 01 01 12 01 02 12"),
    ("AT2", "02 02 03 03", "01 12 12 02 23 01 02"),
    ("AT3", "02 03 02 03", "23 03 02 12 01 01 13"),
    ("AT4", "02 03 03 02", "01 12 13 34 04 14 24"),
    ("T2T2", "02 02 13 13", "24 04 04 14 34 01 14"),
    ("T2T3", "02 03 12 13", "23 03 02 24 14 04 34"),
    ("T2T4", "02 03 13 12", "23 03 02 12 23 01 13"),
    ("T3T3", "02 13 02 13", "03 23 01 12 01 02 03"),
    ("T3T4", "02 13 03 12", "23 03 12 02 23 01 13"),
    ("T4T4", "02 13 13 02", "03 23 01 12 23 02 03"),
)


def label(text: str) -> int:
    assert len(text) == 2 and text[0] < text[1]
    result = (1 << int(text[0])) | (1 << int(text[1]))
    assert result.bit_count() == 2
    return result


LABELS = tuple(
    (1 << first) | (1 << second)
    for first in range(5)
    for second in range(first + 1, 5)
)


def transformed(value: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for old in range(5):
        if (value >> old) & 1:
            result |= 1 << permutation[old]
    return result


def connected(vertices: tuple[int, ...], edges: tuple[tuple[int, int], ...]) -> bool:
    seen = {vertices[0]}
    stack = [vertices[0]]
    adjacency = {vertex: [] for vertex in vertices}
    for first, second in edges:
        adjacency[first].append(second)
        adjacency[second].append(first)
    while stack:
        current = stack.pop()
        for other in adjacency[current]:
            if other not in seen:
                seen.add(other)
                stack.append(other)
    return len(seen) == len(vertices)


def main() -> None:
    vertices = tuple(range(2, 8))
    assert len(set(EDGES)) == len(EDGES)
    assert all(first < second for first, second in EDGES)
    assert connected(vertices, EDGES)
    degrees = {vertex: 0 for vertex in vertices}
    for first, second in EDGES:
        degrees[first] += 1
        degrees[second] += 1
    assert tuple(degrees[vertex] for vertex in PORTS) == (2, 2, 2, 2)
    assert degrees[5] == degrees[6] == 3
    for removed in range(len(EDGES)):
        assert connected(vertices, EDGES[:removed] + EDGES[removed + 1 :])

    admissible = {
        word
        for word in product(LABELS, repeat=4)
        if word[0] ^ word[1] ^ word[2] ^ word[3] == 0
    }
    assert len(admissible) == 640

    covered: set[tuple[int, int, int, int]] = set()
    orbit_sizes: dict[str, int] = {}
    for name, boundary_text, internal_text in ROWS:
        boundary = tuple(label(item) for item in boundary_text.split())
        internal = tuple(label(item) for item in internal_text.split())
        assert len(boundary) == 4 and len(internal) == len(EDGES)

        incident_xor = {vertex: 0 for vertex in vertices}
        for (first, second), value in zip(EDGES, internal):
            incident_xor[first] ^= value
            incident_xor[second] ^= value
        for port, value in zip(PORTS, boundary):
            incident_xor[port] ^= value
        assert all(value == 0 for value in incident_xor.values())

        orbit = {
            tuple(transformed(value, permutation) for value in boundary)
            for permutation in permutations(range(5))
        }
        orbit_sizes[name] = len(orbit)
        covered.update(orbit)

    assert orbit_sizes == {
        "AA": 10,
        "AT2": 60,
        "AT3": 60,
        "AT4": 60,
        "T2T2": 30,
        "T2T3": 120,
        "T2T4": 120,
        "T3T3": 30,
        "T3T4": 120,
        "T4T4": 30,
    }
    assert covered == admissible

    # A connected simple terminal-distinct cubic four-pole has at least
    # four vertices.  If it has four, all four vertices are ports of degree
    # two, hence its core is C4.  The K3,3 checker proves that C4 is not full.
    assert len(vertices) == 6

    print("PASS minimum-order cube four-pole full-boundary theorem")
    print("proper vertices: 6; proper edges: 7; ports: 4")
    print("simple, connected, bridgeless: true")
    print("certificate rows: 10")
    print("xor-zero boundary words covered: 640")
    print(f"orbit sizes: {orbit_sizes}")


if __name__ == "__main__":
    main()
