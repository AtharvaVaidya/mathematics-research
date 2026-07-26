#!/usr/bin/env python3
"""Replay every retained hit with the clean-room verifier implementation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import independent_verifier as clean


def main() -> int:
    parser = argparse.ArgumentParser()
    here = Path(__file__).resolve().parent
    parser.add_argument(
        "--witnesses",
        type=Path,
        default=here / "search-witnesses.jsonl",
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    records = tuple(
        json.loads(line)
        for line in arguments.witnesses.read_text(
            encoding="utf-8"
        ).splitlines()
        if line
    )
    require = clean.require
    literal_rows: set[str] = set()
    colouring_counts: dict[str, int] = {}
    girth_counts: dict[str, int] = {}
    marked_subdivision_girth_counts: dict[str, int] = {}
    marked_girth_at_least_10 = 0
    for position, record in enumerate(records, 1):
        order, edges = clean.decode_graph6(record["graph6"])
        require(order == 24, f"row {position}: wrong order")
        incident = clean.incidence(order, edges)
        require(
            len(edges) == 36
            and len(set(edges)) == 36
            and all(len(row) == 3 for row in incident),
            f"row {position}: graph is not simple cubic",
        )
        require(
            clean.connected(order, edges, incident),
            f"row {position}: graph is disconnected",
        )
        mark_edges = tuple(tuple(item) for item in record["mark_edges"])
        require(
            len(mark_edges) == 3
            and len(set(itertools.chain.from_iterable(mark_edges))) == 6,
            f"row {position}: marks are not a matching",
        )
        edge_to_index = {item: index for index, item in enumerate(edges)}
        require(
            all(item in edge_to_index for item in mark_edges),
            f"row {position}: marked edge is absent",
        )
        for size in range(1, 4):
            for removed in itertools.combinations(range(36), size):
                require(
                    not clean.cyclic_cut(
                        order, edges, incident, removed
                    ),
                    f"row {position}: cyclic cut below four",
                )
        colourings = clean.enumerate_tait_colourings(edges, incident)
        require(
            len(colourings) == record["colourings_mod_s3"],
            f"row {position}: Tait-colouring count mismatch",
        )
        clean.verify_universal_separation(
            colourings,
            tuple(edge_to_index[item] for item in mark_edges),
            edges,
            incident,
        )
        girth = clean.shortest_cycle_length(order, edges)
        marked_girth = clean.marked_subdivision_girth(
            order,
            edges,
            tuple(edge_to_index[item] for item in mark_edges),
        )
        girth_counts[str(girth)] = girth_counts.get(str(girth), 0) + 1
        marked_subdivision_girth_counts[str(marked_girth)] = (
            marked_subdivision_girth_counts.get(str(marked_girth), 0) + 1
        )
        marked_girth_at_least_10 += marked_girth >= 10
        literal_rows.add(record["graph6"])
        key = str(len(colourings))
        colouring_counts[key] = colouring_counts.get(key, 0) + 1

    payload = arguments.witnesses.read_bytes()
    report = {
        "status": "VERIFIED",
        "witness_records": len(records),
        "distinct_literal_graph6_rows": len(literal_rows),
        "tait_colourings_mod_s3_distribution": colouring_counts,
        "girth_distribution": girth_counts,
        "marked_subdivision_girth_distribution":
            marked_subdivision_girth_counts,
        "records_satisfying_every_circuit_length_plus_marks_at_least_10":
            marked_girth_at_least_10,
        "witness_stream_sha256": hashlib.sha256(payload).hexdigest(),
        "checks": (
            "simple connected cubic; three-edge matching; no cyclic cut "
            "of size below four; complete normalized Tait-colouring "
            "enumeration; universal bichromatic separation"
        ),
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
