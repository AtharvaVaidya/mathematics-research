#!/usr/bin/env python3
"""Build 7 packing and 21 binary-cycle-repair CNFs.

Each CNF is satisfiable exactly when the named positive certificate exists.
For this frozen state all 28 formulas are expected to be UNSAT.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import product
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
STATE = PACKAGE / "countermodel-order144.txt"
CNF_DIR = PACKAGE / "cnf"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    require(record.startswith("~") and not record.startswith("~~"),
            "expected an 18-bit graph6 header")
    order = 0
    for character in record[1:4]:
        value = ord(character) - 63
        require(0 <= value < 64, "invalid graph6 header")
        order = (order << 6) | value
    bits: list[int] = []
    for character in record[4:]:
        value = ord(character) - 63
        require(0 <= value < 64, "invalid graph6 payload")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    cursor = 0
    edges = []
    for right in range(1, order):
        for left in range(right):
            require(cursor < len(bits), "truncated graph6 payload")
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    require(not any(bits[cursor:]), "nonzero graph6 padding")
    return order, tuple(edges)


def incidence(order: int, edges: tuple[tuple[int, int], ...]):
    rows: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


class Formula:
    def __init__(self) -> None:
        self.variables = 0
        self.clauses: list[tuple[int, ...]] = []

    def new_variables(self, count: int) -> tuple[int, ...]:
        result = tuple(range(self.variables + 1, self.variables + count + 1))
        self.variables += count
        return result

    def add(self, *literals: int) -> None:
        require(bool(literals), "empty source clause")
        self.clauses.append(tuple(literals))

    def xor(self, variables: tuple[int, ...], target: int) -> None:
        require(len(set(variables)) == len(variables),
                "duplicate variable in XOR")
        for assignment in product((0, 1), repeat=len(variables)):
            if sum(assignment) % 2 == target:
                continue
            self.add(*(
                -variable if bit else variable
                for variable, bit in zip(variables, assignment, strict=True)
            ))

    def write(self, path: Path, comments: tuple[str, ...]) -> dict[str, object]:
        with path.open("w", encoding="ascii", newline="\n") as output:
            for comment in comments:
                output.write("c " + comment + "\n")
            output.write(f"p cnf {self.variables} {len(self.clauses)}\n")
            for row in self.clauses:
                output.write(" ".join(map(str, row)) + " 0\n")
        digest = sha256(path.read_bytes()).hexdigest()
        return {
            "path": str(path.relative_to(PACKAGE)),
            "variables": self.variables,
            "clauses": len(self.clauses),
            "sha256": digest,
        }


def packing_formula(
    rows: tuple[tuple[int, ...], ...],
    flow: tuple[int, ...],
    value: int,
) -> Formula:
    formula = Formula()
    edge_count = len(flow)
    red = formula.new_variables(edge_count)
    blue = formula.new_variables(edge_count)
    for edge, edge_value in enumerate(flow):
        if edge_value == value:
            formula.add(-red[edge])
            formula.add(-blue[edge])
        else:
            formula.add(-red[edge], -blue[edge])
    for row in rows:
        terminal_parity = sum(flow[edge] == value for edge in row) % 2
        formula.xor(
            tuple(red[edge] for edge in row if flow[edge] != value),
            terminal_parity,
        )
        formula.xor(
            tuple(blue[edge] for edge in row if flow[edge] != value),
            terminal_parity,
        )
    return formula


def repair_formula(
    rows: tuple[tuple[int, ...], ...],
    flow: tuple[int, ...],
    switch_value: int,
    target_value: int,
) -> Formula:
    formula = Formula()
    edge_count = len(flow)
    switch = formula.new_variables(edge_count)
    red = formula.new_variables(edge_count)
    blue = formula.new_variables(edge_count)
    other_target = target_value ^ switch_value
    for edge, value in enumerate(flow):
        if value == switch_value:
            formula.add(-switch[edge])
        formula.add(-red[edge], -blue[edge])
        if value == target_value:
            formula.add(switch[edge], -red[edge])
            formula.add(switch[edge], -blue[edge])
        elif value == other_target:
            formula.add(-switch[edge], -red[edge])
            formula.add(-switch[edge], -blue[edge])
    for row in rows:
        formula.xor(tuple(switch[edge] for edge in row), 0)
        red_boundary = [red[edge] for edge in row]
        blue_boundary = [blue[edge] for edge in row]
        target = 0
        for edge in row:
            if flow[edge] == target_value:
                target ^= 1
                red_boundary.append(switch[edge])
                blue_boundary.append(switch[edge])
            elif flow[edge] == other_target:
                red_boundary.append(switch[edge])
                blue_boundary.append(switch[edge])
        formula.xor(tuple(red_boundary), target)
        formula.xor(tuple(blue_boundary), target)
    return formula


def normalized_incidences() -> tuple[tuple[int, int], ...]:
    return tuple(
        (switch, target)
        for switch in range(1, 8)
        for target in range(1, 8)
        if target < (target ^ switch)
    )


def tait_formula(rows, edge_count: int) -> Formula:
    formula = Formula()
    colors = formula.new_variables(3 * edge_count)
    variable = lambda edge, color: colors[3 * edge + color]
    for edge in range(edge_count):
        formula.add(*(variable(edge, color) for color in range(3)))
        for first in range(3):
            for second in range(first):
                formula.add(
                    -variable(edge, first), -variable(edge, second)
                )
    for row in rows:
        for color in range(3):
            for first in range(3):
                for second in range(first):
                    formula.add(
                        -variable(row[first], color),
                        -variable(row[second], color),
                    )
    return formula


def main() -> None:
    record, flow_line = STATE.read_text(encoding="ascii").splitlines()
    order, edges = decode_graph6(record)
    flow = tuple(map(int, flow_line.split(",")))
    rows = incidence(order, edges)
    require((order, len(edges), len(flow)) == (144, 216, 216),
            "wrong graph size")
    require(len(set(edges)) == len(edges), "parallel edge")
    require(all(len(row) == 3 for row in rows), "not cubic")
    require(all(1 <= value <= 7 for value in flow), "zero flow")
    require(all(flow[a] ^ flow[b] ^ flow[c] == 0 for a, b, c in rows),
            "flow conservation failure")
    CNF_DIR.mkdir(exist_ok=True)
    manifest: list[dict[str, object]] = []
    for value in range(1, 8):
        name = f"packing-value-{value}"
        formula = packing_formula(rows, flow, value)
        row = formula.write(
            CNF_DIR / f"{name}.cnf",
            (
                "fano-binary-packing-v1",
                f"SAT iff flow value class {value} packs two disjoint joins",
            ),
        )
        row.update({"kind": "packing", "value": value, "name": name})
        manifest.append(row)
    for switch, target in normalized_incidences():
        name = f"repair-t{switch}-b{target}"
        formula = repair_formula(rows, flow, switch, target)
        row = formula.write(
            CNF_DIR / f"{name}.cnf",
            (
                "fano-binary-cycle-repair-v1",
                "SAT iff the named normalized incidence has a repair",
                f"switch={switch} target={target} other={target ^ switch}",
            ),
        )
        row.update({
            "kind": "repair",
            "switch": switch,
            "target": target,
            "other_target": target ^ switch,
            "name": name,
        })
        manifest.append(row)
    name = "tait-coloring"
    formula = tait_formula(rows, len(edges))
    row = formula.write(
        CNF_DIR / f"{name}.cnf",
        (
            "cubic-three-edge-coloring-v1",
            "SAT iff the graph has a Tait three-edge-coloring",
        ),
    )
    row.update({"kind": "tait", "name": name})
    manifest.append(row)
    payload = {
        "schema": "fano-binary-repair-cyclic4-order144-cnf-manifest-v1",
        "state": STATE.name,
        "state_sha256": sha256(STATE.read_bytes()).hexdigest(),
        "order": order,
        "edges": len(edges),
        "packing_instances": 7,
        "repair_instances": 21,
        "tait_instances": 1,
        "instances": manifest,
    }
    (PACKAGE / "cnf-manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
        newline="\n",
    )
    print(json.dumps({
        "instances": len(manifest),
        "variables": sum(int(row["variables"]) for row in manifest),
        "clauses": sum(int(row["clauses"]) for row in manifest),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
