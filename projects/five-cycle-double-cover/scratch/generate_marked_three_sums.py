#!/usr/bin/env python3
"""Generate the frozen 13,824 marked three-edge-sum stress instances.

Each row is a vertex three-sum of two copies of one order-20 cubic core.
Two of the core's three distinguished matching edges are retained on
each side.  The four retained marks are relabelled to the fixed endpoint
pairs 0-1, 2-3, 4-5, and 6-7 so that the C++ marked-core checker can read
the graph6 stream without a side channel.

The stream is deliberately not quotient by isomorphism.  Its purpose is
to make one structured finite test exactly reproducible.
"""

from __future__ import annotations

import itertools
import sys

import networkx as nx


BASE_GRAPH6 = "S????A?O@?R?d?EGGSAK?H_?HG?Ao@A_?"
BASE_MARKS = ((3, 11), (6, 15), (7, 18))
FIXED_MARKS = ((0, 1), (2, 3), (4, 5), (6, 7))


def normalized_graph6(
    graph: nx.Graph, retained_marks: tuple[tuple[object, object], ...]
) -> str:
    """Relabel four disjoint retained marks to FIXED_MARKS."""

    mapping: dict[object, int] = {}
    for source_edge, target_edge in zip(
        retained_marks, FIXED_MARKS, strict=True
    ):
        for source, target in zip(source_edge, target_edge, strict=True):
            if source in mapping:
                raise AssertionError("retained marks are not a matching")
            mapping[source] = target

    next_label = 2 * len(FIXED_MARKS)
    for vertex in sorted(graph, key=repr):
        if vertex not in mapping:
            mapping[vertex] = next_label
            next_label += 1

    normalized = nx.Graph()
    normalized.add_nodes_from(range(len(graph)))
    normalized.add_edges_from(
        sorted(
            (min(mapping[u], mapping[v]), max(mapping[u], mapping[v]))
            for u, v in graph.edges()
        )
    )
    if sorted(dict(normalized.degree()).values()) != [3] * len(normalized):
        raise AssertionError("three-sum output is not cubic")
    if not nx.is_connected(normalized):
        raise AssertionError("three-sum output is disconnected")
    if len(normalized) != 38 or normalized.number_of_edges() != 57:
        raise AssertionError("unexpected three-sum size")
    for edge in FIXED_MARKS:
        if not normalized.has_edge(*edge):
            raise AssertionError(f"fixed marked edge {edge} is absent")
    return nx.to_graph6_bytes(normalized, header=False).decode().strip()


def rows():
    base = nx.from_graph6_bytes(BASE_GRAPH6.encode())
    if len(base) != 20 or base.number_of_edges() != 30:
        raise AssertionError("unexpected base size")
    if sorted(dict(base.degree()).values()) != [3] * len(base):
        raise AssertionError("base is not cubic")
    for mark in BASE_MARKS:
        if not base.has_edge(*mark):
            raise AssertionError(f"base mark {mark} is absent")

    mark_pairs = tuple(itertools.combinations(BASE_MARKS, 2))
    for left_marks in mark_pairs:
        forbidden_left = set(itertools.chain.from_iterable(left_marks))
        deleted_left = sorted(set(base) - forbidden_left)
        for right_marks in mark_pairs:
            forbidden_right = set(itertools.chain.from_iterable(right_marks))
            deleted_right = sorted(set(base) - forbidden_right)
            for left_vertex in deleted_left:
                left_neighbours = sorted(base.neighbors(left_vertex))
                for right_vertex in deleted_right:
                    right_neighbours = sorted(base.neighbors(right_vertex))
                    for right_order in itertools.permutations(right_neighbours):
                        graph = nx.Graph()
                        graph.add_nodes_from(
                            ("L", vertex)
                            for vertex in base
                            if vertex != left_vertex
                        )
                        graph.add_nodes_from(
                            ("R", vertex)
                            for vertex in base
                            if vertex != right_vertex
                        )
                        graph.add_edges_from(
                            (("L", u), ("L", v))
                            for u, v in base.edges()
                            if left_vertex not in (u, v)
                        )
                        graph.add_edges_from(
                            (("R", u), ("R", v))
                            for u, v in base.edges()
                            if right_vertex not in (u, v)
                        )
                        graph.add_edges_from(
                            (("L", u), ("R", v))
                            for u, v in zip(
                                left_neighbours, right_order, strict=True
                            )
                        )
                        retained = tuple(
                            (("L", u), ("L", v)) for u, v in left_marks
                        ) + tuple(
                            (("R", u), ("R", v)) for u, v in right_marks
                        )
                        yield normalized_graph6(graph, retained)


def main() -> int:
    count = 0
    for row in rows():
        print(row)
        count += 1
    if count != 13_824:
        raise AssertionError(f"expected 13,824 rows, generated {count}")
    print(f"generated={count}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
