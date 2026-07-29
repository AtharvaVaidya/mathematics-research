#!/usr/bin/env python3
"""Search coloured eight-poles for a goal-free dynamic Kempe component.

This is an exploratory search, not a certificate.  The support and the four
small two-poles are the size-16 state from the static-exchange package.  A
randomly generated connected eight-pole replaces its large complement block.
Literal internal colourings are retained in the state graph.
"""

from __future__ import annotations

import argparse
import functools
import itertools
import random
from collections import defaultdict, deque

LARGE_POSITIONS = (4, 5, 6, 7, 8, 9, 14, 15)
PARTITION = tuple(map(int, "0123444444130244"))
DERIVATIVE = tuple(map(int, "3111113121113132"))
CIRCUITS = (tuple(range(8)), tuple(range(8, 16)))
SMALL_POSITIONS = tuple(
    tuple(i for i, owner in enumerate(PARTITION) if owner == block)
    for block in range(4)
)
PAIRS = ((1, 2), (1, 3), (2, 3))
PERMS = tuple((0,) + row for row in itertools.permutations((1, 2, 3)))


def integrate(transitions):
    base = [0] * 16
    for circuit in CIRCUITS:
        value = 0
        for position in circuit:
            value ^= transitions[position]
            base[position] = value
        if value:
            return None
    return tuple(base)


def clean(base):
    for relative_shift in range(4):
        parity = [[0] * 4 for _ in range(5)]
        for circuit_index, circuit in enumerate(CIRCUITS):
            shift = relative_shift if circuit_index else 0
            for local, edge in enumerate(circuit):
                successor = circuit[(local + 1) % len(circuit)]
                left, right = PARTITION[edge], PARTITION[successor]
                if left == right:
                    continue
                colour = base[edge] ^ shift
                parity[left][colour] ^= 1
                parity[right][colour] ^= 1
        if not any(bit for row in parity for bit in row):
            return True
    return False


def random_pole(rng: random.Random, order: int, profile: tuple[int, ...]):
    """Generate a simple properly coloured eight-pole on `order` vertices."""
    assert order % 2 == 0
    for _attempt in range(10_000):
        boundary_vertex = [-1] * 8
        available = {
            colour: list(range(order))
            for colour in (1, 2, 3)
        }
        ok = True
        for terminal, colour in enumerate(profile):
            if not available[colour]:
                ok = False
                break
            chosen = rng.choice(available[colour])
            available[colour].remove(chosen)
            boundary_vertex[terminal] = chosen
        if not ok or any(len(row) % 2 for row in available.values()):
            continue

        edges = [(boundary_vertex[t], -(t + 1)) for t in range(8)]
        colours = list(profile)
        pairs = set()
        for colour in (1, 2, 3):
            ports = available[colour]
            rng.shuffle(ports)
            for a, b in zip(ports[::2], ports[1::2]):
                pair = tuple(sorted((a, b)))
                if a == b or pair in pairs:
                    ok = False
                    break
                pairs.add(pair)
                edges.append((a, b))
                colours.append(colour)
            if not ok:
                break
        if not ok:
            continue

        adjacency = [[] for _ in range(order)]
        for edge_index, (a, b) in enumerate(edges):
            if a >= 0:
                adjacency[a].append(edge_index)
            if b >= 0:
                adjacency[b].append(edge_index)
        if any(len(row) != 3 for row in adjacency):
            continue
        seen = {0}
        stack = [0]
        while stack:
            vertex = stack.pop()
            for edge_index in adjacency[vertex]:
                a, b = edges[edge_index]
                other = b if a == vertex else a
                if other >= 0 and other not in seen:
                    seen.add(other)
                    stack.append(other)
        if len(seen) != order:
            continue
        return tuple(edges), tuple(colours)
    return None


