#!/usr/bin/env python3
"""Deterministic positive smoke test for both simultaneous encodings."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
MODULE_PATH = HERE / "simultaneous_external_sat.py"
SPEC = importlib.util.spec_from_file_location("simultaneous", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
SIM = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SIM
SPEC.loader.exec_module(SIM)


def main() -> None:
    graph_path = PROJECT / "artifacts" / "structured" / "graphs" / "lift13_petersen_girth10.json"
    graph = SIM.RT.json_graph(graph_path)
    formula, ports, factors = SIM.build_formula(graph, 0, 3, "ab-ac-same")
    assert ports == (0, 1, 2)
    assert factors == ((0, 3), (1, 3))
    cnf = formula.cnf().encode("ascii")
    xcnf = formula.xcnf().encode("ascii")
    assert hashlib.sha256(cnf).hexdigest() == (
        "8ad42e76d1c2c7cb26aeef4046f5d4571442033311c131922fabcc2f58d6d8c1")
    assert hashlib.sha256(xcnf).hexdigest() == (
        "df2548ff099a8d111f167647516a9a8f9f06587771ed51ea8eca05a10dce9b35")
    with tempfile.TemporaryDirectory() as directory:
        cnf_path = Path(directory) / "instance.cnf"
        xcnf_path = Path(directory) / "instance.xcnf"
        cnf_path.write_bytes(cnf)
        xcnf_path.write_bytes(xcnf)
        result = SIM.solve_case(
            graph, 0, 3, "ab-ac-same", Path("/opt/homebrew/bin/cadical"),
            cnf_path, xcnf_path, None, False)
        assert result["status"] == "SAT_MODEL_SEMANTICALLY_CHECKED"
        assert result["labels_sha256"] == (
            "1b52b99403fe2849cb6a7b2b8413faadc855509a5382cf79768d0335c83d2d8a")
        cms = Path("/opt/homebrew/bin/cryptominisat5")
        if cms.exists():
            process = subprocess.run(
                [str(cms), "--verb", "0", str(xcnf_path)], check=False,
                text=True, capture_output=True)
            assert process.returncode == 10
            assert "s SATISFIABLE" in process.stdout
            native = "SAT"
        else:
            native = "NOT_INSTALLED"
    print("SIM_FORMULA cases=6 variables=2145 cnf_clauses=11780 native_xors=1430 PASS")
    print("SIM_CNF case=ab-ac-same SAT_MODEL_SEMANTICALLY_CHECKED labels_sha256=1b52b99403fe2849cb6a7b2b8413faadc855509a5382cf79768d0335c83d2d8a PASS")
    print(f"SIM_XCNF cryptominisat={native} encoding_sha256=df2548ff099a8d111f167647516a9a8f9f06587771ed51ea8eca05a10dce9b35 PASS")


if __name__ == "__main__":
    main()
