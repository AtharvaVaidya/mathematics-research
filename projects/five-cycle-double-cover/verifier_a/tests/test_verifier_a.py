from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path
import tempfile
import unittest

from verifier_a.core import (
    FORMAT,
    Edge,
    Graph,
    GraphFormatError,
    ModelFormatError,
    build_cnf,
    canonical_graph_bytes,
    check_assignment,
    check_premises,
    clauses_satisfied,
    extend_gate_assignment,
    parse_graph_text,
    parse_model_text,
    render_cnf,
    render_xor_dimacs,
    x_variable,
)


def graph_text(vertices, endpoint_pairs):
    return json.dumps(
        {
            "format": FORMAT,
            "vertices": vertices,
            "edges": [
                {"id": edge_id, "u": u, "v": v}
                for edge_id, (u, v) in enumerate(endpoint_pairs)
            ],
        }
    )


def exact_two_assignment(graph, pair=(1, 2)):
    return {
        x_variable(edge.id, coordinate): coordinate in pair
        for edge in graph.edges
        for coordinate in range(1, 6)
    }


class GraphFormatTests(unittest.TestCase):
    def test_canonical_round_trip(self):
        graph = parse_graph_text(graph_text(2, [(0, 0), (0, 1), (0, 1)]))
        self.assertEqual(parse_graph_text(canonical_graph_bytes(graph)), graph)
        self.assertTrue(canonical_graph_bytes(graph).endswith(b"\n"))

    def test_malformed_cases(self):
        bad_objects = [
            {"format": FORMAT, "vertices": True, "edges": []},
            {
                "format": FORMAT,
                "vertices": 1,
                "edges": [{"id": 0, "u": 0, "v": 1}],
            },
            {
                "format": FORMAT,
                "vertices": 2,
                "edges": [{"id": 1, "u": 0, "v": 1}],
            },
            {
                "format": FORMAT,
                "vertices": 2,
                "edges": [{"id": 0, "u": 1, "v": 0}],
            },
            {"format": FORMAT, "vertices": 0, "edges": [], "extra": 1},
        ]
        for obj in bad_objects:
            with self.subTest(obj=obj):
                with self.assertRaises(GraphFormatError):
                    parse_graph_text(json.dumps(obj))
        with self.assertRaises(GraphFormatError):
            parse_graph_text(
                '{"format":"five-cdc-multigraph-v1","vertices":0,'
                '"vertices":0,"edges":[]}'
            )


