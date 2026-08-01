#!/usr/bin/env python3
"""Export the frozen JSON F10 pole to the tiny enumerator input format."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("atom", type=Path)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()
    atom = json.loads(arguments.atom.read_text(encoding="ascii"))
    ports = atom["connectors"][0] + atom["connectors"][1]
    rows = [
        f"{atom['vertices']} {len(atom['edges'])} {len(ports)}",
        " ".join(map(str, ports)),
        *(f"{left} {right}" for left, right in atom["edges"]),
    ]
    arguments.output.write_text("\n".join(rows) + "\n", encoding="ascii")
    print(
        f"vertices={atom['vertices']} edges={len(atom['edges'])} "
        f"ports={','.join(map(str, ports))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
