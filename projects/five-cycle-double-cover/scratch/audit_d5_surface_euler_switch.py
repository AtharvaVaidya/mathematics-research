#!/usr/bin/env python3
"""Exact cube witness that a D5 Kempe switch changes surface Euler data."""

from __future__ import annotations

import json


EDGES = (
    (0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 3),
    (2, 6), (3, 5), (4, 5), (4, 7), (5, 6), (6, 7),
)
INITIAL = (
    0x03, 0x05, 0x06, 0x05, 0x06, 0x03,
    0x06, 0x06, 0x03, 0x05, 0x05, 0x03,
)
PAIR = (1, 2)
SWITCH_COMPONENT = (0, 1, 3, 5)
ORIENTABILITY_INITIAL = (
    0x03, 0x05, 0x06, 0x09, 0x0A, 0x03,
    0x0A, 0x06, 0x0A, 0x0C, 0x0C, 0x06,
)
ORIENTABILITY_PAIR = (0, 1)
ORIENTABILITY_COMPONENT = (1, 2, 7, 8)


def incidence() -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(8)]
    for edge, (left, right) in enumerate(EDGES):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


INCIDENCE = incidence()


def component_masks(selected: int) -> tuple[int, ...]:
    unseen = {edge for edge in range(12) if (selected >> edge) & 1}
    answer = []
    while unseen:
        queue = [min(unseen)]
        component: set[int] = set()
        while queue:
            edge = queue.pop()
            if edge in component:
                continue
            component.add(edge)
            for vertex in EDGES[edge]:
                queue.extend(
                    other
                    for other in INCIDENCE[vertex]
                    if (selected >> other) & 1 and other not in component
                )
        unseen -= component
        answer.append(sum(1 << edge for edge in component))
    return tuple(sorted(answer))


def coordinate_component_counts(state: tuple[int, ...]) -> list[int]:
    answer = []
    for coordinate in range(5):
        selected = sum(
            1 << edge
            for edge, label in enumerate(state)
            if (label >> coordinate) & 1
        )
        answer.append(len(component_masks(selected)))
    return answer


def active_mask(
    state: tuple[int, ...], pair: tuple[int, int]
) -> int:
    first, second = pair
    return sum(
        1 << edge
        for edge, label in enumerate(state)
        if ((label >> first) & 1) ^ ((label >> second) & 1)
    )


def switched_state(
    state: tuple[int, ...],
    pair: tuple[int, int],
    component_edges: tuple[int, ...],
) -> tuple[int, ...]:
    first, second = pair
    component = sum(1 << edge for edge in component_edges)
    answer = []
    for edge, label in enumerate(state):
        if (component >> edge) & 1:
            assert ((label >> first) & 1) ^ ((label >> second) & 1)
            label ^= (1 << first) | (1 << second)
        answer.append(label)
    return tuple(answer)


def is_orientable(state: tuple[int, ...]) -> bool:
    triangle_colours = []
    for row in INCIDENCE:
        union = 0
        for edge in row:
            union |= state[edge]
        colours = tuple(
            coordinate
            for coordinate in range(5)
            if (union >> coordinate) & 1
        )
        assert len(colours) == 3
        triangle_colours.append(colours)

    def side_direction(
        colours: tuple[int, int, int], label: int
    ) -> int:
        cyclic_edges = (
            (colours[0], colours[1]),
            (colours[1], colours[2]),
            (colours[2], colours[0]),
        )
        left, right = sorted(
            coordinate
            for coordinate in range(5)
            if (label >> coordinate) & 1
        )
        return 1 if (left, right) in cyclic_edges else -1

    orientations = {0: 1}
    queue = [0]
    while queue:
        vertex = queue.pop()
        for edge in INCIDENCE[vertex]:
            left, right = EDGES[edge]
            other = right if left == vertex else left
            required = (
                -side_direction(
                    triangle_colours[vertex], state[edge]
                )
                * side_direction(
                    triangle_colours[other], state[edge]
                )
                * orientations[vertex]
            )
            if other in orientations:
                if orientations[other] != required:
                    return False
            else:
                orientations[other] = required
                queue.append(other)
    return True


def validate(state: tuple[int, ...]) -> None:
    assert all(label.bit_count() == 2 for label in state)
    assert all(len(row) == 3 for row in INCIDENCE)
    assert all(
        state[row[0]] ^ state[row[1]] ^ state[row[2]] == 0
        for row in INCIDENCE
    )


def main() -> None:
    validate(INITIAL)
    component = sum(1 << edge for edge in SWITCH_COMPONENT)
    assert component in component_masks(active_mask(INITIAL, PAIR))
    final = switched_state(INITIAL, PAIR, SWITCH_COMPONENT)
    validate(final)
    before = coordinate_component_counts(INITIAL)
    after = coordinate_component_counts(final)
    # The normalized coloured surface has F=8 and E=12, hence chi=V-4.
    before_chi = sum(before) - 4
    after_chi = sum(after) - 4
    assert before == [2, 1, 1, 0, 0]
    assert after == [2, 2, 2, 0, 0]
    assert (before_chi, after_chi) == (0, 2)

    validate(ORIENTABILITY_INITIAL)
    orientability_component = sum(
        1 << edge for edge in ORIENTABILITY_COMPONENT
    )
    assert orientability_component in component_masks(
        active_mask(ORIENTABILITY_INITIAL, ORIENTABILITY_PAIR)
    )
    orientability_final = switched_state(
        ORIENTABILITY_INITIAL,
        ORIENTABILITY_PAIR,
        ORIENTABILITY_COMPONENT,
    )
    assert coordinate_component_counts(ORIENTABILITY_INITIAL) == [
        1, 1, 1, 1, 0
    ]
    assert coordinate_component_counts(orientability_final) == [
        1, 1, 1, 1, 0
    ]
    assert not is_orientable(ORIENTABILITY_INITIAL)
    assert is_orientable(orientability_final)
    print(
        json.dumps(
            {
                "status": "PASS",
                "graph": "cube",
                "graph6": "Gl_XIS",
                "edges": [list(edge) for edge in EDGES],
                "initial_labels_hex": [
                    f"{label:02x}" for label in INITIAL
                ],
                "switch_pair": list(PAIR),
                "switch_component_edges": list(SWITCH_COMPONENT),
                "final_labels_hex": [
                    f"{label:02x}" for label in final
                ],
                "coordinate_link_components_before": before,
                "coordinate_link_components_after": after,
                "surface_euler_characteristic_before": before_chi,
                "surface_euler_characteristic_after": after_chi,
                "conclusion": (
                    "One legal Kempe switch changes the normalized "
                    "coloured surface Euler characteristic by two."
                ),
                "orientability_witness": {
                    "initial_labels_hex": [
                        f"{label:02x}"
                        for label in ORIENTABILITY_INITIAL
                    ],
                    "switch_pair": list(ORIENTABILITY_PAIR),
                    "switch_component_edges": list(
                        ORIENTABILITY_COMPONENT
                    ),
                    "coordinate_link_components_before_and_after": [
                        1, 1, 1, 1, 0
                    ],
                    "surface_euler_characteristic_before_and_after": 0,
                    "orientable_before": False,
                    "orientable_after": True,
                    "classification": "Klein bottle to torus",
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
