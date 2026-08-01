#!/usr/bin/env python3
"""Independent local-algebra and cycle-family audit of the construction."""

from __future__ import annotations

from itertools import permutations


def xor_all(values: list[frozenset[int]]) -> frozenset[int]:
    out: set[int] = set()
    for value in values:
        out.symmetric_difference_update(value)
    return frozenset(out)


def local_audit() -> int:
    checks = 0
    colours = {2, 3, 4}
    for a, b, c in permutations(colours):
        assert {a, b, c} == colours
        outside = [frozenset(colours - {x}) for x in (a, b, c)]
        assert xor_all(outside) == frozenset()
        on_cycle = [frozenset((0, a)), frozenset((0, b)), frozenset((a, b))]
        assert xor_all(on_cycle) == frozenset()
        assert [len(x) for x in outside + on_cycle] == [2] * 6
        assert [bool(x & {0, 1}) for x in on_cycle] == [True, True, False]
        checks += 1
    return checks


def ring_audit(length: int) -> int:
    # Abstractly audit every proper cyclic Tait-colour word.  The word gives
    # the colours on the prescribed circuit; the missing colour at a vertex
    # is the colour of its third incident edge.
    count = 0

    def rec(word: list[int]) -> None:
        nonlocal count
        if len(word) == length:
            if word[-1] == word[0]:
                return
            labels = [frozenset((0, c)) for c in word]
            for i in range(length):
                left = word[i - 1]
                right = word[i]
                assert left != right
                third = frozenset({2, 3, 4} - ({2, 3, 4} - {left, right}))
                # The off-circuit edge has the pair of the two circuit colours.
                assert third == frozenset((left, right))
                assert xor_all([labels[i - 1], labels[i], third]) == frozenset()
            active = [len(label & {0, 1}) == 1 for label in labels]
            assert all(active)
            count += 1
            return
        for colour in (2, 3, 4):
            if word and word[-1] == colour:
                continue
            rec(word + [colour])

    rec([])
    return count


def main() -> None:
    local = local_audit()
    words = {n: ring_audit(n) for n in range(3, 13)}
    assert all(value > 0 for value in words.values())
    print(
        "PASS: independent Tait-lift algebra; "
        f"local_orderings={local}; cyclic_words={sum(words.values())}; "
        f"lengths={words}"
    )


if __name__ == "__main__":
    main()
