#!/usr/bin/env python3
"""Independent literal checker for the size-14 Kempe deletion certificates."""

from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from itertools import combinations
from operator import xor


DERIVATIVE = tuple(map(int, "31111212111311"))
CIRCUITS = (tuple(range(7)), tuple(range(7, 14)))


@dataclass(frozen=True)
class State:
    name: str
    partition: tuple[int, ...]
    switched_block: int
    delta: int
    certificates: dict[tuple[int, int], tuple[str, str, int, int]]


# A certificate row is
#     pair: (five component maps, zero-start bases, deleted circuit, missing colour).
# A map "abcd" means 0->a, 1->b, 2->c, 3->d.
SIX_TERMINAL = State(
    name="profile-6+2+2+2+2",
    partition=tuple(map(int, "01234444413024")),
    switched_block=4,
    delta=3,
    certificates={
        (4, 5): ("0123/0123/0123/0123/0321", "3232030|2101230", 0, 1),
        (4, 6): ("0123/0123/0123/0123/0123", "3232020|2323010", 0, 1),
        (4, 7): ("0123/0123/0123/0123/0123", "3101310|1023010", 0, 2),
        (4, 8): ("0123/0123/0123/0123/0123", "3101310|2023010", 0, 2),
        (4, 13): ("0123/0123/0123/0123/0123", "3101310|2310320", 0, 2),
        (5, 6): ("0123/0123/0123/0123/0123", "3232320|2323010", 0, 1),
        (5, 7): ("0123/0123/0123/0123/0123", "3101010|1023010", 0, 2),
        (5, 8): ("0123/0123/0123/0123/0123", "3101010|2023010", 0, 2),
        (5, 13): ("0123/0123/0123/0123/0123", "3101010|2310320", 0, 2),
        (6, 7): ("0123/0123/0123/0123/0132", "3101030|1023010", 0, 2),
        (6, 8): ("0123/0123/0123/0123/0132", "3101030|3023010", 0, 2),
        (6, 13): ("0123/0123/0123/0123/0132", "3101030|3201230", 0, 2),
        (7, 8): ("0123/0123/0123/0213/0213", "3231320|2320320", 1, 1),
        (7, 13): ("0123/0123/0123/0213/0312", "3231230|3013010", 1, 2),
        (8, 13): ("0123/0123/0123/0213/0213", "3231320|1013010", 1, 2),
    },
)


FOUR_TERMINAL_BLOCK_ZERO = State(
    name="profile-4+4+2+2+2-block0",
    partition=tuple(map(int, "00123404413024")),
    switched_block=0,
    delta=2,
    certificates={
        (0, 1): ("0123/0213/0123/0123/0213", "1201010|1310320", 0, 3),
        (0, 6): ("0123/0123/0123/0123/0123", "1010130|2323010", 0, 2),
        (0, 11): ("0123/0123/0213/0123/0213", "1031010|1301020", 0, 2),
        (1, 6): ("0123/0123/0123/0123/0123", "3010130|2323010", 0, 2),
        (1, 11): ("0123/0123/0213/0123/0213", "3031010|1301020", 0, 2),
        (6, 11): ("0123/0132/0213/0213/0132", "3202030|3202310", 0, 1),
    },
)


FOUR_TERMINAL_BLOCK_FOUR = State(
    name="profile-4+4+2+2+2-block4",
    partition=tuple(map(int, "00123404413024")),
    switched_block=4,
    delta=3,
    certificates={
        (5, 7): ("0123/0123/0123/0213/0213", "3201310|2020320", 1, 1),
        (5, 8): ("0123/0123/0123/0213/0231", "3201310|3020320", 1, 1),
        (5, 13): ("0123/0123/0123/0213/0213", "3201310|1313010", 1, 2),
        (7, 8): ("0123/0123/0123/0213/0213", "3232010|2320320", 1, 1),
        (7, 13): ("0123/0123/0123/0213/0312", "3232010|3013010", 1, 2),
        (8, 13): ("0123/0123/0123/0213/0213", "3232010|1013010", 1, 2),
    },
)


STATES = (
    SIX_TERMINAL,
    FOUR_TERMINAL_BLOCK_ZERO,
    FOUR_TERMINAL_BLOCK_FOUR,
)


def integrate(transformed: tuple[int, ...]) -> tuple[int, ...]:
    base = [0] * 14
    for circuit in CIRCUITS:
        value = 0
        for index in circuit:
            value ^= transformed[index]
            base[index] = value
        assert value == 0
    return tuple(base)


def check_state(state: State) -> None:
    terminals = tuple(
        index
        for index, block in enumerate(state.partition)
        if block == state.switched_block
    )
    assert set(state.certificates) == set(combinations(terminals, 2))

    auxiliary = tuple(
        index
        for index, block in enumerate(state.partition)
        if block == 1
    )
    assert len(auxiliary) == 2
    assert all(DERIVATIVE[index] == 1 for index in auxiliary)

    for pair, (map_text, base_text, deleted, missing) in (
        state.certificates.items()
    ):
        changed = list(DERIVATIVE)
        for index in pair:
            changed[index] ^= state.delta

        cross_circuit = (pair[0] < 7) != (pair[1] < 7)
        if cross_circuit:
            for index in auxiliary:
                changed[index] ^= state.delta

        # Both circuit closure and every component charge are necessary
        # before any component maps are applied.
        assert all(
            reduce(xor, (changed[index] for index in circuit), 0) == 0
            for circuit in CIRCUITS
        )
        assert all(
            reduce(
                xor,
                (
                    changed[index]
                    for index, block in enumerate(state.partition)
                    if block == component
                ),
                0,
            )
            == 0
            for component in range(5)
        )
        assert all(value in (1, 2, 3) for value in changed)

        maps = tuple(
            tuple(map(int, encoded)) for encoded in map_text.split("/")
        )
        assert len(maps) == 5
        assert all(mapping[0] == 0 for mapping in maps)
        assert all(set(mapping[1:]) == {1, 2, 3} for mapping in maps)

        transformed = tuple(
            maps[state.partition[index]][changed[index]]
            for index in range(14)
        )
        base = integrate(transformed)
        claimed_base = tuple(
            map(int, base_text.replace("|", ""))
        )
        assert base == claimed_base

        selected = tuple(base[index] for index in CIRCUITS[deleted])
        assert missing not in selected
        translated = tuple(value ^ missing for value in selected)
        assert all(translated)

    print(
        f"PASS {state.name}: "
        f"{len(state.certificates)} literal Kempe-deletion certificates"
    )


def main() -> None:
    assert reduce(xor, DERIVATIVE[:7], 0) == 0
    assert reduce(xor, DERIVATIVE[7:], 0) == 0
    for state in STATES:
        check_state(state)
    print("PASS: every listed Kempe endpoint pairing deletes a 7-circuit")


if __name__ == "__main__":
    main()
