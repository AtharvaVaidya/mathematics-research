"""Version-latched CaDiCaL 3.0.1 text-LRAT production wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Sequence, Union


REQUIRED_CADICAL_VERSION = "3.0.1"


class SolverError(RuntimeError):
    pass


@dataclass(frozen=True)
class SolverRun:
    command: Sequence[str]
    returncode: int
    stdout: str
    stderr: str
    proof_exists: bool
    proof_bytes: int

    @property
    def unsat(self) -> bool:
        return self.returncode == 20 and "s UNSATISFIABLE" in self.stdout


def cadical_version(executable: str) -> str:
    try:
        completed = subprocess.run(
            [executable, "--version"],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        raise SolverError("cannot execute {!r}: {}".format(executable, exc)) from exc
    if completed.returncode != 0:
        raise SolverError(
            "CaDiCaL version command failed with code {}".format(
                completed.returncode
            )
        )
    return completed.stdout.strip().splitlines()[0] if completed.stdout.strip() else ""


def produce_text_lrat(
    cnf_path: Union[Path, str],
    proof_path: Union[Path, str],
    executable: str = "cadical",
    extra_options: Sequence[str] = (),
) -> SolverRun:
    """Run exactly CaDiCaL 3.0.1 and request a text LRAT artifact.

    This function verifies the solver's version and result protocol.  It does
    not independently validate the generated LRAT proof.
    """

    version = cadical_version(executable)
    if version != REQUIRED_CADICAL_VERSION:
        raise SolverError(
            "expected CaDiCaL {}, got {!r}".format(
                REQUIRED_CADICAL_VERSION, version
            )
        )
    cnf = Path(cnf_path)
    proof = Path(proof_path)
    if not cnf.is_file():
        raise SolverError("CNF does not exist: {}".format(cnf))
    command = [
        executable,
        *extra_options,
        "--lrat",
        "--no-binary",
        "--checkproof=2",
        str(cnf),
        str(proof),
    ]
    try:
        completed = subprocess.run(
            command,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        raise SolverError("cannot run CaDiCaL: {}".format(exc)) from exc
    proof_exists = proof.is_file()
    proof_bytes = proof.stat().st_size if proof_exists else 0
    run = SolverRun(
        tuple(command),
        completed.returncode,
        completed.stdout,
        completed.stderr,
        proof_exists,
        proof_bytes,
    )
    if completed.returncode not in (10, 20):
        raise SolverError(
            "CaDiCaL returned unexpected code {}\nstdout:\n{}\nstderr:\n{}".format(
                completed.returncode, completed.stdout, completed.stderr
            )
        )
    if completed.returncode == 20:
        if "s UNSATISFIABLE" not in completed.stdout:
            raise SolverError("exit 20 without UNSATISFIABLE status")
        if not proof_exists or proof_bytes == 0:
            raise SolverError("UNSAT result did not produce a nonempty proof")
    return run
