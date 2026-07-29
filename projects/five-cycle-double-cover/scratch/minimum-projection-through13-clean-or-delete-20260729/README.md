# Minimum extendable projections through size thirteen are cleanable

Date: 2026-07-29

Status: **HUMAN-CHECKABLE CLEAN-OR-DELETE THEOREM WITH EXACT FINITE
CERTIFICATES / NOT A FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

## Theorem

Let \(G\) be a finite connected bridgeless loopless cubic graph;
parallel edges are allowed.  A binary cycle \(h\) is **extendable** if
there are binary cycles \(p,q\) with
\[
                         E(G)-h\subseteq p\cup q.          \tag{1}
\]
Equivalently, \(f=(h,s)\), where \(s=(p,q)\), is a nowhere-zero
\(\mathbb F_2\times\mathbb F_2^2\)-flow.

For \(c\in K=\mathbb F_2^2\), put
\[
                         M_c=\{e\in h:s(e)=c\}.            \tag{2}
\]
An extension is **clean** if every component \(W\) of \(G-h\) satisfies
\[
                   |M_c\cap\delta(W)|\equiv0\pmod2
                   \quad(c\in K).                         \tag{3}
\]

> **Theorem.** Every cardinality-minimum extendable projection of size
> at most thirteen is cleanable.

The sibling packages
`minimum-projection-through11-cleanability-20260729/` and
`minimum-projection-through12-clean-or-delete-20260729/` supply the
earlier steps.  This package proves the new size-thirteen step.  It
does not bound the minimum support in general and does not resolve
FiveCDC.

## 1. Clean-or-delete boundary dichotomy

Fix a cardinality-minimum projection \(h\) and an extension \(f=(h,s)\).
The minimum-projection exchange theorem implies that every circuit
component of \(h\) contains all four affine classes \(M_c\); hence each
circuit has at least four edges.

Index the circuit vertices and edges cyclically, write \(c_i=s(e_i)\),
and let \(\pi_i\) name the component of \(G-h\) containing the vertex
between \(e_{i-1}\) and \(e_i\).  The third edge there has nonzero low
value
\[
                         d_i=c_{i-1}+c_i.                 \tag{4}
\]
For every component block \(a\), conservation gives
\[
                    \mathop{\mathbin\oplus}_{\pi_i=a}d_i=0. \tag{5}
\]

Choose one \(L_a\in\mathrm{GL}(2,2)\) per component and seek new
circuit-edge low values \(r_i\) satisfying
\[
                    r_{i-1}+r_i=L_{\pi_i}d_i.             \tag{6}
\]
Independent additive starts are allowed on distinct circuit components.

There are two successful outcomes:

1. **clean:** every affine cut-colour parity computed from the \(r_i\)'s
   is even; or
2. **delete:** all low values \(r_i\) on at least one circuit component
   \(D\) are nonzero.

In the delete branch, remove \(D\) from the first-coordinate support.
On \(D\), the full values become \((0,r_i)\), which remain nonzero.
The other support circuits retain first coordinate one, and every edge
inside \(G-h\) retains a transformed nonzero low value.  Equation (6)
gives conservation everywhere.  Thus \(h-D\) is an extendable
projection strictly smaller than \(h\), contradicting global
minimality.

Consequently, a globally minimum boundary state must take the clean
branch whenever the finite clean-or-delete dichotomy holds.

### A small algebra check for the clean test

Write \(q(x_1,x_2)=x_1x_2\) and let
\[
             B(x,y)=q(x+y)+q(x)+q(y)
\]
be its polar symplectic form.  For fixed component maps, the four
cut-colour parities at a block \(a\) are equal.  Their common value is
\[
 Q_a=\bigoplus_{\pi_i=a}\bigl(q(r_{i-1})+q(r_i)\bigr).    \tag{7}
\]
Indeed, the constant terms in the four colour indicators occur twice,
and their linear differences cancel by (5); only the common quadratic
term remains.

