#!/usr/bin/env python3
"""Independent audit of the CVT[80,30] all-C10 selector scan.

The C++ program exhausts all normalized Tait colourings.  This checker uses
NetworkX for graph decoding and isomorphism, verifies every saved all-C10
colouring, proves that all 60 common-colour cases are colour-preservingly
isomorphic (allowing exchange of the two noncommon colours), and recomputes
the full perfect-transversal/selector histogram on one representative.
It also enumerates the perfect transversals in all 60 cases to check the
raw and distinct mark-set totals.
"""

from collections import Counter
import argparse
import json
from pathlib import Path

import networkx as nx


CERTIFICATE = Path("scratch/order80-c10-selector-scan-result.json")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def graph6_edge_order(graph):
    return [
        (u, v)
        for v in range(1, len(graph))
        for u in range(v)
        if graph.has_edge(u, v)
    ]


def factors(edges, incidence, colours, omitted):
    seen = set()
    rows = []
    for start in range(len(edges)):
        if colours[start] == omitted or start in seen:
            continue
        stack = [start]
        seen.add(start)
        component = set()
        while stack:
            edge = stack.pop()
            component.add(edge)
            for vertex in edges[edge]:
                for other in incidence[vertex]:
                    if colours[other] != omitted and other not in seen:
                        seen.add(other)
                        stack.append(other)
        rows.append(frozenset(component))
    return rows


def case_data(edges, incidence, colours, common):
    other = [value for value in range(3) if value != common]
    factor_a = factors(edges, incidence, colours, other[1])
    factor_b = factors(edges, incidence, colours, other[0])
    require(
        len(factor_a) == len(factor_b) == 8
        and all(len(row) == 10 for row in factor_a + factor_b),
        "not an all-C10 factor pair",
    )
    a_of = {}
    b_of = {}
    for index, row in enumerate(factor_a):
        for edge in row:
            a_of[edge] = index
    for index, row in enumerate(factor_b):
        for edge in row:
            b_of[edge] = index
    rows = [[] for _ in range(8)]
    for edge, colour in enumerate(colours):
        if colour == common:
            rows[a_of[edge]].append(edge)
    require(all(len(row) == 5 for row in rows), "incidence degree is not five")
    return factor_a, factor_b, a_of, b_of, rows


def perfect_transversals(rows, b_of):
    answer = []

    def visit(a, used_b, marks):
        if a == 8:
            answer.append(tuple(marks))
            return
        for edge in rows[a]:
            b = b_of[edge]
            if (used_b >> b) & 1:
                continue
            marks.append(edge)
            visit(a + 1, used_b | (1 << b), marks)
            marks.pop()

    visit(0, 0, [])
    return answer


def normalized_coloured_graph(edges, colours, common, swap=False):
    other = [value for value in range(3) if value != common]
    relabel = {
        common: 0,
        other[0]: 2 if swap else 1,
        other[1]: 1 if swap else 2,
    }
    graph = nx.Graph()
    graph.add_nodes_from(range(80))
    graph.add_edges_from(
        (u, v, {"colour": relabel[colours[edge]]})
        for edge, (u, v) in enumerate(edges)
    )
    return graph


