#!/usr/bin/env python3
"""Exact sparse searches in B=k[u,v,w]/(w^2-u-u^2*v).

No third-party packages are used.  Polynomials are dictionaries indexed by
(u-degree, v-degree, w-degree), where the last entry is 0 or 1.  Arithmetic is
performed either over Q (fractions.Fraction) or over a prime field.
"""

from __future__ import annotations

import argparse
import itertools
from fractions import Fraction


Monomial = tuple[int, int, int]
Polynomial = dict[Monomial, object]


def add(a: Polynomial, b: Polynomial, p: int | None = None) -> Polynomial:
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, 0) + c
        if p:
            out[m] %= p
        if not out[m]:
            del out[m]
    return out


def scale(a: Polynomial, c, p: int | None = None) -> Polynomial:
    out = {}
    for m, d in a.items():
        value = c * d
        if p:
            value %= p
        if value:
            out[m] = value
    return out


def mul(a: Polynomial, b: Polynomial, p: int | None = None) -> Polynomial:
    out: Polynomial = {}
    for (i, j, k), c in a.items():
        for (ii, jj, kk), d in b.items():
            coeff = c * d
            base = (i + ii, j + jj, k + kk)
            terms = {base: coeff}
            if base[2] == 2:
                terms = {
                    (base[0] + 1, base[1], 0): coeff,
                    (base[0] + 2, base[1] + 1, 0): coeff,
                }
            out = add(out, terms, p)
    return out


def derivative(a: Polynomial, variable: int, p: int | None = None) -> Polynomial:
    out = {}
    for m, c in a.items():
        exponent = m[variable]
        if exponent:
            mm = list(m)
            mm[variable] -= 1
            value = c * exponent
            if p:
                value %= p
            if value:
                out[tuple(mm)] = value
    return out


def bracket(a: Polynomial, b: Polynomial, p: int | None = None) -> Polynomial:
    """The bracket from the research brief, reduced to the standard B-basis."""
    au, av, aw = (derivative(a, i, p) for i in range(3))
    bu, bv, bw = (derivative(b, i, p) for i in range(3))
    u2 = {(2, 0, 0): 1}
    neg2w = {(0, 0, 1): -2 if not p else (-2) % p}
    one_plus_2uv = {(0, 0, 0): 1, (1, 1, 0): 2 if not p else 2 % p}
    t1 = mul(neg2w, add(mul(au, bv, p), scale(mul(av, bu, p), -1, p), p), p)
    t2 = scale(mul(u2, add(mul(au, bw, p), scale(mul(aw, bu, p), -1, p), p), p), -1, p)
    t3 = mul(one_plus_2uv, add(mul(av, bw, p), scale(mul(aw, bv, p), -1, p), p), p)
    return add(add(t1, t2, p), t3, p)


def basis(total_degree: int, include_constant: bool = True) -> list[Monomial]:
    ans = []
    for k in range(2):
        for i in range(total_degree + 1):
            for j in range(total_degree + 1):
                if i + j + k <= total_degree and (include_constant or (i, j, k) != (0, 0, 0)):
                    ans.append((i, j, k))
    return sorted(ans, key=lambda m: (sum(m), m[2], m[1], m[0]))


def format_polynomial(a: Polynomial) -> str:
    if not a:
        return "0"
    pieces = []
    for m in sorted(a, key=lambda z: (sum(z), z[2], z[1], z[0])):
        c = a[m]
        variables = []
        for name, exponent in zip(("u", "v", "w"), m):
            if exponent == 1:
                variables.append(name)
            elif exponent:
                variables.append(f"{name}^{exponent}")
        term = "*".join(variables) or "1"
        pieces.append(f"({c})*{term}")
    return " + ".join(pieces)


def rref_solve_mod(matrix: list[list[int]], rhs: list[int], p: int):
    """Return one solution over F_p, or None."""
    if not matrix:
        return [] if not any(x % p for x in rhs) else None
    rows = [list(map(lambda x: x % p, row)) + [b % p] for row, b in zip(matrix, rhs)]
    nrows, ncols = len(rows), len(matrix[0])
    pivot_cols = []
    pivot_row = 0
    for col in range(ncols):
        pivot = next((r for r in range(pivot_row, nrows) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][col], -1, p)
        rows[pivot_row] = [(x * inverse) % p for x in rows[pivot_row]]
        for r in range(nrows):
            if r != pivot_row and rows[r][col]:
                factor = rows[r][col]
                rows[r] = [(x - factor * y) % p for x, y in zip(rows[r], rows[pivot_row])]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == nrows:
            break
    if any(not any(row[:ncols]) and row[ncols] for row in rows):
        return None
    solution = [0] * ncols
    for r, col in enumerate(pivot_cols):
        solution[col] = rows[r][ncols]
    return solution


