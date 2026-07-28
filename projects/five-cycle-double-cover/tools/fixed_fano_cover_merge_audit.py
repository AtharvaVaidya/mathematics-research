#!/usr/bin/env python3
"""Search all three-pair merges over every 8-CDC with one fixed Fano flow.

Let ``phi`` be a nowhere-zero F_2^3-flow on a loopless cubic graph.  An
8-CDC over the coordinate set F_2^3 that projects to ``phi`` assigns an
unordered pair ``P_e`` to every edge such that

    xor(P_e) = phi(e)

and the three pairs at each vertex form a triangle.  The latter condition is
equivalent to even incidence of each of the eight coordinates.

Merging eight coordinates into five by identifying three disjoint pairs is
valid exactly when none of those three pairs occurs as an edge label.  This
script enumerates every size-three matching of the eight coordinates and
uses a small SAT instance to choose all vertex triangles consistently.

This audits the freedom among *all* 8-CDCs projecting to one fixed flow.  It
does not quantify over other nowhere-zero F_2^3-flows and therefore cannot,
by itself, decide the five-cycle double cover conjecture.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable


Pair = tuple[int, int]
State = tuple[Pair, Pair, Pair]


def normalized_pair(first: int, second: int) -> Pair:
    if first == second:
        raise ValueError("a coordinate pair must contain two distinct points")
    return (first, second) if first < second else (second, first)


def load_cover(path: Path) -> tuple[int, tuple[tuple[int, int], ...], tuple[Pair, ...]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    vertices = len(value["vertices"])
    rows = sorted(value["edges"], key=lambda row: int(row["id"]))
    if [int(row["id"]) for row in rows] != list(range(len(rows))):
        raise ValueError("edge IDs must be consecutive")
    edges = tuple((int(row["u"]), int(row["v"])) for row in rows)
    labels = tuple(
        normalized_pair(int(row["label"][0]), int(row["label"][1]))
        for row in rows
    )
    return vertices, edges, labels


def load_flow_witness(
    path: Path, object_key: str | None
) -> tuple[int, tuple[tuple[int, int], ...], tuple[int, ...]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if object_key is not None:
        for key in object_key.split("."):
            value = value[key]
    vertices = int(value["vertices"])
    edges = tuple(
        (
            int(row["u"]) if isinstance(row, dict) else int(row[0]),
            int(row["v"]) if isinstance(row, dict) else int(row[1]),
        )
        for row in value["edges"]
    )
    flow_rows = value.get("flow_values_by_edge", value.get("flow"))
    if flow_rows is None:
        raise ValueError("flow witness has neither flow_values_by_edge nor flow")
    flow = tuple(int(item) for item in flow_rows)
    if len(flow) != len(edges):
        raise ValueError("flow value count differs from the edge count")
    return vertices, edges, flow


def graph_incidence(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    incidence: list[list[int]] = [[] for _ in range(vertices)]
    seen_edges: set[Pair] = set()
    for edge, (u, v) in enumerate(edges):
        if not (0 <= u < vertices and 0 <= v < vertices):
            raise ValueError("edge endpoint outside the vertex range")
        if u == v:
            raise ValueError("this audit is for loopless cubic graphs")
        pair = normalized_pair(u, v)
        if pair in seen_edges:
            raise ValueError("this audit currently requires a simple graph")
        seen_edges.add(pair)
        incidence[u].append(edge)
        incidence[v].append(edge)
    if any(len(row) != 3 for row in incidence):
        raise ValueError("the input graph is not cubic")
    return tuple(tuple(sorted(row)) for row in incidence)


def validate_supplied_cover(
    vertices: int,
    incidence: tuple[tuple[int, ...], ...],
    labels: tuple[Pair, ...],
) -> None:
    for vertex in range(vertices):
        counts: Counter[int] = Counter()
        for edge in incidence[vertex]:
            counts.update(labels[edge])
        if any(count & 1 for count in counts.values()):
            raise ValueError(f"supplied labels have odd parity at vertex {vertex}")


def local_states(
    incidence: tuple[tuple[int, ...], ...],
    flow: tuple[int, ...],
) -> tuple[tuple[State, ...], ...]:
    result: list[tuple[State, ...]] = []
    for vertex, incident in enumerate(incidence):
        values = tuple(flow[edge] for edge in incident)
        if 0 in values or len(set(values)) != 3 or values[0] ^ values[1] ^ values[2]:
            raise ValueError(
                f"edge values at vertex {vertex} are not a nonzero Fano line"
            )
        states: set[State] = set()
        for triangle in combinations(range(8), 3):
            by_difference = {
                first ^ second: normalized_pair(first, second)
                for first, second in combinations(triangle, 2)
            }
            if set(by_difference) == set(values):
                states.add(tuple(by_difference[value] for value in values))
        ordered = tuple(sorted(states))
        if len(ordered) != 8:
            raise AssertionError(
                f"expected eight local coordinate triangles, found {len(ordered)}"
            )
        result.append(ordered)
    return tuple(result)


def all_three_pair_matchings() -> tuple[tuple[Pair, Pair, Pair], ...]:
    matchings: set[tuple[Pair, Pair, Pair]] = set()
    for used_points in combinations(range(8), 6):
        first = used_points[0]
        remaining = used_points[1:]
        for mate in remaining:
            rest = tuple(point for point in remaining if point != mate)
            for second_mate in rest[1:]:
                first_pair = normalized_pair(first, mate)
                second_pair = normalized_pair(rest[0], second_mate)
                last = tuple(
                    point for point in rest[1:] if point != second_mate
                )
                third_pair = normalized_pair(last[0], last[1])
                matchings.add(tuple(sorted((first_pair, second_pair, third_pair))))
    ordered = tuple(sorted(matchings))
    if len(ordered) != 420:
        raise AssertionError(f"expected 420 matchings, found {len(ordered)}")
    return ordered


PAIR_INDEX = {
    pair: index for index, pair in enumerate(combinations(range(8), 2))
}
MATCHING_MASKS = tuple(
    (
        sum(1 << PAIR_INDEX[pair] for pair in matching),
        matching,
    )
    for matching in all_three_pair_matchings()
)


def five_coloring_of_used_pairs(used_mask: int) -> tuple[int, ...] | None:
    """Return a proper coloring of the eight-coordinate co-occurrence graph."""

    adjacency = [0] * 8
    for (first, second), index in PAIR_INDEX.items():
        if (used_mask >> index) & 1:
            adjacency[first] |= 1 << second
            adjacency[second] |= 1 << first
    colors = [-1] * 8

    def search(colored: int, used_colors: int) -> bool:
        if colored == 8:
            return True
        uncolored = [vertex for vertex in range(8) if colors[vertex] < 0]
        vertex = max(
            uncolored,
            key=lambda item: (
                len(
                    {
                        colors[neighbor]
                        for neighbor in range(8)
                        if colors[neighbor] >= 0
                        and ((adjacency[item] >> neighbor) & 1)
                    }
                ),
                (adjacency[item] & sum(1 << v for v in uncolored)).bit_count(),
                -item,
            ),
        )
        forbidden = {
            colors[neighbor]
            for neighbor in range(8)
            if colors[neighbor] >= 0
            and ((adjacency[vertex] >> neighbor) & 1)
        }
        for color in range(min(used_colors + 1, 5)):
            if color in forbidden:
                continue
            colors[vertex] = color
            if search(colored + 1, max(used_colors, color + 1)):
                return True
            colors[vertex] = -1
        return False

    return tuple(colors) if search(0, 0) else None


def maximum_clique_size_of_used_pairs(used_mask: int) -> int:
    best = 1
    for size in range(2, 9):
        if any(
            all(
                (used_mask >> PAIR_INDEX[normalized_pair(first, second)]) & 1
                for first, second in combinations(vertices, 2)
            )
            for vertices in combinations(range(8), size)
        ):
            best = size
        else:
            break
    return best


def fixed_flow_potential_rows(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    flow: tuple[int, ...],
    *,
    fix_translation: bool,
) -> list[tuple[int, int]]:
    """Build Oum's linear compatibility system for the vertex potentials."""

    rows: list[tuple[int, int]] = []
    for edge, (u, v) in enumerate(edges):
        u_other = next(item for item in incidence[u] if item != edge)
        v_other = next(item for item in incidence[v] if item != edge)
        difference = flow[u_other] ^ flow[v_other]
        value = flow[edge]
        orthogonal = [
            vector
            for vector in range(1, 8)
            if ((vector & value).bit_count() & 1) == 0
        ]
        if len(orthogonal) != 3:
            raise AssertionError("nonzero Fano value has wrong orthogonal plane")
        for functional in orthogonal[:2]:
            mask = 0
            for vertex in (u, v):
                for bit in range(3):
                    if (functional >> bit) & 1:
                        mask ^= 1 << (3 * vertex + bit)
            rhs = (functional & difference).bit_count() & 1
            rows.append((mask, rhs))
    if fix_translation:
        rows.extend((1 << bit, 0) for bit in range(3))
    return rows


