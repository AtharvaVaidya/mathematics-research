#!/usr/bin/env python3
"""Reproduce the exact small-order host census with nauty-geng.

This optional audit needs `geng` on PATH.  It independently generates every
connected simple cubic graph through order 16, tests Tait colourability by
perfect-matching/two-factor enumeration, and tests cyclic edge connectivity
by deleting every set of at most three edges.
"""

from __future__ import annotations

from itertools import combinations
import shutil
import subprocess


def decode_graph6(record):
    n = ord(record[0]) - 63
    bits = tuple(
        (ord(character) - 63 >> shift) & 1
        for character in record[1:]
        for shift in range(5, -1, -1)
    )
    pairs = tuple((u, v) for v in range(1, n) for u in range(v))
    return n, tuple(pair for pair, bit in zip(pairs, bits) if bit)


class CubicGraph:
    def __init__(self, record):
        self.record = record
        self.n, self.edges = decode_graph6(record)
        self.m = len(self.edges)
        rows = [[] for _ in range(self.n)]
        for edge, (u, v) in enumerate(self.edges):
            rows[u].append(edge)
            rows[v].append(edge)
        self.rows = tuple(tuple(row) for row in rows)
        assert self.m * 2 == self.n * 3 and all(len(row) == 3 for row in self.rows)

    def components_after_deleting(self, deleted):
        unseen = set(range(self.n))
        answer = []
        while unseen:
            root = min(unseen)
            unseen.remove(root)
            vertices = {root}
            queue = [root]
            internal_edges_twice = 0
            for vertex in queue:
                for edge in self.rows[vertex]:
                    if edge in deleted:
                        continue
                    internal_edges_twice += 1
                    u, v = self.edges[edge]
                    other = u ^ v ^ vertex
                    if other in unseen:
                        unseen.remove(other)
                        vertices.add(other)
                        queue.append(other)
            answer.append((frozenset(vertices), internal_edges_twice // 2))
        return tuple(answer)

    def is_cyclically_four(self):
        for size in (1, 2, 3):
            for deleted in combinations(range(self.m), size):
                components = self.components_after_deleting(frozenset(deleted))
                cyclic = sum(edge_count >= len(vertices) for vertices, edge_count in components)
                if cyclic >= 2:
                    return False
        return True

    def has_even_two_factor(self, matching):
        two_factor = ((1 << self.m) - 1) ^ matching
        unseen = set(range(self.n))
        while unseen:
            root = min(unseen)
            unseen.remove(root)
            previous = -1
            vertex = root
            length = 1
            while True:
                next_vertices = []
                for edge in self.rows[vertex]:
                    if not ((two_factor >> edge) & 1):
                        continue
                    u, v = self.edges[edge]
                    other = u ^ v ^ vertex
                    if other != previous:
                        next_vertices.append(other)
                assert next_vertices
                other = next_vertices[0]
                if other == root:
                    break
                assert other in unseen
                unseen.remove(other)
                length += 1
                previous, vertex = vertex, other
            if length & 1:
                return False
        return True

    def is_tait(self):
        edge_of = {}
        neighbours = [[] for _ in range(self.n)]
        for edge, (u, v) in enumerate(self.edges):
            edge_of[u, v] = edge_of[v, u] = edge
            neighbours[u].append(v)
            neighbours[v].append(u)

        def recurse(unmatched, selected):
            if not unmatched:
                return self.has_even_two_factor(selected)
            vertex = (unmatched & -unmatched).bit_length() - 1
            rest = unmatched ^ (1 << vertex)
            for other in neighbours[vertex]:
                if (rest >> other) & 1 and recurse(
                    rest ^ (1 << other), selected | (1 << edge_of[vertex, other])
                ):
                    return True
            return False

        return recurse((1 << self.n) - 1, 0)


def records(geng, order):
    result = subprocess.run(
        (geng, "-cq", "-d3", "-D3", str(order)),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return tuple(line for line in result.stdout.splitlines() if line)


def main():
    geng = shutil.which("geng")
    if geng is None:
        raise SystemExit("SKIP: geng is not installed or not on PATH")
    totals = {}
    qualifying = []
    for order in range(4, 18, 2):
        generated = records(geng, order)
        non_tait = []
        cyclic_four_non_tait = []
        for record in generated:
            graph = CubicGraph(record)
            if not graph.is_tait():
                non_tait.append(record)
                if graph.is_cyclically_four():
                    cyclic_four_non_tait.append(record)
        totals[order] = (len(generated), len(non_tait), len(cyclic_four_non_tait))
        qualifying.extend((order, record) for record in cyclic_four_non_tait)
        print(
            f"order={order} connected_cubic={len(generated)} "
            f"non_tait={len(non_tait)} cyclically4_non_tait={len(cyclic_four_non_tait)}"
        )
    print(f"qualifying={qualifying}")
    assert len(qualifying) == 1 and qualifying[0][0] == 10
    assert totals == {
        4: (1, 0, 0),
        6: (2, 0, 0),
        8: (5, 0, 0),
        10: (19, 2, 1),
        12: (85, 5, 0),
        14: (509, 34, 0),
        16: (4060, 212, 0),
    }
    print("CERTIFIED: Petersen is the only cyclically-4 non-Tait simple cubic graph below order 18")


if __name__ == "__main__":
    main()
