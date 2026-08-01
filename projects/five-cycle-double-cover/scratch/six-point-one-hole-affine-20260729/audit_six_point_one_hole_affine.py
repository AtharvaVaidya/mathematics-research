#!/usr/bin/env python3
"""Exact audit of the six-point/one-hole affine FiveCDC lift.

This program uses only the Python standard library.  It independently
enumerates the local Fano-plane lists, builds the global affine system,
and checks the retained 34-vertex strictness witness.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
W = tuple(range(8))
REFERENCE = (
    ROOT
    / "output"
    / "jaeger-star-thinning-countermodel-34v"
    / "star-good-six-witness.json"
)


def bit_dot(left: int, right: int) -> int:
    return (left & right).bit_count() & 1


def span2(first: int, second: int) -> frozenset[int]:
    return frozenset((0, first, second, first ^ second))


PLANES = tuple(
    sorted(
        {
            span2(first, second)
            for first in range(1, 8)
            for second in range(first + 1, 8)
            if first != second
        },
        key=lambda plane: tuple(sorted(plane)),
    )
)
assert len(PLANES) == 7


def local_triangle(plane: frozenset[int], potential: int) -> tuple[int, ...]:
    """Return (potential + plane) minus potential."""

    return tuple(sorted(potential ^ value for value in plane if value))


def allowed_potentials(
    support: frozenset[int],
    missing_pair: frozenset[int] | None,
    plane: frozenset[int],
) -> frozenset[int]:
    admitted = []
    for potential in W:
        triangle = frozenset(local_triangle(plane, potential))
        if not triangle <= support:
            continue
        if missing_pair is not None and missing_pair <= triangle:
            continue
        admitted.append(potential)
    return frozenset(admitted)


def is_affine_set(points: frozenset[int]) -> bool:
    if not points:
        return False
    base = min(points)
    translated = {point ^ base for point in points}
    return all(left ^ right in translated for left in translated for right in translated)


def predicted_local_set(
    omitted_pair: tuple[int, int],
    missing_pair: tuple[int, int],
    plane: frozenset[int],
) -> frozenset[int]:
    """Closed local formula, normalized by the first omitted point."""

    root, other = omitted_pair
    first, second = (first ^ root for first in missing_pair)
    direction_omitted = root ^ other
    direction_missing = first ^ second
    normalized = None

    if direction_missing == direction_omitted:
        distinguished = span2(direction_omitted, first)
        if direction_omitted in plane:
            if plane == distinguished:
                normalized = frozenset(set(W) - set(plane))
            else:
                normalized = frozenset((first, second))
        else:
            normalized = frozenset((0, direction_omitted))
    else:
        has_omitted_direction = direction_omitted in plane
        has_missing_direction = direction_missing in plane
        if has_omitted_direction and has_missing_direction:
            normalized = frozenset((first, second))
        elif has_omitted_direction:
            normalized = frozenset(set(W) - set(plane))
        elif has_missing_direction:
            normalized = frozenset(
                point
                for point in (0, direction_omitted)
                if (first ^ point) not in plane
            )
        else:
            normalized = frozenset((0, direction_omitted))

    return frozenset(point ^ root for point in normalized)


def affine_equations(points: frozenset[int]) -> list[tuple[int, int]]:
    """Return redundant exact scalar equations h.t = rhs for an affine set."""

    assert is_affine_set(points)
    base = min(points)
    equations = []
    for functional in range(1, 8):
        if all(bit_dot(functional, point ^ base) == 0 for point in points):
            equations.append((functional, bit_dot(functional, base)))
    return equations


def gf2_rref(variable_count: int, rows: list[tuple[int, int]]) -> dict:
    work = [[mask, rhs] for mask, rhs in rows]
    pivot_columns: list[int] = []
    rank = 0
    for column in range(variable_count):
        bit = 1 << column
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][0] & bit),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for index in range(len(work)):
            if index != rank and work[index][0] & bit:
                work[index][0] ^= work[rank][0]
                work[index][1] ^= work[rank][1]
        pivot_columns.append(column)
        rank += 1
    if any(mask == 0 and rhs for mask, rhs in work):
        return {"sat": False, "rank": rank, "dimension": None, "solution": None}
    solution = 0
    for row, column in enumerate(pivot_columns):
        if work[row][1]:
            solution |= 1 << column
    assert all(((mask & solution).bit_count() & 1) == rhs for mask, rhs in rows)
    return {
        "sat": True,
        "rank": rank,
        "dimension": variable_count - rank,
        "solution": solution,
    }


def gf2_dual_certificate(
    variable_count: int, rows: list[tuple[int, int]]
) -> list[int] | None:
    """Return row indices whose xor is 0=1, or None when none is found."""

    work = [
        [mask, rhs, 1 << index] for index, (mask, rhs) in enumerate(rows)
    ]
    rank = 0
    for column in range(variable_count):
        bit = 1 << column
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][0] & bit),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for index in range(len(work)):
            if index != rank and work[index][0] & bit:
                work[index][0] ^= work[rank][0]
                work[index][1] ^= work[rank][1]
                work[index][2] ^= work[rank][2]
        rank += 1
    contradiction = next(
        (
            source_mask
            for mask, rhs, source_mask in work
            if mask == 0 and rhs == 1
        ),
        None,
    )
    if contradiction is None:
        return None
    selected = [
        index
        for index in range(len(rows))
        if contradiction & (1 << index)
    ]
    xor_mask = 0
    xor_rhs = 0
    for index in selected:
        xor_mask ^= rows[index][0]
        xor_rhs ^= rows[index][1]
    assert xor_mask == 0 and xor_rhs == 1
    return selected


def graph_incidence(vertex_count: int, edges: list[list[int]]) -> list[list[int]]:
    incidence = [[] for _ in range(vertex_count)]
    for edge_index, (left, right) in enumerate(edges):
        incidence[left].append(edge_index)
        incidence[right].append(edge_index)
    return incidence


def check_connected(
    vertex_count: int, edges: list[list[int]], omitted_edge: int | None = None
) -> bool:
    adjacency = [[] for _ in range(vertex_count)]
    for edge_index, (left, right) in enumerate(edges):
        if edge_index == omitted_edge:
            continue
        adjacency[left].append(right)
        adjacency[right].append(left)
    reached = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbour in adjacency[vertex]:
            if neighbour not in reached:
                reached.add(neighbour)
                stack.append(neighbour)
    return len(reached) == vertex_count


def local_planes(
    incidence: list[list[int]], flow: list[int]
) -> list[frozenset[int]]:
    planes = []
    for incident in incidence:
        values = [flow[edge] for edge in incident]
        assert len(values) == 3
        assert 0 not in values and len(set(values)) == 3
        assert values[0] ^ values[1] ^ values[2] == 0
        plane = frozenset((0, *values))
        assert plane in PLANES
        planes.append(plane)
    return planes


def build_global_rows(
    edges: list[list[int]],
    incidence: list[list[int]],
    flow: list[int],
    planes: list[frozenset[int]],
    support: frozenset[int],
    missing_pair: frozenset[int] | None,
) -> tuple[list[tuple[int, int]], list[dict]] | None:
    vertex_count = len(incidence)
    rows: list[tuple[int, int]] = []
    descriptions: list[dict] = []

    for vertex, plane in enumerate(planes):
        admitted = allowed_potentials(support, missing_pair, plane)
        if not admitted:
            return None
        assert is_affine_set(admitted)
        for functional, rhs in affine_equations(admitted):
            mask = 0
            for coordinate in range(3):
                if functional & (1 << coordinate):
                    mask |= 1 << (3 * vertex + coordinate)
            rows.append((mask, rhs))
            descriptions.append(
                {
                    "kind": "local",
                    "vertex": vertex,
                    "functional": functional,
                    "rhs": rhs,
                    "allowed_potentials": sorted(admitted),
                }
            )

    for edge_index, (left, right) in enumerate(edges):
        value = flow[edge_index]
        other_left = next(
            flow[edge] for edge in incidence[left] if edge != edge_index
        )
        other_right = next(
            flow[edge] for edge in incidence[right] if edge != edge_index
        )
        constant = other_left ^ other_right
        for functional in range(1, 8):
            if bit_dot(functional, value):
                continue
            mask = 0
            for coordinate in range(3):
                if functional & (1 << coordinate):
                    mask ^= 1 << (3 * left + coordinate)
                    mask ^= 1 << (3 * right + coordinate)
            rows.append((mask, bit_dot(functional, constant)))
            descriptions.append(
                {
                    "kind": "edge",
                    "edge": edge_index,
                    "ends": [left, right],
                    "flow_value": value,
                    "functional": functional,
                    "rhs": bit_dot(functional, constant),
                    "other_value_xor": constant,
                }
            )

    assert len(rows) == len(descriptions)
    return rows, descriptions


def build_global_system(
    edges: list[list[int]],
    incidence: list[list[int]],
    flow: list[int],
    planes: list[frozenset[int]],
    support: frozenset[int],
    missing_pair: frozenset[int] | None,
) -> dict:
    vertex_count = len(incidence)
    built = build_global_rows(
        edges, incidence, flow, planes, support, missing_pair
    )
    if built is None:
        return {"sat": False, "rank": 0, "dimension": None, "solution": None}
    rows, _ = built

    return gf2_rref(3 * vertex_count, rows)


def decode_potentials(solution: int, vertex_count: int) -> list[int]:
    return [
        sum(
            ((solution >> (3 * vertex + coordinate)) & 1) << coordinate
            for coordinate in range(3)
        )
        for vertex in range(vertex_count)
    ]


def labels_from_potentials(
    edges: list[list[int]],
    incidence: list[list[int]],
    flow: list[int],
    potentials: list[int],
) -> list[tuple[int, int]]:
    labels: list[tuple[int, int]] = []
    for edge_index, (left, right) in enumerate(edges):
        value = flow[edge_index]
        other_left = next(
            flow[edge] for edge in incidence[left] if edge != edge_index
        )
        other_right = next(
            flow[edge] for edge in incidence[right] if edge != edge_index
        )
        pair_left = tuple(
            sorted(
                (
                    potentials[left] ^ other_left,
                    potentials[left] ^ other_left ^ value,
                )
            )
        )
        pair_right = tuple(
            sorted(
                (
                    potentials[right] ^ other_right,
                    potentials[right] ^ other_right ^ value,
                )
            )
        )
        assert pair_left == pair_right
        labels.append(pair_left)
    return labels


def local_audit() -> dict:
    pairs = list(itertools.combinations(W, 2))
    count_histogram = {"parallel": {}, "skew": {}}
    configurations = {"parallel": 0, "skew": 0}
    triangle_total = 0

    for omitted_pair in pairs:
        support = frozenset(set(W) - set(omitted_pair))
        for missing_pair in pairs:
            if set(omitted_pair) & set(missing_pair):
                continue
            kind = (
                "parallel"
                if omitted_pair[0] ^ omitted_pair[1]
                == missing_pair[0] ^ missing_pair[1]
                else "skew"
            )
            configurations[kind] += 1
            row_counts = []
            for plane in PLANES:
                literal = allowed_potentials(
                    support, frozenset(missing_pair), plane
                )
                predicted = predicted_local_set(omitted_pair, missing_pair, plane)
                assert literal == predicted
                assert is_affine_set(literal)
                row_counts.append(len(literal))
                triangle_total += len(literal)
                key = str(len(literal))
                count_histogram[kind][key] = (
                    count_histogram[kind].get(key, 0) + 1
                )
            expected = (
                [2, 2, 2, 2, 2, 2, 4]
                if kind == "parallel"
                else [1, 1, 2, 2, 2, 4, 4]
            )
            assert sorted(row_counts) == expected

    assert configurations == {"parallel": 84, "skew": 336}
    assert count_histogram == {
        "parallel": {"2": 504, "4": 84},
        "skew": {"1": 672, "2": 1008, "4": 672},
    }
    assert triangle_total == 420 * 16 == 6720
    return {
        "pair_pair_configurations": configurations,
        "local_case_histogram": count_histogram,
        "admitted_local_triangles": triangle_total,
    }


def witness_audit() -> dict:
    raw = REFERENCE.read_bytes()
    witness = json.loads(raw)
    vertex_count = int(witness["vertices"])
    edges = witness["edges"]
    flow = list(map(int, witness["flow"]))
    labels = [tuple(map(int, pair)) for pair in witness["point_labels"]]

    assert vertex_count == 34 and len(edges) == 51
    assert all(left != right for left, right in edges)
    assert len({tuple(edge) for edge in edges}) == len(edges)
    incidence = graph_incidence(vertex_count, edges)
    assert all(len(row) == 3 for row in incidence)
    assert check_connected(vertex_count, edges)
    assert all(
        check_connected(vertex_count, edges, omitted_edge=edge)
        for edge in range(len(edges))
    )
    assert len(flow) == len(edges)
    assert all(
        not (flow[incident[0]] ^ flow[incident[1]] ^ flow[incident[2]])
        for incident in incidence
    )
    planes = local_planes(incidence, flow)

    assert len(labels) == len(edges)
    assert all(
        first != second and first ^ second == flow[edge]
        for edge, (first, second) in enumerate(labels)
    )
    for vertex, incident in enumerate(incidence):
        for point in W:
            assert sum(point in labels[edge] for edge in incident) % 2 == 0
        triangle_points = set().union(*(set(labels[edge]) for edge in incident))
        assert len(triangle_points) == 3
        potential = 0
        for point in triangle_points:
            potential ^= point
        assert frozenset(triangle_points) == frozenset(
            local_triangle(planes[vertex], potential)
        )

    omitted_pair = (1, 2)
    missing_pair = (4, 5)
    support = frozenset(set(W) - set(omitted_pair))
    assert set().union(*map(set, labels)) == set(support)
    used_pair_types = {frozenset(pair) for pair in labels}
    expected_pair_types = {
        frozenset(pair)
        for pair in itertools.combinations(sorted(support), 2)
        if pair != missing_pair
    }
    assert used_pair_types == expected_pair_types

    strict_system = build_global_system(
        edges,
        incidence,
        flow,
        planes,
        support,
        frozenset(missing_pair),
    )
    assert strict_system["sat"]
    assert strict_system["rank"] == 101
    assert strict_system["dimension"] == 1
    potentials = decode_potentials(strict_system["solution"], vertex_count)
    rebuilt_labels = labels_from_potentials(
        edges, incidence, flow, potentials
    )
    assert set().union(*map(set, rebuilt_labels)) <= set(support)
    assert frozenset(missing_pair) not in map(frozenset, rebuilt_labels)

    five_set_passes = []
    for support_five in itertools.combinations(W, 5):
        result = build_global_system(
            edges,
            incidence,
            flow,
            planes,
            frozenset(support_five),
            None,
        )
        if result["sat"]:
            five_set_passes.append(
                {"support": list(support_five), "dimension": result["dimension"]}
            )
    assert five_set_passes == []

    certificate_support = frozenset((0, 1, 2, 3, 4))
    built_certificate = build_global_rows(
        edges,
        incidence,
        flow,
        planes,
        certificate_support,
        None,
    )
    assert built_certificate is not None
    certificate_rows, certificate_descriptions = built_certificate
    certificate_indices = gf2_dual_certificate(
        3 * vertex_count, certificate_rows
    )
    assert certificate_indices is not None
    five_certificate = {
        "five_point_support": sorted(certificate_support),
        "row_count": len(certificate_rows),
        "selected_row_indices": certificate_indices,
        "selected_row_count": len(certificate_indices),
        "selected_rows": [
            certificate_descriptions[index] for index in certificate_indices
        ],
        "verification": "xor coefficients = 0 and xor rhs = 1",
    }

    failed_omitted_pair = frozenset((0, 1))
    failed_missing_pair = frozenset((2, 3))
    failed_six_support = frozenset(set(W) - set(failed_omitted_pair))
    built_six_certificate = build_global_rows(
        edges,
        incidence,
        flow,
        planes,
        failed_six_support,
        failed_missing_pair,
    )
    assert built_six_certificate is not None
    six_certificate_rows, six_certificate_descriptions = built_six_certificate
    six_certificate_indices = gf2_dual_certificate(
        3 * vertex_count, six_certificate_rows
    )
    assert six_certificate_indices is not None
    six_certificate = {
        "omitted_pair": sorted(failed_omitted_pair),
        "missing_pair": sorted(failed_missing_pair),
        "row_count": len(six_certificate_rows),
        "selected_row_indices": six_certificate_indices,
        "selected_row_count": len(six_certificate_indices),
        "selected_rows": [
            six_certificate_descriptions[index]
            for index in six_certificate_indices
        ],
        "verification": "xor coefficients = 0 and xor rhs = 1",
    }

    six_hole_passes = []
    for omitted in itertools.combinations(W, 2):
        six_support = frozenset(set(W) - set(omitted))
        for missing in itertools.combinations(sorted(six_support), 2):
            result = build_global_system(
                edges,
                incidence,
                flow,
                planes,
                six_support,
                frozenset(missing),
            )
            if result["sat"]:
                kind = (
                    "parallel"
                    if omitted[0] ^ omitted[1] == missing[0] ^ missing[1]
                    else "skew"
                )
                six_hole_passes.append(
                    {
                        "omitted_pair": list(omitted),
                        "missing_pair": list(missing),
                        "kind": kind,
                        "dimension": result["dimension"],
                    }
                )
    expected_passes = [
        ((0, 3), (4, 5)),
        ((0, 3), (6, 7)),
        ((1, 2), (4, 5)),
        ((1, 2), (6, 7)),
        ((4, 7), (0, 1)),
        ((4, 7), (2, 3)),
        ((5, 6), (0, 1)),
        ((5, 6), (2, 3)),
    ]
    assert [
        (tuple(row["omitted_pair"]), tuple(row["missing_pair"]))
        for row in six_hole_passes
    ] == expected_passes
    assert all(
        row["kind"] == "skew" and row["dimension"] == 1
        for row in six_hole_passes
    )

    return {
        "reference_sha256": hashlib.sha256(raw).hexdigest(),
        "vertices": vertex_count,
        "edges": len(edges),
        "simple_cubic_connected_bridgeless": True,
        "literal_six_point_pair_types_used": len(used_pair_types),
        "fixed_flow_five_point_passes": len(five_set_passes),
        "sample_five_point_left_kernel_certificate": five_certificate,
        "sample_six_hole_left_kernel_certificate": six_certificate,
        "fixed_flow_six_point_one_hole_passes": six_hole_passes,
    }


def main() -> None:
    report = {
        "schema": "six-point-one-hole-affine-audit-v1",
        "status": "PASS",
        "local": local_audit(),
        "strict_witness": witness_audit(),
        "scope": (
            "Exact local and fixed-flow affine characterization for "
            "finite loopless cubic graphs; not a FiveCDC resolution."
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