def gf2_rref(
    rows: Iterable[tuple[int, int]],
) -> dict[int, tuple[int, int]]:
    pivots: dict[int, tuple[int, int]] = {}
    for original_mask, original_rhs in rows:
        mask, rhs = original_mask, original_rhs
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (mask, rhs)
                break
            old_mask, old_rhs = pivots[pivot]
            mask ^= old_mask
            rhs ^= old_rhs
        if mask == 0 and rhs:
            raise AssertionError("Oum compatibility system is inconsistent")
    return pivots


def potential_assignment(
    pivots: dict[int, tuple[int, int]],
    free_variables: tuple[int, ...],
    free_bits: int,
) -> int:
    assignment = sum(
        1 << variable
        for index, variable in enumerate(free_variables)
        if (free_bits >> index) & 1
    )
    for pivot in sorted(pivots):
        mask, rhs = pivots[pivot]
        lower = mask & ((1 << pivot) - 1)
        value = ((lower & assignment).bit_count() & 1) ^ rhs
        if value:
            assignment |= 1 << pivot
    return assignment


def labels_from_potentials(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    flow: tuple[int, ...],
    assignment: int,
) -> tuple[Pair, ...]:
    potentials = tuple(
        sum(
            ((assignment >> (3 * vertex + bit)) & 1) << bit
            for bit in range(3)
        )
        for vertex in range(vertices)
    )
    labels: list[Pair] = []
    for edge, (u, v) in enumerate(edges):
        u_other = next(item for item in incidence[u] if item != edge)
        first = potentials[u] ^ flow[u_other]
        u_pair = normalized_pair(first, first ^ flow[edge])
        v_other = next(item for item in incidence[v] if item != edge)
        second = potentials[v] ^ flow[v_other]
        v_pair = normalized_pair(second, second ^ flow[edge])
        if u_pair != v_pair:
            raise AssertionError("potential solution gives inconsistent edge labels")
        labels.append(u_pair)
    return tuple(labels)


