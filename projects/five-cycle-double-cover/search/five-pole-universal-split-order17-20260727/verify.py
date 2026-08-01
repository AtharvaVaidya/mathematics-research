#!/usr/bin/env python3
"""Independent structural and optional SAT replay of the order-17 census."""

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
EXPECTED_ROWS = (119043, 129064, 149874, 133432, 144691, 145113, 127195, 161432)
EXPECTED_CORPUS_SHA256 = (
    "94da0e3f080226a907e7badcb93127fde46439a32e100d02c362cce8fbf61ae1",
    "b22bdf5b1afb20f1a085aebe5dec3de41130ffc96ba2b08b7d0e815a7f3be5b4",
    "548244b3effc92e91d188838ded222870546dde069d5afc4215476edc4fb19f9",
    "14bafcccb0ce6800368ebb8760a97ad422a48828315b9edbee61d5315c442afd",
    "98a8c04fafd6b3cc736a7dfee9d06f630391a2e6327c456c33f92a8be4cdb6cf",
    "8f0e10fb9608d7a6cf4d1fc6ac799e66dfe1784819e7af472e809998ccb0dfdd",
    "3e82a35b27ea39eaa6d7b7c048e7eef27c759e396910ebb8af249fddad155646",
    "df9871a96400836bac988ace55c1373794acd6174fb5074dc3a481f0abe1271e",
)
EXPECTED_SUMMARY_SHA256 = (
    "02f9ccb6d2fb18c32e16b05ce3148b80325624d35a3f81178d4f041420a1ccae",
    "bd83953fa37a6be3de9f28f61aecbc7c58c2d8aed95be4de5082807568ea1061",
    "bd92fc1e064c130013a65dd65cae1e3fba2b21faf1a430190ecad89cf2507b9a",
    "14e0debf50a4d7774ee2301205d3ef326b4ee94240118308e25477c746072c52",
    "90dc5953e8cfc5937a2c021ba341803e4cdc063adc91cef7306e0e65c8133ccf",
    "230ba980b49a709f798c6c6116f4ede4ad3997c505e79574429101eda3781b43",
    "c7dd9c89c36137609a8cc0f2f9b6ceec23870d69eb877517ade31aada83fc292",
    "10c91a8e36d0c22f95bc28862cefebfb58660c0c5f38ab5239198bce5accd501",
)
EXPECTED_TOTAL = 1_109_844


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    if not record or record[0] == "~":
        raise ValueError("only short graph6 records are supported")
    order = ord(record[0]) - 63
    if not 0 <= order <= 62:
        raise ValueError("invalid graph6 order")
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


def audit_local_algebra() -> None:
    d5 = tuple(
        (1 << left) | (1 << right)
        for left in range(5)
        for right in range(left + 1, 5)
    )
    doubled = (1 << 0) | (1 << 1)
    triangle = (
        (1 << 2) | (1 << 3),
        (1 << 2) | (1 << 4),
        (1 << 3) | (1 << 4),
    )
    if len(d5) != 10 or doubled ^ doubled ^ triangle[0] ^ triangle[1] ^ triangle[2]:
        raise AssertionError("bad split-state boundary algebra")
    point_values = (0, 0, 1, 2, 3)

    def quotient(mask: int) -> int:
        value = 0
        for point in range(5):
            if mask >> point & 1:
                value ^= point_values[point]
        return value

    if tuple(mask for mask in d5 if quotient(mask) == 0) != (doubled,):
        raise AssertionError("quotient zero fibre is not exactly {01}")
    if {quotient(mask) for mask in triangle} != {1, 2, 3}:
        raise AssertionError("complement triangle has wrong quotient")
    if any(doubled ^ mask in d5 for mask in triangle):
        raise AssertionError("repeated-terminal local obstruction failed")


def read_summaries() -> tuple[bytes, ...]:
    payloads = []
    for shard, expected_rows in enumerate(EXPECTED_ROWS):
        path = RESULTS / f"order17-shard-{shard}.txt"
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != EXPECTED_SUMMARY_SHA256[shard]:
            raise AssertionError(f"summary hash mismatch in shard {shard}")
        expected = f"PASS\trecords\t{expected_rows}\ttarget_checks\t{10 * expected_rows}\n"
        if raw.decode("ascii") != expected:
            raise AssertionError(f"bad summary in shard {shard}")
        payloads.append(raw)
    if sum(EXPECTED_ROWS) != EXPECTED_TOTAL:
        raise AssertionError("bad expected aggregate")
    return tuple(payloads)


