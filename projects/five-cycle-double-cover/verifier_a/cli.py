"""Command-line interface for verifier A."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

from .core import (
    GraphFormatError,
    ModelFormatError,
    build_cnf,
    canonical_graph_bytes,
    check_assignment,
    check_premises,
    load_graph,
    parse_model_text,
    render_cnf,
    render_xor_dimacs,
)
from .solver import SolverError, produce_text_lrat


def _json_output(value: object, stream=sys.stdout) -> None:
    stream.write(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")


def _write_text(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="ascii")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m verifier_a",
        description="Independent exact verifier A for five-cycle double covers",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check-graph", help="check format and premises")
    check.add_argument("graph")

    canonicalize = subparsers.add_parser(
        "canonicalize", help="write canonical bytes for an indexed graph"
    )
    canonicalize.add_argument("graph")
    canonicalize.add_argument("output")

    encode = subparsers.add_parser(
        "encode", help="generate ordinary CNF and/or native XOR DIMACS"
    )
    encode.add_argument("graph")
    encode.add_argument("--cnf")
    encode.add_argument("--xor")
    encode.add_argument(
        "--allow-nonbridgeless",
        action="store_true",
        help="encode even when graph premise fails",
    )

    model = subparsers.add_parser(
        "check-model", help="check a SAT model against original semantics"
    )
    model.add_argument("graph")
    model.add_argument("model")

    prove = subparsers.add_parser(
        "prove-unsat",
        help="generate CNF and ask CaDiCaL 3.0.1 for text LRAT",
    )
    prove.add_argument("graph")
    prove.add_argument("--cnf", required=True)
    prove.add_argument("--proof", required=True)
    prove.add_argument("--solver", default="cadical")
    prove.add_argument("--log")

    return parser


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    try:
        graph = load_graph(args.graph)

        if args.command == "check-graph":
            premise = check_premises(graph)
            result = {
                "format_valid": True,
                "vertices": graph.vertices,
                "edges": len(graph.edges),
                "loops": sum(edge.is_loop for edge in graph.edges),
                "canonical_sha256": sha256(
                    canonical_graph_bytes(graph)
                ).hexdigest(),
                **premise.as_object(),
            }
            _json_output(result)
            return 0 if premise.bridgeless else 1

        if args.command == "canonicalize":
            Path(args.output).write_bytes(canonical_graph_bytes(graph))
            _json_output({"written": args.output})
            return 0

        if args.command == "encode":
            if not args.cnf and not args.xor:
                raise GraphFormatError("encode requires --cnf and/or --xor")
            premise = check_premises(graph)
            if not premise.bridgeless and not args.allow_nonbridgeless:
                raise GraphFormatError(
                    "graph has bridges {}; pass --allow-nonbridgeless to encode"
                    .format(list(premise.bridge_ids))
                )
            result = {}
            if args.cnf:
                cnf = render_cnf(graph)
                _write_text(args.cnf, cnf)
                encoding = build_cnf(graph)
                result["cnf"] = {
                    "path": args.cnf,
                    "variables": encoding.variables,
                    "clauses": len(encoding.clauses),
                    "sha256": sha256(cnf.encode("ascii")).hexdigest(),
                }
            if args.xor:
                xor_text = render_xor_dimacs(graph)
                _write_text(args.xor, xor_text)
                result["xor"] = {
                    "path": args.xor,
                    "sha256": sha256(xor_text.encode("ascii")).hexdigest(),
                }
            _json_output(result)
            return 0

        if args.command == "check-model":
            encoding = build_cnf(graph)
            model_text = Path(args.model).read_text(encoding="utf-8")
            assignment = parse_model_text(
                model_text,
                encoding.base_variables,
                encoding.variables,
            )
            result = check_assignment(graph, assignment)
            _json_output(result.as_object())
            return 0 if result.valid else 1

        if args.command == "prove-unsat":
            premise = check_premises(graph)
            if not premise.bridgeless:
                raise GraphFormatError(
                    "refusing proof run: graph has bridges {}".format(
                        list(premise.bridge_ids)
                    )
                )
            cnf_text = render_cnf(graph)
            _write_text(args.cnf, cnf_text)
            run = produce_text_lrat(args.cnf, args.proof, args.solver)
            if args.log:
                Path(args.log).write_text(
                    run.stdout + run.stderr, encoding="utf-8"
                )
            result = {
                "returncode": run.returncode,
                "unsat_reported": run.unsat,
                "proof_path": args.proof,
                "proof_bytes": run.proof_bytes,
                "independently_checked": False,
                "warning": (
                    "LRAT production is not independent LRAT verification; "
                    "use a separately implemented checker before acceptance"
                ),
            }
            _json_output(result)
            return 0 if run.unsat else 1

        raise AssertionError("unhandled command")
    except (GraphFormatError, ModelFormatError, SolverError, OSError) as exc:
        _json_output({"error": str(exc)}, stream=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
