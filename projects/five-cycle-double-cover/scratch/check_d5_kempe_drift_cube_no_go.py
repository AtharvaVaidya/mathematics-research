#!/usr/bin/env python3
"""Exact checker for the D5 Kempe-drift identities' cube no-go.

The checker uses only the Python standard library.  It verifies:

* the displayed cube is simple, connected, cubic, and bridgeless;
* the displayed labels satisfy the D5 local xor equations;
* all ten factor component lists and all eighteen Kempe moves;
* the drift histogram 12 x 0 and 6 x -2, hence total drift -12;
* root edges 0 and 6 share no factor component;
* one displayed neutral move reaches an (0,6)-root-good state in the
  same terminal plateau;
* the cross-pair symmetric-difference update law for every cube move;
* the fixed-pair Boolean-cube identities, including the Fourier formula;
* minimum order for negative drift among connected simple cubic graphs,
  by an exact audit of K4, K3,3, and the triangular prism.

This is a checker for a no-go result about a proposed proof strategy.
It is not a Five-Cycle Double Cover solver or resolution.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json


PAIRS = tuple((1 << i) | (1 << j) for i, j in combinations(range(5), 2))
PAIR_SET = frozenset(PAIRS)

CUBE_EDGES = (
    (0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 3),
    (2, 6), (3, 5), (4, 5), (4, 7), (5, 6), (6, 7),
)
CUBE_FLOW = (
    0x05, 0x03, 0x06, 0x03, 0x06, 0x05,
    0x06, 0x06, 0x03, 0x05, 0x05, 0x03,
)

K4_EDGES = tuple(combinations(range(4), 2))
K33_EDGES = tuple(
    (left, right) for left in range(3) for right in range(3, 6)
)
PRISM_EDGES = (
    (0, 1), (1, 2), (0, 2),
    (3, 4), (4, 5), (3, 5),
    (0, 3), (1, 4), (2, 5),
)


def incidence(
    vertex_count: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(vertex_count)]
    for edge_id, (left, right) in enumerate(edges):
        assert left != right
        rows[left].append(edge_id)
        rows[right].append(edge_id)
    return tuple(tuple(row) for row in rows)


def validate_simple_connected_cubic(
    vertex_count: int, edges: tuple[tuple[int, int], ...]
) -> None:
    assert len(set(tuple(sorted(edge)) for edge in edges)) == len(edges)
    rows = incidence(vertex_count, edges)
    assert all(len(row) == 3 for row in rows)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for edge_id in rows[vertex]:
            left, right = edges[edge_id]
            other = right if left == vertex else left
            if other not in seen:
                seen.add(other)
                stack.append(other)
    assert len(seen) == vertex_count


def is_bridgeless(
    vertex_count: int, edges: tuple[tuple[int, int], ...]
) -> bool:
    rows = incidence(vertex_count, edges)
    for omitted in range(len(edges)):
        seen = {0}
        stack = [0]
        while stack:
            vertex = stack.pop()
            for edge_id in rows[vertex]:
                if edge_id == omitted:
                    continue
                left, right = edges[edge_id]
                other = right if left == vertex else left
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        if len(seen) != vertex_count:
            return False
    return True


def validate_flow(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
) -> None:
    assert len(flow) == len(edges)
    assert all(label in PAIR_SET for label in flow)
    for row in incidence(vertex_count, edges):
        assert flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0


def component_masks(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    selected: int,
) -> tuple[int, ...]:
    rows = incidence(vertex_count, edges)
    unseen = {
        edge_id
        for edge_id in range(len(edges))
        if (selected >> edge_id) & 1
    }
    answer = []
    while unseen:
        stack = [min(unseen)]
        component: set[int] = set()
        while stack:
            edge_id = stack.pop()
            if edge_id in component:
                continue
            component.add(edge_id)
            for vertex in edges[edge_id]:
                stack.extend(
                    other
                    for other in rows[vertex]
                    if (selected >> other) & 1
                    and other not in component
                )
        unseen -= component
        answer.append(sum(1 << edge_id for edge_id in component))
    return tuple(sorted(answer))


def coordinate_counts(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(
        len(
            component_masks(
                vertex_count,
                edges,
                sum(
                    1 << edge_id
                    for edge_id, label in enumerate(flow)
                    if (label >> coordinate) & 1
                ),
            )
        )
        for coordinate in range(5)
    )


def phi(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
) -> int:
    return sum(coordinate_counts(vertex_count, edges, flow)) - vertex_count // 2


def active_mask(flow: tuple[int, ...], pair: tuple[int, int]) -> int:
    first, second = pair
    return sum(
        1 << edge_id
        for edge_id, label in enumerate(flow)
        if ((label >> first) & 1) ^ ((label >> second) & 1)
    )


def switched(
    flow: tuple[int, ...],
    pair: tuple[int, int],
    component: int,
) -> tuple[int, ...]:
    toggle = (1 << pair[0]) | (1 << pair[1])
    answer = tuple(
        label ^ toggle if (component >> edge_id) & 1 else label
        for edge_id, label in enumerate(flow)
    )
    return answer


def moves(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
):
    base = phi(vertex_count, edges, flow)
    for pair in combinations(range(5), 2):
        factor = active_mask(flow, pair)
        for component in component_masks(vertex_count, edges, factor):
            target = switched(flow, pair, component)
            validate_flow(vertex_count, edges, target)
            yield pair, component, target, phi(vertex_count, edges, target) - base


def edge_tuple(mask: int, edge_count: int) -> tuple[int, ...]:
    return tuple(edge_id for edge_id in range(edge_count) if (mask >> edge_id) & 1)


def check_cross_pair_update_law() -> None:
    for pair, component, target, _ in moves(8, CUBE_EDGES, CUBE_FLOW):
        for other in combinations(range(5), 2):
            before = active_mask(CUBE_FLOW, other)
            expected = (
                before ^ component
                if len(set(pair) & set(other)) == 1
                else before
            )
            assert active_mask(target, other) == expected


def switch_subset(
    flow: tuple[int, ...],
    pair: tuple[int, int],
    components: tuple[int, ...],
    subset: int,
) -> tuple[int, ...]:
    answer = flow
    for index, component in enumerate(components):
        if (subset >> index) & 1:
            answer = switched(answer, pair, component)
    return answer


def check_fixed_pair_cube_identities() -> None:
    for pair in combinations(range(5), 2):
        components = component_masks(
            8, CUBE_EDGES, active_mask(CUBE_FLOW, pair)
        )
        dimension = len(components)
        full = (1 << dimension) - 1
        values = tuple(
            phi(
                8,
                CUBE_EDGES,
                switch_subset(CUBE_FLOW, pair, components, subset),
            )
            for subset in range(1 << dimension)
        )

        for subset in range(1 << dimension):
            assert values[subset] == values[full ^ subset]
            for coordinate in range(dimension):
                derivative = values[subset ^ (1 << coordinate)] - values[subset]
                reverse = (
                    values[subset] - values[subset ^ (1 << coordinate)]
                )
                complement_derivative = (
                    values[(full ^ subset) ^ (1 << coordinate)]
                    - values[full ^ subset]
                )
                assert derivative == -reverse
                assert derivative == complement_derivative

        for coordinate in range(dimension):
            assert sum(
                values[subset ^ (1 << coordinate)] - values[subset]
                for subset in range(1 << dimension)
            ) == 0

        fourier = {}
        for mask in range(1 << dimension):
            numerator = sum(
                values[subset]
                * (-1 if (mask & subset).bit_count() % 2 else 1)
                for subset in range(1 << dimension)
            )
            fourier[mask] = Fraction(numerator, 1 << dimension)
            if mask.bit_count() % 2:
                assert fourier[mask] == 0
        initial_drift = sum(
            values[1 << coordinate] - values[0]
            for coordinate in range(dimension)
        )
        fourier_drift = -2 * sum(
            mask.bit_count() * coefficient
            for mask, coefficient in fourier.items()
            if mask and mask.bit_count() % 2 == 0
        )
        assert initial_drift == fourier_drift


def enumerate_flows(
    vertex_count: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    """Enumerate literal D5 flows using local xor propagation."""
    rows = incidence(vertex_count, edges)
    state = [0] * len(edges)
    answers: list[tuple[int, ...]] = []

    def assign(edge_id: int, label: int, changed: list[int]) -> bool:
        if state[edge_id]:
            return state[edge_id] == label
        if label not in PAIR_SET:
            return False
        state[edge_id] = label
        changed.append(edge_id)
        pending = list(edges[edge_id])
        while pending:
            vertex = pending.pop()
            row = rows[vertex]
            assigned = [item for item in row if state[item]]
            if len(assigned) < 2:
                continue
            if len(assigned) == 3:
                if state[row[0]] ^ state[row[1]] ^ state[row[2]]:
                    return False
                continue
            missing = next(item for item in row if not state[item])
            forced = state[assigned[0]] ^ state[assigned[1]]
            if forced not in PAIR_SET:
                return False
            state[missing] = forced
            changed.append(missing)
            pending.extend(edges[missing])
        return True

    def visit() -> None:
        try:
            edge_id = next(
                index for index, label in enumerate(state) if not label
            )
        except StopIteration:
            answer = tuple(state)
            validate_flow(vertex_count, edges, answer)
            answers.append(answer)
            return
        for label in PAIRS:
            changed: list[int] = []
            if assign(edge_id, label, changed):
                visit()
            for item in reversed(changed):
                state[item] = 0

    visit()
    return tuple(answers)


def minimum_order_audit() -> dict[str, dict[str, int]]:
    result = {}
    graphs = (
        ("K4", 4, K4_EDGES, 180),
        ("K3,3", 6, K33_EDGES, 840),
        ("triangular_prism", 6, PRISM_EDGES, 540),
    )
    for name, vertex_count, edges, expected_flows in graphs:
        validate_simple_connected_cubic(vertex_count, edges)
        flows = enumerate_flows(vertex_count, edges)
        assert len(flows) == expected_flows
        move_count = 0
        for flow in flows:
            for _, _, _, delta in moves(vertex_count, edges, flow):
                move_count += 1
                assert delta == 0
        result[name] = {
            "literal_flows": len(flows),
            "indexed_moves_checked": move_count,
        }
    return result


def main() -> None:
    validate_simple_connected_cubic(8, CUBE_EDGES)
    assert is_bridgeless(8, CUBE_EDGES)
    validate_flow(8, CUBE_EDGES, CUBE_FLOW)
    assert coordinate_counts(8, CUBE_EDGES, CUBE_FLOW) == (2, 2, 2, 0, 0)
    assert phi(8, CUBE_EDGES, CUBE_FLOW) == 2

    records = tuple(moves(8, CUBE_EDGES, CUBE_FLOW))
    histogram: dict[int, int] = {}
    for _, _, _, delta in records:
        histogram[delta] = histogram.get(delta, 0) + 1
    assert histogram == {-2: 6, 0: 12}
    assert sum(delta for _, _, _, delta in records) == -12

    factors = {}
    root_good = False
    root_mask = (1 << 0) | (1 << 6)
    for pair in combinations(range(5), 2):
        components = component_masks(
            8, CUBE_EDGES, active_mask(CUBE_FLOW, pair)
        )
        factors["".join(map(str, pair))] = [
            list(edge_tuple(component, len(CUBE_EDGES)))
            for component in components
        ]
        if any(component & root_mask == root_mask for component in components):
            root_good = True
    assert not root_good

    # The displayed state is root-bad, but its terminal neutral plateau
    # is root-universal for this root pair.  One neutral move suffices.
    rescue_pair = (0, 3)
    rescue_component = sum(1 << edge_id for edge_id in (0, 1, 3, 5))
    assert rescue_component in component_masks(
        8, CUBE_EDGES, active_mask(CUBE_FLOW, rescue_pair)
    )
    rescued = switched(CUBE_FLOW, rescue_pair, rescue_component)
    validate_flow(8, CUBE_EDGES, rescued)
    assert phi(8, CUBE_EDGES, rescued) == 2
    rescue_factor_pair = (0, 2)
    rescue_root_component = sum(
        1 << edge_id for edge_id in (0, 2, 4, 5, 6, 7, 8, 11)
    )
    assert rescue_root_component in component_masks(
        8, CUBE_EDGES, active_mask(rescued, rescue_factor_pair)
    )
    assert rescue_root_component & root_mask == root_mask

    check_cross_pair_update_law()
    check_fixed_pair_cube_identities()
    small = minimum_order_audit()

    print(
        json.dumps(
            {
                "status": "PASS",
                "scope": (
                    "no-go for averaged-positive D5 Kempe Euler drift; "
                    "not a FiveCDC resolution"
                ),
                "graph": "cube",
                "graph6": "Gl_XIS",
                "vertices": 8,
                "edges": [list(edge) for edge in CUBE_EDGES],
                "bridgeless": True,
                "labels_hex": [f"{label:02x}" for label in CUBE_FLOW],
                "coordinate_component_counts": [2, 2, 2, 0, 0],
                "surface_euler_characteristic": 2,
                "factor_components": factors,
                "indexed_moves": len(records),
                "delta_histogram": {
                    str(delta): count
                    for delta, count in sorted(histogram.items())
                },
                "total_drift": -12,
                "root_edges": [0, 6],
                "root_good_at_displayed_state": False,
                "neutral_root_rescue": {
                    "switch_pair": list(rescue_pair),
                    "switch_component_edges": [
                        0, 1, 3, 5
                    ],
                    "delta": 0,
                    "rescued_labels_hex": [
                        f"{label:02x}" for label in rescued
                    ],
                    "root_good_factor_pair": list(rescue_factor_pair),
                    "root_good_component_edges": [
                        0, 2, 4, 5, 6, 7, 8, 11
                    ],
                },
                "cross_pair_update_law": "PASS",
                "fixed_pair_cube_identities": "PASS",
                "smaller_simple_cubic_audit": small,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
