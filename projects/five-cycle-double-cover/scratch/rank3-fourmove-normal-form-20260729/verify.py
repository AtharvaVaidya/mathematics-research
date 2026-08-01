#!/usr/bin/env python3
"""Independent verifier for the rank-three four-move normal form.

Only the Python standard library is used.  The Petersen--Foster graph and
the two endpoint flows are reconstructed directly from the frozen source
certificate; no code is imported from the source package.
"""

from __future__ import annotations

from collections.abc import Iterable
from collections import Counter
from itertools import product
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "petersen-foster-girth10-nontait-20260729"
CERTIFICATE = SOURCE / "reconfiguration-certificate.json"
LABELS = SOURCE / "fivecdc-labels.txt"

FOSTER_LCF = (17, -9, 37, -37, 9, -17) * 15
PETERSEN_EDGES = (
    (0, 1), (1, 2), (2, 3), (0, 4), (3, 4),
    (0, 5), (1, 6), (2, 7), (5, 7), (3, 8),
    (5, 8), (6, 8), (4, 9), (6, 9), (7, 9),
)
FOSTER_PORTS = (1, 17, 89)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def foster_edges() -> set[tuple[int, int]]:
    answer: set[tuple[int, int]] = set()
    for u in range(90):
        for v in ((u + 1) % 90, (u + FOSTER_LCF[u]) % 90):
            answer.add(tuple(sorted((u, v))))
    assert len(answer) == 135
    return answer


def petersen_foster_edges() -> tuple[tuple[int, int], ...]:
    answer: set[tuple[int, int]] = set()
    for copy in range(10):
        for u, v in foster_edges():
            if 0 in (u, v):
                continue
            answer.add(tuple(sorted((
                89 * copy + u - 1,
                89 * copy + v - 1,
            ))))

    used = [0] * 10
    for u, v in PETERSEN_EDGES:
        pu = FOSTER_PORTS[used[u]]
        pv = FOSTER_PORTS[used[v]]
        used[u] += 1
        used[v] += 1
        answer.add(tuple(sorted((
            89 * u + pu - 1,
            89 * v + pv - 1,
        ))))
    assert used == [3] * 10
    assert len(answer) == 1335

    # This is the edge order used by graph6: increasing right endpoint, then
    # increasing left endpoint.
    return tuple(
        (u, v)
        for v in range(1, 890)
        for u in range(v)
        if (u, v) in answer
    )


def incidence(
    order: int, edges: tuple[tuple[int, int], ...]
) -> list[list[int]]:
    rows = [[] for _ in range(order)]
    for edge, (u, v) in enumerate(edges):
        rows[u].append(edge)
        rows[v].append(edge)
    return rows


def binary_rank(values: tuple[int, ...] | list[int] | set[int]) -> int:
    basis = [0, 0, 0]
    rank = 0
    for value in values:
        for bit in range(2, -1, -1):
            if not ((value >> bit) & 1):
                continue
            if basis[bit]:
                value ^= basis[bit]
            else:
                basis[bit] = value
                rank += 1
                break
    return rank


def linear_image(constants: tuple[int, ...], mask: int) -> int:
    answer = 0
    for position, constant in enumerate(constants):
        if (mask >> position) & 1:
            answer ^= constant
    return answer


def legal_prefixes(start: int, constants: tuple[int, ...], mask: int) -> bool:
    current = start
    for position, constant in enumerate(constants):
        if (mask >> position) & 1:
            current ^= constant
        if current == 0:
            return False
    return True


def flow_is_nowhere_zero(
    flow: tuple[int, ...],
    rows: list[list[int]],
) -> bool:
    return (
        all(1 <= value <= 7 for value in flow)
        and all(
            not_value == 0
            for row in rows
            for not_value in [xor_values(flow[edge] for edge in row)]
        )
    )


def xor_values(values: Iterable[int]) -> int:
    answer = 0
    for value in values:
        answer ^= value
    return answer


