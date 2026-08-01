#!/usr/bin/env python3
"""Literal audit of the reciprocal-exchange defect-change formula.

The audit replays every candidate exchange at two frozen states:

* the 14-vertex fixed-coordinate descent countermodel; and
* the all-seven-profile-4 state in the targeted order-16 fibre.

For every legal exchange it verifies the odd-kernel circuit-exchange law,
the bilinear intersection update, and the quotient-boundary/Hamming-weight
formula for the coordinate untouched by the exchange.
"""

from __future__ import annotations

from collections import Counter, deque
import importlib.util
import json
from pathlib import Path
from types import ModuleType


ROOT_DIR = Path(__file__).resolve().parent.parent


def load(name: str, relative: str) -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        name, ROOT_DIR / relative
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


FIXED = load(
    "fixed_countermodel",
    "scratch/verify_jaeger_star_parity_descent_countermodel.py",
)
ORDER16 = load(
    "order16_local",
    "scratch/verify_jaeger_fano_min_descent_order16_closure_no_go.py",
)


def is_connected_tree(
    order: int,
    edges: tuple[tuple[int, int], ...],
    chosen: frozenset[int],
) -> bool:
    if len(chosen) != order - 1:
        return False
    adjacency: list[list[int]] = [[] for _ in range(order)]
    for edge in chosen:
        left, right = edges[edge]
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other in adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                stack.append(other)
    return len(seen) == order


