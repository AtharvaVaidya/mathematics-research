#!/usr/bin/env python3
"""Verify frozen cyclic-block census summaries and arithmetic."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED = {
    12: {
        "status": "PASS",
        "graphs": 81,
        "flows": 25_960,
        "terminal_states": 20_578,
        "oriented_root_tests": 6_296_868,
        "applicable": 278_412,
        "positive_blocker_tests": 508,
        "fixed_distance_blocker_plateaus": 67_504,
        "maximum_blocker": 1,
    },
    14: {
        "status": "PASS",
        "graphs": 480,
        "flows": 537_418,
        "terminal_states": 400_668,
        "oriented_root_tests": 168_280_560,
        "applicable": 8_362_978,
        "positive_blocker_tests": 47_011,
        "fixed_distance_blocker_plateaus": 1_293_664,
        "maximum_blocker": 1,
    },
}


def main():
    for order, expected in EXPECTED.items():
        path = ROOT / f"d5-cyclic-block-lex-order{order}.json"
        observed = json.loads(path.read_text(encoding="utf-8"))
        assert observed == expected
        edge_count = 3 * order // 2
        assert observed["oriented_root_tests"] == (
            observed["terminal_states"] * edge_count * (edge_count - 1)
        )
        assert 0 <= observed["positive_blocker_tests"] <= observed["applicable"]
        assert observed["maximum_blocker"] == 1
    print("PASS")
    print("order 12 and 14 frozen cyclic-block summaries verified")


if __name__ == "__main__":
    main()
