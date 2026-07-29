#!/usr/bin/env python3
"""Extend the frozen size-14 residuals by one same-block occurrence.

This is a targeted regression, not the exhaustive size-15 census.  Each
new occurrence is inserted immediately before an old occurrence and placed in
the same complement-component block.  This preserves the xor charge of every
block.  We then test the exact component-GL clean-or-delete dichotomy.
"""

from __future__ import annotations

import functools
import itertools
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FAILURES = (
    ROOT.parent
    / "minimum-projection-size14-kempe-escape-20260729"
    / "failure-states.txt"
)
LINE = re.compile(r"COUNTERSTATE word=(\S+) partition=(\d+)$")
GL = tuple((0,) + row for row in itertools.permutations((1, 2, 3)))
ID = (0, 1, 2, 3)


def circuits_for(lengths: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    result = []
    offset = 0
    for length in lengths:
        result.append(tuple(range(offset, offset + length)))
        offset += length
    return tuple(result)


def derivative(word: tuple[int, ...], circuits) -> tuple[int, ...]:
    result = [0] * len(word)
    for circuit in circuits:
        for local, edge in enumerate(circuit):
            result[edge] = word[circuit[local - 1]] ^ word[edge]
    return tuple(result)


def integrate(transitions: tuple[int, ...], circuits):
    result = [0] * len(transitions)
    for circuit in circuits:
        value = 0
        for edge in circuit:
            value ^= transitions[edge]
            result[edge] = value
        if value:
            return None
    return tuple(result)


def clean(base, partition, circuits) -> bool:
    shifts = itertools.product(range(4), repeat=len(circuits) - 1)
    for tail in shifts:
        shift = (0,) + tail
        parity = [[0] * 4 for _ in range(max(partition) + 1)]
        for circuit_index, circuit in enumerate(circuits):
            for local, edge in enumerate(circuit):
                successor = circuit[(local + 1) % len(circuit)]
                left, right = partition[edge], partition[successor]
                if left == right:
                    continue
                colour = base[edge] ^ shift[circuit_index]
                parity[left][colour] ^= 1
                parity[right][colour] ^= 1
        if not any(bit for row in parity for bit in row):
            return True
    return False


@functools.lru_cache(maxsize=None)
def classify(word, partition, lengths):
    circuits = circuits_for(lengths)
    d = derivative(word, circuits)
    components = max(partition) + 1
    feasible = clean_count = delete_count = 0
    first_delete = None
    for tail in itertools.product(GL, repeat=components - 1):
        maps = (ID,) + tail
        transformed = tuple(
            maps[partition[position]][d[position]]
            for position in range(len(word))
        )
        base = integrate(transformed, circuits)
        if base is None:
            continue
        feasible += 1
        if clean(base, partition, circuits):
            clean_count += 1
        for circuit_index, circuit in enumerate(circuits):
            used = {base[position] for position in circuit}
            if len(used) < 4:
                delete_count += 1
                if first_delete is None:
                    first_delete = (
                        circuit_index,
                        next(value for value in range(4) if value not in used),
                        maps,
                        base,
                    )
                break
    return feasible, clean_count, delete_count, first_delete


def insert_state(encoded_word, encoded_partition):
    pieces = tuple(tuple(map(int, piece)) for piece in encoded_word.split("|"))
    parts = tuple(map(int, encoded_partition))
    old_lengths = tuple(map(len, pieces))
    offset = 0
    for circuit_index, piece in enumerate(pieces):
        for local, successor_colour in enumerate(piece):
            predecessor_colour = piece[local - 1]
            old_position = offset + local
            for new_colour in range(4):
                if new_colour in (predecessor_colour, successor_colour):
                    continue
                new_piece = piece[:local] + (new_colour,) + piece[local:]
                new_pieces = (
                    pieces[:circuit_index]
                    + (new_piece,)
                    + pieces[circuit_index + 1 :]
                )
                word = tuple(value for row in new_pieces for value in row)
                partition = (
                    parts[:old_position]
                    + (parts[old_position],)
                    + parts[old_position:]
                )
                lengths = (
                    old_lengths[:circuit_index]
                    + (old_lengths[circuit_index] + 1,)
                    + old_lengths[circuit_index + 1 :]
                )
                yield word, partition, lengths
        offset += len(piece)


def encode_word(word, lengths):
    rows = []
    offset = 0
    for length in lengths:
        rows.append("".join(map(str, word[offset : offset + length])))
        offset += length
    return "|".join(rows)


def main() -> None:
    states = set()
    for raw in FAILURES.read_text(encoding="utf-8").splitlines():
        match = LINE.fullmatch(raw)
        assert match
        states.update(insert_state(*match.groups()))
    print(f"unique_extensions={len(states)}")
    residuals = []
    counts = [0, 0, 0]
    for index, (word, partition, lengths) in enumerate(sorted(states)):
        feasible, cleans, deletes, _certificate = classify(
            word, partition, lengths
        )
        assert feasible
        if cleans:
            counts[0] += 1
        elif deletes:
            counts[1] += 1
        else:
            counts[2] += 1
            residuals.append((word, partition, lengths, feasible))
            print(
                "RESIDUAL"
                f" word={encode_word(word, lengths)}"
                f" partition={''.join(map(str, partition))}"
                f" feasible={feasible}"
            )
        if (index + 1) % 1000 == 0:
            print(f"progress={index + 1} counts={tuple(counts)}")
    print(f"RESULT clean={counts[0]} delete={counts[1]} residual={counts[2]}")


if __name__ == "__main__":
    main()
