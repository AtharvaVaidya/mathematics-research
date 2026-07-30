#!/usr/bin/env python3
"""Independent literal audit of the eight fixed-word residuals."""

from __future__ import annotations

import hashlib
import itertools
from collections import Counter


WORD_ROWS = ("01010123", "01012302")
WORD = tuple(map(int, "".join(WORD_ROWS)))
LENGTHS = (8, 8)
OFFSETS = (0, 8)
RESIDUALS = (
    "0001234000314200",
    "0001234003144422",
    "0012344041300022",
    "0012344044130244",
    "0012344400314200",
    "0012344403144422",
    "0123444441300022",
    "0123444444130244",
)
EXPECTED_SHA256 = (
    "3b0d26a74107e67b64878342cb9fb509"
    "bc1b8830d9da89a308fb5a1305274c0d"
)


def derivative() -> tuple[int, ...]:
    answer = []
    for offset, length in zip(OFFSETS, LENGTHS):
        answer.extend(
            WORD[offset + (local - 1) % length] ^ WORD[offset + local]
            for local in range(length)
        )
    return tuple(answer)


DERIVATIVE = derivative()


def matrix_maps() -> tuple[tuple[int, ...], ...]:
    """Generate GL(2,2) from its two linearly independent columns."""
    answer = []
    for first_column in (1, 2, 3):
        for second_column in (1, 2, 3):
            if first_column == second_column:
                continue
            answer.append(
                (0, first_column, second_column,
                 first_column ^ second_column)
            )
    answer.sort()
    return tuple(answer)


GL = matrix_maps()
IDENTITY_INDEX = GL.index((0, 1, 2, 3))


def integrate(values: tuple[int, ...]):
    base = [0] * 16
    used = []
    for offset, length in zip(OFFSETS, LENGTHS):
        point = 0
        colours = set()
        for local in range(length):
            position = offset + local
            point ^= values[position]
            base[position] = point
            colours.add(point)
        if point:
            return None
        used.append(frozenset(colours))
    return tuple(base), tuple(used)


def literal_clean(base: tuple[int, ...], owner: tuple[int, ...]) -> bool:
    blocks = max(owner) + 1
    for shift in range(4):
        parity = [[0] * 4 for _ in range(blocks)]
        for circuit, (offset, length) in enumerate(zip(OFFSETS, LENGTHS)):
            translation = shift if circuit else 0
            for local in range(length):
                edge = offset + local
                successor = offset + (local + 1) % length
                first, second = owner[edge], owner[successor]
                if first == second:
                    continue
                colour = base[edge] ^ translation
                parity[first][colour] ^= 1
                parity[second][colour] ^= 1
        if not any(value for row in parity for value in row):
            return True
    return False


def classify(partition: str) -> tuple[int, int, int]:
    owner = tuple(map(int, partition))
    assert set(owner) == set(range(max(owner) + 1))
    assert all(
        owner[position] <= 1 + max(owner[:position], default=-1)
        for position in range(16)
    )
    blocks = max(owner) + 1
    for block in range(blocks):
        charge = 0
        for position in range(16):
            if owner[position] == block:
                charge ^= DERIVATIVE[position]
        assert charge == 0

    feasible = clean = deletes = 0
    for tail in itertools.product(range(6), repeat=blocks - 1):
        map_indices = (IDENTITY_INDEX,) + tail
        values = tuple(
            GL[map_indices[owner[position]]][DERIVATIVE[position]]
            for position in range(16)
        )
        integrated = integrate(values)
        if integrated is None:
            continue
        feasible += 1
        base, used = integrated
        clean += literal_clean(base, owner)
        deletes += any(len(colours) < 4 for colours in used)
    return feasible, clean, deletes


def dihedral_actions(offset: int):
    for anchor in range(8):
        yield tuple(offset + (anchor + local) % 8 for local in range(8))
        yield tuple(offset + (anchor - local - 1) % 8 for local in range(8))