def representative_histograms(edges, incidence, colours, common):
    factor_a, factor_b, _, b_of, rows = case_data(
        edges, incidence, colours, common
    )
    transversals = perfect_transversals(rows, b_of)
    edge_neighbours = []
    for edge, (u, v) in enumerate(edges):
        neighbours = 0
        for other in incidence[u] + incidence[v]:
            if other != edge:
                neighbours |= 1 << other
        edge_neighbours.append(neighbours)
    factor_a_masks = [sum(1 << edge for edge in row) for row in factor_a]
    factor_b_masks = [sum(1 << edge for edge in row) for row in factor_b]
    profile_histogram = Counter()
    good_count_histogram = Counter()

    for marks in transversals:
        marked_mask = sum(1 << edge for edge in marks)
        b_for_a = [b_of[edge] for edge in marks]
        require(len(set(b_for_a)) == 8, "not a perfect transversal")
        good = 0
        for selector in range(256):
            cycle = 0
            for a in range(8):
                cycle ^= (
                    factor_a_masks[a]
                    if (selector >> a) & 1
                    else factor_b_masks[b_for_a[a]]
                )
            remaining = cycle
            profile = []
            while remaining:
                frontier = remaining & -remaining
                component = 0
                while frontier:
                    component |= frontier
                    neighbourhood = 0
                    active = frontier
                    while active:
                        bit = active & -active
                        edge = bit.bit_length() - 1
                        neighbourhood |= edge_neighbours[edge]
                        active ^= bit
                    frontier = neighbourhood & cycle & ~component
                remaining &= ~component
                count = (component & marked_mask).bit_count()
                if count:
                    profile.append(count)
            profile.sort()
            require(sum(profile) == 8, "selector loses a mark")
            profile_histogram["+".join(map(str, profile))] += 1
            if all(count % 2 == 0 for count in profile):
                good += 1
        good_count_histogram[good] += 1
    return transversals, profile_histogram, good_count_histogram


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("scratch/order80-c10-selector-audit-result.json"),
    )
    args = parser.parse_args()
    report = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    graph = nx.from_graph6_bytes(report["graph6"].encode("ascii"))
    edges = graph6_edge_order(graph)
    require(len(graph) == 80 and len(edges) == 120, "bad graph size")
    require(nx.is_connected(graph), "graph disconnected")
    require(all(graph.degree(vertex) == 3 for vertex in graph), "graph not cubic")
    incidence = [[] for _ in range(80)]
    for edge, (u, v) in enumerate(edges):
        incidence[u].append(edge)
        incidence[v].append(edge)

    words = [
        tuple(map(int, word))
        for word in report["all_c10_colour_words"]
    ]
    require(len(words) == len(set(words)) == 20, "bad all-C10 word list")
    for colours in words:
        require(len(colours) == 120, "bad colour word length")
        require(
            all(
                {colours[edge] for edge in incidence[vertex]} == {0, 1, 2}
                for vertex in range(80)
            ),
            "word is not a Tait colouring",
        )
        require(
            [colours[edge] for edge in incidence[0]] == [0, 1, 2],
            "word is not normalized at vertex zero",
        )
        for omitted in range(3):
            rows = factors(edges, incidence, colours, omitted)
            require(
                len(rows) == 8 and all(len(row) == 10 for row in rows),
                "saved word is not all-C10",
            )

    reference = normalized_coloured_graph(edges, words[0], 0)
    edge_match = nx.algorithms.isomorphism.categorical_edge_match(
        "colour", -1
    )
    isomorphism_checks = 0
    all_transversal_masks = set()
    transversal_counts = []
    for colours in words:
        for common in range(3):
            target = normalized_coloured_graph(edges, colours, common)
            swapped = normalized_coloured_graph(
                edges, colours, common, swap=True
            )
            require(
                nx.is_isomorphic(reference, target, edge_match=edge_match)
                or nx.is_isomorphic(reference, swapped, edge_match=edge_match),
                "common-colour case is not isomorphic to the reference",
            )
            isomorphism_checks += 1
            _, _, _, b_of, rows = case_data(
                edges, incidence, colours, common
            )
            transversals = perfect_transversals(rows, b_of)
            transversal_counts.append(len(transversals))
            all_transversal_masks.update(
                sum(1 << edge for edge in marks)
                for marks in transversals
            )

    transversals, profile_histogram, good_histogram = (
        representative_histograms(edges, incidence, words[0], 0)
    )
    require(len(transversals) == 1249, "bad representative permanent")
    multiplier = 60
    global_profiles = {
        key: value * multiplier
        for key, value in sorted(profile_histogram.items())
    }
    global_good = {
        str(key): value * multiplier
        for key, value in sorted(good_histogram.items())
    }
    require(
        global_profiles == report["marked_component_profile_histogram"],
        "profile histogram differs",
    )
    require(
        global_good == report["good_selector_count_histogram"],
        "good-count histogram differs",
    )
    require(set(transversal_counts) == {1249}, "case permanent differs")
    require(sum(transversal_counts) == report["mark_set_records"], "raw total differs")
    require(
        len(all_transversal_masks) == report["unique_edge_mark_sets"],
        "distinct mark-set total differs",
    )
    require(min(good_histogram) == 94, "unexpected minimum good count")
    require(sum(good_histogram.values()) == 1249, "bad good histogram total")
    require(
        sum(key * value for key, value in good_histogram.items()) * multiplier
        == report["total_good_selectors"],
        "total good selectors differs",
    )
    require(report["no_good_selector_records"] == 0, "saved no-good record")

    audit = {
        "status": "PASS_INDEPENDENT_ISOMORPHISM_AUDIT",
        "saved_all_c10_colourings_checked": len(words),
        "common_colour_cases_isomorphic": isomorphism_checks,
        "perfect_transversals_per_case": 1249,
        "mark_set_records": sum(transversal_counts),
        "unique_edge_mark_sets": len(all_transversal_masks),
        "representative_selector_evaluations": 1249 * 256,
        "minimum_good_selectors_per_mark_set": min(good_histogram),
        "no_good_mark_sets": 0,
    }
    args.output.write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()
