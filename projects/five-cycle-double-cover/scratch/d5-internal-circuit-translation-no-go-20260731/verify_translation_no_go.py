#!/usr/bin/env python3
"""Exhaustive replay of the normalized same-circuit translation no-go lemma."""

from __future__ import annotations

import itertools


def label(*coordinates: int) -> int:
    value = 0
    for coordinate in coordinates:
        value |= 1 << coordinate
    return value


def name(value: int) -> str:
    if value == 0:
        return "empty"
    return "".join(str(i) for i in range(5) if value & (1 << i))


D5 = tuple(label(*pair) for pair in itertools.combinations(range(5), 2))
EVEN = tuple(value for value in range(1 << 5) if value.bit_count() % 2 == 0)
P = label(1, 2)
PORT_A = label(0, 1)
PORT_B = label(0, 2)
EXTERNAL = tuple(value for value in D5 if not (value & P))


def active(edge_label: int, pair: int) -> bool:
    return (edge_label & pair).bit_count() == 1


def legal(edge_label: int, shift: int) -> bool:
    return (edge_label ^ shift).bit_count() == 2


def main() -> None:
    assert tuple(map(name, EXTERNAL)) == ("03", "04", "34")

    local_rows: list[tuple[int, tuple[int, ...]]] = []
    for shift in EVEN:
        if not all(legal(value, shift) for value in (PORT_A, PORT_B)):
            continue
        targets = tuple(
            pair
            for pair in EXTERNAL
            if all(active(value ^ shift, pair) for value in (PORT_A, PORT_B))
        )
        if targets:
            local_rows.append((shift, targets))

    expected_rows = (
        (0, (label(0, 3), label(0, 4))),
        (label(1, 2), (label(0, 3), label(0, 4))),
        (label(0, 3), (label(0, 3), label(3, 4))),
        (label(0, 1, 2, 3), (label(0, 3), label(3, 4))),
        (label(0, 4), (label(0, 4), label(3, 4))),
        (label(0, 1, 2, 4), (label(0, 4), label(3, 4))),
    )
    # Sort by the human table rather than integer bit-mask order.
    row_map = {shift: targets for shift, targets in local_rows}
    assert set(local_rows) == set(expected_rows)
    for shift, expected_targets in expected_rows:
        assert row_map[shift] == expected_targets
        print(
            "LOCAL"
            f" shift={name(shift)}"
            f" targets={','.join(map(name, expected_targets))}"
        )

    crossing = tuple(value for value in D5 if active(value, P))
    supports: list[frozenset[int]] = []
    for size in range(len(crossing) + 1):
        for chosen in itertools.combinations(crossing, size):
            support = frozenset(chosen)
            if {PORT_A, PORT_B} <= support:
                supports.append(support)

    admissible_cases = 0
    counterexamples: list[tuple[frozenset[int], int, int]] = []
    for support in supports:
        for shift in EVEN:
            if not all(legal(value, shift) for value in support):
                continue
            for target in EXTERNAL:
                if not all(active(value ^ shift, target) for value in support):
                    continue
                admissible_cases += 1
                original_external = [
                    pair
                    for pair in EXTERNAL
                    if all(active(value, pair) for value in support)
                ]
                if not original_external:
                    counterexamples.append((support, shift, target))

    print(f"SUPPORTS {len(supports)}")
    print(f"ADMISSIBLE_CASES {admissible_cases}")
    print(f"COUNTEREXAMPLES {len(counterexamples)}")
    assert len(supports) == 16
    assert admissible_cases == 36
    assert not counterexamples
    print("PASS")


if __name__ == "__main__":
    main()
