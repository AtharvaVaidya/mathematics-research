# Minimum extendable projections through size twelve are cleanable

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

> **Theorem.**  Every cardinality-minimum extendable projection of
> size at most twelve is cleanable.

The sibling package
`minimum-projection-through11-cleanability-20260729/` supplies the full
proof and certificates through size eleven.  This package proves the
new size-twelve step.  The result does not bound the minimum support in
general and does not resolve FiveCDC.

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
For each component block \(a\), conservation gives
\[
                    \mathop{\mathbin\oplus}_{\pi_i=a}d_i=0. \tag{5}
\]

Choose one \(L_a\in\mathrm{GL}(2,2)\) per component and seek new
circuit-edge low values \(r_i\) satisfying
\[
                    r_{i-1}+r_i=L_{\pi_i}d_i.             \tag{6}
\]
Independent additive starts are allowed on distinct circuit components.

There are two useful successful outcomes:

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
branch whenever the following finite dichotomy holds.

## 2. Exhaustive size-twelve theorem

The complete support-shape list at size twelve is:

- one 12-cycle;
- two circuits of lengths \(4+8\), \(5+7\), or \(6+6\);
- three 4-cycles.

`verify.cpp` canonically generates every proper four-colour circuit word
using all four colours on every circuit.  It quotients by the global
affine colour action, the independent dihedral actions, and interchange
of equal-length circuits.  For each word it generates exactly every set
partition satisfying (5), tests dirtiness, and exhausts the component
maps and relative circuit starts.

The exact mutually exclusive counts are:

| shape | canonical words | charge-valid states | dirty states | direct clean | direct failure, delete succeeds | dichotomy failures |
|:---:|---:|---:|---:|---:|---:|---:|
| 12 | 1,014 | 14,196,654 | 11,465,978 | 11,465,978 | 0 | 0 |
| 4+8 | 66 | 922,048 | 773,721 | 773,717 | 4 | 0 |
| 5+7 | 64 | 884,604 | 738,969 | 738,763 | 206 | 0 |
| 6+6 | 66 | 926,640 | 774,196 | 774,014 | 182 | 0 |
| 4+4+4 | 3 | 41,975 | 35,960 | 35,960 | 0 | 0 |

All \(392\) direct-clean failures therefore contradict global
minimality by strict circuit deletion.  This proves the size-twelve
step and hence the theorem.

## 3. Literal certificates and orbit coverage

The frozen `size12-census.txt` contains:

- all 392 literal direct-clean failures;
- for each, the original circuit words and component partition;
- one map \(L_a\) for every component;
- the integrated zero-start word on every circuit;
- a circuit whose integrated word omits a displayed affine colour;
- the missing colour, whose use as the circuit translation makes every
  low value on that circuit nonzero;
- the exact summary counts.

The 392 states form 294 orbits under the full word/partition action:

| shape | literal states | canonical pair orbits |
|:---:|---:|---:|
| 4+8 | 4 | 2 |
| 5+7 | 206 | 188 |
| 6+6 | 182 | 104 |

`verify_output.py` independently parses every frozen certificate,
rechecks the charge equations, dirtiness, all component maps, cyclic
recurrences, omitted colour, nonzero translated circuit, counts, and
orbit totals.  It also rejects any `COUNTERSTATE` line.

The C++ enumeration is exact rather than graph sampling.  The word
quotient is used only to reduce equivalent colour words; every
transported set partition is still enumerated.

## 4. Reproduction

Run:

```sh
clang++ -std=c++20 -O3 -DNDEBUG verify.cpp -o verify
./verify regenerated-size12-census.txt
cmp regenerated-size12-census.txt size12-census.txt
python3 verify_output.py
shasum -a 256 -c SHA256SUMS
```

The reference census took about 26 seconds on an Apple Silicon
workstation.  The frozen output has 742 lines and includes progress
records so an interrupted replay is auditable.

## Scope and disclosure

The theorem assumes a connected loopless cubic graph.  Parallel edges
are allowed; loops require separate conventions and are outside the
statement.  This work has not received independent human peer review.

OpenAI Codex agents under human direction proposed the clean-or-delete
dichotomy, discovered the size-twelve certificates, implemented the
independent verifiers, and prepared this proof.  All finite proof data
are included so the result can be checked without trusting an
AI-generated summary.  No literature-wide priority claim is made, and
FiveCDC remains unresolved.
