#!/usr/bin/env python3
"""Independent replay of the girth-10 three-way exchange cube."""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
GRAPH_PATH = (
    HERE.parent.parent
    / "artifacts/structured/graphs/lift13_petersen_girth10.json"
)
SEMANTICS_PATH = (
    HERE.parent
    / "jaeger-lift13-girth10-augmented-trap-20260729"
    / "independent_verify.py"
)
SPEC = importlib.util.spec_from_file_location("semantics", SEMANTICS_PATH)
assert SPEC and SPEC.loader
semantics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(semantics)

EXPECTED_CUBE = {
    0: ((72, 69, 69), (22, 28, 14, 24, 16, 14, 2), 0, (2, 210)),
    1: ((72, 69, 69), (22, 28, 14, 24, 16, 14, 2), 0, (2, 210)),
    2: ((72, 70, 68), (20, 22, 10, 26, 16, 14, 2), 0, (2, 210)),
    3: ((72, 70, 68), (20, 22, 10, 26, 16, 14, 2), 0, (2, 210)),
    4: ((73, 69, 69), (20, 26, 14, 26, 14, 20, 6), 0, (6, 211)),
    5: ((71, 67, 69), (18, 26, 12, 24, 12, 16, 4), 0, (4, 207)),
    6: ((73, 70, 68), (20, 20, 14, 30, 10, 22, 6), 0, (6, 211)),
    7: ((71, 70, 68), (20, 22, 10, 24, 16, 14, 2), 0, (2, 209)),
}
EXPECTED_PATH_CIRCUITS = (
    (
        (0, 32, False, 14),
        (1, 10, False, 5),
    ),
    (
        (1, 29, True, 14),
        (2, 11, True, 6),
    ),
    (
        (0, 11, True, 6),
        (1, 16, False, 7),
    ),
)


def apply_exchange(labels, exchange):
    changed = list(labels)
    first, second = exchange
    changed[first], changed[second] = (
        changed[second], changed[first]
    )
    return tuple(changed)


def load_graph():
    source = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    order = int(source["vertices"])
    unordered = {
        tuple(sorted((int(edge["u"]), int(edge["v"]))))
        for edge in source["edges"]
    }
    edges = tuple(sorted(unordered, key=lambda edge: (edge[1], edge[0])))
    assert order == 130 and len(edges) == len(unordered) == 195
    assert all(left != right for left, right in edges)
    degrees = Counter(vertex for edge in edges for vertex in edge)
    assert len(degrees) == order and set(degrees.values()) == {3}
    return order, edges


