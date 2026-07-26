import json
from pathlib import Path
import tempfile
import unittest

from tools.encode_five_cdc_xor_fast import encode


class FastXorEncoderTests(unittest.TestCase):
    def test_parallel_edges_and_loop_have_incidence_multiplicity_semantics(self) -> None:
        graph = {
            "format": "five-cdc-multigraph-v1",
            "vertices": 2,
            "edges": [
                {"id": 0, "u": 0, "v": 1},
                {"id": 1, "u": 0, "v": 1},
                {"id": 2, "u": 0, "v": 0},
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            graph_path = root / "graph.json"
            graph_path.write_text(json.dumps(graph), encoding="utf-8")
            output = root / "instance.xor.cnf"
            summary = encode(graph_path, output)
            lines = output.read_text(encoding="ascii").splitlines()
        self.assertEqual(summary["ordinary_clauses"], 45)
        self.assertEqual(summary["xor_rows"], 10)
        self.assertEqual(lines[2], "p cnf 15 55")
        xor = [line for line in lines if line.startswith("x ")]
        self.assertEqual(len(xor), 10)
        self.assertTrue(all("11" not in line and "12" not in line and "13" not in line for line in xor))

    def test_refuses_overwrite(self) -> None:
        graph = {
            "format": "five-cdc-multigraph-v1",
            "vertices": 0,
            "edges": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            graph_path = root / "graph.json"
            graph_path.write_text(json.dumps(graph), encoding="utf-8")
            output = root / "instance.xor.cnf"
            output.write_text("sentinel", encoding="ascii")
            with self.assertRaises(ValueError):
                encode(graph_path, output)


if __name__ == "__main__":
    unittest.main()
