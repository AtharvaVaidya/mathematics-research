#!/usr/bin/env python3
"""Verify an abstract order-80 equality-case rotation countermodel.

The witness has:

* a connected 5-regular bipartite incidence multigraph on 8+8 vertices;
* eight distinguished incidence edges forming a perfect matching;
* cyclic orders and twist bits reconstructing a connected simple cubic
  80-vertex graph with a proper a/b/c edge-colouring;
* eight 10-cycles in each of the ac and bc factors, one mark per cycle; and
* no good selector among the exact 2^8 all-mark selector space.

The checker also solves the unrestricted two-edge-disjoint-T-join formula
after subdividing the marks.  That formula is SAT: the witness refutes only
the selector implication from equality incidence/rotation data, not packing
itself and not five-CDC.
"""

from __future__ import annotations

from collections import Counter, deque
import argparse
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

import networkx as nx


INCIDENCE = (
    (2, 0, 1, 2, 0, 0, 0, 0),
    (0, 1, 1, 0, 1, 2, 0, 0),
    (0, 2, 1, 0, 0, 0, 2, 0),
    (0, 0, 0, 2, 1, 0, 0, 2),
    (1, 0, 1, 0, 1, 0, 1, 1),
    (1, 0, 1, 0, 1, 2, 0, 0),
    (0, 2, 0, 0, 0, 0, 2, 1),
    (1, 0, 0, 1, 1, 1, 0, 1),
)

ROTATION_A = (
    (9, 0, 11, 8, 10),
    (15, 14, 1, 13, 12),
    (16, 17, 2, 19, 18),
    (22, 3, 21, 20, 23),
    (27, 25, 26, 4, 24),
    (5, 31, 30, 28, 29),
    (6, 32, 33, 34, 35),
    (7, 37, 38, 36, 39),
)

ROTATION_B = (
    (8, 24, 36, 28, 0),
    (32, 17, 16, 33, 1),
    (9, 25, 29, 12, 2),
    (3, 20, 10, 37, 11),
    (38, 13, 4, 30, 21),
    (14, 15, 39, 5, 31),
    (26, 19, 18, 34, 6),
    (23, 7, 22, 35, 27),
)

