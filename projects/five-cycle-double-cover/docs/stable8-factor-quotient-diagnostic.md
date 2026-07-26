# Stable-eight factor-quotient diagnostic

Date: **2026-07-26**.

Status: **exact finite diagnostic / retained marked support remains
nonpacking / no five-CDC conclusion**.

This note records an exact test of the factor-quotient route on the
retained order-\(60\) universally separated eight-mark core and the first
terminal pairing
\[
 (0,1),(2,3),(4,5),(6,7).
\]
The program and full result are:

- `scratch/stable8_factor_quotient_diagnostic.cpp`;
- `scratch/stable8-factor-quotient-diagnostic-result.json`.

## 1. Construction checked

The program decodes the retained graph6 string, verifies a proper Tait
colouring in which all eight marked edges have colour \(c\), subdivides
the marks, and adds the four pairing edges.  It directly checks that the
ambient expansion is a connected simple cubic graph with \(68\) vertices
and \(102\) edges and that the four new edges form a matching \(M\).

Deleting \(M\) leaves \(98\) edges.  The lifted \(ac\)-factor is a
spanning \(2\)-factor with \(68\) edges and component lengths
\[
 17,13,5,9,5,5,9,5.
\]
Each factor circuit contains exactly one terminal.

Contract the eight factor circuits.  The \(30\) complementary
\(b\)-edges form an eight-vertex quotient multigraph \(Q\), with nine
loops.  Each quotient vertex is a terminal vertex for the projected
\(T\)-join problem.

## 2. Exact local lifting criterion

Project a \(T\)-join in \(G-M\) to the complementary \(b\)-edges.  Its
projection is a \(T\)-join in \(Q\).  Conversely, at each contracted
factor circuit, the incident selected quotient ports together with the
terminal form an even set.  There are exactly two complementary parity
paths on the circuit with that boundary, so every single quotient
\(T\)-join lifts.

For two edge-disjoint quotient \(T\)-joins, choose one base parity path
for each.  Every factor edge then has one of four states
\[
 00,\quad 01,\quad 10,\quad 11.
\]
Complementing either base path permutes these four classes.  Therefore
the two quotient joins have edge-disjoint lifts through this factor
circuit if and only if at least one of the four classes is absent.
They are locally obstructed exactly when all four classes occur.  This
criterion is checked independently at every factor circuit.

This gives a human-checkable equivalence:

> two edge-disjoint \(T\)-joins exist in \(G-M\) if and only if an
> edge-disjoint quotient-\(T\)-join pair passes the four-state test on
> every contracted factor circuit.

## 3. Exact counts

The quotient admits
\[
 14\,801\,616\,000
\]
ordered pairs of edge-disjoint quotient \(T\)-joins, or
\[
 7\,400\,808\,000
\]
unordered pairs.  Exactly zero pass all cyclic-port lifting tests.

The large ordered count is obtained twice:

1. a factor-message computation classifies every pair by its exact
   eight-bit local-obstruction mask;
2. an independent pass enumerates all \(2^{23}=8\,388\,608\) possible
   first quotient \(T\)-joins and counts second joins from the binary
   cycle-space dimension of the unused quotient subgraph.

Both computations give \(14\,801\,616\,000\).  All \(8\,388\,608\)
first joins have a \(T\)-even complement.  The complete complement
cycle-dimension and obstruction-mask histograms are retained in the
JSON result.

There are \(128\) nonzero obstruction masks, precisely all masks
containing factor \(0\).  Thus the lifted \(17\)-cycle at factor \(0\)
already obstructs every quotient pair for this colouring, although
additional local obstructions vary freely across all subsets of the
other seven factors.

## 4. Smallest interlacing obstruction

A globally realized obstruction occurs on a lifted \(5\)-cycle at
factor \(2\).  In cyclic order its ports are
\[
 5,\ 1,\ T,\ 6,\ 2,
\]
where \(T\) is the terminal.  For the retained ordered quotient-pair
witness, the two demand sets occupy positions
\[
 \{0,1,2,3\},\qquad \{2,4\}.
\]
Their base parity paths have four-state multiplicities
\[
 (n_{00},n_{01},n_{10},n_{11})=(2,1,1,1).
\]
All four states occur, so none of the four complementary path choices
is edge-disjoint.  This is the smallest possible obstruction in the
displayed lifted factor because its circuit length is five.  The full
quotient edge sets of the witness are in the JSON result.

## 5. Independent full nonpacking comparison

The program separately solves the core cycle-space equations with all
eight marks present.  The equation rank is \(67\), leaving affine
dimension \(23\).  It enumerates all
\[
 2^{23}=8\,388\,608
\]
cycles and finds zero whose every circuit component contains an even
number of marks.  The complete marked-component-profile histogram is
retained.

Thus the two independent outcomes agree exactly:
\[
 \#\{\text{fully liftable quotient pairs}\}=0
 =\#\{\text{all-mark cycles even componentwise}\}.
\]
This confirms the known nonpacking result for the specified size-four
support.  The ambient graph itself has a standard five-cycle double
cover and smaller exact-zero supports, so this is not a counterexample
to five-CDC.

## 6. Alternate-colouring and paired-cut scope

An exact fixed-mark perfect-matching enumeration finds:

- \(40\) possible \(c\)-colour perfect matchings containing all marks;
- \(192\) raw all-\(c\) Tait colourings;
- \(96\) such colourings modulo swapping \(a\) and \(b\);
- \(32\) \(c\)-matchings with complementary profile \(8+52\);
- \(8\) with complementary profile \(8+8+44\).

The independent paired-cut audit still has zero surviving pairings among
all \(105\) possibilities: its minimum-score histogram is
\[
 2:27,\qquad 3:78.
\]
Consequently there is no paired-cut-qualified alternate
pairing/colouring case on this retained core to test.  The diagnostic
does not extrapolate from the first colouring to a hypothetical
high-girth, paired-cut-qualified core.

## 7. Reproduction

From the project root:

```sh
clang++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic \
  scratch/stable8_factor_quotient_diagnostic.cpp \
  -o /tmp/stable8_factor_quotient_diagnostic

/tmp/stable8_factor_quotient_diagnostic \
  --output scratch/stable8-factor-quotient-diagnostic-result.json

python3 -B scratch/audit_stable8_paired_cuts_cleanroom.py
```

The retained files have SHA-256 digests:

```text
ce3f172b2c2529c8d018707cf8ed8ea6f91c75fdd70137fe28ad5dfd22313b73  scratch/stable8_factor_quotient_diagnostic.cpp
4a2be7f9455ea3258df2d08055e988eef382b703abd5006888059912a52f41f4  scratch/stable8-factor-quotient-diagnostic-result.json
aef39f3393cbace4e94798c9bbf6055aa9d5063673625b6e06f2a9cad33e20fd  scratch/stable8-paired-cut-result.json
```

## AI-use disclosure

This diagnostic, implementation, and explanatory note were produced by
an OpenAI Codex agent under human direction.  The mathematical lifting
criterion is stated explicitly, the aggregate count is obtained by two
different exact methods, and the original nonpacking condition is
re-enumerated independently so that the result can be checked without
trusting an unsupported agent conclusion.
