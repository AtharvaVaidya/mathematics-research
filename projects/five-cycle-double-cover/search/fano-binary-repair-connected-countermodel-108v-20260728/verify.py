#!/usr/bin/env python3
"""Independent semantic, CNF, LRAT, and FiveCDC audit for the package."""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import subprocess


PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent.parent
STATE = (
    PROJECT
    / "scratch"
    / "fano-binary-repair-connected-countermodel-order108.txt"
)
BASE_STATE = PROJECT / "scratch" / "fano-binary-repair-score14-order36.txt"
CNF = PACKAGE / "all-21-binary-repairs.cnf"
LRAT = PACKAGE / "all-21-binary-repairs.lrat"

MAPS = ((1, 2, 4), (3, 4, 6), (7, 6, 2))
SUM_RECIPE = (((0, 18), (1, 29)), ((1, 31), (2, 34)))
BASE_LABELS = (
    "56", "05", "45", "05", "57", "46", "56", "05", "47", "04",
    "07", "45", "57", "45", "47", "57", "56", "06", "04", "47",
    "05", "04", "45", "46", "47", "07", "67", "67", "06", "67",
    "07", "06", "47", "04", "06", "07", "06", "67", "05", "07",
    "07", "57", "06", "05", "56", "04", "46", "07", "06", "57",
    "67", "46", "45", "56",
)
COVER_MAPS = (
    {"0": "0", "4": "4", "5": "5", "6": "6", "7": "7"},
    {"0": "5", "4": "6", "5": "7", "6": "0", "7": "4"},
    {"0": "0", "4": "4", "5": "6", "6": "5", "7": "7"},
)
COVER_BITS = {"0": 1, "4": 2, "5": 4, "6": 8, "7": 16}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def linear_image(value: int, images: tuple[int, int, int]) -> int:
    answer = 0
    for bit, image in zip((1, 2, 4), images, strict=True):
        if value & bit:
            answer ^= image
    return answer


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    if record[0] == "~":
        order = 0
        for character in record[1:4]:
            order = order * 64 + ord(character) - 63
        payload = record[4:]
    else:
        order = ord(record[0]) - 63
        payload = record[1:]
    bits = "".join(
        f"{ord(character) - 63:06b}" for character in payload
    )
    edges = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            require(cursor < len(bits), "truncated graph6")
            if bits[cursor] == "1":
                edges.append((left, right))
            cursor += 1
    require("1" not in bits[cursor:], "nonzero graph6 padding")
    return order, tuple(edges)


def encode_graph6(order: int, pairs: set[tuple[int, int]]) -> str:
    if order <= 62:
        header = chr(order + 63)
    else:
        header = "~" + "".join(
            chr(((order >> shift) & 63) + 63) for shift in (12, 6, 0)
        )
    bits = [
        int((left, right) in pairs)
        for right in range(1, order)
        for left in range(right)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start:start + 6]:
            value = value * 2 + bit
        payload.append(chr(value + 63))
    return header + "".join(payload)


