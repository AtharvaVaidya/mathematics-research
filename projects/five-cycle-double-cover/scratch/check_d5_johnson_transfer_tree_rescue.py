#!/usr/bin/env python3
"""Exhaust the Johnson-labeled transfer-tree endpoint rescue theorem."""

from __future__ import annotations

import itertools
import sys
from collections import deque
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for item in (str(PROJECT_ROOT), str(PROJECT_ROOT / "scratch")):
    if item not in sys.path:
        sys.path.insert(0, item)

from check_d5_capped_ladder_exact_lifting import (  # noqa: E402
    ADJACENT,
    active,
    alternatize,
    transpose,
    word_move,
)


def prufer_edges(code):
    vertices = len(code) + 2
    degree = [1] * vertices
    for vertex in code:
        degree[vertex] += 1
    edges = []
    for vertex in code:
        leaf = next(index for index in range(vertices) if degree[index] == 1)
        edges.append((leaf, vertex))
        degree[leaf] -= 1
        degree[vertex] -= 1
    remaining = [index for index in range(vertices) if degree[index] == 1]
    assert len(remaining) == 2
    edges.append(tuple(remaining))
    return tuple(edges)


def adjacency(vertices, edges):
    answer = [[] for _ in range(vertices)]
    for left, right in edges:
        answer[left].append(right)
        answer[right].append(left)
    return answer


def marked_path(rows, first, second):
    parent = {first: None}
    queue = deque([first])
    while queue:
        vertex = queue.popleft()
        if vertex == second:
            break
        for other in rows[vertex]:
            if other not in parent:
                parent[other] = vertex
                queue.append(other)
    path = []
    cursor = second
    while cursor is not None:
        path.append(cursor)
        cursor = parent[cursor]
    return tuple(reversed(path))


def homomorphisms(rows):
    vertices = len(rows)
    parent = {0: None}
    order = [0]
    for vertex in order:
        for other in rows[vertex]:
            if other not in parent:
                parent[other] = vertex
                order.append(other)
    assert len(order) == vertices
    for choices in itertools.product(range(6), repeat=vertices - 1):
        labels = [None] * vertices
        labels[0] = 0b00011  # Normalize the first tree vertex to 01.
        for vertex, choice in zip(order[1:], choices):
            labels[vertex] = ADJACENT[labels[parent[vertex]]][choice]
        yield tuple(labels)


def tree_move(rows, labels, root, pair_mask):
    assert active(labels[root], pair_mask)
    component = {root}
    stack = [root]
    while stack:
        vertex = stack.pop()
        for other in rows[vertex]:
            if (
                other not in component
                and active(labels[other], pair_mask)
            ):
                component.add(other)
                stack.append(other)
    answer = list(labels)
    for vertex in component:
        answer[vertex] = transpose(answer[vertex], pair_mask)
    answer = tuple(answer)
    for vertex, neighbors in enumerate(rows):
        for other in neighbors:
            assert (
                answer[vertex] & answer[other]
            ).bit_count() == 1
    return answer, frozenset(component)


def audit_state(rows, labels, roots):
    path = marked_path(rows, *roots)
    path_word = tuple(labels[vertex] for vertex in path)
    final_word, plan = alternatize(path_word)
    current_labels = labels
    current_word = path_word
    for side, pair_mask in plan:
        root = roots[0] if side == "left" else roots[1]
        current_labels, component = tree_move(
            rows, current_labels, root, pair_mask
        )
        expected = word_move(current_word, side, pair_mask)
        actual = tuple(current_labels[vertex] for vertex in path)
        assert actual == expected

        # Exact path projection: the moved tree component can include
        # branches, but its intersection with the path is the moved prefix
        # or suffix and nothing else.
        moved_path = tuple(vertex for vertex in path if vertex in component)
        if side == "left":
            assert moved_path == path[: len(moved_path)]
        else:
            assert moved_path == path[len(path) - len(moved_path) :]
        current_word = expected
    assert current_word == final_word
    common_pair = final_word[0] ^ final_word[1]
    assert all(active(label, common_pair) for label in final_word)
    return len(plan), len(path)


def main():
    trees = 0
    states = 0
    maximum_plan = 0
    maximum_path = 0
    for vertices in range(2, 6):
        for code in itertools.product(range(vertices), repeat=vertices - 2):
            edges = prufer_edges(code)
            rows = adjacency(vertices, edges)
            trees += 1
            roots = (0, vertices - 1)
            for labels in homomorphisms(rows):
                plan_length, path_length = audit_state(rows, labels, roots)
                states += 1
                maximum_plan = max(maximum_plan, plan_length)
                maximum_path = max(maximum_path, path_length)
    assert trees == sum(vertices ** (vertices - 2) for vertices in range(2, 6))
    assert states == sum(
        vertices ** (vertices - 2) * 6 ** (vertices - 1)
        for vertices in range(2, 6)
    )
    print(
        "PASS: Johnson transfer-tree endpoint rescue; "
        f"labeled_trees={trees}, normalized_homomorphisms={states}, "
        f"maximum_path={maximum_path}, maximum_plan={maximum_plan}"
    )


if __name__ == "__main__":
    main()
