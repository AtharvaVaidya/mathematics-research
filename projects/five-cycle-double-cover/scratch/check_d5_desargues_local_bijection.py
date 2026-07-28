#!/usr/bin/env python3
"""Exact checks for the Desargues/Petersen formulation of cubic D5 flows.

The script uses only the Python standard library.  It independently checks:

* the two-way conversion between D5 flows and Desargues incidence maps;
* the conversion on a cubic multigraph with three parallel edge objects;
* the exact vertex-state/port-extension criterion;
* a hand-sized K_{3,3} obstruction to the tempting stronger requirement
  that the two endpoint point-states of every edge be distinct; and
* the local distinction between this formulation and Petersen coloring.

It is not a Five-Cycle Double Cover solver.
"""

from __future__ import annotations

from itertools import combinations, product


OMEGA = (1 << 5) - 1
PAIRS = tuple((1 << i) | (1 << j) for i, j in combinations(range(5), 2))
PAIR_SET = frozenset(PAIRS)
TRIPLES = tuple(
    (1 << i) | (1 << j) | (1 << k)
    for i, j, k in combinations(range(5), 3)
)
TRIPLE_SET = frozenset(TRIPLES)


THETA_EDGES = ((0, 1), (0, 1), (0, 1))
K4_EDGES = tuple(combinations(range(4), 2))
K33_EDGES = tuple((left, right) for left in range(3) for right in range(3, 6))
PETERSEN_EDGES = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (0, 4),
    (0, 5),
    (1, 6),
    (2, 7),
    (3, 8),
    (4, 9),
    (5, 7),
    (7, 9),
    (6, 9),
    (6, 8),
    (5, 8),
)


def bits(mask: int) -> tuple[int, ...]:
    return tuple(i for i in range(5) if (mask >> i) & 1)


def text(mask: int) -> str:
    return "".join(str(i) for i in bits(mask))


