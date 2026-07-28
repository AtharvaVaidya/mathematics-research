#!/usr/bin/env python3
"""Exact finite audit for the four-cycle Fourier and code no-go note."""

from __future__ import annotations

from itertools import combinations, product
import json


A = tuple(value for value in range(16) if value.bit_count() in (1, 2))


def character_transform(point: int) -> int:
    return sum(
        -1 if (point & allowed).bit_count() & 1 else 1
        for allowed in A
    )


def simplex_has_witness() -> bool:
    nonzero = tuple(range(1, 8))
    for images in product(range(16), repeat=3):
        valid = True
        for point in nonzero:
            image = 0
            for bit in range(3):
                if (point >> bit) & 1:
                    image ^= images[bit]
            if image not in A:
                valid = False
                break
        if valid:
            return True
    return False


def cayley_adjacency() -> list[set[int]]:
    return [
        {
            other
            for other in range(16)
            if other != vertex and (other ^ vertex) in A
        }
        for vertex in range(16)
    ]


def clique_number(adjacency: list[set[int]]) -> int:
    best = 0

    def visit(clique: tuple[int, ...], candidates: set[int]) -> None:
        nonlocal best
        best = max(best, len(clique))
        if len(clique) + len(candidates) <= best:
            return
        while candidates:
            vertex = min(candidates)
            candidates.remove(vertex)
            visit(
                clique + (vertex,),
                candidates & adjacency[vertex],
            )

    visit((), set(range(len(adjacency))))
    return best


def direct_simplex_count() -> int:
    codewords = []
    for functional in range(8):
        codewords.append(
            tuple(
                (functional & point).bit_count() & 1
                for point in range(1, 8)
            )
        )
    count = 0
    for rows in product(codewords, repeat=4):
        if all(
            sum(rows[bit][edge] << bit for bit in range(4)) in A
            for edge in range(7)
        ):
            count += 1
    return count


def main() -> None:
    transform = {
        weight: sorted(
            {
                character_transform(point)
                for point in range(16)
                if point.bit_count() == weight
            }
        )
        for weight in range(5)
    }
    assert transform == {
        0: [10],
        1: [2],
        2: [-2],
        3: [-2],
        4: [2],
    }
    for point in range(16):
        quadratic = sum(
            ((point >> first) & 1) * ((point >> second) & 1)
            for first, second in combinations(range(4), 2)
        ) & 1
        expected = 10 if point == 0 else 2 * (-1 if quadratic else 1)
        assert character_transform(point) == expected

    assert not simplex_has_witness()
    assert direct_simplex_count() == 0
    adjacency = cayley_adjacency()
    maximum_clique = clique_number(adjacency)
    assert maximum_clique == 5
    assert all(
        (left ^ right) in A
        for left, right in combinations((0, 1, 2, 4, 8), 2)
    )

    print(
        json.dumps(
            {
                "allowed_values": list(A),
                "fourier_by_weight": transform,
                "quadratic_sign_identity": "PASS",
                "simplex_length": 7,
                "simplex_direct_witness_count": 0,
                "simplex_linear_map_exhaustion": "UNSAT",
                "cayley_vertices": 16,
                "cayley_clique_number": maximum_clique,
                "K6_cographic_witness": "UNSAT",
                "standard_five_cdc_counterexample": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
