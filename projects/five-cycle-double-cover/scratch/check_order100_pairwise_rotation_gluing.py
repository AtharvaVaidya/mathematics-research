#!/usr/bin/env python3
"""Glue exact row-star words across the three order-100 frontier profiles.

Each variable is a complete cyclic neighbour word for one marked factor
circuit.  For every repeated incidence cell, the fixed A-side and B-side
gap patterns must admit one common-edge bijection and endpoint orientation
whose complete two-circuit union has girth at least ten.

This is stronger than separate row/column stars and weaker than a global
girth test: a short circuit may traverse several A- and B-factor circuits.
"""

from __future__ import annotations

import functools
import itertools
import json
from pathlib import Path

import check_order100_row_star_patterns as row_kernel


ARTIFACT = Path("scratch/order100-exact-row-star-survivors.json")


def weighted_girth_at_least_ten(edges):
    """Check all circuits in a positive weighted multigraph."""
    vertex_count = 1 + max(max(u, v) for u, v, _weight in edges)
    adjacency = [[] for _ in range(vertex_count)]
    for edge_id, (u, v, weight) in enumerate(edges):
        adjacency[u].append((v, weight, edge_id))
        adjacency[v].append((u, weight, edge_id))
    for removed, (source, target, removed_weight) in enumerate(edges):
        distance = [10**9] * vertex_count
        distance[source] = 0
        queue = [(0, source)]
        while queue:
            queue.sort(reverse=True)
            value, vertex = queue.pop()
            if value != distance[vertex] or value >= 10:
                continue
            for following, weight, edge_id in adjacency[vertex]:
                if edge_id == removed:
                    continue
                candidate = value + weight
                if candidate < distance[following]:
                    distance[following] = candidate
                    queue.append((candidate, following))
        if distance[target] + removed_weight < 10:
            return False
    return True


def residual_weights(half_length: int, positions, diagonal: bool):
    """Exact residual path weights in the circuit's own cyclic order."""
    return row_kernel.fixed_a_weights(
        half_length, tuple(sorted(positions)), diagonal
    )


@functools.lru_cache(maxsize=None)
def compatible_fixed_subsets(
    x: int,
    y: int,
    diagonal: bool,
    positions_a,
    positions_b,
):
    """Return one (B-to-A bijection, orientations) witness, or ``None``."""
    positions_a = tuple(sorted(positions_a))
    positions_b = tuple(sorted(positions_b))
    if len(positions_a) != len(positions_b):
        return None
    m = len(positions_a)
    if m == 0:
        return None
    if diagonal:
        if not positions_a or positions_a[0] != 0 or positions_b[0] != 0:
            return None
    elif 0 in positions_a or 0 in positions_b:
        return None

    a_weights = residual_weights(5 + x, positions_a, diagonal)
    b_weights = residual_weights(5 + y, positions_b, diagonal)
    q_edges = [
        (2 * q, 2 * q + 1, 2 if diagonal and q == 0 else 1)
        for q in range(m)
    ]
    a_edges = [
        (
            2 * q + 1,
            2 * ((q + 1) % m),
            a_weights[q],
        )
        for q in range(m)
    ]

    if diagonal:
        bijections = (
            (0,) + tail
            for tail in itertools.permutations(range(1, m))
        )
    else:
        bijections = itertools.permutations(range(m))
    for order in bijections:
        for orientation in range(1 << m):
            b_edges = []
            for position, current in enumerate(order):
                following = order[(position + 1) % m]
                current_reverse = orientation >> current & 1
                following_reverse = orientation >> following & 1
                exit_vertex = 2 * current + (
                    0 if current_reverse else 1
                )
                entry_vertex = 2 * following + (
                    1 if following_reverse else 0
                )
                b_edges.append(
                    (exit_vertex, entry_vertex, b_weights[position])
                )
            if weighted_girth_at_least_ten(q_edges + a_edges + b_edges):
                return tuple(order), orientation
    return None


@functools.lru_cache(maxsize=None)
def all_words(own_excess: int, opposite_excesses, own_index: int, counts):
    """All cyclic neighbour words satisfying every one-sided star test."""
    opposite_excesses = tuple(opposite_excesses)
    counts = tuple(counts)
    remaining = list(counts)
    if counts[own_index] < 1:
        return ()
    remaining[own_index] -= 1
    result = []
    for tail in row_kernel.multiset_words(remaining):
        word = (own_index,) + tail
        good = True
        for opposite, multiplicity in enumerate(counts):
            if multiplicity <= 1:
                continue
            positions = tuple(
                position
                for position, label in enumerate(word)
                if label == opposite
            )
            if not row_kernel.pair_extends(
                own_excess,
                opposite_excesses[opposite],
                opposite == own_index,
                positions,
            ):
                good = False
                break
        if good:
            result.append(word)
    return tuple(result)


