#!/usr/bin/env python3
"""Independent checker for the triangular-prism fixed-label no-go.

The checker has no SAT dependency.  It verifies:

* the displayed prism star state and its exact-good defect profile;
* its compatible canonical five-point labelling;
* direct exhaustive generation of all indexed five-cycle-double-cover
  pair labellings of the prism (540 with coordinates fixed);
* the one-point intersection obstruction on the two selected cut edges;
* an explicit exact-good square-local tree lift, showing that the no-go
  does not refute the tree-local statements (L) or (F).
"""

from __future__ import annotations

from itertools import combinations, permutations


EDGES = (
    (0, 1), (0, 2), (0, 3),
    (1, 2), (1, 4), (2, 5),
    (3, 4), (3, 5), (4, 5),
)
GRAPH6 = "E{Sw"
ROOT = 0
CUT_EDGES = (2, 4, 5)
SELECTED = (4, 5)
STATE = (
    frozenset((0, 3, 4, 6, 7)),
    frozenset((1, 3, 5, 7, 8)),
    frozenset((2, 4, 5, 6, 8)),
)
CANONICAL_LABELS = (
    (0, 6), (5, 6), (0, 5),
    (4, 6), (0, 4), (4, 5),
    (0, 7), (5, 7), (4, 7),
)

# Delete original edges 4=(1,4) and 5=(2,5), preserve the other seven
# edges as 0,...,6, and append Aa,Bb,Cc,Dd,ab,bc,cd,da.
UP_EDGES = (
    (0, 1), (0, 2), (0, 3), (1, 2),
    (3, 4), (3, 5), (4, 5),
    (1, 6), (2, 7), (4, 8), (5, 9),
    (6, 7), (7, 8), (8, 9), (9, 6),
)
UP_GRAPH6 = "I{CY@CH@g"
UP_STATE = (
    frozenset((0, 3, 4, 5, 7, 9, 10, 11, 14)),
    frozenset((1, 3, 5, 6, 8, 9, 11, 12, 13)),
    frozenset((2, 4, 6, 7, 8, 10, 12, 13, 14)),
)
STATE_MASKS = (217, 426, 372)
UP_STATE_MASKS = (20153, 15210, 30164)
LOCAL_MASKS = (0b10011101, 0b01110110, 0b11101011)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def incidence(order: int, edges):
    return tuple(
        tuple(edge for edge, ends in enumerate(edges) if vertex in ends)
        for vertex in range(order)
    )


def encode_graph6(order: int, edges) -> str:
    require(0 <= order < 63, "only short graph6 supported")
    edge_set = {tuple(sorted(edge)) for edge in edges}
    bits = [
        int((left, right) in edge_set)
        for right in range(1, order)
        for left in range(right)
    ]
    while len(bits) % 6:
        bits.append(0)
    chunks = [
        sum(bits[offset + index] << (5 - index) for index in range(6))
        for offset in range(0, len(bits), 6)
    ]
    return chr(order + 63) + "".join(chr(chunk + 63) for chunk in chunks)


def is_tree(order: int, edges, selected) -> bool:
    if len(selected) != order - 1:
        return False
    parent = list(range(order))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in selected:
        left, right = map(find, edges[edge])
        if left == right:
            return False
        parent[left] = right
    return True


