#!/usr/bin/env python3
"""Exact finite checks for the support-16 loop/higher-occurrence lemmas.

This program deliberately separates:

* local marked-word statements, which need no abstract graph realization;
* the four finite interaction profiles left by the human shape reduction
  for two-occurrence components with loops through support 16; and
* the boundary effect of every forced two-terminal Kempe path.

All arithmetic is in K = F_2^2, represented by xor on {0,1,2,3}.
"""

from __future__ import annotations

import hashlib
import itertools
from collections import Counter
from dataclasses import dataclass


NONZERO = (1, 2, 3)
GL = tuple((0,) + row for row in itertools.permutations(NONZERO))
AFFINE = tuple(
    (linear, shift, tuple(linear[value] ^ shift for value in range(4)))
    for linear in GL
    for shift in range(4)
)


def derivative(word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(word[index - 1] ^ word[index] for index in range(len(word)))


def proper_dirty(word: tuple[int, ...]) -> bool:
    return (
        len(set(word)) == 4
        and all(word[index - 1] != word[index] for index in range(len(word)))
    )


def translate_interval(
    word: tuple[int, ...], first: int, second: int, delta: int
) -> tuple[int, ...]:
    assert first < second
    changed = list(word)
    for index in range(first, second):
        changed[index] ^= delta
    return tuple(changed)


def marked_image(
    word: tuple[int, ...],
    marks: tuple[int, ...],
    reverse: bool,
    anchor: int,
    linear: tuple[int, ...],
    affine: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Apply an affine colour map and a dihedral circuit action.

    Marks index derivatives d_i = c_{i-1}+c_i, rather than edge colours.
    Under reversal c'_k=c_{anchor-k}, derivative index p goes to
    k=anchor+1-p.  This one-index offset is asserted below.
    """

    length = len(word)
    sign = -1 if reverse else 1
    image = tuple(
        affine[word[(anchor + sign * index) % length]]
        for index in range(length)
    )
    if reverse:
        image_marks = tuple(
            sorted((anchor + 1 - position) % length for position in marks)
        )
    else:
        image_marks = tuple(
            sorted((position - anchor) % length for position in marks)
        )
    assert sorted(derivative(image)[position] for position in image_marks) == (
        sorted(linear[derivative(word)[position]] for position in marks)
    )
    return image, image_marks


def canonical_marked(
    word: tuple[int, ...], marks: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return min(
        marked_image(word, marks, reverse, anchor, linear, affine)
        for reverse in (False, True)
        for anchor in range(len(word))
        for linear, _shift, affine in AFFINE
    )


EXPECTED_LOOP_FAILURES = (
    ("010123", (1, 2)),
    ("010123", (1, 3)),
    ("010123", (2, 5)),
    ("010213", (1, 2)),
    ("010232", (1, 5)),
    ("012013", (0, 2)),
    ("012013", (1, 4)),
)
EXPECTED_TRIPLE_FAILURES = (
    ("010213", (0, 1, 3)),
    ("010213", (1, 4, 5)),
)


def local_marked_census() -> tuple[str, ...]:
    """Prove the length-five lemmas and classify first length-six failures."""

    report = []
    expected_dirty_orbits = {
        4: (("0123", 24),),
        5: (("01023", 120),),
    }
    for length in (4, 5):
        orbit_count: Counter[tuple[int, ...]] = Counter()
        for word in itertools.product(range(4), repeat=length):
            if proper_dirty(word):
                unmarked = min(
                    image
                    for reverse in (False, True)
                    for anchor in range(length)
                    for _linear, _shift, affine in AFFINE
                    for image, _marks in (
                        marked_image(
                            word, (), reverse, anchor, _linear, affine
                        ),
                    )
                )
                orbit_count[unmarked] += 1
        literal = tuple(
            ("".join(map(str, word)), count)
            for word, count in sorted(orbit_count.items())
        )
        assert literal == expected_dirty_orbits[length]

    loop_failures: Counter[
        tuple[tuple[int, ...], tuple[int, ...]]
    ] = Counter()
    triple_failures: Counter[
        tuple[tuple[int, ...], tuple[int, ...]]
    ] = Counter()
    tested = Counter()

    for length in (4, 5, 6):
        for word in itertools.product(range(4), repeat=length):
            if not proper_dirty(word):
                continue
            differences = derivative(word)
            for marks in itertools.combinations(range(length), 2):
                if differences[marks[0]] != differences[marks[1]]:
                    continue
                tested[("loop", length)] += 1
                value = differences[marks[0]]
                deletes = any(
                    len(
                        set(
                            translate_interval(
                                word, marks[0], marks[1], delta
                            )
                        )
                    )
                    < 4
                    for delta in NONZERO
                    if delta != value
                )
                if not deletes:
                    loop_failures[canonical_marked(word, marks)] += 1

            for marks in itertools.combinations(range(length), 3):
                if {differences[position] for position in marks} != set(
                    NONZERO
                ):
                    continue
                tested[("triple", length)] += 1
                deletes = any(
                    len(
                        set(
                            translate_interval(
                                word,
                                first,
                                second,
                                differences[first] ^ differences[second],
                            )
                        )
                    )
                    < 4
                    for first, second in itertools.combinations(marks, 2)
                )
                if not deletes:
                    triple_failures[canonical_marked(word, marks)] += 1

    assert tested == {
        ("loop", 4): 48,
        ("loop", 5): 360,
        ("triple", 5): 360,
        ("loop", 6): 2304,
        ("triple", 6): 2112,
    }, tested
    assert not any(
        len(key[0]) <= 5
        for failures in (loop_failures, triple_failures)
        for key in failures
    )

    loop_literal = tuple(
        ("".join(map(str, word)), marks)
        for (word, marks) in sorted(loop_failures)
    )
    triple_literal = tuple(
        ("".join(map(str, word)), marks)
        for (word, marks) in sorted(triple_failures)
    )
    assert loop_literal == EXPECTED_LOOP_FAILURES
    assert triple_literal == EXPECTED_TRIPLE_FAILURES
    assert sum(loop_failures.values()) == 1080
    assert sum(triple_failures.values()) == 576

    report.append(
        "LOCAL"
        " loop_tested_4/5/6=48/360/2304"
        " loop_fail_orbits_4/5/6=0/0/7"
        " triple_tested_4/5/6=0/360/2112"
        " triple_fail_orbits_4/5/6=0/0/2"
    )
    return tuple(report)


def forced_two_terminal_redundancy() -> str:
    """Check the exact boundary action of every two-terminal path.

    If the x,y-subgraph has exactly two boundary terminals, their value
    multiset is either {x,y} or {x,x} (up to exchanging x,y).  Switching
    the path agrees at every boundary occurrence with the global linear
    transposition x<->y, because no other occurrence has derivative x or y.
    """

    rows = 0
    for length in range(2, 17):
        for count_one in range(length + 1):
            for count_two in range(length - count_one + 1):
                count_three = length - count_one - count_two
                values = (
                    (1,) * count_one
                    + (2,) * count_two
                    + (3,) * count_three
                )
                if _xor(values):
                    continue
                for first, second in itertools.combinations(NONZERO, 2):
                    terminals = tuple(
                        index
                        for index, value in enumerate(values)
                        if value in (first, second)
                    )
                    if len(terminals) != 2:
                        continue
                    delta = first ^ second
                    switched = tuple(
                        value ^ delta if index in terminals else value
                        for index, value in enumerate(values)
                    )
                    transposed = tuple(
                        second
                        if value == first
                        else first
                        if value == second
                        else value
                        for value in values
                    )
                    assert switched == transposed
                    rows += 1
    assert rows == 69
    return f"FORCED_TWO_TERMINAL rows={rows} boundary_action=GL_transposition"


def _xor(values) -> int:
    answer = 0
    for value in values:
        answer ^= value
    return answer


def perfect_matchings(items: tuple[int, ...]):
    if not items:
        yield ()
        return
    first = items[0]
    for offset in range(1, len(items)):
        second = items[offset]
        rest = items[1:offset] + items[offset + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def paired_port_census() -> str:
    """Check the local two-vertex-bundle lemma used in the shape proof.

    A port occurs once and is shared with the other interaction vertex.
    A loop symbol occurs twice.  The only global condition on the port
    values in a two-vertex bundle is that their xor is zero.
    """

    expected = {
        (5, 3): 10,
        (5, 5): 1,
        (7, 3): 105,
        (7, 5): 21,
        (7, 7): 1,
    }
    checked = 0
    assignments = 0
    for (length, port_count), expected_patterns in expected.items():
        patterns = 0
        for port_positions in itertools.combinations(
            range(length), port_count
        ):
            port_set = set(port_positions)
            remaining = tuple(
                position
                for position in range(length)
                if position not in port_set
            )
            for pairs in perfect_matchings(remaining):
                owner = [-1] * length
                for port, position in enumerate(port_positions):
                    owner[position] = port
                for loop, pair in enumerate(pairs, start=port_count):
                    for position in pair:
                        owner[position] = loop
                patterns += 1
                checked += 1
                found = False
                symbols = port_count + len(pairs)
                for values in itertools.product(NONZERO, repeat=symbols):
                    if _xor(values[:port_count]):
                        continue
                    assignments += 1
                    point = 0
                    used = 0
                    for symbol in owner:
                        used |= 1 << point
                        point ^= values[symbol]
                    assert point == 0
                    if used != 15:
                        found = True
                        break
                assert found, (length, port_count, tuple(owner))
        assert patterns == expected_patterns
    assert checked == 138
    assert assignments == 406
    return (
        "PAIRED_PORT"
        " patterns_5:3/5=10/1"
        " patterns_7:3/5/7=105/21/1"
        f" assignments_until_witness={assignments} residual=0"
    )


HARD_WORD = tuple(map(int, "0101012301012302"))
HARD_LENGTHS = (8, 8)
HARD_OFFSETS = (0, 8)
HARD_TRIPLE_RESIDUALS = (
    "0001234003144422",
    "0012344041300022",
    "0012344403144422",
    "0123444441300022",
)


def hard_derivative() -> tuple[int, ...]:
    answer = []
    for offset, length in zip(HARD_OFFSETS, HARD_LENGTHS):
        answer.extend(
            HARD_WORD[offset + (local - 1) % length]
            ^ HARD_WORD[offset + local]
            for local in range(length)
        )
    return tuple(answer)


HARD_DERIVATIVE = hard_derivative()


def hard_integrate(values: tuple[int, ...]):
    base = [0] * 16
    used = []
    for offset, length in zip(HARD_OFFSETS, HARD_LENGTHS):
        point = 0
        colours = set()
        for local in range(length):
            position = offset + local
            point ^= values[position]
            base[position] = point
            colours.add(point)
        if point:
            return None
        used.append(frozenset(colours))
    return tuple(base), tuple(used)


def hard_clean(base: tuple[int, ...], owner: tuple[int, ...]) -> bool:
    blocks = max(owner) + 1
    for relative_shift in range(4):
        parity = [[0] * 4 for _ in range(blocks)]
        for circuit, (offset, length) in enumerate(
            zip(HARD_OFFSETS, HARD_LENGTHS)
        ):
            shift = relative_shift if circuit else 0
            for local in range(length):
                edge = offset + local
                successor = offset + (local + 1) % length
                first = owner[edge]
                second = owner[successor]
                if first == second:
                    continue
                colour = base[edge] ^ shift
                parity[first][colour] ^= 1
                parity[second][colour] ^= 1
        if not any(value for row in parity for value in row):
            return True
    return False


def hard_triple_residual_audit() -> str:
    """Recheck the four hard residual states containing six 3-blocks."""

    assert HARD_DERIVATIVE == tuple(map(int, "3111113121113132"))
    triple_blocks = 0
    state_digest = hashlib.sha256()
    for partition in HARD_TRIPLE_RESIDUALS:
        owner = tuple(map(int, partition))
        blocks = max(owner) + 1
        assert blocks == 5
        for block in range(blocks):
            positions = tuple(
                position
                for position, owner_block in enumerate(owner)
                if owner_block == block
            )
            assert _xor(HARD_DERIVATIVE[position] for position in positions) == 0
            if len(positions) != 3:
                continue
            triple_blocks += 1
            assert {
                HARD_DERIVATIVE[position] for position in positions
            } == set(NONZERO)
            first_circuit = tuple(
                position for position in positions if position < 8
            )
            second_circuit = tuple(
                position for position in positions if position >= 8
            )
            same_circuit_pair = (
                first_circuit if len(first_circuit) == 2 else second_circuit
            )
            assert len(same_circuit_pair) == 2
            first, second = same_circuit_pair
            delta = HARD_DERIVATIVE[first] ^ HARD_DERIVATIVE[second]
            switched = {
                position: (
                    HARD_DERIVATIVE[position] ^ delta
                    if position in same_circuit_pair
                    else HARD_DERIVATIVE[position]
                )
                for position in positions
            }
            matching_maps = tuple(
                linear
                for linear in GL
                if all(
                    linear[HARD_DERIVATIVE[position]]
                    == switched[position]
                    for position in positions
                )
            )
            assert len(matching_maps) == 1

        feasible = clean = deletes = 0
        for tail in itertools.product(range(6), repeat=blocks - 1):
            maps = (GL.index((0, 1, 2, 3)),) + tail
            values = tuple(
                GL[maps[owner[position]]][HARD_DERIVATIVE[position]]
                for position in range(16)
            )
            integrated = hard_integrate(values)
            if integrated is None:
                continue
            feasible += 1
            base, used = integrated
            clean += hard_clean(base, owner)
            deletes += any(len(colours) < 4 for colours in used)
        assert (feasible, clean, deletes) == (320, 0, 0)
        state_digest.update(
            f"{partition}|{feasible}|{clean}|{deletes}\n".encode("ascii")
        )
    assert triple_blocks == 6
    digest = state_digest.hexdigest()
    assert digest == (
        "2d30c29b876cb4108f555280417be3ac"
        "a6bf9043a759671ca3eee261031136d8"
    )
    return (
        "HARD_TRIPLES states=4 triple_blocks=6"
        " feasible_each=320 clean=0 delete=0"
        f" sha256={digest}"
    )


def cyclic_orders(tokens: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """All cyclic token orders modulo rotation and reversal."""

    images = set(itertools.permutations(tokens))
    canonical = set()
    length = len(tokens)
    for row in images:
        orbit = []
        for offset in range(length):
            orbit.append(row[offset:] + row[:offset])
            reverse = tuple(reversed(row))
            orbit.append(reverse[offset:] + reverse[:offset])
        canonical.add(min(orbit))
    return tuple(sorted(canonical))


@dataclass(frozen=True)
class Profile:
    name: str
    lengths: tuple[int, int, int]
    multiplicities: tuple[int, int, int]  # 01, 02, 12
    loops_at_two: int
    expected_orders: tuple[int, int, int]
    expected_states: int
    expected_feasible_flows: int


PROFILES = (
    Profile(
        "457-a",
        (4, 5, 7),
        (2, 2, 3),
        1,
        (3, 12, 180),
        6_480,
        138,
    ),
    Profile(
        "457-b",
        (4, 5, 7),
        (3, 1, 2),
        2,
        (3, 12, 90),
        3_240,
        126,
    ),
    Profile(
        "556-a",
        (5, 5, 6),
        (3, 2, 2),
        1,
        (12, 12, 30),
        4_320,
        138,
    ),
    Profile(
        "556-b",
        (5, 5, 6),
        (4, 1, 1),
        2,
        (12, 12, 16),
        2_304,
        180,
    ),
)


def build_profile(profile: Profile):
    edge_ends = []
    for ends, multiplicity in zip(
        ((0, 1), (0, 2), (1, 2)), profile.multiplicities
    ):
        edge_ends.extend([ends] * multiplicity)
    for _ in range(profile.loops_at_two):
        edge_ends.append((2, 2))
    appearances = [[] for _ in range(3)]
    for edge, (first, second) in enumerate(edge_ends):
        appearances[first].append(edge)
        appearances[second].append(edge)
    assert tuple(map(len, appearances)) == profile.lengths
    orders = tuple(cyclic_orders(tuple(row)) for row in appearances)
    assert tuple(map(len, orders)) == profile.expected_orders
    return tuple(edge_ends), orders


def feasible_flows(edge_ends: tuple[tuple[int, int], ...]):
    """Enumerate normalized nowhere-zero interaction flows."""

    answer = []
    for tail in itertools.product(NONZERO, repeat=len(edge_ends) - 1):
        values = (1,) + tail
        charges = [0, 0, 0]
        for value, (first, second) in zip(values, edge_ends):
            charges[first] ^= value
            charges[second] ^= value
        if charges == [0, 0, 0]:
            answer.append(values)
    return tuple(answer)


def evaluate_interaction_state(
    orders: tuple[tuple[int, ...], ...],
    flows: tuple[tuple[int, ...], ...],
) -> tuple[bool, bool]:
    """Return (clean_seen, deletion_seen) over every feasible flow."""

    deletion_seen = False
    for values in flows:
        origins = []
        traversed = []
        deletes = False
        for order in orders:
            point = 0
            used = 0
            local_origins = []
            local_edges = []
            for edge in order:
                used |= 1 << point
                local_origins.append(point)
                successor = point ^ values[edge]
                local_edges.append(frozenset((point, successor)))
                point = successor
            assert point == 0
            deletes = deletes or used != 15
            origins.append(tuple(local_origins))
            traversed.append(tuple(local_edges))
        if deletes:
            deletion_seen = True
            return False, True

        for shifts in itertools.product(range(4), repeat=2):
            translations = (0,) + shifts
            seen = {}
            clean = True
            for vertex, order in enumerate(orders):
                shift = translations[vertex]
                for local, edge in enumerate(order):
                    literal = frozenset(
                        point ^ shift for point in traversed[vertex][local]
                    )
                    if edge in seen and seen[edge] != literal:
                        clean = False
                        break
                    seen[edge] = literal
                if not clean:
                    break
            if clean:
                return True, deletion_seen
    return False, deletion_seen


def finite_loop_profiles() -> tuple[str, ...]:
    report = []
    stream = hashlib.sha256()
    for profile in PROFILES:
        edge_ends, order_sets = build_profile(profile)
        flows = feasible_flows(edge_ends)
        assert len(flows) == profile.expected_feasible_flows
        states = selected_clean = selected_delete = residual = 0
        for orders in itertools.product(*order_sets):
            states += 1
            clean_seen, deletion_seen = evaluate_interaction_state(
                orders, flows
            )
            if clean_seen:
                category = "C"
                selected_clean += 1
            elif deletion_seen:
                category = "D"
                selected_delete += 1
            else:
                category = "R"
                residual += 1
            encoded = (
                profile.name
                + "|"
                + "|".join(",".join(map(str, row)) for row in orders)
                + "|"
                + category
                + "\n"
            )
            stream.update(encoded.encode("ascii"))
        assert states == profile.expected_states
        assert residual == 0
        report.append(
            f"PROFILE {profile.name} states={states}"
            f" flows={len(flows)} selected_clean={selected_clean}"
            f" selected_delete={selected_delete} residual={residual}"
        )
    digest = stream.hexdigest()
    assert digest == (
        "8168cff38b861ac162ada05f89bb9f69"
        "86d9fe12d1ae3eb9b1bbb02682826228"
    )
    report.append(f"PROFILE_SHA256 {digest}")
    return tuple(report)


def main() -> None:
    lines = []
    lines.extend(local_marked_census())
    lines.append(forced_two_terminal_redundancy())
    lines.append(paired_port_census())
    lines.append(hard_triple_residual_audit())
    lines.extend(finite_loop_profiles())
    for line in lines:
        print(line)
    print("PASS support-16 loop/higher-occurrence exact verifier")


if __name__ == "__main__":
    main()
