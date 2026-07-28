#!/usr/bin/env python3
"""Independent replay of the abstract D5 one-ear countermodel.

This checker imports no project module and does not use the primary ear
audit.  It reconstructs U_4 and U_5, the color action, the relation R, the
one-internal-vertex ear image, all pair projections, all C5-cap hits, and
the elementary bichromatic-switch condition.

R is an abstract boundary relation, not a graph-realizable five-pole.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, permutations, product
import json


LABELS = tuple(
    (1 << left) | (1 << right)
    for left, right in combinations(range(5), 2)
)
LABEL_SET = set(LABELS)
COLOR_ACTIONS = tuple(permutations(range(5)))
SELECTED_FOUR_ORBITS = {
    (0x03, 0x03, 0x03, 0x03),
    (0x03, 0x05, 0x03, 0x05),
    (0x03, 0x05, 0x05, 0x03),
    (0x03, 0x05, 0x0A, 0x0C),
    (0x03, 0x05, 0x0C, 0x0A),
}


@lru_cache(maxsize=None)
def relabel(value: int, action: tuple[int, ...]) -> int:
    output = 0
    for color in range(5):
        if value & (1 << color):
            output |= 1 << action[color]
    return output


@lru_cache(maxsize=None)
def representative(word: tuple[int, ...]) -> tuple[int, ...]:
    answer = None
    for action in COLOR_ACTIONS:
        candidate = tuple(relabel(value, action) for value in word)
        if answer is None or candidate < answer:
            answer = candidate
    assert answer is not None
    return answer


def universe(length: int) -> tuple[tuple[int, ...], ...]:
    words = []
    for prefix in product(LABELS, repeat=length - 1):
        final = 0
        for value in prefix:
            final ^= value
        if final in LABEL_SET:
            words.append((*prefix, final))
    return tuple(words)


def ear_image(word: tuple[int, ...]) -> tuple[int, ...] | None:
    new_value = word[0] ^ word[1]
    if new_value not in LABEL_SET:
        return None
    return (*word[2:], new_value)


def cap_extends(boundary: tuple[int, ...]) -> bool:
    for initial in LABELS:
        current = initial
        valid = True
        for value in boundary:
            current ^= value
            if current not in LABEL_SET:
                valid = False
                break
        if valid:
            assert current == initial
            return True
    return False


def cap_sets(
    five_words: tuple[tuple[int, ...], ...]
) -> tuple[set[tuple[int, ...]], ...]:
    orders = tuple(
        (0, *tail)
        for tail in permutations((1, 2, 3, 4))
        if tail[0] < tail[-1]
    )
    answer = []
    for order in orders:
        answer.append({
            representative(word)
            for word in five_words
            if cap_extends(tuple(word[position] for position in order))
        })
    assert len(answer) == 12
    assert {len(row) for row in answer} == {46}
    return tuple(answer)


def switch(
    word: tuple[int, ...], positions: tuple[int, ...], pair: int
) -> tuple[int, ...]:
    output = list(word)
    for position in positions:
        output[position] ^= pair
    answer = tuple(output)
    assert all(value in LABEL_SET for value in answer)
    return answer


def elementary_switch_check(
    state_orbits: set[tuple[int, ...]]
) -> bool:
    expanded = {
        tuple(relabel(value, action) for value in state)
        for state in state_orbits
        for action in COLOR_ACTIONS
    }
    for word in expanded:
        for color_left, color_right in combinations(range(5), 2):
            color_pair = (1 << color_left) | (1 << color_right)
            ends = tuple(
                position for position, value in enumerate(word)
                if bool(value & (1 << color_left))
                != bool(value & (1 << color_right))
            )
            if len(ends) == 0:
                continue
            if len(ends) == 2:
                if representative(
                    switch(word, ends, color_pair)
                ) not in state_orbits:
                    return False
                continue
            assert len(ends) == 4
            if representative(
                switch(word, ends, color_pair)
            ) not in state_orbits:
                return False
            a, b, c, d = ends
            endpoint_pairings = (
                ((a, b), (c, d)),
                ((a, c), (b, d)),
                ((a, d), (b, c)),
            )
            if not any(
                all(
                    representative(
                        switch(word, endpoint_pair, color_pair)
                    ) in state_orbits
                    for endpoint_pair in pairing
                )
                for pairing in endpoint_pairings
            ):
                return False
    return True


def main() -> int:
    four_words = universe(4)
    five_words = universe(5)
    assert len(four_words) == 640
    assert len(five_words) == 6_240
    assert len({representative(word) for word in four_words}) == 10
    assert len({representative(word) for word in five_words}) == 62

    relation = set()
    for word in five_words:
        image = ear_image(word)
        if image is None:
            relation.add(word)
        elif representative(image) in SELECTED_FOUR_ORBITS:
            relation.add(word)
    relation_orbits = {representative(word) for word in relation}
    image = {
        output for word in relation
        if (output := ear_image(word)) is not None
    }
    image_orbits = {representative(word) for word in image}

    assert len(relation) == 4_620
    assert len(relation_orbits) == 46
    assert len(image) == 370
    assert image_orbits == SELECTED_FOUR_ORBITS
    assert elementary_switch_check(relation_orbits)
    assert elementary_switch_check(image_orbits)

    projection_sizes = {
        f"{left},{right}": len({
            (word[left], word[right]) for word in relation
        })
        for left, right in combinations(range(5), 2)
    }
    assert set(projection_sizes.values()) == {100}
    hits = tuple(
        len(relation_orbits & cap) for cap in cap_sets(five_words)
    )
    assert hits == (33, 37, 33, 37, 33, 33, 35, 35, 32, 35, 35, 32)

    print(json.dumps({
        "schema": "independent-d5-one-ear-countermodel-audit-v1",
        "classification": (
            "INDEPENDENT ABSTRACT-RELATION REPLAY; "
            "GRAPH REALIZABILITY NOT CLAIMED"
        ),
        "input": {
            "ordered_words": len(relation),
            "color_orbits": len(relation_orbits),
            "pair_projection_sizes": projection_sizes,
            "cap_intersection_sizes": hits,
            "elementary_switching_closed": True,
        },
        "one_internal_vertex_ear_image": {
            "ordered_words": len(image),
            "color_orbits": len(image_orbits),
            "elementary_switching_closed": True,
        },
        "warning": (
            "This refutes only coarse ear invariants. It is not a graph "
            "pole, a FiveCDC counterexample, or an orientable claim."
        ),
        "status": "PASS",
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
