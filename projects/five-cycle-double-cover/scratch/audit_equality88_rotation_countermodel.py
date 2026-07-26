#!/usr/bin/env python3
"""Clean-room audit of the saved equality-88 selector certificate.

This checker deliberately does not import the search or reconstruction code.
It reads only the explicit coloured edge list and the two saved T-joins.  Its
selector enumeration forms literal symmetric differences of whole factor
circuits, rather than using the local selector formula of the main verifier.
"""

from collections import Counter
import json
from pathlib import Path


CERTIFICATE = Path("scratch/equality88-rotation-countermodel-result.json")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def components(vertex_count, edge_ids, edges):
    adjacency = [[] for _ in range(vertex_count)]
    for edge_id in edge_ids:
        u, v = edges[edge_id]
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))
    seen = set()
    answer = []
    for start in range(vertex_count):
        if start in seen or not adjacency[start]:
            continue
        stack = [start]
        seen.add(start)
        vertices = set()
        component_edges = set()
        while stack:
            vertex = stack.pop()
            vertices.add(vertex)
            for other, edge_id in adjacency[vertex]:
                component_edges.add(edge_id)
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        answer.append((vertices, component_edges))
    return answer


def marked_factor_circuits(edges, colours, pair):
    edge_ids = [i for i, colour in enumerate(colours) if colour in pair]
    rows = components(80, edge_ids, edges)
    require(len(rows) == 8, "factor does not have eight circuits")
    by_mark = {}
    for vertices, circuit_edges in rows:
        require(len(vertices) == len(circuit_edges) == 10, "factor is not a 10-cycle")
        marks = [mark for mark in range(8) if mark in circuit_edges]
        require(len(marks) == 1, "factor circuit does not have one mark")
        by_mark[marks[0]] = circuit_edges
    require(set(by_mark) == set(range(8)), "factor misses a marked edge")
    return by_mark


def main():
    report = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    edges = [tuple(edge) for edge in report["core"]["edge_rows"]]
    colours = report["core"]["colours_by_edge"]
    require(len(edges) == 120 == len(colours), "bad core edge count")
    require(all(u != v for u, v in edges), "core loop")
    require(len({tuple(sorted(edge)) for edge in edges}) == 120, "parallel core edge")

    incidence = [[] for _ in range(80)]
    for edge_id, (u, v) in enumerate(edges):
        incidence[u].append(edge_id)
        incidence[v].append(edge_id)
    require(all(len(row) == 3 for row in incidence), "core is not cubic")
    require(
        all({colours[edge] for edge in row} == {"a", "b", "c"} for row in incidence),
        "saved colouring is not proper",
    )

    ac = marked_factor_circuits(edges, colours, {"a", "c"})
    bc = marked_factor_circuits(edges, colours, {"b", "c"})
    histogram = Counter()
    good = []
    for selector in range(256):
        selected = set()
        for mark in range(8):
            circuit = ac[mark] if (selector >> mark) & 1 else bc[mark]
            selected.symmetric_difference_update(circuit)
        profile = []
        for _, component_edges in components(80, selected, edges):
            count = len(component_edges & set(range(8)))
            if count:
                profile.append(count)
        require(sum(profile) == 8, "selector loses a mark")
        profile.sort()
        histogram[tuple(profile)] += 1
        if all(count % 2 == 0 for count in profile):
            good.append(selector)
    require(not good, "clean-room enumeration found a good selector")
    saved_histogram = {
        "+".join(map(str, key)): value for key, value in sorted(histogram.items())
    }
    require(
        saved_histogram
        == report["selector_check"]["marked_component_profile_histogram"],
        "selector histogram differs from main verifier",
    )

    expanded = edges[8:]
    for mark in range(8):
        u, v = edges[mark]
        terminal = 80 + mark
        expanded.extend(((u, terminal), (v, terminal)))
    joins = report["unrestricted_two_t_join_check"]["join_edge_ids"]
    require(not (set(joins[0]) & set(joins[1])), "saved T-joins overlap")
    terminal_set = set(range(80, 88))
    for join in joins:
        parity = [0] * 88
        for edge_id in join:
            u, v = expanded[edge_id]
            parity[u] ^= 1
            parity[v] ^= 1
        require(
            {vertex for vertex, bit in enumerate(parity) if bit} == terminal_set,
            "saved edge set is not a T-join",
        )

    print(json.dumps({
        "status": "PASS_CLEAN_ROOM",
        "selectors": 256,
        "good_selectors": 0,
        "profile_histogram": saved_histogram,
        "two_saved_t_joins": "DISJOINT_AND_PARITY_CHECKED",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
