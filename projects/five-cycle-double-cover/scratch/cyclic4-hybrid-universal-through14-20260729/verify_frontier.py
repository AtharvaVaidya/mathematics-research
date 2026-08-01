#!/usr/bin/env python3
"""Independent solver-free audit of the cyclic-4 path-core frontier.

This file imports no producer module.  It reconstructs the graph census,
automorphism orbits, six connector states, both Blanusa six-poles, and all
saved macro/atom witnesses.
"""

from __future__ import annotations

from itertools import combinations, permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ORDERS = (6, 8, 10, 12, 14)
CONNECTED_COUNTS = {6: 2, 8: 5, 10: 19, 12: 85, 14: 509}
CYCLIC4_COUNTS = {6: 1, 8: 2, 10: 5, 12: 18, 14: 84}
ORBIT_COUNTS = {6: 1, 8: 5, 10: 32, 12: 445, 14: 8795}
GIRTH5_ORBIT_COUNTS = {6: 0, 8: 0, 10: 2, 12: 20, 14: 433}
DUADS = frozenset((3, 5, 6, 9, 10, 12, 17, 18, 20, 24))
ATOM_SOURCES = {
    "A": (
        "Q??CA?_CCOW_Q_M?AD@A_@K?F??",
        (4, 9),
        (8, 10, 11, 3, 13, 14),
    ),
    "B": (
        "Q???C@?GCoOoDO[?CcAO_?k?J??",
        (13, 16),
        (1, 2, 3, 6, 8, 9),
    ),
}


def path_core():
    answer = []
    universe = {1, 2, 3, 4}
    for first, second in combinations(sorted(universe), 2):
        other = sorted(universe.difference({first, second}))
        answer.append(tuple(sorted((
            1 | (1 << first),
            1 | (1 << second),
            (1 << other[0]) | (1 << other[1]),
        ))))
    return tuple(sorted(answer))


PATH_CORE = path_core()
STAR_STATE = (6, 10, 18)
SEVEN_STATES = frozenset((*PATH_CORE, STAR_STATE))
ORDERED_PATH = frozenset(
    tuple(row[index] for index in action)
    for row in PATH_CORE
    for action in permutations(range(3))
)


def decode_graph6(record):
    vertices = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, tuple(edges)


def incidence(vertices, edges):
    rows = [[] for _ in range(vertices)]
    masks = [0] * vertices
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
        masks[left] |= 1 << right
        masks[right] |= 1 << left
    return tuple(tuple(sorted(row)) for row in rows), tuple(masks)


def connected(vertices, masks):
    seen = 1
    queue = [0]
    for vertex in queue:
        unseen = masks[vertex] & ~seen
        while unseen:
            bit = unseen & -unseen
            unseen ^= bit
            seen |= bit
            queue.append(bit.bit_length() - 1)
    return seen == (1 << vertices) - 1


def cyclically_four(vertices, edges, masks):
    internal = [0] * (1 << (vertices - 1))
    for reduced in range(1 << (vertices - 1)):
        if reduced:
            bit = reduced & -reduced
            previous = reduced ^ bit
            vertex = bit.bit_length()
            previous_shore = (previous << 1) | 1
            internal[reduced] = (
                internal[previous]
                + (masks[vertex] & previous_shore).bit_count()
            )
        shore = (reduced << 1) | 1
        shore_vertices = shore.bit_count()
        if shore_vertices == vertices:
            continue
        shore_edges = internal[reduced]
        cut = 3 * shore_vertices - 2 * shore_edges
        if cut > 3:
            continue
        other_vertices = vertices - shore_vertices
        other_edges = len(edges) - shore_edges - cut
        if shore_edges >= shore_vertices and other_edges >= other_vertices:
            return False
    return True


def graph_girth(vertices, masks):
    best = vertices + 1
    for source in range(vertices):
        distance = [-1] * vertices
        parent = [-1] * vertices
        distance[source] = 0
        queue = [source]
        for vertex in queue:
            neighbours = masks[vertex]
            while neighbours:
                bit = neighbours & -neighbours
                neighbours ^= bit
                other = bit.bit_length() - 1
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    best = min(
                        best,
                        distance[vertex] + distance[other] + 1,
                    )
    return best


