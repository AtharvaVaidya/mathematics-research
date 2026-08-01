#!/usr/bin/env python3
"""Second implementation of the minimized strict-lock audit.

This checker uses incidence-matrix elimination for cycle spaces, Tarjan's
bridge algorithm, and combination-by-combination lock minimization.
"""

from __future__ import annotations

import hashlib
import itertools
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent

S = (
    (0, 7), (1, 8), (2, 9), (3, 9), (4, 10), (5, 10),
    (2, 11), (3, 11), (6, 11), (2, 12), (3, 12), (4, 12),
    (0, 13), (6, 13), (10, 13), (1, 14), (5, 14), (6, 14),
    (5, 15), (7, 15), (9, 15), (0, 16), (7, 16), (8, 16),
    (1, 17), (4, 17), (8, 17),
)

B = (
    tuple((i, (i + 1) % 7) for i in range(7))
    + tuple((7 + i, 7 + (i + 1) % 7) for i in range(7))
    + (
        (0, 11), (1, 9), (2, 12), (3, 10), (14, 4),
        (14, 5), (14, 15), (15, 6), (15, 16), (16, 13),
        (16, 17), (17, 7), (17, 8),
    )
)

L = (0, 2, 3, 4, 7, 8, 9, 10)
T = (1 << 14) - 1
H_LOCAL = sum(1 << edge for edge in (5, 13, 14, 16, 17))


def incidence_cycles(order, edges):
    """Nullspace of the vertex-edge incidence matrix over GF(2)."""
    rows = []
    for vertex in range(order):
        rows.append(
            sum(
                1 << edge
                for edge, endpoints in enumerate(edges)
                if vertex in endpoints
            )
        )

    rank = 0
    pivots = []
    for column in range(len(edges)):
        selected = next(
            (
                row
                for row in range(rank, order)
                if (rows[row] >> column) & 1
            ),
            None,
        )
        if selected is None:
            continue
        rows[rank], rows[selected] = rows[selected], rows[rank]
        for row in range(order):
            if row != rank and ((rows[row] >> column) & 1):
                rows[row] ^= rows[rank]
        pivots.append(column)
        rank += 1

    free = [edge for edge in range(len(edges)) if edge not in pivots]
    basis = []
    for column in free:
        vector = 1 << column
        for row, pivot in enumerate(pivots):
            if (rows[row] >> column) & 1:
                vector |= 1 << pivot
        basis.append(vector)

    cycles = [0]
    for vector in basis:
        cycles += [cycle ^ vector for cycle in cycles]
    assert all(
        all(
            sum(
                (cycle >> edge) & 1
                for edge, endpoints in enumerate(edges)
                if vertex in endpoints
            )
            % 2
            == 0
            for vertex in range(order)
        )
        for cycle in cycles
    )
    return tuple(cycles)


def extension_rows(edges, cycles):
    full = (1 << len(edges)) - 1
    missing_multiplicity = {}
    for first in cycles:
        for second in cycles:
            missing = full ^ (first | second)
            missing_multiplicity[missing] = (
                missing_multiplicity.get(missing, 0) + 1
            )
    rows = {}
    for support in cycles:
        count = sum(
            multiplicity
            for missing, multiplicity in missing_multiplicity.items()
            if missing & ~support == 0
        )
        if count:
            rows[support] = count
    return missing_multiplicity, rows


def tarjan_bridges(order, edges):
    graph = [[] for _ in range(order)]
    for edge, (u, v) in enumerate(edges):
        graph[u].append((v, edge))
        graph[v].append((u, edge))

    timer = 0
    entered = [-1] * order
    low = [-1] * order
    bridges = []

    def visit(vertex, parent_edge):
        nonlocal timer
        entered[vertex] = low[vertex] = timer
        timer += 1
        for neighbor, edge in graph[vertex]:
            if edge == parent_edge:
                continue
            if entered[neighbor] >= 0:
                low[vertex] = min(low[vertex], entered[neighbor])
                continue
            visit(neighbor, edge)
            low[vertex] = min(low[vertex], low[neighbor])
            if low[neighbor] > entered[vertex]:
                bridges.append(edge)

    visit(0, -1)
    assert all(value >= 0 for value in entered)
    return tuple(bridges), tuple(tuple(row) for row in graph)


def closure():
    bridges, graph = tarjan_bridges(18, S)
    assert not bridges
    assert all(len(row) == 3 for row in graph)
    cycles = incidence_cycles(18, S)
    assert len(cycles) == 1024
    missing, extensions = extension_rows(S, cycles)
    assert len(missing) == 70780

    rows = {}
    for bit in (0, 1):
        minimum = min(
            support.bit_count()
            for support in extensions
            if ((support >> 5) & 1) == bit
        )
        ties = {
            support: count
            for support, count in extensions.items()
            if support.bit_count() == minimum
            and ((support >> 5) & 1) == bit
        }
        rows[bit] = minimum, ties
    assert rows[0][0] == 7
    assert len(rows[0][1]) == 9
    assert sum(rows[0][1].values()) == 6336
    assert rows[1] == (5, {H_LOCAL: 240})
    return rows


