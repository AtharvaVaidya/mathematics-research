#!/usr/bin/env python3
"""Exact exploratory search for boundary states of simple cubic five-poles.

A five-pole is represented by a connected simple graph having exactly five
degree-2 vertices and all remaining vertices of degree 3.  One semiedge is
attached to each degree-2 vertex.  Every edge and semiedge receives one of the
ten weight-2 vectors in F_2^5, and the xor at each completed cubic vertex must
vanish.

This script is exploratory, not a proof certificate.  It uses nauty ``geng``
only to generate one representative of each unlabelled underlying graph; its
state computation is a small, self-contained constraint solver.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
import json
import subprocess
import sys
import time


D = tuple(sum(1 << color for color in pair) for pair in combinations(range(5), 2))
D_INDEX = {mask: index for index, mask in enumerate(D)}
COLOR_PERMUTATIONS = tuple(permutations(range(5)))
POSITION_PERMUTATIONS = tuple(permutations(range(5)))
FULL_DOMAIN = (1 << len(D)) - 1


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    """Parse the graph6 subset emitted by geng (including extended orders)."""
    record = record.rstrip("\r\n")
    if record.startswith(">>graph6<<"):
        record = record[len(">>graph6<<") :]
    values = [ord(char) - 63 for char in record]
    if not values or any(value < 0 or value > 63 for value in values):
        raise ValueError("invalid graph6 record")
    if values[0] != 63:
        n, offset = values[0], 1
    elif values[1] != 63:
        n = (values[1] << 12) | (values[2] << 6) | values[3]
        offset = 4
    else:
        n = 0
        for value in values[2:8]:
            n = (n << 6) | value
        offset = 8
    bit_count = n * (n - 1) // 2
    data_count = (bit_count + 5) // 6
    if len(values) != offset + data_count:
        raise ValueError("graph6 length mismatch")
    bits = [
        (value >> shift) & 1
        for value in values[offset:]
        for shift in range(5, -1, -1)
    ]
    if any(bits[bit_count:]):
        raise ValueError("nonzero graph6 padding")
    edges: list[tuple[int, int]] = []
    cursor = 0
    for v in range(1, n):
        for u in range(v):
            if bits[cursor]:
                edges.append((u, v))
            cursor += 1
    return n, tuple(edges)


@lru_cache(maxsize=None)
def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(
        1 << permutation[color]
        for color in range(5)
        if mask & (1 << color)
    )


@lru_cache(maxsize=None)
def color_orbit_representative(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(permute_mask(mask, permutation) for mask in word)
        for permutation in COLOR_PERMUTATIONS
    )


def boundary_orbit_representatives() -> tuple[tuple[int, ...], ...]:
    result = {
        color_orbit_representative((*prefix, last))
        for prefix in product(D, repeat=4)
        for last in (prefix[0] ^ prefix[1] ^ prefix[2] ^ prefix[3],)
        if last in D_INDEX
    }
    assert len(result) == 62
    return tuple(sorted(result))


@lru_cache(maxsize=None)
def allowed_tuples(arity: int, target: int) -> tuple[tuple[int, ...], ...]:
    """Tuples of label indices whose corresponding masks xor to target."""
    answer = []
    for values in product(range(len(D)), repeat=arity):
        xor = 0
        for value in values:
            xor ^= D[value]
        if xor == target:
            answer.append(values)
    return tuple(answer)


def satisfiable(
    variable_count: int,
    constraints: tuple[tuple[tuple[int, ...], int], ...],
) -> bool:
    """Decide the finite-domain CSP by arc consistency plus exact branching."""

    memo: set[tuple[int, ...]] = set()

    def propagate(domains: list[int]) -> bool:
        changed = True
        while changed:
            changed = False
            for scope, target in constraints:
                supports = [0] * len(scope)
                for values in allowed_tuples(len(scope), target):
                    if all(domains[var] & (1 << value) for var, value in zip(scope, values)):
                        for position, value in enumerate(values):
                            supports[position] |= 1 << value
                for position, var in enumerate(scope):
                    narrowed = domains[var] & supports[position]
                    if not narrowed:
                        return False
                    if narrowed != domains[var]:
                        domains[var] = narrowed
                        changed = True
        return True

    def visit(domains: list[int]) -> bool:
        if not propagate(domains):
            return False
        key = tuple(domains)
        if key in memo:
            return False
        if all(domain & (domain - 1) == 0 for domain in domains):
            return True
        var = min(
            (index for index, domain in enumerate(domains) if domain & (domain - 1)),
            key=lambda index: domains[index].bit_count(),
        )
        values = domains[var]
        while values:
            choice = values & -values
            values -= choice
            branch = domains.copy()
            branch[var] = choice
            if visit(branch):
                return True
        memo.add(key)
        return False

    return visit([FULL_DOMAIN] * variable_count)


def pole_data(
    n: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    incident: list[list[int]] = [[] for _ in range(n)]
    for edge_id, (u, v) in enumerate(edges):
        incident[u].append(edge_id)
        incident[v].append(edge_id)
    degrees = tuple(map(len, incident))
    terminals = tuple(vertex for vertex, degree in enumerate(degrees) if degree == 2)
    if len(terminals) != 5 or any(degree not in (2, 3) for degree in degrees):
        raise ValueError("not a cubic five-pole core")
    terminal_index = {vertex: index for index, vertex in enumerate(terminals)}
    scopes = tuple(tuple(row) for row in incident)
    return terminals, scopes


def gluable_core(
    n: int,
    edges: tuple[tuple[int, int], ...],
    terminals: tuple[int, ...],
) -> bool:
    """Every core bridge must have terminals on both sides.

    This is exactly the condition needed to ensure that the bridge ceases to
    be a bridge after this core is joined terminal-by-terminal to any other
    connected five-pole core.
    """
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for edge_id, (u, v) in enumerate(edges):
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))
    terminal_set = set(terminals)
    for removed_edge, (start, _) in enumerate(edges):
        visited = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for other, edge_id in adjacency[vertex]:
                if edge_id != removed_edge and other not in visited:
                    visited.add(other)
                    stack.append(other)
        if len(visited) != n:
            terminal_count = len(visited & terminal_set)
            if terminal_count in (0, 5):
                return False
    return True


def state_set(
    n: int,
    edges: tuple[tuple[int, int], ...],
    orbit_representatives: tuple[tuple[int, ...], ...],
) -> frozenset[tuple[int, ...]]:
    terminals, scopes = pole_data(n, edges)
    terminal_index = {vertex: index for index, vertex in enumerate(terminals)}
    result = set()
    for word in orbit_representatives:
        constraints = tuple(
            (scopes[vertex], word[terminal_index[vertex]] if vertex in terminal_index else 0)
            for vertex in range(n)
        )
        if satisfiable(len(edges), constraints):
            result.add(word)
    return frozenset(result)


@lru_cache(maxsize=None)
def permute_positions(
    states: frozenset[tuple[int, ...]],
    permutation: tuple[int, ...],
) -> frozenset[tuple[int, ...]]:
    return frozenset(
        color_orbit_representative(tuple(word[index] for index in permutation))
        for word in states
    )


def geng_records(geng: str, n: int):
    edge_count = (3 * n - 5) // 2
    process = subprocess.Popen(
        [geng, "-cq", "-d2", "-D3", str(n), f"{edge_count}:{edge_count}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert process.stdout is not None
    for line in process.stdout:
        if line.strip():
            yield line.strip()
    stderr = process.stderr.read() if process.stderr is not None else ""
    return_code = process.wait()
    if return_code:
        raise RuntimeError(f"geng failed with code {return_code}: {stderr}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geng", default="/opt/homebrew/bin/geng")
    parser.add_argument("--max-order", type=int, default=13)
    parser.add_argument("--jsonl")
    args = parser.parse_args()
    if args.max_order < 5 or args.max_order % 2 == 0:
        parser.error("--max-order must be odd and at least 5")

    representatives = boundary_orbit_representatives()
    unique: dict[frozenset[tuple[int, ...]], tuple[int, str]] = {}
    output = open(args.jsonl, "w", encoding="ascii") if args.jsonl else None
    started = time.monotonic()
    try:
        for n in range(5, args.max_order + 1, 2):
            order_profile: Counter[int] = Counter()
            graph_count = 0
            rejected_count = 0
            for record in geng_records(args.geng, n):
                parsed_n, edges = parse_graph6(record)
                if parsed_n != n:
                    raise AssertionError("geng returned the wrong order")
                terminals, _ = pole_data(n, edges)
                if not gluable_core(n, edges, terminals):
                    rejected_count += 1
                    continue
                states = state_set(n, edges, representatives)
                graph_count += 1
                order_profile[len(states)] += 1
                unique.setdefault(states, (n, record))
                if output is not None:
                    print(
                        json.dumps(
                            {
                                "graph6": record,
                                "order": n,
                                "state_indices": [
                                    index
                                    for index, word in enumerate(representatives)
                                    if word in states
                                ],
                            },
                            sort_keys=True,
                        ),
                        file=output,
                    )
            report = {
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "graphs": graph_count,
                "minimum_states": min(order_profile) if order_profile else None,
                "order": n,
                "profile": dict(sorted(order_profile.items())),
                "rejected_nongluable": rejected_count,
                "unique_state_sets_total": len(unique),
            }
            print(json.dumps(report, sort_keys=True), flush=True)

        unique_items = list(unique.items())
        for left_index, (left, left_witness) in enumerate(unique_items):
            for right, right_witness in unique_items[left_index:]:
                if len(left) + len(right) > len(representatives):
                    continue
                for permutation in POSITION_PERMUTATIONS:
                    if left.isdisjoint(permute_positions(right, permutation)):
                        print(
                            json.dumps(
                                {
                                    "disjoint_pair": {
                                        "left": left_witness,
                                        "left_states": len(left),
                                        "permutation": permutation,
                                        "right": right_witness,
                                        "right_states": len(right),
                                    }
                                },
                                sort_keys=True,
                            )
                        )
                        return
        print(
            json.dumps(
                {
                    "disjoint_pair": None,
                    "scope": f"all connected simple five-pole cores through order {args.max_order}",
                    "unique_state_sets": len(unique),
                },
                sort_keys=True,
            )
        )
    finally:
        if output is not None:
            output.close()


if __name__ == "__main__":
    main()
