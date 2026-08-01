#!/usr/bin/env python3
"""Check the unbounded b* family from even bipyramid flag graphs.

For every even n >= 4, the flag graph of the n-gonal bipyramid has a
Tait-supported D5 state and a fixed ordered root pair with

    distance = 2,  b* = n/2 - 1.

The human proof is in d5-closed-cage-forced-inequalities.md.  This
standard-library checker reconstructs and exhausts the exact shortest
profiles for several requested family members.
"""

from __future__ import annotations

import argparse
from collections import deque
from itertools import combinations


PAIRS = tuple(combinations(range(5), 2))


class Witness:
    def __init__(self, n: int):
        assert n >= 4 and n % 2 == 0
        self.n = n
        apex_top, apex_bottom = n, n + 1
        faces = []
        for index in range(n):
            following = (index + 1) % n
            faces.append((apex_top, index, following))
            faces.append((apex_bottom, following, index))
        self.faces = tuple(faces)
        self.flags = tuple(
            (face, side, endpoint)
            for face in range(2 * n)
            for side in range(3)
            for endpoint in range(2)
        )
        flag_id = {flag: index for index, flag in enumerate(self.flags)}

        side_owners = {}
        for face, row in enumerate(self.faces):
            for side in range(3):
                left, right = row[side], row[(side + 1) % 3]
                side_owners.setdefault(
                    tuple(sorted((left, right))), []
                ).append((face, side, left, right))
        assert all(len(owners) == 2 for owners in side_owners.values())

        def r0(flag):
            face, side, endpoint = flag
            return face, side, 1 - endpoint

        def r1(flag):
            face, side, endpoint = flag
            if endpoint == 0:
                return face, (side - 1) % 3, 1
            return face, (side + 1) % 3, 0

        def r2(flag):
            face, side, endpoint = flag
            row = self.faces[face]
            actual = row[side] if endpoint == 0 else row[(side + 1) % 3]
            owners = side_owners[
                tuple(sorted((row[side], row[(side + 1) % 3])))
            ]
            other = owners[0] if owners[1][0] == face else owners[1]
            other_face, other_side, left, right = other
            return other_face, other_side, 0 if left == actual else 1

        self.matchings = tuple(
            frozenset(
                tuple(sorted((flag_id[flag], flag_id[involution(flag)])))
                for flag in self.flags
            )
            for involution in (r0, r1, r2)
        )
        assert all(
            len(matching) == len(self.flags) // 2
            for matching in self.matchings
        )
        assert not (self.matchings[0] & self.matchings[1])
        assert not (self.matchings[0] & self.matchings[2])
        assert not (self.matchings[1] & self.matchings[2])

        self.edges = tuple(sorted(set().union(*self.matchings)))
        self.edge_id = {
            edge: index for index, edge in enumerate(self.edges)
        }
        self.incidence = [[] for _ in self.flags]
        for edge, (left, right) in enumerate(self.edges):
            self.incidence[left].append(edge)
            self.incidence[right].append(edge)

        edge_label = {}
        for matching, label in zip(
            self.matchings, (0x03, 0x05, 0x06), strict=True
        ):
            for edge in matching:
                edge_label[edge] = label
        self.state = tuple(edge_label[edge] for edge in self.edges)

        # r is the r1 corner at the top apex in top face 0.
        root = self.edge_id[(0, 5)]
        # s is the r0 side at the top apex in the opposite top face.
        opposite_face = n
        target_flag = 6 * opposite_face
        target = self.edge_id[(target_flag, target_flag + 1)]
        self.roots = (root, target)

        self.rows = self.factors()
        self.row_adjacency = [[] for _ in self.rows]
        for left in range(len(self.rows)):
            for right in range(left + 1, len(self.rows)):
                if self.rows[left][1] & self.rows[right][1]:
                    self.row_adjacency[left].append(right)
                    self.row_adjacency[right].append(left)

    def edge_components(self, mask: int) -> tuple[int, ...]:
        answer = []
        unseen = mask
        while unseen:
            bit = unseen & -unseen
            unseen ^= bit
            component = bit
            queue = deque([bit.bit_length() - 1])
            while queue:
                edge = queue.popleft()
                for endpoint in self.edges[edge]:
                    for other in self.incidence[endpoint]:
                        other_bit = 1 << other
                        if unseen & other_bit:
                            unseen ^= other_bit
                            component |= other_bit
                            queue.append(other)
            answer.append(component)
        return tuple(answer)

    def factors_for_state(self, state: tuple[int, ...]):
        answer = []
        for pair in PAIRS:
            pair_mask = (1 << pair[0]) | (1 << pair[1])
            active = sum(
                1 << edge
                for edge, label in enumerate(state)
                if (label & pair_mask).bit_count() == 1
            )
            answer.extend(
                (pair, component)
                for component in self.edge_components(active)
            )
        return tuple(answer)

    def factors(self):
        return self.factors_for_state(self.state)

    def circuit_order(self, component: int, root: int) -> tuple[int, ...]:
        selected = {
            edge
            for edge in range(len(self.edges))
            if (component >> edge) & 1
        }

        def adjacent(edge):
            return sorted(
                other
                for endpoint in self.edges[edge]
                for other in self.incidence[endpoint]
                if other != edge and other in selected
            )

        assert all(len(adjacent(edge)) == 2 for edge in selected)
        answer = [root]
        previous = root
        current = adjacent(root)[0]
        while current != root:
            answer.append(current)
            choices = adjacent(current)
            following = choices[0] if choices[0] != previous else choices[1]
            previous, current = current, following
        assert len(answer) == len(selected)
        return tuple(answer)

    def distances_to_target(self) -> list[int]:
        target = self.roots[1]
        distance = [10**9] * len(self.rows)
        queue = deque()
        for index, (_, component) in enumerate(self.rows):
            if (component >> target) & 1:
                distance[index] = 1
                queue.append(index)
        while queue:
            current = queue.popleft()
            for other in self.row_adjacency[current]:
                if distance[other] == 10**9:
                    distance[other] = distance[current] + 1
                    queue.append(other)
        return distance

    def profile(self, first: int, second: int):
        pair_p, circuit = self.rows[first]
        pair_q, target_component = self.rows[second]
        if len(set(pair_p) & set(pair_q)) != 1:
            return None
        root = self.roots[0]
        q_rows = [
            (index, component)
            for index, (pair, component) in enumerate(self.rows)
            if pair == pair_q
        ]
        root_rows = [
            (index, component)
            for index, component in q_rows
            if (component >> root) & 1
        ]
        assert len(root_rows) <= 1
        if not root_rows or root_rows[0][0] == second:
            return None
        root_index, root_component = root_rows[0]

        owner = {}
        for index, component in q_rows:
            common = circuit & component
            while common:
                bit = common & -common
                common ^= bit
                edge = bit.bit_length() - 1
                assert edge not in owner
                owner[edge] = index

        order = self.circuit_order(circuit, root)
        size = len(order)
        scans = []
        for step in (1, -1):
            cursor = step
            while owner.get(order[cursor % size]) == root_index:
                cursor += step
            blockers = []
            previous = object()
            while abs(cursor) <= size:
                edge = order[cursor % size]
                current = owner.get(edge)
                if current != previous:
                    if current == second:
                        scans.append((tuple(blockers), edge))
                        break
                    if current is not None and current != root_index:
                        blockers.append(current)
                previous = current
                cursor += step
            else:
                raise AssertionError("target component not reached")
        return {
            "P": pair_p,
            "Q": pair_q,
            "C": circuit,
            "H": root_component,
            "D": target_component,
            "order": order,
            "scans": tuple(scans),
            "blockers": min(len(scan[0]) for scan in scans),
        }

    def metric(self):
        target_distance = self.distances_to_target()
        source_rows = [
            index
            for index, (_, component) in enumerate(self.rows)
            if (component >> self.roots[0]) & 1
        ]
        distance = min(target_distance[index] for index in source_rows)
        profiles = []
        for first in source_rows:
            for second in self.row_adjacency[first]:
                if 1 + target_distance[second] != distance:
                    continue
                candidate = self.profile(first, second)
                if candidate is not None:
                    profiles.append(candidate)
        blocker = min(
            candidate["blockers"] for candidate in profiles
        )
        return distance, blocker, tuple(profiles)

    def connected_without_edge(self, omitted: int) -> bool:
        seen = {0}
        queue = deque([0])
        while queue:
            current = queue.popleft()
            for edge in self.incidence[current]:
                if edge == omitted:
                    continue
                left, right = self.edges[edge]
                other = left ^ right ^ current
                if other not in seen:
                    seen.add(other)
                    queue.append(other)
        return len(seen) == len(self.flags)

    def surface_chi(self, state: tuple[int, ...]) -> int:
        coordinate_circuits = 0
        for coordinate in range(5):
            mask = sum(
                1 << edge
                for edge, label in enumerate(state)
                if (label >> coordinate) & 1
            )
            coordinate_circuits += len(self.edge_components(mask))
        return coordinate_circuits - len(self.edges) + len(self.flags)

    def delta_histogram(self) -> dict[int, int]:
        level = self.surface_chi(self.state)
        answer: dict[int, int] = {}
        for pair, component in self.rows:
            pair_mask = (1 << pair[0]) | (1 << pair[1])
            other = tuple(
                label ^ pair_mask if (component >> edge) & 1 else label
                for edge, label in enumerate(self.state)
            )
            delta = self.surface_chi(other) - level
            answer[delta] = answer.get(delta, 0) + 1
        return answer

    def validate(self):
        assert len(self.flags) == 12 * self.n
        assert len(self.edges) == 18 * self.n
        assert len(set(self.edges)) == len(self.edges)
        assert all(left != right for left, right in self.edges)
        assert all(len(row) == 3 for row in self.incidence)
        assert self.connected_without_edge(-1)
        assert all(
            self.connected_without_edge(edge)
            for edge in range(len(self.edges))
        )
        assert all(label.bit_count() == 2 for label in self.state)
        assert all(
            self.state[row[0]] ^ self.state[row[1]] ^ self.state[row[2]]
            == 0
            for row in self.incidence
        )
        distance, blocker, profiles = self.metric()
        expected = self.n // 2 - 1
        assert (distance, blocker) == (2, expected)
        assert len(profiles) == 7
        assert all(candidate["blockers"] == expected for candidate in profiles)
        expected_histogram = {
            0: 12 * self.n + 4,
            -2: 3 * self.n,
            -4: 2 * self.n,
            -6: self.n,
        }
        apex_delta = -(2 * self.n - 2)
        expected_histogram[apex_delta] = (
            expected_histogram.get(apex_delta, 0) + 2
        )
        assert self.surface_chi(self.state) == 2
        assert self.delta_histogram() == expected_histogram

        # One neutral fresh-coordinate switch on the apex C_2 circuit
        # rescues the roots, independently of its unbounded b* value.
        coordinate_two = sum(
            1 << edge
            for edge, label in enumerate(self.state)
            if (label >> 2) & 1
        )
        apex_components = [
            component
            for component in self.edge_components(coordinate_two)
            if (component >> self.roots[0]) & 1
        ]
        assert len(apex_components) == 1
        apex = apex_components[0]
        switch_mask = (1 << 2) | (1 << 4)
        rescued_state = tuple(
            label ^ switch_mask if (apex >> edge) & 1 else label
            for edge, label in enumerate(self.state)
        )
        assert self.surface_chi(rescued_state) == 2
        rescue_components = [
            component
            for pair, component in self.factors_for_state(rescued_state)
            if pair == (0, 2)
            and (component >> self.roots[0]) & 1
            and (component >> self.roots[1]) & 1
        ]
        assert len(rescue_components) == 1
        return (
            distance,
            blocker,
            profiles,
            expected_histogram,
            apex,
            rescue_components[0],
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orders",
        default="4,6,8,10,12",
        help="comma-separated even bipyramid orders",
    )
    arguments = parser.parse_args()
    for text in arguments.orders.split(","):
        witness = Witness(int(text))
        (
            distance,
            blocker,
            profiles,
            histogram,
            apex,
            rescue,
        ) = witness.validate()
        print(
            "PASS",
            f"n={witness.n}",
            f"vertices={len(witness.flags)}",
            f"edges={len(witness.edges)}",
            f"roots={witness.roots}",
            f"distance={distance}",
            f"b*={blocker}",
            f"profiles={len(profiles)}",
            f"deltas={histogram}",
            f"neutral_24_apex_size={apex.bit_count()}",
            f"rescue_Y02_size={rescue.bit_count()}",
        )


if __name__ == "__main__":
    main()