def k33_cut_pole(rng: random.Random):
    """Cut four random K3,3 edges and randomly label the eight half-edges."""
    full = tuple((a, b) for a in range(3) for b in range(3, 6))
    cut = set(rng.sample(full, 4))
    rows = []
    terminal = 0
    for edge in full:
        if edge not in cut:
            rows.append(edge)
            continue
        a, b = edge
        rows.append((a, -(terminal + 1)))
        terminal += 1
        rows.append((b, -(terminal + 1)))
        terminal += 1
    permutation = list(range(8))
    rng.shuffle(permutation)
    relabelled = []
    for a, b in rows:
        if b < 0:
            b = -(permutation[-b - 1] + 1)
        relabelled.append((a, b))
    relabelled.sort(key=lambda edge: (-edge[1] - 1) if edge[1] < 0 else 8)
    return tuple(relabelled), cut, tuple(permutation)


def enumerate_colourings(order, edges):
    incident = [[] for _ in range(order)]
    for edge_index, (a, b) in enumerate(edges):
        if a >= 0:
            incident[a].append(edge_index)
        if b >= 0:
            incident[b].append(edge_index)
    assert all(len(row) == 3 for row in incident)
    edge_vertices = [
        tuple(vertex for vertex in (a, b) if vertex >= 0)
        for a, b in edges
    ]
    values = [0] * len(edges)
    used = [0] * order
    result = []

    def recurse(done):
        if done == len(edges):
            result.append(tuple(values))
            return
        best = -1
        domain = None
        for edge_index, value in enumerate(values):
            if value:
                continue
            forbidden = 0
            for vertex in edge_vertices[edge_index]:
                forbidden |= used[vertex]
            choices = tuple(
                colour
                for colour in (1, 2, 3)
                if not forbidden & (1 << colour)
            )
            if not choices:
                return
            if domain is None or len(choices) < len(domain):
                best, domain = edge_index, choices
                if len(domain) == 1:
                    break
        for colour in domain:
            values[best] = colour
            for vertex in edge_vertices[best]:
                used[vertex] |= 1 << colour
            recurse(done + 1)
            for vertex in edge_vertices[best]:
                used[vertex] ^= 1 << colour
            values[best] = 0

    recurse(0)
    return tuple(result)


def boundary_profile(colouring):
    return colouring[:8]


def derivative(small, colouring):
    result = [0] * 16
    for block, colour in enumerate(small):
        for position in SMALL_POSITIONS[block]:
            result[position] = colour
    for position, colour in zip(LARGE_POSITIONS, boundary_profile(colouring)):
        result[position] = colour
    return tuple(result)


def integrable(transitions):
    return all(
        functools.reduce(
            int.__xor__, (transitions[position] for position in circuit), 0
        )
        == 0
        for circuit in CIRCUITS
    )


@functools.lru_cache(maxsize=None)
def is_goal(transitions):
    """Boolean classifier, quotienting equal-terminal two-pole relabellings."""
    assert transitions[SMALL_POSITIONS[0][0]] == transitions[SMALL_POSITIONS[0][1]]
    for targets in itertools.product((1, 2, 3), repeat=3):
        for large_map in PERMS:
            changed = list(transitions)
            for block, target in enumerate(targets, 1):
                for position in SMALL_POSITIONS[block]:
                    changed[position] = target
            for position in LARGE_POSITIONS:
                changed[position] = large_map[changed[position]]
            base = integrate(tuple(changed))
            if base is None:
                continue
            if clean(base):
                return True
            if any(
                len({base[position] for position in circuit}) < 4
                for circuit in CIRCUITS
            ):
                return True
    return False


def components_for_pair(order, edges, colouring, pair):
    adjacency = defaultdict(list)
    for edge_index, colour in enumerate(colouring):
        if colour not in pair:
            continue
        a, b = edges[edge_index]
        adjacency[a].append((b, edge_index))
        adjacency[b].append((a, edge_index))
    seen_edges = set()
    result = []
    for edge_index, colour in enumerate(colouring):
        if colour not in pair or edge_index in seen_edges:
            continue
        seen_edges.add(edge_index)
        stack = [edge_index]
        row = []
        terminals = set()
        while stack:
            current = stack.pop()
            row.append(current)
            for endpoint in edges[current]:
                if endpoint < 0:
                    terminals.add(-endpoint - 1)
                for _other, following in adjacency[endpoint]:
                    if following not in seen_edges:
                        seen_edges.add(following)
                        stack.append(following)
        assert len(terminals) in (0, 2)
        result.append((tuple(sorted(terminals)), tuple(sorted(row))))
    return tuple(result)


