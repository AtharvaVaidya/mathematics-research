#!/usr/bin/env python3
"""Independent audit of the triangle-free 3-connected cap root screen."""

from __future__ import annotations

from itertools import zip_longest
from pathlib import Path
import gzip
import hashlib
import json
import re


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
SOURCES = (
    (20, 128, "b1c94a57d1dfe6279ae062a09c0913260e4f294f66d8c4d57a3dad4032b6685f"),
    (22, 1_161, "15f5d1ee39187885ad0ec7aa9523ac88e4afa1eaa6443d0e6acd404b2ad33108"),
    (24, 12_612, "5682ab6385d26b9222286045b165f5478f557f45ab7ad35d81efaf35233d607a"),
)
EXPECTED_CORES = 330_790
EXPECTED_CORE_SHA256 = (
    "0a93a380b566d28a037a322c7b35f6f87b96900e8a87f875747a6fe7d7b0881f"
)
EXPECTED_ROOTS = 10_824_084
EXPECTED_CALLS = 33_363_003
EXPECTED_EMPTY = 0
EXPECTED_CLOSED = 10_824_084
EXPECTED_TRANSCRIPT_SHA256 = (
    "130180f347c4fe3f82b94eeb16c3c990be967680ef16a02283e4962383464c75"
)
SHARDS = "abcdef"
SHARD_CORE_COUNTS = (55_132, 55_132, 55_132, 55_132, 55_132, 55_130)
SUMMARY = re.compile(
    r"^SUMMARY implementation=(cadical|csp) graphs=(\d+) "
    r"nonbridge_roots=(\d+) empty=(\d+) closed=(\d+) "
    r"violations=(\d+) calls=(\d+)$"
)
BASE_PAIR_MASKS = (0x0C, 0x12, 0x21)
ORBIT_SIZES = (1, 1, 1, 2, 2, 2, 1)


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
    edges: list[tuple[int, int]] = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, edges


