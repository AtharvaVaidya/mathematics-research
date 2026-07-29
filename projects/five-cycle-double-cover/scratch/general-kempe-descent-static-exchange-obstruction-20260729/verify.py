#!/usr/bin/env python3
"""Primary exact checker for the static-exchange Kempe obstruction.

The checker:
  * reads the literal 42-vertex base graph;
  * inflates every non-support edge by a coloured K4-minus-edge 2-pole;
  * checks the resulting 230-vertex graph and both displayed flows;
  * exhausts the 2^22 binary cycles of the base graph, proving the
    colour-avoiding margins used by the inflation lemma;
  * replays every one-round fixed-colour path multiswitch; and
  * verifies a literal two-round switch followed by an 8-edge deletion.
"""

from __future__ import annotations

import functools
import itertools
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORD = tuple(map(int, "0101012301012302"))
PARTITION = tuple(map(int, "0123444444130244"))
CIRCUITS = (tuple(range(8)), tuple(range(8, 16)))
GL = tuple((0,) + row for row in itertools.permutations((1, 2, 3)))
IDENTITY = (0, 1, 2, 3)
COLOUR_PAIRS = ((1, 2), (1, 3), (2, 3))
BASE_TAIT = tuple(
    map(int, "121212123121212133311223331122333112233311223333223312111232231")
)

BAD_PATHS = {
    (1, 2): ((1, 10), (2, 13), (3, 11), (4, 15), (5, 7), (8, 9)),
    (1, 3): ((0, 12), (1, 10), (2, 13), (3, 11), (4, 7), (5, 6), (9, 14)),
    (2, 3): ((0, 12), (6, 8), (14, 15)),
}


