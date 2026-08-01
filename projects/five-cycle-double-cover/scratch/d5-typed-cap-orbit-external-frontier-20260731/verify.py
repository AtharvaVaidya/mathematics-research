#!/usr/bin/env python3
"""Exact D5 typed-cap Kempe-orbit census through order twelve.

The program uses only the Python standard library and nauty's ``geng``.
It independently enumerates D5 flows modulo global S5, reconstructs every
component-Kempe orbit, and computes the six-state typed signature of every
proper cap/root interface inside each orbit.
"""

from __future__ import annotations

from collections import Counter, deque
import itertools
import os
import subprocess


LABELS = tuple(
    (1 << first) | (1 << second)
    for first, second in itertools.combinations(range(5), 2)
)
LABEL_SET = frozenset(LABELS)
PERMUTATIONS = tuple(itertools.permutations(range(5)))
WAGNER_GRAPH6 = "GCrb`o"
WAGNER_INITIAL = (3, 5, 6, 6, 3, 5, 5, 3, 6, 6, 5, 3)
ORDER12_GRAPH6 = "K?`@EQgLAcAo"
ORDER12_ORBIT_INITIAL = tuple(bytes.fromhex("030c05051411061412110514180c14091811"))
ORDER12_ALL_FLOW_WITNESS = tuple(bytes.fromhex("030505050306060305060a0c061214180911"))
ORDER14_GRAPH6 = "M??CBAPqB_B_H_B_?"
ORDER14_ORBIT_INITIAL = tuple(bytes.fromhex("03050c1118091203110614120a121818120a030a09"))
ORDER14_ALL_FLOW_WITNESS = tuple(bytes.fromhex("030305050306060503060305060a0c061412091811"))


def permute_label(label: int, permutation: tuple[int, ...]) -> int:
    return sum(
        1 << permutation[coordinate]
        for coordinate in range(5)
        if (label >> coordinate) & 1
    )


PERMUTED = tuple(
    {label: permute_label(label, permutation) for label in LABELS}
    for permutation in PERMUTATIONS
)


def canonical(state: tuple[int, ...]) -> tuple[int, ...]:
    return min(tuple(table[label] for label in state) for table in PERMUTED)


def decode_graph6(row: str) -> tuple[int, tuple[tuple[int, int], ...], tuple[tuple[int, ...], ...]]:
    assert row and row[0] != "~"
    n = ord(row[0]) - 63
    assert 0 <= n <= 62
    bits: list[int] = []
    for char in row[1:]:
        value = ord(char) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    incidence: list[list[int]] = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    assert len(edges) == len(set(edges)) == 3 * n // 2
    assert all(left != right for left, right in edges)
    assert all(len(local) == 3 for local in incidence)
    return n, tuple(edges), tuple(tuple(local) for local in incidence)


def connected_after_omitting(
    n: int,
    edges: tuple[tuple[int, int], ...],
    omitted: int | None,
) -> bool:
    adjacency = [[] for _ in range(n)]
    for left, right in edges:
        if omitted not in (left, right):
            adjacency[left].append(right)
            adjacency[right].append(left)
    start = next(vertex for vertex in range(n) if vertex != omitted)
    seen, todo = {start}, [start]
    while todo:
        for other in adjacency[todo.pop()]:
            if other not in seen:
                seen.add(other)
                todo.append(other)
    return len(seen) == n - int(omitted is not None)


def validate_biconnected(n: int, edges: tuple[tuple[int, int], ...]) -> None:
    assert connected_after_omitting(n, edges, None)
    assert all(connected_after_omitting(n, edges, vertex) for vertex in range(n))


def connected_with_skipped_edges(
    n: int,
    edges: tuple[tuple[int, int], ...],
    skipped: frozenset[int],
) -> bool:
    adjacency = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        if edge not in skipped:
            adjacency[left].append(right)
            adjacency[right].append(left)
    seen, todo = {0}, [0]
    while todo:
        for other in adjacency[todo.pop()]:
            if other not in seen:
                seen.add(other)
                todo.append(other)
    return len(seen) == n


def edge_connectivity_at_least_three(
    n: int, edges: tuple[tuple[int, int], ...]
) -> bool:
    return (
        all(connected_with_skipped_edges(n, edges, frozenset({edge}))
            for edge in range(len(edges)))
        and all(connected_with_skipped_edges(n, edges, frozenset({first, second}))
                for first in range(len(edges))
                for second in range(first + 1, len(edges)))
    )


