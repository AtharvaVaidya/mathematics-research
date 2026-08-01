#!/usr/bin/env python3
"""Finite audit of the minimal larger-blocker value profiles.

The seven nonzero vectors of F_2^3 are represented by the integers 1..7,
with vector addition represented by bitwise XOR.  For a fixed target b, an
H-cut value is nonzero and different from b.  An odd blocker has an odd
number k of H-cut values whose XOR is b.

This script checks the partner-free lemma for k=3,5,7, exhibits its sharp
failure at k=9, and checks the two possible flow-cut XORs in the cut-space
argument.  It is deliberately independent of every graph/SAT implementation.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations_with_replacement


def xor_all(values: tuple[int, ...]) -> int:
    answer = 0
    for value in values:
        answer ^= value
    return answer


def partner_free(values: tuple[int, ...], b: int) -> tuple[int, ...]:
    support = set(values)
    return tuple(sorted(value for value in support if (value ^ b) not in support))


def admissible_profiles(b: int, k: int) -> tuple[tuple[int, ...], ...]:
    alphabet = tuple(value for value in range(1, 8) if value != b)
    return tuple(
        values
        for values in combinations_with_replacement(alphabet, k)
        if xor_all(values) == b
    )


def main() -> None:
    totals: Counter[int] = Counter()
    failures: Counter[int] = Counter()

    for b in range(1, 8):
        for k in (3, 5, 7, 9):
            profiles = admissible_profiles(b, k)
            totals[k] += len(profiles)
            failures[k] += sum(not partner_free(values, b) for values in profiles)

            if k < 9:
                assert all(partner_free(values, b) for values in profiles)
            if k == 3:
                assert all(len(set(values)) == 3 for values in profiles)
                assert all(
                    set(partner_free(values, b)) == set(values)
                    for values in profiles
                )

    sharp = (2, 2, 3, 4, 4, 5, 6, 6, 7)
    assert xor_all(sharp) == 1
    assert not partner_free(sharp, 1)

    # In the cycle/cut contradiction, the full cut consists of an odd
    # number of b-edges and either an even or an odd number of t-edges.
    # Its XOR is therefore b or b+t, never zero for distinct nonzero b,t.
    cut_xor_cases = 0
    for b in range(1, 8):
        for t in range(1, 8):
            if t == b:
                continue
            for t_parity in (0, 1):
                assert b ^ (t if t_parity else 0)
                cut_xor_cases += 1

    print("minimal larger profiles: (k,q)=(3,3) and (5,1)")
    for k in (3, 5, 7, 9):
        print(
            f"k={k}: admissible_multisets={totals[k]} "
            f"without_partner_free_direction={failures[k]}"
        )
    print("sharp k=9 no-partner-free example for b=1:", ",".join(map(str, sharp)))
    print(f"nonzero cut-XOR cases checked={cut_xor_cases}")
    print("PASS")


if __name__ == "__main__":
    main()
