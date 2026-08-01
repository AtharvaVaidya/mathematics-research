#!/usr/bin/env python3
"""Search the two Blanusa snarks for an optimal refined-gate blocker."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from z3 import Bool, Not, Or, Solver, Xor, sat


SOURCE = (
    Path(__file__).resolve().parents[2]
    / "search/order22-filter-census-20260725/strict-snarks-through18.g6"
)


def decode_graph6(record):
    n = ord(record[0]) - 63
    bits = [
        (ord(character) - 63 >> shift) & 1
        for character in record[1:]
        for shift in range(5, -1, -1)
    ]
    pairs = tuple((u, v) for v in range(1, n) for u in range(v))
    return n, tuple(pair for pair, bit in zip(pairs, bits) if bit)


def make_rows(n, edges):
    answer = [[] for _ in range(n)]
    for edge, (u, v) in enumerate(edges):
        answer[u].append(edge)
        answer[v].append(edge)
    return tuple(tuple(row) for row in answer)


def xor_equals(items, value):
    expression = items[0]
    for item in items[1:]:
        expression = Xor(expression, item)
    return expression if value else Not(expression)


class SearchGraph:
    def __init__(self, record):
        self.record = record
        self.n, self.edges = decode_graph6(record)
        self.m = len(self.edges)
        self.rows = make_rows(self.n, self.edges)
        self.full = (1 << self.m) - 1

    def components(self, allowed):
        unseen = set(range(self.n))
        answer = []
        while unseen:
            root = min(unseen)
            unseen.remove(root)
            shore = {root}
            queue = [root]
            for vertex in queue:
                for edge in self.rows[vertex]:
                    if not ((allowed >> edge) & 1):
                        continue
                    u, v = self.edges[edge]
                    other = u ^ v ^ vertex
                    if other in unseen:
                        unseen.remove(other)
                        shore.add(other)
                        queue.append(other)
            answer.append(frozenset(shore))
        return tuple(answer)

    def cut(self, shore):
        return sum(
            1 << edge
            for edge, (u, v) in enumerate(self.edges)
            if (u in shore) != (v in shore)
        )

    def boundary(self, mask):
        return sum(
            (sum((mask >> edge) & 1 for edge in self.rows[v]) & 1) << v
            for v in range(self.n)
        )

    def cycle_basis(self, allowed):
        parent = list(range(self.n))

        def root(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        tree, chords = [], []
        for edge in range(self.m):
            if not ((allowed >> edge) & 1):
                continue
            u, v = self.edges[edge]
            ru, rv = root(u), root(v)
            if ru == rv:
                chords.append(edge)
            else:
                parent[rv] = ru
                tree.append(edge)
        tree_rows = [[] for _ in range(self.n)]
        for edge in tree:
            u, v = self.edges[edge]
            tree_rows[u].append(edge)
            tree_rows[v].append(edge)
        basis = []
        for chord in chords:
            source, target = self.edges[chord]
            previous = {source: (-1, -1)}
            queue = [source]
            for vertex in queue:
                if target in previous:
                    break
                for edge in tree_rows[vertex]:
                    u, v = self.edges[edge]
                    other = u ^ v ^ vertex
                    if other not in previous:
                        previous[other] = (vertex, edge)
                        queue.append(other)
            vector = 1 << chord
            vertex = target
            while vertex != source:
                vertex, edge = previous[vertex]
                vector ^= 1 << edge
            basis.append(vector)
        assert len(basis) == allowed.bit_count() - self.n + len(self.components(allowed))
        return tuple(basis)

    @staticmethod
    def span(basis):
        answer = [0]
        for vector in basis:
            answer += [old ^ vector for old in answer]
        return tuple(answer)

    def one_join(self, allowed, target):
        """Construct one allowed edge set with the requested boundary in O(n+m)."""
        tree_rows = [[] for _ in range(self.n)]
        parent = [-1] * self.n
        parent_edge = [-1] * self.n
        roots = []
        order = []
        for root in range(self.n):
            if parent[root] != -1:
                continue
            parent[root] = root
            roots.append(root)
            queue = [root]
            for vertex in queue:
                order.append(vertex)
                for edge in self.rows[vertex]:
                    if not ((allowed >> edge) & 1):
                        continue
                    u, v = self.edges[edge]
                    other = u ^ v ^ vertex
                    if parent[other] == -1:
                        parent[other] = vertex
                        parent_edge[other] = edge
                        tree_rows[vertex].append(edge)
                        tree_rows[other].append(edge)
                        queue.append(other)
        need = [(target >> vertex) & 1 for vertex in range(self.n)]
        answer = 0
        for vertex in reversed(order):
            if vertex == parent[vertex]:
                continue
            if need[vertex]:
                answer |= 1 << parent_edge[vertex]
                need[parent[vertex]] ^= 1
        if any(need[root] for root in roots):
            return None
        assert not (answer & ~allowed)
        assert self.boundary(answer) == target
        return answer

    def potential(self, data, matching):
        tight = second = 0
        for _shore, component_cut in data:
            q = (component_cut & matching).bit_count()
            d = component_cut.bit_count()
            if q & 1:
                tight += d == 4
                second += d - q
        return tight, second

    @lru_cache(maxsize=None)
    def optimum(self, matching):
        h = self.full ^ matching
        target = self.boundary(matching)
        base = self.one_join(h, target)
        assert base is not None
        records = []
        for cycle in self.span(self.cycle_basis(h)):
            join = base ^ cycle
            residual = self.full ^ (matching | join)
            data = tuple((shore, self.cut(shore)) for shore in self.components(residual))
            records.append((self.potential(data, matching), join, data))
        value = min(record[0] for record in records)
        return value, tuple(record for record in records if record[0] == value)

    def matchings(self):
        neighbours = [[] for _ in range(self.n)]
        edge_of = {}
        for edge, (u, v) in enumerate(self.edges):
            neighbours[u].append(v)
            neighbours[v].append(u)
            edge_of[u, v] = edge_of[v, u] = edge

        def rec(unprocessed, selected):
            if not unprocessed:
                yield selected
                return
            vertex = (unprocessed & -unprocessed).bit_length() - 1
            rest = unprocessed ^ (1 << vertex)
            yield from rec(rest, selected)
            for other in neighbours[vertex]:
                if (rest >> other) & 1:
                    yield from rec(
                        rest ^ (1 << other), selected | (1 << edge_of[vertex, other])
                    )

        yield from rec((1 << self.n) - 1, 0)

    def find_flow(self, matching):
        variables = [[Bool(f"x_{edge}_{bit}") for bit in range(3)] for edge in range(self.m)]
        solver = Solver()
        for edge in range(self.m):
            solver.add(Or(*variables[edge]))
            if (matching >> edge) & 1:
                solver.add(variables[edge][0], Not(variables[edge][1]), Not(variables[edge][2]))
            else:
                solver.add(Or(Not(variables[edge][0]), variables[edge][1], variables[edge][2]))
        for vertex in range(self.n):
            for bit in range(3):
                solver.add(xor_equals([variables[e][bit] for e in self.rows[vertex]], False))
        if solver.check() != sat:
            return None
        model = solver.model()
        flow = tuple(
            sum((1 << bit) * int(bool(model.evaluate(variables[edge][bit]))) for bit in range(3))
            for edge in range(self.m)
        )
        assert all(flow)
        assert {edge for edge, value in enumerate(flow) if value == 1} == {
            edge for edge in range(self.m) if (matching >> edge) & 1
        }
        return flow

    @staticmethod
    def partner_free(values, b=1):
        support = set(values)
        return tuple(sorted(value for value in support if (value ^ b) not in support))

    def direction(self, flow, matching, join, data, q_index, t):
        q_cut = data[q_index][1]
        e4 = tuple(
            component_cut
            for _shore, component_cut in data
            if component_cut.bit_count() == 4
            and not ((component_cut & matching).bit_count() & 1)
        )
        forbidden = sum(
            1 << edge
            for edge, value in enumerate(flow)
            if value == t or (value == (1 ^ t) and not ((join >> edge) & 1))
        )
        allowed = self.full ^ forbidden
        p = sum(1 << edge for edge, value in enumerate(flow) if value in (1, 1 ^ t))
        basis = self.cycle_basis(allowed)
        feasible = []
        selected_nonzero = False
        for cycle in self.span(basis):
            effect = (cycle & p & q_cut).bit_count() & 1
            selected_nonzero |= bool(effect)
            if not effect:
                continue
            if any((cycle & p & component_cut).bit_count() & 1 for component_cut in e4):
                continue
            target = matching
            for edge, value in enumerate(flow):
                if (cycle >> edge) & 1 and value in (1, 1 ^ t):
                    target ^= 1 << edge
            feasible.append((self.potential(data, target), cycle))
        return len(basis), selected_nonzero, len(feasible), min(feasible, default=None)


def main():
    records = [line.strip() for line in SOURCE.read_text().splitlines() if line.strip()]
    for graph_index, record in enumerate(records[1:], 1):
        graph = SearchGraph(record)
        assert graph.n == 18 and graph.m == 27
        matchings = larger = flowable = states = 0
        for matching in graph.matchings():
            matchings += 1
            if matching == 0:
                continue
            optimum, optimal_records = graph.optimum(matching)
            if optimum[0] != 0 or optimum[1] == 0:
                continue
            larger += 1
            flow = graph.find_flow(matching)
            if flow is None:
                continue
            flowable += 1
            for _value, join, data in optimal_records:
                states += 1
                for q_index, (_shore, q_cut) in enumerate(data):
                    if not ((q_cut & matching).bit_count() & 1):
                        continue
                    h_cut = q_cut & ~matching
                    k, q = h_cut.bit_count(), (q_cut & matching).bit_count()
                    if k >= 9:
                        continue
                    directions = graph.partner_free(
                        tuple(flow[e] for e in range(graph.m) if (h_cut >> e) & 1)
                    )
                    rows = tuple((t,) + graph.direction(flow, matching, join, data, q_index, t) for t in directions)
                    if rows and all(row[3] == 0 or row[4][0] >= optimum for row in rows):
                        print("FOUND")
                        print(f"graph_index={graph_index} graph6={record}")
                        print(f"matchings={matchings} larger={larger} flowable={flowable} states={states}")
                        print("flow=" + ",".join(map(str, flow)))
                        print("matching=" + ",".join(str(e) for e in range(graph.m) if (matching >> e) & 1))
                        print("join=" + ",".join(str(e) for e in range(graph.m) if (join >> e) & 1))
                        print(f"optimum={optimum} Q={q_index} shore={sorted(data[q_index][0])} profile=({k},{q})")
                        for row in rows:
                            print(f"direction t={row[0]} dim={row[1]} selected_nonzero={int(row[2])} feasible={row[3]} best={row[4]}")
                        return
        print(f"graph_index={graph_index} NO_BLOCKER matchings={matchings} larger={larger} flowable={flowable} states={states}")


if __name__ == "__main__":
    main()
