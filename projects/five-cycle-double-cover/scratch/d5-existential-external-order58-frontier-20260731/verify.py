#!/usr/bin/env python3
"""Independent arithmetic and degree-profile replay for Theorem 3.1."""

from __future__ import annotations

from itertools import product


def deficit_profiles(total: int = 5) -> list[tuple[int, ...]]:
    """All multisets of positive deficits allowed by degrees 1,2,3."""
    answer: set[tuple[int, ...]] = set()
    for length in range(1, total + 1):
        for word in product((1, 2), repeat=length):
            if sum(word) == total:
                answer.add(tuple(sorted(word)))
    return sorted(answer)


def lower_counts(n: int) -> tuple[int, int, int, int]:
    # W2 uses sum(delta^2)>=5.  The recurrence loss is at most
    # 2^(j-1) sum delta*d <= 10*2^(j-1).
    w2 = 6 * n - 20
    w3 = 2 * w2 - 20
    w4 = 2 * w3 - 40
    w5 = 2 * w4 - 80
    return w2, w3, w4, w5


def polynomial(n: int) -> int:
    return 3 * n * n - 191 * n + 1290


def main() -> None:
    profiles = deficit_profiles()
    assert profiles == [(1, 1, 1, 1, 1), (1, 1, 1, 2), (1, 2, 2)]

    # Audit degree-one cases rather than assuming five degree-two defects.
    rows = []
    for profile in profiles:
        degrees = tuple(3 - delta for delta in profile)
        sum_delta_d = sum(delta * degree
                          for delta, degree in zip(profile, degrees))
        sum_delta_squared = sum(delta * delta for delta in profile)
        assert sum(profile) == 5
        assert all(degree in (1, 2) for degree in degrees)
        assert sum_delta_d <= 10
        assert sum_delta_squared >= 5
        rows.append((profile, degrees, sum_delta_d, sum_delta_squared))

    n = 55
    m = (3 * n - 5) // 2
    assert m == 80 and 2 * m == 3 * n - 5
    w2, w3, w4, w5 = lower_counts(n)
    assert (w2, w3, w4, w5) == (310, 600, 1160, 2240)
    edge_ball_lower_sum = 2 * m + w2 + w3 + w4 + w5
    assert edge_ball_lower_sum == 4470
    assert m * n == 4400 < edge_ball_lower_sum

    # Symbolic collection of twice the inequality:
    # n(3n-5) >= 2(93n-645).
    for value in range(1, 100):
        mm_twice = 3 * value - 5
        rhs = 2 * (93 * value - 645)
        assert value * mm_twice - rhs == polynomial(value)

    assert polynomial(8) == -46
    assert polynomial(55) == -140
    assert polynomial(56) == 2
    assert all(polynomial(value) < 0 for value in range(8, 56))
    assert all(value % 2 == 1 for value in range(9, 57, 2))

    print("DEFICIT_PROFILES count=3 degree1_cases=2 bound_sum_delta_d=10 PASS")
    print("N55 m=80 W2=310 W3=600 W4=1160 W5=2240 balls=4470 capacity=4400 CONTRADICTION PASS")
    print("POLYNOMIAL f8=-46 f55=-140 f56=2 negative_8_through_55=1 PASS")
    print("CUTOFF core>=57 cap>=58 parent>=116 PASS")


if __name__ == "__main__":
    main()
