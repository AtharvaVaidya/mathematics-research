#!/usr/bin/env python3
"""Exact SAT/XOR characterization of single-flow external port coverage.

Every positive solver model is checked from the graph, labels, vertex XORs,
and the two factor components.  A negative solver answer is not accepted as
a theorem unless its emitted proof is checked separately.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "d5-root-transition-sat-20260731" / "search.py"
SPEC = importlib.util.spec_from_file_location("root_transition", BASE)
assert SPEC is not None and SPEC.loader is not None
RT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RT
SPEC.loader.exec_module(RT)


# name, first factor, second factor, common physical port slot.  The ordered
# port labels are fixed to 01,02,12.  Global 3<->4 identifies the omitted
# mate of every case.
CASES = (
    ("ab-ac-same", (0, 3), (1, 3), 0),
    ("ab-ac-different", (0, 3), (1, 4), 0),
    ("ab-bc-same", (0, 3), (2, 3), 1),
    ("ab-bc-different", (0, 3), (2, 4), 1),
    ("ac-bc-same", (1, 3), (2, 3), 2),
    ("ac-bc-different", (1, 3), (2, 4), 2),
)
CASE_BY_NAME = {row[0]: row for row in CASES}


class DualFormula:
    """One abstract formula rendered both as expanded CNF and native XOR."""

    def __init__(self) -> None:
        self.names: dict[tuple[object, ...], int] = {}
        self.direct_clauses: list[tuple[int, ...]] = []
        self.xors: list[tuple[tuple[int, ...], int]] = []
        self.cnf_clauses: list[tuple[int, ...]] = []

    def var(self, *name: object) -> int:
        key = tuple(name)
        if key not in self.names:
            self.names[key] = len(self.names) + 1
        return self.names[key]

    def add(self, *literals: int) -> None:
        assert literals
        row = tuple(literals)
        self.direct_clauses.append(row)
        self.cnf_clauses.append(row)

    def add_xor(self, variables: list[int] | tuple[int, ...], rhs: int) -> None:
        variables = tuple(variables)
        assert variables and rhs in (0, 1)
        self.xors.append((variables, rhs))
        for assignment in product((0, 1), repeat=len(variables)):
            if sum(assignment) % 2 != rhs:
                self.cnf_clauses.append(tuple(
                    variable if bit == 0 else -variable
                    for variable, bit in zip(variables, assignment)
                ))

    def cnf(self) -> str:
        rows = [f"p cnf {len(self.names)} {len(self.cnf_clauses)}"]
        rows.extend(" ".join(map(str, row)) + " 0" for row in self.cnf_clauses)
        return "\n".join(rows) + "\n"

    def xcnf(self) -> str:
        constraints = len(self.direct_clauses) + len(self.xors)
        rows = [f"p cnf {len(self.names)} {constraints}"]
        rows.extend(" ".join(map(str, row)) + " 0" for row in self.direct_clauses)
        for variables, rhs in self.xors:
            # CryptoMiniSat's x-line has right-hand side true.  Negating one
            # literal toggles it, and therefore represents even parity.
            literals = list(variables)
            if rhs == 0:
                literals[0] = -literals[0]
            rows.append("x" + " ".join(map(str, literals)) + " 0")
        return "\n".join(rows) + "\n"


def build_formula(graph, z: int, root: int, case_name: str
                  ) -> tuple[DualFormula, tuple[int, int, int], tuple[tuple[int, int], ...]]:
    assert case_name in CASE_BY_NAME
    _, first_factor, second_factor, shared_slot = CASE_BY_NAME[case_name]
    rows = RT.incidence(graph)
    ports = rows[z]
    assert len(ports) == 3
    assert root not in ports and z not in graph.edges[root]
    formula = DualFormula()

    for edge in range(len(graph.edges)):
        variables = [formula.var("x", edge, coordinate) for coordinate in range(5)]
        for triple in combinations(variables, 3):
            formula.add(*(-variable for variable in triple))
        for four in combinations(variables, 4):
            formula.add(*four)

    for row in rows:
        assert len(row) == 3
        for coordinate in range(5):
            formula.add_xor(
                [formula.var("x", edge, coordinate) for edge in row], 0)

    # Every D5 vertex triple is a coordinate triangle.  S5 is transitive on
    # ordered triangles, so this is an equisatisfiable normalization.
    for port, label in zip(ports, (3, 5, 6)):  # 01, 02, 12
        for coordinate in range(5):
            variable = formula.var("x", port, coordinate)
            formula.add(variable if label >> coordinate & 1 else -variable)

    shared_port = ports[shared_slot]
    for copy, factor in enumerate((first_factor, second_factor)):
        for edge in range(len(graph.edges)):
            formula.add_xor([
                formula.var("x", edge, factor[0]),
                formula.var("x", edge, factor[1]),
                formula.var("y", copy, edge),
            ], 0)

        touching: list[list[int]] = [[] for _ in graph.edges]
        for vertex, row in enumerate(rows):
            for first, second in combinations(row, 2):
                transition = formula.var(
                    "transition", copy, vertex, first, second)
                formula.add(-transition, formula.var("y", copy, first))
                formula.add(-transition, formula.var("y", copy, second))
                touching[first].append(transition)
                touching[second].append(transition)
        for edge, variables in enumerate(touching):
            assert len(variables) == 4
            formula.add_xor(variables, int(edge in (root, shared_port)))

    m = len(graph.edges)
    assert len(formula.names) == 11 * m
    assert len(formula.cnf_clauses) == 181 * m // 3 + 15
    return formula, ports, (first_factor, second_factor)


def parse_model(output: str) -> set[int] | None:
    if "s UNSATISFIABLE" in output:
        return None
    assert "s SATISFIABLE" in output, output[-4000:]
    positive = set()
    for row in output.splitlines():
        if row.startswith("v "):
            positive.update(int(token) for token in row.split()[1:]
                            if int(token) > 0)
    return positive


def factor_component(graph, labels: tuple[int, ...], root: int,
                     factor: tuple[int, int]) -> set[int]:
    rows = RT.incidence(graph)
    mask = (1 << factor[0]) | (1 << factor[1])
    active = {edge for edge, label in enumerate(labels)
              if (label & mask).bit_count() == 1}
    assert root in active
    reached = {root}
    todo = [root]
    while todo:
        edge = todo.pop()
        for vertex in graph.edges[edge]:
            local = [other for other in rows[vertex] if other in active]
            assert len(local) == 2
            for other in local:
                if other not in reached:
                    reached.add(other)
                    todo.append(other)
    return reached


def validate_model(graph, z: int, root: int, case_name: str,
                   formula: DualFormula, positive: set[int]
                   ) -> tuple[int, ...]:
    rows = RT.incidence(graph)
    labels = tuple(sum(
        1 << coordinate for coordinate in range(5)
        if formula.names[("x", edge, coordinate)] in positive
    ) for edge in range(len(graph.edges)))
    assert all(0 < label < 32 and label.bit_count() == 2 for label in labels)
    assert all(labels[row[0]] ^ labels[row[1]] ^ labels[row[2]] == 0
               for row in rows)
    ports = rows[z]
    assert tuple(labels[port] for port in ports) == (3, 5, 6)
    _, first_factor, second_factor, shared_slot = CASE_BY_NAME[case_name]
    shared_port = ports[shared_slot]
    realized_pairs = []
    for factor in (first_factor, second_factor):
        component = factor_component(graph, labels, root, factor)
        assert shared_port in component
        mask = (1 << factor[0]) | (1 << factor[1])
        active_slots = tuple(slot for slot, port in enumerate(ports)
                             if (labels[port] & mask).bit_count() == 1)
        assert len(active_slots) == 2 and shared_slot in active_slots
        inactive_slot = next(slot for slot in range(3) if slot not in active_slots)
        assert labels[ports[inactive_slot]] & mask == 0
        realized_pairs.append(frozenset(active_slots))
    assert set.union(*(set(pair) for pair in realized_pairs)) == {0, 1, 2}
    return labels


def solve_case(graph, z: int, root: int, case_name: str, cadical: Path,
               cnf_path: Path | None, xcnf_path: Path | None,
               proof_path: Path | None, include_labels: bool) -> dict[str, object]:
    formula, ports, factors = build_formula(graph, z, root, case_name)
    remove_cnf = cnf_path is None
    if cnf_path is None:
        handle = tempfile.NamedTemporaryFile(suffix=".cnf", delete=False)
        handle.close()
        cnf_path = Path(handle.name)
    else:
        cnf_path.parent.mkdir(parents=True, exist_ok=True)
    cnf_path.write_text(formula.cnf(), encoding="ascii")
    if xcnf_path is not None:
        xcnf_path.parent.mkdir(parents=True, exist_ok=True)
        xcnf_path.write_text(formula.xcnf(), encoding="ascii")
    command = [str(cadical), "--quiet", "--checkproof=1"]
    if proof_path is not None:
        proof_path.parent.mkdir(parents=True, exist_ok=True)
        command.append("--no-binary")
    command.append(str(cnf_path))
    if proof_path is not None:
        command.append(str(proof_path))
    try:
        process = subprocess.run(command, check=False, text=True,
                                 capture_output=True)
        assert process.returncode in (10, 20), process.stderr[-4000:]
        positive = parse_model(process.stdout)
        result: dict[str, object] = {
            "case": case_name,
            "factors": [list(factor) for factor in factors],
            "ports": list(ports),
            "variables": len(formula.names),
            "cnf_clauses": len(formula.cnf_clauses),
            "native_xor_constraints": len(formula.xors),
            "cnf_sha256": hashlib.sha256(cnf_path.read_bytes()).hexdigest(),
        }
        if xcnf_path is not None:
            result["xcnf_sha256"] = hashlib.sha256(
                xcnf_path.read_bytes()).hexdigest()
        if positive is None:
            result["status"] = (
                "UNSAT_TRACE_GENERATED_NOT_INDEPENDENTLY_CHECKED"
                if proof_path is not None else "UNSAT_UNCERTIFIED")
            if proof_path is not None:
                result["proof_sha256"] = hashlib.sha256(
                    proof_path.read_bytes()).hexdigest()
            return result
        labels = validate_model(
            graph, z, root, case_name, formula, positive)
        result.update({
            "status": "SAT_MODEL_SEMANTICALLY_CHECKED",
            "labels_sha256": hashlib.sha256(bytes(labels)).hexdigest(),
        })
        if include_labels:
            result["labels"] = list(labels)
        if proof_path is not None:
            proof_path.unlink(missing_ok=True)
        return result
    finally:
        if remove_cnf:
            cnf_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--petersen-foster", action="store_true")
    source.add_argument("--graph-json", type=Path)
    source.add_argument("--graph6", type=Path)
    parser.add_argument("--row", type=int, default=0)
    parser.add_argument("--z", type=int, required=True)
    parser.add_argument("--root", type=int, required=True)
    parser.add_argument("--case", choices=tuple(CASE_BY_NAME))
    parser.add_argument("--cadical", type=Path,
                        default=Path("/opt/homebrew/bin/cadical"))
    parser.add_argument("--cnf-dir", type=Path)
    parser.add_argument("--xcnf-dir", type=Path)
    parser.add_argument("--proof-dir", type=Path)
    parser.add_argument("--include-labels", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    if arguments.petersen_foster:
        graph = RT.petersen_foster_graph()
        source_name = "Petersen--Foster"
    elif arguments.graph_json is not None:
        graph = RT.json_graph(arguments.graph_json)
        source_name = str(arguments.graph_json)
    else:
        graph = RT.graph6_file(arguments.graph6, arguments.row)
        source_name = f"{arguments.graph6} row {arguments.row}"
    assert 0 <= arguments.z < graph.n
    assert 0 <= arguments.root < len(graph.edges)
    selected_cases = (
        (CASE_BY_NAME[arguments.case],) if arguments.case else CASES)
    results = []
    for case_name, _, _, _ in selected_cases:
        stem = case_name.replace("-", "_")
        result = solve_case(
            graph, arguments.z, arguments.root, case_name, arguments.cadical,
            arguments.cnf_dir / f"{stem}.cnf" if arguments.cnf_dir else None,
            arguments.xcnf_dir / f"{stem}.xcnf" if arguments.xcnf_dir else None,
            arguments.proof_dir / f"{stem}.drat" if arguments.proof_dir else None,
            arguments.include_labels,
        )
        results.append(result)
        if result["status"] == "SAT_MODEL_SEMANTICALLY_CHECKED":
            break
    payload = {
        "schema": "d5-simultaneous-external-sat-v1",
        "source": source_name,
        "graph_sha256": RT.graph_digest(graph),
        "vertices": graph.n,
        "edges": len(graph.edges),
        "z": arguments.z,
        "root": arguments.root,
        "root_edge": list(graph.edges[arguments.root]),
        "status": (
            "SAT_SINGLE_FLOW_EXTERNAL_PORT_COVER_CHECKED"
            if any(row["status"] == "SAT_MODEL_SEMANTICALLY_CHECKED"
                   for row in results)
            else "NO_SAT_CASE_REQUIRES_SIX_INDEPENDENTLY_CHECKED_PROOFS"
        ),
        "results": results,
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output is None:
        print(text, end="")
    else:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