def restricted_growth(sequence) -> str:
    names = {}
    result = []
    for value in sequence:
        if value not in names:
            names[value] = str(len(names))
        result.append(names[value])
    return "".join(result)


def canonical_key(partition: str) -> str:
    rows = []
    for first in dihedral_actions(0):
        for second in dihedral_actions(8):
            for indices in (first + second, second + first):
                normalized_word = restricted_growth(WORD[index] for index in indices)
                normalized_partition = restricted_growth(
                    partition[index] for index in indices
                )
                rows.append(normalized_word + "|" + normalized_partition)
    return min(rows)


def main() -> None:
    assert DERIVATIVE == tuple(map(int, "3111113121113132"))
    assert len(GL) == 6

    word_images = []
    for first in dihedral_actions(0):
        for second in dihedral_actions(8):
            for indices in (first + second, second + first):
                word_images.append(
                    restricted_growth(WORD[index] for index in indices)
                )
    assert len(word_images) == 512
    assert len(set(word_images)) == 512
    assert min(word_images) == "".join(WORD_ROWS)
    proper_eight = sum(
        len(set(word)) == 4
        and all(word[index] != word[(index + 1) % 8] for index in range(8))
        for word in itertools.product(range(4), repeat=8)
    )
    assert proper_eight == 5_544
    raw_pairs = proper_eight**2
    symmetry_order = 24 * 16 * 16 * 2
    orbit_lower_bound = (
        raw_pairs + symmetry_order - 1
    ) // symmetry_order
    assert orbit_lower_bound == 2_502

    profile_histogram: Counter[tuple[int, ...]] = Counter()
    rows = []
    for partition in RESIDUALS:
        result = classify(partition)
        assert result == (320, 0, 0), (partition, result)
        flat_word = "".join(WORD_ROWS)
        assert canonical_key(partition) == flat_word + "|" + partition
        profile = tuple(
            sorted(Counter(partition).values(), reverse=True)
        )
        profile_histogram[profile] += 1
        matrix = tuple(
            (
                partition[:8].count(str(block)),
                partition[8:].count(str(block)),
            )
            for block in range(max(map(int, partition)) + 1)
        )
        interaction_loop = any(
            first + second == 2 and (first == 0 or second == 0)
            for first, second in matrix
        )
        higher_occurrence = any(
            first + second > 2 for first, second in matrix
        )
        assert not interaction_loop
        assert higher_occurrence
        row = "|".join(WORD_ROWS) + "|" + partition
        rows.append(row)
        print(
            f"RESIDUAL key={row} feasible={result[0]}"
            f" clean={result[1]} delete={result[2]}"
            f" profile={'+'.join(map(str, profile))}"
            f" matrix={','.join(f'{a}/{b}' for a, b in matrix)}"
            f" interaction_loop={int(interaction_loop)}"
            f" higher_occurrence={int(higher_occurrence)}"
        )

    assert profile_histogram == {
        (8, 2, 2, 2, 2): 2,
        (6, 4, 2, 2, 2): 2,
        (6, 3, 3, 2, 2): 2,
        (5, 4, 3, 2, 2): 2,
    }
    digest = hashlib.sha256(
        "".join(row + "\n" for row in sorted(rows)).encode("ascii")
    ).hexdigest()
    assert digest == EXPECTED_SHA256
    print(
        "CANONICAL word_orbit_images=512 stabilizer=1"
        f" residual_orbits={len(RESIDUALS)}"
    )
    print(
        f"FRONTIER_BOUND proper_length8={proper_eight}"
        f" raw_ordered_pairs={raw_pairs}"
        f" symmetry_order={symmetry_order}"
        f" orbit_lower_bound={orbit_lower_bound}"
    )
    print(f"RESIDUAL_SHA256 {digest}")
    print("PASS independent residual and canonical-key audit")


if __name__ == "__main__":
    main()