def odd_kernel(
    order: int,
    edges: tuple[tuple[int, int], ...],
    tree: frozenset[int],
) -> frozenset[int]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge in tree:
        left, right = edges[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    parent = [-2] * order
    parent_edge = [-1] * order
    parent[0] = -1
    traversal = [0]
    for vertex in traversal:
        for other, edge in adjacency[vertex]:
            if parent[other] == -2:
                parent[other] = vertex
                parent_edge[other] = edge
                traversal.append(other)
    assert len(traversal) == order
    size = [1] * order
    answer: set[int] = set()
    for vertex in reversed(traversal[1:]):
        if size[vertex] % 2:
            answer.add(parent_edge[vertex])
        size[parent[vertex]] += size[vertex]
    return frozenset(answer)


def fundamental_cycle(
    order: int,
    edges: tuple[tuple[int, int], ...],
    tree: frozenset[int],
    added: int,
) -> frozenset[int]:
    assert added not in tree
    left, right = edges[added]
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge in tree:
        first, second = edges[edge]
        adjacency[first].append((second, edge))
        adjacency[second].append((first, edge))
    parent = [-2] * order
    parent_edge = [-1] * order
    parent[left] = -1
    queue = deque([left])
    while queue and parent[right] == -2:
        vertex = queue.popleft()
        for other, edge in adjacency[vertex]:
            if parent[other] == -2:
                parent[other] = vertex
                parent_edge[other] = edge
                queue.append(other)
    assert parent[right] != -2
    cycle = {added}
    vertex = right
    while vertex != left:
        cycle.add(parent_edge[vertex])
        vertex = parent[vertex]
    return frozenset(cycle)


def component_labels(
    order: int,
    edges: tuple[tuple[int, int], ...],
    forest: frozenset[int],
) -> tuple[int, ...]:
    adjacency: list[list[int]] = [[] for _ in range(order)]
    for edge in forest:
        left, right = edges[edge]
        adjacency[left].append(right)
        adjacency[right].append(left)
    labels = [-1] * order
    for start in range(order):
        if labels[start] >= 0:
            continue
        component = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if other not in component:
                    component.add(other)
                    stack.append(other)
        label = min(component)
        for vertex in component:
            labels[vertex] = label
    return tuple(labels)


def quotient_boundary(
    order: int,
    edges: tuple[tuple[int, int], ...],
    forest: frozenset[int],
    edge_set: frozenset[int],
) -> tuple[int, ...]:
    labels = component_labels(order, edges, forest)
    parity = [0] * order
    for edge in edge_set:
        left, right = edges[edge]
        first, second = labels[left], labels[right]
        if first != second:
            parity[first] ^= 1
            parity[second] ^= 1
    return tuple(parity)


def symmetric_difference(*sets: frozenset[int]) -> frozenset[int]:
    answer: set[int] = set()
    for edge_set in sets:
        answer.symmetric_difference_update(edge_set)
    return frozenset(answer)


def audit_case(
    *,
    name: str,
    order: int,
    edges: tuple[tuple[int, int], ...],
    root: int,
    omitted_masks: tuple[int, int, int],
    expected_candidates: int,
    expected_legal: int,
) -> dict[str, object]:
    incidence: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    spokes = tuple(incidence[root])
    internal = tuple(
        edge for edge in range(len(edges)) if edge not in spokes
    )
    assert len(spokes) == 3
    assert (
        omitted_masks[0] ^ omitted_masks[1] ^ omitted_masks[2]
        == (1 << len(internal)) - 1
    )

    def trees_and_kernels(
        classes: tuple[int, int, int],
    ) -> tuple[
        tuple[frozenset[int], frozenset[int], frozenset[int]],
        tuple[frozenset[int], frozenset[int], frozenset[int]],
    ] | None:
        trees = []
        kernels = []
        for coordinate in range(3):
            tree = frozenset(
                [spokes[coordinate]]
                + [
                    edge
                    for local, edge in enumerate(internal)
                    if not ((classes[coordinate] >> local) & 1)
                ]
            )
            if not is_connected_tree(order, edges, tree):
                return None
            trees.append(tree)
            kernels.append(odd_kernel(order, edges, tree))
        return tuple(trees), tuple(kernels)  # type: ignore[return-value]

    reconstructed = trees_and_kernels(omitted_masks)
    assert reconstructed is not None
    trees, kernels = reconstructed
    candidates = 0
    legal = 0
    active_histogram: Counter[tuple[int, int]] = Counter()
    score_change_histogram: Counter[int] = Counter()
    for first in range(3):
        for second in range(first + 1, 3):
            untouched = 3 - first - second
            for first_local in range(len(internal)):
                if not ((omitted_masks[first] >> first_local) & 1):
                    continue
                for second_local in range(len(internal)):
                    if not ((omitted_masks[second] >> second_local) & 1):
                        continue
                    candidates += 1
                    first_added = internal[first_local]
                    second_added = internal[second_local]
                    toggle = (1 << first_local) | (1 << second_local)
                    changed_masks = list(omitted_masks)
                    changed_masks[first] ^= toggle
                    changed_masks[second] ^= toggle
                    changed = trees_and_kernels(tuple(changed_masks))
                    if changed is None:
                        continue
                    legal += 1
                    changed_trees, changed_kernels = changed
                    assert changed_kernels[untouched] == kernels[untouched]

                    first_cycle = fundamental_cycle(
                        order, edges, trees[first], first_added
                    )
                    second_cycle = fundamental_cycle(
                        order, edges, trees[second], second_added
                    )
                    alpha = int(second_added in kernels[first])
                    beta = int(first_added in kernels[second])
                    active_histogram[(alpha, beta)] += 1
                    predicted_first = (
                        symmetric_difference(kernels[first], first_cycle)
                        if alpha
                        else kernels[first]
                    )
                    predicted_second = (
                        symmetric_difference(kernels[second], second_cycle)
                        if beta
                        else kernels[second]
                    )
                    assert predicted_first == changed_kernels[first]
                    assert predicted_second == changed_kernels[second]

                    terms = []
                    if alpha:
                        terms.append(first_cycle & kernels[second])
                    if beta:
                        terms.append(second_cycle & kernels[first])
                    if alpha and beta:
                        terms.append(first_cycle & second_cycle)
                    toggle_set = symmetric_difference(*terms)
                    old_pure = kernels[first] & kernels[second]
                    new_pure = (
                        changed_kernels[first] & changed_kernels[second]
                    )
                    assert (
                        symmetric_difference(old_pure, new_pure)
                        == toggle_set
                    )

                    old_boundary = quotient_boundary(
                        order,
                        edges,
                        kernels[untouched],
                        old_pure,
                    )
                    new_boundary = quotient_boundary(
                        order,
                        edges,
                        kernels[untouched],
                        new_pure,
                    )
                    toggle_boundary = quotient_boundary(
                        order,
                        edges,
                        kernels[untouched],
                        toggle_set,
                    )
                    assert tuple(
                        old ^ toggle
                        for old, toggle in zip(
                            old_boundary, toggle_boundary
                        )
                    ) == new_boundary
                    old_score = sum(old_boundary)
                    new_score = sum(new_boundary)
                    toggle_weight = sum(toggle_boundary)
                    overlap = sum(
                        old and toggle
                        for old, toggle in zip(
                            old_boundary, toggle_boundary
                        )
                    )
                    assert (
                        new_score - old_score
                        == toggle_weight - 2 * overlap
                    )
                    score_change_histogram[new_score - old_score] += 1
                    assert changed_trees[first] == (
                        trees[first] | {first_added}
                    ) - {second_added}
                    assert changed_trees[second] == (
                        trees[second] | {second_added}
                    ) - {first_added}

    assert candidates == expected_candidates
    assert legal == expected_legal
    return {
        "case": name,
        "candidate_exchanges": candidates,
        "legal_exchanges": legal,
        "active_bit_histogram": {
            f"{first},{second}": count
            for (first, second), count in sorted(active_histogram.items())
        },
        "untouched_coordinate_score_change_histogram": dict(
            sorted(score_change_histogram.items())
        ),
        "all_formula_checks_pass": True,
    }


def main() -> None:
    order14, edges14 = FIXED.parse_graph6(FIXED.GRAPH6)
    all14 = (1 << (len(edges14) - 3)) - 1
    masks14 = (
        FIXED.OMITTED_MASKS[0],
        FIXED.OMITTED_MASKS[1],
        all14 ^ FIXED.OMITTED_MASKS[0] ^ FIXED.OMITTED_MASKS[1],
    )
    results = [
        audit_case(
            name="fixed-coordinate-countermodel-14v",
            order=order14,
            edges=edges14,
            root=FIXED.ROOT,
            omitted_masks=masks14,
            expected_candidates=108,
            expected_legal=18,
        ),
        audit_case(
            name="all-seven-profile-four-state-16v",
            order=16,
            edges=ORDER16.EXPECTED_EDGES,
            root=ORDER16.ROOT,
            omitted_masks=ORDER16.OMITTED_LOCAL_MASKS,
            expected_candidates=147,
            expected_legal=25,
        ),
    ]
    print(
        json.dumps(
            {
                "claim": (
                    "exact odd-kernel, bilinear intersection, and "
                    "fixed-quotient defect-change formulas"
                ),
                "cases": results,
                "verified": True,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
