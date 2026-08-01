#!/usr/bin/env python3
"""Independent exact search for two-occurrence clean/delete states.

The interaction graph has two vertices joined by m parallel edges.
The first cyclic order is fixed, and the second is enumerated modulo
rotation and reversal.  This file deliberately shares no implementation
with any earlier multi-circuit search.
"""

from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass


K = (0, 1, 2, 3)
NZ = (1, 2, 3)


def bilinear(x: int, y: int) -> int:
    """The alternating form x1*y2 + x2*y1 on F_2^2."""
    return ((x & 1) & ((y >> 1) & 1)) ^ (
        ((x >> 1) & 1) & (y & 1)
    )


def canonical_cycle(order: tuple[int, ...]) -> tuple[int, ...]:
    images = []
    n = len(order)
    for reverse in (False, True):
        current = order if not reverse else tuple(reversed(order))
        images.extend(current[i:] + current[:i] for i in range(n))
    return min(images)


def cyclic_representatives(n: int):
    """Cyclic orders of range(n), modulo dihedral action."""
    for tail in itertools.permutations(range(1, n)):
        order = (0,) + tail
        if order == canonical_cycle(order):
            yield order


def prefixes(order: tuple[int, ...], flow: tuple[int, ...]):
    value = 0
    result = {}
    used = set()
    for edge in order:
        result[edge] = value
        used.add(value)
        value ^= flow[edge]
    assert value == 0
    return result, frozenset(used)


@dataclass(frozen=True)
class FlowResult:
    flow: tuple[int, ...]
    clean: bool
    deletes: bool
    used0: frozenset[int]
    used1: frozenset[int]
    rhs: tuple[int, ...]


def classify_flow(
    order0: tuple[int, ...],
    order1: tuple[int, ...],
    flow: tuple[int, ...],
) -> FlowResult:
    assert _xor(flow) == 0
    prefix0, used0 = prefixes(order0, flow)
    prefix1, used1 = prefixes(order1, flow)
    rhs = tuple(
        bilinear(prefix0[e] ^ prefix1[e], flow[e])
        for e in range(len(flow))
    )

    # A common translation has no effect.  Fix x_0=0 and exhaust x_1.
    clean = any(
        all(bilinear(x, flow[e]) == rhs[e] for e in range(len(flow)))
        for x in K
    )
    deletes = len(used0) < 4 or len(used1) < 4
    return FlowResult(flow, clean, deletes, used0, used1, rhs)


def _xor(values) -> int:
    result = 0
    for value in values:
        result ^= value
    return result


def feasible_flows(m: int):
    for flow in itertools.product(NZ, repeat=m):
        if _xor(flow) == 0:
            yield flow


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-edges", type=int, default=4)
    parser.add_argument("--max-edges", type=int, default=9)
    args = parser.parse_args()

    fixed_counterexample = None
    universal_counterexamples = []
    for m in range(args.min_edges, args.max_edges + 1):
        order0 = tuple(range(m))
        flows = tuple(feasible_flows(m))
        orders = 0
        clean_or_delete = 0
        for order1 in cyclic_representatives(m):
            orders += 1
            has_goal = False
            sample = None
            for flow in flows:
                row = classify_flow(order0, order1, flow)
                if row.clean or row.deletes:
                    has_goal = True
                elif fixed_counterexample is None:
                    fixed_counterexample = (m, order1, row)
                    print(
                        "FIXED_FLOW_COUNTEREXAMPLE"
                        f" m={m} order1={order1} flow={row.flow}"
                        f" rhs={row.rhs}"
                        f" used0={sorted(row.used0)}"
                        f" used1={sorted(row.used1)}"
                    )
                if sample is None:
                    sample = row
                if has_goal and fixed_counterexample is not None:
                    break
            assert sample is not None
            if has_goal:
                clean_or_delete += 1
            else:
                universal_counterexamples.append((m, order1, sample))
                print(
                    "UNIVERSAL_COUNTEREXAMPLE"
                    f" m={m} order1={order1}"
                )
                break
        print(
            f"ORDER m={m} rotations={orders}"
            f" feasible_flows={len(flows)}"
            f" rotations_with_goal={clean_or_delete}"
            f" universal_counterexamples="
            f"{sum(1 for row in universal_counterexamples if row[0] == m)}"
        )
        if universal_counterexamples:
            break

    assert fixed_counterexample is not None
    if universal_counterexamples:
        raise SystemExit(1)
    print("PASS no universal two-vertex counterexample in searched range")


if __name__ == "__main__":
    main()
