#!/usr/bin/env python3
"""Exact audit of the current Hušek--Šámal one-switch boundary.

For a nowhere-zero F_2^3-flow f and nonzero functional mu, let K_mu be
the edges on which mu(f(e)) = 0.  The Hušek--Šámal condition says that
every component of K_mu contains an even number of endpoints of any
one affine value class mu(f(e)) = 1.

This solver-independent checker verifies:

* explicit one-simple-cycle repairs on cyclically 4-edge-connected
  36- and 60-vertex cubic graphs; and
* exhaustive failure of every legal one-simple-cycle switch on a
  connected 40-vertex cubic graph having nontrivial cyclic 2-edge-cuts.

The 40-vertex certificate is read from the separately checked
``connected-one-switch-countermodel-40v-20260726/construction.json``.
The graph has an explicit FiveCDC, so it is only a counterexample to
the unrestricted one-switch auxiliary statement.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ORDER40_CERTIFICATE = (
    HERE.parent
    / "search"
    / "connected-one-switch-countermodel-40v-20260726"
    / "construction.json"
)

GRAPH36 = (
    "chc?GC@@G?_P?H??_?G?@??C??G?@G??C??P??@G?A?__?@_???C???g???"
    "GA??@?A??CG???G???GG????C_???@??A??G??A??_???OH"
)
FLOW36 = (
    3, 5, 1, 6, 7, 2, 4, 1, 7, 6, 1, 6, 3, 7, 5, 2, 4, 7,
    3, 5, 3, 1, 2, 4, 5, 4, 1, 6, 5, 5, 3, 5, 6, 1, 6, 7,
    5, 1, 2, 4, 1, 6, 6, 7, 1, 4, 7, 6, 3, 7, 5, 4, 6, 2,
)
SWITCH36 = (
    7,
    (0, 1, 2, 3, 6, 7, 9, 10, 11, 14, 15, 16, 19, 20, 21, 32,
     33, 38, 40, 41, 47, 50, 51, 53),
)
PROFILE36_BEFORE = (8, 6, 6, 10, 8, 4, 6)
PROFILE36_AFTER = (10, 6, 6, 6, 6, 0, 8)

GRAPH60 = (
    "{??K`C?O[@G@P??Go??G?A????w_?_O@C??GC??G??@????G??????C???@O???"
    "J???B????BG?G???????????C?G???????????????@???????????G_???????A??"
    "A@?????_G????@AG????AG??????DC????A???????@???????O????????F?????"
    "C?C?????A?G_??????@??????_?@????????G?????@???????@????????????_??"
    "??????I????????@W????????W?????????X"
)
FLOW60 = (
    7, 6, 5, 6, 3, 6, 5, 3, 4, 6, 3, 2, 5, 2, 5, 7, 2, 5,
    5, 5, 2, 7, 2, 7, 2, 7, 5, 2, 7, 3, 1, 4, 4, 2, 6, 3,
    7, 4, 3, 2, 2, 3, 1, 1, 1, 2, 4, 6, 3, 2, 1, 3, 7, 1,
    3, 5, 6, 2, 6, 6, 2, 4, 6, 2, 2, 2, 6, 4, 6, 4, 6, 4,
    2, 6, 4, 3, 5, 5, 7, 7, 6, 1, 3, 4, 7, 3, 6, 6, 3, 5,
)
SWITCH60 = (
    7,
    (1, 2, 8, 11, 18, 22, 24, 26, 27, 30, 31, 33, 35, 37, 39, 40,
     42, 43, 45, 62, 65, 67, 73, 74, 75),
)
PROFILE60_BEFORE = (8, 8, 4, 6, 6, 8, 6)
PROFILE60_AFTER = (10, 6, 6, 8, 8, 6, 0)

PROFILE40_BEFORE = (12, 6, 6, 10, 12, 6, 6)

GRAPH40_REDUCED = (
    "gCO?_O_???o?G??A??C???O???IC??A???g_???O?C?_??A?@G??@?o?A@??"
    "G???A?????ACC????OO????OO@?A?@???G`??_?A??K?A??G??C??_?@?O?a?_"
    "??A??_??C"
)
FLOW40_REDUCED = (
    1, 3, 2, 1, 2, 1, 3, 3, 7, 2, 3, 5, 1, 3, 2, 1, 6, 7,
    4, 5, 3, 7, 7, 1, 4, 2, 6, 3, 6, 1, 2, 6, 4, 2, 6, 1,
    3, 3, 5, 6, 2, 5, 7, 1, 6, 7, 2, 6, 4, 3, 5, 1, 5, 4,
    3, 2, 1, 2, 4, 6,
)
PROFILE40_REDUCED = (6, 8, 10, 4, 10, 6, 6)
TAIT40_REDUCED = (
    1, 1, 2, 2, 3, 3, 2, 2, 2, 3, 1, 2, 2, 1, 3, 2, 1, 3,
    1, 1, 2, 3, 3, 1, 1, 3, 2, 1, 3, 2, 3, 3, 1, 2, 3, 2,
    1, 3, 1, 2, 3, 2, 1, 1, 2, 3, 3, 2, 1, 1, 3, 3, 1, 2,
    1, 2, 3, 3, 1, 2,
)

GRAPH26_STRICT = (
    "Y?HI@e??GC?Ba??CO???ACG??BH?G?g?C??O??GI??@??C@?A?C??C@_"
)
FLOW26_STRICT = (
    7, 5, 3, 7, 1, 3, 2, 3, 5, 5, 2, 6, 1, 4, 7, 2, 3, 7,
    6, 5, 4, 1, 6, 4, 4, 6, 2, 5, 6, 4, 2, 1, 4, 3, 3, 2,
    6, 7, 1,
)
PROFILE26_STRICT = (8, 8, 4, 6, 6, 6, 4)
FIVECDC26_STRICT = (
    12, 6, 20, 12, 6, 3, 5, 3, 18, 9, 17, 3, 17, 24, 3, 18,
    18, 9, 17, 9, 17, 24, 10, 18, 10, 18, 24, 24, 24, 10, 10,
    18, 10, 24, 10, 18, 10, 18, 24,
)
TWO_SWITCH26_STRICT = (
    (
        1,
        (1, 2, 3, 7, 8, 9, 10, 11, 13, 15, 16, 19, 20, 27, 28, 29),
    ),
    (
        5,
        (0, 1, 2, 4, 6, 7, 8, 9, 10, 11, 15, 30, 32, 33),
    ),
)
TWO_SWITCH26_PROFILES = (
    (2, 8, 4, 6, 6, 6, 10),
    (2, 4, 4, 6, 4, 0, 6),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parity(value: int) -> int:
    return value.bit_count() & 1


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    """Decode graph6 records of order at most 62 in upper-triangle order."""

    require(record and record[0] != "~", "only small graph6 is supported")
    order = ord(record[0]) - 63
    require(0 <= order <= 62, "bad graph6 order")
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, "bad graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            require(cursor < len(bits), "truncated graph6 record")
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    require(
        not any(bits[cursor:]),
        "nonzero graph6 padding or trailing payload",
    )
    return order, tuple(edges)


def incidence(
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], ...]:
    rows = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        require(0 <= left < right < order, "edge is not normalized")
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


def check_cubic_flow(
    order: int,
    edges: tuple[tuple[int, int], ...],
    values: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    require(len(edges) == 3 * order // 2, "wrong cubic edge count")
    require(len(set(edges)) == len(edges), "parallel edge")
    vertex_edges = incidence(order, edges)
    require(all(len(row) == 3 for row in vertex_edges), "not cubic")
    require(len(values) == len(edges), "flow length mismatch")
    require(all(1 <= value <= 7 for value in values), "zero flow value")
    require(
        all(
            values[row[0]] ^ values[row[1]] ^ values[row[2]] == 0
            for row in vertex_edges
        ),
        "flow conservation failed",
    )
    reached = {0}
    queue = [0]
    for vertex in queue:
        for edge in vertex_edges[vertex]:
            left, right = edges[edge]
            other = left ^ right ^ vertex
            if other not in reached:
                reached.add(other)
                queue.append(other)
    require(len(reached) == order, "graph is disconnected")
    return vertex_edges


def component_defects(
    order: int,
    edges: tuple[tuple[int, int], ...],
    values: tuple[int, ...],
    functional: int,
) -> int:
    """Count K_mu components having odd affine-value endpoint parity."""

    adjacency = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        if parity(values[edge] & functional) == 0:
            adjacency[left].append(right)
            adjacency[right].append(left)

    components = []
    unseen = set(range(order))
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        queue = [root]
        for vertex in queue:
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        components.append(component)

    affine_values = tuple(
        value for value in range(1, 8)
        if parity(value & functional)
    )
    require(len(affine_values) == 4, "functional has wrong affine side")
    parity_rows = []
    for affine_value in affine_values:
        marked = {
            vertex
            for edge, (left, right) in enumerate(edges)
            if values[edge] == affine_value
            for vertex in (left, right)
        }
        parity_rows.append(tuple(
            len(marked & component) & 1
            for component in components
        ))
    require(
        len(set(parity_rows)) == 1,
        "affine value classes disagree on component parity",
    )
    return sum(parity_rows[0])


def defect_profile(
    order: int,
    edges: tuple[tuple[int, int], ...],
    values: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(
        component_defects(order, edges, values, functional)
        for functional in range(1, 8)
    )


def is_simple_cycle(
    order: int,
    edges: tuple[tuple[int, int], ...],
    selected: tuple[int, ...],
) -> bool:
    require(len(set(selected)) == len(selected), "repeated cycle edge")
    degree: Counter[int] = Counter()
    adjacency = [[] for _ in range(order)]
    for edge in selected:
        require(0 <= edge < len(edges), "cycle edge out of range")
        left, right = edges[edge]
        degree[left] += 1
        degree[right] += 1
        adjacency[left].append(right)
        adjacency[right].append(left)
    if not degree or set(degree.values()) != {2}:
        return False
    reached = {min(degree)}
    queue = list(reached)
    for vertex in queue:
        for neighbor in adjacency[vertex]:
            if neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    return reached == set(degree)


def switched(
    values: tuple[int, ...],
    switch_value: int,
    selected: tuple[int, ...],
) -> tuple[int, ...]:
    selected_set = set(selected)
    require(
        all(values[edge] != switch_value for edge in selected),
        "switch would create a zero edge",
    )
    return tuple(
        value ^ switch_value if edge in selected_set else value
        for edge, value in enumerate(values)
    )


def all_simple_cycle_masks(
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[int, ...]:
    """Enumerate each undirected simple cycle exactly once."""

    vertex_edges = incidence(order, edges)
    cycles = []
    used = [False] * order
    path_vertices = []

    def extend(start: int, vertex: int, support: int) -> None:
        for edge in vertex_edges[vertex]:
            left, right = edges[edge]
            other = left ^ right ^ vertex
            if other == start:
                if len(path_vertices) >= 3 and path_vertices[1] < vertex:
                    cycles.append(support | (1 << edge))
                continue
            if other < start or used[other]:
                continue
            used[other] = True
            path_vertices.append(other)
            extend(start, other, support | (1 << edge))
            path_vertices.pop()
            used[other] = False

    for start in range(order):
        used[start] = True
        path_vertices[:] = [start]
        extend(start, start, 0)
        used[start] = False

    require(len(cycles) == len(set(cycles)), "duplicate simple cycle")
    return tuple(cycles)


def components_after_removal(
    order: int,
    edges: tuple[tuple[int, int], ...],
    vertex_edges: tuple[tuple[int, ...], ...],
    removed: frozenset[int],
) -> tuple[frozenset[int], ...]:
    unseen = set(range(order))
    components = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        piece = {root}
        queue = [root]
        for vertex in queue:
            for edge in vertex_edges[vertex]:
                if edge in removed:
                    continue
                left, right = edges[edge]
                other = left ^ right ^ vertex
                if other in unseen:
                    unseen.remove(other)
                    piece.add(other)
                    queue.append(other)
        components.append(frozenset(piece))
    return tuple(components)


def cyclic_cut_count(
    order: int,
    edges: tuple[tuple[int, int], ...],
    size: int,
) -> int:
    vertex_edges = incidence(order, edges)
    result = 0
    for removed_tuple in combinations(range(len(edges)), size):
        removed = frozenset(removed_tuple)
        pieces = components_after_removal(
            order, edges, vertex_edges, removed
        )
        cyclic_pieces = 0
        for piece in pieces:
            internal_edges = sum(
                edge not in removed and left in piece and right in piece
                for edge, (left, right) in enumerate(edges)
            )
            cyclic_pieces += internal_edges >= len(piece)
        result += cyclic_pieces >= 2
    return result


def graph_girth(
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> int:
    vertex_edges = incidence(order, edges)
    best = order + 1
    for forbidden, (source, target) in enumerate(edges):
        distance = [-1] * order
        distance[source] = 0
        queue = [source]
        for vertex in queue:
            if distance[vertex] + 1 >= best:
                continue
            for edge in vertex_edges[vertex]:
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


def has_tait_coloring(
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> bool:
    vertex_edges = incidence(order, edges)
    colors = [-1] * len(edges)
    used = [0] * order

    def search(colored: int) -> bool:
        if colored == len(edges):
            return True
        best_edge = -1
        best_available = 0
        best_count = 4
        for edge, (left, right) in enumerate(edges):
            if colors[edge] >= 0:
                continue
            available = 0b111 & ~(used[left] | used[right])
            count = available.bit_count()
            if count == 0:
                return False
            if count < best_count:
                best_edge = edge
                best_available = available
                best_count = count
                if count == 1:
                    break
        require(best_edge >= 0, "Tait search lost an edge")
        left, right = edges[best_edge]
        available = best_available
        while available:
            bit = available & -available
            available ^= bit
            colors[best_edge] = bit
            used[left] |= bit
            used[right] |= bit
            if search(colored + 1):
                return True
            used[left] ^= bit
            used[right] ^= bit
            colors[best_edge] = -1
        return False

    # The incidence is computed here deliberately: it also ensures no
    # isolated edge data escaped the cubic checks in callers.
    require(all(len(row) == 3 for row in vertex_edges), "not cubic")
    return search(0)


def check_positive(
    name: str,
    graph6: str,
    values: tuple[int, ...],
    switch: tuple[int, tuple[int, ...]],
    expected_before: tuple[int, ...],
    expected_after: tuple[int, ...],
) -> dict[str, object]:
    order, edges = decode_graph6(graph6)
    vertex_edges = check_cubic_flow(order, edges, values)
    before = defect_profile(order, edges, values)
    require(before == expected_before, f"{name}: initial profile differs")
    require(0 not in before, f"{name}: initial flow is already clean")
    switch_value, cycle = switch
    require(
        is_simple_cycle(order, edges, cycle),
        f"{name}: switch support is not a simple cycle",
    )
    repaired = switched(values, switch_value, cycle)
    check_cubic_flow(order, edges, repaired)
    after = defect_profile(order, edges, repaired)
    require(after == expected_after, f"{name}: repaired profile differs")
    require(0 in after, f"{name}: switch did not repair the flow")
    cyclic_cut_counts = {
        str(size): cyclic_cut_count(order, edges, size)
        for size in range(1, 4)
    }
    require(
        all(count == 0 for count in cyclic_cut_counts.values()),
        f"{name}: graph is not cyclically 4-edge-connected",
    )
    return {
        "order": order,
        "edges": len(edges),
        "initial_defect_profile": before,
        "switch_value": switch_value,
        "switch_edge_ids": cycle,
        "switch_length": len(cycle),
        "repaired_defect_profile": after,
        "clean_functionals_after": [
            functional
            for functional, defect in enumerate(after, start=1)
            if defect == 0
        ],
        "cyclic_cut_counts_sizes_1_to_3": cyclic_cut_counts,
        "cyclically_4_edge_connected": True,
        "flow_conservation_after": all(
            repaired[row[0]] ^ repaired[row[1]] ^ repaired[row[2]] == 0
            for row in vertex_edges
        ),
    }


def check_negative_order40() -> dict[str, object]:
    certificate = json.loads(
        ORDER40_CERTIFICATE.read_text(encoding="utf-8")
    )
    expanded = certificate["expanded_graph"]
    order = int(expanded["vertices"])
    edges = tuple(
        tuple(sorted(map(int, row)))
        for row in expanded["edges"]
    )
    values = tuple(map(int, expanded["flow_values_by_edge"]))
    decoded_order, decoded_edges = decode_graph6(str(expanded["graph6"]))
    require(decoded_order == order, "order-40 graph6 order differs")
    require(
        set(decoded_edges) == set(edges),
        "order-40 graph6 edge set differs",
    )
    check_cubic_flow(order, edges, values)
    before = defect_profile(order, edges, values)
    require(before == PROFILE40_BEFORE, "order-40 initial profile differs")
    require(0 not in before, "order-40 initial flow is already clean")

    cycles = all_simple_cycle_masks(order, edges)
    legal_switches = 0
    clean_switches = 0
    minimum_defect = min(before)
    minimum_profile = None
    for cycle_mask in cycles:
        selected = tuple(
            edge for edge in range(len(edges))
            if cycle_mask >> edge & 1
        )
        for switch_value in range(1, 8):
            if any(values[edge] == switch_value for edge in selected):
                continue
            legal_switches += 1
            candidate = switched(values, switch_value, selected)
            candidate_profile = defect_profile(
                order, edges, candidate
            )
            candidate_minimum = min(candidate_profile)
            if candidate_minimum < minimum_defect:
                minimum_defect = candidate_minimum
                minimum_profile = candidate_profile
            if candidate_minimum == 0:
                clean_switches += 1

    require(len(cycles) == 6780, "order-40 cycle count differs")
    require(legal_switches == 1844, "order-40 legal-switch count differs")
    require(clean_switches == 0, "order-40 has a clean one-switch repair")
    require(minimum_defect == 2, "order-40 minimum defect differs")
    two_cuts = cyclic_cut_count(order, edges, 2)
    require(two_cuts == 5, "order-40 cyclic 2-cut count differs")
    five_cdc_checks = expanded["five_cdc_checks"]
    require(
        five_cdc_checks["exact_two"]
        and five_cdc_checks["even_incidence"],
        "order-40 positive FiveCDC control failed",
    )
    return {
        "order": order,
        "edges": len(edges),
        "initial_defect_profile": before,
        "simple_cycles_exhausted": len(cycles),
        "legal_cycle_value_switches_exhausted": legal_switches,
        "clean_one_switch_repairs": clean_switches,
        "minimum_defect_after_at_most_one_switch": minimum_defect,
        "one_minimum_profile": minimum_profile,
        "cyclic_2_edge_cuts": two_cuts,
        "cyclically_4_edge_connected": False,
        "explicit_five_cdc_control": True,
    }


def check_negative_reduced_order40() -> dict[str, object]:
    order, edges = decode_graph6(GRAPH40_REDUCED)
    values = FLOW40_REDUCED
    vertex_edges = check_cubic_flow(order, edges, values)
    before = defect_profile(order, edges, values)
    require(
        before == PROFILE40_REDUCED,
        "reduced order-40 initial profile differs",
    )
    require(0 not in before, "reduced order-40 flow is already clean")

    require(
        len(TAIT40_REDUCED) == len(edges)
        and set(TAIT40_REDUCED) == {1, 2, 3},
        "reduced order-40 Tait data malformed",
    )
    require(
        all(
            sorted(TAIT40_REDUCED[edge] for edge in row) == [1, 2, 3]
            for row in vertex_edges
        ),
        "reduced order-40 Tait coloring failed",
    )

    cycles = all_simple_cycle_masks(order, edges)
    legal_switches = 0
    clean_switches = 0
    minimum_defect = min(before)
    minimum_profile = None
    for cycle_mask in cycles:
        selected = tuple(
            edge for edge in range(len(edges))
            if cycle_mask >> edge & 1
        )
        present = {
            values[edge] for edge in selected
        }
        for switch_value in range(1, 8):
            if switch_value in present:
                continue
            legal_switches += 1
            candidate = switched(values, switch_value, selected)
            candidate_profile = defect_profile(
                order, edges, candidate
            )
            candidate_minimum = min(candidate_profile)
            if candidate_minimum < minimum_defect:
                minimum_defect = candidate_minimum
                minimum_profile = candidate_profile
            clean_switches += candidate_minimum == 0

    require(
        len(cycles) == 941438,
        "reduced order-40 cycle count differs",
    )
    require(
        legal_switches == 48544,
        "reduced order-40 legal-switch count differs",
    )
    require(
        clean_switches == 0,
        "reduced order-40 has a clean one-switch repair",
    )
    cyclic_cut_counts = {
        str(size): cyclic_cut_count(order, edges, size)
        for size in range(1, 4)
    }
    require(
        all(count == 0 for count in cyclic_cut_counts.values()),
        "reduced order-40 graph is not cyclically 4-edge-connected",
    )
    girth = graph_girth(order, edges)
    require(girth == 5, "reduced order-40 girth differs")
    return {
        "order": order,
        "edges": len(edges),
        "girth": girth,
        "initial_defect_profile": before,
        "simple_cycles_exhausted": len(cycles),
        "legal_cycle_value_switches_exhausted": legal_switches,
        "clean_one_switch_repairs": clean_switches,
        "minimum_defect_after_at_most_one_switch": minimum_defect,
        "one_minimum_profile": minimum_profile,
        "cyclic_cut_counts_sizes_1_to_3": cyclic_cut_counts,
        "cyclically_4_edge_connected": True,
        "three_edge_colorable": True,
        "explicit_three_cdc_control": True,
        "strict_snark": False,
    }


def check_negative_strict_order26() -> dict[str, object]:
    order, edges = decode_graph6(GRAPH26_STRICT)
    values = FLOW26_STRICT
    vertex_edges = check_cubic_flow(order, edges, values)
    before = defect_profile(order, edges, values)
    require(
        before == PROFILE26_STRICT,
        "strict order-26 initial profile differs",
    )
    require(0 not in before, "strict order-26 flow is already clean")

    cycles = all_simple_cycle_masks(order, edges)
    legal_switches = 0
    clean_switches = 0
    minimum_defect = min(before)
    minimum_profile = None
    for cycle_mask in cycles:
        selected = tuple(
            edge for edge in range(len(edges))
            if cycle_mask >> edge & 1
        )
        present = {values[edge] for edge in selected}
        for switch_value in range(1, 8):
            if switch_value in present:
                continue
            legal_switches += 1
            candidate = switched(values, switch_value, selected)
            candidate_profile = defect_profile(
                order, edges, candidate
            )
            candidate_minimum = min(candidate_profile)
            if candidate_minimum < minimum_defect:
                minimum_defect = candidate_minimum
                minimum_profile = candidate_profile
            clean_switches += candidate_minimum == 0

    require(len(cycles) == 8797, "strict order-26 cycle count differs")
    require(
        legal_switches == 1604,
        "strict order-26 legal-switch count differs",
    )
    require(
        clean_switches == 0,
        "strict order-26 has a clean one-switch repair",
    )
    cyclic_cut_counts = {
        str(size): cyclic_cut_count(order, edges, size)
        for size in range(1, 4)
    }
    require(
        all(count == 0 for count in cyclic_cut_counts.values()),
        "strict order-26 graph is not cyclically 4-edge-connected",
    )
    girth = graph_girth(order, edges)
    require(girth == 5, "strict order-26 girth differs")
    require(
        not has_tait_coloring(order, edges),
        "strict order-26 graph is Tait colorable",
    )

    current = values
    path_profiles = []
    for (switch_value, selected), expected_profile in zip(
        TWO_SWITCH26_STRICT, TWO_SWITCH26_PROFILES
    ):
        require(
            is_simple_cycle(order, edges, selected),
            "strict order-26 path support is not a simple cycle",
        )
        current = switched(current, switch_value, selected)
        check_cubic_flow(order, edges, current)
        current_profile = defect_profile(order, edges, current)
        require(
            current_profile == expected_profile,
            "strict order-26 path profile differs",
        )
        path_profiles.append(current_profile)
    require(
        0 not in path_profiles[0] and 0 in path_profiles[1],
        "strict order-26 distance-two control failed",
    )

    require(
        len(FIVECDC26_STRICT) == len(edges)
        and all(label.bit_count() == 2 for label in FIVECDC26_STRICT),
        "strict order-26 FiveCDC labels fail exact-two",
    )
    for row in vertex_edges:
        for coordinate in range(5):
            require(
                sum(
                    FIVECDC26_STRICT[edge] >> coordinate & 1
                    for edge in row
                ) % 2 == 0,
                "strict order-26 FiveCDC parity failed",
            )

    return {
        "order": order,
        "edges": len(edges),
        "girth": girth,
        "initial_defect_profile": before,
        "simple_cycles_exhausted": len(cycles),
        "legal_cycle_value_switches_exhausted": legal_switches,
        "clean_one_switch_repairs": clean_switches,
        "minimum_defect_after_at_most_one_switch": minimum_defect,
        "one_minimum_profile": minimum_profile,
        "cyclic_cut_counts_sizes_1_to_3": cyclic_cut_counts,
        "cyclically_4_edge_connected": True,
        "three_edge_colorable": False,
        "strict_snark": True,
        "explicit_five_cdc_labels": FIVECDC26_STRICT,
        "explicit_five_cdc_control": True,
        "exact_husek_samal_distance": 2,
        "two_switch_repair": TWO_SWITCH26_STRICT,
        "two_switch_profiles": path_profiles,
    }


def main() -> None:
    result = {
        "schema": "husek-samal-one-switch-boundary-check-v1",
        "scope": (
            "auxiliary reconfiguration boundary; no FiveCDC "
            "counterexample is claimed"
        ),
        "positive_cyclic4_controls": {
            "order36": check_positive(
                "order36",
                GRAPH36,
                FLOW36,
                SWITCH36,
                PROFILE36_BEFORE,
                PROFILE36_AFTER,
            ),
            "order60": check_positive(
                "order60",
                GRAPH60,
                FLOW60,
                SWITCH60,
                PROFILE60_BEFORE,
                PROFILE60_AFTER,
            ),
        },
        "negative_unrestricted_control": check_negative_order40(),
        "negative_cyclic4_girth5_control": (
            check_negative_reduced_order40()
        ),
        "negative_strict_snark_control": (
            check_negative_strict_order26()
        ),
        "conclusion": (
            "Direct one-switch domination is false even for simple "
            "cyclically 4-edge-connected non-Tait cubic graphs of "
            "girth five. The retained strict order-26 graph has an "
            "explicit FiveCDC, so this closes only the radius-one "
            "auxiliary route."
        ),
        "solver_independent": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
