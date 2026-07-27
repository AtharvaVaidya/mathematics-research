#!/usr/bin/env python3
"""Exhaust the 2^10 D5 label supports behind Lemma 2.2."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


D5 = tuple(value for value in range(32) if value.bit_count() == 2)
EVEN = tuple(value for value in range(32) if value.bit_count() % 2 == 0)


def edge(mask: int) -> tuple[int, int]:
    vertices = tuple(index for index in range(5) if mask >> index & 1)
    assert len(vertices) == 2
    return vertices


def connected(support: int) -> bool:
    members = [index for index in range(10) if support >> index & 1]
    if not members:
        return False
    reached = {members[0]}
    stack = [members[0]]
    while stack:
        first = stack.pop()
        for second in members:
            if second not in reached and D5[first] & D5[second]:
                reached.add(second)
                stack.append(second)
    return len(reached) == len(members)


def is_blocker(support: int) -> bool:
    for shift in EVEN:
        if shift and all(
            D5[index] ^ shift in D5
            for index in range(10)
            if support >> index & 1
        ):
            return False
    return True


def degrees(support: int) -> tuple[int, ...]:
    result = [0] * 5
    for index, label in enumerate(D5):
        if support >> index & 1:
            left, right = edge(label)
            result[left] += 1
            result[right] += 1
    return tuple(result)


def bipartite(support: int) -> bool:
    adjacency = [[] for _ in range(5)]
    for index, label in enumerate(D5):
        if support >> index & 1:
            left, right = edge(label)
            adjacency[left].append(right)
            adjacency[right].append(left)
    colour: list[int | None] = [None] * 5
    for start in range(5):
        if colour[start] is not None:
            continue
        colour[start] = 0
        stack = [start]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if colour[other] is None:
                    colour[other] = 1 - colour[vertex]
                    stack.append(other)
                elif colour[other] == colour[vertex]:
                    return False
    return True


def characterized(support: int) -> bool:
    profile = degrees(support)
    if 0 in profile:
        return False
    if not bipartite(support):
        return True
    return sorted(profile) == [1, 1, 1, 1, 4]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    connected_supports = [
        support for support in range(1, 1 << 10) if connected(support)
    ]
    blockers = [support for support in connected_supports if is_blocker(support)]
    mismatches = [
        support
        for support in connected_supports
        if is_blocker(support) != characterized(support)
    ]
    minimal = [
        support
        for support in blockers
        if not any(
            is_blocker(support ^ (1 << index))
            for index in range(10)
            if support >> index & 1
        )
    ]

    degree_profiles = Counter(
        tuple(sorted(degrees(support), reverse=True)) for support in minimal
    )
    result = {
        "schema": "five-cdc-rooted-cycle-translation-blockers-v1",
        "label_universe": len(D5),
        "even_shift_universe": len(EVEN),
        "nonempty_supports": (1 << 10) - 1,
        "connected_supports": len(connected_supports),
        "connected_blockers": len(blockers),
        "characterization_mismatches": len(mismatches),
        "inclusion_minimal_connected_blockers": len(minimal),
        "minimal_blocker_degree_profiles": {
            ",".join(map(str, profile)): count
            for profile, count in sorted(degree_profiles.items())
        },
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