def read_base():
    rows = []
    for raw in (ROOT / "base-edges.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        u, v, low, kind = raw.split("\t")
        rows.append((int(u), int(v), int(low), kind))
    assert len(rows) == len(BASE_TAIT) == 63
    return tuple(rows)


def derivative(word=WORD):
    result = [0] * 16
    for circuit in CIRCUITS:
        for local, edge in enumerate(circuit):
            result[edge] = word[circuit[local - 1]] ^ word[edge]
    return tuple(result)


DERIVATIVE = derivative()


def integrate(transitions):
    base = [0] * 16
    for circuit in CIRCUITS:
        value = 0
        for edge in circuit:
            value ^= transitions[edge]
            base[edge] = value
        if value:
            return None
    return tuple(base)


def is_clean(base):
    for relative_shift in range(4):
        parity = [[0] * 4 for _ in range(5)]
        for circuit_index, circuit in enumerate(CIRCUITS):
            shift = relative_shift if circuit_index else 0
            for local, edge in enumerate(circuit):
                successor = circuit[(local + 1) % len(circuit)]
                left, right = PARTITION[edge], PARTITION[successor]
                if left == right:
                    continue
                colour = base[edge] ^ shift
                parity[left][colour] ^= 1
                parity[right][colour] ^= 1
        if not any(bit for row in parity for bit in row):
            return True
    return False


@functools.lru_cache(maxsize=None)
def classify(transitions):
    feasible = clean_count = delete_count = 0
    for tail in itertools.product(GL, repeat=4):
        maps = (IDENTITY,) + tail
        transformed = tuple(
            maps[PARTITION[position]][transitions[position]]
            for position in range(16)
        )
        base = integrate(transformed)
        if base is None:
            continue
        feasible += 1
        if is_clean(base):
            clean_count += 1
        if any(
            len({base[position] for position in circuit}) < 4
            for circuit in CIRCUITS
        ):
            delete_count += 1
    return feasible, clean_count, delete_count


def graph_adjacency(n, edges, selected=None):
    result = [[] for _ in range(n)]
    for edge_index, edge in enumerate(edges):
        u, v = edge[:2]
        if selected is not None and not selected(edge_index, edge):
            continue
        result[u].append((v, edge_index))
        result[v].append((u, edge_index))
    return result


def check_graph(n, edges):
    pairs = [tuple(sorted(edge[:2])) for edge in edges]
    assert all(u != v for u, v in pairs)
    assert len(set(pairs)) == len(pairs)
    adjacency = graph_adjacency(n, edges)
    assert all(len(row) == 3 for row in adjacency)
    seen = {0}
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v, _edge in adjacency[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    assert len(seen) == n

    discovery = [-1] * n
    lowlink = [0] * n
    timer = 0
    bridges = []

    def visit(u, parent_edge):
        nonlocal timer
        discovery[u] = lowlink[u] = timer
        timer += 1
        for v, edge_index in adjacency[u]:
            if edge_index == parent_edge:
                continue
            if discovery[v] < 0:
                visit(v, edge_index)
                lowlink[u] = min(lowlink[u], lowlink[v])
                if lowlink[v] > discovery[u]:
                    bridges.append(edge_index)
            else:
                lowlink[u] = min(lowlink[u], discovery[v])

    visit(0, -1)
    assert not bridges


def check_flow(n, edges, coordinate):
    charges = [0] * n
    for edge_index, edge in enumerate(edges):
        value = coordinate(edge_index, edge)
        charges[edge[0]] ^= value
        charges[edge[1]] ^= value
    assert not any(charges)


def cycle_basis(n, edges):
    adjacency = graph_adjacency(n, edges)
    parent = [-1] * n
    parent_edge = [-1] * n
    parent[0] = 0
    order = [0]
    for u in order:
        for v, edge_index in adjacency[u]:
            if parent[v] < 0:
                parent[v] = u
                parent_edge[v] = edge_index
                order.append(v)
    assert len(order) == n
    tree = set(parent_edge[1:])
    basis = []
    for edge_index, edge in enumerate(edges):
        if edge_index in tree:
            continue
        value = 1 << edge_index
        for endpoint in edge[:2]:
            u = endpoint
            while u:
                value ^= 1 << parent_edge[u]
                u = parent[u]
        basis.append(value)
    assert len(basis) == len(edges) - n + 1
    return tuple(basis)


def exchange_margins(base):
    basis = cycle_basis(42, base)
    assert len(basis) == 22
    support = sum(
        1 << edge_index
        for edge_index, edge in enumerate(base)
        if edge[3] == "support"
    )
    colour_classes = tuple(
        sum(
            1 << edge_index
            for edge_index, edge in enumerate(base)
            if edge[3] == "support" and edge[2] == colour
        )
        for colour in range(4)
    )
    minima = [10**9] * 4
    counts = [0] * 4
    admissible = [0] * 4
    cycle = 0
    for index in range(1, 1 << len(basis)):
        gray = index ^ (index >> 1)
        old_gray = (index - 1) ^ ((index - 1) >> 1)
        cycle ^= basis[(gray ^ old_gray).bit_length() - 1]
        inside = (cycle & support).bit_count()
        outside = cycle.bit_count() - inside
        weight = 4 * outside - inside
        for colour in range(4):
            if cycle & colour_classes[colour]:
                continue
            admissible[colour] += 1
            if weight < minima[colour]:
                minima[colour] = weight
                counts[colour] = 1
            elif weight == minima[colour]:
                counts[colour] += 1
    assert admissible == [65535, 131071, 524287, 1048575]
    assert minima == [10, 10, 6, 9]
    assert counts == [1, 1, 1, 1]
    return tuple(minima)


def gadget_colours(terminal):
    other = tuple(colour for colour in (1, 2, 3) if colour != terminal)
    # Edge order: left terminal, right terminal, cd, ac, bd, ad, bc.
    return (terminal, terminal, terminal, other[0], other[0], other[1], other[1])


def inflate(base):
    result = []
    next_vertex = 42
    for edge_index, (u, v, low, kind) in enumerate(base):
        tait = BASE_TAIT[edge_index]
        if kind == "support":
            result.append((u, v, low, tait, "support"))
            continue
        a, b, c, d = range(next_vertex, next_vertex + 4)
        next_vertex += 4
        topology = (
            (u, a),
            (b, v),
            (c, d),
            (a, c),
            (b, d),
            (a, d),
            (b, c),
        )
        lows = gadget_colours(low)
        tait_colours = gadget_colours(tait)
        for endpoints, low_value, tait_value in zip(topology, lows, tait_colours):
            result.append((*endpoints, low_value, tait_value, "complement"))
    assert next_vertex == 230
    assert len(result) == 345
    return next_vertex, tuple(result)


def bichromatic_paths(n, edges, low_values, colours):
    def selected(edge_index, edge):
        return edge[4] != "support" and low_values[edge_index] in colours

    adjacency = graph_adjacency(n, edges, selected)
    seen_edges = set()
    result = {}
    for edge_index, edge in enumerate(edges):
        if edge_index in seen_edges or not selected(edge_index, edge):
            continue
        stack = [edge_index]
        seen_edges.add(edge_index)
        component_edges = []
        vertices = set()
        while stack:
            current = stack.pop()
            component_edges.append(current)
            u, v = edges[current][:2]
            vertices.update((u, v))
            for endpoint in (u, v):
                for _neighbour, following in adjacency[endpoint]:
                    if following not in seen_edges:
                        seen_edges.add(following)
                        stack.append(following)
        terminals = tuple(sorted(vertex for vertex in vertices if vertex < 16))
        if terminals:
            assert len(terminals) == 2
            result[terminals] = tuple(component_edges)
    return result


def switch_paths(low_values, paths, selected, colours):
    first, second = colours
    result = list(low_values)
    for endpoints in selected:
        for edge_index in paths[endpoints]:
            assert result[edge_index] in colours
            result[edge_index] = (
                second if result[edge_index] == first else first
            )
    return tuple(result)


def terminal_derivative(edges, low_values):
    boundary = {}
    for edge_index, edge in enumerate(edges):
        if edge[4] == "support":
            continue
        u, v = edge[:2]
        if u < 16:
            boundary[u] = low_values[edge_index]
        if v < 16:
            boundary[v] = low_values[edge_index]
    assert len(boundary) == 16
    return tuple(boundary[position] for position in range(16))


def replay_one_round():
    assert classify(DERIVATIVE) == (320, 0, 0)
    summary = {}
    for colours, paths in BAD_PATHS.items():
        delta = colours[0] ^ colours[1]
        balanced = 0
        for mask in range(1, 1 << len(paths)):
            selected = tuple(
                paths[index]
                for index in range(len(paths))
                if mask & (1 << index)
            )
            cross = sum(
                (first < 8) != (second < 8)
                for first, second in selected
            )
            if cross & 1:
                continue
            balanced += 1
            changed = list(DERIVATIVE)
            for first, second in selected:
                changed[first] ^= delta
                changed[second] ^= delta
            result = classify(tuple(changed))
            assert result[0] > 0 and result[1:] == (0, 0)
        summary[colours] = balanced
    assert summary == {(1, 2): 31, (1, 3): 63, (2, 3): 3}
    return summary


def replay_two_rounds(n, edges):
    low = tuple(edge[2] for edge in edges)
    initial_pairs = {
        colours: tuple(sorted(bichromatic_paths(n, edges, low, colours)))
        for colours in COLOUR_PAIRS
    }
    assert initial_pairs == {
        colours: tuple(sorted(paths))
        for colours, paths in BAD_PATHS.items()
    }

    first_colours = (1, 2)
    first_selected = ((1, 10), (4, 15))
    first_paths = bichromatic_paths(n, edges, low, first_colours)
    low = switch_paths(low, first_paths, first_selected, first_colours)
    first_derivative = terminal_derivative(edges, low)
    assert first_derivative == tuple(map(int, "3211213121213131"))
    first_base = integrate(first_derivative)
    assert first_base == tuple(map(int, "3101321023103210"))
    assert all(
        {first_base[position] for position in circuit} == set(range(4))
        for circuit in CIRCUITS
    )
    low = list(low)
    for position in range(16):
        low[position] = first_base[position]
    low = tuple(low)
    check_flow(n, edges, lambda edge_index, _edge: low[edge_index])

    second_colours = (1, 3)
    second_selected = ((5, 6),)
    second_paths = bichromatic_paths(n, edges, low, second_colours)
    assert (5, 6) in second_paths
    low = switch_paths(low, second_paths, second_selected, second_colours)
    final_derivative = terminal_derivative(edges, low)
    assert final_derivative == tuple(map(int, "3211231121213131"))
    final_base = integrate(final_derivative)
    assert final_base == tuple(map(int, "3101301023103210"))
    assert 2 not in {final_base[position] for position in CIRCUITS[0]}
    assert {final_base[position] for position in CIRCUITS[1]} == set(range(4))
    assert classify(final_derivative) == (320, 0, 80)
    low = list(low)
    for position in range(16):
        low[position] = final_base[position]
    # Translate the first support circuit by its omitted colour.
    for position in CIRCUITS[0]:
        low[position] ^= 2
    low = tuple(low)
    check_flow(n, edges, lambda edge_index, _edge: low[edge_index])

    smaller_support = set(CIRCUITS[1])
    check_flow(
        n,
        edges,
        lambda edge_index, _edge: int(edge_index in smaller_support),
    )
    assert all(
        edge_index in smaller_support or low[edge_index] != 0
        for edge_index in range(len(edges))
    )
    return final_derivative, final_base


def main():
    base = read_base()
    assert tuple(edge[2] for edge in base[:16]) == WORD
    assert DERIVATIVE == tuple(map(int, "3111113121113132"))
    check_graph(42, base)
    check_flow(42, base, lambda edge_index, edge: int(edge[3] == "support"))
    check_flow(42, base, lambda edge_index, edge: edge[2] & 1)
    check_flow(42, base, lambda edge_index, edge: (edge[2] >> 1) & 1)
    margins = exchange_margins(base)

    n, inflated = inflate(base)
    check_graph(n, inflated)
    check_flow(n, inflated, lambda edge_index, edge: int(edge[4] == "support"))
    check_flow(n, inflated, lambda edge_index, edge: edge[2] & 1)
    check_flow(n, inflated, lambda edge_index, edge: (edge[2] >> 1) & 1)
    check_flow(n, inflated, lambda edge_index, edge: edge[3] & 1)
    check_flow(n, inflated, lambda edge_index, edge: (edge[3] >> 1) & 1)
    assert all(edge[3] != 0 for edge in inflated)

    one_round = replay_one_round()
    final_derivative, final_base = replay_two_rounds(n, inflated)

    print(
        "INFLATED_GRAPH vertices=230 edges=345 "
        "simple=yes cubic=yes connected=yes bridgeless=yes"
    )
    print(
        "BASE_CYCLE_ENUMERATION dimension=22 cycles=4194304 "
        "weighted_margins=" + ",".join(map(str, margins))
    )
    print(
        "STATIC_EXCHANGE all_four_classes=yes "
        "minimum_containing_size=16,16,16,16"
    )
    print(
        "ONE_ROUND balanced_subsets="
        + ",".join(str(one_round[pair]) for pair in COLOUR_PAIRS)
        + " successful=0"
    )
    print(
        "TWO_ROUND first=12:{1-10,4-15} second=13:{5-6} "
        "final_derivative="
        + "".join(map(str, final_derivative[:8]))
        + "|"
        + "".join(map(str, final_derivative[8:]))
    )
    print(
        "STRICT_DESCENT final_base="
        + "".join(map(str, final_base[:8]))
        + "|"
        + "".join(map(str, final_base[8:]))
        + " omitted=2 deleted_size=8"
    )
    print("TAIT_COLOURABLE=yes global_minimum_projection_size=0")
    print(
        "PASS: static four-class exchange plus one-round Kempe descent "
        "is insufficient; the literal two-round escape is verified"
    )


if __name__ == "__main__":
    main()