TWIST = tuple(map(int, "1110111111000001001100001111000111010001"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def incidence_edges() -> tuple[tuple[int, int], ...]:
    remaining = [list(row) for row in INCIDENCE]
    edges: list[tuple[int, int]] = []
    for index in range(8):
        require(remaining[index][index] > 0, "missing marked diagonal edge")
        edges.append((index, index))
        remaining[index][index] -= 1
    for a in range(8):
        for b in range(8):
            edges.extend((a, b) for _ in range(remaining[a][b]))
    require(len(edges) == 40, "bad incidence edge count")
    return tuple(edges)


def build_coloured_core():
    incidence = incidence_edges()
    core_edges: list[tuple[int, int]] = []
    colours: list[str] = []
    owners: list[int] = []

    for edge in range(40):
        core_edges.append((2 * edge, 2 * edge + 1))
        colours.append("c")
        owners.append(edge)
    for a, rotation in enumerate(ROTATION_A):
        for position, edge in enumerate(rotation):
            following = rotation[(position + 1) % 5]
            core_edges.append((2 * edge + 1, 2 * following))
            colours.append("a")
            owners.append(a)
    for b, rotation in enumerate(ROTATION_B):
        for position, edge in enumerate(rotation):
            following = rotation[(position + 1) % 5]
            core_edges.append(
                (
                    2 * edge + (1 - TWIST[edge]),
                    2 * following + TWIST[following],
                )
            )
            colours.append("b")
            owners.append(b)

    normalized = tuple(tuple(sorted(edge)) for edge in core_edges)
    return incidence, normalized, tuple(colours), tuple(owners)


def factor_components(
    graph: nx.Graph,
    edge_rows: tuple[tuple[int, int], ...],
    colours: tuple[str, ...],
    allowed: frozenset[str],
) -> tuple[frozenset[int], ...]:
    factor = nx.Graph()
    factor.add_nodes_from(graph.nodes)
    factor.add_edges_from(
        edge_rows[index]
        for index, colour in enumerate(colours)
        if colour in allowed
    )
    require(all(factor.degree(vertex) == 2 for vertex in factor), "bad factor")
    return tuple(
        sorted(
            (frozenset(component) for component in nx.connected_components(factor)),
            key=lambda row: tuple(sorted(row)),
        )
    )


def selector_profile(
    selector: int,
    incidence: tuple[tuple[int, int], ...],
    edge_rows: tuple[tuple[int, int], ...],
    colours: tuple[str, ...],
    owners: tuple[int, ...],
) -> tuple[int, ...]:
    selected: list[tuple[int, int, int]] = []
    for edge_id, ((u, v), colour, owner) in enumerate(
        zip(edge_rows, colours, owners)
    ):
        if colour == "a":
            take = (selector >> owner) & 1
        elif colour == "b":
            take = 1 - ((selector >> owner) & 1)
        else:
            a, b = incidence[owner]
            y_b = 1 - ((selector >> b) & 1)
            take = ((selector >> a) & 1) ^ y_b
        if take:
            selected.append((u, v, edge_id))

    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(80)]
    for u, v, edge_id in selected:
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))
    require(all(len(row) in (0, 2) for row in adjacency), "selector not Eulerian")

    seen: set[int] = set()
    profile: list[int] = []
    for root in range(80):
        if root in seen or not adjacency[root]:
            continue
        seen.add(root)
        stack = [root]
        twice_marks = 0
        while stack:
            vertex = stack.pop()
            for other, edge_id in adjacency[vertex]:
                if colours[edge_id] == "c" and owners[edge_id] < 8:
                    twice_marks += 1
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        marks = twice_marks // 2
        if marks:
            profile.append(marks)
    require(sum(profile) == 8, "selector lost a mark")
    return tuple(sorted(profile))


def forest_even_transversal(
    selector: int,
    incidence: tuple[tuple[int, int], ...],
) -> bool:
    """Test the rotation-independent forest/even-component sufficient condition."""
    chosen = {
        a for a in range(8) if (selector >> a) & 1
    } | {
        8 + b for b in range(8) if not ((selector >> b) & 1)
    }
    parent = list(range(16))
    size = [1] * 16

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for a, b in incidence:
        u, v = a, 8 + b
        if u not in chosen or v not in chosen:
            continue
        ru, rv = root(u), root(v)
        if ru == rv:
            return False
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
    return all(size[root(vertex)] % 2 == 0 for vertex in chosen)


def girth(graph: nx.Graph) -> int | None:
    best: int | None = None
    for root in graph:
        distance = {root: 0}
        parent = {root: None}
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for other in graph[vertex]:
                if other not in distance:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    length = distance[vertex] + distance[other] + 1
                    best = length if best is None else min(best, length)
    return best


def separation_conflict(
    graph: nx.Graph,
    edges: tuple[tuple[int, int], ...],
    colours: tuple[str, ...],
) -> dict | None:
    for allowed in (
        frozenset(("a", "b")),
        frozenset(("a", "c")),
        frozenset(("b", "c")),
    ):
        components = factor_components(graph, edges, colours, allowed)
        for component_index, component in enumerate(components):
            marks = [
                edge
                for edge in range(8)
                if colours[edge] in allowed
                and edges[edge][0] in component
                and edges[edge][1] in component
            ]
            if len(marks) > 1:
                return {
                    "colour_pair": "".join(sorted(allowed)),
                    "component_index": component_index,
                    "component_vertices": sorted(component),
                    "marked_edge_ids": marks,
                }
    return None


def separated_in_colouring(
    graph: nx.Graph,
    edges: tuple[tuple[int, int], ...],
    colours: tuple[str, ...],
) -> bool:
    return separation_conflict(graph, edges, colours) is None


