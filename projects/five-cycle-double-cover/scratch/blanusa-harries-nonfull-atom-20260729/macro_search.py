#!/usr/bin/env python3
"""Search the first simple trivalent macro network for the useful six-pole.

The macro incidence graph is K_{4,4} minus a perfect matching.  Its four
left vertices are paired into two six-pole atoms; its four right vertices
are trivalent junctions.  A port ordering is chosen independently at each
left vertex.

This is a relation-level discovery search, not a graph-level UNSAT proof.
The exact relation used here is xor-zero minus the S5 closure of the 16
negative orbit representatives listed below.
"""

from __future__ import annotations

from collections import Counter
from functools import reduce
from itertools import permutations, product
from multiprocessing import get_context
import argparse
import json
from operator import xor
from pathlib import Path


DUADS = (3, 5, 6, 9, 10, 12, 17, 18, 20, 24)
TRIANGLE = (3, 5, 6)
NEGATIVE_REPRESENTATIVES = (
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
EDGES = tuple(
    (left, right)
    for left in range(4)
    for right in range(4)
    if left != right
)


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for coordinate in range(5):
        if mask & (1 << coordinate):
            result |= 1 << permutation[coordinate]
    return result


def forbidden_words() -> frozenset[tuple[int, ...]]:
    return frozenset(
        tuple(permute_mask(label, permutation) for label in word)
        for word in NEGATIVE_REPRESENTATIVES
        for permutation in permutations(range(5))
    )


FORBIDDEN = forbidden_words()


def relation_allows(word: tuple[int, ...]) -> bool:
    return (
        len(word) == 6
        and all(label in DUADS for label in word)
        and reduce(xor, word, 0) == 0
        and word not in FORBIDDEN
    )


def proper_three_edge_colourings():
    colourings = []
    for local_permutations in product(permutations(range(3)), repeat=4):
        colouring = {}
        for left in range(4):
            neighbours = [right for right in range(4) if right != left]
            for right, colour in zip(
                neighbours, local_permutations[left], strict=True
            ):
                colouring[(left, right)] = colour
        if all(
            len({
                colouring[(left, right)]
                for left in range(4)
                if left != right
            }) == 3
            for right in range(4)
        ):
            colourings.append(colouring)
    return colourings


def all_port_orderings():
    for local_permutations in product(permutations(range(3)), repeat=4):
        yield tuple(
            tuple(
                [right for right in range(4) if right != left][index]
                for index in local_permutations[left]
            )
            for left in range(4)
        )


def atom_word(ordering, atom, labels):
    word = []
    for left in (2 * atom, 2 * atom + 1):
        word.extend(labels[(left, right)] for right in ordering[left])
    return tuple(word)


def transition_witness(ordering, colourings):
    for colouring in colourings:
        labels = {
            edge: TRIANGLE[colour]
            for edge, colour in colouring.items()
        }
        if all(
            relation_allows(atom_word(ordering, atom, labels))
            for atom in range(2)
        ):
            return labels
    return None


def full_relation_solve(ordering):
    from z3 import BitVec, Or, Solver, sat

    variables = {
        edge: BitVec(f"edge_{edge[0]}_{edge[1]}", 5)
        for edge in EDGES
    }
    solver = Solver()
    for variable in variables.values():
        solver.add(Or(*(variable == label for label in DUADS)))
    for right in range(4):
        incident = [
            variables[(left, right)]
            for left in range(4)
            if left != right
        ]
        solver.add(incident[0] ^ incident[1] ^ incident[2] == 0)
    for atom in range(2):
        atom_variables = []
        for left in (2 * atom, 2 * atom + 1):
            atom_variables.extend(
                variables[(left, right)]
                for right in ordering[left]
            )
        solver.add(reduce(xor, atom_variables) == 0)
        for word in FORBIDDEN:
            solver.add(Or(*(
                atom_variables[position] != word[position]
                for position in range(6)
            )))

    status = solver.check()
    if status != sat:
        return str(status), ordering, None
    model = solver.model()
    witness = {
        f"{left}-{right}": model[variable].as_long()
        for (left, right), variable in variables.items()
    }
    integer_labels = {
        edge: witness[f"{edge[0]}-{edge[1]}"]
        for edge in EDGES
    }
    if not all(
        reduce(
            xor,
            (
                integer_labels[(left, right)]
                for left in range(4)
                if left != right
            ),
            0,
        ) == 0
        for right in range(4)
    ):
        raise AssertionError("invalid junction witness returned by Z3")
    if not all(
        relation_allows(atom_word(ordering, atom, integer_labels))
        for atom in range(2)
    ):
        raise AssertionError("invalid atom witness returned by Z3")
    return "sat", ordering, witness


def serializable_ordering(ordering):
    return [list(row) for row in ordering]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--workers", type=int, default=1)
    arguments = parser.parse_args()

    if len(FORBIDDEN) != 1440:
        raise AssertionError("unexpected size of S5-expanded negative set")
    diagonal = {
        str(label): relation_allows((label,) * 6)
        for label in DUADS
    }
    if not all(diagonal.values()):
        raise AssertionError("the direct-pairing closure check failed")

    colourings = proper_three_edge_colourings()
    if len(colourings) != 24:
        raise AssertionError("unexpected K4,4-minus-matching colouring count")
    transition_negative = []
    transition_positive = 0
    for ordering in all_port_orderings():
        if transition_witness(ordering, colourings) is None:
            transition_negative.append(ordering)
        else:
            transition_positive += 1
    if (transition_positive, len(transition_negative)) != (400, 896):
        raise AssertionError("unexpected transition-search census")

    if arguments.workers == 1:
        results = map(full_relation_solve, transition_negative)
        results = list(results)
    else:
        # macOS defaults to spawn.  Fork is intentional here: workers only
        # consume immutable Python tuples and construct fresh Z3 contexts.
        with get_context("fork").Pool(arguments.workers) as pool:
            results = list(pool.imap_unordered(
                full_relation_solve,
                transition_negative,
                chunksize=4,
            ))
    statuses = Counter(status for status, _, _ in results)
    nonsat = [
        {
            "status": status,
            "ordering": serializable_ordering(ordering),
        }
        for status, ordering, _ in results
        if status != "sat"
    ]
    sample_status, sample_ordering, sample_witness = results[0]
    if sample_status != "sat":
        raise AssertionError("first full-relation instance was not SAT")

    report = {
        "schema": "blanusa-useful-atom-k44-macro-search-v1",
        "scope": (
            "relation-level search only; not a graph-level UNSAT claim"
        ),
        "relation": {
            "negative_s5_orbits": len(NEGATIVE_REPRESENTATIVES),
            "negative_ordered_words": len(FORBIDDEN),
            "diagonal_words_all_positive": all(diagonal.values()),
            "diagonal_word_checks": diagonal,
        },
        "macro": {
            "incidence_graph": "K4,4 minus the diagonal perfect matching",
            "atoms": [[0, 1], [2, 3]],
            "junctions": [0, 1, 2, 3],
            "edges": [list(edge) for edge in EDGES],
            "port_orderings": 6 ** 4,
            "proper_three_edge_colourings": len(colourings),
        },
        "three_label_transition_search": {
            "sat_orderings": transition_positive,
            "unsat_orderings": len(transition_negative),
            "first_unsat_ordering": serializable_ordering(
                transition_negative[0]
            ),
        },
        "full_relation_search_on_transition_unsat_orderings": {
            "statuses": dict(sorted(statuses.items())),
            "nonsat": nonsat,
            "first_sat_ordering": serializable_ordering(sample_ordering),
            "first_sat_witness": sample_witness,
        },
        "conclusion": (
            "all 1296 port orderings are satisfiable for the full relation: "
            "400 already in the three-label restriction, and the other 896 "
            "by direct full-relation witnesses"
        ),
    }
    arguments.report.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(json.dumps({
        "full_statuses": dict(statuses),
        "transition_sat": transition_positive,
        "transition_unsat": len(transition_negative),
    }, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
