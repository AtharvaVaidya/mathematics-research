#!/usr/bin/env python3
"""Build deletion-only Kempe certificates for all frozen size-14 failures."""

from __future__ import annotations

import functools
import itertools
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FAILURES = ROOT / "failure-states.txt"
OUTPUT = ROOT / "all-kempe-certificates.json"
LINE = re.compile(r"COUNTERSTATE word=(\S+) partition=(\d+)$")
GL = tuple((0,) + row for row in itertools.permutations((1, 2, 3)))
IDENTITY = (0, 1, 2, 3)
CIRCUITS = (tuple(range(7)), tuple(range(7, 14)))
COLOUR_PAIRS = ((1, 2), (1, 3), (2, 3))


def derivative(encoded: str) -> tuple[int, ...]:
    pieces = encoded.split("|")
    assert tuple(map(len, pieces)) == (7, 7)
    result = []
    for piece in pieces:
        word = tuple(map(int, piece))
        result.extend(
            word[position - 1] ^ word[position] for position in range(7)
        )
    return tuple(result)


def integrate(transformed: tuple[int, ...]) -> tuple[int, ...] | None:
    base = [0] * 14
    for circuit in CIRCUITS:
        value = 0
        for position in circuit:
            value ^= transformed[position]
            base[position] = value
        if value:
            return None
    return tuple(base)


def clean(base: tuple[int, ...], partition: tuple[int, ...]) -> bool:
    for relative_shift in range(4):
        parity = [[0] * 4 for _ in range(5)]
        for circuit_index, circuit in enumerate(CIRCUITS):
            shift = relative_shift if circuit_index else 0
            for local, edge in enumerate(circuit):
                successor = circuit[(local + 1) % 7]
                left = partition[edge]
                right = partition[successor]
                if left == right:
                    continue
                colour = base[edge] ^ shift
                parity[left][colour] ^= 1
                parity[right][colour] ^= 1
        if not any(bit for row in parity for bit in row):
            return True
    return False


@functools.lru_cache(maxsize=None)
def classify(
    transitions: tuple[int, ...], partition: tuple[int, ...]
) -> tuple[int, int, int, dict[str, object] | None]:
    feasible = clean_count = delete_count = 0
    first_delete = None
    for tail in itertools.product(GL, repeat=4):
        maps = (IDENTITY,) + tail
        transformed = tuple(
            maps[partition[position]][transitions[position]]
            for position in range(14)
        )
        base = integrate(transformed)
        if base is None:
            continue
        feasible += 1
        if clean(base, partition):
            clean_count += 1
        for circuit_index, circuit in enumerate(CIRCUITS):
            used = {base[position] for position in circuit}
            if len(used) == 4:
                continue
            delete_count += 1
            if first_delete is None:
                missing = next(value for value in range(4) if value not in used)
                first_delete = {
                    "maps": ["".join(map(str, mapping)) for mapping in maps],
                    "base": (
                        "".join(map(str, base[:7]))
                        + "|"
                        + "".join(map(str, base[7:]))
                    ),
                    "delete_circuit": circuit_index,
                    "missing_colour": missing,
                }
            break
    return feasible, clean_count, delete_count, first_delete


def perfect_matchings(items: tuple[int, ...]):
    if not items:
        yield ()
        return
    first = items[0]
    for index in range(1, len(items)):
        second = items[index]
        remainder = items[1:index] + items[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


def circuit_index(position: int) -> int:
    return int(position >= 7)


def minimum_hitting_pairs(successful, matchings):
    pairs = tuple(sorted(successful))
    full = (1 << len(matchings)) - 1
    coverage = {}
    for pair in pairs:
        mask = 0
        for index, matching in enumerate(matchings):
            if pair in matching:
                mask |= 1 << index
        coverage[pair] = mask
    for size in range(1, len(pairs) + 1):
        for selected in itertools.combinations(pairs, size):
            covered = 0
            for pair in selected:
                covered |= coverage[pair]
            if covered == full:
                return selected
    raise AssertionError("successful pairs do not hit all matchings")


def blocks(partition: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            position
            for position, owner in enumerate(partition)
            if owner == block
        )
        for block in range(5)
    )


def switch(
    transitions: tuple[int, ...],
    primary: tuple[int, int],
    auxiliary: tuple[int, ...],
    delta: int,
) -> tuple[int, ...]:
    result = list(transitions)
    for position in primary + auxiliary:
        result[position] ^= delta
    return tuple(result)


