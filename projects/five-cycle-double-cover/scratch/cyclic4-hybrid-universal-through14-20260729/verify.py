#!/usr/bin/env python3
"""Replay the frozen cyclically-4 hybrid frontier."""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent


def verify_ledger() -> None:
    for line in (HERE / "SHA256SUMS").read_text(
        encoding="ascii"
    ).splitlines():
        digest, relative = line.split("  ", 1)
        actual = hashlib.sha256((HERE / relative).read_bytes()).hexdigest()
        if actual != digest:
            raise AssertionError(
                f"SHA-256 mismatch for {relative}: {actual} != {digest}"
            )


def main() -> int:
    verify_ledger()
    print("PASS SHA-256 ledger", flush=True)
    subprocess.run(
        [sys.executable, str(HERE / "verify_frontier.py")],
        cwd=HERE,
        check=True,
    )
    print("PASS frozen cyclically-4 hybrid package")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
