#!/usr/bin/env python3
"""Rebuild the producer and byte-replay all 13 deterministic search runs."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"


def main() -> None:
    raw_paths = sorted(RAW.glob("*.jsonl"))
    assert len(raw_paths) == 13
    first_row = json.loads(
        raw_paths[0].read_text(encoding="utf-8").splitlines()[0]
    )
    graph6 = str(first_row["graph6"]) + "\n"
    with tempfile.TemporaryDirectory(
        prefix="jaeger-lift13-portfolio-"
    ) as temporary:
        binary = Path(temporary) / "producer"
        subprocess.run(
            [
                "clang++",
                "-O3",
                "-std=c++20",
                "-Wall",
                "-Wextra",
                "-pedantic",
                str(HERE / "producer.cpp"),
                "-o",
                str(binary),
            ],
            check=True,
        )
        for path in raw_paths:
            root_row = json.loads(
                path.read_text(encoding="utf-8").splitlines()[-1]
            )
            completed = subprocess.run(
                [
                    str(binary),
                    str(root_row["steps"]),
                    str(root_row["seed"]),
                    str(root_row["root"]),
                    "trap-directed",
                ],
                input=graph6,
                text=True,
                capture_output=True,
                check=True,
            )
            if completed.stdout != path.read_text(encoding="utf-8"):
                raise AssertionError(f"search replay mismatch: {path.name}")
            print(f"PASS {path.name}", flush=True)


if __name__ == "__main__":
    main()
