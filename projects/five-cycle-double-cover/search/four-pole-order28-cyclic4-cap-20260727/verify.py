#!/usr/bin/env python3
"""Independent replay of the order-28 two-orbit witness package."""

from __future__ import annotations

from collections import deque
from itertools import permutations
from pathlib import Path
import gzip
import hashlib
import json
import re


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
EXPECTED_SOURCE_ROWS = 12_517
EXPECTED_SOURCE_SHA256 = (
    "b4f6494c23793a40158a03ccd7c0943ae2e397c90a1467e27814bd007789be1f"
)
EXPECTED_POLE_ROWS = 9_725_709
EXPECTED_POLE_SHA256 = (
    "f42168e2786bdee409304e9e7b167ae0a0e250c78e7c2413e55ee56f5627a839"
)
EXPECTED_WITNESS_SHA256 = (
    "658374b00418fa626da704670689f4dfad25cf740121509a725da4158491ef7d"
)
SHARD_SOURCE_ROWS = (1_565,) * 5 + (1_564,) * 3
SHARD_POLE_ROWS = (1_216_005,) * 5 + (1_215_228,) * 3
SUMMARY = re.compile(
    r"^SUMMARY implementation=cadical mode=two-orbit-witness "
    r"rows=(\d+) queries=(\d+) witnesses=(\d+) missing=(\d+)$"
)
D5 = tuple(value for value in range(32) if value.bit_count() == 2)
EXCEPTIONAL = (0x02B, 0x053, 0x119, 0x2E4, 0x3A4, 0x3C4)
CERTIFICATE_ORBITS = (0, 2)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for coordinate in range(5):
        if mask >> coordinate & 1:
            result |= 1 << permutation[coordinate]
    return result


def canonical_word(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(permute_mask(mask, permutation) for mask in word)
        for permutation in permutations(range(5))
    )


def orbit_representatives() -> tuple[tuple[int, ...], ...]:
    representatives = {
        canonical_word((first, second, third, first ^ second ^ third))
        for first in D5
        for second in D5
        for third in D5
        if (first ^ second ^ third).bit_count() == 2
    }
    result = tuple(sorted(representatives))
    if len(result) != 10:
        raise SystemExit("expected ten boundary orbits")
    return result


def decode_graph6(
    record: bytes,
) -> tuple[int, list[tuple[int, int]], list[int]]:
    if not record or record[0] == 126:
        raise SystemExit("only short graph6 records are supported")
    vertices = record[0] - 63
    if not 0 <= vertices <= 62:
        raise SystemExit("bad graph order")
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
    positions = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
                positions.append(cursor)
            cursor += 1
    return vertices, edges, positions


def clear_two_edges(record: bytes, first: int, second: int) -> bytes:
    result = bytearray(record)
    for position in (first, second):
        byte = 1 + position // 6
        bit = 1 << (5 - position % 6)
        value = result[byte] - 63
        if not value & bit:
            raise SystemExit("attempted to clear an absent graph6 edge")
        result[byte] = (value ^ bit) + 63
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


def connected(
    vertices: int,
    adjacency: list[list[tuple[int, int]]],
    removed_edge: int = -1,
) -> bool:
    reached = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other, edge in adjacency[vertex]:
            if edge == removed_edge or other in reached:
                continue
            reached.add(other)
            stack.append(other)
    return len(reached) == vertices


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


def check_source(record_number: int, record: bytes) -> tuple[
    list[tuple[int, int]], list[int]
]:
    vertices, edges, positions = decode_graph6(record)
    incidence, adjacency = graph_data(vertices, edges)
    if vertices != 28 or len(edges) != 42:
        raise SystemExit(f"source row {record_number}: wrong order or size")
    if any(len(row) != 3 for row in incidence):
        raise SystemExit(f"source row {record_number}: not cubic")
    if not connected(vertices, adjacency):
        raise SystemExit(f"source row {record_number}: disconnected")
    for edge in range(len(edges)):
        if not connected(vertices, adjacency, edge):
            raise SystemExit(f"source row {record_number}: bridge")
    neighbour_sets = [
        {other for other, _ in adjacency[vertex]} for vertex in range(vertices)
    ]
    if any(neighbour_sets[left] & neighbour_sets[right] for left, right in edges):
        raise SystemExit(f"source row {record_number}: triangle")
    if three_edge_colourable(vertices, edges):
        raise SystemExit(f"source row {record_number}: Tait colouring")
    return edges, positions


