#!/usr/bin/env python3
"""Independently replay the retained rooted-frontier report."""

from __future__ import annotations

import gzip
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ORBIT_LABELS = (
    frozenset((0b00011,)),
    frozenset((0b00101,)),
    frozenset((0b00110,)),
    frozenset((0b01001, 0b10001)),
    frozenset((0b01010, 0b10010)),
    frozenset((0b01100, 0b10100)),
    frozenset((0b11000,)),
)


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def actual_labels(mask: int) -> set[int]:
    return set().union(
        *(ORBIT_LABELS[index] for index in range(7) if mask >> index & 1)
    )


def relation(first: int, second: int) -> str:
    result = set()
    for left in actual_labels(first):
        for right in actual_labels(second):
            if left == right:
                result.add("E")
            elif left & right:
                result.add("I")
            else:
                result.add("D")
    return "".join(sorted(result))


def verify_full_order(row: dict) -> set[int]:
    order = row["order"]
    expected_edges = (3 * order - 3) // 2
    path = ROOT / row["retained_file"]
    if digest(path) != row["retained_sha256"]:
        raise SystemExit(f"order {order}: retained gzip digest mismatch")
    raw = gzip.decompress(path.read_bytes())
    if hashlib.sha256(raw).hexdigest() != row["raw_transcript_sha256"]:
        raise SystemExit(f"order {order}: raw transcript digest mismatch")

    lines = raw.decode("ascii").splitlines()
    if len(lines) != row["roots"]:
        raise SystemExit(f"order {order}: transcript root count mismatch")
    size_profile = Counter()
    singleton = 0
    singleton_nonbridge = 0
    graph_roots: dict[str, list[int]] = {}
    nonempty_nonbridge_masks = set()
    for number, line in enumerate(lines, start=1):
        fields = line.split("\t")
        if len(fields) != 4:
            raise SystemExit(f"order {order}, row {number}: malformed transcript")
        record, root_text, mask_text, bridge_text = fields
        root = int(root_text)
        mask = int(mask_text, 16)
        if mask >= 1 << 7 or bridge_text not in {"0", "1"}:
            raise SystemExit(f"order {order}, row {number}: invalid mask/bridge")
        graph_roots.setdefault(record, []).append(root)
        size = mask.bit_count()
        size_profile[size] += 1
        singleton += size == 1
        singleton_nonbridge += size == 1 and bridge_text == "0"
        if mask and bridge_text == "0":
            nonempty_nonbridge_masks.add(mask)

    if len(graph_roots) != row["graphs"]:
        raise SystemExit(f"order {order}: graph count mismatch")
    for record, roots in graph_roots.items():
        if roots != list(range(expected_edges)):
            raise SystemExit(f"order {order}, graph {record}: root sequence mismatch")
    expected_profile = {int(key): value for key, value in row["size_profile"].items()}
    if dict(size_profile) != expected_profile:
        raise SystemExit(f"order {order}: size profile mismatch")
    if singleton != row["singleton"] or singleton_nonbridge != 0:
        raise SystemExit(f"order {order}: singleton count mismatch")
    if row["roots"] != row["graphs"] * expected_edges:
        raise SystemExit(f"order {order}: degree/root arithmetic mismatch")
    return nonempty_nonbridge_masks


def parse_summary(text: str) -> dict:
    match = re.fullmatch(
        r"SUMMARY graphs=(\d+) roots=(\d+) singleton=(\d+) "
        r"singleton_nonbridge=(\d+) size_profile=([0-7]:\d+(?:,[0-7]:\d+)*)\n",
        text,
    )
    if not match:
        raise SystemExit("malformed retained order-15 summary")
    return {
        "graphs": int(match.group(1)),
        "roots": int(match.group(2)),
        "singleton": int(match.group(3)),
        "singleton_nonbridge": int(match.group(4)),
        "size_profile": {
            int(pair.split(":")[0]): int(pair.split(":")[1])
            for pair in match.group(5).split(",")
        },
    }


def parse_base_pair_summary(text: str, implementation: str) -> dict:
    match = re.fullmatch(
        rf"SUMMARY implementation={implementation} graphs=(\d+) "
        r"nonbridge_roots=(\d+) empty=(\d+) closed=(\d+) "
        r"violations=(\d+) calls=(\d+)\n",
        text,
    )
    if not match:
        raise SystemExit(
            f"malformed retained order-15 {implementation} base-pair summary"
        )
    return {
        "graphs": int(match.group(1)),
        "nonbridge_roots": int(match.group(2)),
        "empty": int(match.group(3)),
        "closed": int(match.group(4)),
        "violations": int(match.group(5)),
        "calls_per_implementation": int(match.group(6)),
    }


