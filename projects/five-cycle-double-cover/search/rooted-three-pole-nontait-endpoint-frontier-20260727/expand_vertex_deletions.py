#!/usr/bin/env python3
"""Expand cubic graph6 caps into all one-vertex-deleted three-poles."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


def decode_graph6(record: bytes) -> tuple[int, list[tuple[int, int]]]:
    if not record or record[0] == 126:
        raise ValueError("only short graph6 records are supported")
    vertices = record[0] - 63
    if not 0 <= vertices <= 62:
        raise ValueError("invalid graph order")
    bits: list[int] = []
    for character in record[1:]:
        value = character - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = vertices * (vertices - 1) // 2
    if len(bits) < needed or any(bits[needed:]):
        raise ValueError("malformed graph6 padding")
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("sources", nargs="+", type=Path)
    args = parser.parse_args()

    graphs = 0
    cores = 0
    by_order: dict[int, list[int]] = {}
    output = sys.stdout.buffer
    for source in args.sources:
        source_graphs = 0
        source_cores = 0
        for line_number, record in enumerate(
            source.read_bytes().splitlines(), start=1
        ):
            vertices, edges = decode_graph6(record)
            incidence = [0] * vertices
            for left, right in edges:
                incidence[left] += 1
                incidence[right] += 1
            if len(edges) != 3 * vertices // 2 or any(
                degree != 3 for degree in incidence
            ):
                raise SystemExit(
                    f"{source}:{line_number}: source is not cubic"
                )
            for deleted in range(vertices):
                output.write(delete_vertex(vertices, edges, deleted) + b"\n")
                cores += 1
                source_cores += 1
            graphs += 1
            source_graphs += 1
        by_order.setdefault(vertices, [0, 0])
        by_order[vertices][0] += source_graphs
        by_order[vertices][1] += source_cores

    detail = ",".join(
        f"{order}:{counts[0]}:{counts[1]}"
        for order, counts in sorted(by_order.items())
    )
    print(
        f"SUMMARY graphs={graphs} cores={cores} by_order={detail}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
