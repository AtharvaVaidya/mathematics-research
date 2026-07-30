#!/usr/bin/env python3
"""Verify the frozen lift-13 trap-directed portfolio and audit summaries."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
AUDITS = HERE / "audits"
EXPECTED_RUNS = {
    (0, 211): (500, 498, 18, 16, 207646),
    (13, 211): (500, 500, 17, 15, 211490),
    (26, 211): (500, 500, 11, 8, 214010),
    (39, 211): (500, 499, 22, 22, 204636),
    (52, 211): (500, 499, 25, 24, 205604),
    (65, 211): (500, 500, 17, 14, 192838),
    (78, 211): (500, 499, 18, 18, 206342),
    (91, 211): (500, 500, 15, 10, 199382),
    (104, 211): (500, 500, 19, 18, 205012),
    (117, 211): (500, 498, 22, 20, 202630),
    (0, 307): (300, 300, 15, 12, 121568),
    (39, 307): (300, 300, 8, 5, 125546),
    (91, 307): (300, 298, 16, 14, 123366),
}


def load_lines(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def audit_path(raw_path: Path) -> Path:
    return AUDITS / raw_path.name.replace(".jsonl", "-radius3.jsonl")


def replay(raw_paths: list[Path]) -> None:
    for raw_path in raw_paths:
        completed = subprocess.run(
            [sys.executable, str(HERE / "audit_radius3.py")],
            stdin=raw_path.open("r", encoding="utf-8"),
            text=True,
            capture_output=True,
            check=True,
        )
        expected = audit_path(raw_path).read_text(encoding="utf-8")
        if completed.stdout != expected:
            raise AssertionError(f"audit replay mismatch: {raw_path.name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--replay",
        action="store_true",
        help="recompute every exact neighborhood and escape (slow)",
    )
    arguments = parser.parse_args()

    raw_paths = sorted(RAW.glob("*.jsonl"))
    audit_paths = sorted(AUDITS.glob("*.jsonl"))
    assert len(raw_paths) == len(audit_paths) == len(EXPECTED_RUNS) == 13

    root_rows = []
    augmented_rows = []
    audit_escape_rows = []
    raw_hashes = {}
    audit_hashes = {}
    for raw_path in raw_paths:
        rows = load_lines(raw_path)
        roots = [row for row in rows if row["status"] == "ROOT_DONE"]
        assert len(roots) == 1 and rows[-1] == roots[0]
        root_row = roots[0]
        key = (int(root_row["root"]), int(root_row["seed"]))
        assert key in EXPECTED_RUNS
        expected = EXPECTED_RUNS[key]
        assert (
            int(root_row["steps"]),
            int(root_row["distinct_states"]),
            int(root_row["distinct_local_minima_audited"]),
            int(root_row["exact_augmented_traps"]),
            int(root_row["exact_neighbours_checked"]),
        ) == expected
        traps = [
            row for row in rows
            if row["status"] == "EXACT_AUGMENTED_TRAP"
        ]
        old_only = [
            row for row in rows if row["status"] == "EXACT_OLD_TRAP"
        ]
        assert len(traps) == int(root_row["exact_augmented_traps"])
        assert len(traps) + len(old_only) == int(
            root_row["distinct_local_minima_audited"]
        )
        assert all(
            int(row["parallel_successful_flags"]) == 0
            and int(row["lower_neighbours"]) == 0
            and int(row["parallel_success_neighbours"]) == 0
            and len(row["full_neighbourhood"])
                == int(row["legal_neighbours"])
            for row in traps
        )

        corresponding_audit = audit_path(raw_path)
        audit_rows = load_lines(corresponding_audit)
        audit_roots = [
            row for row in audit_rows if row["status"] == "ROOT_DONE"
        ]
        escapes = [
            row for row in audit_rows if row["status"] == "ESCAPES"
        ]
        assert len(audit_roots) == 1
        assert len(escapes) == len(traps)
        assert not any(
            row["status"] == "RADIUS_THREE_COUNTEREXAMPLE"
            for row in audit_rows
        )
        by_step = {int(row["step"]): row for row in traps}
        assert set(by_step) == {int(row["step"]) for row in escapes}
        for escape in escapes:
            trap = by_step[int(escape["step"])]
            assert int(escape["distance"]) == 2
            assert tuple(escape["seed_psi"]) == (
                int(trap["d_min"]),
                int(trap["kernel_sum"]),
            )
            assert (
                tuple(escape["endpoint_psi"])
                    < tuple(escape["seed_psi"])
                or int(escape["endpoint_flags"]) > 0
            )
            assert len(escape["escape_exchanges_local_positions"]) == 2

        root_rows.append(root_row)
        augmented_rows.extend(traps)
        audit_escape_rows.extend(
            {
                **escape,
                "_root": key[0],
                "_seed": key[1],
            }
            for escape in escapes
        )
        raw_hashes[raw_path.name] = file_sha256(raw_path)
        audit_hashes[corresponding_audit.name] = file_sha256(
            corresponding_audit
        )

    if arguments.replay:
        replay(raw_paths)

    sampled_steps = sum(int(row["steps"]) for row in root_rows)
    distinct_states = sum(
        int(row["distinct_states"]) for row in root_rows
    )
    search_legal_neighbours = sum(
        int(row["exact_neighbours_checked"]) for row in root_rows
    )
    safe_sources = sum(
        int(row["safe_sources_examined"]) for row in audit_escape_rows
    )
    later_legal_arcs = sum(
        int(row["legal_arcs_examined"]) for row in audit_escape_rows
    )
    start_legal_neighbours = sum(
        int(row["legal_neighbours"]) for row in augmented_rows
    )
    candidate_exchanges = 12288 * (
        len(augmented_rows) + safe_sources
    )
    maximum_source_row = max(
        audit_escape_rows,
        key=lambda row: int(row["safe_sources_examined"]),
    )
    summary = {
        "status": "PASS",
        "scope": "deterministic_sample_only_not_complete_state_space",
        "graph": "lift13_petersen_girth10",
        "runs": len(root_rows),
        "roots": sorted({int(row["root"]) for row in root_rows}),
        "seeds": sorted({int(row["seed"]) for row in root_rows}),
        "sampled_steps": sampled_steps,
        "distinct_states_sum_across_runs": distinct_states,
        "old_objective_local_minima_audited": sum(
            int(row["distinct_local_minima_audited"])
            for row in root_rows
        ),
        "exact_augmented_traps": len(augmented_rows),
        "escape_distance_histogram": dict(
            sorted(Counter(
                int(row["distance"]) for row in audit_escape_rows
            ).items())
        ),
        "radius_three_counterexamples": 0,
        "producer_legal_neighbour_evaluations_over_all_sample_steps":
            search_legal_neighbours,
        "independent_audit_seed_candidate_exchanges":
            12288 * len(augmented_rows),
        "independent_audit_safe_sources_examined": safe_sources,
        "independent_audit_total_candidate_exchanges":
            candidate_exchanges,
        "independent_audit_seed_legal_neighbours":
            start_legal_neighbours,
        "independent_audit_later_legal_arcs": later_legal_arcs,
        "independent_audit_total_legal_neighbours":
            start_legal_neighbours + later_legal_arcs,
        "maximum_safe_sources_before_escape": {
            "count": int(maximum_source_row["safe_sources_examined"]),
            "root": int(maximum_source_row["_root"]),
            "seed": int(maximum_source_row["_seed"]),
            "step": int(maximum_source_row["step"]),
            "seed_psi": maximum_source_row["seed_psi"],
        },
        "raw_sha256": raw_hashes,
        "audit_sha256": audit_hashes,
        "full_replay_performed": bool(arguments.replay),
    }
    frozen_summary = json.loads(json.dumps({
        **summary,
        "full_replay_performed": False,
    }))
    assert frozen_summary == json.loads(
        (HERE / "SUMMARY.json").read_text(encoding="utf-8")
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
