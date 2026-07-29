#!/usr/bin/env python3
"""Search connected 2-sums of three relabelled score-14 obstruction states.

This is discovery code, not a certificate checker.  It forms a chain of
two cubic 2-sums, preserving the displayed F_2^3-flow whenever the two
removed edges have the same value, and calls the exact C++ binary-repair
audit on each generated state.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
BASE_STATE = HERE / "fano-binary-repair-score14-order36.txt"
LINEAR_MAPS = ((1, 2, 4), (3, 4, 6), (7, 6, 2))


def linear_image(value: int, images: tuple[int, int, int]) -> int:
    return (
        (images[0] if value & 1 else 0)
        ^ (images[1] if value & 2 else 0)
        ^ (images[2] if value & 4 else 0)
    )


def decode_graph6(record: str) -> tuple[int, list[tuple[int, int]]]:
    if record[0] != "~":
        order = ord(record[0]) - 63
        payload = 1
    else:
        order = 0
        for character in record[1:4]:
            order = (order << 6) | (ord(character) - 63)
        payload = 4
    bits = []
    for character in record[payload:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, edges


def encode_graph6(order: int, edges: list[tuple[int, int, int]]) -> str:
    pairs = {(min(left, right), max(left, right)) for left, right, _ in edges}
    if len(pairs) != len(edges):
        raise ValueError("loop or parallel edge in composition")
    if order <= 62:
        header = chr(order + 63)
    else:
        header = "~" + "".join(
            chr(((order >> shift) & 63) + 63) for shift in (12, 6, 0)
        )
    bits = []
    for right in range(1, order):
        for left in range(right):
            bits.append(int((left, right) in pairs))
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for cursor in range(0, len(bits), 6):
        value = 0
        for bit in bits[cursor:cursor + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return header + "".join(payload)


def sorted_state(
    order: int,
    edges: list[tuple[int, int, int]],
) -> tuple[str, str]:
    normalized = sorted(
        (max(left, right), min(left, right), value)
        for left, right, value in edges
    )
    graph6 = encode_graph6(order, edges)
    flow = ",".join(str(value) for _, _, value in normalized)
    return graph6, flow


def two_sum(
    edges: list[tuple[int, int, int]],
    first: int,
    second: int,
    crossed: bool,
) -> list[tuple[int, int, int]]:
    if first == second:
        raise ValueError("2-sum uses one edge twice")
    left = edges[first]
    right = edges[second]
    if left[2] != right[2]:
        raise ValueError("2-sum flow values differ")
    result = [
        edge for index, edge in enumerate(edges)
        if index not in (first, second)
    ]
    a, b, value = left
    c, d, _ = right
    if crossed:
        c, d = d, c
    result.extend(((a, c, value), (b, d, value)))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_binary")
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260820)
    args = parser.parse_args()

    record, flow_line = BASE_STATE.read_text(encoding="utf-8").splitlines()
    base_order, base_pairs = decode_graph6(record)
    base_flow = tuple(int(item) for item in flow_line.split(","))
    base = [
        (left, right, value)
        for (left, right), value in zip(base_pairs, base_flow, strict=True)
    ]
    copies = []
    origins = []
    for copy, images in enumerate(LINEAR_MAPS):
        offset = copy * base_order
        for edge, (left, right, value) in enumerate(base):
            copies.append((
                left + offset,
                right + offset,
                linear_image(value, images),
            ))
            origins.append((copy, edge))

    rng = random.Random(args.seed)
    by_copy_value: dict[tuple[int, int], list[int]] = {}
    for index, (_, _, value) in enumerate(copies):
        copy, _ = origins[index]
        by_copy_value.setdefault((copy, value), []).append(index)

    outcomes: dict[str, int] = {}
    for trial in range(args.trials):
        first_value = rng.randrange(1, 8)
        second_value = rng.randrange(1, 8)
        edge_a = rng.choice(by_copy_value[(0, first_value)])
        edge_b1 = rng.choice(by_copy_value[(1, first_value)])
        candidates_b2 = [
            edge for edge in by_copy_value[(1, second_value)]
            if edge != edge_b1
        ]
        if not candidates_b2:
            continue
        edge_b2 = rng.choice(candidates_b2)
        edge_c = rng.choice(by_copy_value[(2, second_value)])

        # Perform the higher-index deletion first so the retained origin
        # lookup can identify the second pair after the first sum.
        selected_origins = (
            origins[edge_a], origins[edge_b1],
            origins[edge_b2], origins[edge_c],
        )
        current = list(copies)

        def locate(origin: tuple[int, int]) -> int:
            copy, local = origin
            target = base[local]
            offset = copy * base_order
            value = linear_image(target[2], LINEAR_MAPS[copy])
            endpoints = {target[0] + offset, target[1] + offset}
            return next(
                index for index, (left, right, edge_value) in enumerate(current)
                if {left, right} == endpoints and edge_value == value
            )

        first_crossed = bool(rng.randrange(2))
        second_crossed = bool(rng.randrange(2))
        a_now = locate(selected_origins[0])
        b1_now = locate(selected_origins[1])
        current = two_sum(current, a_now, b1_now, first_crossed)
        b2_now = locate(selected_origins[2])
        c_now = locate(selected_origins[3])
        current = two_sum(current, b2_now, c_now, second_crossed)
        state = sorted_state(3 * base_order, current)

        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".txt"
        ) as stream:
            stream.write(state[0] + "\n" + state[1] + "\n")
            stream.flush()
            completed = subprocess.run(
                [
                    args.audit_binary,
                    "--packing-binary-switch-pair-audit",
                    stream.name,
                    "0",
                    "0",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
        output = completed.stdout.strip()
        if output:
            result = json.loads(output)
            status = result["status"]
            repairs = result.get("repair_pairs", -1)
            key = f"{status}:{repairs}"
            outcomes[key] = outcomes.get(key, 0) + 1
            if repairs == 0:
                print(json.dumps({
                    "status": "CONNECTED_BINARY_REPAIR_COUNTERMODEL",
                    "trial": trial,
                    "selected_origins": selected_origins,
                    "crossed": (first_crossed, second_crossed),
                    "state": state,
                    "audit": result,
                }))
                return
        else:
            key = completed.stderr.strip().splitlines()[-1]
            outcomes[key] = outcomes.get(key, 0) + 1

    print(json.dumps({
        "status": "COMPOSITION_SEARCH_DONE",
        "trials": args.trials,
        "seed": args.seed,
        "outcomes": outcomes,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