def rref_solve_q(matrix: list[list[Fraction]], rhs: list[Fraction]):
    """Return one exact rational solution, or None."""
    if not matrix:
        return [] if not any(rhs) else None
    rows = [list(row) + [b] for row, b in zip(matrix, rhs)]
    nrows, ncols = len(rows), len(matrix[0])
    pivot_cols = []
    pivot_row = 0
    for col in range(ncols):
        pivot = next((r for r in range(pivot_row, nrows) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = 1 / rows[pivot_row][col]
        rows[pivot_row] = [x * inverse for x in rows[pivot_row]]
        for r in range(nrows):
            if r != pivot_row and rows[r][col]:
                factor = rows[r][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[pivot_row])]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == nrows:
            break
    if any(not any(row[:ncols]) and row[ncols] for row in rows):
        return None
    solution = [Fraction(0)] * ncols
    for r, col in enumerate(pivot_cols):
        solution[col] = rows[r][ncols]
    return solution


def slice_for_p(P: Polynomial, q_degree: int, p: int | None):
    qb = basis(q_degree)
    columns = [bracket(P, {m: 1}, p) for m in qb]
    support = sorted(set().union(*(column.keys() for column in columns), {(0, 0, 0)}))
    matrix = [[column.get(m, 0) for column in columns] for m in support]
    rhs = [1 if m == (0, 0, 0) else 0 for m in support]
    if p:
        solution = rref_solve_mod(matrix, rhs, p)
    else:
        matrix = [[Fraction(x) for x in row] for row in matrix]
        rhs = [Fraction(x) for x in rhs]
        solution = rref_solve_q(matrix, rhs)
    if solution is None:
        return None
    Q = {m: c for m, c in zip(qb, solution) if c}
    assert bracket(P, Q, p) == {(0, 0, 0): 1}
    return Q


def exhaustive_p_search(p: int, p_degree: int, q_degree: int, max_solutions: int):
    pb = basis(p_degree, include_constant=False)
    count = 0
    for leading_index in range(len(pb)):
        # Overall scaling is redundant because it can be absorbed into Q.
        tail = len(pb) - leading_index - 1
        for coeff_tail in itertools.product(range(p), repeat=tail):
            coeffs = [0] * leading_index + [1] + list(coeff_tail)
            P = {m: c for m, c in zip(pb, coeffs) if c}
            count += 1
            Q = slice_for_p(P, q_degree, p)
            if Q is not None:
                print(f"solution after {count} projective P candidates")
                print("P =", format_polynomial(P))
                print("Q =", format_polynomial(Q))
                print("{P,Q} =", format_polynomial(bracket(P, Q, p)))
                max_solutions -= 1
                if not max_solutions:
                    return
    print(f"no solution in {count} projective P candidates")


def named_p_search(q_degree: int):
    names = {
        "u": {(1, 0, 0): Fraction(1)},
        "v": {(0, 1, 0): Fraction(1)},
        "w": {(0, 0, 1): Fraction(1)},
        "u+v": {(1, 0, 0): Fraction(1), (0, 1, 0): Fraction(1)},
        "u+w": {(1, 0, 0): Fraction(1), (0, 0, 1): Fraction(1)},
        "v+w": {(0, 1, 0): Fraction(1), (0, 0, 1): Fraction(1)},
    }
    for name, P in names.items():
        Q = slice_for_p(P, q_degree, None)
        print(name, "=>", "none" if Q is None else format_polynomial(Q))


def sparse_char_zero(p_degree: int, q_degree: int, support_size: int):
    """Test all monomial/binomial P with coefficients +/-1 over Q.

    The result is exact for this explicitly stated finite ansatz.  Constants in
    P are omitted because they do not affect its Hamiltonian derivation, and an
    overall sign is normalized by fixing the first coefficient to +1.
    """
    if support_size not in (1, 2):
        raise ValueError("the implemented exact sparse search supports size 1 or 2")
    pb = basis(p_degree, include_constant=False)
    candidates = [((m,), (1,)) for m in pb]
    if support_size == 2:
        candidates.extend(
            ((pb[i], pb[j]), (1, sign))
            for i in range(len(pb))
            for j in range(i + 1, len(pb))
            for sign in (1, -1)
        )
    hits = 0
    for index, (monomials, coefficients) in enumerate(candidates, 1):
        P = {m: Fraction(c) for m, c in zip(monomials, coefficients)}
        Q = slice_for_p(P, q_degree, None)
        if Q is not None:
            hits += 1
            print("P =", format_polynomial(P))
            print("Q =", format_polynomial(Q))
            print("{P,Q} =", format_polynomial(bracket(P, Q)))
    print(
        f"tested {len(candidates)} exact P candidates; "
        f"p-degree<={p_degree}, q-degree<={q_degree}, hits={hits}"
    )


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    exhaustive = subparsers.add_parser("exhaustive-mod-p")
    exhaustive.add_argument("--prime", type=int, required=True)
    exhaustive.add_argument("--p-degree", type=int, required=True)
    exhaustive.add_argument("--q-degree", type=int, required=True)
    exhaustive.add_argument("--max-solutions", type=int, default=5)
    named = subparsers.add_parser("named-char-zero")
    named.add_argument("--q-degree", type=int, required=True)
    sparse = subparsers.add_parser("sparse-char-zero")
    sparse.add_argument("--p-degree", type=int, required=True)
    sparse.add_argument("--q-degree", type=int, required=True)
    sparse.add_argument("--support-size", type=int, choices=(1, 2), default=2)
    args = parser.parse_args()
    if args.command == "exhaustive-mod-p":
        exhaustive_p_search(args.prime, args.p_degree, args.q_degree, args.max_solutions)
    elif args.command == "named-char-zero":
        named_p_search(args.q_degree)
    elif args.command == "sparse-char-zero":
        sparse_char_zero(args.p_degree, args.q_degree, args.support_size)


if __name__ == "__main__":
    main()
