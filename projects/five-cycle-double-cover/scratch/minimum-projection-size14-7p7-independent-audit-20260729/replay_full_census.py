#!/usr/bin/env python3
"""Regenerate the complete 7+7 census with the independent C++ auditor."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_WORD_FILE_SHA256 = (
    "c2cbd4b9e06145ec22e516440b0aa2905aa5ed6c71121068398fde435374ef9f"
)
EXPECTED_TOTAL = (333, 91_481_505, 80_104_020, 37_463, 224)
EXPECTED_FAILURE_SET_SHA256 = (
    "eec4d091247385ab4aef5c567e52377062d6a7eae8f68e988069c1a3920215ca"
)
FINAL_RE = re.compile(
    r"FINAL words=(\d+) charge_valid=(\d+) dirty=(\d+) "
    r"direct_failures=(\d+) dichotomy_failures=(\d+)"
)


def generate_words():
    result = subprocess.run(
        [sys.executable, str(HERE / "independent_word_orbits.py")],
        text=True,
        capture_output=True,
        check=True,
    )
    encoded = result.stdout.encode("ascii")
    assert hashlib.sha256(encoded).hexdigest() == EXPECTED_WORD_FILE_SHA256
    lines = result.stdout.splitlines()
    assert lines[0] == "7 7"
    assert len(lines[1:]) == 333
    assert len(set(lines[1:])) == 333
    return lines[1:]


def run_chunk(binary, words):
    input_text = "7 7\n" + "\n".join(words) + "\n"
    result = subprocess.run(
        [str(binary)],
        input=input_text,
        text=True,
        capture_output=True,
        check=True,
    )
    matches = FINAL_RE.findall(result.stdout)
    assert len(matches) == 1
    total = tuple(map(int, matches[0]))
    failures = tuple(
        line
        for line in result.stdout.splitlines()
        if line.startswith("COUNTERSTATE ")
    )
    assert len(failures) == total[-1]
    return total, failures


def primary_failure_rows():
    rows = tuple(
        line
        for line in (HERE / "census-7+7.txt").read_text(encoding="ascii").splitlines()
        if line.startswith("COUNTERSTATE ")
    )
    assert len(rows) == 224
    assert len(set(rows)) == 224
    return rows


def digest_rows(rows):
    encoded = ("\n".join(sorted(rows)) + "\n").encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def main():
    words = generate_words()
    worker_count = min(8, os.cpu_count() or 1)
    chunks = [words[index::worker_count] for index in range(worker_count)]
    output_lines = []

    with tempfile.TemporaryDirectory(prefix="fivecdc-7p7-independent-") as temporary:
        binary = Path(temporary) / "independent_full_census"
        subprocess.run(
            [
                "c++",
                "-O3",
                "-std=c++17",
                "-Wall",
                "-Wextra",
                "-pedantic",
                str(HERE / "independent_full_census.cpp"),
                "-o",
                str(binary),
            ],
            check=True,
        )
        results = []
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            futures = [
                executor.submit(run_chunk, binary, chunk) for chunk in chunks
            ]
            for completed, future in enumerate(as_completed(futures), 1):
                result = future.result()
                results.append(result)
                line = f"completed_shards={completed}/{worker_count}"
                output_lines.append(line)
                print(line, flush=True)

    observed_total = tuple(
        sum(result[0][column] for result in results)
        for column in range(5)
    )
    assert observed_total == EXPECTED_TOTAL, observed_total

    independent_failures = tuple(
        row for _, rows in results for row in rows
    )
    assert len(independent_failures) == 224
    assert len(set(independent_failures)) == 224
    assert digest_rows(independent_failures) == EXPECTED_FAILURE_SET_SHA256

    primary_failures = primary_failure_rows()
    assert digest_rows(primary_failures) == EXPECTED_FAILURE_SET_SHA256
    assert set(independent_failures) == set(primary_failures)

    final_line = (
        "FINAL words={} charge_valid={} dirty={} direct_failures={} "
        "dichotomy_failures={}".format(*observed_total)
    )
    digest_line = f"failure_set_sha256={EXPECTED_FAILURE_SET_SHA256}"
    pass_line = (
        "PASS: independent word-orbit and valid-block exact-cover census "
        "reproduces the complete primary 7+7 table and all 224 failures"
    )
    output_lines.extend((final_line, digest_line, pass_line))
    frozen = (HERE / "full-replay-output.txt").read_text(encoding="ascii")
    assert "\n".join(output_lines) + "\n" == frozen
    print(final_line)
    print(digest_line)
    print(pass_line)


if __name__ == "__main__":
    main()
