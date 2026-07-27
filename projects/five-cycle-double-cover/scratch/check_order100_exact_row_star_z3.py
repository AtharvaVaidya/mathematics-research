#!/usr/bin/env python3
"""Independent exact-SMT replay of the order-100 row-star census.

The fixed-subset weighted-kernel predicate is imported from the independently
written ``check_order100_row_star_patterns.py``.  This file separately
enumerates bounded incidence rows, separately constructs row-star words by
literal multiset permutation, and asks Z3 to join the resulting row and
column domains.  It uses the frozen baseline artifact only to skip the 847
profiles already proved infeasible by the weaker relaxation.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import check_order100_row_star_patterns as kernel


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


def bounded_vectors(caps, total, support_cap, diagonal):
    current = [0] * 8

    def visit(position, remaining, support):
        if support > support_cap:
            return
        if position == 8:
            if remaining == 0 and current[diagonal] >= 1:
                yield tuple(current)
            return
        minimum = 1 if position == diagonal else 0
        for value in range(minimum, min(caps[position], remaining) + 1):
            current[position] = value
            yield from visit(
                position + 1,
                remaining - value,
                support + (value > 0),
            )

    yield from visit(0, total, 0)


def first_word(x, y, index, counts):
    """Literal independent word construction using the kernel predicate."""
    remaining = list(counts)
    remaining[index] -= 1
    for tail in kernel.multiset_words(remaining):
        word = (index,) + tail
        if all(
            multiplicity <= 1
            or kernel.pair_extends(
                x,
                y[opposite],
                opposite == index,
                tuple(
                    position
                    for position, label in enumerate(word)
                    if label == opposite
                ),
            )
            for opposite, multiplicity in enumerate(counts)
        ):
            return word
    return None


def domains(x, y):
    result = []
    for index in range(8):
        caps = tuple(
            (DIAGONAL_CAP if index == opposite else OFF_DIAGONAL_CAP)
            [x[index]][y[opposite]]
            for opposite in range(8)
        )
        candidates = []
        for counts in bounded_vectors(
            caps,
            5 + x[index],
            (7 + x[index]) // 2,
            index,
        ):
            word = first_word(x[index], y, index, counts)
            if word is not None:
                candidates.append((counts, word))
        result.append(tuple(candidates))
    return tuple(result)


def smt_instance(x, y, request_model):
    row_domains = domains(x, y)
    column_domains = domains(y, x)
    lines = ["(set-logic QF_LIA)"]
    for row in range(8):
        for column in range(8):
            lines.append(f"(declare-const m_{row}_{column} Int)")

    for row, domain in enumerate(row_domains):
        alternatives = []
        for counts, _word in domain:
            terms = " ".join(
                f"(= m_{row}_{column} {counts[column]})"
                for column in range(8)
            )
            alternatives.append(f"(and {terms})")
        if alternatives:
            lines.append(f"(assert (or {' '.join(alternatives)}))")
        else:
            lines.append("(assert false)")

    for column, domain in enumerate(column_domains):
        alternatives = []
        for counts, _word in domain:
            terms = " ".join(
                f"(= m_{row}_{column} {counts[row]})"
                for row in range(8)
            )
            alternatives.append(f"(and {terms})")
        if alternatives:
            lines.append(f"(assert (or {' '.join(alternatives)}))")
        else:
            lines.append("(assert false)")

    lines.append("(check-sat)")
    if request_model:
        terms = " ".join(
            f"m_{row}_{column}"
            for row in range(8)
            for column in range(8)
        )
        lines.append(f"(get-value ({terms}))")
    return "\n".join(lines) + "\n"


def parse_model(output):
    tokens = (
        output.replace("(", " ").replace(")", " ").replace("\n", " ").split()
    )
    values = {}
    for position, token in enumerate(tokens):
        if token.startswith("m_"):
            values[token] = int(tokens[position + 1])
    assert len(values) == 64
    return tuple(
        tuple(values[f"m_{row}_{column}"] for column in range(8))
        for row in range(8)
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--baseline-json",
        type=Path,
        required=True,
    )
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()
    artifact = json.loads(args.baseline_json.read_text(encoding="utf-8"))
    assert artifact["schema"] == "order100-all-marked-incidence-relaxation-v1"
    baseline_records = artifact["records"]
    assert len(baseline_records) == 1002

    statuses = []
    survivors = []
    for record in baseline_records:
        x = tuple(record["x"])
        y = tuple(record["y"])
        if not record["feasible"]:
            statuses.append({"x": x, "y": y, "status": "baseline-unsat"})
            continue
        assert max(x + y) <= 4
        instance = smt_instance(x, y, False)
        decision = subprocess.run(
            ["z3", "-in", "-smt2"],
            input=instance,
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
    if args.output_json:
        args.output_json.write_text(
            json.dumps(
                {
                    "schema": "order100-independent-row-star-smt-v1",
                    "statuses": statuses,
                    "survivors": survivors,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    print("order-100 independent exact row-star SMT replay: PASS")
    print(f"canonical_profile_pairs={len(statuses)}")
    print(
        "baseline_unsat="
        f"{sum(record['status'] == 'baseline-unsat' for record in statuses)}"
    )
    print(f"row_star_sat={len(survivors)}")
    print(
        "row_star_unsat="
        f"{sum(record['status'] == 'unsat' for record in statuses)}"
    )
    print(
        "status_sha256="
        f"{hashlib.sha256(status_text.encode()).hexdigest()}"
    )
    print(
        "survivor_sha256="
        f"{hashlib.sha256(witness_text.encode()).hexdigest()}"
    )
    print(
        "scope=independent row-word enumeration plus exact Z3 domain join; "
        "no global graph realization"
    )
    if survivors:
        print("canonical_frontier_survivor=")
        print(json.dumps(survivors[0], indent=2))


if __name__ == "__main__":
    main()
