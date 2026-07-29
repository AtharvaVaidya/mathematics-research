#!/usr/bin/env python3
"""Generate the 7+7 proper-word orbits without primary-project data."""

from itertools import product


def rename_by_first_occurrence(word):
    names = {}
    answer = []
    for value in word:
        if value not in names:
            names[value] = len(names)
        answer.append(names[value])
    return tuple(answer)


def dihedral_orders(offset):
    for anchor in range(7):
        yield tuple(offset + (anchor + step) % 7 for step in range(7))
        yield tuple(offset + (anchor - step - 1) % 7 for step in range(7))


ORDERS_A = tuple(dihedral_orders(0))
ORDERS_B = tuple(dihedral_orders(7))


def canonical(word):
    representatives = []
    for order_a in ORDERS_A:
        for order_b in ORDERS_B:
            representatives.append(
                rename_by_first_occurrence(
                    tuple(word[position] for position in order_a + order_b)
                )
            )
            representatives.append(
                rename_by_first_occurrence(
                    tuple(word[position] for position in order_b + order_a)
                )
            )
    return min(representatives)


def proper_seven_words():
    for word in product(range(4), repeat=7):
        if set(word) != {0, 1, 2, 3}:
            continue
        if any(word[i] == word[(i + 1) % 7] for i in range(7)):
            continue
        yield word


def colour_normalized_seven_words():
    word = [0] * 7

    def extend(position, largest):
        if position == 7:
            if largest == 3 and word[-1] != word[0]:
                yield tuple(word)
            return
        for value in range(min(3, largest + 1) + 1):
            if value == word[position - 1]:
                continue
            word[position] = value
            yield from extend(position + 1, max(largest, value))

    yield from extend(1, 0)


def main():
    proper = tuple(proper_seven_words())
    normalized = tuple(colour_normalized_seven_words())
    representatives = {
        canonical(first + second)
        for first in normalized
        for second in proper
    }
    print("7 7")
    for word in sorted(representatives):
        print("".join(map(str, word)))


if __name__ == "__main__":
    main()
