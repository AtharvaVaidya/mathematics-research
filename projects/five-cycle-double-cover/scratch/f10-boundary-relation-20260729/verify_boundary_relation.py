#!/usr/bin/env python3
"""Independent semantic audit of the frozen F10 boundary witnesses.

This checker deliberately does not import any producer code and does not call
a SAT solver.  It verifies the mathematical certificate directly.
"""

from __future__ import annotations

from itertools import combinations, permutations, product
import argparse
import json
from pathlib import Path


def read_atom(path: Path) -> tuple[int, list[int], list[tuple[int, int]]]:
    tokens = [int(token) for token in path.read_text(encoding="ascii").split()]
    if len(tokens) < 9:
        raise AssertionError("truncated atom")
    vertices, edge_count, port_count = tokens[:3]
    if (vertices, edge_count, port_count) != (288, 429, 6):
        raise AssertionError("unexpected atom dimensions")
    ports = tokens[3:9]
    if (
        len(set(ports)) != port_count
        or any(vertex < 0 or vertex >= vertices for vertex in ports)
    ):
        raise AssertionError("invalid or repeated port vertex")
    edge_tokens = tokens[9:]
    if len(edge_tokens) != 2 * edge_count:
        raise AssertionError("wrong atom edge count")
    edges = [
        (edge_tokens[2 * edge], edge_tokens[2 * edge + 1])
        for edge in range(edge_count)
    ]
    undirected_edges = {
        (min(left, right), max(left, right))
        for left, right in edges
    }
    if len(undirected_edges) != edge_count:
        raise AssertionError("duplicate internal edge")
    if any(
        left < 0
        or left >= vertices
        or right < 0
        or right >= vertices
        or left == right
        for left, right in edges
    ):
        raise AssertionError("invalid internal edge")
    return vertices, ports, edges


def duads() -> tuple[int, ...]:
    return tuple(
        sum(1 << coordinate for coordinate in pair)
        for pair in combinations(range(5), 2)
    )


def coordinate_actions() -> tuple[tuple[int, ...], ...]:
    actions = []
    for permutation in permutations(range(5)):
        table = []
        for mask in range(32):
            table.append(sum(
                1 << permutation[coordinate]
                for coordinate in range(5)
                if mask >> coordinate & 1
            ))
        actions.append(tuple(table))
    return tuple(actions)


def xor_zero_words(labels: tuple[int, ...]) -> set[tuple[int, ...]]:
    answer = set()
    for word in product(labels, repeat=6):
        total = 0
        for mask in word:
            total ^= mask
        if total == 0:
            answer.add(word)
    return answer


def check_witnesses(
    vertices: int,
    ports: list[int],
    edges: list[tuple[int, int]],
    representatives: list[list[int]],
    results: list[dict],
) -> None:
    incident = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        incident[left].append(edge)
        incident[right].append(edge)
    for port, vertex in enumerate(ports):
        incident[vertex].append(len(edges) + port)
    if any(len(row) != 3 for row in incident):
        raise AssertionError("the completed pole is not cubic")

    if len(representatives) != len(results):
        raise AssertionError("witness row count mismatch")
    allowed_labels = set(duads())
    for expected_orbit, (expected_boundary, result) in enumerate(
        zip(representatives, results)
    ):
        if result.get("orbit") != expected_orbit:
            raise AssertionError("wrong orbit index")
        if result.get("status") != "SAT_SEMANTIC_CHECK":
            raise AssertionError("nonpositive row in positive certificate")
        if result.get("boundary") != expected_boundary:
            raise AssertionError("boundary representative mismatch")
        labels = result.get("labels")
        if not isinstance(labels, list) or len(labels) != 435:
            raise AssertionError("wrong witness length")
        if any(
            not isinstance(mask, int) or mask not in allowed_labels
            for mask in labels
        ):
            raise AssertionError("witness edge without a duad label")
        if labels[429:] != expected_boundary:
            raise AssertionError("witness has wrong boundary labels")
        for row in incident:
            total = 0
            for edge in row:
                total ^= labels[edge]
            if total:
                raise AssertionError(
                    f"orbit {expected_orbit} violates a vertex xor"
                )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("atom", type=Path)
    parser.add_argument("representatives", type=Path)
    parser.add_argument("results", type=Path)
    parser.add_argument("summary", type=Path)
    arguments = parser.parse_args()
    vertices, ports, edges = read_atom(arguments.atom)
    representative_document = json.loads(
        arguments.representatives.read_text(encoding="ascii")
    )
    representatives = representative_document["representatives"]
    results = [
        json.loads(line)
        for line in arguments.results.read_text(encoding="ascii").splitlines()
    ]
    summary = json.loads(arguments.summary.read_text(encoding="ascii"))

    labels = duads()
    if tuple(representative_document["duads"]) != labels:
        raise AssertionError("duad list mismatch")
    expected = xor_zero_words(labels)
    if len(expected) != 62560:
        raise AssertionError("wrong xor-zero word census")
    actions = coordinate_actions()
    expanded: set[tuple[int, ...]] = set()
    for representative in representatives:
        word = tuple(representative)
        if any(mask not in labels for mask in word):
            raise AssertionError("representative is not a duad word")
        if word not in expected:
            raise AssertionError("representative is not xor-zero")
        orbit = {
            tuple(action[mask] for mask in word)
            for action in actions
        }
        if expanded.intersection(orbit):
            raise AssertionError("duplicate S5 orbit representative")
        expanded.update(orbit)
    if expanded != expected:
        raise AssertionError("S5 representatives do not cover the relation")

    check_witnesses(vertices, ports, edges, representatives, results)

    quotient = {
        min(
            tuple(sorted(action[mask] for mask in word))
            for action in actions
        )
        for word in expected
    }
    if len(quotient) != 11:
        raise AssertionError("wrong S5 times S6 quotient")
    frozen_quotient = {
        tuple(word)
        for word in summary["emergent_port_symmetry"]["representatives"]
    }
    if quotient != frozen_quotient:
        raise AssertionError("frozen S5 times S6 quotient mismatch")
    relation = summary["relation"]
    if relation != {
        "ordered_duad_words": 1000000,
        "ordered_xor_zero_words": 62560,
        "s5_coordinate_orbits": 571,
        "positive_s5_orbits": 571,
        "negative_s5_orbits": 0,
        "description": (
            "exactly the ordered six-duad words with total xor zero"
        ),
    }:
        raise AssertionError("frozen relation summary mismatch")

    print("PASS independent F10 six-port relation audit")
    print(
        "ordered_duad_words=1000000 xor_zero=62560 "
        "S5_orbits=571 positive=571 negative=0"
    )
    print(
        "directly checked 571 witnesses, 248385 edge labels, "
        "and 164448 vertex xor equations"
    )
    print("emergent_relation_symmetry=S6 S5xS6_orbits=11")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
