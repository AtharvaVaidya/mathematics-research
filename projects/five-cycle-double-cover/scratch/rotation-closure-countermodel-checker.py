#!/usr/bin/env python3
"""Exact checker for the boundary-eight rotation-closure countermodels.

The universal focused statement is not asserted here.  This checker:

* verifies the literal 18-vertex graph and rooted obstruction;
* reconstructs its Gallai--Edmonds decomposition from all maximum
  matchings of H;
* checks all elementary maximum-matching rotations/cycle switches;
* verifies the two K_{2,3} contractions to the Petersen graph;
* independently checks non-Taitness by all perfect matchings; and
* checks order-minimality inside the retained complete non-Tait corpora
  at orders 10, 12, 14, and 16.

Only the Python standard library is used.
"""

from __future__ import annotations

from collections import Counter, deque
from functools import lru_cache
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GRAPH6 = "Q???C@?GF?CKSOF?AQ?W_B_AA_?"
ORDER = 18
EDGES = (
    (0, 7),
    (1, 8),
    (2, 9),
    (0, 10),
    (1, 10),
    (2, 10),
    (2, 11),
    (7, 11),
    (8, 11),
    (1, 12),
    (3, 12),
    (7, 12),
    (3, 13),
    (4, 13),
    (5, 13),
    (3, 14),
    (6, 14),
    (9, 14),
    (4, 15),
    (5, 15),
    (9, 15),
    (4, 16),
    (5, 16),
    (6, 16),
    (0, 17),
    (6, 17),
    (8, 17),
)
ROOT_EDGES = (12, 20)
ROOT_VERTICES = frozenset({3, 9, 13, 15})
H_VERTICES = frozenset(set(range(ORDER)) - ROOT_VERTICES)

FIRST_K23 = frozenset({4, 5, 13, 15, 16})
FIRST_CUT = frozenset({12, 20, 23})
SECOND_EXPANDED_SHORE = frozenset({3, 4, 5, 6, 9, 13, 14, 15, 16})
SECOND_CUT = frozenset({2, 10, 25})

CANONICAL_D = frozenset(
    {0, 1, 2, 4, 5, 7, 8, 10, 11, 12, 14, 17}
)
CANONICAL_A = frozenset({6, 16})
CANONICAL_C = frozenset()
BIG_D_COMPONENT = frozenset({0, 1, 2, 7, 8, 10, 11, 12, 17})

SMALL_CORPORA = {
    10: (
        ROOT
        / "search/order22-prelaunch-validation-20260725/controls/"
        "hard-order10.g6",
        "a6cff1c7754501629b55cab98200a0bead74be2ed37918c76e45cb2f2a560d1c",
        1,
        1,
        75,
    ),
    12: (
        ROOT
        / "search/order22-prelaunch-validation-20260725/controls/"
        "hard-order12.g6",
        "d17cceb075a174f69b65ce024350dd1d6d14bea0f4022aac3b39d2ff3c8856fa",
        1,
        1,
        117,
    ),
    14: (
        ROOT
        / "search/order22-prelaunch-validation-20260725/controls/"
        "hard-order14.g6",
        "1dbf6a326032b8ea59e5b4ccf4d2fb4e6a59a6b36223710afdc7be0149cf6e97",
        5,
        4,
        672,
    ),
    16: (
        ROOT
        / "search/order22-prelaunch-validation-20260725/controls/"
        "hard-order16.g6",
        "c05b3f5b94ee84a245077d5b1372a837512939471d2cc81e7dc7ed5296bbad6a",
        26,
        18,
        4104,
    ),
}


