#!/usr/bin/env python3
"""Independent standard-library verifier for the Petersen--Foster test graph.

The graph replaces each vertex of the Petersen graph by the three-pole
obtained by deleting vertex 0 from the Foster graph.  This script constructs
the graph from the published LCF description of the Foster graph and checks
all claimed properties without relying on NetworkX or a SAT solver.
"""

from __future__ import annotations

from collections import deque
import hashlib
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
FOSTER_LCF = (17, -9, 37, -37, 9, -17) * 15
PETERSEN_EDGES = (
    (0, 1),
    (1, 2),
    (2, 3),
    (0, 4),
    (3, 4),
    (0, 5),
    (1, 6),
    (2, 7),
    (5, 7),
    (3, 8),
    (5, 8),
    (6, 8),
    (4, 9),
    (6, 9),
    (7, 9),
)
FOSTER_ROOT = 0
FOSTER_PORTS = (1, 17, 89)
EXPECTED_GRAPH6_SHA256 = (
    "c89a74ee736367cb6571600ee748f68e4eb4667787f57b1c05ccba6ee49cbd47"
)
EXPECTED_LABELS_SHA256 = (
    "441f2c328ff9631c3a7c9fe48ef39c6b029297a66676d7214131671dfc72b863"
)


def foster_edges() -> set[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for u in range(90):
        v = (u + 1) % 90
        edges.add((min(u, v), max(u, v)))
        v = (u + FOSTER_LCF[u]) % 90
        edges.add((min(u, v), max(u, v)))
    assert len(edges) == 135
    return edges


def petersen_foster_edges() -> set[tuple[int, int]]:
    """Construct the graph on vertices 0,...,889.

    In copy ``a``, retained Foster vertex ``u`` is numbered
    ``89*a + (u-1)``.  The three incidences at each Petersen vertex are
    assigned to Foster ports 1, 17, 89 in the order in PETERSEN_EDGES.
    """
    base = foster_edges()
    edges: set[tuple[int, int]] = set()
    for copy in range(10):
        for u, v in base:
            if FOSTER_ROOT in (u, v):
                continue
            uu = 89 * copy + (u - 1)
            vv = 89 * copy + (v - 1)
            edges.add((min(uu, vv), max(uu, vv)))

    incidence_count = [0] * 10
    for a, b in PETERSEN_EDGES:
        pa = FOSTER_PORTS[incidence_count[a]]
        pb = FOSTER_PORTS[incidence_count[b]]
        incidence_count[a] += 1
        incidence_count[b] += 1
        u = 89 * a + (pa - 1)
        v = 89 * b + (pb - 1)
        edges.add((min(u, v), max(u, v)))
    assert incidence_count == [3] * 10
    return edges


def adjacency(n: int, edges: set[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for eid, (u, v) in enumerate(sorted(edges)):
        adj[u].append((v, eid))
        adj[v].append((u, eid))
    return adj


def graph6_edge_order(n: int, edges: set[tuple[int, int]]) -> list[tuple[int, int]]:
    return [(u, v) for v in range(1, n) for u in range(v) if (u, v) in edges]


def graph6(n: int, edges: set[tuple[int, int]]) -> str:
    assert 63 <= n <= 258047
    chars = [
        126,
        63 + ((n >> 12) & 63),
        63 + ((n >> 6) & 63),
        63 + (n & 63),
    ]
    bits = [int((u, v) in edges) for v in range(1, n) for u in range(v)]
    bits.extend([0] * ((-len(bits)) % 6))
    chars.extend(63 + sum(bits[i + j] << (5 - j) for j in range(6))
                 for i in range(0, len(bits), 6))
    return "".join(map(chr, chars))


def connected(n: int, edges: set[tuple[int, int]]) -> bool:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = {0}
    todo = [0]
    while todo:
        u = todo.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return len(seen) == n


def bridges(
    n: int, ordered_edges: list[tuple[int, int]], omitted: int | None = None
) -> list[int]:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for eid, (u, v) in enumerate(ordered_edges):
        if eid == omitted:
            continue
        adj[u].append((v, eid))
        adj[v].append((u, eid))

    timer = 0
    tin = [-1] * n
    low = [-1] * n
    answer: list[int] = []

    def dfs(u: int, parent_eid: int) -> None:
        nonlocal timer
        tin[u] = low[u] = timer
        timer += 1
        for v, eid in adj[u]:
            if eid == parent_eid:
                continue
            if tin[v] != -1:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, eid)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    answer.append(eid)

    dfs(0, -1)
    if any(t == -1 for t in tin):
        return [-1]
    return answer


def girth(n: int, edges: set[tuple[int, int]]) -> int:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    best = n + 1
    for root in range(n):
        dist = [-1] * n
        parent = [-1] * n
        dist[root] = 0
        q = deque([root])
        while q:
            u = q.popleft()
            if 2 * dist[u] + 1 >= best:
                continue
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    q.append(v)
                elif parent[u] != v:
                    best = min(best, dist[u] + dist[v] + 1)
    return best


def enumerate_perfect_matchings(
    n: int, edges: tuple[tuple[int, int], ...]
) -> list[tuple[int, ...]]:
    incident = [[] for _ in range(n)]
    for eid, (u, v) in enumerate(edges):
        incident[u].append((v, eid))
        incident[v].append((u, eid))
    answers: list[tuple[int, ...]] = []

    def rec(used: set[int], chosen: list[int]) -> None:
        if len(used) == n:
            answers.append(tuple(sorted(chosen)))
            return
        u = min(set(range(n)) - used)
        for v, eid in incident[u]:
            if v not in used:
                rec(used | {u, v}, chosen + [eid])

    rec(set(), [])
    return sorted(set(answers))


def component_sizes(
    n: int, edges: list[tuple[int, int]]
) -> list[int]:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    sizes: list[int] = []
    unseen = set(range(n))
    while unseen:
        root = min(unseen)
        seen = {root}
        todo = [root]
        while todo:
            u = todo.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        sizes.append(len(seen))
        unseen -= seen
    return sorted(sizes)


def verify_fivecdc(
    n: int, edges: set[tuple[int, int]]
) -> tuple[list[int], list[int]]:
    label_text = (HERE / "fivecdc-labels.txt").read_text()
    digest = hashlib.sha256(label_text.encode()).hexdigest()
    assert digest == EXPECTED_LABELS_SHA256
    masks = [int(x) for x in label_text.split()]
    ordered = graph6_edge_order(n, edges)
    assert len(masks) == len(ordered)
    assert all(0 < m < 32 and m.bit_count() == 2 for m in masks)

    parity = [0] * n
    counts = [0] * 5
    for (u, v), mask in zip(ordered, masks):
        parity[u] ^= mask
        parity[v] ^= mask
        for colour in range(5):
            counts[colour] += (mask >> colour) & 1
    assert parity == [0] * n
    return masks, counts


def main() -> None:
    sys.setrecursionlimit(10_000)
    n = 890
    edges = petersen_foster_edges()
    assert len(edges) == 1335
    assert all(u != v for u, v in edges)
    assert connected(n, edges)
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    assert deg == [3] * n

    encoding = graph6(n, edges)
    graph6_digest = hashlib.sha256((encoding + "\n").encode()).hexdigest()
    assert graph6_digest == EXPECTED_GRAPH6_SHA256

    ordered = sorted(edges)
    assert bridges(n, ordered) == []
    for omitted in range(len(ordered)):
        assert bridges(n, ordered, omitted) == []
    edge_connectivity = 3

    graph_girth = girth(n, edges)
    assert graph_girth == 10
    explicit_cycle = [0, 81, 80, 79, 78, 77, 4, 3, 2, 1]
    assert len(set(explicit_cycle)) == 10
    assert all(
        (min(u, v), max(u, v)) in edges
        for u, v in zip(explicit_cycle, explicit_cycle[1:] + explicit_cycle[:1])
    )

    p_edges = tuple(PETERSEN_EDGES)
    matchings = enumerate_perfect_matchings(10, p_edges)
    assert len(matchings) == 6
    complement_components = []
    for matching in matchings:
        complement = [e for eid, e in enumerate(p_edges) if eid not in matching]
        sizes = component_sizes(10, complement)
        assert sizes == [5, 5]
        complement_components.append(sizes)

    masks, circuit_sizes = verify_fivecdc(n, edges)

    # The three external edges at macro-vertex 0 form a cyclic 3-edge cut.
    copy_zero = set(range(89))
    cut = [(u, v) for u, v in edges if (u in copy_zero) != (v in copy_zero)]
    assert len(cut) == 3
    inside = {(u, v) for u, v in edges if u in copy_zero and v in copy_zero}
    outside = {(u, v) for u, v in edges if u not in copy_zero and v not in copy_zero}
    assert len(inside) >= len(copy_zero)
    assert len(outside) >= n - len(copy_zero)

    report = {
        "classification": "VERIFIED_POSITIVE_NONTait_TEST_GRAPH",
        "construction": "Petersen vertex substitution by Foster-minus-vertex-0",
        "vertices": n,
        "edges": len(edges),
        "simple": True,
        "cubic": True,
        "connected": True,
        "bridgeless": True,
        "edge_connectivity": edge_connectivity,
        "cyclic_three_edge_cut": cut,
        "cyclic_edge_connectivity": 3,
        "girth": graph_girth,
        "explicit_ten_cycle": explicit_cycle,
        "petersen_perfect_matchings": len(matchings),
        "petersen_matching_complement_component_sizes": complement_components,
        "tait_colourable": False,
        "tait_proof": "odd-pole parity lemma plus Petersen matching audit",
        "fivecdc": True,
        "fivecdc_edge_masks": len(masks),
        "fivecdc_subgraph_edge_counts": circuit_sizes,
        "graph6_sha256_with_newline": graph6_digest,
        "fivecdc_labels_sha256": EXPECTED_LABELS_SHA256,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
