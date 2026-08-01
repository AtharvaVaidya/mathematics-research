#!/usr/bin/env python3
"""Check the frozen size-fourteen census and the Kempe escape linkage."""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
KEMPE = ROOT.parent / "minimum-projection-size14-kempe-escape-20260729"

RESULT = re.compile(
    r"RESULT shape=(\S+) canonical_words=(\d+)"
    r"(?: shard=(\d+)/(\d+) selected_words=(\d+))?"
    r" charge_valid=(\d+) dirty=(\d+) direct_clean=(\d+)"
    r" delete_branch=(\d+) dichotomy_failures=(\d+)"
)
COUNTERSTATE = re.compile(r"COUNTERSTATE word=\S+ partition=\d+")


@dataclass(frozen=True)
class Counts:
    words: int
    charge: int
    dirty: int
    direct: int
    delete: int
    failures: int

    def check_partition(self) -> None:
        assert self.direct + self.delete + self.failures == self.dirty


EXPECTED_FIXED = {
    "4+4+6": Counts(22, 6_078_286, 5_408_156, 5_408_156, 0, 0),
    "4+5+5": Counts(14, 3_831_414, 3_401_666, 3_401_596, 70, 0),
    "4+10": Counts(
        416, 114_769_776, 100_736_602, 100_735_166, 1_436, 0
    ),
    "5+9": Counts(
        505, 138_260_253, 121_073_174, 121_032_843, 40_331, 0
    ),
    "6+8": Counts(
        809, 223_526_053, 195_911_662, 195_844_374, 67_288, 0
    ),
    "7+7": Counts(
        333, 91_481_505, 80_104_020, 80_066_557, 37_239, 224
    ),
}

EXPECTED_SINGLE = Counts(
    7_382, 2_038_187_702, 1_748_842_896, 1_748_842_896, 0, 0
)

FIXED_FILES = (
    "triples-census.txt",
    "shape4p10-census.txt",
    "shape5p9-census.txt",
    "shape6p8-census.txt",
    "shape7p7-census.txt",
)


def parsed_results(path: Path):
    text = path.read_text(encoding="utf-8")
    rows = []
    for match in RESULT.finditer(text):
        (
            shape,
            words,
            shard,
            shards,
            selected,
            charge,
            dirty,
            direct,
            delete,
            failures,
        ) = match.groups()
        rows.append(
            (
                shape,
                Counts(
                    int(words),
                    int(charge),
                    int(dirty),
                    int(direct),
                    int(delete),
                    int(failures),
                ),
                None
                if shard is None
                else (int(shard), int(shards), int(selected)),
            )
        )
    return text, rows


def add_counts(rows: list[Counts], *, words: int | None = None) -> Counts:
    return Counts(
        sum(row.words for row in rows) if words is None else words,
        sum(row.charge for row in rows),
        sum(row.dirty for row in rows),
        sum(row.direct for row in rows),
        sum(row.delete for row in rows),
        sum(row.failures for row in rows),
    )


def main() -> None:
    observed_fixed = {}
    failure_lines = []
    for filename in FIXED_FILES:
        text, rows = parsed_results(ROOT / filename)
        for shape, counts, shard in rows:
            assert shard is None
            assert shape not in observed_fixed
            counts.check_partition()
            observed_fixed[shape] = counts
        failure_lines.extend(COUNTERSTATE.findall(text))
    assert observed_fixed == EXPECTED_FIXED
    assert len(failure_lines) == len(set(failure_lines)) == 224
    assert len(failure_lines) == EXPECTED_FIXED["7+7"].failures

    kempe_lines = (
        KEMPE.joinpath("failure-states.txt")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    assert failure_lines == kempe_lines

    shard_counts = []
    selected_total = 0
    seen_shards = set()
    canonical_words = None
    for shard in range(12):
        path = ROOT / f"single14-shard12-{shard}.txt"
        text, rows = parsed_results(path)
        assert not COUNTERSTATE.search(text)
        assert len(rows) == 1
        shape, counts, metadata = rows[0]
        assert shape == "14"
        assert metadata is not None
        observed_shard, shards, selected = metadata
        assert (observed_shard, shards) == (shard, 12)
        assert selected == (616 if shard < 2 else 615)
        assert observed_shard not in seen_shards
        seen_shards.add(observed_shard)
        if canonical_words is None:
            canonical_words = counts.words
        assert counts.words == canonical_words
        counts.check_partition()
        selected_total += selected
        shard_counts.append(counts)
    assert seen_shards == set(range(12))
    assert canonical_words is not None
    assert selected_total == canonical_words
    single = add_counts(shard_counts, words=canonical_words)
    single.check_partition()
    assert single == EXPECTED_SINGLE

    all_shapes = list(observed_fixed.values()) + [single]
    total = add_counts(all_shapes)
    total.check_partition()
    assert total.failures == 224

    subprocess.run(
        [sys.executable, str(KEMPE / "verify_all_certificates.py")],
        check=True,
    )

    print("shape words charge_valid dirty direct_clean delete failures")
    for shape in (
        "4+4+6",
        "4+5+5",
        "4+10",
        "5+9",
        "6+8",
        "7+7",
    ):
        row = observed_fixed[shape]
        print(shape, *row.__dict__.values())
    print("14", *single.__dict__.values())
    print("TOTAL", *total.__dict__.values())
    print("PASS: the only primary residuals are the 224 Kempe-excluded rows")


if __name__ == "__main__":
    main()