def connected_after_deleting(order: int, edges, deleted) -> bool:
    rows = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        if edge in deleted:
            continue
        rows[left].append(right)
        rows[right].append(left)
    seen = {0}
    queue = [0]
    for vertex in queue:
        for neighbour in rows[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return len(seen) == order


def check_graph(order: int, edges) -> None:
    require(len(set(edges)) == len(edges), "parallel edge")
    require(all(left != right for left, right in edges), "loop")
    rows = incidence(order, edges)
    require(all(len(row) == 3 for row in rows), "not cubic")
    for size in (0, 1, 2):
        for deleted in combinations(range(len(edges)), size):
            require(
                connected_after_deleting(order, edges, set(deleted)),
                "not three-edge-connected",
            )


def odd_kernel(order: int, edges, tree):
    rows = [[] for _ in range(order)]
    for edge in tree:
        left, right = edges[edge]
        rows[left].append((right, edge))
        rows[right].append((left, edge))
    parent = [-1] * order
    parent_edge = [-1] * order
    traversal = [0]
    parent[0] = 0
    for vertex in traversal:
        for neighbour, edge in rows[vertex]:
            if parent[neighbour] == -1:
                parent[neighbour] = vertex
                parent_edge[neighbour] = edge
                traversal.append(neighbour)
    require(len(traversal) == order, "tree traversal failed")
    sizes = [1] * order
    kernel = set()
    for vertex in reversed(traversal[1:]):
        if sizes[vertex] & 1:
            kernel.add(parent_edge[vertex])
        sizes[parent[vertex]] += sizes[vertex]
    return frozenset(kernel)


def components(order: int, edges, selected):
    rows = [[] for _ in range(order)]
    for edge in selected:
        left, right = edges[edge]
        rows[left].append(right)
        rows[right].append(left)
    unseen = set(range(order))
    answer = []
    while unseen:
        start = next(iter(unseen))
        component = {start}
        unseen.remove(start)
        queue = [start]
        for vertex in queue:
            for neighbour in rows[vertex]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    component.add(neighbour)
                    queue.append(neighbour)
        answer.append(component)
    return tuple(answer)


def defect_profile(order: int, edges, state):
    kernels = tuple(odd_kernel(order, edges, tree) for tree in state)
    profile = []
    for coordinate in range(3):
        first, second = tuple(i for i in range(3) if i != coordinate)
        pure = kernels[first] & kernels[second]
        defect = 0
        for component in components(order, edges, kernels[coordinate]):
            crossings = sum(
                (edges[edge][0] in component) != (edges[edge][1] in component)
                for edge in pure
            )
            defect += crossings & 1
        profile.append(defect)
    return tuple(profile), kernels


def check_star_state(order: int, edges, state) -> None:
    require(all(is_tree(order, edges, tree) for tree in state), "not trees")
    for edge, ends in enumerate(edges):
        expected = 1 if ROOT in ends else 2
        actual = sum(edge in tree for tree in state)
        require(actual == expected, f"wrong multiplicity at edge {edge}")


def check_canonical_labelling(kernels) -> None:
    # The good coordinate is old bit 1.  Send old bits (0,2,1) to new
    # bits (0,1,2), making its kernel the canonical plane {0,1,2,3}.
    flow = tuple(
        sum((edge not in kernels[coordinate]) << coordinate
            for coordinate in range(3))
        for edge in range(len(EDGES))
    )
    normalized = tuple(
        ((value >> 0) & 1)
        | (((value >> 2) & 1) << 1)
        | (((value >> 1) & 1) << 2)
        for value in flow
    )
    require(normalized == (6, 3, 5, 2, 4, 1, 7, 2, 3), "flow mismatch")
    for edge, pair in enumerate(CANONICAL_LABELS):
        require(len(pair) == 2 and pair[0] != pair[1], "not a pair")
        require(pair[0] ^ pair[1] == normalized[edge], "wrong pair difference")
    for row in incidence(6, EDGES):
        for point in range(8):
            require(
                sum(point in CANONICAL_LABELS[edge] for edge in row) % 2 == 0,
                "pair labelling is not locally compatible",
            )
    require(
        set(CANONICAL_LABELS[SELECTED[0]])
        & set(CANONICAL_LABELS[SELECTED[1]])
        == {4},
        "selected canonical labels do not meet once",
    )


def enumerate_all_five_cover_labellings() -> int:
    """Directly enumerate all indexed five-cover pair labellings."""
    rows = incidence(6, EDGES)
    local_options = []
    for points in combinations(range(5), 3):
        triangle = tuple(combinations(points, 2))
        local_options.extend(permutations(triangle))
    labels: list[tuple[int, int] | None] = [None] * len(EDGES)
    assigned = [False] * 6
    count = 0

    def recurse(remaining: int) -> None:
        nonlocal count
        if remaining == 0:
            count += 1
            cut_labels = tuple(set(labels[edge]) for edge in CUT_EDGES)
            require(
                cut_labels[0] ^ cut_labels[1] ^ cut_labels[2] == set(),
                "cut parity failed",
            )
            for first, second in combinations(cut_labels, 2):
                require(
                    len(first & second) == 1,
                    "an extendible cut-edge pair was found",
                )
            return
        vertex = max(
            (v for v in range(6) if not assigned[v]),
            key=lambda v: sum(labels[edge] is not None for edge in rows[v]),
        )
        assigned[vertex] = True
        for option in local_options:
            if any(
                labels[edge] is not None and labels[edge] != option[slot]
                for slot, edge in enumerate(rows[vertex])
            ):
                continue
            new_edges = []
            for slot, edge in enumerate(rows[vertex]):
                if labels[edge] is None:
                    labels[edge] = option[slot]
                    new_edges.append(edge)
            recurse(remaining - 1)
            for edge in new_edges:
                labels[edge] = None
        assigned[vertex] = False

    recurse(6)
    require(count == 540, "unexpected complete labelling count")
    return count


def main() -> None:
    check_graph(6, EDGES)
    require(encode_graph6(6, EDGES) == GRAPH6, "downstairs graph6 mismatch")
    require(
        tuple(sum(1 << edge for edge in tree) for tree in STATE) == STATE_MASKS,
        "downstairs state-mask mismatch",
    )
    check_star_state(6, EDGES, STATE)
    profile, kernels = defect_profile(6, EDGES, STATE)
    require(profile == (2, 0, 2), "wrong downstairs defect profile")
    require(
        kernels
        == (
            frozenset((0, 3, 4, 7)),
            frozenset((1, 3, 5, 7, 8)),
            frozenset((2, 4, 5)),
        ),
        "wrong downstairs odd kernels",
    )
    check_canonical_labelling(kernels)
    count = enumerate_all_five_cover_labellings()

    check_graph(10, UP_EDGES)
    require(encode_graph6(10, UP_EDGES) == UP_GRAPH6, "upstairs graph6 mismatch")
    require(
        tuple(sum(1 << edge for edge in tree) for tree in UP_STATE)
        == UP_STATE_MASKS,
        "upstairs state-mask mismatch",
    )
    require(
        tuple(
            sum(1 << (edge - 7) for edge in tree if edge >= 7)
            for tree in UP_STATE
        )
        == LOCAL_MASKS,
        "local gadget-mask mismatch",
    )
    check_star_state(10, UP_EDGES, UP_STATE)
    up_profile, _ = defect_profile(10, UP_EDGES, UP_STATE)
    require(up_profile == (2, 0, 2), "wrong lifted defect profile")

    print(
        "PASS: triangular prism; 540 indexed five-cover labellings; "
        "all three matching-cut labels meet pairwise once; "
        "downstairs and square-local lifted profiles both (2,0,2)"
    )


if __name__ == "__main__":
    main()
