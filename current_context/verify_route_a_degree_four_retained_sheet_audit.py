#!/usr/bin/env python3
"""Exact finite checks for the Route A degree-four retained-sheet audit."""

from itertools import permutations


def compose(p, q):
    """Return p after q, with permutations represented by image tuples."""
    return tuple(p[q[i]] for i in range(4))


def inverse(p):
    out = [0] * 4
    for i, value in enumerate(p):
        out[value] = i
    return tuple(out)


def cycle_lengths(p):
    seen = set()
    lengths = []
    for i in range(4):
        if i in seen:
            continue
        j = i
        length = 0
        while j not in seen:
            seen.add(j)
            length += 1
            j = p[j]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def generated_group(generators):
    identity = tuple(range(4))
    group = {identity}
    frontier = [identity]
    generators = list(generators) + [inverse(g) for g in generators]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            nxt = compose(current, generator)
            if nxt not in group:
                group.add(nxt)
                frontier.append(nxt)
    return group


def orbit_sizes(group):
    unused = set(range(4))
    sizes = []
    while unused:
        seed = next(iter(unused))
        orbit = {g[seed] for g in group}
        unused -= orbit
        sizes.append(len(orbit))
    return tuple(sorted(sizes, reverse=True))


all_permutations = list(permutations(range(4)))
ramified_with_fixed_sheet = {
    cycle_lengths(p)
    for p in all_permutations
    if cycle_lengths(p) != (1, 1, 1, 1)
    and 1 in cycle_lengths(p)
}
assert ramified_with_fixed_sheet == {(2, 1, 1), (3, 1)}

cases = []
for c in range(1, 5):
    for triple_components in range(c + 1):
        for deficit in range(5):
            boundary_components = 3 - c - triple_components - deficit
            if boundary_components >= c:
                cases.append(
                    (c, triple_components, deficit, boundary_components)
                )
assert cases == [
    (1, 0, 0, 2),
    (1, 0, 1, 1),
    (1, 1, 0, 1),
]

a = (1, 0, 2, 3)  # (12)
b = (0, 2, 1, 3)  # (23)
c = (0, 1, 3, 2)  # (34)
identity = tuple(range(4))

assert compose(compose(a, b), a) == compose(compose(b, a), b)
assert compose(a, c) == compose(c, a)
assert orbit_sizes(generated_group([a, b])) == (3, 1)
assert orbit_sizes(generated_group([a, c])) == (2, 2)
assert len(generated_group([a, b, c])) == 24
assert orbit_sizes(generated_group([a, b, c])) == (4,)

# Expand the weighted-homogeneous factorization in equation (27).
# Put q=z^3 and compare coefficients in x and q.
left = {
    (4, 0): 27,
    (3, 1): 256,
    (2, 2): 768,
    (1, 3): 768,
    (0, 4): 256,
}
factor_one = {(2, 0): 1, (1, 1): 8, (0, 2): 16}
factor_two = {(2, 0): 27, (1, 1): 40, (0, 2): 16}
product = {}
for (x1, q1), coefficient_one in factor_one.items():
    for (x2, q2), coefficient_two in factor_two.items():
        key = (x1 + x2, q1 + q2)
        product[key] = (
            product.get(key, 0) + coefficient_one * coefficient_two
        )
assert product == left

# The residual quadratic 27 a^2 + 40 a + 16 has discriminant -128.
assert 40**2 - 4 * 27 * 16 == -128

print("route A degree-four retained-sheet audit: exact checks passed")
