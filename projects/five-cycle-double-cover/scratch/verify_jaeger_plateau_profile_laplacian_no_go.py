#!/usr/bin/env python3
"""Check the realization-sensitive Laplacian countermodel.

The graph, state, tree, odd-kernel, and exact-profile primitives come from
the standalone radius-four verifier in the same directory.  This derived
checker adds a fresh exhaustive enumeration of the two complete reciprocal
exchange neighbourhoods and verifies their discrete defect Laplacians.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


BASE = Path(__file__).with_name(
    "verify_jaeger_plateau_escape_radius4_order40.py"
)
SPEC = importlib.util.spec_from_file_location("plateau_base", BASE)
assert SPEC is not None and SPEC.loader is not None
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

EXPECTED_PROFILE = (8, 2, 8, 8, 6, 10, 10)
EXPECTED_DEGREES = (65, 63)
EXPECTED_LAPLACIANS = (
    (-12, 140, -6, -6, 28, -40, -94),
    (-16, 134, -6, -2, 34, -58, -100),
)
EXPECTED_TOTAL_LAPLACIANS = (10, -14)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    order, edges = base.decode_graph6(base.GRAPH6)
    inc = base.incidence(order, edges)
    internal = tuple(
        edge for edge in range(len(edges)) if edge not in base.SPOKES
    )
    require(len(internal) == 57, "wrong internal-edge count")
    all_internal = (1 << len(internal)) - 1
    reconstruction_cache: dict[
        tuple[int, int, int],
        tuple[frozenset[int], ...] | None,
    ] = {}
    profile_cache: dict[tuple[int, int, int], tuple[int, ...]] = {}

    def reconstruct(
        omitted: tuple[int, int, int],
    ) -> tuple[frozenset[int], ...] | None:
        known = reconstruction_cache.get(omitted)
        if known is not None or omitted in reconstruction_cache:
            return known
        if (
            omitted[0] ^ omitted[1] ^ omitted[2] != all_internal
            or omitted[0] & omitted[1]
            or omitted[0] & omitted[2]
            or omitted[1] & omitted[2]
            or tuple(mask.bit_count() for mask in omitted) != (19, 19, 19)
        ):
            reconstruction_cache[omitted] = None
            return None
        kernels: list[frozenset[int]] = []
        for coordinate in range(3):
            tree = frozenset(
                [base.SPOKES[coordinate]]
                + [
                    edge
                    for local, edge in enumerate(internal)
                    if not ((omitted[coordinate] >> local) & 1)
                ]
            )
            if not base.is_tree(order, edges, inc, tree):
                reconstruction_cache[omitted] = None
                return None
            kernels.append(base.odd_kernel(order, edges, inc, tree))
        answer = tuple(kernels)
        reconstruction_cache[omitted] = answer
        return answer

    def profile(omitted: tuple[int, int, int]) -> tuple[int, ...]:
        known = profile_cache.get(omitted)
        if known is not None:
            return known
        kernels = reconstruct(omitted)
        require(kernels is not None, "profile requested for illegal state")
        answer = base.exact_profile(order, edges, inc, kernels)
        profile_cache[omitted] = answer
        return answer

    def neighbours(
        omitted: tuple[int, int, int],
    ) -> tuple[tuple[int, int, int], ...]:
        answer: list[tuple[int, int, int]] = []
        for first in range(3):
            for second in range(first + 1, 3):
                first_bits = omitted[first]
                while first_bits:
                    first_bit = first_bits & -first_bits
                    first_bits ^= first_bit
                    second_bits = omitted[second]
                    while second_bits:
                        second_bit = second_bits & -second_bits
                        second_bits ^= second_bit
                        changed = list(omitted)
                        toggle = first_bit | second_bit
                        changed[first] ^= toggle
                        changed[second] ^= toggle
                        candidate = tuple(changed)
                        if reconstruct(candidate) is not None:
                            answer.append(candidate)
        require(len(answer) == len(set(answer)), "duplicate neighbour")
        return tuple(answer)

    states = base.EXPECTED_PATH[:2]
    require(profile(states[0]) == EXPECTED_PROFILE, "wrong first profile")
    require(profile(states[1]) == EXPECTED_PROFILE, "wrong second profile")
    require(states[1] in neighbours(states[0]), "states are not adjacent")
    require(states[0] in neighbours(states[1]), "adjacency is not symmetric")

    observed_laplacians: list[tuple[int, ...]] = []
    observed_totals: list[int] = []
    for index, state in enumerate(states):
        adjacent = neighbours(state)
        require(
            len(adjacent) == EXPECTED_DEGREES[index],
            "wrong legal-neighbour count",
        )
        current = profile(state)
        laplacian = tuple(
            sum(profile(other)[functional] - current[functional]
                for other in adjacent)
            for functional in range(7)
        )
        total_laplacian = sum(laplacian)
        require(
            laplacian == EXPECTED_LAPLACIANS[index],
            "wrong coordinate Laplacian",
        )
        require(
            total_laplacian == EXPECTED_TOTAL_LAPLACIANS[index],
            "wrong total-defect Laplacian",
        )
        observed_laplacians.append(laplacian)
        observed_totals.append(total_laplacian)

    require(
        observed_totals[0] > 0 > observed_totals[1],
        "the total-defect Laplacian does not change sign",
    )
    print("PASS realization-sensitive plateau Laplacian no-go")
    print(f"ordered profile: {EXPECTED_PROFILE}")
    print(f"legal degrees: {EXPECTED_DEGREES}")
    print(f"coordinate Laplacians: {tuple(observed_laplacians)}")
    print(f"total-defect Laplacians: {tuple(observed_totals)}")


if __name__ == "__main__":
    main()
