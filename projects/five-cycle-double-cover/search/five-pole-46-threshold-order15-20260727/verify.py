#!/usr/bin/env python3
"""Structural and optional full replay of the order-15 threshold screen."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
EXPECTED_SHARD_ROWS = (11266, 8327, 8753, 7932, 5318, 4367, 14213, 9067)
EXPECTED_TOTAL = 69243


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    if not record or record[0] == "~":
        raise ValueError("unsupported graph6 record")
    order = ord(record[0]) - 63
    if not 0 <= order <= 62:
        raise ValueError("only short graph6 records are supported")
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    required = order * (order - 1) // 2
    if len(bits) < required or any(bits[required:]):
        raise ValueError("bad graph6 payload or padding")
    edges = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def bridge_count(order: int, edges: tuple[tuple[int, int], ...]) -> int:
    incident: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge_id, (left, right) in enumerate(edges):
        incident[left].append((right, edge_id))
        incident[right].append((left, edge_id))
    entered = [-1] * order
    low = [-1] * order
    clock = 0
    bridges = 0

    def visit(vertex: int, parent_edge: int) -> None:
        nonlocal clock, bridges
        entered[vertex] = low[vertex] = clock
        clock += 1
        for other, edge_id in incident[vertex]:
            if edge_id == parent_edge:
                continue
            if entered[other] < 0:
                visit(other, edge_id)
                low[vertex] = min(low[vertex], low[other])
                bridges += low[other] > entered[vertex]
            else:
                low[vertex] = min(low[vertex], entered[other])

    visit(0, -1)
    if any(value < 0 for value in entered):
        raise AssertionError("record is disconnected")
    return bridges


def read_results() -> tuple[tuple[str, ...], tuple[bytes, ...]]:
    records: list[str] = []
    payloads: list[bytes] = []
    seen: set[str] = set()
    for shard, expected_rows in enumerate(EXPECTED_SHARD_ROWS):
        path = RESULTS / f"fivepole-order15-shard-{shard}.tsv"
        raw = path.read_bytes()
        payloads.append(raw)
        lines = raw.decode("ascii").splitlines()
        if len(lines) != expected_rows:
            raise AssertionError(f"wrong row count in shard {shard}")
        for line in lines:
            fields = line.split("\t")
            if len(fields) != 3:
                raise AssertionError("bad transcript row")
            record, count_text, mask_text = fields
            if record in seen:
                raise AssertionError("duplicate graph6 record")
            seen.add(record)
            if int(count_text) != 46 or int(mask_text, 16).bit_count() != 46:
                raise AssertionError("record did not reach the 46-state threshold")
            order, edges = parse_graph6(record)
            if order != 15 or len(edges) != 20:
                raise AssertionError("wrong graph order or size")
            degrees = [0] * order
            for left, right in edges:
                degrees[left] += 1
                degrees[right] += 1
            if sorted(degrees) != [2] * 5 + [3] * 10:
                raise AssertionError("wrong terminal/degree profile")
            if bridge_count(order, edges):
                raise AssertionError("proper core has a bridge")
            records.append(record)
    if len(records) != EXPECTED_TOTAL:
        raise AssertionError("wrong aggregate record count")
    return tuple(records), tuple(payloads)


def verify_metadata_and_manifest() -> None:
    report = json.loads((HERE / "report.json").read_text(encoding="utf-8"))
    if report["status"] != "PASS":
        raise AssertionError("report status is not PASS")
    if report["scope"]["canonical_records"] != EXPECTED_TOTAL:
        raise AssertionError("report record count differs")
    if report["result"]["records_below_46"] != 0:
        raise AssertionError("report claims a below-threshold record")
    if report["boundary_encoding"]["stopping_threshold"] != 46:
        raise AssertionError("report threshold differs")

    manifest_path = HERE / "SHA256SUMS"
    expected: dict[Path, str] = {}
    for line in manifest_path.read_text(encoding="ascii").splitlines():
        digest, relative = line.split("  ", 1)
        path = HERE / relative
        if path in expected:
            raise AssertionError("duplicate manifest path")
        expected[path] = digest
    actual_paths = {
        path
        for path in HERE.rglob("*")
        if path.is_file()
        and path.name != "SHA256SUMS"
        and "__pycache__" not in path.parts
    }
    if set(expected) != actual_paths:
        raise AssertionError("manifest path set differs from package files")
    for path, digest in expected.items():
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise AssertionError(f"checksum mismatch: {path.relative_to(HERE)}")


def generated_shards(geng: str) -> tuple[bytes, ...]:
    payloads = []
    for shard in range(8):
        completed = subprocess.run(
            [
                geng,
                "-Cq",
                "-d2",
                "-D3",
                "15",
                "20:20",
                f"{shard}/8",
            ],
            check=True,
            capture_output=True,
        )
        payloads.append(completed.stdout)
    return tuple(payloads)


def compile_classifier(directory: Path) -> Path:
    compiler = shutil.which("c++")
    if compiler is None:
        raise RuntimeError("c++ is required for --replay")
    include_candidates = (
        Path("/opt/homebrew/include"),
        Path("/usr/local/include"),
        Path("/usr/include"),
    )
    library_candidates = (
        Path("/opt/homebrew/lib/libcadical.a"),
        Path("/usr/local/lib/libcadical.a"),
        Path("/usr/lib/libcadical.a"),
    )
    include = next(
        (path for path in include_candidates if (path / "cadical.hpp").exists()),
        None,
    )
    library = next((path for path in library_candidates if path.exists()), None)
    if include is None or library is None:
        raise RuntimeError("CaDiCaL headers/static library are required for --replay")
    binary = directory / "classifier"
    subprocess.run(
        [
            compiler,
            "-O3",
            "-std=c++17",
            f"-I{include}",
            str(HERE / "primary_classifier.cpp"),
            str(library),
            "-o",
            str(binary),
        ],
        check=True,
    )
    return binary


def replay_classifier(generated: tuple[bytes, ...], expected: tuple[bytes, ...]) -> None:
    with tempfile.TemporaryDirectory(prefix="five-pole-order15-replay-") as raw:
        binary = compile_classifier(Path(raw))
        for shard, (corpus, transcript) in enumerate(zip(generated, expected)):
            completed = subprocess.run(
                [str(binary), "--terminals", "5", "--stop-at", "46"],
                input=corpus,
                check=True,
                capture_output=True,
            )
            if completed.stdout != transcript:
                raise AssertionError(f"classifier replay differs on shard {shard}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", action="store_true")
    arguments = parser.parse_args()

    verify_metadata_and_manifest()
    records, expected_payloads = read_results()
    geng = shutil.which("geng")
    if geng is None:
        raise RuntimeError("nauty geng is required")
    generated_payloads = generated_shards(geng)
    generated_records = tuple(
        line.decode("ascii")
        for payload in generated_payloads
        for line in payload.splitlines()
        if line
    )
    if set(generated_records) != set(records):
        raise AssertionError("fresh canonical corpus differs from retained records")
    if arguments.replay:
        replay_classifier(generated_payloads, expected_payloads)

    print(
        {
            "status": "PASS",
            "mode": "full-replay" if arguments.replay else "structural",
            "records": len(records),
            "threshold": 46,
            "shard_sha256": [
                hashlib.sha256(payload).hexdigest()
                for payload in expected_payloads
            ],
        }
    )


if __name__ == "__main__":
    main()
