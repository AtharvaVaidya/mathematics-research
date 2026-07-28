#!/usr/bin/env python3
"""Search cyclically-four-connected Petersen four-pole gluings.

This is a targeted search for a countermodel to the sufficient assertion
that every nowhere-zero F_2^3-flow has a cleanable functional projection.
It is not a Five-CDC solver.

Four copies of the Petersen graph have the endpoints of one edge deleted.
Their sixteen dangling incidences are paired value-preservingly.  The
resulting cubic graph has order 32.  We retain only pairings whose macro
four-vertex multigraph has no cut below four and then check cyclic
four-edge-connectivity literally.  Cleanability is decided by the exact
CNF model in search_iterated_petersen_fano_obstruction.py.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parent.parent
BASE_SOURCE = ROOT / "scratch/search_iterated_petersen_fano_obstruction.py"


def load_base():
    spec = importlib.util.spec_from_file_location("petersen_base", BASE_SOURCE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@dataclass(frozen=True)
class State:
    values: tuple[int, ...]
    deleted_edge: int
    ports: tuple[tuple[int, int, int], ...]  # (surviving vertex, value, side)
    covered_functionals: tuple[int, ...]


def cycle_masks(edges: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    result = []
    for mask in range(1 << len(edges)):
        if all(
            sum(
                (mask >> edge) & 1
                for edge, endpoints in enumerate(edges)
                if vertex in endpoints
            )
            % 2
            == 0
            for vertex in range(10)
        ):
            result.append(mask)
    assert len(result) == 64
    return tuple(result)


def perfect_matchings(edges: tuple[tuple[int, int], ...]) -> tuple[frozenset[int], ...]:
    result = []
    for choice in itertools.combinations(range(len(edges)), 5):
        endpoints = [vertex for edge in choice for vertex in edges[edge]]
        if len(set(endpoints)) == 10:
            result.append(frozenset(choice))
    assert len(result) == 6
    return tuple(result)


def enumerate_states(base, deleted_in_factor: bool = True) -> tuple[State, ...]:
    edges = base.PETERSEN_EDGES
    cycles = cycle_masks(edges)
    matchings = set(perfect_matchings(edges))
    states: set[State] = set()
    for first in cycles:
        for second in cycles:
            for third in cycles:
                if (first | second | third) != (1 << 15) - 1:
                    continue
                values = tuple(
                    ((first >> edge) & 1)
                    | (((second >> edge) & 1) << 1)
                    | (((third >> edge) & 1) << 2)
                    for edge in range(15)
                )
                for deleted_edge, (u, v) in enumerate(edges):
                    covered_rows = []
                    for functional in range(1, 8):
                        factor = frozenset(
                            edge
                            for edge, value in enumerate(values)
                            if (functional & value).bit_count() % 2 == 0
                        )
                        if factor in matchings and (
                            (deleted_edge in factor) == deleted_in_factor
                        ):
                            covered_rows.append(functional)
                    covered = tuple(covered_rows)
                    if not covered:
                        continue
                    ports = []
                    for side, removed in enumerate((u, v)):
                        for edge, endpoints in enumerate(edges):
                            if deleted_edge == edge or removed not in endpoints:
                                continue
                            neighbor = endpoints[0] ^ endpoints[1] ^ removed
                            ports.append((neighbor, values[edge], side))
                    assert len(ports) == 4
                    states.add(State(values, deleted_edge, tuple(ports), covered))
    result = tuple(states)
    assert result
    return result


def random_value_pairing(
    chosen: tuple[State, ...], generator: random.Random
) -> tuple[tuple[int, int, int, int], ...] | None:
    # A connector is (block_a, port_a, block_b, port_b).
    by_value: dict[int, list[tuple[int, int]]] = {}
    for block, state in enumerate(chosen):
        for port, (_, value, _) in enumerate(state.ports):
            by_value.setdefault(value, []).append((block, port))
    if any(len(ports) % 2 for ports in by_value.values()):
        return None

    for _ in range(64):
        connectors = []
        okay = True
        for ports in by_value.values():
            pool = ports[:]
            generator.shuffle(pool)
            while pool:
                first = pool.pop()
                choices = [
                    index
                    for index, second in enumerate(pool)
                    if second[0] != first[0]
                ]
                if not choices:
                    okay = False
                    break
                index = generator.choice(choices)
                second = pool.pop(index)
                connectors.append((*first, *second))
            if not okay:
                break
        if not okay or len(connectors) != 8:
            continue
        macro = nx.MultiGraph()
        macro.add_nodes_from(range(4))
        macro.add_edges_from((a, b) for a, _, b, _ in connectors)
        if nx.is_connected(macro) and nx.edge_connectivity(macro) >= 4:
            return tuple(connectors)
    return None


def random_central_core(
    chosen: tuple[State, ...], generator: random.Random
) -> tuple[
    tuple[tuple[int, int, int, int], ...],
    tuple[tuple[int, int, int], ...],
] | None:
    """Pair ports at eight central vertices, then match equal XOR values.

    The first returned tuple records (block, port, block, port) at each
    central vertex.  The second records (central_a, central_b, value) for
    the four internal central matching edges.
    """

    ports = [(block, port) for block in range(4) for port in range(4)]
    for _ in range(512):
        generator.shuffle(ports)
        central_ports = []
        xors: dict[int, list[int]] = {}
        okay = True
        for central in range(8):
            first = ports[2 * central]
            second = ports[2 * central + 1]
            if first[0] == second[0]:
                okay = False
                break
            value_first = chosen[first[0]].ports[first[1]][1]
            value_second = chosen[second[0]].ports[second[1]][1]
            value = value_first ^ value_second
            if value == 0:
                okay = False
                break
            central_ports.append((*first, *second))
            xors.setdefault(value, []).append(central)
        if not okay or any(len(rows) % 2 for rows in xors.values()):
            continue
        central_edges = []
        for value, rows in xors.items():
            generator.shuffle(rows)
            central_edges.extend(
                (rows[index], rows[index + 1], value)
                for index in range(0, len(rows), 2)
            )
        macro = nx.Graph()
        macro.add_nodes_from(range(12))
        for central, (block_a, _, block_b, _) in enumerate(central_ports):
            macro.add_edge(block_a, 4 + central)
            macro.add_edge(block_b, 4 + central)
        macro.add_edges_from(
            (4 + first, 4 + second) for first, second, _ in central_edges
        )
        if nx.is_connected(macro) and nx.edge_connectivity(macro) >= 3:
            return tuple(central_ports), tuple(central_edges)
    return None


def build(base, chosen: tuple[State, ...], connectors, central_edges=()):
    edges = base.PETERSEN_EDGES
    deleted_vertices = [set(edges[state.deleted_edge]) for state in chosen]
    kept = [
        [vertex for vertex in range(10) if vertex not in deleted_vertices[block]]
        for block in range(4)
    ]
    central_order = 8 if central_edges else 0
    relabel = {
        (block, vertex): block * 8 + index
        for block in range(4)
        for index, vertex in enumerate(kept[block])
    }
    output_edges: list[tuple[int, int]] = []
    output_values: list[int] = []
    for block, state in enumerate(chosen):
        removed = deleted_vertices[block]
        for edge, (u, v) in enumerate(edges):
            if u in removed or v in removed:
                continue
            output_edges.append(
                tuple(sorted((relabel[(block, u)], relabel[(block, v)])))
            )
            output_values.append(state.values[edge])
    for connector, (block_a, port_a, block_b, port_b) in enumerate(connectors):
        vertex_a, value_a, _ = chosen[block_a].ports[port_a]
        vertex_b, value_b, _ = chosen[block_b].ports[port_b]
        if central_edges:
            central = 32 + connector
            output_edges.extend(
                (
                    tuple(sorted((relabel[(block_a, vertex_a)], central))),
                    tuple(sorted((relabel[(block_b, vertex_b)], central))),
                )
            )
            output_values.extend((value_a, value_b))
        else:
            assert value_a == value_b
            output_edges.append(
                tuple(
                    sorted(
                        (
                            relabel[(block_a, vertex_a)],
                            relabel[(block_b, vertex_b)],
                        )
                    )
                )
            )
            output_values.append(value_a)
    for first, second, value in central_edges:
        output_edges.append(tuple(sorted((32 + first, 32 + second))))
        output_values.append(value)
    ordering = sorted(range(len(output_edges)), key=lambda edge: output_edges[edge])
    graph = base.FlowGraph(
        32 + central_order,
        tuple(output_edges[edge] for edge in ordering),
        tuple(output_values[edge] for edge in ordering),
    )
    base.validate(graph)
    return graph


def cyclic_connectivity_at_least_four(graph) -> bool:
    adjacency = [[] for _ in range(graph.order)]
    for edge, (u, v) in enumerate(graph.edges):
        adjacency[u].append((v, edge))
        adjacency[v].append((u, edge))
    edge_ids = range(len(graph.edges))
    for size in range(1, 4):
        for removed in itertools.combinations(edge_ids, size):
            blocked = set(removed)
            unseen = set(range(graph.order))
            components = []
            while unseen:
                root = unseen.pop()
                component = {root}
                stack = [root]
                while stack:
                    vertex = stack.pop()
                    for neighbor, edge in adjacency[vertex]:
                        if edge not in blocked and neighbor in unseen:
                            unseen.remove(neighbor)
                            component.add(neighbor)
                            stack.append(neighbor)
                components.append(component)
            if len(components) <= 1:
                continue
            cyclic = 0
            for component in components:
                induced_edges = sum(
                    1
                    for edge, (u, v) in enumerate(graph.edges)
                    if edge not in blocked and u in component and v in component
                )
                if induced_edges >= len(component):
                    cyclic += 1
            if cyclic >= 2:
                return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260728)
    parser.add_argument("--trials", type=int, default=10000)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--central-core", action="store_true")
    parser.add_argument("--deleted-outside-factor", action="store_true")
    parser.add_argument("--skip-cyclic-check", action="store_true")
    parser.add_argument("--cadical", default=shutil.which("cadical"))
    arguments = parser.parse_args()
    if not arguments.cadical:
        raise SystemExit("cadical not found")
    base = load_base()
    states = enumerate_states(
        base, deleted_in_factor=not arguments.deleted_outside_factor
    )
    generator = random.Random(arguments.seed)
    by_signature: dict[tuple[tuple[int, ...], tuple[int, ...]], list[State]] = {}
    for state in states:
        port_values = tuple(sorted(value for _, value, _ in state.ports))
        by_signature.setdefault((state.covered_functionals, port_values), []).append(
            state
        )
    representatives = [
        generator.choice(rows) for rows in by_signature.values()
    ]
    by_coverage: dict[tuple[int, ...], list[State]] = {}
    for representative in representatives:
        by_coverage.setdefault(
            representative.covered_functionals, []
        ).append(representative)
    cover_profiles = [
        choice
        for choice in itertools.combinations_with_replacement(
            tuple(by_coverage), 4
        )
        if set().union(*(set(profile) for profile in choice))
        == set(range(1, 8))
    ]
    print(
        json.dumps(
            {
                "states": len(states),
                "representative_states": len(representatives),
                "signatures": len(by_signature),
                "cover_profiles": len(cover_profiles),
            }
        ),
        flush=True,
    )

    tested = 0
    cyclic4 = 0
    histogram: dict[int, int] = {}
    best = None
    for trial in range(arguments.trials):
        profiles = generator.choice(cover_profiles)
        chosen = tuple(
            generator.choice(by_coverage[profile]) for profile in profiles
        )
        if arguments.central_core:
            core = random_central_core(chosen, generator)
            if core is None:
                continue
            connectors, central_edges = core
            graph = build(base, chosen, connectors, central_edges)
        else:
            connectors = random_value_pairing(chosen, generator)
            central_edges = ()
            if connectors is None:
                continue
            graph = build(base, chosen, connectors)
        tested += 1
        if (
            not arguments.skip_cyclic_check
            and not cyclic_connectivity_at_least_four(graph)
        ):
            continue
        cyclic4 += 1
        bad = base.profile(graph, arguments.cadical)
        histogram[len(bad)] = histogram.get(len(bad), 0) + 1
        if best is None or len(bad) > len(best["bad_functionals"]):
            best = {
                "trial": trial,
                "graph6": base.graph6(graph),
                "edges": graph.edges,
                "flow_values": graph.values,
                "bad_functionals": bad,
                "local_covered_functionals": [
                    state.covered_functionals for state in chosen
                ],
                "deleted_edges": [state.deleted_edge for state in chosen],
                "connectors": connectors,
                "central_edges": central_edges,
            }
            print(
                json.dumps(
                    {
                        "trial": trial,
                        "tested": tested,
                        "cyclic4": cyclic4,
                        "bad": bad,
                        "local": best["local_covered_functionals"],
                    }
                ),
                flush=True,
            )
        if len(bad) == 7:
            break

    report = {
        "schema": "petersen-fourpole-allseven-search-v1",
        "seed": arguments.seed,
        "trials": arguments.trials,
        "tested": tested,
        "cyclic4": cyclic4,
        "histogram": histogram,
        "best": best,
    }
    print(json.dumps({key: value for key, value in report.items() if key != "best"}))
    if arguments.output:
        arguments.output.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
