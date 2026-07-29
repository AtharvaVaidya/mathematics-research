#!/usr/bin/env python3
"""Matching-universal common-robust search on the cyclic-4 census.

One incremental SAT instance is built per macro graph.  Junction variables
activate the appropriate local constraints under assumptions, allowing all
automorphism-reduced junction sets for that graph to share learned clauses.

UNSAT means only that the stronger all-connector-pairs ansatz fails.
It is not macro UNSAT and not a FiveCDC counterexample.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product
from multiprocessing import get_context
import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DUADS = frozenset((3, 5, 6, 9, 10, 12, 17, 18, 20, 24))
NEGATIVE_A = (
    (3, 3, 3, 3, 3, 3),
    (3, 3, 5, 5, 3, 3),
    (3, 3, 12, 12, 3, 3),
    (3, 12, 3, 12, 3, 3),
    (3, 12, 5, 10, 3, 3),
    (3, 12, 12, 3, 3, 3),
)
NEGATIVE_B = (
    (3, 5, 3, 6, 5, 6),
    (3, 5, 3, 6, 6, 5),
    (3, 5, 5, 6, 3, 6),
    (3, 5, 5, 6, 6, 3),
    (3, 5, 6, 3, 5, 6),
    (3, 5, 6, 3, 6, 5),
    (3, 5, 6, 5, 3, 6),
    (3, 5, 6, 5, 6, 3),
    (3, 5, 9, 10, 3, 6),
    (3, 5, 9, 10, 6, 3),
    (3, 5, 9, 12, 5, 6),
    (3, 5, 9, 12, 6, 5),
    (3, 5, 10, 9, 3, 6),
    (3, 5, 10, 9, 6, 3),
    (3, 5, 12, 9, 5, 6),
    (3, 5, 12, 9, 6, 5),
)
LOCAL_ACTIONS = tuple(sorted({
    left + right
    for swap in (False, True)
    for first in permutations((0, 1, 2))
    for second in permutations((3, 4, 5))
    for left, right in [((second, first) if swap else (first, second))]
}))


def coordinate_image(mask, action):
    answer = 0
    for coordinate in range(5):
        if mask & (1 << coordinate):
            answer |= 1 << action[coordinate]
    return answer


def coordinate_closure(representatives):
    return frozenset(
        tuple(coordinate_image(label, action) for label in word)
        for word in representatives
        for action in permutations(range(5))
    )


FORBIDDEN = (
    coordinate_closure(NEGATIVE_A),
    coordinate_closure(NEGATIVE_B),
)
COMMON_UNSAFE = tuple(sorted({
    tuple(word[action[position]] for position in range(6))
    for relation in FORBIDDEN
    for word in relation
    for action in LOCAL_ACTIONS
}))
COMMON_UNSAFE_SET = frozenset(COMMON_UNSAFE)


def decode_graph6(record):
    vertices = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, tuple(edges)


def incidence(vertices, edges):
    rows = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(sorted(row)) for row in rows)


def parity_forbidding_clauses(variables):
    """CNF clauses forbidding odd parity assignments."""

    clauses = []
    for bits in product((0, 1), repeat=len(variables)):
        if sum(bits) % 2 == 0:
            continue
        clauses.append([
            -variable if bit else variable
            for variable, bit in zip(variables, bits, strict=True)
        ])
    return clauses


def common_robust(word):
    return (
        len(word) == 6
        and all(label in DUADS for label in word)
        and word[0] ^ word[1] ^ word[2]
        ^ word[3] ^ word[4] ^ word[5] == 0
        and tuple(word) not in COMMON_UNSAFE_SET
    )


def solve_graph(task):
    import pycryptosat

    order, graph = task
    graph_index = graph["graph_index"]
    graph6 = graph["graph6"]
    junction_rows = [
        tuple(row) for row in graph["junction_representatives"]
    ]
    vertices, edges = decode_graph6(graph6)
    rows = incidence(vertices, edges)
    edge_variable_count = 5 * len(edges)

    def edge_variable(edge, coordinate):
        return 5 * edge + coordinate + 1

    def junction_variable(vertex):
        return edge_variable_count + vertex + 1

    solver = pycryptosat.Solver()
    for edge in range(len(edges)):
        variables = [edge_variable(edge, c) for c in range(5)]
        for triple in combinations(variables, 3):
            solver.add_clause([-entry for entry in triple])
        for four in combinations(variables, 4):
            solver.add_clause(list(four))

    # Sound global S5 symmetry break: the first duad can be renamed {0,1}.
    for coordinate in range(5):
        solver.add_clause([
            edge_variable(0, coordinate)
            if coordinate < 2
            else -edge_variable(0, coordinate)
        ])

    for vertex in range(vertices):
        activation = -junction_variable(vertex)
        for coordinate in range(5):
            variables = [
                edge_variable(edge, coordinate)
                for edge in rows[vertex]
            ]
            for clause in parity_forbidding_clauses(variables):
                solver.add_clause([activation, *clause])

    for first, second in combinations(range(vertices), 2):
        activations = [
            junction_variable(first),
            junction_variable(second),
        ]
        order_edges = rows[first] + rows[second]
        for coordinate in range(5):
            variables = [
                edge_variable(edge, coordinate)
                for edge in order_edges
            ]
            for clause in parity_forbidding_clauses(variables):
                solver.add_clause([*activations, *clause])
        for word in COMMON_UNSAFE:
            clause = list(activations)
            for edge, label in zip(order_edges, word, strict=True):
                clause.extend(
                    -edge_variable(edge, coordinate)
                    for coordinate in range(5)
                    if label & (1 << coordinate)
                )
            solver.add_clause(clause)

    witnesses = []
    failures = []
    for junctions in junction_rows:
        junction_set = set(junctions)
        assumptions = [
            junction_variable(vertex)
            if vertex in junction_set
            else -junction_variable(vertex)
            for vertex in range(vertices)
        ]
        sat, model = solver.solve(assumptions)
        base = {
            "order": order,
            "graph_index": graph_index,
            "graph6": graph6,
            "girth": graph["girth"],
            "junctions": list(junctions),
            "connector_count": vertices - len(junctions),
        }
        if not sat:
            failures.append(base)
            continue
        labels = tuple(
            sum(
                1 << coordinate
                for coordinate in range(5)
                if model[edge_variable(edge, coordinate)]
            )
            for edge in range(len(edges))
        )
        if any(label not in DUADS for label in labels):
            raise AssertionError("model has a non-duad macro edge")
        for junction in junctions:
            row = rows[junction]
            if labels[row[0]] ^ labels[row[1]] ^ labels[row[2]]:
                raise AssertionError("model violates junction parity")
        connectors = tuple(
            vertex
            for vertex in range(vertices)
            if vertex not in junction_set
        )
        for first, second in combinations(connectors, 2):
            word = tuple(
                labels[edge] for edge in rows[first] + rows[second]
            )
            if not common_robust(word):
                raise AssertionError("model violates common robust relation")
        base["edge_labels"] = list(labels)
        witnesses.append(base)
    return {
        "order": order,
        "graph_index": graph_index,
        "graph6": graph6,
        "girth": graph["girth"],
        "junction_orbits": len(junction_rows),
        "witnesses": witnesses,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--orders",
        type=int,
        nargs="*",
        default=[6, 8, 10, 12, 14],
    )
    arguments = parser.parse_args()
    if (
        len(LOCAL_ACTIONS),
        len(FORBIDDEN[0]),
        len(FORBIDDEN[1]),
        len(COMMON_UNSAFE),
    ) != (72, 280, 1440, 10540):
        raise AssertionError("frozen local relations changed")
    census = json.loads(
        (HERE / "census-report.json").read_text(encoding="ascii")
    )
    tasks = [
        (order, graph)
        for order in arguments.orders
        for graph in census["orders"][str(order)]["graphs"]
    ]
    if arguments.workers == 1:
        results = list(map(solve_graph, tasks))
    else:
        with get_context("fork").Pool(arguments.workers) as pool:
            results = list(pool.imap_unordered(
                solve_graph, tasks, chunksize=1
            ))
    results.sort(key=lambda row: (row["order"], row["graph_index"]))
    witnesses = [
        record
        for result in results
        for record in result["witnesses"]
    ]
    failures = [
        record
        for result in results
        for record in result["failures"]
    ]
    by_order = {}
    for order in arguments.orders:
        local_witnesses = [
            record for record in witnesses if record["order"] == order
        ]
        local_failures = [
            record for record in failures if record["order"] == order
        ]
        by_order[str(order)] = {
            "witnesses": len(local_witnesses),
            "ansatz_failures_not_macro_unsat": len(local_failures),
            "girth_at_least_5_witnesses": sum(
                record["girth"] >= 5 for record in local_witnesses
            ),
            "girth_at_least_5_failures": sum(
                record["girth"] >= 5 for record in local_failures
            ),
        }
    report = {
        "schema": "cyclic4-hybrid-matching-universal-through14-v1",
        "scope": (
            "cyclically-4 connected simple cubic macro graphs; independent "
            "positive-even junction sets; common robust all-pairs ansatz"
        ),
        "warning": (
            "ansatz UNSAT is not fixed-matching macro UNSAT and not target "
            "FiveCDC UNSAT"
        ),
        "local_relation_counts": {
            "atom_A_negative_ordered_words": len(FORBIDDEN[0]),
            "atom_B_negative_ordered_words": len(FORBIDDEN[1]),
            "local_port_actions": len(LOCAL_ACTIONS),
            "common_robust_unsafe_ordered_words": len(COMMON_UNSAFE),
        },
        "orders": by_order,
        "graph_results": results,
        "universal_witnesses": witnesses,
        "ansatz_failures": failures,
        "statuses": dict(Counter(
            ["matching_universal_safe_sat"] * len(witnesses)
            + [
                "matching_universal_ansatz_unsat_not_macro_unsat"
            ] * len(failures)
        )),
    }
    (HERE / "universal-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(json.dumps({
        "orders": by_order,
        "statuses": report["statuses"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
