#!/usr/bin/env python3
"""Independent exhaustive replay of the first clean-or-delete counterstate."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORDS = ("0101023", "0101232")
PARTITION = tuple(map(int, "01234444413024"))
CIRCUITS = (tuple(range(7)), tuple(range(7, 14)))
IDENTITY = (0, 1, 2, 3)
GL = tuple((0,) + p for p in itertools.permutations((1, 2, 3)))


def derivatives(word):
    return tuple(
        word[position - 1] ^ word[position]
        for position in range(len(word))
    )


WORD = tuple(map(int, "".join(WORDS)))
DERIVATIVE = derivatives(tuple(map(int, WORDS[0]))) + derivatives(
    tuple(map(int, WORDS[1]))
)


def integrate(transformed):
    base = [0] * 14
    for circuit in CIRCUITS:
        value = 0
        for edge in circuit:
            value ^= transformed[edge]
            base[edge] = value
        assert value == 0
    return tuple(base)


def q(value):
    return ((value >> 1) & 1) & (value & 1)


def block_q(base):
    result = [0] * 5
    for circuit in CIRCUITS:
        for position, edge in enumerate(circuit):
            previous = circuit[position - 1]
            result[PARTITION[edge]] ^= q(base[previous]) ^ q(base[edge])
    return tuple(result)


def translated(base, second_shift):
    return base[:7] + tuple(value ^ second_shift for value in base[7:])


def clean_by_colours(base):
    parity = [[0] * 4 for _ in range(5)]
    for circuit in CIRCUITS:
        for position, edge in enumerate(circuit):
            successor = circuit[(position + 1) % len(circuit)]
            first = PARTITION[edge]
            second = PARTITION[successor]
            if first != second:
                parity[first][base[edge]] ^= 1
                parity[second][base[edge]] ^= 1
    return not any(any(row) for row in parity)


def transition_sums(transformed):
    result = [[0, 0] for _ in range(5)]
    for circuit_index, circuit in enumerate(CIRCUITS):
        for edge in circuit:
            result[PARTITION[edge]][circuit_index] ^= transformed[edge]
    return tuple(tuple(row) for row in result)


def dual_witness(q_values, transition):
    for mask in range(1, 1 << 5):
        sums = [0, 0]
        rhs = 0
        for block in range(5):
            if (mask >> block) & 1:
                rhs ^= q_values[block]
                sums[0] ^= transition[block][0]
                sums[1] ^= transition[block][1]
        if sums == [0, 0] and rhs == 1:
            return tuple(block for block in range(5) if (mask >> block) & 1)
    raise AssertionError("missing dual inconsistency witness")


def main():
    assert len(WORD) == len(PARTITION) == len(DERIVATIVE) == 14
    assert set(PARTITION) == set(range(5))
    assert all(DERIVATIVE)
    for text in WORDS:
        values = tuple(map(int, text))
        assert set(values) == set(range(4))
        assert all(
            values[index] != values[(index + 1) % len(values)]
            for index in range(len(values))
        )
    for block in range(5):
        charge = 0
        for index, component in enumerate(PARTITION):
            if component == block:
                charge ^= DERIVATIVE[index]
        assert charge == 0

    total_map_tuples = 0
    integrable = 0
    directly_cleanable = 0
    deletion_maps = 0
    full_records = []
    reduced = {}

    # A common left composition is harmless, so block zero is fixed to
    # the identity.  Every one of the remaining 6^4 tuples is explicit.
    for tail in itertools.product(GL, repeat=4):
        maps = (IDENTITY,) + tail
        total_map_tuples += 1
        transformed = tuple(
            maps[PARTITION[index]][DERIVATIVE[index]]
            for index in range(14)
        )
        circuit_charges = tuple(
            __import__("functools").reduce(
                int.__xor__, (transformed[index] for index in circuit), 0
            )
            for circuit in CIRCUITS
        )
        if circuit_charges != (0, 0):
            continue

        integrable += 1
        base = integrate(transformed)
        colour_sets = tuple(
            tuple(sorted({base[index] for index in circuit}))
            for circuit in CIRCUITS
        )
        if any(len(colours) < 4 for colours in colour_sets):
            deletion_maps += 1

        clean_shifts = []
        q_rows = []
        for shift in range(4):
            candidate = translated(base, shift)
            by_colours = clean_by_colours(candidate)
            by_quadratic = not any(block_q(candidate))
            assert by_colours == by_quadratic
            q_rows.append("".join(map(str, block_q(candidate))))
            if by_colours:
                clean_shifts.append(shift)
        if clean_shifts:
            directly_cleanable += 1

        q_zero = block_q(base)
        transitions = transition_sums(transformed)
        dual = dual_witness(q_zero, transitions)
        reduced_key = (
            maps[1][1],
            maps[2][1],
            maps[3][1],
            maps[4][1],
            maps[4][2],
        )
        record = {
            "reduced_images": "".join(map(str, reduced_key)),
            "base": (
                "".join(map(str, base[:7]))
                + "|"
                + "".join(map(str, base[7:]))
            ),
            "q_by_second_translation": q_rows,
            "dual_blocks": "".join(map(str, dual)),
        }
        if reduced_key in reduced:
            assert reduced[reduced_key] == record
        else:
            reduced[reduced_key] = record
        full_records.append(record)

    assert total_map_tuples == 1296
    assert directly_cleanable == 0
    assert deletion_maps == 0
    assert integrable == len(full_records)
    assert integrable == 8 * len(reduced)

    certificate = {
        "word": "|".join(WORDS),
        "partition": "".join(map(str, PARTITION)),
        "total_map_tuples_mod_global_GL": total_map_tuples,
        "integrable_full_map_tuples": integrable,
        "integrable_reduced_transition_tuples": len(reduced),
        "directly_cleanable_map_tuples": directly_cleanable,
        "deletion_map_tuples": deletion_maps,
        "reduced_cases": sorted(
            reduced.values(), key=lambda row: row["reduced_images"]
        ),
    }
    encoded = (
        json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    ).encode("ascii")
    frozen = ROOT / "counterstate-certificate.json"
    if frozen.exists():
        assert frozen.read_bytes() == encoded
    else:
        frozen.write_bytes(encoded)

    print("PASS: exhaustive size-14 clean-or-delete counterstate")
    print(f"map_tuples_mod_global_GL={total_map_tuples}")
    print(f"integrable_full_map_tuples={integrable}")
    print(f"integrable_reduced_transition_tuples={len(reduced)}")
    print(f"directly_cleanable_map_tuples={directly_cleanable}")
    print(f"deletion_map_tuples={deletion_maps}")
    print(f"certificate_sha256={hashlib.sha256(encoded).hexdigest()}")


if __name__ == "__main__":
    main()
