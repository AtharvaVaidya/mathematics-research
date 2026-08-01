#!/usr/bin/env python3
"""Independent verifier for the 16-vertex kernel-closure no-go.

This checker does not import the CNF producer or the C++ discovery program.
It verifies the literal graph, its connectivity hypotheses, two independent
LRAT-checker results, and a separate exact component-parity/support-five
witness in the same star fibre.
"""

from __future__ import annotations

from collections import defaultdict, deque
import hashlib
from pathlib import Path
import subprocess


ROOT_DIR = Path(__file__).resolve().parent.parent
PACKAGE = (
    ROOT_DIR / "output" / "jaeger-star-kernel-closure-countermodel-16v"
)
GRAPH6 = "O??CA?_ceOGgH_F?AK@P?"
ORDER = 16
ROOT_VERTEX = 13
EDGES = (
    (0, 6), (0, 9), (0, 10),
    (1, 7), (1, 10), (1, 11),
    (2, 8), (2, 12), (2, 15),
    (3, 9), (3, 13), (3, 14),
    (4, 10), (4, 13), (4, 15),
    (5, 11), (5, 12), (5, 13),
    (6, 9), (6, 12),
    (7, 11), (7, 14),
    (8, 14), (8, 15),
)
STAR = (10, 13, 17)

# This witness was produced by a different five-support search encoding.
# Edge indices use the literal EDGES order above.
TREES = (
    (0, 2, 3, 8, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 23),
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 16, 17, 19, 22),
    (1, 4, 5, 6, 7, 9, 10, 11, 14, 15, 18, 20, 21, 22, 23),
)
FLOW = (
    6, 3, 5, 4, 1, 5, 7, 3, 4, 1, 3, 2,
    4, 6, 2, 2, 7, 5, 2, 4, 7, 3, 1, 6,
)
PAIR_LABELS = (
    (0, 6), (5, 6), (0, 5), (0, 4), (4, 5), (0, 5),
    (0, 7), (4, 7), (0, 4), (4, 5), (5, 6), (4, 6),
    (0, 4), (0, 6), (4, 6), (5, 7), (0, 7), (0, 5),
    (4, 6), (0, 4), (0, 7), (4, 7), (6, 7), (0, 6),
)
EXPECTED_SHA256 = {
    "star-kernel-closure.cnf":
        "ccd8ef9504ef725dc02be9234992cbc9e238f1c12ed39ad3068645c73e3c5baf",
    "star-kernel-closure.lrat":
        "ffcd95bc48db7c5be222e05b86aa72cf0828ef01e45e7cf45e9a92cab76aa3a5",
}


def parse_short_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    order = ord(record[0]) - 63
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    cursor = 0
    edges = []
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def incidence() -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(ORDER)]
    for edge, (left, right) in enumerate(EDGES):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


INCIDENCE = incidence()


def connected(
    deleted_edges: frozenset[int] = frozenset(),
    deleted_vertices: frozenset[int] = frozenset(),
) -> bool:
    vertices = [v for v in range(ORDER) if v not in deleted_vertices]
    if not vertices:
        return True
    seen = {vertices[0]}
    queue = deque(seen)
    while queue:
        vertex = queue.popleft()
        for edge in INCIDENCE[vertex]:
            if edge in deleted_edges:
                continue
            left, right = EDGES[edge]
            if left in deleted_vertices or right in deleted_vertices:
                continue
            other = right if left == vertex else left
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return len(seen) == len(vertices)


def is_tree(tree: set[int]) -> bool:
    return len(tree) == ORDER - 1 and connected(
        frozenset(set(range(len(EDGES))) - tree)
    )


