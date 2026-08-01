#!/usr/bin/env python3
"""Exhaustively test the bridgeless-deleted-root four-mark linkage claim.

For every connected simple cubic graph through a requested even order,
every four-edge matching S, and every unmarked edge f for which G-f is
bridgeless, test whether some binary cycle contains S, avoids f, and has
even S-parity on every circuit component.

No Tait-colourability, universal separation, or marked-cut condition is
assumed.  A witness refutes the tempting purely subcubic linkage lemma,
not the rooted theorem with its full hypotheses.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import json
import subprocess
import sys

from analyze_rooted_four_mark_batch import (
    componentwise_even,
    fundamental_cycle_basis,
    incidence,
    parse_graph6,
    solve_affine_trace,
)


def connected_after_deleting(
    order: int,
    edges: list[tuple[int, int]],
    incident: list[list[int]],
    deleted: set[int],
) -> bool:
    reached = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for edge_id in incident[vertex]:
            if edge_id in deleted:
                continue
            left, right = edges[edge_id]
            neighbour = left ^ right ^ vertex
            if neighbour not in reached:
                reached.add(neighbour)
                stack.append(neighbour)
    return len(reached) == order


def deletion_is_bridgeless(
    order: int,
    edges: list[tuple[int, int]],
    incident: list[list[int]],
    root: int,
) -> bool:
    if not connected_after_deleting(order, edges, incident, {root}):
        return False
    return all(
        connected_after_deleting(order, edges, incident, {root, edge_id})
        for edge_id in range(len(edges))
        if edge_id != root
    )


def matching(edge_ids: tuple[int, ...], edges: list[tuple[int, int]]) -> bool:
    ends: set[int] = set()
    for edge_id in edge_ids:
        left, right = edges[edge_id]
        if left in ends or right in ends:
            return False
        ends.add(left)
        ends.add(right)
    return True


def tait_colourings(
    order: int,
    edges: list[tuple[int, int]],
    incident: list[list[int]],
) -> list[tuple[int, ...]]:
    colours = [-1] * len(edges)
    used = [0] * order
    answer: list[tuple[int, ...]] = []

    # Normalize the three colours at vertex zero.
    assigned = 0
    for colour, edge_id in enumerate(incident[0]):
        left, right = edges[edge_id]
        bit = 1 << colour
        colours[edge_id] = colour
        used[left] |= bit
        used[right] |= bit
        assigned += 1

    def recurse(done: int) -> None:
        if done == len(edges):
            answer.append(tuple(colours))
            return
        best_edge = -1
        best_choices = 0
        best_size = 4
        for edge_id, colour in enumerate(colours):
            if colour != -1:
                continue
            left, right = edges[edge_id]
            choices = 0b111 & ~(used[left] | used[right])
            size = choices.bit_count()
            if not size:
                return
            if size < best_size:
                best_edge = edge_id
                best_choices = choices
                best_size = size
                if size == 1:
                    break
        left, right = edges[best_edge]
        while best_choices:
            bit = best_choices & -best_choices
            best_choices ^= bit
            colour = bit.bit_length() - 1
            colours[best_edge] = colour
            used[left] |= bit
            used[right] |= bit
            recurse(done + 1)
            used[left] ^= bit
            used[right] ^= bit
            colours[best_edge] = -1

    recurse(assigned)
    return answer


def forced_unmarked_edges(
    order: int,
    edges: list[tuple[int, int]],
    incident: list[list[int]],
    basis: list[int],
    marks: tuple[int, ...],
) -> tuple[int, int] | None:
    mark_mask = sum(1 << edge_id for edge_id in marks)
    try:
        particular, kernel = solve_affine_trace(basis, list(marks))
    except AssertionError:
        return None
    current = particular
    previous_gray = 0
    forced = (1 << len(edges)) - 1
    good = 0
    for index in range(1 << len(kernel)):
        if index:
            gray = index ^ (index >> 1)
            changed = gray ^ previous_gray
            current ^= kernel[changed.bit_length() - 1]
            previous_gray = gray
        if componentwise_even(current, mark_mask, edges, incident):
            good += 1
            forced &= current
    return good, forced & ~mark_mask


def graph_rows(geng: str, order: int):
    completed = subprocess.run(
        [geng, "-cq", "-d3", "-D3", str(order)],
        check=True,
        capture_output=True,
        text=True,
    )
    yield from (
        row
        for row in completed.stdout.splitlines()
        if row and not row.startswith(">>")
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geng", default="/opt/homebrew/bin/geng")
    parser.add_argument("--maximum-order", type=int, default=14)
    parser.add_argument(
        "--require-root-colouring",
        action="store_true",
        help="retain only roots with an all-one-colour mark colouring",
    )
    arguments = parser.parse_args()

    total_graphs = 0
    total_matchings = 0
    for order in range(8, arguments.maximum_order + 1, 2):
        order_graphs = 0
        order_matchings = 0
        for graph6 in graph_rows(arguments.geng, order):
            order_graphs += 1
            total_graphs += 1
            parsed_order, edges = parse_graph6(graph6)
            assert parsed_order == order
            incident = incidence(order, edges)
            basis = fundamental_cycle_basis(order, edges, incident)
            colourings = (
                tait_colourings(order, edges, incident)
                if arguments.require_root_colouring
                else []
            )
            if arguments.require_root_colouring and not colourings:
                continue
            admissible_roots = {
                edge_id
                for edge_id in range(len(edges))
                if deletion_is_bridgeless(
                    order, edges, incident, edge_id
                )
            }
            if not admissible_roots:
                continue
            for marks in combinations(range(len(edges)), 4):
                if not matching(marks, edges):
                    continue
                order_matchings += 1
                total_matchings += 1
                good, forced = forced_unmarked_edges(
                    order, edges, incident, basis, marks
                ) or (0, 0)
                if not good:
                    continue
                bad_roots = sorted(
                    edge_id
                    for edge_id in admissible_roots
                    if (forced >> edge_id) & 1
                    and (
                        not arguments.require_root_colouring
                        or any(
                            len({colours[mark] for mark in marks}) == 1
                            and colours[edge_id] != colours[marks[0]]
                            for colours in colourings
                        )
                    )
                )
                if bad_roots:
                    print(
                        json.dumps(
                            {
                                "classification": (
                                    "COUNTEREXAMPLE_TO_PURE_SUBCUBIC_"
                                    "ROOTED_LINKAGE_LEMMA"
                                ),
                                "graph6": graph6,
                                "order": order,
                                "marks": [edges[index] for index in marks],
                                "mark_edge_ids": marks,
                                "root": edges[bad_roots[0]],
                                "root_edge_id": bad_roots[0],
                                "componentwise_even_cycles": good,
                                "tait_colourings_mod_s3": len(colourings),
                                "root_colouring_required": (
                                    arguments.require_root_colouring
                                ),
                            },
                            sort_keys=True,
                        )
                    )
                    return
        print(
            json.dumps(
                {
                    "order": order,
                    "graphs": order_graphs,
                    "four_edge_matchings": order_matchings,
                },
                sort_keys=True,
            ),
            file=sys.stderr,
            flush=True,
        )
    print(
        json.dumps(
            {
                "classification": "NO_COUNTEREXAMPLE_IN_FINITE_SCREEN",
                "maximum_order": arguments.maximum_order,
                "graphs": total_graphs,
                "four_edge_matchings": total_matchings,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
