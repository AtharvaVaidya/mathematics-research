#!/usr/bin/env python3
"""Exhaust the FiveCDC boundary relation of K3,3 minus adjacent vertices.

The proper core is K2,2.  Ports are ordered x0,x1,y0,y1, with x0,x1 in
one bipartition and y0,y1 in the other.  Proper edges are ordered
x0y0,x0y1,x1y0,x1y1.
"""

from itertools import permutations, product


LABELS = tuple((1 << a) | (1 << b) for a in range(5) for b in range(a + 1, 5))
REPRESENTATIVE = (0b00101, 0b00101, 0b01001, 0b01001)  # 02,02,03,03


def permute_label(label: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for old in range(5):
        if (label >> old) & 1:
            result |= 1 << permutation[old]
    return result


def main() -> None:
    admissible = {
        word
        for word in product(LABELS, repeat=4)
        if word[0] ^ word[1] ^ word[2] ^ word[3] == 0
    }
    relation: set[tuple[int, int, int, int]] = set()
    for e00, e01, e10, e11 in product(LABELS, repeat=4):
        boundary = (
            e00 ^ e01,
            e10 ^ e11,
            e00 ^ e10,
            e01 ^ e11,
        )
        if all(label in LABELS for label in boundary):
            relation.add(boundary)

    missing = admissible - relation
    orbit = {
        tuple(permute_label(label, permutation) for label in REPRESENTATIVE)
        for permutation in permutations(range(5))
    }

    assert len(admissible) == 640
    assert len(relation) == 580
    assert len(missing) == 60
    assert len(orbit) == 60
    assert missing == orbit
    assert REPRESENTATIVE not in relation

    print("PASS K3,3 adjacent-deletion four-pole boundary")
    print("admissible xor-zero words: 640")
    print("extended words: 580")
    print("missing words: 60")
    print("missing orbit representative: 02 02 03 03")


if __name__ == "__main__":
    main()