def odd_kernel(tree: set[int]) -> set[int]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(ORDER)]
    for edge in tree:
        left, right = EDGES[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    parent = [-2] * ORDER
    parent_edge = [-1] * ORDER
    parent[0] = -1
    order = [0]
    for vertex in order:
        for other, edge in adjacency[vertex]:
            if parent[other] == -2:
                parent[other] = vertex
                parent_edge[other] = edge
                order.append(other)
    assert len(order) == ORDER
    size = [1] * ORDER
    kernel: set[int] = set()
    for vertex in reversed(order[1:]):
        if size[vertex] % 2:
            kernel.add(parent_edge[vertex])
        size[parent[vertex]] += size[vertex]
    assert kernel <= tree
    assert all(
        sum(edge in kernel for edge in INCIDENCE[vertex]) % 2 == 1
        for vertex in range(ORDER)
    )
    return kernel


def component_map(forest: set[int]) -> tuple[int, ...]:
    parent = list(range(ORDER))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in forest:
        left, right = EDGES[edge]
        a, b = find(left), find(right)
        assert a != b
        parent[a] = b
    return tuple(find(vertex) for vertex in range(ORDER))


def closure_good(kernels: tuple[set[int], ...], coordinate: int) -> bool:
    first, second = (index for index in range(3) if index != coordinate)
    common = kernels[first] & kernels[second]
    component = component_map(kernels[coordinate])
    return all(
        component[left] == component[right]
        for edge, (left, right) in enumerate(EDGES)
        if edge in common
    )


def component_parity_good(
    kernels: tuple[set[int], ...], coordinate: int
) -> bool:
    first, second = (index for index in range(3) if index != coordinate)
    common = kernels[first] & kernels[second]
    component = component_map(kernels[coordinate])
    boundary: dict[int, int] = defaultdict(int)
    for edge in common:
        left, right = EDGES[edge]
        a, b = component[left], component[right]
        if a != b:
            boundary[a] ^= 1
            boundary[b] ^= 1
    return not any(boundary.values())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    order, column_major_edges = parse_short_graph6(GRAPH6)
    assert order == ORDER
    assert frozenset(column_major_edges) == frozenset(EDGES)
    assert len(EDGES) == 24
    assert len({frozenset(edge) for edge in EDGES}) == len(EDGES)
    assert all(left != right for left, right in EDGES)
    assert all(len(row) == 3 for row in INCIDENCE)
    assert tuple(INCIDENCE[ROOT_VERTEX]) == STAR
    assert connected()
    assert all(
        connected(frozenset(deleted))
        for size in (1, 2)
        for deleted in __import__("itertools").combinations(
            range(len(EDGES)), size
        )
    )
    assert all(
        connected(deleted_vertices=frozenset(deleted))
        for size in (1, 2)
        for deleted in __import__("itertools").combinations(
            range(ORDER), size
        )
    )

    for name, expected in EXPECTED_SHA256.items():
        assert expected != "TO_BE_FILLED"
        assert digest(PACKAGE / name) == expected

    cnf = PACKAGE / "star-kernel-closure.cnf"
    lrat = PACKAGE / "star-kernel-closure.lrat"
    lrat_check = (
        ROOT_DIR / ".tools" / "cert-checkers" / "drat-trim" / "lrat-check"
    )
    cake_lpr = (
        ROOT_DIR / ".tools" / "cert-checkers" / "cake_lpr" / "cake_lpr"
    )
    checked = subprocess.run(
        [str(lrat_check), str(cnf), str(lrat)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "c VERIFIED" in checked.stdout
    checked_cake = subprocess.run(
        [str(cake_lpr), str(cnf), str(lrat)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "s VERIFIED UNSAT" in checked_cake.stdout

    trees = tuple(set(tree) for tree in TREES)
    assert all(is_tree(tree) for tree in trees)
    for edge in range(len(EDGES)):
        expected = 1 if edge in STAR else 2
        assert sum(edge in tree for tree in trees) == expected
    kernels = tuple(odd_kernel(tree) for tree in trees)

    # This particular packing fails the closure strengthening in all three
    # coordinates but passes the exact parity criterion in coordinate 2.
    assert not any(
        closure_good(kernels, coordinate) for coordinate in range(3)
    )
    assert tuple(
        component_parity_good(kernels, coordinate)
        for coordinate in range(3)
    ) == (False, False, True)

    completions = tuple(
        set(range(len(EDGES))) - kernel for kernel in kernels
    )
    computed_flow = tuple(
        sum(
            (edge in completions[coordinate]) << coordinate
            for coordinate in range(3)
        )
        for edge in range(len(EDGES))
    )
    assert computed_flow == FLOW
    assert all(flow != 0 for flow in FLOW)
    assert all(
        first < second and first ^ second == FLOW[edge]
        for edge, (first, second) in enumerate(PAIR_LABELS)
    )
    assert {point for pair in PAIR_LABELS for point in pair} == {
        0, 4, 5, 6, 7
    }
    for vertex in range(ORDER):
        for point in range(8):
            assert (
                sum(
                    point in PAIR_LABELS[edge]
                    for edge in INCIDENCE[vertex]
                )
                % 2
                == 0
            )

    print("PASS")
    print(
        "graph6=O??CA?_ceOGgH_F?AK@P?; n=16 m=24; "
        "simple cubic 3-edge-connected and 3-vertex-connected"
    )
    print("root=13; star_edges=10,13,17")
    print(
        "kernel-closure formula=UNSAT; LRAT accepted by lrat-check "
        "and CakeML cake_lpr"
    )
    print(
        "independent witness=exact component parity and five-point "
        "support pass; closure strengthening only is refuted"
    )


if __name__ == "__main__":
    main()
