#!/usr/bin/env python3
"""Independent checker for the H2--H5 prescribed-equal-label covers."""

from __future__ import annotations

from collections import deque
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"

EXPECTED = {
    2: {
        "vertices": 82,
        "pairs": 7_257,
        "certificates": 79,
        "sha256": (
            "8aa5e7dd47499b172a4dc1fe3de2af15"
            "af8efea954414f90dffbb304205c5b88"
        ),
    },
    3: {
        "vertices": 122,
        "pairs": 16_287,
        "certificates": 92,
        "sha256": (
            "cb505649d4f98a04d1c5d73dc66a036"
            "3824b3fbfd5f94568de7c816a45eaa0dc"
        ),
    },
    4: {
        "vertices": 162,
        "pairs": 28_917,
        "certificates": 103,
        "sha256": (
            "27d629e992314df69838784186fa54ce6"
            "f7d52ab9f2db7c0f02d41ac85d086cd"
        ),
    },
    5: {
        "vertices": 202,
        "pairs": 45_147,
        "certificates": 120,
        "sha256": (
            "552864926e9b06862929e52454d527bb3"
            "2760a25fec5b3d4ba91d04fd6965d22"
        ),
    },
}
EXPECTED_TABLE_SHA256 = (
    "ad2192ff178482a97d5a905d71bcfe47"
    "f3b4e96879cb41ad7bb5ae6099d2f8e7"
)
EXPECTED_LOG_SHA256 = (
    "90903250d3376a3352d7aeb764bba9f7"
    "7ea705fb9c1d7016bfe98e7e9175fb83"
)
D5 = tuple(value for value in range(32) if value.bit_count() == 2)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_graph6(record: bytes) -> tuple[int, list[tuple[int, int]]]:
    if not record:
        raise SystemExit("empty graph6 record")
    if record[0] == 126:
        if len(record) < 4 or record[1] == 126:
            raise SystemExit("unsupported graph6 order header")
        header = record[1:4]
        if any(not 63 <= value < 127 for value in header):
            raise SystemExit("invalid graph6 order header")
        vertices = 0
        for value in header:
            vertices = 64 * vertices + value - 63
        data = record[4:]
    else:
        vertices = record[0] - 63
        data = record[1:]
    if not 0 <= vertices <= 258_047:
        raise SystemExit("invalid graph6 order")

    bits: list[int] = []
    for character in data:
        value = character - 63
        if not 0 <= value < 64:
            raise SystemExit("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = vertices * (vertices - 1) // 2
    if len(bits) < needed or any(bits[needed:]):
        raise SystemExit("malformed graph6 padding")

    edges: list[tuple[int, int]] = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, edges


def graph_data(
    vertices: int, edges: list[tuple[int, int]]
) -> tuple[list[list[int]], list[list[tuple[int, int]]]]:
    incidence = [[] for _ in range(vertices)]
    adjacency = [[] for _ in range(vertices)]
    for edge_id, (left, right) in enumerate(edges):
        incidence[left].append(edge_id)
        incidence[right].append(edge_id)
        adjacency[left].append((right, edge_id))
        adjacency[right].append((left, edge_id))
    return incidence, adjacency


def reached_without(
    adjacency: list[list[tuple[int, int]]], skipped: int | None
) -> int:
    reached = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for other, edge_id in adjacency[vertex]:
            if edge_id == skipped or other in reached:
                continue
            reached.add(other)
            queue.append(other)
    return len(reached)


def independent_pairs(
    edges: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    result = []
    for first, (a, b) in enumerate(edges):
        for second in range(first + 1, len(edges)):
            c, d = edges[second]
            if len({a, b, c, d}) == 4:
                result.append((first, second))
    return result


def check_graph(
    graph_number: int,
) -> tuple[list[tuple[int, int]], list[list[int]]]:
    raw = (ARTIFACTS / f"H{graph_number}.g6").read_bytes()
    if sha256(raw) != EXPECTED[graph_number]["sha256"]:
        raise SystemExit(f"H{graph_number}: source digest mismatch")
    records = raw.splitlines()
    if len(records) != 1:
        raise SystemExit(f"H{graph_number}: expected one graph6 record")
    vertices, edges = decode_graph6(records[0])
    incidence, adjacency = graph_data(vertices, edges)
    if vertices != EXPECTED[graph_number]["vertices"]:
        raise SystemExit(f"H{graph_number}: wrong order")
    if len(edges) * 2 != 3 * vertices:
        raise SystemExit(f"H{graph_number}: wrong size")
    if any(len(row) != 3 for row in incidence):
        raise SystemExit(f"H{graph_number}: not cubic")
    if reached_without(adjacency, None) != vertices:
        raise SystemExit(f"H{graph_number}: disconnected")
    for edge_id in range(len(edges)):
        if reached_without(adjacency, edge_id) != vertices:
            raise SystemExit(f"H{graph_number}: bridge at edge {edge_id}")
    return edges, incidence


def parse_table() -> dict[int, list[list[bytes]]]:
    raw = (ARTIFACTS / "equal-label-cover.tsv").read_bytes()
    if sha256(raw) != EXPECTED_TABLE_SHA256:
        raise SystemExit("equal-label table digest mismatch")
    result = {graph_number: [] for graph_number in EXPECTED}
    for row_number, row in enumerate(raw.splitlines(), start=1):
        fields = row.split(b"\t")
        if len(fields) != 6:
            raise SystemExit(f"table row {row_number}: expected six fields")
        try:
            source_index = int(fields[0])
        except ValueError as error:
            raise SystemExit(
                f"table row {row_number}: bad graph number"
            ) from error
        graph_number = source_index + 1
        if graph_number not in result:
            raise SystemExit(f"table row {row_number}: unknown graph")
        result[graph_number].append(fields)
    return result


def check_certificates(
    graph_number: int,
    edges: list[tuple[int, int]],
    incidence: list[list[int]],
    rows: list[list[bytes]],
) -> dict[str, int]:
    pairs = independent_pairs(edges)
    expected = EXPECTED[graph_number]
    if len(pairs) != expected["pairs"]:
        raise SystemExit(f"H{graph_number}: independent-pair count mismatch")
    if len(rows) != expected["certificates"]:
        raise SystemExit(f"H{graph_number}: certificate count mismatch")

    covered = [False] * len(pairs)
    covered_count = 0
    for certificate, fields in enumerate(rows, start=1):
        try:
            recorded_certificate = int(fields[1])
            first = int(fields[2])
            second = int(fields[3])
            recorded_new = int(fields[4])
        except ValueError as error:
            raise SystemExit(
                f"H{graph_number} certificate {certificate}: bad integer"
            ) from error
        if recorded_certificate != certificate:
            raise SystemExit(
                f"H{graph_number}: nonconsecutive certificate index"
            )
        try:
            pivot = covered.index(False)
        except ValueError as error:
            raise SystemExit(
                f"H{graph_number}: redundant trailing certificate"
            ) from error
        if (first, second) != pairs[pivot]:
            raise SystemExit(
                f"H{graph_number} certificate {certificate}: wrong pivot"
            )

        model = fields[5]
        if len(model) != len(edges) or any(not 48 <= value <= 57 for value in model):
            raise SystemExit(
                f"H{graph_number} certificate {certificate}: malformed model"
            )
        labels = [value - 48 for value in model]
        if labels[first] != 0 or labels[second] != 0:
            raise SystemExit(
                f"H{graph_number} certificate {certificate}: "
                "pivot labels are not the fixed representative"
            )
        for vertex, incident in enumerate(incidence):
            if (
                D5[labels[incident[0]]]
                ^ D5[labels[incident[1]]]
                ^ D5[labels[incident[2]]]
            ):
                raise SystemExit(
                    f"H{graph_number} certificate {certificate}: "
                    f"parity failure at vertex {vertex}"
                )

        newly_covered = 0
        for index, (left, right) in enumerate(pairs):
            if not covered[index] and labels[left] == labels[right]:
                covered[index] = True
                covered_count += 1
                newly_covered += 1
        if newly_covered != recorded_new:
            raise SystemExit(
                f"H{graph_number} certificate {certificate}: "
                "coverage count mismatch"
            )

    if covered_count != len(pairs):
        raise SystemExit(f"H{graph_number}: uncovered independent pair")
    return {
        "vertices": EXPECTED[graph_number]["vertices"],
        "edges": len(edges),
        "independent_pairs": len(pairs),
        "explicit_d5_labellings": len(rows),
    }


def main() -> int:
    log = (ARTIFACTS / "cadical.log").read_bytes()
    if sha256(log) != EXPECTED_LOG_SHA256:
        raise SystemExit("CaDiCaL log digest mismatch")
    expected_summary = (
        b"SUMMARY implementation=cadical mode=cap-equal-label "
        b"graphs=4 queries=394 sat=394 unsat=0 pairs=97608"
    )
    if expected_summary not in log.splitlines():
        raise SystemExit("CaDiCaL aggregate summary mismatch")

    table = parse_table()
    results = {}
    for graph_number in EXPECTED:
        edges, incidence = check_graph(graph_number)
        results[f"H{graph_number}"] = check_certificates(
            graph_number, edges, incidence, table[graph_number]
        )

    result = {
        "schema": "five-cdc-mnp-h2-h5-prescribed-equal-label-v1",
        "classification": "FINITE EXPLICIT POSITIVE CERTIFICATE",
        "graphs": results,
        "independent_pairs": sum(
            entry["independent_pairs"] for entry in results.values()
        ),
        "explicit_d5_labellings": sum(
            entry["explicit_d5_labellings"] for entry in results.values()
        ),
        "table_sha256": EXPECTED_TABLE_SHA256,
        "theorem": (
            "For every independent edge pair in each retained H2, H3, H4, "
            "and H5 graph, an explicit fixed-five D5 labelling assigns the "
            "same label to both prescribed edges. Equivalently, every "
            "corresponding deletion four-pole realizes boundary type AA."
        ),
        "warning": (
            "This is a finite theorem for four reconstructed "
            "high-flow-resistance graphs. It is not a universal "
            "prescribed-pair theorem and does not resolve Five-CDC."
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
