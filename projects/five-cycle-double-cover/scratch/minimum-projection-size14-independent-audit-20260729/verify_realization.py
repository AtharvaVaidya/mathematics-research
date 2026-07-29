#!/usr/bin/env python3
"""Second independent cubic realization and projection-semantics audit."""

from itertools import combinations


ORDER = 18
WORD = tuple(map(int, "01010230101232"))
PENDANT = tuple(map(int, "31111212111311"))
EDGES = []
for offset in (0, 7):
    EDGES.extend(
        (offset + local, offset + (local + 1) % 7)
        for local in range(7)
    )
EDGES.extend(((0, 11), (1, 9), (2, 12), (3, 10)))
# The six-vertex boundary block is realized by the unique unlabelled cubic
# tree shape compatible with a nonzero extension: a four-internal-vertex path.
EDGES.extend((
    (4, 14), (5, 14), (6, 15), (13, 16), (8, 17), (7, 17),
    (14, 15), (15, 16), (16, 17),
))
EDGES = tuple(EDGES)
TARGET = (1 << 14) - 1
CANONICAL_GRAPH6 = "Qs???SC@GS@_CDOoC@@@?O?CO?g"


def connected(omitted=None):
    adjacency = [[] for _ in range(ORDER)]
    for index, (first, second) in enumerate(EDGES):
        if index == omitted:
            continue
        adjacency[first].append(second)
        adjacency[second].append(first)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbour in adjacency[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return len(seen) == ORDER


def tait_colourable():
    used = [0] * ORDER
    colours = [-1] * len(EDGES)

    def recurse(remaining):
        if not remaining:
            return True
        edge = max(
            remaining,
            key=lambda index: (
                used[EDGES[index][0]] | used[EDGES[index][1]]
            ).bit_count(),
        )
        first, second = EDGES[edge]
        forbidden = used[first] | used[second]
        rest = remaining - {edge}
        for colour in range(3):
            bit = 1 << colour
            if forbidden & bit:
                continue
            colours[edge] = colour
            used[first] |= bit
            used[second] |= bit
            if recurse(rest):
                return True
            used[first] ^= bit
            used[second] ^= bit
            colours[edge] = -1
        return False

    return recurse(set(range(len(EDGES))))


def spanning_tree_and_chords():
    adjacency = [[] for _ in range(ORDER)]
    for index, (first, second) in enumerate(EDGES):
        adjacency[first].append((second, index))
        adjacency[second].append((first, index))
    parent = [-1] * ORDER
    parent_edge = [-1] * ORDER
    parent[0] = 0
    queue = [0]
    tree_edges = set()
    for vertex in queue:
        for neighbour, edge in adjacency[vertex]:
            if parent[neighbour] >= 0:
                continue
            parent[neighbour] = vertex
            parent_edge[neighbour] = edge
            tree_edges.add(edge)
            queue.append(neighbour)
    assert len(queue) == ORDER
    chords = [
        index for index in range(len(EDGES)) if index not in tree_edges
    ]
    return parent, parent_edge, chords


def tree_path_mask(first, second, parent, parent_edge):
    first_path = {}
    mask = 0
    vertex = first
    while vertex:
        first_path[vertex] = mask
        mask ^= 1 << parent_edge[vertex]
        vertex = parent[vertex]
    first_path[0] = mask

    mask = 0
    vertex = second
    while vertex not in first_path:
        mask ^= 1 << parent_edge[vertex]
        vertex = parent[vertex]
    return mask ^ first_path[vertex]


def cycle_space():
    parent, parent_edge, chords = spanning_tree_and_chords()
    basis = []
    for edge in chords:
        first, second = EDGES[edge]
        basis.append(
            (1 << edge)
            ^ tree_path_mask(first, second, parent, parent_edge)
        )
    assert len(basis) == len(EDGES) - ORDER + 1 == 10
    cycles = []
    for choice in range(1 << len(basis)):
        mask = 0
        for index, value in enumerate(basis):
            if (choice >> index) & 1:
                mask ^= value
        cycles.append(mask)
    assert len(set(cycles)) == 1024
    return tuple(cycles)


def components_without(projection):
    adjacency = [[] for _ in range(ORDER)]
    for index, (first, second) in enumerate(EDGES):
        if (projection >> index) & 1:
            continue
        adjacency[first].append(second)
        adjacency[second].append(first)
    unseen = set(range(ORDER))
    result = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        stack = [root]
        while stack:
            vertex = stack.pop()
            for neighbour in adjacency[vertex]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    component.add(neighbour)
                    stack.append(neighbour)
        result.append(frozenset(component))
    return tuple(result)


def clean_intersection(projection, intersection):
    for component in components_without(projection):
        parity = 0
        for index, (first, second) in enumerate(EDGES):
            if not ((projection >> index) & 1):
                continue
            if (first in component) == (second in component):
                continue
            parity ^= (intersection >> index) & 1
        if parity:
            return False
    return True


def semantic_states(cycles):
    return tuple({
        (first | second, first & second)
        for first in cycles for second in cycles
    })


def target_ordered_extension_counts(cycles):
    all_edges = (1 << len(EDGES)) - 1
    complement = all_edges ^ TARGET
    extensions = 0
    clean = 0
    for first in cycles:
        for second in cycles:
            if complement & ~(first | second):
                continue
            extensions += 1
            clean += clean_intersection(TARGET, first & second)
    return extensions, clean


def k33_subdivision_certificate():
    left = {2, 10, 16}
    right = {3, 9, 12}
    paths = (
        (2, 3),
        (2, 1, 9),
        (2, 12),
        (10, 3),
        (10, 9),
        (10, 11, 12),
        (16, 15, 14, 4, 3),
        (16, 17, 8, 9),
        (16, 13, 12),
    )
    graph_edges = {tuple(sorted(edge)) for edge in EDGES}
    endpoints = set()
    internal = set()
    for path in paths:
        assert path[0] in left and path[-1] in right
        endpoints.add((path[0], path[-1]))
        for first, second in zip(path, path[1:]):
            assert tuple(sorted((first, second))) in graph_edges
        assert not (set(path[1:-1]) & internal)
        internal.update(path[1:-1])
    assert endpoints == {(first, second) for first in left for second in right}
    assert not (internal & (left | right))
    return paths


def profile():
    cycles = cycle_space()
    states = semantic_states(cycles)
    all_edges = (1 << len(EDGES)) - 1
    properties = {}
    for projection in sorted(cycles, key=int.bit_count):
        complement = all_edges ^ projection
        liftable = False
        cleanable = False
        for union, intersection in states:
            if complement & ~union:
                continue
            liftable = True
            if clean_intersection(projection, intersection):
                cleanable = True
                break
        properties[projection] = (liftable, cleanable)
    liftable = [
        projection for projection, row in properties.items() if row[0]
    ]
    minimum = min(projection.bit_count() for projection in liftable)
    minima = [
        projection for projection in liftable
        if projection.bit_count() == minimum
    ]
    return cycles, states, properties, minimum, minima


def explicit_target_flow():
    low = [None] * len(EDGES)
    low[:14] = WORD
    # Four two-terminal components.
    low[14:18] = (3, 1, 1, 1)
    # Six leaf edges in the order displayed above.
    low[18:24] = (1, 2, 1, 1, 1, 2)
    # Internal path values are the boundary XORs on one side.
    low[24:27] = (3, 2, 3)
    assert all(value is not None and value != 0
               for value in low[14:])
    for vertex in range(ORDER):
        total = 0
        for index, edge in enumerate(EDGES):
            if vertex in edge:
                total ^= low[index]
        assert total == 0
    return tuple(low)


def main():
    assert len(EDGES) == 27
    assert len({tuple(sorted(edge)) for edge in EDGES}) == 27
    degrees = [0] * ORDER
    for first, second in EDGES:
        assert first != second
        degrees[first] += 1
        degrees[second] += 1
    assert degrees == [3] * ORDER
    assert connected()
    assert all(connected(omitted=index) for index in range(len(EDGES)))
    explicit_target_flow()
    tait = tait_colourable()
    cycles, states, properties, minimum, minima = profile()
    ordered_extensions, ordered_clean = target_ordered_extension_counts(
        cycles
    )
    target = properties[TARGET]
    paths = k33_subdivision_certificate()
    print("order", ORDER, "size", len(EDGES))
    print("simple_connected_cubic_bridgeless", True)
    print("tait_colourable", tait)
    print("cycle_space", len(cycles), "semantic_states", len(states))
    print("target_size", TARGET.bit_count())
    print("target_liftable_cleanable", target)
    print("target_ordered_extensions", ordered_extensions)
    print("target_ordered_clean_extensions", ordered_clean)
    print("minimum_extendable_size", minimum)
    print("minimum_count", len(minima))
    print(
        "minimum_clean_count",
        sum(properties[projection][1] for projection in minima),
    )
    print("minimum_masks", minima)
    print("canonical_graph6", CANONICAL_GRAPH6)
    print("k33_subdivision_paths", paths)


if __name__ == "__main__":
    main()