def automorphisms(vertices, edges):
    neighbours = [set() for _ in range(vertices)]
    for left, right in edges:
        neighbours[left].add(right)
        neighbours[right].add(left)
    mapping = {}
    used = set()
    answer = []

    def choose():
        return max(
            (v for v in range(vertices) if v not in mapping),
            key=lambda v: sum(w in mapping for w in neighbours[v]),
        )

    def visit():
        if len(mapping) == vertices:
            answer.append(tuple(mapping[v] for v in range(vertices)))
            return
        vertex = choose()
        for image in range(vertices):
            if image in used:
                continue
            if all(
                (other in neighbours[vertex])
                == (mapping[other] in neighbours[image])
                for other in mapping
            ):
                mapping[vertex] = image
                used.add(image)
                visit()
                used.remove(image)
                del mapping[vertex]

    visit()
    return tuple(answer)


def junction_orbits(vertices, edges, actions):
    edge_set = set(edges)
    representatives = {}
    raw = 0
    for size in range(2, vertices + 1, 2):
        for junctions in combinations(range(vertices), size):
            if any(
                tuple(sorted(pair)) in edge_set
                for pair in combinations(junctions, 2)
            ):
                continue
            raw += 1
            key = min(
                tuple(sorted(action[v] for v in junctions))
                for action in actions
            )
            representatives.setdefault(key, junctions)
    return representatives, raw


def reconstruct_census():
    expected = {}
    graph_data = {}
    girth5_orbits = 0
    report = json.loads(
        (HERE / "census-report.json").read_text(encoding="ascii")
    )
    for order in ORDERS:
        records = [
            line
            for line in (HERE / f"order{order}-connected-cubic.g6")
            .read_text(encoding="ascii")
            .splitlines()
            if line
        ]
        if len(records) != CONNECTED_COUNTS[order]:
            raise AssertionError("wrong connected cubic source count")
        reported = {
            row["graph_index"]: row
            for row in report["orders"][str(order)]["graphs"]
        }
        cyclic_count = 0
        orbit_count = 0
        local_girth5 = 0
        for graph_index, graph6 in enumerate(records):
            vertices, edges = decode_graph6(graph6)
            rows, masks = incidence(vertices, edges)
            if (
                vertices != order
                or len(edges) != 3 * order // 2
                or any(len(row) != 3 for row in rows)
                or not connected(vertices, masks)
            ):
                raise AssertionError("bad graph6 source record")
            if not cyclically_four(vertices, edges, masks):
                if graph_index in reported:
                    raise AssertionError("non-cyclic4 graph entered census")
                continue
            cyclic_count += 1
            girth = graph_girth(vertices, masks)
            actions = automorphisms(vertices, edges)
            representatives, raw = junction_orbits(
                vertices, edges, actions
            )
            row = reported.get(graph_index)
            if row is None or (
                row["graph6"],
                row["girth"],
                row["automorphisms"],
                row["raw_independent_positive_even_junction_sets"],
                row["canonical_junction_orbits"],
            ) != (
                graph6,
                girth,
                len(actions),
                raw,
                len(representatives),
            ):
                raise AssertionError("census metadata mismatch")
            claimed_reps = {
                tuple(value) for value in row["junction_representatives"]
            }
            actual_reps = set(representatives.values())
            if claimed_reps != actual_reps:
                raise AssertionError("junction representatives mismatch")
            for junctions in actual_reps:
                expected[(order, graph_index, junctions)] = None
                graph_data[(order, graph_index)] = (
                    edges,
                    rows,
                    girth,
                )
            orbit_count += len(actual_reps)
            if girth >= 5:
                local_girth5 += len(actual_reps)
        if (
            cyclic_count,
            orbit_count,
            local_girth5,
        ) != (
            CYCLIC4_COUNTS[order],
            ORBIT_COUNTS[order],
            GIRTH5_ORBIT_COUNTS[order],
        ):
            raise AssertionError("wrong independent cyclic4 order summary")
        girth5_orbits += local_girth5
    if len(expected) != 9278 or girth5_orbits != 455:
        raise AssertionError("wrong total cyclic4 frontier")
    return expected, graph_data


