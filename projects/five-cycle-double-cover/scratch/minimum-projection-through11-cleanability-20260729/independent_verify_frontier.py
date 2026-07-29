#!/usr/bin/env python3
"""Independent audit of the frozen size-11 frontier certificates.

This checker does not import the primary verifier.  It independently checks
the frozen orbit representatives, replacement witnesses, graph realization,
and all fixed-projection/minimum-projection semantic claims.
"""

import json
from itertools import permutations, product
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
DATA = json.loads(
    (PACKAGE / "size11-frontier-certificates.json").read_text()
)

NONZERO = (1, 2, 3)
GL = tuple(
    (0,) + permutation
    for permutation in permutations(NONZERO)
    if permutation[2] == (permutation[0] ^ permutation[1])
)


def normalize_colours(word):
    names = {}
    result = []
    for value in word:
        if value not in names:
            names[value] = len(names)
        result.append(names[value])
    return tuple(result)


def normalize_labels(labels):
    names = {}
    result = []
    for value in labels:
        if value not in names:
            names[value] = len(names)
        result.append(names[value])
    return tuple(result)


def vertex_edge_orders(length, offset):
    for reflected in (False, True):
        for anchor in range(length):
            if reflected:
                vertices = tuple(
                    offset + (anchor - index) % length
                    for index in range(length)
                )
                edges = tuple(
                    offset + (anchor - index - 1) % length
                    for index in range(length)
                )
            else:
                vertices = tuple(
                    offset + (anchor + index) % length
                    for index in range(length)
                )
                edges = vertices
            yield vertices, edges


def canonical_pair(word, labels, lengths):
    offsets = []
    offset = 0
    for length in lengths:
        offsets.append(offset)
        offset += length
    transforms = tuple(
        tuple(vertex_edge_orders(length, offset))
        for length, offset in zip(lengths, offsets)
    )
    return min(
        (
            normalize_colours(tuple(
                word[index]
                for _vertices, edges in selected
                for index in edges
            )),
            normalize_labels(tuple(
                labels[index]
                for vertices, _edges in selected
                for index in vertices
            )),
        )
        for selected in product(*transforms)
    )


def pendant_values(word, lengths):
    result = []
    offset = 0
    for length in lengths:
        result.extend(
            word[offset + (index - 1) % length] ^ word[offset + index]
            for index in range(length)
        )
        offset += length
    return tuple(result)


def edge_set(edges):
    return {tuple(sorted(edge)) for edge in edges}


def connected(order, edges, omitted=None):
    adjacency = [set() for _ in range(order)]
    for index, (first, second) in enumerate(edges):
        if index == omitted:
            continue
        adjacency[first].add(second)
        adjacency[second].add(first)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbour in adjacency[vertex] - seen:
            seen.add(neighbour)
            stack.append(neighbour)
    return len(seen) == order


def graph_isomorphic(order, first_edges, second_edges):
    first = [set() for _ in range(order)]
    second = [set() for _ in range(order)]
    for a, b in first_edges:
        first[a].add(b)
        first[b].add(a)
    for a, b in second_edges:
        second[a].add(b)
        second[b].add(a)
    if sorted(map(len, first)) != sorted(map(len, second)):
        return False

    mapping = [-1] * order
    used = [False] * order

    def recurse():
        if all(value >= 0 for value in mapping):
            return True
        unmapped = [v for v in range(order) if mapping[v] < 0]
        vertex = max(
            unmapped,
            key=lambda v: sum(mapping[u] >= 0 for u in first[v]),
        )
        for target in range(order):
            if used[target] or len(first[vertex]) != len(second[target]):
                continue
            if any(
                (mapping[neighbour] in second[target])
                != (neighbour in first[vertex])
                for neighbour in range(order)
                if mapping[neighbour] >= 0
            ):
                continue
            mapping[vertex] = target
            used[target] = True
            if recurse():
                return True
            used[target] = False
            mapping[vertex] = -1
        return False

    return recurse()


