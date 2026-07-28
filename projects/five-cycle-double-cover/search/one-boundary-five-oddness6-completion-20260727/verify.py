#!/usr/bin/env python3
"""Independent audit of the order-100 one-boundary-five specimen.

The script reconstructs the graph from Petersen pieces.  Its quick mode
checks the exact Gallai--Edmonds profile, factor-criticality of the
93-vertex shore, an explicit six-odd-circuit 2-factor, and an explicit
standard five-cycle-double-cover.  ``--full`` additionally enumerates all
edge cuts of size at most three in the source and the completion.

Only the Python standard library is used.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
KINDS = ("N2", "N2", "N2", "N1")
DELETED_PATH = (4, 0, 5)
BOUNDARY_OLD = (3, 7, 8, 9, 12)
EXPECTED_COMPONENT_SIZES = (5, 5, 8, 9, 9, 9, 9, 10, 12, 12, 12)


def petersen_edges() -> tuple[tuple[int, int], ...]:
    edges = [(i, (i + 1) % 5) for i in range(5)]
    edges += [(i, i + 5) for i in range(5)]
    edges += [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    return tuple(sorted(tuple(sorted(edge)) for edge in edges))


def p4v() -> tuple[
    int, list[tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]
]:
    retained = [vertex for vertex in range(10) if vertex not in (0, 1)]
    index = {vertex: position for position, vertex in enumerate(retained)}
    edges = [
        (index[left], index[right])
        for left, right in petersen_edges()
        if left in index and right in index
    ]
    return 8, edges, (
        (index[4], index[5]),
        (index[2], index[6]),
    )


def p4e() -> tuple[
    int, list[tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]
]:
    removed = {(0, 1), (2, 3)}
    edges = [edge for edge in petersen_edges() if edge not in removed]
    return 10, edges, ((0, 1), (2, 3))


def block(kind: str) -> tuple[
    int, list[tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]
]:
    order, edges, base_pairs = p4e()
    free_pairs: list[tuple[int, int]] = []
    copies = {"N1": 1, "N2": 2}[kind]
    for copy in range(copies):
        piece_order, piece_edges, piece_pairs = p4v()
        offset = order
        order += piece_order
        edges.extend((left + offset, right + offset)
                     for left, right in piece_edges)
        edges.extend(
            (left, right + offset)
            for left, right in zip(base_pairs[copy], piece_pairs[0])
        )
        free_pairs.append(tuple(vertex + offset for vertex in piece_pairs[1]))
    if kind == "N1":
        free_pairs.append(base_pairs[1])
    return order, edges, (free_pairs[0], free_pairs[1])


def build_source() -> tuple[int, tuple[tuple[int, int], ...]]:
    order = 0
    edges: list[tuple[int, int]] = []
    connectors = []
    for kind in KINDS:
        piece_order, piece_edges, piece_connectors = block(kind)
        edges.extend((left + order, right + order)
                     for left, right in piece_edges)
        connectors.append(tuple(
            tuple(vertex + order for vertex in pair)
            for pair in piece_connectors
        ))
        order += piece_order
    for index in range(len(KINDS)):
        edges.extend(zip(
            connectors[index][1],
            connectors[(index + 1) % len(KINDS)][0],
        ))
    return order, tuple(sorted(tuple(sorted(edge)) for edge in edges))


def delete_vertices(
    order: int,
    edges: tuple[tuple[int, int], ...],
    deleted: tuple[int, ...],
) -> tuple[int, tuple[tuple[int, int], ...], dict[int, int]]:
    retained = [vertex for vertex in range(order) if vertex not in deleted]
    index = {old: new for new, old in enumerate(retained)}
    result = tuple(sorted(
        (index[left], index[right])
        for left, right in edges
        if left in index and right in index
    ))
    return len(retained), result, index


def build_completion() -> tuple[
    int, tuple[tuple[int, int], ...], tuple[int, ...], dict[str, tuple[int, ...]]
]:
    source_order, source_edges = build_source()
    q_order, q_edges, index = delete_vertices(
        source_order, source_edges, DELETED_PATH
    )
    terminals = tuple(index[vertex] for vertex in BOUNDARY_OLD)
    w = tuple(range(q_order, q_order + 5))
    z = (q_order + 5, q_order + 6)
    edges = list(q_edges)
    edges.extend(((w[0], w[1]), (w[2], w[3])))
    edges.extend((z[0], w[local]) for local in (0, 2, 4))
    edges.extend((z[1], w[local]) for local in (1, 3, 4))
    edges.extend(zip(terminals, w))
    normalized = tuple(sorted(tuple(sorted(edge)) for edge in edges))
    return q_order + 7, normalized, terminals, {
        "Q": tuple(range(q_order)),
        "U": w[:4],
        "A": (w[4],),
        "Z": z,
        "W": w,
    }


def adjacency(
    order: int, edges: tuple[tuple[int, int], ...]
) -> list[int]:
    rows = [0] * order
    seen = set()
    for left, right in edges:
        if not 0 <= left < right < order or (left, right) in seen:
            raise AssertionError("edge table is not simple and normalized")
        seen.add((left, right))
        rows[left] |= 1 << right
        rows[right] |= 1 << left
    return rows


def components(rows: list[int], allowed: int) -> list[int]:
    result = []
    while allowed:
        reached = allowed & -allowed
        frontier = reached
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            vertex = bit.bit_length() - 1
            fresh = rows[vertex] & allowed & ~reached
            reached |= fresh
            frontier |= fresh
        result.append(reached)
        allowed &= ~reached
    return result


def component_has_circuit(rows: list[int], vertices: int) -> bool:
    twice_edges = sum(
        (rows[vertex] & vertices).bit_count()
        for vertex in range(len(rows))
        if vertices >> vertex & 1
    )
    return twice_edges // 2 >= vertices.bit_count()


def cyclically_four(
    rows: list[int], edges: tuple[tuple[int, int], ...]
) -> bool:
    full = (1 << len(rows)) - 1
    for size in (1, 2, 3):
        for cut in combinations(edges, size):
            modified = rows[:]
            for left, right in cut:
                modified[left] &= ~(1 << right)
                modified[right] &= ~(1 << left)
            parts = components(modified, full)
            if len(parts) > 1 and sum(
                component_has_circuit(modified, part) for part in parts
            ) >= 2:
                return False
    return True


def factor_critical(rows: list[int]) -> bool:
    full = (1 << len(rows)) - 1

    @lru_cache(maxsize=None)
    def matchable(vertices: int) -> bool:
        if not vertices:
            return True
        if vertices.bit_count() % 2:
            return False
        first_bit = vertices & -vertices
        first = first_bit.bit_length() - 1
        candidates = rows[first] & vertices & ~first_bit
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            if matchable(vertices ^ first_bit ^ second_bit):
                return True
        return False

    return all(matchable(full ^ (1 << vertex))
               for vertex in range(len(rows)))


def graph_object(
    order: int, edges: tuple[tuple[int, int], ...]
) -> dict[str, object]:
    return {
        "format": "five-cdc-multigraph-v1",
        "vertices": order,
        "edges": [
            {"id": edge_id, "u": left, "v": right}
            for edge_id, (left, right) in enumerate(edges)
        ],
    }


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("ascii")


def check_retained_graph(
    name: str,
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> None:
    retained = json.loads((ROOT / name).read_text(encoding="ascii"))
    expected = graph_object(order, edges)
    if retained != expected:
        raise AssertionError(f"{name} does not match reconstruction")


def check_ge_profile(
    rows: list[int], parts: dict[str, tuple[int, ...]]
) -> None:
    full = (1 << len(rows)) - 1
    u_mask = sum(1 << vertex for vertex in parts["U"])
    a_mask = sum(1 << vertex for vertex in parts["A"])
    pieces = components(rows, full & ~u_mask & ~a_mask)
    expected = [
        sum(1 << vertex for vertex in parts["Q"]),
        *(1 << vertex for vertex in parts["Z"]),
    ]
    if {piece for piece in pieces} != set(expected):
        raise AssertionError("wrong components after deleting U and A")
    a = parts["A"][0]
    if not all(rows[a] & piece for piece in expected):
        raise AssertionError("A does not meet all three D-components")


def check_matching(
    rows: list[int],
    edges: tuple[tuple[int, int], ...],
) -> dict[str, object]:
    witness = json.loads(
        (ROOT / "oddness6-matching.json").read_text(encoding="ascii")
    )
    chosen = {tuple(edge) for edge in witness["matching_edges"]}
    if not chosen <= set(edges):
        raise AssertionError("matching uses a nonedge")
    degree = [0] * len(rows)
    complement = rows[:]
    for left, right in chosen:
        degree[left] += 1
        degree[right] += 1
        complement[left] &= ~(1 << right)
        complement[right] &= ~(1 << left)
    if degree != [1] * len(rows):
        raise AssertionError("displayed edges are not a perfect matching")
    sizes = tuple(sorted(part.bit_count() for part in components(
        complement, (1 << len(rows)) - 1
    )))
    if sizes != EXPECTED_COMPONENT_SIZES:
        raise AssertionError("complement component sizes changed")
    odd = sum(size % 2 for size in sizes)
    if odd != 6:
        raise AssertionError("displayed 2-factor does not have six odd circuits")
    return {"component_sizes": sizes, "odd_circuits": odd}


def check_cover(
    rows: list[int], edges: tuple[tuple[int, int], ...]
) -> None:
    cover = json.loads(
        (ROOT / "fivecdc-cover.json").read_text(encoding="ascii")
    )
    graph_digest = sha256((ROOT / "graph.json").read_bytes()).hexdigest()
    if cover.get("graph_sha256") != graph_digest:
        raise AssertionError("cover is not bound to retained graph.json")
    labels = cover["labels"]
    if len(labels) != len(edges):
        raise AssertionError("cover has wrong edge count")
    parity = [[0] * 5 for _ in rows]
    for edge_id, ((left, right), label) in enumerate(zip(edges, labels)):
        if len(label) != 2 or len(set(label)) != 2:
            raise AssertionError(f"edge {edge_id} does not have two labels")
        for coordinate in label:
            if not 0 <= coordinate < 5:
                raise AssertionError("coordinate outside 0..4")
            parity[left][coordinate] ^= 1
            parity[right][coordinate] ^= 1
    if any(any(row) for row in parity):
        raise AssertionError("cover violates an Eulerian parity equation")


def check_hashes() -> None:
    for line in (ROOT / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        digest, name = line.split("  ", 1)
        if name == "SHA256SUMS":
            continue
        actual = sha256((ROOT / name).read_bytes()).hexdigest()
        if actual != digest:
            raise AssertionError(f"hash mismatch for {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()

    source_order, source_edges = build_source()
    order, edges, terminals, parts = build_completion()
    source_rows = adjacency(source_order, source_edges)
    rows = adjacency(order, edges)
    if source_order != 96 or len(source_edges) != 144:
        raise AssertionError("source order/size changed")
    if order != 100 or len(edges) != 150:
        raise AssertionError("completion order/size changed")
    if [row.bit_count() for row in source_rows] != [3] * source_order:
        raise AssertionError("source is not cubic")
    if [row.bit_count() for row in rows] != [3] * order:
        raise AssertionError("completion is not cubic")
    check_retained_graph("source.graph.json", source_order, source_edges)
    check_retained_graph("graph.json", order, edges)

    q_rows = adjacency(
        len(parts["Q"]),
        tuple(edge for edge in edges
              if edge[0] in parts["Q"] and edge[1] in parts["Q"]),
    )
    if terminals != (2, 4, 5, 6, 9):
        raise AssertionError("boundary terminals changed")
    if not factor_critical(q_rows):
        raise AssertionError("Q is not factor-critical")
    check_ge_profile(rows, parts)
    matching = check_matching(rows, edges)
    check_cover(rows, edges)
    check_hashes()

    result = {
        "status": "PASS",
        "source": {"vertices": source_order, "edges": len(source_edges)},
        "completion": {"vertices": order, "edges": len(edges)},
        "Q_factor_critical": True,
        "boundary_terminals": terminals,
        "one_boundary_five_GE_profile": True,
        "explicit_fivecdc": True,
        "explicit_2factor": matching,
        "full_cyclic_cut_audit": args.full,
    }
    if args.full:
        result["source_cyclically_four"] = cyclically_four(
            source_rows, source_edges
        )
        result["completion_cyclically_four"] = cyclically_four(rows, edges)
        if not result["source_cyclically_four"]:
            raise AssertionError("source has a cyclic cut below four")
        if not result["completion_cyclically_four"]:
            raise AssertionError("completion has a cyclic cut below four")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