def solve_profile(record):
    x = tuple(record["x"])
    y = tuple(record["y"])
    matrix = tuple(tuple(row) for row in record["matrix"])
    columns = tuple(
        tuple(matrix[row][column] for row in range(8))
        for column in range(8)
    )
    domains = {}
    for row in range(8):
        domains[("A", row)] = all_words(x[row], y, row, matrix[row])
    for column in range(8):
        domains[("B", column)] = all_words(
            y[column], x, column, columns[column]
        )
    assert all(domains.values())

    constraints = {}
    witnesses = {}
    for row in range(8):
        for column in range(8):
            if matrix[row][column] <= 1:
                continue
            left_key = ("A", row)
            right_key = ("B", column)
            allowed = set()
            for left_index, left_word in enumerate(domains[left_key]):
                left_positions = tuple(
                    position
                    for position, label in enumerate(left_word)
                    if label == column
                )
                for right_index, right_word in enumerate(domains[right_key]):
                    right_positions = tuple(
                        position
                        for position, label in enumerate(right_word)
                        if label == row
                    )
                    witness = compatible_fixed_subsets(
                        x[row],
                        y[column],
                        row == column,
                        left_positions,
                        right_positions,
                    )
                    if witness is not None:
                        allowed.add((left_index, right_index))
                        witnesses[
                            (row, column, left_index, right_index)
                        ] = witness
            constraints[left_key, right_key] = allowed

    neighbours = {variable: [] for variable in domains}
    for (left, right), allowed in constraints.items():
        neighbours[left].append((right, allowed, False))
        neighbours[right].append((left, allowed, True))

    active = {
        variable: frozenset(range(len(domain)))
        for variable, domain in domains.items()
    }

    def propagate(state):
        state = dict(state)
        changed = True
        while changed:
            changed = False
            for variable, links in neighbours.items():
                for other, allowed, reversed_relation in links:
                    supported = set()
                    for value in state[variable]:
                        if any(
                            (
                                (other_value, value)
                                if reversed_relation
                                else (value, other_value)
                            )
                            in allowed
                            for other_value in state[other]
                        ):
                            supported.add(value)
                    if not supported:
                        return None
                    frozen = frozenset(supported)
                    if frozen != state[variable]:
                        state[variable] = frozen
                        changed = True
        return state

    nodes = 0

    def visit(state):
        nonlocal nodes
        nodes += 1
        state = propagate(state)
        if state is None:
            return None
        unresolved = [
            variable for variable, values in state.items() if len(values) > 1
        ]
        if not unresolved:
            return {
                variable: next(iter(values))
                for variable, values in state.items()
            }
        variable = min(unresolved, key=lambda key: len(state[key]))
        for value in sorted(state[variable]):
            following = dict(state)
            following[variable] = frozenset((value,))
            found = visit(following)
            if found is not None:
                return found
        return None

    assignment = visit(active)
    if assignment is None:
        return {
            "sat": False,
            "nodes": nodes,
            "domain_sizes": {
                f"{side}{index}": len(domain)
                for (side, index), domain in domains.items()
            },
        }
    chosen_words = {
        f"{side}{index}": domains[side, index][assignment[side, index]]
        for side, index in domains
    }
    chosen_cells = {}
    for row in range(8):
        for column in range(8):
            if matrix[row][column] <= 1:
                continue
            chosen_cells[f"{row},{column}"] = witnesses[
                (
                    row,
                    column,
                    assignment["A", row],
                    assignment["B", column],
                )
            ]
    expansion = build_expansion(
        matrix,
        domains,
        assignment,
        witnesses,
    )
    return {
        "sat": True,
        "nodes": nodes,
        "domain_sizes": {
            f"{side}{index}": len(domain)
            for (side, index), domain in domains.items()
        },
        "words": chosen_words,
        "cell_witnesses": chosen_cells,
        "first_glued_expansion": expansion,
    }