def direct_potential_merge_audit(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    flow: tuple[int, ...],
    *,
    exhaustive: bool = True,
    criterion: str = "three-pair",
) -> dict[str, Any]:
    """Exhaust the affine potential space after fixing global translation."""

    if criterion not in {"three-pair", "five-color"}:
        raise ValueError("criterion must be 'three-pair' or 'five-color'")
    rows = fixed_flow_potential_rows(
        vertices, edges, incidence, flow, fix_translation=True
    )
    pivots = gf2_rref(rows)
    free = tuple(
        variable for variable in range(3 * vertices) if variable not in pivots
    )
    solutions = 1 << len(free)
    used_pair_profile: Counter[int] = Counter()
    clique_profile: Counter[int] = Counter()
    maximum_missing_matching = 0
    first_witness: dict[str, Any] | None = None
    first_five_color_witness: dict[str, Any] | None = None
    examined = 0
    for free_bits in range(solutions):
        examined += 1
        assignment = potential_assignment(pivots, free, free_bits)
        if any(
            ((mask & assignment).bit_count() & 1) != rhs
            for mask, rhs in rows
        ):
            raise AssertionError("enumerated potential violates a row")
        labels = labels_from_potentials(
            vertices, edges, incidence, flow, assignment
        )
        used_mask = 0
        for pair in labels:
            used_mask |= 1 << PAIR_INDEX[pair]
        used_pair_profile[used_mask.bit_count()] += 1
        clique_profile[maximum_clique_size_of_used_pairs(used_mask)] += 1
        matching = next(
            (
                candidate
                for matching_mask, candidate in MATCHING_MASKS
                if not (matching_mask & used_mask)
            ),
            None,
        )
        coloring = five_coloring_of_used_pairs(used_mask)
        if coloring is not None and first_five_color_witness is None:
            first_five_color_witness = {
                "free_assignment_index": free_bits,
                "potential_word": assignment,
                "color_by_coordinate": list(coloring),
                "eight_cover_labels": [list(pair) for pair in labels],
            }
        if matching is not None:
            maximum_missing_matching = max(maximum_missing_matching, 3)
            if first_witness is None:
                first_witness = {
                    "free_assignment_index": free_bits,
                    "potential_word": assignment,
                    "forbidden_merge_pairs": [
                        list(pair) for pair in matching
                    ],
                    "eight_cover_labels": [list(pair) for pair in labels],
                }
        elif maximum_missing_matching < 2:
            missing_pairs = tuple(
                pair
                for pair, index in PAIR_INDEX.items()
                if not ((used_mask >> index) & 1)
            )
            if any(
                len({*first, *second}) == 4
                for first, second in combinations(missing_pairs, 2)
            ):
                maximum_missing_matching = 2
            elif missing_pairs:
                maximum_missing_matching = 1
        criterion_satisfied = (
            first_witness is not None
            if criterion == "three-pair"
            else first_five_color_witness is not None
        )
        if criterion_satisfied and not exhaustive:
            break

    return {
        "compatibility_rows": len(rows),
        "rank_after_translation_gauge": len(pivots),
        "free_dimension_after_translation_gauge": len(free),
        "potential_solutions_after_translation_gauge": solutions,
        "potential_solutions_before_translation_gauge": 8 * solutions,
        "potential_solutions_examined": examined,
        "exhaustive": exhaustive or examined == solutions,
        "used_pair_count_profile": {
            str(count): multiplicity
            for count, multiplicity in sorted(used_pair_profile.items())
        },
        "maximum_clique_size_profile": {
            str(size): multiplicity
            for size, multiplicity in sorted(clique_profile.items())
        },
        "maximum_missing_pair_matching": maximum_missing_matching,
        "merge_exists": first_witness is not None,
        "first_witness": first_witness,
        "five_color_merge_exists": first_five_color_witness is not None,
        "first_five_color_witness": first_five_color_witness,
        "stopping_criterion": criterion,
    }


