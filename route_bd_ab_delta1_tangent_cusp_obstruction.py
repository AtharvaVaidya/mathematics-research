#!/usr/bin/env python3
"""Valuation certificate excluding the nonzero-tangent cusp chart."""

from __future__ import annotations

import sympy as sp


def verify_symbolic_valuation_identities() -> None:
    m, n, r = sp.symbols("m n r", integer=True)

    # q2=g'p2+(1/2)g''p1^2.  Its two potentially polar valuations are
    # -1 and n-2m+2r.
    q2_singular = n - 2 * m + 2 * r

    # The z^4 Taylor identity.
    z4 = (
        n - 2 * m - 2,
        n - 3 * m + 2 * r - 1,
        n - 4 * m + 4 * r,
    )
    assert sp.expand(z4[1] - z4[0]) == 2 * r - m + 1
    assert sp.expand(z4[2] - z4[1]) == 2 * r - m + 1

    # If q2 is regular, its fixed p2 pole must cancel:
    # n-2m+2r=-1.  If the z4 sum vanishes, its arithmetic progression
    # cannot have a unique minimum, so 2r=m-1.  Together these give n=m.
    n_from_q2 = sp.solve(sp.Eq(q2_singular, -1), n)[0]
    contradiction = sp.expand(n_from_q2.subs(r, (m - 1) / 2))
    assert contradiction == m


def verify_all_degree_capped_valuations() -> None:
    survivors: list[tuple[int, int, int]] = []
    for m in range(2, 9):
        for n in range(m + 1, min(2 * m, 13)):
            for r in range(0, 9):
                if n - 2 * m + 2 * r != -1:
                    continue
                valuations = (
                    n - 2 * m - 2,
                    n - 3 * m + 2 * r - 1,
                    n - 4 * m + 4 * r,
                )
                if sum(value == min(valuations) for value in valuations) >= 2:
                    survivors.append((m, n, r))
    assert survivors == []


def main() -> None:
    verify_symbolic_valuation_identities()
    verify_all_degree_capped_valuations()
    print("verified q2 pole cancellation forces n-2m+2r=-1")
    print("verified the z4 identity forces 2r=m-1")
    print("verified these conditions contradict m<n<2m")
    print("RESULT: NONZERO-TANGENT CUSP CHART IS IMPOSSIBLE")


if __name__ == "__main__":
    main()
