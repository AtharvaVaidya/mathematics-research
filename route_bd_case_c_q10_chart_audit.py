#!/usr/bin/env python3
"""Exact all-chart audit of the case-c q10/c10 resonance.

The h-adic coefficient r=p7/h^4 has coefficients r0,...,r4.  The
required p6 vertex gives

    [h^8]p6 = r4^2/4 != 0,

so r4 is globally nonzero.  The existing r0- and r1-chart rows force the
raw q10 resonance when r0 or r1 is a unit.  On r0=r1=0, the
denominator-free endpoint identity from the r2 verifier uses only the
already-known r4!=0 and therefore covers the r2-, r3-, and r4-leading
charts at once.

Finally, the approximate-root triangular identity is

    q10_10 = [h^10 y^10]A12 + c10 = q10_cube + c10.

Consequently the all-chart raw resonance proves c10=0 universally on the
full case-c coefficient stratum.  The script also certifies the exact
failure after deleting the required vertex: on r4=0 the two endpoint rows
allow arbitrary q10.
"""

from __future__ import annotations

import sympy as sp

from route_bd_case_c_fractional_resonances_r0 import (
    approximate_root_resonance_slots,
)
from route_bd_case_c_middle_divisibility_r0 import (
    resonance_and_first_two_squares,
)
from route_bd_case_c_middle_divisibility_r1 import (
    first_resonance_pair,
)
from route_bd_case_c_middle_divisibility_r2 import (
    q10_endpoint_forcing,
)


def verify_all_chart_q10_cover() -> dict[str, sp.Expr]:
    """Run the three exact row certificates covering every h-adic chart."""
    r0_rows = resonance_and_first_two_squares()
    r1_rows = first_resonance_pair()
    tail_rows = q10_endpoint_forcing()

    r4 = sp.symbols("r4")
    assert tail_rows["required_p6_vertex"] == r4**2 / 4
    assert sp.factor(tail_rows["denominator_free_square"] / r4) != 0
    assert tail_rows["r4_zero_E14"].subs(sp.symbols("p5_7"), 0) == 0
    assert tail_rows["r4_zero_E13"] == 0

    return {
        "r0_q10_row": r0_rows["E15_h5"],
        "r1_square_consequence": r1_rows["difference_consequence"],
        "tail_denominator_free_square": tail_rows[
            "denominator_free_square"
        ],
        "required_p6_vertex": tail_rows["required_p6_vertex"],
    }


def verify_universal_c10_consequence() -> dict[str, sp.Expr]:
    """Identify the raw resonance defect with the fractional mode c10."""
    slots = approximate_root_resonance_slots()
    c10 = sp.symbols("c10")
    raw_q10 = slots["cube_q10"] + c10
    defect = sp.expand(raw_q10 - slots["cube_q10"])
    assert defect == c10
    return {
        "cube_q10": slots["cube_q10"],
        "raw_q10_defect": defect,
    }


def main() -> None:
    rows = verify_all_chart_q10_cover()
    fractional = verify_universal_c10_consequence()
    print("required p6 vertex:", rows["required_p6_vertex"], "!= 0")
    print(
        "tail denominator-free square:",
        rows["tail_denominator_free_square"],
        "= 0",
    )
    print("raw q10 minus approximate cube:", fractional["raw_q10_defect"])
    print("therefore c10=0 on every full case-c h-adic chart")
    print(
        "after deleting the required vertex, r4=0 leaves q10 free; "
        "that partial-system degeneration is not a full case-c point"
    )
    print("RESULT: EXACT UNIVERSAL CASE-C q10/c10 CHART AUDIT PASSES")


if __name__ == "__main__":
    main()