def allowed_toggles(
    start: tuple[int, ...],
    constants: tuple[int, ...],
    base: list[int],
    dependency: int,
) -> list[int]:
    """Return two-bit sets: bit y permits the kernel toggle y."""
    answer = []
    for value, mask in zip(start, base):
        choices = 0
        for toggle in (0, 1):
            candidate = mask ^ (dependency if toggle else 0)
            if legal_prefixes(value, constants, candidate):
                choices |= 1 << toggle
        answer.append(choices)
    return answer


def component_feasible(
    order: int,
    edges: tuple[tuple[int, int], ...],
    demand: list[int],
    allowed: list[int],
) -> bool:
    """Solve B_free y = demand + B(forced-one) by components."""
    if any(choices == 0 for choices in allowed):
        return False

    residual = demand[:]
    parent = list(range(order))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def union(first: int, second: int) -> None:
        first = find(first)
        second = find(second)
        if first != second:
            parent[second] = first

    for edge, choices in enumerate(allowed):
        u, v = edges[edge]
        if choices == 2:
            # A loop toggles the same entry twice and hence contributes zero.
            residual[u] ^= 1
            residual[v] ^= 1
        elif choices == 3:
            union(u, v)

    component_parity: dict[int, int] = {}
    for vertex, value in enumerate(residual):
        root = find(vertex)
        component_parity[root] = component_parity.get(root, 0) ^ value
    return not any(component_parity.values())


def brute_feasible(
    order: int,
    edges: tuple[tuple[int, int], ...],
    demand: list[int],
    allowed: list[int],
) -> bool:
    """Tiny-instance oracle, independent of the component test."""
    for assignment in product((0, 1), repeat=len(edges)):
        if any(not (allowed[edge] & (1 << value))
               for edge, value in enumerate(assignment)):
            continue
        boundary = [0] * order
        for edge, value in enumerate(assignment):
            if value:
                u, v = edges[edge]
                boundary[u] ^= 1
                boundary[v] ^= 1
        if boundary == demand:
            return True
    return False


def self_test_component_criterion() -> int:
    """Exhaustively test loops, parallel edges, and isolated vertices."""
    edges = ((0, 0), (0, 1), (0, 1), (1, 2), (2, 3))
    instances = 0
    for demand_mask in range(16):
        demand = [(demand_mask >> vertex) & 1 for vertex in range(4)]
        for allowed in product((0, 1, 2, 3), repeat=len(edges)):
            allowed_list = list(allowed)
            assert component_feasible(
                4, edges, demand, allowed_list
            ) == brute_feasible(4, edges, demand, allowed_list)
            instances += 1
    return instances


def vertex_demands(
    rows: list[list[int]],
    base: list[int],
    dependency: int,
) -> list[int]:
    answer = []
    for row in rows:
        parity_vector = xor_values(base[edge] for edge in row)
        assert parity_vector in (0, dependency)
        answer.append(int(parity_vector == dependency))
    return answer


def check_all_four_tuples(
    edges: tuple[tuple[int, int], ...],
    rows: list[list[int]],
    start: tuple[int, ...],
    difference: tuple[int, ...],
    scramble: list[int],
) -> dict[str, object]:
    classification: Counter[str] = Counter()
    dependency_weights: Counter[int] = Counter()
    demand_weights: Counter[int] = Counter()

    for constants in product(range(1, 8), repeat=4):
        if binary_rank(constants) != 3:
            continue

        dependencies = [
            mask for mask in range(1, 16)
            if linear_image(constants, mask) == 0
        ]
        assert len(dependencies) == 1
        dependency = dependencies[0]
        dependency_weights[dependency.bit_count()] += 1

        canonical = {
            value: min(
                mask for mask in range(16)
                if linear_image(constants, mask) == value
            )
            for value in range(8)
        }
        base = [
            canonical[value] ^ (dependency if scramble[edge] else 0)
            for edge, value in enumerate(difference)
        ]
        assert all(
            linear_image(constants, base[edge]) == difference[edge]
            for edge in range(len(edges))
        )

        demand = vertex_demands(rows, base, dependency)
        demand_weights[sum(demand)] += 1
        allowed = allowed_toggles(start, constants, base, dependency)
        if 0 in allowed:
            classification["local_blocker"] += 1
        elif component_feasible(890, edges, demand, allowed):
            classification["legal"] += 1
        else:
            classification["component_parity_blocker"] += 1

    return {
        "classification": dict(sorted(classification.items())),
        "dependency_weight_histogram": {
            str(key): value
            for key, value in sorted(dependency_weights.items())
        },
        "vertex_demand_weight_histogram": {
            str(key): value
            for key, value in sorted(demand_weights.items())
        },
    }


