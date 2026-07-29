#!/usr/bin/env python3
"""Clean-room audit of the 16-vertex Blanusa six-pole relation.

This checker does not import the construction, enumerator, or CNF producer.
It checks all positive witnesses directly, independently reconstructs the
CNF for the 16 negative representatives, and runs two LRAT checkers.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product
import json
import os
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
EXPECTED_NEGATIVE_ORBITS = (
    80, 81, 117, 118, 143, 144, 147, 148,
    200, 201, 206, 207, 254, 255, 318, 319,
)
DUADS = tuple(
    sum(1 << coordinate for coordinate in pair)
    for pair in combinations(range(5), 2)
)


def load_pole():
    raw = [
        int(token)
        for token in (HERE / "small-pole.txt").read_text(
            encoding="ascii"
        ).split()
    ]
    if raw[:3] != [16, 21, 6]:
        raise AssertionError("wrong small-pole header")
    ports = raw[3:9]
    endpoints = raw[9:]
    if len(endpoints) != 42:
        raise AssertionError("wrong small-pole edge payload")
    edges = [
        (endpoints[index], endpoints[index + 1])
        for index in range(0, len(endpoints), 2)
    ]
    if len(ports) != len(set(ports)) or len(ports) != 6:
        raise AssertionError("ports are not six distinct vertices")
    canonical_edges = {
        tuple(sorted(edge))
        for edge in edges
    }
    if (
        len(canonical_edges) != 21
        or any(left == right for left, right in edges)
        or any(not 0 <= endpoint < 16 for edge in edges for endpoint in edge)
    ):
        raise AssertionError("small pole is not a simple 16-vertex graph")
    incidence = [[] for _ in range(16)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    port_set = set(ports)
    degree_census = Counter(len(row) for row in incidence)
    if degree_census != Counter({3: 10, 2: 6}):
        raise AssertionError("wrong pole degree census")
    if {v for v, row in enumerate(incidence) if len(row) == 2} != port_set:
        raise AssertionError("the port list is not the degree-two set")
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for edge in incidence[vertex]:
            left, right = edges[edge]
            other = right if left == vertex else left
            if other not in seen:
                seen.add(other)
                stack.append(other)
    if len(seen) != 16:
        raise AssertionError("small pole is disconnected")
    return ports, edges, incidence


def coordinate_actions():
    answer = []
    for permutation in permutations(range(5)):
        table = []
        for mask in range(32):
            image = 0
            for coordinate in range(5):
                if mask & (1 << coordinate):
                    image |= 1 << permutation[coordinate]
            table.append(image)
        answer.append(tuple(table))
    return tuple(answer)


def verify_representatives():
    document = json.loads(
        (HERE / "s5-representatives.json").read_text(encoding="ascii")
    )
    if tuple(document["duads"]) != DUADS:
        raise AssertionError("wrong frozen duad list")
    representatives = [
        tuple(word)
        for word in document["representatives"]
    ]
    if representatives != sorted(representatives) or len(representatives) != 571:
        raise AssertionError("wrong representative list")
    universe = {
        word
        for word in product(DUADS, repeat=6)
        if word[0] ^ word[1] ^ word[2] ^ word[3] ^ word[4] ^ word[5] == 0
    }
    if len(universe) != 62560:
        raise AssertionError("wrong xor-zero universe size")
    actions = coordinate_actions()
    covered = set()
    for representative in representatives:
        orbit = {
            tuple(action[label] for label in representative)
            for action in actions
        }
        if covered.intersection(orbit):
            raise AssertionError("overlapping frozen S5 representatives")
        covered.update(orbit)
    if covered != universe:
        raise AssertionError("representatives do not partition the universe")
    return representatives


def verify_relation_rows(representatives, ports, incidence):
    rows = [
        json.loads(line)
        for line in (HERE / "boundary-relation.jsonl").read_text(
            encoding="ascii"
        ).splitlines()
    ]
    if len(rows) != 571:
        raise AssertionError("wrong relation row count")
    statuses = Counter(row.get("status") for row in rows)
    if statuses != Counter({
        "SAT_SEMANTIC_CHECK": 555,
        "UNSAT_UNCERTIFIED": 16,
    }):
        raise AssertionError("wrong relation status census")
    negative = []
    allowed = set(DUADS)
    for orbit, (representative, row) in enumerate(
        zip(representatives, rows, strict=True)
    ):
        if row.get("orbit") != orbit:
            raise AssertionError("relation orbit order changed")
        if tuple(row.get("boundary", ())) != representative:
            raise AssertionError("boundary representative changed")
        if row["status"] == "UNSAT_UNCERTIFIED":
            negative.append((orbit, representative))
            continue
        labels = row.get("labels")
        if (
            not isinstance(labels, list)
            or len(labels) != 27
            or any(label not in allowed for label in labels)
        ):
            raise AssertionError(f"invalid positive witness at orbit {orbit}")
        if tuple(labels[21:]) != representative:
            raise AssertionError(f"wrong boundary at orbit {orbit}")
        completed_incidence = [list(row) for row in incidence]
        for port, vertex in enumerate(ports):
            completed_incidence[vertex].append(21 + port)
        if any(
            labels[row[0]] ^ labels[row[1]] ^ labels[row[2]]
            for row in completed_incidence
        ):
            raise AssertionError(f"xor failure in witness orbit {orbit}")
    if tuple(orbit for orbit, _ in negative) != EXPECTED_NEGATIVE_ORBITS:
        raise AssertionError("wrong negative orbit indices")
    return negative


def parse_cnf():
    comments = []
    clauses = []
    variables = None
    declared_clauses = None
    for line in (HERE / "negative-boundary-orbits.cnf").read_text(
        encoding="ascii"
    ).splitlines():
        if line.startswith("c "):
            comments.append(line)
        elif line.startswith("p cnf "):
            _, _, variables_text, clauses_text = line.split()
            variables = int(variables_text)
            declared_clauses = int(clauses_text)
        else:
            entries = tuple(map(int, line.split()))
            if not entries or entries[-1] != 0 or 0 in entries[:-1]:
                raise AssertionError("malformed CNF clause")
            clauses.append(entries[:-1])
    if (variables, declared_clauses, len(clauses)) != (121, 1476, 1476):
        raise AssertionError("wrong CNF dimensions")
    if any(abs(literal) > variables for clause in clauses for literal in clause):
        raise AssertionError("CNF literal out of range")
    return clauses


def block_assignment(variables, bits):
    return tuple(
        (-variable if bit else variable)
        for variable, bit in zip(variables, bits, strict=True)
    )


def expected_cnf(negative, ports, incidence):
    clauses = []
    # Edge variables 5e+c+1 have Hamming weight exactly two.
    for edge in range(21):
        coordinates = tuple(5 * edge + coordinate + 1 for coordinate in range(5))
        for chosen in combinations(coordinates, 3):
            clauses.append(tuple(-variable for variable in chosen))
        for chosen in combinations(coordinates, 4):
            clauses.append(chosen)

    port_number = {vertex: index for index, vertex in enumerate(ports)}
    for vertex, row in enumerate(incidence):
        if vertex in port_number:
            continue
        for coordinate in range(5):
            variables = tuple(5 * edge + coordinate + 1 for edge in row)
            for bits in product((0, 1), repeat=3):
                if sum(bits) & 1:
                    clauses.append(block_assignment(variables, bits))

    selectors = tuple(range(106, 122))
    clauses.append(selectors)
    for selector, (_, boundary) in zip(selectors, negative, strict=True):
        for vertex in ports:
            port = port_number[vertex]
            for coordinate in range(5):
                variables = tuple(
                    5 * edge + coordinate + 1
                    for edge in incidence[vertex]
                )
                target = (boundary[port] >> coordinate) & 1
                for bits in product((0, 1), repeat=2):
                    if (sum(bits) & 1) != target:
                        clauses.append(
                            (-selector, *block_assignment(variables, bits))
                        )
    return clauses


def locate_checkers():
    roots = []
    configured = os.environ.get("FIVECDC_TOOLS")
    if configured:
        roots.append(Path(configured))
    roots.append(
        Path("/Users/atharvavaidya/Documents/conjectures/.tools")
    )
    for root in roots:
        lrat = root / "cert-checkers/drat-trim/lrat-check"
        cake = root / "cert-checkers/cake_lpr/cake_lpr"
        if lrat.is_file() and cake.is_file():
            return lrat, cake
    raise FileNotFoundError("set FIVECDC_TOOLS to the checker tool root")


def main() -> int:
    ports, _, incidence = load_pole()
    representatives = verify_representatives()
    negative = verify_relation_rows(representatives, ports, incidence)
    frozen_clauses = parse_cnf()
    reconstructed = expected_cnf(negative, ports, incidence)
    if frozen_clauses != reconstructed:
        raise AssertionError("CNF differs from independent reconstruction")

    lrat, cake = locate_checkers()
    proof = HERE / "negative-boundary-orbits.lrat"
    cnf = HERE / "negative-boundary-orbits.cnf"
    subprocess.run([str(lrat), str(cnf), str(proof)], check=True)
    subprocess.run([str(cake), str(cnf), str(proof)], check=True)
    print("PASS exact 16-vertex Blanusa six-pole relation")
    print("positive_s5_orbits=555 negative_s5_orbits=16")
    print("positive_witnesses=555 checked_vertex_xors=44400")
    print("negative_selector_cnf=121_variables,1476_clauses")
    print("negative_LRAT=lrat-check_PASS,cake_lpr_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
