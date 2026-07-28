# The terminal-\(\chi\), component-chain lexicographic target

Date: **2026-07-28**

Status: **COMPLETE FINITE CENSUS THROUGH ORDER 14 / SHARP HUMAN
PROOF TARGET / NOT A FIVECDC RESOLUTION**.

## 1. Two potentials which fit together

For a \(D_5\)-flow \(q\) on a cubic graph with \(n\) vertices, write
\[
 C_i(q)=\{e:i\in q(e)\},\qquad
 \chi(q)=\sum_{i=0}^4\kappa(C_i(q))-\frac n2.
\]
This is the Euler characteristic of the normalized properly
5-coloured surface dual to \(G\).

Let \(\mathcal K(q)\) be the family of all circuit components of all ten
factors \(Y_{ij}=C_i\triangle C_j\).  For root edges \(r,s\), let
\(d_q(r,s)\) be the least number of members of \(\mathcal K(q)\) in an
intersection chain from \(r\) to \(s\).  Then
\[
 d_q(r,s)=1
 \quad\Longleftrightarrow\quad
 q\text{ is root-good for }r,s.                                \tag{1}
\]

A **terminal \(\chi\)-plateau** is a connected component of the graph
of equal-\(\chi\) Kempe moves with no outgoing \(\chi\)-increasing move.
Inside one such plateau \(T\), fix \(r,s\) and a value \(d>1\).  A
**fixed-\(d\) subplateau** is a connected component of
\[
                         \{q\in T:d_q(r,s)=d\}
\]
under equal-\(\chi\), equal-\(d\) moves.

The exact lexicographic theorem suggested by all current data is:

> **Terminal-\(\chi\) chain theorem.**  Every fixed-\(d>1\) subplateau
> in a terminal \(\chi\)-plateau has an equal-\(\chi\) Kempe edge to a
> state of smaller component-chain distance.

This is a lexicographic \((\chi,-d)\) statement with plateaus allowed
at both levels.  If true, repeated descent reaches \(d=1\), and (1)
proves every terminal \(\chi\)-plateau root-universal.  It therefore
implies the earlier terminal surface-Euler plateau theorem.

## 2. Complete order-14 result

Across all 480 biconnected simple cubic graphs on 14 vertices:

| quantity | count |
|---|---:|
| normalized \(D_5\)-flows | 537,418 |
| terminal \(\chi\)-plateaus | 33,598 |
| terminal-\(\chi\), fixed-\(d>1\) subplateaus | 642,167 |
| maximum component-chain distance | 3 |
| failing fixed-\(d\) subplateaus | **0** |

The full machine-readable report is

```text
scratch/d5-terminal-chi-chain-lex-order14.jsonl
```

An independently written Python implementation gives, through order 12,

| quantity | count |
|---|---:|
| terminal \(\chi\)-plateaus | 2,659 |
| fixed-\(d>1\) subplateaus | 33,610 |
| failures | **0** |

The C++ implementation reproduces those order-12 totals exactly before
running the order-14 census.

The Python source is

```text
scratch/audit_d5_terminal_chi_chain_lex_order12.py
```

## 3. Exact Euler change under a pivot

Let \(K\) be one component of \(Y_{ij}\), and switch \(i,j\) on \(K\).
Only the two coordinate circuits \(C_i,C_j\) change:
\[
                         C_i'=C_i\triangle K,\qquad
                         C_j'=C_j\triangle K.
\]
Consequently
\[
\Delta\chi(K;i,j)=
 \kappa(C_i\triangle K)+\kappa(C_j\triangle K)
 -\kappa(C_i)-\kappa(C_j).                                    \tag{2}
\]
At a terminal plateau every switch has \(\Delta\chi\le0\), and a legal
plateau move has equality in (2).

The fixed-pair Tait-core formula makes (2) completely finite.  Suppress
degree-two paths in \(C_i\cup C_j\), let
\(m_{10},m_{01},m_{11}\) be its three matching involutions, and let
the switch exchange \(m_{10},m_{01}\) on the vertices of \(K\).  Then
\[
\Delta\chi=
\frac12\left[
z(m'_{10}m_{11})+z(m'_{01}m_{11})
-z(m_{10}m_{11})-z(m_{01}m_{11})
\right].                                                       \tag{3}
\]
Thus a neutral pivot is an exact balance of splits and merges in two
coordinate-link circuit partitions.

