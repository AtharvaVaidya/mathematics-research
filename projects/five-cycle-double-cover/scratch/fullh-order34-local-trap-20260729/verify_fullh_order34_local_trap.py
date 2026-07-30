#!/usr/bin/env python3
"""Independent semantic replay of the order-34 full-H local trap.

This checker does not call the C++ audit.  It parses graph6, rebuilds the
binary cycle space, evaluates the full-H linear systems, enumerates the
entire legal one-move neighbourhood, and checks the explicit FiveCDC.
"""

from collections import deque
from itertools import combinations
import json
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "fullh-order34-local-trap-certificate.jsonl"
PLANES = (0x0F, 0x33, 0x55, 0x69, 0x99, 0xA5, 0xC3)
FNV_OFFSET = 1469598103934665603
FNV_PRIME = 1099511628211
WORD_MASK = (1 << 64) - 1


def parse_graph6(record):
    """Parse short graph6 directly, retaining graph6's edge order."""
    record = record.strip()
    if record.startswith(">>graph6<<"):
        record = record[10:]
    n = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        chunk = ord(character) - 63
        bits.extend((chunk >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return n, tuple(edges)


def incidence(n, edges):
    answer = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        answer[left].append(edge)
        answer[right].append(edge)
    return answer


def other_endpoint(edges, edge, vertex):
    left, right = edges[edge]
    return right if left == vertex else left


def flow_rank(flow):
    pivots = {}
    for original in flow:
        value = original
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    return len(pivots)


def boundary(edges, selected):
    result = 0
    for edge in selected:
        left, right = edges[edge]
        result ^= 1 << left
        result ^= 1 << right
    return result


def in_span(target, columns):
    pivots = {}
    for original in columns:
        value = original
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    while target:
        pivot = target.bit_length() - 1
        if pivot not in pivots:
            return False
        target ^= pivots[pivot]
    return True


def full_h_success(n, edges, inc, flow, plane_mask):
    in_plane = tuple(
        edge for edge, value in enumerate(flow)
        if (plane_mask >> value) & 1
    )
    outside = tuple(
        edge for edge, value in enumerate(flow)
        if not ((plane_mask >> value) & 1)
    )

    component = [-1] * n
    h_inc = [[] for _ in range(n)]
    for edge in in_plane:
        left, right = edges[edge]
        h_inc[left].append(right)
        h_inc[right].append(left)
    component_count = 0
    for start in range(n):
        if component[start] >= 0:
            continue
        component[start] = component_count
        stack = [start]
        while stack:
            vertex = stack.pop()
            for other in h_inc[vertex]:
                if component[other] < 0:
                    component[other] = component_count
                    stack.append(other)
        component_count += 1

    outside_inc = [[] for _ in range(n)]
    for edge in outside:
        for vertex in edges[edge]:
            outside_inc[vertex].append(edge)
    circuits = []
    unseen = set(outside)
    while unseen:
        first = next(iter(unseen))
        circuit = set()
        stack = [first]
        while stack:
            edge = stack.pop()
            if edge in circuit:
                continue
            circuit.add(edge)
            for vertex in edges[edge]:
                stack.extend(outside_inc[vertex])
        unseen.difference_update(circuit)
        circuits.append(circuit)

    representative = next(
        value for value in range(1, 8)
        if not ((plane_mask >> value) & 1)
    )

    def contract(vertex_mask):
        result = 0
        for vertex in range(n):
            if (vertex_mask >> vertex) & 1:
                result ^= 1 << component[vertex]
        return result

    beta = contract(boundary(
        edges,
        (edge for edge, value in enumerate(flow)
         if value == representative),
    ))
    columns = []
    for circuit in circuits:
        for increment in range(1, 8):
            if not ((plane_mask >> increment) & 1):
                continue
            columns.append(contract(boundary(
                edges,
                (edge for edge in circuit
                 if flow[edge] in
                 (representative, representative ^ increment)),
            )))
    return in_span(beta, columns)


def success_mask(n, edges, inc, flow):
    return sum(
        (1 << index)
        for index, plane in enumerate(PLANES)
        if full_h_success(n, edges, inc, flow, plane)
    )


def cycle_basis(n, edges, inc):
    parent = [-1] * n
    parent_edge = [-1] * n
    depth = [0] * n
    parent[0] = 0
    stack = [0]
    while stack:
        vertex = stack.pop()
        for edge in inc[vertex]:
            other = other_endpoint(edges, edge, vertex)
            if parent[other] >= 0:
                continue
            parent[other] = vertex
            parent_edge[other] = edge
            depth[other] = depth[vertex] + 1
            stack.append(other)
    tree_edges = set(parent_edge[1:])
    answer = []
    for edge, endpoints in enumerate(edges):
        if edge in tree_edges:
            continue
        left, right = endpoints
        mask = 1 << edge
        while depth[left] > depth[right]:
            mask ^= 1 << parent_edge[left]
            left = parent[left]
        while depth[right] > depth[left]:
            mask ^= 1 << parent_edge[right]
            right = parent[right]
        while left != right:
            mask ^= 1 << parent_edge[left]
            left = parent[left]
            mask ^= 1 << parent_edge[right]
            right = parent[right]
        answer.append(mask)
    return tuple(answer)


def all_cycles(basis):
    cycles = [0]
    for value in basis:
        cycles += [old ^ value for old in cycles]
    return tuple(sorted(cycles))


def move(flow, cycle, increment):
    changed = tuple(
        value ^ increment if (cycle >> edge) & 1 else value
        for edge, value in enumerate(flow)
    )
    return None if 0 in changed else changed


def has_even_complement(n, edges, inc, matching):
    colour = [-1] * n
    for start in range(n):
        if colour[start] >= 0:
            continue
        colour[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for edge in inc[vertex]:
                if (matching >> edge) & 1:
                    continue
                other = other_endpoint(edges, edge, vertex)
                if colour[other] < 0:
                    colour[other] = colour[vertex] ^ 1
                    queue.append(other)
                elif colour[other] == colour[vertex]:
                    return False
    return True


def three_edge_colourable(n, edges, inc):
    """Use the distinct perfect-matching/even-two-factor criterion."""
    all_vertices = (1 << n) - 1

    def search(matched, matching):
        if matched == all_vertices:
            return has_even_complement(n, edges, inc, matching)
        vertex = next(
            index for index in range(n) if not ((matched >> index) & 1)
        )
        for edge in inc[vertex]:
            other = other_endpoint(edges, edge, vertex)
            if (matched >> other) & 1:
                continue
            if search(
                matched | (1 << vertex) | (1 << other),
                matching | (1 << edge),
            ):
                return True
        return False

    return search(0, 0)


def cyclic_cut_size(n, edges):
    def separates(cut):
        removed = set(cut)
        graph = nx.Graph()
        graph.add_nodes_from(range(n))
        graph.add_edges_from(
            endpoints for edge, endpoints in enumerate(edges)
            if edge not in removed
        )
        cyclic = 0
        for vertices in nx.connected_components(graph):
            subgraph = graph.subgraph(vertices)
            if subgraph.number_of_edges() >= subgraph.number_of_nodes():
                cyclic += 1
        return cyclic >= 2

    for size in range(1, 5):
        for cut in combinations(range(len(edges)), size):
            if separates(cut):
                return size, cut
    return None, ()


def main():
    certificate = json.loads(CERTIFICATE.read_text())
    n, edges = parse_graph6(certificate["graph6"])
    inc = incidence(n, edges)
    assert n == 34 and len(edges) == 51
    assert len(set(edges)) == len(edges)
    assert all(left != right for left, right in edges)
    assert all(len(row) == 3 for row in inc)

    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from(edges)
    assert nx.is_connected(graph)
    assert nx.edge_connectivity(graph) >= 2
    assert min(len(cycle) for cycle in nx.cycle_basis(graph)) == 5
    planar, _ = nx.check_planarity(graph)
    assert not planar
    cut_size, cut = cyclic_cut_size(n, edges)
    assert cut_size == 4
    assert tuple(certificate["cyclic_cut_witness"]) == cut

    assert not three_edge_colourable(n, edges, inc)

    flow = tuple(certificate["trap_flow"])
    assert all(1 <= value <= 7 for value in flow)
    assert all(
        flow[inc[vertex][0]]
        ^ flow[inc[vertex][1]]
        ^ flow[inc[vertex][2]] == 0
        for vertex in range(n)
    )
    assert flow_rank(flow) == 3
    assert success_mask(n, edges, inc, flow) == 0

    basis = cycle_basis(n, edges, inc)
    cycles = all_cycles(basis)
    assert len(basis) == 18
    assert len(cycles) == 262_144
    assert all(
        sum((cycle >> edge) & 1 for edge in inc[vertex]) % 2 == 0
        for cycle in cycles
        for vertex in range(n)
    )

    legal_count = 0
    legal_by_increment = [0] * 8
    checksum = FNV_OFFSET
    for cycle in cycles[1:]:
        for increment in range(1, 8):
            changed = move(flow, cycle, increment)
            if changed is None:
                continue
            legal_count += 1
            legal_by_increment[increment] += 1
            assert success_mask(n, edges, inc, changed) == 0
            for value in changed:
                checksum ^= value
                checksum = (checksum * FNV_PRIME) & WORD_MASK
            checksum ^= cycle
            checksum = (checksum * FNV_PRIME) & WORD_MASK
            checksum ^= increment
            checksum = (checksum * FNV_PRIME) & WORD_MASK
    assert legal_count == certificate["legal_moves"] == 19_193
    assert legal_by_increment[1:] == certificate["legal_by_increment"]
    assert f"{checksum:016x}" == certificate["neighbour_checksum_fnv64"]
    assert certificate["successful_neighbours"] == 0

    middle = move(
        flow,
        certificate["escape_first_cycle"],
        certificate["escape_first_increment"],
    )
    assert middle == tuple(certificate["escape_middle_flow"])
    assert success_mask(n, edges, inc, middle) == 0
    final = move(
        middle,
        certificate["escape_second_cycle"],
        certificate["escape_second_increment"],
    )
    assert final == tuple(certificate["escape_final_flow"])
    assert success_mask(n, edges, inc, final) == 64
    assert certificate["shortest_success_distance"] == 2

    labels = tuple(map(tuple, certificate["five_cdc_edge_labels"]))
    assert len(labels) == len(edges)
    assert all(1 <= first < second <= 5 for first, second in labels)
    for vertex in range(n):
        for index in range(1, 6):
            degree = sum(
                index in labels[edge] for edge in inc[vertex]
            )
            assert degree % 2 == 0

    print("PASS: independent order-34 full-H local-trap replay")
    print("graph: simple cubic, nonplanar, girth 5, cyclic connectivity 4")
    print("non-Tait; all 19,193 legal one-move neighbours still fail")
    print("shortest successful full-H distance: 2")
    print("explicit standard FiveCDC: verified")


if __name__ == "__main__":
    main()
