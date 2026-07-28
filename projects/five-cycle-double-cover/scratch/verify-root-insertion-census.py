#!/usr/bin/env python3
"""Clean-room replay of the restricted root-insertion census.

This implementation uses Python integer masks and a separately written
recursive perfect-matching predicate.  It does not invoke, parse, or import
the C++ producer.  A row shard can be selected for parallel order-28 replay.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CORPUS = (
    ROOT
    / "search"
    / "focused-theta-choice-through28-20260727"
    / "artifacts"
)


def decode_graph6(text: str, expected_order: int) -> tuple[
    tuple[tuple[int, int], ...],
    tuple[tuple[tuple[int, int], ...], ...],
    tuple[int, ...],
]:
    if not text or ord(text[0]) >= 126:
        raise AssertionError("only short graph6 is accepted")
    order = ord(text[0]) - 63
    if order != expected_order:
        raise AssertionError("graph6 order mismatch")
    stream: list[int] = []
    for character in text[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise AssertionError("bad graph6 character")
        stream.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    cursor = 0
    edges: list[tuple[int, int]] = []
    for high in range(1, order):
        for low in range(high):
            if cursor >= len(stream):
                raise AssertionError("truncated graph6")
            if stream[cursor]:
                edges.append((low, high))
            cursor += 1
    if len(edges) * 2 != 3 * order or len(set(edges)) != len(edges):
        raise AssertionError("not simple cubic-size")
    rows: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    neighbours = [0] * order
    for edge, (u, v) in enumerate(edges):
        rows[u].append((v, edge))
        rows[v].append((u, edge))
        neighbours[u] |= 1 << v
        neighbours[v] |= 1 << u
    if any(len(row) != 3 for row in rows):
        raise AssertionError("not cubic")
    return tuple(edges), tuple(tuple(row) for row in rows), tuple(neighbours)


class Replay:
    def __init__(
        self,
        order: int,
        edges: tuple[tuple[int, int], ...],
        rows: tuple[tuple[tuple[int, int], ...], ...],
        neighbours: tuple[int, ...],
    ) -> None:
        self.order = order
        self.edges = edges
        self.rows = rows
        self.neighbours = neighbours
        self.all_vertices = (1 << order) - 1
        self.edge_by_ends = {
            (min(u, v), max(u, v)): edge
            for edge, (u, v) in enumerate(edges)
        }

        @lru_cache(maxsize=None)
        def matchable(vertices: int) -> bool:
            if vertices == 0:
                return True
            if vertices.bit_count() % 2:
                return False
            candidates = [
                (
                    (neighbours[vertex] & vertices).bit_count(),
                    vertex,
                )
                for vertex in range(order)
                if (vertices >> vertex) & 1
            ]
            degree, vertex = min(candidates)
            if degree == 0:
                return False
            remainder = vertices & ~(1 << vertex)
            available = neighbours[vertex] & remainder
            while available:
                bit = available & -available
                available -= bit
                if matchable(remainder & ~bit):
                    return True
            return False

        self.matchable = matchable

    def singleton_gallai_edmonds(self, h_vertices: int) -> bool:
        d_set = 0
        vertices = [
            vertex
            for vertex in range(self.order)
            if (h_vertices >> vertex) & 1
        ]
        for first_index, first in enumerate(vertices):
            for second in vertices[first_index + 1 :]:
                if self.matchable(
                    h_vertices & ~(1 << first) & ~(1 << second)
                ):
                    d_set |= (1 << first) | (1 << second)
        if any(
            ((d_set >> u) & 1) and ((d_set >> v) & 1)
            for u, v in self.edges
        ):
            return False
        a_set = 0
        remaining_d = d_set
        while remaining_d:
            bit = remaining_d & -remaining_d
            remaining_d -= bit
            vertex = bit.bit_length() - 1
            a_set |= self.neighbours[vertex] & h_vertices & ~d_set
        c_set = h_vertices & ~d_set & ~a_set
        return c_set == 0

    def no_bridge(self, deleted: int) -> bool:
        discovery = [-1] * self.order
        low = [-1] * self.order
        clock = 0
        bridge = False

        def visit(vertex: int, parent_edge: int) -> None:
            nonlocal clock, bridge
            discovery[vertex] = low[vertex] = clock
            clock += 1
            for neighbour, edge in self.rows[vertex]:
                if ((deleted >> edge) & 1) or edge == parent_edge:
                    continue
                if discovery[neighbour] < 0:
                    visit(neighbour, edge)
                    low[vertex] = min(low[vertex], low[neighbour])
                    if low[neighbour] > discovery[vertex]:
                        bridge = True
                else:
                    low[vertex] = min(
                        low[vertex], discovery[neighbour]
                    )

        for vertex in range(self.order):
            if discovery[vertex] < 0:
                visit(vertex, -1)
        return not bridge

    def enumerate_fixed_perfect_matchings(
        self,
        remaining: int,
        chosen: int,
        removed_first: int,
        removed_second: int,
        inserted: int,
    ) -> bool:
        if remaining == 0:
            near_matching = (
                chosen
                & ~(1 << removed_first)
                & ~(1 << removed_second)
            ) | (1 << inserted)
            return self.no_bridge(near_matching)
        choices = [
            (
                (self.neighbours[vertex] & remaining).bit_count(),
                vertex,
            )
            for vertex in range(self.order)
            if (remaining >> vertex) & 1
        ]
        degree, vertex = min(choices)
        if degree == 0:
            return False
        rest = remaining & ~(1 << vertex)
        for neighbour, edge in self.rows[vertex]:
            if not ((rest >> neighbour) & 1):
                continue
            reduced = rest & ~(1 << neighbour)
            if not self.matchable(reduced):
                continue
            if self.enumerate_fixed_perfect_matchings(
                reduced,
                chosen | (1 << edge),
                removed_first,
                removed_second,
                inserted,
            ):
                return True
        return False

    def orientation_witness(self, kept: int, inserted: int) -> bool:
        p, q = self.edges[kept]
        a, b = self.edges[inserted]
        if len({p, q, a, b}) != 4:
            raise AssertionError("roots not independent")
        for x, ax in self.rows[a]:
            if ax == inserted:
                continue
            for y, by in self.rows[b]:
                if by == inserted or x == y:
                    continue
                covered_vertices = {p, q, a, b, x, y}
                if len(covered_vertices) != 6:
                    continue
                covered = sum(1 << vertex for vertex in covered_vertices)
                remaining = self.all_vertices & ~covered
                if not self.matchable(remaining):
                    continue
                fixed = (1 << kept) | (1 << ax) | (1 << by)
                if self.enumerate_fixed_perfect_matchings(
                    remaining, fixed, ax, by, inserted
                ):
                    return True
        return False

    def local_witness(self, first: int, second: int) -> bool:
        return self.orientation_witness(
            first, second
        ) or self.orientation_witness(second, first)


def replay_order(
    order: int, shard: int, shard_count: int
) -> dict[str, object]:
    path = CORPUS / f"cyclic4-nontait-order{order}.g6"
    data = path.read_bytes()
    rows = data.decode("ascii").splitlines()
    answer: dict[str, object] = {
        "order": order,
        "corpus_sha256": hashlib.sha256(data).hexdigest(),
        "source_graphs": len(rows),
        "shard": shard,
        "shard_count": shard_count,
        "graphs": 0,
        "pairs": 0,
        "deficient": 0,
        "local_witness": 0,
        "local_failure": 0,
        "singleton": 0,
        "singleton_local_witness": 0,
        "singleton_local_failure": 0,
        "first_failure": "",
        "first_singleton_failure": "",
    }
    for graph_index, graph6 in enumerate(rows):
        if graph_index % shard_count != shard:
            continue
        edges, adjacency, neighbours = decode_graph6(graph6, order)
        replay = Replay(order, edges, adjacency, neighbours)
        answer["graphs"] += 1
        for first, (a, b) in enumerate(edges):
            for second in range(first + 1, len(edges)):
                c, d = edges[second]
                if len({a, b, c, d}) != 4:
                    continue
                answer["pairs"] += 1
                roots = (1 << a) | (1 << b) | (1 << c) | (1 << d)
                h_vertices = replay.all_vertices & ~roots
                if replay.matchable(h_vertices):
                    continue
                answer["deficient"] += 1
                local = replay.local_witness(first, second)
                if local:
                    answer["local_witness"] += 1
                else:
                    answer["local_failure"] += 1
                    if not answer["first_failure"]:
                        answer["first_failure"] = (
                            f"{graph_index}:{first},{second}:{graph6}"
                        )
                singleton = replay.singleton_gallai_edmonds(h_vertices)
                if singleton:
                    answer["singleton"] += 1
                    if local:
                        answer["singleton_local_witness"] += 1
                    else:
                        answer["singleton_local_failure"] += 1
                        if not answer["first_singleton_failure"]:
                            answer["first_singleton_failure"] = (
                                f"{graph_index}:{first},{second}:{graph6}"
                            )
    return answer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orders",
        nargs="+",
        type=int,
        default=[10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
    )
    parser.add_argument("--shard", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    if not 0 <= arguments.shard < arguments.shard_count:
        raise SystemExit("require 0 <= shard < shard-count")
    results = [
        replay_order(order, arguments.shard, arguments.shard_count)
        for order in arguments.orders
    ]
    text = json.dumps(
        {
            "implementation": "clean-room-python-bitmask-v1",
            "results": results,
        },
        indent=2,
        sort_keys=True,
    ) + "\n"
    if arguments.output:
        arguments.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
