#!/usr/bin/env python3
"""Check every same-block one-occurrence extension of the size-14 residuals.

The family is a regression set only.  In particular, it omits insertions
whose two resulting derivative occurrences belong to distinct complement
components.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from kempe_game import analyze_state
from targeted_extensions import (
    FAILURES,
    LINE,
    classify,
    encode_word,
    insert_state,
)


def main() -> None:
    states = set()
    for raw in FAILURES.read_text(encoding="utf-8").splitlines():
        match = LINE.fullmatch(raw)
        assert match
        states.update(insert_state(*match.groups()))

    checked = robust = 0
    ordered = sorted(states, reverse="--reverse" in sys.argv[1:])
    for word, partition, lengths in ordered:
        feasible, cleans, deletes, _certificate = classify(
            word, partition, lengths
        )
        assert feasible and not cleans and not deletes
        checked += 1
        rescued, attempts = analyze_state(word, partition, lengths)
        if not rescued:
            print(
                "KEMPE_COUNTERSTATE"
                f" word={encode_word(word, lengths)}"
                f" partition={''.join(map(str, partition))}"
                f" feasible={feasible}"
            )
            for row in attempts:
                print(
                    "ATTEMPT"
                    f" block={row[0]} colours={row[1]}"
                    f" terminals={row[2]} matchings={row[3]}"
                    f" first_bad={row[5][-1][0] if row[5] else None}"
                )
            print(
                f"RESULT checked={checked} robust={robust}"
                " kempe_counterstates=1"
            )
            return
        robust += 1
        if checked % 250 == 0:
            print(f"progress={checked}/{len(states)} robust={robust}")
    print(
        f"RESULT checked={checked} robust={robust} kempe_counterstates=0"
    )


if __name__ == "__main__":
    main()