def verify_macro_witnesses(expected, graph_data):
    report = json.loads(
        (HERE / "path-core-report.json").read_text(encoding="ascii")
    )
    if (
        report["statuses"] != {"path_core_safe_sat": 9278}
        or report["failures"]
    ):
        raise AssertionError("wrong path-core status summary")
    selected = {
        tuple(row) for row in report["selected_connector_states"]
    }
    if selected != set(PATH_CORE):
        raise AssertionError("wrong claimed path-core states")
    seen = set()
    for record in report["witnesses"]:
        key = (
            record["order"],
            record["graph_index"],
            tuple(record["junctions"]),
        )
        if key in seen or key not in expected:
            raise AssertionError("unexpected or duplicate macro witness")
        seen.add(key)
        edges, rows, girth = graph_data[key[:2]]
        if record["girth"] != girth:
            raise AssertionError("macro witness girth mismatch")
        labels = tuple(record["edge_labels"])
        if (
            len(labels) != len(edges)
            or any(label not in DUADS for label in labels)
        ):
            raise AssertionError("macro witness has non-duad edge")
        junctions = set(key[2])
        for vertex, row in enumerate(rows):
            word = tuple(labels[edge] for edge in row)
            if vertex in junctions:
                if word[0] ^ word[1] ^ word[2]:
                    raise AssertionError("junction is not Eulerian")
            elif tuple(sorted(word)) not in PATH_CORE:
                raise AssertionError("connector left the path core")
    if seen != set(expected):
        raise AssertionError("macro witness coverage is incomplete")


def six_pole(graph6, deleted_vertices, expected_ports):
    vertices, edges = decode_graph6(graph6)
    source_rows = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        source_rows[left].append((right, edge))
        source_rows[right].append((left, edge))
    deleted = set(deleted_vertices)
    retained = [v for v in range(vertices) if v not in deleted]
    mapping = {old: new for new, old in enumerate(retained)}
    internal = tuple(
        (mapping[left], mapping[right])
        for left, right in edges
        if left not in deleted and right not in deleted
    )
    ports = tuple(
        mapping[other]
        for deleted_vertex in deleted_vertices
        for other, _ in sorted(source_rows[deleted_vertex])
    )
    if (
        vertices,
        len(edges),
        len(internal),
        ports,
    ) != (18, 27, 21, expected_ports):
        raise AssertionError("wrong independent atom topology")
    rows = [[] for _ in range(16)]
    for edge, (left, right) in enumerate(internal):
        rows[left].append(edge)
        rows[right].append(edge)
    return internal, ports, tuple(tuple(row) for row in rows)


def verify_atom_witnesses():
    report = json.loads(
        (HERE / "path-atom-witnesses.json").read_text(encoding="ascii")
    )
    if (
        {tuple(row) for row in report["path_states_unordered"]}
        != set(PATH_CORE)
        or report["ordered_connector_states"] != 36
        or report["ordered_boundary_words_per_atom"] != 1296
    ):
        raise AssertionError("wrong path-atom witness premise")
    expected_words = {
        left + right for left in ORDERED_PATH for right in ORDERED_PATH
    }
    if len(expected_words) != 1296:
        raise AssertionError("wrong independent boundary-word count")
    atoms = {row["atom_type"]: row for row in report["atoms"]}
    if set(atoms) != set(ATOM_SOURCES):
        raise AssertionError("wrong atom set")
    for atom_type, (graph6, deleted, expected_ports) in ATOM_SOURCES.items():
        internal, ports, rows = six_pole(
            graph6, deleted, expected_ports
        )
        atom = atoms[atom_type]
        if (
            atom["graph6"] != graph6
            or tuple(atom["deleted_vertices"]) != deleted
            or tuple(atom["ports"]) != ports
            or tuple(tuple(edge) for edge in atom["internal_edges"])
            != internal
        ):
            raise AssertionError("atom record topology mismatch")
        seen = set()
        port_index = {vertex: index for index, vertex in enumerate(ports)}
        for witness in atom["witnesses"]:
            word = tuple(witness["boundary_word"])
            labels = tuple(witness["internal_labels"])
            if (
                word in seen
                or word not in expected_words
                or len(labels) != 21
                or any(label not in DUADS for label in labels)
            ):
                raise AssertionError("bad atom witness record")
            seen.add(word)
            for vertex in range(16):
                parity = 0
                for edge in rows[vertex]:
                    parity ^= labels[edge]
                if vertex in port_index:
                    parity ^= word[port_index[vertex]]
                if parity:
                    raise AssertionError("atom witness violates parity")
        if seen != expected_words:
            raise AssertionError("atom boundary coverage is incomplete")


