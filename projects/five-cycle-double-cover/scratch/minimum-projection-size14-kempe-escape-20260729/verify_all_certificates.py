#!/usr/bin/env python3
"""Literal replay of the frozen all-state Kempe deletion certificate."""

from __future__ import annotations

import json
import re
from collections import Counter
from functools import reduce
from itertools import combinations
from operator import xor
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FAILURES = ROOT / "failure-states.txt"
CERTIFICATE = ROOT / "all-kempe-certificates.json"
LINE = re.compile(r"COUNTERSTATE word=(\S+) partition=(\d+)$")
CIRCUITS = (tuple(range(7)), tuple(range(7, 14)))


def derivatives(word_text: str) -> tuple[int, ...]:
    answer = []
    for text in word_text.split("|"):
        values = tuple(map(int, text))
        assert len(values) == 7
        answer.extend(
            values[(index - 1) % 7] ^ values[index]
            for index in range(7)
        )
    return tuple(answer)


def all_matchings(vertices: tuple[int, ...]):
    if len(vertices) == 0:
        yield ()
        return
    anchor = vertices[0]
    for partner_index in range(1, len(vertices)):
        partner = vertices[partner_index]
        unused = vertices[1:partner_index] + vertices[partner_index + 1 :]
        for continuation in all_matchings(unused):
            yield ((anchor, partner),) + continuation


def integrate(values: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * 14
    for circuit in CIRCUITS:
        running = 0
        for position in circuit:
            running ^= values[position]
            result[position] = running
        assert running == 0
    return tuple(result)


def main() -> None:
    frozen_states = []
    for text in FAILURES.read_text(encoding="utf-8").splitlines():
        parsed = LINE.fullmatch(text)
        assert parsed
        frozen_states.append(parsed.groups())
    assert len(frozen_states) == len(set(frozen_states)) == 224

    document = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert document["format"] == "fivecdc-size14-kempe-deletion-v1"
    assert document["states"] == len(document["records"]) == 224
    assert [
        (record["word"], record["partition"])
        for record in document["records"]
    ] == frozen_states

    profiles = Counter()
    move_types = Counter()
    total_rows = 0
    four_of_six = 0
    for expected_index, record in enumerate(document["records"], 1):
        assert record["index"] == expected_index
        transition = derivatives(record["word"])
        assert record["derivative"] == (
            "".join(map(str, transition[:7]))
            + "|"
            + "".join(map(str, transition[7:]))
        )
        partition = tuple(map(int, record["partition"]))
        assert len(partition) == 14
        assert set(partition) == set(range(5))
        block_rows = tuple(
            tuple(
                position
                for position, owner in enumerate(partition)
                if owner == block
            )
            for block in range(5)
        )
        profile = tuple(
            sorted((len(block) for block in block_rows), reverse=True)
        )
        assert list(profile) == record["profile"]
        profiles[profile] += 1

        strategy = record["strategy"]
        active_block = strategy["active_block"]
        colours = tuple(strategy["colours"])
        assert len(colours) == 2
        assert all(value in (1, 2, 3) for value in colours)
        assert colours[0] != colours[1]
        delta = colours[0] ^ colours[1]
        assert strategy["delta"] == delta
        occurrences = block_rows[active_block]
        assert strategy["block_size"] == len(occurrences)
        terminals = tuple(
            position
            for position in occurrences
            if transition[position] in colours
        )
        assert strategy["terminals"] == list(terminals)
        assert len(terminals) in (4, 6)
        if len(occurrences) == 6 and len(terminals) == 4:
            four_of_six += 1

        matchings = tuple(all_matchings(terminals))
        assert strategy["perfect_matchings"] == len(matchings)
        row_pairs = {
            tuple(row["pair"]) for row in strategy["rows"]
        }
        assert len(row_pairs) == len(strategy["rows"])
        assert row_pairs <= set(combinations(terminals, 2))
        assert all(
            any(pair in row_pairs for pair in matching)
            for matching in matchings
        )

        total_rows += len(strategy["rows"])
        move_types[
            (profile, len(occurrences), len(terminals), colours)
        ] += 1
        for row in strategy["rows"]:
            pair = tuple(row["pair"])
            cross = (pair[0] < 7) != (pair[1] < 7)
            auxiliary = tuple(row["auxiliary"])
            auxiliary_block = row["auxiliary_block"]
            if cross:
                assert auxiliary_block is not None
                assert auxiliary_block != active_block
                expected_auxiliary = tuple(
                    position
                    for position in block_rows[auxiliary_block]
                    if transition[position] in colours
                )
                assert auxiliary == expected_auxiliary
                assert len(auxiliary) == 2
                assert (auxiliary[0] < 7) != (auxiliary[1] < 7)
            else:
                assert auxiliary_block is None
                assert auxiliary == ()

            changed = list(transition)
            for position in pair + auxiliary:
                assert changed[position] in colours
                changed[position] ^= delta
                assert changed[position] in colours
            changed = tuple(changed)
            assert all(
                reduce(
                    xor,
                    (changed[position] for position in circuit),
                    0,
                )
                == 0
                for circuit in CIRCUITS
            )
            assert all(
                reduce(
                    xor,
                    (
                        changed[position]
                        for position, owner in enumerate(partition)
                        if owner == block
                    ),
                    0,
                )
                == 0
                for block in range(5)
            )

            maps = tuple(
                tuple(map(int, encoded)) for encoded in row["maps"]
            )
            assert len(maps) == 5
            assert all(mapping[0] == 0 for mapping in maps)
            assert all(set(mapping[1:]) == {1, 2, 3} for mapping in maps)
            transformed = tuple(
                maps[partition[position]][changed[position]]
                for position in range(14)
            )
            base = integrate(transformed)
            assert row["base"] == (
                "".join(map(str, base[:7]))
                + "|"
                + "".join(map(str, base[7:]))
            )

            deleted = row["delete_circuit"]
            missing = row["missing_colour"]
            assert deleted in (0, 1)
            assert missing in range(4)
            selected = tuple(base[position] for position in CIRCUITS[deleted])
            assert missing not in selected
            assert all(value ^ missing for value in selected)
            assert row["feasible_maps"] > 0
            assert row["delete_maps"] > 0

    assert profiles == Counter(
        {
            (6, 2, 2, 2, 2): 46,
            (4, 4, 2, 2, 2): 178,
        }
    )
    assert four_of_six == 20
    assert total_rows == 724
    assert document["profile_counts"] == {
        "4+4+2+2+2": 178,
        "6+2+2+2+2": 46,
    }
    encoded_move_types = Counter(
        {
            (
                tuple(row["profile"]),
                row["block_size"],
                row["terminals"],
                tuple(row["colours"]),
            ): row["states"]
            for row in document["move_type_counts"]
        }
    )
    assert move_types == encoded_move_types

    print("states=224")
    print("profiles=46*(6+2+2+2+2),178*(4+4+2+2+2)")
    print("four-terminal strategies on six-blocks=20")
    print("literal deletion rows=724")
    print("PASS: every perfect matching hits a checked deletion row")


if __name__ == "__main__":
    main()
