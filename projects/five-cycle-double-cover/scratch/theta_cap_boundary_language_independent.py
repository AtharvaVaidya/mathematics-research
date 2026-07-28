#!/usr/bin/env python3
"""Independent audit of the ordered theta-cap D5 boundary relation.

This is a separately written implementation: it neither imports nor mimics
theta_cap_boundary_language.py.  It builds the local relation directly from
the five parity equations and solves the resulting small CSP for each even
ordered boundary word.
"""

from itertools import combinations, permutations, product
from collections import Counter
import json

COLORS = tuple(range(5))
LABELS = tuple(sum(1 << x for x in p) for p in combinations(COLORS, 2))
LABELSET = set(LABELS)
S5 = tuple(permutations(COLORS))

# Boundary names are deliberately tied explicitly to the stated terminal order.
BOUNDARY = ("b0", "b1", "b2", "b3", "b4")
INTERNAL = ("e01", "e23", "e0a", "e2a", "e4a",
            "e1b", "e3b", "e4b")
VERTICES = {
    "w0": ("b0", "e01", "e0a"),
    "w1": ("b1", "e01", "e1b"),
    "w2": ("b2", "e23", "e2a"),
    "w3": ("b3", "e23", "e3b"),
    "w4": ("b4", "e4a", "e4b"),
    "z0": ("e0a", "e2a", "e4a"),
    "z1": ("e1b", "e3b", "e4b"),
}
INCIDENT = {
    edge: tuple(v for v, row in VERTICES.items() if edge in row)
    for edge in BOUNDARY + INTERNAL
}

# Native definition: each coordinate occurs an even number of times.
LOCAL = tuple(
    row for row in product(LABELS, repeat=3)
    if row[0] ^ row[1] ^ row[2] == 0
)


def compatible_rows(vertex, assignment):
    edges = VERTICES[vertex]
    return tuple(
        row for row in LOCAL
        if all(edge not in assignment or assignment[edge] == row[i]
               for i, edge in enumerate(edges))
    )


def solve_boundary(word):
    assignment = dict(zip(BOUNDARY, word))

    def recurse(current):
        current = dict(current)
        while True:
            rows_at = {}
            for vertex in VERTICES:
                rows = compatible_rows(vertex, current)
                if not rows:
                    return None
                rows_at[vertex] = rows

            changed = False
            domains = {}
            for edge in INTERNAL:
                if edge in current:
                    continue
                possible = set(LABELS)
                for vertex in INCIDENT[edge]:
                    slot = VERTICES[vertex].index(edge)
                    possible &= {row[slot] for row in rows_at[vertex]}
                if not possible:
                    return None
                domains[edge] = possible
                if len(possible) == 1:
                    current[edge] = next(iter(possible))
                    changed = True
            if not changed:
                break

        if all(edge in current for edge in INTERNAL):
            return current

        edge = min(domains, key=lambda e: (len(domains[e]), e))
        for label in sorted(domains[edge]):
            trial = dict(current)
            trial[edge] = label
            answer = recurse(trial)
            if answer is not None:
                return answer
        return None

    return recurse(assignment)


def relabel_mask(label, p):
    result = 0
    for old in COLORS:
        if label & (1 << old):
            result |= 1 << p[old]
    return result


def canonical(word):
    return min(tuple(relabel_mask(label, p) for label in word) for p in S5)


def text(label):
    return "".join(str(x) for x in COLORS if label & (1 << x))


def parse_word(strings):
    return tuple(sum(1 << int(x) for x in s) for s in strings)


def local_ok(labels):
    return all(label in LABELSET for label in labels) and (
        labels[0] ^ labels[1] ^ labels[2] == 0
    )


def validate_displayed_row(boundary, internal):
    b = parse_word(boundary)
    e = parse_word(internal)
    assignment = dict(zip(BOUNDARY, b))
    assignment.update(dict(zip(INTERNAL, e)))
    failures = []
    for vertex, edges in VERTICES.items():
        labels = tuple(assignment[edge] for edge in edges)
        if not local_ok(labels):
            failures.append((vertex, tuple(text(x) for x in labels)))
    return failures


def toggle(word, positions, pairmask):
    answer = list(word)
    for i in positions:
        answer[i] ^= pairmask
    assert all(x in LABELSET for x in answer)
    return tuple(answer)


