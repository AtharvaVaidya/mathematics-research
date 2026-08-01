#!/usr/bin/env python3
"""Independent count-vector audit of the partner-free threshold.

Unlike verify_minimal_profiles.py, this checker never constructs sorted
multisets.  It enumerates weak compositions into the six allowed value
classes and evaluates XOR from the parities of their multiplicities.
"""

from __future__ import annotations


def weak_compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, parts - 1):
            yield (first,) + rest


def main() -> None:
    expected = {
        3: (28, 0),
        5: (168, 0),
        7: (588, 0),
        9: (1568, 28),
    }
    observed = {}

    for k in (3, 5, 7, 9):
        admissible = 0
        bad = 0
        for b in range(1, 8):
            values = tuple(value for value in range(1, 8) if value != b)
            index = {value: position for position, value in enumerate(values)}
            for counts in weak_compositions(k, 6):
                cut_xor = 0
                for value, count in zip(values, counts):
                    if count & 1:
                        cut_xor ^= value
                if cut_xor != b:
                    continue
                admissible += 1
                support = {
                    value for value, count in zip(values, counts) if count
                }
                no_partner_free = all(
                    counts[index[value ^ b]] > 0 for value in support
                )
                bad += no_partner_free
        observed[k] = (admissible, bad)

    assert observed == expected, (observed, expected)
    for k in (3, 5, 7, 9):
        admissible, bad = observed[k]
        print(f"k={k}: admissible_count_vectors={admissible} bad={bad}")
    print("INDEPENDENT PASS")


if __name__ == "__main__":
    main()