def check_model(
    encoded: bytes,
    retained: list[tuple[int, int]],
    terminals: list[int],
    boundary: tuple[int, ...],
    row_number: int,
    orbit: int,
) -> None:
    total_edges = len(retained) + 4
    if encoded == b"-":
        raise SystemExit(f"row {row_number}: missing orbit-{orbit} witness")
    if len(encoded) != total_edges or any(not 48 <= byte <= 57 for byte in encoded):
        raise SystemExit(f"row {row_number}: malformed orbit-{orbit} witness")
    labels = [D5[byte - 48] for byte in encoded]
    if tuple(labels[len(retained):]) != boundary:
        raise SystemExit(f"row {row_number}: wrong orbit-{orbit} boundary")
    vertex_sums = [0] * 28
    for label, (left, right) in zip(labels, retained):
        vertex_sums[left] ^= label
        vertex_sums[right] ^= label
    for label, terminal in zip(labels[len(retained):], terminals):
        vertex_sums[terminal] ^= label
    if any(vertex_sums):
        vertex = next(index for index, value in enumerate(vertex_sums) if value)
        raise SystemExit(
            f"row {row_number}: orbit-{orbit} parity failure at vertex {vertex}"
        )


def parse_log(shard: int) -> dict[str, int]:
    path = ARTIFACTS / f"shard{shard}-witness.log"
    matches = [
        match
        for line in path.read_text(encoding="utf-8").splitlines()
        if (match := SUMMARY.fullmatch(line))
    ]
    if len(matches) != 1:
        raise SystemExit(f"{path}: malformed summary")
    return {
        "rows": int(matches[0].group(1)),
        "queries": int(matches[0].group(2)),
        "witnesses": int(matches[0].group(3)),
        "missing": int(matches[0].group(4)),
    }


