#!/usr/bin/env python3
"""Lazy exact global rotation/twist solver for order-100 frontier matrices.

Variables choose:

* one exact row-star word for each A-factor circuit;
* one exact row-star word for each B-factor circuit; and
* in every nonempty incidence cell, a bijection and endpoint orientation
  that gives the selected two factor circuits local girth at least ten.

The labelled 46 c-edge objects are then globally glued.  Every short cycle
in the resulting marked expansion G-M yields a sound no-good over precisely
the cell choices that determine its B-edges.  Once G-M has girth at least
ten, all 105 pairings of the eight marked subdivision vertices are checked.

SAT returns a concrete 100-vertex graph.  UNSAT is exact for the fixed
matrix and finite domains, but this discovery script does not request a
proof object.  An unfinished run proves nothing.
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import subprocess
import sys
from pathlib import Path

import check_order100_pairwise_rotation_gluing as local


N_MARKS = 8
ARTIFACT = Path("scratch/order100-exact-row-star-survivors.json")


def all_pairings(items):
    if not items:
        yield ()
        return
    first = items[0]
    for position in range(1, len(items)):
        second = items[position]
        rest = items[1:position] + items[position + 1 :]
        for tail in all_pairings(rest):
            yield ((first, second),) + tail


PAIRINGS = tuple(all_pairings(tuple(range(N_MARKS))))
assert len(PAIRINGS) == 105


def word_domains(record):
    x = tuple(record["x"])
    y = tuple(record["y"])
    matrix = tuple(tuple(row) for row in record["matrix"])
    columns = tuple(
        tuple(matrix[row][column] for row in range(8))
        for column in range(8)
    )
    a_words = tuple(
        local.all_words(x[row], y, row, matrix[row])
        for row in range(8)
    )
    b_words = tuple(
        local.all_words(y[column], x, column, columns[column])
        for column in range(8)
    )
    assert all(a_words) and all(b_words)
    return x, y, matrix, a_words, b_words


def pair_option_is_good(
    x_value,
    y_value,
    diagonal,
    positions_a,
    positions_b,
    mapping,
    orientation,
):
    """Check one fixed word-pair bijection/orientation exactly."""
    m = len(positions_a)
    a_weights = local.residual_weights(5 + x_value, positions_a, diagonal)
    b_weights = local.residual_weights(5 + y_value, positions_b, diagonal)
    q_edges = [
        (2 * q, 2 * q + 1, 2 if diagonal and q == 0 else 1)
        for q in range(m)
    ]
    a_edges = [
        (2 * q + 1, 2 * ((q + 1) % m), a_weights[q])
        for q in range(m)
    ]
    b_edges = []
    for b_index, current in enumerate(mapping):
        following = mapping[(b_index + 1) % m]
        current_reverse = orientation >> current & 1
        following_reverse = orientation >> following & 1
        exit_vertex = 2 * current + (0 if current_reverse else 1)
        entry_vertex = 2 * following + (1 if following_reverse else 0)
        b_edges.append((exit_vertex, entry_vertex, b_weights[b_index]))
    return local.weighted_girth_at_least_ten(q_edges + a_edges + b_edges)


def build_cell_domains(x, y, matrix, a_words, b_words):
    domains = {}
    for row in range(8):
        for column in range(8):
            m = matrix[row][column]
            if m == 0:
                continue
            options = []
            for a_index, a_word in enumerate(a_words[row]):
                positions_a = tuple(
                    position
                    for position, label in enumerate(a_word)
                    if label == column
                )
                assert len(positions_a) == m
                for b_index, b_word in enumerate(b_words[column]):
                    positions_b = tuple(
                        position
                        for position, label in enumerate(b_word)
                        if label == row
                    )
                    assert len(positions_b) == m
                    if row == column:
                        mappings = (
                            (0,) + tail
                            for tail in itertools.permutations(range(1, m))
                        )
                    else:
                        mappings = itertools.permutations(range(m))
                    for mapping in mappings:
                        for orientation in range(1 << m):
                            # An undirected B-circuit has two traversal
                            # descriptions.  Reverse it if necessary so the
                            # marked diagonal connection (local A index 0)
                            # is traversed with orientation bit zero.
                            if row == column and orientation & 1:
                                continue
                            if not pair_option_is_good(
                                x[row],
                                y[column],
                                row == column,
                                positions_a,
                                positions_b,
                                mapping,
                                orientation,
                            ):
                                continue
                            options.append(
                                (a_index, b_index, tuple(mapping), orientation)
                            )
            assert options, (row, column)
            domains[row, column] = tuple(options)
    return domains


def token_layout(a_words, chosen_a):
    """Use fixed A-position slots as the canonical 46 c-edge tokens."""
    offsets = []
    total = 0
    for row in range(8):
        offsets.append(total)
        total += len(a_words[row][chosen_a[row]])
    assert total == 46
    return tuple(offsets)


def chosen_graph(
    matrix,
    a_words,
    b_words,
    cell_domains,
    values,
    pairing_index=None,
):
    """Build G-M, or G when ``pairing_index`` is supplied."""
    chosen_a = tuple(values[f"A{row}"] for row in range(8))
    chosen_b = tuple(values[f"B{column}"] for column in range(8))
    offsets = token_layout(a_words, chosen_a)
    marked_tokens = tuple(offsets[row] for row in range(8))
    terminal_of = {
        token: 92 + index for index, token in enumerate(marked_tokens)
    }
    graph_edges = []

    # c-connections, including the eight marked subdivisions.
    for token in range(46):
        if token in terminal_of:
            terminal = terminal_of[token]
            graph_edges.append((2 * token, terminal, frozenset()))
            graph_edges.append((terminal, 2 * token + 1, frozenset()))
        else:
            graph_edges.append((2 * token, 2 * token + 1, frozenset()))

    # A-edges are fixed by the canonical A-position slots.
    for row in range(8):
        length = len(a_words[row][chosen_a[row]])
        for position in range(length):
            token = offsets[row] + position
            following = offsets[row] + (position + 1) % length
            graph_edges.append(
                (2 * token + 1, 2 * following, frozenset())
            )

    # Resolve every B position to one A token through its cell option.
    rotations = []
    twists = {}
    sources = {}
    for column in range(8):
        b_word = b_words[column][chosen_b[column]]
        rotation = [None] * len(b_word)
        for row in range(8):
            if matrix[row][column] == 0:
                continue
            variable = f"C{row}_{column}"
            option = cell_domains[row, column][values[variable]]
            a_index, b_index, mapping, orientation = option
            assert a_index == chosen_a[row]
            assert b_index == chosen_b[column]
            a_word = a_words[row][a_index]
            positions_a = tuple(
                position
                for position, label in enumerate(a_word)
                if label == column
            )
            positions_b = tuple(
                position
                for position, label in enumerate(b_word)
                if label == row
            )
            for local_b, b_position in enumerate(positions_b):
                local_a = mapping[local_b]
                token = offsets[row] + positions_a[local_a]
                rotation[b_position] = token
                twists[token] = orientation >> local_a & 1
                sources[token] = variable
        assert all(token is not None for token in rotation)
        rotations.append(tuple(rotation))

    assert len(twists) == 46 and len(sources) == 46
    for rotation in rotations:
        for position, token in enumerate(rotation):
            following = rotation[(position + 1) % len(rotation)]
            provenance = frozenset((sources[token], sources[following]))
            graph_edges.append(
                (
                    2 * token + (1 - twists[token]),
                    2 * following + twists[following],
                    provenance,
                )
            )

    if pairing_index is not None:
        for left, right in PAIRINGS[pairing_index]:
            graph_edges.append(
                (92 + left, 92 + right, frozenset(("P",)))
            )
        assert len(graph_edges) == 150
    else:
        assert len(graph_edges) == 146
    return graph_edges, rotations, twists, marked_tokens


def defects(graph_edges):
    """Return variable sets for parallel edges and all circuits below ten."""
    adjacency = [[] for _ in range(100)]
    pairs = {}
    for edge_id, (left, right, provenance) in enumerate(graph_edges):
        pair = tuple(sorted((left, right)))
        pairs.setdefault(pair, []).append(edge_id)
        adjacency[left].append((right, edge_id))
        adjacency[right].append((left, edge_id))

    found = set()
    for edge_ids in pairs.values():
        if len(edge_ids) > 1:
            provenance = frozenset().union(
                *(graph_edges[edge_id][2] for edge_id in edge_ids)
            )
            assert provenance
            found.add(provenance)

    used = [False] * 100
    path_vertices = []
    path_edges = []
    for root in range(100):
        path_vertices[:] = [root]
        path_edges.clear()
        used[root] = True

        def visit(current):
            if len(path_vertices) >= 10:
                return
            for following, edge_id in adjacency[current]:
                if following == root:
                    length = len(path_vertices)
                    if length >= 3 and path_vertices[1] < path_vertices[-1]:
                        provenance = frozenset().union(
                            *(
                                graph_edges[used_edge][2]
                                for used_edge in path_edges + [edge_id]
                            )
                        )
                        assert provenance
                        found.add(provenance)
                    continue
                if (
                    following <= root
                    or used[following]
                    or len(path_vertices) >= 9
                ):
                    continue
                used[following] = True
                path_vertices.append(following)
                path_edges.append(edge_id)
                visit(following)
                path_edges.pop()
                path_vertices.pop()
                used[following] = False

        visit(root)
        used[root] = False
    return found


def defects_fast(graph_edges):
    """Return one shortest-cycle no-good per edge via bounded BFS.

    This is logically equivalent for lazy refinement: the returned set is
    empty exactly when the graph is simple and has girth at least ten.  It
    need not enumerate every short circuit of the current model.
    """
    adjacency = [[] for _ in range(100)]
    pairs = {}
    for edge_id, (left, right, provenance) in enumerate(graph_edges):
        pair = tuple(sorted((left, right)))
        pairs.setdefault(pair, []).append(edge_id)
        adjacency[left].append((right, edge_id))
        adjacency[right].append((left, edge_id))

    found = set()
    for edge_ids in pairs.values():
        if len(edge_ids) > 1:
            provenance = frozenset().union(
                *(graph_edges[edge_id][2] for edge_id in edge_ids)
            )
            assert provenance
            found.add(provenance)

    for removed, (source, target, removed_source) in enumerate(graph_edges):
        distance = [-1] * 100
        parent_vertex = [-1] * 100
        parent_edge = [-1] * 100
        distance[source] = 0
        queue = [source]
        for vertex in queue:
            if distance[vertex] >= 8 or distance[target] >= 0:
                break
            for following, edge_id in adjacency[vertex]:
                if edge_id == removed or distance[following] >= 0:
                    continue
                distance[following] = distance[vertex] + 1
                parent_vertex[following] = vertex
                parent_edge[following] = edge_id
                queue.append(following)
        if distance[target] < 0 or distance[target] + 1 >= 10:
            continue
        provenance = set(removed_source)
        current = target
        while current != source:
            provenance.update(graph_edges[parent_edge[current]][2])
            current = parent_vertex[current]
        assert provenance
        found.add(frozenset(provenance))
    return found


VALUE_RE = re.compile(r"\(([ABC][0-9_]+) (-?[0-9]+)\)")


def read_status(process):
    line = process.stdout.readline()
    if not line:
        raise RuntimeError("Z3 terminated unexpectedly")
    return line.strip()


def read_values(process, expected):
    chunks = []
    depth = 0
    started = False
    while True:
        line = process.stdout.readline()
        if not line:
            raise RuntimeError("Z3 terminated while returning values")
        chunks.append(line)
        depth += line.count("(") - line.count(")")
        started = started or "(" in line
        if started and depth == 0:
            break
    values = {
        name: int(value) for name, value in VALUE_RE.findall("".join(chunks))
    }
    if len(values) != expected:
        raise RuntimeError(f"could not parse values: {''.join(chunks)}")
    return values


def realization_record(
    profile_index,
    record,
    a_words,
    b_words,
    cell_domains,
    values,
    pairing_index,
):
    graph_edges, rotations, twists, marked = chosen_graph(
        tuple(tuple(row) for row in record["matrix"]),
        a_words,
        b_words,
        cell_domains,
        values,
        pairing_index,
    )
    return {
        "schema": "order100-global-word-gluing-realization-v1",
        "scope_warning": (
            "Concrete girth-ten rotation realization of one fixed incidence "
            "matrix; universal mark separation and five-CDC are not asserted."
        ),
        "profile_index": profile_index,
        "x": record["x"],
        "y": record["y"],
        "matrix": record["matrix"],
        "choices": values,
        "pairing_index": pairing_index,
        "terminal_pairing": PAIRINGS[pairing_index],
        "a_words": [
            a_words[row][values[f"A{row}"]] for row in range(8)
        ],
        "b_words": [
            b_words[column][values[f"B{column}"]] for column in range(8)
        ],
        "b_rotations": rotations,
        "twists": twists,
        "marked_tokens": marked,
        "graph_order": 100,
        "graph_edges": [
            {"u": left, "v": right}
            for left, right, _provenance in graph_edges
        ],
    }


def solve(profile_index, max_models, seed, output):
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert artifact["schema"] == "order100-exact-row-star-relaxation-v1"
    record = artifact["survivors"][profile_index]
    x, y, matrix, a_words, b_words = word_domains(record)
    cell_domains = build_cell_domains(
        x, y, matrix, a_words, b_words
    )

    process = subprocess.Popen(
        ["z3", "-in", "-smt2"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    assert process.stdin is not None and process.stdout is not None
    variables = [f"A{row}" for row in range(8)]
    variables += [f"B{column}" for column in range(8)]
    variables += [
        f"C{row}_{column}" for row, column in sorted(cell_domains)
    ]
    process.stdin.write(f"(set-option :random-seed {seed})\n")
    for row in range(8):
        process.stdin.write(f"(declare-const A{row} Int)\n")
        process.stdin.write(
            f"(assert (and (<= 0 A{row}) "
            f"(< A{row} {len(a_words[row])})))\n"
        )
    for column in range(8):
        process.stdin.write(f"(declare-const B{column} Int)\n")
        process.stdin.write(
            f"(assert (and (<= 0 B{column}) "
            f"(< B{column} {len(b_words[column])})))\n"
        )
    for (row, column), domain in sorted(cell_domains.items()):
        variable = f"C{row}_{column}"
        process.stdin.write(f"(declare-const {variable} Int)\n")
        process.stdin.write(
            f"(assert (and (<= 0 {variable}) "
            f"(< {variable} {len(domain)})))\n"
        )
        for option_index, (a_index, b_index, _mapping, _orientation) in enumerate(
            domain
        ):
            process.stdin.write(
                f"(assert (=> (= {variable} {option_index}) "
                f"(and (= A{row} {a_index}) (= B{column} {b_index}))))\n"
            )
    process.stdin.flush()

    clauses = 0
    seen_nogoods = set()
    core_pairing_failures = 0
    for model_number in range(1, max_models + 1):
        process.stdin.write("(check-sat)\n")
        process.stdin.flush()
        status = read_status(process)
        if status == "unsat":
            result = {
                "status": "UNSAT",
                "profile_index": profile_index,
                "models_checked": model_number - 1,
                "clauses": clauses,
                "core_pairing_failures": core_pairing_failures,
                "certificate_warning": "No proof certificate was requested.",
                "word_domain_sizes": {
                    **{f"A{row}": len(a_words[row]) for row in range(8)},
                    **{
                        f"B{column}": len(b_words[column])
                        for column in range(8)
                    },
                },
                "cell_domain_sizes": {
                    f"{row},{column}": len(domain)
                    for (row, column), domain in cell_domains.items()
                },
            }
            print(json.dumps(result, indent=2))
            return 20
        if status != "sat":
            raise RuntimeError(f"unexpected Z3 status: {status}")
        process.stdin.write(f"(get-value ({' '.join(variables)}))\n")
        process.stdin.flush()
        values = read_values(process, len(variables))
        graph_edges, _rotations, _twists, _marked = chosen_graph(
            matrix, a_words, b_words, cell_domains, values
        )
        bad = defects(graph_edges)
        if not bad:
            for pairing_index in range(len(PAIRINGS)):
                full_edges, _r, _t, _m = chosen_graph(
                    matrix,
                    a_words,
                    b_words,
                    cell_domains,
                    values,
                    pairing_index,
                )
                if defects(full_edges):
                    continue
                result = realization_record(
                    profile_index,
                    record,
                    a_words,
                    b_words,
                    cell_domains,
                    values,
                    pairing_index,
                )
                rendered = json.dumps(result, indent=2)
                if output:
                    output.write_text(rendered + "\n", encoding="utf-8")
                print(rendered)
                return 0

            core_pairing_failures += 1
            provenance = tuple(
                variable for variable in variables if variable.startswith("C")
            )
            bad = {frozenset(provenance)}

        new_clauses = 0
        for provenance in sorted(bad, key=lambda item: (len(item), sorted(item))):
            chosen = tuple(
                sorted((variable, values[variable]) for variable in provenance)
            )
            if chosen in seen_nogoods:
                continue
            seen_nogoods.add(chosen)
            literals = " ".join(
                f"(not (= {variable} {value}))"
                for variable, value in chosen
            )
            process.stdin.write(f"(assert (or {literals}))\n")
            clauses += 1
            new_clauses += 1
        assert new_clauses > 0
        process.stdin.flush()
        if model_number == 1 or model_number % 100 == 0:
            print(
                f"models={model_number} new_clauses={new_clauses} "
                f"clauses={clauses} core_pairing_failures="
                f"{core_pairing_failures}",
                file=sys.stderr,
                flush=True,
            )

    print(
        f"UNKNOWN iteration limit models={max_models} clauses={clauses}",
        file=sys.stderr,
    )
    return 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=int, choices=range(3), required=True)
    parser.add_argument("--max-models", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=100_100)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    raise SystemExit(
        solve(
            args.profile,
            args.max_models,
            args.seed,
            args.output,
        )
    )


if __name__ == "__main__":
    main()
