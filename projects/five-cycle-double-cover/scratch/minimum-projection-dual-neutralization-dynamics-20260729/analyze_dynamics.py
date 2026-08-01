#!/usr/bin/env python3
"""Exact Proposition-5 neutralization graph of the size-14 counterstate."""

from __future__ import annotations

import itertools
import importlib.util
from collections import Counter, deque
from pathlib import Path


GL = tuple((0,) + row for row in itertools.permutations((1, 2, 3)))
IDENTITY = (0, 1, 2, 3)
PARTITION = tuple(map(int, "01234444413024"))
CIRCUITS = (tuple(range(7)), tuple(range(7, 14)))
DERIVATIVE = tuple(map(int, "3111121" + "2111311"))


def compose(first, second):
    """Return first after second."""
    return tuple(first[second[value]] for value in range(4))


def inverse(mapping):
    result = [0] * 4
    for value, image in enumerate(mapping):
        result[image] = value
    return tuple(result)


def q(value):
    return ((value >> 1) & 1) & (value & 1)


def integrate(transitions):
    base = [0] * 14
    for circuit in CIRCUITS:
        current = 0
        for position in circuit:
            current ^= transitions[position]
            base[position] = current
        assert current == 0
    return tuple(base)


def block_q(base):
    result = [0] * 5
    for circuit in CIRCUITS:
        for local, position in enumerate(circuit):
            previous = circuit[local - 1]
            result[PARTITION[position]] ^= q(base[previous]) ^ q(base[position])
    return tuple(result)


def key_transitions(key):
    u1, u2, u3, a, b = key
    return (
        3, u1, u2, u3, a, b, a,
        b, a, u1, u3, 3, u2, a,
    )


def transition_sums(transitions):
    rows = [[0, 0] for _ in range(5)]
    for circuit_index, circuit in enumerate(CIRCUITS):
        for position in circuit:
            rows[PARTITION[position]][circuit_index] ^= transitions[position]
    return tuple(tuple(row) for row in rows)


def states():
    result = []
    for u1, u2, u3 in itertools.product((1, 2, 3), repeat=3):
        b = 3 ^ u1 ^ u2 ^ u3
        if b == 0:
            continue
        for a in (1, 2, 3):
            if a != b:
                result.append((u1, u2, u3, a, b))
    assert len(result) == len(set(result)) == 40
    return tuple(sorted(result))


STATES = states()
STATE_SET = set(STATES)


HERE = Path(__file__).resolve().parent
REALIZATION_PATH = (
    HERE.parent
    / "minimum-projection-size14-dichotomy-counterstate-20260729"
    / "analyze_realization.py"
)
REALIZATION_SPEC = importlib.util.spec_from_file_location(
    "counterstate_realization", REALIZATION_PATH
)
assert REALIZATION_SPEC is not None and REALIZATION_SPEC.loader is not None
REALIZATION = importlib.util.module_from_spec(REALIZATION_SPEC)
REALIZATION_SPEC.loader.exec_module(REALIZATION)
GRAPH_CYCLES = REALIZATION.all_cycles(REALIZATION.cycle_basis())
TARGET_H = REALIZATION.TARGET_H
ALL_EDGES = REALIZATION.ALL


def data(key):
    transitions = key_transitions(key)
    base = integrate(transitions)
    q_values = block_q(base)
    sums = transition_sums(transitions)
    assert all(first == second for first, second in sums)
    return transitions, base, q_values, sums


def exchange_profile(key, relative_shift):
    _transitions, base, _q_values, _sums = data(key)
    low = base[:7] + tuple(value ^ relative_shift for value in base[7:])
    result = []
    witnesses = []
    for colour in range(4):
        forbidden = sum(
            (low[edge] == colour) << edge for edge in range(14)
        )
        best_gain = -100
        best_cycle = None
        for cycle in GRAPH_CYCLES:
            if cycle & forbidden:
                continue
            gain = (cycle & TARGET_H).bit_count() - (
                cycle & (ALL_EDGES ^ TARGET_H)
            ).bit_count()
            if gain > best_gain:
                best_gain = gain
                best_cycle = cycle
        assert best_cycle is not None and best_gain >= 0
        result.append(best_gain)
        witnesses.append(best_cycle)
    return tuple(result), tuple(witnesses)


def witnesses(key):
    _transitions, _base, q_values, sums = data(key)
    result = []
    for mask in range(1, 1 << 5):
        charge = 0
        rhs = 0
        for block in range(5):
            if mask & (1 << block):
                charge ^= sums[block][0]
                rhs ^= q_values[block]
        if charge == 0 and rhs == 1:
            result.append(mask)
    assert result
    return tuple(result)


def switch(key, mask, operator):
    values = [3, key[0], key[1], key[2]]
    basis4 = [key[3], key[4]]
    normalizer = inverse(operator) if mask & 1 else IDENTITY

    def changed(block, value):
        if mask & (1 << block):
            value = operator[value]
        return normalizer[value]

    new = (
        changed(1, values[1]),
        changed(2, values[2]),
        changed(3, values[3]),
        changed(4, basis4[0]),
        changed(4, basis4[1]),
    )
    assert new in STATE_SET
    return new


def neutralizes(source, target, mask):
    _t0, _b0, q0, _s0 = data(source)
    _t1, _b1, q1, _s1 = data(target)
    before = after = 0
    for block in range(5):
        if mask & (1 << block):
            before ^= q0[block]
            after ^= q1[block]
    assert before == 1
    return after == 0


