#!/usr/bin/env python3
"""End-to-end replay of the F10 full boundary relation package."""

from __future__ import annotations

import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent


def run(command: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=True,
        text=True,
        **kwargs,
    )


def same(left: Path, right: Path) -> None:
    if left.read_bytes() != right.read_bytes():
        raise AssertionError(f"regenerated file differs: {left.name}")


def check_hashes() -> None:
    expected = {}
    for line in (HERE / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        digest, name = line.split(maxsplit=1)
        expected[name] = digest
    for name, digest in expected.items():
        actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        if actual != digest:
            raise AssertionError(f"SHA256 mismatch for {name}")


def main() -> int:
    check_hashes()
    run([
        "python3",
        str(HERE / "verify_boundary_relation.py"),
        str(HERE / "f10-atom.txt"),
        str(HERE / "s5-representatives.json"),
        str(HERE / "boundary-witnesses.jsonl"),
        str(HERE / "relation-summary.json"),
    ])

    compiler = shutil.which("c++")
    if compiler is None:
        raise AssertionError("c++ compiler not found")
    include = Path("/opt/homebrew/include")
    library = Path("/opt/homebrew/lib/libcadical.a")
    if not (include / "cadical.hpp").is_file() or not library.is_file():
        raise AssertionError("Homebrew CaDiCaL headers/library not found")

    with tempfile.TemporaryDirectory(prefix="f10-boundary-replay-") as raw:
        temporary = Path(raw)
        atom = temporary / "f10-atom.txt"
        representatives = temporary / "s5-representatives.json"
        witnesses = temporary / "boundary-witnesses.jsonl"
        summary = temporary / "relation-summary.json"
        executable = temporary / "enumerate_f10_boundary"

        # The standalone topology is itself frozen and hash-checked above.
        # Copy it into the temporary replay area without depending on another
        # untracked scratch package.
        shutil.copyfile(HERE / "f10-atom.txt", atom)
        run([
            "python3",
            str(HERE / "generate_s5_representatives.py"),
            str(representatives),
        ], stdout=subprocess.DEVNULL)
        same(representatives, HERE / "s5-representatives.json")
        run([
            compiler,
            "-std=c++20",
            "-O3",
            str(HERE / "enumerate_f10_boundary.cpp"),
            f"-I{include}",
            str(library),
            "-o",
            str(executable),
        ])
        with witnesses.open("w", encoding="ascii") as output:
            producer = run(
                [str(executable), str(atom), str(representatives)],
                stdout=output,
                stderr=subprocess.PIPE,
            )
        if (
            "representatives=571 sat=571 unsat_uncertified=0"
            not in producer.stderr
        ):
            raise AssertionError("unexpected producer summary")
        run([
            "python3",
            str(HERE / "summarize_relation.py"),
            str(representatives),
            str(witnesses),
            str(summary),
        ], stdout=subprocess.DEVNULL)
        same(summary, HERE / "relation-summary.json")
        run([
            "python3",
            str(HERE / "verify_boundary_relation.py"),
            str(atom),
            str(representatives),
            str(witnesses),
            str(summary),
        ])

    print("PASS F10 full boundary relation and universal network theorem")
    print("PASS frozen artifacts, independent audit, and full producer replay")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