def main():
    assert len(LOCAL) == 60

    # Boundary parity determines b4 from b0..b3.
    all_even = set()
    witnesses = {}
    for prefix in product(LABELS, repeat=4):
        last = prefix[0] ^ prefix[1] ^ prefix[2] ^ prefix[3]
        if last not in LABELSET:
            continue
        word = prefix + (last,)
        all_even.add(word)
        witness = solve_boundary(word)
        if witness is not None:
            witnesses[word] = tuple(witness[e] for e in INTERNAL)

    even_orbits = {canonical(w) for w in all_even}
    theta_orbits = {canonical(w) for w in witnesses}
    missing = tuple(sorted(even_orbits - theta_orbits))

    # A separate direct join for the three-vertex path cap.  Local tuple slots
    # are (internal edge, first port, second port) at its end vertices and
    # (left internal, right internal, middle port) at its middle vertex.
    path_words = set()
    for left_state in LOCAL:
        for middle_state in LOCAL:
            if left_state[0] != middle_state[0]:
                continue
            for right_state in LOCAL:
                if right_state[0] != middle_state[1]:
                    continue
                path_words.add((
                    left_state[1], left_state[2],
                    right_state[1], right_state[2],
                    middle_state[2],
                ))

    # Independently enumerate coordinate 5-cycles and the two symmetry groups.
    cycle_label_sets = {
        frozenset(
            (1 << order[i]) | (1 << order[(i + 1) % 5])
            for i in range(5)
        )
        for order in permutations(COLORS)
    }
    simple_cycle_words = {
        word
        for edge_set in cycle_label_sets
        for word in permutations(tuple(edge_set))
    }

    cap_edges = {
        frozenset(edge) for edge in (
            (0, 1), (2, 3), (0, 5), (2, 5), (4, 5),
            (1, 6), (3, 6), (4, 6),
        )
    }
    cap_terminal_actions = set()
    for image in permutations(range(7)):
        if {image[i] for i in range(5)} != set(range(5)):
            continue
        moved = {
            frozenset((image[u], image[v])) for u, v in map(tuple, cap_edges)
        }
        if moved == cap_edges:
            cap_terminal_actions.add(image[:5])

    canonical_cycle = frozenset(
        ((1 << 0) | (1 << 1),
         (1 << 1) | (1 << 2),
         (1 << 2) | (1 << 3),
         (1 << 3) | (1 << 4),
         (1 << 4) | (1 << 0))
    )
    cycle_color_actions = tuple(
        p for p in S5
        if frozenset(relabel_mask(edge, p) for edge in canonical_cycle)
        == canonical_cycle
    )

    unseen = set(permutations(tuple(canonical_cycle)))
    placement_orbit_sizes = []
    while unseen:
        seed = next(iter(unseen))
        orbit = set()
        for terminal_action in cap_terminal_actions:
            for color_action in cycle_color_actions:
                moved = [None] * 5
                for old_terminal in range(5):
                    moved[terminal_action[old_terminal]] = relabel_mask(
                        seed[old_terminal], color_action
                    )
                orbit.add(tuple(moved))
        unseen -= orbit
        placement_orbit_sizes.append(len(orbit))

    expected_missing = (
        ("01", "01", "02", "12", "01"),
        ("01", "02", "01", "12", "01"),
        ("01", "02", "12", "02", "02"),
        ("01", "02", "12", "12", "12"),
    )
    expected_pairs = ((0, 3), (0, 3), (0, 3), (1, 3))
    switching = []
    for raw, color_pair in zip(expected_missing, expected_pairs):
        word = parse_word(raw)
        assert canonical(word) == word
        a, b = color_pair
        pairmask = (1 << a) | (1 << b)
        positions = tuple(
            i for i, label in enumerate(word)
            if bool(label & (1 << a)) != bool(label & (1 << b))
        )
        assert len(positions) == 4
        pairings = (
            ((positions[0], positions[1]), (positions[2], positions[3])),
            ((positions[0], positions[2]), (positions[1], positions[3])),
            ((positions[0], positions[3]), (positions[1], positions[2])),
        )
        cases = []
        for pairing in pairings:
            outputs = []
            for path in pairing:
                out = toggle(word, path, pairmask)
                outcanon = canonical(out)
                direct = solve_boundary(out)
                outputs.append({
                    "path": path,
                    "word": tuple(text(x) for x in out),
                    "orbit": tuple(text(x) for x in outcanon),
                    "directly_accepted": direct is not None,
                    "orbit_accepted": outcanon in theta_orbits,
                })
            cases.append(outputs)
        switching.append({
            "missing": raw,
            "pair": color_pair,
            "positions": positions,
            "cases": cases,
        })

    table = (
        (("01","12","23","34","04"),
         ("02","03","12","02","01","01","04","14")),
        (("01","12","23","04","34"),
         ("13","03","03","02","23","23","34","24")),
        (("01","12","34","23","04"),
         ("14","13","04","14","01","24","12","14")),
        (("01","12","04","23","34"),
         ("13","24","03","02","23","23","34","24")),
        (("01","23","12","34","04"),
         ("13","23","03","13","01","12","24","14")),
        (("01","23","12","04","34"),
         ("13","02","03","01","13","12","24","14")),
    )
    table_failures = [
        validate_displayed_row(boundary, internal)
        for boundary, internal in table
    ]

    orbit_sizes = Counter()
    for representative in even_orbits:
        orbit = {
            tuple(relabel_mask(label, p) for label in representative)
            for p in S5
        }
        orbit_sizes[len(orbit)] += 1

    report = {
        "implementation": "independent generic parity CSP",
        "local_states_from_parity": len(LOCAL),
        "ordered_even_words": len(all_even),
        "ordered_theta_words": len(witnesses),
        "ordered_path_words": len(path_words),
        "path_words_rejected_by_theta": len(path_words - set(witnesses)),
        "even_S5_orbits": len(even_orbits),
        "theta_S5_orbits": len(theta_orbits),
        "S5_orbit_size_distribution_even": dict(sorted(orbit_sizes.items())),
        "missing_orbits": [
            tuple(text(x) for x in word) for word in missing
        ],
        "missing_ordered_orbit_sizes": [
            len({
                tuple(relabel_mask(label, p) for label in word)
                for p in S5
            })
            for word in missing
        ],
        "coordinate_five_cycles": len(cycle_label_sets),
        "ordered_coordinate_five_cycles": len(simple_cycle_words),
        "all_coordinate_five_cycles_accepted": (
            simple_cycle_words <= set(witnesses)
        ),
        "cap_terminal_automorphisms": sorted(cap_terminal_actions),
        "coordinate_cycle_stabilizer_size": len(cycle_color_actions),
        "placement_orbit_sizes": sorted(placement_orbit_sizes),
        "displayed_table_failures": table_failures,
        "all_switch_outputs_directly_accepted": all(
            output["directly_accepted"]
            for item in switching for case in item["cases"] for output in case
        ),
        "all_switch_output_orbits_accepted": all(
            output["orbit_accepted"]
            for item in switching for case in item["cases"] for output in case
        ),
        "switching": switching,
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
