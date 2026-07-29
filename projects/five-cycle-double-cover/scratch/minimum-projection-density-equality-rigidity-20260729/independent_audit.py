#!/usr/bin/env python3
"""Independent audit of the slack identity and witness balance."""

from itertools import product

slack_checks = 0
for j, m, extra, unused in product(range(13), repeat=4):
    # One-colour identity:
    # dual cut incidence is both 2j+extra and j+m-unused.
    if 2 * j + extra != j + m - unused:
        continue
    assert m - j == extra + unused
    slack_checks += 1

balance_checks = 0
for total in range(0, 61, 3):
    target = total // 3
    for selected in product(range(target + 1), repeat=3):
        outside = tuple(target - value for value in selected)
        inequality = max(selected) + max(outside) <= target
        exact_balance = selected[0] == selected[1] == selected[2]
        assert inequality == exact_balance
        balance_checks += 1

# Equality topology profiles through h=240.
topology_rows = []
for h in range(12, 241, 12):
    m = 3 * h // 4
    n = h // 6
    q = 5 * h // 12
    assert m == (3 * (h + n)) // 2 - h
    assert n == h - 2 * q
    topology_rows.append((h, m, n, q))

print(
    "PASS:",
    f"slack_checks={slack_checks}",
    f"balance_checks={balance_checks}",
    f"topology_rows={len(topology_rows)}",
)
