#!/usr/bin/env python3
"""Verify package hashes and rerun the clean-room single and batch audits."""

from __future__ import annotations

import hashlib
from pathlib import Path
import shutil
import subprocess


HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def checked_output(command: list[str]) -> bytes:
    completed = subprocess.run(
        command,
        cwd=HERE,
        check=False,
        capture_output=True,
    )
    require(
        completed.returncode == 0,
        "command failed: "
        + " ".join(command)
        + "\n"
        + completed.stderr.decode("utf-8", errors="replace"),
    )
    return completed.stdout


def main() -> int:
    for line in (HERE / "SHA256SUMS").read_text(
        encoding="ascii"
    ).splitlines():
        digest, relative = line.split("  ", 1)
        path = HERE / relative
        require(path.is_file(), f"missing manifest file: {relative}")
        require(
            hashlib.sha256(path.read_bytes()).hexdigest() == digest,
            f"hash mismatch: {relative}",
        )

    single = checked_output(
        ["python3", "-B", str(HERE / "independent_verifier.py")]
    )
    require(
        single == (HERE / "verification-report.json").read_bytes(),
        "single-witness replay differs from frozen report",
    )
    batch = checked_output(
        ["python3", "-B", str(HERE / "batch_verifier.py")]
    )
    require(
        batch == (HERE / "batch-verification-report.json").read_bytes(),
        "batch replay differs from frozen report",
    )

    labelg = shutil.which("labelg")
    canonicalization = "SKIPPED (labelg unavailable)"
    if labelg:
        canonical = checked_output(
            [labelg, "-q", str(HERE / "graph.g6")]
        )
        require(
            canonical == (HERE / "graph.canonical.g6").read_bytes(),
            "nauty canonical graph6 mismatch",
        )
        canonicalization = "VERIFIED"

    print(
        "VERIFIED: hashes, first witness, 144-hit batch, "
        f"canonicalization={canonicalization}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
