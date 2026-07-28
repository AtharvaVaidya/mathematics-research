#!/usr/bin/env python3
"""Exhaust the order-six controls for statewise square lifting.

The two connected simple cubic graphs on six vertices are K_3,3 and the
triangular prism.  Both are vertex-transitive, so root 0 represents every
root orbit.  For every good root-0 star state and every eligible pair of
independent nonroot edges, this script finds a square-local lift good in
at least one coordinate.
"""

from itertools import combinations

from verify_jaeger_star_square_any_coordinate_lift_countermodel import (
    defect_profile,
    is_tree,
)


K33_EDGES = (
    (0, 3), (0, 4), (0, 5),
    (1, 3), (1, 4), (1, 5),
    (2, 3), (2, 4), (2, 5),
)

PRISM_EDGES = (
    (0, 1), (0, 2), (0, 3),
    (1, 2), (1, 4), (2, 5),
    (3, 4), (3, 5), (4, 5),
)


def all_star_states(edges, root=0):
    vertex_count = 6
    trees = [
        frozenset(chosen)
        for chosen in combinations(range(len(edges)), vertex_count - 1)
        if is_tree(vertex_count, edges, frozenset(chosen))
    ]
    expected = [1 if root in edge else 2 for edge in edges]
    tree_lookup = set(trees)
    states = []
    for first in trees:
        for second in trees:
            remaining = []
            valid = True
            for edge_index in range(len(edges)):
                count = (
                    expected[edge_index]
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
                states.append((first, second, third))
    return states


def eligible_pairs(edges, root=0):
    answer = []
    for first, second in combinations(range(len(edges)), 2):
        edge_first = edges[first]
        edge_second = edges[second]
        if root in edge_first or root in edge_second:
            continue
        if len(set(edge_first + edge_second)) == 4:
            answer.append((first, second))
    return answer


def local_lifts(vertex_count, edges, trees, first_edge, second_edge):
    removed = {first_edge, second_edge}
    outside_edges = tuple(
        edge for edge_index, edge in enumerate(edges)
        if edge_index not in removed
    )
    down_to_outside = {}
    outside_index = 0
    for edge_index in range(len(edges)):
        if edge_index not in removed:
            down_to_outside[edge_index] = outside_index
            outside_index += 1
    fixed_outside = tuple(
        frozenset(
            down_to_outside[edge_index]
            for edge_index in tree
            if edge_index not in removed
        )
        for tree in trees
    )

    # AC is first_edge and BD is second_edge.
    A, C = edges[first_edge]
    B, D = edges[second_edge]
    a, b, c, d = range(vertex_count, vertex_count + 4)
    gadget_edges = (
        (A, a), (B, b), (C, c), (D, d),
        (a, b), (b, c), (c, d), (d, a),
    )
    up_edges = outside_edges + gadget_edges
    offset = len(outside_edges)

    options = []
    for tree_index in range(3):
        candidates = []
        for local_mask in range(1 << 8):
            local = {
                offset + edge_index
                for edge_index in range(8)
                if local_mask >> edge_index & 1
            }
            lifted = fixed_outside[tree_index] | local
            if is_tree(vertex_count + 4, up_edges, lifted):
                omitted = 255 ^ local_mask
                candidates.append((omitted, lifted))
        options.append(candidates)

    third_by_omitted = dict(options[2])
    for omitted_zero, tree_zero in options[0]:
        for omitted_one, tree_one in options[1]:
            if omitted_zero & omitted_one:
                continue
            omitted_two = 255 ^ omitted_zero ^ omitted_one
            tree_two = third_by_omitted.get(omitted_two)
            if tree_two is not None:
                yield up_edges, (tree_zero, tree_one, tree_two)


def has_good_local_lift(edges, state, edge_pair):
    for up_edges, lifted in local_lifts(6, edges, state, *edge_pair):
        profile, _ = defect_profile(10, up_edges, lifted)
        if 0 in profile:
            return True
    return False


def check_graph(name, edges, expected_states, expected_good_states):
    states = all_star_states(edges)
    pairs = eligible_pairs(edges)
    assert len(states) == expected_states
    assert len(pairs) == 6

    good_states = []
    for state in states:
        profile, _ = defect_profile(6, edges, state)
        if 0 in profile:
            good_states.append(state)
    assert len(good_states) == expected_good_states

    checked = 0
    for state in good_states:
        for edge_pair in pairs:
            assert has_good_local_lift(edges, state, edge_pair)
            checked += 1
    assert checked == expected_good_states * 6
    print(
        f"PASS: {name}: states={len(states)}, good_states={len(good_states)}, "
        f"eligible_pairs={len(pairs)}, state/pair instances={checked}"
    )


def main():
    check_graph("K_3,3", K33_EDGES, 288, 288)
    check_graph("triangular prism", PRISM_EDGES, 216, 156)
    print("PASS: every order-six good state has an any-coordinate good lift")


if __name__ == "__main__":
    main()
