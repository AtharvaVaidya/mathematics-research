#!/usr/bin/env python3
"""Enumerate all unlabeled simple graphs through order 8 against R5.

Each positive row contains a literal homomorphism to the even component of
R5.  Each negative row contains either a K6 vertex set or the explicit
K3-join-C5 decomposition.  The only external dependency is nauty's geng.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path
import shutil
import subprocess


TARGET = tuple(word for word in range(32) if word.bit_count() % 2 == 0)
TARGET_NEIGHBORS = tuple(
    sum(
        1 << other
        for other, right in enumerate(TARGET)
        if (left ^ right).bit_count() == 2
    )
    for left in TARGET
)
ALL_TARGETS = (1 << len(TARGET)) - 1


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    vertices = ord(record[0]) - 63
    assert 0 <= vertices <= 62
    bits = "".join(f"{ord(character) - 63:06b}" for character in record[1:])
    edges = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor] == "1":
                edges.append((left, right))
            cursor += 1
    return vertices, tuple(edges)


def adjacency_masks(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> tuple[int, ...]:
    answer = [0] * vertices
    for left, right in edges:
        answer[left] |= 1 << right
        answer[right] |= 1 << left
    return tuple(answer)


def r5_homomorphism(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> tuple[int, ...] | None:
    adjacency = adjacency_masks(vertices, edges)
    image = [-1] * vertices
    domains = [ALL_TARGETS] * vertices

    # Each connected component may be translated independently in R5, so fix
    # one maximum-degree source vertex in every component to target word zero.
    unseen = (1 << vertices) - 1
    while unseen:
        seed_bit = unseen & -unseen
        seed = seed_bit.bit_length() - 1
        unseen ^= seed_bit
        queue = [seed]
        component = [seed]
        for current in queue:
            new = adjacency[current] & unseen
            while new:
                bit = new & -new
                new ^= bit
                other = bit.bit_length() - 1
                unseen ^= bit
                queue.append(other)
                component.append(other)
        root = max(
            component,
            key=lambda vertex: (adjacency[vertex].bit_count(), -vertex),
        )
        image[root] = 0
        domains[root] = 1
        for other in component:
            if (adjacency[root] >> other) & 1:
                domains[other] &= TARGET_NEIGHBORS[0]

    def recurse(unassigned: int) -> bool:
        if unassigned == 0:
            return True
        candidates = [
            vertex for vertex in range(vertices) if image[vertex] < 0
        ]
        vertex = min(
            candidates,
            key=lambda item: (
                domains[item].bit_count(),
                -sum(
                    image[other] >= 0
                    for other in range(vertices)
                    if (adjacency[item] >> other) & 1
                ),
                -adjacency[item].bit_count(),
                item,
            ),
        )
        choices = domains[vertex]
        while choices:
            bit = choices & -choices
            choices ^= bit
            target = bit.bit_length() - 1
            image[vertex] = target
            changes: list[tuple[int, int]] = []
            valid = True
            for other in range(vertices):
                if not ((adjacency[vertex] >> other) & 1):
                    continue
                if image[other] >= 0:
                    if not (
                        (TARGET_NEIGHBORS[target] >> image[other]) & 1
                    ):
                        valid = False
                        break
                else:
                    old = domains[other]
                    new = old & TARGET_NEIGHBORS[target]
                    if new != old:
                        changes.append((other, old))
                        domains[other] = new
                    if new == 0:
                        valid = False
                        break
            if valid and recurse(unassigned - 1):
                return True
            for other, old in reversed(changes):
                domains[other] = old
            image[vertex] = -1
        return False

    if not recurse(sum(value < 0 for value in image)):
        return None
    return tuple(TARGET[target] for target in image)


def find_k6(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> tuple[int, ...] | None:
    edge_set = set(edges)
    for subset in combinations(range(vertices), 6):
        if all(
            (left, right) in edge_set
            for left, right in combinations(subset, 2)
        ):
            return subset
    return None


def find_k3_join_c5(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    if vertices != 8:
        return None
    adjacency = adjacency_masks(vertices, edges)
    universal = tuple(
        vertex
        for vertex in range(vertices)
        if adjacency[vertex].bit_count() == 7
    )
    if len(universal) != 3:
        return None
    cycle_vertices = tuple(
        vertex for vertex in range(vertices) if vertex not in universal
    )
    if not all(
        ((adjacency[left] >> right) & 1)
        for left, right in combinations(universal, 2)
    ):
        return None
    if not all(
        sum(
            (adjacency[vertex] >> other) & 1
            for other in cycle_vertices
        )
        == 2
        for vertex in cycle_vertices
    ):
        return None
    # Recover a deterministic cyclic order.
    start = min(cycle_vertices)
    order = [start]
    previous = -1
    current = start
    while len(order) < 5:
        choices = sorted(
            other
            for other in cycle_vertices
            if other != previous and ((adjacency[current] >> other) & 1)
        )
        following = choices[0]
        if following == start and len(order) < 4:
            following = choices[1]
        order.append(following)
        previous, current = current, following
    if len(set(order)) != 5 or not ((adjacency[order[-1]] >> start) & 1):
        return None
    return universal, tuple(order)


def geng_path(explicit: str | None) -> str:
    if explicit:
        return explicit
    for candidate in ("/opt/homebrew/bin/geng", shutil.which("geng")):
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise FileNotFoundError("nauty geng not found")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geng")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/r5-hom-frontier-order8/frontier.jsonl"),
    )
    arguments = parser.parse_args()
    executable = geng_path(arguments.geng)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)

    totals = {
        "graphs": 0,
        "maps": 0,
        "k6_obstructions": 0,
        "k3_join_c5_obstructions": 0,
    }
    per_order = {}
    with arguments.output.open("w", encoding="utf-8", newline="\n") as stream:
        for order in range(1, 9):
            process = subprocess.run(
                [executable, "-q", str(order)],
                check=True,
                capture_output=True,
                text=True,
            )
            order_totals = {
                "graphs": 0,
                "maps": 0,
                "k6_obstructions": 0,
                "k3_join_c5_obstructions": 0,
            }
            for record in process.stdout.splitlines():
                if not record:
                    continue
                vertices, edges = decode_graph6(record)
                image = r5_homomorphism(vertices, edges)
                row: dict[str, object] = {
                    "type": "GRAPH",
                    "order": order,
                    "graph6": record,
                    "edges": len(edges),
                }
                if image is not None:
                    row["result"] = "MAP"
                    row["image"] = list(image)
                    order_totals["maps"] += 1
                else:
                    clique = find_k6(vertices, edges)
                    if clique is not None:
                        row["result"] = "K6_OBSTRUCTION"
                        row["vertices"] = list(clique)
                        order_totals["k6_obstructions"] += 1
                    else:
                        decomposition = find_k3_join_c5(vertices, edges)
                        if decomposition is None:
                            raise AssertionError(
                                f"unclassified obstruction {record}"
                            )
                        triangle, cycle = decomposition
                        row["result"] = "K3_JOIN_C5_OBSTRUCTION"
                        row["triangle"] = list(triangle)
                        row["cycle"] = list(cycle)
                        order_totals["k3_join_c5_obstructions"] += 1
                order_totals["graphs"] += 1
                stream.write(
                    json.dumps(row, sort_keys=True, separators=(",", ":"))
                    + "\n"
                )
            per_order[str(order)] = order_totals
            for key, value in order_totals.items():
                totals[key] += value
        summary = {
            "type": "SUMMARY",
            **totals,
            "per_order": per_order,
            "target": "even component of R5",
            "geng": executable,
        }
        stream.write(
            json.dumps(summary, sort_keys=True, separators=(",", ":")) + "\n"
        )
    print(json.dumps(summary, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
