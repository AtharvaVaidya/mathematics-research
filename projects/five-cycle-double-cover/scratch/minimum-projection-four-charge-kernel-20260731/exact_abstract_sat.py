#!/usr/bin/env python3
"""Exact SAT synthesis for the four-charge, two-circuit tensor model.

The first four vertices carry the same normalized source charge 1; all
remaining vertices have zero charge.  SAT means that arbitrary pair-tensor
functionals can defeat every integrable map assignment and every relative
circuit translation.  UNSAT means that every such tensor family admits a
directly clean assignment in this finite abstract model.
"""

from __future__ import annotations

import argparse
import itertools
import pathlib
import subprocess


GL = tuple((0,) + image for image in itertools.permutations((1, 2, 3)))
IDENTITY = (0, 1, 2, 3)
CANONICAL_N5_MASKS = (0, 0, 0, 0, 0, 0, 10, 0, 8, 2)


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
    return (
        linear_map[1] & 1,
        linear_map[1] >> 1 & 1,
        linear_map[2] & 1,
        linear_map[2] >> 1 & 1,
    )


def alternating(left, right):
    return ((left & 1) & (right >> 1 & 1)) ^ (
        (left >> 1 & 1) & (right & 1)
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
            output.write(f"p cnf {self.variable_count} {len(self.clauses)}\n")
            for clause in self.clauses:
                output.write(" ".join(map(str, clause)) + " 0\n")


def configurations(vertex_count):
    """Yield gauge-fixed map assignments satisfying charge integrability."""
    for tail in itertools.product(range(6), repeat=vertex_count - 1):
        spins = (0,) + tail
        if GL[spins[0]][1] ^ GL[spins[1]][1] ^ GL[spins[2]][1] ^ GL[spins[3]][1]:
            continue
        yield spins


def allowed_degree_masks(spins, vertex_count):
    masks = set()
    for translation in range(4):
        mask = 0
        for vertex in range(4):
            mask |= alternating(translation, GL[spins[vertex]][1]) << vertex
        masks.add(mask)
    return tuple(sorted(masks))


def build_countermodel_cnf(vertex_count):
    assert 4 <= vertex_count <= 8
    edges = tuple(
        (left, right)
        for left in range(vertex_count)
        for right in range(left + 1, vertex_count)
    )
    cnf = Cnf()
    tensor = tuple(
        tuple(cnf.variable() for _entry in range(4)) for _edge in edges
    )

    configuration_count = 0
    clean_target_count = 0
    for spins in configurations(vertex_count):
        edge_values = []
        for edge_index, (left, right) in enumerate(edges):
            relative = RELATIVE[spins[left]][spins[right]]
            selected = [
                tensor[edge_index][entry]
                for entry, bit in enumerate(matrix_bits(GL[relative]))
                if bit
            ]
            edge_values.append(cnf.xor(selected))

        degree_parities = []
        for vertex in range(vertex_count):
            incident = [
                edge_values[edge_index]
                for edge_index, edge in enumerate(edges)
                if vertex in edge
            ]
            degree_parities.append(cnf.xor(incident))

        # For each degree vector obtainable from a relative circuit
        # translation, require at least one vertex to disagree with it.
        for target in allowed_degree_masks(spins, vertex_count):
            cnf.add(
                *(
                    -parity if target >> vertex & 1 else parity
                    for vertex, parity in enumerate(degree_parities)
                )
            )
            clean_target_count += 1
        configuration_count += 1

    return cnf, edges, tensor, configuration_count, clean_target_count


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
    for spins in configurations(vertex_count):
        degree = 0
        for mask, (left, right) in zip(masks, edges):
            relative = GL[RELATIVE[spins[left]][spins[right]]]
            value = sum(
                (mask >> entry & 1) * bit
                for entry, bit in enumerate(matrix_bits(relative))
            ) & 1
            if value:
                degree ^= (1 << left) | (1 << right)
        if degree in allowed_degree_masks(spins, vertex_count):
            return spins, degree
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, nargs="+", default=[4, 5])
    parser.add_argument(
        "--expect-minimum",
        type=int,
        default=5,
        help="require UNSAT below this order and SAT at this order",
    )
    parser.add_argument("--solver", default="cadical")
    parser.add_argument("--work", type=pathlib.Path, default=pathlib.Path("generated"))
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)

    print("GL maps:", len(GL))
    print("matrix order: m11,m21,m12,m22")
    for vertex_count in args.vertices:
        cnf, edges, tensor, config_count, target_count = build_countermodel_cnf(
            vertex_count
        )
        cnf_path = args.work / f"four-charge-n{vertex_count}.cnf"
        proof_path = args.work / f"four-charge-n{vertex_count}.drat"
        witness_path = args.work / f"four-charge-n{vertex_count}.sol"
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
            f"n={vertex_count} edges={len(edges)} configurations={config_count} "
            f"targets={target_count} vars={cnf.variable_count} "
            f"clauses={len(cnf.clauses)} status={status}"
        )
        if completed.returncode == 10:
            masks = [
                sum(
                    1 << entry
                    for entry, variable in enumerate(coefficients)
                    if values[variable]
                )
                for coefficients in tensor
            ]
            assert direct_clean_assignment(vertex_count, masks) is None
            print("SOLVER COUNTERMODEL masks:", " ".join(map(str, masks)))
            if vertex_count == 5:
                assert direct_clean_assignment(
                    vertex_count, CANONICAL_N5_MASKS
                ) is None
                print(
                    "CANONICAL COUNTERMODEL masks:",
                    " ".join(map(str, CANONICAL_N5_MASKS)),
                )
            if vertex_count < args.expect_minimum:
                raise SystemExit("countermodel occurs below expected minimum")
            if vertex_count == args.expect_minimum:
                print(f"n={vertex_count} PASS: exact countermodel verified")
            continue
        if completed.returncode != 20 or status != "s UNSATISFIABLE":
            print(completed.stdout)
            print(completed.stderr)
            raise SystemExit(
                f"solver did not certify UNSAT (return {completed.returncode})"
            )
        if vertex_count == args.expect_minimum:
            raise SystemExit("expected countermodel order is UNSAT")
        print(f"n={vertex_count} PASS: no abstract tensor countermodel")


if __name__ == "__main__":
    main()
