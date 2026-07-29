#!/usr/bin/env python3
"""Dependency-free direct-cleaning proof through support size ten.

This checker works only with the exact boundary data forced by a fixed
nowhere-zero extension of a minimum projection.  It enumerates one
GL(2,2) map per component of G-h and arbitrary low starting values on
each circuit of h.  It then checks the resulting affine cut parities.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import permutations, product
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NONZERO = (1, 2, 3)
GL = tuple(
    (0,) + image
    for image in permutations(NONZERO)
    if image[2] == (image[0] ^ image[1])
)
AFFINE = tuple(permutations(range(4)))


def set_partitions(order):
    """Generate each set partition once as a restricted-growth string."""
    labels = [0] * order

    def recurse(index, maximum):
        if index == order:
            yield tuple(labels)
            return
        for value in range(maximum + 2):
            labels[index] = value
            yield from recurse(index + 1, max(maximum, value))

    yield from recurse(1, 0)


def normalize_partition(partition):
    names = {}
    result = []
    for value in partition:
        if value not in names:
            names[value] = len(names)
        result.append(names[value])
    return tuple(result)


def normalize_colours(word):
    """Lexicographically least relabelling of a word using all colours."""
    names = {}
    result = []
    for value in word:
        if value not in names:
            names[value] = len(names)
        result.append(names[value])
    assert len(names) == 4
    return tuple(result)


def normalized_colour_words(order):
    """One representative of every S4-orbit before dihedral quotient."""
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


def circuit_transform(circuit):
    """Yield corresponding vertex/edge indices for its dihedral action."""
    order = len(circuit)
    for reflected in (False, True):
        for anchor in range(order):
            if not reflected:
                vertices = tuple(
                    circuit[(anchor + index) % order]
                    for index in range(order)
                )
                edges = vertices
            else:
                # If new vertex i is old vertex anchor-i, new edge i is
                # old edge anchor-i-1.
                vertices = tuple(
                    circuit[(anchor - index) % order]
                    for index in range(order)
                )
                edges = tuple(
                    circuit[(anchor - index - 1) % order]
                    for index in range(order)
                )
            yield vertices, edges


def shape_transforms(circuits):
    """Dihedral actions, plus interchange of equal-length circuits."""
    local = tuple(tuple(circuit_transform(circuit)) for circuit in circuits)
    if len(circuits) == 1:
        yield from local[0]
        return
    assert len(circuits) == 2
    for vertices0, edges0 in local[0]:
        for vertices1, edges1 in local[1]:
            yield vertices0 + vertices1, edges0 + edges1
            if len(circuits[0]) == len(circuits[1]):
                yield vertices1 + vertices0, edges1 + edges0


def canonical_word(word, circuits):
    return min(
        normalize_colours(tuple(word[index] for index in edges))
        for _vertices, edges in shape_transforms(circuits)
    )


def canonical_pair(word, partition, circuits):
    return min(
        (
            normalize_colours(tuple(word[index] for index in edges)),
            normalize_partition(
                tuple(partition[index] for index in vertices)
            ),
        )
        for vertices, edges in shape_transforms(circuits)
    )


def proper_word(word, circuits):
    if any(set(word[index] for index in circuit) != set(range(4))
           for circuit in circuits):
        return False
    return all(
        word[index] != word[circuit[(position + 1) % len(circuit)]]
        for circuit in circuits
        for position, index in enumerate(circuit)
    )


def pendant_values(word, circuits):
    result = [0] * len(word)
    for circuit in circuits:
        for position, index in enumerate(circuit):
            result[index] = word[circuit[position - 1]] ^ word[index]
    assert all(result)
    return tuple(result)


def cut_parities(word, partition, circuits):
    """Four M_c cut parities for every component block."""
    result = []
    for component in range(max(partition) + 1):
        row = []
        for colour in range(4):
            parity = 0
            for circuit in circuits:
                for position, edge in enumerate(circuit):
                    successor = circuit[(position + 1) % len(circuit)]
                    crosses = (
                        (partition[edge] == component)
                        != (partition[successor] == component)
                    )
                    parity ^= int(crosses and word[edge] == colour)
            row.append(parity)
        result.append(tuple(row))
    return tuple(result)


def valid_dirty_boundary(word, partition, circuits):
    pendant = pendant_values(word, circuits)
    for component in range(max(partition) + 1):
        charge = 0
        for index, label in enumerate(partition):
            if label == component:
                charge ^= pendant[index]
        if charge:
            return False
    parities = cut_parities(word, partition, circuits)
    return (
        all(len(set(row)) == 1 for row in parities)
        and any(row[0] for row in parities)
    )


def integrate(transformed, circuits, starting_values):
    result = [0] * len(transformed)
    for circuit, starting in zip(circuits, starting_values, strict=True):
        previous = starting
        for index in circuit:
            previous ^= transformed[index]
            result[index] = previous
        if previous != starting:
            return None
    return tuple(result)


def clean_repair(word, partition, circuits):
    """Find component maps and h-edge low values with all cuts clean."""
    pendant = pendant_values(word, circuits)
    components = max(partition) + 1
    # A common postcomposition by GL(2,2) only permutes the four clean
    # cut rows, so normalize the map on component zero to the identity.
    for tail in product(GL, repeat=components - 1):
        maps = ((0, 1, 2, 3),) + tail
        transformed = tuple(
            maps[partition[index]][pendant[index]]
            for index in range(len(word))
        )
        # A common translation of all circuit values only permutes their
        # affine colour names.  Normalize the first start to zero and
        # enumerate every relative translation of the other circuits.
        for relative in product(range(4), repeat=len(circuits) - 1):
            starts = (0,) + relative
            repaired = integrate(transformed, circuits, starts)
            if repaired is None:
                continue
            if all(
                row == (0, 0, 0, 0)
                for row in cut_parities(repaired, partition, circuits)
            ):
                return maps, starts, repaired
    return None


def tait_repair(word, partition, circuits):
    """The narrower componentwise-GL repair to a nowhere-zero low flow."""
    pendant = pendant_values(word, circuits)
    components = max(partition) + 1
    for tail in product(GL, repeat=components - 1):
        maps = ((0, 1, 2, 3),) + tail
        transformed = tuple(
            maps[partition[index]][pendant[index]]
            for index in range(len(word))
        )
        for starts in product(NONZERO, repeat=len(circuits)):
            repaired = integrate(transformed, circuits, starts)
            if repaired is not None and all(repaired):
                return True
    return False


def cut_sizes(partition, circuits):
    result = []
    for component in range(max(partition) + 1):
        size = 0
        for circuit in circuits:
            for position, edge in enumerate(circuit):
                successor = circuit[(position + 1) % len(circuit)]
                size += (
                    (partition[edge] == component)
                    != (partition[successor] == component)
                )
        result.append(size)
    return tuple(result)


def canonical_words(circuits):
    order = sum(map(len, circuits))
    if len(circuits) == 1:
        candidates = normalized_colour_words(order)
    else:
        candidates = product(
            *(
                tuple(permutations(range(4)))
                if len(circuit) == 4
                else tuple(
                    word
                    for word in product(range(4), repeat=len(circuit))
                    if set(word) == set(range(4))
                    and all(
                        word[index] != word[(index + 1) % len(circuit)]
                        for index in range(len(circuit))
                    )
                )
                for circuit in circuits
            )
        )
        candidates = (
            tuple(value for piece in pieces for value in piece)
            for pieces in candidates
        )
    return {
        canonical_word(tuple(word), circuits)
        for word in candidates
        if proper_word(tuple(word), circuits)
    }


def format_repair(word, partition, circuits, repair):
    maps, starts, repaired = repair
    return {
        "word": ["".join(map(str, (word[index] for index in circuit)))
                 for circuit in circuits],
        "partition": "".join(map(str, partition)),
        "maps": ["".join(map(str, row)) for row in maps],
        "starts": list(starts),
        "clean_word": [
            "".join(map(str, (repaired[index] for index in circuit)))
            for circuit in circuits
        ],
    }


def audit_shape(circuits, expected_words, expected_dirty):
    words = canonical_words(circuits)
    assert len(words) == expected_words
    partitions = tuple(set_partitions(sum(map(len, circuits))))
    dirty = 0
    failures = []
    for word in words:
        for partition in partitions:
            if max(partition) == 0:
                continue
            if not valid_dirty_boundary(word, partition, circuits):
                continue
            dirty += 1
            if clean_repair(word, partition, circuits) is None:
                failures.append((word, partition))
    assert dirty == expected_dirty
    assert not failures
    return words, partitions


def size8_residual_certificates():
    """Independently regenerate and clean the previous 88+5 residuals."""
    single = (tuple(range(8)),)
    two = (tuple(range(4)), tuple(range(4, 8)))
    certificates = {"single_8cycle": [], "two_4cycles": []}

    for key, circuits, expected in (
        ("single_8cycle", single, 88),
        ("two_4cycles", two, 5),
    ):
        pairs = set()
        for word in canonical_words(circuits):
            for partition in set_partitions(8):
                if max(partition) == 0:
                    continue
                if not valid_dirty_boundary(word, partition, circuits):
                    continue
                if tait_repair(word, partition, circuits):
                    continue
                if max(partition) + 1 <= 2:
                    continue
                pair = canonical_pair(word, partition, circuits)
                if key == "two_4cycles" and 0 in cut_sizes(
                    pair[1], circuits
                ):
                    continue
                pairs.add(pair)
        assert len(pairs) == expected
        for word, partition in sorted(pairs):
            repair = clean_repair(word, partition, circuits)
            assert repair is not None
            certificates[key].append(
                format_repair(word, partition, circuits, repair)
            )
    return certificates


def raw_size7_audit():
    """Independent check of the earlier 26,880/5,376 raw counts."""
    circuits = (tuple(range(7)),)
    partitions = tuple(set_partitions(7))
    valid = failed_tait = failed_clean = 0
    for word in product(range(4), repeat=7):
        if not proper_word(word, circuits):
            continue
        for partition in partitions:
            if max(partition) == 0:
                continue
            if not valid_dirty_boundary(word, partition, circuits):
                continue
            valid += 1
            failed_tait += int(not tait_repair(word, partition, circuits))
            failed_clean += int(
                clean_repair(word, partition, circuits) is None
            )
    assert (valid, failed_tait, failed_clean) == (26880, 5376, 0)
    return valid, failed_tait, failed_clean


def canonical_json(value):
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    arguments = parser.parse_args()

    assert len(GL) == 6
    assert len(AFFINE) == 24

    one_counts = {
        4: (1, 1),
        5: (1, 2),
        6: (5, 27),
        7: (7, 116),
        8: (26, 1386),
        9: (49, 8840),
        10: (151, 102290),
    }
    for order, (word_count, dirty_count) in one_counts.items():
        audit_shape(
            (tuple(range(order)),),
            expected_words=word_count,
            expected_dirty=dirty_count,
        )
        print(
            f"one_{order}cycle: canonical_words={word_count} "
            f"dirty_word_partitions={dirty_count} failed_clean_repairs=0"
        )

    two_counts = (
        ((4, 4), 2, 114),
        ((4, 5), 2, 372),
        ((4, 6), 11, 7798),
        ((5, 5), 6, 4232),
    )
    for lengths, word_count, dirty_count in two_counts:
        first, second = lengths
        circuits = (
            tuple(range(first)),
            tuple(range(first, first + second)),
        )
        audit_shape(circuits, word_count, dirty_count)
        print(
            f"cycles_{first}+{second}: canonical_words={word_count} "
            f"dirty_word_partitions={dirty_count} failed_clean_repairs=0"
        )

    raw = raw_size7_audit()
    print(
        f"size7_raw: valid_dirty={raw[0]} "
        f"failed_tait_repair={raw[1]} failed_clean_repair={raw[2]}"
    )

    certificates = size8_residual_certificates()
    encoded = canonical_json(certificates)
    digest = hashlib.sha256(encoded.encode("ascii")).hexdigest()
    output = ROOT / "size8-residual-clean-repairs.json"
    if arguments.write:
        output.write_text(encoded, encoding="ascii")
    else:
        assert output.read_text(encoding="ascii") == encoded
    print(
        "size8_residuals: "
        f"single={len(certificates['single_8cycle'])} "
        f"two_4cycles={len(certificates['two_4cycles'])} "
        "failed_clean_repairs=0"
    )
    print(f"size8_certificate_sha256={digest}")
    print("PASS: every minimum projection through size ten is cleanable")


if __name__ == "__main__":
    main()
