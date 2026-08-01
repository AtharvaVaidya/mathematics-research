#!/usr/bin/env python3
"""Reproduce 13 exact order-16 triangle-expansion descent rows."""

from __future__ import annotations

import concurrent.futures
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scratch" / "search_jaeger_star_parity_descent.cpp"
BASE_GRAPH6 = "M?AA@BORDGEOEOAo?"
OUTPUT = (
    ROOT
    / "output"
    / "jaeger-fano-min-descent-triangle-expansions-16v"
    / "census.jsonl"
)


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    order = ord(record[0]) - 63
    assert 0 < order <= 62
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    cursor = 0
    edges: list[tuple[int, int]] = []
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def encode_graph6(
    order: int, edges: tuple[tuple[int, int], ...]
) -> str:
    edge_set = {tuple(sorted(edge)) for edge in edges}
    bits = [
        int((left, right) in edge_set)
        for right in range(1, order)
        for left in range(right)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = 2 * value + bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def expanded_graph6(vertex: int) -> str:
    order, base_edges = parse_graph6(BASE_GRAPH6)
    assert order == 14
    neighbours = [
        right if left == vertex else left
        for left, right in base_edges
        if vertex in (left, right)
    ]
    expanded = [edge for edge in base_edges if vertex not in edge]
    expanded.extend(((14, 15), (15, 16), (16, 14)))
    expanded.extend(zip((14, 15, 16), neighbours))
    labels = sorted({endpoint for edge in expanded for endpoint in edge})
    relabel = {old: new for new, old in enumerate(labels)}
    edges = tuple(
        sorted(
            tuple(sorted((relabel[left], relabel[right])))
            for left, right in expanded
        )
    )
    return encode_graph6(16, edges)


def run_row(binary: Path, vertex: int) -> dict[str, object]:
    graph6 = expanded_graph6(vertex)
    completed = subprocess.run(
        [str(binary), "--root", "0", "--objective", "seven"],
        input=graph6 + "\n",
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [
        json.loads(line) for line in completed.stdout.splitlines() if line
    ]
    assert len(rows) == 1
    row = rows[0]
    row["expanded_vertex"] = vertex
    return row


def main() -> None:
    with tempfile.TemporaryDirectory(
        prefix="jaeger-triangle-descent-"
    ) as directory:
        binary = Path(directory) / "descent"
        subprocess.run(
            [
                "/usr/bin/clang++",
                "-O3",
                "-std=c++20",
                "-Wall",
                "-Wextra",
                "-pedantic",
                str(SOURCE),
                "-o",
                str(binary),
            ],
            check=True,
        )
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            rows = list(pool.map(lambda vertex: run_row(binary, vertex), range(1, 14)))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(
                json.dumps(row, sort_keys=True, separators=(",", ":"))
            )
            stream.write("\n")
    print(
        json.dumps(
            {
                "rows": len(rows),
                "states": sum(int(row["states"]) for row in rows),
                "failures": sum(bool(row["failure"]) for row in rows),
                "maximum_d_min": max(int(row["max_score"]) for row in rows),
                "output": str(OUTPUT.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
