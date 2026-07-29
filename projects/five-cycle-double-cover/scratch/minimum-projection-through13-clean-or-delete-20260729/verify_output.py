#!/usr/bin/env python3
"""Independently check the frozen size-thirteen deletion certificates."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
GL = {
    (0,) + image
    for image in __import__("itertools").permutations((1, 2, 3))
}
EXPECTED = {
    "4+4+5": {
        "canonical_words": 4,
        "charge_valid": 238522,
        "dirty": 208144,
        "direct_clean": 208144,
        "delete_branch": 0,
        "delete_orbits": 0,
        "dichotomy_failures": 0,
    },
    "4+9": {
        "canonical_words": 130,
        "charge_valid": 7753918,
        "dirty": 6657654,
        "direct_clean": 6657594,
        "delete_branch": 60,
        "delete_orbits": 60,
        "dichotomy_failures": 0,
    },
    "5+8": {
        "canonical_words": 203,
        "charge_valid": 12144485,
        "dirty": 10404652,
        "direct_clean": 10401428,
        "delete_branch": 3224,
        "delete_orbits": 2775,
        "dichotomy_failures": 0,
    },
    "6+7": {
        "canonical_words": 242,
        "charge_valid": 14480258,
        "dirty": 12415026,
        "direct_clean": 12410636,
        "delete_branch": 4390,
        "delete_orbits": 3663,
        "dichotomy_failures": 0,
    },
    "13": {
        "canonical_words": 2583,
        "charge_valid": 155381679,
        "dirty": 129684490,
        "direct_clean": 129684490,
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
    assert offset == 13
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
    assert len(word) == len(base) == len(partition) == 13
    assert set(partition) == set(range(max(partition) + 1))

    for circuit in circuits:
        values = tuple(word[index] for index in circuit)
        assert set(values) == set(range(4))
        assert all(
            values[index] != values[(index + 1) % len(values)]
            for index in range(len(values))
        )

    derivative = [0] * 13
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
        maps[partition[index]][derivative[index]] for index in range(13)
    )

    reconstructed = [0] * 13
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
    path = ROOT / "size13-census.txt"
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
    assert sum(map(len, states.values())) == 7674
    assert sum(map(len, orbits.values())) == 6498

    digest = hashlib.sha256(raw).hexdigest()
    print("PASS: frozen size-thirteen clean-or-delete certificates")
    print(f"delete_states={sum(map(len, states.values()))}")
    print(f"delete_orbits={sum(map(len, orbits.values()))}")
    print("dichotomy_failures=0")
    print(f"census_sha256={digest}")


if __name__ == "__main__":
    main()
