# Minimum extendable projections through size fourteen are cleanable

Date: 2026-07-29

Status: **HUMAN-CHECKABLE KEMPE REDUCTION WITH EXACT FINITE
CERTIFICATES / CUBIC GRAPHS ONLY / NOT A FIVE-CYCLE-DOUBLE-COVER
RESOLUTION**.

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
> at most fourteen is cleanable.

The sibling packages through size thirteen supply the earlier steps.
This package proves the new size-fourteen step.  It does not bound the
minimum support in general, does not reduce arbitrary higher-degree
graphs to cubic graphs, and does not resolve FiveCDC.

## 1. Boundary census

The minimum-projection exchange theorem implies that every circuit
component of a nonzero globally minimum projection contains all four
affine classes \(M_c\), and therefore has length at least four.  The
complete support-shape list at total size fourteen is
\[
\begin{gathered}
14,\quad 4+10,\quad 5+9,\quad 6+8,\quad 7+7,\\
4+4+6,\quad 4+5+5.                                      \tag{4}
\end{gathered}
\]

For a circuit word \(c_i=s(e_i)\), put
\[
                         d_i=c_{i-1}+c_i.                 \tag{5}
\]
If \(\pi_i\) names the component of \(G-h\) incident with the circuit
vertex between \(e_{i-1}\) and \(e_i\), low-flow conservation gives
\[
                    \mathop{\mathbin\oplus}_{\pi_i=a}d_i=0
                    \quad\hbox{for every block }a.        \tag{6}
\]

`verify.cpp` canonically generates every proper four-colour circuit
word using all four colours on every circuit.  It quotients only by
the global affine colour action, independent dihedral circuit actions,
and interchange of equal-length circuits.  For every word it generates
exactly every set partition satisfying (6), tests dirtiness, and
exhausts the componentwise \(\operatorname{GL}(2,2)\) maps and relative
circuit starts.

The exact mutually exclusive counts are:

| shape | canonical words | charge-valid states | dirty states | direct clean | direct failure, delete succeeds | residual |
|:---:|---:|---:|---:|---:|---:|---:|
| 4+4+6 | 22 | 6,078,286 | 5,408,156 | 5,408,156 | 0 | 0 |
| 4+5+5 | 14 | 3,831,414 | 3,401,666 | 3,401,596 | 70 | 0 |
| 4+10 | 416 | 114,769,776 | 100,736,602 | 100,735,166 | 1,436 | 0 |
| 5+9 | 505 | 138,260,253 | 121,073,174 | 121,032,843 | 40,331 | 0 |
| 6+8 | 809 | 223,526,053 | 195,911,662 | 195,844,374 | 67,288 | 0 |
| 7+7 | 333 | 91,481,505 | 80,104,020 | 80,066,557 | 37,239 | 224 |
| 14 | 7,382 | 2,038,187,702 | 1,748,842,896 | 1,748,842,896 | 0 | 0 |
| **total** | **9,481** | **2,616,134,989** | **2,255,478,176** | **2,255,331,588** | **146,364** | **224** |

A deletion row has an integrated low word omitting a colour on one
support circuit.  Translating that circuit by the omitted colour and
removing it from the first-coordinate support gives a strictly smaller
extendable projection.  Thus neither a deletion row nor a residual with
a later strict-deletion escape can represent a global minimum.

Two independently written full \(7+7\) enumerators agree on 333 word
orbits, 91,481,505 charge-valid states, 80,104,020 dirty states,
37,463 direct failures, and the same 224 residual rows.  The independent
package freezes the sorted residual-row digest.  Only the \(7+7\) branch
has an independently implemented full state census.  For the other six
shapes---\(14\), \(4+10\), \(5+9\), \(6+8\), \(4+4+6\), and
\(4+5+5\)---the word-orbit counts, charge-valid partition counts, and all
direct-clean/delete decisions currently rest on the primary classifier.

## 2. Kempe escape from every residual

All 224 residuals have shape \(7+7\).  Their complement-component size
profiles are
\[
\begin{array}{c|r}
6+2+2+2+2&46\\
4+4+2+2+2&178.
\end{array}                                               \tag{7}
\]

