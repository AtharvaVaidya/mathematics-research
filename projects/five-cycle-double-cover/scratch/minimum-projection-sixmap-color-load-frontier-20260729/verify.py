#!/usr/bin/env python3
"""Audit the finite colour-count form of the six-map load inequality."""

from itertools import permutations, product

BOUND = 4
maps = [(0,) + perm for perm in permutations((1, 2, 3))]

# The three nonzero functionals are represented by their unique nonzero
# kernel element a.  alpha_a(x)=0 exactly for x in {0,a}.
profiles = 0
state_checks = 0
for N in product(range(BOUND + 1), repeat=3):
    for O in product(range(BOUND + 1), repeat=3):
        profiles += 1
        total = sum(N) + sum(O)

        # Twice every functional half-load, avoiding fractions.
        all_post_loads = []
        for perm in maps:
            for kernel in (1, 2, 3):
                outside_ones = sum(
                    O[colour - 1]
                    for colour in (1, 2, 3)
                    if colour != kernel
                )
                inside_ones = sum(
                    N[colour - 1]
                    for colour in (1, 2, 3)
                    if perm[colour] != kernel
                )
                all_post_loads.append(2 * (outside_ones + inside_ones))
                state_checks += 1

        # A formal support size h may be any integer from 0 to 2m.
        # Check that all 18 post-map/function inequalities are equivalent
        # to the nine pair inequalities O_a+N_b <= m-h/2.
        for h in range(2 * total + 1):
            lhs = all(value >= h for value in all_post_loads)
            rhs = all(
                2 * (O[a] + N[b]) <= 2 * total - h
                for a in range(3)
                for b in range(3)
            )
            assert lhs == rhs

print(
    "PASS:",
    f"bound={BOUND}",
    f"profiles={profiles}",
    f"postmap_function_checks={state_checks}",
)
