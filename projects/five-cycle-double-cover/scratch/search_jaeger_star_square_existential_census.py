#!/usr/bin/env python3
"""Search the whole-fibre square-expansion implication on small cubic graphs.

The canonical graph stream is frozen as graph6 strings obtained with

    geng -cq -d3 -D3 N

Only simple 3-edge-connected records are tested.  For each labelled root
and each pair of independent edges avoiding it, the search asks for a
downstairs exact-good star packing having an exact-good square-local lift.
The search stops at the first graph/root/pair failure and prints every
good downstairs state, so a failure can be replayed independently.

This is a finite-census search, not a proof of the universal implication.
"""

from itertools import combinations
import argparse
import hashlib
import time


ORDER10 = (
    "I?BeeOwM?", "I?Bcu`gM?", "I?bFB_wF?", "I?bEHow[?",
    "I?`bfAWF?", "I?`cu`oJ?", "I?`cspoX?", "I?`bM_we?",
    "I?`cm`gM?", "I?`cmPoM?", "I?`amQoM?", "I?`c]`oM?",
    "ICOfBaKF?", "ICOf@pSb?", "ICOef?kF?", "ICOedPKL?",
    "ICOedO[X?", "ICQRD_kQ_", "ICQRD_iR?",
)

ORDER12 = (
    "K??FEb_F?wD_", "K??FEbGL@WB_", "K??FEagT@WB_",
    "K??FEaKY@gB_", "K??FEaKR@oE_", "K?AEF@oM?w@o",
    "K?AEB`gHcoB_", "K?AEEHaM@oB_", "K?AEEDcF@oF?",
    "K?AEDDWX@oB_", "K?ABF@ce?sB_", "K?ABEb_J?sB_",
    "K?ABEagE`gH_", "K?ABE`Ke@gDO", "K?ABE`Ke@WEO",
    "K?ABBb_e?[B_", "K?ABBb_E_wP_", "K?ABB`gc_wP_",
    "K?ABB`gEcgP_", "K?ABCqWUBGCo", "K?ABArOb@WEO",
    "K?ABApok?[P_", "K?ABApoMCWOo", "K?ABApoc`WP_",
    "K?ABArCe@gDO", "K?ABCiWRB_DO", "K?ABCiWFBOKO",
    "K?ABCiKU@oKO", "K?ABEDoM?wP_", "K?ABEDWM?wS_",
    "K?ABEESU@WF?", "K?ABBF_e?wB_", "K?ABBFOe@WB_",
    "K?ABBFOb@oB_", "K?ABBFCe@oB_", "K?ABCfOY?wD_",
    "K?ABCfOR@oD_", "K?ABCfGT@oD_", "K?ABCeWU@WK_",
    "K?ABCdWT@WT?", "K?ABCfCY?wF?", "K?ABCfCU@WF?",
    "K?ABAdoi?wP_", "K?ABAdgi?wQ_", "K?ABAfCi?wF?",
    "K?AB?vOTDOD_", "K?AB?tos@WP_", "K?ABCN_U?wF?",
    "K?ABCNOY?wF?", "K?BD?qcKaoHG", "K?BD?pck?sHG",
    "K?BD?pSw@SBG", "K?`@F@gd?sAo", "K?`@Eb_M?k@o",
    "K?`@Eb_J?sAo", "K?`@Eb_F?[EO", "K?`@E`gh?sAo",
    "K?`@E`gFCcCo", "K?`@E`gFCKEO", "K?`@E`gEcKE_",
    "K?`@E`Wh?kDO", "K?`@EaKY?kEO", "K?`@EaKX?sEO",
    "K?`@EROM?kCo", "K?`@EQgLAcAo", "K?`@EQK[?kEO",
    "K?`@Cr_T?[EO", "K?`@CrGX?kEO", "K?`@CrGT@KEO",
    "K?`@CqW[AKCo", "K?`@CrCY?kEO", "K?`DAagK_iH_",
    "K?`D@`gE_iW_", "K?`D@`cS_wPG", "K?`D@bAJAgBG",
    "K?`D@`ae?iH_", "K?`D@aQY?wGg", "K?`@`ago_YI_",
    "K?`CRAWK`gGg", "K?`CPbGP`gEG", "K?`CPbGHb_Ag",
    "K?`CPag[?kGg", "K?`CPagXAcAg", "K?`CPagWagAg",
    "K?`CPagPagEG",
)

LOCAL_MASKS_BY_SIZE = {
    size: tuple(
        mask for mask in range(256) if mask.bit_count() == size
    )
    for size in range(9)
}


