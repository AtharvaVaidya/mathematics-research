#!/usr/bin/env python3
"""Independently verify the order-16 whole-fibre square witness census.

This checker does not import or call the C++ discovery program.  It obtains
the canonical connected cubic order-16 stream from nauty ``geng``, checks a
frozen SHA-256 digest, independently filters 3-edge-connected graphs, and
requires exactly one witness for every labelled root and eligible independent
edge pair.  Every downstairs and lifted spanning-tree triple, multiplicity
condition, outside-edge agreement, and odd-kernel component-parity condition
is recomputed from the integer masks in the corpus.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import shutil
import subprocess
from pathlib import Path


CANONICAL_SHA256 = (
    "b3610f3eab739083ece9fc9c5d896708de5345b8b22104e13425bfcb88b9df5e"
)
EXPECTED_RETAINED = 2828


def canonical_records(geng_path: str | None) -> tuple[str, ...]:
    executable = geng_path or shutil.which("geng")
    if executable is None:
        homebrew = Path("/opt/homebrew/bin/geng")
        if homebrew.exists():
            executable = str(homebrew)
    if executable is None:
        raise SystemExit("geng not found; pass --geng /path/to/geng")
    result = subprocess.run(
        [executable, "-cq", "-d3", "-D3", "16"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    digest = hashlib.sha256(result.stdout).hexdigest()
    assert digest == CANONICAL_SHA256, (digest, CANONICAL_SHA256)
    records = tuple(result.stdout.decode("ascii").splitlines())
    assert len(records) == 4060
    assert len(set(records)) == len(records)
    return records


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    assert record and record[0] != "~"
    vertex_count = ord(record[0]) - 63
    bits = "".join(f"{ord(character) - 63:06b}" for character in record[1:])
    edges = []
    position = 0
    for right in range(1, vertex_count):
        for left in range(right):
            if bits[position] == "1":
                edges.append((left, right))
            position += 1
    assert all(bit == "0" for bit in bits[position:])
    assert vertex_count == 16
    assert len(edges) == 24
    assert len(set(edges)) == len(edges)
    assert all(
        sum(vertex in edge for edge in edges) == 3
        for vertex in range(vertex_count)
    )
    return vertex_count, tuple(edges)


def connected_after_deleting(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    deleted: frozenset[int],
) -> bool:
    adjacency = [[] for _ in range(vertex_count)]
    for edge_index, (left, right) in enumerate(edges):
        if edge_index in deleted:
            continue
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = {0}
    queue = [0]
    for vertex in queue:
        for neighbour in adjacency[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return len(seen) == vertex_count


def is_three_edge_connected(
    vertex_count: int, edges: tuple[tuple[int, int], ...]
) -> bool:
    return all(
        connected_after_deleting(
            vertex_count, edges, frozenset((first, second))
        )
        for first in range(len(edges))
        for second in range(first, len(edges))
    )


def selected_indices(mask: int, edge_count: int) -> tuple[int, ...]:
    assert mask >= 0
    assert mask >> edge_count == 0
    return tuple(
        edge_index
        for edge_index in range(edge_count)
        if mask >> edge_index & 1
    )


def is_tree(
    vertex_count: int, edges: tuple[tuple[int, int], ...], mask: int
) -> bool:
    selected = selected_indices(mask, len(edges))
    if len(selected) != vertex_count - 1:
        return False
    adjacency = [[] for _ in range(vertex_count)]
    for edge_index in selected:
        left, right = edges[edge_index]
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = {0}
    queue = [0]
    for vertex in queue:
        for neighbour in adjacency[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return len(seen) == vertex_count


def odd_kernel(
    vertex_count: int, edges: tuple[tuple[int, int], ...], tree: int
) -> frozenset[int]:
    assert is_tree(vertex_count, edges, tree)
    adjacency = [[] for _ in range(vertex_count)]
    for edge_index in selected_indices(tree, len(edges)):
        left, right = edges[edge_index]
        adjacency[left].append((right, edge_index))
        adjacency[right].append((left, edge_index))
    parent = [-1] * vertex_count
    parent_edge = [-1] * vertex_count
    order = [0]
    parent[0] = 0
    for vertex in order:
        for neighbour, edge_index in adjacency[vertex]:
            if parent[neighbour] == -1:
                parent[neighbour] = vertex
                parent_edge[neighbour] = edge_index
                order.append(neighbour)
    assert len(order) == vertex_count
    sizes = [1] * vertex_count
    answer = set()
    for vertex in reversed(order[1:]):
        if sizes[vertex] & 1:
            answer.add(parent_edge[vertex])
        sizes[parent[vertex]] += sizes[vertex]
    return frozenset(answer)


def components(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    selected: frozenset[int],
) -> tuple[frozenset[int], ...]:
    adjacency = [[] for _ in range(vertex_count)]
    for edge_index in selected:
        left, right = edges[edge_index]
        adjacency[left].append(right)
        adjacency[right].append(left)
    unseen = set(range(vertex_count))
    result = []
    while unseen:
        start = min(unseen)
        component = {start}
        unseen.remove(start)
        queue = [start]
        for vertex in queue:
            for neighbour in adjacency[vertex]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    component.add(neighbour)
                    queue.append(neighbour)
        result.append(frozenset(component))
    return tuple(result)


def defect_profile(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    state: tuple[int, int, int],
) -> tuple[int, int, int]:
    kernels = tuple(
        odd_kernel(vertex_count, edges, tree) for tree in state
    )
    result = []
    for coordinate in range(3):
        others = [index for index in range(3) if index != coordinate]
        pure = kernels[others[0]] & kernels[others[1]]
        defect = 0
        for component in components(
            vertex_count, edges, kernels[coordinate]
        ):
            crossing_count = sum(
                (edges[edge_index][0] in component)
                != (edges[edge_index][1] in component)
                for edge_index in pure
            )
            defect += crossing_count & 1
        result.append(defect)
    return tuple(result)


def check_star_multiplicities(
    root: int,
    edges: tuple[tuple[int, int], ...],
    state: tuple[int, int, int],
) -> None:
    for tree in state:
        assert is_tree(max(max(edge) for edge in edges) + 1, edges, tree)
    for edge_index, edge in enumerate(edges):
        multiplicity = sum(tree >> edge_index & 1 for tree in state)
        assert multiplicity == (1 if root in edge else 2)


def eligible_pairs(
    edges: tuple[tuple[int, int], ...], root: int
) -> tuple[tuple[int, int], ...]:
    result = []
    for first in range(len(edges)):
        if root in edges[first]:
            continue
        for second in range(first + 1, len(edges)):
            if root in edges[second]:
                continue
            if len(set(edges[first] + edges[second])) == 4:
                result.append((first, second))
    assert len(result) == 171
    return tuple(result)


def square_expansion(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    pair: tuple[int, int],
) -> tuple[tuple[tuple[int, int], ...], dict[int, int]]:
    first, second = pair
    outside = []
    down_to_up = {}
    for edge_index, edge in enumerate(edges):
        if edge_index in pair:
            continue
        down_to_up[edge_index] = len(outside)
        outside.append(edge)
    A, C = edges[first]
    B, D = edges[second]
    a, b, c, d = range(vertex_count, vertex_count + 4)
    gadget = (
        (A, a),
        (B, b),
        (C, c),
        (D, d),
        (a, b),
        (b, c),
        (c, d),
        (d, a),
    )
    return tuple(outside) + gadget, down_to_up


def check_witness(
    graph_index: int,
    record: str,
    root: int,
    pair: tuple[int, int],
    down_state: tuple[int, int, int],
    up_state: tuple[int, int, int],
    records: tuple[str, ...],
    graphs: tuple[tuple[int, tuple[tuple[int, int], ...]], ...],
    checked_down: set[tuple[int, int, int, int, int]],
) -> None:
    assert 0 <= graph_index < len(records)
    assert record == records[graph_index]
    vertex_count, edges = graphs[graph_index]
    first, second = pair
    assert 0 <= first < second < len(edges)
    assert root not in edges[first] and root not in edges[second]
    assert len(set(edges[first] + edges[second])) == 4
    down_key = (graph_index, root) + down_state
    if down_key not in checked_down:
        check_star_multiplicities(root, edges, down_state)
        assert 0 in defect_profile(vertex_count, edges, down_state)
        checked_down.add(down_key)

    up_edges, down_to_up = square_expansion(vertex_count, edges, pair)
    check_star_multiplicities(root, up_edges, up_state)
    for coordinate in range(3):
        for down_edge, up_edge in down_to_up.items():
            assert (
                (down_state[coordinate] >> down_edge) & 1
            ) == ((up_state[coordinate] >> up_edge) & 1)
    assert 0 in defect_profile(vertex_count + 4, up_edges, up_state)


def open_text(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="ascii", newline="")
    return path.open("rt", encoding="ascii", newline="")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus", type=Path, nargs="+")
    parser.add_argument("--geng")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=4060)
    arguments = parser.parse_args()
    assert 0 <= arguments.start <= arguments.end <= 4060

    records = canonical_records(arguments.geng)
    graphs = tuple(decode_graph6(record) for record in records)
    all_retained = {
        graph_index
        for graph_index, graph in enumerate(graphs)
        if is_three_edge_connected(*graph)
    }
    assert len(all_retained) == EXPECTED_RETAINED
    retained = {
        graph_index
        for graph_index in all_retained
        if arguments.start <= graph_index < arguments.end
    }

    # A compact bit set avoids retaining millions of Python pair tuples.
    # Bit ``first * 24 + second`` represents one eligible edge pair.
    seen: dict[tuple[int, int], int] = {}
    checked_down: set[tuple[int, int, int, int, int]] = set()
    corpus_digest = hashlib.sha256()
    witness_count = 0
    for path in arguments.corpus:
        with open_text(path) as handle:
            for raw_line in handle:
                corpus_digest.update(raw_line.encode("ascii"))
                fields = raw_line.rstrip("\n").split("\t")
                assert len(fields) == 12 and fields[0] == "W", fields[:2]
                graph_index = int(fields[1])
                record = fields[2]
                root = int(fields[3])
                pair = (int(fields[4]), int(fields[5]))
                down_state = tuple(map(int, fields[6:9]))
                up_state = tuple(map(int, fields[9:12]))
                assert graph_index in retained
                assert 0 <= root < 16
                key = (graph_index, root)
                pair_bit = 1 << (pair[0] * 24 + pair[1])
                bucket = seen.setdefault(key, 0)
                assert not bucket & pair_bit, (key, pair)
                check_witness(
                    graph_index,
                    record,
                    root,
                    pair,
                    down_state,
                    up_state,
                    records,
                    graphs,
                    checked_down,
                )
                seen[key] = bucket | pair_bit
                witness_count += 1

    expected_keys = {
        (graph_index, root)
        for graph_index in retained
        for root in range(16)
    }
    assert set(seen) == expected_keys
    for graph_index, root in sorted(expected_keys):
        expected_pair_bits = sum(
            1 << (first * 24 + second)
            for first, second in eligible_pairs(
                graphs[graph_index][1], root
            )
        )
        assert seen[(graph_index, root)] == expected_pair_bits
    assert witness_count == len(retained) * 16 * 171
    print(
        "PASS: independently verified order-16 existential square census:",
        f"range=[{arguments.start},{arguments.end})",
        f"canonical_records={len(records)}",
        f"canonical_sha256={CANONICAL_SHA256}",
        f"3ec_graphs={len(retained)}",
        f"roots={len(expected_keys)}",
        f"witnesses={witness_count}",
        f"distinct_downstairs_states={len(checked_down)}",
        f"corpus_sha256={corpus_digest.hexdigest()}",
    )


if __name__ == "__main__":
    main()
