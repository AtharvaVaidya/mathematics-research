#!/usr/bin/env python3
"""Primary finite audit of the six-map T-join recomputation identities."""

from itertools import product

K = range(4)


def bits(x):
    return ((x >> 1) & 1, x & 1)


def from_bits(a, b):
    return (a << 1) | b


def apply(matrix, x):
    a, b = bits(x)
    return from_bits(
        (matrix[0][0] * a + matrix[0][1] * b) & 1,
        (matrix[1][0] * a + matrix[1][1] * b) & 1,
    )


GL = []
for entries in product(range(2), repeat=4):
    matrix = ((entries[0], entries[1]), (entries[2], entries[3]))
    images = tuple(apply(matrix, x) for x in K)
    if set(images) == set(K):
        GL.append((matrix, images))

assert len(GL) == 6
identity = next(item for item in GL if item[1] == (0, 1, 2, 3))
order3 = [item for item in GL if item[1] in ((0, 2, 3, 1), (0, 3, 1, 2))]
involutions = [
    item for item in GL
    if item != identity and item not in order3
]
cosets = [[identity] + order3, involutions]
assert [len(coset) for coset in cosets] == [3, 3]


def switched(r, p, item):
    up = item[1][p]
    return r ^ up ^ p


pointwise_rows = 0
for coset in cosets:
    for r, p in product(K, repeat=2):
        got = sorted(switched(r, p, item) for item in coset)
        want = sorted([r, r, r] if p == 0 else [x for x in K if x != (r ^ p)])
        assert got == want
        pointwise_rows += 1


# Exhaust the local transition at one circuit vertex.  This is sufficient
# because the cyclic integration law is the conjunction of these local
# transitions; closure is exactly the separately stated xor condition.
cyclic_rows = 0
for r_prev, r_now, p_prev, p_now, epsilon in product(K, K, K, K, range(2)):
    g = r_prev ^ r_now
    if (p_prev ^ p_now) != (epsilon * g):
        continue
    for item in GL:
        new_prev = switched(r_prev, p_prev, item)
        new_now = switched(r_now, p_now, item)
        got = new_prev ^ new_now
        want = item[1][g] if epsilon else g
        assert got == want
        cyclic_rows += 1


# Check the class-size law independently on all r/p words through length 4.
class_rows = 0
for n in range(1, 5):
    for rword in product(K, repeat=n):
        for pword in product(K, repeat=n):
            m = sum(p != 0 for p in pword)
            for coset in cosets:
                for c in K:
                    lhs = 0
                    for item in coset:
                        lhs += sum(
                            switched(rword[i], pword[i], item) == c
                            for i in range(n)
                        )
                    a = sum(pword[i] == 0 and rword[i] == c for i in range(n))
                    b = sum(
                        pword[i] != 0 and (rword[i] ^ pword[i]) == c
                        for i in range(n)
                    )
                    assert lhs == 3 * a + m - b
                    class_rows += 1

print(
    "PASS:",
    f"GL_maps={len(GL)}",
    f"pointwise_rows={pointwise_rows}",
    f"cyclic_derivative_checks={cyclic_rows}",
    f"class_size_rows={class_rows}",
)
