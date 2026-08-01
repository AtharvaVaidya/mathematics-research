#!/usr/bin/env python3
"""Independent audit using support-colour words and perfect matchings."""

from __future__ import annotations

import itertools
from collections import deque


COLOURS = range(4)
ORDER_B = (0, 3, 1, 4, 2)
POSITION_B = {edge: position for position, edge in enumerate(ORDER_B)}


def proper_cyclic_words():
    return tuple(
        word
        for word in itertools.product(COLOURS, repeat=5)
        if all(word[index] != word[(index + 1) % 5] for index in range(5))
    )


def derivative(word):
    return tuple(word[index - 1] ^ word[index] for index in range(5))


def component_derivative_b(word):
    local = derivative(word)
    return tuple(local[POSITION_B[edge]] for edge in range(5))


def occurrence_lines(word, order):
    return {
        edge: frozenset((word[position - 1], word[position]))
        for position, edge in enumerate(order)
    }


def word_pair_audit():
    words = proper_cyclic_words()
    assert len(words) == 240
    by_flow_a = {}
    by_flow_b = {}
    for word in words:
        by_flow_a.setdefault(derivative(word), []).append(word)
        by_flow_b.setdefault(component_derivative_b(word), []).append(word)
    common = set(by_flow_a) & set(by_flow_b)
    assert len(common) == 60
    pairs = clean = deletion = 0
    profiles = set()
    for values in common:
        assert all(values) and __import__("functools").reduce(
            int.__xor__, values, 0
        ) == 0
        for first in by_flow_a[values]:
            for second in by_flow_b[values]:
                pairs += 1
                clean += (
                    occurrence_lines(first, range(5))
                    == occurrence_lines(second, ORDER_B)
                )
                sizes = (len(set(first)), len(set(second)))
                profiles.add(sizes)
                deletion += min(sizes) < 4
    assert pairs == 960
    assert clean == 0
    assert deletion == 960
    assert profiles == {(3, 4), (4, 3)}
    return len(words), len(common), pairs, clean, deletion, profiles


def graph():
    edges = []
    for offset in (0, 5):
        edges.extend(
            tuple(sorted((offset + index, offset + (index + 1) % 5)))
            for index in range(5)
        )
    edges.extend(
        tuple(sorted((edge, 5 + POSITION_B[edge]))) for edge in range(5)
    )
    assert len(edges) == len(set(edges)) == 15
    return tuple(edges)


def components(edges):
    adjacency = [set() for _ in range(10)]
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    unseen = set(range(10))
    result = []
    while unseen:
        root = min(unseen)
        part = {root}
        queue = deque([root])
        unseen.remove(root)
        while queue:
            vertex = queue.popleft()
            for neighbour in adjacency[vertex] & unseen:
                unseen.remove(neighbour)
                part.add(neighbour)
                queue.append(neighbour)
        result.append(part)
    return tuple(result)


def perfect_matching_audit(edges):
    matchings = []
    all_edges = set(range(15))
    for chosen in itertools.combinations(range(15), 5):
        degree = [0] * 10
        for edge in chosen:
            for vertex in edges[edge]:
                degree[vertex] += 1
        if degree == [1] * 10:
            matchings.append(chosen)
    assert len(matchings) == 6
    cycle_profiles = []
    for matching in matchings:
        complement = tuple(
            edges[edge] for edge in sorted(all_edges - set(matching))
        )
        parts = components(complement)
        profile = tuple(sorted(map(len, parts)))
        assert profile == (5, 5)
        cycle_profiles.append(profile)
    # A Tait colouring would make the complement of any one colour class a
    # disjoint union of even alternating cycles, impossible here.
    return len(matchings), tuple(cycle_profiles)


def bridge_audit(edges):
    assert len(components(edges)) == 1
    assert all(
        len(components(tuple(edge for i, edge in enumerate(edges) if i != skip)))
        == 1
        for skip in range(15)
    )


def low_flow_audit(edges):
    word_a = tuple(map(int, "10130"))
    word_b = tuple(map(int, "13210"))
    matching = (1, 1, 1, 2, 3)
    lows = word_a + word_b + matching
    support = (1,) * 10 + (0,) * 5
    degree_low = [0] * 10
    degree_high = [0] * 10
    for index, edge in enumerate(edges):
        for vertex in edge:
            degree_low[vertex] ^= lows[index]
            degree_high[vertex] ^= support[index]
    assert degree_low == degree_high == [0] * 10

    descended_low = tuple(
        low ^ (2 if index < 5 else 0) for index, low in enumerate(lows)
    )
    descended_support = (0,) * 5 + (1,) * 5 + (0,) * 5
    assert all(high or low for high, low in zip(descended_support, descended_low))
    for vertex in range(10):
        incident = [i for i, edge in enumerate(edges) if vertex in edge]
        assert __import__("functools").reduce(
            int.__xor__, (descended_low[i] for i in incident), 0
        ) == 0
        assert __import__("functools").reduce(
            int.__xor__, (descended_support[i] for i in incident), 0
        ) == 0
    complement = tuple(
        edges[index]
        for index in range(15)
        if not descended_support[index]
    )
    assert len(components(complement)) == 1
    return "".join(map(str, descended_low))


def main():
    word_counts = word_pair_audit()
    edges = graph()
    bridge_audit(edges)
    matching_count, profiles = perfect_matching_audit(edges)
    descended = low_flow_audit(edges)
    print("PASS: independent two-occurrence/Petersen audit")
    print(
        f"proper_words={word_counts[0]} flows={word_counts[1]} "
        f"word_pairs={word_counts[2]} clean={word_counts[3]} "
        f"deletion={word_counts[4]} profiles=3/4,4/3"
    )
    print(
        f"perfect_matchings={matching_count} "
        f"complement_profiles={','.join('5+5' for _ in profiles)}"
    )
    print("graph simple_cubic_bridgeless=yes tait=no")
    print(f"descent_support=5 complement_connected=yes low={descended}")


if __name__ == "__main__":
    main()
