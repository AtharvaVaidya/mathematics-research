#!/usr/bin/env python3
"""Exhaust the finite D5 claims used in the human reduction proof."""

from itertools import combinations, permutations, product


D5 = tuple(
    sum(1 << i for i in pair)
    for pair in combinations(range(5), 2)
)
D5_SET = set(D5)


def weight(x: int) -> int:
    return x.bit_count()


def fmt(x: int) -> str:
    return "".join(str(i) for i in range(5) if (x >> i) & 1)


# Lemma 5.1: every xor-zero cubic triple is a triangle, and every ordering
# of every triangle occurs.
cubic_triples = []
for triple in product(D5, repeat=3):
    if triple[0] ^ triple[1] ^ triple[2]:
        continue
    assert len(set(triple)) == 3
    support = triple[0] | triple[1] | triple[2]
    assert weight(support) == 3
    expected = {
        sum(1 << i for i in pair)
        for pair in combinations(
            [i for i in range(5) if (support >> i) & 1], 2
        )
    }
    assert set(triple) == expected
    cubic_triples.append(triple)
assert len(cubic_triples) == 10 * 6

# Check ordered-triple transitivity under S5.
base = cubic_triples[0]
orbit = set()
for perm in permutations(range(5)):
    mapped = []
    for label in base:
        out = 0
        for i in range(5):
            if (label >> i) & 1:
                out |= 1 << perm[i]
        mapped.append(out)
    orbit.add(tuple(mapped))
assert orbit == set(cubic_triples)

# Lemma 5.2.
parallel_witnesses = {}
for a in D5:
    witnesses = [
        (b, c) for b in D5 for c in D5 if a ^ b ^ c == 0
    ]
    assert witnesses
    parallel_witnesses[a] = witnesses

# Lemma 5.3.
square_witnesses = {}
for a in D5:
    for b in D5:
        witnesses = [
            t for t in D5 if (t ^ a) in D5_SET and (t ^ b) in D5_SET
        ]
        assert witnesses
        for t in witnesses:
            internal = (t ^ a, t, t ^ b, t)
            assert all(label in D5_SET for label in internal)
            boundary = tuple(
                internal[(i - 1) % 4] ^ internal[i] for i in range(4)
            )
            assert boundary == (a, a, b, b)
        square_witnesses[(a, b)] = witnesses

# Section 4: the cyclic word 01,02,01,02 has xor zero but no D5-valued
# internal cyclic solution.
a01 = (1 << 0) | (1 << 1)
a02 = (1 << 0) | (1 << 2)
bad_word = (a01, a02, a01, a02)
assert bad_word[0] ^ bad_word[1] ^ bad_word[2] ^ bad_word[3] == 0


def extends_cyclic_word(word: tuple[int, ...]) -> bool:
    # Choose the label before boundary position zero and propagate equation
    # Y_{j-1} xor Y_j = A_j.
    for initial in D5:
        previous = initial
        labels = []
        for boundary in word:
            current = previous ^ boundary
            labels.append(current)
            previous = current
        if previous == initial and all(x in D5_SET for x in labels):
            return True
    return False


assert not extends_cyclic_word(bad_word)

print("PASS")
print(f"D5 labels: {len(D5)}")
print(f"ordered xor-zero cubic triples: {len(cubic_triples)}")
print(f"parallel-pair inputs checked: {len(parallel_witnesses)}")
print(f"ordered square-boundary pairs checked: {len(square_witnesses)}")
print(
    "nonextendable xor-zero cyclic word:",
    ",".join(fmt(x) for x in bad_word),
)
