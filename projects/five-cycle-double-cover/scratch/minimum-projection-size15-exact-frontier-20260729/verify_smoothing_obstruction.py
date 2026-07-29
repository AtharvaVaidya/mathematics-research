#!/usr/bin/env python3
"""Replay a literal obstruction to lifting cleanability through smoothing."""

from targeted_extensions import classify, encode_word


def canonical_partition(values):
    names = {}
    result = []
    for value in values:
        if value not in names:
            names[value] = len(names)
        result.append(names[value])
    return tuple(result)


def smooth(word, partition, lengths, circuit_index, local_index):
    offset = sum(lengths[:circuit_index])
    length = lengths[circuit_index]
    removed = offset + local_index
    successor = offset + (local_index + 1) % length
    first = partition[removed]
    second = partition[successor]
    new_word = word[:removed] + word[removed + 1 :]
    new_partition = list(partition)
    new_partition.pop(removed)
    if first != second:
        new_partition = [
            first if value == second else value for value in new_partition
        ]
    new_lengths = (
        lengths[:circuit_index]
        + (length - 1,)
        + lengths[circuit_index + 1 :]
    )
    return (
        new_word,
        canonical_partition(new_partition),
        new_lengths,
        (first, second),
    )


def main():
    pieces = ("01010123", "0101232")
    word = tuple(map(int, "".join(pieces)))
    partition = tuple(map(int, "001234404130002"))
    lengths = tuple(map(len, pieces))
    original = classify(word, partition, lengths)
    assert original[:3] == (320, 0, 0)

    smoothed = smooth(word, partition, lengths, 1, 0)
    short_word, short_partition, short_lengths, merged = smoothed
    short = classify(short_word, short_partition, short_lengths)
    assert merged == (4, 1)
    assert encode_word(short_word, short_lengths) == "01010123|101232"
    assert "".join(map(str, short_partition)) == "00123110130002"
    assert short[:3] == (56, 16, 0)

    print(
        "ORIGINAL"
        " word=01010123|0101232"
        " partition=001234404130002"
        f" feasible={original[0]} clean={original[1]} delete={original[2]}"
    )
    print(
        "SMOOTHED"
        f" word={encode_word(short_word, short_lengths)}"
        f" partition={''.join(map(str, short_partition))}"
        f" merged_blocks={merged[0]},{merged[1]}"
        f" feasible={short[0]} clean={short[1]} delete={short[2]}"
    )
    print("PASS")


if __name__ == "__main__":
    main()
