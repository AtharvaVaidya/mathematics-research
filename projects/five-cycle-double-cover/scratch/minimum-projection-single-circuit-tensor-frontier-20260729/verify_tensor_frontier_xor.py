#!/usr/bin/env python3
"""Independent native-XOR synthesis for the six-vertex tensor frontier.

The ordinary-CNF checker in ``verify_tensor_frontier.py`` is the
certificate-producing reference.  This companion emits the same exact
negation using CryptoMiniSat's extended-DIMACS XOR rows.  A SAT answer is
decoded and rejected unless direct enumeration independently confirms
that the returned tensor family has no clean spin assignment.
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
    for left_index, _left in enumerate(GL)
)


def matrix_bits(linear_map):
    """Return (m11,m21,m12,m22), i.e. the two columns in order."""
    return (
        linear_map[1] & 1,
        linear_map[1] >> 1 & 1,
        linear_map[2] & 1,
        linear_map[2] >> 1 & 1,
    )


def edges(vertex_count):
    return tuple(
        (left, right)
        for left in range(vertex_count)
        for right in range(left + 1, vertex_count)
    )


def direct_clean_assignment(vertex_count, masks):
    edge_list = edges(vertex_count)
    for tail in itertools.product(range(6), repeat=vertex_count - 1):
        spins = (0,) + tail
        degree = [0] * vertex_count
        for mask, (left, right) in zip(masks, edge_list):
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


def support_cut_clauses(vertex_count, edge_list, tensor):
    """Force the graph of nonzero tensors to be connected and bridgeless."""
    clauses = []
    # Keep vertex zero on one fixed side to quotient complementary cuts.
    for other_members in itertools.product((0, 1), repeat=vertex_count - 1):
        selected = (1,) + other_members
        if all(selected):
            continue
        crossing = [
            edge_index
            for edge_index, (left, right) in enumerate(edge_list)
            if selected[left] != selected[right]
        ]
        all_crossing_bits = [
            variable
            for edge_index in crossing
            for variable in tensor[edge_index]
        ]
        # At least one nonzero tensor crosses the cut.
        clauses.append(tuple(all_crossing_bits))
        # If one crossing edge is nonzero, a different crossing edge is
        # nonzero too.  Hence no nonzero-support edge can be a bridge.
        for edge_index in crossing:
            other_bits = [
                variable
                for other_edge in crossing
                if other_edge != edge_index
                for variable in tensor[other_edge]
            ]
            for variable in tensor[edge_index]:
                clauses.append(tuple((-variable, *other_bits)))
    return tuple(clauses)


def write_xor_cnf(
    vertex_count,
    path,
    first_mask=None,
    support_two_edge_connected=False,
):
    edge_list = edges(vertex_count)
    tensor = tuple(
        tuple(4 * edge_index + entry + 1 for entry in range(4))
        for edge_index in range(len(edge_list))
    )
    first_auxiliary = 4 * len(edge_list) + 1
    spin_count = 6 ** (vertex_count - 1)
    # The last degree parity follows from the first n-1 because every
    # selected edge has two ends.
    auxiliary_count = spin_count * (vertex_count - 1)
    variable_count = first_auxiliary - 1 + auxiliary_count
    support_clauses = (
        support_cut_clauses(vertex_count, edge_list, tensor)
        if support_two_edge_connected
        else ()
    )
    row_count = (
        spin_count * vertex_count
        + (4 if first_mask is not None else 0)
        + len(support_clauses)
    )

    with path.open("w", encoding="ascii") as output:
        output.write(f"p cnf {variable_count} {row_count}\n")
        if first_mask is not None:
            for entry, variable in enumerate(tensor[0]):
                output.write(
                    f"{variable if first_mask >> entry & 1 else -variable} 0\n"
                )
        for clause in support_clauses:
            output.write(" ".join(map(str, clause)) + " 0\n")
        auxiliary = first_auxiliary
        for tail in itertools.product(range(6), repeat=vertex_count - 1):
            spins = (0,) + tail
            edge_coefficients = []
            for edge_index, (left, right) in enumerate(edge_list):
                relative = RELATIVE[spins[left]][spins[right]]
                bits = matrix_bits(GL[relative])
                edge_coefficients.append(
                    tuple(
                        tensor[edge_index][entry]
                        for entry, bit in enumerate(bits)
                        if bit
                    )
                )

            degree_variables = []
            for vertex in range(vertex_count - 1):
                selected = []
                for edge_index, edge in enumerate(edge_list):
                    if vertex in edge:
                        selected.extend(edge_coefficients[edge_index])
                # Extended DIMACS says an XOR row is true.  Negating the
                # auxiliary therefore encodes aux XOR selected = false.
                output.write(
                    "x"
                    + " ".join(map(str, (-auxiliary, *selected)))
                    + " 0\n"
                )
                degree_variables.append(auxiliary)
                auxiliary += 1
            output.write(" ".join(map(str, degree_variables)) + " 0\n")

    assert auxiliary == variable_count + 1
    return edge_list, tensor, spin_count, variable_count, row_count


def parse_model(stdout):
    status = None
    values = {}
    for line in stdout.splitlines():
        if line.startswith("s "):
            status = line
        elif line.startswith("v "):
            for literal in map(int, line.split()[1:]):
                if literal:
                    values[abs(literal)] = literal > 0
    return status, values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, default=6)
    parser.add_argument("--solver", default="cryptominisat5")
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--maxtime", type=int, default=0)
    parser.add_argument("--first-mask", type=int, choices=range(16))
    parser.add_argument("--support-two-edge-connected", action="store_true")
    parser.add_argument(
        "--cnf",
        type=pathlib.Path,
        default=pathlib.Path("generated/tensor-k6-xor.cnf"),
    )
    args = parser.parse_args()
    args.cnf.parent.mkdir(parents=True, exist_ok=True)

    edge_list, tensor, spin_count, variable_count, row_count = write_xor_cnf(
        args.vertices,
        args.cnf,
        args.first_mask,
        args.support_two_edge_connected,
    )
    print(
        f"k={args.vertices} edges={len(edge_list)} spins={spin_count} "
        f"vars={variable_count} rows={row_count}",
        flush=True,
    )
    command = [
        args.solver,
        "--verb",
        "0",
        "--threads",
        str(args.threads),
        "--maxmatrixrows",
        "100000",
        "--maxmatrixcols",
        "100000",
        "--autodisablegauss",
        "0",
    ]
    if args.maxtime:
        command.extend(("--maxtime", str(args.maxtime)))
    command.append(str(args.cnf))
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout, end="")
    status, values = parse_model(completed.stdout)
    if completed.returncode == 10 and status == "s SATISFIABLE":
        masks = [
            sum(
                1 << entry
                for entry, variable in enumerate(coefficients)
                if values.get(variable, False)
            )
            for coefficients in tensor
        ]
        clean = direct_clean_assignment(args.vertices, masks)
        print("COUNTERMODEL masks:", " ".join(map(str, masks)))
        print("independent clean assignment:", clean)
        if clean is not None:
            raise SystemExit("invalid SAT witness")
        print("PASS: SAT countermodel independently verified")
        return
    if completed.returncode == 20 and status == "s UNSATISFIABLE":
        print("UNSAT discovery only: rerun the ordinary-CNF checker for proof")
        return
    raise SystemExit(
        f"solver ended without a decision: return={completed.returncode} "
        f"status={status}"
    )


if __name__ == "__main__":
    main()
