#!/usr/bin/env python3
"""Independent small-order replay of one-flow external port coverage."""

from __future__ import annotations

from collections import Counter
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
TYPED = HERE.parent / "d5-typed-cap-double-star-frontier-20260731"
sys.path.insert(0, str(TYPED))
import verify_small_and_algebra as base  # noqa: E402


def graph6_rows(order: int) -> list[str]:
    geng = os.environ.get("GENG", "/opt/homebrew/bin/geng")
    run = subprocess.run(
        [geng, "-Cq", "-d3", "-D3", str(order)],
        check=True,
        text=True,
        capture_output=True,
    )
    return [row for row in run.stdout.splitlines() if row and not row.startswith(">")]


def fixed_external_bits(n, edges, incidence, labels):
    result = {
        (z, root): 0
        for z in range(n)
        for root, endpoints in enumerate(edges)
        if z not in endpoints
    }
    for pair in base.LABELS:
        for component in base.active_components(labels, pair, edges, incidence):
            component_set = set(component)
            for z in range(n):
                slots = tuple(
                    slot for slot, edge in enumerate(incidence[z])
                    if edge in component_set
                )
                if len(slots) != 2:
                    continue
                inactive = next(slot for slot in range(3) if slot not in slots)
                third = labels[incidence[z][inactive]]
                if pair == third:
                    continue
                assert not (pair & third)
                port_bits = sum(1 << slot for slot in slots)
                for root in component:
                    if z not in edges[root]:
                        result[z, root] |= port_bits
    return result


def main() -> None:
    expected = {
        4: (1, 18, 12),
        6: (2, 138, 72),
        8: (5, 1464, 360),
        10: (18, 18012, 2160),
        12: (81, 309678, 14580),
    }
    for order, (expected_graphs, expected_flows, expected_interfaces) in expected.items():
        graph_count = flow_count = interface_count = 0
        maxima: list[int] = []
        for row in graph6_rows(order):
            n, edges, incidence = base.decode_graph6(row)
            assert n == order
            local = {
                (z, root): 0
                for z in range(n)
                for root, endpoints in enumerate(edges)
                if z not in endpoints
            }
            for labels in base.enumerate_representatives(edges, incidence):
                flow_count += 1
                values = fixed_external_bits(n, edges, incidence, labels)
                for key, bits in values.items():
                    local[key] = max(local[key], bits.bit_count())
            maxima.extend(local.values())
            graph_count += 1
        interface_count = len(maxima)
        counts = Counter(maxima)
        assert (graph_count, flow_count, interface_count) == (
            expected_graphs, expected_flows, expected_interfaces
        )
        assert counts == {3: interface_count}
        print(
            f"PYTHON_SIMULTANEOUS order={order} graphs={graph_count} "
            f"representative_flows={flow_count} interfaces={interface_count} "
            "PASS"
        )
    print("PYTHON_SIMULTANEOUS_FRONTIER PASS")


if __name__ == "__main__":
    main()
