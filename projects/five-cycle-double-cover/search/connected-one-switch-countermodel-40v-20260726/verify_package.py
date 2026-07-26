#!/usr/bin/env python3
"""Verify hashes and rerun the independent checker."""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent


def main() -> None:
    manifest = HERE / "SHA256SUMS"
    for line in manifest.read_text(encoding="ascii").splitlines():
        digest, relative = line.split("  ", 1)
        path = (HERE / relative).resolve()
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            raise RuntimeError(f"hash mismatch: {relative}")
    checked = subprocess.run(
        ["python3", str(HERE / "independent_checker.py")],
        text=True,
        capture_output=True,
        check=False,
    )
    if checked.returncode != 0 or '"status": "ACCEPTED"' not in checked.stdout:
        raise RuntimeError(
            "independent checker failed\n"
            + checked.stdout
            + checked.stderr
        )
    print("ACCEPTED: hashes and independent semantic checks")


if __name__ == "__main__":
    main()
