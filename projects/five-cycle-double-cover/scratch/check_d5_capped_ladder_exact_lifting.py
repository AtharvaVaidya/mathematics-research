#!/usr/bin/env python3
"""Check exact capped-ladder word lifting and constructive eventual rescue."""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for item in (str(PROJECT_ROOT), str(PROJECT_ROOT / "scratch")):
    if item not in sys.path:
        sys.path.insert(0, item)

from check_d5_hzero_capped_ladder_delay_family import (  # noqa: E402
    construct,
)


PAIRS = tuple(itertools.combinations(range(5), 2))
LABELS = tuple(sum(1 << i for i in pair) for pair in PAIRS)
ADJACENT = {
    label: tuple(
        other
        for other in LABELS
        if (label & other).bit_count() == 1
    )
    for label in LABELS
}
P = (0, 3, 4, 5, 6, 7)
Q = (0, 1, 2, 3)


def active(label, pair_mask):
    return (label & pair_mask).bit_count() == 1


def transpose(label, pair_mask):
    return label ^ pair_mask if active(label, pair_mask) else label


def word_move(word, side, pair_mask):
    answer = list(word)
    if side == "left":
        position = 0
        assert active(answer[position], pair_mask)
        while position < len(answer) and active(
            answer[position], pair_mask
        ):
            answer[position] = transpose(answer[position], pair_mask)
            position += 1
    else:
        position = len(answer) - 1
        assert active(answer[position], pair_mask)
        while position >= 0 and active(answer[position], pair_mask):
            answer[position] = transpose(answer[position], pair_mask)
            position -= 1
    return tuple(answer)


def recolor_last(word, target):
    """Use at most two singleton suffix moves fixing the penultimate label."""
    if word[-1] == target:
        return word, []
    penultimate = word[-2]
    assert (penultimate & target).bit_count() == 1
    inside = [
        coordinate
        for coordinate in range(5)
        if (penultimate >> coordinate) & 1
    ]
    outside = [
        coordinate
        for coordinate in range(5)
        if not ((penultimate >> coordinate) & 1)
    ]

    def code(label):
        removed = next(
            coordinate
            for coordinate in inside
            if not ((label >> coordinate) & 1)
        )
        added = next(
            coordinate
            for coordinate in outside
            if (label >> coordinate) & 1
        )
        return removed, added

    removed, added = code(word[-1])
    target_removed, target_added = code(target)
    moves = []
    if removed != target_removed:
        pair_mask = (1 << inside[0]) | (1 << inside[1])
        assert not active(penultimate, pair_mask)
        word = word_move(word, "right", pair_mask)
        moves.append(("right", pair_mask))
        removed, added = code(word[-1])
    if added != target_added:
        pair_mask = (1 << added) | (1 << target_added)
        assert not active(penultimate, pair_mask)
        word = word_move(word, "right", pair_mask)
        moves.append(("right", pair_mask))
    assert word[-1] == target
    assert len(moves) <= 2
    return word, moves


def alternatize(word):
    """Construct the inductive endpoint-move sequence from Theorem 4."""
    if len(word) <= 2:
        return word, []

    prefix_final, prefix_plan = alternatize(word[:-1])
    current = word
    plan = []
    for side, pair_mask in prefix_plan:
        if side == "left":
            current = word_move(current, side, pair_mask)
            plan.append((side, pair_mask))
        else:
            penultimate = current[-2]
            assert active(penultimate, pair_mask)
            active_neighbor = transpose(penultimate, pair_mask)
            current, preparation = recolor_last(
                current, active_neighbor
            )
            plan.extend(preparation)
            current = word_move(current, side, pair_mask)
            plan.append((side, pair_mask))

    assert current[:-1] == prefix_final
    first, second = prefix_final[:2]
    assert all(
        label == (first if index % 2 == 0 else second)
        for index, label in enumerate(prefix_final)
    )
    target = second if current[-2] == first else first
    current, preparation = recolor_last(current, target)
    plan.extend(preparation)
    assert all(
        label == (current[0] if index % 2 == 0 else current[1])
        for index, label in enumerate(current)
    )
    return current, plan