def base_and_locks():
    cycles = incidence_cycles(18, B)
    missing, extensions = extension_rows(B, cycles)
    assert len(cycles) == 1024
    assert len(missing) == 66207
    assert len(extensions) == 1008
    competitors = [support for support in extensions if support != T]

    successful = []
    best = []
    for size in range(15):
        best_delta = -100
        count_positive = 0
        for chosen in itertools.combinations(range(14), size):
            mask = sum(1 << edge for edge in chosen)
            minimum_delta = min(
                2 * ((T & ~support) & mask).bit_count()
                - (T & ~support).bit_count()
                + (support & ~T).bit_count()
                for support in competitors
            )
            best_delta = max(best_delta, minimum_delta)
            if minimum_delta > 0:
                count_positive += 1
                successful.append((mask, minimum_delta))
        best.append(best_delta)
        if count_positive:
            assert size >= 8

    assert best == [
        -9, -7, -5, -5, -3, -3, -1, -1,
        1, 1, 3, 3, 3, 3, 3,
    ]
    minima = [
        row for row in successful if row[0].bit_count() == 8
    ]
    assert len(minima) == 180
    chosen = sum(1 << edge for edge in L)
    assert (chosen, 1) in minima
    digest = hashlib.sha256(
        (
            "\n".join(
                str(mask)
                for mask, _delta in sorted(minima)
            )
            + "\n"
        ).encode("ascii")
    ).hexdigest()
    return digest


def expanded():
    edges = []
    high = set()
    offset = 18
    for base_edge, (u, v) in enumerate(B):
        if base_edge not in L:
            edge = len(edges)
            edges.append((u, v))
            if base_edge < 14:
                high.add(edge)
            continue
        for local_edge, (a, b) in enumerate(S):
            if local_edge == 5:
                continue
            edge = len(edges)
            edges.append((offset + a, offset + b))
            if local_edge in (13, 14, 16, 17):
                high.add(edge)
        high.add(len(edges))
        edges.append((u, offset + 5))
        high.add(len(edges))
        edges.append((v, offset + 10))
        offset += 18

    assert offset == 162
    assert len(edges) == 243
    assert len(high) == 54
    assert len({tuple(sorted(edge)) for edge in edges}) == 243
    bridges, graph = tarjan_bridges(162, edges)
    assert not bridges
    assert all(len(row) == 3 for row in graph)
    return tuple(edges), frozenset(high), graph


def labels_and_graph6(edges, graph):
    raw = (ROOT / "fivecdc-direct-labels.txt").read_text(
        encoding="ascii"
    )
    assert hashlib.sha256(raw.encode("ascii")).hexdigest() == (
        "845668d8778e48ae55cf7373ed159519804407a6d7afeb9999fda02cf97ae8c7"
    )
    labels = tuple(tuple(map(int, token)) for token in raw.split())
    assert len(labels) == 243
    for vertex in range(162):
        for colour in range(5):
            assert (
                sum(
                    colour in labels[edge]
                    for _neighbor, edge in graph[vertex]
                )
                % 2
                == 0
            )
    assert tuple(
        sum(colour in pair for pair in labels)
        for colour in range(5)
    ) == (92, 109, 97, 94, 94)

    labelled = (ROOT / "labelled.g6").read_text(
        encoding="ascii"
    ).strip()
    canonical = (ROOT / "canonical.g6").read_text(
        encoding="ascii"
    ).strip()
    if shutil.which("labelg"):
        process = subprocess.run(
            ("labelg", "-q"),
            input=labelled + "\n",
            text=True,
            capture_output=True,
            check=True,
        )
        assert process.stdout.strip() == canonical
    return (
        hashlib.sha256((labelled + "\n").encode("ascii")).hexdigest(),
        hashlib.sha256((canonical + "\n").encode("ascii")).hexdigest(),
    )


def main():
    conditional = closure()
    minimizer_digest = base_and_locks()
    edges, high, graph = expanded()
    labelled_digest, canonical_digest = labels_and_graph6(edges, graph)

    assert conditional[0][0] == 7
    assert conditional[1][0] == 5
    assert len(high) == 54
    print("INDEPENDENT closure a0=7 a1=5 a1_support_ties=1")
    print(
        "INDEPENDENT locks base_extendable=1008 subsets=16384"
        " minimum=8 minimizers=180 canonical_gap=1"
    )
    print(f"  minimizer_mask_sha256={minimizer_digest}")
    print(
        "INDEPENDENT graph order=162 edges=243"
        " simple=1 cubic=1 bridgeless=1 global_minimum=54"
    )
    print(
        "INDEPENDENT FiveCDC status=SAT direct_sha256="
        "845668d8778e48ae55cf7373ed159519804407a6d7afeb9999fda02cf97ae8c7"
    )
    print(f"  labelled_graph6_sha256={labelled_digest}")
    print(f"  canonical_graph6_sha256={canonical_digest}")
    print(
        "PASS: independent minimized strict-lock and FiveCDC audit"
    )


if __name__ == "__main__":
    main()
