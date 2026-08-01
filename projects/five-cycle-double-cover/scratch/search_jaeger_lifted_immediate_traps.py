#!/usr/bin/env python3
"""Exact strict-trap search among triangle lifts of a frozen Jaeger state.

The contracted state is the first order-16 state in
``verify_jaeger_fano_min_immediate_descent_countermodel.py``.  It has
positive symmetric Fano score and no lower one-exchange neighbour, but it
has neutral neighbours.  This program expands a prescribed number of
distinct nonroot vertices into triangles, exhausts every choice of expanded
vertices and every S_3 lift, and asks whether the lift has eliminated all
neutral exchanges.  A reported witness is therefore an exact strict local
minimum (and hence a counterexample to the full same-level-component
descent proposal).

This is a search program, not a proof of a clean run.
"""

from __future__ import annotations

import argparse
from collections import Counter
import importlib.util
import itertools
import json
from pathlib import Path
import random
from typing import Hashable


ROOT_DIR = Path(__file__).resolve().parents[1]
VERIFIER_PATH = (
    ROOT_DIR
    / "scratch"
    / "verify_jaeger_fano_min_immediate_descent_countermodel.py"
)
SPEC = importlib.util.spec_from_file_location("frozen_immediate", VERIFIER_PATH)
assert SPEC is not None and SPEC.loader is not None
FROZEN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FROZEN)


def base_trees() -> tuple[frozenset[int], ...]:
    return tuple(frozenset(tree) for tree in FROZEN.EXPECTED_START_TREES)


def configure_base(
    graph6: str,
    root: int,
    spokes: tuple[int, int, int],
    omitted_masks: tuple[int, int, int],
) -> None:
    """Replace the frozen base state by another literal star-fibre state."""

    order, edges = FROZEN.parse_graph6(graph6)
    assert 0 <= root < order
    assert set(spokes) == {
        edge for edge, endpoints in enumerate(edges) if root in endpoints
    }
    internal = tuple(
        edge for edge in range(len(edges)) if edge not in spokes
    )
    all_internal = (1 << len(internal)) - 1
    assert (
        omitted_masks[0] ^ omitted_masks[1] ^ omitted_masks[2]
    ) == all_internal
    assert not (
        omitted_masks[0] & omitted_masks[1]
        or omitted_masks[0] & omitted_masks[2]
        or omitted_masks[1] & omitted_masks[2]
    )
    trees = tuple(
        tuple(
            sorted(
                [spokes[coordinate]]
                + [
                    edge
                    for local, edge in enumerate(internal)
                    if not ((omitted_masks[coordinate] >> local) & 1)
                ]
            )
        )
        for coordinate in range(3)
    )
    assert all(
        FROZEN.is_tree(order, edges, frozenset(tree)) for tree in trees
    )
    FROZEN.GRAPH6 = graph6
    FROZEN.ROOT = root
    FROZEN.SPOKES = spokes
    FROZEN.EXPECTED_START_TREES = trees


