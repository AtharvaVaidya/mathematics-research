#!/usr/bin/env python3
"""Exact cover-level Kempe audit for the Petersen K6-duad cover.

The frozen Petersen witness labels its 15 edges by all 15 duads of K6,
once each, and the three labels at every graph vertex form a K6 triangle.
We regard this as an eight-coordinate CDC by adjoining coordinates 6 and 7
with empty support.

A legal cover-level Kempe move chooses coordinates i,j, takes one connected
component of D_i symmetric-difference D_j, and swaps i,j on that component.
This checker exhausts the entire reachable component and independently
checks that all 20,160 states retain a K6 co-occurrence graph.  Since the
distance-two graph R5 has clique number five, no state maps to R5.

Only the Python standard library is required.
"""

from __future__ import annotations

from collections import Counter, deque
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "search"
    / "k6-petersen-star-barrier-20260725"
    / "witness.json"
)
EXPECTED_SOURCE_SHA256 = (
    "b9be3936c93e6a589dfadf53c8a9e9229fe4ecefda8e03eaa564fc147e6408b3"
)
COORDINATES = tuple(range(8))
PAIRS = tuple(combinations(COORDINATES, 2))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def endpoints(mask: int) -> tuple[int, int]:
    require(mask.bit_count() == 2, f"non-duad mask {mask}")
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    second = (mask ^ first_bit).bit_length() - 1
    return first, second


def load() -> tuple[
    tuple[tuple[int, int], ...],
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
]:
    actual_hash = sha256(SOURCE.read_bytes()).hexdigest()
    require(
        actual_hash == EXPECTED_SOURCE_SHA256,
        f"frozen source hash changed: {actual_hash}",
    )
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    graph = data["graph"]
    require(graph["name"] == "Petersen", "wrong frozen graph")
    require(graph["vertex_count"] == 10, "wrong Petersen order")
    edges = tuple(tuple(map(int, edge)) for edge in graph["edge_order"])
    require(len(edges) == 15, "wrong Petersen size")

    duad_map = {
        int(value): tuple(map(int, pair))
        for value, pair in data["abstract_value_to_k6_duad"].items()
    }
    flow = tuple(map(int, data["flow"]))
    require(len(flow) == len(edges), "flow has wrong size")
    labels = tuple(
        sum(1 << coordinate for coordinate in duad_map[value])
        for value in flow
    )

    incidence: list[list[int]] = [[] for _ in range(10)]
    for edge, (left, right) in enumerate(edges):
        require(0 <= left < right < 10, f"bad edge {edge}")
        incidence[left].append(edge)
        incidence[right].append(edge)
    return edges, labels, tuple(tuple(row) for row in incidence)


def graph_components(
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    deleted: frozenset[int],
) -> tuple[frozenset[int], ...]:
    unseen = set(range(10))
    output = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        seen = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for edge in incidence[vertex]:
                if edge in deleted:
                    continue
                left, right = edges[edge]
                other = right if left == vertex else left
                if other in unseen:
                    unseen.remove(other)
                    seen.add(other)
                    stack.append(other)
        output.append(frozenset(seen))
    return tuple(output)


def internal_edge_count(
    vertices: frozenset[int],
    edges: tuple[tuple[int, int], ...],
) -> int:
    return sum(left in vertices and right in vertices for left, right in edges)


