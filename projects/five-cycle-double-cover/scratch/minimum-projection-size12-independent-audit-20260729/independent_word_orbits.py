#!/usr/bin/env python3
"""Independently emit canonical proper four-colour size-12 circuit words."""

import argparse
from itertools import permutations, product


def normalize(word):
    names = {}
    result = []
    for value in word:
        if value not in names:
            names[value] = len(names)
        result.append(names[value])
    return tuple(result)


def restricted_words(length):
    word = [0] * length

    def recurse(index, maximum):
        if index == length:
            if maximum == 3 and word[-1] != word[0]:
                yield tuple(word)
            return
        for value in range(min(3, maximum + 1) + 1):
            if value == word[index - 1]:
                continue
            word[index] = value
            yield from recurse(index + 1, max(maximum, value))

    yield from recurse(1, 0)


def all_words(length):
    return (
        word
        for word in product(range(4), repeat=length)
        if set(word) == set(range(4))
        and all(word[index] != word[(index + 1) % length]
                for index in range(length))
    )


def local_edge_orders(length, offset):
    for reflected in (False, True):
        for anchor in range(length):
            if reflected:
                yield tuple(
                    offset + (anchor - index - 1) % length
                    for index in range(length)
                )
            else:
                yield tuple(
                    offset + (anchor + index) % length
                    for index in range(length)
                )


def allowed_circuit_orders(lengths):
    return tuple(
        order
        for order in permutations(range(len(lengths)))
        if tuple(lengths[index] for index in order) == lengths
    )


def canonical(word, lengths):
    offsets = []
    offset = 0
    for length in lengths:
        offsets.append(offset)
        offset += length
    transforms = tuple(
        tuple(local_edge_orders(length, offset))
        for length, offset in zip(lengths, offsets)
    )
    circuit_orders = allowed_circuit_orders(lengths)
    return min(
        normalize(tuple(
            word[index]
            for circuit in circuit_order
            for index in selected[circuit]
        ))
        for selected in product(*transforms)
        for circuit_order in circuit_orders
    )


def representatives(lengths):
    first = tuple(restricted_words(lengths[0]))
    later = tuple(tuple(all_words(length)) for length in lengths[1:])
    return sorted({
        canonical(
            tuple(value for circuit in selected for value in circuit),
            lengths,
        )
        for selected in product(first, *later)
    })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "shape", choices=("12", "4+8", "5+7", "6+6", "4+4+4")
    )
    arguments = parser.parse_args()
    lengths = tuple(map(int, arguments.shape.split("+")))
    words = representatives(lengths)
    print(" ".join(map(str, lengths)))
    for word in words:
        print("".join(map(str, word)))


if __name__ == "__main__":
    main()
