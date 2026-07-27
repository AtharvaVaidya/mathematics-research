#!/usr/bin/env python3
"""Audit the combined-line Fano span theorem and nonlinear normal form.

The universal proof is in docs/fano-combined-line-span.md.  This script
checks its finite transition table and replays the theorem on the retained
ten-vertex resistant flow without calling a SAT solver.  In particular,
it computes actual final colors after mixed switches rather than identifying
the initial linearization with the final rainbow change.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations


EDGES = (
    (0, 3),
    (0, 6),
    (0, 7),
    (1, 4),
    (1, 6),
    (1, 8),
    (2, 5),
    (2, 7),
    (2, 9),
    (3, 6),
    (3, 9),
    (4, 7),
    (4, 8),
    (5, 8),
    (5, 9),
)
FLOW = (2, 1, 3, 5, 6, 3, 6, 7, 1, 7, 5, 4, 1, 2, 4)
ORDER = 10
LINES = tuple(
    sorted(
        {
            tuple(sorted((first, second, first ^ second)))
            for first, second in combinations(range(1, 8), 2)
        }
    )
)


def boundary(mask: int) -> int:
    result = 0
    for edge, (u, v) in enumerate(EDGES):
        if (mask >> edge) & 1:
            result ^= 1 << u
            result ^= 1 << v
    return result


def components(selected: set[int]) -> tuple[frozenset[int], ...]:
    adjacency = [[] for _ in range(ORDER)]
    for edge in selected:
        u, v = EDGES[edge]
        adjacency[u].append(v)
        adjacency[v].append(u)
    unseen = set(range(ORDER))
    output = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if v in unseen:
                    unseen.remove(v)
                    component.add(v)
                    queue.append(v)
        output.append(frozenset(component))
    return tuple(output)


def cut(component: frozenset[int]) -> set[int]:
    return {
        edge
        for edge, (u, v) in enumerate(EDGES)
        if (u in component) != (v in component)
    }


def potential(state: int) -> int:
    u = (state >> 3) & 1
    x1 = state & 1
    x2 = (state >> 1) & 1
    x3 = (state >> 2) & 1
    first = u & (x2 ^ x3)
    second = u & (x1 ^ x3)
    third = (x1 & x2) ^ (x1 & x3) ^ (x2 & x3)
    return first | (second << 1) | (third << 2)


def dot(first: int, second: int) -> int:
    return (first & second).bit_count() & 1


def active_delta(color: int) -> int:
    if color <= 3:
        coordinate = {1: 0, 2: 1, 3: 2}[color]
        return 1 << coordinate
    return 0b1000 | {4: 0b111, 5: 0b001, 6: 0b010, 7: 0b100}[color]


def toggle(
    line: tuple[int, int, int],
    line_components: tuple[frozenset[int], ...],
    switch_value: int,
    cycle: int,
) -> int:
    outside = [value for value in range(1, 8) if value not in line]
    pair = {outside[0], outside[0] ^ switch_value}
    result = 0
    for position, component in enumerate(line_components):
        parity = sum(
            (cycle >> edge) & 1
            for edge in cut(component)
            if FLOW[edge] in pair
        ) & 1
        result |= parity << position
    return result


def rainbow_vector(
    line: tuple[int, int, int],
    line_components: tuple[frozenset[int], ...],
    flow: tuple[int, ...] = FLOW,
) -> int:
    outside = [value for value in range(1, 8) if value not in line]
    result = 0
    for position, component in enumerate(line_components):
        parities = tuple(
            sum(flow[edge] == value for edge in cut(component)) & 1
            for value in outside
        )
        assert len(set(parities)) == 1
        result |= parities[0] << position
    return result


def mixed_affine_change(s: int, membership: int) -> tuple[int, int]:
    """Return actual and initial-linearized b-color changes.

    The kernel line is encoded as 1,2,3 and the affine color as 4+s.
    Bit t-1 of membership records the switch by t.
    """

    z = 0
    linear = 0
    for switch_value in (1, 2, 3):
        if (membership >> (switch_value - 1)) & 1:
            z ^= switch_value
            linear ^= int(s in (0, switch_value))
    actual = int(s == 0) ^ int((s ^ z) == 0)
    return actual, linear


def main() -> int:
    # Check the local telescoping identity on all 16 states, including
    # both the inactive and active transition for every flow color.
    transition_checks = 0
    for color in range(1, 8):
        delta = active_delta(color)
        for state in range(16):
            for other in (state, state ^ delta):
                observed = dot(potential(state) ^ potential(other), color)
                expected = int(color == 4 and other != state)
                assert observed == expected
                transition_checks += 1

    for vertex in range(ORDER):
        incident = [
            FLOW[edge]
            for edge, endpoints in enumerate(EDGES)
            if vertex in endpoints
        ]
        assert len(incident) == 3
        assert incident[0] ^ incident[1] ^ incident[2] == 0
        assert len(set(incident)) == 3

    cycles = tuple(
        mask for mask in range(1 << len(EDGES)) if boundary(mask) == 0
    )
    assert len(cycles) == 64

    mixed_nonlinearity_mismatches = 0
    for affine_offset in range(4):
        for membership in range(8):
            actual, linear = mixed_affine_change(
                affine_offset, membership
            )
            if actual != linear:
                mixed_nonlinearity_mismatches += 1
            assert (actual == linear) == (membership.bit_count() <= 1)
    assert mixed_nonlinearity_mismatches == 16

    audited_lines = 0
    actual_clean_lines = 0
    normal_form_lines = 0
    for line in LINES:
        line_edges = {
            edge for edge, value in enumerate(FLOW) if value in line
        }
        line_components = components(line_edges)
        rainbow = rainbow_vector(line, line_components)
        assert rainbow != 0

        options: dict[int, list[tuple[int, int]]] = {}
        span = {0}
        for switch_value in line:
            forbidden = sum(
                1 << edge
                for edge, value in enumerate(FLOW)
                if value == switch_value
            )
            options[switch_value] = [
                (
                    cycle,
                    toggle(
                        line,
                        line_components,
                        switch_value,
                        cycle,
                    ),
                )
                for cycle in cycles
                if cycle & forbidden == 0
            ]
            for _, image in options[switch_value]:
                span |= {value ^ image for value in tuple(span)}
        assert rainbow in span

        first, second, third = line
        found_actual = False
        masks = {
            value: sum(
                1 << edge
                for edge, edge_value in enumerate(FLOW)
                if edge_value == value
            )
            for value in line
        }
        for cycle_first, _ in options[first]:
            for cycle_second, _ in options[second]:
                if cycle_first & cycle_second & masks[first ^ second]:
                    continue
                for cycle_third, _ in options[third]:
                    if cycle_first & cycle_third & masks[first ^ third]:
                        continue
                    if cycle_second & cycle_third & masks[second ^ third]:
                        continue
                    final_flow = tuple(
                        value
                        ^ (first if (cycle_first >> edge) & 1 else 0)
                        ^ (second if (cycle_second >> edge) & 1 else 0)
                        ^ (third if (cycle_third >> edge) & 1 else 0)
                        for edge, value in enumerate(FLOW)
                    )
                    assert all(final_flow)
                    for vertex in range(ORDER):
                        incident = [
                            final_flow[edge]
                            for edge, endpoints in enumerate(EDGES)
                            if vertex in endpoints
                        ]
                        assert incident[0] ^ incident[1] ^ incident[2] == 0
                    if (
                        rainbow_vector(
                            line, line_components, final_flow
                        )
                        == 0
                    ):
                        found_actual = True
                        break
                if found_actual:
                    break
            if found_actual:
                break
        assert found_actual
        actual_clean_lines += 1

        # Audit the exact two-cycle normal form.  Choose coordinates on
        # ker(mu) by mapping the three line values to 01, 10, 11.
        line_coordinates = {
            line[0]: 1,
            line[1]: 2,
            line[2]: 3,
        }
        found_normal_form = False
        for p_cycle in cycles:
            for q_cycle in cycles:
                if any(
                    (
                        ((p_cycle >> edge) & 1) == 0
                        and ((q_cycle >> edge) & 1) == 0
                    )
                    for edge in line_edges
                ):
                    continue
                if any(
                    sum(
                        ((p_cycle >> edge) & 1)
                        & ((q_cycle >> edge) & 1)
                        for edge in cut(component)
                    )
                    & 1
                    for component in line_components
                ):
                    continue
                candidate_flow = []
                affine_base = min(
                    value for value in range(1, 8) if value not in line
                )
                basis_images = {
                    0: 0,
                    1: line[0],
                    2: line[1],
                    3: line[2],
                }
                for edge, old_value in enumerate(FLOW):
                    kernel_part = basis_images[
                        ((p_cycle >> edge) & 1)
                        | (((q_cycle >> edge) & 1) << 1)
                    ]
                    candidate_flow.append(
                        kernel_part
                        if edge in line_edges
                        else affine_base ^ kernel_part
                    )
                candidate = tuple(candidate_flow)
                assert all(candidate)
                assert rainbow_vector(
                    line, line_components, candidate
                ) == 0
                found_normal_form = True
                break
            if found_normal_form:
                break
        assert found_normal_form
        normal_form_lines += 1
        audited_lines += 1

    print("Fano combined-line span audit: PASS")
    print(f"transition_checks={transition_checks}")
    print(
        "mixed_nonlinearity_mismatches="
        f"{mixed_nonlinearity_mismatches}"
    )
    print(f"binary_cycles={len(cycles)}")
    print(f"audited_lines={audited_lines}")
    print(f"actual_clean_lines={actual_clean_lines}")
    print(f"normal_form_lines={normal_form_lines}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
