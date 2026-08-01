#!/usr/bin/env python3
"""Independently check the frozen size-twelve deletion certificates."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
GL = {
    (0,) + image
    for image in __import__("itertools").permutations((1, 2, 3))
}
EXPECTED = {
    "12": {
        "canonical_words": 1014,
        "charge_valid": 14196654,
        "dirty": 11465978,
        "direct_clean": 11465978,
        "delete_branch": 0,
        "delete_orbits": 0,
        "dichotomy_failures": 0,
    },
    "4+8": {
        "canonical_words": 66,
        "charge_valid": 922048,
        "dirty": 773721,
        "direct_clean": 773717,
        "delete_branch": 4,
        "delete_orbits": 2,
        "dichotomy_failures": 0,
    },
    "5+7": {
        "canonical_words": 64,
        "charge_valid": 884604,
        "dirty": 738969,
        "direct_clean": 738763,
        "delete_branch": 206,
        "delete_orbits": 188,
        "dichotomy_failures": 0,
    },
    "6+6": {
        "canonical_words": 66,
        "charge_valid": 926640,
        "dirty": 774196,
        "direct_clean": 774014,
        "delete_branch": 182,
        "delete_orbits": 104,
        "dichotomy_failures": 0,
    },
    "4+4+4": {
        "canonical_words": 3,
        "charge_valid": 41975,
        "dirty": 35960,
        "direct_clean": 35960,
        "delete_branch": 0,
        "delete_orbits": 0,
        "dichotomy_failures": 0,
    },
}


def fields(line):
    return dict(item.split("=", 1) for item in line.split()[1:])


def circuit_ranges(lengths):
    result = []
    offset = 0
    for length in lengths:
        result.append(tuple(range(offset, offset + length)))
        offset += length
    assert offset == 12
    return tuple(result)


def check_deletion(row):
    lengths = tuple(map(int, row["shape"].split("+")))
    circuits = circuit_ranges(lengths)
    word_pieces = row["word"].split("|")
    base_pieces = row["base"].split("|")
    assert tuple(map(len, word_pieces)) == lengths
    assert tuple(map(len, base_pieces)) == lengths
    word = tuple(map(int, "".join(word_pieces)))
    base = tuple(map(int, "".join(base_pieces)))
    partition = tuple(map(int, row["partition"]))
    assert len(word) == len(base) == len(partition) == 12
    assert set(partition) == set(range(max(partition) + 1))

    for circuit in circuits:
        values = tuple(word[index] for index in circuit)
        assert set(values) == set(range(4))
        assert all(
            values[index] != values[(index + 1) % len(values)]
            for index in range(len(values))
        )

    derivative = [0] * 12
    for circuit in circuits:
        for position, index in enumerate(circuit):
            derivative[index] = word[circuit[position - 1]] ^ word[index]
    assert all(derivative)

    components = max(partition) + 1
    for component in range(components):
        charge = 0
        for index, label in enumerate(partition):
            if label == component:
                charge ^= derivative[index]
        assert charge == 0

    parities = [[0] * 4 for _ in range(components)]
    for circuit in circuits:
        for position, edge in enumerate(circuit):
            successor = circuit[(position + 1) % len(circuit)]
            first = partition[edge]
            second = partition[successor]
            if first != second:
                parities[first][word[edge]] ^= 1
                parities[second][word[edge]] ^= 1
    assert all(len(set(component)) == 1 for component in parities)
    assert any(component[0] for component in parities)

    maps = tuple(
        tuple(map(int, encoded)) for encoded in row["maps"].split("/")
    )
    assert len(maps) == components
    assert all(mapping in GL for mapping in maps)
    transformed = tuple(
        maps[partition[index]][derivative[index]] for index in range(12)
    )

    reconstructed = [0] * 12
    for circuit in circuits:
        value = 0
        for index in circuit:
            value ^= transformed[index]
            reconstructed[index] = value
        assert value == 0
    assert tuple(reconstructed) == base

    deleted = int(row["delete_circuit"])
    missing = int(row["missing_colour"])
    assert 0 <= deleted < len(circuits)
    assert 0 <= missing < 4
    assert missing not in {base[index] for index in circuits[deleted]}
    translated = tuple(base[index] ^ missing for index in circuits[deleted])
    assert all(translated)
    assert lengths[deleted] < sum(lengths)


def main():
    path = ROOT / "size12-census.txt"
    raw = path.read_bytes()
    lines = raw.decode("ascii").splitlines()
    results = {}
    states = {shape: [] for shape in EXPECTED}
    orbits = {shape: set() for shape in EXPECTED}

    for line in lines:
        if line.startswith("RESULT "):
            row = fields(line)
            shape = row.pop("shape")
            results[shape] = {key: int(value) for key, value in row.items()}
        elif line.startswith("DELETESTATE "):
            row = fields(line)
            check_deletion(row)
            states[row["shape"]].append(row)
        elif line.startswith("DELETEORBIT "):
            _tag, shape_field, word, partition = line.split()
            shape = shape_field.split("=", 1)[1]
            orbits[shape].add((word, partition))
        elif line.startswith("COUNTERSTATE "):
            raise AssertionError(f"unresolved counterstate: {line}")

    assert results == EXPECTED
    for shape, expected in EXPECTED.items():
        assert len(states[shape]) == expected["delete_branch"]
        assert len(orbits[shape]) == expected["delete_orbits"]
        assert (
            expected["direct_clean"] + expected["delete_branch"]
            == expected["dirty"]
        )
    assert sum(map(len, states.values())) == 392
    assert sum(map(len, orbits.values())) == 294

    digest = hashlib.sha256(raw).hexdigest()
    print("PASS: frozen size-twelve clean-or-delete certificates")
    print(f"delete_states={sum(map(len, states.values()))}")
    print(f"delete_orbits={sum(map(len, orbits.values()))}")
    print("dichotomy_failures=0")
    print(f"census_sha256={digest}")


if __name__ == "__main__":
    main()