def variable(vertex: int, state: int) -> int:
    return 8 * vertex + state + 1


def build_cnf(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    states: tuple[tuple[State, ...], ...],
    forbidden: tuple[Pair, Pair, Pair],
) -> tuple[int, list[tuple[int, ...]]]:
    clauses: list[tuple[int, ...]] = []
    forbidden_set = frozenset(forbidden)
    edge_position = [
        {edge: position for position, edge in enumerate(incidence[vertex])}
        for vertex in range(vertices)
    ]
    for vertex in range(vertices):
        clauses.append(tuple(variable(vertex, state) for state in range(8)))
        for first, second in combinations(range(8), 2):
            clauses.append((-variable(vertex, first), -variable(vertex, second)))
        for state, pairs in enumerate(states[vertex]):
            if any(pair in forbidden_set for pair in pairs):
                clauses.append((-variable(vertex, state),))

    for edge, (u, v) in enumerate(edges):
        u_position = edge_position[u][edge]
        v_position = edge_position[v][edge]
        for u_state in range(8):
            u_pair = states[u][u_state][u_position]
            for v_state in range(8):
                if u_pair != states[v][v_state][v_position]:
                    clauses.append(
                        (-variable(u, u_state), -variable(v, v_state))
                    )
    return 8 * vertices, clauses


