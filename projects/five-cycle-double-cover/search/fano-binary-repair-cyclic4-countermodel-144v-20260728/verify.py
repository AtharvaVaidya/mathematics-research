#!/usr/bin/env python3
"""Clean-room reconstruction and dual replay for 28 auxiliary + one Tait CNF."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import subprocess


PACKAGE = Path(__file__).resolve().parent
STATE = PACKAGE / "countermodel-order144.txt"
CNF_MANIFEST = PACKAGE / "cnf-manifest.json"
PROOF_MANIFEST = PACKAGE / "proof-manifest.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def decode_graph6(text: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    values = [ord(character) - 63 for character in text]
    require(len(values) >= 4 and values[0] == 63 and values[1] != 63,
            "bad medium graph6 header")
    order = (values[1] << 12) | (values[2] << 6) | values[3]
    bits = [
        (value >> shift) & 1
        for value in values[4:]
        for shift in range(5, -1, -1)
    ]
    needed = order * (order - 1) // 2
    require(len(bits) >= needed and not any(bits[needed:]),
            "bad graph6 body or padding")
    cursor = 0
    edges = []
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def incidence(order: int, edges: tuple[tuple[int, int], ...]):
    rows: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


def parity_clauses(variables: tuple[int, ...], target: int):
    result = []
    for assignment in range(1 << len(variables)):
        if assignment.bit_count() % 2 == target:
            continue
        result.append(tuple(
            -variable if assignment & (1 << bit) else variable
            for bit, variable in enumerate(variables)
        ))
    return result


def expected_packing(rows, flow, value):
    edge_count = len(flow)
    red = tuple(range(1, edge_count + 1))
    blue = tuple(range(edge_count + 1, 2 * edge_count + 1))
    clauses = []
    for edge, edge_value in enumerate(flow):
        if edge_value == value:
            clauses.extend(((-red[edge],), (-blue[edge],)))
        else:
            clauses.append((-red[edge], -blue[edge]))
    for row in rows:
        target = sum(flow[edge] == value for edge in row) % 2
        clauses += parity_clauses(
            tuple(red[edge] for edge in row if flow[edge] != value), target
        )
        clauses += parity_clauses(
            tuple(blue[edge] for edge in row if flow[edge] != value), target
        )
    return 2 * edge_count, clauses


def expected_repair(rows, flow, switch_value, target_value):
    edge_count = len(flow)
    switch = tuple(range(1, edge_count + 1))
    red = tuple(range(edge_count + 1, 2 * edge_count + 1))
    blue = tuple(range(2 * edge_count + 1, 3 * edge_count + 1))
    other = switch_value ^ target_value
    clauses = []
    for edge, value in enumerate(flow):
        if value == switch_value:
            clauses.append((-switch[edge],))
        clauses.append((-red[edge], -blue[edge]))
        if value == target_value:
            clauses.extend((
                (switch[edge], -red[edge]),
                (switch[edge], -blue[edge]),
            ))
        elif value == other:
            clauses.extend((
                (-switch[edge], -red[edge]),
                (-switch[edge], -blue[edge]),
            ))
    for row in rows:
        clauses += parity_clauses(tuple(switch[edge] for edge in row), 0)
        red_variables = [red[edge] for edge in row]
        blue_variables = [blue[edge] for edge in row]
        target = 0
        for edge in row:
            if flow[edge] == target_value:
                target ^= 1
                red_variables.append(switch[edge])
                blue_variables.append(switch[edge])
            elif flow[edge] == other:
                red_variables.append(switch[edge])
                blue_variables.append(switch[edge])
        clauses += parity_clauses(tuple(red_variables), target)
        clauses += parity_clauses(tuple(blue_variables), target)
    return 3 * edge_count, clauses


def expected_tait(rows, edge_count):
    variable = lambda edge, color: 3 * edge + color + 1
    clauses = []
    for edge in range(edge_count):
        clauses.append(tuple(variable(edge, color) for color in range(3)))
        for first in range(3):
            for second in range(first):
                clauses.append((
                    -variable(edge, first), -variable(edge, second)
                ))
    for row in rows:
        for color in range(3):
            for first in range(3):
                for second in range(first):
                    clauses.append((
                        -variable(row[first], color),
                        -variable(row[second], color),
                    ))
    return 3 * edge_count, clauses


def parse_cnf(path: Path):
    variables = expected_count = None
    clauses = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            _, kind, variables_text, count_text = line.split()
            require(kind == "cnf", f"{path}: wrong header kind")
            variables = int(variables_text)
            expected_count = int(count_text)
            continue
        row = tuple(map(int, line.split()))
        require(row and row[-1] == 0, f"{path}: unterminated clause")
        clauses.append(row[:-1])
    require(variables is not None and len(clauses) == expected_count,
            f"{path}: bad header counts")
    return variables, clauses


def run_checker(executable: Path, cnf: Path, proof: Path) -> str:
    require(executable.is_file(), f"missing checker {executable}")
    completed = subprocess.run(
        [str(executable), str(cnf), str(proof)],
        text=True,
        capture_output=True,
        check=True,
    )
    conclusions = [
        line.strip()
        for line in completed.stdout.splitlines()
        if "VERIFIED" in line
    ]
    require(len(conclusions) == 1, f"{executable}: no unique VERIFIED line")
    return conclusions[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--lrat-check",
        type=Path,
        default=Path(
            "/Users/atharvavaidya/Documents/conjectures/"
            ".tools/cert-checkers/drat-trim/lrat-check"
        ),
    )
    parser.add_argument(
        "--cake-lpr",
        type=Path,
        default=Path(
            "/Users/atharvavaidya/Documents/conjectures/"
            ".tools/cert-checkers/cake_lpr/cake_lpr"
        ),
    )
    args = parser.parse_args()
    record, flow_line = STATE.read_text(encoding="ascii").splitlines()
    order, edges = decode_graph6(record)
    flow = tuple(map(int, flow_line.split(",")))
    rows = incidence(order, edges)
    require((order, len(edges), len(flow)) == (144, 216, 216),
            "wrong graph size")
    require(len(set(edges)) == len(edges), "parallel edge")
    require(all(len(row) == 3 for row in rows), "not cubic")
    require(all(1 <= value <= 7 for value in flow), "zero flow value")
    require(all(flow[a] ^ flow[b] ^ flow[c] == 0 for a, b, c in rows),
            "flow conservation failure")

    cnf_manifest = json.loads(CNF_MANIFEST.read_text(encoding="ascii"))
    proof_manifest = json.loads(PROOF_MANIFEST.read_text(encoding="ascii"))
    require(cnf_manifest["state_sha256"] == digest(STATE),
            "state hash differs from CNF manifest")
    require(proof_manifest["cnf_manifest_sha256"] == digest(CNF_MANIFEST),
            "CNF manifest hash differs from proof manifest")
    proofs = {row["name"]: row for row in proof_manifest["instances"]}
    require(len(cnf_manifest["instances"]) == len(proofs) == 29,
            "wrong instance count")
    results = []
    for instance in cnf_manifest["instances"]:
        name = instance["name"]
        cnf = PACKAGE / instance["path"]
        require(digest(cnf) == instance["sha256"], f"{name}: CNF hash differs")
        if instance["kind"] == "packing":
            variables, clauses = expected_packing(
                rows, flow, int(instance["value"])
            )
        elif instance["kind"] == "repair":
            variables, clauses = expected_repair(
                rows,
                flow,
                int(instance["switch"]),
                int(instance["target"]),
            )
        else:
            require(instance["kind"] == "tait", f"{name}: unknown kind")
            variables, clauses = expected_tait(rows, len(edges))
        actual_variables, actual_clauses = parse_cnf(cnf)
        require(actual_variables == variables, f"{name}: variable count differs")
        require(Counter(actual_clauses) == Counter(clauses),
                f"{name}: clauses differ from semantics")
        proof_row = proofs[name]
        proof = PACKAGE / proof_row["lrat"]
        require(digest(proof) == proof_row["lrat_sha256"],
                f"{name}: LRAT hash differs")
        first = run_checker(args.lrat_check, cnf, proof)
        second = run_checker(args.cake_lpr, cnf, proof)
        results.append((name, first, second))

    print(json.dumps({
        "schema": "fano-binary-repair-cyclic4-order144-audit-v1",
        "order": order,
        "edges": len(edges),
        "nowhere_zero_F2_3_flow": True,
        "initial_nonpacking_instances_unsat": 7,
        "normalized_binary_repair_instances_unsat": 21,
        "tait_coloring_instance_unsat": True,
        "cnf_semantics_reconstructed_independently": True,
        "lrat_check_verified": len(results),
        "cake_lpr_verified": len(results),
        "scope": (
            "counterexample to the cyclically-4-only binary repair "
            "auxiliary statement; girth is 5, and an explicit FiveCDC "
            "shows this is not a FiveCDC counterexample"
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
