#!/usr/bin/env python3
"""Independent audit of the non-Tait endpoint rooted-three-pole screen."""

from __future__ import annotations

from collections import deque
from itertools import combinations, zip_longest
import gzip
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
SOURCES = (
    (20, 6, "a65153d9dc38bebffca52b2c2ec05f194807b10ca097f50a551d5aab871244f1"),
    (22, 31, "b75b970d99382cf03493c8693b26786e5fcf7189b57cbb3cb1bebb451577682c"),
    (24, 155, "37ef068ab597c6cc882eb2121d9743464b0717bc4beefab4348ef4221b6a7456"),
    (26, 1_297, "1d2b95b9d412f5f6b8ccb788779bd685df23b3239bda8c7e9557266375519760"),
)
EXPECTED_CORES = 38_244
EXPECTED_CORE_SHA256 = (
    "3b7c3951f681545daa5afba3b5a0ca19af041f966ff9024a85483bdb8d476ec2"
)
EXPECTED_ROOTS = 1_360_452
EXPECTED_CALLS = 4_157_844
EXPECTED_TRANSCRIPT_SHA256 = (
    "bfb90fd89b43e66f02ada87abcb87ab643d87a4b36dba616cd1f3e5d603b7364"
)
SHARDS = "abcdef"
EXPECTED_GRAPHS_PER_SHARD = EXPECTED_CORES // len(SHARDS)
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
    edges = []
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
    if len(components(vertices, adjacency, set())) != 1:
        raise SystemExit(f"order {order} row {row_number}: disconnected")

    for skipped, (source, target) in enumerate(edges):
        distance = {source: 0}
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            if distance[vertex] == 2:
                continue
            for other, edge_id in adjacency[vertex]:
                if edge_id == skipped or other in distance:
                    continue
                distance[other] = distance[vertex] + 1
                queue.append(other)
        if target in distance and distance[target] <= 2:
            raise SystemExit(f"order {order} row {row_number}: triangle")

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
                    f"order {order} row {row_number}: cyclic cut below four"
                )
    if three_edge_colourable(vertices, edges):
        raise SystemExit(f"order {order} row {row_number}: Tait colouring")
    return edges


def delete_vertex(
    vertices: int, edges: list[tuple[int, int]], deleted: int
) -> bytes:
    relabel = {}
    cursor = 0
    for vertex in range(vertices):
        if vertex == deleted:
            continue
        relabel[vertex] = cursor
        cursor += 1
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
        path = ARTIFACTS / f"cyclic4-nontait-order{order}.g6"
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
        # Different orders cannot share a graph6 record, so this is mostly a
        # guard against accidental repeated files.
        raise SystemExit("source streams overlap")

    core_data = gzip.decompress(
        (ARTIFACTS / "vertex-deleted-cores-through26.g6.gz").read_bytes()
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
    with gzip.open(ARTIFACTS / "cadical-transcript.tsv.gz", "rb") as left, gzip.open(
        ARTIFACTS / "csp-transcript.tsv.gz", "rb"
    ) as right:
        rows = zip_longest(left, right)
        for core in core_data.splitlines():
            vertices, edges = decode_graph6(core)
            incidence, adjacency = graph_data(vertices, edges)
            if sorted(map(len, incidence)).count(2) != 3:
                raise SystemExit("expanded core does not have three terminals")
            if any(len(row) not in (2, 3) for row in incidence):
                raise SystemExit("expanded core has wrong degree")
            for root in range(len(edges)):
                if is_bridge(vertices, edges, adjacency, root):
                    continue
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
                if record != core or int(root_text) != root or category != b"1":
                    raise SystemExit(f"wrong decision at root row {roots + 1}")
                queried = int(queried_text, 16)
                observed = int(observed_text, 16)
                if observed & ~queried:
                    raise SystemExit(f"unqueried positive orbit at row {roots + 1}")
                if not any(observed & mask == mask for mask in BASE_PAIR_MASKS):
                    raise SystemExit(f"no base pair at root row {roots + 1}")
                calls += sum(
                    ORBIT_SIZES[orbit]
                    for orbit in range(7)
                    if queried >> orbit & 1
                )
                roots += 1
        extra_left, extra_right = next(rows, (None, None))
        if extra_left is not None or extra_right is not None:
            raise SystemExit("long transcript")

    if roots != EXPECTED_ROOTS or calls != EXPECTED_CALLS:
        raise SystemExit("unexpected root or solver-call total")
    if transcript_hash.hexdigest() != EXPECTED_TRANSCRIPT_SHA256:
        raise SystemExit("transcript digest mismatch")

    for implementation in ("cadical", "csp"):
        totals = {
            "graphs": 0,
            "roots": 0,
            "empty": 0,
            "closed": 0,
            "violations": 0,
            "calls": 0,
        }
        for shard in SHARDS:
            status = (
                ARTIFACTS / f"{implementation}-shard{shard}.status"
            ).read_text(encoding="utf-8")
            if status != "0\n":
                raise SystemExit(
                    f"{implementation} shard {shard}: nonzero status"
                )
            summary = parse_summary(implementation, shard)
            if summary["graphs"] != EXPECTED_GRAPHS_PER_SHARD:
                raise SystemExit(
                    f"{implementation} shard {shard}: wrong graph count"
                )
            for key, value in summary.items():
                totals[key] += value
        expected_totals = {
            "graphs": EXPECTED_CORES,
            "roots": EXPECTED_ROOTS,
            "empty": 0,
            "closed": EXPECTED_ROOTS,
            "violations": 0,
            "calls": EXPECTED_CALLS,
        }
        if totals != expected_totals:
            raise SystemExit(f"{implementation}: wrong aggregate summary")

    result = {
        "schema": "five-cdc-rooted-nontait-endpoint-through26-v1",
        "classification": "FINITE TWO-IMPLEMENTATION ROOTED CLASSIFICATION",
        "source_caps": source_total,
        "vertex_deleted_cores": EXPECTED_CORES,
        "nonbridge_roots": EXPECTED_ROOTS,
        "solver_calls_per_implementation": EXPECTED_CALLS,
        "empty_signatures": 0,
        "base_pair_closed": EXPECTED_ROOTS,
        "violations": 0,
        "core_stream_sha256": EXPECTED_CORE_SHA256,
        "transcript_sha256": EXPECTED_TRANSCRIPT_SHA256,
        "result": (
            "Every nonbridge root in every vertex-deleted cyclically "
            "4-edge-connected non-Tait simple cubic factor of orders "
            "20, 22, 24, and 26 has a fixed-five root signature "
            "containing a base pair."
        ),
        "warning": (
            "Canonical source completeness relies on Snarkhunter. The "
            "cyclic-three order bounds also use the human Tait-cap, "
            "cap-connectivity, three-sum path, and earlier "
            "rooted-order-17 reductions. "
            "This is not universal base-pair closure or Five-CDC."
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
