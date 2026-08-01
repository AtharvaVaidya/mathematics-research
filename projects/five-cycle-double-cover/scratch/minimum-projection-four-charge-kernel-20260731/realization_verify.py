#!/usr/bin/env python3
"""Build and audit a cubic realization of the four-charge counterstate."""

from __future__ import annotations

from collections import Counter, defaultdict, deque
import itertools
import json


MAPS = tuple((0,) + p for p in itertools.permutations((1, 2, 3)))
IDENTITY = (0, 1, 2, 3)
PAIR_EDGES = tuple((a, b) for a in range(5) for b in range(a + 1, 5))
TERMS = (
    (),
    (),
    (),
    (),
    (),
    (),
    ((3, 1),),
    (),
    ((2, 1),),
    ((1, 1),),
)


def build_words():
    first = [(block, 1) for block in range(4)]
    for (left, right), terms in zip(PAIR_EDGES, TERMS, strict=True):
        for x, y in terms:
            first.extend(((right, x), (left, y), (right, x), (left, y)))
    return tuple(first), tuple((block, 1) for block in range(4))


WORDS = build_words()
CIRCUIT_OFFSETS = (0, len(WORDS[0]))
SUPPORT_SIZE = sum(map(len, WORDS))
RING_STARTS = (0, 2, 2, 2, 3)

# In the first four blocks, global occurrence order works.  Block 4 needs
# this permutation to keep every edge of its complementary ring nonzero.
BLOCK4_ORDER = (4, 0, 2, 3, 1, 5)

# One independently found proper 3-edge-colouring in the edge order built
# below.  It certifies a nowhere-zero low flow and hence projection zero.
THREE_EDGE_COLOURING = (
    "323232323232323232321111132321111323211113232111111323232"
)


def source_occurrences():
    result = []
    for circuit, word in enumerate(WORDS):
        for index, (block, derivative) in enumerate(word):
            result.append((circuit, index, block, derivative))
    return tuple(result)


OCCURRENCES = source_occurrences()


def build_graph():
    """Return edges as (u,v,low,high,block,role)."""
    edges = []
    offset = 0
    for word in WORDS:
        current = 0
        length = len(word)
        for index, (_block, derivative) in enumerate(word):
            current ^= derivative
            edges.append(
                (offset + index, offset + (index + 1) % length,
                 current, 1, None, "support")
            )
        assert current == 0
        offset += length

    terminals = {
        block: [
            occurrence
            for occurrence, row in enumerate(OCCURRENCES)
            if row[2] == block
        ]
        for block in range(5)
    }
    terminals[4] = [terminals[4][index] for index in BLOCK4_ORDER]

    next_vertex = SUPPORT_SIZE
    for block in range(5):
        rows = terminals[block]
        if len(rows) == 2:
            assert OCCURRENCES[rows[0]][3] == OCCURRENCES[rows[1]][3]
            edges.append(
                (rows[0], rows[1], OCCURRENCES[rows[0]][3], 0,
                 block, "pair")
            )
            continue
        internal = tuple(range(next_vertex, next_vertex + len(rows)))
        next_vertex += len(rows)
        ring_values = []
        current = RING_STARTS[block]
        for terminal in rows:
            derivative = OCCURRENCES[terminal][3]
            edges.append(
                (terminal, internal[len(ring_values)], derivative, 0,
                 block, "spoke")
            )
            current ^= derivative
            ring_values.append(current)
        assert current == RING_STARTS[block] and all(ring_values)
        for index, value in enumerate(ring_values):
            edges.append(
                (internal[index], internal[(index + 1) % len(internal)],
                 value, 0, block, "ring")
            )

    return tuple(edges), next_vertex, terminals


EDGES, VERTEX_COUNT, TERMINALS = build_graph()


def connected(edge_rows, deleted=None):
    adjacency = [[] for _ in range(VERTEX_COUNT)]
    for edge_index, row in enumerate(edge_rows):
        if edge_index == deleted:
            continue
        left, right = row[:2]
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = {0}
    queue = deque((0,))
    while queue:
        vertex = queue.popleft()
        for following in adjacency[vertex]:
            if following not in seen:
                seen.add(following)
                queue.append(following)
    return len(seen) == VERTEX_COUNT