def find_geng() -> str:
    geng = shutil.which("geng")
    if geng is None and Path("/opt/homebrew/bin/geng").exists():
        geng = "/opt/homebrew/bin/geng"
    if geng is None:
        raise RuntimeError("nauty geng is required")
    return geng


def geng_command(geng: str, shard: int) -> list[str]:
    return [geng, "-Cq", "-d2", "-D3", "17", "23:23", f"{shard}/8"]


def verify_corpora(geng: str) -> None:
    seen: set[str] = set()
    for shard, expected_rows in enumerate(EXPECTED_ROWS):
        process = subprocess.Popen(
            geng_command(geng, shard),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert process.stdout is not None
        digest = hashlib.sha256()
        rows = 0
        for raw in process.stdout:
            digest.update(raw)
            record = raw.rstrip(b"\n").decode("ascii")
            if record in seen:
                raise AssertionError("duplicate graph6 record across shards")
            seen.add(record)
            order, edges = parse_graph6(record)
            if order != 17 or len(edges) != 23:
                raise AssertionError("wrong graph order or size")
            degrees = [0] * order
            for left, right in edges:
                degrees[left] += 1
                degrees[right] += 1
            if sorted(degrees) != [2] * 5 + [3] * 12:
                raise AssertionError("wrong terminal/degree profile")
            if bridge_count(order, edges):
                raise AssertionError("proper core has a bridge")
            rows += 1
        stderr = process.stderr.read() if process.stderr is not None else b""
        if process.wait() != 0:
            raise RuntimeError(f"geng failed on shard {shard}: {stderr.decode()}")
        if rows != expected_rows:
            raise AssertionError(f"wrong corpus row count in shard {shard}")
        if digest.hexdigest() != EXPECTED_CORPUS_SHA256[shard]:
            raise AssertionError(f"corpus hash mismatch in shard {shard}")
    if len(seen) != EXPECTED_TOTAL:
        raise AssertionError("wrong distinct aggregate corpus count")


def compile_primary(directory: Path) -> Path:
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
        raise RuntimeError("CaDiCaL headers/static library are required")
    binary = directory / "primary-census"
    subprocess.run(
        [
            compiler,
            "-O3",
            "-std=c++17",
            f"-I{include}",
            str(HERE / "primary_census.cpp"),
            str(library),
            "-o",
            str(binary),
        ],
        check=True,
    )
    return binary


def replay_sat(geng: str, summaries: tuple[bytes, ...]) -> None:
    with tempfile.TemporaryDirectory(prefix="split-state-order17-") as raw:
        binary = compile_primary(Path(raw))
        for shard, expected in enumerate(summaries):
            generator = subprocess.Popen(
                geng_command(geng, shard),
                stdout=subprocess.PIPE,
            )
            assert generator.stdout is not None
            completed = subprocess.run(
                [str(binary)],
                stdin=generator.stdout,
                capture_output=True,
                check=True,
            )
            generator.stdout.close()
            if generator.wait() != 0:
                raise RuntimeError(f"geng failed on SAT replay shard {shard}")
            if completed.stdout != expected:
                raise AssertionError(f"SAT replay differs on shard {shard}")


def verify_report() -> None:
    report = json.loads((HERE / "report.json").read_text(encoding="utf-8"))
    if report["status"] != "PASS":
        raise AssertionError("report status is not PASS")
    if report["scope"]["canonical_records"] != EXPECTED_TOTAL:
        raise AssertionError("report aggregate differs")
    if report["target"]["sat_checks"] != 10 * EXPECTED_TOTAL:
        raise AssertionError("report target total differs")
    for shard, row in enumerate(report["shards"]):
        if row["index"] != shard:
            raise AssertionError("report shard order differs")
        if row["records"] != EXPECTED_ROWS[shard]:
            raise AssertionError("report shard count differs")
        if row["corpus_sha256"] != EXPECTED_CORPUS_SHA256[shard]:
            raise AssertionError("report corpus hash differs")
        if row["summary_sha256"] != EXPECTED_SUMMARY_SHA256[shard]:
            raise AssertionError("report summary hash differs")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--replay",
        action="store_true",
        help="also recompile and rerun every CaDiCaL query",
    )
    arguments = parser.parse_args()
    verify_report()
    audit_local_algebra()
    summaries = read_summaries()
    geng = find_geng()
    verify_corpora(geng)
    if arguments.replay:
        replay_sat(geng, summaries)
    print(
        json.dumps(
            {
                "status": "PASS",
                "mode": "structural+sat-replay" if arguments.replay else "structural",
                "records": EXPECTED_TOTAL,
                "target_checks": 10 * EXPECTED_TOTAL,
                "corpus_sha256": list(EXPECTED_CORPUS_SHA256),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
