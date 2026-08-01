#!/usr/bin/env python3
"""Deterministic canonical enumeration for small simple cubic graphs.

The generator quotient (one graph per isomorphism class) is delegated to
nauty ``geng``.  Everything after graph6 production is checked independently
with the Python standard library before the frozen verifier A is invoked.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import platform
import shlex
import subprocess
import sys
import time
from typing import Dict, Iterator, List, Optional, Sequence, Tuple


EXPECTED_GENG_VERSION = "Nauty&Traces version 2.9301 (32 bits)"
GRAPH_FORMAT = "five-cdc-multigraph-v1"
COORDINATES = 5
SAT_RETURN_CODE = 10
UNSAT_RETURN_CODE = 20


class SearchError(RuntimeError):
    """The search cannot continue without losing an exactness guarantee."""


@dataclass(frozen=True)
class SimpleGraph:
    vertices: int
    edges: Tuple[Tuple[int, int], ...]

    def adjacency(self) -> Tuple[Tuple[int, ...], ...]:
        result: List[List[int]] = [[] for _ in range(self.vertices)]
        for u, v in self.edges:
            result[u].append(v)
            result[v].append(u)
        return tuple(tuple(sorted(row)) for row in result)

    def witness_object(self) -> dict:
        return {
            "format": GRAPH_FORMAT,
            "vertices": self.vertices,
            "edges": [
                {"id": edge_id, "u": u, "v": v}
                for edge_id, (u, v) in enumerate(self.edges)
            ],
        }

    def witness_bytes(self) -> bytes:
        return (
            json.dumps(
                self.witness_object(),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
            )
            + "\n"
        ).encode("ascii")


@dataclass(frozen=True)
class EdgeColoringResult:
    colorable: bool
    colors: Optional[Tuple[int, ...]]
    search_nodes: int


@dataclass(frozen=True)
class OddnessResult:
    oddness: Optional[int]
    perfect_matching: Optional[Tuple[int, ...]]
    perfect_matchings_examined: int
    exact: bool


def _decode_graph6_order(text: str) -> Tuple[int, int]:
    """Return ``(n, data_offset)`` for a graph6 payload."""

    if not text:
        raise ValueError("empty graph6 record")
    values = [ord(char) - 63 for char in text]
    if any(value < 0 or value > 63 for value in values):
        raise ValueError("graph6 characters must have ASCII codes 63..126")
    if values[0] != 63:
        return values[0], 1
    if len(values) < 4:
        raise ValueError("truncated medium graph6 order")
    if values[1] != 63:
        n = (values[1] << 12) | (values[2] << 6) | values[3]
        if n < 63:
            raise ValueError("noncanonical medium graph6 order")
        return n, 4
    if len(values) < 8:
        raise ValueError("truncated large graph6 order")
    n = 0
    for value in values[2:8]:
        n = (n << 6) | value
    if n < 258048:
        raise ValueError("noncanonical large graph6 order")
    return n, 8


def parse_graph6(record: str) -> SimpleGraph:
    """Independently parse one canonical graph6 line.

    graph6 stores the strict upper triangle in column-major order:
    ``(0,1),(0,2),(1,2),(0,3),...``.  This parser does not use nauty code.
    """

    if record.startswith(">>graph6<<"):
        record = record[len(">>graph6<<") :]
    if "\n" in record or "\r" in record:
        record = record.rstrip("\r\n")
        if "\n" in record or "\r" in record:
            raise ValueError("graph6 parser accepts exactly one record")
    n, offset = _decode_graph6_order(record)
    bit_count = n * (n - 1) // 2
    data_count = (bit_count + 5) // 6
    if len(record) != offset + data_count:
        raise ValueError(
            "graph6 length mismatch: expected {}, got {}".format(
                offset + data_count, len(record)
            )
        )
    chunks = [ord(char) - 63 for char in record[offset:]]
    bits = [
        (chunk >> shift) & 1
        for chunk in chunks
        for shift in range(5, -1, -1)
    ]
    if any(bits[bit_count:]):
        raise ValueError("nonzero graph6 padding bits")
    edges = []
    cursor = 0
    for v in range(1, n):
        for u in range(v):
            if bits[cursor]:
                edges.append((u, v))
            cursor += 1
    return SimpleGraph(n, tuple(sorted(edges)))


def validate_simple_cubic(graph: SimpleGraph) -> dict:
    """Check simplicity, cubicity, connectivity, and bridgelessness."""

    n = graph.vertices
    if n < 0:
        raise ValueError("negative vertex count")
    if tuple(sorted(graph.edges)) != graph.edges:
        raise ValueError("edges are not in canonical lexicographic order")
    seen = set()
    degree = [0] * n
    for edge in graph.edges:
        if len(edge) != 2:
            raise ValueError("malformed edge")
        u, v = edge
        if not (0 <= u < v < n):
            raise ValueError("simple edges must satisfy 0 <= u < v < n")
        if edge in seen:
            raise ValueError("parallel edge in simple graph")
        seen.add(edge)
        degree[u] += 1
        degree[v] += 1
    cubic = bool(n) and all(value == 3 for value in degree)
    adjacency = graph.adjacency()

    visited = set()
    if n:
        stack = [0]
        visited.add(0)
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if other not in visited:
                    visited.add(other)
                    stack.append(other)
    connected = n > 0 and len(visited) == n

    discovery = [-1] * n
    low = [-1] * n
    tick = 0
    bridges: List[int] = []
    incident: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    for edge_id, (u, v) in enumerate(graph.edges):
        incident[u].append((v, edge_id))
        incident[v].append((u, edge_id))
    for row in incident:
        row.sort()

    def visit(vertex: int, parent_edge: int) -> None:
        nonlocal tick
        discovery[vertex] = low[vertex] = tick
        tick += 1
        for other, edge_id in incident[vertex]:
            if edge_id == parent_edge:
                continue
            if discovery[other] < 0:
                visit(other, edge_id)
                low[vertex] = min(low[vertex], low[other])
                if low[other] > discovery[vertex]:
                    bridges.append(edge_id)
            else:
                low[vertex] = min(low[vertex], discovery[other])

    for root in range(n):
        if discovery[root] < 0:
            visit(root, -1)

    return {
        "simple": True,
        "cubic": cubic,
        "degree_sequence": degree,
        "connected": connected,
        "bridgeless": not bridges,
        "bridge_ids": sorted(bridges),
    }


def girth(graph: SimpleGraph) -> Optional[int]:
    """Return the exact girth, or ``None`` for a forest."""

    adjacency: List[List[Tuple[int, int]]] = [
        [] for _ in range(graph.vertices)
    ]
    for edge_id, (u, v) in enumerate(graph.edges):
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))
    best: Optional[int] = None
    for excluded, (source, target) in enumerate(graph.edges):
        distance = [-1] * graph.vertices
        distance[source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            if best is not None and distance[vertex] + 1 >= best:
                continue
            for other, edge_id in adjacency[vertex]:
                if edge_id == excluded or distance[other] >= 0:
                    continue
                distance[other] = distance[vertex] + 1
                if other == target:
                    candidate = distance[other] + 1
                    best = candidate if best is None else min(best, candidate)
                    queue.clear()
                    break
                queue.append(other)
    return best


def exact_three_edge_coloring(graph: SimpleGraph) -> EdgeColoringResult:
    """Decide 3-edge-colorability by exhaustive constraint propagation."""

    m = len(graph.edges)
    incident: List[List[int]] = [[] for _ in range(graph.vertices)]
    for edge_id, (u, v) in enumerate(graph.edges):
        incident[u].append(edge_id)
        incident[v].append(edge_id)
    colors = [-1] * m
    used = [0] * graph.vertices
    nodes = 0

    # Color-name symmetry: in every cubic proper coloring, the three edges at
    # vertex 0 have three distinct colors.
    if graph.vertices and len(incident[0]) == 3:
        for color, edge_id in enumerate(sorted(incident[0])):
            colors[edge_id] = color
            u, v = graph.edges[edge_id]
            used[u] |= 1 << color
            used[v] |= 1 << color
        if any(
            bin(used[vertex]).count("1")
            != sum(colors[edge_id] >= 0 for edge_id in incident[vertex])
            for vertex in range(graph.vertices)
        ):
            return EdgeColoringResult(False, None, 1)

    def search(colored: int) -> bool:
        nonlocal nodes
        nodes += 1
        if colored == m:
            return True
        choice = -1
        choice_options: Tuple[int, ...] = ()
        for edge_id, (u, v) in enumerate(graph.edges):
            if colors[edge_id] >= 0:
                continue
            options = tuple(
                color
                for color in range(3)
                if not (used[u] & (1 << color))
                and not (used[v] & (1 << color))
            )
            if not options:
                return False
            if choice < 0 or len(options) < len(choice_options):
                choice = edge_id
                choice_options = options
        u, v = graph.edges[choice]
        for color in choice_options:
            bit = 1 << color
            colors[choice] = color
            used[u] |= bit
            used[v] |= bit
            if search(colored + 1):
                return True
            used[u] ^= bit
            used[v] ^= bit
            colors[choice] = -1
        return False

    initially_colored = sum(color >= 0 for color in colors)
    result = search(initially_colored)
    return EdgeColoringResult(
        result, tuple(colors) if result else None, nodes
    )


def _odd_cycles_outside_matching(
    graph: SimpleGraph, matching: Sequence[int]
) -> int:
    matching_set = set(matching)
    adjacency: List[List[int]] = [[] for _ in range(graph.vertices)]
    for edge_id, (u, v) in enumerate(graph.edges):
        if edge_id in matching_set:
            continue
        adjacency[u].append(v)
        adjacency[v].append(u)
    if any(len(row) != 2 for row in adjacency):
        raise AssertionError("complement of perfect matching is not a 2-factor")
    visited = set()
    odd = 0
    for root in range(graph.vertices):
        if root in visited:
            continue
        stack = [root]
        visited.add(root)
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for other in adjacency[vertex]:
                if other not in visited:
                    visited.add(other)
                    stack.append(other)
        odd += size % 2
    return odd


def exact_oddness(
    graph: SimpleGraph,
    coloring: EdgeColoringResult,
    maximum_vertices: int,
) -> OddnessResult:
    """Minimize odd circuits in a spanning 2-factor.

    The search enumerates every perfect matching exactly once.  It is only
    attempted at or below ``maximum_vertices``.  A proper 3-edge-coloring
    supplies an immediate exact oddness-zero certificate.
    """

    if coloring.colorable:
        assert coloring.colors is not None
        matching = tuple(
            edge_id
            for edge_id, color in enumerate(coloring.colors)
            if color == 0
        )
        return OddnessResult(0, matching, 1, True)
    if graph.vertices > maximum_vertices:
        return OddnessResult(None, None, 0, False)

    incident: List[List[int]] = [[] for _ in range(graph.vertices)]
    for edge_id, (u, v) in enumerate(graph.edges):
        incident[u].append(edge_id)
        incident[v].append(edge_id)
    for row in incident:
        row.sort()
    matched = [False] * graph.vertices
    chosen: List[int] = []
    best: Optional[int] = None
    best_matching: Optional[Tuple[int, ...]] = None
    examined = 0

    def enumerate_matchings() -> None:
        nonlocal best, best_matching, examined
        try:
            vertex = next(
                index for index, value in enumerate(matched) if not value
            )
        except StopIteration:
            examined += 1
            value = _odd_cycles_outside_matching(graph, chosen)
            if best is None or value < best:
                best = value
                best_matching = tuple(sorted(chosen))
            return
        for edge_id in incident[vertex]:
            u, v = graph.edges[edge_id]
            other = v if u == vertex else u
            if matched[other]:
                continue
            matched[vertex] = matched[other] = True
            chosen.append(edge_id)
            enumerate_matchings()
            chosen.pop()
            matched[vertex] = matched[other] = False

    enumerate_matchings()
    return OddnessResult(best, best_matching, examined, True)


def s5_normalization_units(graph: SimpleGraph) -> Tuple[int, ...]:
    """Force the first cubic vertex's ordered labels to 01, 02, 12.

    Coordinate strings in documentation are zero-based.  DIMACS variables use
    verifier A's one-based coordinates, hence pairs (1,2), (1,3), (2,3).
    """

    if not graph.vertices:
        raise ValueError("normalization requires a nonempty graph")
    incident = [
        edge_id
        for edge_id, edge in enumerate(graph.edges)
        if 0 in edge
    ]
    if len(incident) != 3:
        raise ValueError("normalization requires cubic vertex 0")
    pairs = ((1, 2), (1, 3), (2, 3))
    units = []
    for edge_id, pair in zip(sorted(incident), pairs):
        for coordinate in range(1, 6):
            variable = 5 * edge_id + coordinate
            units.append(variable if coordinate in pair else -variable)
    return tuple(units)


def augment_dimacs_with_units(text: str, units: Sequence[int]) -> str:
    """Add unit clauses without changing the variable set."""

    lines = text.splitlines()
    header_index = next(
        (index for index, line in enumerate(lines) if line.startswith("p cnf ")),
        None,
    )
    if header_index is None:
        raise ValueError("DIMACS header not found")
    fields = lines[header_index].split()
    if len(fields) != 4:
        raise ValueError("malformed DIMACS header")
    variables, constraints = int(fields[2]), int(fields[3])
    if any(abs(literal) > variables or literal == 0 for literal in units):
        raise ValueError("unit outside DIMACS variable range")
    lines[header_index] = "p cnf {} {}".format(
        variables, constraints + len(units)
    )
    insertion = ["{} 0".format(literal) for literal in units]
    lines[header_index + 1 : header_index + 1] = insertion
    return "\n".join(lines) + "\n"


def _distance_profiles(graph: SimpleGraph) -> Tuple[Tuple[int, ...], ...]:
    adjacency = graph.adjacency()
    profiles = []
    for source in range(graph.vertices):
        distances = [-1] * graph.vertices
        distances[source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for other in adjacency[vertex]:
                if distances[other] < 0:
                    distances[other] = distances[vertex] + 1
                    queue.append(other)
        profiles.append(tuple(sorted(distances)))
    return tuple(profiles)


def enumerate_automorphisms(
    graph: SimpleGraph, maximum: int = 1_000_000
) -> Tuple[Tuple[int, ...], ...]:
    """Exhaustively enumerate graph automorphisms by exact backtracking."""

    n = graph.vertices
    adjacency = tuple(
        sum(1 << other for other in row) for row in graph.adjacency()
    )
    profiles = _distance_profiles(graph)
    mapping = [-1] * n
    used = [False] * n
    result: List[Tuple[int, ...]] = []

    def compatible(source: int, target: int) -> bool:
        if profiles[source] != profiles[target]:
            return False
        for earlier_source, earlier_target in enumerate(mapping):
            if earlier_target < 0:
                continue
            source_adjacent = bool(adjacency[source] & (1 << earlier_source))
            target_adjacent = bool(adjacency[target] & (1 << earlier_target))
            if source_adjacent != target_adjacent:
                return False
        return True

    def search() -> None:
        if len(result) > maximum:
            raise SearchError(
                "automorphism count exceeded configured maximum {}".format(
                    maximum
                )
            )
        unmapped = [vertex for vertex in range(n) if mapping[vertex] < 0]
        if not unmapped:
            result.append(tuple(mapping))
            return
        source = min(
            unmapped,
            key=lambda vertex: (
                -sum(
                    mapping[other] >= 0
                    for other in range(n)
                    if adjacency[vertex] & (1 << other)
                ),
                vertex,
            ),
        )
        for target in range(n):
            if used[target] or not compatible(source, target):
                continue
            mapping[source] = target
            used[target] = True
            search()
            used[target] = False
            mapping[source] = -1

    search()
    return tuple(result)


def _permute_label(label: Tuple[int, int], permutation: Sequence[int]) -> Tuple[int, int]:
    return tuple(sorted((permutation[label[0]], permutation[label[1]])))  # type: ignore[return-value]


def canonicalize_cover(
    graph: SimpleGraph,
    labels: Sequence[Tuple[int, int]],
    maximum_vertices: int,
    maximum_automorphisms: int = 1_000_000,
) -> dict:
    """Canonicalize a cover under ``Aut(G) x S5`` when the graph is small."""

    if len(labels) != len(graph.edges):
        raise ValueError("one label is required per edge")
    if graph.vertices > maximum_vertices:
        return {
            "canonicalized": False,
            "reason": "vertex threshold exceeded",
            "labels": ["{}{}".format(*label) for label in labels],
        }
    automorphisms = enumerate_automorphisms(graph, maximum_automorphisms)
    edge_index = {edge: edge_id for edge_id, edge in enumerate(graph.edges)}
    best: Optional[Tuple[Tuple[int, int], ...]] = None
    for automorphism in automorphisms:
        transported: List[Optional[Tuple[int, int]]] = [None] * len(labels)
        for edge_id, (u, v) in enumerate(graph.edges):
            image = tuple(sorted((automorphism[u], automorphism[v])))
            transported[edge_index[image]] = labels[edge_id]
        if any(label is None for label in transported):
            raise AssertionError("automorphism did not permute edges")
        typed = tuple(transported)  # type: ignore[arg-type]
        for coordinate_permutation in permutations(range(5)):
            candidate = tuple(
                _permute_label(label, coordinate_permutation)
                for label in typed
            )
            if best is None or candidate < best:
                best = candidate
    assert best is not None
    canonical_strings = ["{}{}".format(*label) for label in best]
    digest = sha256(
        (" ".join(canonical_strings) + "\n").encode("ascii")
    ).hexdigest()
    return {
        "canonicalized": True,
        "group_action": "Aut(G) x S5",
        "automorphisms_enumerated": len(automorphisms),
        "coordinate_permutations_enumerated": 120,
        "labels": canonical_strings,
        "sha256": digest,
    }


def labels_from_model(text: str, edge_count: int) -> Tuple[Tuple[int, int], ...]:
    assignment: Dict[int, bool] = {}
    maximum = 5 * edge_count
    for raw_line in text.splitlines():
        tokens = raw_line.strip().split()
        if not tokens or tokens[0] in {"c", "s"}:
            continue
        if tokens[0] == "v":
            tokens = tokens[1:]
        for token in tokens:
            literal = int(token)
            if literal == 0:
                continue
            variable = abs(literal)
            if variable <= maximum:
                value = literal > 0
                if variable in assignment and assignment[variable] != value:
                    raise SearchError("contradictory model literal")
                assignment[variable] = value
    missing = [
        variable for variable in range(1, maximum + 1)
        if variable not in assignment
    ]
    if missing:
        raise SearchError("SAT solver omitted base model variables")
    labels = []
    for edge_id in range(edge_count):
        label = tuple(
            coordinate - 1
            for coordinate in range(1, 6)
            if assignment[5 * edge_id + coordinate]
        )
        if len(label) != 2:
            raise SearchError("model violates exact-two while decoding")
        labels.append(label)
    return tuple(labels)  # type: ignore[return-value]


def _run(
    command: Sequence[str],
    cwd: Path,
    allowed_returncodes: Sequence[int] = (0,),
) -> subprocess.CompletedProcess:
    completed = subprocess.run(
        list(command),
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="strict",
        check=False,
    )
    if completed.returncode not in allowed_returncodes:
        raise SearchError(
            "command failed ({}): {}\nstdout:\n{}\nstderr:\n{}".format(
                completed.returncode,
                shlex.join(command),
                completed.stdout,
                completed.stderr,
            )
        )
    return completed


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _tool_metadata(path: str, version_args: Sequence[str]) -> dict:
    resolved = Path(path).resolve()
    completed = _run([str(resolved), *version_args], Path.cwd())
    version = (completed.stdout + completed.stderr).strip()
    return {
        "path": str(resolved),
        "version_command": shlex.join([str(resolved), *version_args]),
        "version": version,
        "sha256": _sha256_file(resolved),
    }


def iter_geng(
    executable: str, n: int, repo_root: Path
) -> Iterator[Tuple[int, str, SimpleGraph]]:
    if n <= 0 or n % 2:
        raise ValueError("cubic graph order must be positive and even")
    edge_count = 3 * n // 2
    command = [
        executable,
        "-cq",
        "-d3",
        "-D3",
        str(n),
        "{}:{}".format(edge_count, edge_count),
    ]
    process = subprocess.Popen(
        command,
        cwd=str(repo_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="ascii",
        errors="strict",
    )
    assert process.stdout is not None
    for index, raw_line in enumerate(process.stdout, 1):
        graph6 = raw_line.rstrip("\r\n")
        yield index, graph6, parse_graph6(graph6)
    assert process.stderr is not None
    stderr = process.stderr.read()
    returncode = process.wait()
    if returncode:
        raise SearchError(
            "geng failed ({}): {}\n{}".format(
                returncode, shlex.join(command), stderr
            )
        )
    if stderr:
        raise SearchError("quiet geng unexpectedly wrote stderr: " + stderr)


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def _solver_run(
    name: str,
    executable: str,
    instance: Path,
    graph_path: Path,
    graph: SimpleGraph,
    artifact_dir: Path,
    repo_root: Path,
    python_executable: str,
    cover_canon_max_vertices: int,
) -> dict:
    if name == "cms":
        command = [
            executable,
            "--verb",
            "0",
            "--threads",
            "1",
            "--random",
            "0",
            "--printsol",
            "1",
            str(instance),
        ]
    elif name == "cadical":
        command = [
            executable,
            "-q",
            "--no-colors",
            "--seed=0",
            str(instance),
        ]
    else:
        raise ValueError("unknown solver")
    started = time.monotonic()
    completed = _run(
        command, repo_root, (SAT_RETURN_CODE, UNSAT_RETURN_CODE)
    )
    duration = time.monotonic() - started
    model_path = artifact_dir / "{}.model".format(name)
    model_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path = artifact_dir / "{}.stderr".format(name)
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    status = "SAT" if completed.returncode == SAT_RETURN_CODE else "UNSAT"
    result = {
        "name": name,
        "command": shlex.join(command),
        "returncode": completed.returncode,
        "status": status,
        "duration_seconds": duration,
        "instance_sha256": _sha256_file(instance),
        "model_sha256": _sha256_file(model_path),
        "stderr_sha256": _sha256_file(stderr_path),
        "certificate_produced": False,
    }
    if status == "SAT":
        verifier_command = [
            python_executable,
            "-m",
            "verifier_a",
            "check-model",
            str(graph_path),
            str(model_path),
        ]
        verified = _run(verifier_command, repo_root)
        verifier_object = json.loads(verified.stdout)
        verifier_path = artifact_dir / "{}.verifier-a.json".format(name)
        _write_json(verifier_path, verifier_object)
        if verifier_object.get("valid") is not True:
            raise SearchError("verifier A rejected {} SAT model".format(name))
        labels = labels_from_model(completed.stdout, len(graph.edges))
        cover = canonicalize_cover(
            graph, labels, cover_canon_max_vertices
        )
        cover_path = artifact_dir / "{}.cover.json".format(name)
        _write_json(cover_path, cover)
        result.update(
            {
                "semantic_verifier": "verifier_a 1.0.0 check-model",
                "semantic_verifier_command": shlex.join(verifier_command),
                "semantic_verified": True,
                "verifier_output_sha256": _sha256_file(verifier_path),
                "cover_artifact": cover_path.name,
                "cover": cover,
            }
        )
    else:
        result.update(
            {
                "semantic_verified": None,
                "warning": (
                    "solver-only UNSAT has no independently checked proof "
                    "and is not a counterexample"
                ),
            }
        )
    return result


def _git_metadata(repo_root: Path) -> dict:
    revision_run = _run(
        ["git", "rev-parse", "--verify", "HEAD"], repo_root, (0, 128)
    )
    revision = (
        revision_run.stdout.strip() if revision_run.returncode == 0 else None
    )
    status = _run(
        ["git", "status", "--porcelain=v1"], repo_root
    ).stdout
    return {
        "revision": revision,
        "unborn_head": revision is None,
        "dirty": bool(status),
        "status": status,
    }


def _verifier_metadata(repo_root: Path) -> dict:
    sums_path = repo_root / "verifier_a" / "SHA256SUMS"
    entries = {}
    for line in sums_path.read_text(encoding="ascii").splitlines():
        expected, relative = line.split(None, 1)
        relative = relative.strip()
        actual = _sha256_file(repo_root / relative)
        if actual != expected:
            raise SearchError(
                "frozen verifier checksum mismatch for {}".format(relative)
            )
        entries[relative] = expected
    return {
        "version": json.loads(
            (repo_root / "verifier_a" / "VERSION.json").read_text(
                encoding="utf-8"
            )
        ),
        "sha256sums_sha256": _sha256_file(sums_path),
        "files": entries,
        "all_hashes_verified": True,
    }


def _write_checksums(root: Path) -> None:
    paths = sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    )
    lines = [
        "{}  {}".format(_sha256_file(path), path.relative_to(root))
        for path in paths
    ]
    (root / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="ascii")


def run_enumeration(args: argparse.Namespace) -> int:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[2]
    output = Path(args.output).resolve()
    if output.exists():
        raise SearchError("refusing to overwrite existing output: {}".format(output))
    output.mkdir(parents=True)
    graph_root = output / "graphs"
    graph_root.mkdir()

    geng_metadata = _tool_metadata(args.geng, ("--version",))
    if geng_metadata["version"] != EXPECTED_GENG_VERSION:
        raise SearchError(
            "required geng {}, got {!r}".format(
                EXPECTED_GENG_VERSION, geng_metadata["version"]
            )
        )
    solver_metadata = {}
    if args.solver in {"cms", "both"}:
        solver_metadata["cms"] = _tool_metadata(
            args.cryptominisat, ("--version",)
        )
    if args.solver in {"cadical", "both"}:
        solver_metadata["cadical"] = _tool_metadata(
            args.cadical, ("--version",)
        )

    start_wall = datetime.now(timezone.utc)
    start_mono = time.monotonic()
    metadata = {
        "format": "five-cdc-canonical-search-run-v1",
        "status": "RUNNING",
        "started_utc": start_wall.isoformat(),
        "host": {
            "platform": platform.platform(),
            "python": sys.version,
            "executable": sys.executable,
        },
        "git": _git_metadata(repo_root),
        "verifier_a": _verifier_metadata(repo_root),
        "tools": {"geng": geng_metadata, **solver_metadata},
        "configuration": {
            "min_n": args.min_n,
            "max_n": args.max_n,
            "solver": args.solver,
            "oddness_max_vertices": args.oddness_max_vertices,
            "cover_canon_max_vertices": args.cover_canon_max_vertices,
            "random_seeds": {"cryptominisat": 0, "cadical": 0},
            "geng_isomorphism_quotient": True,
            "solver_s5_symmetry_breaking": True,
            "minimum_counterexample_filter": {
                "girth_at_least": 10,
                "oddness_at_least": 6,
                "status": (
                    "source-backed imported restriction; see "
                    "docs/current-status.md and docs/reductions.md"
                ),
            },
        },
        "geng_commands": [
            shlex.join(
                [
                    str(Path(args.geng).resolve()),
                    "-cq",
                    "-d3",
                    "-D3",
                    str(n),
                    "{}:{}".format(3 * n // 2, 3 * n // 2),
                ]
            )
            for n in range(args.min_n, args.max_n + 1)
            if n > 0 and n % 2 == 0
        ],
        "invocation": shlex.join([sys.executable, *sys.argv]),
    }
    _write_json(output / "metadata.json", metadata)

    counts = {
        "geng_records": 0,
        "validated": 0,
        "bridgeless": 0,
        "nonbridgeless_rejected": 0,
        "three_edge_colorable": 0,
        "non_three_edge_colorable": 0,
        "cms_sat": 0,
        "cms_unsat_uncertified": 0,
        "cadical_sat": 0,
        "cadical_unsat_uncertified": 0,
        "semantic_models_verified": 0,
        "minimum_counterexample_domain_girth10_oddness6": 0,
    }
    per_order: Dict[str, dict] = {}
    results_path = output / "results.jsonl"
    with results_path.open("w", encoding="utf-8") as results_stream:
        for n in range(args.min_n, args.max_n + 1):
            if n <= 0 or n % 2:
                continue
            order_stats = {
                "geng_records": 0,
                "bridgeless": 0,
                "nonbridgeless_rejected": 0,
                "three_edge_colorable": 0,
                "non_three_edge_colorable": 0,
                "minimum_counterexample_domain_girth10_oddness6": 0,
                "cms_sat": 0,
                "cms_unsat_uncertified": 0,
                "cadical_sat": 0,
                "cadical_unsat_uncertified": 0,
                "semantic_models_verified": 0,
            }
            for index, graph6, graph in iter_geng(args.geng, n, repo_root):
                counts["geng_records"] += 1
                order_stats["geng_records"] += 1
                checks = validate_simple_cubic(graph)
                if not (
                    checks["simple"]
                    and checks["cubic"]
                    and checks["connected"]
                ):
                    raise SearchError(
                        "geng output failed independent domain checks: {}".format(
                            checks
                        )
                    )
                counts["validated"] += 1

                graph_digest = sha256(graph.witness_bytes()).hexdigest()
                artifact_dir = graph_root / (
                    "n{:03d}-g{:06d}-{}".format(n, index, graph_digest[:12])
                )
                artifact_dir.mkdir()
                graph_path = artifact_dir / "graph.json"
                graph_path.write_bytes(graph.witness_bytes())

                graph_check_command = [
                    sys.executable,
                    "-m",
                    "verifier_a",
                    "check-graph",
                    str(graph_path),
                ]
                graph_check = _run(
                    graph_check_command,
                    repo_root,
                    (0, 1),
                )
                graph_check_object = json.loads(graph_check.stdout)
                if bool(graph_check_object.get("bridgeless")) != bool(
                    checks["bridgeless"]
                ):
                    raise SearchError("verifier A disagreed on bridgelessness")
                _write_json(
                    artifact_dir / "verifier-a.graph.json",
                    graph_check_object,
                )
                if not checks["bridgeless"]:
                    counts["nonbridgeless_rejected"] += 1
                    order_stats["nonbridgeless_rejected"] += 1
                    rejected_record = {
                        "order": n,
                        "geng_index": index,
                        "graph6": graph6,
                        "graph_sha256": graph_digest,
                        "artifact_directory": str(
                            artifact_dir.relative_to(output)
                        ),
                        "checks": checks,
                        "verifier_a_check_graph_command": shlex.join(
                            graph_check_command
                        ),
                        "candidate": False,
                        "exclusion": (
                            "graph has a bridge and is outside the conjecture "
                            "premise"
                        ),
                        "solvers": [],
                    }
                    results_stream.write(
                        json.dumps(
                            rejected_record,
                            sort_keys=True,
                            separators=(",", ":"),
                        )
                        + "\n"
                    )
                    results_stream.flush()
                    continue
                counts["bridgeless"] += 1
                order_stats["bridgeless"] += 1

                coloring = exact_three_edge_coloring(graph)
                if coloring.colorable:
                    counts["three_edge_colorable"] += 1
                    order_stats["three_edge_colorable"] += 1
                else:
                    counts["non_three_edge_colorable"] += 1
                    order_stats["non_three_edge_colorable"] += 1
                oddness = exact_oddness(
                    graph, coloring, args.oddness_max_vertices
                )
                graph_girth = girth(graph)
                in_minimum_domain = (
                    graph_girth is not None
                    and graph_girth >= 10
                    and oddness.exact
                    and oddness.oddness is not None
                    and oddness.oddness >= 6
                )
                if in_minimum_domain:
                    counts[
                        "minimum_counterexample_domain_girth10_oddness6"
                    ] += 1
                    order_stats[
                        "minimum_counterexample_domain_girth10_oddness6"
                    ] += 1

                cnf_path = artifact_dir / "base.cnf"
                xor_path = artifact_dir / "base.xor.cnf"
                encode_command = [
                    sys.executable,
                    "-m",
                    "verifier_a",
                    "encode",
                    str(graph_path),
                    "--cnf",
                    str(cnf_path),
                    "--xor",
                    str(xor_path),
                ]
                encode = _run(
                    encode_command,
                    repo_root,
                )
                _write_json(
                    artifact_dir / "verifier-a.encode.json",
                    json.loads(encode.stdout),
                )
                units = s5_normalization_units(graph)
                sym_cnf = artifact_dir / "sym.cnf"
                sym_xor = artifact_dir / "sym.xor.cnf"
                sym_cnf.write_text(
                    augment_dimacs_with_units(
                        cnf_path.read_text(encoding="ascii"), units
                    ),
                    encoding="ascii",
                )
                sym_xor.write_text(
                    augment_dimacs_with_units(
                        xor_path.read_text(encoding="ascii"), units
                    ),
                    encoding="ascii",
                )

                solver_results = []
                if args.solver in {"cms", "both"}:
                    result = _solver_run(
                        "cms",
                        args.cryptominisat,
                        sym_xor,
                        graph_path,
                        graph,
                        artifact_dir,
                        repo_root,
                        sys.executable,
                        args.cover_canon_max_vertices,
                    )
                    solver_results.append(result)
                if args.solver in {"cadical", "both"}:
                    result = _solver_run(
                        "cadical",
                        args.cadical,
                        sym_cnf,
                        graph_path,
                        graph,
                        artifact_dir,
                        repo_root,
                        sys.executable,
                        args.cover_canon_max_vertices,
                    )
                    solver_results.append(result)

                statuses = {item["status"] for item in solver_results}
                if len(statuses) > 1:
                    raise SearchError("CMS and CaDiCaL status disagreement")
                for result in solver_results:
                    key = "{}_{}".format(
                        result["name"],
                        "sat" if result["status"] == "SAT"
                        else "unsat_uncertified",
                    )
                    counts[key] += 1
                    order_stats[key] += 1
                    if result.get("semantic_verified"):
                        counts["semantic_models_verified"] += 1
                        order_stats["semantic_models_verified"] += 1
                record = {
                    "order": n,
                    "geng_index": index,
                    "graph6": graph6,
                    "graph_sha256": graph_digest,
                    "artifact_directory": str(
                        artifact_dir.relative_to(output)
                    ),
                    "checks": checks,
                    "verifier_a_check_graph_command": shlex.join(
                        graph_check_command
                    ),
                    "verifier_a_encode_command": shlex.join(encode_command),
                    "girth": graph_girth,
                    "three_edge_coloring": {
                        "colorable": coloring.colorable,
                        "colors": coloring.colors,
                        "search_nodes": coloring.search_nodes,
                    },
                    "oddness": {
                        "value": oddness.oddness,
                        "perfect_matching": oddness.perfect_matching,
                        "perfect_matchings_examined": (
                            oddness.perfect_matchings_examined
                        ),
                        "exact": oddness.exact,
                    },
                    "minimum_counterexample_domain": {
                        "criteria": "girth >= 10 and exact oddness >= 6",
                        "included": in_minimum_domain,
                        "restriction_status": (
                            "source-backed imported theorem, not proved by "
                            "this computation"
                        ),
                    },
                    "s5_normalization_units": units,
                    "solvers": solver_results,
                }
                results_stream.write(
                    json.dumps(record, sort_keys=True, separators=(",", ":"))
                    + "\n"
                )
                results_stream.flush()
            per_order[str(n)] = order_stats

    finish_wall = datetime.now(timezone.utc)
    summary = {
        "format": "five-cdc-canonical-search-summary-v1",
        "status": "VERIFIED FINITE CASE",
        "scope": {
            "raw_validation_domain": (
                "all connected simple cubic graphs in the stated orders, "
                "generated once per isomorphism class by geng"
            ),
            "minimum_counterexample_domain": (
                "the source-backed imported restrictions girth >= 10 and "
                "oddness >= 6; this run searched no graph in that domain"
            ),
            "interpretation": (
                "pipeline validation only, not a new finite bound and not "
                "a proof of the reduction from all bridgeless graphs"
            ),
        },
        "counts_by_order": per_order,
        "counts": counts,
        "started_utc": start_wall.isoformat(),
        "finished_utc": finish_wall.isoformat(),
        "duration_seconds": time.monotonic() - start_mono,
        "counterexample_claimed": False,
        "warnings": [
            "No finite search proves the conjecture.",
            (
                "An UNSAT solver status, if any, is uncertified here and is "
                "not a disproof."
            ),
            (
                "geng removes graph-isomorphic duplicates; cover "
                "canonicalization separately quotients Aut(G) x S5."
            ),
        ],
    }
    _write_json(output / "summary.json", summary)
    metadata["status"] = "COMPLETE"
    metadata["finished_utc"] = finish_wall.isoformat()
    _write_json(output / "metadata.json", metadata)
    _write_checksums(output)
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Enumerate connected simple cubic graphs with nauty geng and "
            "solve the exact five-CDC encoding"
        )
    )
    parser.add_argument("--min-n", type=int, required=True)
    parser.add_argument("--max-n", type=int, required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--geng", default="geng")
    parser.add_argument(
        "--solver", choices=("cms", "cadical", "both"), default="both"
    )
    parser.add_argument("--cryptominisat", default="cryptominisat5")
    parser.add_argument("--cadical", default="cadical")
    parser.add_argument("--oddness-max-vertices", type=int, default=18)
    parser.add_argument("--cover-canon-max-vertices", type=int, default=12)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    if args.min_n > args.max_n:
        raise SearchError("--min-n exceeds --max-n")
    return run_enumeration(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, SearchError, ValueError) as exc:
        print(
            json.dumps({"error": str(exc)}, sort_keys=True, separators=(",", ":")),
            file=sys.stderr,
        )
        raise SystemExit(2)