def search_one(order, edges, colourings):
    colouring_index = {row: index for index, row in enumerate(colourings)}
    states = []
    for small in itertools.product((1, 2, 3), repeat=4):
        for large_index, colouring in enumerate(colourings):
            if integrable(derivative(small, colouring)):
                states.append((small, large_index))
    state_set = set(states)
    if not states:
        return None, (0, 0, 0)

    @functools.lru_cache(maxsize=None)
    def mapped_states(state):
        small, large_index = state
        colouring = colourings[large_index]
        result = set()
        for targets in itertools.product((1, 2, 3), repeat=4):
            for permutation in PERMS:
                changed = tuple(permutation[value] for value in colouring)
                following = (targets, colouring_index[changed])
                if following in state_set:
                    result.add(following)
        return tuple(result)

    @functools.lru_cache(maxsize=None)
    def switch_states(state):
        small, large_index = state
        colouring = colourings[large_index]
        result = set()
        for pair in PAIRS:
            rows = []
            for block, colour in enumerate(small):
                if colour in pair:
                    rows.append(
                        (
                            tuple(SMALL_POSITIONS[block]),
                            ("small", block),
                        )
                    )
            for terminals, edge_row in components_for_pair(
                order, edges, colouring, pair
            ):
                positions = tuple(LARGE_POSITIONS[t] for t in terminals)
                rows.append((positions, ("large", edge_row)))
            delta = pair[0] ^ pair[1]
            for mask in range(1, 1 << len(rows)):
                endpoint_parity = [0, 0]
                for index, (positions, _payload) in enumerate(rows):
                    if not mask & (1 << index):
                        continue
                    for position in positions:
                        endpoint_parity[int(position >= 8)] ^= 1
                if endpoint_parity != [0, 0]:
                    continue
                changed_small = list(small)
                changed_colouring = list(colouring)
                for index, (_positions, payload) in enumerate(rows):
                    if not mask & (1 << index):
                        continue
                    if payload[0] == "small":
                        block = payload[1]
                        changed_small[block] ^= delta
                    else:
                        for edge_index in payload[1]:
                            changed_colouring[edge_index] ^= delta
                following = (
                    tuple(changed_small),
                    colouring_index[tuple(changed_colouring)],
                )
                assert following in state_set
                result.add(following)
        return tuple(result)

    unseen = set(states)
    components = 0
    while unseen:
        components += 1
        root = next(iter(unseen))
        reached = {root}
        queue = deque([root])
        all_bad = True
        while queue:
            state = queue.popleft()
            transitions = derivative(state[0], colourings[state[1]])
            if is_goal(transitions):
                all_bad = False
            for following in itertools.chain(
                mapped_states(state), switch_states(state)
            ):
                if following not in reached:
                    reached.add(following)
                    queue.append(following)
        unseen -= reached
        if all_bad:
            return (root, reached), (
                len(states),
                components,
                len(reached),
            )
    return None, (len(states), components, 0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=10)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260729)
    parser.add_argument("--k33-cut", action="store_true")
    args = parser.parse_args()
    rng = random.Random(args.seed)
    initial_profile = tuple(
        DERIVATIVE[position] for position in LARGE_POSITIONS
    )
    for trial in range(args.trials):
        metadata = None
        if args.k33_cut:
            edges, cut, permutation = k33_cut_pole(rng)
            displayed = ()
            order = 6
            metadata = (cut, permutation)
        else:
            generated = random_pole(rng, args.order, initial_profile)
            if generated is None:
                continue
            edges, displayed = generated
            order = args.order
        colourings = enumerate_colourings(order, edges)
        witness, summary = search_one(order, edges, colourings)
        print(
            f"trial={trial} colourings={len(colourings)}"
            f" states={summary[0]} components_seen={summary[1]}"
            f" bad_component={summary[2]}",
            flush=True,
        )
        if witness is not None:
            root, reached = witness
            print("FOUND")
            print(f"order={order}")
            print(f"edges={edges!r}")
            print(f"displayed={displayed!r}")
            print(f"metadata={metadata!r}")
            print(f"root={root!r}")
            print(f"component_size={len(reached)}")
            return
    print("NO_WITNESS")


if __name__ == "__main__":
    main()
