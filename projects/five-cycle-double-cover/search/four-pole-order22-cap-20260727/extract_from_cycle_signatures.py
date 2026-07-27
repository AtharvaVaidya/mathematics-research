#!/usr/bin/env python3
"""Second extraction of order-22 cyclically-4 hard rows.

This checker imports the already tested cycle-space cut routine but reads the
identity-audited hard corpus directly.  Its output must agree byte-for-byte
with the independently written Tarjan-after-deletions C++ classifier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from search.canonical.canonical_search import parse_graph6
from tools.order22_filter_analysis import small_cyclic_edge_cuts


EXPECTED_HARD_ROWS = 12_892
EXPECTED_CYCLIC4_ROWS = 31


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("hard_input", type=Path)
    parser.add_argument("cyclic4_output", type=Path)
    parser.add_argument("report_output", type=Path)
    arguments = parser.parse_args()

    input_digest = hashlib.sha256()
    output_digest = hashlib.sha256()
    rows = 0
    selected = 0
    temporary = arguments.cyclic4_output.with_suffix(
        arguments.cyclic4_output.suffix + ".tmp"
    )
    with arguments.hard_input.open("rb") as source, temporary.open(
        "wb"
    ) as output:
        for rows, raw in enumerate(source, start=1):
            if not raw.endswith(b"\n"):
                raise SystemExit(f"unterminated input row {rows}")
            input_digest.update(raw)
            graph = parse_graph6(raw[:-1].decode("ascii"))
            two_cuts, three_cuts = small_cyclic_edge_cuts(graph)
            if two_cuts or three_cuts:
                continue
            output.write(raw)
            output_digest.update(raw)
            selected += 1
    if rows != EXPECTED_HARD_ROWS:
        raise SystemExit(f"hard row count {rows} != {EXPECTED_HARD_ROWS}")
    if selected != EXPECTED_CYCLIC4_ROWS:
        raise SystemExit(
            f"cyclically-4 row count {selected} != {EXPECTED_CYCLIC4_ROWS}"
        )
    temporary.replace(arguments.cyclic4_output)

    report = {
        "schema": "order22-cyclic4-cycle-signature-extraction-v1",
        "hard_corpus": {
            "rows": rows,
            "sha256": input_digest.hexdigest(),
        },
        "cyclically_four": {
            "rows": selected,
            "sha256": output_digest.hexdigest(),
            "path": str(arguments.cyclic4_output),
        },
    }
    arguments.report_output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
