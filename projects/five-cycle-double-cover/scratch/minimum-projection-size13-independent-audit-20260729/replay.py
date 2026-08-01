#!/usr/bin/env python3
"""Compile and replay the independent size-13 clean-or-delete audit."""

import importlib.util
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SHAPES = {
    "13": (2583, 155381679, 129684490, 0, 0),
    "4+9": (130, 7753918, 6657654, 60, 0),
    "5+8": (203, 12144485, 10404652, 3224, 0),
    "6+7": (242, 14480258, 12415026, 4390, 0),
    "4+4+5": (4, 238522, 208144, 0, 0),
}
FINAL = re.compile(
    r"FINAL words=(\d+) charge_valid=(\d+) dirty=(\d+) "
    r"direct_failures=(\d+) dichotomy_failures=(\d+)"
)


def parse_final(output):
    matches = FINAL.findall(output)
    assert len(matches) == 1, output
    return tuple(map(int, matches[0]))


def run_input(binary, input_text):
    result = subprocess.run(
        [str(binary)],
        input=input_text,
        text=True,
        capture_output=True,
        check=True,
    )
    return parse_final(result.stdout)


def word_text(shape):
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "independent_word_orbits.py"),
            shape,
        ],
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.splitlines()


def single_circuit_parallel(binary):
    lines = word_text("13")
    assert lines[0] == "13"
    words = lines[1:]
    workers = min(8, os.cpu_count() or 1)
    chunks = [words[index::workers] for index in range(workers)]
    inputs = ["13\n" + "\n".join(chunk) + "\n" for chunk in chunks]
    with ThreadPoolExecutor(max_workers=workers) as executor:
        rows = tuple(executor.map(
            lambda text: run_input(binary, text), inputs
        ))
    return tuple(sum(row[index] for row in rows) for index in range(5))


def format_row(shape, row):
    return (
        f"shape={shape} words={row[0]} charge_valid={row[1]} "
        f"dirty={row[2]} direct_failures={row[3]} "
        f"dichotomy_failures={row[4]}"
    )


def main():
    output = []
    with tempfile.TemporaryDirectory(
        prefix="size13-independent-audit-"
    ) as temporary:
        binary = Path(temporary) / "independent_audit"
        subprocess.run(
            [
                "c++", "-O3", "-std=c++17", "-Wall", "-Wextra",
                "-pedantic", str(ROOT / "independent_audit.cpp"),
                "-o", str(binary),
            ],
            check=True,
        )

        for shape, expected in SHAPES.items():
            if shape == "13":
                observed = single_circuit_parallel(binary)
            else:
                observed = run_input(
                    binary, "\n".join(word_text(shape)) + "\n"
                )
            assert observed == expected, (shape, observed, expected)
            output.append(format_row(shape, observed))

    total_dirty = sum(row[2] for row in SHAPES.values())
    total_direct_failures = sum(row[3] for row in SHAPES.values())
    assert total_dirty == 159369966
    assert total_direct_failures == 7674
    output.extend((
        "PASS: independent exhaustive size-13 clean-or-delete audit",
        f"total_dirty={total_dirty}",
        f"direct_clean_failures={total_direct_failures}",
        "failures_with_proper_circuit_deletion=7674",
        "clean_or_delete_failures=0",
    ))
    encoded = "\n".join(output) + "\n"
    frozen = (ROOT / "full-run-output.txt").read_text(encoding="ascii")
    assert encoded == frozen
    print(encoded, end="")


if __name__ == "__main__":
    main()