def verify_diagnostic():
    report = json.loads(
        (HERE / "diagnostic-summary.json").read_text(encoding="ascii")
    )
    failure = report["smallest_diagnostic_failure"]
    vertices, edges = decode_graph6(failure["graph6"])
    rows, masks = incidence(vertices, edges)
    if (
        vertices != 14
        or failure["girth"] != graph_girth(vertices, masks)
        or cyclically_four(vertices, edges, masks)
    ):
        raise AssertionError("wrong diagnostic macro metadata")
    full = (1 << vertices) - 1
    for shore in range(1, full):
        if not (shore & 1) or shore == full:
            continue
        cut_size = sum(
            (masks[v] & (full ^ shore)).bit_count()
            for v in range(vertices)
            if shore & (1 << v)
        )
        if cut_size < 3:
            raise AssertionError("diagnostic macro is not 3-edge-connected")
    cut = failure["cyclic_three_edge_cut"]
    cut_indices = tuple(cut["edge_indices"])
    if tuple(tuple(edges[index]) for index in cut_indices) != tuple(
        tuple(edge) for edge in cut["edges"]
    ):
        raise AssertionError("diagnostic cut edges moved")
    shore = set(cut["shore"])
    actual_cut = {
        index
        for index, (left, right) in enumerate(edges)
        if (left in shore) != (right in shore)
    }
    if actual_cut != set(cut_indices):
        raise AssertionError("diagnostic shore has wrong boundary")
    shore_edges = sum(
        left in shore and right in shore for left, right in edges
    )
    other_edges = (
        len(edges) - shore_edges - len(actual_cut)
    )
    if (
        shore_edges < len(shore)
        or other_edges < vertices - len(shore)
    ):
        raise AssertionError("displayed 3-cut is not cyclic")
    junctions = set(failure["junctions"])
    repair = report["seven_state_repair"]
    labels = tuple(repair["explicit_repair_edge_labels"])
    if (
        len(labels) != len(edges)
        or any(label not in DUADS for label in labels)
        or tuple(repair["added_star_state"]) != STAR_STATE
    ):
        raise AssertionError("bad diagnostic repair labels")
    for vertex, row in enumerate(rows):
        word = tuple(labels[edge] for edge in row)
        if vertex in junctions:
            if word[0] ^ word[1] ^ word[2]:
                raise AssertionError("diagnostic junction parity failure")
        elif tuple(sorted(word)) not in SEVEN_STATES:
            raise AssertionError("diagnostic repair left seven states")


def main() -> int:
    if (
        len(PATH_CORE) != 6
        or len(ORDERED_PATH) != 36
        or {label for row in PATH_CORE for label in row} != DUADS
    ):
        raise AssertionError("wrong independently constructed path core")
    expected, graph_data = reconstruct_census()
    verify_macro_witnesses(expected, graph_data)
    verify_atom_witnesses()
    verify_diagnostic()
    print("PASS cyclically-4 hybrid path-core frontier through order 14")
    print("cyclic4_macros=110 junction_orbits=9278")
    print("girth_at_least_5_macros=12 junction_orbits=455")
    print("macro_witnesses=9278 atom_completions=2592")
    print("cyclic_three_cut_diagnostic_repair=checked")
    print("all_matchings_all_atom_types_all_port_orders=true")
    print("target_unsat=0 target_resolution=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
