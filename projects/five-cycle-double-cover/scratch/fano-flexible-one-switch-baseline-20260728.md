# Flexible one-switch baseline on the strict snarks through order 18

Date: 2026-07-28

Status: **EXACT FINITE BASELINE / LINE-ONLY VERSION REFUTED /
LINE-OR-OUM DISJUNCTION SURVIVES / NOT A FIVE-CDC RESOLUTION**.

## Why a clean Fano line is sufficient

Let \(\phi:E(G)\to\mathbb F_2^3-\{0\}\) be a flow, let
\(\mu\ne0\), and put \(L=\ker\mu-\{0\}\). In the standard quotient
\[
E_5/\langle\kappa\rangle\cong\mathbb F_2^3,
\]
where \(\kappa\) has weight four, the three quotient classes having two
representatives in
\[
D_5=\{x\in\mathbb F_2^5:|x|=2\}
\]
form \(L\). The other four classes have one forced representative.

For each component of the \(L\)-valued factor, conservation makes the
four forced boundary parities equal. A clean line means these common
parities are all zero, so the forced lift bits extend across every
component. This gives a conserved map \(q:E(G)\to D_5\).

For \(i=1,\ldots,5\), define
\[
C_i=\{e:q(e)_i=1\}.
\]
Conservation makes every \(C_i\) Eulerian, and weight two makes every
edge occur in exactly two \(C_i\). Empty coordinates are permitted.
Thus a clean Fano line alone is sufficient for an ordinary “at most
five” cycle double cover.

A five-colouring of the Oum coordinate co-occurrence graph is a separate
sufficient branch: it merges the supplied eight Eulerian coordinates
into at most five without identifying the two coordinates used by an
edge.

## Exact claim tested

For every normalized nowhere-zero \(\mathbb F_2^3\)-flow on the Petersen
graph and the two Blanuša snarks:

1. test the fixed-line cleaning branch;
2. if that fails, test the Oum merge branch;
3. for each exact Oum-hard remainder, exhaust every nonzero
   \(t\in\mathbb F_2^3\) and every nonempty binary cycle
   \(C\subseteq G-M_t\);
4. switch \(\phi\) by \(t\) on \(C\), and ask whether the result has
   either a clean Fano line or a five-colourable Oum co-occurrence graph.

The binary cycle may be disconnected. Its circuit components can be
switched successively: translation by \(t\) fixes \(M_t\) and never
creates a new \(t\)-edge.

## Universal inclusion lemma for disconnected switches

The use of arbitrary binary cycles removes the avoiding-*circuit*
obstruction completely.

**Lemma.**  Let \(\phi\) be a nowhere-zero
\(\mathbb F_2^3\)-flow, let \(s\ne t\), and let
\(S\subseteq M_s=\phi^{-1}(s)\).  There is a binary cycle
\(Q\subseteq G-M_t\) with \(S\subseteq Q\).

**Proof.**  Put \(H=G-M_t\), and restrict the binary cycle space of
\(H\) to the coordinates in \(S\).  If its image did not contain the
all-ones vector, trace-space duality would give a subset \(T\subseteq S\)
of odd cardinality whose characteristic vector, extended by zero to
the other edges of \(H\), lies in the cut space of \(H\).  Thus
\(T=\delta_H(W)\) for some vertex set \(W\).  Because every edge of
\(T\) has value \(s\), the flow sum across the corresponding cut of
\(G\) is
\[
  (|T|\bmod2)s+(|\delta_G(W)\cap M_t|\bmod2)t.
\]
It must be zero.  But \(|T|\) is odd, so the displayed sum is either
\(s\) or \(s+t\), both nonzero because \(s,t\) are distinct nonzero
vectors.  This contradiction proves that the all-ones trace is
realized by some binary cycle \(Q\) of \(H\). \(\square\)

This lemma needs neither cubicity nor cyclic connectivity.  It does not
produce a connected circuit; the 18-vertex avoiding-circuit
counterexample therefore remains consistent with it.

## Complete counts

The input has one representative of every flow orbit under
\(GL(3,2)\).

| graph | normalized flow orbits | no fixed-line cleaning | initially Oum-hard | post-switch clean line | no post-switch clean line | Oum-only rescue |
|---|---:|---:|---:|---:|---:|---:|
| Petersen | 170 | 0 | 0 | 0 | 0 | 0 |
| first Blanuša | 118,960 | 1,888 | 624 | 608 | 16 | 16 |
| second Blanuša | 119,260 | 2,390 | 332 | 332 | 0 | 0 |
| **total** | **238,390** | **4,278** | **956** | **940** | **16** | **16** |

Consequently:

- the assertion “every Oum-hard flow has one switch to a clean Fano
  line” is false already on a cyclically 4-edge-connected 18-vertex
  snark;
- all 16 exceptions are rescued by a post-switch Oum merge; and
- no countermodel to the **disjunctive** line-or-Oum claim occurs in this
  complete strict-snark baseline.

The first retained line-only exception has flow values

```text
1 2 3 3 4 7 6 2 4 1 7 6 3 5 6 4 5 1 7 2 5 2 3 5 6 2 4
```

in the lexicographic edge order of graph6

```text
Q???C@?GCoOoDO[?CcAO_?k?J??
```

All 537 admissible nonempty binary-cycle switches leave every Fano line
dirty. Switching the cycle mask `8389016` by value \(1\) nevertheless
makes the Oum co-occurrence graph five-colourable.

## Reproduction

Full census:

```bash
python3 scratch/census_fano_flexible_one_switch_snarks.py \
  search/order22-filter-census-20260725/strict-snarks-through18.g6 \
  --output scratch/fano-flexible-one-switch-strict-through18-20260728.json
```

Focused semantic replay:

```bash
python3 scratch/verify_fano_flexible_one_switch_report.py
```

This is a finite theorem on the stated graph and flow corpus. It does not
prove the disjunctive claim for larger cyclically 4-edge-connected snarks,
and it does not resolve FiveCDC.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the flexible
switch test, implemented and ran the normalized-flow census, found the 16
line-only exceptions, checked their Oum rescues, and drafted this report.
The exact implications and finite verification are exposed for human
checking. This is not independent human peer review.
