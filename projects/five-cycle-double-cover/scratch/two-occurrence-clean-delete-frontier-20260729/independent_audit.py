#!/usr/bin/env python3
"""Independent literal checker for the loopless support-16 theorem.

Unlike the primary checker, this audit never uses the alternating
bilinear-form equation for cleanliness.  It integrates each local walk,
forms the two literal endpoint sets in F_2^2, and compares those sets.
"""

from __future__ import annotations

import itertools


POINTS = range(4)
NONZERO = (1, 2, 3)
PROFILES = ((3, 2, 2), (3, 3, 2), (4, 3, 1))
EXPECTED = {
    (3, 2, 2): {
        "flows": 138,
        "states": 432,
        "clean": 432,
        "delete_only": 0,
        "histogram": (
            (114, 12),
            (120, 24),
            (126, 132),
            (132, 120),
            (138, 144),
        ),
    },
    (3, 3, 2): {
        "flows": 402,
        "states": 8640,
        "clean": 8640,
        "delete_only": 0,
        "histogram": (
            (306, 180),
            (318, 72),
            (324, 144),
            (330, 1404),
            (336, 1584),
            (342, 1296),
            (348, 1944),
            (354, 360),
            (360, 648),
            (366, 468),
            (372, 360),
            (378, 144),
            (402, 36),
        ),
    },
    (4, 3, 1): {
        "flows": 420,
        "states": 12960,
        "clean": 12744,
        "delete_only": 216,
        "histogram": (
            (360, 936),
            (366, 1728),
            (372, 1872),
            (378, 3888),
            (384, 1296),
            (390, 1584),
            (396, 1008),
            (402, 144),
            (408, 432),
            (420, 72),
        ),
    },
}


def xor_all(values) -> int:
    answer = 0
    for value in values:
        answer ^= value
    return answer


def instance(profile):
    x01, x02, x12 = profile
    ends = (
        ((0, 1),) * x01
        + ((0, 2),) * x02
        + ((1, 2),) * x12
    )
    stars = tuple(
        tuple(edge for edge, pair in enumerate(ends) if vertex in pair)
        for vertex in range(3)
    )
    return ends, stars


def rotations(star):
    """All unoriented cyclic orders, by a direct anchored reversal test."""
    anchor = min(star)
    tail = tuple(edge for edge in star if edge != anchor)
    for permutation in itertools.permutations(tail):
        order = (anchor,) + permutation
        reversed_order = (anchor,) + tuple(reversed(permutation))
        if order <= reversed_order:
            yield order


def all_flows(edge_count, stars):
    return tuple(
        values
        for values in itertools.product(NONZERO, repeat=edge_count)
        if all(xor_all(values[edge] for edge in star) == 0 for star in stars)
    )


def literal_walk(order, flow):
    prefixes = {}
    point = 0
    visited = set()
    for edge in order:
        prefixes[edge] = point
        visited.add(point)
        point ^= flow[edge]
    assert point == 0
    return prefixes, frozenset(visited)


def classify(ends, orders, flow):
    prefixes = []
    visited = []
    for order in orders:
        local_prefixes, local_visited = literal_walk(order, flow)
        prefixes.append(local_prefixes)
        visited.append(local_visited)

    deletion = any(len(points) < 4 for points in visited)
    clean = False
    for shift1, shift2 in itertools.product(POINTS, repeat=2):
        shifts = (0, shift1, shift2)
        works = True
        for edge, (u, v) in enumerate(ends):
            first_u = prefixes[u][edge] ^ shifts[u]
            first_v = prefixes[v][edge] ^ shifts[v]
            pair_u = frozenset((first_u, first_u ^ flow[edge]))
            pair_v = frozenset((first_v, first_v ^ flow[edge]))
            if pair_u != pair_v:
                works = False
                break
        if works:
            clean = True
            break
    return clean, deletion


def audit_profile(profile):
    ends, stars = instance(profile)
    flow_rows = all_flows(len(ends), stars)
    order_rows = tuple(tuple(rotations(star)) for star in stars)
    states = 0
    clean_states = 0
    delete_only_states = 0
    no_goal_states = 0
    histogram = {}

    for orders in itertools.product(*order_rows):
        states += 1
        clean_count = 0
        deletion_count = 0
        goal_count = 0
        for flow in flow_rows:
            clean, deletion = classify(ends, orders, flow)
            clean_count += clean
            deletion_count += deletion
            goal_count += clean or deletion
        histogram[goal_count] = histogram.get(goal_count, 0) + 1
        if clean_count:
            clean_states += 1
        elif deletion_count:
            delete_only_states += 1
        else:
            no_goal_states += 1

    result = {
        "flows": len(flow_rows),
        "states": states,
        "clean": clean_states,
        "delete_only": delete_only_states,
        "histogram": tuple(sorted(histogram.items())),
    }
    assert no_goal_states == 0
    assert result == EXPECTED[profile], (profile, result)
    print(
        f"PROFILE multiplicities={profile}"
        f" degrees={tuple(map(len, stars))}"
        f" flows={result['flows']} states={result['states']}"
        f" clean_states={result['clean']}"
        f" delete_only_states={result['delete_only']}"
        f" no_goal_states={no_goal_states}"
    )
    print(f"  goal_histogram={result['histogram']}")
    return result


def main():
    totals = {"flows": 0, "states": 0, "clean": 0, "delete_only": 0}
    for profile in PROFILES:
        result = audit_profile(profile)
        for key in totals:
            totals[key] += result[key]
    assert totals == {
        "flows": 960,
        "states": 22032,
        "clean": 21816,
        "delete_only": 216,
    }
    print(f"TOTAL {totals}")
    print("PASS independent literal endpoint-set audit")


if __name__ == "__main__":
    main()
