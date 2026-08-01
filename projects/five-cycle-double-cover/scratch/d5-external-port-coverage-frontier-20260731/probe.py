#!/usr/bin/env python3
"""Exact SAT probe for an external rooted-cap state.

This imports the frozen root-transition encoding, adds only the clauses
which forbid the inactive cap port from carrying the fixed factor pair 01,
and semantically checks every positive model.  An UNSAT response is only a
candidate unless a proof is retained and checked separately.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile


PROJECT = Path(__file__).resolve().parents[2]
BASE = PROJECT / "scratch" / "d5-root-transition-sat-20260731" / "search.py"
SPEC = importlib.util.spec_from_file_location("root_transition", BASE)
assert SPEC is not None and SPEC.loader is not None
RT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RT
SPEC.loader.exec_module(RT)


def solve_external(graph, z: int, root: int, selected_port: int,
                   cadical: Path) -> tuple[str, tuple[int, ...] | None]:
    rows = RT.incidence(graph)
    ports = rows[z]
    assert selected_port in ports
    assert z not in graph.edges[root]
    assert set(graph.edges[root]).isdisjoint(graph.edges[selected_port])

    cnf, transition = RT.build_cnf(graph, (root, selected_port), True)
    for port in ports:
        if port == selected_port:
            continue
        cnf.add(-cnf.var("x", port, 0), -cnf.var("x", port, 1))

    with tempfile.NamedTemporaryFile(suffix=".cnf") as handle:
        Path(handle.name).write_text(cnf.dimacs(), encoding="ascii")
        run = subprocess.run(
            [str(cadical), "--quiet", "--checkproof=1", handle.name],
            check=False, text=True, capture_output=True,
        )
    assert run.returncode in (10, 20), run.stderr[-4000:]
    positive = RT.parse_model(run.stdout)
    if positive is None:
        return "UNSAT_UNCERTIFIED", None

    labels, _ = RT.validate_model(
        graph, (root, selected_port), cnf, transition, positive)
    factor = 3
    active_ports = [
        port for port in ports if (labels[port] & factor).bit_count() == 1
    ]
    assert selected_port in active_ports and len(active_ports) == 2
    inactive = next(port for port in ports if port not in active_ports)
    assert labels[inactive] & factor == 0
    return "SAT_MODEL_CHECKED_EXTERNAL", labels


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph6", nargs="?", type=Path)
    parser.add_argument("--petersen-foster", action="store_true")
    parser.add_argument("--row", type=int, default=0)
    parser.add_argument("--z", type=int, required=True)
    parser.add_argument("--root", type=int, required=True)
    parser.add_argument("--port-slot", type=int, choices=(0, 1, 2), required=True)
    parser.add_argument("--cadical", type=Path,
                        default=Path("/opt/homebrew/bin/cadical"))
    args = parser.parse_args()
    assert args.petersen_foster ^ (args.graph6 is not None)
    graph = (RT.petersen_foster_graph() if args.petersen_foster
             else RT.graph6_file(args.graph6, args.row))
    port = RT.incidence(graph)[args.z][args.port_slot]
    status, labels = solve_external(graph, args.z, args.root, port, args.cadical)
    print(
        f"row={args.row} z={args.z} root={args.root} "
        f"port={port} status={status}"
    )
    if labels is not None:
        print("labels_sha256=" + __import__("hashlib").sha256(bytes(labels)).hexdigest())


if __name__ == "__main__":
    main()
