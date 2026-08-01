#!/usr/bin/env python3
"""Small standard-library checker for the prescribed-root matching lemma.

The universal deficiency theorem is proved in the companion memo.  This
program checks the finite claims around the sharp 10-vertex limitation:

* graph6 and the literal edge table agree;
* the graph is simple, cubic, and 3-edge-connected;
* it has a displayed nontrivial cyclic 3-edge-cut and a Tait colouring;
* for roots 2 and 5, H=G-U has exactly four maximum matchings;
* every one gives a loop-link-loop suppressed core, never a theta core;
* the complete canonical connected cubic graph6 lists at orders 4, 6, and
  8 contain no smaller 3-edge-connected obstruction.

The three short lower-order lists are the output of:

    geng -cq -d3 -D3 4
    geng -cq -d3 -D3 6
    geng -cq -d3 -D3 8
"""

from __future__ import annotations

from functools import lru_cache
import json


GRAPH6 = "I?BeeOwM?"
ORDER = 10
EDGES = (
    (0, 5),
    (1, 5),
    (2, 5),
    (0, 6),
    (1, 6),
    (3, 6),
    (0, 7),
    (1, 7),
    (4, 7),
    (2, 8),
    (3, 8),
    (4, 8),
    (2, 9),
    (3, 9),
    (4, 9),
)
ROOTS = (2, 5)
CYCLIC_THREE_SHORE = {0, 1, 5, 6, 7}
CYCLIC_THREE_CUT = {2, 5, 8}
TAIT_CLASSES = (
    {0, 5, 7, 9, 14},
    {1, 3, 8, 10, 12},
    {2, 4, 6, 11, 13},
)

# Complete canonical connected simple cubic graph6 rows at smaller even
# orders.  At order 8 one of the five rows is not 3-edge-connected; the
# checker filters rather than silently deleting it.
SMALL_CONNECTED_CUBIC = {
    4: ("C~",),
    6: ("EFz_", "EUxo"),
    8: ("G?zTb_", "GCrb`o", "GCZJd_", "GCXmd_", "GCY^B_"),
}


