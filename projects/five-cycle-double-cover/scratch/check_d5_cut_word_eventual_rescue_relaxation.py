#!/usr/bin/env python3
"""Exhaust the constructive relaxed cut-word termination theorem."""

from __future__ import annotations

import itertools


COORDINATES = range(5)
PAIRS = tuple(itertools.combinations(COORDINATES, 2))
LABELS = tuple(
    sum(1 << coordinate for coordinate in pair) for pair in PAIRS
)


def active(label, target):
    mask = (1 << target[0]) | (1 << target[1])
    return (label & mask).bit_count() == 1


def transpose(label, pair):
    mask = (1 << pair[0]) | (1 << pair[1])
    if (label & mask).bit_count() == 1:
        return label ^ mask
    return label


def repair(word, target):
    state = list(word)
    moves = []
    for position in range(len(state) - 1, -1, -1):
        fixed_suffix = tuple(state[position + 1 :])
        assert all(active(label, target) for label in fixed_suffix)
        if active(state[position], target):
            continue
        pair = next(
            candidate
            for candidate in PAIRS
            if active(transpose(state[position], candidate), target)
        )
        for index in range(position + 1):
            state[index] = transpose(state[index], pair)
        assert tuple(state[position + 1 :]) == fixed_suffix
        assert active(state[position], target)
        moves.append((position, pair))
    assert all(active(label, target) for label in state)
    assert len(moves) <= len(word)
    return tuple(state), tuple(moves)


def main():
    words = 0
    target_tests = 0
    for length in range(6):
        for word in itertools.product(LABELS, repeat=length):
            words += 1
            for target in PAIRS:
                target_tests += 1
                final, moves = repair(word, target)
                assert len(final) == length
                assert len(moves) <= length
    assert words == sum(10**length for length in range(6))
    assert target_tests == 10 * words
    print(
        "PASS: every word through length 5 and all ten target factors; "
        f"words={words}, target_tests={target_tests}"
    )


if __name__ == "__main__":
    main()