def labels_from_masks(masks, length):
    labels = []
    for local in range(length):
        choices = [
            coordinate for coordinate, mask in enumerate(masks)
            if int(mask) >> local & 1
        ]
        assert len(choices) == 1
        labels.append(choices[0])
    assert Counter(labels) == {0: 64, 1: 64, 2: 64}
    return tuple(labels)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-cyclic-five",
        action="store_true",
        help="skip compilation and exhaustive cyclic-cut audit",
    )
    args = parser.parse_args()

    witness = json.loads(
        (HERE / "WITNESS.json").read_text(encoding="utf-8")
    )
    order, edges = load_graph()
    root = int(witness["root"])
    spokes = tuple(
        edge for edge, endpoints in enumerate(edges) if root in endpoints
    )
    internal = tuple(
        edge for edge, endpoints in enumerate(edges)
        if root not in endpoints
    )
    assert spokes == (4, 39, 70) and len(internal) == 192
    labels = labels_from_masks(witness["omitted_masks"], len(internal))
    exchanges = tuple(
        tuple(map(int, exchange))
        for exchange in witness["cube_exchanges_local_positions"]
    )
    assert exchanges == ((0, 102), (41, 153), (178, 78))
    assert len(set(position for pair in exchanges for position in pair)) == 6
    assert tuple(
        (labels[first], labels[second])
        for first, second in exchanges
    ) == ((0, 1), (1, 2), (0, 1))

    assert semantics.graph_girth(order, edges) == 10
    assert semantics.connected(order, edges)
    for first in range(-1, len(edges)):
        for second in range(first + 1, len(edges)):
            deleted = frozenset(
                edge for edge in (first, second) if edge >= 0
            )
            assert semantics.connected(order, edges, deleted)

    state_cache = {}

    def state_data(state_labels):
        state_labels = tuple(state_labels)
        if state_labels in state_cache:
            return state_cache[state_labels]
        trees = semantics.build_trees(
            order, edges, internal, spokes, state_labels
        )
        kernels, profile, flags = semantics.evaluate(
            order, edges, trees
        )
        result = {
            "trees": trees,
            "kernels": kernels,
            "kernel_sizes": tuple(map(len, kernels)),
            "profile": profile,
            "flags": flags,
            "psi": (min(profile), sum(map(len, kernels))),
        }
        state_cache[state_labels] = result
        return result

    cube = {}
    for subset_mask in range(8):
        state_labels = labels
        for index, exchange in enumerate(exchanges):
            if subset_mask >> index & 1:
                state_labels = apply_exchange(state_labels, exchange)
        cube[subset_mask] = state_data(state_labels)
        expected = EXPECTED_CUBE[subset_mask]
        assert (
            cube[subset_mask]["kernel_sizes"],
            cube[subset_mask]["profile"],
            cube[subset_mask]["flags"],
            cube[subset_mask]["psi"],
        ) == expected

    seed_psi = cube[0]["psi"]
    assert all(
        cube[subset]["flags"] == 0
        and not cube[subset]["psi"] < seed_psi
        for subset in range(7)
    )
    assert cube[7]["flags"] > 0 or cube[7]["psi"] < seed_psi
    assert cube[1]["kernels"] == cube[0]["kernels"]
    assert cube[3]["psi"] == seed_psi

    path_circuits = []
    current = labels
    for exchange, expected_sides in zip(
        exchanges, EXPECTED_PATH_CIRCUITS
    ):
        current_data = state_data(current)
        first, second = exchange
        first_coordinate = current[first]
        second_coordinate = current[second]
        sides = []
        for coordinate, inserted_local, removed_local in (
            (first_coordinate, first, second),
            (second_coordinate, second, first),
        ):
            inserted = internal[inserted_local]
            removed = internal[removed_local]
            circuit = semantics.fundamental_cycle(
                order,
                edges,
                current_data["trees"][coordinate],
                inserted,
            )
            assert removed in circuit
            degree = Counter(
                vertex for edge in circuit for vertex in edges[edge]
            )
            assert set(degree.values()) == {2}
            sides.append(
                (
                    coordinate,
                    len(circuit),
                    removed in current_data["kernels"][coordinate],
                    len(circuit & current_data["kernels"][coordinate]),
                )
            )
        assert tuple(sides) == expected_sides
        path_circuits.append(tuple(sides))
        current = apply_exchange(current, exchange)
    assert current in state_cache
    assert min(
        side[1] for exchange in path_circuits for side in exchange
    ) == 10

    candidates = 0
    legal = 0
    equal = 0
    for first_coordinate, second_coordinate in combinations(range(3), 2):
        for first, first_label in enumerate(labels):
            if first_label != first_coordinate:
                continue
            for second, second_label in enumerate(labels):
                if second_label != second_coordinate:
                    continue
                candidates += 1
                changed = apply_exchange(labels, (first, second))
                try:
                    data = state_data(changed)
                except AssertionError:
                    continue
                legal += 1
                assert data["flags"] == 0
                assert not data["psi"] < seed_psi
                equal += data["psi"] == seed_psi
    assert candidates == 12288
    assert legal == 382 and equal == 90

    outside_path = tuple(
        tuple(map(int, exchange))
        for exchange in witness["outside_cube_distance_two_escape"]
    )
    outside = labels
    for exchange in outside_path:
        outside = apply_exchange(outside, exchange)
        state_data(outside)
    outside_data = state_data(outside)
    assert outside_data["kernel_sizes"] == (72, 69, 68)
    assert outside_data["profile"] == (24, 20, 14, 24, 16, 14, 2)
    assert outside_data["flags"] == 0
    assert outside_data["psi"] == (2, 209) < seed_psi

    cyclic_five = "not requested"
    if not args.skip_cyclic_five:
        with tempfile.TemporaryDirectory(
            prefix="fivecdc-cyclic5-"
        ) as temp_name:
            executable = Path(temp_name) / "check_cyclic5"
            subprocess.run(
                [
                    os.environ.get("CXX", "c++"),
                    "-O3",
                    "-std=c++20",
                    str(HERE / "check_cyclic5.cpp"),
                    "-o",
                    str(executable),
                ],
                check=True,
            )
            completed = subprocess.run(
                [str(executable), str(GRAPH_PATH)],
                text=True,
                capture_output=True,
                check=True,
            )
            expected = (
                "PASS triples=1216865 three_edge_cuts=130 "
                "cyclic_three_edge_cuts=0 bridge_occurrences=75660 "
                "distinct_four_edge_cuts=25155 "
                "cyclic_four_edge_cuts=0\n"
            )
            assert completed.stdout == expected
            cyclic_five = "PASS"

    print("PASS: girth-10 proper-subset-safe three-way cube")
    print("  graph: simple cubic, 3-edge-connected, girth 10")
    print(f"  cyclically 5-edge-connected audit: {cyclic_five}")
    print("  cube: all 8 states legal; 7 proper subsets nonterminal")
    print("  full triple: Psi (2,210) -> (2,209)")
    print("  path circuit lengths: ((32,10),(29,11),(11,16))")
    print("  seed augmented-trap neighbourhood: 12,288/382/90")
    print("  global distance-two escape outside cube: verified")


if __name__ == "__main__":
    main()