def color_variable(vertices: int, point: int, color: int) -> int:
    return 8 * vertices + 5 * point + color + 1


def build_joint_merge_cnf(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    states: tuple[tuple[State, ...], ...],
) -> tuple[int, list[tuple[int, ...]]]:
    """Choose the 8-CDC and the three disjoint coordinate merges jointly."""

    variables, clauses = build_cnf(
        vertices, edges, incidence, states, ()
    )
    if variables != 8 * vertices:
        raise AssertionError("unexpected local-state variable range")

    for point in range(8):
        clauses.append(
            tuple(color_variable(vertices, point, color) for color in range(5))
        )
        for first, second in combinations(range(5), 2):
            clauses.append(
                (
                    -color_variable(vertices, point, first),
                    -color_variable(vertices, point, second),
                )
            )
    for color in range(5):
        clauses.append(
            tuple(color_variable(vertices, point, color) for point in range(8))
        )
        for triple in combinations(range(8), 3):
            clauses.append(
                tuple(
                    -color_variable(vertices, point, color) for point in triple
                )
            )

    for vertex in range(vertices):
        for state, pairs in enumerate(states[vertex]):
            for first, second in pairs:
                for color in range(5):
                    clauses.append(
                        (
                            -variable(vertex, state),
                            -color_variable(vertices, first, color),
                            -color_variable(vertices, second, color),
                        )
                    )
    return 8 * vertices + 40, clauses


