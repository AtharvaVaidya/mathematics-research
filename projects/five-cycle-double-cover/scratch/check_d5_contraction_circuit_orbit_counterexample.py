#!/usr/bin/env python3
"""Independent replay of the smallest contraction-orbit counterexample.

The counterexample is to the *reconfiguration lemma*

    every generalized factor-circuit orbit on an edge contraction contains
    a side-xor-weight-two state,

not to FiveCDC.  The original cubic graph and its other orbit do have good
states.

Only the Python standard library is used.
"""

from __future__ import annotations

from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, permutations


GRAPH6 = "M?AA@BORD_CoEOAo?"
CONTRACTED_EDGE = 15
WITNESS_TEXT = (
    "01",
    "02",
    "03",
    "13",
    "03",
    "01",
    "23",
    "02",
    "03",
    "03",
    "02",
    "23",
    "23",
    "13",
    "12",
    "01",
    "23",
    "12",
    "01",
    "02",
)
LABELS = tuple(
    (1 << first) | (1 << second)
    for first, second in combinations(range(5), 2)
)
LABEL_SET = frozenset(LABELS)
PERMUTATIONS = tuple(permutations(range(5)))


def decode_graph6(row: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    assert row and row[0] != "~"
    vertices = ord(row[0]) - 63
    bits = []
    for character in row[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    cursor = 0
    edges = []
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, tuple(edges)


def connected_after_deleting(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    deleted_vertices: frozenset[int] = frozenset(),
    deleted_edge: int | None = None,
) -> bool:
    remaining = [v for v in range(vertices) if v not in deleted_vertices]
    if not remaining:
        return True
    adjacency = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        if edge == deleted_edge:
            continue
        if left in deleted_vertices or right in deleted_vertices:
            continue
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = {remaining[0]}
    queue = deque((remaining[0],))
    while queue:
        vertex = queue.popleft()
        for other in adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return seen == set(remaining)


def contract(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    root: int,
):
    u, v = edges[root]
    vertex_map = {u: 0, v: 0}
    next_vertex = 1
    for vertex in range(vertices):
        if vertex not in (u, v):
            vertex_map[vertex] = next_vertex
            next_vertex += 1
    contracted = []
    old_indices = []
    u_side = []
    v_side = []
    for old_edge, (left, right) in enumerate(edges):
        if old_edge == root:
            continue
        edge = len(contracted)
        contracted.append((vertex_map[left], vertex_map[right]))
        old_indices.append(old_edge)
        if u in (left, right):
            u_side.append(edge)
        if v in (left, right):
            v_side.append(edge)
    assert len(u_side) == len(v_side) == 2
    return (
        vertices - 1,
        tuple(contracted),
        tuple(old_indices),
        tuple(u_side),
        tuple(v_side),
    )


def incidence(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


def parse_label(text: str) -> int:
    assert len(text) == 2 and text[0] != text[1]
    return (1 << int(text[0])) | (1 << int(text[1]))


def label_text(label: int) -> str:
    return "".join(str(i) for i in range(5) if (label >> i) & 1)


def permute_label(label: int, permutation: tuple[int, ...]) -> int:
    answer = 0
    for coordinate in range(5):
        if (label >> coordinate) & 1:
            answer |= 1 << permutation[coordinate]
    return answer


PERMUTED = {
    permutation: {
        label: permute_label(label, permutation)
        for label in LABELS
    }
    for permutation in PERMUTATIONS
}


def canonical(state: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(PERMUTED[permutation][label] for label in state)
        for permutation in PERMUTATIONS
    )


class DSU:
    def __init__(self, size: int):
        self.parent = list(range(size))

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def join(self, left: int, right: int) -> bool:
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return False
        self.parent[right] = left
        return True


def cycle_basis(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    active: tuple[int, ...],
) -> tuple[int, ...]:
    dsu = DSU(vertices)
    tree: list[list[tuple[int, int]]] = [[] for _ in range(vertices)]
    chords = []
    for edge in active:
        left, right = edges[edge]
        if dsu.join(left, right):
            tree[left].append((right, edge))
            tree[right].append((left, edge))
        else:
            chords.append(edge)
    basis = []
    for chord in chords:
        source, target = edges[chord]
        parent: dict[int, tuple[int, int | None]] = {
            source: (source, None)
        }
        queue = deque((source,))
        while target not in parent:
            vertex = queue.popleft()
            for other, edge in tree[vertex]:
                if other not in parent:
                    parent[other] = (vertex, edge)
                    queue.append(other)
        mask = 1 << chord
        vertex = target
        while vertex != source:
            previous, edge = parent[vertex]
            assert edge is not None
            mask |= 1 << edge
            vertex = previous
        basis.append(mask)
    return tuple(basis)


def even_masks(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    active: tuple[int, ...],
) -> tuple[int, ...]:
    basis = cycle_basis(vertices, edges, active)
    answer = []
    for selection in range(1, 1 << len(basis)):
        mask = 0
        for index, cycle in enumerate(basis):
            if (selection >> index) & 1:
                mask ^= cycle
        answer.append(mask)
    return tuple(answer)


def validate_flow(
    state: tuple[int, ...],
    rows: tuple[tuple[int, ...], ...],
) -> None:
    assert all(label in LABEL_SET for label in state)
    for row in rows:
        total = 0
        for edge in row:
            total ^= state[edge]
        assert total == 0


def enumerate_flows(
    edges: tuple[tuple[int, int], ...],
    rows: tuple[tuple[int, ...], ...],
) -> frozenset[tuple[int, ...]]:
    state = [0] * len(edges)
    answers: set[tuple[int, ...]] = set()

    def assign(edge: int, label: int, changed: list[int]) -> bool:
        if state[edge]:
            return state[edge] == label
        if label not in LABEL_SET:
            return False
        state[edge] = label
        changed.append(edge)
        pending = list(edges[edge])
        while pending:
            vertex = pending.pop()
            unassigned = [item for item in rows[vertex] if not state[item]]
            if len(unassigned) > 1:
                continue
            total = 0
            for item in rows[vertex]:
                total ^= state[item]
            if not unassigned:
                if total:
                    return False
            else:
                if total not in LABEL_SET:
                    return False
                forced = unassigned[0]
                state[forced] = total
                changed.append(forced)
                pending.extend(edges[forced])
        return True

    def visit() -> None:
        try:
            edge = state.index(0)
        except ValueError:
            result = tuple(state)
            validate_flow(result, rows)
            answers.add(canonical(result))
            return
        choices = (LABELS[0],) if not any(state) else LABELS
        for label in choices:
            changed: list[int] = []
            if assign(edge, label, changed):
                visit()
            for changed_edge in reversed(changed):
                state[changed_edge] = 0

    visit()
    return frozenset(answers)


def neighbours(
    state: tuple[int, ...],
    vertices: int,
    edges: tuple[tuple[int, int], ...],
) -> frozenset[tuple[int, ...]]:
    answer = set()
    for pair in LABELS:
        active = tuple(
            edge
            for edge, label in enumerate(state)
            if (label & pair).bit_count() == 1
        )
        for mask in even_masks(vertices, edges, active):
            switched = list(state)
            for edge in range(len(edges)):
                if (mask >> edge) & 1:
                    switched[edge] ^= pair
                    assert switched[edge] in LABEL_SET
            answer.add(canonical(tuple(switched)))
    return frozenset(answer)


def orbit(
    initial: tuple[int, ...],
    vertices: int,
    edges: tuple[tuple[int, int], ...],
) -> frozenset[tuple[int, ...]]:
    seen = {initial}
    queue = deque((initial,))
    while queue:
        state = queue.popleft()
        for other in neighbours(state, vertices, edges):
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return frozenset(seen)


def state_text(state: tuple[int, ...]) -> str:
    return ",".join(label_text(label) for label in state)


def main() -> None:
    vertices, edges = decode_graph6(GRAPH6)
    assert vertices == 14 and len(edges) == 21
    assert len(set(edges)) == len(edges)
    original_rows = incidence(vertices, edges)
    assert all(len(row) == 3 for row in original_rows)
    assert connected_after_deleting(vertices, edges)
    assert all(
        connected_after_deleting(vertices, edges, deleted_edge=edge)
        for edge in range(len(edges))
    )
    # This witness is actually 3-vertex-connected, stronger than needed.
    assert all(
        connected_after_deleting(vertices, edges, frozenset(deleted))
        for size in (1, 2)
        for deleted in combinations(range(vertices), size)
    )

    (
        contracted_vertices,
        contracted_edges,
        old_indices,
        u_side,
        v_side,
    ) = contract(vertices, edges, CONTRACTED_EDGE)
    assert contracted_vertices == 13
    assert len(contracted_edges) == 20
    rows = incidence(contracted_vertices, contracted_edges)
    assert sorted(map(len, rows)) == [3] * 12 + [4]
    assert u_side == (5, 11)
    assert v_side == (15, 16)

    witness = canonical(tuple(parse_label(text) for text in WITNESS_TEXT))
    validate_flow(witness, rows)

    def good(state: tuple[int, ...]) -> bool:
        left = state[u_side[0]] ^ state[u_side[1]]
        right = state[v_side[0]] ^ state[v_side[1]]
        assert left == right
        return left.bit_count() == 2

    bad_orbit = orbit(
        witness,
        contracted_vertices,
        contracted_edges,
    )
    assert len(bad_orbit) == 12
    assert not any(map(good, bad_orbit))
    assert Counter(
        (state[u_side[0]] ^ state[u_side[1]]).bit_count()
        for state in bad_orbit
    ) == Counter({4: 12})
    # Structural reason that the fifth coordinate cannot enter this orbit:
    # every state uses four coordinates, and each used coordinate class is
    # one circuit.  A switch against the missing coordinate can therefore
    # only swap the two coordinate names on that whole circuit.
    for state in bad_orbit:
        used = {
            coordinate
            for label in state
            for coordinate in range(5)
            if (label >> coordinate) & 1
        }
        assert len(used) == 4
        missing = next(iter(set(range(5)) - used))
        for coordinate in used:
            active = tuple(
                edge
                for edge, label in enumerate(state)
                if (label >> coordinate) & 1
            )
            masks = even_masks(
                contracted_vertices,
                contracted_edges,
                active,
            )
            assert masks == (sum(1 << edge for edge in active),)
            pair = (1 << coordinate) | (1 << missing)
            switched = list(state)
            for edge in active:
                switched[edge] ^= pair
            assert canonical(tuple(switched)) == state

    all_flows = enumerate_flows(contracted_edges, rows)
    assert len(all_flows) == 1_681
    assert bad_orbit <= all_flows
    remaining = set(all_flows - bad_orbit)
    good_orbit = orbit(
        next(iter(remaining)),
        contracted_vertices,
        contracted_edges,
    )
    assert len(good_orbit) == 1_669
    assert good_orbit == remaining
    good_count = sum(map(good, good_orbit))
    assert good_count > 0

    ordered_bad = sorted(bad_orbit)
    bad_index = {state: index for index, state in enumerate(ordered_bad)}
    adjacency = []
    for state in ordered_bad:
        row = sorted(
            bad_index[other]
            for other in neighbours(
                state,
                contracted_vertices,
                contracted_edges,
            )
            if other != state
        )
        adjacency.append(tuple(row))
        assert all(other in bad_orbit for other in neighbours(
            state,
            contracted_vertices,
            contracted_edges,
        ))

    orbit_digest = sha256(
        "\n".join(state_text(state) for state in ordered_bad).encode()
    ).hexdigest()
    assert orbit_digest == "6aee922a63835496506597e93a1a600314b59583f28e0617e90978c9688858e3"

    print(f"graph6: {GRAPH6}")
    print(f"original edges: {list(enumerate(edges))}")
    print(
        "contracted edge:",
        CONTRACTED_EDGE,
        edges[CONTRACTED_EDGE],
        "u-side",
        u_side,
        "v-side",
        v_side,
    )
    print(f"contracted old-edge order: {old_indices}")
    print(f"normalized D5 flows: {len(all_flows)}")
    print(
        "generalized orbit sizes:",
        sorted((len(bad_orbit), len(good_orbit))),
    )
    print(f"good states in large orbit: {good_count}")
    print(f"bad orbit SHA256: {orbit_digest}")
    print("complete bad-orbit certificate:")
    for index, state in enumerate(ordered_bad):
        side_xor = state[u_side[0]] ^ state[u_side[1]]
        print(
            f"  {index:02d}: {state_text(state)}"
            f"  xor={label_text(side_xor)}"
            f"  neighbours={adjacency[index]}"
        )
    print("PASS")


if __name__ == "__main__":
    main()
