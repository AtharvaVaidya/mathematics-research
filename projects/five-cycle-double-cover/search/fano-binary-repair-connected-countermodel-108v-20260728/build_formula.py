#!/usr/bin/env python3
"""Build one selector-gated CNF for all 21 binary-repair incidences."""

from __future__ import annotations

import argparse
from itertools import product
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent.parent
STATE = (
    PROJECT
    / "scratch"
    / "fano-binary-repair-connected-countermodel-order108.txt"
)


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
    bits = []
    for character in record[4:]:
        value = ord(character) - 63
        require(0 <= value < 64, "invalid graph6 data")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            require(cursor < len(bits), "truncated graph6")
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    require(not any(bits[cursor:]), "nonzero graph6 padding")
    return order, tuple(edges)


def incidence(
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], ...]:
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
        answer = tuple(range(self.variables + 1, self.variables + count + 1))
        self.variables += count
        return answer

    def add(self, clause: tuple[int, ...], selector: int | None = None) -> None:
        if selector is not None:
            clause = clause + (-selector,)
        require(clause, "empty source clause")
        self.clauses.append(clause)

    def add_xor(
        self,
        variables: tuple[int, ...],
        target: int,
        selector: int,
    ) -> None:
        require(len(set(variables)) == len(variables),
                "duplicate variable in XOR")
        for assignment in product((0, 1), repeat=len(variables)):
            if sum(assignment) % 2 == target:
                continue
            clause = tuple(
                -variable if bit else variable
                for variable, bit in zip(variables, assignment, strict=True)
            )
            self.add(clause, selector)


def representative_incidences() -> tuple[tuple[int, int], ...]:
    answer = []
    for switch_value in range(1, 8):
        seen = set()
        for target in range(1, 8):
            if target == switch_value:
                continue
            pair = tuple(sorted((target, target ^ switch_value)))
            if pair in seen:
                continue
            seen.add(pair)
            answer.append((switch_value, pair[0]))
        require(len(seen) == 3, "wrong Fano incidence count at point")
    require(len(answer) == 21, "wrong total Fano incidence count")
    return tuple(answer)


def add_repair_block(
    formula: Formula,
    rows: tuple[tuple[int, ...], ...],
    flow: tuple[int, ...],
    switch_value: int,
    target_value: int,
    selector: int,
) -> None:
    edge_count = len(flow)
    switch = formula.new_variables(edge_count)
    red = formula.new_variables(edge_count)
    blue = formula.new_variables(edge_count)

    for edge, value in enumerate(flow):
        if value == switch_value:
            formula.add((-switch[edge],), selector)
        formula.add((-red[edge], -blue[edge]), selector)
        if value == target_value:
            # m'_b = not x.
            formula.add((switch[edge], -red[edge]), selector)
            formula.add((switch[edge], -blue[edge]), selector)
        elif value == (target_value ^ switch_value):
            # m'_b = x.
            formula.add((-switch[edge], -red[edge]), selector)
            formula.add((-switch[edge], -blue[edge]), selector)

    for row in rows:
        formula.add_xor(tuple(switch[edge] for edge in row), 0, selector)
        parity_red = [red[edge] for edge in row]
        parity_blue = [blue[edge] for edge in row]
        constant = 0
        for edge in row:
            if flow[edge] == target_value:
                parity_red.append(switch[edge])
                parity_blue.append(switch[edge])
                constant ^= 1
            elif flow[edge] == (target_value ^ switch_value):
                parity_red.append(switch[edge])
                parity_blue.append(switch[edge])
        formula.add_xor(tuple(parity_red), constant, selector)
        formula.add_xor(tuple(parity_blue), constant, selector)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=PACKAGE / "all-21-binary-repairs.cnf",
    )
    args = parser.parse_args()

    record, flow_line = STATE.read_text(encoding="utf-8").splitlines()
    order, edges = decode_graph6(record)
    flow = tuple(int(item) for item in flow_line.split(","))
    rows = incidence(order, edges)
    require(order == 108 and len(edges) == 162, "wrong graph size")
    require(len(flow) == len(edges), "wrong flow length")
    require(all(len(row) == 3 for row in rows), "graph is not cubic")
    require(all(1 <= value <= 7 for value in flow), "zero flow value")
    require(
        all(flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0
            for row in rows),
        "flow conservation fails",
    )

    formula = Formula()
    incidences = representative_incidences()
    selectors = formula.new_variables(len(incidences))
    for selector, (switch_value, target_value) in zip(
        selectors, incidences, strict=True
    ):
        add_repair_block(
            formula,
            rows,
            flow,
            switch_value,
            target_value,
            selector,
        )
    formula.add(tuple(selectors))

    with args.output.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {formula.variables} {len(formula.clauses)}\n")
        for clause in formula.clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")

    print(json.dumps({
        "schema": "fano-binary-repair-all-incidences-cnf-v1",
        "state": str(STATE.relative_to(PROJECT)),
        "order": order,
        "edges": len(edges),
        "incidences": incidences,
        "selectors": selectors,
        "variables": formula.variables,
        "clauses": len(formula.clauses),
        "output": str(args.output),
        "meaning": (
            "SAT iff at least one of the 21 Fano point-line binary "
            "switch/target packing incidences repairs the displayed flow"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
