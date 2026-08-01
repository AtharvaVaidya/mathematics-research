#!/usr/bin/env python3
"""Exhaustive checker for the six H=0 repeated-circuit label tracks."""

from itertools import combinations


def active(label: int, left: int, right: int) -> bool:
    return bool(((label >> left) & 1) ^ ((label >> right) & 1))


def transpose(label: int, left: int, right: int) -> int:
    if not active(label, left, right):
        return label
    return label ^ (1 << left) ^ (1 << right)


def text(label: int) -> str:
    return "".join(str(i) for i in range(5) if (label >> i) & 1)


def main() -> None:
    labels = [
        sum(1 << coordinate for coordinate in pair)
        for pair in combinations(range(5), 2)
    ]
    tracks: dict[int, list[tuple[str, str, str]]] = {0: [], 1: []}

    # Normalization a=0,b=1,h=2.  K1 uses 12, K2 uses 01, K3 uses 02.
    for in_middle in (0, 1):
        for initial in labels:
            if not active(initial, 1, 2):
                continue
            after_first = transpose(initial, 1, 2)
            if in_middle:
                if not active(after_first, 0, 1):
                    continue
                after_second = transpose(after_first, 0, 1)
            else:
                after_second = after_first
            if not active(after_second, 0, 2):
                continue
            tracks[in_middle].append(
                (text(initial), text(after_first), text(after_second))
            )

    assert tracks == {
        0: [("02", "01", "01"), ("13", "23", "23"), ("14", "24", "24")],
        1: [("01", "02", "12"), ("23", "13", "03"), ("24", "14", "04")],
    }

    # If K=K2, an endpoint of the root edge 01 would need a distinct
    # incident K-edge from {01,23,24} sharing a coordinate with 01.
    # There is no such label.
    middle_initials = {track[0] for track in tracks[1]}
    companions = {
        label
        for label in middle_initials - {"01"}
        if set(label) & set("01")
    }
    assert not companions

    print("PASS: six local tracks; H=0 forces nonempty hidden support Z")


if __name__ == "__main__":
    main()