def audit_graph_and_flow():
    assert VERTEX_COUNT == 38 and len(EDGES) == 57
    unordered = [tuple(sorted(row[:2])) for row in EDGES]
    assert all(left != right for left, right in unordered)
    assert len(set(unordered)) == len(unordered)
    degree = [0] * VERTEX_COUNT
    flow_xor = [0] * VERTEX_COUNT
    for left, right, low, high, _block, _role in EDGES:
        degree[left] += 1
        degree[right] += 1
        value = low | (high << 2)
        assert value
        flow_xor[left] ^= value
        flow_xor[right] ^= value
    assert set(degree) == {3}
    assert not any(flow_xor)
    assert connected(EDGES)
    bridgeless_checks = 0
    for edge_index in range(len(EDGES)):
        assert connected(EDGES, edge_index)
        bridgeless_checks += 1

    # Recover the five complement components and their boundary owners.
    complement = [row for row in EDGES if row[5] != "support"]
    adjacency = [[] for _ in range(VERTEX_COUNT)]
    for left, right, *_rest in complement:
        adjacency[left].append(right)
        adjacency[right].append(left)
    unseen = set(range(VERTEX_COUNT))
    components = []
    while unseen:
        root = next(iter(unseen))
        if not adjacency[root]:
            unseen.remove(root)
            continue
        seen = {root}
        queue = [root]
        while queue:
            vertex = queue.pop()
            for following in adjacency[vertex]:
                if following not in seen:
                    seen.add(following)
                    queue.append(following)
        unseen -= seen
        boundary = sorted(vertex for vertex in seen if vertex < SUPPORT_SIZE)
        components.append(boundary)
    assert sorted(components) == sorted(map(sorted, TERMINALS.values()))
    return bridgeless_checks


def integrated_sizes(local_maps, changes=None):
    changes = changes or {}
    sizes = []
    offset = 0
    for word in WORDS:
        current = 0
        values = []
        for index, (block, derivative) in enumerate(word):
            current ^= local_maps[block][derivative] ^ changes.get(
                offset + index, 0
            )
            values.append(current)
        if current:
            return None
        sizes.append(len(set(values)))
        offset += len(word)
    return tuple(sizes)


def complement_kempe_paths(local_maps):
    """List (delta,endpoints,block,colours,edge-set) complement paths."""
    paths = []
    for block in range(5):
        edge_indices = [
            index
            for index, row in enumerate(EDGES)
            if row[4] == block
        ]
        for colours in itertools.combinations((1, 2, 3), 2):
            adjacency = defaultdict(list)
            for edge_index in edge_indices:
                left, right, low, _high, _block, _role = EDGES[edge_index]
                if local_maps[block][low] in colours:
                    adjacency[left].append((right, edge_index))
                    adjacency[right].append((left, edge_index))
            unseen = set(adjacency)
            while unseen:
                root = next(iter(unseen))
                vertices = {root}
                used_edges = set()
                queue = [root]
                while queue:
                    vertex = queue.pop()
                    for following, edge_index in adjacency[vertex]:
                        used_edges.add(edge_index)
                        if following not in vertices:
                            vertices.add(following)
                            queue.append(following)
                unseen -= vertices
                endpoints = tuple(sorted(v for v in vertices if v < SUPPORT_SIZE))
                assert len(endpoints) in (0, 2)
                if endpoints:
                    paths.append(
                        (
                            colours[0] ^ colours[1],
                            endpoints,
                            block,
                            colours,
                            frozenset(used_edges),
                        )
                    )
    return tuple(paths)


def circuit_of(occurrence):
    return 0 if occurrence < CIRCUIT_OFFSETS[1] else 1


def audit_switched_flow_and_deletion(local_maps, selected_paths):
    changes = {}
    for path in selected_paths:
        delta, endpoints, _block, _colours, _edge_set = path
        for endpoint in endpoints:
            changes[endpoint] = changes.get(endpoint, 0) ^ delta

    low_values = [0] * len(EDGES)
    circuit_edge_values = []
    edge_offset = 0
    occurrence_offset = 0
    for word in WORDS:
        current = 0
        values = []
        for index, (block, derivative) in enumerate(word):
            current ^= local_maps[block][derivative] ^ changes.get(
                occurrence_offset + index, 0
            )
            low_values[edge_offset + index] = current
            values.append(current)
        assert current == 0
        circuit_edge_values.append(tuple(values))
        edge_offset += len(word)
        occurrence_offset += len(word)
    for edge_index, row in enumerate(EDGES[SUPPORT_SIZE:], SUPPORT_SIZE):
        low_values[edge_index] = local_maps[row[4]][row[2]]

    for path in selected_paths:
        _delta, _endpoints, _block, colours, edge_set = path
        for edge_index in edge_set:
            assert low_values[edge_index] in colours
            low_values[edge_index] ^= colours[0] ^ colours[1]

    vertex_xor = [0] * VERTEX_COUNT
    for low, (left, right, *_rest) in zip(low_values, EDGES, strict=True):
        vertex_xor[left] ^= low
        vertex_xor[right] ^= low
    assert not any(vertex_xor)
    assert all(low_values[index] for index in range(SUPPORT_SIZE, len(EDGES)))

    deleted_circuit = next(
        circuit
        for circuit, values in enumerate(circuit_edge_values)
        if len(set(values)) < 4
    )
    missing = next(
        value
        for value in range(4)
        if value not in circuit_edge_values[deleted_circuit]
    )
    high_values = [row[3] for row in EDGES]
    start = CIRCUIT_OFFSETS[deleted_circuit]
    stop = start + len(WORDS[deleted_circuit])
    for edge_index in range(start, stop):
        low_values[edge_index] ^= missing
        high_values[edge_index] = 0

    full_xor = [0] * VERTEX_COUNT
    for low, high, (left, right, *_rest) in zip(
        low_values, high_values, EDGES, strict=True
    ):
        value = low | high << 2
        assert value
        full_xor[left] ^= value
        full_xor[right] ^= value
    assert not any(full_xor)
    return deleted_circuit, missing


