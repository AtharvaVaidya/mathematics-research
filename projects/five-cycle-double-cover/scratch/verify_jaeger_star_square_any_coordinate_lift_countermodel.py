#!/usr/bin/env python3
"""Check a good star state having no good square-local lift in any coordinate.

The checker is solver-free and uses only the Python standard library.  It
enumerates all 3^8 omitted-owner words for the eight square-gadget edges.
"""

from collections import Counter
from itertools import combinations, product


ROOT = 0

# Labelled graph6: G?zTb_
DOWN_EDGES = (
    (0, 4), (0, 5), (0, 6),
    (1, 4), (1, 5), (1, 7),
    (2, 4), (2, 6), (2, 7),
    (3, 5), (3, 6), (3, 7),
)
DOWN_TREES = (
    frozenset((0, 3, 4, 5, 7, 8, 9)),
    frozenset((2, 3, 4, 6, 8, 10, 11)),
    frozenset((1, 5, 6, 7, 9, 10, 11)),
)

# Expand AC=(1,7) and BD=(2,4), with a,b,c,d=8,9,10,11.
REMOVED = (5, 6)
OUTSIDE_EDGES = tuple(
    edge for edge_index, edge in enumerate(DOWN_EDGES)
    if edge_index not in REMOVED
)
GADGET_EDGES = (
    (1, 8),   # Aa
    (2, 9),   # Bb
    (7, 10),  # Cc
    (4, 11),  # Dd
    (8, 9),   # ab
    (9, 10),  # bc
    (10, 11), # cd
    (11, 8),  # da
)
UP_EDGES = OUTSIDE_EDGES + GADGET_EDGES

# A different good downstairs state and one good square-local lift of it.
# This shows that changing the selected state, rather than changing the
# graph or smoothing, rescues the same expanded fibre.
ALTERNATE_DOWN_TREES = (
    frozenset((0, 3, 4, 5, 6, 7, 10)),
    frozenset((1, 3, 4, 7, 8, 9, 11)),
    frozenset((2, 5, 6, 8, 9, 10, 11)),
)
UP_CONTROL_TREES = (
    frozenset((0, 3, 4, 5, 8, 10, 11, 12, 13, 14, 15)),
    frozenset((1, 3, 4, 5, 6, 7, 9, 11, 14, 16, 17)),
    frozenset((2, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17)),
)


def is_tree(vertex_count, edges, selected):
    if len(selected) != vertex_count - 1:
        return False
    parent = list(range(vertex_count))

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge_index in selected:
        left, right = edges[edge_index]
        left = find(left)
        right = find(right)
        if left == right:
            return False
        parent[left] = right
    return len({find(vertex) for vertex in range(vertex_count)}) == 1


def odd_kernel(vertex_count, edges, tree):
    adjacency = [[] for _ in range(vertex_count)]
    for edge_index in tree:
        left, right = edges[edge_index]
        adjacency[left].append((right, edge_index))
        adjacency[right].append((left, edge_index))

    parent = [-1] * vertex_count
    parent_edge = [-1] * vertex_count
    order = [0]
    parent[0] = 0
    for vertex in order:
        for neighbour, edge_index in adjacency[vertex]:
            if parent[neighbour] == -1:
                parent[neighbour] = vertex
                parent_edge[neighbour] = edge_index
                order.append(neighbour)
    assert len(order) == vertex_count

    sizes = [1] * vertex_count
    kernel = set()
    for vertex in reversed(order[1:]):
        if sizes[vertex] & 1:
            kernel.add(parent_edge[vertex])
        sizes[parent[vertex]] += sizes[vertex]

    boundary = [0] * vertex_count
    for edge_index in kernel:
        left, right = edges[edge_index]
        boundary[left] ^= 1
        boundary[right] ^= 1
    assert boundary == [1] * vertex_count
    return frozenset(kernel)


def components(vertex_count, edges, selected):
    adjacency = [[] for _ in range(vertex_count)]
    for edge_index in selected:
        left, right = edges[edge_index]
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = set()
    answer = []
    for start in range(vertex_count):
        if start in seen:
            continue
        component = {start}
        seen.add(start)
        queue = [start]
        for vertex in queue:
            for neighbour in adjacency[vertex]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    component.add(neighbour)
                    queue.append(neighbour)
        answer.append(frozenset(component))
    return answer


def defect_profile(vertex_count, edges, trees):
    kernels = tuple(odd_kernel(vertex_count, edges, tree) for tree in trees)
    profile = []
    for coordinate in range(3):
        other = [index for index in range(3) if index != coordinate]
        pure_value = kernels[other[0]] & kernels[other[1]]
        defect = 0
        for component in components(
            vertex_count, edges, kernels[coordinate]
        ):
            crossings = sum(
                1
                for edge_index in pure_value
                if ((edges[edge_index][0] in component)
                    != (edges[edge_index][1] in component))
            )
            defect += crossings & 1
        profile.append(defect)
    return tuple(profile), kernels


def check_simple_cubic(vertex_count, edges):
    assert all(left != right for left, right in edges)
    assert len({tuple(sorted(edge)) for edge in edges}) == len(edges)
    degree = [0] * vertex_count
    for left, right in edges:
        degree[left] += 1
        degree[right] += 1
    assert degree == [3] * vertex_count


