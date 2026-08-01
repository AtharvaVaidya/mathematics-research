#!/usr/bin/env python3
"""Independent shortest-T-join audit of all four exchange conditions.

Unlike verify.py, this checker does not enumerate the base cycle space.
It constructs the 230-vertex inflated graph from the literal TSV and uses
the standard metric-closure dynamic program for a minimum T-join in G-M.
"""

from __future__ import annotations

from collections import deque
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load():
    rows = []
    for raw in (ROOT / "base-edges.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        a, b, colour, kind = raw.split("\t")
        rows.append((int(a), int(b), int(colour), kind))
    return rows


def replacement_colours(terminal):
    rest = [colour for colour in (1, 2, 3) if colour != terminal]
    return [terminal, terminal, terminal, rest[0], rest[0], rest[1], rest[1]]


def construct():
    old = load()
    graph = []
    vertex_count = 42
    for u, v, colour, kind in old:
        if kind == "support":
            graph.append((u, v, colour, True))
            continue
        a, b, c, d = range(vertex_count, vertex_count + 4)
        vertex_count += 4
        pairs = [(u, a), (b, v), (c, d), (a, c), (b, d), (a, d), (b, c)]
        for pair, new_colour in zip(pairs, replacement_colours(colour)):
            graph.append((*pair, new_colour, False))
    assert vertex_count == 230 and len(graph) == 345
    return vertex_count, graph


def distances(vertex_count, graph, deleted, source):
    adjacency = [[] for _ in range(vertex_count)]
    for edge_index, (u, v, _colour, _support) in enumerate(graph):
        if edge_index in deleted:
            continue
        adjacency[u].append(v)
        adjacency[v].append(u)
    result = [-1] * vertex_count
    result[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if result[v] < 0:
                result[v] = result[u] + 1
                queue.append(v)
    assert all(value >= 0 for value in result)
    return result


def minimum_t_join(vertex_count, graph, matching):
    terminals = []
    for edge_index in matching:
        terminals.extend(graph[edge_index][:2])
    metric = []
    for source in terminals:
        row = distances(vertex_count, graph, set(matching), source)
        metric.append([row[target] for target in terminals])

    @lru_cache(maxsize=None)
    def solve(mask):
        if mask == 0:
            return 0
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        answer = 10**9
        candidates = remainder
        while candidates:
            second_bit = candidates & -candidates
            second = second_bit.bit_length() - 1
            answer = min(
                answer,
                metric[first][second] + solve(remainder ^ second_bit),
            )
            candidates ^= second_bit
        return answer

    return solve((1 << len(terminals)) - 1)


def main():
    vertex_count, graph = construct()
    totals = []
    class_sizes = []
    for colour in range(4):
        matching = tuple(
            edge_index
            for edge_index, edge in enumerate(graph)
            if edge[3] and edge[2] == colour
        )
        # The support value classes are matchings, as required by the
        # cycle-containing / T-join equivalence.
        endpoints = [vertex for edge_index in matching for vertex in graph[edge_index][:2]]
        assert len(endpoints) == len(set(endpoints))
        join_size = minimum_t_join(vertex_count, graph, matching)
        class_sizes.append(len(matching))
        totals.append(len(matching) + join_size)
        print(
            f"COLOUR {colour} matching={len(matching)} "
            f"shortest_t_join={join_size} containing_cycle={totals[-1]}"
        )
    assert class_sizes == [6, 5, 3, 2]
    assert totals == [16, 16, 16, 16]
    print(
        "PASS: independent metric-closure T-join audit proves all four "
        "full binary-cycle exchange inequalities"
    )


if __name__ == "__main__":
    main()
