#!/usr/bin/env python3
"""Independent standard-library verification of the 36-vertex APX countermodel.

The discovery program uses CaDiCaL to test two-T-join packing.  This
checker instead enumerates the complete binary cycle space of every
relevant complement and applies the elementary even-marked-circuit
criterion.  It also checks the graph premises and all counting identities
(19)--(27) from ``fano-reduced-kp-two-bond-frontier.md``.

Scope: the witness refutes only the auxiliary affine pair-exchange axiom
(APX).  It is not a counterexample to the Five-Cycle Double Cover
Conjecture.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json


GRAPH6 = (
    "chc?GC@@G?_P?H??_?G?@??C??G?@G??C??P??@G?A?__?@_???C???g???"
    "GA??@?A??CG???G???GG????C_???@??A??G??A??_???OH"
)

# Edge order is the standard graph6 upper-triangle order reconstructed below.
FLOW = (
    3, 5, 1, 6, 7, 2, 4, 1, 7, 6, 1, 6, 3, 7, 5, 2, 4, 7,
    3, 5, 3, 1, 2, 4, 5, 4, 1, 6, 5, 5, 3, 5, 6, 1, 6, 7,
    5, 1, 2, 4, 1, 6, 6, 7, 1, 4, 7, 6, 3, 7, 5, 4, 6, 2,
)

# Independent positive control: an explicit standard five-cycle double cover.
# Each two-character word gives the two coordinates containing that edge.
FIVE_CDC_LABELS = (
    "56", "05", "45", "05", "57", "46", "56", "05", "47", "04",
    "07", "45", "57", "45", "47", "57", "56", "06", "04", "47",
    "05", "04", "45", "46", "47", "07", "67", "67", "06", "67",
    "07", "06", "47", "04", "06", "07", "06", "67", "05", "07",
    "07", "57", "06", "05", "56", "04", "46", "07", "06", "57",
    "67", "46", "45", "56",
)

REPAIR_SWITCH_VALUE = 1
REPAIR_CIRCUIT = (0, 1, 17, 18, 20, 22, 31, 45, 47, 48, 49, 51, 53)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parity(value: int) -> int:
    return value.bit_count() & 1


def decode_graph6(record: str) -> tuple[int, list[tuple[int, int]]]:
    require(record and record[0] != "~", "only small graph6 is supported")
    order = ord(record[0]) - 63
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, "invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            require(cursor < len(bits), "truncated graph6")
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, edges


def incidence(
    order: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    answer = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        answer[left].append(edge)
        answer[right].append(edge)
    return answer


def components_after_edges(
    order: int,
    edges: list[tuple[int, int]],
    inc: list[list[int]],
    removed: set[int],
) -> list[set[int]]:
    seen: set[int] = set()
    answer: list[set[int]] = []
    for start in range(order):
        if start in seen:
            continue
        piece = {start}
        seen.add(start)
        queue = [start]
        for vertex in queue:
            for edge in inc[vertex]:
                if edge in removed:
                    continue
                left, right = edges[edge]
                other = left ^ right ^ vertex
                if other not in seen:
                    seen.add(other)
                    piece.add(other)
                    queue.append(other)
        answer.append(piece)
    return answer


def component_has_cycle(
    piece: set[int],
    edges: list[tuple[int, int]],
    removed: set[int],
) -> bool:
    internal_edges = sum(
        edge not in removed and left in piece and right in piece
        for edge, (left, right) in enumerate(edges)
    )
    return internal_edges >= len(piece)


def girth(
    order: int,
    edges: list[tuple[int, int]],
    inc: list[list[int]],
) -> int:
    best = order + 1
    for forbidden, (source, target) in enumerate(edges):
        distance = [-1] * order
        distance[source] = 0
        queue = [source]
        for vertex in queue:
            if distance[vertex] + 1 >= best:
                continue
            for edge in inc[vertex]:
                if edge == forbidden:
                    continue
                left, right = edges[edge]
                other = left ^ right ^ vertex
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    queue.append(other)
        if distance[target] >= 0:
            best = min(best, distance[target] + 1)
    return best


def first_cyclic_cut(
    order: int,
    edges: list[tuple[int, int]],
    inc: list[list[int]],
    size: int,
) -> tuple[int, ...] | None:
    for removed_tuple in combinations(range(len(edges)), size):
        removed = set(removed_tuple)
        pieces = components_after_edges(order, edges, inc, removed)
        cyclic = sum(
            component_has_cycle(piece, edges, removed) for piece in pieces
        )
        if cyclic >= 2:
            return removed_tuple
    return None


def perfect_matching_tait_test(
    order: int,
    edges: list[tuple[int, int]],
    inc: list[list[int]],
) -> tuple[int, bool]:
    """Enumerate all perfect matchings; an even complementary 2-factor is Tait."""

    all_vertices = (1 << order) - 1
    count = 0
    tait = False

    def complement_is_even(matching: int) -> bool:
        remaining = set(range(order))
        while remaining:
            start = min(remaining)
            previous = -1
            vertex = start
            length = 0
            while True:
                remaining.discard(vertex)
                next_vertex = -1
                for edge in inc[vertex]:
                    if (matching >> edge) & 1:
                        continue
                    left, right = edges[edge]
                    other = left ^ right ^ vertex
                    if other != previous:
                        next_vertex = other
                        break
                require(next_vertex >= 0, "complement is not a two-factor")
                previous, vertex = vertex, next_vertex
                length += 1
                if vertex == start:
                    break
            if length & 1:
                return False
        return True

    def visit(unmatched: int, matching: int) -> None:
        nonlocal count, tait
        if tait:
            return
        if not unmatched:
            count += 1
            tait = complement_is_even(matching)
            return
        vertex = (unmatched & -unmatched).bit_length() - 1
        for edge in inc[vertex]:
            left, right = edges[edge]
            other = left ^ right ^ vertex
            if (unmatched >> other) & 1:
                visit(
                    unmatched ^ (1 << vertex) ^ (1 << other),
                    matching | (1 << edge),
                )

    visit(all_vertices, 0)
    return count, tait


def fundamental_cycle_basis(
    order: int,
    edges: list[tuple[int, int]],
    inc: list[list[int]],
    kept_mask: int,
) -> list[int]:
    parent = [-1] * order
    parent_edge = [-1] * order
    depth = [0] * order
    tree_mask = 0
    for root in range(order):
        if parent[root] >= 0:
            continue
        parent[root] = root
        queue = [root]
        for vertex in queue:
            for edge in inc[vertex]:
                if not ((kept_mask >> edge) & 1):
                    continue
                left, right = edges[edge]
                other = left ^ right ^ vertex
                if parent[other] >= 0:
                    continue
                parent[other] = vertex
                parent_edge[other] = edge
                depth[other] = depth[vertex] + 1
                tree_mask |= 1 << edge
                queue.append(other)
    basis: list[int] = []
    for edge, (left0, right0) in enumerate(edges):
        if not ((kept_mask >> edge) & 1) or ((tree_mask >> edge) & 1):
            continue
        cycle = 1 << edge
        left, right = left0, right0
        while depth[left] > depth[right]:
            cycle ^= 1 << parent_edge[left]
            left = parent[left]
        while depth[right] > depth[left]:
            cycle ^= 1 << parent_edge[right]
            right = parent[right]
        while left != right:
            cycle ^= 1 << parent_edge[left]
            left = parent[left]
            cycle ^= 1 << parent_edge[right]
            right = parent[right]
        basis.append(cycle)
    return basis


class PackingOracle:
    """Exact two-disjoint-T-join test by complete binary-cycle enumeration."""

    def __init__(
        self,
        order: int,
        edges: list[tuple[int, int]],
        inc: list[list[int]],
    ) -> None:
        self.order = order
        self.edges = edges
        self.inc = inc
        self.all_edges = (1 << len(edges)) - 1
        self.cache: dict[int, bool] = {}
        self.ranks: dict[int, int] = {}
        self.cycles_tested = 0

    def packs(self, matching: int) -> bool:
        known = self.cache.get(matching)
        if known is not None:
            return known
        terminal_mask = 0
        occupied = 0
        for edge, (left, right) in enumerate(self.edges):
            if not ((matching >> edge) & 1):
                continue
            require(
                not ((occupied >> left) & 1)
                and not ((occupied >> right) & 1),
                "packing query is not a matching",
            )
            occupied |= (1 << left) | (1 << right)
            terminal_mask ^= (1 << left) | (1 << right)
        kept = self.all_edges ^ matching
        basis = fundamental_cycle_basis(
            self.order, self.edges, self.inc, kept
        )
        self.ranks[matching] = len(basis)
        cycle = 0
        previous_gray = 0
        answer = False
        for choice in range(1 << len(basis)):
            self.cycles_tested += 1
            gray = choice ^ (choice >> 1)
            if choice:
                changed = gray ^ previous_gray
                cycle ^= basis[changed.bit_length() - 1]
            previous_gray = gray
            if any(
                ((terminal_mask >> vertex) & 1)
                and sum((cycle >> edge) & 1 for edge in self.inc[vertex])
                != 2
                for vertex in range(self.order)
            ):
                continue
            selected_components = components_after_edges(
                self.order,
                self.edges,
                self.inc,
                {
                    edge
                    for edge in range(len(self.edges))
                    if not ((cycle >> edge) & 1)
                },
            )
            if all(
                sum((terminal_mask >> vertex) & 1 for vertex in piece) % 2
                == 0
                for piece in selected_components
                if any(
                    (cycle >> edge) & 1
                    for vertex in piece
                    for edge in self.inc[vertex]
                )
            ):
                answer = True
                break
        self.cache[matching] = answer
        return answer


def value_classes(flow: tuple[int, ...]) -> list[int]:
    answer = [0] * 8
    for edge, value in enumerate(flow):
        answer[value] |= 1 << edge
    return answer


def support_components(
    order: int,
    edges: list[tuple[int, int]],
    inc: list[list[int]],
    flow: tuple[int, ...],
    functional: int,
) -> tuple[list[int], list[int]]:
    labels = [-1] * order
    edge_counts: list[int] = []
    for start in range(order):
        if labels[start] >= 0:
            continue
        label = len(edge_counts)
        labels[start] = label
        queue = [start]
        twice = 0
        for vertex in queue:
            for edge in inc[vertex]:
                if not parity(functional & flow[edge]):
                    continue
                twice += 1
                left, right = edges[edge]
                other = left ^ right ^ vertex
                if labels[other] < 0:
                    labels[other] = label
                    queue.append(other)
        require(twice % 2 == 0, "component edge count is not integral")
        edge_counts.append(twice // 2)
    return labels, edge_counts


def balanced_collision_bound(boxes: int, objects: int) -> int:
    if boxes == 0:
        require(objects == 0, "objects in zero boxes")
        return 0
    quotient, remainder = divmod(objects, boxes)
    return (
        remainder * ((quotient + 1) * quotient // 2)
        + (boxes - remainder) * (quotient * (quotient - 1) // 2)
    )


def main() -> None:
    order, edges = decode_graph6(GRAPH6)
    inc = incidence(order, edges)
    require(order == 36 and len(edges) == 54, "wrong graph dimensions")
    require(len(set(edges)) == len(edges), "parallel edge")
    require(all(left != right for left, right in edges), "loop")
    require(all(len(row) == 3 for row in inc), "graph is not cubic")
    require(
        len(components_after_edges(order, edges, inc, set())) == 1,
        "graph is disconnected",
    )
    require(len(FLOW) == len(edges), "flow length mismatch")
    require(all(1 <= value <= 7 for value in FLOW), "flow has zero value")
    require(
        all(
            FLOW[row[0]] ^ FLOW[row[1]] ^ FLOW[row[2]] == 0
            for row in inc
        ),
        "flow equation fails",
    )
    require(len(FIVE_CDC_LABELS) == len(edges), "five-cover length mismatch")
    require(
        all(
            len(label) == 2
            and label[0] < label[1]
            and all(character in "04567" for character in label)
            for label in FIVE_CDC_LABELS
        ),
        "invalid five-cover edge label",
    )
    for vertex, row in enumerate(inc):
        for coordinate in "04567":
            require(
                sum(coordinate in FIVE_CDC_LABELS[edge] for edge in row) % 2
                == 0,
                f"five-cover parity fails at vertex {vertex}, "
                f"coordinate {coordinate}",
            )
    cover_sizes = [
        sum(coordinate in label for label in FIVE_CDC_LABELS)
        for coordinate in "04567"
    ]
    require(cover_sizes == [25, 19, 21, 21, 22], "five-cover sizes mismatch")

    graph_girth = girth(order, edges, inc)
    require(graph_girth == 5, "unexpected girth")
    for size in (1, 2, 3):
        require(
            first_cyclic_cut(order, edges, inc, size) is None,
            f"cyclic edge cut of size {size}",
        )
    cyclic_four_witness = first_cyclic_cut(order, edges, inc, 4)
    require(cyclic_four_witness is not None, "no cyclic four-cut found")
    perfect_matchings, tait = perfect_matching_tait_test(order, edges, inc)
    require(not tait, "graph is three-edge-colourable")

    classes = value_classes(FLOW)
    oracle = PackingOracle(order, edges, inc)
    class_sizes: dict[int, int] = {}
    q: dict[int, int] = {}
    packing_pair_counts: dict[int, int] = {}
    for value in range(1, 8):
        matching = classes[value]
        members = [
            edge for edge in range(len(edges)) if (matching >> edge) & 1
        ]
        class_sizes[value] = len(members)
        require(not oracle.packs(matching), f"value {value} already packs")
        packing_pairs = 0
        for left, right in combinations(members, 2):
            reduced = matching ^ (1 << left) ^ (1 << right)
            packing_pairs += oracle.packs(reduced)
        packing_pair_counts[value] = packing_pairs
        q[value] = len(members) * (len(members) - 1) // 2 - packing_pairs

    repair_mask = sum(1 << edge for edge in REPAIR_CIRCUIT)
    repair_degrees = [
        sum((repair_mask >> edge) & 1 for edge in row) for row in inc
    ]
    require(
        all(degree in (0, 2) for degree in repair_degrees),
        "repair support is not a binary cycle",
    )
    repair_vertices = {
        vertex for vertex, degree in enumerate(repair_degrees) if degree
    }
    repair_edges = [
        edges[edge] for edge in REPAIR_CIRCUIT
    ]
    repair_adjacency = {vertex: [] for vertex in repair_vertices}
    for left, right in repair_edges:
        repair_adjacency[left].append(right)
        repair_adjacency[right].append(left)
    reached = {min(repair_vertices)}
    queue = [min(repair_vertices)]
    for vertex in queue:
        for other in repair_adjacency[vertex]:
            if other not in reached:
                reached.add(other)
                queue.append(other)
    require(reached == repair_vertices, "repair support is disconnected")
    require(
        all(FLOW[edge] != REPAIR_SWITCH_VALUE for edge in REPAIR_CIRCUIT),
        "repair switch creates a zero value",
    )
    repaired_flow = tuple(
        value ^ REPAIR_SWITCH_VALUE
        if edge in REPAIR_CIRCUIT
        else value
        for edge, value in enumerate(FLOW)
    )
    require(
        all(
            repaired_flow[row[0]]
            ^ repaired_flow[row[1]]
            ^ repaired_flow[row[2]]
            == 0
            for row in inc
        ),
        "repaired flow equation fails",
    )
    repaired_classes = value_classes(repaired_flow)
    repaired_successful_values = [
        value
        for value in range(1, 8)
        if oracle.packs(repaired_classes[value])
    ]
    require(
        repaired_successful_values == [3],
        f"unexpected repaired successful values {repaired_successful_values}",
    )

    component_data: dict[int, tuple[list[int], list[int]]] = {}
    local_line: list[int] = []
    for vertex in range(order):
        line_values = [FLOW[edge] for edge in inc[vertex]]
        annihilators = [
            mu
            for mu in range(1, 8)
            if all(not parity(mu & value) for value in line_values)
        ]
        require(len(annihilators) == 1, "local line is not a Fano line")
        local_line.append(annihilators[0])

    z = Counter(local_line)
    a = Counter()
    for left, right in edges:
        if local_line[left] == local_line[right]:
            a[local_line[left]] += 1

    r: dict[int, int] = {}
    h: dict[tuple[int, int], int] = {}
    collision_occurrences: dict[tuple[int, int], int] = {}
    affine_occurrences: list[tuple[int, int, int, int]] = []
    for mu in range(1, 8):
        labels, edge_counts = support_components(
            order, edges, inc, FLOW, mu
        )
        component_data[mu] = labels, edge_counts
        isolated = sum(count == 0 for count in edge_counts)
        nontrivial = sum(count > 0 for count in edge_counts)
        require(isolated == z[mu], "z_U mismatch")
        r[mu] = nontrivial
        for value in range(1, 8):
            if parity(mu & value):
                continue
            members = [
                edge for edge in range(len(edges)) if FLOW[edge] == value
            ]
            boxes: Counter[tuple[int, int]] = Counter()
            big_big = 0
            for edge in members:
                left, right = edges[edge]
                box = tuple(sorted((labels[left], labels[right])))
                boxes[box] += 1
                if edge_counts[box[0]] and edge_counts[box[1]]:
                    big_big += 1
            h[value, mu] = big_big
            collisions = 0
            for box, multiplicity in boxes.items():
                if not edge_counts[box[0]] or not edge_counts[box[1]]:
                    require(multiplicity == 1, "isolated type repeats")
                collisions += multiplicity * (multiplicity - 1) // 2
            collision_occurrences[value, mu] = collisions
            for left_index, right_index in combinations(range(len(members)), 2):
                p, q_edge = members[left_index], members[right_index]
                p_ends = tuple(
                    sorted(labels[vertex] for vertex in edges[p])
                )
                q_ends = tuple(
                    sorted(labels[vertex] for vertex in edges[q_edge])
                )
                if p_ends == q_ends:
                    affine_occurrences.append((value, mu, p, q_edge))

    require(
        len(affine_occurrences)
        == sum(collision_occurrences.values()),
        "collision occurrence count mismatch",
    )
    apx_witnesses: list[tuple[int, int, int, int]] = []
    for value, mu, p, q_edge in affine_occurrences:
        reduced = classes[value] ^ (1 << p) ^ (1 << q_edge)
        if oracle.packs(reduced):
            apx_witnesses.append((value, mu, p, q_edge))
    require(not apx_witnesses, "APX witness found")

    # Identities (19)--(23).
    require(sum(z[mu] for mu in range(1, 8)) == order, "(19) fails")
    for value in range(1, 8):
        require(
            sum(z[mu] for mu in range(1, 8) if not parity(mu & value))
            == 2 * class_sizes[value],
            f"(20) fails for value {value}",
        )
    for mu in range(1, 8):
        line_values = [
            value for value in range(1, 8) if not parity(mu & value)
        ]
        require(
            sum(class_sizes[value] for value in line_values)
            == order // 2 + z[mu],
            f"(21) fails for line {mu}",
        )
        require(
            sum(h[value, mu] for value in line_values)
            == order // 2 - 2 * z[mu] + a[mu],
            f"(22) fails for line {mu}",
        )
    total_h = sum(h.values())
    total_a = sum(a.values())
    require(total_h == 3 * order // 2 + total_a, "(23) fails")

    # Inequalities (24)--(27), evaluated exactly on the countermodel.
    boxes_by_line = {
        mu: r[mu] * (r[mu] + 1) // 2 for mu in range(1, 8)
    }
    pure_repeat_left = order + 2 * total_a / 3
    pure_repeat_right = sum(r[mu] * (r[mu] + 1) for mu in range(1, 8))
    H = 3 * order // 2 + total_a
    B = 3 * sum(boxes_by_line.values())
    Q = sum(q.values())
    aggregate_lower = balanced_collision_bound(B, H)
    separated_lower = sum(
        balanced_collision_bound(boxes_by_line[mu], h[value, mu])
        for mu in range(1, 8)
        for value in range(1, 8)
        if not parity(mu & value)
    )
    require(aggregate_lower <= 3 * Q, "(25) contradicts APX failure")
    require(separated_lower <= 3 * Q, "(26) contradicts APX failure")
    require(
        sum(r.values()) * graph_girth <= 6 * order,
        "(27) fails",
    )

    by_value = {}
    expected_rows = {
        1: (9, 36, 6, 30, 5, 5),
        2: (5, 10, 9, 1, 0, 0),
        3: (6, 15, 12, 3, 0, 0),
        4: (7, 21, 10, 11, 2, 2),
        5: (9, 36, 9, 27, 4, 4),
        6: (10, 45, 0, 45, 14, 14),
        7: (8, 28, 11, 17, 8, 7),
    }
    for value in range(1, 8):
        occurrences = [
            item for item in affine_occurrences if item[0] == value
        ]
        unique_pairs = {(p, q_edge) for _, _, p, q_edge in occurrences}
        row = {
            "class_size": class_sizes[value],
            "all_pairs": class_sizes[value] * (class_sizes[value] - 1) // 2,
            "packing_pairs": packing_pair_counts[value],
            "q_s_nonpacking_pairs": q[value],
            "affine_occurrences": len(occurrences),
            "affine_unique_pairs": len(unique_pairs),
            "affine_packing_occurrences": 0,
        }
        require(
            tuple(
                row[key]
                for key in (
                    "class_size",
                    "all_pairs",
                    "packing_pairs",
                    "q_s_nonpacking_pairs",
                    "affine_occurrences",
                    "affine_unique_pairs",
                )
            )
            == expected_rows[value],
            f"frozen summary mismatch for value {value}",
        )
        by_value[str(value)] = row

    require(perfect_matchings == 221, "perfect-matching count mismatch")
    require(
        cyclic_four_witness == (15, 29, 36, 38),
        "first cyclic four-cut mismatch",
    )
    require(len(affine_occurrences) == 33, "affine count mismatch")
    require(Q == 134, "global nonpacking budget mismatch")

    print(
        json.dumps(
            {
                "status": "PASS",
                "scope": "APX countermodel only; FiveCDC remains open",
                "graph6": GRAPH6,
                "vertices": order,
                "edges": len(edges),
                "girth": graph_girth,
                "cyclic_edge_connectivity": 4,
                "displayed_cyclic_four_cut": list(cyclic_four_witness),
                "perfect_matchings_exhausted": perfect_matchings,
                "three_edge_colourable": tait,
                "bad_value_classes": 7,
                "positive_five_cdc_control": {
                    "valid": True,
                    "cover_sizes": cover_sizes,
                    "labels": list(FIVE_CDC_LABELS),
                },
                "one_circuit_repair_control": {
                    "switch_value": REPAIR_SWITCH_VALUE,
                    "circuit_edges": list(REPAIR_CIRCUIT),
                    "successful_values_after_switch": repaired_successful_values,
                    "complete_cpp_audit": {
                        "simple_circuits": 166792,
                        "legal_switches": 9532,
                        "good_switches": 6699,
                    },
                },
                "apx_witness_count": len(apx_witnesses),
                "affine_occurrence_count": len(affine_occurrences),
                "per_value": by_value,
                "affine_occurrences": [
                    {"s": value, "mu": mu, "pair": [p, q_edge]}
                    for value, mu, p, q_edge in affine_occurrences
                ],
                "identities_19_23": True,
                "line_statistics": {
                    str(mu): {
                        "z_U": z[mu],
                        "a_U": a[mu],
                        "r_U": r[mu],
                        "N_U": boxes_by_line[mu],
                        "h_s_U": {
                            str(value): h[value, mu]
                            for value in range(1, 8)
                            if not parity(mu & value)
                        },
                    }
                    for mu in range(1, 8)
                },
                "global_budget": {
                    "A": total_a,
                    "H": H,
                    "B": B,
                    "Q": Q,
                    "L_B_H": aggregate_lower,
                    "separated_L_sum": separated_lower,
                    "three_Q": 3 * Q,
                    "sum_r": sum(r.values()),
                    "girth_times_sum_r": graph_girth * sum(r.values()),
                    "six_n": 6 * order,
                    "repeat_left_24": pure_repeat_left,
                    "repeat_right_24": pure_repeat_right,
                },
                "maximum_cycle_rank_checked": max(oracle.ranks.values()),
                "packing_queries": len(oracle.cache),
                "binary_cycles_tested": oracle.cycles_tested,
                "edge_value_table": [
                    [left, right, FLOW[edge]]
                    for edge, (left, right) in enumerate(edges)
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
