#!/usr/bin/env python3
"""Verify frozen hashes, then run the independent relation audit."""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent


def main() -> int:
    for line in (HERE / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        digest, name = line.split(maxsplit=1)
        actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        if actual != digest:
            raise AssertionError(f"SHA256 mismatch: {name}")
    subprocess.run(
        [sys.executable, str(HERE / "independent_verify.py")],
        check=True,
    )
    print("PASS frozen Blanusa six-pole relation package")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
