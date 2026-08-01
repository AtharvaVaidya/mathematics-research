#!/usr/bin/env python3
"""Exact small search for two-occurrence-component boundary states.

A pairing of support occurrences is the interaction multigraph.  Each pairing
edge receives an arbitrary nonzero K value.  The search asks:

1. is there a nowhere-zero K-flow on the interaction multigraph?
2. among all such flows and independent circuit translations, is one clean?

This is an exploratory producer; any surviving counterstate is emitted
literally for a separate verifier.
"""

from __future__ import annotations

import functools
import itertools
import sys


KSTAR = (1, 2, 3)


def xor_all(values):
    return functools.reduce(int.__xor__, values, 0)


def symplectic(first, second):
    return (((first >> 1) & 1) & (second & 1)) ^ (
        (first & 1) & ((second >> 1) & 1)
    )


def perfect_matchings(items):
    if not items:
        yield ()
        return
    first = items[0]
    for index in range(1, len(items)):
        second = items[index]
        rest = items[1:index] + items[index + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def circuits_for_shape(shape):
    circuits = []
    offset = 0
    for length in shape:
        circuits.append(tuple(range(offset, offset + length)))
        offset += length
    return tuple(circuits)


def owners(pairing, order):
    result = [-1] * order
    for edge, pair in enumerate(pairing):
        for occurrence in pair:
            result[occurrence] = edge
    assert all(value >= 0 for value in result)
    return tuple(result)


def flow_values(pairing, circuits):
    owner = owners(pairing, sum(map(len, circuits)))
    for values in itertools.product(KSTAR, repeat=len(pairing)):
        if all(
            xor_all(values[owner[position]] for position in circuit) == 0
            for circuit in circuits
        ):
            yield values


def prefixes(values, owner, circuits):
    result = [0] * len(owner)
    for circuit in circuits:
        current = 0
        for position in circuit:
            result[position] = current
            current ^= values[owner[position]]
        assert current == 0
    return tuple(result)


def clean_for_flow(pairing, circuits, values):
    order = sum(map(len, circuits))
    owner = owners(pairing, order)
    where = [None] * order
    for circuit_index, circuit in enumerate(circuits):
        for position in circuit:
            where[position] = circuit_index
    base = prefixes(values, owner, circuits)
    for tail in itertools.product(range(4), repeat=len(circuits) - 1):
        shifts = (0,) + tail
        okay = True
        for edge, (first, second) in enumerate(pairing):
            value = values[edge]
            left = base[first] ^ shifts[where[first]]
            right = base[second] ^ shifts[where[second]]
            if symplectic(value, left) != symplectic(value, right):
                okay = False
                break
        if okay:
            return shifts
    return None


def canonical_pairing(pairing):
    # Cheap label renaming only.  This deliberately does not quotient circuit
    # dihedrals; small searches retain duplicates rather than risk omission.
    renamed = {}
    next_name = 0
    word = []
    lookup = {}
    for edge, pair in enumerate(pairing):
        for position in pair:
            lookup[position] = edge
    for position in range(2 * len(pairing)):
        edge = lookup[position]
        if edge not in renamed:
            renamed[edge] = next_name
            next_name += 1
        word.append(renamed[edge])
    return tuple(word)


def search_shape(shape):
    order = sum(shape)
    assert order % 2 == 0
    circuits = circuits_for_shape(shape)
    seen_words = set()
    pairings = flowable = cleanable = 0
    for raw in perfect_matchings(tuple(range(order))):
        word = canonical_pairing(raw)
        if word in seen_words:
            continue
        seen_words.add(word)
        pairing = tuple(
            tuple(position for position, label in enumerate(word) if label == edge)
            for edge in range(order // 2)
        )
        pairings += 1
        flows = tuple(flow_values(pairing, circuits))
        if not flows:
            continue
        flowable += 1
        certificate = None
        for values in flows:
            shifts = clean_for_flow(pairing, circuits, values)
            if shifts is not None:
                certificate = values, shifts
                break
        if certificate is not None:
            cleanable += 1
            continue
        print(
            "COUNTERSTATE shape="
            + "+".join(map(str, shape))
            + " pairing="
            + "".join(map(str, word))
            + " flow="
            + "".join(map(str, flows[0]))
            + f" flow_count={len(flows)}"
        )
        return False, (pairings, flowable, cleanable)
    print(
        "PASS shape="
        + "+".join(map(str, shape))
        + f" pairings={pairings} flowable={flowable} cleanable={cleanable}"
    )
    return True, (pairings, flowable, cleanable)


def main():
    shapes = tuple(
        tuple(map(int, argument.split("+")))
        for argument in sys.argv[1:]
    ) or (
        (3, 3),
        (3, 5),
        (4, 4),
        (3, 3, 4),
        (3, 7),
        (4, 6),
        (5, 5),
    )
    for shape in shapes:
        okay, _counts = search_shape(shape)
        if not okay:
            return


if __name__ == "__main__":
    main()
