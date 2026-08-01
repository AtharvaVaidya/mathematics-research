#!/usr/bin/env python3
"""Exact SAT synthesis for the abstract one-circuit tensor obstruction.

SAT means that a literal family of pair tensors defeats every local
GL(2,2) assignment.  UNSAT means that every tensor family on k vertices
has an assignment whose selected cross-pair graph has all degrees even.
"""

from __future__ import annotations

import argparse
import itertools
import pathlib
import subprocess


GL = tuple((0,) + image for image in itertools.permutations((1, 2, 3)))
IDENTITY = (0, 1, 2, 3)


def compose(left, right):
    return tuple(left[right[value]] for value in range(4))


def inverse(linear_map):
    return next(
        candidate
        for candidate in GL
        if compose(linear_map, candidate) == IDENTITY
        and compose(candidate, linear_map) == IDENTITY
    )


INVERSE = tuple(inverse(linear_map) for linear_map in GL)
INDEX = {linear_map: index for index, linear_map in enumerate(GL)}
RELATIVE = tuple(
    tuple(INDEX[compose(INVERSE[left_index], right)] for right in GL)
    for left_index in range(len(GL))
)


def matrix_bits(linear_map):
    """Return matrix entries (m11,m21,m12,m22), i.e. column-major."""
    return (
        linear_map[1] & 1,
        linear_map[1] >> 1 & 1,
        linear_map[2] & 1,
        linear_map[2] >> 1 & 1,
    )


class Cnf:
    def __init__(self):
        self.variable_count = 0
        self.clauses: list[tuple[int, ...]] = []

    def variable(self):
        self.variable_count += 1
        return self.variable_count

    def add(self, *literals):
        assert literals
        self.clauses.append(tuple(literals))

    def xor2(self, left, right):
        """Return a variable equivalent to left XOR right."""
        output = self.variable()
        self.add(left, right, -output)
        self.add(-left, -right, -output)
        self.add(left, -right, output)
        self.add(-left, right, output)
        return output

    def xor(self, literals):
        literals = tuple(literals)
        assert literals
        result = literals[0]
        for literal in literals[1:]:
            result = self.xor2(result, literal)
        return result

    def write(self, path):
        with path.open("w", encoding="ascii") as output:
            output.write(
                f"p cnf {self.variable_count} {len(self.clauses)}\n"
            )
            for clause in self.clauses:
                output.write(" ".join(map(str, clause)) + " 0\n")


def build_countermodel_cnf(vertex_count):
    assert 2 <= vertex_count <= 8
    edges = tuple(
        (left, right)
        for left in range(vertex_count)
        for right in range(left + 1, vertex_count)
    )
    cnf = Cnf()

    # Four coefficient bits specify an arbitrary linear functional on
    # Mat_2(F_2) for each unordered vertex pair.
    tensor = tuple(
        tuple(cnf.variable() for _entry in range(4))
        for _edge in edges
    )

    # Common left multiplication changes no relative map, so fix L_0=I.
    spin_count = 0
    for tail in itertools.product(range(6), repeat=vertex_count - 1):
        spins = (0,) + tail
        edge_values = []
        for edge_index, (left, right) in enumerate(edges):
            relative = RELATIVE[spins[left]][spins[right]]
            entries = matrix_bits(GL[relative])
            selected = [
                tensor[edge_index][entry]
                for entry in range(4)
                if entries[entry]
            ]
            edge_values.append(cnf.xor(selected))

        degree_parities = []
        for vertex in range(vertex_count):
            incident = [
                edge_values[edge_index]
                for edge_index, (left, right) in enumerate(edges)
                if vertex in (left, right)
            ]
            degree_parities.append(cnf.xor(incident))

        # Negation of the desired result for this spin assignment.
        cnf.add(*degree_parities)
        spin_count += 1

    return cnf, edges, tensor, spin_count


def parse_witness(path):
    values = {}
    status = None
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("s "):
            status = line
        elif line.startswith("v "):
            for literal in map(int, line.split()[1:]):
                if literal:
                    values[abs(literal)] = literal > 0
    return status, values


def direct_clean_assignment(vertex_count, masks):
    edges = tuple(
        (left, right)
        for left in range(vertex_count)
        for right in range(left + 1, vertex_count)
    )
    for tail in itertools.product(range(6), repeat=vertex_count - 1):
        spins = (0,) + tail
        degree = [0] * vertex_count
        for mask, (left, right) in zip(masks, edges):
            relative = GL[RELATIVE[spins[left]][spins[right]]]
            value = sum(
                (mask >> entry & 1) * bit
                for entry, bit in enumerate(matrix_bits(relative))
            ) & 1
            degree[left] ^= value
            degree[right] ^= value
        if not any(degree):
            return spins
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, nargs="+", default=[3, 4, 5])
    parser.add_argument("--solver", default="cadical")
    parser.add_argument(
        "--work",
        type=pathlib.Path,
        default=pathlib.Path("generated"),
    )
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)

    print("GL maps:", len(GL))
    print("matrix order: m11,m21,m12,m22")
    for vertex_count in args.vertices:
        cnf, edges, tensor, spin_count = build_countermodel_cnf(vertex_count)
        cnf_path = args.work / f"tensor-k{vertex_count}.cnf"
        proof_path = args.work / f"tensor-k{vertex_count}.drat"
        witness_path = args.work / f"tensor-k{vertex_count}.sol"
        cnf.write(cnf_path)
        completed = subprocess.run(
            [
                args.solver,
                "--quiet",
                "--checkproof=1",
                "-w",
                str(witness_path),
                str(cnf_path),
                str(proof_path),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        status, values = parse_witness(witness_path)
        print(
            f"k={vertex_count} edges={len(edges)} spins={spin_count} "
            f"vars={cnf.variable_count} clauses={len(cnf.clauses)} "
            f"status={status}"
        )
        if completed.returncode == 10:
            masks = []
            for coefficients in tensor:
                masks.append(
                    sum(
                        (1 << entry)
                        for entry, variable in enumerate(coefficients)
                        if values[variable]
                    )
                )
            assert direct_clean_assignment(vertex_count, masks) is None
            print("COUNTERMODEL masks:", " ".join(map(str, masks)))
            raise SystemExit(1)
        if completed.returncode != 20 or status != "s UNSATISFIABLE":
            print(completed.stdout)
            print(completed.stderr)
            raise SystemExit(
                f"solver did not certify UNSAT (return {completed.returncode})"
            )
        print(f"k={vertex_count} PASS: no tensor countermodel")


if __name__ == "__main__":
    main()
