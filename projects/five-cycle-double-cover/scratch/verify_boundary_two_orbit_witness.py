#!/usr/bin/env python3
"""Independently check two-orbit D5 witnesses for four-pole streams."""

from __future__ import annotations

from contextlib import contextmanager
from itertools import permutations
from pathlib import Path
import argparse
import gzip
import hashlib
import json


D5 = tuple(value for value in range(32) if value.bit_count() == 2)
EXCEPTIONAL = (0x02B, 0x053, 0x119, 0x2E4, 0x3A4, 0x3C4)
CERTIFICATE_ORBITS = (0, 2)


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


def decode_graph6(record: bytes) -> tuple[int, list[tuple[int, int]]]:
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
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, edges


@contextmanager
def open_binary(path: Path):
    if path.suffix == ".gz":
        with gzip.open(path, "rb") as handle:
            yield handle
    else:
        with path.open("rb") as handle:
            yield handle


def check_witness(
    record: bytes,
    encoded: bytes,
    orbit: int,
    representatives: tuple[tuple[int, ...], ...],
    row_number: int,
) -> None:
    vertices, edges = decode_graph6(record)
    incidence = [[] for _ in range(vertices)]
    for edge_id, (left, right) in enumerate(edges):
        incidence[left].append(edge_id)
        incidence[right].append(edge_id)
    terminals = [
        vertex for vertex, incident_edges in enumerate(incidence)
        if len(incident_edges) == 2
    ]
    if len(terminals) != 4 or any(len(row) not in (2, 3) for row in incidence):
        raise SystemExit(f"row {row_number}: input is not a cubic four-pole")

    total_edges = len(edges) + 4
    if encoded == b"-":
        raise SystemExit(f"row {row_number}: missing orbit-{orbit} witness")
    if len(encoded) != total_edges or any(not 48 <= byte <= 57 for byte in encoded):
        raise SystemExit(f"row {row_number}: malformed orbit-{orbit} witness")
    labels = [D5[byte - 48] for byte in encoded]
    expected_boundary = representatives[orbit]
    if tuple(labels[len(edges):]) != expected_boundary:
        raise SystemExit(f"row {row_number}: wrong orbit-{orbit} boundary")

    for position, terminal in enumerate(terminals):
        incidence[terminal].append(len(edges) + position)
    for vertex, incident_edges in enumerate(incidence):
        if len(incident_edges) != 3:
            raise SystemExit(f"row {row_number}: bad incidence at vertex {vertex}")
        value = 0
        for edge in incident_edges:
            value ^= labels[edge]
        if value:
            raise SystemExit(
                f"row {row_number}: orbit-{orbit} parity failure at vertex {vertex}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("poles", type=Path)
    parser.add_argument("witnesses", type=Path)
    arguments = parser.parse_args()

    for mask in EXCEPTIONAL:
        if not any((mask >> orbit & 1) == 0 for orbit in CERTIFICATE_ORBITS):
            raise SystemExit("certificate orbits do not exclude every mask")

    representatives = orbit_representatives()
    pole_hash = hashlib.sha256()
    witness_hash = hashlib.sha256()
    rows = 0
    with open_binary(arguments.poles) as pole_file, open_binary(
        arguments.witnesses
    ) as witness_file:
        for row_number, pole_line in enumerate(pole_file, start=1):
            witness_line = witness_file.readline()
            if not witness_line:
                raise SystemExit(f"short witness stream at row {row_number}")
            pole_hash.update(pole_line)
            witness_hash.update(witness_line)
            record = pole_line.rstrip(b"\n")
            fields = witness_line.rstrip(b"\n").split(b"\t")
            if len(fields) != 3 or fields[0] != record:
                raise SystemExit(f"row {row_number}: witness/pole mismatch")
            check_witness(
                record, fields[1], CERTIFICATE_ORBITS[0],
                representatives, row_number
            )
            check_witness(
                record, fields[2], CERTIFICATE_ORBITS[1],
                representatives, row_number
            )
            rows += 1
        if witness_file.readline():
            raise SystemExit("long witness stream")

    result = {
        "schema": "boundary-two-orbit-witness-replay-v1",
        "classification": "INDEPENDENT EXPLICIT D5 WITNESS CHECK",
        "rows": rows,
        "witnesses": 2 * rows,
        "certificate_orbits": list(CERTIFICATE_ORBITS),
        "exceptional_masks_excluded": [f"0x{mask:03x}" for mask in EXCEPTIONAL],
        "pole_stream_sha256": pole_hash.hexdigest(),
        "witness_stream_sha256": witness_hash.hexdigest(),
        "status": "PASS",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