def components(edges, state, pair_mask):
    vertices = 1 + max(max(edge) for edge in edges)
    incidence = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    unseen = {
        edge
        for edge, label in enumerate(state)
        if active(label, pair_mask)
    }
    answer = []
    while unseen:
        first = min(unseen)
        unseen.remove(first)
        component = {first}
        stack = [first]
        while stack:
            edge = stack.pop()
            for vertex in edges[edge]:
                for other in incidence[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        component.add(other)
                        stack.append(other)
        answer.append(tuple(sorted(component)))
    return tuple(answer)


def switch_state(state, pair_mask, component):
    answer = list(state)
    for edge in component:
        answer[edge] = transpose(answer[edge], pair_mask)
    return tuple(answer)


def check_cap_transfer():
    # Left diamond: internal edges 0..4, attachment edges 5,6.
    edges = (
        (0, 2), (1, 2), (0, 3), (1, 3), (2, 3), (0, 4), (1, 5)
    )
    solutions = []
    for e0, e1, e2, e3 in itertools.product(LABELS, repeat=4):
        e4 = e0 ^ e1
        e5 = e0 ^ e2
        e6 = e1 ^ e3
        if e4 in LABELS and e5 in LABELS and e6 == e5:
            solutions.append((e0, e1, e2, e3, e4, e5, e6))
    assert len(solutions) == 180
    for state in solutions:
        assert (state[0] & state[5]).bit_count() == 1
        for pair_mask in LABELS:
            if not active(state[0], pair_mask):
                continue
            root_component = next(
                component
                for component in components(edges, state, pair_mask)
                if 0 in component
            )
            expected = active(state[5], pair_mask)
            assert (5 in root_component) == expected
            assert (6 in root_component) == expected
    return len(solutions)


def check_cell_transfer():
    directed_cells = 0
    factor_tests = 0
    for left in LABELS:
        for right in LABELS:
            rung = left ^ right
            if rung not in LABELS:
                continue
            directed_cells += 1
            assert (left & right).bit_count() == 1
            for pair_mask in LABELS:
                factor_tests += 1
                left_active = active(left, pair_mask)
                right_active = active(right, pair_mask)
                rung_active = active(rung, pair_mask)
                assert rung_active == (left_active ^ right_active)
                if left_active and right_active:
                    assert not rung_active  # two straight strands
                if left_active and not right_active:
                    assert rung_active  # left U-turn
                if right_active and not left_active:
                    assert rung_active  # right U-turn
    assert directed_cells == 60
    return directed_cells, factor_tests


def check_abstract_walks(through=6):
    walks = 0
    maximum_plan = 0
    for length in range(1, through + 1):
        for choices in itertools.product(range(6), repeat=length - 1):
            word = [0b00011]  # Normalize the first label to 01.
            for choice in choices:
                word.append(ADJACENT[word[-1]][choice])
            final, plan = alternatize(tuple(word))
            replay = tuple(word)
            for side, pair_mask in plan:
                replay = word_move(replay, side, pair_mask)
            assert replay == final
            assert all(
                label == (final[0] if index % 2 == 0 else final[1])
                for index, label in enumerate(final)
            )
            common_pair = (
                final[0] ^ final[1]
                if len(final) >= 2
                else final[0] ^ ADJACENT[final[0]][0]
            )
            assert common_pair in LABELS
            assert all(active(label, common_pair) for label in final)
            walks += 1
            maximum_plan = max(maximum_plan, len(plan))
    assert walks == sum(6 ** (length - 1) for length in range(1, through + 1))
    return walks, maximum_plan


def check_actual_lifts():
    rows = []
    for length in range(2, 9):
        edges, _, state, _ = construct(length)
        roots = (0, 10 + 3 * length)  # noncentral right-cap edge
        cuts = (
            ((5, 6),)
            + tuple(
                (8 + 3 * index, 9 + 3 * index)
                for index in range(length)
            )
            + ((8 + 3 * length, 9 + 3 * length),)
        )

        def word(value):
            assert all(value[left] == value[right] for left, right in cuts)
            return (
                (value[roots[0]],)
                + tuple(value[left] for left, _ in cuts)
                + (value[roots[1]],)
            )

        initial_word = word(state)
        assert all(
            (initial_word[index] & initial_word[index + 1]).bit_count()
            == 1
            for index in range(len(initial_word) - 1)
        )
        final_word, plan = alternatize(initial_word)
        current_word = initial_word
        current_state = state
        for side, pair_mask in plan:
            root = roots[0] if side == "left" else roots[1]
            component = next(
                component
                for component in components(
                    edges, current_state, pair_mask
                )
                if root in component
            )
            current_state = switch_state(
                current_state, pair_mask, component
            )
            current_word = word_move(current_word, side, pair_mask)
            assert word(current_state) == current_word
        assert current_word == final_word
        common_pair = final_word[0] ^ final_word[1]
        common_component = next(
            component
            for component in components(
                edges, current_state, common_pair
            )
            if roots[0] in component
        )
        assert roots[1] in common_component

        # The noncentral-root version still has the uniform H=0 loop.
        other_label = state[roots[1]]
        hole = next(
            coordinate
            for coordinate in range(3)
            if not ((other_label >> coordinate) & 1)
        )
        line_by_hole = {
            0: ((0, 4), (3, 4), (0, 3)),
            1: ((1, 3), (3, 4), (1, 4)),
            2: ((2, 4), (3, 4), (2, 3)),
        }
        line_state = state
        line_circuits = []
        for pair in line_by_hole[hole]:
            pair_mask = (1 << pair[0]) | (1 << pair[1])
            component = next(
                component
                for component in components(
                    edges, line_state, pair_mask
                )
                if roots[0] in component
            )
            assert roots[1] not in component
            line_circuits.append(component)
            line_state = switch_state(
                line_state, pair_mask, component
            )
        assert line_circuits[0] == line_circuits[2] == Q
        assert line_circuits[1] == P
        rows.append((length, len(initial_word), len(plan)))
    return rows


def main():
    cap_solutions = check_cap_transfer()
    cells, cell_factor_tests = check_cell_transfer()
    walks, maximum_plan = check_abstract_walks()
    actual_rows = check_actual_lifts()
    print(
        "PASS: exact capped-ladder lifting and eventual rescue; "
        f"cap_solutions={cap_solutions}, directed_cells={cells}, "
        f"cell_factor_tests={cell_factor_tests}, "
        f"normalized_walks_through6={walks}, "
        f"maximum_constructive_plan={maximum_plan}, "
        f"actual_lifts={actual_rows}"
    )


if __name__ == "__main__":
    main()
