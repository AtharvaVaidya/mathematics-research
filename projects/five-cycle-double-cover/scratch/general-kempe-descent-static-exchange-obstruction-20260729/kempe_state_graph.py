#!/usr/bin/env python3
"""Exact multi-round boundary reconfiguration census for this multipole.

The four small complement components are K4-e two-poles.  Their terminal
colour is one of 1,2,3 and their boundary pairing is forced.  The large
component has 252 proper three-edge-colourings with 252 distinct boundary
profiles.  This checker enumerates all circuit-integrable products, builds
the charge-preserving Kempe graph, and checks direct clean/delete goals.
"""

from __future__ import annotations

import functools
import itertools
from collections import defaultdict, deque

import verify as core


BASE = core.read_base()
W4_VERTICES = set(range(32, 42))
TERMINALS = tuple(
    tuple(position for position, owner in enumerate(core.PARTITION) if owner == block)
    for block in range(5)
)


def enumerate_large_component():
    edge_indices = tuple(
        edge_index
        for edge_index, edge in enumerate(BASE)
        if edge[3] != "support"
        and (edge[0] in W4_VERTICES or edge[1] in W4_VERTICES)
    )
    local_index = {edge_index: local for local, edge_index in enumerate(edge_indices)}
    boundary = []
    for edge_index in edge_indices:
        edge = BASE[edge_index]
        if edge[3] != "boundary":
            continue
        terminal = edge[0] if edge[0] < 16 else edge[1]
        boundary.append((terminal, edge_index))
    boundary.sort()

    order = sorted(
        range(len(edge_indices)),
        key=lambda local: -sum(
            endpoint in W4_VERTICES for endpoint in BASE[edge_indices[local]][:2]
        ),
    )
    used = {vertex: 0 for vertex in W4_VERTICES}
    colours = [0] * len(edge_indices)
    result = {}

    def search(depth):
        if depth == len(order):
            profile = tuple(
                colours[local_index[edge_index]]
                for _terminal, edge_index in boundary
            )
            assert profile not in result
            result[profile] = tuple(colours)
            return
        local = order[depth]
        edge_index = edge_indices[local]
        u, v = BASE[edge_index][:2]
        forbidden = (
            (used[u] if u in W4_VERTICES else 0)
            | (used[v] if v in W4_VERTICES else 0)
        )
        for colour in (1, 2, 3):
            bit = 1 << colour
            if forbidden & bit:
                continue
            colours[local] = colour
            if u in W4_VERTICES:
                used[u] |= bit
            if v in W4_VERTICES:
                used[v] |= bit
            search(depth + 1)
            if u in W4_VERTICES:
                used[u] ^= bit
            if v in W4_VERTICES:
                used[v] ^= bit

    search(0)
    assert len(result) == 252
    return edge_indices, tuple(boundary), result


W4_EDGES, W4_BOUNDARY, PROFILE_COLOURING = enumerate_large_component()


@functools.lru_cache(maxsize=None)
def large_pairing(profile, colour_pair):
    colours = PROFILE_COLOURING[profile]
    adjacency = defaultdict(list)
    for local, edge_index in enumerate(W4_EDGES):
        if colours[local] not in colour_pair:
            continue
        u, v = BASE[edge_index][:2]
        adjacency[u].append(v)
        adjacency[v].append(u)
    terminal_set = {
        terminal
        for (terminal, _edge_index), colour in zip(W4_BOUNDARY, profile)
        if colour in colour_pair
    }
    seen = set()
    pairs = []
    for root in sorted(terminal_set):
        if root in seen:
            continue
        queue = deque([root])
        seen.add(root)
        endpoints = []
        while queue:
            vertex = queue.popleft()
            if vertex in terminal_set:
                endpoints.append(vertex)
            for neighbour in adjacency[vertex]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        assert len(endpoints) == 2
        pairs.append(tuple(sorted(endpoints)))
    return tuple(sorted(pairs))


def all_integrable_states():
    result = []
    for small_colours in itertools.product((1, 2, 3), repeat=4):
        for profile in PROFILE_COLOURING:
            derivative = [0] * 16
            for block, colour in enumerate(small_colours):
                for terminal in TERMINALS[block]:
                    derivative[terminal] = colour
            for terminal, colour in zip(TERMINALS[4], profile):
                derivative[terminal] = colour
            derivative = tuple(derivative)
            if core.integrate(derivative) is not None:
                result.append(derivative)
    assert len(result) == len(set(result)) == 5094
    return tuple(result)


STATES = all_integrable_states()
STATE_SET = set(STATES)


@functools.lru_cache(maxsize=None)
def neighbours(derivative):
    result = set()
    large_profile = tuple(derivative[position] for position in TERMINALS[4])
    for colour_pair in core.COLOUR_PAIRS:
        paths = []
        for block in range(4):
            if derivative[TERMINALS[block][0]] in colour_pair:
                paths.append(TERMINALS[block])
        paths.extend(large_pairing(large_profile, colour_pair))
        same = [
            pair for pair in paths if (pair[0] < 8) == (pair[1] < 8)
        ]
        cross = [
            pair for pair in paths if (pair[0] < 8) != (pair[1] < 8)
        ]
        # These moves generate every even-cross-parity path subset:
        # one same-circuit path, or two cross-circuit paths.
        moves = [(pair,) for pair in same]
        moves.extend(itertools.combinations(cross, 2))
        delta = colour_pair[0] ^ colour_pair[1]
        for selected in moves:
            changed = list(derivative)
            for pair in selected:
                for endpoint in pair:
                    changed[endpoint] ^= delta
            changed = tuple(changed)
            assert changed in STATE_SET
            result.add(changed)
    return tuple(sorted(result))


def main():
    goals = {
        state
        for state in STATES
        if core.classify(state)[1] or core.classify(state)[2]
    }
    assert len(goals) == 3294

    root = STATES[0]
    reached = {root}
    queue = deque([root])
    while queue:
        state = queue.popleft()
        for following in neighbours(state):
            if following not in reached:
                reached.add(following)
                queue.append(following)
    assert len(reached) == len(STATES)

    edge_count = sum(len(neighbours(state)) for state in STATES) // 2
    degrees = tuple(len(neighbours(state)) for state in STATES)
    assert edge_count == 64497
    assert (min(degrees), max(degrees)) == (19, 34)

    initial = core.DERIVATIVE
    distance = {initial: 0}
    queue = deque([initial])
    nearest_goal = None
    while queue:
        state = queue.popleft()
        if state in goals:
            nearest_goal = distance[state]
            break
        for following in neighbours(state):
            if following not in distance:
                distance[following] = distance[state] + 1
                queue.append(following)
    assert nearest_goal == 2

    print("LARGE_COMPONENT colourings=252 boundary_profiles=252")
    print("INTEGRABLE_STATES 5094")
    print("DIRECT_CLEAN_OR_DELETE_STATES 3294")
    print(
        "KEMPE_GRAPH components=1 vertices=5094 edges=64497 "
        "degree_min=19 degree_max=34"
    )
    print("DISPLAYED_STATE nearest_clean_or_delete_distance=2")
    print(
        "PASS: the complete charge-preserving boundary Kempe graph for "
        "this multipole is connected and the displayed state escapes in two rounds"
    )


if __name__ == "__main__":
    main()
