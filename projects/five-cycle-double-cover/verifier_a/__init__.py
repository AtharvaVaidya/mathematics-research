"""Independent verifier A for the five-cycle double cover encoding."""

from .core import (
    FORMAT,
    COORDINATES,
    CNFEncoding,
    Edge,
    Graph,
    GraphFormatError,
    ModelFormatError,
    ModelResult,
    PremiseResult,
    build_cnf,
    canonical_graph_bytes,
    check_assignment,
    check_premises,
    load_graph,
    parse_graph_text,
    parse_model_text,
    render_cnf,
    render_xor_dimacs,
)

__all__ = [
    "FORMAT",
    "COORDINATES",
    "CNFEncoding",
    "Edge",
    "Graph",
    "GraphFormatError",
    "ModelFormatError",
    "ModelResult",
    "PremiseResult",
    "build_cnf",
    "canonical_graph_bytes",
    "check_assignment",
    "check_premises",
    "load_graph",
    "parse_graph_text",
    "parse_model_text",
    "render_cnf",
    "render_xor_dimacs",
]

__version__ = "1.0.0"