def first_strategy(
    transitions: tuple[int, ...], partition: tuple[int, ...]
) -> dict[str, object]:
    state_blocks = blocks(partition)
    for active_block, occurrences in enumerate(state_blocks):
        if len(occurrences) not in (4, 6):
            continue
        for colours in COLOUR_PAIRS:
            terminals = tuple(
                position
                for position in occurrences
                if transitions[position] in colours
            )
            if len(terminals) < 4 or len(terminals) % 2:
                continue
            delta = colours[0] ^ colours[1]
            successful = {}
            for primary in itertools.combinations(terminals, 2):
                crosses = circuit_index(primary[0]) != circuit_index(primary[1])
                if crosses:
                    auxiliaries = []
                    for block, candidates in enumerate(state_blocks):
                        if block == active_block:
                            continue
                        endpoints = tuple(
                            position
                            for position in candidates
                            if transitions[position] in colours
                        )
                        if (
                            len(endpoints) == 2
                            and circuit_index(endpoints[0])
                            != circuit_index(endpoints[1])
                        ):
                            auxiliaries.append((block, endpoints))
                else:
                    auxiliaries = [(None, ())]

                best = None
                for auxiliary_block, auxiliary in auxiliaries:
                    modified = switch(
                        transitions, primary, auxiliary, delta
                    )
                    if any(
                        functools.reduce(
                            int.__xor__,
                            (modified[position] for position in circuit),
                            0,
                        )
                        for circuit in CIRCUITS
                    ):
                        continue
                    result = classify(modified, partition)
                    if result[2] == 0:
                        continue
                    candidate = (
                        result[2],
                        {
                            "pair": list(primary),
                            "auxiliary_block": auxiliary_block,
                            "auxiliary": list(auxiliary),
                            "feasible_maps": result[0],
                            "clean_maps": result[1],
                            "delete_maps": result[2],
                            **result[3],
                        },
                    )
                    if best is None or candidate[0] > best[0]:
                        best = candidate
                if best is not None:
                    successful[primary] = best[1]

            matchings = tuple(perfect_matchings(terminals))
            if matchings and all(
                any(pair in successful for pair in matching)
                for matching in matchings
            ):
                hitting_pairs = minimum_hitting_pairs(successful, matchings)
                return {
                    "active_block": active_block,
                    "block_size": len(occurrences),
                    "colours": list(colours),
                    "delta": delta,
                    "terminals": list(terminals),
                    "perfect_matchings": len(matchings),
                    "rows": [
                        successful[pair] for pair in hitting_pairs
                    ],
                }
    raise AssertionError("no deletion-only pairing-robust strategy")


def main() -> None:
    states = []
    for raw in FAILURES.read_text(encoding="utf-8").splitlines():
        match = LINE.fullmatch(raw)
        assert match
        states.append(match.groups())
    assert len(states) == len(set(states)) == 224

    records = []
    profiles = Counter()
    move_types = Counter()
    for index, (word, partition_text) in enumerate(states, 1):
        partition = tuple(map(int, partition_text))
        transitions = derivative(word)
        assert set(partition) == set(range(5))
        assert all(transitions)
        assert all(
            functools.reduce(
                int.__xor__,
                (
                    transitions[position]
                    for position, owner in enumerate(partition)
                    if owner == block
                ),
                0,
            )
            == 0
            for block in range(5)
        )

        # Independently confirm that the frozen input really is an
        # unrestricted clean-or-delete failure.
        original = classify(transitions, partition)
        assert original[0] > 0
        assert original[1] == original[2] == 0

        profile = tuple(
            sorted((len(row) for row in blocks(partition)), reverse=True)
        )
        profiles[profile] += 1
        strategy = first_strategy(transitions, partition)
        move_types[
            (
                profile,
                strategy["block_size"],
                len(strategy["terminals"]),
                tuple(strategy["colours"]),
            )
        ] += 1
        records.append(
            {
                "index": index,
                "word": word,
                "partition": partition_text,
                "derivative": "".join(map(str, transitions[:7]))
                + "|"
                + "".join(map(str, transitions[7:])),
                "profile": list(profile),
                "strategy": strategy,
            }
        )

    document = {
        "format": "fivecdc-size14-kempe-deletion-v1",
        "states": len(records),
        "profile_counts": {
            "+".join(map(str, key)): value
            for key, value in sorted(profiles.items())
        },
        "move_type_counts": [
            {
                "profile": list(key[0]),
                "block_size": key[1],
                "terminals": key[2],
                "colours": list(key[3]),
                "states": value,
            }
            for key, value in sorted(move_types.items())
        ],
        "records": records,
    }
    OUTPUT.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"states={len(records)}")
    print(f"profiles={dict(profiles)}")
    print(f"move_types={dict(move_types)}")
    print(f"wrote={OUTPUT.name}")
    print("PASS: all frozen failures have deletion-only Kempe escapes")


if __name__ == "__main__":
    main()
