#!/usr/bin/env python3
"""Exact full-lex radius-two audit of all through-order-14 augmented traps."""

from __future__ import annotations

from collections import Counter
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent / "jaeger-high-girth-local-trap-frontier-20260729"
spec = importlib.util.spec_from_file_location(
    "local", PACKAGE / "verify_blanusa_a_trap.py"
)
assert spec and spec.loader
local = importlib.util.module_from_spec(spec)
spec.loader.exec_module(local)


def audit_row(row):
    order, edges = local.parse_graph6(str(row["graph6"]))
    root = int(row["root"])
    local.ROOT = root
    spokes = tuple(
        edge for edge, endpoints in enumerate(edges) if root in endpoints
    )
    internal = tuple(
        edge for edge, endpoints in enumerate(edges)
        if root not in endpoints
    )
    all_internal = (1 << len(internal)) - 1
    state_cache = {}
    neighbour_cache = {}

    def state(omitted):
        omitted = tuple(omitted)
        if omitted not in state_cache:
            _, kernels, profile, flags = local.state_data(
                order, edges, internal, spokes, omitted
            )
            state_cache[omitted] = (
                (min(profile), sum(map(len, kernels))),
                flags,
            )
        return state_cache[omitted]

    def neighbours(omitted):
        omitted = tuple(omitted)
        if omitted in neighbour_cache:
            return neighbour_cache[omitted]
        answer = []
        for first in range(3):
            for second in range(first + 1, 3):
                first_edges = [
                    edge for edge in range(len(internal))
                    if omitted[first] >> edge & 1
                ]
                second_edges = [
                    edge for edge in range(len(internal))
                    if omitted[second] >> edge & 1
                ]
                for first_local in first_edges:
                    for second_local in second_edges:
                        changed = list(omitted)
                        toggle = (
                            (1 << first_local) | (1 << second_local)
                        )
                        changed[first] ^= toggle
                        changed[second] ^= toggle
                        if not (
                            local.deleted_root_tree(
                                order, edges, internal, changed[first]
                            )
                            and local.deleted_root_tree(
                                order, edges, internal, changed[second]
                            )
                        ):
                            continue
                        changed = tuple(changed)
                        answer.append(
                            (
                                changed,
                                (first_local, second_local),
                                state(changed),
                            )
                        )
        neighbour_cache[omitted] = answer
        return answer

    results = []
    for trap_index, trap in enumerate(row["local_traps"]):
        omitted = (
            int(trap["omitted0"]),
            int(trap["omitted1"]),
            all_internal
            ^ int(trap["omitted0"])
            ^ int(trap["omitted1"]),
        )
        psi, flags = state(omitted)
        assert flags == 0
        assert psi == (int(trap["d_min"]), int(trap["kernel_sum"]))
        layer_one = neighbours(omitted)
        assert len(layer_one) == int(trap["legal_exchanges"])
        assert not any(data[0] < psi for _, _, data in layer_one)
        if any(data[1] > 0 for _, _, data in layer_one):
            continue

        equal_sources = [
            (candidate, exchange)
            for candidate, exchange, data in layer_one
            if data == (psi, 0)
        ]
        sources_examined = 0
        legal_arcs = 0
        escape = None
        for parent, first_exchange in equal_sources:
            sources_examined += 1
            for endpoint, second_exchange, (endpoint_psi, endpoint_flags) in (
                neighbours(parent)
            ):
                legal_arcs += 1
                if endpoint_psi < psi or endpoint_flags > 0:
                    escape = {
                        "first_exchange": first_exchange,
                        "second_exchange": second_exchange,
                        "endpoint_psi": endpoint_psi,
                        "endpoint_flags": endpoint_flags,
                    }
                    break
            if escape is not None:
                break
        results.append(
            {
                "trap_index": trap_index,
                "psi": psi,
                "equal_layer_one": len(equal_sources),
                "sources_examined": sources_examined,
                "legal_arcs_examined": legal_arcs,
                "distance": 2 if escape is not None else None,
                "escape": escape,
            }
        )
    return results


def main():
    rows = [
        json.loads(line)
        for line in (PACKAGE / "trap-structures-through14.jsonl")
        .read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    results = []
    rows_with_survivors = 0
    old_objective_traps = sum(
        len(row["local_traps"]) for row in rows
    )
    for index, row in enumerate(rows):
        local_results = audit_row(row)
        if local_results:
            rows_with_survivors += 1
            for result in local_results:
                result.update(
                    {
                        "row": index,
                        "graph6": row["graph6"],
                        "order": row["order"],
                        "root": row["root"],
                    }
                )
                results.append(result)
        if (index + 1) % 100 == 0:
            print(
                json.dumps(
                    {
                        "progress_rows": index + 1,
                        "augmented_traps": len(results),
                        "without_distance_two": sum(
                            result["distance"] is None
                            for result in results
                        ),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    print(
        "FINAL "
        + json.dumps(
            {
                "status": "PASS",
                "scope": "complete_canonical_cubic_census_through_order_14",
                "source_rows": len(rows),
                "old_objective_traps": old_objective_traps,
                "augmented_trap_rows": rows_with_survivors,
                "augmented_traps": len(results),
                "distance_histogram": Counter(
                    result["distance"] for result in results
                ),
                "safe_sources_examined": sum(
                    result["sources_examined"] for result in results
                ),
                "legal_arcs_examined": sum(
                    result["legal_arcs_examined"] for result in results
                ),
                "maximum_sources_examined": max(
                    (result["sources_examined"] for result in results),
                    default=0,
                ),
                "results": results,
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
