#!/usr/bin/env python3
"""Complete order-12 audit of the residual-transport trichotomy.

For every saturated disjoint root-bad state and every all-bad oriented
line triangle at the first root with nonzero residual H, try both
orientations of both complementary star triangles at the second root,
in both operation orders.  Accept rescue or strict lexicographic descent
of (number of H edges, number of H circuit components).
"""

from __future__ import annotations

import functools
import itertools
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for item in (str(PROJECT_ROOT), str(PROJECT_ROOT / "scratch")):
    if item not in sys.path:
        sys.path.insert(0, item)

from audit_d5_root_kempe_orbits import (  # noqa: E402
    PAIRS,
    active_mask,
    component_edge_masks,
    enumerate_flows,
)
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402


PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}


def graph_records(geng: Path, order: int) -> list[str]:
    return subprocess.check_output(
        [str(geng), "-Cq", "-d3", "-D3", str(order)],
        text=True,
        encoding="ascii",
    ).splitlines()


def audit_graph(record: str) -> dict[str, int]:
    graph = graph_from_graph6(record)
    edge_count = graph.edge_count

    @functools.lru_cache(maxsize=None)
    def factor_data(state: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
        return tuple(
            tuple(
                component
                for component in component_edge_masks(
                    graph, active_mask(state, *pair)
                )
                if component
            )
            for pair in PAIRS
        )

    @functools.lru_cache(maxsize=None)
    def successful_pairs(state: tuple[int, ...]) -> frozenset[tuple[int, int]]:
        answer = set()
        for components in factor_data(state):
            for component in components:
                edges = [
                    edge
                    for edge in range(edge_count)
                    if (component >> edge) & 1
                ]
                answer.update(itertools.combinations(edges, 2))
        return frozenset(answer)

    def switch(
        state: tuple[int, ...],
        pair: tuple[int, int],
        component: int,
    ) -> tuple[int, ...]:
        toggle = (1 << pair[0]) | (1 << pair[1])
        return tuple(
            label ^ toggle if (component >> edge) & 1 else label
            for edge, label in enumerate(state)
        )

    def lift(
        state: tuple[int, ...],
        moving_root: int,
        other_root: int,
        sequence: tuple[tuple[int, int], ...],
    ) -> tuple[tuple[int, ...], tuple[int, ...], bool]:
        circuits = []
        root_pair = tuple(sorted((moving_root, other_root)))
        for pair in sequence:
            component = next(
                component
                for component in factor_data(state)[PAIR_INDEX[pair]]
                if (component >> moving_root) & 1
            )
            if (component >> other_root) & 1:
                return state, tuple(circuits), True
            state = switch(state, pair, component)
            circuits.append(component)
            if root_pair in successful_pairs(state):
                return state, tuple(circuits), True
        return state, tuple(circuits), False

    def coordinates(label: int) -> tuple[int, int]:
        answer = tuple(
            coordinate for coordinate in range(5) if (label >> coordinate) & 1
        )
        assert len(answer) == 2
        return answer

    def component_count(even_mask: int) -> int:
        return len(
            [
                component
                for component in component_edge_masks(graph, even_mask)
                if component
            ]
        )

    def root_neighbours(
        state: tuple[int, ...],
        first_root: int,
        second_root: int,
    ) -> set[tuple[int, ...]]:
        answer = set()
        for root in (first_root, second_root):
            root_label = state[root]
            for pair_index, pair in enumerate(PAIRS):
                pair_mask = (1 << pair[0]) | (1 << pair[1])
                if (root_label & pair_mask).bit_count() != 1:
                    continue
                component = next(
                    component
                    for component in factor_data(state)[pair_index]
                    if (component >> root) & 1
                )
                answer.add(switch(state, pair, component))
        return answer

    def root_rescue_radius(
        state: tuple[int, ...],
        first_root: int,
        second_root: int,
    ) -> int:
        root_pair = tuple(sorted((first_root, second_root)))
        first_layer = root_neighbours(state, first_root, second_root)
        if any(root_pair in successful_pairs(other) for other in first_layer):
            return 1
        if any(
            root_pair in successful_pairs(last)
            for other in first_layer
            for last in root_neighbours(other, first_root, second_root)
        ):
            return 2
        return 3

    counts = {
        "candidate_line_residuals": 0,
        "rescues": 0,
        "strict_descents": 0,
        "descents_to_zero": 0,
        "descents_by_fewer_edges": 0,
        "descents_by_fewer_components_at_equal_edges": 0,
        "failures": 0,
        "maximum_residual_edges": 0,
        "maximum_residual_components": 0,
        "hzero_line_loops": 0,
        "hzero_identity_line_loops": 0,
        "hzero_nontrivial_line_loops": 0,
        "hzero_root_radius_one": 0,
        "hzero_root_radius_two": 0,
        "hzero_root_radius_failures": 0,
        "maximum_hzero_support_edges": 0,
    }

    for state in enumerate_flows(graph):
        if functools.reduce(int.__or__, state, 0) != 0b11111:
            continue
        initial_successes = successful_pairs(state)
        for first_root, second_root in itertools.permutations(
            range(edge_count), 2
        ):
            if state[first_root] & state[second_root]:
                continue
            if tuple(sorted((first_root, second_root))) in initial_successes:
                continue

            first_label = coordinates(state[first_root])
            second_label = coordinates(state[second_root])
            hole = next(
                coordinate
                for coordinate in range(5)
                if coordinate not in first_label + second_label
            )
            for a, b in (first_label, first_label[::-1]):
                hidden = tuple(sorted((a, b)))
                line_sequence = (
                    tuple(sorted((b, hole))),
                    hidden,
                    tuple(sorted((a, hole))),
                )
                after_line, line_circuits, line_rescue = lift(
                    state,
                    first_root,
                    second_root,
                    line_sequence,
                )
                if line_rescue or len(line_circuits) != 3:
                    continue
                residual = line_circuits[0] ^ line_circuits[2]
                if not residual:
                    support = line_circuits[0] ^ line_circuits[1]
                    counts["hzero_line_loops"] += 1
                    if support:
                        counts["hzero_nontrivial_line_loops"] += 1
                    else:
                        counts["hzero_identity_line_loops"] += 1
                    counts["maximum_hzero_support_edges"] = max(
                        counts["maximum_hzero_support_edges"],
                        support.bit_count(),
                    )
                    radius = min(
                        root_rescue_radius(
                            state, first_root, second_root
                        ),
                        root_rescue_radius(
                            after_line, first_root, second_root
                        ),
                    )
                    if radius == 1:
                        counts["hzero_root_radius_one"] += 1
                    elif radius == 2:
                        counts["hzero_root_radius_two"] += 1
                    else:
                        counts["hzero_root_radius_failures"] += 1
                        raise AssertionError(
                            (
                                "hzero-root-radius",
                                record,
                                state,
                                first_root,
                                second_root,
                                line_sequence,
                                support,
                            )
                        )
                    continue

                counts["candidate_line_residuals"] += 1
                measure = (
                    residual.bit_count(),
                    component_count(residual),
                )
                counts["maximum_residual_edges"] = max(
                    counts["maximum_residual_edges"], measure[0]
                )
                counts["maximum_residual_components"] = max(
                    counts["maximum_residual_components"], measure[1]
                )

                accepted = False
                accepted_by_rescue = False
                accepted_measure = None
                for replaced_coordinate in second_label:
                    # The other second-root coordinate remains fixed in the
                    # corresponding star triangle.
                    star_sequences = (
                        (
                            tuple(sorted((a, replaced_coordinate))),
                            hidden,
                            tuple(sorted((b, replaced_coordinate))),
                        ),
                        (
                            tuple(sorted((b, replaced_coordinate))),
                            hidden,
                            tuple(sorted((a, replaced_coordinate))),
                        ),
                    )
                    for star_sequence in star_sequences:
                        after_star, _, star_rescue = lift(
                            state,
                            second_root,
                            first_root,
                            star_sequence,
                        )
                        if star_rescue:
                            accepted = accepted_by_rescue = True
                            break

                        _, _, line_then_star_rescue = lift(
                            after_line,
                            second_root,
                            first_root,
                            star_sequence,
                        )
                        if line_then_star_rescue:
                            accepted = accepted_by_rescue = True
                            break

                        _, transported_circuits, star_then_line_rescue = lift(
                            after_star,
                            first_root,
                            second_root,
                            line_sequence,
                        )
                        if star_then_line_rescue:
                            accepted = accepted_by_rescue = True
                            break

                        assert len(transported_circuits) == 3
                        transported = (
                            transported_circuits[0]
                            ^ transported_circuits[2]
                        )
                        transported_measure = (
                            transported.bit_count(),
                            component_count(transported)
                            if transported
                            else 0,
                        )
                        if transported_measure < measure:
                            accepted = True
                            accepted_measure = transported_measure
                            break
                    if accepted:
                        break

                if accepted_by_rescue:
                    counts["rescues"] += 1
                elif accepted:
                    counts["strict_descents"] += 1
                    assert accepted_measure is not None
                    if accepted_measure[0] == 0:
                        counts["descents_to_zero"] += 1
                    elif accepted_measure[0] < measure[0]:
                        counts["descents_by_fewer_edges"] += 1
                    else:
                        assert accepted_measure[1] < measure[1]
                        counts[
                            "descents_by_fewer_components_at_equal_edges"
                        ] += 1
                else:
                    counts["failures"] += 1
                    raise AssertionError(
                        (
                            record,
                            state,
                            first_root,
                            second_root,
                            line_sequence,
                            residual,
                            measure,
                        )
                    )
    return counts


def main() -> None:
    geng = Path("/opt/homebrew/bin/geng")
    totals: dict[str, int] = {}
    start = time.monotonic()
    graph_count = 0
    for order in (4, 6, 8, 10, 12):
        for record in graph_records(geng, order):
            row = audit_graph(record)
            graph_count += 1
            for key, value in row.items():
                if key.startswith("maximum_"):
                    totals[key] = max(totals.get(key, 0), value)
                else:
                    totals[key] = totals.get(key, 0) + value

    assert graph_count == 107
    print(f"totals={totals}", flush=True)
    assert totals["candidate_line_residuals"] == 11_718
    assert totals["rescues"] == 11_076
    assert totals["strict_descents"] == 642
    assert totals["descents_to_zero"] == 622
    assert totals["descents_by_fewer_edges"] == 20
    assert totals["descents_by_fewer_components_at_equal_edges"] == 0
    assert totals["maximum_residual_edges"] == 10
    assert totals["maximum_residual_components"] == 2
    assert totals["hzero_line_loops"] == 22_197
    assert totals["hzero_identity_line_loops"] == 0
    assert totals["hzero_nontrivial_line_loops"] == 22_197
    assert totals["hzero_root_radius_one"] == 20_805
    assert totals["hzero_root_radius_two"] == 1_392
    assert totals["hzero_root_radius_failures"] == 0
    assert totals["maximum_hzero_support_edges"] == 12
    assert (
        totals["hzero_identity_line_loops"]
        + totals["hzero_nontrivial_line_loops"]
        == totals["hzero_line_loops"]
    )
    assert totals["failures"] == 0
    assert (
        totals["rescues"] + totals["strict_descents"]
        == totals["candidate_line_residuals"]
    )
    print(
        "PASS: 107 graphs through order 12, "
        f"{totals['candidate_line_residuals']} nonzero all-bad line "
        f"residuals, {totals['rescues']} complementary-star rescues, "
        f"{totals['strict_descents']} strict residual descents, "
        f"0 failures; descent split zero={totals['descents_to_zero']}, "
        f"fewer_edges={totals['descents_by_fewer_edges']}, "
        "equal_edges_fewer_components="
        f"{totals['descents_by_fewer_components_at_equal_edges']}; "
        f"max residual=({totals['maximum_residual_edges']} edges,"
        f"{totals['maximum_residual_components']} components); "
        f"H=0 loops={totals['hzero_line_loops']} with root-local rescue "
        f"radius1={totals['hzero_root_radius_one']}, "
        f"radius2={totals['hzero_root_radius_two']}, failures=0; "
        f"elapsed={time.monotonic() - start:.2f}s"
    )


if __name__ == "__main__":
    main()