Fix two distinct nonzero low colours \(x,y\), and put
\(\Delta=x+y\).  In a complement component \(W\), retain the edges
whose low value is \(x\) or \(y\).  There is a linear functional
\(\ell:K\to\mathbb F_2\) with
\[
                 \ell(x)=\ell(y)=1,\qquad\ell(\Delta)=0.
\]
The low-flow equation makes the retained degree even at every internal
vertex.  Its odd vertices are exactly the split boundary occurrences
whose derivatives lie in \(\{x,y\}\), so those occurrences are paired
by paths.

Interchanging \(x\) and \(y\) on one path preserves every internal
flow equation and adds \(\Delta\) at its two boundary endpoints.  If
the endpoints lie on the same support circuit, integrability is
preserved.  If they lie on different circuits, the certificate names
a second component having exactly two relevant occurrences, one on
each circuit.  Switching its forced path adds a second \(\Delta\) to
both circuit closure equations and restores integrability.

The actual path pairing inside \(W\) is not part of the abstract
boundary state.  A valid certificate must therefore store a set \(S\)
of successful endpoint pairs meeting every possible perfect matching
of the four or six terminals.  The sibling package
`minimum-projection-size14-kempe-escape-20260729/` contains such a
strategy for every residual.  Its 724 literal rows replay:

- the primary endpoints and any auxiliary path;
- all component maps;
- both integrated circuit words;
- a circuit and a colour absent from its word; and
- the resulting strict seven-circuit deletion.

The matching-hitting property makes the certificate independent of the
unknown internal routing.  Consequently every cubic realization of any
residual state has a smaller size-seven extendable projection.  No
residual can be globally minimum.  Together with the direct-clean and
strict-deletion rows, this proves the theorem.

This path argument uses the split-occurrence boundary model, which is
automatic in a cubic realization: every occurrence is a distinct support
vertex with one incident complement edge of low value \(d_i\).  If
several occurrences are identified at a higher-degree vertex, the
complement sees only their xor.  No general reduction from that setting
is claimed.

## 3. Why the sharp counterstate remains valid

The first residual is
```text
word=0101023|0101232
partition=01234444413024
```
and has no direct clean-or-delete map assignment.  Its 18-vertex simple
bridgeless cubic realization has 15,360 ordered extensions of the
displayed projection and none is clean.  This remains a sharp
counterexample to the **unrestricted support-preserving** boundary
dichotomy.

The Kempe escape does not contradict that result.  It first changes the
low flow along one or two complement paths and only then applies
component maps and deletes a circuit.  The same realization has minimum
projection size five, so its displayed size-fourteen projection was
never globally minimum.

## 4. Reproduction

The frozen census was produced by:

```sh
clang++ -std=c++20 -O3 -DNDEBUG verify.cpp -o verify
./verify 4+4+6
./verify 4+5+5
./verify 4+10
./verify 5+9
./verify 6+8
./verify 7+7
```

The expensive one-cycle shape is exactly split into twelve disjoint
canonical-word shards:

```sh
clang++ -std=c++20 -O3 -DNDEBUG verify_sharded.cpp -o verify_sharded
for shard in 0 1 2 3 4 5 6 7 8 9 10 11; do
  ./verify_sharded 14 "$shard" 12 > "single14-shard12-$shard.txt"
done
```

Check the frozen summaries, their literal link to the 224-row Kempe
certificate, and all hashes with:

```sh
python3 verify_summary.py
shasum -a 256 -c SHA256SUMS
```

## Scope and disclosure

The theorem assumes a connected bridgeless loopless cubic graph.
Parallel edges are allowed; loops and arbitrary higher-degree vertices
require separate conventions and reductions.  The boundary theorem is a
computational theorem with a human-checkable Kempe implication.  It has
not received independent human peer review.

OpenAI Codex agents under human direction proposed the clean-or-delete
and Kempe reductions, performed the exact censuses, implemented the
certificate checkers, and prepared this proof package.  The finite claims
are exposed as replayable source, outputs, certificates, and hashes so
that they can be checked without trusting an AI-generated summary.  No
literature-wide priority claim is made, and FiveCDC remains unresolved.
