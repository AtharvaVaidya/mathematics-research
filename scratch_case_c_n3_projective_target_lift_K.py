#!/usr/bin/env python3
"""Exact targeted projective memberships for the case-c generic charts.

The computation stays in the original weighted-homogeneous coordinate
ring over K = Q[s]/(f).  It asks Singular only for the two fixed-degree
memberships discovered modulo 32003:

    L^23 in (F5, F6[0..2], F7[0], F7[1]),
    A^8  in (L, F5, F6[0..2], F7[0]).

Here L=coeff(F5,X6) and A=coeff(F5,X5).  A returned lift is accepted only
after exact symbolic recomputation of J*C-target gives the zero
polynomial.  Thus the generated witness is deterministic even though
the exponents were discovered in finite characteristic.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import pickle
import subprocess
import tempfile
import time

from route_bd_case_c_n3_hurwitz_bridge import (
    NVAR,
    ParameterPolynomial,
    QuotientElement,
    parameter_coefficient,
)
from scratch_case_c_n3_generic_charts_Q import (
    DEFAULT_CACHE,
    minpoly_text,
    polynomial_text,
    polynomial_weights,
)
from scratch_case_c_n3_weighted_projective_Q import chart_coordinates


WEIGHTS = (1, 1, 2, 2, 3, 3, 4)
DEFAULT_OUTPUT = Path("tmp/case_c_n3_projective_target_lift_K")


def ring_text(eliminant_text: str) -> str:
    variables = ",".join(f"X{index}" for index in range(NVAR))
    weights = ",".join(map(str, WEIGHTS))
    return "\n".join(
        (
            f"ring R=(0,s),({variables}),wp({weights});",
            f"minpoly={eliminant_text};",
            "option(redSB);",
        )
    )


def singular_string(path: Path) -> str:
    return str(path).replace("\\", "\\\\").replace('"', '\\"')


def program_text(
    name: str,
    eliminant_text: str,
    generators: list[ParameterPolynomial],
    target_base: ParameterPolynomial,
    target_power: int,
    output_path: Path,
    algorithm: str,
) -> str:
    ring = ring_text(eliminant_text)
    ideal_text = ",\n".join(polynomial_text(row) for row in generators)
    target_base_text = polynomial_text(target_base)
    serialized_ring = ring.replace("\n", " ")
    return "\n".join(
        (
            ring,
            f"ideal J=\n{ideal_text};",
            f"poly targetbase={target_base_text};",
            f"poly target=targetbase^{target_power};",
            "ideal Target=target;",
            "matrix Units;",
            f'matrix C=lift(J,Target,Units,"{algorithm}");',
            "poly residual=-target;",
            "for (int row=1; row<=nrows(C); row++) {",
            "  residual=residual+J[row]*C[row,1];",
            "}",
            "if (residual<>0) {",
            f'  print("FAIL {name} NONZERO_EXACT_RESIDUAL");',
            "  residual;",
            "  exit(3);",
            "}",
            f'print("CERTIFIED {name} EXACT_RESIDUAL_ZERO");',
            f'print("CERTIFIED {name} GENERATORS "+string(size(J)));',
            f'print("CERTIFIED {name} TARGET_WEIGHT "+string(deg(target)));',
            f'string out="{singular_string(output_path)}";',
            'write(out,"// Exact weighted-homogeneous membership certificate");',
            f'write(out,"// Membership: {name}");',
            f'write(out,"{serialized_ring}");',
            'write(out,"ideal J="+string(J)+";");',
            'write(out,"poly target="+string(target)+";");',
            'write(out,"matrix C["+string(nrows(C))+"][1]="+string(C)+";");',
            'write(out,"poly residual=-target;");',
            "for (row=1; row<=nrows(C); row++) {",
            '  write(out,"residual=residual+J["+string(row)+"]*C["'
            '+string(row)+",1];");',
            "}",
            'write(out,"if (residual<>0) { residual; exit(3); }");',
            f'write(out,"print(\\\"REPLAY CERTIFIED {name} EXACT_RESIDUAL_ZERO\\\");");',
            "exit(0);",
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--membership",
        choices=("L23", "A8"),
        action="append",
        help="membership to run; repeat to select both (default: both)",
    )
    parser.add_argument(
        "--algorithm",
        choices=("std", "slimgb"),
        default="slimgb",
    )
    args = parser.parse_args()

    with args.cache.open("rb") as stream:
        cache = pickle.load(stream)
    _, eliminant, _, _ = cache["outer"]
    imposed: list[ParameterPolynomial] = cache["imposed"]
    QuotientElement.configure(eliminant)

    by_weight = {
        weight: [
            row for row in imposed
            if row and polynomial_weights(row) == {weight}
        ]
        for weight in (5, 6, 7)
    }
    assert {weight: len(rows) for weight, rows in by_weight.items()} == {
        5: 1,
        6: 3,
        7: 5,
    }
    f5, linear_form, quadratic_form = chart_coordinates(imposed)
    f6 = by_weight[6]
    f7 = by_weight[7]
    assert polynomial_weights(linear_form) == {1}
    assert polynomial_weights(quadratic_form) == {2}

    tasks = {
        "L23": (
            "L23_IN_F5_F6_F7_01",
            [f5, *f6, f7[0], f7[1]],
            linear_form,
            23,
        ),
        "A8": (
            "A8_IN_L_F5_F6_F7_0",
            [linear_form, f5, *f6, f7[0]],
            quadratic_form,
            8,
        ),
    }
    selected = args.membership or list(tasks)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for key in selected:
        name, generators, target_base, target_power = tasks[key]
        certificate_path = (
            args.output_dir / f"{name}.sing"
        ).resolve()
        program = program_text(
            name,
            minpoly_text(eliminant),
            generators,
            target_base,
            target_power,
            certificate_path,
            args.algorithm,
        )
        print(
            f"starting {name}: {len(generators)} generators, "
            f"target weight "
            f"{next(iter(polynomial_weights(target_base))) * target_power}, "
            f"{len(program)} input characters",
            flush=True,
        )
        start = time.monotonic()
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".sing",
            prefix="case_c_projective_lift_",
            delete=False,
        ) as stream:
            stream.write(program)
            input_path = Path(stream.name)
        try:
            result = subprocess.run(
                ["Singular", "-q", str(input_path)],
                text=True,
                capture_output=True,
                check=False,
            )
        finally:
            input_path.unlink(missing_ok=True)
        elapsed = time.monotonic() - start
        output = result.stdout + result.stderr
        print(output.strip(), flush=True)
        marker = f"CERTIFIED {name} EXACT_RESIDUAL_ZERO"
        if result.returncode or marker not in output:
            raise RuntimeError(
                f"Singular membership failed for {name} after "
                f"{elapsed:.1f}s (return code {result.returncode})"
            )
        print(
            f"wrote {certificate_path} in {elapsed:.1f}s "
            f"({certificate_path.stat().st_size} bytes)",
            flush=True,
        )

        replay_start = time.monotonic()
        replay = subprocess.run(
            ["Singular", "-q", str(certificate_path)],
            text=True,
            capture_output=True,
            check=False,
        )
        replay_elapsed = time.monotonic() - replay_start
        replay_output = replay.stdout + replay.stderr
        print(replay_output.strip(), flush=True)
        replay_marker = (
            f"REPLAY CERTIFIED {name} EXACT_RESIDUAL_ZERO"
        )
        if replay.returncode or replay_marker not in replay_output:
            raise RuntimeError(
                f"standalone certificate replay failed for {name}"
            )
        print(
            f"replayed {name} exact identity in {replay_elapsed:.1f}s",
            flush=True,
        )


if __name__ == "__main__":
    main()
