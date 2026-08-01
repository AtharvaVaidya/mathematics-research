#!/usr/bin/env python3
"""Independent exact-SMT replay of the order-100 incidence relaxation.

This checker imports no project module.  It generates simultaneous-S8
profile orbits as multisets of pair types, writes each feasibility problem
as QF_LIA, and asks a fresh Z3 process for an exact decision.
"""

from __future__ import annotations

import hashlib
import json
import subprocess


OFF_DIAGONAL_CAP = (
    (1, 2, 2, 2, 2),
    (2, 2, 2, 3, 3),
    (2, 2, 3, 3, 4),
    (2, 3, 3, 3, 4),
    (2, 3, 4, 4, 4),
)

DIAGONAL_CAP = (
    (1, 1, 2, 2, 2),
    (1, 2, 2, 2, 3),
    (2, 2, 2, 3, 3),
    (2, 2, 3, 3, 4),
    (2, 3, 3, 4, 4),
)


def profile_pairs():
    """Generate simultaneous-S8 orbits directly as multisets of pairs."""
    pair_types = tuple(
        sorted(((a, b) for a in range(7) for b in range(7)), reverse=True)
    )
    result = []

    def visit(first_type, positions_left, x_left, y_left, pairs):
        if positions_left == 0:
            if x_left == 0 and y_left == 0:
                result.append(
                    (
                        tuple(pair[0] for pair in pairs),
                        tuple(pair[1] for pair in pairs),
                    )
                )
            return
        for type_index in range(first_type, len(pair_types)):
            x_value, y_value = pair_types[type_index]
            if x_value > x_left or y_value > y_left:
                continue
            visit(
                type_index,
                positions_left - 1,
                x_left - x_value,
                y_left - y_value,
                pairs + ((x_value, y_value),),
            )

    visit(0, 8, 6, 6, ())
    assert len(result) == 1002
    return result


def cap(x_value: int, y_value: int, diagonal: bool):
    if x_value <= 4 and y_value <= 4:
        table = DIAGONAL_CAP if diagonal else OFF_DIAGONAL_CAP
        return table[x_value][y_value]
    if diagonal:
        return min(1 + x_value + y_value, 5 + min(x_value, y_value))
    return min(1 + x_value + y_value, 4 + min(x_value, y_value))


def smt_instance(x, y, request_model: bool):
    lines = ["(set-logic QF_LIA)"]
    doubled = {}
    for row in range(8):
        for column in range(8):
            m = f"m_{row}_{column}"
            z = f"z_{row}_{column}"
            bound = cap(x[row], y[column], row == column)
            lines.extend(
                (
                    f"(declare-const {m} Int)",
                    f"(declare-const {z} Int)",
                    f"(assert (and (<= 0 {m}) (<= {m} {bound})))",
                    f"(assert (and (<= 0 {z}) (<= {z} 1)))",
                    f"(assert (>= {m} {z}))",
                    f"(assert (<= {m} (* {bound} {z})))",
                )
            )
            if row == column:
                lines.append(f"(assert (= {z} 1))")
            if row != column and (
                (x[row] == 0 and y[column] == 1)
                or (x[row] == 1 and y[column] == 0)
            ):
                q = f"q_{row}_{column}"
                doubled[row, column] = q
                lines.extend(
                    (
                        f"(declare-const {q} Int)",
                        f"(assert (and (<= 0 {q}) (<= {q} 1)))",
                        f"(assert (>= {m} (* 2 {q})))",
                        f"(assert (<= {m} (+ 1 {q})))",
                    )
                )

    for row in range(8):
        entries = " ".join(f"m_{row}_{column}" for column in range(8))
        supports = " ".join(f"z_{row}_{column}" for column in range(8))
        lines.append(f"(assert (= (+ {entries}) {5 + x[row]}))")
        lines.append(f"(assert (<= (+ {supports}) {(7 + x[row]) // 2}))")
    for column in range(8):
        entries = " ".join(f"m_{row}_{column}" for row in range(8))
        supports = " ".join(f"z_{row}_{column}" for row in range(8))
        lines.append(f"(assert (= (+ {entries}) {5 + y[column]}))")
        lines.append(
            f"(assert (<= (+ {supports}) {(7 + y[column]) // 2}))"
        )

    for row in range(8):
        if x[row] == 0:
            terms = [
                doubled[row, column]
                for column in range(8)
                if (row, column) in doubled
            ]
            if terms:
                lines.append(f"(assert (<= (+ {' '.join(terms)}) 1))")
    for column in range(8):
        if y[column] == 0:
            terms = [
                doubled[row, column]
                for row in range(8)
                if (row, column) in doubled
            ]
            if terms:
                lines.append(f"(assert (<= (+ {' '.join(terms)}) 1))")

    lines.append("(check-sat)")
    if request_model:
        terms = " ".join(
            f"m_{row}_{column}"
            for row in range(8)
            for column in range(8)
        )
        lines.append(f"(get-value ({terms}))")
    return "\n".join(lines) + "\n"


def parse_model(output: str):
    tokens = (
        output.replace("(", " ").replace(")", " ").replace("\n", " ").split()
    )
    values = {}
    for index, token in enumerate(tokens):
        if token.startswith("m_"):
            values[token] = int(tokens[index + 1])
    assert len(values) == 64
    return tuple(
        tuple(values[f"m_{row}_{column}"] for column in range(8))
        for row in range(8)
    )


def main():
    statuses = []
    survivors = []
    for x, y in profile_pairs():
        decision = subprocess.run(
            ["z3", "-in", "-smt2"],
            input=smt_instance(x, y, False),
            text=True,
            capture_output=True,
            check=True,
        )
        status = decision.stdout.splitlines()[0].strip()
        assert status in {"sat", "unsat"}
        statuses.append({"x": x, "y": y, "status": status})
        if status == "sat":
            model_run = subprocess.run(
                ["z3", "-in", "-smt2"],
                input=smt_instance(x, y, True),
                text=True,
                capture_output=True,
                check=True,
            )
            assert model_run.stdout.splitlines()[0].strip() == "sat"
            survivors.append(
                {"x": x, "y": y, "matrix": parse_model(model_run.stdout)}
            )

    status_text = json.dumps(statuses, sort_keys=True, separators=(",", ":"))
    witness_text = json.dumps(
        survivors, sort_keys=True, separators=(",", ":")
    )
    print("order-100 independent exact-SMT relaxation: PASS")
    print(f"canonical_profile_pairs={len(statuses)}")
    print(f"sat={len(survivors)}")
    print(f"unsat={len(statuses) - len(survivors)}")
    print(
        "status_sha256="
        f"{hashlib.sha256(status_text.encode()).hexdigest()}"
    )
    print(
        "survivor_sha256="
        f"{hashlib.sha256(witness_text.encode()).hexdigest()}"
    )
    print(
        "scope=exact Z3 QF_LIA replay of the abstract relaxation; "
        "no graph realization"
    )
    if survivors:
        print("canonical_frontier_survivor=")
        print(json.dumps(survivors[0], indent=2))


if __name__ == "__main__":
    main()
