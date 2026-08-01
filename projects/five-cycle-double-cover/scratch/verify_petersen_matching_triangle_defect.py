#!/usr/bin/env python3
"""Solver-free Petersen audit for the matching/local-triangle defect.

Fix the standard Petersen graph with outer cycle a_i a_(i+1), inner
cycle b_i b_(i+2), and spoke matching a_i b_i (indices modulo five).
In a D5 labelling, let p_i be the label of spoke i.  The labels on either
5-cycle are a cyclic lift of the corresponding order of the p_i through
L(K_5).  The outer and inner orders are respectively

    0,1,2,3,4    and    0,2,4,1,3.

The program enumerates the 6,240 xor-zero spoke words, all of their cyclic
lifts, and checks the complete D5 semantics.  It also quotients the spoke
words by S5 on colours and AGL(1,5) on spoke indices, yielding the six-row
human table recorded in the accompanying note.

No SAT solver and no project graph helper is used.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product


ALL = (1 << 5) - 1
D5 = tuple(
    (1 << first) | (1 << second)
    for first in range(5)
    for second in range(first + 1, 5)
)
OUTER_ORDER = (0, 1, 2, 3, 4)
INNER_ORDER = (0, 2, 4, 1, 3)

# Vertices 0,...,4 are a_0,...,a_4 and 5,...,9 are b_0,...,b_4.
PETERSEN_EDGES = frozenset(
    {frozenset((index, (index + 1) % 5)) for index in range(5)}
    | {frozenset((5 + index, 5 + (index + 2) % 5)) for index in range(5)}
    | {frozenset((index, 5 + index)) for index in range(5)}
)
SPOKE_MATCHING = frozenset(
    frozenset((index, 5 + index)) for index in range(5)
)

# One explicitly checkable automorphism carrying the spoke matching to
# each of the six perfect matchings.  An entry sigma[v] is the image of v.
AUTOMORPHISM_TRANSVERSAL = (
    (0, 4, 3, 8, 5, 1, 9, 2, 6, 7),
    (0, 4, 9, 7, 5, 1, 3, 6, 2, 8),
    (0, 1, 6, 8, 5, 4, 2, 9, 3, 7),
    (0, 1, 2, 7, 5, 4, 6, 3, 9, 8),
    (0, 1, 6, 9, 4, 5, 2, 8, 7, 3),
    tuple(range(10)),
)


def edge_image(
    edges: frozenset[frozenset[int]], permutation: tuple[int, ...]
) -> frozenset[frozenset[int]]:
    return frozenset(
        frozenset(permutation[vertex] for vertex in edge)
        for edge in edges
    )


def check_perfect_matching_transitivity() -> None:
    """Enumerate all perfect matchings and verify an explicit orbit transversal."""
    perfect_matchings = set()
    for candidate in combinations(PETERSEN_EDGES, 5):
        degree = Counter(vertex for edge in candidate for vertex in edge)
        if len(degree) == 10 and all(value == 1 for value in degree.values()):
            perfect_matchings.add(frozenset(candidate))

    assert len(perfect_matchings) == 6
    matching_images = set()
    for permutation in AUTOMORPHISM_TRANSVERSAL:
        assert tuple(sorted(permutation)) == tuple(range(10))
        assert edge_image(PETERSEN_EDGES, permutation) == PETERSEN_EDGES
        matching_images.add(edge_image(SPOKE_MATCHING, permutation))
    assert matching_images == perfect_matchings


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for colour in range(5):
        if mask & (1 << colour):
            result |= 1 << permutation[colour]
    return result


COLOUR_ACTIONS = tuple(
    tuple(permute_mask(mask, permutation) for mask in range(32))
    for permutation in permutations(range(5))
)
INDEX_ACTIONS = tuple(
    (multiplier, offset)
    for multiplier in range(1, 5)
    for offset in range(5)
)


def canonical(word: tuple[int, ...]) -> tuple[int, ...]:
    best: tuple[int, ...] | None = None
    for action in COLOUR_ACTIONS:
        recoloured = tuple(action[label] for label in word)
        for multiplier, offset in INDEX_ACTIONS:
            image = [0] * 5
            for index, label in enumerate(recoloured):
                image[(multiplier * index + offset) % 5] = label
            candidate = tuple(image)
            if best is None or candidate < best:
                best = candidate
    assert best is not None
    return best


def cyclic_lifts(
    word: tuple[int, ...], order: tuple[int, ...]
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    """Return (cycle-edge labels by traversal, local q_i by spoke index)."""
    lifts = []
    for initial in D5:
        current = initial
        cycle_labels = []
        local_complements = [0] * 5
        valid = True
        for vertex in order:
            following = current ^ word[vertex]
            if following not in D5:
                valid = False
                break
            # The two cycle labels and the spoke label are the three edges
            # of a K5 triangle.  Its two-colour complement is q_v.
            local_complements[vertex] = ALL ^ (current | following)
            cycle_labels.append(following)
            current = following
        if valid and current == initial:
            lifts.append((tuple(cycle_labels), tuple(local_complements)))
    return tuple(lifts)


def check_literal_petersen_model(
    word: tuple[int, ...],
    outer_lift: tuple[tuple[int, ...], tuple[int, ...]],
    inner_lift: tuple[tuple[int, ...], tuple[int, ...]],
) -> int:
    outer_labels, outer_q = outer_lift
    inner_labels_in_traversal_order, inner_q = inner_lift
    assert all(label in D5 for label in word)
    assert all(label in D5 for label in outer_labels)
    assert all(label in D5 for label in inner_labels_in_traversal_order)

    # outer_labels[i] is a_i a_(i+1).
    for index in range(5):
        incident = (
            outer_labels[(index - 1) % 5],
            outer_labels[index],
            word[index],
        )
        assert incident[0] ^ incident[1] ^ incident[2] == 0
        triangle = incident[0] | incident[1] | incident[2]
        assert triangle.bit_count() == 3
        assert outer_q[index] == ALL ^ triangle

    # inner_labels_in_traversal_order[j] follows INNER_ORDER[j].
    inner_after = {
        vertex: inner_labels_in_traversal_order[position]
        for position, vertex in enumerate(INNER_ORDER)
    }
    inner_before = {
        INNER_ORDER[position]: inner_labels_in_traversal_order[position - 1]
        for position in range(5)
    }
    for index in range(5):
        incident = (inner_before[index], inner_after[index], word[index])
        assert incident[0] ^ incident[1] ^ incident[2] == 0
        triangle = incident[0] | incident[1] | incident[2]
        assert triangle.bit_count() == 3
        assert inner_q[index] == ALL ^ triangle

    return sum(
        outer_q[index] == inner_q[index]
        for index in range(5)
    )


def pair_text(mask: int) -> str:
    return "".join(str(index) for index in range(5) if mask & (1 << index))


def main() -> None:
    check_perfect_matching_transitivity()

    words = []
    for prefix in product(D5, repeat=4):
        final = 0
        for label in prefix:
            final ^= label
        if final in D5:
            words.append(prefix + (final,))
    assert len(words) == 6_240

    orbit_members: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for word in words:
        orbit_members.setdefault(canonical(word), []).append(word)

    expected_rows = (
        ("01 01 01 02 12", 600, 3, 0, None),
        ("01 01 02 03 23", 2_400, 2, 0, None),
        ("01 01 02 23 03", 1_200, 1, 2, 0),
        ("01 01 23 24 34", 600, 2, 2, 2),
        ("01 02 13 24 34", 1_200, 1, 1, 1),
        ("01 02 23 34 14", 240, 0, 1, None),
    )

    actual_rows = []
    # First perform the literal, unquotiented semantic enumeration.
    histogram: Counter[int] = Counter()
    both_liftable_words = 0
    literal_labellings = 0
    witness = None
    for word in words:
        outer = cyclic_lifts(word, OUTER_ORDER)
        inner = cyclic_lifts(word, INNER_ORDER)
        if outer and inner:
            both_liftable_words += 1
        for outer_lift in outer:
            for inner_lift in inner:
                equal_count = check_literal_petersen_model(
                    word, outer_lift, inner_lift
                )
                histogram[equal_count] += 1
                literal_labellings += 1
                if witness is None or equal_count > witness[0]:
                    witness = (
                        equal_count,
                        word,
                        outer_lift,
                        inner_lift,
                    )

    # Then construct the independent six-row quotient presentation.
    for representative, members in sorted(orbit_members.items()):
        outer = cyclic_lifts(representative, OUTER_ORDER)
        inner = cyclic_lifts(representative, INNER_ORDER)
        defects = []
        for outer_lift in outer:
            for inner_lift in inner:
                equal_count = check_literal_petersen_model(
                    representative, outer_lift, inner_lift
                )
                defects.append(equal_count)
        row = (
            " ".join(pair_text(label) for label in representative),
            len(members),
            len(outer),
            len(inner),
            max(defects) if defects else None,
        )
        actual_rows.append(row)

    assert tuple(actual_rows) == expected_rows
    assert both_liftable_words == 3_000
    assert literal_labellings == 6_000
    assert histogram == Counter({0: 2_400, 1: 2_400, 2: 1_200})
    assert witness is not None and witness[0] == 2

    print("Petersen matching/local-triangle defect: PASS")
    print("perfect matchings: 6, covered by explicit automorphisms: 6")
    print("xor-zero spoke words: 6240")
    print("S5 x AGL(1,5) word orbits: 6")
    print("words liftable in both Petersen cycle orders: 3000")
    print("literal fixed-matching D5 labellings: 6000")
    print("equal matching-edge endpoint triangles: 0:2400 1:2400 2:1200")
    print("maximum equal matching-edge endpoint triangles: 2 of 5")
    print("six-row quotient table:")
    for row in actual_rows:
        maximum = "-" if row[4] is None else str(row[4])
        print(
            f"  {row[0]} | orbit={row[1]} outer={row[2]} "
            f"inner={row[3]} max={maximum}"
        )


if __name__ == "__main__":
    main()
