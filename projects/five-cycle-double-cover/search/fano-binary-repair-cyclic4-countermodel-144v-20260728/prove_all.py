#!/usr/bin/env python3
"""Generate and independently check 28 auxiliary and one Tait LRAT proof."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
import subprocess


PACKAGE = Path(__file__).resolve().parent
CNF_MANIFEST = PACKAGE / "cnf-manifest.json"
LRAT_DIR = PACKAGE / "lrat"
LOG_DIR = PACKAGE / "logs"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run_logged(
    command: list[str],
    log: Path,
    accepted_codes: tuple[int, ...] = (0,),
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, text=True, capture_output=True)
    log.write_text(
        "$ " + " ".join(command) + "\n"
        + completed.stdout
        + completed.stderr
        + f"\nexit_code={completed.returncode}\n",
        encoding="utf-8",
        newline="\n",
    )
    if completed.returncode not in accepted_codes:
        raise RuntimeError(f"command failed; see {log}")
    return completed


def prove(instance: dict[str, object], tools: dict[str, str]) -> dict[str, object]:
    name = str(instance["name"])
    cnf = PACKAGE / str(instance["path"])
    lrat = LRAT_DIR / f"{name}.lrat"
    solver = run_logged(
        [tools["cadical"], "--lrat", "--no-binary", str(cnf), str(lrat)],
        LOG_DIR / f"{name}-cadical.txt",
        (20,),
    )
    if "UNSATISFIABLE" not in solver.stdout:
        raise RuntimeError(f"{name}: solver did not report UNSAT")
    first = run_logged(
        [tools["lrat_check"], str(cnf), str(lrat)],
        LOG_DIR / f"{name}-lrat-check.txt",
    )
    second = run_logged(
        [tools["cake_lpr"], str(cnf), str(lrat)],
        LOG_DIR / f"{name}-cake-lpr.txt",
    )
    if "VERIFIED" not in first.stdout:
        raise RuntimeError(f"{name}: lrat-check did not verify")
    if "VERIFIED" not in second.stdout:
        raise RuntimeError(f"{name}: cake_lpr did not verify")
    result = dict(instance)
    result.update({
        "lrat": str(lrat.relative_to(PACKAGE)),
        "lrat_bytes": lrat.stat().st_size,
        "lrat_sha256": digest(lrat),
        "cadical": "UNSATISFIABLE",
        "lrat_check": next(
            line.strip() for line in first.stdout.splitlines()
            if "VERIFIED" in line
        ),
        "cake_lpr": next(
            line.strip() for line in second.stdout.splitlines()
            if "VERIFIED" in line
        ),
    })
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cadical", default="/opt/homebrew/bin/cadical")
    parser.add_argument(
        "--lrat-check",
        default=(
            "/Users/atharvavaidya/Documents/conjectures/"
            ".tools/cert-checkers/drat-trim/lrat-check"
        ),
    )
    parser.add_argument(
        "--cake-lpr",
        default=(
            "/Users/atharvavaidya/Documents/conjectures/"
            ".tools/cert-checkers/cake_lpr/cake_lpr"
        ),
    )
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    tools = {
        "cadical": args.cadical,
        "lrat_check": args.lrat_check,
        "cake_lpr": args.cake_lpr,
    }
    for path in tools.values():
        if not Path(path).is_file():
            raise FileNotFoundError(path)
    source = json.loads(CNF_MANIFEST.read_text(encoding="ascii"))
    LRAT_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
    results = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(prove, instance, tools): str(instance["name"])
            for instance in source["instances"]
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                result["name"],
                result["cadical"],
                result["lrat_check"],
                result["cake_lpr"],
                flush=True,
            )
    by_name = {str(row["name"]): row for row in results}
    ordered = [by_name[str(row["name"])] for row in source["instances"]]
    payload = {
        "schema": "fano-binary-repair-cyclic4-order144-lrat-manifest-v1",
        "cnf_manifest_sha256": digest(CNF_MANIFEST),
        "tools": tools,
        "instances": ordered,
        "total_lrat_bytes": sum(int(row["lrat_bytes"]) for row in ordered),
        "all_instances_unsat": True,
        "all_instances_lrat_check_verified": True,
        "all_instances_cake_lpr_verified": True,
    }
    (PACKAGE / "proof-manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
        newline="\n",
    )
    print(json.dumps({
        "proved": len(ordered),
        "lrat_bytes": payload["total_lrat_bytes"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
