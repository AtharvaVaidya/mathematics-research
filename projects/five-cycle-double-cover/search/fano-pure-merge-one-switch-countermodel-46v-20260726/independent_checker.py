#!/usr/bin/env python3
"""Independent finite checker for the 46-vertex pure-merge countermodel.

This program deliberately imports neither the producer nor any project
module.  It reconstructs the graph from frozen small constants, checks the
graph/flow/cover data, solves the relevant binary linear systems with its own
Gauss-Jordan routine, and checks the finite base-circuit assertion.

It is a checker for a proof-strategy countermodel, not for a counterexample to
the five-cycle double-cover conjecture.
"""

from __future__ import annotations

import argparse
import itertools
import json
import shutil
import subprocess
from collections import Counter, deque
from pathlib import Path


BASE_GRAPH6 = "It?GYDKKO"
BASE_EDGES = (
    (0, 1), (0, 2), (0, 3), (2, 3), (4, 5),
    (4, 6), (5, 6), (1, 7), (6, 7), (1, 8),
    (4, 8), (5, 8), (2, 9), (3, 9), (7, 9),
)
BASE_COLORS = (0, 1, 2, 0, 2, 0, 1, 1, 2, 2, 1, 0, 2, 1, 0)
BASE_FLOW_BY_COLOR = (1, 2, 3)
BASE_PAIR_BY_COLOR = ((2, 3), (1, 3), (1, 2))
MARKED_BASE_EDGES = (1, 6, 7)

BLOCK_GRAPH6 = "K??FEaKR@oE_"
BLOCK_EDGES = (
    (0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 9),
    (2, 6), (2, 10), (2, 11), (3, 7), (3, 10), (3, 11),
    (4, 8), (4, 9), (4, 10), (5, 8), (5, 9), (5, 11),
)
BLOCK_FLOW = (1, 2, 3, 4, 7, 3, 5, 3, 6, 5, 7, 2, 5, 1, 4, 6, 2, 4)
BLOCK_COLORS = (0, 1, 2, 1, 0, 2, 2, 0, 1, 2, 1, 0, 0, 1, 2, 1, 0, 2)
BLOCK_PORT = 1


def incidence(vertices: int, edges: tuple[tuple[int, int], ...]) -> tuple[tuple[int, ...], ...]:
    rows = [[] for _ in range(vertices)]
    for edge, (u, v) in enumerate(edges):
        rows[u].append(edge)
        rows[v].append(edge)
    return tuple(tuple(row) for row in rows)


def encode_graph6(vertices: int, edges: tuple[tuple[int, int], ...]) -> str:
    if not 0 <= vertices <= 62:
        raise AssertionError("checker only implements the short graph6 header")
    present = {tuple(sorted(edge)) for edge in edges}
    bits = [
        int((u, v) in present)
        for v in range(1, vertices)
        for u in range(v)
    ]
    bits.extend([0] * (-len(bits) % 6))
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start:start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(vertices + 63) + "".join(payload)


