#!/usr/bin/env python3
"""Test the affine six-hole criterion on all 900 flow orbits of the rigid 12v graph."""

from __future__ import annotations

from collections import Counter
import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE_PATH = HERE / "audit_six_point_one_hole_affine.py"
REPORT_PATH = ROOT / "output" / "oum-combined-choice-12v" / "all-flow-orbits.json"

spec = importlib.util.spec_from_file_location("six_hole_core", CORE_PATH)
assert spec is not None and spec.loader is not None
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

EDGES = [
    [0, 6], [0, 7], [0, 8], [1, 6], [1, 7], [1, 9],
    [2, 6], [2, 10], [2, 11], [3, 7], [3, 10], [3, 11],
    [4, 8], [4, 9], [4, 10], [5, 8], [5, 9], [5, 11],
]
INCIDENCE = core.graph_incidence(12, EDGES)


def translate_set(points: tuple[int, ...], shift: int) -> tuple[int, ...]:
    return tuple(sorted(point ^ shift for point in points))


def canonical_five(points: tuple[int, ...]) -> tuple[int, ...]:
    return min(translate_set(points, shift) for shift in core.W)


def canonical_pair_configuration(
    omitted: tuple[int, int], missing: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    return min(
        (
            translate_set(omitted, shift),
            translate_set(missing, shift),
        )
        for shift in core.W
    )


FIVE_REPRESENTATIVES = sorted(
    {
        canonical_five(points)
        for points in itertools.combinations(core.W, 5)
    }
)
PAIR_REPRESENTATIVES = sorted(
    {
        canonical_pair_configuration(omitted, missing)
        for omitted in itertools.combinations(core.W, 2)
        for missing in itertools.combinations(
            sorted(set(core.W) - set(omitted)), 2
        )
    }
)
assert len(FIVE_REPRESENTATIVES) == 7
assert len(PAIR_REPRESENTATIVES) == 63


def passes_five(flow: list[int], planes: list[frozenset[int]]) -> bool:
    return any(
        core.build_global_system(
            EDGES,
            INCIDENCE,
            flow,
            planes,
            frozenset(support),
            None,
        )["sat"]
        for support in FIVE_REPRESENTATIVES
    )


def passes_six_hole(flow: list[int], planes: list[frozenset[int]]) -> bool:
    for omitted, missing in PAIR_REPRESENTATIVES:
        support = frozenset(set(core.W) - set(omitted))
        if core.build_global_system(
            EDGES,
            INCIDENCE,
            flow,
            planes,
            support,
            frozenset(missing),
        )["sat"]:
            return True
    return False


def main() -> None:
    source = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    rows = source["flow_orbits"]
    assert len(rows) == 900
    profile: Counter[str] = Counter()
    weighted_profile: Counter[str] = Counter()
    examples: dict[str, list[int]] = {}

    for row in rows:
        flow = list(map(int, row["flow"]))
        planes = core.local_planes(INCIDENCE, flow)
        five = passes_five(flow, planes)
        six = passes_six_hole(flow, planes)
        general = int(row["successful_potentials"]) > 0
        assert not five or six
        assert not six or general
        key = f"five={int(five)},six_hole={int(six)},general={int(general)}"
        profile[key] += 1
        weighted_profile[key] += int(row["gl3_orbit_size"])
        examples.setdefault(key, flow)

    assert sum(profile.values()) == 900
    assert sum(weighted_profile.values()) == 150_192
    assert sum(
        count for key, count in profile.items() if key.endswith("general=0")
    ) == 64
    report = {
        "schema": "six-point-one-hole-all-flow-12v-v1",
        "status": "PASS",
        "graph6": "K??FEaKR@oE_",
        "translation_orbit_representatives": {
            "five_sets": len(FIVE_REPRESENTATIVES),
            "six_point_one_hole_pairs": len(PAIR_REPRESENTATIVES),
        },
        "flow_orbits": len(rows),
        "labelled_flows": sum(weighted_profile.values()),
        "orbit_profile": dict(sorted(profile.items())),
        "labelled_flow_profile": dict(sorted(weighted_profile.items())),
        "first_examples": dict(sorted(examples.items())),
        "scope": (
            "Complete fixed-flow orbit census on one 12-vertex graph; "
            "not a graph-level obstruction and not a FiveCDC resolution."
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