def decode_graph6(record):
    assert 1 <= ord(record[0]) - 63 < 63
    vertex_count = ord(record[0]) - 63
    bits = "".join(f"{ord(character) - 63:06b}" for character in record[1:])
    edges = []
    position = 0
    for right in range(1, vertex_count):
        for left in range(right):
            if bits[position] == "1":
                edges.append((left, right))
            position += 1
    assert all(bit == "0" for bit in bits[position:])
    return vertex_count, tuple(edges)


def verify_fixed_cover_square_lemma():
    """Exhaust the ten possible two-subset labels on five points."""
    pairs = tuple(
        frozenset(pair) for pair in combinations(range(5), 2)
    )
    for first in pairs:
        for second in pairs:
            extends = any(
                all(len(label) == 2 for label in (
                    local,
                    local ^ second,
                    local ^ first ^ second,
                    local ^ first,
                ))
                for local in pairs
            )
            assert extends == (
                first == second or first.isdisjoint(second)
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
    return True


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
    answer = set()
    for vertex in reversed(order[1:]):
        if sizes[vertex] & 1:
            answer.add(parent_edge[vertex])
        sizes[parent[vertex]] += sizes[vertex]
    return frozenset(answer)


def components(vertex_count, edges, selected):
    adjacency = [[] for _ in range(vertex_count)]
    for edge_index in selected:
        left, right = edges[edge_index]
        adjacency[left].append(right)
        adjacency[right].append(left)
    answer = []
    seen = set()
    for start in range(vertex_count):
        if start in seen:
            continue
        component = {start}
        seen.add(start)
        queue = [start]
        for vertex in queue:
            for neighbour in adjacency[vertex]:
                if neighbour not in seen:
                    component.add(neighbour)
                    seen.add(neighbour)
                    queue.append(neighbour)
        answer.append(component)
    return answer


def defect_profile(vertex_count, edges, state):
    kernels = tuple(
        odd_kernel(vertex_count, edges, tree) for tree in state
    )
    profile = []
    for coordinate in range(3):
        first, second = [
            index for index in range(3) if index != coordinate
        ]
        pure = kernels[first] & kernels[second]
        defect = 0
        for component in components(
            vertex_count, edges, kernels[coordinate]
        ):
            crossings = sum(
                ((edges[edge_index][0] in component)
                 != (edges[edge_index][1] in component))
                for edge_index in pure
            )
            defect += crossings & 1
        profile.append(defect)
    return tuple(profile)


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


def is_three_edge_connected(vertex_count, edges):
    return all(
        connected_after_deleting(vertex_count, edges, deleted)
        for size in (1, 2)
        for deleted in combinations(range(len(edges)), size)
    )


def spanning_trees(vertex_count, edges):
    return tuple(
        sum(1 << edge_index for edge_index in chosen)
        for chosen in combinations(range(len(edges)), vertex_count - 1)
        if is_tree(vertex_count, edges, chosen)
    )


def state_generator(vertex_count, edges, root, trees):
    tree_lookup = set(trees)
    all_edges = (1 << len(edges)) - 1
    root_edges = sum(
        1 << edge_index
        for edge_index, edge in enumerate(edges)
        if root in edge
    )
    nonroot_edges = all_edges ^ root_edges
    for first in trees:
        for second in trees:
            if first & second & root_edges:
                continue
            if (first | second) & nonroot_edges != nonroot_edges:
                continue
            third = (
                (root_edges & ~(first | second))
                | (nonroot_edges & (first ^ second))
            )
            if third not in tree_lookup:
                continue
            yield tuple(
                frozenset(
                    edge_index
                    for edge_index in range(len(edges))
                    if tree >> edge_index & 1
                )
                for tree in (first, second, third)
            )


def eligible_pairs(edges, root):
    return tuple(
        pair
        for pair in combinations(range(len(edges)), 2)
        if root not in edges[pair[0]]
        and root not in edges[pair[1]]
        and len(set(edges[pair[0]] + edges[pair[1]])) == 4
    )


def good_local_lift(vertex_count, edges, state, removed_pair):
    removed = set(removed_pair)
    outside_edges = tuple(
        edge for edge_index, edge in enumerate(edges)
        if edge_index not in removed
    )
    down_to_outside = {}
    for edge_index in range(len(edges)):
        if edge_index not in removed:
            down_to_outside[edge_index] = len(down_to_outside)
    outside_parts = tuple(
        frozenset(
            down_to_outside[edge_index]
            for edge_index in tree
            if edge_index not in removed
        )
        for tree in state
    )
    first_edge, second_edge = removed_pair
    A, C = edges[first_edge]
    B, D = edges[second_edge]
    a, b, c, d = range(vertex_count, vertex_count + 4)
    gadget_edges = (
        (A, a), (B, b), (C, c), (D, d),
        (a, b), (b, c), (c, d), (d, a),
    )
    up_edges = outside_edges + gadget_edges
    local_offset = len(outside_edges)
    options = []
    for tree_index in range(3):
        candidates = []
        required_local_size = (
            vertex_count + 3 - len(outside_parts[tree_index])
        )
        for local_mask in LOCAL_MASKS_BY_SIZE[required_local_size]:
            local = frozenset(
                local_offset + index
                for index in range(8)
                if local_mask >> index & 1
            )
            lifted = outside_parts[tree_index] | local
            if is_tree(vertex_count + 4, up_edges, lifted):
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
            state_up = (tree_zero, tree_one, tree_two)
            if 0 in defect_profile(vertex_count + 4, up_edges, state_up):
                return state_up
    return None


def census(records, verbose):
    started = time.monotonic()
    witness_digest = hashlib.sha256()
    checked_graphs = 0
    checked_rows = 0
    checked_pairs = 0
    attempts = 0
    skipped = 0
    for graph_index, record in enumerate(records):
        vertex_count, edges = decode_graph6(record)
        assert len(edges) == 3 * vertex_count // 2
        assert all(left < right for left, right in edges)
        assert len(set(edges)) == len(edges)
        assert all(
            sum(vertex in edge for edge in edges) == 3
            for vertex in range(vertex_count)
        )
        if not is_three_edge_connected(vertex_count, edges):
            skipped += 1
            continue
        trees = spanning_trees(vertex_count, edges)
        checked_graphs += 1
        graph_max_states = 0
        graph_max_good = 0
        for root in range(vertex_count):
            unresolved = set(eligible_pairs(edges, root))
            good_count = 0
            state_count = 0
            good_states = []
            for state in state_generator(
                vertex_count, edges, root, trees
            ):
                state_count += 1
                profile = defect_profile(vertex_count, edges, state)
                if 0 not in profile:
                    continue
                good_count += 1
                good_states.append(state)
                for pair in sorted(unresolved):
                    attempts += 1
                    lifted = good_local_lift(
                        vertex_count, edges, state, pair
                    )
                    if lifted is not None:
                        witness_digest.update(repr((
                            record,
                            root,
                            pair,
                            tuple(tuple(sorted(tree)) for tree in state),
                            tuple(tuple(sorted(tree)) for tree in lifted),
                        )).encode("ascii"))
                        unresolved.remove(pair)
                if not unresolved:
                    break
            if unresolved:
                if good_count == 0:
                    print(
                        "VACUOUS:",
                        f"record={record} root={root} "
                        "has no exact-good downstairs state",
                        flush=True,
                    )
                    continue
                print(
                    "FAIL:",
                    f"record={record} root={root} "
                    f"pairs={sorted(unresolved)} "
                    f"states={state_count} good={good_count}",
                    flush=True,
                )
                for state in good_states:
                    print(
                        "GOOD_STATE:",
                        tuple(sorted(tree) for tree in state),
                        flush=True,
                    )
                return False
            checked_rows += 1
            checked_pairs += len(eligible_pairs(edges, root))
            graph_max_states = max(graph_max_states, state_count)
            graph_max_good = max(graph_max_good, good_count)
            if verbose:
                print(
                    "PASS:",
                    f"graph={graph_index + 1}/{len(records)} "
                    f"record={record} root={root} trees={len(trees)} "
                    f"states_to_cover={state_count} "
                    f"good_to_cover={good_count}",
                    flush=True,
                )
        print(
            "PASS:",
            f"graph={graph_index + 1}/{len(records)} record={record} "
            f"trees={len(trees)} roots={vertex_count} "
            f"max_states_to_cover={graph_max_states} "
            f"max_good_to_cover={graph_max_good}",
            flush=True,
        )
    expected_counts = {
        19: (14, 140, 6300),
        85: (57, 684, 53352),
    }
    assert (
        checked_graphs,
        checked_rows,
        checked_pairs,
    ) == expected_counts[len(records)]
    print(
        "PASS: existential square census:",
        f"records={len(records)} 3ec={checked_graphs} skipped={skipped} "
        f"rows={checked_rows} pairs={checked_pairs} "
        f"local_attempts={attempts} "
        f"witness_sha256={witness_digest.hexdigest()} "
        f"seconds={time.monotonic() - started:.3f}",
        flush=True,
    )
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, choices=(10, 12), required=True)
    parser.add_argument("--verbose", action="store_true")
    arguments = parser.parse_args()
    records = {10: ORDER10, 12: ORDER12}[arguments.order]
    expected = {
        10: (19, 14, 140, 6300),
        12: (85, 57, 684, 53352),
    }
    assert len(records) == expected[arguments.order][0]
    assert len(set(records)) == len(records)
    verify_fixed_cover_square_lemma()
    assert census(records, arguments.verbose)


if __name__ == "__main__":
    main()
