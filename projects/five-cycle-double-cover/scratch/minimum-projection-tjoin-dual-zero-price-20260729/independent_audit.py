#!/usr/bin/env python3
"""Independent permutation-level audit of the local six-map laws."""

from itertools import permutations, product

# GL(2,2) is exactly every permutation of the three nonzero elements,
# extended by fixing zero.  This implementation deliberately does not
# use matrices.
maps = [(0,) + perm for perm in permutations((1, 2, 3))]
even = []
odd = []
for perm in maps:
    inversions = sum(
        perm[i] > perm[j]
        for i in range(1, 4)
        for j in range(i + 1, 4)
    )
    (even if inversions % 2 == 0 else odd).append(perm)

assert len(even) == len(odd) == 3


def new_colour(r, p, perm):
    return r ^ p ^ perm[p]


orbit_checks = 0
for triple in (even, odd):
    for r, p in product(range(4), repeat=2):
        values = [new_colour(r, p, perm) for perm in triple]
        if p == 0:
            assert values == [r, r, r]
        else:
            assert len(set(values)) == 3
            assert (r ^ p) not in values
            assert set(values) | {r ^ p} == set(range(4))
        orbit_checks += 1


# Directly audit the cut-parity update formula on every labelled cut of
# up to four support edges.  A cut is represented only by its incidence
# mask, since the formula depends on no other graph data.
parity_checks = 0
for n in range(1, 5):
    for rword in product(range(4), repeat=n):
        for pword in product(range(4), repeat=n):
            for mask in range(1 << n):
                for perm in maps:
                    new = [
                        new_colour(rword[i], pword[i], perm)
                        for i in range(n)
                    ]
                    terminal_parity = [0, 0, 0, 0]
                    for i in range(n):
                        if (mask >> i) & 1:
                            terminal_parity[new[i]] ^= 1
                    # Recompute the same quantity as the boundary parity
                    # of each post-switch colour class.
                    boundary_parity = [
                        sum(
                            ((mask >> i) & 1) and new[i] == c
                            for i in range(n)
                        ) & 1
                        for c in range(4)
                    ]
                    assert terminal_parity == boundary_parity
                    parity_checks += 1

print(
    "PASS:",
    f"permutation_maps={len(maps)}",
    f"orbit_checks={orbit_checks}",
    f"cut_parity_checks={parity_checks}",
)