For a second switch on a component \(H\) of \(Y_{ab}\) in the new
state, the total change is the sum of two instances of (2), with the
second evaluated after the first:
\[
\begin{split}
\Delta\chi_{\rm total}
={}&\Delta\chi_q(K;i,j)\\
 &+\Delta\chi_{q'}(H;a,b).                                    \tag{4}
\end{split}
\]
When \(\{i,j\}\cap\{a,b\}=\varnothing\), the coordinate-count terms in
(4) are independent and the switches commute.  When the pairs share
one coordinate, the exact factor law
\[
                         Y_{ab}(q')=Y_{ab}(q)\triangle K         \tag{5}
\]
shows where the new remote surgery component comes from.

Equations (2)--(5) are the precise local algebra needed by a human
proof.  Component counts alone do not suffice: in the sharp terminal
order-12 path recorded in
`scratch/d5-terminal-chi-two-stage-pivot-no-go.md`, both neutral
switches leave the entire coordinate-component profile unchanged while
rewiring \(d=2\) to \(d=1\).

## 4. Why simpler label potentials fail

The saturated disjoint normal form gives root-label evolution
\[
                           01\mid24
                 \longrightarrow 12\mid24
                 \longrightarrow 24\mid24
\]
on one exact neutral rescue, suggesting that root-label intersection
might increase monotonically.  That is not a global potential.  A
different terminal state with equal bad labels requires
\[
                           12\mid12
                 \longrightarrow 23\mid12
                 \longrightarrow \text{root-good},
\]
so the intersection first decreases from two to one.

The component-chain distance handles both examples:
\[
                              2,\ 2,\ 1.
\]
This is why the fixed-\(d\) plateau, rather than the root-label
intersection pattern, is the surviving secondary object.

## 5. Exact remaining human lemma

The finite census reduces the proof obligation to a single closed-cage
exclusion:

> Let \(T\) be a terminal \(\chi\)-plateau and let
> \(D\subseteq T\) be a connected fixed-\(d>1\) subplateau for roots
> \(r,s\).  Then some state in \(D\) has a neutral switch to distance
> \(<d\).

The local outside-handle table supplies the moves.  If consecutive
factor circuits in a shortest root chain meet on an edge, two
independent coordinate pairs can reroute either circuit while leaving
the other fixed.  Formula (3) decides whether each rerouting is neutral.
What remains is global: show that a closed collection of wrong-return
interlacement patterns would force either

1. a positive value in (3), contradicting terminality; or
2. a neutral rerouting which shortens the factor-component chain.

The order-14 census proves that no third behavior occurs in any state of
the complete finite range.  It does not replace the required universal
closed-cage argument.

## 6. Reproduction

Compile and run:

```text
clang++ -std=c++17 -O3 -DNDEBUG \
  scratch/audit_d5_terminal_chi_chain_lex.cpp \
  -o /tmp/audit_d5_terminal_chi_chain_lex

/opt/homebrew/bin/geng -Cq -d3 -D3 14 \
  | /tmp/audit_d5_terminal_chi_chain_lex \
  > scratch/d5-terminal-chi-chain-lex-order14.jsonl
```

The producer canonicalizes only by global \(S_5\), reconstructs every
Kempe edge, independently computes \(\chi\) and every factor-component
chain distance, identifies terminal equal-\(\chi\) components, and then
checks every fixed-\(d>1\) component for a neutral descent edge.

The frozen order-14 report is checked against its SHA-256 digest, canonical
`geng` graph order, all per-row failure fields, and all summary arithmetic
by

```text
python3 scratch/verify_d5_terminal_chi_chain_lex_order14_report.py
```

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the
lexicographic target, implemented two independent finite audits, ran the
complete order-14 census, analyzed the exact switch algebra, and drafted
this note.  This is finite evidence and a human proof target, not peer
review and not a resolution of FiveCDC.
