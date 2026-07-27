#!/usr/bin/env python3
"""Independent verifier for the retained order-26 strict-snark pole probe."""

from __future__ import annotations

from collections import deque
from itertools import combinations
import gzip
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
EXPECTED_SOURCE_ROWS = 280
EXPECTED_SOURCE_SHA256 = (
    "5ce072d86e9fa639f34d1a9ec916b69c62a46816f5486a0d813e56279320e35d"
)
EXPECTED_POLE_ROWS = 185_640
EXPECTED_POLE_SHA256 = (
    "9073b2390f68070a121ae0523d5000acc0e5e2ad8ec8d6214a65a6d23ef106dc"
)
EXPECTED_TABLE_SHA256 = (
    "07c466b2c0839098b534f2a1bb1e894b973a619bb3eccd3118a69edfed8a1f68"
)
EXPECTED_SHARD_ROWS = 23_205
SUMMARY = re.compile(
    r"^SUMMARY implementation=(cadical|csp) mode=full "
    r"rows=(\d+) queries=(\d+) sat=(\d+) hits=(\d+)$"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_graph6(record: bytes) -> tuple[int, list[tuple[int, int]]]:
    if not record or record[0] == 126:
        raise SystemExit("only short graph6 records are permitted")
    vertices = record[0] - 63
    if not 0 <= vertices <= 62:
        raise SystemExit("invalid graph6 order")
    bits: list[int] = []
    for character in record[1:]:
        value = character - 63
        if not 0 <= value < 64:
            raise SystemExit("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = vertices * (vertices - 1) // 2
    if len(bits) < needed or any(bits[needed:]):
        raise SystemExit("malformed graph6 padding")
    edges = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, edges


def encode_graph6(vertices: int, edges: list[tuple[int, int]]) -> bytes:
    adjacent = set(edges)
    bits = [
        int((left, right) in adjacent)
        for right in range(1, vertices)
        for left in range(right)
    ]
    while len(bits) % 6:
        bits.append(0)
    result = bytearray((vertices + 63,))
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = 2 * value + bit
        result.append(value + 63)
    return bytes(result)


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


def components(
    vertices: int,
    adjacency: list[list[tuple[int, int]]],
    deleted: set[int],
) -> list[set[int]]:
    unseen = set(range(vertices))
    result = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        shore = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for other, edge_id in adjacency[vertex]:
                if edge_id in deleted or other not in unseen:
                    continue
                unseen.remove(other)
                shore.add(other)
                stack.append(other)
        result.append(shore)
    return result


def three_edge_colourable(
    vertices: int,
    edges: list[tuple[int, int]],
) -> bool:
    colours = [-1] * len(edges)
    used = [0] * vertices

    def extend(coloured: int) -> bool:
        if coloured == len(edges):
            return True
        best_edge = -1
        best_allowed = 0
        best_count = 4
        for edge_id, (left, right) in enumerate(edges):
            if colours[edge_id] >= 0:
                continue
            allowed = 0b111 & ~(used[left] | used[right])
            count = allowed.bit_count()
            if count < best_count:
                best_edge = edge_id
                best_allowed = allowed
                best_count = count
                if count <= 1:
                    break
        if not best_allowed:
            return False
        left, right = edges[best_edge]
        for colour in range(3):
            bit = 1 << colour
            if not best_allowed & bit:
                continue
            colours[best_edge] = colour
            used[left] |= bit
            used[right] |= bit
            if extend(coloured + 1):
                return True
            used[left] ^= bit
            used[right] ^= bit
            colours[best_edge] = -1
        return False

    return extend(0)


def check_strict_snark(record_number: int, record: bytes) -> list[tuple[int, int]]:
    vertices, edges = decode_graph6(record)
    incidence, adjacency = graph_data(vertices, edges)
    if vertices != 26 or len(edges) != 39:
        raise SystemExit(f"source row {record_number}: wrong order or size")
    if any(len(row) != 3 for row in incidence):
        raise SystemExit(f"source row {record_number}: not cubic")
    if len(components(vertices, adjacency, set())) != 1:
        raise SystemExit(f"source row {record_number}: disconnected")

    # Girth at least five: after deleting any edge, its endpoints have no
    # path of length at most three.
    for skipped, (source, target) in enumerate(edges):
        distance = {source: 0}
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            if distance[vertex] == 3:
                continue
            for other, edge_id in adjacency[vertex]:
                if edge_id == skipped or other in distance:
                    continue
                distance[other] = distance[vertex] + 1
                queue.append(other)
        if target in distance and distance[target] <= 3:
            raise SystemExit(f"source row {record_number}: girth below five")

    # No set of at most three edges separates two components containing
    # cycles.  The size-one case also checks bridgelessness.
    for size in range(1, 4):
        for deleted_tuple in combinations(range(len(edges)), size):
            shores = components(vertices, adjacency, set(deleted_tuple))
            cyclic_shores = 0
            for shore in shores:
                internal = sum(
                    left in shore and right in shore for left, right in edges
                )
                cyclic_shores += int(internal >= len(shore))
            if cyclic_shores >= 2:
                raise SystemExit(
                    f"source row {record_number}: cyclic edge cut below four"
                )

    if three_edge_colourable(vertices, edges):
        raise SystemExit(f"source row {record_number}: Tait colouring found")
    return edges


def parse_log(path: Path, implementation: str) -> dict[str, int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    matches = [match for line in lines if (match := SUMMARY.fullmatch(line))]
    if len(matches) != 1 or matches[0].group(1) != implementation:
        raise SystemExit(f"{path}: malformed summary")
    match = matches[0]
    result = {
        "rows": int(match.group(2)),
        "queries": int(match.group(3)),
        "sat": int(match.group(4)),
        "hits": int(match.group(5)),
    }
    return result


def check_logs(implementation: str) -> None:
    if implementation == "cadical":
        paths = [ARTIFACTS / "cadical.log"]
        expected_rows = [EXPECTED_POLE_ROWS]
    else:
        paths = [
            ARTIFACTS / f"csp-shard{shard}.log"
            for shard in range(8)
        ]
        expected_rows = [EXPECTED_SHARD_ROWS] * 8
        for shard in range(8):
            status = (
                ARTIFACTS / f"csp-shard{shard}.status"
            ).read_text(encoding="utf-8")
            if status != "0\n":
                raise SystemExit(f"csp shard {shard}: nonzero status")

    totals = {"rows": 0, "queries": 0, "sat": 0, "hits": 0}
    for path, rows in zip(paths, expected_rows):
        result = parse_log(path, implementation)
        expected = {
            "rows": rows,
            "queries": 10 * rows,
            "sat": 10 * rows,
            "hits": 0,
        }
        if result != expected:
            raise SystemExit(f"{path}: unexpected aggregate")
        for key in totals:
            totals[key] += result[key]
    if totals != {
        "rows": EXPECTED_POLE_ROWS,
        "queries": 10 * EXPECTED_POLE_ROWS,
        "sat": 10 * EXPECTED_POLE_ROWS,
        "hits": 0,
    }:
        raise SystemExit(f"{implementation}: wrong log totals")


def main() -> int:
    generator_log = (ARTIFACTS / "snarkhunter.log").read_text(
        encoding="utf-8"
    )
    if (
        "snarkhunter 26 5 S s C4 o g" not in generator_log
        or "All done, 280 graphs generated with 26 vertices."
        not in generator_log
    ):
        raise SystemExit("malformed Snarkhunter log")
    if (ARTIFACTS / "expand.log").read_text(encoding="utf-8") != (
        "SUMMARY graphs=280 poles=185640\n"
    ):
        raise SystemExit("malformed pole-expansion log")

    source = (ARTIFACTS / "strict-snarks-order26.g6").read_bytes()
    records = source.splitlines()
    if len(records) != EXPECTED_SOURCE_ROWS or len(set(records)) != len(records):
        raise SystemExit("wrong or duplicate strict-snark records")
    if sha256(source) != EXPECTED_SOURCE_SHA256:
        raise SystemExit("strict-snark source digest mismatch")

    expanded = bytearray()
    for record_number, record in enumerate(records, start=1):
        edges = check_strict_snark(record_number, record)
        for first, (a, b) in enumerate(edges):
            for second in range(first + 1, len(edges)):
                c, d = edges[second]
                if len({a, b, c, d}) != 4:
                    continue
                remaining = [
                    edge
                    for edge_id, edge in enumerate(edges)
                    if edge_id not in {first, second}
                ]
                expanded.extend(encode_graph6(26, remaining))
                expanded.append(10)

    poles = gzip.decompress(
        (ARTIFACTS / "strict-snarks-order26-poles.g6.gz").read_bytes()
    )
    if bytes(expanded) != poles:
        raise SystemExit("pole stream is not the exact independent-edge expansion")
    if poles.count(b"\n") != EXPECTED_POLE_ROWS:
        raise SystemExit("wrong pole row count")
    if sha256(poles) != EXPECTED_POLE_SHA256:
        raise SystemExit("pole stream digest mismatch")

    tables = {}
    pole_records = poles.splitlines()
    for implementation in ("cadical", "csp"):
        table = gzip.decompress(
            (ARTIFACTS / f"{implementation}-full.tsv.gz").read_bytes()
        )
        if sha256(table) != EXPECTED_TABLE_SHA256:
            raise SystemExit(f"{implementation}: classification digest mismatch")
        rows = table.splitlines()
        if len(rows) != EXPECTED_POLE_ROWS:
            raise SystemExit(f"{implementation}: classification row count mismatch")
        for row_number, (row, pole) in enumerate(zip(rows, pole_records), start=1):
            fields = row.split(b"\t")
            if fields != [pole, b"10", b"3ff"]:
                raise SystemExit(
                    f"{implementation}: wrong full signature at row {row_number}"
                )
        tables[implementation] = table
        check_logs(implementation)
    if tables["cadical"] != tables["csp"]:
        raise SystemExit("the two implementation tables differ")

    result = {
        "schema": "five-cdc-order26-strict-cap-signatures-v1",
        "classification": "FINITE TWO-IMPLEMENTATION EXACT CLASSIFICATION",
        "source_graphs": EXPECTED_SOURCE_ROWS,
        "independent_edge_deletions": EXPECTED_POLE_ROWS,
        "queries_per_implementation": 10 * EXPECTED_POLE_ROWS,
        "satisfiable_per_implementation": 10 * EXPECTED_POLE_ROWS,
        "full_signature_rows": EXPECTED_POLE_ROWS,
        "exceptional_hits": 0,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "pole_stream_sha256": EXPECTED_POLE_SHA256,
        "classification_sha256": EXPECTED_TABLE_SHA256,
        "result": (
            "Every independent-edge deletion pole from the retained 280 "
            "strict order-26 snarks realizes all ten fixed-five D5 boundary types."
        ),
        "warning": (
            "Completeness of the 280-graph strict-snark source relies on the "
            "retained Snarkhunter run. This is not a census of all order-26 "
            "non-Tait caps, a universal full-signature theorem, or a Five-CDC "
            "resolution."
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
