#!/usr/bin/env python3
"""Finite whole-selection square-lift census at order eight.

For every simple 3-edge-connected cubic graph on eight vertices, every
labelled root, and every pair of independent edges avoiding the root, the
script finds some exact-good downstairs star state having some exact-good
square-local lift.  This is a finite theorem only.
"""

from itertools import combinations

from verify_jaeger_star_square_any_coordinate_lift_countermodel import (
    connected_after_deleting,
    defect_profile,
    is_tree,
)


# Complete `geng -cq -d3 -D3 8` stream, represented by the graph6 record
# and its labelled edge list.  GCXmd_ is the sole graph with a 2-edge cut.
ORDER8 = (
    ("G?zTb_", (
        (0, 4), (0, 5), (0, 6), (1, 4), (1, 5), (1, 7),
        (2, 4), (2, 6), (2, 7), (3, 5), (3, 6), (3, 7),
    )),
    ("GCrb`o", (
        (0, 3), (0, 4), (0, 5), (1, 4), (1, 5), (1, 6),
        (2, 5), (2, 6), (2, 7), (3, 6), (3, 7), (4, 7),
    )),
    ("GCZJd_", (
        (0, 3), (0, 5), (0, 7), (1, 4), (1, 5), (1, 6),
        (2, 4), (2, 6), (2, 7), (3, 6), (3, 7), (4, 5),
    )),
    ("GCXmd_", (
        (0, 3), (0, 6), (0, 7), (1, 4), (1, 5), (1, 6),
        (2, 4), (2, 5), (2, 7), (3, 6), (3, 7), (4, 5),
    )),
    ("GCY^B_", (
        (0, 3), (0, 5), (0, 6), (1, 4), (1, 6), (1, 7),
        (2, 4), (2, 6), (2, 7), (3, 5), (3, 7), (4, 5),
    )),
)


def is_three_edge_connected(edges):
    return all(
        connected_after_deleting(8, edges, deleted)
        for size in (1, 2)
        for deleted in combinations(range(len(edges)), size)
    )


def spanning_trees(edges):
    return [
        frozenset(chosen)
        for chosen in combinations(range(12), 7)
        if is_tree(8, edges, frozenset(chosen))
    ]


def star_states(edges, root, trees):
    tree_lookup = set(trees)
    multiplicity = [1 if root in edge else 2 for edge in edges]
    answer = []
    for first in trees:
        for second in trees:
            remaining = []
            valid = True
            for edge_index in range(12):
                count = (
                    multiplicity[edge_index]
                    - (edge_index in first)
                    - (edge_index in second)
                )
                if count not in (0, 1):
                    valid = False
                    break
                if count:
                    remaining.append(edge_index)
            if not valid:
                continue
            third = frozenset(remaining)
            if third in tree_lookup:
                answer.append((first, second, third))
    return answer


def eligible_pairs(edges, root):
    return [
        pair
        for pair in combinations(range(12), 2)
        if root not in edges[pair[0]]
        and root not in edges[pair[1]]
        and len(set(edges[pair[0]] + edges[pair[1]])) == 4
    ]


def good_local_lift(edges, state, first_edge, second_edge):
    removed = {first_edge, second_edge}
    outside_edges = tuple(
        edge for edge_index, edge in enumerate(edges)
        if edge_index not in removed
    )
    down_to_outside = {}
    next_outside = 0
    for edge_index in range(12):
        if edge_index not in removed:
            down_to_outside[edge_index] = next_outside
            next_outside += 1
    outside_parts = tuple(
        frozenset(
            down_to_outside[edge_index]
            for edge_index in tree
            if edge_index not in removed
        )
        for tree in state
    )

    A, C = edges[first_edge]
    B, D = edges[second_edge]
    a, b, c, d = 8, 9, 10, 11
    gadget_edges = (
        (A, a), (B, b), (C, c), (D, d),
        (a, b), (b, c), (c, d), (d, a),
    )
    up_edges = outside_edges + gadget_edges

    options = []
    for tree_index in range(3):
        candidates = []
        for local_mask in range(256):
            local = {
                10 + edge_index
                for edge_index in range(8)
                if local_mask >> edge_index & 1
            }
            lifted = outside_parts[tree_index] | local
            if is_tree(12, up_edges, lifted):
                candidates.append((255 ^ local_mask, lifted))
        options.append(candidates)

    third_by_omitted = dict(options[2])
    for omitted_zero, tree_zero in options[0]:
        for omitted_one, tree_one in options[1]:
            if omitted_zero & omitted_one:
                continue
            omitted_two = 255 ^ omitted_zero ^ omitted_one
            tree_two = third_by_omitted.get(omitted_two)
            if tree_two is None:
                continue
            profile, _ = defect_profile(
                12, up_edges, (tree_zero, tree_one, tree_two)
            )
            if 0 in profile:
                return True
    return False


def main():
    assert len(ORDER8) == 5
    three_connected = [
        (record, edges)
        for record, edges in ORDER8
        if is_three_edge_connected(edges)
    ]
    assert [record for record, _ in three_connected] == [
        "G?zTb_", "GCrb`o", "GCZJd_", "GCY^B_"
    ]

    rows = 0
    graph_root_pairs = 0
    state_attempts = 0
    for record, edges in three_connected:
        trees = spanning_trees(edges)
        for root in range(8):
            states = star_states(edges, root, trees)
            good_states = [
                state
                for state in states
                if 0 in defect_profile(8, edges, state)[0]
            ]
            pairs = eligible_pairs(edges, root)
            assert len(pairs) == 21
            for first_edge, second_edge in pairs:
                found = False
                for state in good_states:
                    state_attempts += 1
                    if good_local_lift(
                        edges, state, first_edge, second_edge
                    ):
                        found = True
                        break
                assert found
                graph_root_pairs += 1
            print(
                f"PASS: {record} root={root} trees={len(trees)} "
                f"states={len(states)} good={len(good_states)} pairs=21"
            )
            rows += 1

    assert rows == 32
    assert graph_root_pairs == 672
    assert state_attempts == 688
    print(
        "PASS: order-8 existential square-local selection:",
        f"rows={rows}, graph/root/pairs={graph_root_pairs}, "
        f"state_attempts={state_attempts}",
    )


if __name__ == "__main__":
    main()
