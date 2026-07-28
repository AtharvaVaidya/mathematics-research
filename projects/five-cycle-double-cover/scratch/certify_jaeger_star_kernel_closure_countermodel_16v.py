#!/usr/bin/env python3
"""Emit the exact CNF for a 16-vertex kernel-closure countermodel.

The formula asks for three spanning trees in the vertex-star fibre at
vertex 13 and, after permuting the tree coordinates if necessary,

    K(T_0) intersection K(T_1) subset cl_G(K(T_2)).

Here K(T) is the unique all-vertices-odd forest contained in T.  The
encoding is intentionally independent of the C++ search program that found
the graph.  Connectivity is encoded directly by all nontrivial cut
clauses; the fixed total edge multiplicity then forces each connected
coordinate to have exactly |V|-1 edges, hence to be a spanning tree.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


GRAPH6 = "O??CA?_ceOGgH_F?AK@P?"
ORDER = 16
ROOT = 13
EDGES = (
    (0, 6), (0, 9), (0, 10),
    (1, 7), (1, 10), (1, 11),
    (2, 8), (2, 12), (2, 15),
    (3, 9), (3, 13), (3, 14),
    (4, 10), (4, 13), (4, 15),
    (5, 11), (5, 12), (5, 13),
    (6, 9), (6, 12),
    (7, 11), (7, 14),
    (8, 14), (8, 15),
)
STAR = (10, 13, 17)


class CNF:
    def __init__(self) -> None:
        self.variables = 0
        self.clauses: list[list[int]] = []

    def var(self) -> int:
        self.variables += 1
        return self.variables

    def add(self, *literals: int) -> None:
        self.clauses.append(list(literals))


def xor3(cnf: CNF, variables: tuple[int, int, int], parity: int) -> None:
    """Require the xor of three variables to equal parity."""
    for assignment in range(8):
        if assignment.bit_count() % 2 == parity:
            continue
        cnf.add(
            *(
                -variable if assignment & (1 << bit) else variable
                for bit, variable in enumerate(variables)
            )
        )


def xor4_even(cnf: CNF, variables: tuple[int, int, int, int]) -> None:
    for assignment in range(16):
        if assignment.bit_count() % 2 == 0:
            continue
        cnf.add(
            *(
                -variable if assignment & (1 << bit) else variable
                for bit, variable in enumerate(variables)
            )
        )


def incidence() -> tuple[tuple[int, int, int], ...]:
    rows: list[list[int]] = [[] for _ in range(ORDER)]
    for edge, (left, right) in enumerate(EDGES):
        rows[left].append(edge)
        rows[right].append(edge)
    assert all(len(row) == 3 for row in rows)
    return tuple(tuple(row) for row in rows)  # type: ignore[return-value]


INCIDENCE = incidence()


def build() -> tuple[
    CNF,
    list[list[int]],
    list[list[int]],
    list[int],
    list[list[int]],
]:
    cnf = CNF()
    tree = [[cnf.var() for _ in range(3)] for _ in EDGES]
    kernel = [[cnf.var() for _ in range(3)] for _ in EDGES]
    pure = [cnf.var() for _ in EDGES]
    path = [[cnf.var() for _ in EDGES] for _ in EDGES]

    # A star edge occurs in exactly one coordinate.  Every other edge
    # occurs in exactly two coordinates.
    star = set(STAR)
    for edge in range(len(EDGES)):
        a, b, c = tree[edge]
        if edge in star:
            cnf.add(a, b, c)
            cnf.add(-a, -b)
            cnf.add(-a, -c)
            cnf.add(-b, -c)
        else:
            cnf.add(a, b)
            cnf.add(a, c)
            cnf.add(b, c)
            cnf.add(-a, -b, -c)

    # Direct spanning-connectivity encoding.  It is enough to enumerate
    # vertex sets not containing the fixed anchor vertex 0.
    for coordinate in range(3):
        for subset in range(1, 1 << (ORDER - 1)):
            crossing = []
            for edge, (left, right) in enumerate(EDGES):
                left_in = left != 0 and bool(subset & (1 << (left - 1)))
                right_in = right != 0 and bool(subset & (1 << (right - 1)))
                if left_in != right_in:
                    crossing.append(tree[edge][coordinate])
            assert crossing
            cnf.clauses.append(crossing)

    # K_i is an all-vertices-odd subset of T_i.  Since T_i is a tree, this
    # subset exists uniquely and equals the odd-side forest K(T_i).
    for edge in range(len(EDGES)):
        for coordinate in range(3):
            cnf.add(-kernel[edge][coordinate], tree[edge][coordinate])
    for vertex in range(ORDER):
        for coordinate in range(3):
            xor3(
                cnf,
                tuple(
                    kernel[edge][coordinate]
                    for edge in INCIDENCE[vertex]
                ),
                1,
            )

    # pure[e] iff e belongs to K_0 intersection K_1.
    for edge in range(len(EDGES)):
        cnf.add(-pure[edge], kernel[edge][0])
        cnf.add(-pure[edge], kernel[edge][1])
        cnf.add(pure[edge], -kernel[edge][0], -kernel[edge][1])

    # Conditional paths in the forest K_2.  If pure[e] is true, the row
    # path[e,*] has boundary equal to the endpoints of e.  If it is false,
    # it has empty boundary.  Because K_2 is a forest, this is equivalent
    # to requiring the endpoints of every pure edge to be in one K_2
    # component.
    for target, (left, right) in enumerate(EDGES):
        for edge in range(len(EDGES)):
            cnf.add(-path[target][edge], kernel[edge][2])
        for vertex in range(ORDER):
            row = tuple(path[target][edge] for edge in INCIDENCE[vertex])
            if vertex == left or vertex == right:
                xor4_even(cnf, (*row, pure[target]))
            else:
                xor3(cnf, row, 0)

    return cnf, tree, kernel, pure, path


def write_dimacs(path: Path, cnf: CNF) -> None:
    comments = (
        "c jaeger-star-kernel-closure-countermodel-16v-v1",
        f"c graph6 {GRAPH6}",
        f"c root {ROOT}; star edge indices {' '.join(map(str, STAR))}",
        "c coordinates may be permuted, so coordinate 2 is the candidate "
        "closure coordinate",
        f"p cnf {cnf.variables} {len(cnf.clauses)}",
    )
    rows = (" ".join(map(str, clause)) + " 0" for clause in cnf.clauses)
    path.write_text("\n".join((*comments, *rows)) + "\n", encoding="ascii")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    arguments = parser.parse_args()
    cnf, _, _, _, _ = build()
    arguments.cnf.parent.mkdir(parents=True, exist_ok=True)
    write_dimacs(arguments.cnf, cnf)
    print(f"variables={cnf.variables}")
    print(f"clauses={len(cnf.clauses)}")
    print(f"sha256={sha256(arguments.cnf)}")


if __name__ == "__main__":
    main()
