#!/usr/bin/env python3
"""Compile the exact scanner, replay the frozen inputs, and check aggregates."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]

CYCLIC_INPUTS = {
    10: (
        "search/focused-theta-choice-through28-20260727/artifacts/"
        "cyclic4-nontait-order10.g6",
        "7aec0fba73c081d7eebc551fc46b2484e73e58b2d36718dee105dbb6226e76aa",
    ),
    12: (
        "search/focused-theta-choice-through28-20260727/artifacts/"
        "cyclic4-nontait-order12.g6",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ),
    14: (
        "search/focused-theta-choice-through28-20260727/artifacts/"
        "cyclic4-nontait-order14.g6",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ),
    16: (
        "search/focused-theta-choice-through28-20260727/artifacts/"
        "cyclic4-nontait-order16.g6",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ),
    18: (
        "search/focused-theta-choice-through28-20260727/artifacts/"
        "cyclic4-nontait-order18.g6",
        "2660e7d5c8a351b4ed3d69f8df316e748e264a630c01328ea4bed43f96f78dfd",
    ),
    20: (
        "search/focused-theta-choice-through28-20260727/artifacts/"
        "cyclic4-nontait-order20.g6",
        "a65153d9dc38bebffca52b2c2ec05f194807b10ca097f50a551d5aab871244f1",
    ),
    22: (
        "search/focused-theta-choice-through28-20260727/artifacts/"
        "cyclic4-nontait-order22.g6",
        "2c3d91e55cb264450cf321e2299355f6cf0f5c2c60a83c99372a1d73ed5a4223",
    ),
    24: (
        "search/focused-theta-choice-through28-20260727/artifacts/"
        "cyclic4-nontait-order24.g6",
        "37ef068ab597c6cc882eb2121d9743464b0717bc4beefab4348ef4221b6a7456",
    ),
    26: (
        "search/focused-theta-choice-through28-20260727/artifacts/"
        "cyclic4-nontait-order26.g6",
        "1d2b95b9d412f5f6b8ccb788779bd685df23b3239bda8c7e9557266375519760",
    ),
    28: (
        "search/focused-theta-choice-through28-20260727/artifacts/"
        "cyclic4-nontait-order28.g6",
        "b4f6494c23793a40158a03ccd7c0943ae2e397c90a1467e27814bd007789be1f",
    ),
}

EXPECTED_CYCLIC = {
    10: (1, {5: 1}, 12),
    12: (0, {}, 0),
    14: (0, {}, 0),
    16: (0, {}, 0),
    18: (2, {5: 2}, 18),
    20: (6, {5: 6}, 40),
    22: (31, {5: 31}, 228),
    24: (155, {5: 155}, 1129),
    26: (1297, {5: 1297}, 9634),
    28: (12517, {5: 12515, 6: 1, 9: 1}, 92754),
}

HARD22 = (
    "search/four-pole-order22-cap-20260727/artifacts/order22-hard.g6",
    "230f2cd88e72011d73a40c5f3d7d5f9fb0fca6110de2ec2541581bc50982037c",
)
EXPECTED_HARD22 = (
    12892,
    {5: 11776, 6: 1025, 7: 55, 8: 20, 9: 6, 10: 10},
    54785,
)
BASE_SCANNER = (
    ROOT / "scratch/fano_all_bad_projection_search_linear.cpp",
    "bf713d5bdcaa11a76bf98b77422ab55914fba29e36792de71fbed53d102687db",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def source_rows(path: Path) -> list[str]:
    return [row for row in path.read_text(encoding="ascii").splitlines() if row]


def run_scan(binary: Path, path: Path) -> list[dict[str, object]]:
    completed = subprocess.run(
        (str(binary), str(path)),
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    rows = [json.loads(row) for row in completed.stdout.splitlines() if row]
    source = source_rows(path)
    assert len(rows) == len(source)
    for index, (observed, graph6) in enumerate(zip(rows, source)):
        assert observed["row"] == index
        assert observed["graph6"] == graph6
        assert observed["minimum"] > 0
        assert observed["minimum_extendable"] > 0
        assert observed["bad_minimum"] == 0
        assert observed["bad_hex"] == []
    return rows


def summary(rows: list[dict[str, object]]) -> tuple[int, dict[int, int], int]:
    return (
        len(rows),
        dict(sorted(Counter(int(row["minimum"]) for row in rows).items())),
        sum(int(row["minimum_extendable"]) for row in rows),
    )


def main() -> None:
    assert digest(BASE_SCANNER[0]) == BASE_SCANNER[1]
    for relative, expected_digest in tuple(CYCLIC_INPUTS.values()) + (HARD22,):
        assert digest(ROOT / relative) == expected_digest

    with tempfile.TemporaryDirectory(prefix="minimum-projection-") as directory:
        binary = Path(directory) / "scan"
        subprocess.run(
            (
                "c++",
                "-O3",
                "-std=c++20",
                str(PACKAGE / "scan.cpp"),
                "-o",
                str(binary),
            ),
            check=True,
        )
        total_cyclic = 0
        for order, (relative, _expected_digest) in CYCLIC_INPUTS.items():
            rows = run_scan(binary, ROOT / relative)
            observed = summary(rows)
            assert observed == EXPECTED_CYCLIC[order]
            total_cyclic += observed[0]
            print(
                json.dumps(
                    {
                        "order": order,
                        "graphs": observed[0],
                        "minimum_profile": observed[1],
                        "minimum_extendable": observed[2],
                        "bad_minimum": 0,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        assert total_cyclic == 14009

        hard_rows = run_scan(binary, ROOT / HARD22[0])
        hard_summary = summary(hard_rows)
        assert hard_summary == EXPECTED_HARD22
        print(
            json.dumps(
                {
                    "population": "frozen-order22-hard-source",
                    "graphs": hard_summary[0],
                    "minimum_profile": hard_summary[1],
                    "minimum_extendable": hard_summary[2],
                    "bad_minimum": 0,
                },
                sort_keys=True,
            ),
            flush=True,
        )

    print("PASS: exact minimum-projection summaries reproduced")


if __name__ == "__main__":
    main()