def deletion_or_kempe_census():
    census = Counter()
    move_signatures = Counter()
    feasible = 0
    for tail in itertools.product(MAPS, repeat=4):
        local_maps = (IDENTITY,) + tail
        charges = tuple(local_maps[block][1] for block in range(4))
        if charges[0] ^ charges[1] ^ charges[2] ^ charges[3]:
            continue
        feasible += 1
        sizes = integrated_sizes(local_maps)
        assert sizes is not None
        if min(sizes) < 4:
            audit_switched_flow_and_deletion(local_maps, ())
            census["direct_deletion"] += 1
            continue

        paths = complement_kempe_paths(local_maps)
        witness = None
        for path in paths:
            delta, endpoints, block, colours, _edge_set = path
            if circuit_of(endpoints[0]) != circuit_of(endpoints[1]):
                continue
            after = integrated_sizes(
                local_maps, {endpoints[0]: delta, endpoints[1]: delta}
            )
            if after is not None and min(after) < 4:
                witness = (path, None, after)
                break
        if witness is None:
            cross_paths = [
                path
                for path in paths
                if circuit_of(path[1][0]) != circuit_of(path[1][1])
            ]
            for first, second in itertools.combinations(cross_paths, 2):
                if first[0] != second[0] or first[4] & second[4]:
                    continue
                changes = {
                    endpoint: first[0]
                    for endpoint in first[1] + second[1]
                }
                after = integrated_sizes(local_maps, changes)
                if after is not None and min(after) < 4:
                    witness = (first, second, after)
                    break
        assert witness is not None
        census["kempe_then_deletion"] += 1
        first, second, after = witness
        selected_paths = (first,) if second is None else (first, second)
        audit_switched_flow_and_deletion(local_maps, selected_paths)
        signature = (
            first[2], first[3], first[1],
            None if second is None else (second[2], second[3], second[1]),
            after,
        )
        move_signatures[repr(signature)] += 1

    assert feasible == 336
    assert census == Counter(
        {"direct_deletion": 240, "kempe_then_deletion": 96}
    )
    return census, move_signatures


def audit_empty_projection_certificate():
    colours = tuple(map(int, THREE_EDGE_COLOURING))
    assert len(colours) == len(EDGES) and set(colours) == {1, 2, 3}
    incident = [[] for _ in range(VERTEX_COUNT)]
    for colour, (left, right, *_rest) in zip(colours, EDGES, strict=True):
        incident[left].append(colour)
        incident[right].append(colour)
    assert all(sorted(row) == [1, 2, 3] for row in incident)
    return len(colours)


def main():
    bridge_checks = audit_graph_and_flow()
    deletion_census, move_signatures = deletion_or_kempe_census()
    colouring_edges = audit_empty_projection_certificate()
    print(
        json.dumps(
            {
                "status": "VERIFIED_CUBIC_REALIZATION_AND_DESCENT",
                "vertices": VERTEX_COUNT,
                "edges": len(EDGES),
                "simple": True,
                "cubic": True,
                "connected": True,
                "bridgeless_edge_deletion_checks": bridge_checks,
                "displayed_projection_size": SUPPORT_SIZE,
                "complement_blocks": 5,
                "gauge_integrable_component_maps": 336,
                "deletion_census": deletion_census,
                "kempe_move_signatures": move_signatures,
                "three_edge_colouring_edges_checked": colouring_edges,
                "global_minimum_projection_size": 0,
                "minimum_clean_descendant": [],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
