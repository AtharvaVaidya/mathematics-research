#!/usr/bin/env python3
"""Independent count of charge-valid partitions for the fixed word."""

from __future__ import annotations

import functools
import math


DERIVATIVE = tuple(map(int, "3111113121113132"))
N = len(DERIVATIVE)


def main() -> None:
    charge = [0] * (1 << N)
    blocks = [[] for _ in range(N)]
    for mask in range(1, 1 << N):
        bit = (mask & -mask).bit_length() - 1
        charge[mask] = charge[mask ^ (1 << bit)] ^ DERIVATIVE[bit]
        if charge[mask] == 0:
            blocks[bit].append(mask)

    @functools.cache
    def partitions(remaining: int) -> int:
        if remaining == 0:
            return 1
        first = (remaining & -remaining).bit_length() - 1
        return sum(
            partitions(remaining ^ block)
            for block in blocks[first]
            if block & remaining == block
        )

    total = partitions((1 << N) - 1)
    assert total == 8_046_330

    # A size-two zero-charge block pairs equal derivative values.  The
    # total multiplicities are 10,2,4, giving 9!! 1!! 3!! pairings.
    multiplicities = tuple(DERIVATIVE.count(value) for value in (1, 2, 3))
    pair_partitions = math.prod(
        math.prod(range(count - 1, 0, -2))
        for count in multiplicities
    )
    assert multiplicities == (10, 2, 4)
    assert pair_partitions == 2_835

    # No all-cross-circuit pairing exists: derivative value 2 occurs zero
    # times on the first circuit and twice on the second.
    first_counts = tuple(DERIVATIVE[:8].count(value) for value in (1, 2, 3))
    second_counts = tuple(DERIVATIVE[8:].count(value) for value in (1, 2, 3))
    assert first_counts == (6, 0, 2)
    assert second_counts == (4, 2, 2)
    cross_pair_partitions = 0

    print(
        f"PARTITIONS charge_valid={total}"
        f" derivative_multiplicities={multiplicities}"
    )
    print(
        f"PAIR_SUBCASE all_pair_partitions={pair_partitions}"
        f" loopless_cross_pair_partitions={cross_pair_partitions}"
        f" loop_only_partitions={pair_partitions}"
    )
    print("PASS independent partition-count recurrence")


if __name__ == "__main__":
    main()