def connected_after_deleting(vertex_count, edges, deleted):
    adjacency = [[] for _ in range(vertex_count)]
    for edge_index, (left, right) in enumerate(edges):
        if edge_index not in deleted:
            adjacency[left].append(right)
            adjacency[right].append(left)
    seen = {0}
    queue = [0]
    for vertex in queue:
        for neighbour in adjacency[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return len(seen) == vertex_count


def check_star_multiplicity(edges, trees):
    actual = [
        sum(edge_index in tree for tree in trees)
        for edge_index in range(len(edges))
    ]
    expected = [1 if ROOT in edge else 2 for edge in edges]
    assert actual == expected


def fixed_outside_parts():
    down_to_outside = {}
    outside_index = 0
    for down_index in range(len(DOWN_EDGES)):
        if down_index not in REMOVED:
            down_to_outside[down_index] = outside_index
            outside_index += 1
    return tuple(
        frozenset(
            down_to_outside[edge_index]
            for edge_index in tree
            if edge_index not in REMOVED
        )
        for tree in DOWN_TREES
    )


def main():
    check_simple_cubic(8, DOWN_EDGES)
    check_simple_cubic(12, UP_EDGES)
    assert all(
        connected_after_deleting(vertex_count, edges, deleted)
        for vertex_count, edges in ((8, DOWN_EDGES), (12, UP_EDGES))
        for size in (1, 2)
        for deleted in combinations(range(len(edges)), size)
    )

    assert all(is_tree(8, DOWN_EDGES, tree) for tree in DOWN_TREES)
    check_star_multiplicity(DOWN_EDGES, DOWN_TREES)
    down_profile, down_kernels = defect_profile(
        8, DOWN_EDGES, DOWN_TREES
    )
    assert down_profile == (2, 2, 0)
    assert down_kernels == (
        frozenset((0, 5, 7, 9)),
        frozenset((2, 4, 6, 11)),
        frozenset((1, 5, 6, 10)),
    )
    assert down_kernels[0].isdisjoint(down_kernels[1])

    outside_parts = fixed_outside_parts()
    histogram = Counter()
    legal_lifts = 0
    for owner in product(range(3), repeat=8):
        lifted = []
        for tree_index in range(3):
            local = {
                len(OUTSIDE_EDGES) + gadget_index
                for gadget_index in range(8)
                if owner[gadget_index] != tree_index
            }
            lifted.append(outside_parts[tree_index] | local)
        lifted = tuple(lifted)
        if not all(is_tree(12, UP_EDGES, tree) for tree in lifted):
            continue
        check_star_multiplicity(UP_EDGES, lifted)
        profile, _ = defect_profile(12, UP_EDGES, lifted)
        legal_lifts += 1
        histogram[profile] += 1

    assert legal_lifts == 72
    assert histogram == Counter({
        (2, 2, 2): 38,
        (2, 2, 4): 12,
        (2, 4, 2): 2,
        (4, 2, 2): 2,
        (4, 4, 2): 18,
    })
    assert all(0 not in profile for profile in histogram)

    assert all(
        is_tree(8, DOWN_EDGES, tree) for tree in ALTERNATE_DOWN_TREES
    )
    check_star_multiplicity(DOWN_EDGES, ALTERNATE_DOWN_TREES)
    alternate_profile, _ = defect_profile(
        8, DOWN_EDGES, ALTERNATE_DOWN_TREES
    )
    assert alternate_profile == (0, 2, 2)

    assert all(is_tree(12, UP_EDGES, tree) for tree in UP_CONTROL_TREES)
    check_star_multiplicity(UP_EDGES, UP_CONTROL_TREES)
    control_profile, _ = defect_profile(
        12, UP_EDGES, UP_CONTROL_TREES
    )
    assert control_profile == (0, 2, 2)

    down_to_outside = {}
    next_outside = 0
    for down_index in range(len(DOWN_EDGES)):
        if down_index not in REMOVED:
            down_to_outside[down_index] = next_outside
            next_outside += 1
    expected_local_masks = (63, 210, 237)
    for tree_index in range(3):
        expected_outside = {
            down_to_outside[edge_index]
            for edge_index in ALTERNATE_DOWN_TREES[tree_index]
            if edge_index not in REMOVED
        }
        assert {
            edge_index
            for edge_index in UP_CONTROL_TREES[tree_index]
            if edge_index < len(OUTSIDE_EDGES)
        } == expected_outside
        actual_local_mask = sum(
            1 << (edge_index - len(OUTSIDE_EDGES))
            for edge_index in UP_CONTROL_TREES[tree_index]
            if edge_index >= len(OUTSIDE_EDGES)
        )
        assert actual_local_mask == expected_local_masks[tree_index]

    print("PASS: downstairs state profile:", down_profile)
    print("PASS: omitted-owner assignments checked:", 3 ** 8)
    print("PASS: legal square-local lifts:", legal_lifts)
    print("PASS: lift profile histogram:", dict(sorted(histogram.items())))
    print("PASS: no local lift is good in any coordinate")
    print("CONTROL: alternate downstairs profile:", alternate_profile)
    print("CONTROL: its good local lift has profile:", control_profile)


if __name__ == "__main__":
    main()