def main() -> int:
    for mask in EXCEPTIONAL:
        if not any((mask >> orbit & 1) == 0 for orbit in CERTIFICATE_ORBITS):
            raise SystemExit("certificate orbits do not exclude every mask")
    representatives = orbit_representatives()
    if representatives[0] != (3, 3, 3, 3):
        raise SystemExit("orbit zero is not AA")
    if representatives[2] != (3, 3, 12, 12):
        raise SystemExit("orbit two is not the prescribed disjoint doubled type")

    snarkhunter_log = (ARTIFACTS / "snarkhunter.log").read_text(
        encoding="utf-8"
    )
    if (
        "snarkhunter 28 4 S s C4 o g" not in snarkhunter_log
        or "All done, 12517 graphs generated with 28 vertices."
        not in snarkhunter_log
    ):
        raise SystemExit("malformed Snarkhunter log")
    if (ARTIFACTS / "expand.log").read_text(encoding="utf-8") != (
        "SUMMARY graphs=12517 poles=9725709\n"
    ):
        raise SystemExit("malformed expansion log")

    source = (ARTIFACTS / "cyclic4-nontait-order28.g6").read_bytes()
    source_records = source.splitlines()
    if (
        len(source_records) != EXPECTED_SOURCE_ROWS
        or len(set(source_records)) != EXPECTED_SOURCE_ROWS
        or sha256(source) != EXPECTED_SOURCE_SHA256
    ):
        raise SystemExit("wrong, duplicate, or corrupted source records")

    for shard, expected_rows in enumerate(SHARD_POLE_ROWS):
        status = (ARTIFACTS / f"shard{shard}.status").read_text(
            encoding="utf-8"
        )
        if status != "0\n":
            raise SystemExit(f"shard {shard}: nonzero status")
        summary = parse_log(shard)
        expected = {
            "rows": expected_rows,
            "queries": 2 * expected_rows,
            "witnesses": 2 * expected_rows,
            "missing": 0,
        }
        if summary != expected:
            raise SystemExit(f"shard {shard}: wrong summary")

    pole_hash = hashlib.sha256()
    witness_hash = hashlib.sha256()
    rows = 0
    pole_path = ARTIFACTS / "cyclic4-nontait-order28-poles.g6.gz"
    witness_path = ARTIFACTS / "cadical-two-orbit-witness.tsv.gz"
    with gzip.open(pole_path, "rb") as pole_file, gzip.open(
        witness_path, "rb"
    ) as witness_file:
        for source_number, source_record in enumerate(source_records, start=1):
            edges, positions = check_source(source_number, source_record)
            for first, (a, b) in enumerate(edges):
                for second in range(first + 1, len(edges)):
                    c, d = edges[second]
                    if len({a, b, c, d}) != 4:
                        continue
                    expected_record = clear_two_edges(
                        source_record, positions[first], positions[second]
                    )
                    pole_line = pole_file.readline()
                    witness_line = witness_file.readline()
                    if not pole_line or not witness_line:
                        raise SystemExit(f"short artifact stream at row {rows + 1}")
                    pole_hash.update(pole_line)
                    witness_hash.update(witness_line)
                    pole_record = pole_line.rstrip(b"\n")
                    if pole_record != expected_record:
                        raise SystemExit(f"wrong pole expansion at row {rows + 1}")
                    fields = witness_line.rstrip(b"\n").split(b"\t")
                    if len(fields) != 3 or fields[0] != pole_record:
                        raise SystemExit(f"witness/pole mismatch at row {rows + 1}")
                    retained = [
                        edge
                        for edge_id, edge in enumerate(edges)
                        if edge_id not in (first, second)
                    ]
                    terminals = sorted((a, b, c, d))
                    check_model(
                        fields[1],
                        retained,
                        terminals,
                        representatives[CERTIFICATE_ORBITS[0]],
                        rows + 1,
                        CERTIFICATE_ORBITS[0],
                    )
                    check_model(
                        fields[2],
                        retained,
                        terminals,
                        representatives[CERTIFICATE_ORBITS[1]],
                        rows + 1,
                        CERTIFICATE_ORBITS[1],
                    )
                    rows += 1
        if pole_file.readline() or witness_file.readline():
            raise SystemExit("long artifact stream")

    if rows != EXPECTED_POLE_ROWS:
        raise SystemExit("wrong pole row count")
    if pole_hash.hexdigest() != EXPECTED_POLE_SHA256:
        raise SystemExit("pole stream digest mismatch")
    if witness_hash.hexdigest() != EXPECTED_WITNESS_SHA256:
        raise SystemExit("witness stream digest mismatch")

    report = {
        "schema": "five-cdc-order28-cyclic4-two-witness-v1",
        "classification": "FINITE EXPLICIT-WITNESS CLASSIFICATION",
        "source_graphs": EXPECTED_SOURCE_ROWS,
        "independent_edge_deletions": EXPECTED_POLE_ROWS,
        "certificate_orbits": list(CERTIFICATE_ORBITS),
        "explicit_d5_witnesses": 2 * EXPECTED_POLE_ROWS,
        "exceptional_hits": 0,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "pole_stream_sha256": EXPECTED_POLE_SHA256,
        "witness_stream_sha256": EXPECTED_WITNESS_SHA256,
        "result": (
            "Every independent-edge deletion pole from the retained "
            "12,517 cyclically 4-edge-connected non-Tait order-28 caps "
            "realizes AA and the fixed disjoint doubled boundary orbit. "
            "No pole has one of the six exceptional fixed-five signatures."
        ),
        "warning": (
            "Completeness and cyclic-4 provenance of the source rely on "
            "the retained Snarkhunter run. The checker independently "
            "checks every source for cubicity, connectedness, "
            "bridgelessness, triangle-freeness, and non-Taitness, "
            "reconstructs every deletion pole, and checks every displayed "
            "D5 labelling. This is not Five-CDC."
        ),
    }
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