def single_kempe_conflict(
    graph: nx.Graph,
    edges: tuple[tuple[int, int], ...],
    colours: tuple[str, ...],
) -> dict | None:
    for first, second in (("a", "b"), ("a", "c"), ("b", "c")):
        components = factor_components(
            graph, edges, colours, frozenset((first, second))
        )
        for component_index, component in enumerate(components):
            switched = list(colours)
            switched_edges = []
            for edge_id, (u, v) in enumerate(edges):
                if (
                    u in component
                    and v in component
                    and colours[edge_id] in (first, second)
                ):
                    switched[edge_id] = (
                        second if colours[edge_id] == first else first
                    )
                    switched_edges.append(edge_id)
            conflict = separation_conflict(graph, edges, tuple(switched))
            if conflict is not None:
                return {
                    "colour_pair": first + second,
                    "component_index": component_index,
                    "component_vertices": sorted(component),
                    "switched_edge_ids": switched_edges,
                    "result_separated": False,
                    "result_conflict": conflict,
                }
    return None


def subdivided_graph(
    edges: tuple[tuple[int, int], ...],
) -> tuple[int, tuple[tuple[int, int], ...], tuple[int, ...]]:
    expanded = list(edges[8:])
    terminals = []
    for mark in range(8):
        u, v = edges[mark]
        terminal = 80 + mark
        terminals.append(terminal)
        expanded.extend(((u, terminal), (v, terminal)))
    return 88, tuple(tuple(sorted(edge)) for edge in expanded), tuple(terminals)


def parity_clauses(variables: list[int], odd: bool) -> list[list[int]]:
    clauses: list[list[int]] = []
    for assignment in itertools.product((0, 1), repeat=len(variables)):
        if (sum(assignment) & 1) == int(odd):
            continue
        clauses.append(
            [
                -variable if value else variable
                for variable, value in zip(variables, assignment)
            ]
        )
    return clauses