def parse_graph6(text: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    if not text or ord(text[0]) >= 126:
        raise AssertionError("expected short graph6")
    order = ord(text[0]) - 63
    bits: list[int] = []
    for character in text[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise AssertionError("invalid graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                edges.append((low, high))
            cursor += 1
    return order, tuple(edges)


def adjacency(
    order: int, edges: tuple[tuple[int, int], ...]
) -> list[list[tuple[int, int]]]:
    rows: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge, (u, v) in enumerate(edges):
        rows[u].append((v, edge))
        rows[v].append((u, edge))
    return rows


def cut_edges(
    shore: set[int] | frozenset[int],
    edges: tuple[tuple[int, int], ...],
) -> frozenset[int]:
    return frozenset(
        edge
        for edge, (u, v) in enumerate(edges)
        if (u in shore) != (v in shore)
    )


def connected_without(
    order: int,
    rows: list[list[tuple[int, int]]],
    deleted: frozenset[int],
) -> bool:
    seen = {0}
    todo = [0]
    while todo:
        vertex = todo.pop()
        for neighbour, edge in rows[vertex]:
            if edge in deleted or neighbour in seen:
                continue
            seen.add(neighbour)
            todo.append(neighbour)
    return len(seen) == order


def at_least_three_edge_connected(
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> bool:
    rows = adjacency(order, edges)
    for first in range(len(edges)):
        if not connected_without(order, rows, frozenset({first})):
            return False
        for second in range(first + 1, len(edges)):
            if not connected_without(
                order, rows, frozenset({first, second})
            ):
                return False
    return True


def induced_has_cycle(
    shore: set[int] | frozenset[int],
    edges: tuple[tuple[int, int], ...],
) -> bool:
    parent = {vertex: vertex for vertex in shore}

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for u, v in edges:
        if u not in shore or v not in shore:
            continue
        first = find(u)
        second = find(v)
        if first == second:
            return True
        parent[first] = second
    return False


def maximum_matchings(
    vertices: set[int] | frozenset[int],
    edges: tuple[tuple[int, int], ...],
) -> tuple[int, tuple[tuple[int, ...], ...]]:
    allowed = frozenset(vertices)
    rows: dict[int, list[tuple[int, int]]] = {
        vertex: [] for vertex in allowed
    }
    for edge, (u, v) in enumerate(edges):
        if u in allowed and v in allowed:
            rows[u].append((edge, v))
            rows[v].append((edge, u))

    @lru_cache(maxsize=None)
    def optimum(state: frozenset[int]) -> int:
        if not state:
            return 0
        vertex = min(state)
        without = state - {vertex}
        best = optimum(without)
        for _, neighbour in rows[vertex]:
            if neighbour in state:
                best = max(
                    best, 1 + optimum(without - {neighbour})
                )
        return best

    target = optimum(allowed)
    answers: list[tuple[int, ...]] = []

    def visit(state: frozenset[int], chosen: tuple[int, ...]) -> None:
        if not state:
            if len(chosen) == target:
                answers.append(tuple(sorted(chosen)))
            return
        current = optimum(state)
        vertex = min(state)
        without = state - {vertex}
        if optimum(without) == current:
            visit(without, chosen)
        for edge, neighbour in rows[vertex]:
            if neighbour not in state:
                continue
            reduced = without - {neighbour}
            if 1 + optimum(reduced) == current:
                visit(reduced, chosen + (edge,))

    visit(allowed, ())
    unique = tuple(sorted(set(answers)))
    return target, unique


def complement_components(
    order: int,
    edges: tuple[tuple[int, int], ...],
    deleted: frozenset[int],
) -> tuple[frozenset[int], ...]:
    rows = adjacency(order, edges)
    unseen = set(range(order))
    answer: list[frozenset[int]] = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        todo = [root]
        while todo:
            vertex = todo.pop()
            for neighbour, edge in rows[vertex]:
                if edge in deleted or neighbour not in unseen:
                    continue
                unseen.remove(neighbour)
                component.add(neighbour)
                todo.append(neighbour)
        answer.append(frozenset(component))
    return tuple(answer)


def bridges_of_complement(
    order: int,
    edges: tuple[tuple[int, int], ...],
    deleted: frozenset[int],
) -> tuple[int, ...]:
    rows = adjacency(order, edges)
    bridges: list[int] = []
    for edge, (u, v) in enumerate(edges):
        if edge in deleted:
            continue
        seen = {u}
        todo = [u]
        while todo:
            vertex = todo.pop()
            for neighbour, candidate in rows[vertex]:
                if (
                    candidate in deleted
                    or candidate == edge
                    or neighbour in seen
                ):
                    continue
                seen.add(neighbour)
                todo.append(neighbour)
        if v not in seen:
            bridges.append(edge)
    return tuple(bridges)


def root_pair_is_perfect_or_theta(
    order: int,
    edges: tuple[tuple[int, int], ...],
    roots: tuple[int, int],
) -> bool:
    root_vertices = frozenset(
        vertex for edge in roots for vertex in edges[edge]
    )
    if len(root_vertices) != 4:
        raise AssertionError("root pair is not independent")
    h_vertices = frozenset(set(range(order)) - root_vertices)
    optimum, matchings = maximum_matchings(h_vertices, edges)
    deficiency = len(h_vertices) - 2 * optimum
    if deficiency == 0:
        return True
    if deficiency != 2:
        return False
    for matching in matchings:
        deleted = frozenset(roots + matching)
        if not bridges_of_complement(order, edges, deleted):
            return True
    return False


def is_tait_colourable(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[bool, int, Counter[tuple[int, ...]]]:
    optimum, perfect_matchings = maximum_matchings(
        frozenset(range(order)), edges
    )
    if optimum * 2 != order:
        return False, 0, Counter()
    profiles: Counter[tuple[int, ...]] = Counter()
    for matching in perfect_matchings:
        components = complement_components(
            order, edges, frozenset(matching)
        )
        profile = tuple(sorted(len(component) for component in components))
        profiles[profile] += 1
        if all(size % 2 == 0 for size in profile):
            return True, len(perfect_matchings), profiles
    return False, len(perfect_matchings), profiles


def graph_components_on_vertices(
    vertices: set[int] | frozenset[int],
    edges: tuple[tuple[int, int], ...],
) -> tuple[frozenset[int], ...]:
    allowed = set(vertices)
    rows = adjacency(max(max(edge) for edge in edges) + 1, edges)
    answer: list[frozenset[int]] = []
    while allowed:
        root = min(allowed)
        allowed.remove(root)
        component = {root}
        todo = [root]
        while todo:
            vertex = todo.pop()
            for neighbour, _ in rows[vertex]:
                if neighbour in allowed:
                    allowed.remove(neighbour)
                    component.add(neighbour)
                    todo.append(neighbour)
        answer.append(frozenset(component))
    return tuple(answer)


def gallai_edmonds(
    h_vertices: frozenset[int],
    edges: tuple[tuple[int, int], ...],
    matchings: tuple[tuple[int, ...], ...],
) -> tuple[
    frozenset[int],
    frozenset[int],
    frozenset[int],
    tuple[frozenset[int], ...],
]:
    exposed_somewhere: set[int] = set()
    for matching in matchings:
        covered = {
            vertex for edge in matching for vertex in edges[edge]
        }
        exposed_somewhere.update(h_vertices - covered)
    d_set = frozenset(exposed_somewhere)
    rows = adjacency(max(max(edge) for edge in edges) + 1, edges)
    a_set = frozenset(
        neighbour
        for vertex in d_set
        for neighbour, _ in rows[vertex]
        if neighbour in h_vertices and neighbour not in d_set
    )
    c_set = h_vertices - d_set - a_set
    components = tuple(
        sorted(
            graph_components_on_vertices(d_set, edges),
            key=lambda component: (min(component), len(component)),
        )
    )
    return d_set, a_set, c_set, components


def tight_barriers(
    h_vertices: frozenset[int],
    edges: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], ...]:
    ordered = sorted(h_vertices)
    answer: list[tuple[int, ...]] = []
    for mask in range(1 << len(ordered)):
        barrier = frozenset(
            ordered[index]
            for index in range(len(ordered))
            if (mask >> index) & 1
        )
        components = graph_components_on_vertices(
            h_vertices - barrier, edges
        )
        odd = sum(len(component) % 2 for component in components)
        if odd == len(barrier) + 2:
            answer.append(tuple(sorted(barrier)))
    return tuple(answer)


def elementary_exchange_graph(
    matchings: tuple[tuple[int, ...], ...],
    edges: tuple[tuple[int, int], ...],
    beta: tuple[int, ...],
) -> dict[str, object]:
    rows: list[list[int]] = [[] for _ in matchings]
    kinds: Counter[str] = Counter()
    lengths: Counter[tuple[str, int]] = Counter()
    transitions: Counter[tuple[int, int]] = Counter()
    for first, matching in enumerate(matchings):
        for second in range(first + 1, len(matchings)):
            difference = set(matching) ^ set(matchings[second])
            incident = {
                vertex for edge in difference for vertex in edges[edge]
            }
            local = {vertex: [] for vertex in incident}
            for edge in difference:
                u, v = edges[edge]
                local[u].append(v)
                local[v].append(u)
            seen = {min(incident)}
            todo = list(seen)
            while todo:
                vertex = todo.pop()
                for neighbour in local[vertex]:
                    if neighbour not in seen:
                        seen.add(neighbour)
                        todo.append(neighbour)
            if seen != incident:
                continue
            degrees = Counter(len(local[vertex]) for vertex in incident)
            if degrees[1] == 2 and degrees[2] == len(incident) - 2:
                kind = "path"
            elif degrees[2] == len(incident):
                kind = "cycle"
            else:
                raise AssertionError("bad matching symmetric difference")
            if len(difference) % 2:
                raise AssertionError("elementary exchange is not even")
            rows[first].append(second)
            rows[second].append(first)
            kinds[kind] += 1
            lengths[(kind, len(difference))] += 1
            transitions[tuple(sorted((beta[first], beta[second])))] += 1

    seen = {0}
    todo = [0]
    while todo:
        vertex = todo.pop()
        for neighbour in rows[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                todo.append(neighbour)
    if len(seen) != len(matchings):
        raise AssertionError("elementary exchange graph is disconnected")
    return {
        "vertices": len(matchings),
        "edges": sum(len(row) for row in rows) // 2,
        "connected": True,
        "kind_counts": dict(sorted(kinds.items())),
        "length_counts": {
            f"{kind}_{length}": count
            for (kind, length), count in sorted(lengths.items())
        },
        "degree_distribution": {
            str(degree): count
            for degree, count in sorted(Counter(map(len, rows)).items())
        },
        "beta_transition_counts": {
            f"{first}_{second}": count
            for (first, second), count in sorted(transitions.items())
        },
    }


def contract_k23(
    edges: tuple[tuple[int, int], ...],
    shore: frozenset[int],
    new_vertex: int,
) -> tuple[tuple[int, int], ...]:
    internal = [
        (u, v) for u, v in edges if u in shore and v in shore
    ]
    if len(shore) != 5 or len(internal) != 6:
        raise AssertionError("contracted shore is not K2,3-sized")
    boundary = cut_edges(shore, edges)
    if len(boundary) != 3:
        raise AssertionError("K2,3 shore does not have three ports")
    result: list[tuple[int, int]] = []
    for u, v in edges:
        if u in shore and v in shore:
            continue
        first = new_vertex if u in shore else u
        second = new_vertex if v in shore else v
        result.append(tuple(sorted((first, second))))
    if len(set(result)) != len(result):
        raise AssertionError("contraction made parallel edges")
    return tuple(sorted(result))


def check_petersen_quotient(
    edges: tuple[tuple[int, int], ...]
) -> dict[str, object]:
    first = contract_k23(edges, FIRST_K23, 18)
    second_shore = frozenset({3, 6, 9, 14, 18})
    quotient = contract_k23(first, second_shore, 19)
    petersen_edges = frozenset(
        {
            (0, 7),
            (1, 8),
            (2, 19),
            (0, 10),
            (1, 10),
            (2, 10),
            (2, 11),
            (7, 11),
            (8, 11),
            (1, 12),
            (12, 19),
            (7, 12),
            (0, 17),
            (17, 19),
            (8, 17),
        }
    )
    if frozenset(quotient) != petersen_edges:
        raise AssertionError("two contractions did not give Petersen")
    quotient_order = len(
        {vertex for edge in quotient for vertex in edge}
    )
    # The quotient has sparse labels, so is_tait_colourable cannot be
    # called directly with quotient_order.  Relabel it first.
    labels = sorted({vertex for edge in quotient for vertex in edge})
    relabel = {vertex: index for index, vertex in enumerate(labels)}
    compact = tuple(
        sorted((relabel[u], relabel[v]) for u, v in quotient)
    )
    tait, perfect_count, profiles = is_tait_colourable(
        quotient_order, compact
    )
    if tait or perfect_count != 6 or profiles != Counter({(5, 5): 6}):
        raise AssertionError("quotient is not the checked Petersen graph")
    return {
        "first_contraction_order": 14,
        "second_contraction_order": 10,
        "petersen_perfect_matchings": perfect_count,
        "petersen_two_factor_profiles": {
            "5_5": profiles[(5, 5)]
        },
    }


def check_lower_orders() -> dict[str, object]:
    answer: dict[str, object] = {}
    for order, (
        path,
        expected_hash,
        expected_rows,
        expected_three_connected,
        expected_pairs,
    ) in SMALL_CORPORA.items():
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected_hash:
            raise AssertionError(f"order-{order} corpus hash changed")
        graph6_rows = data.decode("ascii").splitlines()
        if len(graph6_rows) != expected_rows:
            raise AssertionError(f"order-{order} row count changed")
        retained = 0
        root_pairs = 0
        obstructions = 0
        for graph6 in graph6_rows:
            parsed_order, edges = parse_graph6(graph6)
            if parsed_order != order:
                raise AssertionError("lower-order graph order changed")
            rows = adjacency(order, edges)
            if (
                len(set(edges)) != len(edges)
                or any(u == v for u, v in edges)
                or any(len(row) != 3 for row in rows)
            ):
                raise AssertionError("lower-order row is not simple cubic")
            tait, _, _ = is_tait_colourable(order, edges)
            if tait:
                raise AssertionError("retained hard row is Tait")
            if not at_least_three_edge_connected(order, edges):
                continue
            retained += 1
            for first, (a, b) in enumerate(edges):
                for second in range(first + 1, len(edges)):
                    c, d = edges[second]
                    if len({a, b, c, d}) != 4:
                        continue
                    root_pairs += 1
                    if not root_pair_is_perfect_or_theta(
                        order, edges, (first, second)
                    ):
                        obstructions += 1
        if (
            retained != expected_three_connected
            or root_pairs != expected_pairs
            or obstructions
        ):
            raise AssertionError(f"order-{order} minimality count changed")
        answer[str(order)] = {
            "corpus_sha256": expected_hash,
            "retained_non_tait_graphs": expected_rows,
            "three_edge_connected_graphs": retained,
            "independent_root_pairs_checked": root_pairs,
            "all_dumbbell_pairs": obstructions,
        }
    return answer


def main() -> None:
    parsed_order, parsed_edges = parse_graph6(GRAPH6)
    if parsed_order != ORDER or parsed_edges != EDGES:
        raise AssertionError("literal graph6 and edge table disagree")
    rows = adjacency(ORDER, EDGES)
    if (
        len(set(EDGES)) != len(EDGES)
        or any(u == v for u, v in EDGES)
        or any(len(row) != 3 for row in rows)
    ):
        raise AssertionError("candidate is not simple cubic")
    if not at_least_three_edge_connected(ORDER, EDGES):
        raise AssertionError("candidate is not 3-edge-connected")
    if cut_edges(FIRST_K23, EDGES) != FIRST_CUT:
        raise AssertionError("first cyclic 3-cut changed")
    if cut_edges(SECOND_EXPANDED_SHORE, EDGES) != SECOND_CUT:
        raise AssertionError("second cyclic 3-cut changed")
    complement = set(range(ORDER)) - set(FIRST_K23)
    if not (
        induced_has_cycle(FIRST_K23, EDGES)
        and induced_has_cycle(complement, EDGES)
    ):
        raise AssertionError("displayed 3-cut is not cyclic")
    second_complement = (
        set(range(ORDER)) - set(SECOND_EXPANDED_SHORE)
    )
    if not (
        induced_has_cycle(SECOND_EXPANDED_SHORE, EDGES)
        and induced_has_cycle(second_complement, EDGES)
    ):
        raise AssertionError("second displayed 3-cut is not cyclic")

    if cut_edges(ROOT_VERTICES, EDGES) != frozenset(
        {2, 10, 13, 14, 15, 17, 18, 19}
    ):
        raise AssertionError("root boundary is not the frozen boundary 8")

    tait, perfect_count, two_factor_profiles = is_tait_colourable(
        ORDER, EDGES
    )
    if (
        tait
        or perfect_count != 24
        or two_factor_profiles != Counter({(5, 13): 24})
    ):
        raise AssertionError("candidate non-Tait certificate changed")

    optimum, matchings = maximum_matchings(H_VERTICES, EDGES)
    if optimum != 6 or len(matchings) != 40:
        raise AssertionError("rooted maximum-matching space changed")
    beta = tuple(
        len(
            bridges_of_complement(
                ORDER,
                EDGES,
                frozenset(ROOT_EDGES + matching),
            )
        )
        for matching in matchings
    )
    beta_distribution = Counter(beta)
    if beta_distribution != Counter({3: 8, 4: 8, 5: 8, 8: 8, 10: 8}):
        raise AssertionError("beta distribution changed")
    if min(beta) != 3:
        raise AssertionError("candidate gained a theta matching")

    d_set, a_set, c_set, d_components = gallai_edmonds(
        H_VERTICES, EDGES, matchings
    )
    if (
        d_set != CANONICAL_D
        or a_set != CANONICAL_A
        or c_set != CANONICAL_C
        or set(d_components)
        != {
            BIG_D_COMPONENT,
            frozenset({4}),
            frozenset({5}),
            frozenset({14}),
        }
    ):
        raise AssertionError("Gallai-Edmonds decomposition changed")
    for component in d_components:
        for removed in component:
            size, _ = maximum_matchings(component - {removed}, EDGES)
            if size * 2 != len(component) - 1:
                raise AssertionError("D component is not factor-critical")
    component_profile = sorted(
        (len(component), len(cut_edges(component, EDGES)))
        for component in d_components
    )
    if component_profile != [(1, 3), (1, 3), (1, 3), (9, 3)]:
        raise AssertionError("canonical barrier profile changed")
    if tight_barriers(H_VERTICES, EDGES) != ((6,), (16,), (6, 16)):
        raise AssertionError("tight barrier list changed")

    exchange = elementary_exchange_graph(matchings, EDGES, beta)
    expected_exchange = {
        "vertices": 40,
        "edges": 384,
        "connected": True,
        "kind_counts": {"cycle": 20, "path": 364},
        "length_counts": {
            "cycle_6": 12,
            "cycle_8": 8,
            "path_2": 72,
            "path_4": 92,
            "path_6": 100,
            "path_8": 84,
            "path_10": 16,
        },
        "degree_distribution": {"19": 32, "20": 8},
        "beta_transition_counts": {
            "3_3": 12,
            "3_4": 32,
            "3_5": 32,
            "3_8": 32,
            "3_10": 32,
            "4_4": 12,
            "4_5": 32,
            "4_8": 32,
            "4_10": 32,
            "5_5": 12,
            "5_8": 32,
            "5_10": 32,
            "8_8": 12,
            "8_10": 32,
            "10_10": 16,
        },
    }
    if exchange != expected_exchange:
        raise AssertionError("elementary exchange graph changed")

    result = {
        "classification": "PASS",
        "scope_warning": (
            "This is not a counterexample in the cyclically-four focused "
            "domain. It shows that boundary eight, local barrier counts, "
            "3-edge-connectivity, and even non-Taitness do not replace "
            "global cyclic four-edge-connectivity."
        ),
        "graph6": GRAPH6,
        "order": ORDER,
        "size": len(EDGES),
        "root_edges": list(ROOT_EDGES),
        "root_vertices": sorted(ROOT_VERTICES),
        "root_boundary": 8,
        "simple_cubic": True,
        "edge_connectivity": 3,
        "cyclically_four_edge_connected": False,
        "cyclic_three_cuts": [
            {
                "shore": sorted(FIRST_K23),
                "edges": sorted(FIRST_CUT),
            },
            {
                "shore": sorted(SECOND_EXPANDED_SHORE),
                "edges": sorted(SECOND_CUT),
            },
        ],
        "tait_colourable": False,
        "perfect_matchings": perfect_count,
        "two_factor_profiles": {"5_13": 24},
        "matching_deficiency_of_H": len(H_VERTICES) - 2 * optimum,
        "maximum_matchings_of_H": len(matchings),
        "beta_minimum": min(beta),
        "beta_distribution": {
            str(value): count
            for value, count in sorted(beta_distribution.items())
        },
        "all_maximum_matchings_are_dumbbell": True,
        "gallai_edmonds": {
            "D": sorted(d_set),
            "A": sorted(a_set),
            "C": sorted(c_set),
            "D_component_size_boundary_profile": component_profile,
            "incidence_edges_A_to_D": [16, 21, 22, 25],
            "extra_A_edge": 23,
        },
        "tight_barriers": [list(item) for item in ((6,), (16,), (6, 16))],
        "elementary_exchange_graph": exchange,
        "petersen_contractions": check_petersen_quotient(EDGES),
        "lower_order_non_tait_minimality": check_lower_orders(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