def connected(vertices: int, edges: tuple[tuple[int, int], ...], omitted: int | None = None) -> bool:
    neighbors = [[] for _ in range(vertices)]
    for edge, (u, v) in enumerate(edges):
        if edge == omitted:
            continue
        neighbors[u].append(v)
        neighbors[v].append(u)
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor in neighbors[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == vertices


def solve_affine(
    variables: int,
    equations: list[tuple[int, int]],
) -> tuple[int, tuple[int, ...], int]:
    """Return a particular solution, nullspace basis, and rank over F_2."""

    augmented_rhs = 1 << variables
    rows = [mask | (rhs * augmented_rhs) for mask, rhs in equations]
    rank = 0
    pivot_columns: list[int] = []
    for column in range(variables):
        pivot = next(
            (row for row in range(rank, len(rows)) if (rows[row] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for row in range(len(rows)):
            if row != rank and ((rows[row] >> column) & 1):
                rows[row] ^= rows[rank]
        pivot_columns.append(column)
        rank += 1
    coefficient_mask = (1 << variables) - 1
    if any((row & coefficient_mask) == 0 and (row & augmented_rhs) for row in rows):
        raise AssertionError("inconsistent binary affine system")

    particular = 0
    for row, column in enumerate(pivot_columns):
        if rows[row] & augmented_rhs:
            particular |= 1 << column

    pivot_set = set(pivot_columns)
    nullspace = []
    for free in range(variables):
        if free in pivot_set:
            continue
        vector = 1 << free
        for row, column in enumerate(pivot_columns):
            if (rows[row] >> free) & 1:
                vector |= 1 << column
        nullspace.append(vector)

    for mask, rhs in equations:
        if ((particular & mask).bit_count() & 1) != rhs:
            raise AssertionError("linear solver produced an invalid particular solution")
    for candidate in nullspace:
        for mask, _ in equations:
            if (candidate & mask).bit_count() & 1:
                raise AssertionError("linear solver produced an invalid nullspace vector")
    return particular, tuple(nullspace), rank


def potential_equations(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
    *,
    omitted: frozenset[int] = frozenset(),
    fix_translation: bool = True,
) -> list[tuple[int, int]]:
    rows = incidence(vertices, edges)
    equations: list[tuple[int, int]] = []
    for edge, (u, v) in enumerate(edges):
        if edge in omitted:
            continue
        u_other = next(item for item in rows[u] if item != edge)
        v_other = next(item for item in rows[v] if item != edge)
        difference = flow[u_other] ^ flow[v_other]
        value = flow[edge]
        functionals = [
            vector
            for vector in range(1, 8)
            if ((vector & value).bit_count() & 1) == 0
        ]
        if len(functionals) != 3:
            raise AssertionError("bad orthogonal plane")
        for functional in functionals[:2]:
            mask = 0
            for vertex in (u, v):
                for bit in range(3):
                    if (functional >> bit) & 1:
                        mask ^= 1 << (3 * vertex + bit)
            rhs = (functional & difference).bit_count() & 1
            equations.append((mask, rhs))
    if fix_translation:
        equations.extend((1 << bit, 0) for bit in range(3))
    return equations


def vector_at(word: int, vertex: int) -> int:
    return sum(((word >> (3 * vertex + bit)) & 1) << bit for bit in range(3))


def endpoint_pair(
    vertex: int,
    edge: int,
    word: int,
    flow: tuple[int, ...],
    rows: tuple[tuple[int, ...], ...],
) -> tuple[int, int]:
    other = next(item for item in rows[vertex] if item != edge)
    first = vector_at(word, vertex) ^ flow[other]
    return tuple(sorted((first, first ^ flow[edge])))


def labels_from_word(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
    word: int,
) -> tuple[tuple[int, int], ...]:
    rows = incidence(vertices, edges)
    labels = []
    for edge, (u, v) in enumerate(edges):
        left = endpoint_pair(u, edge, word, flow, rows)
        right = endpoint_pair(v, edge, word, flow, rows)
        if left != right:
            raise AssertionError(f"endpoint labels disagree at edge {edge}")
        labels.append(left)
    return tuple(labels)


def parity_labels(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    labels: tuple[tuple[int, int], ...],
) -> bool:
    rows = incidence(vertices, edges)
    for row in rows:
        counts: Counter[int] = Counter()
        for edge in row:
            counts.update(labels[edge])
        if any(count & 1 for count in counts.values()):
            return False
    return True


def cooccurrence_adjacency(labels: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    adjacency = [0] * 8
    for first, second in labels:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    return tuple(adjacency)


def maximum_clique(adjacency: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    best: tuple[int, ...] = ()
    for mask in range(1, 1 << 8):
        vertices = tuple(vertex for vertex in range(8) if (mask >> vertex) & 1)
        if len(vertices) <= len(best):
            continue
        if all((adjacency[u] >> v) & 1 for u, v in itertools.combinations(vertices, 2)):
            best = vertices
    return len(best), best


def five_colorable(adjacency: tuple[int, ...]) -> bool:
    colors = [-1] * 8

    def extend(done: int) -> bool:
        if done == 8:
            return True
        remaining = [vertex for vertex in range(8) if colors[vertex] < 0]
        vertex = max(
            remaining,
            key=lambda item: sum(
                1
                for neighbor in range(8)
                if colors[neighbor] >= 0 and ((adjacency[item] >> neighbor) & 1)
            ),
        )
        forbidden = {
            colors[neighbor]
            for neighbor in range(8)
            if colors[neighbor] >= 0 and ((adjacency[vertex] >> neighbor) & 1)
        }
        for color in range(5):
            if color in forbidden:
                continue
            colors[vertex] = color
            if extend(done + 1):
                return True
            colors[vertex] = -1
        return False

    return extend(0)


def is_circuit(mask: int, vertices: int, edges: tuple[tuple[int, int], ...]) -> bool:
    if mask == 0:
        return False
    degrees = [0] * vertices
    neighbors = [[] for _ in range(vertices)]
    for edge, (u, v) in enumerate(edges):
        if (mask >> edge) & 1:
            degrees[u] += 1
            degrees[v] += 1
            neighbors[u].append(v)
            neighbors[v].append(u)
    used = [vertex for vertex, degree in enumerate(degrees) if degree]
    if not used or any(degrees[vertex] != 2 for vertex in used):
        return False
    seen = {used[0]}
    queue = deque([used[0]])
    while queue:
        vertex = queue.popleft()
        for neighbor in neighbors[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == len(used)


def reconstruct(
    block_labels: tuple[tuple[int, int], ...],
) -> tuple[
    tuple[tuple[int, int], ...],
    tuple[int, ...],
    tuple[tuple[int, int], ...],
    tuple[int, ...],
    tuple[dict[str, int | str], ...],
]:
    raw_edges: list[tuple[int, int]] = []
    raw_flow: list[int] = []
    raw_labels: list[tuple[int, int]] = []
    raw_colors: list[int] = []
    origins: list[dict[str, int | str]] = []
    next_vertex = 10
    selected = set(MARKED_BASE_EDGES)
    for base_edge, endpoints in enumerate(BASE_EDGES):
        if base_edge not in selected:
            raw_edges.append(endpoints)
            raw_flow.append(BASE_FLOW_BY_COLOR[BASE_COLORS[base_edge]])
            raw_labels.append(BASE_PAIR_BY_COLOR[BASE_COLORS[base_edge]])
            raw_colors.append(BASE_COLORS[base_edge])
            origins.append({"kind": "base", "edge": base_edge})
            continue
        offset = next_vertex
        next_vertex += 12
        for local_edge, (u, v) in enumerate(BLOCK_EDGES):
            if local_edge == BLOCK_PORT:
                continue
            raw_edges.append((offset + u, offset + v))
            raw_flow.append(BLOCK_FLOW[local_edge])
            raw_labels.append(block_labels[local_edge])
            raw_colors.append(BLOCK_COLORS[local_edge])
            origins.append({"kind": "block", "base_edge": base_edge, "edge": local_edge})
        u, v = endpoints
        a, b = BLOCK_EDGES[BLOCK_PORT]
        raw_edges.extend(((u, offset + a), (v, offset + b)))
        raw_flow.extend((BLOCK_FLOW[BLOCK_PORT],) * 2)
        raw_labels.extend((block_labels[BLOCK_PORT],) * 2)
        raw_colors.extend((BLOCK_COLORS[BLOCK_PORT],) * 2)
        origins.extend((
            {"kind": "connector", "base_edge": base_edge, "side": 0},
            {"kind": "connector", "base_edge": base_edge, "side": 1},
        ))
    order = sorted(range(len(raw_edges)), key=lambda edge: raw_edges[edge])
    return (
        tuple(raw_edges[edge] for edge in order),
        tuple(raw_flow[edge] for edge in order),
        tuple(raw_labels[edge] for edge in order),
        tuple(raw_colors[edge] for edge in order),
        tuple(origins[edge] for edge in order),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    here = Path(__file__).resolve().parent
    parser.add_argument("--construction", type=Path, default=here / "construction.json")
    parser.add_argument("--output", type=Path, default=here / "independent-check.json")
    arguments = parser.parse_args()
    frozen = json.loads(arguments.construction.read_text(encoding="utf-8"))

    block_rows = incidence(12, BLOCK_EDGES)
    block_equations = potential_equations(
        12,
        BLOCK_EDGES,
        BLOCK_FLOW,
        omitted=frozenset((BLOCK_PORT,)),
    )
    block_word, block_nullspace, block_rank = solve_affine(36, block_equations)
    if block_nullspace or block_rank != 36:
        raise AssertionError("port-deleted block is not rigid modulo translation")
    block_labels = labels_from_word(12, BLOCK_EDGES, BLOCK_FLOW, block_word)
    port_u, port_v = BLOCK_EDGES[BLOCK_PORT]
    port_pairs = (
        endpoint_pair(port_u, BLOCK_PORT, block_word, BLOCK_FLOW, block_rows),
        endpoint_pair(port_v, BLOCK_PORT, block_word, BLOCK_FLOW, block_rows),
    )
    if port_pairs[0] != port_pairs[1]:
        raise AssertionError("the two dangling port labels disagree")
    internal_plus_port = tuple(
        block_labels[edge] for edge in range(len(BLOCK_EDGES)) if edge != BLOCK_PORT
    ) + (port_pairs[0],)
    block_adjacency = cooccurrence_adjacency(internal_plus_port)
    block_clique_size, block_clique = maximum_clique(block_adjacency)
    expected_pairs = {
        tuple(pair)
        for pair in itertools.combinations((0, 1, 2, 3, 4, 6), 2)
    }
    if set(internal_plus_port) != expected_pairs:
        raise AssertionError("rigid cap does not force the claimed K6")
    if block_clique_size != 6 or five_colorable(block_adjacency):
        raise AssertionError("K6 pure-merge obstruction check failed")

    edges, flow, labels, colors, origins = reconstruct(block_labels)
    if len(edges) != 69 or len({*edges}) != 69 or any(u == v for u, v in edges):
        raise AssertionError("expanded graph is not simple with 69 edges")
    rows = incidence(46, edges)
    if any(len(row) != 3 for row in rows):
        raise AssertionError("expanded graph is not cubic")
    if not connected(46, edges):
        raise AssertionError("expanded graph is disconnected")
    bridges = [edge for edge in range(len(edges)) if not connected(46, edges, edge)]
    if bridges:
        raise AssertionError(f"expanded graph has bridges {bridges}")
    if any(flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] for row in rows):
        raise AssertionError("expanded flow violates conservation")
    if not parity_labels(46, edges, labels):
        raise AssertionError("supplied eight-cover violates coordinate parity")
    if any({colors[edge] for edge in row} != {0, 1, 2} for row in rows):
        raise AssertionError("displayed Tait coloring is not proper")
    explicit_cover = tuple(
        tuple(edge for edge, color in enumerate(colors) if color != coordinate)
        for coordinate in range(3)
    ) + ((), ())
    if [len(coordinate) for coordinate in explicit_cover] != [46, 46, 46, 0, 0]:
        raise AssertionError("unexpected explicit five-cover sizes")
    if any(
        sum(edge in coordinate for coordinate in explicit_cover) != 2
        for edge in range(len(edges))
    ):
        raise AssertionError("explicit five-cover is not exact-two")
    if any(
        sum(edge in coordinate for edge in row) & 1
        for coordinate in explicit_cover
        for row in rows
    ):
        raise AssertionError("explicit five-cover coordinate is not Eulerian")

    if tuple(tuple(edge) for edge in frozen["edges"]) != edges:
        raise AssertionError("frozen edge list differs from reconstruction")
    if tuple(frozen["flow_values_by_edge"]) != flow:
        raise AssertionError("frozen flow differs from reconstruction")
    if tuple(tuple(pair) for pair in frozen["supplied_eight_cover_labels"]) != labels:
        raise AssertionError("frozen eight-cover differs from reconstruction")
    if tuple(frozen["three_edge_coloring_by_edge"]) != colors:
        raise AssertionError("frozen Tait coloring differs from reconstruction")
    if tuple(frozen["edge_origins"]) != origins:
        raise AssertionError("frozen origins differ from reconstruction")

    base_marked_mask = sum(1 << edge for edge in MARKED_BASE_EDGES)
    base_circuits = [
        mask
        for mask in range(1, 1 << len(BASE_EDGES))
        if is_circuit(mask, 10, BASE_EDGES)
    ]
    marked_containing = [
        mask for mask in base_circuits if (mask & base_marked_mask) == base_marked_mask
    ]
    if marked_containing:
        raise AssertionError("a base circuit contains all three marked edges")
    if len(base_circuits) != 30:
        raise AssertionError("unexpected base circuit count")

    global_equations = potential_equations(46, edges, flow)
    global_word, global_basis, global_rank = solve_affine(138, global_equations)
    if len(global_basis) != 7 or global_rank != 131:
        raise AssertionError("unexpected global potential-space dimension")
    pair_count_profile: Counter[int] = Counter()
    clique_profile: Counter[int] = Counter()
    five_colorable_solutions = 0
    for selector in range(1 << len(global_basis)):
        word = global_word
        for index, basis in enumerate(global_basis):
            if (selector >> index) & 1:
                word ^= basis
        candidate_labels = labels_from_word(46, edges, flow, word)
        adjacency = cooccurrence_adjacency(candidate_labels)
        pair_count_profile[len(set(candidate_labels))] += 1
        clique_size, _ = maximum_clique(adjacency)
        clique_profile[clique_size] += 1
        five_colorable_solutions += int(five_colorable(adjacency))
    if pair_count_profile != Counter({24: 96, 15: 32}):
        raise AssertionError("unexpected global used-pair profile")
    if clique_profile != Counter({6: 128}) or five_colorable_solutions:
        raise AssertionError("global fixed-flow pure-merge audit failed")

    raw_graph6 = encode_graph6(46, edges)
    if raw_graph6 != frozen["graph6"]:
        raise AssertionError("frozen graph6 string differs from reconstruction")
    canonical_graph6 = None
    labelg = shutil.which("labelg")
    if labelg:
        completed = subprocess.run(
            [labelg, "-q"],
            input=raw_graph6 + "\n",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        canonical_graph6 = completed.stdout.strip()

    block_shores = []
    for index, replaced in enumerate(MARKED_BASE_EDGES):
        offset = 10 + 12 * index
        shore = set(range(offset, offset + 12))
        connectors = [
            edge
            for edge, (u, v) in enumerate(edges)
            if (u in shore) ^ (v in shore)
        ]
        if len(connectors) != 2:
            raise AssertionError("a block does not have an exact two-edge boundary")
        if any(flow[edge] != 2 for edge in connectors):
            raise AssertionError("a connector has the wrong flow value")
        block_shores.append(
            {
                "replaced_base_edge": replaced,
                "vertices": sorted(shore),
                "connector_edge_ids": connectors,
            }
        )

    result = {
        "schema": "independent-fano-pure-merge-one-switch-check-v1",
        "status": "PASS",
        "scope_warning": (
            "This checks a countermodel to a fixed-flow pure-merge plus "
            "one-connected-circuit repair strategy. It is not a five-CDC "
            "counterexample."
        ),
        "graph": {
            "vertices": 46,
            "edges": 69,
            "simple": True,
            "cubic": True,
            "connected": True,
            "bridgeless_by_all_single_edge_deletions": True,
            "raw_graph6": raw_graph6,
            "canonical_graph6": canonical_graph6,
        },
        "flow_and_positive_cover": {
            "nowhere_zero_flow": True,
            "flow_conservation": True,
            "proper_three_edge_coloring": True,
            "explicit_five_cdc_sizes": [46, 46, 46, 0, 0],
            "eight_cover_parity": True,
        },
        "rigid_block": {
            "graph6": BLOCK_GRAPH6,
            "port_edge": BLOCK_PORT,
            "port_deleted_equations": len(block_equations),
            "rank_after_translation_gauge": block_rank,
            "free_dimension": len(block_nullspace),
            "gauged_potentials_by_vertex": [
                vector_at(block_word, vertex) for vertex in range(12)
            ],
            "dangling_port_pair_from_each_side": [list(pair) for pair in port_pairs],
            "used_pairs": [list(pair) for pair in sorted(set(internal_plus_port))],
            "forced_clique": list(block_clique),
            "maximum_clique_size": block_clique_size,
            "five_colorable": False,
        },
        "base_noncyclability": {
            "graph6": BASE_GRAPH6,
            "circuit_count": len(base_circuits),
            "marked_edge_ids": list(MARKED_BASE_EDGES),
            "circuits_containing_all_marked_edges": 0,
        },
        "expanded_fixed_flow": {
            "potential_equations": len(global_equations),
            "rank_after_translation_gauge": global_rank,
            "free_dimension": len(global_basis),
            "potential_solutions": 1 << len(global_basis),
            "used_pair_count_profile": {
                str(key): value for key, value in sorted(pair_count_profile.items())
            },
            "maximum_clique_size_profile": {
                str(key): value for key, value in sorted(clique_profile.items())
            },
            "five_colorable_solutions": five_colorable_solutions,
        },
        "two_edge_block_shores": block_shores,
        "human_proof_dependencies_checked": [
            "each retained block is potential-rigid modulo global translation",
            "each retained block forces a coordinate K6 including its dangling ports",
            "the three marked base edges are noncyclable",
            "each embedded block has exactly two connectors",
        ],
    }
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": result["status"],
        "canonical_graph6": canonical_graph6,
        "potential_solutions": 1 << len(global_basis),
        "five_colorable_solutions": five_colorable_solutions,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
