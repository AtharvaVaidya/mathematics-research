#!/usr/bin/env python3
"""Independent finite checks for the second-coordinate descent note.

No code is imported from the candidate package.  Profiles are generated as
six-entry multiplicity vectors, not as sorted value tuples.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product


def xor_all(values):
    result = 0
    for value in values:
        result ^= value
    return result


def weak_compositions(total, slots):
    if slots == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, slots - 1):
            yield (first,) + tail


def value_xor(alphabet, multiplicities):
    return xor_all(
        value for value, count in zip(alphabet, multiplicities) if count & 1
    )


def pair_partition(b, alphabet):
    unseen = set(alphabet)
    pairs = []
    while unseen:
        value = min(unseen)
        partner = value ^ b
        assert partner in unseen
        pairs.append((alphabet.index(value), alphabet.index(partner)))
        unseen.remove(value)
        unseen.remove(partner)
    assert len(pairs) == 3
    return tuple(pairs)


def has_partner_free_occurrence(multiplicities, pairs):
    for left, right in pairs:
        if (multiplicities[left] > 0) != (multiplicities[right] > 0):
            return True
    return False


def audit_profiles():
    totals = Counter()
    failures = Counter()
    per_target = {}
    first_sharp = None
    for b in range(1, 8):
        alphabet = tuple(value for value in range(1, 8) if value != b)
        pairs = pair_partition(b, alphabet)
        target_report = []
        for size in (3, 5, 7, 9):
            admissible = saturated = 0
            for multiplicities in weak_compositions(size, 6):
                if value_xor(alphabet, multiplicities) != b:
                    continue
                admissible += 1
                pair_totals = tuple(
                    multiplicities[left] + multiplicities[right]
                    for left, right in pairs
                )
                # Projection to F_2^3/<b>: all three pair parities agree;
                # their odd total makes all three odd.
                assert tuple(total & 1 for total in pair_totals) == (1, 1, 1)
                partner_free = has_partner_free_occurrence(multiplicities, pairs)
                if size < 9:
                    assert partner_free
                if size == 3:
                    assert pair_totals == (1, 1, 1)
                    assert sum(count > 0 for count in multiplicities) == 3
                if not partner_free:
                    saturated += 1
                    assert size >= 9
                    if size == 9:
                        assert pair_totals == (3, 3, 3)
                        assert all(
                            multiplicities[left] > 0 and multiplicities[right] > 0
                            for left, right in pairs
                        )
                        if first_sharp is None:
                            first_sharp = (b, alphabet, multiplicities)
            totals[size] += admissible
            failures[size] += saturated
            target_report.append((size, admissible, saturated))
        per_target[b] = tuple(target_report)

    reference = per_target[1]
    assert all(report == reference for report in per_target.values())
    assert reference == ((3, 4, 0), (5, 24, 0), (7, 84, 0), (9, 224, 4))
    assert tuple(totals[k] for k in (3, 5, 7, 9)) == (28, 168, 588, 1568)
    assert tuple(failures[k] for k in (3, 5, 7, 9)) == (0, 0, 0, 28)

    displayed = (2, 2, 3, 4, 4, 5, 6, 6, 7)
    assert xor_all(displayed) == 1
    display_counts = Counter(displayed)
    display_alphabet = tuple(range(2, 8))
    display_vector = tuple(display_counts[value] for value in display_alphabet)
    assert not has_partner_free_occurrence(
        display_vector, pair_partition(1, display_alphabet)
    )
    return totals, failures, reference, first_sharp


def audit_minimal_numerical_profiles():
    profiles = tuple(
        (k, q)
        for k in range(3, 16, 2)
        for q in range(1, 16, 2)
        if (k, q) != (3, 1)
    )
    minimal = []
    for candidate in profiles:
        if not any(
            other != candidate
            and other[0] <= candidate[0]
            and other[1] <= candidate[1]
            for other in profiles
        ):
            minimal.append(candidate)
    assert tuple(minimal) == ((3, 3), (5, 1))
    return tuple(minimal)


def graph_spaces(vertex_count, host_mask):
    host_edges = tuple(combinations(range(vertex_count), 2))
    edges = tuple(edge for bit, edge in enumerate(host_edges) if (host_mask >> bit) & 1)
    edge_count = len(edges)

    cuts = set()
    for shore in range(1 << vertex_count):
        vector = 0
        for bit, (u, v) in enumerate(edges):
            if ((shore >> u) & 1) ^ ((shore >> v) & 1):
                vector |= 1 << bit
        cuts.add(vector)

    cycles = set()
    for vector in range(1 << edge_count):
        parity = [0] * vertex_count
        for bit, (u, v) in enumerate(edges):
            if (vector >> bit) & 1:
                parity[u] ^= 1
                parity[v] ^= 1
        if not any(parity):
            cycles.add(vector)
    return edge_count, frozenset(cuts), frozenset(cycles)


def audit_cycle_cut_duality():
    graph_count = functional_count = 0
    for vertex_count in range(1, 6):
        complete_edge_count = vertex_count * (vertex_count - 1) // 2
        for host_mask in range(1 << complete_edge_count):
            edge_count, cuts, cycles = graph_spaces(vertex_count, host_mask)
            graph_count += 1
            assert len(cuts) * len(cycles) == (1 << edge_count)
            assert all(
                ((cut & cycle).bit_count() & 1) == 0
                for cut in cuts
                for cycle in cycles
            )
            # Literal single-functional equivalence used in Theorem 3.1.
            for shore_vector in range(1 << edge_count):
                nonzero_on_cycles = any(
                    (shore_vector & cycle).bit_count() & 1 for cycle in cycles
                )
                assert nonzero_on_cycles == (shore_vector not in cuts)
                functional_count += 1
    return graph_count, functional_count


def audit_flow_cut_contradiction():
    cases = 0
    for b in range(1, 8):
        for t in range(1, 8):
            if t == b:
                continue
            for t_edge_parity in (0, 1):
                full_cut_xor = b ^ (t if t_edge_parity else 0)
                assert full_cut_xor != 0
                cases += 1
    assert cases == 84
    return cases


def audit_binary_coordination_obstruction():
    """Audit the F_2 consistency certificate behind displayed equation (22)."""
    systems = 0
    # Three equations: selected Q has RHS one; two protected shores RHS zero.
    for variable_count in range(0, 7):
        for rows in product(range(1 << variable_count), repeat=3):
            feasible = any(
                (rows[0] & assignment).bit_count() & 1
                and not ((rows[1] & assignment).bit_count() & 1)
                and not ((rows[2] & assignment).bit_count() & 1)
                for assignment in range(1 << variable_count)
            )
            dual_obstruction = any(
                (rows[0] ^ (rows[1] if take_one else 0) ^ (rows[2] if take_two else 0)) == 0
                for take_one, take_two in product((0, 1), repeat=2)
            )
            assert feasible == (not dual_obstruction)
            systems += 1
    return systems


def tight(profile):
    d, q = profile
    return d == 4 and (q & 1) == 1


def potential(profiles):
    return (
        sum(tight(profile) for profile in profiles),
        sum(d - q for d, q in profiles if q & 1),
    )


def valid_profile(d, q):
    if d < 0 or q < 0 or q > d or (d & 1):
        return False
    k = d - q
    # For a canonical odd component, the H-cut is odd and cannot have size 1.
    return not (q & 1) or k >= 3


def audit_theorem_4_arithmetic():
    cases = 0
    even_d = tuple(range(4, 15, 2))
    for d_q, old_q, new_q, d_c, old_c, new_c in product(
        even_d, range(15), range(15), even_d, range(15), range(15)
    ):
        old = ((d_q, old_q), (d_c, old_c))
        new = ((d_q, new_q), (d_c, new_c))
        if not all(valid_profile(*profile) for profile in old + new):
            continue
        if potential(old)[0] != 0:
            continue
        # Q is old odd and is removed from the odd sum.
        if not (old_q & 1) or (new_q & 1):
            continue
        # C implements conditions 2 and 3.
        if not (old_c & 1):
            if new_c & 1:
                continue
        elif new_c & 1 and new_c < old_c:
            continue
        assert potential(new)[0] == 0
        assert potential(new) < potential(old)
        cases += 1

    # Parity protection alone is insufficient: C remains odd but loses four
    # target edges, so its integer k-gain exceeds the summand removed at Q.
    parity_only_old = ((6, 3), (8, 5))
    parity_only_new = ((6, 2), (8, 1))
    assert potential(parity_only_old) == (0, 6)
    assert potential(parity_only_new) == (0, 7)

    # Without protection of an old even component, it may become a new tight
    # component and make the first coordinate worse.
    unprotected_old = ((6, 3), (4, 2))
    unprotected_new = ((6, 2), (4, 1))
    assert potential(unprotected_old) == (0, 3)
    assert potential(unprotected_new) == (1, 3)
    return cases, parity_only_old, parity_only_new, unprotected_old, unprotected_new


def main():
    totals, failures, per_target, _first_sharp = audit_profiles()
    minimal = audit_minimal_numerical_profiles()
    graph_count, functional_count = audit_cycle_cut_duality()
    cut_xors = audit_flow_cut_contradiction()
    coordination = audit_binary_coordination_obstruction()
    arithmetic = audit_theorem_4_arithmetic()

    print(f"minimal non-tight numerical profiles: {minimal}")
    for size in (3, 5, 7, 9):
        _size, per_admissible, per_failure = next(
            row for row in per_target if row[0] == size
        )
        print(
            f"k={size}: per-target=({per_admissible},{per_failure}) "
            f"all-targets=({totals[size]},{failures[size]})"
        )
    print("k=9 sharp witness b=1: 2,2,3,4,4,5,6,6,7")
    print(
        f"cycle/cut graphs={graph_count} functionals={functional_count} "
        f"nonzero-flow-cut-cases={cut_xors}"
    )
    print(f"binary coordination systems={coordination}")
    print(f"Theorem 4.1 two-component arithmetic cases={arithmetic[0]}")
    print("parity-only counterprofile: old=(6,3)|(8,5) new=(6,2)|(8,1)")
    print("unprotected-even counterprofile: old=(6,3)|(4,2) new=(6,2)|(4,1)")
    print("NO COUNTEREXAMPLE TO THE STATED CONDITIONAL RESULTS")


if __name__ == "__main__":
    main()
