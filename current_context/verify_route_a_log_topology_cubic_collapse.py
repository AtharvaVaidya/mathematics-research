#!/usr/bin/env python3
"""Exact checks for ROUTE_A_LOG_TOPOLOGY_CUBIC_COLLAPSE.md."""

from itertools import product


def affine_curve_hc1(genus: int, punctures: int, branch_excess: int) -> int:
    """The right side of the normalization formula (17)."""
    assert genus >= 0
    assert punctures >= 1
    assert branch_excess >= 0
    return 2 * genus + punctures - 1 + branch_excess


# χ(S)=1 and b_1(S;Q)=0 on a real two-dimensional affine CW model force b_2=0.
chi_s = 1
b0_s = 1
b1_s = 0
b2_s = b1_s + chi_s - b0_s
assert b2_s == 0


# Vanishing H_c^1 permits only genus zero, one puncture, and no branch excess.
zero_hc1_cases = []
for genus, punctures, branch_excess in product(range(4), range(1, 5), range(5)):
    if affine_curve_hc1(genus, punctures, branch_excess) == 0:
        zero_hc1_cases.append((genus, punctures, branch_excess))
assert zero_hc1_cases == [(0, 1, 0)]


# Two distinct non-étale support points in a flat cubic fiber are impossible.
rank = 3
minimum_non_etale_local_length = 2
assert 2 * minimum_non_etale_local_length > rank


# Solve r+c+N_tr=2 subject to one ramified boundary per branch component.
solutions = []
for r, c, n_transitive in product(range(1, 8), range(1, 8), range(8)):
    if r >= c and r + c + n_transitive == 2:
        solutions.append((r, c, n_transitive))
assert solutions == [(1, 1, 0)]


# The unique solution has no room for an additional boundary component,
# a second branch component, or a transitive/non-Gorenstein affine fiber.
r, c, n_transitive = solutions[0]
assert r == c == 1
assert n_transitive == 0
assert r - c == 0

print("Route A log-topology cubic collapse: exact checks passed")