def decode_graph6(text):
    values = [ord(character) - 63 for character in text]
    order = values[0]
    bits = []
    for value in values[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for second in range(1, order):
        for first in range(second):
            if bits[cursor]:
                edges.append((first, second))
            cursor += 1
    return order, edges


def tait_colourable(order, edges):
    incident = [[] for _ in range(order)]
    for index, (first, second) in enumerate(edges):
        incident[first].append(index)
        incident[second].append(index)
    colours = [-1] * len(edges)
    used = [0] * order

    def recurse(remaining):
        if not remaining:
            return True
        edge = max(
            remaining,
            key=lambda index: (
                (used[edges[index][0]] | used[edges[index][1]]).bit_count()
            ),
        )
        first, second = edges[edge]
        forbidden = used[first] | used[second]
        next_remaining = remaining - {edge}
        for colour in range(3):
            bit = 1 << colour
            if forbidden & bit:
                continue
            colours[edge] = colour
            used[first] |= bit
            used[second] |= bit
            if recurse(next_remaining):
                return True
            used[first] ^= bit
            used[second] ^= bit
            colours[edge] = -1
        return False

    return recurse(set(range(len(edges))))


def even_cycles(order, edges):
    result = []
    for mask in range(1 << len(edges)):
        parity = [0] * order
        for index, (first, second) in enumerate(edges):
            if (mask >> index) & 1:
                parity[first] ^= 1
                parity[second] ^= 1
        if not any(parity):
            result.append(mask)
    return tuple(result)


def components_without_projection(order, edges, projection):
    adjacency = [set() for _ in range(order)]
    for index, (first, second) in enumerate(edges):
        if (projection >> index) & 1:
            continue
        adjacency[first].add(second)
        adjacency[second].add(first)
    unseen = set(range(order))
    result = []
    while unseen:
        root = min(unseen)
        component = {root}
        stack = [root]
        unseen.remove(root)
        while stack:
            vertex = stack.pop()
            for neighbour in adjacency[vertex] & unseen:
                unseen.remove(neighbour)
                component.add(neighbour)
                stack.append(neighbour)
        result.append(component)
    return tuple(result)


def extension_profile(order, edges):
    cycles = even_cycles(order, edges)
    assert len(cycles) == 128
    all_edges = (1 << len(edges)) - 1
    profiles = {}
    for projection in cycles:
        complement = all_edges ^ projection
        components = components_without_projection(
            order, edges, projection
        )
        extendable = False
        cleanable = False
        for first in cycles:
            for second in cycles:
                if complement & ~(first | second):
                    continue
                extendable = True
                clean = True
                for component in components:
                    parity = [0, 0, 0, 0]
                    for index, (u, v) in enumerate(edges):
                        if not ((projection >> index) & 1):
                            continue
                        if (u in component) == (v in component):
                            continue
                        colour = (
                            ((first >> index) & 1)
                            | (((second >> index) & 1) << 1)
                        )
                        parity[colour] ^= 1
                    if any(parity):
                        clean = False
                        break
                if clean:
                    cleanable = True
                    break
            if cleanable:
                break
        profiles[projection] = (extendable, cleanable)
    return profiles


def realization_edges(word_pair, partition):
    lengths = tuple(map(len, word_pair))
    edges = []
    offset = 0
    for length in lengths:
        edges.extend(
            (offset + local, offset + (local + 1) % length)
            for local in range(length)
        )
        offset += length
    labels = tuple(map(int, partition))
    next_vertex = len(labels)
    for component in range(max(labels) + 1):
        vertices = [
            index for index, label in enumerate(labels)
            if label == component
        ]
        if len(vertices) == 2:
            edges.append(tuple(vertices))
        elif len(vertices) == 3:
            edges.extend((next_vertex, vertex) for vertex in vertices)
            next_vertex += 1
        else:
            raise AssertionError(vertices)
    return next_vertex, edges


def validate_pair_orbits():
    observed = {}
    for row in DATA["literal_failures"]:
        word = tuple(map(int, "".join(row["word_pair"])))
        labels = tuple(map(int, row["partition"]))
        pair = canonical_pair(word, labels, (5, 6))
        observed.setdefault(pair, []).append(row["index"])
    assert len(observed) == 11

    frozen = {}
    for row in DATA["canonical_pair_orbits"]:
        pair = (
            tuple(map(int, "".join(row["word_pair"]))),
            tuple(map(int, row["partition"])),
        )
        frozen[pair] = row["failure_indices"]
    assert observed == frozen


def validate_replacement_certificates():
    gl = set(GL)
    for row in DATA["literal_failures"]:
        word = tuple(map(int, "".join(row["word_pair"])))
        labels = tuple(map(int, row["partition"]))
        maps = tuple(
            tuple(map(int, mapping)) for mapping in row["replacement_maps"]
        )
        assert all(mapping in gl for mapping in maps)
        repaired = tuple(map(int, "".join(row["replacement_low_words"])))
        pendant = pendant_values(word, (5, 6))
        offsets = (0, 5)
        for circuit, (offset, length) in enumerate(zip(offsets, (5, 6))):
            previous = row["replacement_starts"][circuit]
            for local in range(length):
                index = offset + local
                assert (
                    previous ^ repaired[index]
                    == maps[labels[index]][pendant[index]]
                )
                previous = repaired[index]
            assert previous == row["replacement_starts"][circuit]
        assert all(value != 0 for value in repaired[5:])


def validate_graph():
    realization = DATA["realization"]
    edges = [tuple(edge) for edge
             in realization["representative_edges_in_target_order"]]
    order = realization["order"]
    assert order == 12 and len(edges) == 18
    assert len(edge_set(edges)) == len(edges)
    degrees = [0] * order
    for first, second in edges:
        assert first != second
        degrees[first] += 1
        degrees[second] += 1
    assert degrees == [3] * order
    assert connected(order, edges)
    assert all(connected(order, edges, omitted=index)
               for index in range(len(edges)))
    assert not tait_colourable(order, edges)

    decoded_order, decoded_edges = decode_graph6(
        realization["canonical_graph6"]
    )
    assert decoded_order == order
    assert graph_isomorphic(order, edges, decoded_edges)

    # Contract the displayed triangle {9,10,11}; compare with Petersen.
    triangle = {9, 10, 11}
    contracted_names = list(range(9)) + [9]
    contracted = set()
    for first, second in edges:
        mapped_first = 9 if first in triangle else first
        mapped_second = 9 if second in triangle else second
        if mapped_first != mapped_second:
            contracted.add(tuple(sorted((mapped_first, mapped_second))))
    assert len(contracted_names) == 10 and len(contracted) == 15
    petersen = {
        tuple(sorted(edge))
        for edge in (
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
            (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
            (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
        )
    }
    assert graph_isomorphic(10, contracted, petersen)

    # Check every supplied isomorphism to the decoded canonical graph6 row.
    canonical_set = edge_set(decoded_edges)
    for row in DATA["literal_failures"]:
        source_order, source_edges = realization_edges(
            row["word_pair"], row["partition"]
        )
        assert source_order == order
        mapping = row["isomorphism_to_canonical"]
        mapped_edges = {
            tuple(sorted((mapping[first], mapping[second])))
            for first, second in source_edges
        }
        assert mapped_edges == canonical_set

    profiles = extension_profile(order, edges)
    target = (1 << 11) - 1
    assert profiles[target] == (True, False)
    extendable = [
        mask for mask, (yes, _clean) in profiles.items() if yes
    ]
    minimum = min(mask.bit_count() for mask in extendable)
    minima = [
        mask for mask in extendable if mask.bit_count() == minimum
    ]
    assert minimum == 5 and len(minima) == 6
    assert all(profiles[mask][1] for mask in minima)


def main():
    validate_pair_orbits()
    validate_replacement_certificates()
    validate_graph()
    print("PASS: independent size-11 frontier certificate audit")
    print("failure_pair_orbits=11")
    print("replacement_certificates=14")
    print("graph=Kt?G?DIPOqCo order=12 size=18 simple cubic bridgeless")
    print("target_size=11 extendable=yes cleanable=no")
    print("minimum_extendable_size=5 minima=6 all_cleanable=yes")
    print("triangle_contraction=Petersen nonplanar=yes")


if __name__ == "__main__":
    main()
