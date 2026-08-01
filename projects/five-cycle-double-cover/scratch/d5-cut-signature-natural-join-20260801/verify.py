#!/usr/bin/env python3
"""Independent finite replay of the rooted/cap cut-signature join laws.

The checker deliberately uses no SAT package and does not import another
project module.  It enumerates every D5 labelling of two literal small cubic
graphs, both directly and shore-by-shore across a 2- or 3-edge cut.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


D5 = tuple((1 << i) | (1 << j) for i, j in combinations(range(5), 2))
D5_SET = frozenset(D5)
PAIR_INDEX = {pair: index for index, pair in enumerate(D5)}
PHYSICAL_INDEX = {(0, 1): 0, (0, 2): 1, (1, 2): 2}


def graph6(word: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    n = ord(word[0]) - 63
    bits = []
    for character in word[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    assert len(edges) == 3 * n // 2
    return n, tuple(edges)


def incidence(n: int, items: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(n)]
    for item, endpoints in enumerate(items):
        for vertex in endpoints:
            rows[vertex].append(item)
    return tuple(tuple(row) for row in rows)


def enumerate_labellings(
    n: int,
    items: tuple[tuple[int, ...], ...],
    fixed: dict[int, int],
) -> tuple[tuple[int, ...], ...]:
    """Enumerate every D5 word satisfying xor zero at every cubic vertex."""

    rows = incidence(n, items)
    assert all(len(row) in (0, 3) for row in rows)
    state = [0] * len(items)
    answers: list[tuple[int, ...]] = []

    def assign(item: int, label: int, trail: list[int]) -> bool:
        if state[item]:
            return state[item] == label
        if label not in D5_SET or (item in fixed and fixed[item] != label):
            return False
        state[item] = label
        trail.append(item)
        queue = list(items[item])
        while queue:
            vertex = queue.pop()
            row = rows[vertex]
            assigned = [other for other in row if state[other]]
            if len(assigned) < 2:
                continue
            if len(assigned) == 3:
                if state[row[0]] ^ state[row[1]] ^ state[row[2]]:
                    return False
                continue
            missing = next(other for other in row if not state[other])
            forced = state[assigned[0]] ^ state[assigned[1]]
            if forced not in D5_SET or (missing in fixed and fixed[missing] != forced):
                return False
            state[missing] = forced
            trail.append(missing)
            queue.extend(items[missing])
        return True

    def visit() -> None:
        try:
            item = next(index for index, label in enumerate(state) if not label)
        except StopIteration:
            answers.append(tuple(state))
            return
        choices = (fixed[item],) if item in fixed else D5
        for label in choices:
            trail: list[int] = []
            if assign(item, label, trail):
                visit()
            for changed in reversed(trail):
                state[changed] = 0

    for item, label in sorted(fixed.items()):
        trail: list[int] = []
        if not assign(item, label, trail):
            return ()
    visit()
    assert len(answers) == len(set(answers))
    return tuple(answers)


@dataclass(frozen=True)
class Pole:
    vertices: frozenset[int]
    items: tuple[tuple[int, ...], ...]
    original_edges: tuple[int, ...]
    boundary_items: tuple[int, ...]


def cut_shores(
    n: int,
    edges: tuple[tuple[int, int], ...],
    cut: tuple[int, ...],
) -> tuple[frozenset[int], frozenset[int]]:
    adjacency = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        if edge not in cut:
            adjacency[left].append(right)
            adjacency[right].append(left)
    first = edges[cut[0]][0]
    seen, todo = {first}, [first]
    while todo:
        for other in adjacency[todo.pop()]:
            if other not in seen:
                seen.add(other)
                todo.append(other)
    other = set(range(n)) - seen
    assert seen and other
    assert all((left in seen) ^ (right in seen) for left, right in (edges[e] for e in cut))
    return frozenset(seen), frozenset(other)


def make_pole(
    edges: tuple[tuple[int, int], ...],
    shore: frozenset[int],
    cut: tuple[int, ...],
) -> Pole:
    items: list[tuple[int, ...]] = []
    original: list[int] = []
    for edge, endpoints in enumerate(edges):
        local = tuple(vertex for vertex in endpoints if vertex in shore)
        if len(local) == 2:
            items.append(local)
            original.append(edge)
        elif edge in cut:
            assert len(local) == 1
            items.append(local)
            original.append(edge)
        else:
            assert len(local) == 0
    boundary = tuple(original.index(edge) for edge in cut)
    assert len(boundary) == len(cut)
    return Pole(shore, tuple(items), tuple(original), boundary)


def active(label: int, factor: int) -> bool:
    return (label & factor).bit_count() == 1


def component(
    pole: Pole,
    labels: tuple[int, ...],
    factor: int,
    start: int,
) -> frozenset[int]:
    rows = incidence(max(pole.vertices) + 1, pole.items)
    active_items = {item for item, label in enumerate(labels) if active(label, factor)}
    assert start in active_items
    reached, todo = {start}, [start]
    while todo:
        item = todo.pop()
        for vertex in pole.items[item]:
            local = [other for other in rows[vertex] if other in active_items]
            assert len(local) == 2
            for other in local:
                if other not in reached:
                    reached.add(other)
                    todo.append(other)
    return frozenset(reached)


def root_state(pole: Pole, labels: tuple[int, ...], root_edge: int) -> int:
    root = pole.original_edges.index(root_edge)
    boundary = frozenset(pole.boundary_items)
    result = 0
    for factor in D5:
        active_boundary = frozenset(item for item in boundary if active(labels[item], factor))
        assert len(active_boundary) in (0, 2)
        if not active(labels[root], factor):
            continue
        found = component(pole, labels, factor, root)
        if found & boundary:
            assert found & boundary == active_boundary
            result |= 1 << PAIR_INDEX[factor]
    return result


def cap_state(
    pole: Pole,
    labels: tuple[int, ...],
    z: int,
    graph_rows: tuple[tuple[int, ...], ...],
) -> tuple[int, int, int]:
    graph_ports = graph_rows[z]
    assert all(edge not in (pole.original_edges[item] for item in pole.boundary_items)
               for edge in graph_ports)
    ports = tuple(pole.original_edges.index(edge) for edge in graph_ports)
    boundary = frozenset(pole.boundary_items)
    result = [0, 0, 0]
    for factor in D5:
        active_ports = tuple(slot for slot, item in enumerate(ports)
                             if active(labels[item], factor))
        assert len(active_ports) in (0, 2)
        if len(active_ports) == 0:
            continue
        found = component(pole, labels, factor, ports[active_ports[0]])
        active_boundary = frozenset(item for item in boundary if active(labels[item], factor))
        assert len(active_boundary) in (0, 2)
        if not (found & boundary):
            continue
        assert found & boundary == active_boundary
        inactive_slot = next(slot for slot in range(3) if slot not in active_ports)
        if labels[ports[inactive_slot]] & factor:
            assert labels[ports[inactive_slot]] == factor
            continue
        physical = PHYSICAL_INDEX[active_ports]
        result[physical] |= 1 << PAIR_INDEX[factor]
    return tuple(result)


def joined_external_mask(root: int, cap: tuple[int, int, int]) -> int:
    return sum(1 << physical for physical in range(3) if root & cap[physical])


def direct_external_mask(
    n: int,
    edges: tuple[tuple[int, int], ...],
    labels: tuple[int, ...],
    z: int,
    root: int,
) -> int:
    rows = incidence(n, tuple(tuple(edge) for edge in edges))
    result = 0
    for factor in D5:
        if not active(labels[root], factor):
            continue
        # Closed factor components are circuits.
        active_edges = {edge for edge, label in enumerate(labels) if active(label, factor)}
        found, todo = {root}, [root]
        while todo:
            edge = todo.pop()
            for vertex in edges[edge]:
                local = [other for other in rows[vertex] if other in active_edges]
                assert len(local) == 2
                for other in local:
                    if other not in found:
                        found.add(other)
                        todo.append(other)
        active_ports = tuple(slot for slot, edge in enumerate(rows[z]) if edge in found)
        if len(active_ports) != 2:
            assert len(active_ports) == 0
            continue
        inactive = next(slot for slot in range(3) if slot not in active_ports)
        if labels[rows[z][inactive]] & factor:
            assert labels[rows[z][inactive]] == factor
            continue
        result |= 1 << PHYSICAL_INDEX[active_ports]
    return result


def direct_typed_data(
    n: int,
    edges: tuple[tuple[int, int], ...],
    labels: tuple[int, ...],
    z: int,
    root: int,
) -> tuple[int, int]:
    rows = incidence(n, tuple(tuple(edge) for edge in edges))
    typed = external = 0
    for factor in D5:
        if not active(labels[root], factor):
            continue
        active_edges = {edge for edge, label in enumerate(labels) if active(label, factor)}
        found, todo = {root}, [root]
        while todo:
            edge = todo.pop()
            for vertex in edges[edge]:
                local = [other for other in rows[vertex] if other in active_edges]
                assert len(local) == 2
                for other in local:
                    if other not in found:
                        found.add(other)
                        todo.append(other)
        active_ports = tuple(slot for slot, edge in enumerate(rows[z]) if edge in found)
        if len(active_ports) != 2:
            assert len(active_ports) == 0
            continue
        physical = PHYSICAL_INDEX[active_ports]
        inactive = next(slot for slot in range(3) if slot not in active_ports)
        inactive_label = labels[rows[z][inactive]]
        assert inactive_label == factor or not (inactive_label & factor)
        mode = int(inactive_label != factor)
        typed |= 1 << (2 * physical + mode)
        if mode:
            external |= 1 << physical
    return typed, external


def project_word(pole: Pole, word: tuple[int, ...]) -> dict[int, int]:
    return {edge: word[item] for item, edge in enumerate(pole.original_edges)}


def audit_case(
    name: str,
    graph_word: str,
    cut: tuple[int, ...],
    boundary_word: tuple[int, ...],
    z: int,
    root: int,
) -> None:
    n, edges = graph6(graph_word)
    rows = incidence(n, tuple(tuple(edge) for edge in edges))
    first, second = cut_shores(n, edges, cut)
    cap_shore = first if z in first else second
    root_shore = second if cap_shore == first else first
    assert all(z not in edges[edge] for edge in cut)
    assert all(endpoint in root_shore for endpoint in edges[root])
    cap_pole = make_pole(edges, cap_shore, cut)
    root_pole = make_pole(edges, root_shore, cut)
    cap_fixed = {item: label for item, label in zip(cap_pole.boundary_items, boundary_word)}
    root_fixed = {item: label for item, label in zip(root_pole.boundary_items, boundary_word)}
    cap_words = enumerate_labellings(n, cap_pole.items, cap_fixed)
    root_words = enumerate_labellings(n, root_pole.items, root_fixed)
    cap_relation = frozenset(cap_state(cap_pole, word, z, rows) for word in cap_words)
    root_relation = frozenset(root_state(root_pole, word, root) for word in root_words)

    direct_fixed = {edge: label for edge, label in zip(cut, boundary_word)}
    direct_words = enumerate_labellings(n, tuple(tuple(edge) for edge in edges), direct_fixed)
    product_words = set()
    predicted_masks = set()
    literal_masks = set()
    for root_word in root_words:
        root_projection = project_word(root_pole, root_word)
        root_signature = root_state(root_pole, root_word, root)
        for cap_word in cap_words:
            cap_projection = project_word(cap_pole, cap_word)
            assert all(root_projection[edge] == cap_projection[edge] for edge in cut)
            combined = tuple(
                root_projection[edge] if edge in root_projection else cap_projection[edge]
                for edge in range(len(edges))
            )
            product_words.add(combined)
            predicted = joined_external_mask(
                root_signature, cap_state(cap_pole, cap_word, z, rows))
            literal = direct_external_mask(n, edges, combined, z, root)
            assert predicted == literal
            predicted_masks.add(predicted)
            literal_masks.add(literal)

    assert product_words == set(direct_words)
    assert predicted_masks == literal_masks

    maximal_roots = frozenset(
        state for state in root_relation
        if not any(state != other and state | other == other for other in root_relation)
    )
    maximal_caps = frozenset(
        state for state in cap_relation
        if not any(state != other and all(a | b == b for a, b in zip(state, other))
                   for other in cap_relation)
    )
    compressed_masks = {
        joined_external_mask(root_state_value, cap_state_value)
        for root_state_value in maximal_roots
        for cap_state_value in maximal_caps
    }
    assert max(mask.bit_count() for mask in compressed_masks) == max(
        mask.bit_count() for mask in predicted_masks)

    print(
        f"{name} graph6={graph_word} cut={','.join(map(str, cut))} "
        f"boundary={','.join(f'{label:02x}' for label in boundary_word)} "
        f"root_flows={len(root_words)} cap_flows={len(cap_words)} "
        f"direct_flows={len(direct_words)} product={len(product_words)} "
        f"root_states={len(root_relation)}->{len(maximal_roots)} "
        f"cap_states={len(cap_relation)}->{len(maximal_caps)} "
        f"external_masks={','.join(map(str, sorted(literal_masks)))} PASS"
    )


def audit_boundary_algebra() -> None:
    two = {(a, b) for a in D5 for b in D5 if a ^ b == 0}
    assert two == {(label, label) for label in D5}
    three = {(a, b, c) for a in D5 for b in D5 for c in D5 if a ^ b ^ c == 0}
    assert len(three) == 60
    assert all(len({coordinate for label in row for coordinate in range(5)
                    if label & (1 << coordinate)}) == 3 for row in three)
    # Each row is an ordered triangle in K5.  There are C(5,3)*3! rows.
    assert len(three) == 10 * 6
    print("BOUNDARY two_pole_equal=10 three_pole_ordered_triangles=60 PASS")


def audit_constant_translation_algebra() -> None:
    """Exhaust the two nonzero legal constant circuit translations."""

    moves = 0
    for shift in range(1, 32):
        if shift.bit_count() not in (2, 4):
            continue
        for label in D5:
            legal = (label ^ shift) in D5_SET
            if shift.bit_count() == 2:
                expected = active(label, shift)
            else:
                missing = next(coordinate for coordinate in range(5)
                               if not (shift & (1 << coordinate)))
                expected = not (label & (1 << missing))
            assert legal == expected
            if not legal:
                continue
            moves += 1
            changed = label ^ shift
            for factor in D5:
                assert active(label, factor) ^ active(changed, factor) == (
                    (shift & factor).bit_count() & 1
                )
    # Ten weight-two shifts have six legal old duads each; five weight-four
    # shifts have C(4,2)=6 legal old duads each.
    assert moves == 90
    print(
        "TRANSLATION legal_weight2=60 legal_weight4=30 "
        "factor_toggle_law=PASS"
    )


def audit_complement_delimiter(
    name: str,
    graph_word: str,
    z: int,
    root: int,
    missing_coordinate: int,
    cycle: tuple[int, ...],
    before_hex: str,
    after_hex: str,
    expected_before: tuple[int, int],
    expected_after: tuple[int, int],
    expected_cap_intersection: tuple[int, ...],
) -> None:
    n, edges = graph6(graph_word)
    rows = incidence(n, tuple(tuple(edge) for edge in edges))
    before = tuple(bytes.fromhex(before_hex))
    after = tuple(bytes.fromhex(after_hex))
    assert len(before) == len(after) == len(edges)
    assert all(label in D5_SET for label in before + after)
    assert all(before[a] ^ before[b] ^ before[c] == 0 for a, b, c in rows)
    assert all(after[a] ^ after[b] ^ after[c] == 0 for a, b, c in rows)
    support = frozenset(cycle)
    support_degrees = [sum(edge in support for edge in row) for row in rows]
    assert all(degree in (0, 2) for degree in support_degrees)
    support_vertices = {vertex for vertex, degree in enumerate(support_degrees) if degree}
    seen, todo = {next(iter(support_vertices))}, [next(iter(support_vertices))]
    while todo:
        vertex = todo.pop()
        for edge in rows[vertex]:
            if edge not in support:
                continue
            for other in edges[edge]:
                if other not in seen:
                    seen.add(other)
                    todo.append(other)
    assert seen == support_vertices
    shift = 31 ^ (1 << missing_coordinate)
    assert shift.bit_count() == 4
    assert all(not (before[edge] & (1 << missing_coordinate)) for edge in support)
    assert after == tuple(label ^ shift if edge in support else label
                          for edge, label in enumerate(before))
    assert direct_typed_data(n, edges, before, z, root) == expected_before
    assert direct_typed_data(n, edges, after, z, root) == expected_after
    cap_intersection = tuple(edge for edge in rows[z] if edge in support)
    assert cap_intersection == expected_cap_intersection
    print(
        f"{name} graph6={graph_word} missing={missing_coordinate} "
        f"cycle={','.join(map(str, cycle))} "
        f"typed={expected_before[0]}->{expected_after[0]} "
        f"external={expected_before[1]}->{expected_after[1]} PASS"
    )


def main() -> None:
    audit_boundary_algebra()
    audit_constant_translation_algebra()
    # GCXmd_ has a nontrivial 2-cut (7,10).  Vertex 0 and root edge 5
    # lie on opposite shores, and the cut is disjoint from the cap edges.
    audit_case("TWO_CUT", "GCXmd_", (7, 10), (3, 3), 0, 5)
    # GCZJd_ has a nontrivial 3-cut (2,3,6).  Vertex 3 and root edge 1
    # lie on opposite shores, and the normalized boundary is 01,02,12.
    audit_case("THREE_CUT", "GCZJd_", (2, 3, 6), (3, 5, 6), 3, 1)
    audit_complement_delimiter(
        "ORDER12_COMPLEMENT", "K?`@EQgLAcAo", 0, 15, 4, (0, 3, 5),
        "03 05 06 05 0c 09 06 0c 0a 0a 06 0c 09 0a 03 0c 09 05",
        "0c 05 06 0a 0c 06 06 0c 0a 0a 06 0c 09 0a 03 0c 09 05",
        (32, 4), (10, 3), (0, 3),
    )
    audit_complement_delimiter(
        "ORDER14_COMPLEMENT", "M??CBAPqB_B_H_B_?", 7, 19, 3,
        (0, 6, 8, 18, 20),
        "03 05 0c 11 18 09 12 03 11 06 14 12 0a 03 09 18 0a 12 12 03 11",
        "14 05 0c 11 18 09 05 03 06 06 14 12 0a 03 09 18 0a 12 05 03 06",
        (19, 1), (51, 5), (),
    )
    print("PASS")


if __name__ == "__main__":
    main()