def expanded_lift(
    selected: tuple[int, ...],
    permutations: tuple[tuple[int, int, int], ...],
    contracted_trees: tuple[frozenset[int], ...] | None = None,
) -> tuple[
    int,
    tuple[tuple[int, int], ...],
    int,
    tuple[frozenset[int], ...],
]:
    """Simultaneously expand original vertices and lift the three trees."""

    old_order, old_edges = FROZEN.parse_graph6(FROZEN.GRAPH6)
    selected_set = frozenset(selected)
    assert FROZEN.ROOT not in selected_set
    permutation_of = dict(zip(selected, permutations, strict=True))

    neighbours: dict[int, tuple[int, int, int]] = {}
    port_of: dict[tuple[int, int], tuple[int, int]] = {}
    for vertex in selected:
        row = tuple(
            sorted(
                right if left == vertex else left
                for left, right in old_edges
                if vertex in (left, right)
            )
        )
        assert len(row) == 3
        neighbours[vertex] = row
        for index, other in enumerate(row):
            port_of[(vertex, other)] = (vertex, index)

    def lifted_endpoint(vertex: int, other: int) -> Hashable:
        if vertex in selected_set:
            return port_of[(vertex, other)]
        return vertex

    symbolic_edges: set[frozenset[Hashable]] = set()
    old_to_symbolic: list[frozenset[Hashable]] = []
    for left, right in old_edges:
        lifted = frozenset(
            (
                lifted_endpoint(left, right),
                lifted_endpoint(right, left),
            )
        )
        assert len(lifted) == 2
        symbolic_edges.add(lifted)
        old_to_symbolic.append(lifted)

    triangle_symbolic: dict[int, tuple[frozenset[Hashable], ...]] = {}
    for vertex in selected:
        triangle = tuple(
            frozenset(
                (
                    (vertex, index),
                    (vertex, (index + 1) % 3),
                )
            )
            for index in range(3)
        )
        assert len(set(triangle)) == 3
        triangle_symbolic[vertex] = triangle
        symbolic_edges.update(triangle)

    symbolic_vertices = set().union(*symbolic_edges)
    root_symbolic: Hashable = FROZEN.ROOT
    ordered_vertices = [root_symbolic] + sorted(
        symbolic_vertices - {root_symbolic}, key=repr
    )
    label = {vertex: index for index, vertex in enumerate(ordered_vertices)}
    edges = tuple(
        sorted(
            (
                min(label[left], label[right]),
                max(label[left], label[right]),
            )
            for symbolic in symbolic_edges
            for left, right in [tuple(symbolic)]
        )
    )
    edge_id = {
        frozenset(endpoints): index for index, endpoints in enumerate(edges)
    }

    trees: list[frozenset[int]] = []
    if contracted_trees is None:
        contracted_trees = base_trees()
    for coordinate, old_tree in enumerate(contracted_trees):
        symbolic_tree = {old_to_symbolic[edge] for edge in old_tree}
        for vertex in selected:
            omitted = permutation_of[vertex][coordinate]
            symbolic_tree.update(
                edge
                for index, edge in enumerate(triangle_symbolic[vertex])
                if index != omitted
            )
        tree = frozenset(
            edge_id[
                frozenset((label[left], label[right]))
            ]
            for symbolic in symbolic_tree
            for left, right in [tuple(symbolic)]
        )
        trees.append(tree)

    order = old_order + 2 * len(selected)
    assert len(ordered_vertices) == order
    assert all(FROZEN.is_tree(order, edges, tree) for tree in trees)
    for edge in range(len(edges)):
        expected = 1 if 0 in edges[edge] else 2
        assert sum(edge in tree for tree in trees) == expected
    return order, edges, 0, tuple(trees)