def main() -> int:
    if REPORT.get("schema") != "five-cdc-rooted-three-pole-frontier-v1":
        raise SystemExit("wrong report schema")
    source_paths = {
        "cadical": ROOT / "rooted_three_pole_cadical.cpp",
        "csp": ROOT / "rooted_three_pole_csp.cpp",
        "base_pair_cadical": ROOT / "rooted_base_pair_screen_cadical.cpp",
        "base_pair_csp": ROOT / "rooted_base_pair_screen_csp.cpp",
    }
    for name, expected in REPORT["sources"].items():
        if not HEX64.fullmatch(expected):
            raise SystemExit("malformed source digest")
        source = source_paths.get(name)
        if source is None:
            raise SystemExit(f"unrecognized source key: {name}")
        if digest(source) != expected:
            raise SystemExit(f"{name}: source digest mismatch")

    realized = set()
    for row in REPORT["orders"][:-1]:
        realized.update(verify_full_order(row))

    order15 = REPORT["orders"][-1]
    csp_summary_path = ROOT / "artifacts/order15-csp-summary.log"
    sat_summary_path = ROOT / "artifacts/order15-cadical-summary.log"
    if digest(csp_summary_path) != order15["summary_sha256"]:
        raise SystemExit("order 15: CSP summary digest mismatch")
    if csp_summary_path.read_bytes() != sat_summary_path.read_bytes():
        raise SystemExit("order 15: independent summaries differ")
    summary = parse_summary(csp_summary_path.read_text(encoding="utf-8"))
    expected_summary = {
        "graphs": order15["graphs"],
        "roots": order15["roots"],
        "singleton": order15["singleton"],
        "singleton_nonbridge": order15["singleton_nonbridge"],
        "size_profile": {
            int(key): value for key, value in order15["size_profile"].items()
        },
    }
    if summary != expected_summary:
        raise SystemExit("order 15: summary/report mismatch")
    for implementation in ("csp", "cadical"):
        path = ROOT / f"artifacts/order15-{implementation}-nonbridge-singletons.tsv"
        if digest(path) != order15["violation_output_sha256"] or path.read_bytes():
            raise SystemExit(f"order 15: {implementation} reported a violation")

    minimal = {
        mask
        for mask in realized
        if not any(other != mask and other & mask == other for other in realized)
    }
    if minimal != {0x0C, 0x12, 0x21}:
        raise SystemExit("base-pair minimal-mask mismatch")
    if any(
        not any(mask & base == base for base in minimal)
        for mask in realized
    ):
        raise SystemExit("base-pair containment violation")
    relations = {relation(first, second) for first in realized for second in realized}
    if relations != {"DI", "DEI"}:
        raise SystemExit("rooted cross-relation profile mismatch")
    exceptional_relations = {"E", "EI", "D"}
    for base in minimal:
        for invariant_mask in range(1, 1 << 7):
            if relation(base, invariant_mask) in exceptional_relations:
                raise SystemExit("one-sided base-pair relation lemma failed")
    if len(realized) != REPORT["base_pair_scope"][
        "distinct_nonempty_nonbridge_masks_through_order_13"
    ]:
        raise SystemExit("distinct rooted-mask count mismatch")

    base_pair = REPORT["base_pair_scope"]["order_15_targeted_screen"]
    expected_base_pair = {
        "graphs": base_pair["graphs"],
        "nonbridge_roots": base_pair["nonbridge_roots"],
        "empty": base_pair["empty"],
        "closed": base_pair["closed"],
        "violations": base_pair["violations"],
        "calls_per_implementation": base_pair["calls_per_implementation"],
    }
    for implementation in ("csp", "cadical"):
        summary_path = (
            ROOT
            / "artifacts"
            / f"order15-base-pair-{implementation}-summary.log"
        )
        actual = parse_base_pair_summary(
            summary_path.read_text(encoding="utf-8"),
            implementation,
        )
        if actual != expected_base_pair:
            raise SystemExit(
                f"order 15: {implementation} base-pair summary/report mismatch"
            )
        transcript_path = (
            ROOT
            / "artifacts"
            / f"order15-base-pair-{implementation}-transcript.sha256"
        )
        expected_line = f"{base_pair['transcript_sha256']}  -\n"
        if transcript_path.read_text(encoding="ascii") != expected_line:
            raise SystemExit(
                f"order 15: {implementation} base-pair transcript mismatch"
            )
    if base_pair["empty"] + base_pair["closed"] != base_pair["nonbridge_roots"]:
        raise SystemExit("order 15: base-pair root accounting mismatch")

    order17 = REPORT["base_pair_scope"]["order_17_targeted_screen"]
    if REPORT["base_pair_scope"]["orders_checked"] != [
        3,
        5,
        7,
        9,
        11,
        13,
        15,
        17,
    ]:
        raise SystemExit("base-pair checked-order list mismatch")
    order17_report_path = ROOT / order17["report"]
    if digest(order17_report_path) != order17["report_sha256"]:
        raise SystemExit("order 17: aggregate report digest mismatch")
    retained_order17 = json.loads(
        order17_report_path.read_text(encoding="utf-8")
    )
    replay = subprocess.run(
        [
            sys.executable,
            str(ROOT / "verify_order17_base_pair_run.py"),
            str(ROOT / "artifacts/order17-base-pair"),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    replayed_order17 = json.loads(replay.stdout)
    if retained_order17 != replayed_order17:
        raise SystemExit("order 17: retained/replayed aggregate mismatch")
    expected_order17 = {
        "graphs": order17["graphs"],
        "nonbridge_roots": order17["nonbridge_roots"],
        "empty": order17["empty"],
        "closed": order17["closed"],
        "violations": order17["violations"],
        "calls": order17["calls_per_implementation"],
    }
    if {
        key: retained_order17[key] for key in expected_order17
    } != expected_order17:
        raise SystemExit("order 17: report/scope totals mismatch")
    if len(retained_order17["shards"]) != order17["shards"]:
        raise SystemExit("order 17: shard count mismatch")

    print(
        "PASS rooted frontier: no nonbridge singleton through order 15; "
        "base-pair closure through order 17"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