def incidence(
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


def reconstruct_composition() -> tuple[str, tuple[int, ...], tuple[int, ...]]:
    base_record, base_flow_line = BASE_STATE.read_text(
        encoding="utf-8"
    ).splitlines()
    base_order, base_edges = decode_graph6(base_record)
    base_flow = tuple(int(item) for item in base_flow_line.split(","))
    require(len(base_edges) == len(base_flow) == len(BASE_LABELS),
            "base certificate lengths differ")

    # Each edge carries endpoints, flow value, cover label, and its immutable
    # (copy, local-edge) provenance.
    composed = []
    for copy in range(3):
        offset = copy * base_order
        for local, ((left, right), value, label) in enumerate(
            zip(base_edges, base_flow, BASE_LABELS, strict=True)
        ):
            mapped_label = frozenset(COVER_MAPS[copy][symbol]
                                     for symbol in label)
            composed.append((
                left + offset,
                right + offset,
                linear_image(value, MAPS[copy]),
                mapped_label,
                (copy, local),
            ))

    for first_origin, second_origin in SUM_RECIPE:
        first = next(edge for edge in composed if edge[4] == first_origin)
        second = next(edge for edge in composed if edge[4] == second_origin)
        require(first[2] == second[2], "2-sum flow values do not match")
        require(first[3] == second[3], "2-sum cover labels do not match")
        composed.remove(first)
        composed.remove(second)
        left, right, value, label, _ = first
        top, bottom, _, _, _ = second
        # Both retained sums use the crossed pairing.
        composed.extend((
            (left, bottom, value, label, ("new", len(composed))),
            (right, top, value, label, ("new", len(composed) + 1)),
        ))

    normalized = sorted(
        (max(left, right), min(left, right), value, label)
        for left, right, value, label, _ in composed
    )
    pairs = {(left, right) for right, left, _, _ in normalized}
    record = encode_graph6(3 * base_order, pairs)
    flow = tuple(value for _, _, value, _ in normalized)
    labels = tuple(
        sum(COVER_BITS[symbol] for symbol in label)
        for _, _, _, label in normalized
    )
    return record, flow, labels


def graph_metadata(
    order: int,
    edges: tuple[tuple[int, int], ...],
    rows: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    def components(deleted: frozenset[int]) -> list[tuple[int, int]]:
        unseen = set(range(order))
        answer = []
        while unseen:
            root = min(unseen)
            reached = {root}
            queue = [root]
            edge_ends = 0
            for vertex in queue:
                for edge in rows[vertex]:
                    if edge in deleted:
                        continue
                    edge_ends += 1
                    left, right = edges[edge]
                    other = left ^ right ^ vertex
                    if other not in reached:
                        reached.add(other)
                        queue.append(other)
            unseen -= reached
            answer.append((len(reached), edge_ends // 2))
        return answer

    require(len(components(frozenset())) == 1, "graph is disconnected")
    cyclic_cut_counts = {}
    for size in (1, 2):
        count = 0
        for deleted in combinations(range(len(edges)), size):
            cyclic = sum(
                edge_count >= vertex_count
                for vertex_count, edge_count in components(frozenset(deleted))
            )
            if cyclic >= 2:
                count += 1
        cyclic_cut_counts[size] = count
    require(cyclic_cut_counts[1] == 0, "graph has a bridge")

    girth = order + 1
    for forbidden, (source, target) in enumerate(edges):
        distance = [-1] * order
        distance[source] = 0
        queue = [source]
        for vertex in queue:
            for edge in rows[vertex]:
                if edge == forbidden:
                    continue
                left, right = edges[edge]
                other = left ^ right ^ vertex
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    queue.append(other)
        if distance[target] >= 0:
            girth = min(girth, distance[target] + 1)
    return {
        "connected": True,
        "bridgeless": True,
        "girth": girth,
        "cyclic_cut_counts_sizes_1_and_2": cyclic_cut_counts,
        "cyclically_4_edge_connected": cyclic_cut_counts[2] == 0,
    }


def expected_incidences() -> tuple[tuple[int, int], ...]:
    answer = []
    for switch_value in range(1, 8):
        pairs = {
            tuple(sorted((target, target ^ switch_value)))
            for target in range(1, 8)
            if target != switch_value
        }
        for pair in sorted(pairs):
            answer.append((switch_value, pair[0]))
    return tuple(answer)


def expected_cnf(
    rows: tuple[tuple[int, ...], ...],
    flow: tuple[int, ...],
) -> tuple[int, list[tuple[int, ...]]]:
    incidences = expected_incidences()
    next_variable = len(incidences) + 1
    clauses: list[tuple[int, ...]] = []

    def parity_clauses(
        variables: tuple[int, ...],
        target: int,
        selector: int,
    ) -> None:
        for assignment in range(1 << len(variables)):
            if assignment.bit_count() % 2 == target:
                continue
            clause = tuple(
                -variable if assignment & (1 << bit) else variable
                for bit, variable in enumerate(variables)
            )
            clauses.append(clause + (-selector,))

    for selector, (switch_value, target_value) in enumerate(
        incidences, start=1
    ):
        edge_count = len(flow)
        switch = tuple(range(next_variable, next_variable + edge_count))
        next_variable += edge_count
        red = tuple(range(next_variable, next_variable + edge_count))
        next_variable += edge_count
        blue = tuple(range(next_variable, next_variable + edge_count))
        next_variable += edge_count

        for edge, value in enumerate(flow):
            if value == switch_value:
                clauses.append((-switch[edge], -selector))
            clauses.append((-red[edge], -blue[edge], -selector))
            if value == target_value:
                clauses.append((switch[edge], -red[edge], -selector))
                clauses.append((switch[edge], -blue[edge], -selector))
            elif value == target_value ^ switch_value:
                clauses.append((-switch[edge], -red[edge], -selector))
                clauses.append((-switch[edge], -blue[edge], -selector))

        for row in rows:
            parity_clauses(
                tuple(switch[edge] for edge in row), 0, selector
            )
            red_variables = [red[edge] for edge in row]
            blue_variables = [blue[edge] for edge in row]
            target = 0
            for edge in row:
                if flow[edge] == target_value:
                    target ^= 1
                    red_variables.append(switch[edge])
                    blue_variables.append(switch[edge])
                elif flow[edge] == target_value ^ switch_value:
                    red_variables.append(switch[edge])
                    blue_variables.append(switch[edge])
            parity_clauses(tuple(red_variables), target, selector)
            parity_clauses(tuple(blue_variables), target, selector)

    clauses.append(tuple(range(1, len(incidences) + 1)))
    return next_variable - 1, clauses


def parse_cnf(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables = -1
    clauses = []
    with path.open(encoding="ascii") as stream:
        for line in stream:
            if line.startswith("c") or not line.strip():
                continue
            if line.startswith("p"):
                _, kind, variables_text, clauses_text = line.split()
                require(kind == "cnf", "not a CNF header")
                variables = int(variables_text)
                expected_count = int(clauses_text)
                continue
            literals = tuple(int(item) for item in line.split())
            require(literals and literals[-1] == 0, "unterminated clause")
            clauses.append(literals[:-1])
    require(len(clauses) == expected_count, "CNF clause count differs")
    return variables, clauses


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--lrat-check",
        type=Path,
        required=True,
        help="path to the C lrat-check executable",
    )
    parser.add_argument(
        "--cake-lpr",
        type=Path,
        required=True,
        help="path to the CakeML-generated cake_lpr executable",
    )
    args = parser.parse_args()

    state_record, state_flow_line = STATE.read_text(
        encoding="utf-8"
    ).splitlines()
    state_flow = tuple(int(item) for item in state_flow_line.split(","))
    rebuilt_record, rebuilt_flow, labels = reconstruct_composition()
    require(state_record == rebuilt_record, "reconstructed graph6 differs")
    require(state_flow == rebuilt_flow, "reconstructed flow differs")

    order, edges = decode_graph6(state_record)
    rows = incidence(order, edges)
    require(order == 108 and len(edges) == 162, "wrong graph size")
    require(len(set(edges)) == len(edges), "parallel edge")
    require(all(len(row) == 3 for row in rows), "graph is not cubic")
    require(
        all(state_flow[row[0]] ^ state_flow[row[1]] ^ state_flow[row[2]] == 0
            for row in rows),
        "flow conservation fails",
    )
    metadata = graph_metadata(order, edges, rows)

    require(all(label.bit_count() == 2 for label in labels),
            "FiveCDC label has wrong weight")
    for row in rows:
        for coordinate in range(5):
            require(
                sum(bool(labels[edge] & (1 << coordinate))
                    for edge in row) % 2 == 0,
                "FiveCDC coordinate parity fails",
            )

    actual_variables, actual_clauses = parse_cnf(CNF)
    expected_variables, clauses = expected_cnf(rows, state_flow)
    require(actual_variables == expected_variables,
            "CNF variable count differs")
    require(Counter(actual_clauses) == Counter(clauses),
            "CNF clauses differ semantically")

    proof_checks = {}
    for name, executable in (
        ("lrat-check", args.lrat_check),
        ("cake_lpr", args.cake_lpr),
    ):
        require(executable.is_file(), f"{name} executable not found")
        completed = subprocess.run(
            [str(executable), str(CNF), str(LRAT)],
            text=True,
            capture_output=True,
            check=True,
        )
        conclusions = [
            line.strip()
            for line in completed.stdout.splitlines()
            if "VERIFIED" in line
        ]
        require(len(conclusions) == 1, f"{name} did not verify the proof")
        proof_checks[name] = conclusions[0]

    print(json.dumps({
        "schema": "fano-binary-repair-connected-108-audit-v1",
        "solver_independent_semantic_checker": True,
        "order": order,
        "edges": len(edges),
        "graph_metadata": metadata,
        "flow": "nowhere-zero F_2^3 flow",
        "composition_recipe_reconstructed": True,
        "explicit_standard_five_cdc": True,
        "cnf_variables": actual_variables,
        "cnf_clauses": len(actual_clauses),
        "cnf_semantics_reconstructed": True,
        "all_21_repair_incidences_unsat": len(proof_checks) == 2,
        "proof_checks": proof_checks,
        "scope": (
            "counterexample to connected binary packing repair only; "
            "cyclic 2-edge cuts keep it outside the minimum FiveCDC "
            "counterexample domain"
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
