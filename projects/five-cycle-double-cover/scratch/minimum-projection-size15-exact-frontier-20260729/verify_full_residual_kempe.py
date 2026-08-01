#!/usr/bin/env python3
"""Run the realization-robust one/two-path game on every census residual."""

from __future__ import annotations

import re
from pathlib import Path

from kempe_game import analyze_state, parse_state
from targeted_extensions import classify, encode_word


ROOT = Path(__file__).resolve().parent
LINE = re.compile(r"COUNTERSTATE word=(\S+) partition=(\d+)$")


def residuals():
    seen = set()
    for path in sorted(ROOT.glob("*-shard16-*.txt")):
        for raw in path.read_text(encoding="utf-8").splitlines():
            match = LINE.fullmatch(raw)
            if match is None:
                continue
            state = parse_state(*match.groups())
            assert state not in seen, (path, raw)
            seen.add(state)
            yield state


def main():
    states = list(residuals())
    print(f"residual_states={len(states)}")
    robust = 0
    failures = []
    for index, (word, partition, lengths) in enumerate(states, 1):
        feasible, cleans, deletes, _certificate = classify(
            word, partition, lengths
        )
        assert feasible and not cleans and not deletes
        rescued, attempts = analyze_state(word, partition, lengths)
        if rescued:
            robust += 1
        else:
            first_bad = tuple(
                (
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[5][-1][0] if row[5] else None,
                )
                for row in attempts
            )
            failures.append((word, partition, lengths, first_bad))
            print(
                "KEMPE_COUNTERSTATE"
                f" word={encode_word(word, lengths)}"
                f" partition={''.join(map(str, partition))}"
                f" feasible={feasible}"
            )
        if index % 250 == 0:
            print(
                f"progress={index}/{len(states)}"
                f" robust={robust} counterstates={len(failures)}"
            )
    print(
        f"RESULT checked={len(states)} robust={robust}"
        f" kempe_counterstates={len(failures)}"
    )
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
