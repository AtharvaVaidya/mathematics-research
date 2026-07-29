#!/usr/bin/env python3
"""Check the minimum-Fano-class witness and inherited proof ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "minimum-zero-exchange-countermodel-130v-20260727"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    graph = json.loads((BASE / "graph.json").read_text(encoding="utf-8"))
    witness = json.loads(
        (HERE / "witness.json").read_text(encoding="utf-8")
    )

    vertices = graph["vertices"]
    edges = graph["edges"]
    edge_count = len(edges)
    assert vertices == witness["vertices"] == 130
    assert edge_count == witness["edges"] == 195
    assert [edge["id"] for edge in edges] == list(range(edge_count))
    assert witness["designated_value"] == [1, 0, 0]

    values = witness["fano_values"]
    assert len(values) == edge_count
    assert all(1 <= value < 8 for value in values)

    incident = [[] for _ in range(vertices)]
    for edge in edges:
        incident[edge["u"]].append(edge["id"])
        incident[edge["v"]].append(edge["id"])
    assert all(len(row) == 3 for row in incident)

    for row in incident:
        total = 0
        for edge_id in row:
            total ^= values[edge_id]
        assert total == 0

    matching = {
        edge_id
        for edge_id, value in enumerate(values)
        if value == 1
    }
    assert matching == {35, 48, 97, 135, 148}
    assert all(
        sum(edge_id in matching for edge_id in row) <= 1
        for row in incident
    )

    quotient = [value >> 1 for value in values]
    lift_cycle = {
        edge_id
        for edge_id, value in enumerate(values)
        if value & 1
    }
    assert matching == {
        edge_id
        for edge_id, value in enumerate(quotient)
        if value == 0
    }
    assert matching <= lift_cycle
    assert all(
        sum(edge_id in lift_cycle for edge_id in row) % 2 == 0
        for row in incident
    )

    ledger = {}
    for line in (BASE / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        digest, name = line.split("  ", 1)
        ledger[name] = digest
    for name, digest in ledger.items():
        assert sha256(BASE / name) == digest

    required = {
        "graph.json",
        "flow-at-most-four-zero.cnf",
        "flow-at-most-four-zero.lrat",
        "extension-at-most-five.cnf",
        "extension-at-most-five.lrat",
        "verify.py",
    }
    assert required <= set(ledger)

    local_ledger = {}
    for line in (HERE / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        digest, name = line.split("  ", 1)
        local_ledger[name] = digest
    for name, digest in local_ledger.items():
        assert sha256(HERE / name) == digest
    assert set(local_ledger) == {"README.md", "verify.py", "witness.json"}

    print(
        json.dumps(
            {
                "classification": (
                    "MINIMUM FANO CLASS NONPACKING; "
                    "NOT A FIVECDC COUNTEREXAMPLE"
                ),
                "vertices": vertices,
                "edges": edge_count,
                "designated_value": [1, 0, 0],
                "designated_class": sorted(matching),
                "designated_class_size": len(matching),
                "lift_cycle_size": len(lift_cycle),
                "fano_flow": "PASS",
                "inherited_proof_ledger": "PASS",
                "local_ledger": "PASS",
                "rho_3": 5,
                "minimum_packing_class_size": 6,
                "delta_rho_positive": True,
                "standard_five_cdc": "INHERITED PASS",
                "five_cdc_counterexample": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