def graph_girth(n: int, edges: tuple[tuple[int, int], ...]) -> int:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    best = n + 1
    for source in range(n):
        distance, parent_edge = [-1] * n, [-1] * n
        distance[source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for other, edge in adjacency[vertex]:
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent_edge[other] = edge
                    queue.append(other)
                elif parent_edge[vertex] != edge:
                    best = min(best, distance[vertex] + distance[other] + 1)
    return best


def tait_colouring_exists(
    edges: tuple[tuple[int, int], ...], incidence: tuple[tuple[int, ...], ...]
) -> bool:
    colours = [-1] * len(edges)

    def visit() -> bool:
        uncoloured = [edge for edge, colour in enumerate(colours) if colour < 0]
        if not uncoloured:
            return True
        edge = max(
            uncoloured,
            key=lambda item: sum(
                colours[other] >= 0
                for vertex in edges[item]
                for other in incidence[vertex]
                if other != item
            ),
        )
        used = {
            colours[other]
            for vertex in edges[edge]
            for other in incidence[vertex]
            if colours[other] >= 0
        }
        for colour in range(3):
            if colour not in used:
                colours[edge] = colour
                if visit():
                    return True
                colours[edge] = -1
        return False

    return visit()


def cyclic_edge_connectivity(n: int, edges: tuple[tuple[int, int], ...]) -> int:
    def has_cycle(vertices: frozenset[int]) -> bool:
        parent = {vertex: vertex for vertex in vertices}

        def root(vertex: int) -> int:
            while parent[vertex] != vertex:
                parent[vertex] = parent[parent[vertex]]
                vertex = parent[vertex]
            return vertex

        for left, right in edges:
            if left in vertices and right in vertices:
                first, second = root(left), root(right)
                if first == second:
                    return True
                parent[first] = second
        return False

    universe = frozenset(range(n))
    best = len(edges) + 1
    # Keep vertex zero on the complementary shore to avoid testing both
    # orientations of one cut.
    for mask in range(1, 1 << (n - 1)):
        shore = frozenset(vertex + 1 for vertex in range(n - 1) if (mask >> vertex) & 1)
        other = universe - shore
        if has_cycle(shore) and has_cycle(other):
            cut = sum((left in shore) ^ (right in shore) for left, right in edges)
            best = min(best, cut)
    return best


def enumerate_flows(
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
) -> set[tuple[int, ...]]:
    state = [0] * len(edges)
    answers: set[tuple[int, ...]] = set()

    def assign(edge: int, label: int, trail: list[int]) -> bool:
        if state[edge]:
            return state[edge] == label
        if label not in LABEL_SET:
            return False
        state[edge] = label
        trail.append(edge)
        queue = list(edges[edge])
        while queue:
            vertex = queue.pop()
            local = incidence[vertex]
            assigned = [item for item in local if state[item]]
            if len(assigned) < 2:
                continue
            if len(assigned) == 3:
                if state[local[0]] ^ state[local[1]] ^ state[local[2]]:
                    return False
                continue
            missing = next(item for item in local if not state[item])
            forced = state[assigned[0]] ^ state[assigned[1]]
            if forced not in LABEL_SET:
                return False
            state[missing] = forced
            trail.append(missing)
            queue.extend(edges[missing])
        return True

    def visit() -> None:
        try:
            edge = next(index for index, label in enumerate(state) if not label)
        except StopIteration:
            answers.add(canonical(tuple(state)))
            return
        choices = (3,) if not any(state) else LABELS
        for label in choices:
            trail: list[int] = []
            if assign(edge, label, trail):
                visit()
            for changed in reversed(trail):
                state[changed] = 0

    visit()
    return answers


def components(
    state: tuple[int, ...],
    pair: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
) -> tuple[frozenset[int], ...]:
    unseen = {
        edge
        for edge, label in enumerate(state)
        if (label & pair).bit_count() == 1
    }
    answer: list[frozenset[int]] = []
    while unseen:
        start = unseen.pop()
        component, todo = {start}, [start]
        while todo:
            edge = todo.pop()
            for vertex in edges[edge]:
                for other in incidence[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        component.add(other)
                        todo.append(other)
        answer.append(frozenset(component))
    return tuple(answer)


def transpose_label(label: int, pair: int) -> int:
    first, second = (coordinate for coordinate in range(5) if (pair >> coordinate) & 1)
    if ((label >> first) & 1) == ((label >> second) & 1):
        return label
    return label ^ pair


def neighbours(
    state: tuple[int, ...],
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
):
    for pair in LABELS:
        for component in components(state, pair, edges, incidence):
            yield canonical(tuple(
                transpose_label(label, pair) if edge in component else label
                for edge, label in enumerate(state)
            ))


def kempe_orbit(
    initial: tuple[int, ...],
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
) -> set[tuple[int, ...]]:
    orbit, queue = {canonical(initial)}, deque([canonical(initial)])
    while queue:
        state = queue.popleft()
        for other in neighbours(state, edges, incidence):
            if other not in orbit:
                orbit.add(other)
                queue.append(other)
    return orbit


def orbit_typed_data(
    orbit: set[tuple[int, ...]],
    n: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
) -> tuple[dict[tuple[int, int], int], dict[tuple[int, int], bool]]:
    masks = {
        (cap, root): 0
        for cap in range(n)
        for root, endpoints in enumerate(edges)
        if cap not in endpoints
    }
    simultaneous = {key: False for key in masks}
    physical_index = {(0, 1): 0, (0, 2): 1, (1, 2): 2}
    for state in orbit:
        current_external: dict[tuple[int, int], int] = {}
        for pair in LABELS:
            for component in components(state, pair, edges, incidence):
                for cap in range(n):
                    slots = tuple(
                        slot
                        for slot, edge in enumerate(incidence[cap])
                        if edge in component
                    )
                    if len(slots) != 2:
                        continue
                    physical = physical_index[slots]
                    inactive_slot = next(slot for slot in range(3) if slot not in slots)
                    inactive_label = state[incidence[cap][inactive_slot]]
                    assert pair == inactive_label or pair & inactive_label == 0
                    mode = int(pair != inactive_label)
                    bit = 1 << (2 * physical + mode)
                    for root in component:
                        if cap not in edges[root]:
                            masks[cap, root] |= bit
                            if mode:
                                key = (cap, root)
                                current_external[key] = (
                                    current_external.get(key, 0) | (1 << physical)
                                )
        for key, external_mask in current_external.items():
            if external_mask.bit_count() >= 2:
                simultaneous[key] = True
    return masks, simultaneous


def orbit_typed_masks(
    orbit: set[tuple[int, ...]],
    n: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
) -> dict[tuple[int, int], int]:
    return orbit_typed_data(orbit, n, edges, incidence)[0]


def contains_double_star(mask: int) -> bool:
    full = ((mask & 3) == 3, (mask & 12) == 12, (mask & 48) == 48)
    return sum(full) >= 2


def externally_covers_all_ports(mask: int) -> bool:
    # The external states are bits 1,3,5.  Any two edges of the physical
    # three-port triangle cover all three physical ports.
    return sum(bool(mask & (1 << bit)) for bit in (1, 3, 5)) >= 2


def validate_rectangle_projection() -> None:
    factors = (9, 17, 10, 18)  # 03,04,13,14 as five-bit masks.
    image = {
        tuple(int((label & pair).bit_count() == 1) for pair in factors)
        for label in LABELS
    }
    even_nonzero = {
        bits
        for bits in itertools.product((0, 1), repeat=4)
        if sum(bits) % 2 == 0 and any(bits)
    }
    assert image == even_nonzero and len(image) == 7
    assert all(
        sum(bits) % 2 == 0
        for label in LABELS
        for bits in [tuple(int((label & pair).bit_count() == 1) for pair in factors)]
    )
    # The normalized cap triangle 01,02,12 projects to 1111,1100,0011.
    projected = tuple(
        tuple(int((label & pair).bit_count() == 1) for pair in factors)
        for label in (3, 5, 6)
    )
    assert projected == ((1, 1, 1, 1), (1, 1, 0, 0), (0, 0, 1, 1))
    print("RECTANGLE labels=10 image_nonzero_even=7 cap=1111,1100,0011 PASS")


def rectangle(label: int) -> tuple[int, int, int, int]:
    factors = (9, 17, 10, 18)
    return tuple(int((label & pair).bit_count() == 1) for pair in factors)


def validate_projected_switch_algebra() -> None:
    # If T is the switched coordinate pair and x crosses T, transposition
    # sends x to x+T.  Linearity then gives pi(x')=pi(x)+pi(T), and every
    # factor support Q is toggled precisely when |Q cap T| is odd.
    checks = 0
    for label in LABELS:
        for switched_pair in LABELS:
            if (label & switched_pair).bit_count() != 1:
                continue
            changed = label ^ switched_pair
            assert changed in LABEL_SET
            assert tuple(a ^ b for a, b in zip(rectangle(label), rectangle(changed))) == rectangle(switched_pair)
            for factor in LABELS:
                before = (label & factor).bit_count() & 1
                after = (changed & factor).bit_count() & 1
                assert before ^ after == ((factor & switched_pair).bit_count() & 1)
                checks += 1
    print(f"SWITCH active_label_factor_checks={checks} projected_circuit_addition=PASS")


def validate_tait_support_local_algebra() -> None:
    # For an injection of four coordinate names into F_2^2, every coordinate
    # triangle maps by endpoint difference to the three nonzero colours.
    values = (0, 1, 2, 3)
    triangles = 0
    for chosen in itertools.combinations(values, 3):
        colours = {
            chosen[0] ^ chosen[1],
            chosen[0] ^ chosen[2],
            chosen[1] ^ chosen[2],
        }
        assert colours == {1, 2, 3}
        triangles += 1
    print(f"TAIT_SUPPORT local_four_coordinate_triangles={triangles} PASS")


def graph6_rows(order: int) -> list[str]:
    geng = os.environ.get("GENG", "/opt/homebrew/bin/geng")
    run = subprocess.run(
        [geng, "-Cq", "-d3", "-D3", str(order)],
        check=True,
        text=True,
        capture_output=True,
    )
    return [row for row in run.stdout.splitlines() if row and not row.startswith(">")]


def census_order(order: int) -> tuple[int, int, int, int, set[int]]:
    graph_count = flow_count = orbit_count = interface_count = 0
    double_star_failures = external_failures = orbit_simultaneous_failures = 0
    all_flow_simultaneous_failures = 0
    masks_seen: set[int] = set()
    for row in graph6_rows(order):
        n, edges, incidence = decode_graph6(row)
        assert n == order
        validate_biconnected(n, edges)
        all_flows = enumerate_flows(edges, incidence)
        flow_count += len(all_flows)
        unseen = set(all_flows)
        graph_simultaneous = {
            (cap, root): False
            for cap in range(n)
            for root, endpoints in enumerate(edges)
            if cap not in endpoints
        }
        while unseen:
            initial = next(iter(unseen))
            orbit = kempe_orbit(initial, edges, incidence)
            assert orbit <= all_flows
            unseen -= orbit
            orbit_count += 1
            masks, simultaneous = orbit_typed_data(orbit, n, edges, incidence)
            interface_count += len(masks)
            for key, mask in masks.items():
                masks_seen.add(mask)
                double_star_failures += not contains_double_star(mask)
                external_failures += not externally_covers_all_ports(mask)
                orbit_simultaneous_failures += not simultaneous[key]
                graph_simultaneous[key] |= simultaneous[key]
        all_flow_simultaneous_failures += sum(not value for value in graph_simultaneous.values())
        graph_count += 1
    print(
        f"ORDER n={order} graphs={graph_count} flows_mod_s5={flow_count} "
        f"kempe_orbits_mod_s5={orbit_count} orbit_interfaces={interface_count} "
        f"double_star_failures={double_star_failures} "
        f"orbit_union_failures={external_failures} "
        f"orbit_simultaneous_failures={orbit_simultaneous_failures} "
        f"all_flow_simultaneous_failures={all_flow_simultaneous_failures} "
        f"masks={','.join(map(str, sorted(masks_seen)))} PASS"
    )
    assert external_failures == all_flow_simultaneous_failures == 0
    return graph_count, flow_count, orbit_count, interface_count, masks_seen


def validate_wagner_counterexample() -> None:
    n, edges, incidence = decode_graph6(WAGNER_GRAPH6)
    validate_biconnected(n, edges)
    assert canonical(WAGNER_INITIAL) == WAGNER_INITIAL
    assert all(label in LABEL_SET for label in WAGNER_INITIAL)
    assert all(
        WAGNER_INITIAL[a] ^ WAGNER_INITIAL[b] ^ WAGNER_INITIAL[c] == 0
        for a, b, c in incidence
    )
    orbit = kempe_orbit(WAGNER_INITIAL, edges, incidence)
    masks = orbit_typed_masks(orbit, n, edges, incidence)
    assert len(orbit) == 13 and masks[0, 7] == 46
    assert not contains_double_star(46)
    assert externally_covers_all_ports(46)
    print(
        "WAGNER graph6=GCrb`o cap=0 root=7 orbit=13 "
        "typed_mask=46 double_star=0 external_ports=3 PASS"
    )


def fixed_typed_data(
    state: tuple[int, ...],
    cap: int,
    root: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
) -> tuple[int, int]:
    physical_index = {(0, 1): 0, (0, 2): 1, (1, 2): 2}
    typed = external = 0
    for pair in LABELS:
        for component in components(state, pair, edges, incidence):
            if root not in component:
                continue
            slots = tuple(
                slot for slot, edge in enumerate(incidence[cap]) if edge in component
            )
            if len(slots) != 2:
                continue
            inactive = next(slot for slot in range(3) if slot not in slots)
            inactive_label = state[incidence[cap][inactive]]
            assert pair == inactive_label or pair & inactive_label == 0
            mode = int(pair != inactive_label)
            physical = physical_index[slots]
            typed |= 1 << (2 * physical + mode)
            if mode:
                external |= 1 << physical
    return typed, external


def validate_orbit_delimiters() -> None:
    n, edges, incidence = decode_graph6(ORDER12_GRAPH6)
    assert n == 12 and canonical(ORDER12_ORBIT_INITIAL) == ORDER12_ORBIT_INITIAL
    all_flows = enumerate_flows(edges, incidence)
    orbit = kempe_orbit(ORDER12_ORBIT_INITIAL, edges, incidence)
    masks, simultaneous = orbit_typed_data(orbit, n, edges, incidence)
    distribution = Counter(
        fixed_typed_data(state, 0, 15, edges, incidence)[1] for state in orbit
    )
    assert len(all_flows) == 498 and len(orbit) == 144
    assert masks[0, 15] == 47 and not simultaneous[0, 15]
    assert distribution == Counter({0: 72, 1: 24, 2: 24, 4: 24})
    assert ORDER12_ALL_FLOW_WITNESS in all_flows
    assert fixed_typed_data(ORDER12_ALL_FLOW_WITNESS, 0, 15, edges, incidence) == (10, 3)
    assert graph_girth(n, edges) == 3
    assert not edge_connectivity_at_least_three(n, edges)
    assert cyclic_edge_connectivity(n, edges) == 2
    assert tait_colouring_exists(edges, incidence)
    print(
        "ORDER12_ORBIT graph6=K?`@EQgLAcAo cap=0 root=15 orbit=144 "
        "aggregate_typed=47 simultaneous=0 all_flow_witness_typed=10 external=3 PASS"
    )

    n, edges, incidence = decode_graph6(ORDER14_GRAPH6)
    assert n == 14 and canonical(ORDER14_ORBIT_INITIAL) == ORDER14_ORBIT_INITIAL
    all_flows = enumerate_flows(edges, incidence)
    orbit = kempe_orbit(ORDER14_ORBIT_INITIAL, edges, incidence)
    masks, simultaneous = orbit_typed_data(orbit, n, edges, incidence)
    distribution = Counter(
        fixed_typed_data(state, 7, 19, edges, incidence)[1] for state in orbit
    )
    assert len(all_flows) == 1423 and len(orbit) == 12
    assert masks[7, 19] == 23 and not simultaneous[7, 19]
    assert distribution == Counter({1: 10, 0: 2})
    assert not externally_covers_all_ports(masks[7, 19])
    assert ORDER14_ALL_FLOW_WITNESS in all_flows
    assert fixed_typed_data(ORDER14_ALL_FLOW_WITNESS, 7, 19, edges, incidence) == (42, 7)
    assert graph_girth(n, edges) == 4
    assert edge_connectivity_at_least_three(n, edges)
    assert cyclic_edge_connectivity(n, edges) == 4
    assert tait_colouring_exists(edges, incidence)
    print(
        "ORDER14_ORBIT graph6=M??CBAPqB_B_H_B_? cap=7 root=19 orbit=12 "
        "aggregate_typed=23 external_union=1 simultaneous=0 "
        "all_flow_witness_typed=42 external=7 PASS"
    )


def main() -> None:
    validate_rectangle_projection()
    validate_projected_switch_algebra()
    validate_tait_support_local_algebra()
    expected = {
        4: (1, 2, 2, 24),
        6: (2, 13, 12, 432),
        8: (5, 128, 35, 2520),
        10: (18, 1525, 323, 38760),
        12: (81, 25960, 2650, 477000),
    }
    for order, counts in expected.items():
        result = census_order(order)
        assert result[:4] == counts
    validate_wagner_counterexample()
    validate_orbit_delimiters()
    print("PASS")


if __name__ == "__main__":
    main()
