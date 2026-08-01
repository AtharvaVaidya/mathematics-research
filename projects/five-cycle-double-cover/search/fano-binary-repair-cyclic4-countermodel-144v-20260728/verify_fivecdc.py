#!/usr/bin/env python3
"""Independent stdlib verifier for an explicit five-cycle double cover.

The witness numbers the graph's undirected edges lexicographically from zero.
For each C_i it then lists the edge IDs in that Eulerian edge subset.
"""

import collections
import hashlib
import pathlib
import sys


def fail(message):
    raise SystemExit("INVALID: " + message)


def decode_graph6(text):
    data = [ord(character) - 63 for character in text.strip()]
    if not data or any(value < 0 or value > 63 for value in data):
        fail("bad graph6 alphabet")
    position = 0
    if data[position] != 63:
        n = data[position]
        position += 1
    else:
        position += 1
        if position >= len(data):
            fail("truncated graph6 header")
        if data[position] != 63:
            if position + 3 > len(data):
                fail("truncated medium graph6 header")
            n = (data[position] << 12) | (data[position + 1] << 6)
            n |= data[position + 2]
            position += 3
        else:
            position += 1
            if position + 6 > len(data):
                fail("truncated large graph6 header")
            n = 0
            for value in data[position : position + 6]:
                n = (n << 6) | value
            position += 6
    bits = []
    for value in data[position:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    if len(bits) < needed:
        fail("truncated graph6 adjacency data")
    if any(bits[needed:]):
        fail("nonzero graph6 padding")
    edges = []
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return n, sorted(edges)


def parse_witness(path):
    raw = pathlib.Path(path).read_bytes()
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError:
        fail("witness is not ASCII")
    if not lines or lines[0] != "FIVECDC-WITNESS-V1":
        fail("wrong witness header")
    fields = {}
    for line in lines[1:]:
        if "=" not in line:
            fail("malformed line")
        key, value = line.split("=", 1)
        if key in fields:
            fail("duplicate field " + key)
        fields[key] = value
    expected = {
        "graph6",
        "n",
        "m",
        "edge_order",
        "edges",
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
    }
    if set(fields) != expected:
        fail("field set differs: " + repr(sorted(set(fields) ^ expected)))
    if fields["edge_order"] != "lexicographic_zero_based":
        fail("unsupported edge order")
    try:
        declared_edges = []
        if fields["edges"]:
            for item in fields["edges"].split(","):
                left, right = item.split("-")
                declared_edges.append((int(left), int(right)))
        cycles = []
        for index in range(1, 6):
            value = fields["C" + str(index)]
            cycles.append([] if not value else [int(x) for x in value.split(",")])
        declared_n = int(fields["n"])
        declared_m = int(fields["m"])
    except (ValueError, TypeError):
        fail("bad integer or edge token")
    return raw, fields["graph6"], declared_n, declared_m, declared_edges, cycles


def graph6_from_state(path):
    lines = pathlib.Path(path).read_text(encoding="ascii").splitlines()
    if lines and lines[0].startswith("~"):
        return lines[0]
    for line in lines:
        if line.startswith("graph6="):
            return line[7:]
    fail("host state has no graph6 field")


def component_sizes(n, edges, edge_ids):
    adjacency = [[] for _ in range(n)]
    active = set()
    for edge_id in edge_ids:
        left, right = edges[edge_id]
        adjacency[left].append(right)
        adjacency[right].append(left)
        active.add(left)
        active.add(right)
    answer = []
    while active:
        start = next(iter(active))
        queue = [start]
        active.remove(start)
        size = 0
        for vertex in queue:
            size += 1
            for other in adjacency[vertex]:
                if other in active:
                    active.remove(other)
                    queue.append(other)
        answer.append(size)
    return sorted(answer)


def main():
    if len(sys.argv) not in (2, 3):
        raise SystemExit(
            "usage: verify_fivecdc.py WITNESS [FROZEN_HOST_STATE]"
        )
    raw, graph6, declared_n, declared_m, declared_edges, cycles = parse_witness(
        sys.argv[1]
    )
    if len(sys.argv) == 3 and graph6 != graph6_from_state(sys.argv[2]):
        fail("witness graph6 differs from frozen host state")
    n, edges = decode_graph6(graph6)
    m = len(edges)
    if (declared_n, declared_m) != (n, m):
        fail("declared n or m does not match graph6")
    if declared_edges != edges:
        fail("explicit edge table does not match graph6")
    if len(set(edges)) != m or any(left >= right for left, right in edges):
        fail("edge table is not a simple undirected graph")
    incidence = [[] for _ in range(n)]
    for edge_id, (left, right) in enumerate(edges):
        incidence[left].append(edge_id)
        incidence[right].append(edge_id)
    if any(len(row) != 3 for row in incidence):
        fail("host graph is not cubic")

    multiplicity = [0] * m
    component_data = []
    for cycle_index, edge_ids in enumerate(cycles, 1):
        if edge_ids != sorted(edge_ids):
            fail("C%d is not in increasing order" % cycle_index)
        if len(set(edge_ids)) != len(edge_ids):
            fail("C%d repeats an edge" % cycle_index)
        if any(edge_id < 0 or edge_id >= m for edge_id in edge_ids):
            fail("C%d has an out-of-range edge" % cycle_index)
        degree = [0] * n
        for edge_id in edge_ids:
            multiplicity[edge_id] += 1
            left, right = edges[edge_id]
            degree[left] += 1
            degree[right] += 1
        odd = [vertex for vertex, value in enumerate(degree) if value % 2]
        if odd:
            fail("C%d is not Eulerian; odd vertices %r" % (cycle_index, odd))
        component_data.append(component_sizes(n, edges, edge_ids))
    bad = [(edge, count) for edge, count in enumerate(multiplicity) if count != 2]
    if bad:
        fail("edge multiplicities are not all two: " + repr(bad[:10]))

    graph_adjacency = [[] for _ in range(n)]
    for left, right in edges:
        graph_adjacency[left].append(right)
        graph_adjacency[right].append(left)
    seen = {0}
    queue = [0]
    for vertex in queue:
        for other in graph_adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                queue.append(other)
    if len(seen) != n:
        fail("host graph is disconnected")

    print("VALID FIVE-CYCLE DOUBLE COVER")
    print("host: n=%d m=%d simple=true cubic=true connected=true" % (n, m))
    print("cycle edge counts:", [len(cycle) for cycle in cycles])
    print("nontrivial component vertex counts:", component_data)
    print("every vertex degree is even in every C_i")
    print("every edge multiplicity is exactly 2")
    print("witness_sha256=" + hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
