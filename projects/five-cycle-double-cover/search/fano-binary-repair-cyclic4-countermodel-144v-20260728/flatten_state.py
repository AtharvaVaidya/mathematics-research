#!/usr/bin/env python3
"""Freeze the discovered graph6 host and score-zero flow into two lines."""

from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
HOST = Path("/tmp/binary-repair-best5-order144.state")
ZERO = Path("/tmp/binary-repair-countermodel-order144.state")


def field(path: Path, name: str) -> str:
    prefix = name + "="
    rows = [
        line[len(prefix):]
        for line in path.read_text(encoding="ascii").splitlines()
        if line.startswith(prefix)
    ]
    if len(rows) != 1:
        raise AssertionError(f"{path}: expected one {name} field")
    return rows[0]


graph6 = field(HOST, "graph6")
flow = field(ZERO, "flow")
(PACKAGE / "countermodel-order144.txt").write_text(
    graph6 + "\n" + flow + "\n", encoding="ascii", newline="\n"
)
(PACKAGE / "countermodel-order144.g6").write_text(
    graph6 + "\n", encoding="ascii", newline="\n"
)
print(PACKAGE / "countermodel-order144.txt")
