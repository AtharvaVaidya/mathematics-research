#!/usr/bin/env python3
"""Solver-free audit of the retained order-80 binary packing repair.

The graph is the sole order-80 cubic vertex-transitive graph of girth ten
in the retained census.  The first state file supplies a Tait flow.  The
second supplies a sampled nowhere-zero F_2^3-flow, a legal binary switch,
and two disjoint boundary joins after the switch.

This script checks the graph metadata, both flows, the switch and joins,
and constructs and checks the resulting standard five-cycle double cover.
It does not certify that all seven initial value classes are nonpacking or
that all 42 ordered binary-repair queries are satisfiable; those are exact
CaDiCaL search results, not claims in this solver-free certificate.
"""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TAIT_STATE = HERE / "order80-girth10-tait-flow-state.txt"
REPAIR_STATE = HERE / "order80-girth10-binary-repair-state.txt"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parse_csv(line: str) -> tuple[int, ...]:
    return tuple(int(item) for item in line.split(",") if item)


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    require(record.startswith("~") and not record.startswith("~~"),
            "expected the 18-bit extended graph6 header")
    require(len(record) >= 4, "truncated graph6 header")
    order = 0
    for character in record[1:4]:
        value = ord(character) - 63
        require(0 <= value < 64, "invalid graph6 header character")
        order = (order << 6) | value
    bits: list[int] = []
    for character in record[4:]:
        value = ord(character) - 63
        require(0 <= value < 64, "invalid graph6 data character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            require(cursor < len(bits), "truncated graph6 data")
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    require(not any(bits[cursor:]), "nonzero graph6 padding")
    return order, tuple(edges)


def incidence(
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        require(0 <= left < right < order, "unnormalized graph edge")
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


def other_endpoint(edge: tuple[int, int], vertex: int) -> int:
    return edge[0] ^ edge[1] ^ vertex


def check_connected(
    order: int,
    edges: tuple[tuple[int, int], ...],
    rows: tuple[tuple[int, ...], ...],
) -> None:
    reached = {0}
    queue = [0]
    for vertex in queue:
        for edge in rows[vertex]:
            other = other_endpoint(edges[edge], vertex)
            if other not in reached:
                reached.add(other)
                queue.append(other)
    require(len(reached) == order, "graph is disconnected")


def check_flow(
    rows: tuple[tuple[int, ...], ...],
    values: tuple[int, ...],
) -> None:
    require(all(1 <= value <= 7 for value in values),
            "flow has a zero or invalid value")
    require(
        all(values[row[0]] ^ values[row[1]] ^ values[row[2]] == 0
            for row in rows),
        "flow conservation fails",
    )


def exact_girth(
    order: int,
    edges: tuple[tuple[int, int], ...],
    rows: tuple[tuple[int, ...], ...],
) -> int:
    best = order + 1
    for forbidden, (source, target) in enumerate(edges):
        distance = [-1] * order
        distance[source] = 0
        queue = [source]
        for vertex in queue:
            if distance[vertex] + 1 >= best:
                continue
            for edge in rows[vertex]:
                if edge == forbidden:
                    continue
                other = other_endpoint(edges[edge], vertex)
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    queue.append(other)
        if distance[target] >= 0:
            best = min(best, distance[target] + 1)
    require(best <= order, "graph is acyclic")
    return best


def cyclic_components_after_deletion(
    order: int,
    edges: tuple[tuple[int, int], ...],
    rows: tuple[tuple[int, ...], ...],
    deleted: frozenset[int],
) -> int:
    unseen = set(range(order))
    cyclic = 0
    while unseen:
        root = min(unseen)
        component = {root}
        queue = [root]
        edge_ends = 0
        for vertex in queue:
            for edge in rows[vertex]:
                if edge in deleted:
                    continue
                edge_ends += 1
                other = other_endpoint(edges[edge], vertex)
                if other not in component:
                    component.add(other)
                    queue.append(other)
        unseen -= component
        if edge_ends // 2 >= len(component):
            cyclic += 1
    return cyclic


def boundary(
    edges: tuple[tuple[int, int], ...],
    selected: frozenset[int],
) -> frozenset[int]:
    odd: set[int] = set()
    for edge in selected:
        for vertex in edges[edge]:
            if vertex in odd:
                odd.remove(vertex)
            else:
                odd.add(vertex)
    return frozenset(odd)


def quotient_functionals(kernel: int) -> tuple[int, int]:
    annihilators = [
        functional
        for functional in range(1, 8)
        if (functional & kernel).bit_count() % 2 == 0
    ]
    require(len(annihilators) == 3, "wrong annihilator plane")
    first = annihilators[0]
    second = next(value for value in annihilators if value != first)
    require(first ^ second in annihilators, "functionals are dependent")
    return first, second


def construct_five_cdc(
    edges: tuple[tuple[int, int], ...],
    switched: tuple[int, ...],
    target: int,
    red: frozenset[int],
    blue: frozenset[int],
) -> tuple[int, ...]:
    matching = frozenset(
        edge for edge, value in enumerate(switched) if value == target
    )
    union = red | blue
    alpha, beta = quotient_functionals(target)
    section = {1: 0b0011, 2: 0b0101, 3: 0b0110}
    labels = []
    for edge, value in enumerate(switched):
        if edge in matching:
            labels.append(0b00011)
            continue
        quotient = (
            ((alpha & value).bit_count() & 1)
            | (((beta & value).bit_count() & 1) << 1)
        )
        require(quotient in section, "quotient flow vanishes off matching")
        lifted = section[quotient]
        ell = lifted & 1
        h = bool(edge in union) ^ bool(ell)
        if h:
            lifted ^= 0b1111
        require(lifted.bit_count() == 2, "four-cover word has wrong weight")
        label = 0
        if edge in red:
            label |= 1
        if edge in blue:
            label |= 2
        label |= ((lifted >> 1) << 2)
        require(label.bit_count() == 2, "five-cover word has wrong weight")
        labels.append(label)
    return tuple(labels)


def main() -> None:
    tait_lines = TAIT_STATE.read_text(encoding="utf-8").splitlines()
    repair_lines = REPAIR_STATE.read_text(encoding="utf-8").splitlines()
    require(len(tait_lines) == 2, "wrong Tait-state format")
    require(len(repair_lines) == 6, "wrong repair-state format")
    require(tait_lines[0] == repair_lines[0], "state graphs differ")

    order, edges = decode_graph6(repair_lines[0])
    rows = incidence(order, edges)
    require(order == 80 and len(edges) == 120, "wrong graph size")
    require(len(set(edges)) == len(edges), "parallel graph edges")
    require(all(len(row) == 3 for row in rows), "graph is not cubic")
    check_connected(order, edges, rows)

    girth = exact_girth(order, edges, rows)
    require(girth == 10, "wrong girth")
    cut_counts = {}
    for size in range(1, 4):
        count = 0
        for deleted in combinations(range(len(edges)), size):
            if cyclic_components_after_deletion(
                order, edges, rows, frozenset(deleted)
            ) >= 2:
                count += 1
        cut_counts[size] = count
    require(cut_counts == {1: 0, 2: 0, 3: 0},
            "graph has a cyclic cut of size at most three")

    tait = parse_csv(tait_lines[1])
    require(len(tait) == len(edges), "wrong Tait-flow length")
    check_flow(rows, tait)
    require(set(tait) == {1, 2, 3}, "Tait flow uses other values")
    require(all({tait[edge] for edge in row} == {1, 2, 3}
                for row in rows), "Tait colouring is improper")

    flow = parse_csv(repair_lines[1])
    require(len(flow) == len(edges), "wrong sampled-flow length")
    check_flow(rows, flow)
    switch_value, target = parse_csv(repair_lines[2])
    switch = frozenset(parse_csv(repair_lines[3]))
    red = frozenset(parse_csv(repair_lines[4]))
    blue = frozenset(parse_csv(repair_lines[5]))
    require(boundary(edges, switch) == frozenset(),
            "switch support is not even")
    require(all(flow[edge] != switch_value for edge in switch),
            "switch meets its forbidden value class")

    switched = tuple(
        value ^ switch_value if edge in switch else value
        for edge, value in enumerate(flow)
    )
    check_flow(rows, switched)
    matching = frozenset(
        edge for edge, value in enumerate(switched) if value == target
    )
    matching_vertices = [
        vertex
        for vertex, row in enumerate(rows)
        if sum(edge in matching for edge in row)
    ]
    require(all(sum(edge in matching for edge in row) <= 1 for row in rows),
            "target value class is not a matching")
    terminals = frozenset(matching_vertices)
    require(boundary(edges, matching) == terminals,
            "matching boundary differs from its incident vertices")
    require(red.isdisjoint(blue), "packing joins overlap")
    require(red.isdisjoint(matching) and blue.isdisjoint(matching),
            "a packing join meets the matching")
    require(boundary(edges, red) == terminals, "red has wrong boundary")
    require(boundary(edges, blue) == terminals, "blue has wrong boundary")

    labels = construct_five_cdc(edges, switched, target, red, blue)
    require(all(label.bit_count() == 2 for label in labels),
            "cover does not cover every edge twice")
    require(
        all(
            all(sum(bool(labels[edge] & (1 << coordinate))
                    for edge in row) % 2 == 0
                for coordinate in range(5))
            for row in rows
        ),
        "a five-cover coordinate is not Eulerian",
    )

    print(json.dumps({
        "schema": "order80-girth10-binary-repair-audit-v1",
        "solver_independent": True,
        "order": order,
        "edges": len(edges),
        "girth": girth,
        "cyclic_cut_counts_sizes_1_to_3": cut_counts,
        "cyclically_4_edge_connected": True,
        "three_edge_colorable": True,
        "sampled_flow_is_nowhere_zero": True,
        "switch_value": switch_value,
        "target_value": target,
        "switch_edges": sorted(switch),
        "target_matching_size": len(matching),
        "red_join_size": len(red),
        "blue_join_size": len(blue),
        "explicit_standard_five_cdc": True,
        "five_cdc_labels": labels,
        "scope": (
            "positive girth-ten finite control; not a FiveCDC resolution "
            "and not a certificate for the 42-query search statement"
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