def incidence(
    vertex_count: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    """Return incident edge IDs; parallel edge objects remain distinct."""
    rows: list[list[int]] = [[] for _ in range(vertex_count)]
    for edge_id, (left, right) in enumerate(edges):
        assert 0 <= left < vertex_count
        assert 0 <= right < vertex_count
        assert left != right, "this audit is for loopless cubic multigraphs"
        rows[left].append(edge_id)
        rows[right].append(edge_id)
    answer = tuple(tuple(row) for row in rows)
    assert all(len(row) == 3 for row in answer)
    return answer


def validate_flow(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
) -> None:
    rows = incidence(vertex_count, edges)
    assert len(flow) == len(edges)
    assert all(label in PAIR_SET for label in flow)
    for row in rows:
        assert flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0


def enumerate_flows(
    vertex_count: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    """Enumerate literal flows by XOR propagation, without SAT libraries."""
    rows = incidence(vertex_count, edges)
    state = [0] * len(edges)
    answers: list[tuple[int, ...]] = []

    def assign(edge_id: int, label: int, changed: list[int]) -> bool:
        if state[edge_id]:
            return state[edge_id] == label
        if label not in PAIR_SET:
            return False
        state[edge_id] = label
        changed.append(edge_id)
        pending = list(edges[edge_id])
        while pending:
            vertex = pending.pop()
            row = rows[vertex]
            assigned = [item for item in row if state[item]]
            if len(assigned) < 2:
                continue
            if len(assigned) == 3:
                if state[row[0]] ^ state[row[1]] ^ state[row[2]]:
                    return False
                continue
            missing = next(item for item in row if not state[item])
            forced = state[assigned[0]] ^ state[assigned[1]]
            if forced not in PAIR_SET:
                return False
            state[missing] = forced
            changed.append(missing)
            pending.extend(edges[missing])
        return True

    def visit() -> None:
        try:
            edge_id = next(i for i, label in enumerate(state) if not label)
        except StopIteration:
            answer = tuple(state)
            validate_flow(vertex_count, edges, answer)
            answers.append(answer)
            return
        for label in PAIRS:
            changed: list[int] = []
            if assign(edge_id, label, changed):
                visit()
            for item in reversed(changed):
                state[item] = 0

    visit()
    return tuple(answers)


def flow_to_dual_desargues(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return complementary point states B_v and line states T_e.

    Directly, q(e) is a Desargues point and the union A_v of the three
    labels at v is a Desargues line.  Complementation gives the dual model
    B_v = Omega\\A_v and T_e = Omega\\q(e).
    """
    validate_flow(vertex_count, edges, flow)
    rows = incidence(vertex_count, edges)
    points = []
    for row in rows:
        support = flow[row[0]] | flow[row[1]] | flow[row[2]]
        assert support in TRIPLE_SET
        points.append(OMEGA ^ support)
    lines = tuple(OMEGA ^ label for label in flow)
    answer = (tuple(points), lines)
    validate_dual_desargues(vertex_count, edges, *answer)
    return answer


def validate_dual_desargues(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    points: tuple[int, ...],
    lines: tuple[int, ...],
) -> None:
    """Check incidence and local port bijectivity at every graph vertex."""
    rows = incidence(vertex_count, edges)
    assert len(points) == vertex_count
    assert len(lines) == len(edges)
    assert all(point in PAIR_SET for point in points)
    assert all(line in TRIPLE_SET for line in lines)
    for edge_id, (left, right) in enumerate(edges):
        line = lines[edge_id]
        assert points[left] & ~line == 0
        assert points[right] & ~line == 0
    for vertex, row in enumerate(rows):
        expected = {
            points[vertex] | (1 << coordinate)
            for coordinate in range(5)
            if not ((points[vertex] >> coordinate) & 1)
        }
        actual = {lines[edge_id] for edge_id in row}
        assert len(actual) == 3
        assert actual == expected


def dual_desargues_to_flow(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    points: tuple[int, ...],
    lines: tuple[int, ...],
) -> tuple[int, ...]:
    validate_dual_desargues(vertex_count, edges, points, lines)
    flow = tuple(OMEGA ^ line for line in lines)
    validate_flow(vertex_count, edges, flow)
    return flow


def direct_realization_count(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    points: tuple[int, ...],
) -> tuple[int, frozenset[tuple[int, ...]]]:
    """Choose common Desargues lines directly, then test all local stars."""
    rows = incidence(vertex_count, edges)
    choices = []
    for left, right in edges:
        common = tuple(
            line
            for line in TRIPLES
            if points[left] & ~line == 0 and points[right] & ~line == 0
        )
        if not common:
            return 0, frozenset()
        choices.append(common)

    flows: set[tuple[int, ...]] = set()
    count = 0
    for lines in product(*choices):
        okay = True
        for vertex, row in enumerate(rows):
            expected = {
                points[vertex] | (1 << coordinate)
                for coordinate in range(5)
                if not ((points[vertex] >> coordinate) & 1)
            }
            actual = {lines[edge_id] for edge_id in row}
            if len(actual) != 3 or actual != expected:
                okay = False
                break
        if okay:
            count += 1
            flows.add(tuple(OMEGA ^ line for line in lines))
    return count, frozenset(flows)


def port_criterion_count(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    points: tuple[int, ...],
) -> int:
    """Count realizations using the forced-port/list-edge-coloring criterion."""
    rows = incidence(vertex_count, edges)
    forced_at_vertex: list[list[int]] = [[] for _ in range(vertex_count)]
    equal_edges = []

    for edge_id, (left, right) in enumerate(edges):
        left_point = points[left]
        right_point = points[right]
        if left_point == right_point:
            equal_edges.append(edge_id)
            continue
        if (left_point & right_point).bit_count() != 1:
            return 0
        left_port = right_point & ~left_point
        right_port = left_point & ~right_point
        assert left_port.bit_count() == right_port.bit_count() == 1
        forced_at_vertex[left].append(left_port)
        forced_at_vertex[right].append(right_port)

    available = []
    for vertex in range(vertex_count):
        forced = forced_at_vertex[vertex]
        if len(set(forced)) != len(forced):
            return 0
        used = 0
        for port in forced:
            used |= port
        palette = (OMEGA ^ points[vertex]) & ~used
        equal_degree = sum(
            1
            for edge_id in rows[vertex]
            if points[edges[edge_id][0]] == points[edges[edge_id][1]]
        )
        assert palette.bit_count() == equal_degree
        available.append(palette)

    edge_choices = []
    for edge_id in equal_edges:
        left, right = edges[edge_id]
        choices = tuple(
            1 << coordinate
            for coordinate in range(5)
            if ((available[left] & available[right]) >> coordinate) & 1
        )
        if not choices:
            return 0
        edge_choices.append(choices)

    count = 0
    for colors in product(*edge_choices):
        color_by_edge = dict(zip(equal_edges, colors))
        okay = True
        for vertex, row in enumerate(rows):
            used = [
                color_by_edge[edge_id]
                for edge_id in row
                if edge_id in color_by_edge
            ]
            if len(set(used)) != len(used):
                okay = False
                break
            union = 0
            for color in used:
                union |= color
            if union != available[vertex]:
                okay = False
                break
        if okay:
            count += 1
    return count


def audit_graph_equivalence(
    name: str,
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[int, int]:
    """Compare independent flow and incidence-map enumerations."""
    literal_flows = frozenset(enumerate_flows(vertex_count, edges))
    map_flows: set[tuple[int, ...]] = set()
    map_count = 0

    for points in product(PAIRS, repeat=vertex_count):
        direct_count, direct_flows = direct_realization_count(
            vertex_count, edges, points
        )
        criterion_count = port_criterion_count(vertex_count, edges, points)
        assert direct_count == criterion_count
        map_count += direct_count
        map_flows.update(direct_flows)

    assert map_count == len(map_flows)
    assert map_flows == literal_flows
    for flow in literal_flows:
        points, lines = flow_to_dual_desargues(vertex_count, edges, flow)
        assert dual_desargues_to_flow(
            vertex_count, edges, points, lines
        ) == flow

    strict_count = 0
    for flow in literal_flows:
        points, _lines = flow_to_dual_desargues(vertex_count, edges, flow)
        if all(points[left] != points[right] for left, right in edges):
            strict_count += 1

    print(
        f"{name}: literal flows={len(literal_flows)}, "
        f"Desargues maps={map_count}, strict={strict_count}"
    )
    return len(literal_flows), strict_count


def k33_hand_case_audit() -> None:
    """Replay the two-case human proof that K_{3,3} has no strict map."""
    base = (1 << 0) | (1 << 1)
    outside = (2, 3, 4)

    # Around base=01, a strict local star has one right state {0 or 1,x}
    # for each x in {2,3,4}.  Up to swapping 0/1 and permuting x, only the
    # number of choices using 0 matters: min(k,3-k) is 0 or 1.
    type_invariants = set()
    for choices in product((0, 1), repeat=3):
        right_states = tuple(
            (1 << chosen) | (1 << external)
            for chosen, external in zip(choices, outside)
        )
        assert all((state & base).bit_count() == 1 for state in right_states)
        external_ports = tuple(state & ~base for state in right_states)
        assert len(set(external_ports)) == 3
        zero_count = sum(1 for chosen in choices if chosen == 0)
        type_invariants.add(min(zero_count, 3 - zero_count))
    assert type_invariants == {0, 1}

    representatives = (
        (
            (1 << 0) | (1 << 2),
            (1 << 0) | (1 << 3),
            (1 << 0) | (1 << 4),
        ),
        (
            (1 << 0) | (1 << 2),
            (1 << 1) | (1 << 3),
            (1 << 1) | (1 << 4),
        ),
    )

    candidate_lists = []
    for right_states in representatives:
        candidates = []
        for point in PAIRS:
            if point == base:
                continue
            if not all((point & state).bit_count() == 1 for state in right_states):
                continue
            ports = tuple(state & ~point for state in right_states)
            if all(port.bit_count() == 1 for port in ports) and len(set(ports)) == 3:
                candidates.append(point)
        candidate_lists.append(tuple(candidates))

    assert candidate_lists[0] == ()
    assert candidate_lists[1] == ((1 << 1) | (1 << 2),)

    # The three left states in K_{3,3} must be distinct: at any fixed right
    # state, equal left states would force the same port twice.  In the first
    # case there is no second left state, and in the second there is only one.
    assert all(len(candidates) < 2 for candidates in candidate_lists)
    print(
        "K3,3 hand cases after B(u0)=01: "
        "other-left candidates=(0, 1); strict map impossible"
    )


def k33_flow_audit() -> None:
    flows = enumerate_flows(6, K33_EDGES)
    strict = 0
    for flow in flows:
        points, _lines = flow_to_dual_desargues(6, K33_EDGES, flow)
        strict += all(points[left] != points[right] for left, right in K33_EDGES)
    assert len(flows) == 840
    assert strict == 0

    # A literal D5 flow still exists: use a Tait coloring and the triangle
    # labels 01, 02, 12.  Thus K_{3,3} refutes only the strict strengthening.
    tait_labels = (
        (1 << 0) | (1 << 1),
        (1 << 0) | (1 << 2),
        (1 << 1) | (1 << 2),
    )
    witness = tuple(
        tait_labels[(left + right - 3) % 3] for left, right in K33_EDGES
    )
    validate_flow(6, K33_EDGES, witness)
    points, _lines = flow_to_dual_desargues(6, K33_EDGES, witness)
    assert len(set(points)) == 1
    assert text(points[0]) == "34"
    print(
        "K3,3: literal flows=840, strict=0; "
        "Tait-supported witness has constant B_v=34"
    )


def petersen_distinction_audit() -> None:
    """Compare allowable endpoint-center relations in the two notions."""
    # In a dual Desargues map both endpoint point-states lie on one 3-set.
    desargues_intersections = set()
    for line in TRIPLES:
        incident_points = tuple(point for point in PAIRS if point & ~line == 0)
        assert len(incident_points) == 3
        for left in incident_points:
            for right in incident_points:
                desargues_intersections.add((left & right).bit_count())
    assert desargues_intersections == {1, 2}

    # In a Petersen coloring both local star centers are incident with the
    # same Petersen edge.  They may choose the same endpoint, or the two
    # distinct (disjoint) endpoints.
    petersen_intersections = set()
    petersen_edges = tuple(
        (left, right)
        for left, right in combinations(PAIRS, 2)
        if left & right == 0
    )
    assert len(petersen_edges) == 15
    for first, second in petersen_edges:
        for left in (first, second):
            for right in (first, second):
                petersen_intersections.add((left & right).bit_count())
    assert petersen_intersections == {0, 2}
    print(
        "endpoint-state intersections: "
        "D5/Desargues={1,2}, Petersen-coloring={0,2}"
    )


def petersen_strict_audit() -> None:
    flows = enumerate_flows(10, PETERSEN_EDGES)
    strict = 0
    for flow in flows:
        points, _lines = flow_to_dual_desargues(10, PETERSEN_EDGES, flow)
        strict += all(
            points[left] != points[right] for left, right in PETERSEN_EDGES
        )
    assert len(flows) == 6000
    assert strict == 0
    print("Petersen graph: literal flows=6000, strict=0")


def main() -> None:
    theta_total, theta_strict = audit_graph_equivalence(
        "triple-edge multigraph", 2, THETA_EDGES
    )
    assert (theta_total, theta_strict) == (60, 0)

    k4_total, k4_strict = audit_graph_equivalence("K4", 4, K4_EDGES)
    assert (k4_total, k4_strict) == (180, 120)

    k33_hand_case_audit()
    k33_flow_audit()
    petersen_distinction_audit()
    petersen_strict_audit()
    print("PASS")


if __name__ == "__main__":
    main()
