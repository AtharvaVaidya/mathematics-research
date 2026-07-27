#!/usr/bin/env python3
"""Independent replay of the frozen complete order-22 cap census."""

from __future__ import annotations

import gzip
import hashlib
import itertools
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
SOURCE = ROOT.parent / "order22-filter-census-20260725"

EXPECTED_CANONICAL_ROWS = 7_319_447
EXPECTED_CANONICAL_SHA256 = (
    "6d90b02cab31dcd40bbf1de18e36bdc7b4b8515e626bfcb5f2d721b90bf2a41b"
)
EXPECTED_FILTER_SHA256 = (
    "bceb0145309b9b0237231a271e74804db2197628ccccf70ac1f51ee8b6c9beb6"
)
EXPECTED_BRIDGELESS_ROWS = 7_187_627
EXPECTED_HARD_ROWS = 12_892
EXPECTED_HARD_SHA256 = (
    "230f2cd88e72011d73a40c5f3d7d5f9fb0fca6110de2ec2541581bc50982037c"
)
EXPECTED_CYCLIC4_ROWS = 31
EXPECTED_CYCLIC4_SHA256 = (
    "2c3d91e55cb264450cf321e2299355f6cf0f5c2c60a83c99372a1d73ed5a4223"
)
EXPECTED_POLE_ROWS = 14_322
EXPECTED_POLE_SHA256 = (
    "74a710c7396ebbe2e294489a4d283606236bcab001cb9379e4169b7735ee9177"
)
EXPECTED_CYCLIC4_FULL_TRANSCRIPT_SHA256 = (
    "52edd8a189012acefd3565a79d5c58b6f209bbe40156560eb57e2c569fd7c091"
)
EXPECTED_FULL_POLE_ROWS = 5_956_104
EXPECTED_FULL_POLE_SHA256 = (
    "cf7a19244912c746c1ef1247a4b45e6ad1df647feaa4251e59db381351b5db46"
)
EXPECTED_TRANSCRIPT_SHA256 = (
    "19f1cdcfe01f6d858a0811bf6d208826a16c0766f54995e0453f60f83128fd6c"
)

