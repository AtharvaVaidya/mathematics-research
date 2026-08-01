#!/usr/bin/env python3
"""Independent, standard-library semantic checker for the 18-vertex record.

This checker does not import any search or certificate-producing module.  It
reconstructs the graph, Oum potential space, all 21 binary-cycle image tests,
the outside-line repair, and the resulting ordinary five-cycle double cover.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def incidence(order, edges):
    rows = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(sorted(row)) for row in rows)


def connected(order, edges, omitted=None):
    adjacency = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        if edge == omitted:
            continue
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for other in adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return len(seen) == order


def induced_has_cycle(vertices, edges, shore):
    points = [vertex for vertex in range(vertices) if vertex in shore]
    if not points:
        return False
    adjacency = {vertex: [] for vertex in points}
    internal_edges = 0
    for left, right in edges:
        if left in shore and right in shore:
            adjacency[left].append(right)
            adjacency[right].append(left)
            internal_edges += 1
    components = 0
    unseen = set(points)
    while unseen:
        components += 1
        root = unseen.pop()
        queue = [root]
        while queue:
            vertex = queue.pop()
            for other in adjacency[vertex]:
                if other in unseen:
                    unseen.remove(other)
                    queue.append(other)
    return internal_edges > len(points) - components


def cyclically_four(order, edges):
    universe = frozenset(range(order))
    for bits in range(1 << (order - 1)):
        shore = frozenset(
            {0}
            | {
                vertex
                for vertex in range(1, order)
                if (bits >> (vertex - 1)) & 1
            }
        )
        if shore == universe:
            continue
        cut = sum((left in shore) != (right in shore) for left, right in edges)
        if cut < 4 and induced_has_cycle(order, edges, shore) and induced_has_cycle(
            order, edges, universe - shore
        ):
            return False
    return True


def three_edge_colorable(order, edges, rows):
    colors = [-1] * len(edges)
    used = [set() for _ in range(order)]

    def search(colored):
        if colored == len(edges):
            return True
        candidates = [
            edge
            for edge in range(len(edges))
            if colors[edge] < 0
        ]
        edge = max(
            candidates,
            key=lambda item: sum(
                colors[other] >= 0
                for vertex in edges[item]
                for other in rows[vertex]
            ),
        )
        left, right = edges[edge]
        for color in range(3):
            if color in used[left] or color in used[right]:
                continue
            colors[edge] = color
            used[left].add(color)
            used[right].add(color)
            if search(colored + 1):
                return True
            used[left].remove(color)
            used[right].remove(color)
            colors[edge] = -1
        return False

    return search(0)


def dot(first, second):
    return (first & second).bit_count() & 1


def gf2_rref(equations):
    pivots = {}
    for original_mask, original_rhs in equations:
        mask, rhs = original_mask, original_rhs
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (mask, rhs)
                break
            old_mask, old_rhs = pivots[pivot]
            mask ^= old_mask
            rhs ^= old_rhs
        assert mask or not rhs
    return pivots


def solve_from_free(pivots, variable_count, free_word):
    free = tuple(variable for variable in range(variable_count) if variable not in pivots)
    assignment = sum(
        1 << variable
        for index, variable in enumerate(free)
        if (free_word >> index) & 1
    )
    for pivot in sorted(pivots):
        mask, rhs = pivots[pivot]
        lower = mask & ((1 << pivot) - 1)
        if ((lower & assignment).bit_count() & 1) ^ rhs:
            assignment |= 1 << pivot
    return assignment


def oum_solutions(order, edges, rows, flow):
    equations = []
    for edge, (left, right) in enumerate(edges):
        left_other = next(item for item in rows[left] if item != edge)
        right_other = next(item for item in rows[right] if item != edge)
        difference = flow[left_other] ^ flow[right_other]
        orthogonal = [
            functional
            for functional in range(1, 8)
            if dot(functional, flow[edge]) == 0
        ]
        assert len(orthogonal) == 3
        for functional in orthogonal[:2]:
            mask = 0
            for vertex in (left, right):
                for bit in range(3):
                    if (functional >> bit) & 1:
                        mask ^= 1 << (3 * vertex + bit)
            equations.append((mask, dot(functional, difference)))
    equations.extend((1 << bit, 0) for bit in range(3))
    pivots = gf2_rref(equations)
    free = 3 * order - len(pivots)
    assert len(equations) == 57 and len(pivots) == 53 and free == 1
    return tuple(
        solve_from_free(pivots, 3 * order, word)
        for word in range(1 << free)
    )


def oum_labels(order, edges, rows, flow, assignment):
    potentials = tuple(
        sum(
            ((assignment >> (3 * vertex + bit)) & 1) << bit
            for bit in range(3)
        )
        for vertex in range(order)
    )
    labels = []
    for edge, (left, right) in enumerate(edges):
        left_other = next(item for item in rows[left] if item != edge)
        right_other = next(item for item in rows[right] if item != edge)
        first = potentials[left] ^ flow[left_other]
        second = potentials[right] ^ flow[right_other]
        left_pair = tuple(sorted((first, first ^ flow[edge])))
        right_pair = tuple(sorted((second, second ^ flow[edge])))
        assert left_pair == right_pair
        labels.append(left_pair)
    return potentials, tuple(labels)


def components(order, edges, selected):
    adjacency = [[] for _ in range(order)]
    for edge in selected:
        left, right = edges[edge]
        adjacency[left].append(right)
        adjacency[right].append(left)
    unseen = set(range(order))
    output = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        queue = [root]
        while queue:
            vertex = queue.pop()
            for other in adjacency[vertex]:
                if other in unseen:
                    unseen.remove(other)
                    component.add(other)
                    queue.append(other)
        output.append(frozenset(component))
    return tuple(output)


def cycle_basis(order, edges, allowed):
    adjacency = [[] for _ in range(order)]
    for edge in allowed:
        left, right = edges[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    seen = set()
    basis = []
    for root in range(order):
        if root in seen:
            continue
        seen.add(root)
        parent = {root: root}
        parent_edge = {root: -1}
        depth = {root: 0}
        stack = [root]
        while stack:
            vertex = stack.pop()
            for other, edge in adjacency[vertex]:
                if other in seen:
                    continue
                seen.add(other)
                parent[other] = vertex
                parent_edge[other] = edge
                depth[other] = depth[vertex] + 1
                stack.append(other)
        component = frozenset(parent)
        tree_edges = {edge for edge in parent_edge.values() if edge >= 0}
        for edge in allowed:
            left, right = edges[edge]
            if left not in component or edge in tree_edges:
                continue
            cycle = 1 << edge
            first, second = left, right
            while depth[first] > depth[second]:
                cycle ^= 1 << parent_edge[first]
                first = parent[first]
            while depth[second] > depth[first]:
                cycle ^= 1 << parent_edge[second]
                second = parent[second]
            while first != second:
                cycle ^= 1 << parent_edge[first]
                first = parent[first]
                cycle ^= 1 << parent_edge[second]
                second = parent[second]
            basis.append(cycle)
    return tuple(basis)


def all_cycle_masks(basis):
    output = []
    for word in range(1 << len(basis)):
        cycle = 0
        for index, generator in enumerate(basis):
            if (word >> index) & 1:
                cycle ^= generator
        output.append(cycle)
    return tuple(output)


def cleaning_row(order, edges, flow, mu, switch_value):
    line = tuple(value for value in range(1, 8) if dot(mu, value) == 0)
    assert switch_value in line
    factor = {edge for edge, value in enumerate(flow) if value in line}
    pieces = components(order, edges, factor)
    owner = {}
    for index, piece in enumerate(pieces):
        owner.update((vertex, index) for vertex in piece)
    affine = tuple(value for value in range(1, 8) if dot(mu, value) == 1)
    base = min(affine)
    defect = 0
    for edge, (left, right) in enumerate(edges):
        if owner[left] != owner[right] and flow[edge] == base:
            defect ^= (1 << owner[left]) ^ (1 << owner[right])
    pair = {base, base ^ switch_value}
    basis = cycle_basis(
        order,
        edges,
        {edge for edge, value in enumerate(flow) if value != switch_value},
    )
    images = set()
    for cycle in all_cycle_masks(basis):
        image = 0
        for edge, (left, right) in enumerate(edges):
            if (
                (cycle >> edge) & 1
                and owner[left] != owner[right]
                and flow[edge] in pair
            ):
                image ^= (1 << owner[left]) ^ (1 << owner[right])
        images.add(image)
    return len(pieces), defect, len(basis), images


def verify_cover(order, edges, rows, cover):
    assert len(cover) == 5
    for coordinate in cover:
        selected = set(coordinate)
        assert len(selected) == len(coordinate)
        assert all(sum(edge in selected for edge in row) % 2 == 0 for row in rows)
    assert all(sum(edge in coordinate for coordinate in cover) == 2 for edge in range(len(edges)))


def main():
    data = json.loads((HERE / "construction.json").read_text(encoding="utf-8"))
    report = json.loads((HERE / "report.json").read_text(encoding="utf-8"))
    order = data["order"]
    edges = tuple((row["u"], row["v"]) for row in data["edges"])
    flow = tuple(data["flow_values_by_edge"])
    rows = incidence(order, edges)

    assert [row["id"] for row in data["edges"]] == list(range(len(edges)))
    assert len(edges) == len(set(edges)) == 27
    assert all(left < right for left, right in edges)
    assert all(len(row) == 3 for row in rows)
    assert connected(order, edges)
    assert all(connected(order, edges, edge) for edge in range(len(edges)))
    assert cyclically_four(order, edges)
    assert not three_edge_colorable(order, edges, rows)
    assert all(1 <= value <= 7 for value in flow)
    assert all(flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0 for row in rows)

    solutions = oum_solutions(order, edges, rows, flow)
    expected_potentials = tuple(
        tuple(row) for row in data["Oum_compatibility"]["potential_vectors"]
    )
    observed_potentials = []
    for assignment in solutions:
        potentials, labels = oum_labels(order, edges, rows, flow, assignment)
        observed_potentials.append(potentials)
        used = set(labels)
        assert len(used) == 19
        # A literal K6 is a short certificate that no five-color merge exists.
        clique = data["Oum_compatibility"]["common_K6_coordinates"]
        assert all(tuple(sorted(pair)) in used for pair in combinations(clique, 2))
        for vertex, row in enumerate(rows):
            counts = {
                point: sum(point in labels[edge] for edge in row)
                for point in range(8)
            }
            assert all(count % 2 == 0 for count in counts.values()), vertex
    assert tuple(observed_potentials) == expected_potentials

    certificate_rows = {
        (row["mu"], row["switch_value"]): row
        for row in report["functional_value_rows"]
    }
    assert len(certificate_rows) == 21
    for mu in range(1, 8):
        line = tuple(value for value in range(1, 8) if dot(mu, value) == 0)
        for switch_value in line:
            piece_count, defect, dimension, images = cleaning_row(
                order, edges, flow, mu, switch_value
            )
            assert defect not in images
            row = certificate_rows[(mu, switch_value)]
            assert row["factor_components"] == piece_count
            assert row["rainbow_defect_mask"] == defect
            assert row["cycle_basis_dimension_G_minus_M_t"] == dimension
            assert row["r_mu_in_image_tau_t"] is False
            dual = row["separating_dual_mask"]
            assert (dual & defect).bit_count() % 2 == 1
            assert all((dual & image).bit_count() % 2 == 0 for image in images)

    repair = data["outside_line_repair"]
    circuit = set(repair["circuit_edge_ids"])
    degrees = [
        sum(edge in circuit for edge in rows[vertex])
        for vertex in range(order)
    ]
    assert set(degrees) <= {0, 2}
    assert all(flow[edge] != repair["switch_value"] for edge in circuit)
    switched = tuple(
        value ^ repair["switch_value"] if edge in circuit else value
        for edge, value in enumerate(flow)
    )
    assert list(switched) == repair["switched_flow_values_by_edge"]
    mu = repair["repaired_functional"]
    line = tuple(value for value in range(1, 8) if dot(mu, value) == 0)
    assert list(line) == repair["repaired_line"]
    factor = {edge for edge, value in enumerate(switched) if value in line}
    pieces = components(order, edges, factor)
    affine = tuple(value for value in range(1, 8) if dot(mu, value) == 1)
    for piece in pieces:
        boundary = [
            edge
            for edge, (left, right) in enumerate(edges)
            if (left in piece) != (right in piece)
        ]
        assert all(
            sum(flow_value == value for edge, flow_value in enumerate(switched) if edge in boundary) % 2 == 0
            for value in affine
        )

    cover = tuple(
        tuple(coordinate)
        for coordinate in data["explicit_standard_five_cdc_edge_ids"]
    )
    verify_cover(order, edges, rows, cover)
    labels = tuple(
        sum((1 << coordinate) for coordinate in range(5) if edge in cover[coordinate])
        for edge in range(len(edges))
    )
    kernel = 0b01111
    basis_images = (0b00011, 0b00101, 0b10001)

    def section(value):
        return (
            (basis_images[0] if value & 1 else 0)
            ^ (basis_images[1] if value & 2 else 0)
            ^ (basis_images[2] if value & 4 else 0)
        )

    quotient = {
        lift: value
        for value in range(8)
        for lift in (section(value), section(value) ^ kernel)
    }

    def line_normalizing_map(value):
        return (
            (4 if value & 1 else 0)
            ^ (1 if value & 2 else 0)
            ^ (2 if value & 4 else 0)
        )

    assert all(label.bit_count() == 2 for label in labels)
    assert tuple(quotient[label] for label in labels) == tuple(
        line_normalizing_map(value) for value in switched
    )

    print("independent semantic checker: PASS")
    print("graph: simple, cubic, bridgeless, cyclically 4-edge-connected, non-Tait")
    print("Oum premise: 2 gauged covers, each contains the displayed K6")
    print("fixed-line test: all 21 cycle images exhaustively reject r_mu")
    print("repair: one outside-line 5-circuit switch yields an explicit five-CDC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
