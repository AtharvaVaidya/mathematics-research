#!/usr/bin/env python3
"""Exact finite audit of the seven value classes of F_2^3 flows.

Let ``f`` be a nowhere-zero F_2^3-flow on a cubic graph.  At every vertex
the three incident values are distinct nonzero vectors summing to zero.
Consequently, for each nonzero value ``k``, the value class

    M_k = {e : f(e) = k}

is a matching.  Quotienting F_2^3 by <k> gives an F_2^2-flow whose exact
zero set is M_k.  The matching/four-flow characterization of a five-cycle
double cover therefore succeeds whenever (G-M_k, boundary(M_k)) packs two
edge-disjoint T-joins.

This program tests the tempting universal strengthening

    every nowhere-zero F_2^3-flow has a successful value class.

It canonically generates connected simple cubic graphs and exhausts every
ordered triple of binary cycles, hence every F_2^3-flow in the fixed
coordinate basis.  Packing is decided by the exact even-marked circuit
criterion.  A finite PASS is not a universal proof; a FAIL is a fully
explicit countermodel to the strengthening, not to five-CDC.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from search.canonical.canonical_search import (  # noqa: E402
    parse_graph6,
    validate_simple_cubic,
)
from tools.cycle_space_switch_audit import (  # noqa: E402
    canonical_cubic_graphs,
    fundamental_cycle_space,
)
from tools.flow_switch_audit import Graph, is_bridgeless, is_flow  # noqa: E402
from tools.minimum_exchange_local_census import (  # noqa: E402
    is_matching,
    mask_edges,
    packs_two_t_joins,
)


def value_class_masks(
    first: int,
    second: int,
    third: int,
    all_edges: int,
) -> tuple[int, ...]:
    """Return the exact edge masks of values 1,...,7."""
    coordinates = (first, second, third)
    result: list[int] = []
    for value in range(1, 8):
        mask = all_edges
        for bit, coordinate in enumerate(coordinates):
            if (value >> bit) & 1:
                mask &= coordinate
            else:
                mask &= all_edges ^ coordinate
        result.append(mask)
    return tuple(result)


def flow_values(
    edge_count: int,
    first: int,
    second: int,
    third: int,
) -> tuple[int, ...]:
    return tuple(
        ((first >> edge) & 1)
        | (((second >> edge) & 1) << 1)
        | (((third >> edge) & 1) << 2)
        for edge in range(edge_count)
    )


def audit_graph(
    graph6: str,
    graph: Graph,
    *,
    stop_at_first: bool,
) -> dict[str, object]:
    cycles = fundamental_cycle_space(graph)
    all_edges = (1 << graph.edge_count) - 1
    packing_cache: dict[int, tuple[bool, int | None]] = {}
    totals: Counter[str] = Counter()
    first_bad: dict[str, object] | None = None

    for first in cycles:
        for second in cycles:
            first_or_second = first | second
            for third in cycles:
                totals["coordinate_triples"] += 1
                if first_or_second | third != all_edges:
                    continue
                totals["nowhere_zero_flows"] += 1
                classes = value_class_masks(
                    first, second, third, all_edges
                )
                assert not any(
                    classes[left] & classes[right]
                    for left in range(7)
                    for right in range(left)
                )
                assert sum(classes) == all_edges
                assert all(is_matching(mask, graph) for mask in classes)

                decisions: list[tuple[bool, int | None]] = []
                successful_value: int | None = None
                for value, matching in enumerate(classes, 1):
                    decision = packing_cache.get(matching)
                    if decision is None:
                        decision = packs_two_t_joins(
                            matching, cycles, graph
                        )
                        packing_cache[matching] = decision
                    decisions.append(decision)
                    if decision[0]:
                        successful_value = value
                        break

                if successful_value is not None:
                    totals["flows_with_successful_value"] += 1
                    continue

                totals["flows_with_no_successful_value"] += 1
                values = flow_values(
                    graph.edge_count, first, second, third
                )
                assert is_flow(graph, values)
                first_bad = {
                    "graph6": graph6,
                    "vertices": graph.vertices,
                    "edges": [
                        {"id": edge, "u": u, "v": v}
                        for edge, (u, v) in enumerate(graph.edges)
                    ],
                    "coordinate_cycle_masks": [
                        first,
                        second,
                        third,
                    ],
                    "coordinate_cycle_edges": [
                        mask_edges(first),
                        mask_edges(second),
                        mask_edges(third),
                    ],
                    "flow_values_by_edge": list(values),
                    "value_class_masks": list(classes),
                    "value_class_edges": [
                        mask_edges(mask) for mask in classes
                    ],
                    "packing_decisions": [
                        {
                            "value": value,
                            "packs_two_t_joins": decision[0],
                            "even_marked_cycle": (
                                None
                                if decision[1] is None
                                else mask_edges(decision[1])
                            ),
                        }
                        for value, decision in enumerate(decisions, 1)
                    ],
                }
                if stop_at_first:
                    return {
                        "cycle_space_size": len(cycles),
                        "distinct_value_classes_decided": len(
                            packing_cache
                        ),
                        "totals": dict(sorted(totals.items())),
                        "first_bad_flow": first_bad,
                    }

    return {
        "cycle_space_size": len(cycles),
        "distinct_value_classes_decided": len(packing_cache),
        "totals": dict(sorted(totals.items())),
        "first_bad_flow": first_bad,
    }


def audit_orders(
    minimum_order: int,
    maximum_order: int,
    geng: str,
    *,
    include_nonbridgeless: bool,
    stop_at_first: bool,
) -> dict[str, object]:
    if minimum_order < 2 or maximum_order < minimum_order:
        raise ValueError("invalid order range")
    rows: list[dict[str, object]] = []
    totals: Counter[str] = Counter()
    first_bad: dict[str, object] | None = None

    for order in range(minimum_order, maximum_order + 1):
        if order % 2:
            continue
        for index, graph6, simple in canonical_cubic_graphs(
            geng, order, PROJECT_ROOT
        ):
            totals["generated_graphs"] += 1
            premise = validate_simple_cubic(simple)
            if not premise["cubic"] or not premise["connected"]:
                raise AssertionError((graph6, premise))
            if not premise["bridgeless"] and not include_nonbridgeless:
                totals["skipped_nonbridgeless_graphs"] += 1
                continue
            totals["audited_graphs"] += 1
            graph = Graph(simple.vertices, simple.edges)
            assert is_bridgeless(graph) == bool(premise["bridgeless"])
            result = audit_graph(
                graph6, graph, stop_at_first=stop_at_first
            )
            row = {
                "order": order,
                "canonical_index": index,
                "graph6": graph6,
                "bridgeless": bool(premise["bridgeless"]),
                **result,
            }
            rows.append(row)
            for key, count in result["totals"].items():
                totals[key] += int(count)
            if first_bad is None and result["first_bad_flow"] is not None:
                first_bad = {
                    "order": order,
                    "canonical_index": index,
                    **dict(result["first_bad_flow"]),
                }
            if result["first_bad_flow"] is not None and stop_at_first:
                return {
                        "schema": "fano-value-class-tjoin-audit-v1",
                        "status": "COUNTERMODEL_FOUND",
                        "scope": {
                            "minimum_order": minimum_order,
                            "maximum_order": maximum_order,
                            "connected_simple_cubic": True,
                            "bridgeless_only": not include_nonbridgeless,
                            "all_fixed_basis_f2_3_flows": True,
                        },
                        "universal_lemma": (
                            "every nowhere-zero F2^3-flow has a value "
                            "class packing two T-joins"
                        ),
                        "five_cdc_counterexample": False,
                        "totals": dict(sorted(totals.items())),
                        "first_bad_flow": first_bad,
                        "graph_rows": rows,
                }

    return {
        "schema": "fano-value-class-tjoin-audit-v1",
        "status": (
            "COUNTERMODEL_FOUND"
            if first_bad is not None
            else "EXACT_FINITE_PASS"
        ),
        "scope": {
            "minimum_order": minimum_order,
            "maximum_order": maximum_order,
            "connected_simple_cubic": True,
            "bridgeless_only": not include_nonbridgeless,
            "all_fixed_basis_f2_3_flows": True,
        },
        "universal_lemma": (
            "every nowhere-zero F2^3-flow has a value class packing "
            "two T-joins"
        ),
        "five_cdc_counterexample": False,
        "totals": dict(sorted(totals.items())),
        "first_bad_flow": first_bad,
        "graph_rows": rows,
    }


def audit_one_graph6(
    graph6: str,
    *,
    stop_at_first: bool,
) -> dict[str, object]:
    simple = parse_graph6(graph6)
    premise = validate_simple_cubic(simple)
    if not premise["cubic"] or not premise["connected"]:
        raise ValueError(f"not a connected simple cubic graph: {premise}")
    graph = Graph(simple.vertices, simple.edges)
    result = audit_graph(graph6, graph, stop_at_first=stop_at_first)
    return {
        "schema": "fano-value-class-tjoin-audit-v1",
        "status": (
            "COUNTERMODEL_FOUND"
            if result["first_bad_flow"] is not None
            else "EXACT_FINITE_PASS"
        ),
        "scope": {
            "graph6": graph6,
            "all_fixed_basis_f2_3_flows": True,
        },
        "universal_lemma": (
            "every nowhere-zero F2^3-flow has a value class packing "
            "two T-joins"
        ),
        "five_cdc_counterexample": False,
        "premise": premise,
        **result,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-order", type=int, default=4)
    parser.add_argument("--max-order", type=int, default=10)
    parser.add_argument("--geng", default="geng")
    parser.add_argument("--graph6")
    parser.add_argument("--include-nonbridgeless", action="store_true")
    parser.add_argument("--exhaust-after-first", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.graph6:
        report = audit_one_graph6(
            args.graph6,
            stop_at_first=not args.exhaust_after_first,
        )
    else:
        report = audit_orders(
            args.min_order,
            args.max_order,
            args.geng,
            include_nonbridgeless=args.include_nonbridgeless,
            stop_at_first=not args.exhaust_after_first,
        )
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
        print(
            json.dumps(
                {
                    "status": report["status"],
                    "totals": report.get("totals"),
                    "first_bad_flow": report.get("first_bad_flow"),
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
