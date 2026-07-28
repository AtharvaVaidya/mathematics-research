#!/usr/bin/env python3
"""Generate deterministic connected 2-lifts of simple graph6 records.

The voltage bit of each base edge is derived from SHA-256, so a seed and
input record reproduce the same sequence without relying on a PRNG library.
Only connected lifts are emitted.  A cover of a bridgeless graph is
bridgeless, but the downstream checker recomputes bridgelessness directly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from search.canonical.canonical_search import parse_graph6, validate_simple_cubic


def encode_order(n: int) -> list[int]:
    if 0 <= n <= 62:
        return [n]
    if n <= 258047:
        return [63, (n >> 12) & 63, (n >> 6) & 63, n & 63]
    if n <= (1 << 36) - 1:
        return [63, 63] + [(n >> shift) & 63 for shift in range(30, -1, -6)]
    raise ValueError("graph too large for graph6")


def encode_graph6(n: int, edges: list[tuple[int, int]]) -> str:
    edge_set = {tuple(sorted(edge)) for edge in edges}
    if len(edge_set) != len(edges):
        raise ValueError("loop or duplicate edge")
    bits: list[int] = []
    for v in range(1, n):
        for u in range(v):
            bits.append(int((u, v) in edge_set))
    while len(bits) % 6:
        bits.append(0)
    chunks = [
        sum(bits[at + bit] << (5 - bit) for bit in range(6))
        for at in range(0, len(bits), 6)
    ]
    return "".join(chr(value + 63) for value in encode_order(n) + chunks)


def voltage_bits(base: str, edges: int, seed: str, counter: int) -> list[int]:
    bits: list[int] = []
    block = 0
    while len(bits) < edges:
        payload = f"{seed}\0{base}\0{counter}\0{block}".encode("ascii")
        digest = hashlib.sha256(payload).digest()
        bits.extend((byte >> bit) & 1 for byte in digest for bit in range(8))
        block += 1
    return bits[:edges]


def lifted_edges(
    base_edges: tuple[tuple[int, int], ...], voltages: list[int]
) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    for (u, v), voltage in zip(base_edges, voltages, strict=True):
        for sheet in range(2):
            result.append(
                tuple(sorted((2 * u + sheet, 2 * v + (sheet ^ voltage))))
            )
    return sorted(result)


def is_connected(n: int, edges: list[tuple[int, int]]) -> bool:
    adjacency: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    reached = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other in adjacency[vertex]:
            if other not in reached:
                reached.add(other)
                stack.append(other)
    return len(reached) == n


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--g6-output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--lifts-per-base", type=int, default=1)
    parser.add_argument("--seed", default="direct-fivecdc-20260728")
    arguments = parser.parse_args()
    if arguments.lifts_per_base <= 0:
        raise ValueError("lifts-per-base must be positive")

    bases = [
        line.strip()
        for line in arguments.input.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    records: list[str] = []
    metadata: list[dict[str, object]] = []
    for base_index, base in enumerate(bases, 1):
        graph = parse_graph6(base)
        checks = validate_simple_cubic(graph)
        if not all(checks[key] for key in ("simple", "cubic", "connected", "bridgeless")):
            raise ValueError(f"base row {base_index} fails premises: {checks}")
        emitted = 0
        counter = 0
        while emitted < arguments.lifts_per_base:
            voltages = voltage_bits(base, len(graph.edges), arguments.seed, counter)
            edges = lifted_edges(graph.edges, voltages)
            if is_connected(2 * graph.vertices, edges):
                record = encode_graph6(2 * graph.vertices, edges)
                # Round-trip through the independent existing parser.
                decoded = parse_graph6(record)
                if decoded.vertices != 2 * graph.vertices or decoded.edges != tuple(edges):
                    raise AssertionError("graph6 round trip failed")
                records.append(record)
                metadata.append(
                    {
                        "base_index": base_index,
                        "base_graph6": base,
                        "counter": counter,
                        "lift_graph6": record,
                        "voltage_hex": hex(
                            sum(bit << edge for edge, bit in enumerate(voltages))
                        ),
                    }
                )
                emitted += 1
            counter += 1

    arguments.g6_output.write_text("\n".join(records) + "\n", encoding="ascii")
    arguments.metadata.write_text(
        "\n".join(json.dumps(row, sort_keys=True) for row in metadata) + "\n",
        encoding="ascii",
    )
    print(
        json.dumps(
            {
                "bases": len(bases),
                "lifts_per_base": arguments.lifts_per_base,
                "records": len(records),
                "seed": arguments.seed,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