def incidence(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    assert all(len(row) == 3 for row in rows)
    return tuple(tuple(row) for row in rows)


def profile(
    order: int,
    edges: tuple[tuple[int, int], ...],
    trees: tuple[frozenset[int], ...],
) -> tuple[int, ...]:
    kernels = tuple(FROZEN.odd_kernel(order, edges, tree) for tree in trees)
    return FROZEN.fano_profile(order, edges, incidence(order, edges), kernels)


def neighbour_histogram(
    order: int,
    edges: tuple[tuple[int, int], ...],
    root: int,
    trees: tuple[frozenset[int], ...],
) -> tuple[int, int, int, int]:
    root_spokes = frozenset(
        edge for edge, endpoints in enumerate(edges) if root in endpoints
    )
    omitted = tuple(
        frozenset(
            edge
            for edge in range(len(edges))
            if edge not in root_spokes and edge not in tree
        )
        for tree in trees
    )
    internal = frozenset(range(len(edges))) - root_spokes
    assert set().union(*omitted) == internal
    assert sum(map(len, omitted)) == len(internal)
    old_score = min(profile(order, edges, trees))
    lower = equal = higher = legal = 0
    for first, second in itertools.combinations(range(3), 2):
        for edge_first in omitted[first]:
            for edge_second in omitted[second]:
                changed = list(trees)
                changed[first] = frozenset(
                    (changed[first] - {edge_second}) | {edge_first}
                )
                changed[second] = frozenset(
                    (changed[second] - {edge_first}) | {edge_second}
                )
                if not (
                    FROZEN.is_tree(order, edges, changed[first])
                    and FROZEN.is_tree(order, edges, changed[second])
                ):
                    continue
                legal += 1
                score = min(profile(order, edges, tuple(changed)))
                lower += score < old_score
                equal += score == old_score
                higher += score > old_score
    return legal, lower, equal, higher


def contracted_neighbour_trees() -> tuple[tuple[frozenset[int], ...], ...]:
    """All 23 legal neighbours of the frozen contracted state."""

    order, edges = FROZEN.parse_graph6(FROZEN.GRAPH6)
    trees = base_trees()
    root_spokes = frozenset(FROZEN.SPOKES)
    omitted = tuple(
        frozenset(
            edge
            for edge in range(len(edges))
            if edge not in root_spokes and edge not in tree
        )
        for tree in trees
    )
    answer: list[tuple[frozenset[int], ...]] = []
    for first, second in itertools.combinations(range(3), 2):
        for edge_first in omitted[first]:
            for edge_second in omitted[second]:
                changed = list(trees)
                changed[first] = frozenset(
                    (changed[first] - {edge_second}) | {edge_first}
                )
                changed[second] = frozenset(
                    (changed[second] - {edge_first}) | {edge_second}
                )
                if (
                    FROZEN.is_tree(order, edges, changed[first])
                    and FROZEN.is_tree(order, edges, changed[second])
                ):
                    answer.append(tuple(changed))
    assert answer
    return tuple(answer)


def product_neighbour_histogram(
    selected: tuple[int, ...],
    permutations: tuple[tuple[int, int, int], ...],
) -> tuple[tuple[int, ...], Counter[int]]:
    """Score current lift and every neighbour from the exact product model."""

    order, edges, _, trees = expanded_lift(selected, permutations)
    current_profile = profile(order, edges, trees)
    scores: Counter[int] = Counter()
    for neighbour_trees in contracted_neighbour_trees():
        lifted = expanded_lift(
            selected, permutations, contracted_trees=neighbour_trees
        )[3]
        scores[min(profile(order, edges, lifted))] += 1
    for index in range(len(selected)):
        for first, second in itertools.combinations(range(3), 2):
            changed = [list(row) for row in permutations]
            changed[index][first], changed[index][second] = (
                changed[index][second],
                changed[index][first],
            )
            lifted = expanded_lift(
                selected, tuple(tuple(row) for row in changed)
            )[3]
            scores[min(profile(order, edges, lifted))] += 1
    assert sum(scores.values()) == len(contracted_neighbour_trees()) + 3 * len(
        selected
    )
    return current_profile, scores


def random_configuration_search(samples: int, seed: int) -> int:
    """Stochastic search over the 7^15 simultaneous triangle-lift choices."""

    rng = random.Random(seed)
    order = FROZEN.parse_graph6(FROZEN.GRAPH6)[0]
    vertices = tuple(
        vertex for vertex in range(order) if vertex != FROZEN.ROOT
    )
    permutation_rows = tuple(itertools.permutations(range(3)))
    # Assignment -1 means unexpanded, 0..5 selects an omitted-edge
    # permutation for that vertex.
    assignment = [-1] * len(vertices)
    # Exact exhaustive searches through three expansions identify this
    # six-neutral-pair reduction as the best current seed.
    if FROZEN.GRAPH6 == "O??CA?_ceOGgH_F?AK@P?" and FROZEN.ROOT == 13:
        for vertex, permutation in {
            0: (0, 1, 2),
            7: (2, 1, 0),
            15: (0, 1, 2),
        }.items():
            assignment[vertices.index(vertex)] = permutation_rows.index(
                permutation
            )
    best_key: tuple[int, int, int, int] | None = None
    best_row: dict[str, object] | None = None
    for sample in range(samples):
        if sample == 0:
            candidate = assignment.copy()
        elif sample % 25 == 0:
            candidate = [
                -1 if rng.random() < 0.25 else rng.randrange(6)
                for _ in vertices
            ]
        else:
            candidate = assignment.copy()
            changed_vertex = rng.randrange(len(vertices))
            candidate[changed_vertex] = rng.randrange(-1, 6)
        selected = tuple(
            vertex
            for vertex, value in zip(vertices, candidate, strict=True)
            if value >= 0
        )
        permutations = tuple(
            permutation_rows[value]
            for value in candidate
            if value >= 0
        )
        current_profile, scores = product_neighbour_histogram(
            selected, permutations
        )
        current = min(current_profile)
        lower = sum(count for value, count in scores.items() if value < current)
        equal = scores[current]
        # Prefer absence of lower moves, then fewer neutral moves, then a
        # larger positive score.  The final term mildly penalizes graph size.
        key = (lower, equal, -current if current else 100, len(selected))
        if best_key is None or key < best_key:
            best_key = key
            assignment = candidate
            best_row = {
                "sample": sample,
                "selected": list(selected),
                "permutations": [list(row) for row in permutations],
                "profile": list(current_profile),
                "score_histogram": dict(sorted(scores.items())),
                "key": list(key),
            }
            print(json.dumps({"status": "BEST_RANDOM", **best_row}), flush=True)
        elif rng.random() < 0.01:
            assignment = candidate
        if current > 0 and lower == 0 and equal == 0:
            print(
                json.dumps(
                    {"status": "STRICT_TRAP", **(best_row or {})},
                    sort_keys=True,
                )
            )
            return 1
    print(
        json.dumps(
            {
                "status": "RANDOM_DONE",
                "samples": samples,
                "seed": seed,
                "best": best_row,
            },
            sort_keys=True,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--triangles", type=int, choices=range(1, 11), default=1)
    parser.add_argument(
        "--selection-limit",
        type=int,
        default=0,
        help="stop after this many vertex subsets (zero means exhaustive)",
    )
    parser.add_argument(
        "--required",
        default="",
        help="comma-separated original vertices required in every subset",
    )
    parser.add_argument(
        "--fixed",
        default="",
        help="comma-separated vertex:permutation rows, for example 0:012,7:210",
    )
    parser.add_argument("--random-configs", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260728)
    parser.add_argument("--graph6", default="")
    parser.add_argument("--root", type=int)
    parser.add_argument("--spokes", default="")
    parser.add_argument("--omitted", default="")
    args = parser.parse_args()
    custom_fields = (
        bool(args.graph6),
        args.root is not None,
        bool(args.spokes),
        bool(args.omitted),
    )
    if any(custom_fields) and not all(custom_fields):
        parser.error("--graph6, --root, --spokes and --omitted are all required")
    if all(custom_fields):
        spokes = tuple(int(value) for value in args.spokes.split(","))
        omitted = tuple(int(value) for value in args.omitted.split(","))
        if len(spokes) != 3 or len(omitted) != 3:
            parser.error("--spokes and --omitted each require three integers")
        configure_base(
            args.graph6,
            args.root,
            spokes,  # type: ignore[arg-type]
            omitted,  # type: ignore[arg-type]
        )
    if args.random_configs:
        return random_configuration_search(args.random_configs, args.seed)
    fixed: dict[int, tuple[int, int, int]] = {}
    for item in args.fixed.split(","):
        if not item:
            continue
        vertex_text, permutation_text = item.split(":", 1)
        permutation = tuple(int(value) for value in permutation_text)
        if sorted(permutation) != [0, 1, 2]:
            raise ValueError(f"bad fixed permutation: {item}")
        fixed[int(vertex_text)] = permutation  # type: ignore[assignment]
    required = frozenset(
        int(value) for value in args.required.split(",") if value
    ) | frozenset(fixed)

    order = FROZEN.parse_graph6(FROZEN.GRAPH6)[0]
    vertices = tuple(
        vertex for vertex in range(order) if vertex != FROZEN.ROOT
    )
    permutation_rows = tuple(itertools.permutations(range(3)))
    tested_selections = tested_lifts = positive_lifts = 0
    best_equal: int | None = None
    best_row: dict[str, object] | None = None
    for selected in itertools.combinations(vertices, args.triangles):
        if not required <= frozenset(selected):
            continue
        if args.selection_limit and tested_selections >= args.selection_limit:
            break
        tested_selections += 1
        free_vertices = tuple(vertex for vertex in selected if vertex not in fixed)
        for free_permutations in itertools.product(
            permutation_rows, repeat=len(free_vertices)
        ):
            free_map = dict(zip(free_vertices, free_permutations, strict=True))
            permutations = tuple(
                fixed[vertex] if vertex in fixed else free_map[vertex]
                for vertex in selected
            )
            tested_lifts += 1
            order, edges, root, trees = expanded_lift(
                selected, permutations
            )
            current_profile = profile(order, edges, trees)
            score = min(current_profile)
            if score == 0:
                continue
            positive_lifts += 1
            legal, lower, equal, higher = neighbour_histogram(
                order, edges, root, trees
            )
            row = {
                "selected": list(selected),
                "permutations": [list(value) for value in permutations],
                "order": order,
                "profile": list(current_profile),
                "score": score,
                "legal": legal,
                "lower": lower,
                "equal": equal,
                "higher": higher,
            }
            if lower == 0 and (best_equal is None or equal < best_equal):
                best_equal = equal
                best_row = row
                print(json.dumps({"status": "BEST", **row}), flush=True)
            if lower == 0 and equal == 0:
                print(json.dumps({"status": "STRICT_TRAP", **row}))
                return 1
    print(
        json.dumps(
            {
                "status": "DONE",
                "triangles": args.triangles,
                "tested_selections": tested_selections,
                "tested_lifts": tested_lifts,
                "positive_lifts": positive_lifts,
                "best_equal": best_equal,
                "best": best_row,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