class PremiseTests(unittest.TestCase):
    def test_empty_graph(self):
        graph = parse_graph_text(graph_text(0, []))
        result = check_premises(graph)
        self.assertTrue(result.bridgeless)
        self.assertFalse(result.connected)
        self.assertEqual(result.components, ())

    def test_loop(self):
        graph = parse_graph_text(graph_text(1, [(0, 0)]))
        result = check_premises(graph)
        self.assertTrue(result.bridgeless)
        self.assertTrue(result.connected)
        self.assertEqual(result.bridge_ids, ())

    def test_parallel_edges(self):
        graph = parse_graph_text(graph_text(2, [(0, 1), (0, 1)]))
        result = check_premises(graph)
        self.assertTrue(result.bridgeless)
        self.assertEqual(result.components, ((0, 1),))

    def test_parallel_pair_beside_bridge(self):
        graph = parse_graph_text(graph_text(3, [(0, 1), (0, 1), (1, 2)]))
        result = check_premises(graph)
        self.assertEqual(result.bridge_ids, (2,))

    def test_bridge(self):
        graph = parse_graph_text(graph_text(3, [(0, 1), (1, 2)]))
        result = check_premises(graph)
        self.assertFalse(result.bridgeless)
        self.assertEqual(result.bridge_ids, (0, 1))

    def test_bridge_check_does_not_depend_on_recursion_limit(self):
        size = 1500
        graph = Graph(
            size,
            tuple(Edge(edge_id, edge_id, edge_id + 1)
                  for edge_id in range(size - 1)),
        )
        result = check_premises(graph)
        self.assertEqual(result.bridge_ids, tuple(range(size - 1)))

    def test_circuit(self):
        graph = parse_graph_text(graph_text(3, [(0, 1), (0, 2), (1, 2)]))
        self.assertTrue(check_premises(graph).bridgeless)
        self.assertTrue(check_assignment(graph, exact_two_assignment(graph)).valid)

    def test_disconnected_bridgeless_components(self):
        graph = parse_graph_text(
            graph_text(
                6,
                [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5)],
            )
        )
        result = check_premises(graph)
        self.assertTrue(result.bridgeless)
        self.assertFalse(result.connected)
        self.assertEqual(result.components, ((0, 1, 2), (3, 4, 5)))

    def test_petersen(self):
        endpoints = [
            (0, 1), (1, 2), (2, 3), (3, 4), (0, 4),
            (5, 7), (7, 9), (6, 9), (6, 8), (5, 8),
            (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
        ]
        graph = parse_graph_text(graph_text(10, endpoints))
        result = check_premises(graph)
        self.assertTrue(result.bridgeless)
        self.assertEqual(len(graph.edges), 15)
        self.assertEqual(build_cnf(graph).base_variables, 75)


class EncodingTests(unittest.TestCase):
    def test_loop_cancels_from_parity(self):
        graph = parse_graph_text(graph_text(1, [(0, 0)]))
        encoding = build_cnf(graph)
        self.assertEqual(encoding.variables, 5)
        self.assertEqual(len(encoding.clauses), 15)
        assignment = exact_two_assignment(graph, (2, 5))
        self.assertTrue(check_assignment(graph, assignment).valid)
        self.assertTrue(clauses_satisfied(encoding.clauses, assignment))
        xor_text = render_xor_dimacs(graph)
        self.assertNotIn("\nx ", xor_text)

    def test_exact_two_encoding_all_assignments(self):
        graph = parse_graph_text(graph_text(1, [(0, 0)]))
        encoding = build_cnf(graph)
        for mask in range(32):
            assignment = {
                variable: bool(mask & (1 << (variable - 1)))
                for variable in range(1, 6)
            }
            expected = sum(assignment.values()) == 2
            self.assertEqual(
                clauses_satisfied(encoding.clauses, assignment), expected
            )

    def test_projection_equivalence_on_two_parallel_edges(self):
        graph = parse_graph_text(graph_text(2, [(0, 1), (0, 1)]))
        encoding = build_cnf(graph)
        for first in combinations(range(1, 6), 2):
            for second in combinations(range(1, 6), 2):
                assignment = {}
                for coordinate in range(1, 6):
                    assignment[x_variable(0, coordinate)] = coordinate in first
                    assignment[x_variable(1, coordinate)] = coordinate in second
                extended = extend_gate_assignment(encoding, assignment)
                semantic = check_assignment(graph, assignment).valid
                self.assertEqual(
                    clauses_satisfied(encoding.clauses, extended), semantic
                )

    def test_cnf_header_counts(self):
        graph = parse_graph_text(graph_text(3, [(0, 1), (0, 2), (1, 2)]))
        encoding = build_cnf(graph)
        cnf = render_cnf(graph)
        self.assertIn(
            "p cnf {} {}".format(encoding.variables, len(encoding.clauses)),
            cnf,
        )

    def test_xor_dimacs_even_equation_convention(self):
        graph = parse_graph_text(graph_text(2, [(0, 1), (0, 1)]))
        text = render_xor_dimacs(graph)
        self.assertIn("x -1 6 0", text)
        header = next(line for line in text.splitlines() if line.startswith("p "))
        self.assertEqual(header, "p cnf 10 40")


class ModelTests(unittest.TestCase):
    def test_parse_and_check_model(self):
        graph = parse_graph_text(graph_text(3, [(0, 1), (0, 2), (1, 2)]))
        assignment = exact_two_assignment(graph)
        literals = [
            str(variable if value else -variable)
            for variable, value in sorted(assignment.items())
        ]
        parsed = parse_model_text(
            "s SATISFIABLE\nv " + " ".join(literals) + " 0\n",
            required_base_variables=15,
            maximum_variable=30,
        )
        self.assertTrue(check_assignment(graph, parsed).valid)

    def test_incomplete_and_contradictory_models(self):
        with self.assertRaises(ModelFormatError):
            parse_model_text("s SATISFIABLE\nv 1 0\n", 2, 2)
        with self.assertRaises(ModelFormatError):
            parse_model_text("s SATISFIABLE\nv 1 -1 0\n", 1, 1)
        with self.assertRaises(ModelFormatError):
            parse_model_text("s UNSATISFIABLE\n", 0, 0)

    def test_bad_semantic_model_is_rejected(self):
        graph = parse_graph_text(graph_text(1, [(0, 0)]))
        assignment = {variable: False for variable in range(1, 6)}
        result = check_assignment(graph, assignment)
        self.assertFalse(result.valid)
        self.assertEqual(result.exact_two_failures, (0,))


if __name__ == "__main__":
    unittest.main()
