#!/usr/bin/env python3
"""Dependency-free audit of the size-at-most-five boundary case split."""

from itertools import permutations, product


def set_partitions(order):
    labels = [0] * order

    def recurse(index, maximum):
        if index == order:
            yield tuple(labels)
            return
        for value in range(maximum + 2):
            labels[index] = value
            yield from recurse(index + 1, max(maximum, value))

    yield from recurse(1, 0)


def canonical_words(order):
    """Proper cyclic four-colour words using every colour, modulo S4."""
    representatives = set()
    for tail in product(range(4), repeat=order - 1):
        word = (0,) + tail
        if any(word[index] == word[(index + 1) % order]
               for index in range(order)):
            continue
        if set(word) != set(range(4)):
            continue
        orbit = []
        for permutation in permutations(range(4)):
            renamed = tuple(permutation[value] for value in word)
            for shift in range(order):
                rotated = renamed[shift:] + renamed[:shift]
                orbit.append(rotated)
                orbit.append((rotated[0],) + tuple(reversed(rotated[1:])))
        representatives.add(min(orbit))
    return tuple(sorted(representatives))


def component_parities(word, partition, component):
    result = []
    order = len(word)
    for colour in range(4):
        parity = 0
        for edge in range(order):
            crosses = ((partition[edge] == component)
                       != (partition[(edge + 1) % order] == component))
            parity ^= int(crosses and word[edge] == colour)
        result.append(parity)
    return tuple(result)


def valid_dirty_partitions(word):
    order = len(word)
    result = []
    for partition in set_partitions(order):
        count = max(partition) + 1
        if count < 2:
            continue
        states = tuple(
            component_parities(word, partition, component)
            for component in range(count)
        )
        if any(len(set(state)) != 1 for state in states):
            continue
        if any(state[0] for state in states):
            result.append((partition, states))
    return result


def blocks(partition):
    return tuple(
        tuple(index for index, value in enumerate(partition)
              if value == component)
        for component in range(max(partition) + 1)
    )


def check_repairs():
    rows = (
        ((3, 1, 2, 2, 2), (2, 3, 1, 3, 1)),
        ((3, 3, 1, 2, 3), (1, 2, 3, 1, 2)),
    )
    for boundary, circuit in rows:
        assert all(value in (1, 2, 3) for value in boundary + circuit)
        for index, value in enumerate(boundary):
            assert circuit[index - 1] ^ circuit[index] == value

    # Every permutation of {1,2,3} preserving xor is a GL(2,2) map.
    maps = [
        (0,) + permutation
        for permutation in permutations((1, 2, 3))
        if permutation[2] == (permutation[0] ^ permutation[1])
    ]
    assert len(maps) == 6
    assert any(mapping[1] == 2 for mapping in maps)
    assert any(mapping[1] == 3 for mapping in maps)


def main():
    words4 = canonical_words(4)
    words5 = canonical_words(5)
    assert words4 == ((0, 1, 2, 3),)
    assert words5 == ((0, 1, 0, 2, 3),)

    dirty4 = valid_dirty_partitions(words4[0])
    dirty5 = valid_dirty_partitions(words5[0])

    blocks4 = {blocks(partition) for partition, _ in dirty4}
    blocks5 = {blocks(partition) for partition, _ in dirty5}

    assert blocks4 == {((0, 2), (1, 3))}
    assert blocks5 == {
        ((0, 1, 3), (2, 4)),
        ((0, 2, 3), (1, 4)),
    }
    assert all(
        all(state == (1, 1, 1, 1) for state in states)
        for _, states in dirty4 + dirty5
    )

    check_repairs()
    print("PASS: size-at-most-five boundary classification and repairs")
    print(f"canonical_words_4={words4}")
    print(f"canonical_words_5={words5}")
    print(f"dirty_partitions_4={sorted(blocks4)}")
    print(f"dirty_partitions_5={sorted(blocks5)}")


if __name__ == "__main__":
    main()
