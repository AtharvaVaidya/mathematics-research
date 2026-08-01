#!/usr/bin/env python3
"""Exact bounded search for incompatible realizable cut signatures.

Requires Brendan McKay's ``geng``.  The scope is every connected shore of
every nontrivial 2/3-edge cut in the complete biconnected simple cubic census
at orders 8 and 10, every separated proper root/cap marker, and all six
ordered 3-cut normalizations.
"""

from __future__ import annotations

import importlib.util
from itertools import combinations, permutations
from pathlib import Path
import shutil
import subprocess
import sys


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("cut_join_verify", HERE / "verify.py")
assert SPEC is not None and SPEC.loader is not None
V = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = V
SPEC.loader.exec_module(V)


def graph_rows(geng: str, order: int) -> tuple[str, ...]:
    process = subprocess.run(
        (geng, "-Cq", "-d3", "-D3", str(order)),
        check=True,
        text=True,
        capture_output=True,
    )
    return tuple(row for row in process.stdout.splitlines()
                 if row and not row.startswith(">"))


def shore_connected(
    shore: frozenset[int],
    edges: tuple[tuple[int, int], ...],
    cut: tuple[int, ...],
) -> bool:
    start = next(iter(shore))
    seen, todo = {start}, [start]
    while todo:
        vertex = todo.pop()
        for edge, (left, right) in enumerate(edges):
            if edge in cut:
                continue
            if left == vertex and right in shore and right not in seen:
                seen.add(right)
                todo.append(right)
            elif right == vertex and left in shore and left not in seen:
                seen.add(left)
                todo.append(left)
    return seen == set(shore)


def cuts(
    n: int,
    edges: tuple[tuple[int, int], ...],
    size: int,
):
    for cut in combinations(range(len(edges)), size):
        try:
            first, second = V.cut_shores(n, edges, cut)
        except AssertionError:
            continue
        if min(len(first), len(second)) < 2:
            continue
        if shore_connected(first, edges, cut) and shore_connected(second, edges, cut):
            yield cut, first, second


def main() -> None:
    geng = shutil.which("geng") or "/opt/homebrew/bin/geng"
    if not Path(geng).is_file():
        raise SystemExit("nauty geng not found")

    root_relations: dict[int, set[frozenset[int]]] = {2: set(), 3: set()}
    cap_relations: dict[int, set[frozenset[tuple[int, int, int]]]] = {
        2: set(), 3: set()
    }
    pole_count = {2: 0, 3: 0}
    graph_count = 0
    minimal_root = {
        2: frozenset(1 << index for index in (1, 2, 3, 4, 5, 6)),
        3: frozenset({1 << 0}),
    }
    minimal_cap = {
        2: frozenset({
            (0, 1 << 1, 1 << 4), (0, 1 << 2, 1 << 5),
            (0, 1 << 3, 1 << 6), (0, 1 << 4, 1 << 1),
            (0, 1 << 5, 1 << 2), (0, 1 << 6, 1 << 3),
        }),
        3: frozenset({(0, 1 << 0, 1 << 1)}),
    }
    pattern_counts = {
        2: {"root_equal": 0, "root_contains": 0,
            "cap_equal": 0, "cap_contains": 0},
        3: {"root_equal": 0, "root_contains": 0,
            "cap_equal": 0, "cap_contains": 0},
    }

    for order in (8, 10):
        rows = graph_rows(geng, order)
        graph_count += len(rows)
        for graph_word in rows:
            n, edges = V.graph6(graph_word)
            graph_incidence = V.incidence(n, tuple(tuple(edge) for edge in edges))
            for size in (2, 3):
                boundary_words = (
                    ((3, 3),)
                    if size == 2
                    else tuple(permutations((3, 5, 6)))
                )
                for cut, first, second in cuts(n, edges, size):
                    for shore in (first, second):
                        pole_count[size] += 1
                        pole = V.make_pole(edges, shore, cut)
                        boundary_vertices = {
                            pole.items[item][0] for item in pole.boundary_items
                        }
                        internal_edges = tuple(
                            original
                            for item, original in enumerate(pole.original_edges)
                            if len(pole.items[item]) == 2
                        )
                        for boundary_word in boundary_words:
                            fixed = dict(zip(pole.boundary_items, boundary_word))
                            words = V.enumerate_labellings(n, pole.items, fixed)
                            assert words
                            for root in internal_edges:
                                relation = frozenset(
                                    V.root_state(pole, word, root) for word in words
                                )
                                root_relations[size].add(relation)
                                pattern_counts[size]["root_equal"] += (
                                    relation == minimal_root[size]
                                )
                                pattern_counts[size]["root_contains"] += (
                                    minimal_root[size] <= relation
                                )
                            for z in shore - boundary_vertices:
                                relation = frozenset(
                                    V.cap_state(
                                        pole, word, z, graph_incidence
                                    ) for word in words
                                )
                                cap_relations[size].add(relation)
                                pattern_counts[size]["cap_equal"] += (
                                    relation == minimal_cap[size]
                                )
                                pattern_counts[size]["cap_contains"] += (
                                    minimal_cap[size] <= relation
                                )

    assert graph_count == 23
    assert pole_count == {2: 12, 3: 92}
    expected = {
        2: (7, 9, {2: 14, 3: 49},
            {"root_equal": 0, "root_contains": 8,
             "cap_equal": 0, "cap_contains": 0}),
        3: (108, 222, {2: 2040, 3: 21936},
            {"root_equal": 0, "root_contains": 64,
             "cap_equal": 0, "cap_contains": 5}),
    }
    for size in (2, 3):
        histogram: dict[int, int] = {}
        for root_relation in root_relations[size]:
            for cap_relation in cap_relations[size]:
                best = max(
                    V.joined_external_mask(root, cap).bit_count()
                    for root in root_relation
                    for cap in cap_relation
                )
                histogram[best] = histogram.get(best, 0) + 1
        actual = (len(root_relations[size]), len(cap_relations[size]),
                  histogram, pattern_counts[size])
        assert actual == expected[size]
        assert min(histogram) >= 2
        print(
            f"CUT size={size} poles={pole_count[size]} "
            f"root_relations={actual[0]} cap_relations={actual[1]} "
            f"cross_pairs={sum(histogram.values())} "
            f"best2={histogram.get(2, 0)} best3={histogram.get(3, 0)} "
            "bad=0 PASS"
        )
        counts = pattern_counts[size]
        print(
            f"MINIMAL_PATTERN size={size} root_equal={counts['root_equal']} "
            f"root_contains={counts['root_contains']} "
            f"cap_equal={counts['cap_equal']} "
            f"cap_contains={counts['cap_contains']} "
            "exact_pair_realized=0 PASS"
        )
    print(f"THROUGH10 host_graphs={graph_count} bad_relation_pairs=0 PASS")


if __name__ == "__main__":
    main()
