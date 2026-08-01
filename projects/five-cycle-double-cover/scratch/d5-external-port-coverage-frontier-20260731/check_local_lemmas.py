#!/usr/bin/env python3
"""Standard-library audit of the finite tables in HUMAN-PROOF.md."""

from itertools import combinations


LABELS = tuple((1 << a) | (1 << b) for a, b in combinations(range(5), 2))
WEIGHT_TWO = frozenset(LABELS)


def crosses(first: int, second: int) -> bool:
    return (first & second).bit_count() == 1


def adjacent_port_table() -> None:
    a, b, c = 0b00011, 0b00101, 0b00110  # 01,02,12
    assert a ^ b ^ c == 0
    root_labels = [label for label in LABELS if label != a and crosses(label, a)]
    external = (0b01001, 0b10001, 0b01010, 0b10010)  # 03,04,13,14
    assert root_labels == [5, 9, 17, 6, 10, 18]
    for root in root_labels:
        choices = [pair for pair in external if crosses(pair, a) and crosses(pair, root)]
        assert choices
        for pair in choices:
            active = [label for label in (a, b, c) if crosses(pair, label)]
            assert len(active) == 2 and a in active
            inactive = next(label for label in (a, b, c) if label not in active)
            assert pair & inactive == 0
    print("ADJACENT_PORT root_labels=6 external_candidates=4 PASS")


def circuit_word_table() -> None:
    states = tuple((u, v, (1 << u) | (1 << v))
                   for u in (1, 2) for v in (0, 3, 4))
    legal_steps = 0
    for u, v, label in states:
        assert crosses(label, 0b00110)  # P=12
        assert crosses(label, 0b01001) == (v in (0, 3))
        assert crosses(label, 0b10001) == (v in (0, 4))
        for u2, v2, label2 in states:
            if label == label2 or (label ^ label2) not in WEIGHT_TWO:
                continue
            legal_steps += 1
            assert (u != u2) ^ (v != v2)
    assert legal_steps == 18
    print("CIRCUIT_WORD states=6 directed_legal_steps=18 PASS")


def cube_inverse_insertion_no_go() -> None:
    top = ((0, 1), (1, 2), (2, 3), (0, 3))
    bottom = ((4, 5), (5, 6), (6, 7), (4, 7))
    vertical = ((0, 4), (1, 5), (2, 6), (3, 7))
    edges = top + bottom + vertical
    labels = (5, 6, 5, 6, 5, 6, 5, 6, 3, 3, 3, 3)
    incident = [[] for _ in range(8)]
    for edge, (left, right) in enumerate(edges):
        incident[left].append(edge)
        incident[right].append(edge)
    assert all(len(row) == 3 for row in incident)
    assert all(labels[row[0]] ^ labels[row[1]] ^ labels[row[2]] == 0
               for row in incident)
    active = {edge for edge, label in enumerate(labels) if crosses(label, 3)}
    assert active == set(range(8))
    # The two endpoints of inserted edge 8=(0,4) are on different Y_01
    # components: the top and bottom horizontal squares.
    assert set(incident[0]) & active == {0, 3}
    assert set(incident[4]) & active == {4, 7}
    assert not any({edge, other} <= active and
                   set(edges[edge]) & set(edges[other])
                   for edge in range(4) for other in range(4, 8))
    print("CUBE_INVERSE_INSERTION y01_components=2 endpoints_separate PASS")


if __name__ == "__main__":
    adjacent_port_table()
    circuit_word_table()
    cube_inverse_insertion_no_go()
    print("PASS")