SUMMARY = re.compile(
    r"^SUMMARY implementation=(cadical|csp) mode=exceptional "
    r"rows=(\d+) queries=(\d+) sat=(\d+) hits=(\d+)$"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def decode_graph6(record: bytes) -> tuple[int, list[tuple[int, int]]]:
    if not record or record[0] == 126:
        raise SystemExit("only short graph6 records are permitted")
    vertices = record[0] - 63
    if not 0 <= vertices <= 62:
        raise SystemExit("invalid graph6 order")
    bits: list[int] = []
    for character in record[1:]:
        value = character - 63
        if not 0 <= value < 64:
            raise SystemExit("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = vertices * (vertices - 1) // 2
    if len(bits) < needed or any(bits[needed:]):
        raise SystemExit("malformed graph6 padding")
    edges: list[tuple[int, int]] = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, edges


def encode_graph6(vertices: int, edges: list[tuple[int, int]]) -> bytes:
    adjacent = {tuple(sorted(edge)) for edge in edges}
    bits = [
        int((left, right) in adjacent)
        for right in range(1, vertices)
        for left in range(right)
    ]
    while len(bits) % 6:
        bits.append(0)
    result = bytearray((vertices + 63,))
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = 2 * value + bit
        result.append(value + 63)
    return bytes(result)


def incidence(
    vertices: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    result = [[] for _ in range(vertices)]
    for edge_id, (left, right) in enumerate(edges):
        result[left].append(edge_id)
        result[right].append(edge_id)
    return result


def connected_after_deleting(
    vertices: int,
    edges: list[tuple[int, int]],
    rows: list[list[int]],
    removed: frozenset[int],
) -> bool:
    reached = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for edge_id in rows[vertex]:
            if edge_id in removed:
                continue
            left, right = edges[edge_id]
            other = right if left == vertex else left
            if other not in reached:
                reached.add(other)
                stack.append(other)
    return len(reached) == vertices


def fundamental_cycle_signatures(
    vertices: int,
    edges: list[tuple[int, int]],
    rows: list[list[int]],
) -> list[int]:
    parent = [-1] * vertices
    parent_edge = [-1] * vertices
    depth = [0] * vertices
    parent[0] = 0
    tree_edges: set[int] = set()
    stack = [0]
    while stack:
        vertex = stack.pop()
        for edge in rows[vertex]:
            left, right = edges[edge]
            other = right if left == vertex else left
            if parent[other] != -1:
                continue
            parent[other] = vertex
            parent_edge[other] = edge
            depth[other] = depth[vertex] + 1
            tree_edges.add(edge)
            stack.append(other)
    if any(value < 0 for value in parent):
        raise SystemExit("hard graph is disconnected")

    basis: list[int] = []
    for chord, (left, right) in enumerate(edges):
        if chord in tree_edges:
            continue
        word = 1 << chord
        first, second = left, right
        while depth[first] > depth[second]:
            word |= 1 << parent_edge[first]
            first = parent[first]
        while depth[second] > depth[first]:
            word |= 1 << parent_edge[second]
            second = parent[second]
        while first != second:
            word |= 1 << parent_edge[first]
            word |= 1 << parent_edge[second]
            first = parent[first]
            second = parent[second]
        basis.append(word)
    if len(basis) != len(edges) - vertices + 1:
        raise SystemExit("wrong cycle-space dimension")
    return [
        sum(
            ((generator >> edge) & 1) << position
            for position, generator in enumerate(basis)
        )
        for edge in range(len(edges))
    ]


def cut_class(
    vertices: int,
    edges: list[tuple[int, int]],
    rows: list[list[int]],
) -> str:
    signatures = fundamental_cycle_signatures(vertices, edges, rows)
    if len(set(signatures)) != len(signatures):
        return "two_cut"
    vertex_stars = {
        tuple(sorted(row))
        for row in rows
    }
    by_signature: dict[int, list[int]] = {}
    for edge, signature in enumerate(signatures):
        by_signature.setdefault(signature, []).append(edge)
    for first in range(len(edges)):
        for second in range(first + 1, len(edges)):
            target = signatures[first] ^ signatures[second]
            for third in by_signature.get(target, []):
                if third <= second:
                    continue
                if (first, second, third) not in vertex_stars:
                    return "nontrivial_three_cut"
    return "cyclically_four"


def even_complement(
    vertices: int,
    edges: list[tuple[int, int]],
    matching: set[int],
) -> bool:
    neighbours = [[] for _ in range(vertices)]
    for edge_id, (left, right) in enumerate(edges):
        if edge_id in matching:
            continue
        neighbours[left].append(right)
        neighbours[right].append(left)
    if any(len(row) != 2 for row in neighbours):
        raise SystemExit("perfect-matching complement is not 2-regular")
    seen: set[int] = set()
    for start in range(vertices):
        if start in seen:
            continue
        previous = -1
        vertex = start
        length = 0
        while True:
            seen.add(vertex)
            length += 1
            first, second = neighbours[vertex]
            following = second if first == previous else first
            previous, vertex = vertex, following
            if vertex == start:
                break
        if length % 2:
            return False
    return True


def tait_colorable(
    vertices: int,
    edges: list[tuple[int, int]],
    rows: list[list[int]],
) -> bool:
    matched = [False] * vertices
    chosen: set[int] = set()

    def search() -> bool:
        try:
            vertex = matched.index(False)
        except ValueError:
            return even_complement(vertices, edges, chosen)
        matched[vertex] = True
        for edge_id in rows[vertex]:
            left, right = edges[edge_id]
            other = right if left == vertex else left
            if matched[other]:
                continue
            matched[other] = True
            chosen.add(edge_id)
            if search():
                return True
            chosen.remove(edge_id)
            matched[other] = False
        matched[vertex] = False
        return False

    return search()


def verify_hard_identity() -> bytes:
    canonical = SOURCE / "canonical-connected-cubic-order22.g6"
    filter_report = SOURCE / "filter-report.json"
    if sha256_file(canonical) != EXPECTED_CANONICAL_SHA256:
        raise SystemExit("canonical corpus digest mismatch")
    if sha256_file(filter_report) != EXPECTED_FILTER_SHA256:
        raise SystemExit("filter report digest mismatch")
    source = json.loads(filter_report.read_text(encoding="utf-8"))
    if source.get("generated") != EXPECTED_CANONICAL_ROWS:
        raise SystemExit("filter/canonical row-count mismatch")
    if source.get("bridgeless") != EXPECTED_BRIDGELESS_ROWS:
        raise SystemExit("filter bridgeless count mismatch")
    if source.get("hard_noncolourable") != EXPECTED_HARD_ROWS:
        raise SystemExit("filter hard count mismatch")
    expected = {
        int(row["index"]): str(row["graph6"]).encode("ascii")
        for row in source["hard_rows"]
    }
    if len(expected) != EXPECTED_HARD_ROWS:
        raise SystemExit("duplicate or missing filter hard rows")

    retained = (ARTIFACTS / "order22-hard.g6").read_bytes()
    if retained.count(b"\n") != EXPECTED_HARD_ROWS:
        raise SystemExit("retained hard row-count mismatch")
    if sha256(retained) != EXPECTED_HARD_SHA256:
        raise SystemExit("retained hard digest mismatch")
    hard_records = retained.splitlines()
    hard_cursor = 0
    rows = 0
    with canonical.open("rb") as stream:
        for rows, raw in enumerate(stream, start=1):
            target = expected.get(rows)
            if target is None:
                continue
            if raw[:-1] != target:
                raise SystemExit(f"hard identity mismatch at row {rows}")
            if hard_records[hard_cursor] != target:
                raise SystemExit("retained hard ordering mismatch")
            hard_cursor += 1
    if rows != EXPECTED_CANONICAL_ROWS or hard_cursor != EXPECTED_HARD_ROWS:
        raise SystemExit("canonical/hard identity accounting mismatch")

    for implementation in ("direct", "matching"):
        duplicate = ARTIFACTS / f"order22-hard-{implementation}.g6"
        if duplicate.read_bytes() != retained:
            raise SystemExit(f"{implementation} full Tait filter output mismatch")
    direct_log = (ARTIFACTS / "tait-direct.log").read_text(encoding="utf-8")
    if direct_log != (
        "SUMMARY rows=7319447 bridgeless=7187627 non_tait=12892\n"
    ):
        raise SystemExit("malformed direct Tait-filter summary")
    matching_log = (
        ARTIFACTS / "tait-matching.log"
    ).read_text(encoding="utf-8")
    if matching_log != (
        "SUMMARY rows=7319447 bridgeless=7187627 non_tait=12892 "
        "algorithm=perfect_matching_even_complement\n"
    ):
        raise SystemExit("malformed matching Tait-filter summary")
    return retained


def verify_cyclic4_extraction(hard: bytes) -> bytes:
    selected = bytearray()
    profile = {
        "two_cut": 0,
        "nontrivial_three_cut": 0,
        "cyclically_four": 0,
    }
    for row_number, record in enumerate(hard.splitlines(), start=1):
        vertices, edges = decode_graph6(record)
        rows = incidence(vertices, edges)
        if vertices != 22 or len(edges) != 33:
            raise SystemExit(f"hard row {row_number}: wrong order or size")
        if any(len(row) != 3 for row in rows):
            raise SystemExit(f"hard row {row_number}: not cubic")
        classification = cut_class(vertices, edges, rows)
        profile[classification] += 1
        if classification == "cyclically_four":
            selected.extend(record)
            selected.append(10)
    expected_profile = {
        "two_cut": 5_024,
        "nontrivial_three_cut": 7_837,
        "cyclically_four": 31,
    }
    if profile != expected_profile:
        raise SystemExit(f"hard cut profile mismatch: {profile}")
    retained = (ARTIFACTS / "order22-cyclic4.g6").read_bytes()
    if retained != bytes(selected):
        raise SystemExit("retained cyclic-4 corpus is not the exact extraction")
    if sha256(retained) != EXPECTED_CYCLIC4_SHA256:
        raise SystemExit("cyclic-4 corpus digest mismatch")
    cleanroom_log = (
        ARTIFACTS / "cyclic4-cleanroom.log"
    ).read_text(encoding="utf-8")
    if cleanroom_log != (
        "SUMMARY rows=12892 bridges=0 two_cut=5024 "
        "nontrivial_three_cut=7837 cyclically_four=31\n"
    ):
        raise SystemExit("malformed clean-room cut summary")
    return retained


def verify_caps_and_expansion(caps: bytes) -> bytes:
    expected_poles = bytearray()
    cap_records = caps.splitlines()
    if len(cap_records) != EXPECTED_CYCLIC4_ROWS:
        raise SystemExit("cyclic-4 cap row-count mismatch")
    for row_number, record in enumerate(cap_records, start=1):
        vertices, edges = decode_graph6(record)
        rows = incidence(vertices, edges)
        if any(
            not connected_after_deleting(
                vertices, edges, rows, frozenset((edge,))
            )
            for edge in range(len(edges))
        ):
            raise SystemExit(f"cap {row_number}: bridge found")
        if tait_colorable(vertices, edges, rows):
            raise SystemExit(f"cap {row_number}: Tait colouring found")

        # A third, brute-force cyclic-connectivity audit on the 31 survivors.
        for first, second in itertools.combinations(range(len(edges)), 2):
            removed = frozenset((first, second))
            if not connected_after_deleting(vertices, edges, rows, removed):
                raise SystemExit(f"cap {row_number}: two-edge cut found")
        vertex_stars = {frozenset(row) for row in rows}
        for triple in itertools.combinations(range(len(edges)), 3):
            removed = frozenset(triple)
            if removed in vertex_stars:
                continue
            if not connected_after_deleting(vertices, edges, rows, removed):
                raise SystemExit(
                    f"cap {row_number}: nontrivial three-edge cut found"
                )

        for first, second in itertools.combinations(range(len(edges)), 2):
            a, b = edges[first]
            c, d = edges[second]
            if len({a, b, c, d}) != 4:
                continue
            remaining = [
                edge
                for edge_id, edge in enumerate(edges)
                if edge_id not in {first, second}
            ]
            expected_poles.extend(encode_graph6(vertices, remaining))
            expected_poles.append(10)
    retained = gzip.decompress(
        (ARTIFACTS / "order22-cyclic4-poles.g6.gz").read_bytes()
    )
    if retained != bytes(expected_poles):
        raise SystemExit("retained pole stream is not the exact cap expansion")
    if retained.count(b"\n") != EXPECTED_POLE_ROWS:
        raise SystemExit("pole row-count mismatch")
    if sha256(retained) != EXPECTED_POLE_SHA256:
        raise SystemExit("pole digest mismatch")
    expand_log = (ARTIFACTS / "expand.log").read_text(encoding="utf-8")
    if expand_log != "SUMMARY graphs=31 poles=14322\n":
        raise SystemExit("malformed expansion summary")
    return retained


def verify_cyclic4_full_signatures(poles: bytes) -> None:
    expected = b"".join(
        record + b"\t10\t3ff\n" for record in poles.splitlines()
    )
    if expected.count(b"\n") != EXPECTED_POLE_ROWS:
        raise SystemExit("cyclic-4 full-signature row-count mismatch")
    if sha256(expected) != EXPECTED_CYCLIC4_FULL_TRANSCRIPT_SHA256:
        raise SystemExit("cyclic-4 full-signature transcript digest mismatch")

    for implementation in ("cadical", "csp"):
        retained = gzip.decompress(
            (
                ARTIFACTS
                / f"cyclic4-full-{implementation}.tsv.gz"
            ).read_bytes()
        )
        if retained != expected:
            raise SystemExit(
                f"{implementation}: cyclic-4 full-signature output mismatch"
            )
        log = (
            ARTIFACTS / f"cyclic4-full-{implementation}.log"
        ).read_text(encoding="utf-8")
        expected_log = (
            "progress rows=5000 queries=50000 hits=0\n"
            "progress rows=10000 queries=100000 hits=0\n"
            f"SUMMARY implementation={implementation} mode=full "
            "rows=14322 queries=143220 sat=143220 hits=0\n"
        )
        if log != expected_log:
            raise SystemExit(
                f"{implementation}: malformed cyclic-4 full-signature log"
            )


def read_classifier_summary(path: Path, implementation: str) -> dict[str, int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if any("ERROR" in line for line in lines):
        raise SystemExit(f"{path}: classifier error present")
    matches = [match for line in lines if (match := SUMMARY.fullmatch(line))]
    if len(matches) != 1 or matches[0].group(1) != implementation:
        raise SystemExit(f"{path}: malformed classifier summary")
    match = matches[0]
    return {
        "rows": int(match.group(2)),
        "queries": int(match.group(3)),
        "sat": int(match.group(4)),
        "hits": int(match.group(5)),
    }


def verify_boundary_decisions() -> dict[str, int]:
    summaries = {}
    audits = {}
    for implementation in ("cadical", "csp"):
        prefix = ARTIFACTS / implementation
        summary = read_classifier_summary(
            prefix.with_suffix(".classifier.log"), implementation
        )
        audit = json.loads(
            prefix.with_suffix(".transcript.audit.json").read_text(
                encoding="utf-8"
            )
        )
        expected_audit = {
            "schema": "five-cdc-exceptional-transcript-audit-v1",
            "implementation": implementation,
            "shard": 0,
            "rows": EXPECTED_POLE_ROWS,
            "exceptional_rows": 0,
            "sha256": EXPECTED_TRANSCRIPT_SHA256,
        }
        if audit != expected_audit:
            raise SystemExit(f"{implementation}: transcript audit mismatch")
        expected_status = f"PASS implementation={implementation}\n"
        if prefix.with_suffix(".status").read_text(
            encoding="utf-8"
        ) != expected_status:
            raise SystemExit(f"{implementation}: malformed PASS marker")
        summaries[implementation] = summary
        audits[implementation] = audit
    if summaries["cadical"] != summaries["csp"]:
        raise SystemExit("boundary-classifier aggregate mismatch")
    expected_summary = {
        "rows": EXPECTED_POLE_ROWS,
        "queries": 57_288,
        "sat": 57_288,
        "hits": 0,
    }
    if summaries["cadical"] != expected_summary:
        raise SystemExit("unexpected boundary-classifier totals")
    if audits["cadical"]["sha256"] != audits["csp"]["sha256"]:
        raise SystemExit("boundary transcript digest mismatch")
    return expected_summary


def verify_full_cap_expansion(hard: bytes) -> list[dict]:
    """Reconstruct the retained 5.9M-row stream without materializing it."""

    cap_records = hard.splitlines()
    if len(cap_records) != EXPECTED_HARD_ROWS:
        raise SystemExit("full cap row-count mismatch")

    pole_path = ARTIFACTS / "order22-all-cap-poles.g6.gz"
    full_digest = hashlib.sha256()
    shard_digests = [hashlib.sha256() for _ in range(8)]
    shard_rows = [0] * 8
    pole_rows = 0

    with gzip.open(pole_path, "rb") as retained:
        for cap_number, record in enumerate(cap_records, start=1):
            vertices, edges = decode_graph6(record)
            rows = incidence(vertices, edges)
            if vertices != 22 or len(edges) != 33:
                raise SystemExit(
                    f"full cap {cap_number}: wrong order or size"
                )
            if any(len(row) != 3 for row in rows):
                raise SystemExit(f"full cap {cap_number}: not cubic")
            if any(
                not connected_after_deleting(
                    vertices, edges, rows, frozenset((edge,))
                )
                for edge in range(len(edges))
            ):
                raise SystemExit(f"full cap {cap_number}: bridge found")
            if tait_colorable(vertices, edges, rows):
                raise SystemExit(
                    f"full cap {cap_number}: Tait colouring found"
                )

            for first, second in itertools.combinations(
                range(len(edges)), 2
            ):
                a, b = edges[first]
                c, d = edges[second]
                if len({a, b, c, d}) != 4:
                    continue
                remaining = [
                    edge
                    for edge_id, edge in enumerate(edges)
                    if edge_id not in {first, second}
                ]
                expected = encode_graph6(vertices, remaining) + b"\n"
                observed = retained.readline()
                pole_rows += 1
                if observed != expected:
                    raise SystemExit(
                        "retained full pole stream differs at row "
                        f"{pole_rows} (cap {cap_number}, edges "
                        f"{first},{second})"
                    )
                full_digest.update(observed)
                shard = (pole_rows - 1) % 8
                shard_digests[shard].update(observed)
                shard_rows[shard] += 1
        if retained.read(1):
            raise SystemExit("retained full pole stream has extra rows")

    if pole_rows != EXPECTED_FULL_POLE_ROWS:
        raise SystemExit(
            "full pole row-count mismatch: "
            f"{pole_rows} != {EXPECTED_FULL_POLE_ROWS}"
        )
    if full_digest.hexdigest() != EXPECTED_FULL_POLE_SHA256:
        raise SystemExit("full pole stream digest mismatch")

    shards = [
        {
            "shard": shard,
            "rows": shard_rows[shard],
            "sha256": shard_digests[shard].hexdigest(),
            "file": f"input-shard{shard}.g6",
        }
        for shard in range(8)
    ]
    manifest = json.loads(
        (ARTIFACTS / "full-run" / "input-manifest.json").read_text(
            encoding="utf-8"
        )
    )
    expected_manifest = {
        "schema": "five-cdc-order22-cap-input-shards-v1",
        "input": {
            "rows": EXPECTED_FULL_POLE_ROWS,
            "sha256": EXPECTED_FULL_POLE_SHA256,
        },
        "shards": shards,
    }
    if manifest != expected_manifest:
        raise SystemExit("retained full-run shard manifest mismatch")
    full_expand_log = (
        ARTIFACTS / "full-expand.log"
    ).read_text(encoding="utf-8")
    if full_expand_log != "SUMMARY graphs=12892 poles=5956104\n":
        raise SystemExit("malformed full expansion summary")
    return shards


def read_full_audit(path: Path, implementation: str, shard: int) -> dict:
    result = json.loads(path.read_text(encoding="utf-8"))
    for key, expected in {
        "schema": "five-cdc-exceptional-transcript-audit-v1",
        "implementation": implementation,
        "shard": shard,
        "exceptional_rows": 0,
    }.items():
        if result.get(key) != expected:
            raise SystemExit(f"{path}: expected {key}={expected!r}")
    digest = result.get("sha256")
    if not isinstance(digest, str) or not re.fullmatch(
        r"[0-9a-f]{64}", digest
    ):
        raise SystemExit(f"{path}: malformed transcript digest")
    if not isinstance(result.get("rows"), int) or result["rows"] < 0:
        raise SystemExit(f"{path}: malformed transcript row count")
    return result


def verify_full_boundary_decisions(
    input_shards: list[dict],
) -> tuple[list[dict], int, int]:
    root = ARTIFACTS / "full-run"
    total_rows = 0
    total_queries = 0
    total_sat = 0
    results = []
    for shard in range(8):
        audits = {}
        summaries = {}
        for implementation in ("cadical", "csp"):
            prefix = root / f"{implementation}-shard{shard}"
            audit = read_full_audit(
                prefix.with_suffix(".transcript.audit.json"),
                implementation,
                shard,
            )
            summary = read_classifier_summary(
                prefix.with_suffix(".classifier.log"), implementation
            )
            status = prefix.with_suffix(".status").read_text(
                encoding="utf-8"
            )
            expected_status = (
                f"PASS implementation={implementation} shard={shard}\n"
            )
            if status != expected_status:
                raise SystemExit(f"{prefix}: malformed PASS marker")
            if audit["rows"] != summary["rows"] or summary["hits"] != 0:
                raise SystemExit(
                    f"full shard {shard}: audit/summary mismatch"
                )
            audits[implementation] = audit
            summaries[implementation] = summary

        if audits["cadical"]["sha256"] != audits["csp"]["sha256"]:
            raise SystemExit(
                f"full shard {shard}: transcript digest mismatch"
            )
        if summaries["cadical"] != summaries["csp"]:
            raise SystemExit(
                f"full shard {shard}: implementation summary mismatch"
            )
        summary = summaries["cadical"]
        if summary["rows"] != input_shards[shard]["rows"]:
            raise SystemExit(
                f"full shard {shard}: decision/input row mismatch"
            )
        total_rows += summary["rows"]
        total_queries += summary["queries"]
        total_sat += summary["sat"]
        results.append(
            {
                "shard": shard,
                **summary,
                "input_sha256": input_shards[shard]["sha256"],
                "transcript_sha256": audits["cadical"]["sha256"],
            }
        )
    if total_rows != EXPECTED_FULL_POLE_ROWS:
        raise SystemExit("full aggregate decision row mismatch")
    return results, total_queries, total_sat


def main() -> int:
    hard = verify_hard_identity()
    caps = verify_cyclic4_extraction(hard)
    poles = verify_caps_and_expansion(caps)
    verify_cyclic4_full_signatures(poles)
    boundary = verify_boundary_decisions()
    full_input_shards = verify_full_cap_expansion(hard)
    full_shards, full_queries, full_sat = verify_full_boundary_decisions(
        full_input_shards
    )
    result = {
        "schema": "five-cdc-order22-full-cap-census-v1",
        "classification": "FINITE INDEPENDENT EXACT ENUMERATION",
        "canonical_graphs": EXPECTED_CANONICAL_ROWS,
        "bridgeless_graphs": EXPECTED_BRIDGELESS_ROWS,
        "bridgeless_non_tait_graphs": EXPECTED_HARD_ROWS,
        "hard_corpus_sha256": EXPECTED_HARD_SHA256,
        "hard_cut_profile": {
            "two_cut": 5_024,
            "nontrivial_three_cut_after_two_cut_exclusion": 7_837,
            "cyclically_four": EXPECTED_CYCLIC4_ROWS,
        },
        "cyclically_four_corpus_sha256": EXPECTED_CYCLIC4_SHA256,
        "independent_edge_deletions": poles.count(b"\n"),
        "pole_corpus_sha256": EXPECTED_POLE_SHA256,
        "cyclically_four_full_signature_rows": EXPECTED_POLE_ROWS,
        "cyclically_four_full_signature_mask": "0x3ff",
        "cyclically_four_full_signature_transcript_sha256": (
            EXPECTED_CYCLIC4_FULL_TRANSCRIPT_SHA256
        ),
        "boundary_classification_per_implementation": boundary,
        "transcript_sha256": EXPECTED_TRANSCRIPT_SHA256,
        "full_cap_graphs": EXPECTED_HARD_ROWS,
        "full_independent_edge_deletions": EXPECTED_FULL_POLE_ROWS,
        "full_pole_corpus_sha256": EXPECTED_FULL_POLE_SHA256,
        "full_queries_per_implementation": full_queries,
        "full_sat_answers_per_implementation": full_sat,
        "full_shards": full_shards,
        "exceptional_hits": 0,
        "theorem": (
            "No bridge-free connected simple terminal-distinct order-22 "
            "four-pole has either exceptional exact boundary signature in "
            "the fixed five-colour D5 model."
        ),
        "warning": (
            "This finite theorem relies on the separately proved simple-cap "
            "reduction. It says nothing about repeated terminals, nonsimple "
            "cores, arbitrary-colour CDC signatures, or higher orders, and "
            "it does not resolve Five-CDC."
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
