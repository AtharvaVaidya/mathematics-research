#!/usr/bin/env python3
"""Verify and optionally replay the exact strong-snark minimum scan."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent

EXPECTED_SHA256 = {
    "inputs/strongsnarks_34_5_cyc4.g6":
        "2f087d5cbd1e97b1e10e7a5a064fe83d037872f838372e4d317c9d3f912fbf1f",
    "inputs/strongsnarks_40_5_cyc4.g6":
        "61d7b01786e983084a6255bb0afe22a503cbb8645fe186b8a962d60609224e1d",
    "results/strong34.jsonl":
        "d83e9af7f80d01fb45bf88dc8eaee663e2f1b7c0ffbbfe1508a3f811e9cc29d2",
    "results/strong40-part0.jsonl":
        "30decf278d5403b2ca7bfcd6c7c54fa5f0a159c9879a593c452f7b2e750eddb6",
    "results/strong40-part1.jsonl":
        "7a4180de1ce624f3c186d787fa1fc43dcec724513be20a6311959fadede19a3b",
    "results/strong40-part2.jsonl":
        "0613909d31f10350c10ed6af58422b5a50c43e01a92b970bd744e40b3d94794f",
    "results/strong40-part3.jsonl":
        "51d463701c3d85d246dcfad0cebc9a5f46f979c5c0c3353cebd3eec9a64f0ef3",
    "scanner/reference/scan.cpp":
        "dd97a7a3c43502b6caf8cab600432ef41b1467ee5e7b91b453eee9020cbc94dd",
    "scanner/fano_all_bad_projection_search_linear.cpp":
        "bf713d5bdcaa11a76bf98b77422ab55914fba29e36792de71fbed53d102687db",
    "scanner/exact_sat_scan.cpp":
        "e2633cfeb9f6d2e2e4a5c51f50bd6c4c8b9c44a17a93deab081e41e0485736dd",
}

PARTS_40 = (
    ("results/strong40-part0.jsonl", 0, 1914),
    ("results/strong40-part1.jsonl", 1914, 3828),
    ("results/strong40-part2.jsonl", 3828, 5742),
    ("results/strong40-part3.jsonl", 5742, 7654),
)

EXPECTED_AGGREGATES = {
    34: {
        "records": 7,
        "minimum": 10,
        "minimum_extendable": 371,
        "min_count": 48,
        "max_count": 60,
        "bad_minimum": 0,
    },
    40: {
        "records": 7654,
        "minimum": 10,
        "minimum_extendable": 433359,
        "min_count": 16,
        "max_count": 85,
        "bad_minimum": 0,
    },
}

EXPECTED_CONCATENATED_40_SHA256 = (
    "97042fbc1b4f6079962d43582d7adb2cba4c1c5659c3bf5e049e88f3eca13d1e"
)
EXPECTED_ALL_RESULTS_SHA256 = (
    "becb7e4b648c000ec874509bccdf389df24f6f0d82bce2da49ba10d5b10d38e3"
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def check_hashes() -> None:
    for relative, expected in EXPECTED_SHA256.items():
        observed = sha256_bytes((ROOT / relative).read_bytes())
        assert observed == expected, (relative, expected, observed)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="ascii").splitlines()
        if line
    ]


def audit_dataset(
    order: int,
    input_relative: str,
    parts: tuple[tuple[str, int, int], ...],
) -> None:
    input_rows = (
        ROOT / input_relative
    ).read_text(encoding="ascii").splitlines()
    observed_rows: list[dict[str, object]] = []
    raw_results = bytearray()
    for result_relative, start, stop in parts:
        result_path = ROOT / result_relative
        raw_results.extend(result_path.read_bytes())
        rows = read_jsonl(result_path)
        assert len(rows) == stop - start
        for local_row, result in enumerate(rows):
            assert result["row"] == local_row
            assert result["graph6"] == input_rows[start + local_row]
            assert result["minimum"] == 10
            assert result["minimum_extendable"] > 0
            assert result["bad_minimum"] == 0
            assert result["bad_hex"] == []
        observed_rows.extend(rows)

    expected = EXPECTED_AGGREGATES[order]
    counts = [int(row["minimum_extendable"]) for row in observed_rows]
    aggregate = {
        "records": len(observed_rows),
        "minimum": min(int(row["minimum"]) for row in observed_rows),
        "minimum_extendable": sum(counts),
        "min_count": min(counts),
        "max_count": max(counts),
        "bad_minimum": sum(int(row["bad_minimum"]) for row in observed_rows),
    }
    assert aggregate == expected, (expected, aggregate)
    if order == 40:
        assert sha256_bytes(bytes(raw_results)) == EXPECTED_CONCATENATED_40_SHA256


def compile_program(
    source: Path,
    output: Path,
    cxx: str,
    extra: list[str],
) -> None:
    command = [cxx, "-O3", "-DNDEBUG", "-std=c++20", str(source), *extra,
               "-o", str(output)]
    subprocess.run(command, check=True)


def run_scanner(binary: Path, input_path: Path) -> bytes:
    process = subprocess.run(
        [str(binary), str(input_path)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode:
        raise RuntimeError(
            f"{binary.name} failed with {process.returncode} on {input_path}:\n"
            + process.stdout.decode("ascii", errors="replace")
            + process.stderr.decode("ascii", errors="replace")
        )
    return process.stdout


def full_sat_replay(
    jobs: int,
    cxx: str,
    cadical_include: Path,
    cadical_library: Path,
) -> None:
    with tempfile.TemporaryDirectory(prefix="minproj-known-snarks-replay-") as tmp:
        temporary = Path(tmp)
        binary = temporary / "exact-sat-scan"
        compile_program(
            ROOT / "scanner/exact_sat_scan.cpp",
            binary,
            cxx,
            [f"-I{cadical_include}", str(cadical_library)],
        )

        work: list[tuple[Path, Path]] = []
        input_34 = ROOT / "inputs/strongsnarks_34_5_cyc4.g6"
        work.append((input_34, ROOT / "results/strong34.jsonl"))

        rows_40 = (
            ROOT / "inputs/strongsnarks_40_5_cyc4.g6"
        ).read_bytes().splitlines(keepends=True)
        for index, (result_relative, start, stop) in enumerate(PARTS_40):
            chunk = temporary / f"strong40-part{index}.g6"
            chunk.write_bytes(b"".join(rows_40[start:stop]))
            work.append((chunk, ROOT / result_relative))

        def replay_one(item: tuple[Path, Path]) -> tuple[Path, bytes]:
            input_path, expected_path = item
            return expected_path, run_scanner(binary, input_path)

        with ThreadPoolExecutor(max_workers=jobs) as executor:
            outputs = list(executor.map(replay_one, work))
        for expected_path, observed in outputs:
            expected = expected_path.read_bytes()
            assert observed == expected, f"replay mismatch: {expected_path}"


def reference_cross_check(cxx: str) -> None:
    with tempfile.TemporaryDirectory(prefix="minproj-reference-check-") as tmp:
        temporary = Path(tmp)
        binary = temporary / "reference-scan"
        compile_program(
            ROOT / "scanner/reference/scan.cpp",
            binary,
            cxx,
            [],
        )
        observed_34 = run_scanner(
            binary, ROOT / "inputs/strongsnarks_34_5_cyc4.g6"
        )
        assert observed_34 == (ROOT / "results/strong34.jsonl").read_bytes()

        first_five_input = temporary / "strong40-first5.g6"
        input_lines = (
            ROOT / "inputs/strongsnarks_40_5_cyc4.g6"
        ).read_bytes().splitlines(keepends=True)
        first_five_input.write_bytes(b"".join(input_lines[:5]))
        observed_40 = run_scanner(binary, first_five_input)
        expected_40 = b"".join(
            (ROOT / "results/strong40-part0.jsonl")
            .read_bytes()
            .splitlines(keepends=True)[:5]
        )
        assert observed_40 == expected_40


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--reference-cross-check", action="store_true")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--cxx", default=os.environ.get("CXX", "c++"))
    parser.add_argument(
        "--cadical-include",
        type=Path,
        default=Path("/opt/homebrew/include"),
    )
    parser.add_argument(
        "--cadical-library",
        type=Path,
        default=Path("/opt/homebrew/lib/libcadical.a"),
    )
    args = parser.parse_args()
    assert args.jobs >= 1

    check_hashes()
    audit_dataset(
        34,
        "inputs/strongsnarks_34_5_cyc4.g6",
        (("results/strong34.jsonl", 0, 7),),
    )
    audit_dataset(
        40,
        "inputs/strongsnarks_40_5_cyc4.g6",
        PARTS_40,
    )
    all_results = (ROOT / "results/strong34.jsonl").read_bytes() + b"".join(
        (ROOT / relative).read_bytes() for relative, _, _ in PARTS_40
    )
    assert sha256_bytes(all_results) == EXPECTED_ALL_RESULTS_SHA256
    print("Frozen hashes, row provenance, exact semantics, and aggregates: PASS")

    if args.replay:
        full_sat_replay(
            args.jobs,
            args.cxx,
            args.cadical_include,
            args.cadical_library,
        )
        print("Full exact SAT replay: PASS")
    if args.reference_cross_check:
        reference_cross_check(args.cxx)
        print("Reference linear cross-check (all 34v + first five 40v): PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
