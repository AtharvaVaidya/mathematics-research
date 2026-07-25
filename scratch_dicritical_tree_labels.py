#!/usr/bin/env python3
"""Enumerate small boundary blowup trees and test horizontal label constraints.

This is an exploratory falsification tool for the all-degree dicritical
ledger.  It tracks the intersection matrix and augmented-canonical labels,
then asks how many negative-determinant horizontal vertices are needed for a
nonnegative pullback of the target line at infinity.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations

import sympy as sp


@dataclass(frozen=True)
class State:
    matrix: tuple[tuple[int, ...], ...]
    canonical: tuple[int, ...]


def rooted_code(state: State) -> tuple:
    matrix = state.matrix
    adjacency = [
        [j for j, value in enumerate(row) if j != i and value]
        for i, row in enumerate(matrix)
    ]

    def encode(vertex: int, parent: int) -> tuple:
        children = sorted(
            encode(child, vertex)
            for child in adjacency[vertex]
            if child != parent
        )
        return (
            matrix[vertex][vertex],
            state.canonical[vertex],
            tuple(children),
        )

    return encode(0, -1)


def blowup_vertex(state: State, vertex: int) -> State:
    old = [list(row) for row in state.matrix]
    size = len(old)
    for row in old:
        row.append(0)
    old.append([0] * (size + 1))
    old[vertex][vertex] -= 1
    old[vertex][size] = old[size][vertex] = 1
    old[size][size] = -1
    return State(
        tuple(tuple(row) for row in old),
        state.canonical + (state.canonical[vertex] + 1,),
    )


def blowup_edge(state: State, left: int, right: int) -> State:
    old = [list(row) for row in state.matrix]
    size = len(old)
    for row in old:
        row.append(0)
    old.append([0] * (size + 1))
    old[left][left] -= 1
    old[right][right] -= 1
    old[left][right] = old[right][left] = 0
    old[left][size] = old[size][left] = 1
    old[right][size] = old[size][right] = 1
    old[size][size] = -1
    return State(
        tuple(tuple(row) for row in old),
        state.canonical
        + (state.canonical[left] + state.canonical[right],),
    )


def next_states(state: State) -> list[State]:
    result = [
        blowup_vertex(state, vertex)
        for vertex in range(len(state.matrix))
    ]
    for left in range(len(state.matrix)):
        for right in range(left + 1, len(state.matrix)):
            if state.matrix[left][right]:
                result.append(blowup_edge(state, left, right))
    unique: dict[tuple, State] = {}
    for item in result:
        unique[rooted_code(item)] = item
    return list(unique.values())


def determinant_labels(
    matrix: sp.Matrix,
    inverse: sp.Matrix | None = None,
) -> tuple[int, ...]:
    """Return the determinant labels using unimodularity.

    For a boundary tree obtained from the line at infinity,
    ``det(M)=(-1)^(n-1)`` and the signed complementary minor defining the
    label is exactly the corresponding diagonal entry of ``M^{-1}``.
    This avoids recomputing one determinant per vertex.
    """

    inverse = matrix.inv() if inverse is None else inverse
    return tuple(int(inverse[index, index]) for index in range(matrix.rows))


def feasible_horizontal_sets(
    state: State,
    maximum_horizontal: int = 8,
) -> list[tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]]:
    matrix = sp.Matrix(state.matrix)
    inverse = matrix.inv()
    labels = determinant_labels(matrix, inverse)
    candidates = [
        index
        for index, (canonical, determinant) in enumerate(
            zip(state.canonical, labels)
        )
        if canonical != 0 and determinant < 0
    ]
    results = []
    for count in range(1, min(maximum_horizontal, len(candidates)) + 1):
        for horizontal in combinations(candidates, count):
            target = sp.Matrix(
                [
                    sp.Rational(-state.canonical[index], 2)
                    if state.canonical[index] < 0
                    else 0
                    for index in horizontal
                ]
            )
            if not any(value > 0 for value in target):
                continue
            principal = inverse.extract(horizontal, horizontal)
            if principal.det() == 0:
                if principal.rank() == principal.row_join(target).rank():
                    raise NotImplementedError(
                        "consistent singular horizontal system needs "
                        "positive-cone analysis"
                    )
                continue
            degrees_vector = principal.inv() * target
            if not all(value.is_Integer and value > 0 for value in degrees_vector):
                continue
            h = sp.zeros(matrix.rows, 1)
            for index, degree in zip(horizontal, degrees_vector):
                h[index] = degree
            pullback = inverse * h
            if not all(value >= 0 and value.is_Integer for value in pullback):
                continue
            if not all(
                canonical + 2 * coefficient >= 0
                for canonical, coefficient in zip(
                    state.canonical,
                    pullback,
                )
            ):
                continue
            results.append(
                (
                    horizontal,
                    tuple(int(value) for value in degrees_vector),
                    tuple(int(value) for value in pullback),
                )
            )
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-vertices",
        type=int,
        default=9,
        help="largest boundary-tree size to inspect",
    )
    args = parser.parse_args()
    states = [State(((1,),), (-2,))]
    for size in range(1, args.max_vertices + 1):
        examples = []
        for state in states:
            feasible = feasible_horizontal_sets(state)
            if feasible:
                examples.append((state, feasible[0]))
        minimum = min(
            (
                len(horizontal)
                for _state, (horizontal, _degrees, _pullback) in examples
            ),
            default=None,
        )
        print(
            "vertices",
            size,
            "trees",
            len(states),
            "minimum negative-label horizontals",
            minimum,
        )
        if examples:
            state, witness = examples[0]
            print("  A", state.canonical)
            print("  M", state.matrix)
            print("  determinant labels", determinant_labels(sp.Matrix(state.matrix)))
            print("  witness", witness)
        expanded: dict[tuple, State] = {}
        for state in states:
            for item in next_states(state):
                expanded[rooted_code(item)] = item
        states = list(expanded.values())


if __name__ == "__main__":
    main()
