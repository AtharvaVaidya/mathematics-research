#!/usr/bin/env python3
"""Build explicit atom completions for the six path connector states."""

from __future__ import annotations

from itertools import combinations, permutations
import json
from pathlib import Path

from search_fano_clique import PATH_CORE
from search_universal import DUADS


HERE = Path(__file__).resolve().parent
ATOMS = {
    "A": {
        "graph6": "Q??CA?_CCOW_Q_M?AD@A_@K?F??",
        "deleted_vertices": (4, 9),
        "expected_ports": (8, 10, 11, 3, 13, 14),
    },
    "B": {
        "graph6": "Q???C@?GCoOoDO[?CcAO_?k?J??",
        "deleted_vertices": (13, 16),
        "expected_ports": (1, 2, 3, 6, 8, 9),
    },
}


def decode_graph6(record):
    vertices = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, tuple(edges)


def six_pole(source):
    vertices, edges = decode_graph6(source["graph6"])
    rows = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append((right, edge))
        rows[right].append((left, edge))
    deleted = set(source["deleted_vertices"])
    retained = [v for v in range(vertices) if v not in deleted]
    mapping = {old: new for new, old in enumerate(retained)}
    internal = tuple(
        (mapping[left], mapping[right])
        for left, right in edges
        if left not in deleted and right not in deleted
    )
    ports = tuple(
        mapping[other]
        for deleted_vertex in source["deleted_vertices"]
        for other, _ in sorted(rows[deleted_vertex])
    )
    if (
        vertices != 18
        or len(edges) != 27
        or len(internal) != 21
        or len(set(ports)) != 6
        or ports != source["expected_ports"]
    ):
        raise AssertionError("wrong Blanusa six-pole topology")
    incidence = [[] for _ in range(16)]
    for edge, (left, right) in enumerate(internal):
        incidence[left].append(edge)
        incidence[right].append(edge)
    if sorted(map(len, incidence)) != [2] * 6 + [3] * 10:
        raise AssertionError("wrong six-pole degree sequence")
    return internal, ports, tuple(tuple(row) for row in incidence)


def ordered_connector_states():
    return tuple(sorted({
        tuple(state[index] for index in action)
        for state in PATH_CORE
        for action in permutations(range(3))
    }))


def build_atom(atom_type, source, boundary_words):
    import pycryptosat

    internal, ports, rows = six_pole(source)
    port_index = {vertex: index for index, vertex in enumerate(ports)}
    internal_variable_count = 5 * len(internal)

    def internal_variable(edge, coordinate):
        return 5 * edge + coordinate + 1

    def boundary_variable(port, coordinate):
        return internal_variable_count + 5 * port + coordinate + 1

    solver = pycryptosat.Solver()
    for edge in range(len(internal)):
        variables = [internal_variable(edge, c) for c in range(5)]
        for triple in combinations(variables, 3):
            solver.add_clause([-entry for entry in triple])
        for four in combinations(variables, 4):
            solver.add_clause(list(four))
    for vertex in range(16):
        for coordinate in range(5):
            variables = [
                internal_variable(edge, coordinate)
                for edge in rows[vertex]
            ]
            if vertex in port_index:
                variables.append(
                    boundary_variable(port_index[vertex], coordinate)
                )
            solver.add_xor_clause(variables, False)

    witnesses = []
    for word in boundary_words:
        assumptions = []
        for port, label in enumerate(word):
            for coordinate in range(5):
                variable = boundary_variable(port, coordinate)
                assumptions.append(
                    variable
                    if label & (1 << coordinate)
                    else -variable
                )
        sat, model = solver.solve(assumptions)
        if not sat:
            raise AssertionError(
                f"path-core boundary unexpectedly fails atom {atom_type}: "
                f"{word}"
            )
        labels = tuple(
            sum(
                1 << coordinate
                for coordinate in range(5)
                if model[internal_variable(edge, coordinate)]
            )
            for edge in range(len(internal))
        )
        if any(label not in DUADS for label in labels):
            raise AssertionError("atom completion contains non-duad")
        for vertex in range(16):
            parity = 0
            for edge in rows[vertex]:
                parity ^= labels[edge]
            if vertex in port_index:
                parity ^= word[port_index[vertex]]
            if parity:
                raise AssertionError("atom completion violates vertex parity")
        witnesses.append({
            "boundary_word": list(word),
            "internal_labels": list(labels),
        })
    return {
        "atom_type": atom_type,
        "graph6": source["graph6"],
        "deleted_vertices": list(source["deleted_vertices"]),
        "ports": list(ports),
        "internal_edges": [list(edge) for edge in internal],
        "witnesses": witnesses,
    }


def main() -> int:
    ordered = ordered_connector_states()
    if len(ordered) != 36:
        raise AssertionError("wrong ordered path-state count")
    words = tuple(left + right for left in ordered for right in ordered)
    if len(words) != 1296 or len(set(words)) != 1296:
        raise AssertionError("wrong ordered path-boundary count")
    atoms = [
        build_atom(atom_type, source, words)
        for atom_type, source in ATOMS.items()
    ]
    report = {
        "schema": "blanusa-two-atom-path-core-positive-witnesses-v1",
        "scope": (
            "all 36 ordered path states in each connector block, for both "
            "atom types; positive witnesses only"
        ),
        "path_states_unordered": [list(row) for row in PATH_CORE],
        "ordered_connector_states": len(ordered),
        "ordered_boundary_words_per_atom": len(words),
        "atoms": atoms,
    }
    (HERE / "path-atom-witnesses.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(
        "PASS explicit path-core atom completions "
        f"atoms={len(atoms)} words_per_atom={len(words)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
