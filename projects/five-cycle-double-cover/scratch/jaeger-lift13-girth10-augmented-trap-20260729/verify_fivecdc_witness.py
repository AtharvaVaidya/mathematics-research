#!/usr/bin/env python3
"""Check an explicit standard FiveCDC of the graph used in this package."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
GRAPH = (
    HERE / "../../artifacts/structured/graphs/"
    "lift13_petersen_girth10.json"
).resolve()
WITNESS = HERE / "fivecdc-witness.txt"


def main() -> None:
    document = json.loads(GRAPH.read_text(encoding="utf-8"))
    order = int(document["vertices"])
    edges = tuple(
        (int(edge["u"]), int(edge["v"]))
        for edge in document["edges"]
    )
    labels = tuple(WITNESS.read_text(encoding="utf-8").split())
    assert order == 130
    assert len(edges) == len(labels) == 195
    assert all(
        len(label) == 2
        and label[0] < label[1]
        and set(label) <= set("01234")
        for label in labels
    )

    incidence: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        assert 0 <= left < order and 0 <= right < order and left != right
        incidence[left].append(edge)
        incidence[right].append(edge)
    assert all(len(row) == 3 for row in incidence)

    cycle_sizes = []
    for coordinate in "01234":
        selected = {
            edge for edge, label in enumerate(labels)
            if coordinate in label
        }
        assert all(
            sum(edge in selected for edge in incidence[vertex]) % 2 == 0
            for vertex in range(order)
        )
        cycle_sizes.append(len(selected))
    assert sum(cycle_sizes) == 2 * len(edges)
    assert cycle_sizes == [64, 82, 94, 71, 79]
    print(
        json.dumps(
            {
                "status": "PASS",
                "standard_fivecdc": True,
                "order": order,
                "edges": len(edges),
                "cycle_sizes": cycle_sizes,
                "every_edge_multiplicity": 2,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