If circuit \(D_j\) is translated by \(z_j\), (7) changes by
\[
 B\!\left(z_j,\,
   \mathop{\mathbin\oplus}_{i\in D_j,\ \pi_i=a}L_a d_i\right). \tag{8}
\]
Thus, for fixed maps, direct cleaning is exactly a linear system in the
two bits of every relative circuit translation.  Equations (7)--(8)
give a short independent mathematical description of the exhaustive
translation test in `verify.cpp`.

## 2. Exhaustive size-thirteen theorem

Since every circuit uses all four colours, the complete support-shape
list at size thirteen is:

- one 13-cycle;
- two circuits of lengths \(4+9\), \(5+8\), or \(6+7\);
- three circuits of lengths \(4+4+5\).

`verify.cpp` canonically generates every proper four-colour circuit word
using all four colours on every circuit.  It quotients only by the
global affine colour action, independent dihedral circuit actions, and
interchange of equal-length circuits.  For every word it generates
exactly every set partition satisfying (5), tests dirtiness, and
exhausts the component maps and relative circuit starts.

The exact mutually exclusive counts are:

| shape | canonical words | charge-valid states | dirty states | direct clean | direct failure, delete succeeds | dichotomy failures |
|:---:|---:|---:|---:|---:|---:|---:|
| 4+4+5 | 4 | 238,522 | 208,144 | 208,144 | 0 | 0 |
| 4+9 | 130 | 7,753,918 | 6,657,654 | 6,657,594 | 60 | 0 |
| 5+8 | 203 | 12,144,485 | 10,404,652 | 10,401,428 | 3,224 | 0 |
| 6+7 | 242 | 14,480,258 | 12,415,026 | 12,410,636 | 4,390 | 0 |
| 13 | 2,583 | 155,381,679 | 129,684,490 | 129,684,490 | 0 | 0 |
| **total** | **3,162** | **189,998,862** | **159,369,966** | **159,362,292** | **7,674** | **0** |

All 7,674 direct-clean failures therefore contradict global minimality
by strict circuit deletion.  This proves the size-thirteen step and
hence the theorem.

An independently implemented census returned the same five tuples
\[
(\text{words},\text{charge-valid},\text{dirty},\text{delete})
\]
as the primary verifier.  This comparison checks the enumeration
counts; the literal witnesses below check every exceptional state.

## 3. Literal certificates

The frozen `size13-census.txt` contains:

- all 7,674 literal direct-clean failures;
- for each, the original circuit words and component partition;
- one map \(L_a\) for every component;
- the integrated zero-start word on every circuit;
- a circuit whose integrated word omits a displayed affine colour;
- the missing colour, whose use as the circuit translation makes every
  low value on that circuit nonzero;
- canonical word/partition orbit representatives and summary counts.

`verify_output.py` independently parses every frozen certificate,
rechecks the charge equations, dirtiness, component maps, cyclic
recurrences, omitted colour, nonzero translated circuit, counts, and
orbit totals.  It also rejects any `COUNTERSTATE` line.

The 7,674 literal exceptional states form 6,498 canonical
word/partition orbits:

| shape | literal states | canonical pair orbits |
|:---:|---:|---:|
| 4+9 | 60 | 60 |
| 5+8 | 3,224 | 2,775 |
| 6+7 | 4,390 | 3,663 |

The C++ enumeration is exact rather than graph sampling.  The word
quotient reduces equivalent colour words, but every compatible set
partition is still generated.

## 4. Reproduction

Run:

```sh
clang++ -std=c++20 -O3 -DNDEBUG verify.cpp -o verify
./verify regenerated-size13-census.txt
cmp regenerated-size13-census.txt size13-census.txt
python3 verify_output.py
shasum -a 256 -c SHA256SUMS
```

The reference primary census took about six minutes on an Apple Silicon
workstation.  Its progress records make an interrupted replay auditable.

## Scope and disclosure

The theorem assumes a connected loopless cubic graph.  Parallel edges
are allowed; loops require separate conventions and are outside the
statement.  This work has not received independent human peer review.

OpenAI Codex agents under human direction proposed the clean-or-delete
dichotomy, derived the algebra check, performed two independent
size-thirteen censuses, implemented the certificate checker, and
prepared this proof package.  All finite proof data are included so the
result can be checked without trusting an AI-generated summary.  No
literature-wide priority claim is made, and FiveCDC remains unresolved.
