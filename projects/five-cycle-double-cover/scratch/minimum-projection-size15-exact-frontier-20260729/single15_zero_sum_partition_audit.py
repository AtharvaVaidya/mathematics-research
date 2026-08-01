#!/usr/bin/env python3
"""Independent exact charge/dirty count for the one-circuit size-15 row.

This never enumerates set partitions.  It counts zero-sum set partitions
from multiplicity vectors by a distinguished-item recurrence.
"""

from __future__ import annotations

import argparse
import functools
import itertools
import math


D_TYPES = (1, 2, 3)
DZ_TYPES = (1, 2, 3, 5, 6, 7)


def normalize(values):
    names = {}
    result = []
    for value in values:
        if value not in names:
            names[value] = len(names)
        result.append(names[value])
    return tuple(result)


def canonical(word):
    length = len(word)
    candidates = []
    for anchor in range(length):
        candidates.append(
            normalize(
                tuple(word[(anchor + index) % length] for index in range(length))
            )
        )
        candidates.append(
            normalize(
                tuple(
                    word[(anchor - index - 1) % length]
                    for index in range(length)
                )
            )
        )
    return min(candidates)


def canonical_words(length):
    representatives = set()
    word = [0] * length

    def recurse(index, maximum):
        if index == length:
            if maximum == 3 and word[-1] != word[0]:
                representatives.add(canonical(tuple(word)))
            return
        for value in range(min(3, maximum + 1) + 1):
            if value == word[index - 1]:
                continue
            word[index] = value
            recurse(index + 1, max(maximum, value))

    recurse(1, 0)
    return tuple(sorted(representatives))


def multiplicities(labels, types):
    return tuple(labels.count(value) for value in types)


def zero_sum_partition_counter(types):
    @functools.cache
    def count(state):
        if not any(state):
            return 1
        first_type = next(
            index for index, multiplicity in enumerate(state) if multiplicity
        )
        distinguished = types[first_type]
        bounds = [
            range(multiplicity + 1 - (index == first_type))
            for index, multiplicity in enumerate(state)
        ]
        total = 0
        for selected in itertools.product(*bounds):
            xor = distinguished
            ways = 1
            for index, number in enumerate(selected):
                if number & 1:
                    xor ^= types[index]
                available = state[index] - (index == first_type)
                ways *= math.comb(available, number)
            if xor:
                continue
            remainder = tuple(
                state[index] - selected[index] - (index == first_type)
                for index in range(len(types))
            )
            total += ways * count(remainder)
        return total

    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, choices=(14, 15), default=15)
    args = parser.parse_args()
    length = args.length
    words = canonical_words(length)
    assert len(words) == {14: 7382, 15: 20004}[length]
    count_d = zero_sum_partition_counter(D_TYPES)
    count_dz = zero_sum_partition_counter(DZ_TYPES)
    charge_valid = initially_clean = 0
    d_profiles = set()
    dz_profiles = set()
    for word in words:
        derivatives = tuple(
            word[index - 1] ^ word[index] for index in range(length)
        )
        zero_incidence = tuple(
            int(word[index - 1] == 0) ^ int(word[index] == 0)
            for index in range(length)
        )
        combined = tuple(
            derivative | (incidence << 2)
            for derivative, incidence in zip(derivatives, zero_incidence)
        )
        d_state = multiplicities(derivatives, D_TYPES)
        dz_state = multiplicities(combined, DZ_TYPES)
        d_profiles.add(d_state)
        dz_profiles.add(dz_state)
        charge_valid += count_d(d_state)
        initially_clean += count_dz(dz_state)
    dirty = charge_valid - initially_clean
    print(
        f"RESULT canonical_words={len(words)}"
        f" length={length}"
        f" derivative_profiles={len(d_profiles)}"
        f" combined_profiles={len(dz_profiles)}"
        f" charge_valid={charge_valid}"
        f" initially_clean={initially_clean}"
        f" dirty={dirty}"
    )
    print("PASS")


if __name__ == "__main__":
    main()