def graph_girth(vertex_count, edges):
    """Return (simplicity, connectivity, girth) for an unweighted graph."""
    pairs = [tuple(sorted(edge)) for edge in edges]
    simple = all(u != v for u, v in pairs) and len(set(pairs)) == len(pairs)
    adjacency = [[] for _ in range(vertex_count)]
    for edge_id, (u, v) in enumerate(edges):
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))
    seen = {0}
    queue = [0]
    for vertex in queue:
        for following, _edge_id in adjacency[vertex]:
            if following not in seen:
                seen.add(following)
                queue.append(following)
    girth = 10**9
    for removed, (source, target) in enumerate(edges):
        distance = [-1] * vertex_count
        distance[source] = 0
        queue = [source]
        for vertex in queue:
            if distance[vertex] + 1 >= girth:
                continue
            for following, edge_id in adjacency[vertex]:
                if edge_id == removed or distance[following] >= 0:
                    continue
                distance[following] = distance[vertex] + 1
                queue.append(following)
        if distance[target] >= 0:
            girth = min(girth, distance[target] + 1)
    return simple, len(seen) == vertex_count, None if girth == 10**9 else girth


def build_expansion(matrix, domains, assignment, witnesses):
    """Build the first globally glued marked expansion, before root pairing."""
    token_at_a = {}
    a_rotations = []
    marked = []
    token_count = 0
    chosen_a_words = {}
    chosen_b_words = {}
    for row in range(8):
        word = domains["A", row][assignment["A", row]]
        chosen_a_words[row] = word
        rotation = []
        for position in range(len(word)):
            token_at_a[row, position] = token_count
            rotation.append(token_count)
            if position == 0:
                marked.append(token_count)
            token_count += 1
        a_rotations.append(tuple(rotation))
    assert token_count == 46 and len(marked) == 8

    b_rotations = []
    twist = [None] * token_count
    for column in range(8):
        word = domains["B", column][assignment["B", column]]
        chosen_b_words[column] = word
        rotation = [None] * len(word)
        for row in range(8):
            positions_a = tuple(
                position
                for position, label in enumerate(chosen_a_words[row])
                if label == column
            )
            positions_b = tuple(
                position
                for position, label in enumerate(word)
                if label == row
            )
            if not positions_a:
                continue
            assert len(positions_a) == len(positions_b) == matrix[row][column]
            if len(positions_a) == 1:
                order, orientation = (0,), 0
            else:
                order, orientation = witnesses[
                    (
                        row,
                        column,
                        assignment["A", row],
                        assignment["B", column],
                    )
                ]
            for b_index, b_position in enumerate(positions_b):
                a_index = order[b_index]
                token = token_at_a[row, positions_a[a_index]]
                rotation[b_position] = token
                twist[token] = orientation >> a_index & 1
        assert all(token is not None for token in rotation)
        b_rotations.append(tuple(rotation))
    assert all(bit is not None for bit in twist)

    terminal_of = {
        token: 2 * token_count + index
        for index, token in enumerate(marked)
    }
    edges = []
    for token in range(token_count):
        if token in terminal_of:
            terminal = terminal_of[token]
            edges.extend(((2 * token, terminal), (terminal, 2 * token + 1)))
        else:
            edges.append((2 * token, 2 * token + 1))
    for rotation in a_rotations:
        for position, token in enumerate(rotation):
            following = rotation[(position + 1) % len(rotation)]
            edges.append((2 * token + 1, 2 * following))
    for rotation in b_rotations:
        for position, token in enumerate(rotation):
            following = rotation[(position + 1) % len(rotation)]
            edges.append(
                (
                    2 * token + (1 - twist[token]),
                    2 * following + twist[following],
                )
            )
    vertex_count = 2 * token_count + len(marked)
    simple, connected, girth = graph_girth(vertex_count, edges)
    return {
        "vertex_count": vertex_count,
        "edge_count": len(edges),
        "simple": simple,
        "connected": connected,
        "girth": girth,
        "a_rotations": a_rotations,
        "b_rotations": b_rotations,
        "twist": twist,
        "marked_tokens": marked,
    }


def main():
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert artifact["schema"] == "order100-exact-row-star-relaxation-v1"
    results = []
    for index, survivor in enumerate(artifact["survivors"]):
        result = solve_profile(survivor)
        results.append(result)
        print(
            f"profile={index} pairwise_gluing="
            f"{'SAT' if result['sat'] else 'UNSAT'} nodes={result['nodes']}"
        )
        print(f"domain_sizes={result['domain_sizes']}")
        if result["sat"]:
            print(
                "first_glued_expansion="
                f"{result['first_glued_expansion']['simple']},"
                f"{result['first_glued_expansion']['connected']},"
                f"girth={result['first_glued_expansion']['girth']}"
            )
    print("order-100 pairwise rotation gluing: PASS")
    print(f"profiles={len(results)}")
    print(f"sat={sum(result['sat'] for result in results)}")
    print(f"unsat={sum(not result['sat'] for result in results)}")
    print(
        "scope=fixed primary frontier matrices; exact pair-union gluing only; "
        "no global girth or universal-separation claim"
    )


if __name__ == "__main__":
    main()