def solve_two_t_joins(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    terminals: tuple[int, ...],
    cadical: str,
) -> dict:
    incidence: list[list[int]] = [[] for _ in range(vertices)]
    for edge_id, (u, v) in enumerate(edges):
        incidence[u].append(edge_id)
        incidence[v].append(edge_id)

    def variable(join: int, edge: int) -> int:
        return 1 + join * len(edges) + edge

    terminal_set = set(terminals)
    clauses: list[list[int]] = []
    for edge in range(len(edges)):
        clauses.append([-variable(0, edge), -variable(1, edge)])
    for join in (0, 1):
        for vertex in range(vertices):
            clauses.extend(
                parity_clauses(
                    [variable(join, edge) for edge in incidence[vertex]],
                    vertex in terminal_set,
                )
            )

    with tempfile.TemporaryDirectory(prefix="equality88-tjoins-") as temporary:
        cnf = Path(temporary) / "instance.cnf"
        with cnf.open("w", encoding="ascii") as stream:
            stream.write(f"p cnf {2 * len(edges)} {len(clauses)}\n")
            for clause in clauses:
                stream.write(" ".join(map(str, clause)) + " 0\n")
        completed = subprocess.run(
            [cadical, "-q", "--seed=0", str(cnf)],
            capture_output=True,
            text=True,
            check=False,
        )
    require(completed.returncode in (10, 20), "CaDiCaL failed")
    if completed.returncode == 20:
        return {
            "status": "UNSAT_UNCERTIFIED",
            "variables": 2 * len(edges),
            "clauses": len(clauses),
        }
    assignment: dict[int, bool] = {}
    for line in completed.stdout.splitlines():
        if not line.startswith("v "):
            continue
        for token in line.split()[1:]:
            literal = int(token)
            if literal:
                assignment[abs(literal)] = literal > 0
    joins = [
        [edge for edge in range(len(edges)) if assignment[variable(join, edge)]]
        for join in (0, 1)
    ]
    require(not (set(joins[0]) & set(joins[1])), "joins overlap")
    for join in joins:
        degrees = [0] * vertices
        for edge in join:
            u, v = edges[edge]
            degrees[u] ^= 1
            degrees[v] ^= 1
        require(
            {vertex for vertex, parity in enumerate(degrees) if parity}
            == terminal_set,
            "bad T-join boundary",
        )
    return {
        "status": "SAT_CHECKED",
        "variables": 2 * len(edges),
        "clauses": len(clauses),
        "join_edge_ids": joins,
        "join_sizes": [len(join) for join in joins],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("scratch/equality88-rotation-countermodel-result.json"),
    )
    parser.add_argument(
        "--cadical",
        default=shutil.which("cadical") or "/opt/homebrew/bin/cadical",
    )
    args = parser.parse_args()

    incidence, edges, colours, owners = build_coloured_core()
    require(all(sum(row) == 5 for row in INCIDENCE), "bad incidence row sum")
    require(
        all(sum(INCIDENCE[a][b] for a in range(8)) == 5 for b in range(8)),
        "bad incidence column sum",
    )
    gamma = nx.MultiGraph()
    gamma.add_nodes_from(range(16))
    gamma.add_edges_from((a, 8 + b, {"edge_id": edge}) for edge, (a, b) in enumerate(incidence))
    require(nx.is_connected(gamma), "incidence multigraph disconnected")
    require(all(gamma.degree(vertex) == 5 for vertex in gamma), "incidence not 5-regular")
    require(
        {incidence[edge] for edge in range(8)}
        == {(index, index) for index in range(8)},
        "marks are not a perfect matching",
    )

    for a, rotation in enumerate(ROTATION_A):
        require(
            sorted(rotation)
            == sorted(edge for edge, ends in enumerate(incidence) if ends[0] == a),
            f"bad A rotation {a}",
        )
    for b, rotation in enumerate(ROTATION_B):
        require(
            sorted(rotation)
            == sorted(edge for edge, ends in enumerate(incidence) if ends[1] == b),
            f"bad B rotation {b}",
        )
    require(len(TWIST) == 40, "bad twist length")

    require(len(edges) == 120 and len(set(edges)) == 120, "core is not simple")
    graph = nx.Graph()
    graph.add_nodes_from(range(80))
    graph.add_edges_from(edges)
    require(nx.is_connected(graph), "core disconnected")
    require(all(graph.degree(vertex) == 3 for vertex in graph), "core not cubic")
    for vertex in graph:
        incident_colours = {
            colours[edge_id]
            for edge_id, edge in enumerate(edges)
            if vertex in edge
        }
        require(incident_colours == {"a", "b", "c"}, "colouring not proper")

    ac = factor_components(graph, edges, colours, frozenset(("a", "c")))
    bc = factor_components(graph, edges, colours, frozenset(("b", "c")))
    require(len(ac) == len(bc) == 8, "factor count mismatch")
    require(all(len(component) == 10 for component in ac + bc), "factor length mismatch")
    for factor in (ac, bc):
        require(
            all(
                sum(
                    1
                    for mark in range(8)
                    if edges[mark][0] in component and edges[mark][1] in component
                )
                == 1
                for component in factor
            ),
            "factor does not have one mark per circuit",
        )

    profiles = Counter(
        selector_profile(selector, incidence, edges, colours, owners)
        for selector in range(256)
    )
    good_selectors = [
        selector
        for selector in range(256)
        if all(value % 2 == 0 for value in selector_profile(
            selector, incidence, edges, colours, owners
        ))
    ]
    require(not good_selectors, "countermodel has a good selector")
    forest_even_selectors = [
        selector
        for selector in range(256)
        if forest_even_transversal(selector, incidence)
    ]
    require(
        not forest_even_selectors,
        "incidence multigraph has a forest/even transversal",
    )

    expanded_n, expanded_edges, terminals = subdivided_graph(edges)
    expanded = nx.Graph()
    expanded.add_nodes_from(range(expanded_n))
    expanded.add_edges_from(expanded_edges)
    require(len(expanded_edges) == 128 and len(set(expanded_edges)) == 128, "bad subdivision")
    require(nx.is_connected(expanded), "subdivision disconnected")
    require(
        all(
            expanded.degree(vertex) == (2 if vertex in terminals else 3)
            for vertex in expanded
        ),
        "bad subdivided degrees",
    )
    packing = solve_two_t_joins(
        expanded_n, expanded_edges, terminals, args.cadical
    )
    require(packing["status"] == "SAT_CHECKED", "expected packing witness")

    conflict = single_kempe_conflict(graph, edges, colours)
    report = {
        "schema": "equality88-rotation-countermodel-v1",
        "classification": "ABSTRACT_SELECTOR_COUNTERMODEL_FULL_PACKING_SAT",
        "scope_warning": (
            "The equality incidence/rotation data do not force a good "
            "bichromatic selector. This witness nevertheless has two "
            "edge-disjoint T-joins, fails the inherited girth condition, "
            "and is not claimed universally separated. It is not a "
            "five-cycle-double-cover counterexample."
        ),
        "incidence": {
            "matrix": INCIDENCE,
            "edge_ends_by_id": incidence,
            "vertices_per_side": 8,
            "edges": 40,
            "regular_degree": 5,
            "connected": True,
            "parallel_edge_pairs": sum(
                max(0, INCIDENCE[a][b] - 1)
                for a in range(8)
                for b in range(8)
            ),
            "marked_edge_ids": list(range(8)),
            "marks_form_perfect_matching": True,
        },
        "rotation_system": {
            "rotation_a": ROTATION_A,
            "rotation_b": ROTATION_B,
            "twist_bits_by_incidence_edge": TWIST,
        },
        "core": {
            "vertices": 80,
            "edges": 120,
            "simple": True,
            "connected": True,
            "cubic": True,
            "proper_tait_colouring": True,
            "girth": girth(graph),
            "planar": nx.check_planarity(graph)[0],
            "edge_rows": edges,
            "colours_by_edge": colours,
        },
        "factor_equalities": {
            "ac_component_lengths": [len(component) for component in ac],
            "bc_component_lengths": [len(component) for component in bc],
            "one_mark_per_ac_component": True,
            "one_mark_per_bc_component": True,
        },
        "selector_check": {
            "selectors_enumerated": 256,
            "good_selectors": good_selectors,
            "good_selector_count": len(good_selectors),
            "marked_component_profile_histogram": {
                "+".join(map(str, profile)): count
                for profile, count in sorted(profiles.items())
            },
        },
        "rotation_independent_sufficient_test": {
            "criterion": (
                "The chosen one-from-each-mark-endpoint transversal "
                "induces a multigraph forest and every forest component "
                "has even order."
            ),
            "selectors_passing": forest_even_selectors,
            "passing_count": len(forest_even_selectors),
        },
        "subdivided_marked_core": {
            "vertices": expanded_n,
            "edges": len(expanded_edges),
            "terminals": terminals,
            "girth": girth(expanded),
        },
        "unrestricted_two_t_join_check": packing,
        "universal_separation_diagnostic": {
            "fixed_colouring_separated": separated_in_colouring(
                graph, edges, colours
            ),
            "single_kempe_conflict": conflict,
            "universally_separated": False if conflict is not None else None,
        },
    }
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "classification": report["classification"],
        "core_girth": report["core"]["girth"],
        "subdivided_girth": report["subdivided_marked_core"]["girth"],
        "selector_profiles": report["selector_check"]["marked_component_profile_histogram"],
        "packing": packing["status"],
        "join_sizes": packing["join_sizes"],
        "single_kempe_conflict": conflict is not None,
        "output": str(args.output),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
