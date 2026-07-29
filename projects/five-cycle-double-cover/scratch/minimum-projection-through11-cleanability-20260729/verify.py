#!/usr/bin/env python3
"""Exact size-eleven frontier and first direct-clean boundary failures."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from itertools import permutations, product
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NONZERO = (1, 2, 3)
IDENTITY = (0, 1, 2, 3)
GL = tuple(
    (0,) + image
    for image in permutations(NONZERO)
    if image[2] == (image[0] ^ image[1])
)
CANONICAL_GRAPH6 = "Kt?G?DIPOqCo"


def normalize(values):
    names = {}
    result = []
    for value in values:
        if value not in names:
            names[value] = len(names)
        result.append(names[value])
    return tuple(result)


def normalized_words(order):
    word = [0] * order

    def recurse(index, maximum):
        if index == order:
            if maximum == 3 and word[-1] != word[0]:
                yield tuple(word)
            return
        for value in range(min(3, maximum + 1) + 1):
            if value == word[index - 1]:
                continue
            word[index] = value
            yield from recurse(index + 1, max(maximum, value))

    yield from recurse(1, 0)


def proper_words(order):
    return tuple(
        word
        for word in product(range(4), repeat=order)
        if set(word) == set(range(4))
        and all(word[index] != word[(index + 1) % order]
                for index in range(order))
    )


def circuit_actions(order, offset):
    for anchor in range(order):
        yield (
            tuple(offset + (anchor + index) % order
                  for index in range(order)),
            tuple(offset + (anchor + index) % order
                  for index in range(order)),
        )
        yield (
            tuple(offset + (anchor - index) % order
                  for index in range(order)),
            tuple(offset + (anchor - index - 1) % order
                  for index in range(order)),
        )


def canonical_single_word(word):
    order = len(word)
    return min(
        normalize(tuple(word[index] for index in edges))
        for _vertices, edges in circuit_actions(order, 0)
    )


def canonical_two_word(word, lengths):
    first, second = lengths
    return min(
        normalize(tuple(word[index] for index in edges0 + edges1))
        for _vertices0, edges0 in circuit_actions(first, 0)
        for _vertices1, edges1 in circuit_actions(second, first)
    )


def canonical_two_pair(word, partition, lengths):
    first, second = lengths
    return min(
        (
            normalize(tuple(word[index] for index in edges0 + edges1)),
            normalize(tuple(
                partition[index] for index in vertices0 + vertices1
            )),
        )
        for vertices0, edges0 in circuit_actions(first, 0)
        for vertices1, edges1 in circuit_actions(second, first)
    )


def canonical_words(lengths):
    if len(lengths) == 1:
        return {
            canonical_single_word(word)
            for word in normalized_words(lengths[0])
        }
    first, second = lengths
    if first == 4:
        fixed = (0, 1, 2, 3)
    elif first == 5:
        fixed = (0, 1, 0, 2, 3)
    else:
        raise AssertionError("unsupported normalized first circuit")
    return {
        canonical_two_word(fixed + word, lengths)
        for word in proper_words(second)
    }


def circuits(lengths):
    result = []
    offset = 0
    for length in lengths:
        result.append(tuple(range(offset, offset + length)))
        offset += length
    return tuple(result)


def pendant_values(word, shape):
    result = [0] * len(word)
    for circuit in shape:
        for position, index in enumerate(circuit):
            result[index] = word[circuit[position - 1]] ^ word[index]
    assert all(result)
    return tuple(result)


def charge_partitions(pendant):
    """Generate exactly the partitions whose every block has xor zero."""
    order = len(pendant)
    universe = (1 << order) - 1
    subset_charge = [0] * (universe + 1)
    for mask in range(1, universe + 1):
        bit = mask & -mask
        subset_charge[mask] = (
            subset_charge[mask ^ bit]
            ^ pendant[bit.bit_length() - 1]
        )
    by_first = [[] for _ in range(order)]
    for mask in range(1, universe + 1):
        if subset_charge[mask] == 0:
            by_first[(mask & -mask).bit_length() - 1].append(mask)

    labels = [-1] * order

    def recurse(remaining, component):
        if remaining == 0:
            yield tuple(labels)
            return
        first = (remaining & -remaining).bit_length() - 1
        for block in by_first[first]:
            if block & remaining != block:
                continue
            mask = block
            while mask:
                bit = mask & -mask
                labels[bit.bit_length() - 1] = component
                mask ^= bit
            yield from recurse(remaining ^ block, component + 1)

    yield from recurse(universe, 0)


def cut_parities(word, partition, shape):
    rows = [[0] * 4 for _ in range(max(partition) + 1)]
    for circuit in shape:
        for position, edge in enumerate(circuit):
            successor = circuit[(position + 1) % len(circuit)]
            first = partition[edge]
            second = partition[successor]
            if first != second:
                rows[first][word[edge]] ^= 1
                rows[second][word[edge]] ^= 1
    return tuple(tuple(row) for row in rows)


def dirty(word, partition, shape):
    rows = cut_parities(word, partition, shape)
    assert all(len(set(row)) == 1 for row in rows)
    return any(row[0] for row in rows)


def integrate(transformed, shape, starts):
    result = [0] * len(transformed)
    for circuit, starting in zip(shape, starts, strict=True):
        previous = starting
        for index in circuit:
            previous ^= transformed[index]
            result[index] = previous
        if previous != starting:
            return None
    return tuple(result)


def direct_clean_repair(word, partition, shape):
    pendant = pendant_values(word, shape)
    components = max(partition) + 1
    for tail in product(GL, repeat=components - 1):
        maps = (IDENTITY,) + tail
        transformed = tuple(
            maps[partition[index]][pendant[index]]
            for index in range(len(word))
        )
        for relative in product(range(4), repeat=len(shape) - 1):
            starts = (0,) + relative
            repaired = integrate(transformed, shape, starts)
            if repaired is None:
                continue
            if all(
                row == (0, 0, 0, 0)
                for row in cut_parities(repaired, partition, shape)
            ):
                return maps, starts, repaired
    return None


def smaller_first_cycle_replacement(word, partition, shape):
    """Make only the first circuit the new first-coordinate support."""
    assert len(shape) == 2
    pendant = pendant_values(word, shape)
    components = max(partition) + 1
    for tail in product(GL, repeat=components - 1):
        maps = (IDENTITY,) + tail
        transformed = tuple(
            maps[partition[index]][pendant[index]]
            for index in range(len(word))
        )
        for starts in product(range(4), repeat=2):
            repaired = integrate(transformed, shape, starts)
            if repaired is None:
                continue
            if all(repaired[index] for index in shape[1]):
                return maps, starts, repaired
    return None


def audit_shape(lengths, expected_words, expected_charge, expected_dirty):
    shape = circuits(lengths)
    words = canonical_words(lengths)
    assert len(words) == expected_words
    charge_count = dirty_count = 0
    failures = []
    for word in sorted(words):
        pendant = pendant_values(word, shape)
        for partition in charge_partitions(pendant):
            charge_count += 1
            if max(partition) == 0 or not dirty(word, partition, shape):
                continue
            dirty_count += 1
            if direct_clean_repair(word, partition, shape) is None:
                failures.append((word, partition))
    assert charge_count == expected_charge
    assert dirty_count == expected_dirty
    return failures


def minimal_realization(word, partition):
    """Replace every 2-block by an edge and every 3-block by a claw."""
    edges = []
    for offset, length in ((0, 5), (5, 6)):
        for local in range(length):
            edges.append((
                offset + local,
                offset + (local + 1) % length,
            ))
    next_vertex = 11
    for component in range(max(partition) + 1):
        block = tuple(
            index for index, label in enumerate(partition)
            if label == component
        )
        if len(block) == 2:
            edges.append(block)
        elif len(block) == 3:
            edges.extend((next_vertex, index) for index in block)
            next_vertex += 1
        else:
            raise AssertionError(f"unexpected block {block}")
    return next_vertex, tuple(edges)


def adjacency(order, edges):
    result = [set() for _ in range(order)]
    for first, second in edges:
        result[first].add(second)
        result[second].add(first)
    return tuple(frozenset(row) for row in result)


def graph_isomorphism(order, source_edges, target_edges):
    source = adjacency(order, source_edges)
    target = adjacency(order, target_edges)
    mapping = {}
    used = set()

    def recurse():
        if len(mapping) == order:
            return True
        candidates_source = [
            vertex for vertex in range(order) if vertex not in mapping
        ]
        vertex = max(
            candidates_source,
            key=lambda item: (
                sum(neighbor in mapping for neighbor in source[item]),
                -item,
            ),
        )
        for image in range(order):
            if image in used or len(source[vertex]) != len(target[image]):
                continue
            if any(
                ((other in source[vertex])
                 != (mapping[other] in target[image]))
                for other in mapping
            ):
                continue
            mapping[vertex] = image
            used.add(image)
            if recurse():
                return True
            used.remove(image)
            del mapping[vertex]
        return False

    if not recurse():
        return None
    return tuple(mapping[index] for index in range(order))


def decode_graph6(text):
    order = ord(text[0]) - 63
    bits = []
    for character in text[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    pairs = tuple(
        (first, second)
        for second in range(1, order)
        for first in range(second)
    )
    return order, tuple(
        pair for pair, bit in zip(pairs, bits, strict=False) if bit
    )


def connected_without_edge(order, edges, omitted):
    rows = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        if edge == omitted:
            continue
        rows[first].append(second)
        rows[second].append(first)
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor in rows[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == order


def tait_colourable(order, edges):
    incident = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        incident[first].append(edge)
        incident[second].append(edge)
    colours = [-1] * len(edges)
    used = [0] * order

    def recurse(done):
        if done == len(edges):
            return True
        best = None
        allowed_best = None
        for edge, colour in enumerate(colours):
            if colour >= 0:
                continue
            first, second = edges[edge]
            allowed = 0b111 & ~used[first] & ~used[second]
            if not allowed:
                return False
            if best is None or allowed.bit_count() < allowed_best.bit_count():
                best = edge
                allowed_best = allowed
        first, second = edges[best]
        allowed = allowed_best
        while allowed:
            bit = allowed & -allowed
            allowed ^= bit
            colours[best] = bit.bit_length() - 1
            used[first] |= bit
            used[second] |= bit
            if recurse(done + 1):
                return True
            used[first] ^= bit
            used[second] ^= bit
            colours[best] = -1
        return False

    return recurse(0)


def cycle_basis(order, edges):
    rows = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        rows[first].append((second, edge))
        rows[second].append((first, edge))
    parent = [-1] * order
    parent_edge = [-1] * order
    parent[0] = 0
    queue = deque([0])
    tree = set()
    while queue:
        vertex = queue.popleft()
        for neighbor, edge in rows[vertex]:
            if parent[neighbor] < 0:
                parent[neighbor] = vertex
                parent_edge[neighbor] = edge
                tree.add(edge)
                queue.append(neighbor)

    def tree_path(first, second):
        paths = {}
        mask = 0
        vertex = first
        while True:
            paths[vertex] = mask
            if vertex == 0:
                break
            mask ^= 1 << parent_edge[vertex]
            vertex = parent[vertex]
        mask = 0
        vertex = second
        while vertex not in paths:
            mask ^= 1 << parent_edge[vertex]
            vertex = parent[vertex]
        return mask ^ paths[vertex]

    return tuple(
        (1 << edge) ^ tree_path(first, second)
        for edge, (first, second) in enumerate(edges)
        if edge not in tree
    )


def all_cycles(order, edges):
    result = [0]
    for vector in cycle_basis(order, edges):
        result += [cycle ^ vector for cycle in result]
    return tuple(result)


def factor_cuts(order, edges, factor):
    rows = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        if factor >> edge & 1:
            rows[first].append(second)
            rows[second].append(first)
    unseen = set(range(order))
    cuts = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for neighbor in rows[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        cut = 0
        for edge, (first, second) in enumerate(edges):
            if (first in component) != (second in component):
                cut |= 1 << edge
        cuts.append(cut)
    return tuple(cuts)


def projection_profile(order, edges):
    cycles = all_cycles(order, edges)
    all_edges = (1 << len(edges)) - 1
    states = {
        (first | second, first & second)
        for first in cycles for second in cycles
    }

    def properties(projection):
        factor = all_edges ^ projection
        cuts = factor_cuts(order, edges, factor)
        liftable = clean = False
        for union, intersection in states:
            if factor & ~union:
                continue
            liftable = True
            if all(not ((intersection & cut).bit_count() & 1)
                   for cut in cuts):
                clean = True
                break
        return liftable, clean

    by_size = {}
    for projection in cycles:
        by_size.setdefault(projection.bit_count(), []).append(projection)
    for size in sorted(by_size):
        rows = [
            (projection, *properties(projection))
            for projection in by_size[size]
        ]
        liftable = [row for row in rows if row[1]]
        if liftable:
            return {
                "minimum_size": size,
                "minimum_liftable_count": len(liftable),
                "minimum_clean_count": sum(row[2] for row in liftable),
                "properties": properties,
            }
    raise AssertionError("no extendable projection")


def full_flow_values(word, partition, edges):
    pendant = pendant_values(word, circuits((5, 6)))
    values = [4 | value for value in word]
    for edge in edges[11:]:
        first, second = edge
        boundary = first if first < 11 else second
        values.append(pendant[boundary])
    return tuple(values)


def check_flow(order, edges, values):
    assert len(edges) == len(values)
    assert all(values)
    sums = [0] * order
    for value, (first, second) in zip(values, edges, strict=True):
        sums[first] ^= value
        sums[second] ^= value
    assert not any(sums)


def petersen_minor_check(edges):
    triangle = {9, 10, 11}
    contracted = set()
    for first, second in edges:
        first = 9 if first in triangle else first
        second = 9 if second in triangle else second
        if first != second:
            contracted.add(tuple(sorted((first, second))))
    standard = {
        (0, 1), (0, 4), (0, 5), (1, 2), (1, 6),
        (2, 3), (2, 7), (3, 4), (3, 8), (4, 9),
        (5, 7), (5, 8), (6, 8), (6, 9), (7, 9),
    }
    mapping = {0: 0, 1: 1, 8: 2, 7: 3, 4: 4,
               5: 5, 2: 6, 9: 7, 6: 8, 3: 9}
    image = {
        tuple(sorted((mapping[first], mapping[second])))
        for first, second in contracted
    }
    assert image == standard


def certificate_record(index, word, partition, replacement,
                       canonical_edges):
    shape = circuits((5, 6))
    maps, starts, repaired = replacement
    order, edges = minimal_realization(word, partition)
    assert order == 12
    assert len(edges) == 18
    assert len(set(tuple(sorted(edge)) for edge in edges)) == len(edges)
    assert all(connected_without_edge(order, edges, edge)
               for edge in range(len(edges)))
    assert not tait_colourable(order, edges)
    check_flow(order, edges, full_flow_values(word, partition, edges))
    isomorphism = graph_isomorphism(order, edges, canonical_edges)
    assert isomorphism is not None
    return {
        "index": index,
        "word_pair": [
            "".join(map(str, word[:5])),
            "".join(map(str, word[5:])),
        ],
        "partition": "".join(map(str, partition)),
        "replacement_support": "first_5cycle",
        "replacement_maps": ["".join(map(str, row)) for row in maps],
        "replacement_starts": list(starts),
        "replacement_low_words": [
            "".join(map(str, (repaired[index] for index in circuit)))
            for circuit in shape
        ],
        "isomorphism_to_canonical": list(isomorphism),
    }


def canonical_json(value):
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def generate():
    assert len(GL) == 6
    failures_11 = audit_shape(
        (11,), expected_words=345,
        expected_charge=1183710, expected_dirty=919764,
    )
    assert not failures_11
    failures_47 = audit_shape(
        (4, 7), expected_words=17,
        expected_charge=57500, expected_dirty=46786,
    )
    assert not failures_47
    failures_56 = audit_shape(
        (5, 6), expected_words=26,
        expected_charge=87884, expected_dirty=71170,
    )
    assert len(failures_56) == 14

    canonical_order, canonical_edges = decode_graph6(CANONICAL_GRAPH6)
    assert canonical_order == 12
    records = []
    orbit_members = {}
    for index, (word, partition) in enumerate(failures_56):
        replacement = smaller_first_cycle_replacement(
            word, partition, circuits((5, 6))
        )
        assert replacement is not None
        record = certificate_record(
            index, word, partition, replacement, canonical_edges
        )
        records.append(record)
        representative = canonical_two_pair(word, partition, (5, 6))
        key = (
            "".join(map(str, representative[0][:5])),
            "".join(map(str, representative[0][5:])),
            "".join(map(str, representative[1])),
        )
        orbit_members.setdefault(key, []).append(index)
    assert len(orbit_members) == 11

    representative_word = failures_56[0][0]
    representative_partition = failures_56[0][1]
    order, representative_edges = minimal_realization(
        representative_word, representative_partition
    )
    profile = projection_profile(order, representative_edges)
    target = (1 << 11) - 1
    smaller = (1 << 5) - 1
    target_liftable, target_clean = profile["properties"](target)
    smaller_liftable, smaller_clean = profile["properties"](smaller)
    assert target_liftable and not target_clean
    assert smaller_liftable and smaller_clean
    assert (
        profile["minimum_size"],
        profile["minimum_liftable_count"],
        profile["minimum_clean_count"],
    ) == (5, 6, 6)
    petersen_minor_check(representative_edges)

    return {
        "schema": "minimum-projection-through11-v1",
        "classification": {
            "one_11cycle": {
                "canonical_words": 345,
                "charge_valid_word_partitions": 1183710,
                "dirty_word_partitions": 919764,
                "direct_clean_failures": 0,
            },
            "cycles_4_plus_7": {
                "canonical_words": 17,
                "charge_valid_word_partitions": 57500,
                "dirty_word_partitions": 46786,
                "direct_clean_failures": 0,
            },
            "cycles_5_plus_6": {
                "canonical_words": 26,
                "charge_valid_word_partitions": 87884,
                "dirty_word_partitions": 71170,
                "direct_clean_failures": 14,
                "canonical_pair_orbits": 11,
                "failures_with_size5_replacement": 14,
            },
        },
        "canonical_pair_orbits": [
            {
                "word_pair": [key[0], key[1]],
                "partition": key[2],
                "failure_indices": members,
            }
            for key, members in sorted(orbit_members.items())
        ],
        "literal_failures": records,
        "realization": {
            "canonical_graph6": CANONICAL_GRAPH6,
            "order": 12,
            "size": 18,
            "simple": True,
            "connected": True,
            "cubic": True,
            "bridgeless": True,
            "tait_colourable": False,
            "planarity": "nonplanar (certified Petersen minor)",
            "all_14_minimal_realizations_isomorphic": True,
            "target_projection_size": 11,
            "target_projection_liftable": target_liftable,
            "target_projection_cleanable": target_clean,
            "minimum_extendable_projection_size": profile["minimum_size"],
            "minimum_extendable_projection_count":
                profile["minimum_liftable_count"],
            "minimum_clean_projection_count":
                profile["minimum_clean_count"],
            "displayed_size5_replacement_cleanable": smaller_clean,
            "representative_edges_in_target_order": [
                list(edge) for edge in representative_edges
            ],
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    arguments = parser.parse_args()
    report = generate()
    encoded = canonical_json(report)
    path = ROOT / "size11-frontier-certificates.json"
    if arguments.write:
        path.write_text(encoded, encoding="ascii")
    else:
        assert path.read_text(encoding="ascii") == encoded
    digest = hashlib.sha256(encoded.encode("ascii")).hexdigest()
    classification = report["classification"]
    print("PASS: exact size-eleven minimum-projection frontier")
    for key in ("one_11cycle", "cycles_4_plus_7", "cycles_5_plus_6"):
        print(f"{key}: {json.dumps(classification[key], sort_keys=True)}")
    print(
        "all_14_failures_have_size5_replacement=True "
        "canonical_pair_orbits=11"
    )
    print(
        f"realization_graph6={CANONICAL_GRAPH6} "
        "simple=True bridgeless=True non_tait=True "
        "target_size11_cleanable=False minimum_size=5"
    )
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