def check_three_tuples(
    start: tuple[int, ...],
    difference: tuple[int, ...],
) -> dict[str, int]:
    spanning = 0
    legal = 0
    for constants in product(range(1, 8), repeat=3):
        if binary_rank(constants) != 3:
            continue
        spanning += 1
        inverse = {
            value: next(
                mask for mask in range(8)
                if linear_image(constants, mask) == value
            )
            for value in range(8)
        }
        if all(
            legal_prefixes(value, constants, inverse[delta])
            for value, delta in zip(start, difference)
        ):
            legal += 1
    return {"spanning_ordered_triples": spanning, "legal": legal}


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text())
    assert payload["schema"] == "petersen-foster-flow-reconfiguration-v1"
    edges = petersen_foster_edges()
    rows = incidence(890, edges)
    assert all(len(row) == 3 for row in rows)

    start = tuple(int(value) for value in payload["bad_flow_digits"])
    masks = tuple(int(value) for value in LABELS.read_text().split())
    points = tuple(payload["good_point_assignment"])
    assert len(start) == len(masks) == len(edges)
    assert len(points) == len(set(points)) == 5

    target_values = []
    for mask in masks:
        pair = [index for index in range(5) if (mask >> index) & 1]
        assert len(pair) == 2
        target_values.append(points[pair[0]] ^ points[pair[1]])
    target = tuple(target_values)
    assert flow_is_nowhere_zero(start, rows)
    assert flow_is_nowhere_zero(target, rows)

    difference = tuple(
        first ^ second for first, second in zip(start, target)
    )
    assert binary_rank(set(difference)) == 3

    canonical = check_all_four_tuples(
        edges, rows, start, difference, [0] * len(edges)
    )
    scrambled_bits = [
        int((edge * edge + 3 * edge + 1) % 7 < 3)
        for edge in range(len(edges))
    ]
    scrambled = check_all_four_tuples(
        edges, rows, start, difference, scrambled_bits
    )

    expected = {
        "component_parity_blocker": 672,
        "local_blocker": 1176,
    }
    assert canonical["classification"] == expected
    assert scrambled["classification"] == expected
    assert canonical["dependency_weight_histogram"] == {
        "2": 1008, "3": 672, "4": 168
    }
    assert canonical["vertex_demand_weight_histogram"] == {"0": 1848}
    assert scrambled["vertex_demand_weight_histogram"] == {"554": 1848}

    triples = check_three_tuples(start, difference)
    assert triples == {"spanning_ordered_triples": 168, "legal": 0}

    result = {
        "classification": "EXACT_RANK3_FOUR_MOVE_NORMAL_FORM_AUDIT",
        "scope": (
            "fixed-vector switches on arbitrary Eulerian supports; "
            "every intermediate flow required nowhere-zero"
        ),
        "source_certificate_sha256": sha256(CERTIFICATE),
        "source_labels_sha256": sha256(LABELS),
        "order": 890,
        "size": len(edges),
        "difference_rank": 3,
        "tiny_component_criterion_instances": self_test_component_criterion(),
        "ordered_rank_three_triples": triples,
        "canonical_lift_audit": canonical,
        "scrambled_lift_audit": scrambled,
        "scrambled_lift_odd_demand_vertices": sum(
            vertex_demands(
                rows,
                [
                    0 ^ (1 if bit else 0)
                    for bit in scrambled_bits
                ],
                1,
            )
        ),
        "conclusion": (
            "all 1848 ordered spanning four-tuples are blocked: "
            "1176 locally and 672 by free-component parity"
        ),
    }
    # The displayed scrambled demand count above is simply B(scramble); it is
    # independent of the constants and equals the per-tuple demand weight.
    assert result["scrambled_lift_odd_demand_vertices"] == 554
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