def parse_graph6(text: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    if not text or ord(text[0]) >= 126:
        raise AssertionError("expected short graph6")
    order = ord(text[0]) - 63
    bits: list[int] = []
    for character in text[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise AssertionError("bad graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                edges.append((low, high))
            cursor += 1
    return order, tuple(edges)


def incidences(
    order: int, edges: tuple[tuple[int, int], ...]
) -> list[list[int]]:
    rows: list[list[int]] = [[] for _ in range(order)]
    for edge, (u, v) in enumerate(edges):
        rows[u].append(edge)
        rows[v].append(edge)
    return rows


def cut_edges(
    shore: set[int], edges: tuple[tuple[int, int], ...]
) -> set[int]:
    return {
        edge
        for edge, (u, v) in enumerate(edges)
        if (u in shore) != (v in shore)
    }


def edge_connectivity(
    order: int, edges: tuple[tuple[int, int], ...]
) -> int:
    """Brute force one representative of every nontrivial cut."""
    answer = len(edges)
    # Fix the last vertex outside the shore.
    for shore_mask in range(1, 1 << (order - 1)):
        size = 0
        for u, v in edges:
            size += ((shore_mask >> u) & 1) ^ ((shore_mask >> v) & 1)
        answer = min(answer, size)
    return answer


def maximum_matchings(
    vertices: set[int],
    edges: tuple[tuple[int, int], ...],
) -> tuple[int, list[tuple[int, ...]]]:
    rows: dict[int, list[tuple[int, int]]] = {
        vertex: [] for vertex in vertices
    }
    for edge, (u, v) in enumerate(edges):
        if u in vertices and v in vertices:
            rows[u].append((edge, v))
            rows[v].append((edge, u))

    @lru_cache(maxsize=None)
    def optimum(state: tuple[int, ...]) -> int:
        unmatched = set(state)
        if not unmatched:
            return 0
        vertex = min(unmatched)
        best = optimum(tuple(sorted(unmatched - {vertex})))
        for _, neighbour in rows[vertex]:
            if neighbour in unmatched:
                best = max(
                    best,
                    1
                    + optimum(
                        tuple(
                            sorted(unmatched - {vertex, neighbour})
                        )
                    ),
                )
        return best

    target = optimum(tuple(sorted(vertices)))
    answers: list[tuple[int, ...]] = []

    def visit(unmatched: set[int], chosen: tuple[int, ...]) -> None:
        if not unmatched:
            if len(chosen) == target:
                answers.append(chosen)
            return
        current = optimum(tuple(sorted(unmatched)))
        vertex = min(unmatched)
        without_vertex = unmatched - {vertex}
        if optimum(tuple(sorted(without_vertex))) == current:
            visit(without_vertex, chosen)
        for edge, neighbour in rows[vertex]:
            if neighbour not in unmatched:
                continue
            reduced = unmatched - {vertex, neighbour}
            if 1 + optimum(tuple(sorted(reduced))) == current:
                visit(reduced, chosen + (edge,))

    visit(set(vertices), ())
    return target, answers


def core_type(
    order: int,
    edges: tuple[tuple[int, int], ...],
    roots: tuple[int, int],
    near_matching: tuple[int, ...],
) -> dict[str, object]:
    zero_matching = set(roots) | set(near_matching)
    complement = [
        (edge, u, v)
        for edge, (u, v) in enumerate(edges)
        if edge not in zero_matching
    ]
    degrees = [0] * order
    for _, u, v in complement:
        degrees[u] += 1
        degrees[v] += 1
    branch_vertices = [
        vertex for vertex, degree in enumerate(degrees) if degree == 3
    ]
    if len(branch_vertices) != 2:
        raise AssertionError("near-perfect complement lacks two branches")
    first, second = branch_vertices

    internal_vertices = set(range(order)) - {first, second}
    rows: dict[int, list[int]] = {
        vertex: [] for vertex in internal_vertices
    }
    for _, u, v in complement:
        if u in internal_vertices and v in internal_vertices:
            rows[u].append(v)
            rows[v].append(u)

    pieces: list[dict[str, object]] = []
    unseen = set(internal_vertices)
    cross_strands = sum(
        1 for _, u, v in complement if {u, v} == {first, second}
    )
    first_loops = 0
    second_loops = 0
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        todo = [root]
        while todo:
            vertex = todo.pop()
            for neighbour in rows[vertex]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    component.add(neighbour)
                    todo.append(neighbour)
        at_first = sum(
            1
            for _, u, v in complement
            if (u in component and v == first)
            or (v in component and u == first)
        )
        at_second = sum(
            1
            for _, u, v in complement
            if (u in component and v == second)
            or (v in component and u == second)
        )
        if at_first == 1 and at_second == 1:
            cross_strands += 1
        elif at_first == 2 and at_second == 0:
            first_loops += 1
        elif at_first == 0 and at_second == 2:
            second_loops += 1
        pieces.append(
            {
                "vertices": sorted(component),
                "first_attachments": at_first,
                "second_attachments": at_second,
            }
        )

    if (cross_strands, first_loops, second_loops) == (3, 0, 0):
        classification = "theta"
    elif (cross_strands, first_loops, second_loops) == (1, 1, 1):
        classification = "loop-link-loop"
    else:
        raise AssertionError("unexpected two-branch suppressed core")
    return {
        "classification": classification,
        "branch_vertices": branch_vertices,
        "cross_strands": cross_strands,
        "first_loops": first_loops,
        "second_loops": second_loops,
        "pieces": pieces,
    }


def root_pair_property(
    order: int,
    edges: tuple[tuple[int, int], ...],
    roots: tuple[int, int],
) -> bool:
    if set(edges[roots[0]]) & set(edges[roots[1]]):
        raise AssertionError("roots are not independent")
    root_vertices = {
        vertex for edge in roots for vertex in edges[edge]
    }
    remaining = set(range(order)) - root_vertices
    optimum, matchings = maximum_matchings(remaining, edges)
    deficiency = len(remaining) - 2 * optimum
    if deficiency == 0:
        return True
    if deficiency != 2:
        return False
    return any(
        core_type(order, edges, roots, matching)["classification"]
        == "theta"
        for matching in matchings
    )


def check_tait_colouring() -> None:
    union = set().union(*TAIT_CLASSES)
    if union != set(range(len(EDGES))):
        raise AssertionError("Tait classes do not cover the edges")
    if sum(len(item) for item in TAIT_CLASSES) != len(EDGES):
        raise AssertionError("Tait classes overlap")
    rows = incidences(ORDER, EDGES)
    for vertex, row in enumerate(rows):
        colours = [
            colour
            for colour, edge_class in enumerate(TAIT_CLASSES)
            for edge in row
            if edge in edge_class
        ]
        if sorted(colours) != [0, 1, 2]:
            raise AssertionError(f"Tait condition fails at {vertex}")


def check_smaller_orders() -> dict[str, object]:
    result: dict[str, object] = {}
    for order, graph6_rows in SMALL_CONNECTED_CUBIC.items():
        retained = 0
        root_pairs = 0
        for graph6 in graph6_rows:
            decoded_order, edges = parse_graph6(graph6)
            if decoded_order != order:
                raise AssertionError("small graph order changed")
            rows = incidences(order, edges)
            if any(len(row) != 3 for row in rows):
                raise AssertionError("small graph is not cubic")
            if edge_connectivity(order, edges) < 3:
                continue
            retained += 1
            for first in range(len(edges)):
                for second in range(first + 1, len(edges)):
                    if set(edges[first]) & set(edges[second]):
                        continue
                    root_pairs += 1
                    if not root_pair_property(
                        order, edges, (first, second)
                    ):
                        raise AssertionError(
                            "smaller 3-edge-connected obstruction found"
                        )
        result[str(order)] = {
            "canonical_connected_cubic_graphs": len(graph6_rows),
            "three_edge_connected_graphs": retained,
            "independent_root_pairs_checked": root_pairs,
        }
    return result


def main() -> None:
    decoded_order, decoded_edges = parse_graph6(GRAPH6)
    if decoded_order != ORDER or decoded_edges != EDGES:
        raise AssertionError("graph6 and edge table differ")
    if len(set(EDGES)) != len(EDGES) or any(u == v for u, v in EDGES):
        raise AssertionError("countermodel is not simple")
    if any(len(row) != 3 for row in incidences(ORDER, EDGES)):
        raise AssertionError("countermodel is not cubic")
    if edge_connectivity(ORDER, EDGES) != 3:
        raise AssertionError("countermodel is not 3-edge-connected")
    if cut_edges(CYCLIC_THREE_SHORE, EDGES) != CYCLIC_THREE_CUT:
        raise AssertionError("displayed cyclic 3-cut changed")
    check_tait_colouring()

    root_vertices = {
        vertex for edge in ROOTS for vertex in EDGES[edge]
    }
    if len(root_vertices) != 4:
        raise AssertionError("roots are not independent")
    remaining = set(range(ORDER)) - root_vertices
    optimum, matchings = maximum_matchings(remaining, EDGES)
    if optimum != 2 or len(matchings) != 4:
        raise AssertionError("near-perfect matching list changed")
    expected_matchings = {
        (6, 11),
        (6, 14),
        (7, 11),
        (7, 14),
    }
    if set(matchings) != expected_matchings:
        raise AssertionError("literal maximum matchings changed")

    core_rows = [
        {
            "matching": list(matching),
            **core_type(ORDER, EDGES, ROOTS, matching),
        }
        for matching in matchings
    ]
    if any(row["classification"] != "loop-link-loop" for row in core_rows):
        raise AssertionError("a theta maximum unexpectedly exists")

    result = {
        "classification": "PASS",
        "graph6": GRAPH6,
        "order": ORDER,
        "size": len(EDGES),
        "simple_cubic": True,
        "edge_connectivity": 3,
        "cyclically_four_edge_connected": False,
        "cyclic_three_shore": sorted(CYCLIC_THREE_SHORE),
        "cyclic_three_cut": sorted(CYCLIC_THREE_CUT),
        "tait_colourable": True,
        "root_edges": list(ROOTS),
        "root_vertices": sorted(root_vertices),
        "remaining_vertices": sorted(remaining),
        "maximum_matching_size": optimum,
        "matching_deficiency": len(remaining) - 2 * optimum,
        "maximum_matching_count": len(matchings),
        "maximum_matching_cores": core_rows,
        "smaller_order_check": check_smaller_orders(),
        "scope_warning": (
            "This is a sharp obstruction to the 3-edge-connected "
            "strengthening.  It is Tait-colourable and has a cyclic "
            "3-edge-cut, so it is not a counterexample in the focused "
            "cyclically-four non-Tait domain."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