def encode_graph6(vertices: int, edges: list[tuple[int, int]]) -> bytes:
    edge_set = {tuple(sorted(edge)) for edge in edges}
    bits = [
        int((left, right) in edge_set)
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


def connected_after_vertices(
    vertices: int,
    adjacency: list[list[tuple[int, int]]],
    deleted: frozenset[int],
) -> bool:
    remaining = [vertex for vertex in range(vertices) if vertex not in deleted]
    if not remaining:
        return True
    reached = {remaining[0]}
    stack = [remaining[0]]
    while stack:
        vertex = stack.pop()
        for other, _ in adjacency[vertex]:
            if other in deleted or other in reached:
                continue
            reached.add(other)
            stack.append(other)
    return len(reached) == len(remaining)


def three_edge_colourable(
    vertices: int, edges: list[tuple[int, int]]
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


def check_cap(order: int, row_number: int, record: bytes) -> list[tuple[int, int]]:
    vertices, edges = decode_graph6(record)
    incidence, adjacency = graph_data(vertices, edges)
    if vertices != order or len(edges) != 3 * order // 2:
        raise SystemExit(f"order {order} row {row_number}: wrong size")
    if any(len(row) != 3 for row in incidence):
        raise SystemExit(f"order {order} row {row_number}: not cubic")
    if not connected_after_vertices(vertices, adjacency, frozenset()):
        raise SystemExit(f"order {order} row {row_number}: disconnected")

    neighbour_sets = [
        {other for other, _ in adjacency[vertex]} for vertex in range(vertices)
    ]
    for left, right in edges:
        if neighbour_sets[left] & neighbour_sets[right]:
            raise SystemExit(f"order {order} row {row_number}: triangle")

    for first in range(vertices):
        if not connected_after_vertices(vertices, adjacency, frozenset((first,))):
            raise SystemExit(f"order {order} row {row_number}: cutvertex")
        for second in range(first + 1, vertices):
            if not connected_after_vertices(
                vertices, adjacency, frozenset((first, second))
            ):
                raise SystemExit(
                    f"order {order} row {row_number}: two-vertex cut"
                )

    if three_edge_colourable(vertices, edges):
        raise SystemExit(f"order {order} row {row_number}: Tait colouring")
    return edges


def delete_vertex(
    vertices: int, edges: list[tuple[int, int]], deleted: int
) -> bytes:
    relabel: dict[int, int] = {}
    for vertex in range(vertices):
        if vertex != deleted:
            relabel[vertex] = len(relabel)
    remaining = [
        (relabel[left], relabel[right])
        for left, right in edges
        if left != deleted and right != deleted
    ]
    return encode_graph6(vertices - 1, remaining)


def is_bridge(
    vertices: int,
    edges: list[tuple[int, int]],
    adjacency: list[list[tuple[int, int]]],
    removed: int,
) -> bool:
    source, target = edges[removed]
    reached = {source}
    stack = [source]
    while stack:
        vertex = stack.pop()
        for other, edge_id in adjacency[vertex]:
            if edge_id == removed or other in reached:
                continue
            reached.add(other)
            stack.append(other)
    return target not in reached


def parse_summary(implementation: str, shard: str) -> dict[str, int]:
    path = ARTIFACTS / f"{implementation}-shard{shard}.log"
    matches = [
        match
        for line in path.read_text(encoding="utf-8").splitlines()
        if (match := SUMMARY.fullmatch(line))
    ]
    if len(matches) != 1 or matches[0].group(1) != implementation:
        raise SystemExit(f"{path}: malformed summary")
    values = tuple(int(matches[0].group(index)) for index in range(2, 8))
    keys = ("graphs", "roots", "empty", "closed", "violations", "calls")
    return dict(zip(keys, values))


def main() -> int:
    expanded = bytearray()
    source_total = 0
    seen_sources: set[bytes] = set()
    for order, expected_rows, expected_sha in SOURCES:
        path = ARTIFACTS / f"c3-nontait-order{order}.g6"
        data = path.read_bytes()
        records = data.splitlines()
        if len(records) != expected_rows or len(set(records)) != len(records):
            raise SystemExit(f"order {order}: wrong or duplicate source rows")
        if sha256(data) != expected_sha:
            raise SystemExit(f"order {order}: source digest mismatch")
        for row_number, record in enumerate(records, start=1):
            edges = check_cap(order, row_number, record)
            for deleted in range(order):
                expanded.extend(delete_vertex(order, edges, deleted))
                expanded.append(10)
        source_total += len(records)
        seen_sources.update(records)
    if len(seen_sources) != source_total:
        raise SystemExit("source streams overlap")

    core_data = gzip.decompress(
        (ARTIFACTS / "vertex-deleted-cores-through24.g6.gz").read_bytes()
    )
    if bytes(expanded) != core_data:
        raise SystemExit("vertex-deleted core stream mismatch")
    if core_data.count(b"\n") != EXPECTED_CORES:
        raise SystemExit("wrong core count")
    if sha256(core_data) != EXPECTED_CORE_SHA256:
        raise SystemExit("core stream digest mismatch")

    transcript_hash = hashlib.sha256()
    roots = 0
    calls = 0
    empty = 0
    closed = 0
    with gzip.open(ARTIFACTS / "cadical-transcript.tsv.gz", "rb") as left, gzip.open(
        ARTIFACTS / "csp-transcript.tsv.gz", "rb"
    ) as right:
        rows = zip_longest(left, right)
        for core in core_data.splitlines():
            vertices, edges = decode_graph6(core)
            incidence, adjacency = graph_data(vertices, edges)
            if sum(len(row) == 2 for row in incidence) != 3:
                raise SystemExit("expanded core does not have three terminals")
            if any(len(row) not in (2, 3) for row in incidence):
                raise SystemExit("expanded core has wrong degree")
            for root in range(len(edges)):
                if is_bridge(vertices, edges, adjacency, root):
                    raise SystemExit("3-connected cap deletion has a bridge")
                left_line, right_line = next(rows, (None, None))
                if left_line is None or right_line is None:
                    raise SystemExit("short transcript")
                if left_line != right_line:
                    raise SystemExit(f"transcripts differ at root row {roots + 1}")
                transcript_hash.update(left_line)
                fields = left_line.rstrip(b"\n").split(b"\t")
                if len(fields) != 5:
                    raise SystemExit(f"malformed transcript row {roots + 1}")
                record, root_text, category, queried_text, observed_text = fields
                if (
                    record != core
                    or int(root_text) != root
                    or category not in (b"0", b"1")
                ):
                    raise SystemExit(f"wrong decision at root row {roots + 1}")
                queried = int(queried_text, 16)
                observed = int(observed_text, 16)
                if observed & ~queried:
                    raise SystemExit(f"unqueried positive orbit at row {roots + 1}")
                if category == b"0" and observed:
                    raise SystemExit(f"nonempty empty row {roots + 1}")
                if category == b"1" and not any(
                    observed & mask == mask for mask in BASE_PAIR_MASKS
                ):
                    raise SystemExit(f"no base pair at root row {roots + 1}")
                empty += category == b"0"
                closed += category == b"1"
                calls += sum(
                    ORBIT_SIZES[orbit]
                    for orbit in range(7)
                    if queried >> orbit & 1
                )
                roots += 1
        extra_left, extra_right = next(rows, (None, None))
        if extra_left is not None or extra_right is not None:
            raise SystemExit("long transcript")

    if (
        roots != EXPECTED_ROOTS
        or calls != EXPECTED_CALLS
        or empty != EXPECTED_EMPTY
        or closed != EXPECTED_CLOSED
        or empty + closed != roots
    ):
        raise SystemExit("unexpected root or solver-call total")
    if transcript_hash.hexdigest() != EXPECTED_TRANSCRIPT_SHA256:
        raise SystemExit("transcript digest mismatch")

    for implementation in ("cadical", "csp"):
        totals = dict.fromkeys(
            ("graphs", "roots", "empty", "closed", "violations", "calls"), 0
        )
        for index, shard in enumerate(SHARDS):
            status = (
                ARTIFACTS / f"{implementation}-shard{shard}.status"
            ).read_text(encoding="utf-8")
            if status != "0\n":
                raise SystemExit(
                    f"{implementation} shard {shard}: nonzero status"
                )
            summary = parse_summary(implementation, shard)
            if summary["graphs"] != SHARD_CORE_COUNTS[index]:
                raise SystemExit(
                    f"{implementation} shard {shard}: wrong graph count"
                )
            for key, value in summary.items():
                totals[key] += value
        expected = {
            "graphs": EXPECTED_CORES,
            "roots": EXPECTED_ROOTS,
            "empty": EXPECTED_EMPTY,
            "closed": EXPECTED_CLOSED,
            "violations": 0,
            "calls": EXPECTED_CALLS,
        }
        if totals != expected:
            raise SystemExit(f"{implementation}: wrong aggregate summary")

    result = {
        "schema": "five-cdc-rooted-c3-cap-through24-v1",
        "classification": "FINITE TWO-IMPLEMENTATION ROOTED CLASSIFICATION",
        "source_caps": source_total,
        "vertex_deleted_cores": EXPECTED_CORES,
        "nonbridge_roots": EXPECTED_ROOTS,
        "solver_calls_per_implementation": EXPECTED_CALLS,
        "empty_signatures": EXPECTED_EMPTY,
        "base_pair_closed": EXPECTED_CLOSED,
        "violations": 0,
        "core_stream_sha256": EXPECTED_CORE_SHA256,
        "transcript_sha256": EXPECTED_TRANSCRIPT_SHA256,
        "result": (
            "Every nonempty root signature in every vertex-deleted "
            "triangle-free 3-connected non-Tait simple cubic cap of "
            "orders 20, 22, and 24 contains a base pair."
        ),
        "warning": (
            "Canonical source completeness relies on Snarkhunter. "
            "The exceptional-pole consequence also uses the human "
            "triangle induction, cap reductions, and cyclically-four "
            "cap census. This is not Five-CDC."
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