def graph():
    adjacency = {key: [] for key in STATES}
    for key in STATES:
        for mask in witnesses(key):
            for operator in GL:
                target = switch(key, mask, operator)
                if neutralizes(key, target, mask):
                    adjacency[key].append((target, mask, operator))
        assert adjacency[key]
    return adjacency


def strongly_connected_components(adjacency):
    index = 0
    stack = []
    on_stack = set()
    indices = {}
    low = {}
    result = []

    def visit(vertex):
        nonlocal index
        indices[vertex] = low[vertex] = index
        index += 1
        stack.append(vertex)
        on_stack.add(vertex)
        for neighbour, _mask, _operator in adjacency[vertex]:
            if neighbour not in indices:
                visit(neighbour)
                low[vertex] = min(low[vertex], low[neighbour])
            elif neighbour in on_stack:
                low[vertex] = min(low[vertex], indices[neighbour])
        if low[vertex] == indices[vertex]:
            component = []
            while True:
                item = stack.pop()
                on_stack.remove(item)
                component.append(item)
                if item == vertex:
                    break
            result.append(tuple(sorted(component)))

    for vertex in adjacency:
        if vertex not in indices:
            visit(vertex)
    return tuple(sorted(result, key=lambda row: (len(row), row)))


def shortest_cycle(adjacency):
    best = None
    for root in STATES:
        queue = deque([root])
        parent = {root: None}
        parent_edge = {}
        while queue:
            vertex = queue.popleft()
            for edge in adjacency[vertex]:
                neighbour = edge[0]
                if neighbour == root:
                    path = []
                    cursor = vertex
                    while cursor != root:
                        path.append((parent[cursor], cursor, parent_edge[cursor]))
                        cursor = parent[cursor]
                    path.reverse()
                    path.append((vertex, root, edge))
                    if best is None or len(path) < len(best):
                        best = path
                    queue.clear()
                    break
                if neighbour not in parent:
                    parent[neighbour] = vertex
                    parent_edge[neighbour] = edge
                    queue.append(neighbour)
    assert best is not None
    return tuple(best)


def mask_text(mask):
    return "".join(str(block) for block in range(5) if mask & (1 << block))


def key_text(key):
    return "".join(map(str, key))


def main():
    adjacency = graph()
    components = strongly_connected_components(adjacency)
    cycle = shortest_cycle(adjacency)
    edge_count = sum(len(rows) for rows in adjacency.values())
    unique_edges = {
        (source, target)
        for source, rows in adjacency.items()
        for target, _mask, _operator in rows
    }
    witness_histogram = Counter(len(witnesses(key)) for key in STATES)
    q_weight_histogram = Counter(sum(data(key)[2]) for key in STATES)
    exchange_rows = {
        (key, shift): exchange_profile(key, shift)
        for key in STATES
        for shift in range(4)
    }
    exchange_valid = tuple(
        (key, shift)
        for (key, shift), (profile, _witnesses) in exchange_rows.items()
        if max(profile) == 0
    )
    exchange_max_gain_histogram = Counter(
        max(profile) for profile, _witnesses in exchange_rows.values()
    )
    exchange_minimax = {
        key: min(
            max(exchange_rows[(key, shift)][0])
            for shift in range(4)
        )
        for key in STATES
    }
    exchange_minimax_histogram = Counter(exchange_minimax.values())
    assert not exchange_valid
    print("PASS: exact Proposition-5 neutralization dynamics")
    print(f"states={len(STATES)} directed_certificates={edge_count}")
    print(f"unique_directed_state_edges={len(unique_edges)}")
    print(
        "scc_sizes=" + ",".join(map(str, sorted(map(len, components), reverse=True)))
    )
    print(
        "witness_count_histogram="
        + ",".join(f"{key}:{value}" for key, value in sorted(witness_histogram.items()))
    )
    print(
        "q_weight_histogram="
        + ",".join(f"{key}:{value}" for key, value in sorted(q_weight_histogram.items()))
    )
    print(
        "exchange_max_gain_histogram="
        + ",".join(
            f"{key}:{value}"
            for key, value in sorted(exchange_max_gain_histogram.items())
        )
    )
    print(
        "exchange_minimax_histogram="
        + ",".join(
            f"{key}:{value}"
            for key, value in sorted(exchange_minimax_histogram.items())
        )
    )
    print(f"exchange_valid_state_translations={len(exchange_valid)}")
    print(f"shortest_cycle_length={len(cycle)}")
    for index, (source, target, edge) in enumerate(cycle):
        _target, mask, operator = edge
        print(
            f"cycle_step={index} source={key_text(source)} "
            f"witness={mask_text(mask)} operator={''.join(map(str, operator))} "
            f"target={key_text(target)} "
            f"source_Q={''.join(map(str, data(source)[2]))} "
            f"target_Q={''.join(map(str, data(target)[2]))}"
        )
        profiles = tuple(exchange_profile(source, shift)[0] for shift in range(4))
        print(
            f"cycle_step_exchange={index} "
            + "|".join("".join(map(str, profile)) for profile in profiles)
        )
        print(
            f"cycle_step_exchange_minimax={index} "
            f"{exchange_minimax[source]}"
        )
        for shift in range(4):
            profile, profile_witnesses = exchange_rows[(source, shift)]
            best_colour = max(range(4), key=lambda colour: profile[colour])
            witness = profile_witnesses[best_colour]
            witness_edges = ",".join(
                str(edge)
                for edge in range(REALIZATION.M)
                if (witness >> edge) & 1
            )
            print(
                f"cycle_step_exchange_witness={index} "
                f"shift={shift} colour={best_colour} "
                f"gain={profile[best_colour]} edges={witness_edges}"
            )


if __name__ == "__main__":
    main()
