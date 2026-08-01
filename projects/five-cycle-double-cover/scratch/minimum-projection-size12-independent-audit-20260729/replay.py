#!/usr/bin/env python3
"""Compile and replay the independent size-12 clean-or-delete audit."""

import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SHAPES = {
    "12": (1014, 14196654, 11465978, 0, 0),
    "4+8": (66, 922048, 773721, 4, 0),
    "5+7": (64, 884604, 738969, 206, 0),
    "6+6": (66, 926640, 774196, 182, 0),
    "4+4+4": (3, 41975, 35960, 0, 0),
}
FINAL = re.compile(
    r"FINAL words=(\d+) charge_valid=(\d+) dirty=(\d+) "
    r"direct_failures=(\d+) dichotomy_failures=(\d+)"
)


def main():
    with tempfile.TemporaryDirectory(
        prefix="size12-independent-audit-"
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
            generator = subprocess.Popen(
                [
                    sys.executable,
                    str(ROOT / "independent_word_orbits.py"),
                    shape,
                ],
                stdout=subprocess.PIPE,
                text=True,
            )
            audit = subprocess.run(
                [str(binary)],
                stdin=generator.stdout,
                text=True,
                capture_output=True,
                check=True,
            )
            assert generator.stdout is not None
            generator.stdout.close()
            assert generator.wait() == 0
            matches = FINAL.findall(audit.stdout)
            assert len(matches) == 1, audit.stdout
            observed = tuple(map(int, matches[0]))
            assert observed == expected, (shape, observed, expected)
            print(
                f"shape={shape} words={observed[0]} "
                f"charge_valid={observed[1]} dirty={observed[2]} "
                f"direct_failures={observed[3]} "
                f"dichotomy_failures={observed[4]}"
            )

    total_dirty = sum(row[2] for row in SHAPES.values())
    total_direct_failures = sum(row[3] for row in SHAPES.values())
    assert total_direct_failures == 392
    print("PASS: independent exhaustive size-12 clean-or-delete audit")
    print(f"total_dirty={total_dirty}")
    print("direct_clean_failures=392")
    print("failures_with_proper_circuit_deletion=392")
    print("clean_or_delete_failures=0")


if __name__ == "__main__":
    main()
