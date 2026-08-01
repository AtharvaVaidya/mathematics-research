#!/usr/bin/env python3
"""Independent replay of compact positive witnesses from predicate_stream.cpp.

This file neither imports nor executes the C++ implementation.  It decodes
graph6, checks each retained D5 flow, rebuilds all factor components, and
recomputes the three rooted-interface predicates.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path


LABELS = frozenset((3, 5, 6, 9, 10, 12, 17, 18, 20, 24))


def decode_graph6(row: str) -> tuple[int, list[tuple[int, int]], list[list[int]]]:
    if not row or row.startswith("~"):
        raise ValueError("only ordinary graph6 rows with n <= 62 are supported")
    n = ord(row[0]) - 63
    if not 0 <= n <= 62:
        raise ValueError("bad graph6 order")
    bits: list[int] = []
    for character in row[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise ValueError("bad graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    if len(bits) < needed or any(bits[needed:]):
        raise ValueError("bad graph6 length or padding")
    edges: list[tuple[int, int]] = []
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    incidence: list[list[int]] = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    if any(len(row_edges) != 3 for row_edges in incidence):
        raise ValueError("graph is not cubic")
    return n, edges, incidence


def vertex_components(
    n: int,
    edges: list[tuple[int, int]],
    removed_edges: frozenset[int] = frozenset(),
    removed_vertex: int | None = None,
) -> list[set[int]]:
    adjacency = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        if edge in removed_edges or left == removed_vertex or right == removed_vertex:
            continue
        adjacency[left].append(right)
        adjacency[right].append(left)
    unseen = set(range(n))
    if removed_vertex is not None:
        unseen.remove(removed_vertex)
    answer: list[set[int]] = []
    while unseen:
        start = next(iter(unseen))
        component = {start}
        stack = [start]
        unseen.remove(start)
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    stack.append(neighbor)
        answer.append(component)
    return answer


def check_biconnected(n: int, edges: list[tuple[int, int]]) -> None:
    if len(vertex_components(n, edges)) != 1:
        raise ValueError("graph is disconnected")
    for vertex in range(n):
        if len(vertex_components(n, edges, removed_vertex=vertex)) != 1:
            raise ValueError(f"vertex {vertex} is a cut vertex")


def check_cyclic_connectivity_four(n: int, edges: list[tuple[int, int]]) -> None:
    for size in (1, 2, 3):
        for cut in itertools.combinations(range(len(edges)), size):
            components = vertex_components(n, edges, frozenset(cut))
            if len(components) == 1:
                continue
            cyclic = 0
            for component in components:
                internal_edges = sum(
                    left in component and right in component for left, right in edges
                )
                cyclic += internal_edges >= len(component)
            if cyclic >= 2:
                raise ValueError(f"cycle-separating edge cut of size {size}")


def girth(n: int, edges: list[tuple[int, int]]) -> int:
    adjacency = [[] for _ in range(n)]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    best = n + 1
    for source in range(n):
        distance = [-1] * n
        parent = [-1] * n
        distance[source] = 0
        queue = [source]
        for vertex in queue:
            for neighbor in adjacency[vertex]:
                if distance[neighbor] < 0:
                    distance[neighbor] = distance[vertex] + 1
                    parent[neighbor] = vertex
                    queue.append(neighbor)
                elif parent[vertex] != neighbor:
                    best = min(best, distance[vertex] + distance[neighbor] + 1)
    return best


def is_three_edge_colorable(
    edges: list[tuple[int, int]], incidence: list[list[int]]
) -> bool:
    colors = [-1] * len(edges)
    used = [0] * len(incidence)

    def assign(edge: int, color: int, trail: list[int]) -> bool:
        queue = [(edge, color)]
        while queue:
            current, current_color = queue.pop()
            if colors[current] >= 0:
                if colors[current] != current_color:
                    return False
                continue
            left, right = edges[current]
            bit = 1 << current_color
            if used[left] & bit or used[right] & bit:
                return False
            colors[current] = current_color
            used[left] |= bit
            used[right] |= bit
            trail.append(current)
            for vertex in (left, right):
                unassigned = [item for item in incidence[vertex] if colors[item] < 0]
                if not unassigned:
                    if used[vertex] != 7:
                        return False
                elif len(unassigned) == 1:
                    missing = 7 ^ used[vertex]
                    if missing not in (1, 2, 4):
                        return False
                    queue.append((unassigned[0], missing.bit_length() - 1))
        return True

    def search() -> bool:
        edge = -1
        score = -1
        for candidate, (left, right) in enumerate(edges):
            if colors[candidate] >= 0:
                continue
            candidate_score = used[left].bit_count() + used[right].bit_count()
            if candidate_score > score:
                edge = candidate
                score = candidate_score
        if edge < 0:
            return True
        choices = (0,) if not any(color >= 0 for color in colors) else (0, 1, 2)
        for color in choices:
            trail: list[int] = []
            if assign(edge, color, trail) and search():
                return True
            for assigned in reversed(trail):
                left, right = edges[assigned]
                used[left] ^= 1 << colors[assigned]
                used[right] ^= 1 << colors[assigned]
                colors[assigned] = -1
        return False

    return search()


def contains_double_star(mask: int) -> bool:
    both_01 = mask & 0x03 == 0x03
    both_02 = mask & 0x0C == 0x0C
    both_12 = mask & 0x30 == 0x30
    return (both_01 and both_02) or (both_01 and both_12) or (
        both_02 and both_12
    )


class GraphReplay:
    def __init__(self, row: str, require_nontait: bool, require_cyclic4: bool,
                 require_girth: int | None) -> None:
        self.row = row
        self.n, self.edges, self.incidence = decode_graph6(row)
        self.m = len(self.edges)
        check_biconnected(self.n, self.edges)
        if require_cyclic4:
            check_cyclic_connectivity_four(self.n, self.edges)
        if require_girth is not None and girth(self.n, self.edges) < require_girth:
            raise ValueError(f"girth is less than {require_girth}")
        if require_nontait and is_three_edge_colorable(self.edges, self.incidence):
            raise ValueError("graph is Tait colorable")
        self.proper = [
            all(vertex != z for vertex in self.edges[root])
            for z in range(self.n)
            for root in range(self.m)
        ]
        self.aggregate_masks = [0] * (self.n * self.m)
        self.aggregate_ports = [0] * (self.n * self.m)
        self.simultaneous = [False] * (self.n * self.m)
        self.states = 0

    def add_state(self, encoded: str) -> None:
        if len(encoded) != 2 * self.m:
            raise ValueError("wrong flow encoding length")
        state = [int(encoded[2 * i : 2 * i + 2], 16) for i in range(self.m)]
        if any(label not in LABELS for label in state):
            raise ValueError("flow uses a label outside D5")
        for incident in self.incidence:
            if state[incident[0]] ^ state[incident[1]] ^ state[incident[2]]:
                raise ValueError("flow violates a vertex xor equation")

        typed_masks = [0] * (self.n * self.m)
        external_ports = [0] * (self.n * self.m)
        for pair in LABELS:
            active = [((label & pair).bit_count() == 1) for label in state]
            for incident in self.incidence:
                if sum(active[edge] for edge in incident) not in (0, 2):
                    raise ValueError("factor is not even")
            component = [-1] * self.m
            next_component = 0
            for start in range(self.m):
                if not active[start] or component[start] >= 0:
                    continue
                component[start] = next_component
                stack = [start]
                while stack:
                    edge = stack.pop()
                    for vertex in self.edges[edge]:
                        for neighbor in self.incidence[vertex]:
                            if active[neighbor] and component[neighbor] < 0:
                                component[neighbor] = next_component
                                stack.append(neighbor)
                next_component += 1

            for z in range(self.n):
                active_slots = [
                    slot
                    for slot, edge in enumerate(self.incidence[z])
                    if active[edge]
                ]
                if len(active_slots) != 2:
                    continue
                inactive_slot = next(slot for slot in range(3) if slot not in active_slots)
                inactive_label = state[self.incidence[z][inactive_slot]]
                if pair != inactive_label and pair & inactive_label:
                    raise ValueError("factor has invalid inactive relation")
                physical = {(0, 1): 0, (0, 2): 1, (1, 2): 2}[
                    tuple(active_slots)
                ]
                mode = int(pair != inactive_label)
                port_bits = sum(1 << slot for slot in active_slots)
                component_id = component[self.incidence[z][active_slots[0]]]
                for root in range(self.m):
                    index = z * self.m + root
                    if self.proper[index] and component[root] == component_id:
                        typed_masks[index] |= 1 << (2 * physical + mode)
                        if mode:
                            external_ports[index] |= port_bits

        for index, is_proper in enumerate(self.proper):
            if not is_proper:
                continue
            self.aggregate_masks[index] |= typed_masks[index]
            self.aggregate_ports[index] |= external_ports[index]
            self.simultaneous[index] |= external_ports[index] == 7
        self.states += 1

    def finish(self, expected_proper: int) -> tuple[int, int, int, int]:
        proper = sum(self.proper)
        if proper != expected_proper:
            raise ValueError("proper-interface count mismatch")
        double_star = sum(
            contains_double_star(self.aggregate_masks[index])
            for index, is_proper in enumerate(self.proper)
            if is_proper
        )
        aggregate = sum(
            self.aggregate_ports[index] == 7
            for index, is_proper in enumerate(self.proper)
            if is_proper
        )
        simultaneous = sum(
            self.simultaneous[index]
            for index, is_proper in enumerate(self.proper)
            if is_proper
        )
        if (double_star, aggregate, simultaneous) != (proper, proper, proper):
            raise ValueError(
                "witness set does not establish all three predicates: "
                f"{double_star}, {aggregate}, {simultaneous} of {proper}"
            )
        return proper, double_star, aggregate, simultaneous


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--corpus-name", required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--expected-graphs", required=True, type=int)
    parser.add_argument("--require-nontait", action="store_true")
    parser.add_argument("--require-cyclic4", action="store_true")
    parser.add_argument("--require-girth", type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    lines = args.certificate.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != "D5_ROOTED_INTERFACE_WITNESSES_V1":
        raise ValueError("bad witness header")

    corpus = hashlib.sha256()
    graphs = 0
    states = 0
    interfaces = 0
    double_star = 0
    aggregate = 0
    simultaneous = 0
    current: GraphReplay | None = None
    expected_states = 0
    expected_proper = 0

    def finish_current() -> None:
        nonlocal states, interfaces, double_star, aggregate, simultaneous
        if current is None:
            return
        if current.states != expected_states:
            raise ValueError("witness-state count mismatch")
        proper, local_double, local_aggregate, local_simultaneous = current.finish(
            expected_proper
        )
        states += current.states
        interfaces += proper
        double_star += local_double
        aggregate += local_aggregate
        simultaneous += local_simultaneous

    for line in lines[1:]:
        fields = line.split("\t")
        if fields[0] == "G":
            finish_current()
            if len(fields) != 7:
                raise ValueError("bad graph witness record")
            graphs += 1
            if int(fields[1]) != graphs:
                raise ValueError("nonsequential graph index")
            row = fields[2]
            corpus.update((row + "\n").encode("ascii"))
            current = GraphReplay(
                row,
                require_nontait=args.require_nontait,
                require_cyclic4=args.require_cyclic4,
                require_girth=args.require_girth,
            )
            if (current.n, current.m) != (int(fields[3]), int(fields[4])):
                raise ValueError("graph metadata mismatch")
            expected_proper = int(fields[5])
            expected_states = int(fields[6])
        elif fields[0] == "F":
            if len(fields) != 2 or current is None:
                raise ValueError("bad flow witness record")
            current.add_state(fields[1])
        else:
            raise ValueError("unknown witness record")
    finish_current()

    digest = corpus.hexdigest()
    if graphs != args.expected_graphs:
        raise ValueError(f"expected {args.expected_graphs} graphs, got {graphs}")
    if digest != args.expected_sha256:
        raise ValueError(f"corpus hash mismatch: {digest}")
    print(
        f"VERIFY corpus={args.corpus_name} graphs={graphs} "
        f"corpus_sha256={digest} witness_states={states} "
        f"interfaces={interfaces} double_star={double_star} "
        f"aggregate_external={aggregate} simultaneous_external={simultaneous} PASS"
    )


if __name__ == "__main__":
    main()