def graph_audit(
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    require(len(set(edges)) == len(edges), "parallel edge")
    require(all(len(row) == 3 for row in incidence), "not cubic")
    require(
        len(graph_components(edges, incidence, frozenset())) == 1,
        "not connected",
    )
    for edge in range(15):
        require(
            len(graph_components(edges, incidence, frozenset((edge,)))) == 1,
            f"bridge {edge}",
        )

    # Direct girth calculation by enumerating vertex subsets that support a
    # connected 2-regular induced edge set.
    shortest = 11
    for size in range(3, 11):
        for vertices_raw in combinations(range(10), size):
            vertices = frozenset(vertices_raw)
            internal = [
                edge
                for edge, (left, right) in enumerate(edges)
                if left in vertices and right in vertices
            ]
            degree = Counter(
                endpoint
                for edge in internal
                for endpoint in edges[edge]
            )
            if len(internal) == size and set(degree.values()) == {2}:
                shortest = size
                break
        if shortest < 11:
            break
    require(shortest == 5, f"unexpected girth {shortest}")

    cut_profile: dict[str, int] = {}
    cyclic_profile: dict[str, int] = {}
    for size in range(1, 6):
        cuts = 0
        cyclic_cuts = 0
        for deleted_raw in combinations(range(15), size):
            components = graph_components(
                edges, incidence, frozenset(deleted_raw)
            )
            if len(components) == 1:
                continue
            cuts += 1
            cyclic_shores = sum(
                internal_edge_count(component, edges) >= len(component)
                for component in components
            )
            cyclic_cuts += cyclic_shores >= 2
        cut_profile[str(size)] = cuts
        cyclic_profile[str(size)] = cyclic_cuts
    require(
        cyclic_profile == {"1": 0, "2": 0, "3": 0, "4": 0, "5": 6},
        f"wrong cyclic-cut profile {cyclic_profile}",
    )

    # A cubic graph is Tait-colourable iff some perfect matching has an
    # even-cycle complement.  Enumerate the complete matching list.
    matchings = []
    complement_cycle_lengths = []
    for chosen in combinations(range(15), 5):
        degree = [0] * 10
        for edge in chosen:
            for vertex in edges[edge]:
                degree[vertex] += 1
        if degree != [1] * 10:
            continue
        matchings.append(chosen)
        remaining = frozenset(set(range(15)) - set(chosen))
        unseen = set(remaining)
        lengths = []
        while unseen:
            first = unseen.pop()
            component = {first}
            stack = [first]
            while stack:
                edge = stack.pop()
                for vertex in edges[edge]:
                    for other in incidence[vertex]:
                        if other in unseen and other in remaining:
                            unseen.remove(other)
                            component.add(other)
                            stack.append(other)
            lengths.append(len(component))
        complement_cycle_lengths.append(tuple(sorted(lengths)))
    require(len(matchings) == 6, "wrong number of perfect matchings")
    require(
        set(complement_cycle_lengths) == {(5, 5)},
        "Petersen unexpectedly has an even 2-factor",
    )

    return {
        "vertices": 10,
        "edges": 15,
        "simple": True,
        "cubic": True,
        "connected": True,
        "bridgeless": True,
        "girth": shortest,
        "cyclic_edge_connectivity": 5,
        "disconnected_deletion_sets_through_five": cut_profile,
        "cyclic_cuts_through_five": cyclic_profile,
        "perfect_matchings": [list(row) for row in matchings],
        "perfect_matching_complement_cycle_lengths": [
            list(row) for row in complement_cycle_lengths
        ],
        "tait_colourable": False,
    }


def validate_cover(
    labels: tuple[int, ...],
    incidence: tuple[tuple[int, ...], ...],
) -> None:
    require(len(labels) == 15, "wrong cover size")
    require(all(mask.bit_count() == 2 for mask in labels), "non-pair label")
    for vertex, incident in enumerate(incidence):
        for coordinate in COORDINATES:
            require(
                sum((labels[edge] >> coordinate) & 1 for edge in incident)
                % 2
                == 0,
                f"parity failure at vertex {vertex}, coordinate {coordinate}",
            )


def symmetric_difference_components(
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    labels: tuple[int, ...],
    first: int,
    second: int,
) -> tuple[frozenset[int], ...]:
    toggle = (1 << first) | (1 << second)
    unseen = {
        edge
        for edge, label in enumerate(labels)
        if (label & toggle).bit_count() == 1
    }
    output = []
    while unseen:
        seed = min(unseen)
        unseen.remove(seed)
        component = {seed}
        stack = [seed]
        while stack:
            edge = stack.pop()
            for vertex in edges[edge]:
                for other in incidence[vertex]:
                    if other in unseen:
                        label = labels[other]
                        if (label & toggle).bit_count() == 1:
                            unseen.remove(other)
                            component.add(other)
                            stack.append(other)
        output.append(frozenset(component))
    return tuple(output)


def apply_move(
    labels: tuple[int, ...],
    first: int,
    second: int,
    component: frozenset[int],
) -> tuple[int, ...]:
    toggle = (1 << first) | (1 << second)
    output = list(labels)
    for edge in component:
        require(
            (output[edge] & toggle).bit_count() == 1,
            "move contains an edge outside the symmetric difference",
        )
        output[edge] ^= toggle
    return tuple(output)


def active_coordinates(labels: tuple[int, ...]) -> frozenset[int]:
    mask = 0
    for label in labels:
        mask |= label
    return frozenset(
        coordinate for coordinate in COORDINATES if (mask >> coordinate) & 1
    )


def is_complete_duad_set(labels: tuple[int, ...]) -> bool:
    active = active_coordinates(labels)
    return (
        len(active) == 6
        and len(set(labels)) == 15
        and set(labels)
        == {
            (1 << first) | (1 << second)
            for first, second in combinations(active, 2)
        }
    )


def r5_clique_number() -> int:
    adjacency = [0] * 32
    for first in range(32):
        for second in range(first + 1, 32):
            if (first ^ second).bit_count() == 2:
                adjacency[first] |= 1 << second
                adjacency[second] |= 1 << first

    best = 0

    def expand(size: int, candidates: int) -> None:
        nonlocal best
        if size + candidates.bit_count() <= best:
            return
        if not candidates:
            best = max(best, size)
            return
        while candidates:
            if size + candidates.bit_count() <= best:
                return
            bit = candidates & -candidates
            vertex = bit.bit_length() - 1
            candidates ^= bit
            expand(size + 1, candidates & adjacency[vertex])
        best = max(best, size)

    expand(0, (1 << 32) - 1)
    return best


def component_audit(
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    initial: tuple[int, ...],
) -> dict[str, object]:
    validate_cover(initial, incidence)
    require(is_complete_duad_set(initial), "initial H is not K6")

    # Record the representative symmetric-difference lengths.  Six active
    # coordinates give 15 eight-cycles; active-empty gives 12 five-cycles;
    # the empty-empty pair has empty support.
    initial_profile = Counter()
    for first, second in PAIRS:
        components = symmetric_difference_components(
            edges, incidence, initial, first, second
        )
        initial_profile[
            tuple(sorted(len(component) for component in components))
        ] += 1
    require(
        initial_profile == Counter({(8,): 15, (5,): 12, (): 1}),
        f"wrong initial component profile {initial_profile}",
    )

    seen = {initial: 0}
    queue = deque((initial,))
    layers = Counter({0: 1})
    degree_profile = Counter()
    while queue:
        state = queue.popleft()
        distance = seen[state]
        require(is_complete_duad_set(state), "reachable state lost its K6")
        validate_cover(state, incidence)
        distinct_neighbors = set()
        for first, second in PAIRS:
            components = symmetric_difference_components(
                edges, incidence, state, first, second
            )
            require(
                len(components) <= 1,
                "a reachable symmetric difference split into components",
            )
            for component in components:
                neighbor = apply_move(state, first, second, component)
                distinct_neighbors.add(neighbor)
                if neighbor not in seen:
                    seen[neighbor] = distance + 1
                    layers[distance + 1] += 1
                    queue.append(neighbor)
        degree_profile[len(distinct_neighbors)] += 1

    require(len(seen) == 20160, f"wrong component size {len(seen)}")
    require(
        degree_profile == Counter({27: 20160}),
        f"wrong degree profile {degree_profile}",
    )
    require(
        len(seen) == 40320 // 2,
        "component is not the expected S8/S2 orbit",
    )

    clique = r5_clique_number()
    require(clique == 5, f"wrong R5 clique number {clique}")
    return {
        "initial_symmetric_difference_profile": {
            "active_active_single_8_cycle": 15,
            "active_empty_single_5_cycle": 12,
            "empty_empty": 1,
        },
        "reachable_states": len(seen),
        "expected_orbit_size": "8!/2! = 20160",
        "distance_layers": [
            layers[distance] for distance in range(max(layers) + 1)
        ],
        "maximum_distance": max(layers),
        "reachable_state_degree_profile": {
            str(degree): count
            for degree, count in sorted(degree_profile.items())
        },
        "cooccurrence_graph_in_every_state": "K6 plus two isolated vertices",
        "r5_clique_number": clique,
        "r5_compressible_states": 0,
    }


def main() -> int:
    edges, labels, incidence = load()
    graph = graph_audit(edges, incidence)
    component = component_audit(edges, incidence, labels)
    report = {
        "schema": "petersen-cover-kempe-component-audit-v1",
        "status": "PASS",
        "classification": (
            "EXACT NON-TAIT CYCLICALLY-5 SUPPLIED-8-CDC "
            "KEMPE/R5 COUNTERMODEL"
        ),
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "graph": graph,
        "cover": {
            "coordinates": 8,
            "nonempty_coordinates": 6,
            "empty_coordinates": [6, 7],
            "edge_labels": [list(endpoints(mask)) for mask in labels],
            "every_edge_covered_exactly_twice": True,
            "every_coordinate_support_eulerian": True,
        },
        "kempe_component": component,
        "scope_warning": (
            "This disproves a universal supplied-cover Kempe-to-R5 route. "
            "It is not a counterexample to FiveCDC: the displayed cover "
            "itself already has only six nonempty coordinates, and Petersen "
            "has explicit five-cycle double covers."
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