def write_dimacs(
    path: Path, variables: int, clauses: Iterable[tuple[int, ...]]
) -> None:
    clause_rows = list(clauses)
    with path.open("w", encoding="ascii") as handle:
        handle.write(f"p cnf {variables} {len(clause_rows)}\n")
        for clause in clause_rows:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def solve(
    cadical: str,
    variables: int,
    clauses: list[tuple[int, ...]],
) -> tuple[bool, frozenset[int], str]:
    with tempfile.TemporaryDirectory(prefix="fixed-fano-merge-") as temporary:
        cnf = Path(temporary) / "instance.cnf"
        write_dimacs(cnf, variables, clauses)
        completed = subprocess.run(
            [cadical, "-q", "--seed=0", str(cnf)],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    if completed.returncode not in (10, 20):
        raise RuntimeError(
            f"CaDiCaL returned {completed.returncode}: {completed.stderr}"
        )
    output = completed.stdout + completed.stderr
    satisfiable = completed.returncode == 10
    model = frozenset(
        literal
        for line in output.splitlines()
        if line.startswith("v ")
        for literal in map(int, line.split()[1:])
        if literal > 0
    )
    if satisfiable and not model:
        raise RuntimeError("CaDiCaL reported SAT without a model")
    return satisfiable, model, output


def decode_and_check(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    states: tuple[tuple[State, ...], ...],
    flow: tuple[int, ...],
    forbidden: tuple[Pair, Pair, Pair],
    model: frozenset[int],
) -> dict[str, Any]:
    chosen_states: list[int] = []
    for vertex in range(vertices):
        chosen = [
            state
            for state in range(8)
            if variable(vertex, state) in model
        ]
        if len(chosen) != 1:
            raise AssertionError("model does not choose exactly one local state")
        chosen_states.append(chosen[0])

    edge_position = [
        {edge: position for position, edge in enumerate(incidence[vertex])}
        for vertex in range(vertices)
    ]
    labels: list[Pair] = []
    for edge, (u, v) in enumerate(edges):
        u_pair = states[u][chosen_states[u]][edge_position[u][edge]]
        v_pair = states[v][chosen_states[v]][edge_position[v][edge]]
        if u_pair != v_pair:
            raise AssertionError("decoded endpoint states disagree")
        if u_pair[0] ^ u_pair[1] != flow[edge]:
            raise AssertionError("decoded edge pair has the wrong flow difference")
        labels.append(u_pair)

    forbidden_set = frozenset(forbidden)
    if any(pair in forbidden_set for pair in labels):
        raise AssertionError("decoded cover uses a forbidden merge pair")
    for vertex in range(vertices):
        counts: Counter[int] = Counter()
        for edge in incidence[vertex]:
            counts.update(labels[edge])
        if any(count & 1 for count in counts.values()):
            raise AssertionError("decoded cover violates coordinate parity")

    merge_color: dict[int, int] = {}
    for color, pair in enumerate(forbidden):
        merge_color[pair[0]] = color
        merge_color[pair[1]] = color
    next_color = 3
    for point in range(8):
        if point not in merge_color:
            merge_color[point] = next_color
            next_color += 1
    if next_color != 5:
        raise AssertionError("forbidden matching did not induce five colors")
    five_labels = [
        normalized_pair(merge_color[first], merge_color[second])
        for first, second in labels
    ]
    for vertex in range(vertices):
        counts = Counter()
        for edge in incidence[vertex]:
            counts.update(five_labels[edge])
        if any(count & 1 for count in counts.values()):
            raise AssertionError("merged five-cover violates coordinate parity")

    return {
        "chosen_local_states": chosen_states,
        "eight_cover_labels": [list(pair) for pair in labels],
        "merge_color_by_coordinate": {
            str(point): merge_color[point] for point in range(8)
        },
        "five_cover_labels": [list(pair) for pair in five_labels],
        "five_coordinate_edge_counts": [
            sum(color in pair for pair in five_labels) for color in range(5)
        ],
    }


def decode_joint_matching(
    vertices: int, model: frozenset[int]
) -> tuple[Pair, Pair, Pair]:
    color_classes: list[list[int]] = [[] for _ in range(5)]
    for point in range(8):
        chosen = [
            color
            for color in range(5)
            if color_variable(vertices, point, color) in model
        ]
        if len(chosen) != 1:
            raise AssertionError("joint model does not assign one color per point")
        color_classes[chosen[0]].append(point)
    if sorted(map(len, color_classes)) != [1, 1, 2, 2, 2]:
        raise AssertionError("joint model does not define three disjoint merges")
    return tuple(
        sorted(
            normalized_pair(points[0], points[1])
            for points in color_classes
            if len(points) == 2
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--cover", type=Path)
    inputs.add_argument("--flow-witness", type=Path)
    parser.add_argument(
        "--flow-object-key",
        help="optional dot-separated object path inside --flow-witness JSON",
    )
    parser.add_argument("--cadical", default=shutil.which("cadical") or "cadical")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--exhaustive",
        action="store_true",
        help="classify all 420 matchings instead of stopping at the first SAT case",
    )
    parser.add_argument(
        "--joint",
        action="store_true",
        help="choose a merge matching inside one SAT instance",
    )
    arguments = parser.parse_args()
    if arguments.joint and arguments.exhaustive:
        parser.error("--joint and --exhaustive are mutually exclusive")

    if arguments.cover is not None:
        vertices, edges, supplied_labels = load_cover(arguments.cover)
        flow = tuple(first ^ second for first, second in supplied_labels)
        input_path = arguments.cover
        input_mode = "supplied-eight-cover"
    else:
        vertices, edges, flow = load_flow_witness(
            arguments.flow_witness, arguments.flow_object_key
        )
        supplied_labels = None
        input_path = arguments.flow_witness
        input_mode = "fixed-flow-witness"
    incidence = graph_incidence(vertices, edges)
    states = local_states(incidence, flow)
    if supplied_labels is not None:
        validate_supplied_cover(vertices, incidence, supplied_labels)
        supplied_state_membership = []
        for vertex in range(vertices):
            pairs = tuple(supplied_labels[edge] for edge in incidence[vertex])
            supplied_state_membership.append(pairs in states[vertex])
        if not all(supplied_state_membership):
            raise AssertionError("the supplied cover is absent from the state system")

    satisfiable_rows: list[dict[str, Any]] = []
    unsatisfiable = 0
    checked = 0
    first_witness: dict[str, Any] | None = None
    if arguments.joint:
        variables, clauses = build_joint_merge_cnf(
            vertices, edges, incidence, states
        )
        satisfiable, model, _ = solve(arguments.cadical, variables, clauses)
        checked = 1
        if satisfiable:
            forbidden = decode_joint_matching(vertices, model)
            witness = decode_and_check(
                vertices,
                edges,
                incidence,
                states,
                flow,
                forbidden,
                model,
            )
            first_witness = {
                "matching_index": all_three_pair_matchings().index(forbidden),
                "forbidden_merge_pairs": [list(pair) for pair in forbidden],
                "variables": variables,
                "clauses": len(clauses),
                **witness,
            }
            satisfiable_rows.append(first_witness)
        else:
            unsatisfiable = 1
        candidate_iterator: Iterable[
            tuple[int, tuple[Pair, Pair, Pair]]
        ] = ()
    else:
        candidate_iterator = enumerate(all_three_pair_matchings())

    for index, forbidden in candidate_iterator:
        variables, clauses = build_cnf(
            vertices, edges, incidence, states, forbidden
        )
        satisfiable, model, _ = solve(arguments.cadical, variables, clauses)
        checked += 1
        if satisfiable:
            witness = decode_and_check(
                vertices,
                edges,
                incidence,
                states,
                flow,
                forbidden,
                model,
            )
            row = {
                "matching_index": index,
                "forbidden_merge_pairs": [list(pair) for pair in forbidden],
                "variables": variables,
                "clauses": len(clauses),
                **witness,
            }
            satisfiable_rows.append(row)
            if first_witness is None:
                first_witness = row
            if not arguments.exhaustive:
                break
        else:
            unsatisfiable += 1

    report = {
        "format": "fixed-fano-cover-three-pair-merge-audit-v1",
        "scope": (
            "All 8-CDCs over F_2^3 projecting to the one fixed flow induced "
            "by the input; other flows are not quantified."
        ),
        "input": str(input_path),
        "input_mode": input_mode,
        "vertices": vertices,
        "edges": len(edges),
        "fixed_flow_value_counts": {
            str(value): count
            for value, count in sorted(Counter(flow).items())
        },
        "candidate_matchings_total": 420,
        "candidate_matchings_checked": checked,
        "joint_merge_encoding": arguments.joint,
        "satisfiable_matchings": len(satisfiable_rows),
        "unsatisfiable_matchings": unsatisfiable,
        "first_witness": first_witness,
    }
    if arguments.exhaustive:
        report["satisfiable_rows"] = satisfiable_rows
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(
        json.dumps(
            {
                "vertices": vertices,
                "edges": len(edges),
                "checked": checked,
                "sat": len(satisfiable_rows),
                "unsat": unsatisfiable,
                "first_forbidden_matching": (
                    first_witness["forbidden_merge_pairs"]
                    if first_witness is not None
                    else None
                ),
                "five_coordinate_edge_counts": (
                    first_witness["five_coordinate_edge_counts"]
                    if first_witness is not None
                    else None
                ),
            },
            sort_keys=True,
        )
    )
    return 0 if first_witness is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
