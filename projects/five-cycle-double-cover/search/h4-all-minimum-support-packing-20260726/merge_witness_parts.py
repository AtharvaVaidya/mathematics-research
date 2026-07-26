#!/usr/bin/env python3
"""Validate and concatenate the eight fixed H4 witness chunks."""

from __future__ import annotations

from pathlib import Path
import shutil


HERE = Path(__file__).resolve().parent
COUNTS = (616429, 616429, 616429, 616429,
          616429, 616429, 616428, 616428)
BYTES_PER_ROW = 31


def main() -> None:
    output_path = HERE / "packing-witnesses.bin"
    with output_path.open("wb") as output:
        for part, rows in enumerate(COUNTS):
            input_path = HERE / f"packing-witnesses.part{part}.bin"
            expected = rows * BYTES_PER_ROW
            actual = input_path.stat().st_size
            if actual != expected:
                raise AssertionError(
                    f"{input_path.name}: expected {expected}, got {actual}"
                )
            with input_path.open("rb") as source:
                shutil.copyfileobj(source, output, 8 * 1024 * 1024)
    expected_total = sum(COUNTS) * BYTES_PER_ROW
    if output_path.stat().st_size != expected_total:
        raise AssertionError("merged witness size mismatch")
    print(
        f"WROTE {output_path.name} rows {sum(COUNTS)} "
        f"bytes {expected_total}"
    )


if __name__ == "__main__":
    main()
